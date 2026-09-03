# ADR-0004: Provenance callouts and the socratic → quiz → quest retrieval rhythm

Date: 2026-09-02

## Status

Accepted

## Context

Research on LIEGGEGG/little-experiments (the TA Adventure skill,
`source-first-interactive-book-adventure` v3.1) surfaced two gaps in teach:

1. **Provenance visibility.** OKB layers knowledge strictly
   (bronze→silver→gold), but lessons did not inherit the layering in
   presentation: AI-derived analogies, mental models, and scenarios sat
   unlabeled next to source-grounded claims. The learner could not tell
   "the source says" from "the AI explains". OKB's gold verification
   already covers TA's evidence-before-content discipline upstream, so the
   remaining gap is purely presentational.

2. **Quiz was the only retrieval instrument.** `quiz.js` (multiple choice)
   tests recognition. Nothing tests free recall — the effortful retrieval
   that builds storage strength — and nothing requires practice to produce
   an observable outcome. TA's chain (Socratic question + hint + reference
   answer → source-bound quiz → observable quest) fills both.

## Decision

1. **Callout ↔ provenance mapping** (no new classes; existing callouts gain
   a second semantic role):
   - SOURCE claims → `.callout-note`, title `Source`/`原文要点`, claim-level
     footnotes to OKB notes.
   - EXTERNAL material → `.callout-note`, title prefixed `外部 · External`;
     never mixed with or silently replacing SOURCE.
   - DERIVED (AI analogies/mental models/scenarios) → `.callout-tip`, title
     ends with `· AI 衍生`.
   - Derived content never masquerades as source.

2. **New `assets/socratic.js`** component: question → hidden hint →
   reference answer. The hint points to source clues and must resolve the
   question — a hint that poses another vague question is a defect. Reveal
   is one-way; hint (purple) and answer (green/success) styles live in
   base.css.

3. **`quiz.js` gains an optional `misconceptions` array** parallel to
   `options`: entry i names the misconception that picking option i
   exposes. Wrong-answer feedback shows the diagnosis, making a wrong pick
   teach what to fix. Backward compatible — pure-string options lessons
   render unchanged.

4. **Retrieval rhythm in SKILL.md**: lesson practice is a three-stage
   ladder — socratic recall (storage strength) → quiz with misconception
   diagnosis (fluency + diagnostic signal) → quest with an observable
   outcome (transfer). Wrong-answer misconceptions are written into the
   session log so the next Probe starts from the diagnosed gap.

## Consequences

- Lessons gain two linked diagnostics: socratic reveals recall failure,
  quiz misconceptions reveal the specific confusion. Both feed
  UNDERSTANDING-MAP via the session log.
- Distractor authoring is now harder (each must be a plausible
  misunderstanding, not a throwaway) — this is the point; guessable
  distractors waste the diagnostic.
- TA's visual system (pixel RPG, XP, multi-ending), READ/MAP/GRAPH views,
  and public/review build separation were evaluated and **rejected**:
  teach is an agent-in-the-loop service, not a standalone product.
- Follow-up candidate (not decided): a mechanical quiz anti-pattern check
  (correct answer not systematically longest, correct position not
  clustered) in the style of css-self-check.py.
