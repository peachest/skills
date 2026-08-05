---
name: review-spec
description: Interrogate a spec from wayfinder before handing off to implement — trace every claim to evidence, reconcile conflicting sources, force acceptance criteria to be exhaustive.
disable-model-invocation: true
---

A spec has arrived — research done, design decisions locked — about to guide `/skill:implement`. Before it does, **interrogate** it. A spec that reads complete rarely is: claims drift from their **evidence**, sources contradict each other silently, and acceptance criteria cover three dimensions when the implementation will touch five. This skill finds those **gaps** and forces them closed.

## Process

1. **Locate the spec.** A file path, a tracker issue, or content the user supplies. Read it fully.
2. **Gather the evidence corpus.** The wayfinder map and its tickets — closed decisions, research outputs, prototype results. The project's ADRs, `CONTEXT.md`, and the codebase the spec proposes to touch. Fetch ticket bodies and resolution comments; read prototype outputs and research docs the spec cites or depends on.
3. **Run the five axes** below in order — earlier axes surface the evidence the later ones check against.
4. **Report** per axis, then a verdict.

## The five axes

### 1 — Evidence

Every claim, decision, and constraint in the spec must trace to a **source**: a wayfinder ticket, a research output, a prototype result, an ADR, a code reading, a doc. An unsourced claim is a gap — the spec author may have inferred it, or it may have drifted from what the source actually said. A claim that cites a source but misrepresents it is the same gap, worse: it looks grounded and isn't.

For each claim, name the source and quote the supporting passage. If the passage doesn't say what the spec says it says, flag it.

**Done when**: every claim in the spec has a named source with a quoted passage that actually supports it, or is flagged as a gap.

### 2 — Consistency

The spec must not contradict itself or its sources. If research found X, the spec can't silently assume the opposite. If two data sources disagree — prototype A says profile 0 works, prototype B says it returns an error — the spec must **reconcile** them: acknowledge the conflict and resolve it.

Check three directions:
- **Internal** — does the spec say one thing in one section and another elsewhere?
- **Against sources** — does the spec's account match what the research, prototype, or ticket actually found?
- **Between sources** — where two sources disagree and the spec depends on one, does it acknowledge the other?

**Done when**: zero unreconciled contradictions, in any direction.

### 3 — Coverage

Acceptance criteria must cover **every dimension** the implementation will touch. A spec that verifies "discovery works" but never mentions "the mock server must set the new interface method or existing tests panic" has a coverage gap — implement will hit the panic and re-open a decision the spec should have closed.

Cross-check acceptance criteria against:
- Every file the spec says to modify
- Every interface the spec says to change — new methods break mocks, codegen, test helpers
- Every test the spec says to write or update
- Every mock, fixture, or generated code the change touches
- Every ADR the change interacts with

**Done when**: every item above has at least one acceptance criterion, or is flagged as a gap.

### 4 — Completeness

Every design decision from the wayfinder tickets must be reflected in the spec. A closed ticket that decided "use v2 struct, not v3" but the spec only says "call the V function" has a completeness gap — implement doesn't know which struct version to use, and will either guess or re-open the decision.

Check each closed ticket on the map: is its decision reflected in the spec, or did it drop on the way?

**Done when**: every closed ticket's decision appears in the spec, or is flagged as dropped.

### 5 — Implementability

The spec must be detailed enough for `/skill:implement` to execute **without re-opening decisions**. A spec that says "add error handling" without specifying hard-error vs. fallback has an implementability gap — implement will have to decide, and that decision belongs in the spec.

For each change the spec describes, ask: could two competent developers read this and produce materially different implementations? If yes, the spec is under-specified.

**Done when**: every change description is specific enough that implementation is mechanical, or is flagged as under-specified.

## Report

For each gap:
- Name the axis
- Quote the spec passage
- Name what's missing — the source, the reconciliation, the dimension, the decision, the specification
- State what the spec must say to close the gap

End with a verdict:

- **Ready** — zero gaps. The spec can hand off to `/skill:implement`.
- **Not ready** — N gaps across M axes. List them. The spec must be revised and re-reviewed.

This skill interrogates and reports. The pressure of the report — every gap named, every claim held to its source — is what forces the spec to improve. Fixing the gaps is the spec author's next step, not this skill's.
