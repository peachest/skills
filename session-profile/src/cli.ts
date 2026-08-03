#!/usr/bin/env node
/**
 * session-profile — CLI
 *
 * PROTOTYPE STUB — validates API shape from #21.
 * Not production code. See https://github.com/peachest/skills/issues/22
 *
 * Usage:
 *   node --experimental-strip-types session-profile/src/cli.ts sessions --limit 10
 *   node --experimental-strip-types session-profile/src/cli.ts tools --limit 100
 *   node --experimental-strip-types session-profile/src/cli.ts usage --limit 100
 *   node --experimental-strip-types session-profile/src/cli.ts trends --limit 100 --bucket daily --days 30
 *   node --experimental-strip-types session-profile/src/cli.ts all --limit 100
 */

import { scanSessions } from "./scan.ts";
import { aggregate } from "./aggregate.ts";

// ── Arg parsing ──────────────────────────────────────────────────────────────

interface ParsedArgs {
  subcommand: string;
  sessions?: string;
  limit?: number;
  project?: string;
  includeChildren?: boolean;
  bucket?: "daily" | "weekly" | "monthly";
  days?: number;
}

function parseArgs(argv: string[]): ParsedArgs {
  const args: ParsedArgs = { subcommand: "" };
  args.subcommand = argv[0] || "help";

  for (let i = 1; i < argv.length; i++) {
    const arg = argv[i];
    const next = argv[i + 1];
    switch (arg) {
      case "--sessions": args.sessions = next; i++; break;
      case "--limit": args.limit = parseInt(next, 10); i++; break;
      case "--project": args.project = next; i++; break;
      case "--include-children": args.includeChildren = true; break;
      case "--bucket": args.bucket = next as "daily" | "weekly" | "monthly"; i++; break;
      case "--days": args.days = parseInt(next, 10); i++; break;
      case "--help": case "-h": args.subcommand = "help"; break;
    }
  }
  return args;
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.subcommand === "help" || !args.subcommand) {
    console.error(`session-profile — pi session analysis base layer

Usage:
  session-profile <subcommand> [flags]

Subcommands:
  sessions    Session-level metrics (precomputed) + totals
  tools       Tool deep profile (bash cmds, file exts, subagent patterns)
  usage       Usage breakdown (per-model tokens/cost, cache hit rate)
  trends      Time trends (daily/weekly buckets, week-over-week, anomalies)
  all         All 5 aggregation categories in one JSON

Common flags:
  --sessions <dir>     Session directory (default: ~/.pi/agent/sessions)
  --limit <N>          Only scan recent N sessions
  --project <path>     Filter by cwd
  --include-children   Include child sessions (default: off)

Trends flags:
  --bucket <type>      daily | weekly | monthly (default: weekly)
  --days <N>           Time range in days (default: 30)

Output: JSON to stdout`);
    process.exit(0);
  }

  const sessions = await scanSessions({
    dir: args.sessions,
    limit: args.limit,
    project: args.project,
    includeChildren: args.includeChildren,
  });

  let result: unknown;

  switch (args.subcommand) {
    case "sessions": {
      result = { sessions, totals: aggregate.crossSession(sessions).totals };
      break;
    }
    case "tools": {
      result = aggregate.toolProfile(sessions);
      break;
    }
    case "usage": {
      result = aggregate.usageBreakdown(sessions);
      break;
    }
    case "trends": {
      result = aggregate.timeTrends(sessions, {
        bucket: args.bucket,
        days: args.days,
      });
      break;
    }
    case "all": {
      const crossSession = aggregate.crossSession(sessions);
      result = {
        sessions,
        crossSession,
        tools: aggregate.toolProfile(sessions),
        usage: aggregate.usageBreakdown(sessions),
        trends: aggregate.timeTrends(sessions, { bucket: args.bucket, days: args.days }),
      };
      if (args.includeChildren) {
        result = { ...(result as Record<string, unknown>), children: await aggregate.childMapping(sessions) };
      }
      break;
    }
    default:
      console.error(`Unknown subcommand: ${args.subcommand}`);
      process.exit(1);
  }

  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

main().catch((e) => {
  console.error("Error:", e);
  process.exit(1);
});
