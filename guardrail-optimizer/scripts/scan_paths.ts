#!/usr/bin/env node
/**
 * Guardrail Optimizer — Path Access Scanner
 *
 * Scans pi session JSONL files and replays each tool call through
 * pi-guardrails' own path-access logic to find outside-cwd paths
 * that would trigger guardrail prompts.
 *
 * Usage:
 *   node --experimental-strip-types scan_paths.ts --sessions ~/.pi/agent/sessions --cwd /path/to/project --limit 100
 *   node --experimental-strip-types scan_paths.ts --sessions ~/.pi/agent/sessions --cwd /path/to/project --global
 */

import { resolve, join, relative, isAbsolute } from "node:path";
import { homedir } from "node:os";
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";

// ─── pi-guardrails logic (re-implemented from source) ──────────────────────────
// These mirror pi-guardrails/src/core/paths/path.ts and access.ts.
// We inline them to avoid node_modules TypeScript stripping issues with Node.js.

/** Expand a leading tilde to the current user's home directory. */
function expandHomePath(input: string): string {
  if (input === "~") return homedir();
  if (input.startsWith("~/") || input.startsWith("~\\"))
    return join(homedir(), input.slice(2));
  return input;
}

function resolveFromCwd(input: string, cwd: string): string {
  return resolve(cwd, expandHomePath(input));
}

/**
 * Lexical boundary check. Returns true if targetAbsPath equals rootAbsPath
 * or is a descendant. Both paths must already be resolved (absolute, no ..).
 */
function isWithinBoundary(targetAbsPath: string, rootAbsPath: string): boolean {
  const rel = relative(rootAbsPath, targetAbsPath);
  return rel === "" || (!rel.startsWith("..") && !isAbsolute(rel));
}

// ─── Path access logic ─────────────────────────────────────────────────────────
// Mirrors pi-guardrails/src/core/paths/access.ts

type PathDecision =
  | { kind: "allow" }
  | { kind: "deny"; reason: string }
  | { kind: "ask"; absolutePath: string; displayPath: string };

interface AllowedPath {
  kind: "file" | "directory";
  path: string;
}

interface PathAccessState {
  cwd: string;
  mode: "allow" | "ask" | "block";
  allowedPaths: AllowedPath[];
  hasUI: boolean;
}

function isPathAllowed(absPath: string, allowedPaths: AllowedPath[]): boolean {
  for (const entry of allowedPaths) {
    if (entry.kind === "directory") {
      if (isWithinBoundary(absPath, entry.path)) return true;
    } else {
      if (absPath === entry.path) return true;
    }
  }
  return false;
}

function checkPathAccess(
  absolutePath: string,
  displayPath: string,
  state: PathAccessState,
): PathDecision {
  if (state.mode === "allow") return { kind: "allow" };
  if (isWithinBoundary(absolutePath, state.cwd)) return { kind: "allow" };
  if (isPathAllowed(absolutePath, state.allowedPaths)) return { kind: "allow" };
  if (state.mode === "block") {
    return {
      kind: "deny",
      reason: `Access to ${displayPath} is blocked (outside working directory).`,
    };
  }
  // mode === "ask"
  if (!state.hasUI) {
    return {
      kind: "deny",
      reason: `Access to ${displayPath} is blocked (outside working directory, no UI to confirm).`,
    };
  }
  return { kind: "ask", absolutePath, displayPath };
}

// ─── Bash path candidate extraction ───────────────────────────────────────────
// Mirrors pi-guardrails/src/shared/paths/bash-paths.ts
// We use a simplified regex-based approach (the fallback path in the original).

function maybePathLike(token: string): boolean {
  if (!token) return false;
  if (token.includes("/")) return true;
  if (token.includes("\\")) return true;
  if (/^[A-Za-z]:[\\/]/.test(token)) return true;
  if (/^(?:~|\.{1,2})[\\/]/.test(token)) return true;
  return false;
}

function extractBashPathCandidates(command: string, cwd: string): string[] {
  const seen = new Set<string>();
  const results: string[] = [];

  const tokenRegex = /"([^"]+)"|'([^']+)'|`([^`]+)`|([^\s"'`<>|;&]+)/g;
  for (const match of command.matchAll(tokenRegex)) {
    const token = match[1] ?? match[2] ?? match[3] ?? match[4] ?? "";
    if (token && !token.startsWith("-") && maybePathLike(token)) {
      const abs = resolve(cwd, expandHomePath(token));
      if (!seen.has(abs)) {
        seen.add(abs);
        results.push(abs);
      }
    }
  }
  return results;
}

// ─── targetsForTool ───────────────────────────────────────────────────────────
// Mirrors pi-guardrails/extensions/path-access/targets.ts
async function targetsForTool(
  toolName: string,
  input: Record<string, unknown>,
  cwd: string,
): Promise<string[]> {
  if (["read", "write", "edit", "grep", "find", "ls"].includes(toolName)) {
    const raw = String(input.file_path ?? input.path ?? "").trim();
    return raw ? [resolveFromCwd(raw, cwd)] : [];
  }

  if (toolName === "bash") {
    return extractBashPathCandidates(String(input.command ?? ""), cwd);
  }

  return [];
}

// ─── Types ─────────────────────────────────────────────────────────────────────

interface SessionContext {
  id: string;
  cwd: string;
  heading: string | null;
}

interface OutsidePath {
  path: string;
  frequency: number;
  tools: string[];
  blocked_count: number;
  sessions: SessionContext[];
}

interface ScanResult {
  scope: "project" | "global";
  cwd: string;
  config_path: string;
  existing_allowed_paths: unknown[];
  sessions_scanned: number;
  date_range: { first: string; last: string };
  outside_paths: OutsidePath[];
}

// ─── Session file discovery ────────────────────────────────────────────────────

/**
 * Convert a cwd path to the session directory name format used by pi.
 * e.g., /mnt/disk1/hyx/skills → --mnt-disk1-hyx-skills--
 */
function cwdToSessionDir(cwd: string): string {
  return "--" + cwd.replace(/^\//, "").replace(/\//g, "-") + "--";
}

/**
 * Find session JSONL files for a given scope.
 * Project scope: only the project's session directory.
 * Global scope: all session directories.
 */
function findSessionFiles(
  sessionsDir: string,
  projectCwd: string,
  isGlobal: boolean,
  limit: number,
): string[] {
  const files: { path: string; mtime: number }[] = [];

  if (isGlobal) {
    // Scan all session directories
    const dirs = readdirSync(sessionsDir).filter((d) =>
      statSync(join(sessionsDir, d)).isDirectory(),
    );
    for (const dir of dirs) {
      const dirPath = join(sessionsDir, dir);
      const entries = readdirSync(dirPath);
      for (const entry of entries) {
        if (entry.endsWith(".jsonl")) {
          const fp = join(dirPath, entry);
          try {
            files.push({ path: fp, mtime: statSync(fp).mtimeMs });
          } catch {
            // skip
          }
        }
      }
    }
  } else {
    // Only the project's session directory
    const projectDir = cwdToSessionDir(projectCwd);
    const projectSessionDir = join(sessionsDir, projectDir);
    if (!existsSync(projectSessionDir)) {
      process.stderr.write(`Project session directory not found: ${projectSessionDir}\n`);
      process.stderr.write(`(Looking for sessions with cwd=${projectCwd})\n`);
      return [];
    }
    const entries = readdirSync(projectSessionDir);
    for (const entry of entries) {
      // Some sessions are directories (new format), some are .jsonl files
      const fp = join(projectSessionDir, entry);
      const st = statSync(fp);
      if (entry.endsWith(".jsonl") && st.isFile()) {
        files.push({ path: fp, mtime: st.mtimeMs });
      } else if (st.isDirectory()) {
        // New format: session directory with .jsonl inside
        const subEntries = readdirSync(fp);
        for (const sub of subEntries) {
          if (sub.endsWith(".jsonl")) {
            const subFp = join(fp, sub);
            try {
              files.push({ path: subFp, mtime: statSync(subFp).mtimeMs });
            } catch {
              // skip
            }
          }
        }
      }
    }
  }

  // Sort by modification time, most recent first
  files.sort((a, b) => b.mtime - a.mtime);
  return files.slice(0, limit).map((f) => f.path);
}

// ─── Session parsing ───────────────────────────────────────────────────────────

interface ParsedSession {
  id: string;
  cwd: string;
  heading: string | null;
  toolCalls: { toolName: string; input: Record<string, unknown> }[];
  blockedResults: number;
  firstTs: string | null;
  lastTs: string | null;
}

function parseSession(filepath: string): ParsedSession | null {
  let content: string;
  try {
    content = readFileSync(filepath, "utf-8");
  } catch {
    return null;
  }

  const result: ParsedSession = {
    id: "",
    cwd: "",
    heading: null,
    toolCalls: [],
    blockedResults: 0,
    firstTs: null,
    lastTs: null,
  };

  for (const line of content.split("\n")) {
    if (!line.trim()) continue;
    let entry: Record<string, unknown>;
    try {
      entry = JSON.parse(line);
    } catch {
      continue;
    }

    const etype = entry.type as string;

    // Session info
    if (etype === "session" || etype === "session_info") {
      if (entry.cwd) result.cwd = entry.cwd as string;
      if (entry.id) result.id = entry.id as string;
      continue;
    }

    // Heading — pi stores heading as { topic, goal } in custom events.
    // Achievement events have { topic:"", goal:"", achievement:"..." } — skip those.
    if (etype === "custom" && (entry as Record<string, unknown>).customType === "heading") {
      const data = (entry as Record<string, unknown>).data as Record<string, unknown>;
      const goal = data?.goal as string | undefined;
      // Only set heading from non-empty goal (skip achievement-only entries)
      if (goal && goal.trim()) {
        result.heading = goal.trim();
      }
      continue;
    }

    if (etype !== "message") continue;

    const msg = entry.message as Record<string, unknown>;
    if (!msg) continue;

    const role = msg.role as string;
    const ts = msg.timestamp as number | undefined;
    if (ts) {
      const tsStr = new Date(ts).toISOString();
      if (!result.firstTs) result.firstTs = tsStr;
      result.lastTs = tsStr;
    }

    const content = msg.content;
    if (!Array.isArray(content)) continue;

    if (role === "assistant") {
      for (const block of content) {
        if (!block || typeof block !== "object") continue;
        const b = block as Record<string, unknown>;
        if (b.type === "toolCall") {
          const toolName = b.name as string;
          const args = (b.arguments ?? {}) as Record<string, unknown>;
          const callId = b.id as string;
          result.toolCalls.push({ toolName, input: args });
        }
      }
    } else if (role === "toolResult") {
      const callId = msg.toolCallId as string;
      const isError = msg.isError as boolean;
      if (isError && callId) {
        // Check if error is related to path access
        const contentArr = msg.content;
        let errorText = "";
        if (Array.isArray(contentArr)) {
          for (const block of contentArr) {
            if (block && typeof block === "object" && (block as Record<string, unknown>).type === "text") {
              errorText += (block as Record<string, unknown>).text as string;
            }
          }
        }
        // Path-access blocks say "outside working directory" or "Outside Workspace Access".
        // Avoid matching cc-safety-net errors (which say "BLOCKED by CC Safety Net").
        if (
          errorText.includes("outside working directory") ||
          errorText.includes("Outside Workspace Access") ||
          errorText.includes("denied access outside")
        ) {
          result.blockedResults++;
        }
      }
    }
  }

  return result;
}

// ─── Path access replay ────────────────────────────────────────────────────────

interface PathHit {
  path: string;
  toolName: string;
  blocked: boolean;
}

/**
 * Replay a tool call through pi-guardrails' path-access logic.
 * Returns paths that would trigger a prompt (ask) or be denied.
 */
async function replayToolCall(
  toolName: string,
  input: Record<string, unknown>,
  sessionCwd: string,
): Promise<PathHit[]> {
  const hits: PathHit[] = [];

  // Use pi-guardrails' own targetsForTool to extract target paths
  let targets: string[];
  try {
    targets = await targetsForTool(toolName, input, sessionCwd);
  } catch {
    return hits;
  }

  if (!targets || targets.length === 0) return hits;

  // Simulate path-access check with empty allowedPaths (to find all outside-cwd paths)
  // We use mode "ask" with hasUI true so outside-cwd paths return { kind: "ask" }
  const state = {
    cwd: sessionCwd,
    mode: "ask" as const,
    allowedPaths: [], // empty to catch ALL outside-cwd paths
    hasUI: true,
  };

  for (const absPath of targets) {
    try {
      const displayPath = absPath;
      const decision = checkPathAccess(absPath, displayPath, state);
      if (decision.kind === "ask" || decision.kind === "deny") {
        hits.push({ path: absPath, toolName, blocked: decision.kind === "deny" });
      }
    } catch {
      // skip on error
    }
  }

  return hits;
}

// ─── Guardrail config reading ──────────────────────────────────────────────────

function getGuardrailsConfigPath(projectCwd: string, isGlobal: boolean): string {
  if (isGlobal) {
    return resolve(homedir(), ".pi/agent/extensions/guardrails.json");
  }
  return resolve(projectCwd, ".pi/extensions/guardrails.json");
}

function readExistingAllowedPaths(configPath: string): unknown[] {
  if (!existsSync(configPath)) return [];
  try {
    const raw = readFileSync(configPath, "utf-8");
    const config = JSON.parse(raw);
    const pathAccess = config.pathAccess ?? {};
    return pathAccess.allowedPaths ?? [];
  } catch {
    return [];
  }
}

/**
 * Read allowed paths from BOTH project and global config.
 * In project mode, global config paths also apply (pi-guardrails merges them).
 * Including global paths in existing_allowed_paths prevents recommending
 * entries that are already allowed globally.
 */
function readAllExistingAllowedPaths(
  projectCwd: string,
  isGlobal: boolean,
): { paths: unknown[]; config_path: string } {
  const configPath = getGuardrailsConfigPath(projectCwd, isGlobal);
  let paths = readExistingAllowedPaths(configPath);

  if (!isGlobal) {
    // Also read global config — its allowed paths apply in project mode too
    const globalConfigPath = getGuardrailsConfigPath(projectCwd, true);
    const globalPaths = readExistingAllowedPaths(globalConfigPath);
    paths = [...paths, ...globalPaths];
  }

  return { paths, config_path: configPath };
}

// ─── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  // Parse args
  let sessionsDir = "";
  let projectCwd = "";
  let limit = 100;
  let isGlobal = false;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--sessions") {
      sessionsDir = args[++i];
    } else if (arg === "--cwd") {
      projectCwd = args[++i];
    } else if (arg === "--limit") {
      limit = parseInt(args[++i], 10);
    } else if (arg === "--global" || arg === "-g") {
      isGlobal = true;
    } else if (arg === "--help" || arg === "-h") {
      process.stdout.write(
        "Usage: scan_paths.ts --sessions <dir> --cwd <project_cwd> [--limit N] [--global]\n",
      );
      process.exit(0);
    }
  }

  if (!sessionsDir || !projectCwd) {
    process.stderr.write(
      "Error: --sessions and --cwd are required\n",
    );
    process.exit(1);
  }

  // Expand ~ in sessionsDir
  if (sessionsDir.startsWith("~/")) {
    sessionsDir = resolve(homedir(), sessionsDir.slice(2));
  }

  const configPath = getGuardrailsConfigPath(projectCwd, isGlobal);
  const { paths: existingAllowedPaths, config_path: resolvedConfigPath } =
    readAllExistingAllowedPaths(projectCwd, isGlobal);

  // Find session files
  const sessionFiles = findSessionFiles(sessionsDir, projectCwd, isGlobal, limit);

  if (sessionFiles.length === 0) {
    process.stdout.write(
      JSON.stringify(
        {
          scope: isGlobal ? "global" : "project",
          cwd: projectCwd,
          config_path: resolvedConfigPath,
          existing_allowed_paths: existingAllowedPaths,
          sessions_scanned: 0,
          date_range: { first: null, last: null },
          outside_paths: [],
        },
        null,
        2,
      ) + "\n",
    );
    return;
  }

  // Track outside-cwd path statistics
  const pathStats: Map<
    string,
    {
      frequency: number;
      tools: Set<string>;
      blocked_count: number;
      sessions: Map<string, SessionContext>;
    }
  > = new Map();

  let sessionsScanned = 0;
  let firstTs: string | null = null;
  let lastTs: string | null = null;

  for (const sessionFile of sessionFiles) {
    const session = parseSession(sessionFile);
    if (!session || !session.cwd) continue;

    // In project mode, skip sessions from other projects.
    // In global mode, process ALL sessions — each session's outside-cwd
    // paths are computed relative to that session's own cwd.
    if (!isGlobal && session.cwd !== projectCwd) continue;

    sessionsScanned++;

    if (session.firstTs && (!firstTs || session.firstTs < firstTs)) {
      firstTs = session.firstTs;
    }
    if (session.lastTs && (!lastTs || session.lastTs > lastTs)) {
      lastTs = session.lastTs;
    }

    const sessionCtx: SessionContext = {
      id: session.id,
      cwd: session.cwd,
      heading: session.heading,
    };

    // Replay each tool call
    for (const { toolName, input } of session.toolCalls) {
      const hits = await replayToolCall(toolName, input, session.cwd);

      for (const hit of hits) {
        if (!pathStats.has(hit.path)) {
          pathStats.set(hit.path, {
            frequency: 0,
            tools: new Set(),
            blocked_count: 0,
            sessions: new Map(),
          });
        }

        const stats = pathStats.get(hit.path)!;
        stats.frequency++;
        stats.tools.add(hit.toolName);
        if (hit.blocked) stats.blocked_count++;
        stats.sessions.set(session.id, sessionCtx);
      }
    }
  }

  // Build output
  const outsidePaths: OutsidePath[] = [];
  for (const [path, stats] of pathStats) {
    outsidePaths.push({
      path,
      frequency: stats.frequency,
      tools: [...stats.tools].sort(),
      blocked_count: stats.blocked_count,
      sessions: [...stats.sessions.values()],
    });
  }

  // Sort by frequency descending
  outsidePaths.sort((a, b) => b.frequency - a.frequency);

  const result: ScanResult = {
    scope: isGlobal ? "global" : "project",
    cwd: projectCwd,
    config_path: resolvedConfigPath,
    existing_allowed_paths: existingAllowedPaths,
    sessions_scanned: sessionsScanned,
    date_range: { first: firstTs, last: lastTs },
    outside_paths: outsidePaths,
  };

  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

main().catch((err) => {
  process.stderr.write(`Error: ${err}\n`);
  process.exit(1);
});
