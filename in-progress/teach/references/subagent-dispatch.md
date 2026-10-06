# Subagent Dispatch Reference

Dispatch contracts for the teach steps that run as background subagents. Read
when launching a fact-check reviewer, a source-extraction scout, a prototype
worker, or a code-archaeology scout. Launch mechanics (async, fresh context,
keyed runs) follow the pi-subagents skill; this file holds the teach-specific
prompt content.

## What stays with the parent

Arbitration between source layers, provenance labeling, recorded rulings,
lesson prose, pacing, and delivery. A subagent reports evidence; the parent
decides what the learner sees. Reviewer findings are adjudication prompts,
not auto-fixes.

## Lesson fact-check (per lesson, async)

- **Goal**: verify every claim in the lesson against the bronze anchor ledger
  and raw sources; produce `lesson-XXX.factcheck.md`.
- **Target**: the lesson HTML path; the bronze anchors JSON; paper source
  dirs and repo paths named in the ledger.
- **Authority**: read-only. Writes only the factcheck file.
- **Success criteria**: every flagged claim carries (a) the lesson quote,
  (b) the anchor checked, (c) verdict — false / unsupported / imprecise /
  verified, (d) the correction where one is known. Runs the mechanical
  checks (anchor-check, css-self-check) and folds their output in.
- **Stop rules**: a suspected fabrication is reported immediately in the
  receipt's first section, not buried; do not keep digging past the ledger —
  missing anchors are parent adjudication material, not blockage.
- **Receipt shape**: findings count + first-section urgent findings +
  artifact path. The parent adjudicates on arrival; the next lesson waits
  for this receipt.

## Plan fact-check (once per plan, async but blocking)

Same contract, target `PLAN.md`, plus: check the dependency graph for
premise errors (X depends on Y when actually Y depends on X). The parent
does not start teaching until this receipt lands and premises are fixed.

## Source-extraction scouts (new topic, parallel async)

One scout per layer; prompts are distinct by layer, not clones:

- **paper scout**: the tex path; extract the five recurring needs (method
  formulas/hyperparameters, experiment tables, observations, appendix
  material, figure map) each as `tex:<line>` + verbatim excerpt.
- **code scout**: the repo path + commit to pin; extract config tables
  (named by tier — code default / config file / CLI), core data structures,
  and every point where code disagrees with the paper's description, each
  as `<commit>:<file>:<line>`.
- **interpretation scout**: the archived article texts; extract explanatory
  claims marked as interpretation, with article locators.

Authority: read-only, output is a structured markdown excerpt file per
layer. Stop rule: stop when the recurring needs are covered — extraction is
bounded by the checklist, not by curiosity. The parent merges, arbitrates
disagreements, and writes the fact base.

## Prototype workers (interactive component before lesson integration)

- **Goal**: a standalone HTML prototype at a named path, rendering-checked.
- **Target**: explicit output file path; shared `base.css` path; the source
  concept and constraints (standalone except base.css, no iframe).
- **Authority**: writes only the prototype file and its render-check
  artifacts.
- **Success criteria**: render check passes (0 JS errors, geometry checks);
  the interaction described in the dispatch works.
- **Report budget**: short receipt (path + check results + one-line design
  note). Long reading lists in the prompt blow the output budget — name the
  three files that matter, not the terrain.
- **Parent**: integrates the prototype inline (never iframe), runs the
  interactive-state check, then retires or untracks the prototype file.
  Sync dispatches for build tasks have failed in practice; launch async.

## Code archaeology (as needed, async when heavy)

- **Heavy** (multi-file hunts, history archaeology, cross-repo tracing):
  async scout with goal/authority/stop rules as above; output is evidence
  lines with commit-anchored citations.
- **Light** (a config value, a function's behavior, counting a structure):
  the parent greps and reads directly — dispatch overhead exceeds the work.
- **Acceptance rule**: the parent re-runs the evidence chain (grep the
  cited lines, check the commit) before the conclusion enters a lesson or a
  ruling. A scout's summary is a lead, not a fact.

## Scheduling rules

- Lesson fact-check: one in flight per lesson; the next lesson's dispatch
  may overlap the previous receipt's adjudication, but the next lesson's
  *delivery* waits for the receipt.
- Scouts: parallel across layers is the point; do not run two scouts on the
  same layer.
- Every dispatch gets a stable key so receipts are addressable
  (`factcheck-0005`, `scout-paper-eagle2`).
