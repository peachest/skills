---
name: challenge-audit
description: Audit the quality of review findings themselves before acting on them — invented gaps, collective misses, misrouting, premature verdicts. Use when a review report (review-spec, code-review, ocr, triage-mr) is about to drive work, its verdict looks too good or too harsh, or the user says 挑战评审意见 / 意见可信吗 / audit the review.
---

## Why this exists

A review report is itself a set of claims. Reviewers invent gaps, misquote sources, miss the same hole collectively, and declare passes early. Every downstream skill (`fix`, `implement`, revision rounds) inherits those defects — paying for phantom work or shipping past real holes. This skill spends one audit pass to price the report before spending many passes acting on it.

**Division of labor**:

| Skill | Unit of work | Question it answers |
|---|---|---|
| **fix** | one finding | Is this single claim true, and what fixes it? |
| **challenge-audit** | the whole report | Can I trust this reviewer at all, and what did it miss? |
| **challenger** (agent) | a design artifact | Where is this spec / ADR itself wrong? |

Run this first when report trust is in doubt. Findings that survive route to `fix` (serial, main session) or `challenge-and-fix` (per-finding adversarial subagents, many findings).

## Process

### 1 — Assemble the three layers

Collect, as paths for cross-reading (if a round's reports live only in a compacted session, consolidate them — findings, classifications, rulings — into one findings document on disk first; the audit needs a cross-examinable artifact, not reconstructed memory):

- **Reports under audit** — every round, verbatim, including closure claims ("全部已收口", "fixed in commit X").
- **The reviewed target** — post-revision state, since closures claim edits landed there.
- **Terrain sources** — everything the reports cite as authority: specs, ADRs, research docs, the canonical issue.

**Completion criterion**: all three layers listed with paths; every closure claim in the reports is identified (they get special treatment in axis A).

### 2 — Attack along four axes

One pass per axis. **Evidence first**: a finding without a citable location in report + target + terrain is noise — cut it. Under 800 words total.

- **A — Invented or distorted findings**. For each gap the report claims, trace report → cited source → quoted passage. A gap whose source doesn't say what the report says is **invented**; one whose source says less than claimed is **distorted**. Attack each ruling's *justification* too — a ruling can stand while its stated reason is wrong (session 01a11f50: the setter ruling survived, but its "a wrapper is no simpler" rationale was falsified; the real cause was a pointer-bound gRPC registration no wrapper could ever shadow). Special target: **closure claims** — re-verify each "fixed" item in the target text itself. Recurring defect: the fix landed in one site of the file while a sibling line with the same defect stayed (same-file siblings are where verified-but-unlanded hides).
- **B — Collective misses**. What did every reviewer pass over? Reviewers scanning file-by-file systematically miss **cross-file ownership holes** — a decision with no owner because each reviewer only checked their own assignment list. Sweep the source of truth section by section: does every commitment land somewhere in the target? Misses of *structural ownership* (who executes this) outweigh missed field details.
- **C — Misclassification**. Findings routed to the wrong handler: escalated to a user decision when sources could be mechanically reconciled against each other (the authoritative-source declaration in the terrain itself settles it), or demoted to mechanical when a real choice exists. Count escalation waste — every grilling-that-was-a-lookup is process cost.
- **D — Verdict soundness**. Attack the report's own conclusion (pass / hold / clear-to-proceed). Would the next stage re-open decisions the verdict said were closed? Is the residual-risk list honest about what was deferred, or does it bury a must-close item?

**Completion criterion**: each axis has findings with grade + evidence, or an explicit "axis empty".

### 3 — Price the report

Score trust 0–100 from the axes: invented-finding rate (axis A) and verdict soundness (axis D) weigh heaviest; misses (axis B) lower it only when they touch must-close items. State the score with its drivers in one line each. A score is a decision input, not a verdict — pair it with a recommendation:

- **放行** — axes empty or C-level only.
- **有条件放行** — gaps exist but all close mechanically against the sources, needing no new decisions. List the mechanical closes; they do not re-open the full review.
- **驳回** — invented findings or unsound verdict touch load-bearing claims; the report must be regenerated, not patched.

**Completion criterion**: score + drivers + recommendation, each mechanically derivable from the findings table.

### 4 — Land the closes

For 有条件放行, parent (you) verifies each close against the sources **before** editing — the auditor's claim is also a claim; 9/9 verified is the observed base rate when the auditor is another agent, and refuting first is cheaper than re-reverting. Land edits, sync every mirrored copy (report repos drift the moment one copy lags), and record the audit trail where the review canon lives.

## Output format

```
## Findings

### [Grade] title
- **Where**: report line + target/source location.
- **Conflict**: what the report says vs what the source/target says.
- **Demand**: a question the report owner closes with accept / partial / rebut-with-evidence.

### Summary
- N findings (a A / b B / c C), axes empty listed explicitly.
- Trust score + drivers.
- Recommendation: 放行 / 有条件放行 / 驳回, with the close list.
```

**Grades**: **A** — report contradicts its own sources or its closure claims (trust broken). **B** — collective miss on a must-close item. **C** — process waste (misrouting, missing annotation) or a miss on deferrable detail.

## Working rules

- **Parent verifies before landing.** The audit is findings, not edits; every close is re-checked against sources by the session that acts.
- **One audit pass, then act.** Re-audit only when the report itself changes; challenge the delta plus any prior rebuttal now breakable.
- **Attack-only toward the report** — target edits happen in step 4 as closes, never as auditor improvisation.
- Round ≥ 2 audits challenge only what changed since the last round, plus closure claims from that round (a "fixed" that didn't land is an A).
