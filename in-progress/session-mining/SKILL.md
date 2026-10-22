---
name: session-mining
description: "Mine pi session logs along two script routes — by skill name (injection marker + read-loads → trace index) or by tool call (args substring, errors-only → calls dump) — plus version anchor and relay enrichment. Use when the user asks to 找出/检索/挖掘/审计 historical sessions (which sessions ran skill X, who called tool Y, trigger-rate audit, error-pattern mining, token-cost mining), before /skill:skill-call-diagnose or /skill:tool-call-diagnose needs a trace, or any backfill over session logs. Questions the scripts cannot express (usage-shape clustering, single-session dissection, harness custom events, full-corpus semantic mining) route to the recipes instead of hand-rolled guessing."
---

# Session Mining

**Leading word:** the **route** — the question type picks the method before any command runs. The two script routes deliver the **trace index** (one line per session entry: role, tool calls, usage — the compact map of a multi-MB log) and the **calls dump** (paired toolCall/toolResult records — self-sufficient evidence for tool diagnosis). The remaining routes are **recipes**: hand-mining patterns the scripts cannot express, each earned in a real mining session.

## 1. Route the question

| Question | Route | Weapon |
|---|---|---|
| Which sessions ran skill X / followed it? | script: skill route | `find-skill-sessions.py` |
| Who called tool Y, which calls failed? | script: tool route | `find-tool-calls.py` |
| What does command Z's real usage look like? | recipe: shape clustering | args regex + de-doc-noise |
| Dissect one known session id | recipe: dissection | skip retrieval, coarse stats → lanes |
| What did peer do since last check? | recipe: tailing | anchor line + window read |
| Cross-corpus semantic signals (no retrieval key) | recipe: full-corpus miner | self-written scanner, replayable |
| Harness custom events (guardrails, compaction) | recipe: event-signature grep | script routes are blind here |
| Subagent transcript recovery (transcripts, not sessions) | recipe: transcript paging | read pagination |

Script routes never cover the recipe rows: "who failed" is audit-shaped, "what shape" is usage-shaped — forcing the wrong one bypasses the skill (observed: orca spawn-chain mining ignored an injected tool-call extract).

## 2. Shared skeleton

1. **Triage** — run the route, write the candidate JSON to `~/tmp/<topic>-sessions.json`; later funnel stages filter that file incrementally, never re-walk the corpus. Noise signature: low marker count + high entry count + scattered tool histogram = incidental injection. Strings from the skill's own body inflate string matches; count real `toolCall` entries.
2. **Anchor versions** — before any cross-session comparison: `python3 <SKILL_DIR>/scripts/version-anchor.py <session.jsonl> [--skill <name>]`. `commit` / `uncommitted` (`matches_current_file: false` = ghost version, findings cite bytes that exist nowhere else) / `third-party`. Skill name ≠ trigger name — a wrapper skill's injection anchors to the wrapper.
3. **Index or dump** —
   ```bash
   python3 <SKILL_DIR>/scripts/find-skill-sessions.py --index <session.jsonl> > trace-index.json
   python3 <SKILL_DIR>/scripts/find-tool-calls.py --dump <session.jsonl> <tool> [--args-contains S] [--errors-only] > calls.json
   ```
   Index caps at 600 entries (`truncated: true` — long files: filter by time window, not entry number). Dump takes the tool name as a positional arg. **Success/fail dual dump is standard** for usage questions: errors-only misses the fix already sitting in an adjacent successful call (recovery-chain diff).
4. **Aggregate, never re-read** — pair calls to results by `toolCallId` (`isError` lives on the message); probe the JSONL structure with one real record before writing a parser (zero-row parsers shipped twice). Line-grep pre-filter, write big outputs to files, return only histograms + samples. `isError: false` still hides runtime errors — sample it.
5. **Deep-read via lanes** — fresh-context subagents per theme. Batch lane fanout goes through a scripted workflow (`runs.all`, fresh context, task text only — a seed of the parent conversation costs ~40K tokens per lane for nothing); bg_delegate is for lanes that need the parent's in-session findings or async wake. Each lane brief carries: entry-structure pointer (`references/session-jsonl.md`), output contract (report to file, ≤30-line receipt), and known-findings in handoff shape — what this effort found, what remains open, the lane's first action. Dump files are the lane input; the main context reads only the summary table.
6. **Relay enrichment (opt-in)** — only when the consumer will face token/latency/cache questions: `python3 <SKILL_DIR>/scripts/relay-enrich.py <session-or-id> > relay-enrich.json`. `no-relay-data` → note it and move on; the JSONL pipeline never blocks on relay.

## 3. Close

Errors needing **attribution** (blame a run, a contract, an agent) → announce and continue into `/skill:tool-call-diagnose` in the same session (one line: "N 次错误，继续分轴分析"). Errors as **portrait material** (usage mining, design input, active-development churn) are recorded in the deliverable, not diagnosed. Multi-session dump matrices skip the single-trace contract — brief the four axes as lanes over the matrix (`references/recipes.md`). Skill-execution traces go to `/skill:skill-call-diagnose` the same way.

**Deliverables**: trace file path · trace index or calls dump path(s) · triage stats · version verdict per compared session · relay enrichment (when run).

**Recheck sweep**: before closing, scan `~/skills/recheck/INDEX.md` for rows targeting the mined skill/tool — rerun those scripts, diff against the baseline column, and report drift in the deliverable. **Window discipline**: portraits over a bounded window (recent-20) answer "how is it used now" but miss population-level phenomena — one-off schema-era error families, rare-but-repeated anti-patterns, unknown-identifier inventories. When the deliverable feeds a redesign (companion skill, named agents, guard rules), cross-check a full-corpus scan or an independent miner's dump before ranking candidates (2026-10-22: a recent-20 four-axis pass missed the top sedimentation candidate — 315+ repeated hand-rolled dispatches — that a same-topic full-corpus peer scan had already ranked).

**Done when**
- [ ] Route chosen against the table and stated (recipes carry their own done-when)
- [ ] Every triage match has a verdict (chosen / skipped with reason)
- [ ] Index/dump built, path stated, truncation noted
- [ ] Version anchor run on every compared session, verdict stated
- [ ] Errors either handed to diagnose or explicitly absent

**Recipes** (`references/recipes.md`) — hand-mining patterns with their own pitfall lists. **Primer** (`references/session-jsonl.md`) — entry structure, marker, pairing, cost accounting; read before touching raw JSONL.
