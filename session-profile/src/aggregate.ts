/**
 * session-profile — Aggregation functions
 *
 * PROTOTYPE STUB — validates API shape from #21.
 * Not production code. See https://github.com/peachest/skills/issues/22
 *
 * Decision from #20: all aggregations are lazy (computed on demand).
 * Decision from #21: pure functions, no state, no cache.
 */

import type {
  SessionMetrics,
  CrossSessionMetrics,
  ToolProfile,
  UsageBreakdown,
  TimeTrends,
  TimeTrendsOptions,
  ChildSessionMapping,
} from "./types.ts";
import { extname, isAbsolute } from "path";
import { scanChildSessions } from "./scan.ts";
import { parseSession } from "./scan.ts";

// ── Cross-session aggregation ────────────────────────────────────────────────

export function crossSession(sessions: SessionMetrics[]): CrossSessionMetrics {
  // Tool frequency ranking
  const toolTotals: Record<string, number> = {};
  const toolSessionCount: Record<string, Set<string>> = {};
  const toolErrorCounts: Record<string, number> = {};

  for (const s of sessions) {
    for (const [tool, count] of Object.entries(s.toolCounts)) {
      toolTotals[tool] = (toolTotals[tool] || 0) + count;
      if (!toolSessionCount[tool]) toolSessionCount[tool] = new Set();
      toolSessionCount[tool].add(s.sessionId);
    }
    for (const [tool, errors] of Object.entries(s.toolErrorCategories)) {
      toolErrorCounts[tool] = (toolErrorCounts[tool] || 0) + errors;
    }
  }

  const toolFrequencyRanking = Object.entries(toolTotals)
    .map(([tool, totalCalls]) => ({
      tool,
      totalCalls,
      sessionCount: toolSessionCount[tool]?.size || 0,
      errorRate: totalCalls > 0 ? (toolErrorCounts[tool] || 0) / totalCalls : 0,
    }))
    .sort((a, b) => b.totalCalls - a.totalCalls);

  // Project distribution
  const projectMap: Record<string, { sessionCount: number; totalTokens: number; totalCost: number }> = {};
  for (const s of sessions) {
    if (!projectMap[s.cwd]) projectMap[s.cwd] = { sessionCount: 0, totalTokens: 0, totalCost: 0 };
    projectMap[s.cwd].sessionCount++;
    projectMap[s.cwd].totalTokens += s.totalInputTokens + s.totalOutputTokens;
    projectMap[s.cwd].totalCost += s.totalCost;
  }
  const projectDistribution = Object.entries(projectMap)
    .map(([cwd, v]) => ({ cwd, ...v }))
    .sort((a, b) => b.sessionCount - a.sessionCount);

  // Model usage breakdown
  const modelMap: Record<string, { inputTokens: number; outputTokens: number; cost: number; sessions: Set<string> }> = {};
  for (const s of sessions) {
    for (const model of s.modelsUsed) {
      if (!modelMap[model]) modelMap[model] = { inputTokens: 0, outputTokens: 0, cost: 0, sessions: new Set() };
      modelMap[model].inputTokens += s.totalInputTokens;
      modelMap[model].outputTokens += s.totalOutputTokens;
      modelMap[model].cost += s.totalCost;
      modelMap[model].sessions.add(s.sessionId);
    }
  }
  const modelUsageBreakdown = Object.entries(modelMap)
    .map(([model, v]) => ({
      model,
      inputTokens: v.inputTokens,
      outputTokens: v.outputTokens,
      cost: v.cost,
      sessionCount: v.sessions.size,
    }))
    .sort((a, b) => b.cost - a.cost);

  // Totals
  const dates = sessions
    .filter((s) => s.startTime > 0)
    .map((s) => new Date(s.startTime).toISOString().slice(0, 10))
    .sort();
  const uniqueDates = [...new Set(dates)];

  return {
    toolFrequencyRanking,
    projectDistribution,
    modelUsageBreakdown,
    totals: {
      totalSessions: sessions.length,
      totalUserMessages: sessions.reduce((sum, s) => sum + s.userMessageCount, 0),
      totalAssistantMessages: sessions.reduce((sum, s) => sum + s.assistantMessageCount, 0),
      totalInputTokens: sessions.reduce((sum, s) => sum + s.totalInputTokens, 0),
      totalOutputTokens: sessions.reduce((sum, s) => sum + s.totalOutputTokens, 0),
      totalCacheReadTokens: sessions.reduce((sum, s) => sum + s.totalCacheReadTokens, 0),
      totalCost: sessions.reduce((sum, s) => sum + s.totalCost, 0),
      totalToolErrors: sessions.reduce((sum, s) => sum + s.toolErrors, 0),
      activeDays: uniqueDates.length,
      dateRange: uniqueDates.length > 0 ? { start: uniqueDates[0], end: uniqueDates[uniqueDates.length - 1] } : { start: "", end: "" },
    },
  };
}

// ── Tool deep profile ────────────────────────────────────────────────────────

export function toolProfile(sessions: SessionMetrics[]): ToolProfile {
  // Reuse cross-session tool ranking
  const cross = crossSession(sessions);

  // Tool arg key profiles — needs re-reading raw entries
  // For prototype: only compute from what's in SessionMetrics
  const bashCommandTypes: Record<string, number> = {};
  const writeFileExtensions: Record<string, number> = {};
  const editFileExtensions: Record<string, number> = {};
  const readPathTypes: Record<string, number> = {};
  const toolArgKeyProfiles: Record<string, Record<string, number>> = {};

  // Subagent patterns
  const modeDistribution: Record<string, number> = {};
  const agentDistribution: Record<string, number> = {};
  let asyncCount = 0;
  let syncCount = 0;
  const advancedFeatures = { worktree: 0, turnBudget: 0, toolBudget: 0, acceptance: 0, skill: 0, modelOverride: 0 };

  // For tool deep profile, we need to re-parse sessions to get tool args
  // This demonstrates the "expose raw entries" extension point from #21
  for (const s of sessions) {
    try {
      const entries = parseSession(s.sessionPath);
      for (const entry of entries) {
        if ((entry as Record<string, unknown>).type !== "message") continue;
        const msg = (entry as Record<string, { role?: string; content?: unknown }>).message;
        if (msg?.role !== "assistant") continue;
        const content = msg.content;
        if (!Array.isArray(content)) continue;

        for (const block of content) {
          if (typeof block !== "object" || block === null) continue;
          const b = block as Record<string, unknown>;
          if (b.type !== "toolCall") continue;

          const name = b.name as string;
          const args = (b.arguments || {}) as Record<string, unknown>;

          // Arg key profiles
          if (!toolArgKeyProfiles[name]) toolArgKeyProfiles[name] = {};
          for (const key of Object.keys(args)) {
            toolArgKeyProfiles[name][key] = (toolArgKeyProfiles[name][key] || 0) + 1;
          }

          // bash command type classification
          if (name === "bash") {
            const cmd = String(args.command || "");
            classifyBashCommand(cmd, bashCommandTypes);
          }

          // write/edit file extensions
          if (name === "write" && args.path) {
            const ext = extname(args.path as string) || "no-ext";
            writeFileExtensions[ext] = (writeFileExtensions[ext] || 0) + 1;
          }
          if (name === "edit" && args.path) {
            const ext = extname(args.path as string) || "no-ext";
            editFileExtensions[ext] = (editFileExtensions[ext] || 0) + 1;
          }

          // read path types
          if (name === "read" && args.path) {
            const p = args.path as string;
            if (p.startsWith("~/.pi")) readPathTypes["pi-config"] = (readPathTypes["pi-config"] || 0) + 1;
            else if (isAbsolute(p)) readPathTypes["absolute"] = (readPathTypes["absolute"] || 0) + 1;
            else readPathTypes["relative"] = (readPathTypes["relative"] || 0) + 1;
          }

          // subagent patterns
          if (name === "subagent") {
            let mode = "single";
            if (args.tasks) mode = "parallel";
            else if (args.chain) mode = "chain";
            else if (args.action) mode = "mgmt";
            modeDistribution[mode] = (modeDistribution[mode] || 0) + 1;

            const agent = (args.agent as string) || "?";
            agentDistribution[agent] = (agentDistribution[agent] || 0) + 1;

            if (args.async) asyncCount++;
            else syncCount++;

            if (args.worktree) advancedFeatures.worktree++;
            if (args.turnBudget) advancedFeatures.turnBudget++;
            if (args.toolBudget) advancedFeatures.toolBudget++;
            if (args.acceptance) advancedFeatures.acceptance++;
            if (args.skill) advancedFeatures.skill++;
            if (args.model) advancedFeatures.modelOverride++;
          }
        }
      }
    } catch {
      // Skip sessions that fail to re-parse
    }
  }

  return {
    toolFrequencyRanking: cross.toolFrequencyRanking,
    bashCommandTypes,
    writeFileExtensions,
    editFileExtensions,
    readPathTypes,
    toolArgKeyProfiles,
    subagentPatterns: {
      modeDistribution,
      agentDistribution,
      asyncVsSync: { async: asyncCount, sync: syncCount },
      advancedFeatureAdoption: advancedFeatures,
    },
  };
}

// ── Usage breakdown ──────────────────────────────────────────────────────────

export function usageBreakdown(sessions: SessionMetrics[]): UsageBreakdown {
  const modelMap: Record<string, { inputTokens: number; outputTokens: number; cacheRead: number; cacheWrite: number; cost: number; sessions: Set<string> }> = {};

  for (const s of sessions) {
    for (const model of s.modelsUsed) {
      if (!modelMap[model]) modelMap[model] = { inputTokens: 0, outputTokens: 0, cacheRead: 0, cacheWrite: 0, cost: 0, sessions: new Set() };
      modelMap[model].inputTokens += s.totalInputTokens;
      modelMap[model].outputTokens += s.totalOutputTokens;
      modelMap[model].cacheRead += s.totalCacheReadTokens;
      modelMap[model].cacheWrite += s.totalCacheWriteTokens;
      modelMap[model].cost += s.totalCost;
      modelMap[model].sessions.add(s.sessionId);
    }
  }

  const byModel = Object.entries(modelMap)
    .map(([model, v]) => ({
      model,
      inputTokens: v.inputTokens,
      outputTokens: v.outputTokens,
      cacheReadTokens: v.cacheRead,
      cacheWriteTokens: v.cacheWrite,
      cost: v.cost,
      sessionCount: v.sessions.size,
    }))
    .sort((a, b) => b.cost - a.cost);

  const totalCacheRead = sessions.reduce((sum, s) => sum + s.totalCacheReadTokens, 0);
  const totalInput = sessions.reduce((sum, s) => sum + s.totalInputTokens, 0);
  const totalCacheWrite = sessions.reduce((sum, s) => sum + s.totalCacheWriteTokens, 0);
  const cacheHitRate = totalCacheRead + totalInput + totalCacheWrite > 0
    ? totalCacheRead / (totalCacheRead + totalInput + totalCacheWrite)
    : 0;

  const costPerTokenByModel: Record<string, number> = {};
  for (const m of byModel) {
    const totalTokens = m.inputTokens + m.outputTokens + m.cacheReadTokens;
    costPerTokenByModel[m.model] = totalTokens > 0 ? m.cost / totalTokens : 0;
  }

  return { byModel, cacheHitRate, costPerTokenByModel };
}

// ── Time trends ──────────────────────────────────────────────────────────────

export function timeTrends(sessions: SessionMetrics[], options: TimeTrendsOptions = {}): TimeTrends {
  const { bucket = "weekly", days = 30 } = options;
  const now = Date.now();
  const cutoff = now - days * 86400000;

  const filtered = sessions.filter((s) => s.startTime > cutoff);

  // Daily buckets
  const dailyMap: Record<string, { sessionCount: number; totalTokens: number; totalCost: number; toolCalls: number }> = {};
  for (const s of filtered) {
    const date = new Date(s.startTime).toISOString().slice(0, 10);
    if (!dailyMap[date]) dailyMap[date] = { sessionCount: 0, totalTokens: 0, totalCost: 0, toolCalls: 0 };
    dailyMap[date].sessionCount++;
    dailyMap[date].totalTokens += s.totalInputTokens + s.totalOutputTokens;
    dailyMap[date].totalCost += s.totalCost;
    dailyMap[date].toolCalls += Object.values(s.toolCounts).reduce((a, b) => a + b, 0);
  }
  const dailyBuckets = Object.entries(dailyMap)
    .map(([date, v]) => ({ date, ...v }))
    .sort((a, b) => a.date.localeCompare(b.date));

  // Weekly buckets
  const weeklyMap: Record<string, { sessionCount: number; totalCost: number; totalErrors: number }> = {};
  for (const s of filtered) {
    const d = new Date(s.startTime);
    const weekStart = new Date(d);
    weekStart.setDate(d.getDate() - d.getDay());
    const weekKey = weekStart.toISOString().slice(0, 10);
    if (!weeklyMap[weekKey]) weeklyMap[weekKey] = { sessionCount: 0, totalCost: 0, totalErrors: 0 };
    weeklyMap[weekKey].sessionCount++;
    weeklyMap[weekKey].totalCost += s.totalCost;
    weeklyMap[weekKey].totalErrors += s.toolErrors;
  }
  const weeklyBuckets = Object.entries(weeklyMap)
    .map(([weekStart, v]) => ({
      weekStart,
      sessionCount: v.sessionCount,
      avgCost: v.sessionCount > 0 ? v.totalCost / v.sessionCount : 0,
      avgErrors: v.sessionCount > 0 ? v.totalErrors / v.sessionCount : 0,
    }))
    .sort((a, b) => a.weekStart.localeCompare(b.weekStart));

  // Week-over-week diff
  let weekOverWeekDiff: TimeTrends["weekOverWeekDiff"] = null;
  if (weeklyBuckets.length >= 2) {
    const latest = weeklyBuckets[weeklyBuckets.length - 1];
    const prev = weeklyBuckets[weeklyBuckets.length - 2];
    const modelCounts: Record<string, number> = {};
    for (const s of filtered) {
      const d = new Date(s.startTime);
      const weekStart = new Date(d);
      weekStart.setDate(d.getDate() - d.getDay());
      if (weekStart.toISOString().slice(0, 10) === latest.weekStart) {
        for (const m of s.modelsUsed) modelCounts[m] = (modelCounts[m] || 0) + 1;
      }
    }
    const primaryModel = Object.entries(modelCounts).sort((a, b) => b[1] - a[1])[0]?.[0] || "";
    weekOverWeekDiff = {
      sessions: latest.sessionCount - prev.sessionCount,
      avgCost: latest.avgCost - prev.avgCost,
      errorsPerSession: latest.avgErrors - prev.avgErrors,
      primaryModel,
    };
  }

  // Trajectory detection
  const halfBuckets = Math.floor(dailyBuckets.length / 2);
  const firstHalf = dailyBuckets.slice(0, halfBuckets);
  const secondHalf = dailyBuckets.slice(halfBuckets);
  const firstAvgCost = firstHalf.length > 0 ? firstHalf.reduce((s, b) => s + b.totalCost, 0) / firstHalf.length : 0;
  const secondAvgCost = secondHalf.length > 0 ? secondHalf.reduce((s, b) => s + b.totalCost, 0) / secondHalf.length : 0;
  const firstAvgErrors = firstHalf.length > 0 ? firstHalf.reduce((s, b) => s + b.totalCost, 0) / firstHalf.length : 0;
  const secondAvgErrors = secondHalf.length > 0 ? secondHalf.reduce((s, b) => s + b.totalCost, 0) / secondHalf.length : 0;

  const trajectory = {
    cost: detectTrajectory(firstAvgCost, secondAvgCost),
    errors: detectTrajectory(firstAvgErrors, secondAvgErrors),
  };

  // Anomaly detection (3σ)
  const costs = filtered.map((s) => s.totalCost).filter((c) => c > 0);
  const avgCost = costs.length > 0 ? costs.reduce((a, b) => a + b, 0) / costs.length : 0;
  const stdCost = costs.length > 0 ? Math.sqrt(costs.reduce((s, c) => s + (c - avgCost) ** 2, 0) / costs.length) : 0;
  const anomalies: TimeTrends["anomalies"] = [];
  for (const s of filtered) {
    if (stdCost > 0 && s.totalCost > avgCost + 3 * stdCost) {
      anomalies.push({ sessionId: s.sessionId, type: "cost_spike", severity: (s.totalCost - avgCost) / stdCost });
    }
  }

  // Decay-weighted averages (10-day half-life, from observal)
  const HALF_LIFE_MS = 10 * 86400000;
  const lambda = Math.log(2) / HALF_LIFE_MS;
  let weightSum = 0;
  let weightedCost = 0;
  let weightedErrors = 0;
  let weightedDuration = 0;
  for (const s of filtered) {
    const age = now - s.startTime;
    const weight = Math.exp(-lambda * age);
    weightSum += weight;
    weightedCost += s.totalCost * weight;
    weightedErrors += s.toolErrors * weight;
    weightedDuration += s.durationMinutes * weight;
  }

  return {
    dailyBuckets,
    weeklyBuckets,
    weekOverWeekDiff,
    trajectory,
    anomalies,
    decayWeightedAverages: {
      avgCost: weightSum > 0 ? weightedCost / weightSum : 0,
      avgErrors: weightSum > 0 ? weightedErrors / weightSum : 0,
      avgDuration: weightSum > 0 ? weightedDuration / weightSum : 0,
    },
  };
}

// ── Child session mapping ────────────────────────────────────────────────────

export async function childMapping(sessions: SessionMetrics[]): Promise<ChildSessionMapping[]> {
  const results: ChildSessionMapping[] = [];
  for (const s of sessions) {
    if (s.childSessionIds.length === 0) continue;
    const children = await scanChildSessions(s.sessionId);
    if (children.length > 0) {
      results.push({
        parentId: s.sessionId,
        children: children.map((m, i) => ({
          sessionId: m.sessionId,
          runId: "", // TODO: extract from path
          runIndex: i,
          metrics: m,
        })),
      });
    }
  }
  return results;
}

// ── Aggregate namespace (decision from #21: aggregate.* pattern) ─────────────

export const aggregate = {
  crossSession,
  toolProfile,
  usageBreakdown,
  timeTrends,
  childMapping,
};

// ── Helpers ──────────────────────────────────────────────────────────────────

function classifyBashCommand(cmd: string, counts: Record<string, number>): void {
  const prefixes: [string, string][] = [
    ["git ", "git"], ["npm ", "npm"], ["npx ", "npx"],
    ["python3 ", "python"], ["python ", "python"],
    ["node ", "node"], ["grep ", "grep"], ["find ", "find"],
    ["ls ", "ls"], ["cat ", "cat"], ["echo ", "echo"],
    ["sed ", "sed"], ["awk ", "awk"], ["curl ", "curl"],
    ["gh ", "gh"], ["glab ", "glab"], ["make ", "make"],
    ["kubectl ", "k8s"], ["nerdctl ", "container"], ["docker ", "container"],
  ];
  for (const [prefix, type] of prefixes) {
    if (cmd.startsWith(prefix) || cmd.includes(`\n${prefix}`) || cmd.includes(`; ${prefix}`) || cmd.includes(`&& ${prefix}`)) {
      counts[type] = (counts[type] || 0) + 1;
      return;
    }
  }
  counts["other"] = (counts["other"] || 0) + 1;
}

function detectTrajectory(first: number, second: number): "increasing" | "decreasing" | "stable" {
  if (first === 0 && second === 0) return "stable";
  const ratio = first > 0 ? second / first : second > 0 ? 2 : 0.5;
  if (ratio > 1.2) return "increasing";
  if (ratio < 0.8) return "decreasing";
  return "stable";
}
