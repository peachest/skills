#!/usr/bin/env node
/**
 * Guardrail Optimizer — Command Execution Scanner
 *
 * Scans pi session JSONL files, extracts bash commands, and replays each
 * through pi-guardrails' dangerous-command detection logic to find commands
 * that would trigger permission-gate prompts but aren't yet covered by
 * allowedPatterns.
 *
 * Usage:
 *   node --experimental-strip-types scan_commands.ts --sessions ~/.pi/agent/sessions --cwd /path/to/project --limit 100
 *   node --experimental-strip-types scan_commands.ts --sessions ~/.pi/agent/sessions --cwd /path/to/project --global
 */

import { resolve, join } from "node:path";
import { homedir } from "node:os";
import { readFileSync, existsSync } from "node:fs";
import {
  type SessionContext,
  type ParsedSession,
  findSessionFiles,
  parseSession,
  getGuardrailsConfigPath,
  expandHomePath,
} from "./shared.ts";

// ─── Command tokenization ─────────────────────────────────────────────────────
// Simplified shell command splitter — handles pipes, &&, ||, ; and subshells.
// Not a full AST parser but catches the vast majority of real-world commands.

/**
 * Split a command string into individual sub-commands by shell operators
 * (|, &&, ||, ;, &) while respecting quotes.
 */
function splitCompoundCommands(command: string): string[] {
  const segments: string[] = [];
  let current = "";
  let i = 0;
  let inSingle = false;
  let inDouble = false;
  let inBacktick = false;
  let parenDepth = 0;

  while (i < command.length) {
    const ch = command[i];
    const next = command[i + 1];

    // Handle quote states
    if (ch === "'" && !inDouble && !inBacktick) {
      inSingle = !inSingle;
      current += ch;
      i++;
      continue;
    }
    if (ch === '"' && !inSingle && !inBacktick) {
      inDouble = !inDouble;
      current += ch;
      i++;
      continue;
    }
    if (ch === "`" && !inSingle && !inDouble) {
      inBacktick = !inBacktick;
      current += ch;
      i++;
      continue;
    }

    // Inside quotes — just copy
    if (inSingle || inDouble || inBacktick) {
      // Handle escaped chars inside double quotes
      if (ch === "\\" && inDouble) {
        current += ch + (next ?? "");
        i += 2;
        continue;
      }
      current += ch;
      i++;
      continue;
    }

    // Track $() subshells
    if (ch === "$" && next === "(") {
      parenDepth++;
      current += "$(";
      i += 2;
      continue;
    }
    if (ch === "(" && !inSingle && !inDouble) {
      parenDepth++;
      current += ch;
      i++;
      continue;
    }
    if (ch === ")" && parenDepth > 0) {
      parenDepth--;
      current += ch;
      i++;
      continue;
    }

    // Inside $() or () — don't split
    if (parenDepth > 0) {
      current += ch;
      i++;
      continue;
    }

    // Shell operators
    if (ch === "&" && next === "&") {
      if (current.trim()) segments.push(current.trim());
      current = "";
      i += 2;
      continue;
    }
    if (ch === "|" && next === "|") {
      if (current.trim()) segments.push(current.trim());
      current = "";
      i += 2;
      continue;
    }
    if (ch === "|" || ch === ";") {
      if (current.trim()) segments.push(current.trim());
      current = "";
      i++;
      continue;
    }
    if (ch === "&") {
      // Background operator
      if (current.trim()) segments.push(current.trim());
      current = "";
      i++;
      continue;
    }

    current += ch;
    i++;
  }

  if (current.trim()) segments.push(current.trim());
  return segments;
}

/**
 * Tokenize a command segment into words, respecting quotes.
 * Returns the command words (first word = command name, rest = args).
 */
function tokenizeCommand(segment: string): string[] {
  const words: string[] = [];
  let current = "";
  let i = 0;
  let inSingle = false;
  let inDouble = false;

  while (i < segment.length) {
    const ch = segment[i];

    if (ch === "'" && !inDouble) {
      inSingle = !inSingle;
      i++;
      continue;
    }
    if (ch === '"' && !inSingle) {
      inDouble = !inDouble;
      i++;
      continue;
    }

    if ((inSingle || inDouble) && ch === "\\" ) {
      // Keep escaped char inside quotes
      current += ch + (segment[i + 1] ?? "");
      i += 2;
      continue;
    }

    if (!inSingle && !inDouble && (ch === " " || ch === "\t" || ch === "\n")) {
      if (current) {
        words.push(current);
        current = "";
      }
      i++;
      continue;
    }

    current += ch;
    i++;
  }

  if (current) words.push(current);
  return words;
}

// ─── Dangerous command matchers ───────────────────────────────────────────────
// Re-implemented from pi-guardrails/src/core/commands/dangerous.ts
// Each matcher checks the command words and returns a description if dangerous.

export interface DangerousMatch {
  description: string;
  matcher: string; // which matcher triggered
  words: string[];
}

/** Check if any word starts with a given prefix. */
function hasArg(words: string[], prefix: string): boolean {
  return words.some((w) => w.startsWith(prefix));
}

/** Check if short options contain a specific flag (handles grouped opts like -rf). */
function hasShortFlag(words: string[], flag: string): boolean {
  return words.some(
    (w) =>
      w === `-${flag}` ||
      (w.startsWith("-") && !w.startsWith("--") && w.includes(flag)),
  );
}

/** Check for long options. */
function hasLongOption(words: string[], option: string): boolean {
  return words.some((w) => w === `--${option}`);
}

type Matcher = {
  name: string;
  check: (words: string[]) => string | undefined;
};

const MATCHERS: Matcher[] = [
  // ── File/Directory Destruction ──
  {
    name: "rm-rf",
    check: (w) => {
      if (w[0] !== "rm") return undefined;
      const hasRecursive =
        hasShortFlag(w, "r") || hasShortFlag(w, "R") ||
        hasLongOption(w, "recursive") || hasLongOption(w, "dir");
      const hasForce = hasShortFlag(w, "f") || hasLongOption(w, "force");
      return hasRecursive && hasForce ? "recursive force delete" : undefined;
    },
  },
  {
    name: "shred",
    check: (w) => (w[0] === "shred" ? "secure file overwrite" : undefined),
  },
  // ── Privilege Escalation ──
  {
    name: "sudo",
    check: (w) => (w[0] === "sudo" ? "superuser command" : undefined),
  },
  {
    name: "doas",
    check: (w) => (w[0] === "doas" ? "privileged command execution" : undefined),
  },
  {
    name: "pkexec",
    check: (w) => (w[0] === "pkexec" ? "privileged command execution" : undefined),
  },
  // ── Disk/Filesystem Operations ──
  {
    name: "dd",
    check: (w) => {
      if (w[0] !== "dd") return undefined;
      return hasArg(w, "of=") ? "disk write operation" : undefined;
    },
  },
  {
    name: "mkfs",
    check: (w) => {
      const cmd = w[0];
      if (cmd === "mkfs" || cmd?.startsWith("mkfs.")) return "filesystem format";
      return undefined;
    },
  },
  {
    name: "wipefs",
    check: (w) => (w[0] === "wipefs" ? "filesystem signature wipe" : undefined),
  },
  {
    name: "blkdiscard",
    check: (w) => (w[0] === "blkdiscard" ? "block device discard" : undefined),
  },
  // ── Disk Partitioning ──
  {
    name: "fdisk",
    check: (w) => {
      const cmd = w[0];
      if (cmd === "fdisk" || cmd === "sfdisk" || cmd === "cfdisk")
        return "disk partitioning";
      return undefined;
    },
  },
  {
    name: "parted",
    check: (w) => {
      const cmd = w[0];
      if (cmd === "parted" || cmd === "sgdisk") return "disk partitioning";
      return undefined;
    },
  },
  // ── Permission Changes ──
  {
    name: "chmod-R",
    check: (w) => {
      if (w[0] !== "chmod") return undefined;
      const hasRecursive = hasShortFlag(w, "R") || hasLongOption(w, "recursive");
      const hasWorldWritable = w.some(
        (x) =>
          x === "777" || x === "0777" || x === "a+rwx" || x === "ugo+rwx" ||
          x === "7777" || x === "1777",
      );
      return hasRecursive && hasWorldWritable
        ? "insecure recursive permissions"
        : undefined;
    },
  },
  {
    name: "chown-R",
    check: (w) => {
      if (w[0] !== "chown") return undefined;
      const hasRecursive = hasShortFlag(w, "R") || hasLongOption(w, "recursive");
      return hasRecursive ? "recursive ownership change" : undefined;
    },
  },
  // ── Container Escape ──
  {
    name: "container-escape",
    check: (w) => {
      const cmd = w[0];
      if (!cmd) return undefined;
      const isDocker = cmd === "docker" || cmd === "podman" || cmd === "nerdctl";
      if (!isDocker) return undefined;
      const sub = w[1];
      if (sub !== "run" && sub !== "create") return undefined;
      if (w.some((x) => x === "--privileged" || x.startsWith("--privileged=")))
        return "container with privileged mode";
      if (w.some((x) => x === "--pid=host" || x.startsWith("--pid=host")))
        return "container with host PID namespace";
      if (w.some((x) => x === "--network=host" || x.startsWith("--network=host")))
        return "container with host network";
      if (w.some((x) => x === "--userns=host" || x.startsWith("--userns=host")))
        return "container with host user namespace";
      if (w.some((x) => x === "--uts=host" || x.startsWith("--uts=host")))
        return "container with host UTS namespace";
      if (w.some((x) => x === "--ipc=host" || x.startsWith("--ipc=host")))
        return "container with host IPC";
      if (
        w.some(
          (x) =>
            x.startsWith("-v/:") || x.startsWith("-v/=>") ||
            x.startsWith("--volume=/:") ||
            x.startsWith("--mount=type=bind,source=/,"),
        )
      )
        return "container with root filesystem mount";
      if (
        w.some(
          (x) =>
            x.includes("/var/run/docker.sock") || x.includes("/run/docker.sock") ||
            x.includes("/var/run/podman.sock") || x.includes("/run/podman.sock"),
        )
      )
        return "container with docker socket access";
      return undefined;
    },
  },
];

/**
 * Check a single command (already tokenized) against all dangerous matchers.
 */
function checkDangerous(words: string[]): DangerousMatch | undefined {
  if (words.length === 0) return undefined;
  for (const m of MATCHERS) {
    const desc = m.check(words);
    if (desc) {
      return { description: desc, matcher: m.name, words };
    }
  }
  return undefined;
}

/**
 * Check a full command string (possibly compound) against all dangerous matchers.
 * Splits by shell operators and checks each sub-command.
 */
function checkCommandDangerous(command: string): DangerousMatch[] {
  const segments = splitCompoundCommands(command);
  const matches: DangerousMatch[] = [];
  for (const seg of segments) {
    const words = tokenizeCommand(seg);
    if (words.length === 0) continue;
    const match = checkDangerous(words);
    if (match) {
      matches.push(match);
    }
  }
  return matches;
}

// ─── Pattern compilation (re-implemented from matching.ts) ─────────────────────

interface PatternConfig {
  pattern: string;
  description?: string;
  regex?: boolean;
}

interface CompiledPattern {
  test: (input: string) => boolean;
  source: PatternConfig;
}

function compileCommandPattern(config: PatternConfig): CompiledPattern {
  if (config.regex) {
    try {
      const re = new RegExp(config.pattern);
      return { test: (input) => re.test(input), source: config };
    } catch {
      return { test: () => false, source: config };
    }
  }
  return {
    test: (input) => input.includes(config.pattern),
    source: config,
  };
}

function compileCommandPatterns(configs: PatternConfig[]): CompiledPattern[] {
  return configs.map(compileCommandPattern);
}

/**
 * Check if a command is already allowed by existing patterns.
 */
function isCommandAllowed(command: string, patterns: CompiledPattern[]): boolean {
  return patterns.some((p) => p.test(command));
}

// ─── Config reading ────────────────────────────────────────────────────────────

interface AllowedPatternRaw {
  pattern: string;
  description?: string;
  regex?: boolean;
}

function readExistingAllowedPatterns(configPath: string): AllowedPatternRaw[] {
  if (!existsSync(configPath)) return [];
  try {
    const raw = readFileSync(configPath, "utf-8");
    const config = JSON.parse(raw);
    const gate = config.permissionGate ?? {};
    return gate.allowedPatterns ?? [];
  } catch {
    return [];
  }
}

/**
 * Read allowed patterns from BOTH project and global config.
 * In project mode, global config patterns also apply.
 */
function readAllExistingAllowedPatterns(
  projectCwd: string,
  isGlobal: boolean,
): { patterns: AllowedPatternRaw[]; config_path: string } {
  const configPath = getGuardrailsConfigPath(projectCwd, isGlobal);
  let patterns = readExistingAllowedPatterns(configPath);

  if (!isGlobal) {
    const globalConfigPath = getGuardrailsConfigPath(projectCwd, true);
    const globalPatterns = readExistingAllowedPatterns(globalConfigPath);
    patterns = [...patterns, ...globalPatterns];
  }

  return { patterns, config_path: configPath };
}

// ─── Types for output ──────────────────────────────────────────────────────────

interface DangerousCommandEntry {
  command: string;
  matched_segment: string;
  frequency: number;
  matched_matcher: string;
  matched_description: string;
  sessions: SessionContext[];
  blocked_count: number;
}

interface CommandScanResult {
  scope: "project" | "global";
  cwd: string;
  config_path: string;
  existing_allowed_patterns: AllowedPatternRaw[];
  sessions_scanned: number;
  date_range: { first: string | null; last: string | null };
  dangerous_commands: DangerousCommandEntry[];
}

// ─── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

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
        "Usage: scan_commands.ts --sessions <dir> --cwd <project_cwd> [--limit N] [--global]\n",
      );
      process.exit(0);
    }
  }

  if (!sessionsDir || !projectCwd) {
    process.stderr.write("Error: --sessions and --cwd are required\n");
    process.exit(1);
  }

  if (sessionsDir.startsWith("~/")) {
    sessionsDir = resolve(homedir(), sessionsDir.slice(2));
  }

  const { patterns: existingRaw, config_path: resolvedConfigPath } =
    readAllExistingAllowedPatterns(projectCwd, isGlobal);
  const existingCompiled = compileCommandPatterns(existingRaw);

  const sessionFiles = findSessionFiles(sessionsDir, projectCwd, isGlobal, limit);

  if (sessionFiles.length === 0) {
    process.stdout.write(
      JSON.stringify(
        {
          scope: isGlobal ? "global" : "project",
          cwd: projectCwd,
          config_path: resolvedConfigPath,
          existing_allowed_patterns: existingRaw,
          sessions_scanned: 0,
          date_range: { first: null, last: null },
          dangerous_commands: [],
        } satisfies CommandScanResult,
        null,
        2,
      ) + "\n",
    );
    return;
  }

  // Track dangerous command statistics
  // Key = command string, value = stats
  const cmdStats = new Map<
    string,
    {
      frequency: number;
      matcher: string;
      description: string;
      matchedSegment: string;
      sessions: Map<string, SessionContext>;
      blocked_count: number;
    }
  >();

  let sessionsScanned = 0;
  let firstTs: string | null = null;
  let lastTs: string | null = null;

  for (const sessionFile of sessionFiles) {
    const session = parseSession(sessionFile);
    if (!session || !session.cwd) continue;

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

    for (const { toolName, input } of session.toolCalls) {
      if (toolName !== "bash") continue;
      const command = String(input.command ?? "").trim();
      if (!command) continue;

      // Check if already allowed
      if (isCommandAllowed(command, existingCompiled)) continue;

      // Check if dangerous
      const matches = checkCommandDangerous(command);
      if (matches.length === 0) continue;

      // Use the first match (most significant)
      const match = matches[0];
      const matchedSegment = match.words.join(" ");

      if (!cmdStats.has(command)) {
        cmdStats.set(command, {
          frequency: 0,
          matcher: match.matcher,
          description: match.description,
          matchedSegment,
          sessions: new Map(),
          blocked_count: 0,
        });
      }

      const stats = cmdStats.get(command)!;
      stats.frequency++;
      stats.sessions.set(session.id, sessionCtx);
    }
  }

  // Build output
  const dangerousCommands: DangerousCommandEntry[] = [];
  for (const [command, stats] of cmdStats) {
    dangerousCommands.push({
      command,
      matched_segment: stats.matchedSegment,
      frequency: stats.frequency,
      matched_matcher: stats.matcher,
      matched_description: stats.description,
      sessions: [...stats.sessions.values()],
      blocked_count: stats.blocked_count,
    });
  }

  dangerousCommands.sort((a, b) => b.frequency - a.frequency);

  const result: CommandScanResult = {
    scope: isGlobal ? "global" : "project",
    cwd: projectCwd,
    config_path: resolvedConfigPath,
    existing_allowed_patterns: existingRaw,
    sessions_scanned: sessionsScanned,
    date_range: { first: firstTs, last: lastTs },
    dangerous_commands: dangerousCommands,
  };

  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

main().catch((err) => {
  process.stderr.write(`Error: ${err}\n`);
  process.exit(1);
});
