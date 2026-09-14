---
name: skill-call-diagnose
description: "Diagnose how a skill executed in a pi session, along three parallel axes — Adherence (did the agent follow the skill's documented workflow?), Friction (tool failures, re-emitted payloads, wasted tokens, cache invalidation), Sedimentation (ad-hoc scripts the agent had to write that the skill should absorb). Takes a trace from /skill:skill-call-extract. Use when the user asks to 诊断 skill 执行过程 / analyze how a skill ran / audit a skill's sessions, or after a session that ran a skill expensively, slowly, or off-script."
---

# Skill Call Diagnose

**Leading word:** the **trace** — the session log under diagnosis, delivered by `/skill:skill-call-extract` as a trace file plus trace index. Every finding cites trace entries (`[31]`, `[37]`) as evidence; a finding with no entry index is an opinion, not a finding.

The skill under diagnosis is the **target skill**; its SKILL.md and referenced docs are the ground truth for Adherence. Three axes run as parallel fresh-context sub-agents (they never pollute each other), each reporting under 400 words:

- **Adherence** — did the agent follow the target skill's documented workflow?
- **Friction** — where did execution stutter: failures, retries, re-emissions, cache collapse, stalls?
- **Sedimentation** — what did the agent improvise (inline scripts, repeated logic) that the target skill should absorb?

Findings do not end in the report: step 5.5 increment-merges them into the persistent wiki (`~/skills/wiki/<target-skill>/` — patterns, run logs, and a proposal ledger that also records rejected proposals). The next diagnosis starts from that wiki; skill edits are gated against it.

## Process

### 1. Resolve inputs

Two things: the **target skill name** (as in its frontmatter — required, ask if absent) and the **trace** (a session file path, or a session id / bare skill name when `/skill:skill-call-extract` has not run yet).

If no trace is in hand, get one: run the extract skill's script from its installed location (`~/.pi/agent/skills/skill-call-extract/scripts/find-skill-sessions.py`) — marker search for a bare skill name, `--session <id>` for an explicit id — and follow its triage flow. If the user already ran `/skill:skill-call-extract`, take its deliverables directly.

### 2. Load the target skill's contract

Read the target skill's SKILL.md. Every file it names as load-on-demand (workflow, references, prompts) is part of the contract — read them all now and list their paths. If the target skill's source lives in a repo (e.g. `~/skills/...`), read the source copy, not the installed one, when the two differ; note any drift.

**Done when**: the contract path list is complete — the Adherence axis needs it.

### 2b. Load wiki context (persistent knowledge layer)

If `~/skills/wiki/<target-skill>/patterns.md` exists, read it and extract the open-pattern list (状态: open). Two consumers: the Sedimentation axis gets the list in its brief (step 4) — a finding sharing a root cause with an open pattern is that pattern **recurring**, cited as such, not a new finding; and step 6 gets `skill-impact.md` — rejected proposals listed there must not be re-proposed without new evidence overturning the rejection rationale.

Also read `~/skills/wiki/_cross-skill/patterns.md` (cross-skill regularities) the same way — a cross-skill pattern recurring in this trace is evidence for it (an `absent-this-run`-style update flows to it too, via step 5.5).

No wiki dir for this skill → note "cold start" in the report and proceed (step 5.5 creates it).

### 3. Build the trace index

```bash
python3 ~/.pi/agent/skills/skill-call-extract/scripts/find-skill-sessions.py --index <trace-file> > trace-index.json
```

(Skip if the extract skill already built one.) One line per entry: role, tool calls with arg sizes, result sizes, per-turn usage. This index is the only map the axis sub-agents need of a multi-MB trace — they read raw lines only where it points.

### 4. Spawn the three axes in parallel

First verify the analysis agent exists (`subagent({ action: "list" })`): a read-only agent that can read/search files (e.g. `delegate`-style). If none is available, run the three axes inline in sequence and note the degradation in the report.

Spawn with `runs.all`, three children, `context: 'fresh'` each. **Every child gets the same four things**: the trace file path, the trace index (file path or full content), `references/trace-signals.md` and the extract skill's `references/session-jsonl.md` (absolute installed paths — sub-agents have fresh context, a bare "the reference docs" leaves them blind). Adherence additionally gets the contract path list from step 2; Sedimentation additionally gets the open-pattern list from step 2b — both the target skill's and `_cross-skill/` — each entry as `P-### (or X-###) + 根因 + 现象一行`, plus the wiki patterns.md paths themselves (public repo, readable) in case deeper context is needed.

Each brief demands: findings each cited by entry index, quantified waste with its arithmetic named, report in Chinese (the final report is user-facing), under 400 words.

#### Axis 1 — Adherence

> Ground truth: the target skill's SKILL.md and every doc it references (paths listed below — read them all). The trace is the session file at `<path>`; navigate with the trace index, read raw entries only where it points.
>
> Reconstruct the executed flow: which documented phases/steps ran, in what order, with which prescribed tools. Tag every contract step with an evidence state: **followed** (trace shows it ran), **violated** (trace shows it did not), or **documented-but-unobservable** (the doc requires it but the trace cannot show it — e.g. an internal judgment with no tool footprint). Then report: (a) **violated steps** — what the doc required, what the trace shows instead, entry indices; distinguish a step the doc made optional from a violation of a mandatory one; (b) **documented-but-unobservable steps** — listed separately, never counted as violations; (c) **improvised alternatives** — where the agent replaced a prescribed tool/flow with its own; (d) one line on what was followed correctly. A step whose precondition made skipping it *legal* (e.g. the doc gates it on document size) still counts as followed — note the gate, don't flag it. 报告用中文，每条发现标注 entry 序号。

#### Axis 2 — Friction

> The trace is the session file at `<path>`; navigate with the trace index. Hunt the waste signals defined in the trace-signals reference: re-emitted payloads, tool failure loops, verbose error echo, prefix-cache collapse, wall-clock stalls.
>
> Per friction cluster report: what happened, entry indices, and a cost estimate that names its arithmetic — wasted output tokens (duplicate rounds × output), context re-read (sum of in= on cache-collapse turns), minutes stalled. Attribute every cluster to one of seven causes: **Harness** (pi/extension/provider plumbing), **Repository** (repo state the skill could not foresee — missing files, dirty worktree), **Model** (retry loops, verbose output, reasoning depth), **Requirement** (the ask itself was ambiguous/conflicting), **External** (network, internal services, CI), **Task complexity** (inherent to the job, nobody's fault), **Unknown** (evidence insufficient — say so, don't guess). 报告用中文，每条发现标注 entry 序号、量化成本和归因类别。

#### Axis 3 — Sedimentation

> The trace is the session file at `<path>`; navigate with the trace index. Find every inline script the agent wrote into tool-call arguments (heredoc python/bash, one-liner pipelines) and every manual procedure it repeated across turns.
>
> Classify each: **one-off** (right to improvise, leave it), **repeated pattern** (same shape written 2+ times in this trace — flag it), **contract gap** (the agent did by hand what the target skill should have provided a script/step for). For every repeated-pattern and contract-gap finding, sketch the sediment: a script or workflow step, its name, its input/output interface, which trace entries it would have replaced. Wiki open patterns for this skill (from step 2b): <list of `P-### + 根因 + 现象一行`>. A finding matching one is a recurrence — report it as such (pattern id + fresh evidence), not as a new finding. 报告用中文，每条发现标注 entry 序号。

### 5. Aggregate

Present the three axis reports under `## 遵循度 (Adherence)`, `## 摩擦点 (Friction)`, `## 沉淀机会 (Sedimentation)` — verbatim or lightly cleaned. **Do not merge or rerank across axes**: one axis's finding can mask another's (a perfectly compliant run can still be the expensive one). End with per-axis one-liners: findings count + worst finding within that axis.

### 5.5. Merge into wiki

Merge the diagnosis into the persistent knowledge layer at `~/skills/wiki/<target-skill>/` (create the dir on cold start; format and entry spec: `~/skills/wiki/README.md`).

- **Increment-merge into `patterns.md`** — a finding sharing a root cause with an existing pattern *updates* that entry (append 证据 `session-id#entry`, add an 出现 record, refine 方案 if a better one emerged); never a duplicate entry. A new root cause gets the next P-### id. Every open pattern must carry a **passCheck** — a single executable pass criterion (a command, or a directly observable condition) that would hold if the fix landed; when merging, a pattern without one gains it now, and `absent-this-run` judgments align with it (this run's trace satisfies the passCheck → absent; still violates it → the pattern recurred, evidence citing the entries that fail it). Bare entry indices in axis reports convert to `session-id#entry` via each trace's session (from step 3's index). Open patterns not seen this run — judged against **all three axis reports combined**, not Sedimentation alone (an environment-rooted pattern recurs as a Friction finding) — get an `absent-this-run` note appended to their 出现 line. The same merge applies to `_cross-skill/patterns.md`: a regularity confirmed in this run's traces appends evidence (with the skill name); a cross-skill pattern not seen this run gets an `absent-this-run` note only when this skill's trace would have surfaced it.
- **Append one line to `logs.md`** — date, run number (next # column value), input session ids, 执行数, one-line conclusion.
- **Promote verified rows in `skill-impact.md`** — when a fix has landed (accepted) and its corresponding pattern now has 2 consecutive `absent-this-run` records, update that row's 验证 cell and 结果 to `verified`, citing the absent records.
- **Surface closure candidates** — after merging, list patterns that now meet the closure condition (fix landed + 2 consecutive absent runs) alongside the step 6 routing table, and ask the user to confirm closing. Closing without asking leaves the entry silently dangling.
- **Sanitize before writing (public repo)** — internal domains/IPs → placeholder set from `docs/agents/skill-authoring.md`; internal project names → generic descriptors; credentials → behavior only, never the value; evidence as `session-id#entry`, never absolute paths or raw excerpts.
- **Gate then commit** — from the skills repo root run gitleaks (`gitleaks dir . --config ~/data/benchmark/config/gitleaks.toml`), then commit the wiki change. Merging is bookkeeping and proceeds automatically; **closing** a pattern (open → closed) is a judgment — only on user confirmation, after the fix landed and the pattern was absent 2 consecutive runs.

### 6. Classify and route

One table, one row per finding:

| # | Axis | Finding | Evidence | Route |
|---|------|---------|----------|-------|

Routes:

Friction findings arrive pre-attributed (step 4 seven-way taxonomy); attribution maps to routes: Model/External/Harness → **harness**; Task complexity/Unknown → **noop** unless the cost is recurring; Requirement → **harness** (route to the user); Repository → **harness**, or **skill-doc** if the skill's contract should have handled that repo state; skill-design findings (the former "skill design" bucket, now split) land in skill-doc / skill-script as before. Adherence and Sedimentation findings route unchanged.

- **skill-doc** — the target skill's markdown must change (workflow steps, ordering, mandatory gates)
- **skill-script** — the target skill needs a new/extended script (sedimentation findings land here)
- **harness** — not the skill's fault (model, provider, environment); route to the user, nothing to edit
- **noop** — one-off, not worth a change

Before proposing any fix, read `~/skills/wiki/<target-skill>/skill-impact.md` — missing file means no rejected proposals to avoid. A proposal whose shape matches a rejected one must not be re-proposed unless new evidence overturns the original rejection rationale.

Ask the user which rows to act on. For skill-doc / skill-script rows, the fix flow is the skills-repo convention: edit the source copy, run its tests (`uv run pytest` from the skill dir), gitleaks, commit, reinstall with `npx skills add -g ./<path> -a pi -y`. Do not reinstall while a live session is mid-run on that skill — the running session already holds the old body in memory, but avoid churn. After each applied fix, append a row to `skill-impact.md` (提案 / 落点 / commit / 验证命令与结果).

**Post-fix independent verification** (same day, not next use): after the fix lands, spawn one fresh read-only subagent with the original trace path, the updated contract (SKILL.md + referenced docs), and the pattern's passCheck. It renders a verdict: **verified** (executing the updated contract over this trace would not hit the finding), **partial** (fix addresses part of it), or **blocked** (cannot tell from this trace). Record the verdict in the skill-impact row. Long-run verification stays as before: the next diagnose run marking the corresponding pattern `absent-this-run` (per its passCheck) is the real gate — the two checks run in parallel: same-day verdict for immediate feedback, behavioral confirmation for closure.

## Done when

- [ ] Trace and trace index in hand (via skill-call-extract or its script)
- [ ] All three axis reports present, every finding carrying entry indices
- [ ] Friction findings carry quantified cost with named arithmetic
- [ ] Every sedimentation finding marked one-off / repeated / contract-gap
- [ ] Routing table delivered (Friction rows carry their seven-way attribution); fixes applied only on user confirmation
- [ ] Wiki increment-merged (or cold start noted); open patterns carry passCheck; sanitize gate passed
- [ ] Applied fixes recorded in skill-impact.md, each with its post-fix verification verdict (verified/partial/blocked)
