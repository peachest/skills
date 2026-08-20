---
name: review-spec
description: Inspect a spec or a set of tickets before handing off to the next skill (to-tickets or implement) — find the gaps and route each to the skill that closes it.
disable-model-invocation: true
---

A route has arrived — a **spec** about to guide `/skill:to-tickets`, or a set of **tickets** about to guide `/skill:implement` — through the terrain. Before anyone traverses it, **inspect** the route. A route that reads complete rarely is: claims drift from their **ground truth**, sources contradict each other silently, and acceptance criteria cover three dimensions when the traverse will touch five. This skill finds those **gaps** and forces them closed.

## Process

1. **Locate the route.** A file path, a tracker issue, or content the user supplies. Read it fully. Identify the **route type**: a spec (traverse = `/skill:to-tickets`) or a set of tickets (traverse = `/skill:implement`). The type shifts Check 3 and Check 5; Checks 1, 2, 4 are route-agnostic.
2. **Gather the terrain data.** The wayfinder map and its tickets — closed decisions, research outputs, prototype results. The project's ADRs, `CONTEXT.md`, and the codebase the route proposes to traverse. Fetch ticket bodies and resolution comments; read prototype outputs and research docs the route cites or depends on. **Done when**: every source the route cites or depends on is read, and its path is listed for the sub-agents.
3. **Spawn five sub-agents in parallel** — one per check below. Each sub-agent gets: the route (path or full text), the **route type**, every terrain-source path it should cross-check against, and the check's body as its brief. For Check 3 and Check 5, pass only the branch matching the route type. Use `runs.all` with five children, `context: 'fresh'` each. List every terrain-source path explicitly in each sub-agent's task text — sub-agents have `context: 'fresh'` and see only what you pass them, so a bare "the terrain sources" with no paths leaves them blind.
4. **Aggregate** the five reports. Present each check's report under its own heading, verbatim or lightly cleaned — the five axes are separate, so each stays on its own heading. The `runs.all` return value already carries each child's `.output` — read it directly from the resolved array; do not `find`/`read` sub-agent session files to locate outputs.
5. **Classify every gap** by the wayfinder ticket type it routes to (see [Gap classification](#gap-classification)).
6. **Report** per check, then the classification table, then a verdict. If gaps exist, ask the user which to route — see [Routing](#routing).

## The five checks

Each check's body is the sub-agent's brief. Each sub-agent reports under 400 words.

### 1 — Ground truth

Every claim, decision, and constraint in the route must trace to a **source** on the terrain: a wayfinder ticket, a research output, a prototype result, an ADR, a code reading, a doc. An unsourced claim is a gap — the route author may have inferred it, or it may have drifted from what the source actually said. A claim that cites a source but misrepresents it is the same gap, worse: it looks grounded and isn't.

For each claim, name the source and quote the supporting passage. If the passage doesn't say what the route says it says, flag it. Report one finding per gap: the claim, the source (or 'unsourced'), the quoted passage, and why it doesn't support the claim.

**Done when**: every claim in the route has a named source with a quoted passage that actually supports it, or is flagged as a gap.

### 2 — Bearing cross-check

The route must not contradict itself or its sources. If research found X, the route can't silently assume the opposite. If two sources disagree — prototype A says profile 0 works, prototype B says it returns an error — the route must **reconcile** them: acknowledge the conflict and resolve it.

Check three directions:
- **Internal** — does the route say one thing in one section and another elsewhere?
- **Against sources** — does the route's account match what the research, prototype, or ticket actually found?
- **Between sources** — where two sources disagree and the route depends on one, does it acknowledge the other?

For each unreconciled contradiction, report: the two passages, the direction, and what the route must say to reconcile.

**Done when**: zero unreconciled contradictions, in any direction.

### 3 — Waymark coverage

Coverage depends on what the route is and what traverses it next.

**Ticket route (traverse = `/skill:implement`):** Acceptance criteria must cover every point the implementation will touch. A route that verifies "discovery works" but never mentions "the mock server must set the new interface method or existing tests panic" has a coverage gap — the traverse will hit the panic and re-open a decision the route should have closed. Cross-check against:
- Every file the route says to modify
- Every interface the route says to change — new methods break mocks, codegen, test helpers
- Every **waymark** (test) the route says to write or update
- Every mock, fixture, or generated code the change touches
- Every ADR the change interacts with

**Spec route (traverse = `/skill:to-tickets`):** The spec must cover every dimension the decomposition will slice along. A spec that names a new interface but never states its contract leaves the decomposition to guess it — a decision re-opened mid-slice. Cross-check against:
- Every test **seam** the spec defines (Testing Decisions) — to-tickets slices around seams; an unspecified seam forces a decision mid-decomposition
- Every module, interface, schema, or API contract the spec adds or changes (Implementation Decisions) — each becomes a slice boundary
- Every wayfinder decision the spec depends on — a decision with no corresponding spec section will be dropped at decomposition
- Every ADR the spec interacts with

For each item with no coverage, report: the item, why the traverse will touch it, and what's missing.

**Done when**: every item above has coverage, or is flagged as a gap.

### 4 — Decision trace

Every decision from the wayfinder tickets must be reflected in the route. A closed ticket that decided "use v2 struct, not v3" but the route only says "call the V function" has a trace gap — the traverse doesn't know which struct version to use, and will either guess or re-open the decision.

Check each closed ticket on the map: is its decision reflected in the route, or did it drop on the way? For each dropped decision, report: the ticket (by name), the decision, and where in the route it should appear.

**Done when**: every closed ticket's decision appears in the route, or is flagged as dropped.

### 5 — Route feasibility

The route must be detailed enough for the next traverse to proceed **without re-opening decisions**.

**Ticket route (traverse = `/skill:implement`):** For each change the route describes, ask: could two competent travelers read this and take materially different paths? A route that says "add error handling" without specifying hard-error vs. fallback has a feasibility gap — the traverse will have to decide, and that decision belongs in the route.

**Spec route (traverse = `/skill:to-tickets`):** For each section of the spec, ask: could two competent decomposers read this and produce materially different ticket sets? A spec that says "add caching" without specifying cache scope, invalidation, and key strategy leaves the decomposition to decide — those decisions belong in the spec, not the tickets.

For each under-specified passage, report: the passage, the ambiguity, and what the route must specify to make the traverse mechanical.

**Done when**: every change description is specific enough that the traverse is mechanical, or is flagged as under-specified.

## Gap classification

Every gap found by the five checks gets classified into one of four wayfinder ticket types. The type determines which skill closes the gap.

| Type | The gap is about… | Routes to | Skill mode |
|------|-------------------|-----------|------------|
| **research** | Knowledge outside the current working directory — an API contract, a third-party behavior, a doc fact the route assumed but no terrain source confirmed. | `/skill:research` | AFK sub-agent |
| **prototype** | "How should it look or behave?" — the route is silent on a shape, interaction, or data structure that a throwaway artifact would clarify. | `/skill:prototype` | HITL |
| **grilling** | A decision the route left open or under-specified — two paths are possible and the route didn't pick. Sharpen it through one-question-at-a-time dialogue. | `/skill:grill-with-docs` | HITL |
| **task** | Manual work that must happen before a decision can be made — provisioning access, moving data, signing up for a service so its API can be judged. Nothing to decide, prototype, or research, but the route is blocked until it's done. | Manual execution (HITL checklist or AFK where the agent can drive) | HITL or AFK |

**How to classify:** read the gap's "what's missing" and ask — is the missing thing a *fact* (research), a *shape* (prototype), a *decision* (grilling), or a *blocking chore* (task)? When a gap could fit two types, pick the one whose skill would most directly close it; note the alternative in the report.

## Report

Present the five check reports under five headings (`## 1 — Ground truth`, etc.), verbatim or lightly cleaned from the sub-agent outputs.

Then a **classification table** — one row per gap:

| # | Check | Gap (short) | Type |
|---|-------|-------------|------|
| 1 | Ground truth | Claim "X supports Y" — source says no | research |
| 2 | Route feasibility | "add error handling" — hard-error vs fallback undecided | grilling |
| … | | | |

End with a verdict:

- **Clear to traverse** — zero gaps. The route can hand off to the next skill (`/skill:to-tickets` for a spec route, `/skill:implement` for a ticket route).
- **Held** — N gaps across M checks. List the classification table. The route must be revised and re-inspected.

## Routing

When the verdict is **Held**, route every gap by its type. **Research, prototype, and grilling gaps must route to their follow-up skills — they cannot be closed by inline revision.** Each requires something inline writing cannot provide: a fact the cwd doesn't contain (research), a shape to react to (prototype), or a one-question-at-a-time decision dialogue (grilling). Offering "revise spec inline" for these types bypasses the very process that closes them — the agent unilaterally picks a path instead of the user deciding. Only **task** gaps (mechanical work — filling an under-reflected decision into the route body, updating a file reference) may be fixed inline.

Ask the user to confirm the routing, grouped by type:

> Found N gaps. Routing plan:
> - research (M gaps) → `/skill:research` (AFK sub-agent): #1, #5
> - grilling (K gaps) → `/skill:grill-with-docs` (HITL dialogue, one question at a time): #2, #7, #9
> - prototype (J gaps) → `/skill:prototype` (HITL artifact): #3
> - task (L gaps) → fix inline or manual checklist: #4, #6, #8
> Confirm to proceed, or adjust the plan.

**After any routed gap is resolved, re-inspect** the revised route — a gap closed by research may surface a new gap in feasibility; only a clean re-inspect clears the route to traverse.

**Execution rules** (the parent session follows these after the user confirms):

- **research** → spawn a `/skill:research` sub-agent (`context: 'fresh'`) with the gap as its question and a path to write findings to. AFK — no human in the loop. Feed the findings back into the route.
- **prototype** → invoke `/skill:prototype` in the parent session (HITL — the user reacts to the artifact). Feed the prototype result back into the route.
- **grilling** → invoke `/skill:grill-with-docs` in the parent session (HITL — one question at a time). Each grilling gap is one decision; the resolved decision goes into the route before the next gap is grilled.
- **task** → fix inline directly (the agent writes the missing content into the route) or hand the user a precise checklist (HITL). Feed any resulting facts back into the route.

This skill inspects, classifies, and routes. The pressure of the report — every gap named, every claim held to its ground truth, every gap tagged with the skill that closes it — is what forces the route to improve. Closing the gaps is the follow-up skills' job, not this skill's.
