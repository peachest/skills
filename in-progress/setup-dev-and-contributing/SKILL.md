---
name: setup-dev-and-contributing
description: Scaffold a repo's development spec and contributing docs — a root DEVELOPMENT.md (branch/remote model, internal-change markers, upstream sync, design records — internal-fork pattern) plus docs/contributing/ (setup, workflow/reviews, testing — NeMo Relay pattern). Run once per repo, on demand.
disable-model-invocation: true
---

# Setup Dev and Contributing Docs

Scaffold two complementary artifacts for a repo:

1. **`DEVELOPMENT.md`** (repo root, single file) — the *development* spec: how to write code in this repo. Modeled on the internal-fork `AGENTS.md` → `DEVELOPMENT.md` pattern: one-line principle, branch/remote model, internal-change markers and isolation, upstream sync, design records, versioning, code-style and domain guards.
2. **`docs/contributing/`** (four pages) — the *contributing* docs: how to get a change reviewed and merged. Modeled on NVIDIA NeMo Relay's contribute structure: index with "Start Here When" routing, Development Setup, Workflow and Reviews, Testing and Documentation.

Read the seed templates in [templates/](./templates/) — they embody both patterns; don't re-derive.

## Content boundary (decided at design time — don't re-ask)

Split by **when it's used**: commands and gates a contributor runs at submit time → `docs/contributing/`; principles and guards a developer applies while writing code → `DEVELOPMENT.md`.

- Toolchain/env setup, pre-commit/lint commands, test thresholds, MR/PR flow, review rules → contributing
- Branch/remote model, commit-prefix markers, anchor comments, upstream sync, design records, versioning, code-style and domain guards → development
- The `[<org>]` commit prefix belongs in DEVELOPMENT.md (it's a sync-cost marker tied to anchor comments); contributing's commit-conventions section links to it.

## Conditionality

Only the fork sections are conditional, decided entirely by posture (Section A), no follow-up questions:

- **Internal fork** → DEVELOPMENT.md keeps 标记与隔离 / 上游同步 / 设计记录 / 版本号 sections; contributing keeps the upstream-sync and relaxed-review sections.
- **Upstream OSS / internal-only** → those sections are dropped. DEVELOPMENT.md shrinks to branch model + code-style/domain guards.

Everything else is written for every repo.

## Process

### 1. Explore

Read what exists; don't assume:

- `git remote -v` — repo posture. An internal remote + upstream GitHub remote (or `*-<org>` branch family) means internal fork.
- `DEVELOPMENT.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md` at root — existing rules to absorb, not duplicate.
- `docs/` layout — existing `docs/contributing/` or dev-docs dir.
- Tooling: `Makefile`, `pyproject.toml`/`go.mod`/`Cargo.toml`, `.pre-commit-config.yaml`, CI config, verify/check entry point, test entry points.
- Doc language: repo's dominant prose language.

### 2. Present findings and ask

**Section A — Repo posture.** Recommended from remotes: upstream OSS / internal fork / internal-only. This single answer decides all fork-conditional sections.

**Section B — Doc set.** Confirm both artifacts: `DEVELOPMENT.md` + the four contributing pages (`README.md`, `development-setup.md`, `workflow-and-reviews.md`, `testing-and-docs.md`). Drop pages the repo genuinely doesn't need (say which and why).

**Section C — Content specifics.** Collect: branch naming scheme, commit prefix marker, anchor-comment syntax, design-record location, the repo's single verify entry point, test selection logic, doc language. Follow the repo's dominant language for output; ask when bilingual.

### 3. Confirm and edit

Show drafts of DEVELOPMENT.md and every contributing page — seed templates adapted with the repo's real facts (commands filled in, fork sections kept or stripped). Let the user edit before writing.

### 4. Write

Write `DEVELOPMENT.md` at repo root and `docs/contributing/*.md`. Then make agents find them:

- If an `## Agent skills` section exists in `AGENTS.md`/`CLAUDE.md`, add a `### Development and contributing` sub-block pointing to both (one line each).
- Else if either file exists, add a two-line pointer near its top.
- If neither exists (fresh repo), **ask the user which to create — don't pick for them** (recommend `AGENTS.md` as the cross-tool entry point; a bare pointer block is enough, no `## Agent skills` scaffolding needed). Don't silently skip: without an entry file, nothing auto-loads the docs for future agents and the whole setup loses its effect.

Never duplicate content owned by `CONTRIBUTING.md` — link to it from `docs/contributing/README.md`.

### 5. Done

Report what was written, which fork sections were included or stripped and why. The user can edit the files directly later; re-run only to restructure.
