/**
 * Shared session discovery and parsing logic for guardrail-optimizer scanners.
 *
 * Used by scan_commands.ts. scan_paths.ts has its own inline copy for
 * backward compatibility — could be refactored to import from here later.
 */

import { resolve, join, relative, isAbsolute } from "node:path";
import { homedir } from "node:os";
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";

// ─── Types ─────────────────────────────────────────────────────────────────────

export interface SessionContext {
  id: string;
  cwd: string;
  heading: string | null;
}

export interface ToolCallEntry {
  toolName: string;
  input: Record<string, unknown>;
}

export interface ParsedSession {
  id: string;
  cwd: string;
  heading: string | null;
  toolCalls: ToolCallEntry[];
  blockedResults: number;
  firstTs: string | null;
  lastTs: string | null;
}

// ─── Session file discovery ────────────────────────────────────────────────────

/**
 * Convert a cwd path to the session directory name format used by pi.
 * e.g., /mnt/disk1/hyx/skills → --mnt-disk1-hyx-skills--
 */
export function cwdToSessionDir(cwd: string): string {
  return "--" + cwd.replace(/^\//, "").replace(/\//g, "-") + "--";
}

/**
 * Find session JSONL files for a given scope.
 * Project scope: only the project's session directory.
 * Global scope: all session directories.
 */
export function findSessionFiles(
  sessionsDir: string,
  projectCwd: string,
  isGlobal: boolean,
  limit: number,
): string[] {
  const files: { path: string; mtime: number }[] = [];

  if (isGlobal) {
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
    const projectDir = cwdToSessionDir(projectCwd);
    const projectSessionDir = join(sessionsDir, projectDir);
    if (!existsSync(projectSessionDir)) {
      process.stderr.write(`Project session directory not found: ${projectSessionDir}\n`);
      process.stderr.write(`(Looking for sessions with cwd=${projectCwd})\n`);
      return [];
    }
    const entries = readdirSync(projectSessionDir);
    for (const entry of entries) {
      const fp = join(projectSessionDir, entry);
      const st = statSync(fp);
      if (entry.endsWith(".jsonl") && st.isFile()) {
        files.push({ path: fp, mtime: st.mtimeMs });
      } else if (st.isDirectory()) {
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

  files.sort((a, b) => b.mtime - a.mtime);
  return files.slice(0, limit).map((f) => f.path);
}

// ─── Session parsing ───────────────────────────────────────────────────────────

export function parseSession(filepath: string): ParsedSession | null {
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

    if (etype === "session" || etype === "session_info") {
      if (entry.cwd) result.cwd = entry.cwd as string;
      if (entry.id) result.id = entry.id as string;
      continue;
    }

    if (etype === "custom" && (entry as Record<string, unknown>).customType === "heading") {
      const data = (entry as Record<string, unknown>).data as Record<string, unknown>;
      const goal = data?.goal as string | undefined;
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

    const msgContent = msg.content;
    if (!Array.isArray(msgContent)) continue;

    if (role === "assistant") {
      for (const block of msgContent) {
        if (!block || typeof block !== "object") continue;
        const b = block as Record<string, unknown>;
        if (b.type === "toolCall") {
          const toolName = b.name as string;
          const args = (b.arguments ?? {}) as Record<string, unknown>;
          result.toolCalls.push({ toolName, input: args });
        }
      }
    } else if (role === "toolResult") {
      const callId = msg.toolCallId as string;
      const isError = msg.isError as boolean;
      if (isError && callId) {
        const contentArr = msg.content;
        let errorText = "";
        if (Array.isArray(contentArr)) {
          for (const block of contentArr) {
            if (block && typeof block === "object" && (block as Record<string, unknown>).type === "text") {
              errorText += (block as Record<string, unknown>).text as string;
            }
          }
        }
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

// ─── Guardrail config helpers ──────────────────────────────────────────────────

export function getGuardrailsConfigPath(projectCwd: string, isGlobal: boolean): string {
  if (isGlobal) {
    return resolve(homedir(), ".pi/agent/extensions/guardrails.json");
  }
  return resolve(projectCwd, ".pi/extensions/guardrails.json");
}

/**
 * Expand a leading tilde to the current user's home directory.
 */
export function expandHomePath(input: string): string {
  if (input === "~") return homedir();
  if (input.startsWith("~/") || input.startsWith("~\\"))
    return join(homedir(), input.slice(2));
  return input;
}
