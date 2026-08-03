/**
 * session-profile — Core scanning functions
 *
 * PROTOTYPE STUB — validates API shape from #21.
 * Not production code. See https://github.com/peachest/skills/issues/22
 */

// PROTOTYPE PAIN POINT: can't use bare import '@earendil-works/pi-coding-agent'
// because skills/ has no node_modules with it. Real impl needs proper package setup.
import { SessionManager } from "/mnt/disk1/hyx/.nvm/versions/node/v24.15.0/lib/node_modules/@earendil-works/pi-coding-agent/dist/index.js";
import { readFileSync, readdirSync, statSync, existsSync } from "fs";
import { join, extname, isAbsolute } from "path";
import { homedir } from "os";
import type {
  SessionMetrics,
  ScanOptions,
  FileEntry,
} from "./types.ts";

// ── Session scanning ─────────────────────────────────────────────────────────

/**
 * Scan top-level sessions and precompute SessionMetrics for each.
 * Decision from #20: session-level metrics are precomputed during scan.
 * Decision from #21: child sessions are opt-in (--include-children).
 */
export async function scanSessions(options: ScanOptions = {}): Promise<SessionMetrics[]> {
  const { dir, limit, project, includeChildren = false } = options;

  // Use pi's SessionManager.listAll (static async)
  const sessionInfos = await SessionManager.listAll(dir);

  // Apply project filter
  let filtered = sessionInfos;
  if (project) {
    const resolvedProject = resolvePath(project);
    filtered = filtered.filter((s) => s.cwd === resolvedProject);
  }

  // Apply limit
  if (limit && limit > 0) {
    filtered = filtered.slice(0, limit);
  }

  // Compute metrics for each session
  const results: SessionMetrics[] = [];
  for (const info of filtered) {
    try {
      const metrics = computeSessionMetrics(info.path);
      results.push(metrics);
    } catch (e) {
      // Skip broken sessions (prototype: no error handling beyond runnable)
      console.error(`Skip ${info.path}: ${(e as Error).message}`);
    }
  }

  // Optionally include child sessions
  if (includeChildren) {
    // TODO: scan child sessions and append
  }

  return results;
}

/**
 * Scan child sessions for a given parent session ID.
 * Decision from #21: explicit function for child session discovery.
 */
export async function scanChildSessions(
  parentId: string,
  _options: ScanOptions = {},
): Promise<SessionMetrics[]> {
  const sessionsDir = getSessionsDir();
  const results: SessionMetrics[] = [];

  // Walk the sessions directory to find child session dirs
  // Pattern: <sessions-dir>/<cwd-hash-dir>/<timestamp>_<parent-id>/<run-id>/run-<n>/session.jsonl
  function findChildSessions(dir: string) {
    const items = readdirSync(dir);
    for (const item of items) {
      const p = join(dir, item);
      const stat = statSync(p);
      if (stat.isDirectory()) {
        // Check if this dir name contains the parent ID
        if (item.includes(parentId)) {
          // Found the parent session dir — look for run dirs inside
          findRunDirs(p);
        } else {
          // Keep searching
          findChildSessions(p);
        }
      }
    }
  }

  function findRunDirs(parentDir: string) {
    const items = readdirSync(parentDir);
    for (const item of items) {
      const p = join(parentDir, item);
      if (statSync(p).isDirectory()) {
        // This is a run-id dir — look for run-N subdirs
        const runDirs = readdirSync(p).filter((d) => d.startsWith("run-"));
        for (const runDir of runDirs) {
          const sessionFile = join(p, runDir, "session.jsonl");
          if (existsSync(sessionFile)) {
            try {
              const metrics = computeSessionMetrics(sessionFile);
              results.push(metrics);
            } catch {
              // Skip broken child sessions
            }
          }
        }
      }
    }
  }

  findChildSessions(sessionsDir);
  return results;
}

/**
 * Parse a single session file and return raw entries.
 * Decision from #21: expose raw entries via parseSession(), no hook mechanism.
 * Delegates to pi's SessionManager.open().
 */
export function parseSession(filePath: string): FileEntry[] {
  const sm = SessionManager.open(filePath);
  return sm.getEntries();
}

// ── Session-level metrics computation (precomputed) ──────────────────────────

function computeSessionMetrics(filePath: string): SessionMetrics {
  const sm = SessionManager.open(filePath);
  const entries = sm.getEntries();

  // PROTOTYPE PAIN POINT: cwd is NOT in entries — it's on the SessionManager instance.
  // Some sessions have no 'session' header entry (start with model_change instead).
  // Must use sm.cwd, not try to extract from entries.
  let cwd = sm.cwd || "";
  let startTime = 0;
  let endTime = 0;
  let userMessageCount = 0;
  let assistantMessageCount = 0;
  let totalInputTokens = 0;
  let totalOutputTokens = 0;
  let totalCacheReadTokens = 0;
  let totalCacheWriteTokens = 0;
  let totalCost = 0;
  let toolErrors = 0;
  let compactionCount = 0;
  let maxTokensBefore = 0;
  let userInterruptions = 0;

  const toolCounts: Record<string, number> = {};
  const toolErrorCategories: Record<string, number> = {};
  const filesModified = new Set<string>();
  const modelsUsed = new Set<string>();
  const thinkingLevels: string[] = [];
  const messageHours: number[] = [];
  const childSessionIds: string[] = [];

  let usesSubagents = false;
  let usesMcp = false;

  for (const entry of entries) {
    const type = (entry as Record<string, unknown>).type as string;

    if (type === "session") {
      cwd = (entry as Record<string, unknown>).cwd as string;
      continue;
    }

    if (type === "model_change") {
      const mc = entry as Record<string, unknown>;
      const modelId = mc.modelId as string;
      const provider = mc.provider as string;
      modelsUsed.add(`${provider}/${modelId}`);
      continue;
    }

    if (type === "thinking_level_change") {
      const tlc = entry as Record<string, unknown>;
      thinkingLevels.push(tlc.thinkingLevel as string);
      continue;
    }

    if (type === "compaction") {
      compactionCount++;
      const tb = (entry as Record<string, unknown>).tokensBefore as number;
      if (tb > maxTokensBefore) maxTokensBefore = tb;
      continue;
    }

    if (type !== "message") continue;

    const msg = (entry as Record<string, { role?: string; content?: unknown; usage?: Record<string, number>; isError?: boolean; toolName?: string; timestamp?: number | string }>).message;
    if (!msg) continue;

    const role = msg.role;
    const ts = msg.timestamp;
    if (ts) {
      const tsNum = typeof ts === "number" ? ts : new Date(ts).getTime();
      if (startTime === 0 || tsNum < startTime) startTime = tsNum;
      if (tsNum > endTime) endTime = tsNum;
    }

    if (role === "user") {
      userMessageCount++;
      // Hour distribution
      if (ts) {
        const tsNum = typeof ts === "number" ? ts : new Date(ts).getTime();
        messageHours.push(new Date(tsNum).getHours());
      }
      // Interrupt detection
      const content = msg.content;
      if (typeof content === "string" && content.includes("[Request interrupted")) {
        userInterruptions++;
      }
      continue;
    }

    if (role === "assistant") {
      assistantMessageCount++;

      // Usage
      const usage = msg.usage;
      if (usage) {
        totalInputTokens += usage.input || 0;
        totalOutputTokens += usage.output || 0;
        totalCacheReadTokens += usage.cacheRead || 0;
        totalCacheWriteTokens += usage.cacheWrite || 0;
        const cost = usage.cost as Record<string, number> | undefined;
        if (cost) {
          totalCost += cost.total || 0;
        }
      }

      // Tool calls
      const content = msg.content;
      if (Array.isArray(content)) {
        for (const block of content) {
          if (typeof block !== "object" || block === null) continue;
          const b = block as Record<string, unknown>;
          if (b.type === "toolCall") {
            const name = b.name as string;
            toolCounts[name] = (toolCounts[name] || 0) + 1;
            if (name === "subagent") usesSubagents = true;
            if (name === "mcp") usesMcp = true;

            // Track files modified
            const args = b.arguments as Record<string, unknown> | undefined;
            if (args) {
              if (name === "write" && args.path) filesModified.add(args.path as string);
              if (name === "edit" && args.path) filesModified.add(args.path as string);

              // Extract child session IDs from subagent calls
              if (name === "subagent") {
                const id = args.id as string;
                if (id) childSessionIds.push(id);
              }
            }
          }
        }
      }
      continue;
    }

    if (role === "toolResult") {
      if (msg.isError) {
        toolErrors++;
        const tn = msg.toolName || "unknown";
        toolErrorCategories[tn] = (toolErrorCategories[tn] || 0) + 1;
      }
      continue;
    }
  }

  const durationMinutes = endTime > 0 && startTime > 0 ? (endTime - startTime) / 60000 : 0;

  return {
    sessionId: sm.sessionId,
    sessionPath: filePath,
    cwd,
    startTime,
    endTime,
    durationMinutes,
    userMessageCount,
    assistantMessageCount,
    toolCounts,
    toolErrors,
    toolErrorCategories,
    totalInputTokens,
    totalOutputTokens,
    totalCacheReadTokens,
    totalCacheWriteTokens,
    totalCost,
    filesModified: [...filesModified],
    linesAdded: 0, // TODO: needs diff parsing
    linesRemoved: 0,
    languages: inferLanguages(filesModified),
    userInterruptions,
    messageHours,
    usesSubagents,
    usesMcp,
    modelsUsed: [...modelsUsed],
    compactionCount,
    maxTokensBefore,
    thinkingLevels,
    childSessionIds,
  };
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function inferLanguages(files: Set<string>): string[] {
  const extMap: Record<string, string> = {
    ".ts": "typescript",
    ".js": "javascript",
    ".py": "python",
    ".go": "go",
    ".rs": "rust",
    ".md": "markdown",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".sh": "shell",
    ".html": "html",
    ".css": "css",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
  };
  const langs = new Set<string>();
  for (const f of files) {
    const ext = extname(f);
    const lang = extMap[ext];
    if (lang) langs.add(lang);
  }
  return [...langs];
}

function getSessionsDir(): string {
  return join(homedir(), ".pi", "agent", "sessions");
}

function resolvePath(p: string): string {
  if (p.startsWith("~/") || p === "~") {
    return join(homedir(), p.slice(2));
  }
  return isAbsolute(p) ? p : join(process.cwd(), p);
}
