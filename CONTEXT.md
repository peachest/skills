# Glossary

## Navigation Metaphor

The shared metaphor system spanning orient, wayfinder, review-spec, project-wiki, and hail. Every skill name is itself a navigation action: survey → orient → wayfind → inspect → traverse → hail.

- **Terrain**: The project's current state — code, tests, docs, decisions, conventions. What orient reads and what wayfinder navigates through.
_Avoid_: codebase (too generic), project state

- **Compass**: The requirement — it points the direction but is not the map. Can be wrong about the terrain.
_Avoid_: spec, requirement (use when discussing the metaphor)

- **Bearing**: The compact grounding summary orient produces from reading terrain. Carries terms, constraints, conventions, seams, landmarks, waymarks, gaps, and calibration. Consumed by wayfinder as the basis for charting the map.
_Avoid_: summary, context, overview

- **Map**: The shared artifact wayfinder creates on the issue tracker — an index of decisions made and pointers to tickets that hold their detail. An index, not a store.
_Avoid_: plan, checklist

- **Chart**: The codebase survey artifact project-wiki produces — a structured map of modules and files with SHA-based drift detection. The persistent form of terrain that orient reads from instead of surveying blindly.
_Avoid_: wiki, documentation

- **Destination**: What reaching the end of a wayfinder map looks like — a spec, a decision, or a change. Fixes the scope.
_Avoid_: goal, objective, milestone

- **Frontier**: The open, unblocked, unclaimed tickets on a wayfinder map — the edge of the known. What's takeable now.
_Avoid_: backlog, queue

- **Fog of war**: Decisions you can sense coming but can't yet pin down sharply enough to ticket. Lives in the map's "Not yet specified" section. Graduates into tickets as the frontier advances.
_Avoid_: unknown unknowns, uncertainty

- **Seam**: An existing interface, module, or pattern in the codebase that the work should follow rather than invent. Recorded in orient's bearing.
_Avoid_: boundary (overloaded with DDD's bounded context), API

- **Landmark**: An existing implementation whose semantics the requirement can migrate from. Not a seam to follow but a point to navigate by — its code encodes behavior more precisely than prose.
_Avoid_: reference (too generic), example

- **Waymark**: A test file — a marker left by previous travelers on the terrain, indicating paths that pass and boundaries that hold. A test named `test_old_user_compatibility` reveals hidden constraints no README documents.
_Avoid_: test (use when discussing the metaphor), fixture

- **Gap**: What the terrain doesn't cover but the requirement needs. Either **surveyed but empty** (you looked and found nothing — seeds the first grilling) or **beyond survey** (you didn't look because it wasn't in scope — flows into fog of war).
_Avoid_: missing piece, unknown

- **Calibration**: Orient's assessment of the requirement against the terrain — where the requirement **over-specifies** (terrain already handles it; extra instruction only binds the agent) and where it **under-specifies** (terrain is complex but the requirement passes over it in a phrase — likely the gap that matters most).
_Avoid_: review, validation

- **Route**: The spec — the planned path through the terrain. What review-spec inspects before handing off to implement for traversal.
_Avoid_: spec, plan

- **Reckon**: Dead-reckon your position after time away — recover where you got to across every project this session touches, from the last known fix (compaction summary + git + MRs + wayfinder frontier) plus the distance traveled since. The temporal complement to orient: orient reads terrain (what is here), reckon reads the wake you left (where did I get to). Invoke `/reckon` once; rules stay on until "stop reckon". See `engineering/reckon`.
_Avoid_: resume (overloaded with pi's `--resume`), status report, progress check, checkpoint

- **Distress signal**: What hail produces when the agent is off-route, looping, or failing to make progress. Captures routes attempted, estimated position, off-route cause, and rescue needed.
_Avoid_: error report, stuck report

## Guardrail Optimizer

- **Outside-cwd path**: An absolute path that falls outside the session's working directory (`cwd`). Pi-guardrails' path-access extension intercepts tool calls targeting such paths and prompts the user to allow or deny. Synonym: "outside-workspace path" (the term used in the guardrail TUI prompt).

- **Path access replay**: Re-running pi-guardrails' `targetsForTool` + `checkPathAccess` logic against historical tool calls recorded in session JSONL files, using empty `allowedPaths` to reconstruct which paths would have triggered a prompt. This is a *reconstruction*, not a reading of stored interception records — guardrail prompts are interactive TUI events and are not persisted to session files.

- **Path hit**: A single instance of a tool call targeting an outside-cwd path, as detected by replay. One path may accumulate many hits across sessions.

- **Noise path**: A path that triggers detection but is not a meaningful access target — e.g., `/dev/null` (bash redirect), glob patterns (`*.jsonl`), `/proc/` virtual filesystem entries. These should be filtered before semantic analysis.

- **Allowed path**: An entry in `guardrails.json` under `pathAccess.allowedPaths` that pre-authorizes agent access to a specific file or directory, bypassing the interactive prompt. Has an explicit `kind` of `file` (exact match) or `directory` (prefix match including descendants).

- **Grant granularity**: The choice between `file` and `directory` kind for a recommended allowed path. File grants are narrower (safer); directory grants are broader (more convenient, fewer future prompts).

## Session Profile

The shared session-analysis foundation. Parses pi agent session JSONL and provides structured scan results — metrics, tool call records, and subagent spawn records — plus lazy cross-session aggregates for downstream consumers (pi-insight, guardrail-optimizer, subagent profilers).

- **Top-level session**: A session JSONL file that a user or agent initiates directly — the primary unit of interaction. Pi's `SessionManager.listAll()` discovers these. Stored as `<timestamp>_<session-id>.jsonl` under the sessions directory.
_Avoid_: Parent session (use only when contrasting with child)

- **Child session**: A session spawned by a subagent spawn call within a top-level session. Stored at `<timestamp>_<parent-id>/<run-id>/run-<n>/session.jsonl`. Pi's `SessionManager` does not discover these — child session discovery is the base layer's unique responsibility. A child's tokens and cost are part of the parent's execution; including both double-counts.
_Avoid_: Sub-session, nested session, subagent session

- **Spawn call**: A subagent tool call that launches one or more subagents — single (one agent + task), parallel (tasks array), or chain (chain array). The tool call arguments contain agent name, task text, and options, but do **not** contain a run ID. The run ID and child session paths appear in the corresponding tool result text.
_Avoid_: Subagent invocation, agent dispatch

- **Management call**: A subagent tool call that operates on an already-running subagent — status query, wait, interrupt, steer, resume, stop. The `id` argument references an existing run. These calls do not spawn child sessions.

- **Subagent spawn record**: A structured pairing of a spawn call and its tool result, extracting the run ID, agent name, mode, task text(s), async flag, and child session file paths. Parsed from toolCall arguments + toolResult text during scan. The base layer's mechanism for linking parent sessions to child sessions — without it, linking requires fragile filesystem directory-name matching.
_Avoid_: Run record, subagent trace

- **Tool call record**: A lightweight per-tool-call projection — tool name, arguments, error flag, and timestamp — retained during scan. Not the full `FileEntry`; only the tool-relevant fields. Consumers needing tool arguments (guardrail-optimizer for path extraction, subagent profiler for task text) use these records instead of re-parsing the session file.
_Avoid_: Tool call (ambiguous — refers to the event, not the record), tool invocation log

- **Session metrics**: The precomputed per-session aggregate — 28 fields covering messages, tool call counts, tokens, cost, code output, user behavior, and context health. Computed during scan alongside tool call records and subagent spawn records, returned as part of the session scan result.
_Avoid_: Session stats, session meta, session profile (overloaded with the module name)

- **Session scan result**: The composite return value of `scanSessions()` — contains session metrics, tool call records, and subagent spawn records. The base layer's primary data product. Most consumers need only this; `parseSession()` is supplementary, for consumers needing non-tool entry types (custom events, compaction details, etc.).
_Avoid_: Scan output, session data

- **Aggregate**: A cross-session computation function that takes session scan results and returns a summary structure (e.g., `ToolProfile`, `UsageBreakdown`, `TimeTrends`). All aggregates are lazy — computed on demand, never during scan. Pure functions with no internal state.
_Avoid_: Aggregation (use the noun for the function, "aggregation" for the process)

- **Tool profile**: The tool argument-level analysis aggregate — bash command type distribution (git/grep/npm/...), write/edit file extension distribution, read path type classification, subagent mode/agent/async patterns, and per-tool argument key profiles. Goes beyond call counts into how tools are used.
_Avoid_: Tool stats, tool analysis

- **Decay-weighted average**: A time-aware average where recent sessions have exponentially more weight, using a 10-day half-life (`λ = ln(2) / 10d`). Borrowed from observal's `decayWeight()`. Used in time trends to make recent behavior matter more than stale history.

- **Consumer**: A downstream tool that imports the base layer (library mode) or calls its CLI to get session scan results and aggregates. Consumers own their own caching and domain-specific analysis. Known consumers: pi-insight, guardrail-optimizer, subagent profiler.
_Avoid_: Client, user (reserved for the human)

- **Raw entries**: The unparsed `FileEntry[]` returned by `parseSession()`, delegated to pi's `SessionManager.open().getEntries()`. Supplementary to the session scan result — consumers needing non-tool entry types (custom events, compaction entries, branch summaries) call this directly. Most consumers should not need it.
_Avoid_: Session entries (ambiguous with parsed entries), JSONL lines

## Mutation Testing

The test-quality validation layer between `tdd` (tests exist) and `code-review` (code conforms). Mutation testing mutates production code and checks whether tests fail — a surviving mutant is a test blind spot that coverage metrics cannot detect.

- **Mutant**: A mutated copy of production code with one operator swap applied (e.g. `==` → `!=`, `+` → `-`). The unit of mutation testing — each mutant is tested independently against the suite.
_Avoid_: mutation (the process), variant

- **Killed**: A mutant whose application caused at least one test to fail — the test suite caught the change. The desired outcome.
_Avoid_: detected, caught (use "killed" for the mutant status)

- **Surviving mutant** (aka **lived**): A mutant whose application left all tests passing — the test suite did NOT catch the change. A test blind spot: the test either doesn't exercise this code or doesn't assert the behavior that distinguishes original from mutated.
_Avoid_: false positive, escaped (use "survived" or "lived" for the mutant status)

- **Not covered**: A mutant at a code location no test executes at all. Gremlins distinguishes this from `lived` — a `lived` mutant is reached by tests but not caught; a `not covered` mutant is never reached. The self-rolled Go mutator and mutmut conflate both as `survived`, which understates the true test quality.
_Avoid_: untested, uncovered (use "not covered" for the gremlins-specific status)

- **Mutation score** (aka **efficacy**): `killed / (killed + survived) × 100%`. Measures how good tests are at catching mutations they *could* catch. `compile-error` and `timeout` are excluded from the denominator. Gremlins additionally reports **mutator coverage** — `(killed + lived) / total` — which measures how much mutated code tests reach at all. A high efficacy + low coverage means tests are good where they exist but don't exercise enough code.
_Avoid_: coverage (that's line coverage, a different and weaker metric), test quality score

## Research Pipeline

The multi-direction research workflow (`/skill:research`): grill → survey directions → parallel per-direction subagents → synthesize. Artifacts live under `~/research/<topic-slug>/`.

- **Direction**: A sub-topic of the research question, researched independently by one subagent. Each direction maps to one report and one subagent (separation of concerns).
_Avoid_: thread, facet, branch

- **Direction report**: The per-direction output, `NN-slug.md` — What + How + key findings only, every claim cited to its source. Deliberately stops before So What / Now What.
_Avoid_: section report, per-topic note

- **Synthesis**: The cross-direction merge, `00-summary.md` — all four layers (What / How / So What / Now What), contradictions reconciled, opening with a direction index that doubles as the topic's index.
_Avoid_: summary, rollup, digest

- **Synthesize subagent** (aka **synthesizer**): The single subagent that merges direction reports into the synthesis. Forks the main session's context to ground So What / Now What, but is explicitly not the main session — cannot spawn subagents, cannot grill, only synthesizes.
_Avoid_: merge agent, summary agent

- **topic-slug**: The directory name under `~/research/` holding one research topic's reports. Chosen by the main session during file layout.
_Avoid_: topic name, folder name, project name
