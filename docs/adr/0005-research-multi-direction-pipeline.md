# Research skill: multi-direction pipeline, parallel subagents, forked synthesizer

The `research` skill was a single background agent writing one Markdown file. We redesigned it into a five-step pipeline — grill, survey directions, dispatch one subagent per direction (each writing `~/research/<topic-slug>/<NN-slug>.md` with What + How + key findings), then a synthesize subagent merging them into a four-layer `00-summary.md`.

## Considered Options

- **Direction reports carry only What + How + key findings, not So What / Now What.** Those two layers need the commissioning context — audience, constraints, success criteria — that lives only in the main session. A direction subagent given only its sub-topic would hallucinate them; they belong in the synthesis.
- **Synthesizer forks the main session's context rather than running `fresh`.** It needs the full aligned context to write grounded So What / Now What. This deliberately deviates from the "always `fresh` subagents" rule; the role-confusion risk is countered by a strong role prompt — the synthesizer is not the main session, cannot spawn subagents, and only synthesizes.
- **Single agent (the old shape)** was rejected: one agent spanning all directions mixes concerns and cannot parallelize.

## Consequences

We edited the vendored skill at `vendor/mattpocock/skills/engineering/research/` in place, so a future re-vendor overwrites these changes.
