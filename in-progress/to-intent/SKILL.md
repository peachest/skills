---
name: to-intent
description: Turn the current conversation into an intent file — product mode writes the repo-root INTENT.md map of stories; effort mode writes a committed intake artifact for one change.
disable-model-invocation: true
---

# To Intent

Synthesize the current conversation into an **intent file** — two modes, two altitudes of the same idea:

- **Product mode (default)** — an `INTENT.md` at the repository root: the product-level source of truth, what is being built, for whom, and what done means (open INTENT.md format v1.0). Do NOT interview the user — synthesize what the conversation already holds. It sits **above** the feature-level cuts: `/skill:to-spec` turns one feature into a spec, `/skill:to-tickets` breaks work into tickets — this file is the map those are cut from. A fresh run writes the first file; a later run is an update pass after verification.
- **Effort mode** — an `intent/<slug>.md` intake artifact for **one change**: what is wanted, why, under which constraints, with open questions. The durable, committed record of a single effort's entry into development; the working artifacts (`.scratch/<slug>/` maps and tickets) stay disposable.

Three altitudes, three artifacts: the product map indexes **stories**, the effort file records **one change's intent**, the `/skill:wayfinder` map charts **decisions**. The story id is the shared token across all three — a wayfinder destination names it, an effort file carries it in frontmatter, the spec and tickets cut from it cite it.

## Process — product mode (default)

If the conversation is about the product as a whole — releases, story cuts, priorities — product mode is the default. If it is about one change or effort, take effort mode (below).

1. **Gather context.** Work from the conversation; explore the repo for the domain glossary if not already explored. **If INTENT.md already exists at the root, this run is an update pass** — read it, re-synthesize against the conversation, and keep the id of every surviving story. Ids are stable forever: an edited story keeps its id; only a replaced story gets a new one. Completed stories drop off the map — tell the user which ones, so the built-versus-planned history is never lost silently.

2. **Draft the four levels of intent.** Each level answers a different question and serves a different downstream use. Draft in this order:

   - **Product** — the problem, who it's for, and why now, in one short paragraph. This is *grounding*: the sentence every downstream decision is checked against.
   - **Release** — sequencing: MVP first, later releases follow. This is *scope control*: an agent asked to build release 1 has a hard boundary.
   - **Story** — one capability from the user's point of view, with priority (must/should/could) and effort (S/M/L). This is the *unit of work*: picked up, implemented, and reported on by id.
   - **Acceptance criterion** — a single verifiable statement of what done means. This is the *unit of verification*: each criterion becomes a check the implementation must pass.

3. **Quiz the user.** Present the draft map: the product brief, the journey line, and the stories grouped by release with priority and effort. Ask:

   - Does the release split match reality — is anything in the MVP actually a later release?
   - Is each priority honest (must / should / could)?
   - Is every *Done when* line independently verifiable — could a checker pass or fail it on its own?

   Iterate until the user approves the map.

   **Fog check:** a story whose *Done when* cannot be sharpened into a single verifiable statement — because the how is still undecided — is **fog**, not a story. Park it in a later release at `could`, or hand its release to `/skill:wayfinder` with the release as the destination: its decision tickets clear the fog, and a later update pass graduates the story to sharp. What stays on this map is only what is buildable as stated.

4. **Write the file.** Write or update `INTENT.md` at the repo root using `<intent-template>`. Omit the Sync section — this file is hand-written, not connected to intentdocs.

5. **Hand off.** Point the user at the next move by the state of the map: a sharp story → `/skill:to-spec`; a foggy release → `/skill:wayfinder` with the release as destination; the map sliced into tracer bullets → `/skill:to-tickets`. Whatever they pick, the story ids travel with it.


## Process — effort mode

When a single effort (a change, a fix, an incident response) needs to enter development, write its intake record instead: `intent/<slug>.md` at the repo root, **committed** — the git history is the governance: author, timestamp, revision trail. Synthesize, do not interview; if the effort is still a loose idea rather than a discussed one, say so and suggest grilling first.

**Write from what the user already stated; verify later.** The user's stated intent (what they want, in what order, under which constraints) is complete intake material on arrival — write it down first. Facts the agent verifies along the way (a model pairing, a resource inventory, a data audit) are **downstream work**: they enter the file as Constraints and Open questions when known, and their full verification belongs to the spec / wayfinder / implementation that follows. An investigation is never a precondition for the file to exist — a 30-minute intake that ends without the file written is a failed run, however good the investigation was.

1. **Gather context — intake only.** Read the product `INTENT.md` if present: an effort cut from a story carries that story's id in frontmatter (`origin: story-<id>`); an effort with no story ancestor records its true origin (`origin: idea | incident | diagnosis | ticket`). This step reads one file and classifies the origin — execution-level investigation (resource checks, compatibility audits, data archaeology) is downstream work, not intake.

2. **Draft the intake.** Four fields, in the originator's terms, per `<effort-template>`:

   - **Problem** — what cannot be done today, who is affected.
   - **Proposed outcome** — what better looks like. This is the line a wayfinder destination or a spec Solution section quotes verbatim.
   - **Constraints** — the boundaries the change must respect (security, external dependencies, no-restart policies). These flow into a wayfinder map's Notes or a spec's Implementation Decisions.
   - **Open questions** — what is genuinely undecided. This section is the **router**: questions already sharp become wayfinder decision tickets directly; questions still unsharp go to the map's Not yet specified.

3. **Quiz the user — on the four fields, not the how.** Confirm Problem, Proposed outcome, Constraints, and the origin. Implementation questions (which pipeline to start, where data lives) belong to the downstream spec or wayfinder session — even when they feel urgent, they are not this quiz. Committing the file is the accept gate — the effort enters development on commit.

4. **Write the file — one of exactly two locations.** The product map `INTENT.md` at the repo root, or the effort file `intent/<slug>.md` at the repo root. There is no third location: a `plans/` directory, a todo list, or the conversation log is **not** persistence — the todo tool is session-scoped by design and loses the intent the moment the session ends. Frontmatter carries `status: draft → accepted → done` — `done` when the change is verified, closing the effort's loop.

5. **Hand off by Open questions.** Empty or all answerable in one sitting → `/skill:to-spec` directly. Questions sharp but unresolved → `/skill:wayfinder` chart: destination from Proposed outcome, first decision tickets from the sharp questions, fog from the rest — the chart's grill is shorter because the intake already did it. Either way the story id (if any) travels with it.

**Loop closure.** When a verified change retires its effort file to `done`, check whether the product map needs an update pass — a completed story drops off `INTENT.md` only there. An incident- or diagnosis-originated effort is maintenance writing back into the loop: its fix proposal arrives as a fresh effort file, not as ad-hoc work.

## Completion criteria

- Every story carries a stable id, a priority, an effort, and at least one *Done when* criterion that is a single verifiable statement.
- Optional sections appear only when they earn their place: a persona exists only if its goals genuinely break ties between two plausible implementations; a journey exists only when the activities form a real spine. Otherwise omit.
- No file paths or code snippets — they go stale fast. Exception: a prototype snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape) — inline it, note it came from a prototype, trim to the decision-rich parts.
- Effort mode: Proposed outcome quotable verbatim downstream, every Open question classified sharp or unsharp, frontmatter origin and status present, and the file committed — not scratch.

<effort-template>

---
origin: story-<8-hex id> | idea | incident | diagnosis | ticket
status: draft
---

# Intent: <slug>

## Problem
<What cannot be done today, who is affected.>

## Proposed outcome
<What better looks like — the line a wayfinder destination or spec Solution quotes.>

## Constraints
<Boundaries the change must respect.>

## Open questions
- <Sharp question — candidate wayfinder decision ticket>
- <Unsharp suspicion — candidate Not yet specified>

</effort-template>

<intent-template>

# INTENT.md
> Hand-written via the to-intent skill. Last updated: <ISO timestamp>

## Product
**<Name> — <one-line positioning>**

<One short paragraph: the problem being solved, for whom, and why now.>

## Personas
### <Name> — <role>
**Goals:** <what they want>
**Pain points:** <what hurts today>

## User journey
<Activity 1> → <Activity 2> → <Activity 3>

## MVP stories — build these first

### <Activity>
**<Story title>** (id: `<8-hex id>`)
*As a <persona>, I want to <capability>, so that <benefit>*
Priority: must | Effort: M
*Done when:*
- <Single verifiable statement>
- <Single verifiable statement>

## Release 2 — <Name>
<Same shape as MVP stories — ### activity, then stories with id, priority, effort, Done when.>

</intent-template>
