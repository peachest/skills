/**
 * session-profile — Type definitions
 *
 * PROTOTYPE STUB — validates API shape from #21.
 * Not production code. See https://github.com/peachest/skills/issues/22
 */

// ── Re-export pi's types (decision from #20: reuse, don't redefine) ──────────

// PROTOTYPE: re-export from absolute path. Real impl needs proper package setup.
export type {
  SessionEntry,
  SessionHeader,
  SessionMessageEntry,
  ModelChangeEntry,
  ThinkingLevelChangeEntry,
  CompactionEntry,
  CustomEntry,
  CustomMessageEntry,
  SessionInfo,
  FileEntry,
  BranchSummaryEntry,
} from "/mnt/disk1/hyx/.nvm/versions/node/v24.15.0/lib/node_modules/@earendil-works/pi-coding-agent/dist/index.js";

// ── Aggregate result types (base layer's own value) ──────────────────────────

/** Precomputed per-session metrics (decision from #20: session-level precompute) */
export interface SessionMetrics {
  sessionId: string;
  sessionPath: string;
  cwd: string;
  startTime: number;
  endTime: number;
  durationMinutes: number;

  // Messages
  userMessageCount: number;
  assistantMessageCount: number;

  // Tools
  toolCounts: Record<string, number>;
  toolErrors: number;
  toolErrorCategories: Record<string, number>;

  // Token / Cost
  totalInputTokens: number;
  totalOutputTokens: number;
  totalCacheReadTokens: number;
  totalCacheWriteTokens: number;
  totalCost: number;

  // Code output
  filesModified: string[];
  linesAdded: number;
  linesRemoved: number;
  languages: string[];

  // User behavior
  userInterruptions: number;
  messageHours: number[];

  // Feature usage
  usesSubagents: boolean;
  usesMcp: boolean;

  // Models
  modelsUsed: string[];

  // Context health
  compactionCount: number;
  maxTokensBefore: number;

  // Thinking
  thinkingLevels: string[];

  // Child sessions (IDs only — not scanned by default, decision from #21)
  childSessionIds: string[];
}

/** Cross-session aggregate (lazy, decision from #20) */
export interface CrossSessionMetrics {
  toolFrequencyRanking: Array<{
    tool: string;
    totalCalls: number;
    sessionCount: number;
    errorRate: number;
  }>;
  projectDistribution: Array<{
    cwd: string;
    sessionCount: number;
    totalTokens: number;
    totalCost: number;
  }>;
  modelUsageBreakdown: Array<{
    model: string;
    inputTokens: number;
    outputTokens: number;
    cost: number;
    sessionCount: number;
  }>;
  totals: {
    totalSessions: number;
    totalUserMessages: number;
    totalAssistantMessages: number;
    totalInputTokens: number;
    totalOutputTokens: number;
    totalCacheReadTokens: number;
    totalCost: number;
    totalToolErrors: number;
    activeDays: number;
    dateRange: { start: string; end: string };
  };
}

/** Tool deep profile (lazy) */
export interface ToolProfile {
  toolFrequencyRanking: Array<{
    tool: string;
    totalCalls: number;
    sessionCount: number;
    errorRate: number;
  }>;
  bashCommandTypes: Record<string, number>;
  writeFileExtensions: Record<string, number>;
  editFileExtensions: Record<string, number>;
  readPathTypes: Record<string, number>;
  toolArgKeyProfiles: Record<string, Record<string, number>>;
  subagentPatterns: {
    modeDistribution: Record<string, number>;
    agentDistribution: Record<string, number>;
    asyncVsSync: { async: number; sync: number };
    advancedFeatureAdoption: {
      worktree: number;
      turnBudget: number;
      toolBudget: number;
      acceptance: number;
      skill: number;
      modelOverride: number;
    };
  };
}

/** Usage breakdown (lazy) */
export interface UsageBreakdown {
  byModel: Array<{
    model: string;
    inputTokens: number;
    outputTokens: number;
    cacheReadTokens: number;
    cacheWriteTokens: number;
    cost: number;
    sessionCount: number;
  }>;
  cacheHitRate: number;
  costPerTokenByModel: Record<string, number>;
}

/** Time trends (lazy) */
export interface TimeTrends {
  dailyBuckets: Array<{
    date: string;
    sessionCount: number;
    totalTokens: number;
    totalCost: number;
    toolCalls: number;
  }>;
  weeklyBuckets: Array<{
    weekStart: string;
    sessionCount: number;
    avgCost: number;
    avgErrors: number;
  }>;
  weekOverWeekDiff: {
    sessions: number;
    avgCost: number;
    errorsPerSession: number;
    primaryModel: string;
  } | null;
  trajectory: {
    cost: "increasing" | "decreasing" | "stable";
    errors: "increasing" | "decreasing" | "stable";
  };
  anomalies: Array<{
    sessionId: string;
    type: "cost_spike" | "error_spike";
    severity: number;
  }>;
  decayWeightedAverages: {
    avgCost: number;
    avgErrors: number;
    avgDuration: number;
  };
}

/** Child session mapping (base layer unique) */
export interface ChildSessionMapping {
  parentId: string;
  children: Array<{
    sessionId: string;
    runId: string;
    runIndex: number;
    metrics: SessionMetrics;
  }>;
}

// ── Function option types ────────────────────────────────────────────────────

export interface ScanOptions {
  dir?: string;
  limit?: number;
  project?: string;
  includeChildren?: boolean;
}

export interface TimeTrendsOptions {
  bucket?: "daily" | "weekly" | "monthly";
  days?: number;
}
