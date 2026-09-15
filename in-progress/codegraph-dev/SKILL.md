---
name: codegraph-dev
description: Deep-integrate CodeGraph into the local skill ecosystem — index lifecycle (init/sync/git hooks), per-stage hooks for wayfinder charts, to-spec/to-tickets grounding, implement/fix pre-edit blast radius, and a peer-verified post-change verification pass (affected + impact gap checks). Use when working in any project with or deserving a .codegraph index, when a spec/ticket/chart needs grounding in real code, when exploring an unfamiliar area before changing it, when verifying a finished change for missed blast radius, or when a codegraph command fails or looks stale.
---

# codegraph-dev

Deep integration of CodeGraph into the local skill ecosystem: index lifecycle, per-stage hooks for wayfinder / to-spec / to-tickets / implement / fix, and a peer-verified post-change verification pass. Use when working in any project that has (or deserves) a `.codegraph/` index, when a wayfinder chart / spec / ticket needs grounding in real code, when exploring an unfamiliar area before changing it, or when verifying a finished change for missed blast radius. Also use when a codegraph command fails unexpectedly or its output looks stale.

## Index lifecycle

- Bootstrap once per project: `codegraph init` at the repo root. Check freshness with `codegraph status -j`.
- Keep it fresh: `codegraph sync -q` after commits — the `-q` flag exists for git hooks (post-commit / post-checkout).
- Addressing: MCP tools (`codegraph_*`) take `projectPath`; CLI subcommands take `-p <path>` or run from the repo.
- No `.codegraph/` in a non-trivial project → offer to init before deep work. Every hook below assumes an index.

## Ecosystem hooks

Load this skill alongside the ecosystem skill at work; run the hook at the named stage.

| Stage | Hook | Why |
|---|---|---|
| `orient` / new project | `codegraph files --format tree` then `codegraph explore <area>` | module index + internals in one pass |
| `wayfinder` chart (Discovery routing, fog) | `codegraph context "<decision question>" --no-code`, `codegraph explore <area>` | ground each fog item and decision ticket in real symbols, not vibes |
| `wayfinder` decision ticket (cost of reversal) | `codegraph impact -d 3 <symbol the decision touches>` | blast radius is the objective cost-of-reversal input |
| `to-spec` (Problem / Solution / Implementation Decisions) | `codegraph context "<feature>"`, `codegraph callers/callees <interface symbol>` | every file/symbol claim in the spec cites the index, not memory |
| `to-tickets` step 2 (explore codebase) | `codegraph files --filter <dir>`, `codegraph explore <slice keywords>` | slices name real symbols; acceptance criteria become passCheck-able |
| `implement` / `fix`, before editing | `codegraph node <symbol>` / `codegraph impact -d 2 <symbol>` | see caller/callee trail and blast radius *before* the diff exists |
| `implement` / `fix`, after editing | **Post-change verification pass** (below) | catch what self-review misses |
| `code-review` / `mr-review` | `affected` for review scope; `context` for the PR's design-context paragraph | reviewer enters the diff with the dependency graph in hand |

## Post-change verification pass

Run this before claiming a change complete. Both steps caught real misses the agent's own diff review missed (see `references/recipes.md`).

1. `codegraph sync` — index must reflect the working tree, not the last commit.
2. `git diff --name-only <base>...HEAD | codegraph affected --stdin -q` → the test files that the change touches by dependency. **Any entry not in your diff and not deliberately untouched is a gap** — find out why before declaring done.
3. `codegraph impact -d 3 <key struct/config symbol you changed>` → consumers of what you changed. Same gap rule: an entry you didn't consider is a finding, not noise.

## Rules

- Codegraph findings outrank recall. "I already handled X" is not an answer to an `affected`/`impact` hit — verify against the diff.
- `affected` returns a conservative dependency closure. Filter by crate/module for the set that actually executes your change; don't run all of it blindly.
- Symbol search can miss literal constants and generated names — fall back to grep for those, not the other way round.
- Rust macros and generic expansion are analyzed coarsely: cross-crate hits from `impact` are file-level associations, not precise call chains. Verify before acting on them.
- Architecture tours have their own skill (`architecture-explorer`) — this skill is about the dev loop, not the survey/drill/synthesize walkthrough.

## References

- [`references/commands.md`](references/commands.md) — full command surface, options that matter, MCP↔CLI mapping, git-hook setup.
- [`references/recipes.md`](references/recipes.md) — validated recipes with the peer-session evidence (env double-layer catch, rolled-back test catch, limits).
