/**
 * session-profile — Public API entry point
 *
 * PROTOTYPE STUB — validates API shape from #21.
 * Not production code. See https://github.com/peachest/skills/issues/22
 *
 * Library import (decision from #21):
 *   import { scanSessions, aggregate, parseSession } from 'session-profile';
 */

export { scanSessions, scanChildSessions, parseSession } from "./scan.ts";
export { aggregate } from "./aggregate.ts";

export type {
  SessionMetrics,
  CrossSessionMetrics,
  ToolProfile,
  UsageBreakdown,
  TimeTrends,
  TimeTrendsOptions,
  ChildSessionMapping,
  ScanOptions,
} from "./types.ts";
