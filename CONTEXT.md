# Glossary

## Guardrail Optimizer

- **Outside-cwd path**: An absolute path that falls outside the session's working directory (`cwd`). Pi-guardrails' path-access extension intercepts tool calls targeting such paths and prompts the user to allow or deny. Synonym: "outside-workspace path" (the term used in the guardrail TUI prompt).

- **Path access replay**: Re-running pi-guardrails' `targetsForTool` + `checkPathAccess` logic against historical tool calls recorded in session JSONL files, using empty `allowedPaths` to reconstruct which paths would have triggered a prompt. This is a *reconstruction*, not a reading of stored interception records — guardrail prompts are interactive TUI events and are not persisted to session files.

- **Path hit**: A single instance of a tool call targeting an outside-cwd path, as detected by replay. One path may accumulate many hits across sessions.

- **Noise path**: A path that triggers detection but is not a meaningful access target — e.g., `/dev/null` (bash redirect), glob patterns (`*.jsonl`), `/proc/` virtual filesystem entries. These should be filtered before semantic analysis.

- **Allowed path**: An entry in `guardrails.json` under `pathAccess.allowedPaths` that pre-authorizes agent access to a specific file or directory, bypassing the interactive prompt. Has an explicit `kind` of `file` (exact match) or `directory` (prefix match including descendants).

- **Grant granularity**: The choice between `file` and `directory` kind for a recommended allowed path. File grants are narrower (safer); directory grants are broader (more convenient, fewer future prompts).

## Session Profile

The shared session-analysis foundation. Parses pi agent session JSONL and provides structured aggregation metrics for downstream consumers (pi-insight, guardrail-optimizer, subagent profilers).

- **Top-level session**: A session JSONL file that a user or agent initiates directly — the primary unit of interaction. Pi's `SessionManager.listAll()` discovers these. Stored as `<timestamp>_<session-id>.jsonl` under the sessions directory.
_Avoid_: Parent session (use only when contrasting with child)

- **Child session**: A session spawned by a subagent tool call within a top-level session. Stored at `<timestamp>_<parent-id>/<run-id>/run-<n>/session.jsonl`. Pi's `SessionManager` does not discover these — child session discovery is the base layer's unique responsibility. A child's tokens and cost are part of the parent's execution; including both double-counts.
_Avoid_: Sub-session, nested session, subagent session

- **Session metrics**: The precomputed per-session aggregate — 28 fields covering messages, tools, tokens, cost, code output, user behavior, and context health. Computed during scan, returned as `SessionMetrics`. This is the base layer's primary data product.
_Avoid_: Session stats, session meta, session profile (overloaded with the module name)

- **Aggregate**: A cross-session computation function that takes `SessionMetrics[]` and returns a summary structure (e.g., `ToolProfile`, `UsageBreakdown`, `TimeTrends`). All aggregates are lazy — computed on demand, never during scan. Pure functions with no internal state.
_Avoid_: Aggregation (use the noun for the function, "aggregation" for the process)

- **Tool profile**: The tool argument-level analysis aggregate — bash command type distribution (git/grep/npm/...), write/edit file extension distribution, read path type classification, subagent mode/agent/async patterns, and per-tool argument key profiles. Goes beyond call counts into how tools are used.
_Avoid_: Tool stats, tool analysis

- **Decay-weighted average**: A time-aware average where recent sessions have exponentially more weight, using a 10-day half-life (`λ = ln(2) / 10d`). Borrowed from observal's `decayWeight()`. Used in time trends to make recent behavior matter more than stale history.

- **Consumer**: A downstream tool that imports the base layer (library mode) or calls its CLI to get session metrics and aggregates. Consumers own their own caching and domain-specific analysis. Known consumers: pi-insight, guardrail-optimizer, subagent profiler.
_Avoid_: Client, user (reserved for the human)

- **Raw entries**: The unparsed `FileEntry[]` returned by `parseSession()`, delegated to pi's `SessionManager.open().getEntries()`. The base layer's extension point — consumers needing custom analysis call this directly instead of through a hook mechanism.
_Avoid_: Session entries (ambiguous with parsed entries), JSONL lines
