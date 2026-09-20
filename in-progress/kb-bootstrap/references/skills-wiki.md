# Skills wiki — bootstrap reference

The skill-execution knowledge layer (patterns / skill-impact / run logs per skill, cross-skill regularities, source ledger) ships **with the skills repo itself** (`wiki/` beside the skills). There is no standalone scaffold to run.

## Bootstrap actions

1. Ensure the skills repo is cloned and its `AGENTS.md` wiki conventions pointer is in place (it ships with the repo — verify, don't rewrite).
2. Cold start happens on use: the first `skill-call-diagnose` run for any skill creates `wiki/<skill>/` (patterns.md, skill-impact.md, logs.md) per its step 5.5.

Done when one diagnose run has executed and its wiki dir exists. All maintenance (pattern merging, closure, impact ledger) belongs to `skill-call-diagnose`.
