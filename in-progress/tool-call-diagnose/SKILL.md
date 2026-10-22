---
name: tool-call-diagnose
description: "Diagnose how a tool was called in pi session traces, along four axes — Failure taxonomy & blame (classify errors into families, blame agent-usage vs harness vs environment, cross-checked against companion skills like pi-subagents for the subagent tool), Retry waste (failed→retried patterns, identical-retry loops, quantified token cost), Usage & sedimentation (habitual anti-patterns across all calls, fallback scripts — propose a new companion skill when none covers the tool), Contract & competition (tool bypass via bash, schema-fit misses, description→behavior gap — repeated same-shape misuse means the tool description failed). Takes a trace from /skill:session-mining. Use when the user asks 诊断工具调用失败 / why subagent workflowScript or bash glab api calls keep failing, or to audit one tool's usage across sessions."
---

# Tool Call Diagnose

**Leading word:** the **calls dump** — paired toolCall/toolResult records delivered by `/skill:session-mining`. Every finding cites dump records or trace entry indices (`call_entry 306`, `[307]`); a finding with neither is an opinion, not a finding.

The tool under diagnosis is the **target tool** (`subagent`, `bash`, `edit`, ...). Four axes run as parallel fresh-context sub-agents: 失败分类判责 / 重试浪费 / 用法沉淀 / 契约与替代. Before any of them runs, one gate decides the whole routing: **does a companion skill already exist for this tool?**

The gate exists because the recurring real-world outcome is: the agent hit pits that a companion skill already documents (pi-subagents documents exactly why `Structured single-child execution cannot be combined with workflowScript` fails) — reading it once would have skipped the failure. Findings of that shape route to behavior fixes, not new documentation.

## Process

### 1. Resolve inputs

Target tool name (required, ask if absent) and the trace: either `/skill:session-mining` deliverables (session file + calls dump + stats), or a session id / symptom the extract skill can resolve. Symptom → filter mapping: "glab api 失败" = `bash --args-contains 'glab api' --errors-only`; "subagent workflowScript 挂" = `subagent --errors-only` (narrow with `--args-contains workflowScript` if noisy).

If no dump in hand, get one from the extract skill's installed script (`~/.agents/skills/session-mining/scripts/find-tool-calls.py`) — search, triage, then dump. Build **two** dumps when diagnosing usage or retries: with and without `--errors-only` (successes and workarounds are evidence). Also build the surrounding-turn trace index:

```bash
python3 ~/.agents/skills/session-mining/scripts/find-skill-sessions.py --index <session-file> > trace-index.json
```

**Relay enrichment (optional)**: only when the user explicitly asks for latency/retry-depth analysis, also run `python3 ~/.agents/skills/session-mining/scripts/relay-enrich.py <session-file> > relay-enrich.json` — per-tool-call `duration_s` / `attempt_index` / `status` from the NeMo Relay ATIF trajectory (`no-relay-data` on miss is non-blocking; pi JSONL stays the primary source).

### 2. Companion-skill gate

Determine whether a skill already documents this tool's usage:

1. Known pairs first: `subagent`/`subagent_supervisor` → **pi-subagents**; `bash` + glab/gitlab args → **glab-api**; `bash` + harbor args → harbor-cli conventions in AGENTS.md; `ocr` CLI → **ocr**.
2. Generic discovery: grep tool name over `~/.pi/agent/skills/*/SKILL.md` and `~/skills/**/SKILL.md` frontmatter/descriptions.

If a companion skill exists, **read it fully now** — its documented pitfalls are the baseline the failure axis checks against, and this diagnosing agent must know them to route correctly. Also check the trace: did the session's agent read that SKILL.md *before* the failures (a `read` toolCall whose path ends `/<skill>/SKILL.md`, or the skill-injection marker, earlier than the first failed call)? Cheap check: grep the raw jsonl for the SKILL.md path and compare entry positions against the dump's `call_entry` values.

If no companion skill exists, note it — axis 3 gets a **new-skill mandate** instead of a cross-check baseline.

### 3. Spawn the four axes in parallel

First verify a read-only analysis agent exists (`subagent({ action: "list" })`); if none, run the axes inline in sequence and note the degradation. Spawn with `runs.all`, four children, `context: 'fresh'` each. **Every child gets**: the session file path, both calls dumps (paths), the trace index path, and the absolute paths of this skill's `references/error-families.md` and the extract skill's `references/session-jsonl.md` (fresh context — bare references leave them blind). Each brief demands: findings cited by dump record (`call_entry N`) or trace entry index, quantified waste with its arithmetic named, report in Chinese, under 400 words.

#### Axis 1 — 失败分类与判责 (Failure taxonomy & blame)

> Ground truth for family classification: `references/error-families.md` (read it first). The calls dump (errors-only variant) lists every failed call. Classify each into a family and assign blame: agent-usage / harness / environment / upstream-tool. For every agent-usage failure, state the one-line correct usage. Each verdict needs **text + temporal dual evidence**: the dump's args/result text says what failed, and the trace index timestamps say when — a verdict backed by only one of the two is provisional. If a relay enrichment was provided, its per-call `duration_s` and `status` are the temporal evidence (they survive pi-JSONL clock skew); use them, citing the enrichment step_id. Companion-skill cross-check (<skill name + path, or "none">): for each failure, is this pit already documented in the companion skill? A documented pit the agent still hit is the strongest finding — report it as `pit-documented-not-read` (or `pit-documented-ignored` if the trace shows the agent read the skill earlier and violated it anyway). 报告用中文，每条发现标注 call_entry 序号。

#### Axis 2 — 重试与浪费 (Retry & waste)

> The calls dump (full variant, including successes) plus the trace index are the evidence. Hunt: (a) failed→retried pairs — same tool, adjacent or near-adjacent turns; for each, did the retry change the args or repeat them identically? (b) identical-retry loops (3+ same-shape failures); (c) the workaround that finally succeeded — what did the agent change? (d) wall-clock stalls (call→result gaps far above the tool's normal latency). If a relay enrichment was provided: per-call `attempt_index` > 0 exposes **LLM/gateway-level attempt retries** the pi JSONL cannot show (distinguish them from agent-initiated retries), and `duration_s` quantifies the latency long-tail per call. Per cluster: entry indices, cost arithmetic named — wasted output tokens (failed attempts × their arg_len and surrounding output), context re-reads (sum of `in=` on cache-collapse turns), minutes stalled. 报告用中文，每条发现标注序号和量化成本。

#### Axis 3 — 用法与沉淀 (Usage & sedimentation)

> The calls dump (full variant) shows every call's args. Across successes and failures: (a) habitual anti-patterns — args shapes that are legal but costly (oversized inline commands, redundant flags, re-emitting payloads the tool already holds); (b) fallback behavior — after failures, what did the agent improvise (inline scripts, different tools, manual procedures)? Classify each improv: one-off (fine, leave it) vs repeated pattern (2+ times in this trace) vs persistent gap (the agent needed something no tool/skill provides). <If companion skill exists: name it and list its documented usage rules — flag only what it does NOT cover.> <If no companion skill exists: for every repeated pattern and persistent gap, sketch a new companion-skill proposal — name, trigger description, content outline drawn from this trace's evidence, which call entries it would have saved.> 报告用中文，每条发现标注 call_entry 序号。

#### Axis 4 — 契约与替代 (Contract & competition)

> The calls dump (full variant) plus the raw session jsonl are the evidence. Three checks: (a) **tool bypass** — did the agent route the same need through `bash` instead of the target tool? Count `bash` toolCalls whose args contain the target tool's CLI name (e.g. diagnosing `worktrunk` → grep bash args for `wt `); report bypass ratio and sample entries — a high bypass ratio means the tool's schema or description is harder to use than raw shell. (b) **schema fit** — args shapes outside the schema's intent: enum misses, repeated-verb duplicates (`{command:"switch",args:["switch"]}`), optional fields re-sent with defaults, invalid combinations the schema failed to prevent. (c) **description→behavior gap** — same-shape misuse repeated across turns or days (e.g. duplicate verbs recurring for 3 weeks): a rule the description states but calls keep violating is a description that failed, not an agent fault — propose the schema-level fix (enum tightening, positional hint, shorter description) over re-stating the rule. 报告用中文，每条发现标注 call_entry 序号和 bash 旁路样本。

### 4. Aggregate

Present the four axis reports under `## 失败分类与判责`, `## 重试与浪费`, `## 用法与沉淀`, `## 契约与替代` — verbatim or lightly cleaned. **Do not merge or rerank across axes.** End with per-axis one-liners: findings count + worst finding.

### 5. Classify and route

One table, one row per finding:

| # | Axis | Finding | Evidence | Route |
|---|------|---------|----------|-------|

Routes:

- **skill-doc** — a companion skill exists; its markdown must change (new pit, clarified usage rule)
- **new-skill** — no companion skill covers the tool; sediment the patterns into a new skill (axis 3's proposal). New skills go to `~/skills/in-progress/` per repo convention
- **agent-behavior** — the knowledge exists (companion skill) and the agent didn't use it; fix is a nudge — AGENTS.md rule, or a trigger-description tweak on the companion skill so it fires earlier
- **harness** — not the agent's fault (tool schema ambiguity, environment, provider); route to the user. Axis 4's schema-fix proposals (enum tightening, description rewrite) land here when the tool is upstream, or as a local patch when the tool is vendored/self-owned
- **noop** — one-off, not worth a change

Before proposing any fix, check the obvious duplicate: a proposal that just re-states what a companion skill already documents is `agent-behavior`, not `skill-doc`.

Ask the user which rows to act on. Applied fixes follow the skills-repo convention: edit the source copy, run its tests (`uv run pytest` from the skill dir) if present, gitleaks, commit, reinstall with `npx skills add -g ./<path> -a pi -y`.

## Done when

- [ ] Trace + calls dumps (+ trace index) in hand
- [ ] Companion-skill gate resolved (skill named & read, or explicit "none")
- [ ] All four axis reports present, every finding carrying call_entry / entry indices
- [ ] Failure findings carry family + blame; documented-pit hits marked as such
- [ ] Retry findings carry quantified cost with named arithmetic
- [ ] Routing table delivered; fixes applied only on user confirmation
