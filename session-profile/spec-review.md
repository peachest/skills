# Spec #28 Review Report

**Spec**: [#28 — Spec: session-profile base layer implementation](https://github.com/peachest/skills/issues/28)
**Reviewers**: review-spec skill (5-axis interrogation) + prior spec audit (evidence sourcing)
**Verdict**: **Not ready** — 22 gaps across 5 axes

---

## Axis 1 — Evidence

### GAP E1: SubagentSpawnRecord toolResult format covers only 15% of real data

**Spec passage**:
> "The toolResult text format (verified from real sessions):
> ```
> Delivered chain subagent results via intercom.
> Run: 1c276a38
> Children: 2 completed
> Sessions:
> - reviewer [completed]: <path>/1c276a38/run-0/session.jsonl
> ```"

**Source cited**: "verified from real sessions" — but only 1 session was verified during #26.

**Actual data** (562 spawn results from 200 sessions):

| Type | Count | % | Has `Sessions:` line | Has `Run:` line |
|------|-------|---|----------------------|-----------------|
| sync completed | 84 | 15% | ✅ | ✅ |
| async pending | 347 | 62% | ❌ | ❌ |
| error (unknown agent / validation) | 124 | 22% | ❌ | ❌ |
| isError=true | 7 | 1% | ❌ | ❌ |

**What's missing**: The spec must acknowledge that 62% of spawn calls (async) produce a toolResult with format `"Async: agent [uuid]"` — no `Run:`, no `Sessions:`, no child session paths. The `SubagentSpawnRecord.childSessionPaths` will be `[]` for all async spawns. The spec must either (a) document this as expected behavior, or (b) specify an additional linking mechanism for async spawns.

### GAP E2: Async child sessions are top-level sessions, not child session dirs

**Spec passage** (from "Child session opt-in"):
> "scanChildSessions(parentId) explicitly scans child sessions for a given parent by walking the filesystem (`<timestamp>_<parent-id>/<run-id>/run-<n>/session.jsonl`)"

**Source cited**: #19 decision + #26 revision.

**Actual data**: Verified that async spawn runs create top-level `.jsonl` files, not `run-N/session.jsonl` child dirs. Session `019facd0` has 4 async child sessions — all are top-level `.jsonl` files (confirmed via mgmt `status` call results containing `"Session: <path>.jsonl"`). The parent session's directory has zero `run-*` subdirs.

**What's missing**: The spec must acknowledge that `scanChildSessions(parentId)` via filesystem walk only finds sync child sessions. For async child sessions, the linking data is in mgmt call results (`status`/`wait`/`resume`), not in the spawn toolResult. The spec must either (a) add a mechanism to extract async child session paths from mgmt call results, or (b) explicitly document that async child sessions are out of scope for the initial implementation.

### GAP E3: "28 fields" claim lacks field enumeration

**Spec passage**:
> "metrics: SessionMetrics — 28-field precomputed aggregate (message counts, tool call counts, tokens, cost, files modified, languages, user interruptions, message hours, models used, compaction stats, thinking levels, feature usage flags)"

**Source**: #20 resolution comment defines SessionMetrics with 29 fields (including `childSessionIds`). #26 removes `childSessionIds` → 28.

**What's missing**: The parenthetical lists 12 categories but doesn't enumerate all 28 fields. The #20 resolution lists fields not mentioned in the spec: `gitCommits`, `userResponseTimes`, `toolErrorCategories`, `totalCacheWriteTokens`, `sessionPath`, `startTime`/`endTime`/`durationMinutes`. The spec must either inline the full type (as it does for `ToolCallRecord` and `SubagentSpawnRecord`) or explicitly reference the #20 resolution's type definition.

### GAP E4: toolResult text parsing risk undocumented

**Spec passage**: SubagentSpawnRecord fields marked "parsed from toolResult text" with no risk acknowledgment.

**What's missing**: The toolResult text format is pi's internal output, not an API contract. A pi version update could change the format silently. The spec must acknowledge this risk and specify a degradation strategy (e.g., return empty arrays with a `parseWarning` flag, not throw).

---

## Axis 2 — Consistency

### GAP C1: zod validation target contradicts ADR-0001

**Spec passage**:
> "zod for runtime validation of JSONL entries"

**Source**: #19 decision says "interfaces + zod schemas (运行时校验 + 类型推导)" for the 6 entities. But ADR-0001 says "reuse pi types, don't redefine entities."

**Contradiction**: If the base layer reuses pi's types and doesn't redefine entities, what does zod validate? pi's `SessionManager.open()` already parses JSONL — does the base layer re-validate its output? Or does zod validate the aggregate result types (`SessionMetrics`, `ToolCallRecord`, etc.)? The spec must specify what zod validates: (a) re-validate pi's parsed output (redundant?), (b) validate aggregate result types, or (c) validate tool call arguments structure.

### GAP C2: toolFrequencyRanking appears in both crossSession and toolProfile

**Spec passage**:
> "aggregate.crossSession(sessions) → CrossSessionMetrics (tool frequency ranking, ...)"
> "aggregate.toolProfile(sessions) → ToolProfile (bash command types, ... — computed from toolCalls)"

**Source**: #20 resolution defines `toolFrequencyRanking` in both `CrossSessionMetrics` and `ToolProfile`.

**Contradiction**: The spec's `toolProfile` description omits `toolFrequencyRanking`, but #20 includes it in both. Is it in `ToolProfile` or not? If yes, the spec description is incomplete. If no, #20's decision was silently dropped.

### GAP C3: "5 aggregation categories" numbering doesn't match #20

**Spec passage**:
> "plus lazy cross-session aggregates" + lists 5 aggregate functions

**Source**: #20 defines 5 categories as: (1) Session-level Meta [precomputed], (2) Cross-session, (3) Tool profile, (4) Usage breakdown, (5) Time trends, + Child association (separate).

**Contradiction**: The spec treats `childMapping` as the 5th aggregate function, but #20 treats Session-level Meta as the 1st category (precomputed, not an aggregate function) and Child as a separate concern. The spec's "5 aggregate functions" ≠ #20's "5 categories + child". This is a numbering mismatch that could confuse implementers about what's precomputed vs lazy.

### GAP C4: Prototype pain point count mismatch

**Spec passage**:
> "7 pain points discovered"

But then lists only 4. The #22 resolution lists 7 distinct pain points.

**What's missing**: The spec must either list all 7 or correct the count to 4 (with a note that 3 were already fixed and omitted).

---

## Axis 3 — Coverage

### GAP V1: No test for async spawn calls (62% of real data)

**Spec testing fixtures** list "A session with subagent spawn calls (single, parallel, chain) + matching toolResults" but don't mention async spawns.

**What's missing**: A fixture for async spawn — toolResult has `"Async: agent [uuid]"`, no `Sessions:` line. Test must verify `SubagentSpawnRecord.childSessionPaths` is `[]` and `runId` is extracted from the async format (or documented as unavailable).

### GAP V2: No test for spawn error results (23% of real data)

**What's missing**: A fixture for error spawn results (isError=true, validation failed, unknown agent). Test must verify how `SubagentSpawnRecord` handles errors — does it still create a record? With what fields?

### GAP V3: No test for empty session / session with no tool calls

**What's missing**: Fixtures for (a) a session with 0 messages, (b) a session with messages but 0 tool calls. Test must verify `toolCalls` is `[]`, `subagentSpawns` is `[]`, and aggregate functions don't crash.

### GAP V4: No test for scanSessions with --project filter

**What's missing**: A test that verifies `scanSessions({ project: '/some/cwd' })` filters correctly. How does project filtering work — exact match on `sm.cwd`? Prefix match? The spec doesn't specify the matching semantics.

### GAP V5: No test for scanChildSessions

**What's missing**: A test for `scanChildSessions(parentId)` — verifies it finds child sessions in `run-N/session.jsonl` dirs. Also needs a test for the async case (child sessions are top-level files, not in run-N dirs).

### GAP V6: No test for zod validation failure

User story 43 requires zod, but no fixture tests malformed JSONL or invalid entry structure.

**What's missing**: A fixture with a corrupted JSONL line. Test must verify zod catches it with a clear error (not a silent skip or a crash).

### GAP V7: No test for aggregate functions on empty input

**What's missing**: Tests for `aggregate.crossSession([])`, `aggregate.timeTrends([], {})`, `aggregate.toolProfile([sessionWithNoTools])`. Spec doesn't specify behavior — should return empty/zero structures, not throw.

### GAP V8: No test for branched sessions

pi sessions have a tree structure (parentId chain). A toolCall and its toolResult might not be adjacent in entry order.

**What's missing**: A fixture where toolCall and toolResult are separated by other entries. Test verifies pairing by `toolCallId` still works.

---

## Axis 4 — Completeness

### GAP M1: #20's `agentUsageDistribution` dropped from spec

**Source**: #20 CrossSessionMetrics includes `agentUsageDistribution: Record<string, number>` (agent name → call count).

**Spec**: `aggregate.crossSession` description says "tool frequency ranking, project distribution, model usage breakdown, totals" — no mention of agentUsageDistribution.

**What's missing**: Either include `agentUsageDistribution` in the spec or explicitly note it was dropped (and why).

### GAP M2: #20's `gitCommits` and `userResponseTimes` dropped from spec

**Source**: #20 SessionMetrics includes `gitCommits: string[]` and `userResponseTimes: number[]`.

**Spec**: The "28-field" description doesn't mention either field.

**What's missing**: Confirm whether these are in the 28 fields or were dropped. If dropped, note why. If present, add to the spec description.

### GAP M3: #21's JSON output schema dropped from spec

**Source**: #21 resolution specifies detailed JSON output schemas for each CLI subcommand (`sessions`, `tools`, `usage`, `trends`, `all`).

**Spec**: Says "Output: JSON to stdout" but doesn't specify the JSON structure for any subcommand.

**What's missing**: The spec should either inline the JSON schemas from #21 or reference them explicitly.

### GAP M4: #21's consumer migration path dropped from spec

**Source**: #21 resolution includes migration code examples for pi-insight and guardrail-optimizer.

**Spec**: "Further Notes" mentions known consumer patterns but doesn't include migration paths.

**What's missing**: While migration is out of scope (correctly), the migration path informs the API shape. The spec should at least reference #21's migration examples in Further Notes.

### GAP M5: Session name/title not in SessionMetrics

**Source**: pi sessions have `session_info` entries with a `name` field. The prototype's scan showed session names are available via `sm.getName()` or `session_info` entry.

**Spec**: No mention of session name in SessionMetrics or any aggregate.

**What's missing**: Decide whether `sessionName` is a field in SessionMetrics. If yes, add it. If no, note that consumers needing the name should call `parseSession()` — but this contradicts the "most consumers should not need parseSession()" design goal.

---

## Axis 5 — Implementability

### GAP I1: SubagentSpawnRecord for async spawns is under-specified

**Spec passage**:
```typescript
interface SubagentSpawnRecord {
  runId: string;               // parsed from toolResult text
  childSessionPaths: string[]; // parsed from toolResult text
}
```

**Problem**: For async spawns (62% of data), the toolResult is `"Async: agent [uuid]"`. There's no `Run:` line and no `Sessions:` line. The spec doesn't say what `runId` and `childSessionPaths` should be for async spawns.

**Two developers would implement this differently**: One might extract the UUID from `"Async: agent [uuid]"` as the runId. Another might leave runId empty. One might return `childSessionPaths: []`. Another might try to find the sessions via mgmt call results.

**What's missing**: The spec must specify async spawn handling: (a) `runId` extracted from `"Async: agent [uuid]"` format, (b) `childSessionPaths: []` for async (with a note that async child sessions are top-level files discoverable via mgmt call results, out of scope for initial implementation), or (c) a `status: 'completed' | 'async_pending' | 'error'` field to distinguish.

### GAP I2: scanChildSessions return type unspecified

**Spec passage**:
> "scanChildSessions(parentId) explicitly scans child sessions for a given parent"

**Problem**: Doesn't specify the return type. `SessionScanResult[]`? `SessionMetrics[]`? If `SessionScanResult[]`, does it include `toolCalls` and `subagentSpawns` for child sessions?

**What's missing**: Specify return type as `SessionScanResult[]` (consistent with `scanSessions`).

### GAP I3: `--project` matching semantics unspecified

**Spec passage**:
> "--project <path> to filter by cwd"

**Problem**: Is it exact match? Prefix match? Symlink-resolved match? `SessionManager.list(cwd)` uses `sessionCwdMatches()` — does the base layer use the same?

**What's missing**: Specify matching semantics (exact match on resolved path, consistent with `SessionManager.list`).

### GAP I4: Error handling for scanSessions unspecified

**Problem**: What happens when a session file is corrupted? When `SessionManager.open()` throws? When the sessions dir doesn't exist?

**What's missing**: Specify error handling strategy: skip broken sessions with stderr warning (prototype behavior) or throw. Specify behavior for missing sessions dir.

### GAP I5: `all` subcommand output structure unspecified

**Problem**: User story 23 says "get all 5 aggregation categories in one JSON" but the spec doesn't specify whether the output includes per-session `SessionScanResult[]` or only the 4 aggregates.

**What's missing**: Specify the JSON structure: `{ sessions: SessionScanResult[], crossSession: ..., tools: ..., usage: ..., trends: ..., children?: ... }` or similar.

### GAP I6: toolResult parsing failure behavior unspecified

**Problem**: If the toolResult text doesn't match any expected format (pi version changed), what happens?

**What's missing**: Specify degradation strategy: return `SubagentSpawnRecord` with available fields and `[]` for unparseable fields, not throw.

### GAP I7: Concurrency strategy for file scanning unspecified

**Problem**: Scanning 100+ session files sequentially is slow. The prototype was slow. insight-learned.md documents that diwu uses concurrency 8, observal uses 50.

**What's missing**: Specify whether scanSessions uses concurrent file scanning and what concurrency level. Or explicitly defer to implementation choice.

---

## Verdict

**Not ready** — 22 gaps across 5 axes.

| Axis | Gaps | Critical |
|------|------|----------|
| Evidence | 4 | E1, E2 (design-changing) |
| Consistency | 4 | C1 (zod contradiction) |
| Coverage | 8 | V1, V2, V5 (62%+ of data untested) |
| Completeness | 5 | M1, M3 (dropped decisions) |
| Implementability | 7 | I1 (async under-specified) |

The spec must be revised to close these gaps before handoff to `/skill:implement`. The most critical issues:

1. **SubagentSpawnRecord must handle async spawns** (E1 + I1) — 62% of real data
2. **scanChildSessions must acknowledge async limitation** (E2 + V5) — async child sessions are invisible to filesystem walk
3. **zod validation target must be specified** (C1) — current spec contradicts ADR-0001
4. **Test coverage must expand** (V1–V8) — 8 missing scenarios, 3 critical
5. **SessionMetrics fields must be enumerated** (E3 + M1 + M2) — dropped fields from #20
