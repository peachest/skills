---
name: deslop
description: >
  Bilingual (中文+English) AI-slop audit and fix with machine-verified
  acceptance. Audit-first scoring decides whether a rewrite is warranted;
  every hit is adjudicated (load-bearing stays, decorative gets a minimal
  fix); conservation of quotes/numbers/hedges/structure is machine-checked.
  Use when asked to 去AI味/去 AI 味/清理 AI 味/改写 AI 味/deslop/de-slop an
  existing document, to audit prose for AI writing patterns (审计 AI 味/slop
  audit), or when a rewrite produced by another skill needs acceptance
  checks. For prose generation-time style rules use the writing skill at
  hand instead; for full English controlled-language rewrites use the
  ste100 skill.
---

# deslop

Fix the form of AI-flavored prose without touching its content. The loop:

```
audit (read-only)  →  verdict  →  adjudicate + fix  →  verify (machine gate)
```

Four leading words carry the contract: **audit-first** (score before any
edit), **flag** (a hit awaiting adjudication — a flag never authorizes an
edit by itself), **conservation** (information survives the rewrite), and
**receipt** (every edit maps to a rule id and every claim matches the diff).

## Hard boundaries

- **Form, never content.** A linter can turn a hollow paragraph into tidy,
  confident hollow prose. Hollow content is a different problem and out of
  scope here.
- **Conservation.** Quotes, numbers, dates, names, sources, causal claims:
  nothing added, nothing removed. Hedges and concessions (可能/通常/据说/
  may/perhaps) stay; tonal strength stays put. Machine gate below.
- **Unmatched text stays verbatim.** Rules are a whitelist; an edit that
  cites no rule id is a contract violation.
- **Off-limits genres** — marketing copy and writing that needs a personal
  voice: run the audit, deliver the report, decline the rewrite. Controlled
  language applied to poetry is a torque wrench on a poem.

## Modes

| mode | applies to | rule surface |
|------|------------|--------------|
| **strict** | procedures, error messages, agent output, runbooks | full rule set + hard caps; en additionally runs the ste100 checker |
| **flavor** (default) | reports, docs, blog prose | machine-auditable subset; expressiveness stays |
| **off-limits** | marketing copy, personal voice | audit only, no rewrite |

Rule packs: [references/rules-zh.md](references/rules-zh.md) (lieflat
corpus-validated zh rules) · [references/rules-en.md](references/rules-en.md)
(ASD-STE100 mechanical subset). Read the pack for the language(s) of the
target document before adjudicating.

## Steps

### 1. Audit-first

```bash
python3 <SKILL_DIR>/scripts/audit.py <file.md> [--mode strict] [--json]
```

Read the hit table and the verdict. **Done when**: you hold the per-rule hit
counts and a verdict in hand.

### 2. Verdict gate

`verdict: skip: below floor` → stop. Deliver the report and say why a
rewrite is not warranted (measured floor: flags and dash-density thresholds
in `scripts/audit.py`, calibration notes in the rule packs). Override only
with the user asking explicitly, then say `--force` was used. A batch of
documents with sub-floor scores gets no rewrite workers at all — this gate
is the cheap version of every wasted-dispatch story.

Genre check: off-limits genre → report only, stop.

**Done when**: every document in scope is marked skip / off-limits /
rewrite, and the marked-rewrite set is non-empty only if the audit says so.

### 3. Adjudicate + fix

Work through the flags one by one. Each flag gets exactly one of:

- **kept** — load-bearing (mathematical 恰好, safety 永远, a
  term——definition dash, a real concession). Record the retained example:
  rule id + line + one-line reason.
- **fixed** — decorative. Minimal edit resolving that rule only; the fix
  cites the rule id. Adjacent text stays untouched.

For discretionary rules (zh 破折号/冒号, en em-dash/modals) adjudicate each
occurrence; keeping zero under a discretionary rule requires the zero to be
explicit. A paragraph that keeps reading as same-shape sentences after the
machine flags are cleared is a human-only check (ZH-3 / synonym rotation) —
read the paragraph, then decide.

Batch branch — dispatch subagents only when hits × document size makes
inline work the slower path: one section per worker, the section text plus
the rule pack in the prompt, and a receipt per
[references/receipt-format.md](references/receipt-format.md). Cross-check
every receipt against the diff before accepting; claimed-but-absent and
unclaimed edits void the run, and a worker returning unchanged text against
nonzero audit hits is an invalid run, not a clean one.

**Done when**: every flag in the audit table has a kept or fixed entry with
a rule id, and the diff contains no edit without one.

### 4. Verify (machine gate)

```bash
python3 <SKILL_DIR>/scripts/conservation.py <orig> <new>   # exit 0 required
python3 <SKILL_DIR>/scripts/audit.py <new>                 # re-score
```

- conservation exits 1 → restore what was lost, re-verify. This gate is
  non-negotiable: it is the machine version of "every substantive word
  traces to the original".
- Re-audit: targeted rules drop, previously-clean rules did not light up.
  Punctuation-class fixes (ZH-4/ZH-5/ZH-5b/EN-2/EN-7) above 50% of all
  fixes → back to step 3: the content-rule flags were dodged, adjudicate
  them.
- **Done when**: conservation passes, the re-audit shows the targeted
  improvement, and every flag from step 1 is accounted for as kept or fixed.
  The completion criterion is full adjudication — a zero-flag output is a
  collapse symptom, not a pass.

## Calibration

Thresholds live in `scripts/audit.py` (`FLOOR_PER_100`,
`DASH_DENSITY_PER_100_LINES`) and are calibrated on real before/after
rewrite pairs, the same way teach's dash density was (slop 30.3 vs clean
23.6 per 100 lines). When a rule fires on text a human reader calls clean,
or stays silent on text a human calls slopped, recalibrate on that pair and
note the pair in the rule pack — rule text stays, numbers move.
