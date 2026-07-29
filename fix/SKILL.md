---
name: fix
description: Verify, grill, and fix code-review findings. Use when review comments, bug reports, or static-analysis findings need verdicts and action.
---

# Fix

Take a list of code review findings — from `/skill:triage-mr`, `/skill:code-review`, `/skill:diagnosing-bugs`, or any source that produces "here are things wrong with this code" — and work each one to a **verdict** and an action.

A finding is a claim, not a fact. The skill's job is to **verify** each claim before acting on it, then **fix** the ones that hold up. Verify before grill, grill before fix — inverting this order is the skill's defining failure.

## Input

A list of findings in this uniform format, regardless of source:

```json
[
  {
    "discussion_id": "unique-id",
    "file": "path/to/file.go",
    "line": 42,
    "body": "description of the issue"
  }
]
```

## Verdicts

Five verdicts:

| Mark | Verdict | Action |
| ---- | ---- | ---- |
| ✅ TP | True positive — real defect | Fix |
| ❌ FP | False positive — misjudgment or design intent | Skip |
| 🟡 Edge | Real but low priority | Optional fix |
| 🔵 OOS | Out of scope — pre-existing, not this change | Skip |
| ⏸️ Question | Cannot determine | Pause and ask |

Verdict definitions, priority levels, decision tree, and field requirements: [CLASSIFICATION.md](CLASSIFICATION.md).

## Process

### 1. Gather context

For each finding, read the file and surrounding code at the cited location. Read `docs/adr/*.md` in the project for architecture decisions that might explain a seeming defect as intentional. Read `docs/agents/review-knowledge.md` if it exists — it carries FP patterns learned from prior runs.

Run two checks:

- **Scope** — is the cited line part of this MR/PR's diff, or pre-existing code? Pre-existing → 🔵 OOS.
- **Prior FP** — does `docs/agents/review-knowledge.md` already flag this pattern as a known FP?

**Completion criterion**: every finding has a file read, a scope check, and a prior-FP check recorded.

### 2. Recommend a verdict

For each finding, state a verdict with a one-line reason. Present the full table to the user and wait for confirmation before proceeding.

**Completion criterion**: every finding has a verdict + reason, and the user has confirmed.

### 3. Verify the claim

Before any grilling or fixing, check that the finding holds up. This is the step that separates this skill from "just fix everything the bot says."

- For a **bug** claim: reproduce it. Run the code path if reachable; otherwise write a quick test; if neither applies, trace the logic by hand. Report: confirmed (with code path), refuted (with counter-evidence), or insufficient detail.
- For a **standards** claim: check whether the cited standard actually applies. Read the standard doc. Does the code genuinely violate it?
- For a **design** claim: check whether the "better" approach the finding suggests actually fits the codebase's architecture.

A refuted finding becomes ❌ FP with the counter-evidence as reason. An insufficient-detail finding becomes ⏸️ Question.

**Completion criterion**: every ✅ TP and 🟡 Edge finding is resolved — confirmed, refuted (with evidence), or reclassified ⏸️ Question (uncertainty stated). Verified findings carry the evidence in their `reason` field.

### 4. Grill the fix plan

For each verified ✅ TP, grill a fix plan before touching code. Delegate to `/skill:code-review` for a Standards + Spec analysis of the impact surface — what calls this code, what breaks if it changes.

The grill produces a concrete fix plan: what to change, why, and what risk it carries. Present the plan and let the user confirm.

For 🟡 Edge findings, the grill is optional — only if the user chooses "discuss" over "fix" or "skip."

**Completion criterion**: every ✅ TP has a confirmed fix plan. The plan names the change, the risk, and the verification step.

### 5. Fix

Work findings in priority order: 🚨 → ⚠️ → 🟢, then 🟡 Edge (user-selected).

For each finding, offer three options via `ask_user_question`:

1. **Fix** — apply the grilled plan
2. **Discuss** — deeper `/skill:code-review` analysis
3. **Skip** — annotate with `// FIXME:` (real defect, deferred) or `// NOTE:` (design decision, not a defect)

One `ask_user_question` at a time. Wait for the user's choice before acting. Batch instructions from the user override this.

#### Fix path

Delegate to `/skill:implement` with the confirmed fix plan. Do not edit code yourself — that is `/skill:implement`'s job. After `/skill:implement` completes, proceed to Step 6 (Verify).

#### Discuss path

Delegate to `/skill:code-review` for Standards + Spec dual-axis analysis. Present the report + recommended plan. If the finding resolves to FP and the source location lacks a design-intent comment, add a `// NOTE:` explaining why the code looks like a defect but is intentional.

#### Skip path

Annotate the code with the chosen prefix (`// FIXME:` or `// NOTE:`).

**Completion criterion**: every ✅ TP and selected 🟡 Edge has been processed (fixed, skipped, or reclassified). Each processed finding's `resolved` field is set to `true` in the output.

### 6. Verify the fix

Run the project's build and test suite. Detect the toolchain from the project root — `go.mod` → Go, `package.json` → npm/yarn, `Cargo.toml` → cargo, `Makefile` → make — and run the matching commands.

A failed build or test marks the finding's **status** as ❌ fix failed (a status, not a verdict — the verdict stays ✅ TP). The status is recorded in the report.

**Completion criterion**: build + tests pass (status ✅ fixed), or failures are documented (status ❌ fix failed with the failure output).

### 7. Report

Generate `fix-plan-<ID>.md` with a summary table + per-finding detail. Template: [REPORT.md](REPORT.md).

**Completion criterion**: report is generated with final verdicts, actions taken, and verification results.

## Output

The skill produces two artifacts:

1. **classified.json** — the input findings enriched with verdicts, reasons, fix plans, and resolved flags. Consumers (like `/skill:triage-mr`) read this to post labels and resolve threads.

2. **fix-plan-<ID>.md** — human-readable report.

### classified.json format

```json
[
  {
    "discussion_id": "...",
    "classification": "TP|FP|Edge|OOS|Question",
    "reason": "why this verdict",
    "fix_plan": "what to change",
    "priority": "high|medium|low",
    "adr": "docs/adr/NNN-xxx.md",
    "resolved": true
  }
]
```

Field requirements and `resolved` defaults per verdict are defined in [CLASSIFICATION.md](CLASSIFICATION.md). After Step 5, processed TP and Edge are set to `resolved: true`.

## Reflect

After the run, if new FP patterns surfaced, write them to `docs/agents/review-knowledge.md`. If new coding-standard insights emerged, write to `docs/agents/coding-patterns.md`. Skip if nothing new.

## Resuming

If `classified.json` from a prior run exists, load it. Findings already marked `resolved: true` are skipped. Present the state and continue from where it left off.
