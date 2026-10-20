---
name: knowledge-point-extraction
description: Extract a domain model (glossary terms + technical decisions) from research sources — papers, tech blogs, research briefs, survey documents. Use when distilling a paper into structured knowledge, building a coverage matrix across sources, extracting terms/decisions from tech reports or blog posts for a course or research project, or onboarding a new paper into a knowledge base. Covers the two-phase multi-worker pipeline, layer tagging, negative-space routing, and sampling strategies.
---

# Knowledge-Point Extraction

Extract a domain model from a research source the way a domain-modeling skill
extracts one from a codebase: glossary terms with precise definitions and
anchors, plus ADR-style technical decisions. This skill adapts that lens to
**research sources** — papers (LaTeX/PDF), tech reports, blog posts, research
briefs — where there is no codebase to cross-reference and no live user to
challenge.

Consumers: course builders (lesson fact bases), knowledge-base curators
(okb ingest), research onboarding (new-paper triage). The extraction output
is a **fact base**: every claim anchored, every gap routed, every term
layer-tagged — ready for downstream verification or lesson writing.

## Source triage first

Before extracting, classify the source — it determines the lens:

| Source type | What dominates | Layer axis |
|---|---|---|
| Paper (LaTeX/PDF) + official code | method terms, mechanisms, hyperparameters | `[paper-only|code-only|both]` |
| Paper, no code released | method terms, empirical claims | `[paper-only]` only — code-anchored claims are impossible, record "no released code" as negative space |
| Tech report (not peer-reviewed) | engineering decisions, unreleased details | `[tech-report]` — lower verification bar than paper, mark it |
| Blog post / talk / research brief | interpretation, synthesis, positions | `[interpretation]` unless it cites a primary source — then cite that source inline |
| Vision document / roadmap | forward-looking vocabulary with no implementation | `[vision]` — do NOT force into paper/code values |

The layer tag answers "where does this knowledge come from", which drives
later arbitration (paper > code > interpretation is the common order — but
use whatever order your consuming skill defines).

## Two-phase pipeline (for sectioned sources)

For a paper or long document with sections, run extraction as a two-phase
multi-worker pipeline (field-validated: three-strategy comparison on one
paper, 16 workers total — two-phase won on union size 81 vs 73/76 and cut
cross-worker duplicate definitions 15→2).

**Phase A — seed (framing sections only, one worker).** Read the abstract,
introduction, and related-work sections. Extract every term the framing
establishes — the paper's own coinages AND the inherited vocabulary it
relies on (later workers need both to recognize inherited terms and skip
re-deriving them). Each term: canonical name + precise definition +
`file:line` anchor + lineage cite (which prior work, where the source says
so) + layer tag.

Then the routing step that makes the pipeline work: every framing-level
claim that is **asserted but not defined** gets an explicit deferral route —
`[deferred to <section>]`. Field result: 8 deferrals routed, all closed
correctly downstream; the one true paper-wide gap (a guarantee asserted but
never defined anywhere) was carried and flagged across all downstream
workers instead of being silently dropped. This is how code-only designs
(defined in the repo, absent from the paper) get caught instead of
surfacing months later from a learner's question.

**Phase B — sections (one worker per section group, seeded).** Each worker
receives the seed glossary in its prompt. Rules:

- Seed terms are referenced `[seed]` — never re-defined.
- Mechanism details that sharpen a seed term: `[extends: <seed term>]`.
- New terms and section decisions: extract normally.
- Negative space: close the seed's routed deferrals, add your own.

Field result: cross-worker duplicate definitions dropped from 15
(unseeded section-parallel) to 2 (legitimate extends).

**Merger.** Seed is canonical. Extends hang off their seed terms. A term
defined twice with different definitions is a **conflict marker** for
adjudication — resolve with your layer-arbitration rule, record the ruling.

## Sampling strategy

| Extraction target | Strategy | Evidence |
|---|---|---|
| Decisions/ADRs | whole-source, single pass | decision skeletons were 4/4 stable across repeated runs |
| Glossary terms | two-phase pipeline; for high-value sources, add N-sample rounds and merge by frequency | single-pass recall was 47%; four-sample union +115% |
| Negative space | runs with glossary (section workers see their own slice's gaps) | section-parallel produced 57 vs 38 negative-space items |

Merging N samples: frequency = confidence. Terms in every sample form the
stable core (direct to matrix); terms in one sample only are marginal
(second-pass confirm or discard). Measure before assuming — the stable core
was as small as 9–10 terms per source in field runs.

## Negative space

Extract what the source does **not** say with the same discipline as what
it does: undefined terms, absent mechanisms, explicit rejections, deferred
work, symbol collisions. In field runs this was 44 items across five sources
— including a guarantee asserted in the abstract but defined nowhere (the
single most valuable finding). Route each negative-space item:
`[deferred to <section>]`, `[rejected: <alternative>]`, or
`[undefined: paper-wide gap]`.

## Layer-tag remap for non-paper sources

The four-value layer axis (`paper-only / code-only / both / interpretation`)
assumes a paper+code pair. Other source types need the axis remapped to the
source's own structure — record the remap in the glossary header:

- Survey/brief: remap to "the studied system's spec vs implementation axis",
  note that most terms are [interpretation] with inline primary-source cites
- Vision document: `[vision]` tag; the four standard values do not fit
- Multi-report corpora: cite report-number §section, flag that
  `[primary]` means "that section cited a primary source" (not that every
  number was re-verified against it)

## Anchors

Every term and decision carries a source anchor. For LaTeX sources:
`file:line`. For briefs: `report §section`. For blogs: article locator.
Anchors must be re-checkable — a fact-check pass re-reads the cited line
and expects the claim there. Never cite a line you did not read.
