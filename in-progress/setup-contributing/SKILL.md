---
name: setup-contributing
description: Scaffold a repo's docs/contributing/ doc set — contribution workflow AND development conventions (setup, branch/commit rules, PR review, testing). Modeled on NVIDIA NeMo Relay's contribute structure and internal-fork development guides (branch/remote model, upstream sync, change markers). Run once per repo, on demand.
disable-model-invocation: true
---

# Setup Contributing Docs

Scaffold the repo's `docs/contributing/` doc set — not a single `CONTRIBUTING.md` but a directory of focused guides covering both **contributing** (PR flow, review rules) and **developing** (setup, branch model, testing).

This is a prompt-driven skill, not a deterministic script. Explore the repo, present what you found, confirm with the user section by section, then write.

## Reference lineage

The doc-set shape comes from two sources (read the seed templates in [templates/](./templates/) — they already embody this; don't re-derive):

- **NeMo Relay contribute docs** — the four-guide split (Development Setup / Workflow and Reviews / Testing and Documentation) plus an index page with "Start Here When" routing.
- **Internal-fork development guides (sglang `AGENTS.md` → `DEVELOPMENT.md` pattern)** — fork remote/branch model, internal-change markers (commit prefix + anchor comments), upstream sync strategy.

Only the fork sections are conditional — everything else is written for every repo. Which sections a repo gets is decided entirely by its posture (Section A), not a separate per-feature questionnaire.

## Process

### 1. Explore

Read what exists; don't assume. Look at:

- `git remote -v` — **repo posture**: single upstream remote vs fork (internal `origin` + upstream GitHub remote, or `*-internal` branch family). Posture decides whether fork-specific sections run.
- `CONTRIBUTING.md`, `DEVELOPMENT.md`, `AGENTS.md`, `CLAUDE.md` at repo root — existing rules to absorb, not duplicate.
- `docs/` layout — is there already `docs/contributing/` or a similar dev-docs dir?
- Dev tooling signals: `Makefile`/`makefile`, `pyproject.toml`/`go.mod`/`Cargo.toml`, `.pre-commit-config.yaml`, CI config (`.gitlab-ci.yml`, `.github/workflows/`), a `verify`/`check` entry point.
- Test entry points: how tests are actually run here (`make test`, `uv run pytest`, `go test ./...`).
- Doc language: is the repo's prose English, Chinese, or bilingual (`_cn.md` variants)?

### 2. Present findings and ask

Summarise what's present and missing, then take the sections in order — one section, one answer. Lead each with the recommended answer so the user can accept in a word. Skip sections exploration already settled.

**Section A — Repo posture.** Recommended from remotes: **upstream OSS** (single public remote, community PRs), **internal fork** (internal remote + upstream; MR-based, internal-change markers, upstream sync) or **internal-only**. This answer directly decides the fork sections: internal fork → keep the upstream-sync section in `workflow-and-reviews.md` and the fork remote/branch model in `development-setup.md`; upstream OSS or internal-only → those sections are dropped entirely. No follow-up question.

**Section B — Doc set.** Default to all four pages; drop pages the repo genuinely doesn't need (say which and why):

- `README.md` — index: "Start Here When" routing + guide list + link to existing `CONTRIBUTING.md` if present
- `development-setup.md` — toolchain, source setup, branch naming, code style
- `workflow-and-reviews.md` — commit conventions, PR/MR flow, review rules, (fork: upstream sync + change markers)
- `testing-and-docs.md` — smallest-validation-set selection, build/test/verify commands, docs checks, licensing

**Section C — Content specifics.** Collect per page: branch naming scheme, commit prefix/convention, the repo's single verify entry point, and doc language (follow the repo's dominant language; ask when bilingual).

### 3. Confirm and edit

Show drafts of every page (seed templates adapted with the repo's real facts — commands filled in, fork sections included or stripped, gates on or off) plus the AGENTS.md/CLAUDE.md pointer line. Let the user edit before writing.

### 4. Write

Write `docs/contributing/*.md` from the adapted templates. Then add a pointer so agents in this repo find the docs:

- If an `## Agent skills` section exists in `AGENTS.md`/`CLAUDE.md`, add a `### Contributing` sub-block: one line + `docs/contributing/README.md` link.
- Else add a one-line pointer near the top of whichever file exists. Create neither if the repo has none — the docs stand alone.

Never duplicate content already owned by `CONTRIBUTING.md` — link to it from `README.md` instead.

### 5. Done

Tell the user what was written, which pages were skipped and why, and that they can edit `docs/contributing/*.md` directly later — re-run only to restructure.
