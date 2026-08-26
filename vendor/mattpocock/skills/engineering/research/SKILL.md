---
name: research
description: Investigate a question against high-trust primary sources — split into per-direction reports written by parallel subagents, then a synthesized four-layer summary. Use when the user wants a topic researched deeply across several directions, docs or API facts gathered, or reading legwork delegated to subagents.
---

A research question is rarely one direction. Split it into **directions** — independent sub-topics, each researched by its own subagent — then **synthesize** them into one summary. Each subagent's job stays small and coherent (separation of concerns); the cross-direction synthesis stays in one place.

## Pipeline

1. **Grill.** Run `/skill:grilling` to align the research question, scope, audience, and success criteria with the user. Nothing is researched until these are settled.
2. **Survey directions.** Shallowly survey primary sources to enumerate candidate **directions** — the independent sub-topics worth deep research. Present the list to the user for confirmation (add / drop / merge).
3. **Lay out files.** Decide the **topic-slug**, the numbering, and the output directory (default `~/research/<topic-slug>/`). Each direction gets `NN-slug.md`; the synthesis gets `00-summary.md`.
4. **Dispatch direction subagents.** One subagent per direction, in parallel. Each writes its own `NN-slug.md` — **What + How + key findings only**, every claim cited to its source. Direction subagents do **not** write So What or Now What: those layers need the commissioning context only the main session holds, and a subagent given just its sub-topic would hallucinate them.
5. **Synthesize.** Dispatch one **synthesize** subagent to read every `NN-slug.md` and write `00-summary.md` — the four-layer report, reconciling contradictions across directions and opening with a direction index.

## Primary sources

Every claim traces back to a **primary source** — official docs, source code, specs, first-party APIs — not a secondary write-up of them. Follow each claim back to the source that owns it.

## The synthesize subagent

The synthesizer **is not** the main session: it cannot spawn subagents, cannot grill, and does not decide directions. It only synthesizes. Launch it **inheriting the main session's context** (fork) so its So What / Now What layers are grounded in the real aligned context, and open its task with a strong role prompt: "You are the synthesize subagent, not the main session. You may not spawn subagents. Your only job is to synthesize the direction reports into the four-layer `00-summary.md`."

## Report structure

- **Direction report** (`NN-slug.md`) — What + How + key findings, each claim cited.
- **Synthesis** (`00-summary.md`) — all four layers (What / How / So What / Now What), contradiction-reconciled, opening with a direction index.

Both per [`references/report-structure.md`](references/report-structure.md).
