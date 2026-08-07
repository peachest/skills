---
name: review-spec
description: Inspect a route from wayfinder before handing off to traverse — trace every claim to ground truth, cross-check bearings, force waymark coverage to be exhaustive.
disable-model-invocation: true
---

A route has arrived — decisions locked, map charted — about to guide `/skill:implement` through the terrain. Before anyone traverses it, **inspect** the route. A route that reads complete rarely is: claims drift from their **ground truth**, sources contradict each other silently, and acceptance criteria cover three dimensions when the traversal will touch five. This skill finds those **gaps** and forces them closed.

## Process

1. **Locate the route.** A file path, a tracker issue, or content the user supplies. Read it fully.
2. **Gather the terrain data.** The wayfinder map and its tickets — closed decisions, research outputs, prototype results. The project's ADRs, `CONTEXT.md`, and the codebase the route proposes to traverse. Fetch ticket bodies and resolution comments; read prototype outputs and research docs the route cites or depends on.
3. **Run the five checks** below in order — earlier checks surface the ground truth the later ones verify against.
4. **Report** per check, then a verdict.

## The five checks

### 1 — Ground truth

Every claim, decision, and constraint in the route must trace to a **source** on the terrain: a wayfinder ticket, a research output, a prototype result, an ADR, a code reading, a doc. An unsourced claim is a gap — the route author may have inferred it, or it may have drifted from what the source actually said. A claim that cites a source but misrepresents it is the same gap, worse: it looks grounded and isn't.

For each claim, name the source and quote the supporting passage. If the passage doesn't say what the route says it says, flag it.

**Done when**: every claim in the route has a named source with a quoted passage that actually supports it, or is flagged as a gap.

### 2 — Bearing cross-check

The route must not contradict itself or its sources. If research found X, the route can't silently assume the opposite. If two sources disagree — prototype A says profile 0 works, prototype B says it returns an error — the route must **reconcile** them: acknowledge the conflict and resolve it.

Check three directions:
- **Internal** — does the route say one thing in one section and another elsewhere?
- **Against sources** — does the route's account match what the research, prototype, or ticket actually found?
- **Between sources** — where two sources disagree and the route depends on one, does it acknowledge the other?

**Done when**: zero unreconciled contradictions, in any direction.

### 3 — Waymark coverage

Acceptance criteria must cover **every point** the traversal will touch. A route that verifies "discovery works" but never mentions "the mock server must set the new interface method or existing tests panic" has a coverage gap — the traverse will hit the panic and re-open a decision the route should have closed.

Cross-check acceptance criteria against:
- Every file the route says to modify
- Every interface the route says to change — new methods break mocks, codegen, test helpers
- Every **waymark** (test) the route says to write or update
- Every mock, fixture, or generated code the change touches
- Every ADR the change interacts with

**Done when**: every item above has at least one acceptance criterion, or is flagged as a gap.

### 4 — Decision trace

Every decision from the wayfinder tickets must be reflected in the route. A closed ticket that decided "use v2 struct, not v3" but the route only says "call the V function" has a trace gap — the traverse doesn't know which struct version to use, and will either guess or re-open the decision.

Check each closed ticket on the map: is its decision reflected in the route, or did it drop on the way?

**Done when**: every closed ticket's decision appears in the route, or is flagged as dropped.

### 5 — Route feasibility

The route must be detailed enough for `/skill:implement` to traverse **without re-opening decisions**. A route that says "add error handling" without specifying hard-error vs. fallback has a feasibility gap — the traverse will have to decide, and that decision belongs in the route.

For each change the route describes, ask: could two competent travelers read this and take materially different paths? If yes, the route is under-specified.

**Done when**: every change description is specific enough that traversal is mechanical, or is flagged as under-specified.

## Report

For each gap:
- Name the check
- Quote the route passage
- Name what's missing — the source, the reconciliation, the waymark, the decision, the specification
- State what the route must say to close the gap

End with a verdict:

- **Clear to traverse** — zero gaps. The route can hand off to `/skill:implement`.
- **Held** — N gaps across M checks. List them. The route must be revised and re-inspected.

This skill inspects and reports. The pressure of the report — every gap named, every claim held to its ground truth — is what forces the route to improve. Fixing the gaps is the route author's next step, not this skill's.
