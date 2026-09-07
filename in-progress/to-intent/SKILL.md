---
name: to-intent
description: Turn the current conversation into an INTENT.md at the repo root — the product-level map of what's being built, for whom, and what done means, in the open INTENT.md format v1.0.
disable-model-invocation: true
---

# To Intent

Synthesize the current conversation into an **INTENT.md** at the repository root — the product-level source of truth: what is being built, for whom, and what done means. Do NOT interview the user — synthesize what the conversation already holds.

INTENT.md sits **above** the feature-level cuts: `/skill:to-spec` turns one feature into a spec, `/skill:to-tickets` breaks work into tickets — this skill writes the map those are cut from. It is the Intent Loop's first and last stop (Intent → Specification → Plan → Implementation → Verification → Updated intent): a fresh run writes the first file, a later run updates it after verification.

No issue tracker is involved — the file is the artifact, committed at the repo root like any other.

Two maps, two altitudes: this file maps **stories** — what to build and what done means. A `/skill:wayfinder` map charts **decisions** — what must be settled before someone can build. The story id is the shared token between them: a wayfinder destination names it, the spec and tickets cut from it cite it.

## Process

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

## Completion criteria

- Every story carries a stable id, a priority, an effort, and at least one *Done when* criterion that is a single verifiable statement.
- Optional sections appear only when they earn their place: a persona exists only if its goals genuinely break ties between two plausible implementations; a journey exists only when the activities form a real spine. Otherwise omit.
- No file paths or code snippets — they go stale fast. Exception: a prototype snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape) — inline it, note it came from a prototype, trim to the decision-rich parts.

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
