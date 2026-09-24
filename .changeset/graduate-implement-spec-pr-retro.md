---
"mattpocock-skills": minor
---

Graduate **`implement-spec`**, **`pr`** and **`retro`** into the **Engineering** bucket, so they ship in the Claude Code plugin, get docs pages, and are routed by `ask-matt`.

- **`implement-spec`** (user-invoked) implements a whole spec in one run. It reads the tickets as a **task graph**, runs implementer subagents in their own worktrees across the ready **frontier**, and lands everything on one **integration branch**, closing out with `code-review`. Ahead of graduating:
  - The goal is now the integration branch, not a PR. A draft PR opens only when the issue tracker closes work through PRs or you ask for one, and only after the first merge (a branch with no commits ahead of main can't open one). Without a PR, the tickets are resolved the way the tracker closes work.
  - It points at the issue tracker like its siblings, telling you to run `/setup-matt-pocock-skills` when none has been provided, rather than silently defaulting to `gh`.
  - Each implementer confirms its worktree is based on the integration branch, builds its ticket with `tdd`, and merges the integration tip into its own branch before reporting done, so each merge is a fast-forward.
- **`pr`** (model-invoked) is the shape a pull request body should take: a summary as the smallest visual that makes the change clear (pseudocode, a call tree, a file tree, Mermaid, a diff), before/after evidence that it works, and a merge-danger call (one-way or two-way door, plus blast radius). The Summary visuals are adapted from Dex Horthy's `show-me`, credited in the skill's `CREDITS.md`.
- **`retro`** (user-invoked) looks back at a coding session and suggests changes to the agent's environment rather than the code: navigation pointers, automated checks, coding standards, steering files, tool economy, information access. It classifies each coding-standards finding first: a mechanical violation gets a deterministic check (a linter rule, a pre-commit hook, or a CI job), and `CODING_STANDARDS.md` is kept for genuine judgement calls. A repo with no guardrail at all is a finding in its own right.
