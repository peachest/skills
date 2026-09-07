---
name: diagnosing-skill-execute
description: "Diagnose how a skill executed in past pi sessions. Given a skill name (or a session id), find the sessions that invoked it, then run three parallel axes — Adherence (did the agent follow the skill's documented workflow?), Friction (tool failures, re-emitted payloads, wasted tokens, cache invalidation), Sedimentation (ad-hoc scripts the agent had to write that the skill should absorb). Use when the user asks to 诊断 skill 执行过程 / analyze how a skill ran / audit a skill's sessions, or after a session that ran a skill expensively, slowly, or off-script."
---

# Diagnosing Skill Execution

**Leading word:** the **trace** — the session log under diagnosis. Every finding cites trace entries (`[31]`, `[37]`) as evidence; a finding with no entry index is an opinion, not a finding.

The skill under diagnosis is the **target skill**; its SKILL.md and referenced docs are the ground truth for Adherence. Three axes run as parallel fresh-context sub-agents (they never pollute each other), each reporting under 400 words:

- **Adherence** — did the agent follow the target skill's documented workflow?
- **Friction** — where did execution stutter: failures, retries, re-emissions, cache collapse, stalls?
- **Sedimentation** — what did the agent improvise (inline scripts, repeated logic) that the target skill should absorb?

## Process

### 1. Resolve inputs

Target skill **name** (as in its frontmatter) — required. Optional: a session **id** the user already has. If the user gave neither, ask; do not guess a skill name.

### 2. Locate the sessions

```bash
python3 scripts/find-skill-sessions.py <skill-name>            # marker search
python3 scripts/find-skill-sessions.py <skill-name> --session <id>   # explicit id
```

Marker = the skill injection tag, not the string `skill:<name>` (that string appears inside other skills' injected bodies and false-positives by the dozen). Subagent fork sessions carry the marker too — include them. Zero matches → report and stop.

### 3. Triage and pick the trace

Present the match list to the user: file path, timestamps, message counts, tool-call histogram, usage totals, `likely_running`. A day of retries yields many sessions on one skill — that is expected.

- User picks → that session is the trace.
- User defers → default to the longest **finished** run (most entries, has a closing assistant summary, `likely_running: false`); note the choice.
- Multiple sessions on the same incident: diagnose the fullest one, cite the others as corroborating evidence, do not run axes on each.

**Done when**: exactly one trace file chosen and stated.

### 4. Load the target skill's contract

Read the target skill's SKILL.md. Every file it names as load-on-demand (workflow, references, prompts) is part of the contract — read them all now and list their paths. If the target skill's source lives in a repo (e.g. `~/skills/...`), read the source copy, not the installed one, when the two differ; note any drift.

**Done when**: the contract path list is complete — the Adherence axis needs it.

### 5. Build the trace index

```bash
python3 scripts/find-skill-sessions.py --index <trace-file> > trace-index.json
```

One line per entry: role, tool calls with arg sizes, result sizes, per-turn usage. This index is the only map the axis sub-agents need of a multi-MB trace — they read raw lines only where the index points.

### 6. Spawn the three axes in parallel

First verify the analysis agent exists (`subagent({ action: "list" })`): a read-only agent that can read/search files (e.g. `delegate`-style). If none is available, run the three axes inline in sequence and note the degradation in the report.

Spawn with `runs.all`, three children, `context: 'fresh'` each. **Every child gets the same four things**: the trace file path, the trace index (file path or full content), `references/session-jsonl.md` path, and its axis brief below. Adherence additionally gets the contract path list from step 4. Sub-agents have fresh context — a bare "the skill docs" with no paths leaves them blind.

Each brief demands: findings each cited by entry index, quantified waste with its arithmetic named, report in Chinese (the final report is user-facing), under 400 words.

#### Axis 1 — Adherence

> Ground truth: the target skill's SKILL.md and every doc it references (paths listed below — read them all). The trace is the session file at `<path>`; navigate with the trace index, read raw entries only where it points.
>
> Reconstruct the executed flow: which documented phases/steps ran, in what order, with which prescribed tools. Then report: (a) **skipped or reordered steps** — what the doc required, what the trace shows instead, entry indices; distinguish a step the doc made optional from a violation of a mandatory one; (b) **improvised alternatives** — where the agent replaced a prescribed tool/flow with its own; (c) one line on what was followed correctly. A step whose precondition made skipping it *legal* (e.g. the doc gates it on document size) still counts as followed — note the gate, don't flag it. 报告用中文，每条发现标注 entry 序号。

#### Axis 2 — Friction

> The trace is the session file at `<path>`; navigate with the trace index. Hunt the waste signals defined in the session-JSONL primer: re-emitted payloads (same large tool args across turns), tool failure loops, verbose error echo, prefix-cache collapse (cacheR drop + in= spike), wall-clock stalls.
>
> Per friction cluster report: what happened, entry indices, and a cost estimate that names its arithmetic — wasted output tokens (duplicate rounds × output), context re-read (sum of in= on cache-collapse turns), minutes stalled. Attribute cause where visible: skill design (e.g. verbose error output) vs harness/environment (network, model provider). 报告用中文，每条发现标注 entry 序号和量化成本。

#### Axis 3 — Sedimentation

> The trace is the session file at `<path>`; navigate with the trace index. Find every inline script the agent wrote into tool-call arguments (heredoc python/bash, one-liner pipelines) and every manual procedure it repeated across turns.
>
> Classify each: **one-off** (right to improvise, leave it), **repeated pattern** (same shape written 2+ times in this trace, or once here but recognizable from earlier sessions — flag it), **contract gap** (the agent did by hand what the target skill should have provided a script/step for). For every repeated-pattern and contract-gap finding, sketch the sediment: a script or workflow step, its name, its input/output interface, which trace entries it would have replaced. 报告用中文，每条发现标注 entry 序号。

### 7. Aggregate

Present the three axis reports under `## 遵循度 (Adherence)`, `## 摩擦点 (Friction)`, `## 沉淀机会 (Sedimentation)` — verbatim or lightly cleaned. **Do not merge or rerank across axes**: one axis's finding can mask another's (a perfectly compliant run can still be the expensive one). End with per-axis one-liners: findings count + worst finding within that axis.

### 8. Classify and route

One table, one row per finding:

| # | Axis | Finding | Evidence | Route |
|---|------|---------|----------|-------|

Routes:

- **skill-doc** — the target skill's markdown must change (workflow steps, ordering, mandatory gates)
- **skill-script** — the target skill needs a new/extended script (sedimentation findings land here)
- **harness** — not the skill's fault (model, provider, environment); route to the user, nothing to edit
- **noop** — one-off, not worth a change

Ask the user which rows to act on. For skill-doc / skill-script rows, the fix flow is the skills-repo convention: edit the source copy, run its tests (`uv run pytest` from the skill dir), gitleaks, commit, reinstall with `npx skills add -g ./<path> -a pi -y`. Do not reinstall while a live session is mid-run on that skill — the running session already holds the old body in memory, but avoid churn.

## Done when

- [ ] Every match from step 2 either diagnosed or explicitly skipped with a reason
- [ ] All three axis reports present, every finding carrying entry indices
- [ ] Friction findings carry quantified cost with named arithmetic
- [ ] Every sedimentation finding marked one-off / repeated / contract-gap
- [ ] Routing table delivered; fixes applied only on user confirmation
