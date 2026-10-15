---
name: setup-git-hooks
description: Set up local git hooks managed through a `hooks/` directory + `make setup`, with optional `worktree`-level isolation. Supports pre-commit, pre-push, commit-msg, post-checkout, post-merge, and post-rewrite hooks written in plain bash shell scripts sourced from a shared `common.sh` library.
disable-model-invocation: true
---

# Setup Git Hooks

Scaffold a repo-local git hooks system (plain bash hooks + `make setup`,
shared `common.sh` library, optional per-worktree isolation):

```
hooks/
├── common.sh           # shared logging and validation functions
├── install-hooks.sh    # symlinks hooks to .git/hooks/
├── commit-msg.sh       # validate commit message format
├── pre-commit.sh       # staged-file checks (format, whitespace)
├── pre-push.sh         # full CI checks (lint, test)
├── post-checkout.sh    # auto-update hooks + deps on branch switch
├── post-merge.sh       # auto-update hooks + deps on merge
└── post-rewrite.sh     # auto-update hooks on rebase/amend
```

This is a **prompt-driven skill**, not a deterministic script. Explore, present
what you found, confirm with the user, then scaffold.

## Process

### 1. Explore

Read the repo to understand its starting state:

- `go.mod` / `package.json` / `Cargo.toml` / `Gemfile` / `pyproject.toml` —
  what language(s) does the repo use? This decides default lint/test commands.
- `Makefile` or `makefile` — which build/test/lint targets exist?
- `hooks/` — does one already exist? If so, what's inside?
- `.git/hooks/` — are any hooks already installed?
- `.golangci.yml`, `.eslintrc*`, `.prettierrc*` — which linters are configured?
- `AGENTS.md` / `CLAUDE.md` — does it mention hooks?
- `Makefile` `setup` target — does one exist?
- Git worktree usage — check `git worktree list`, check if
  `extensions.worktreeConfig` is already set.

### 2. Present findings and ask

Summarise what's present and what's missing. Then go through the sections
one at a time — one section, one answer, then the next.

**Section A — Hook set.** Which hooks to install:

| Hook | Runs on | Typical checks |
|------|---------|----------------|
| `pre-commit` | `git commit` | gofmt / prettier, whitespace, staged-file lint |
| `commit-msg` | `git commit` | Conventional Commits format |
| `pre-push` | `git push` | full lint, test, build |
| `post-checkout` | `git checkout` (branch) | auto-update hooks, reinstall deps |
| `post-merge` | `git merge` | auto-update hooks, reinstall deps |
| `post-rewrite` | `git rebase` / `git commit --amend` | auto-update hooks, reinstall deps |

Default posture: recommend **pre-commit + commit-msg + pre-push** — the three
fast/safe hooks that catch formatting, commit message, and pre-push failures.
**post-checkout + post-merge + post-rewrite** are extras for auto-updating
hooks on pull/rebase — add them if the team frequently runs `git pull`
mid-sprint and wants hooks to stay current without `make setup` each time.

**Section B — Checks per hook.** Fill with sensible defaults based on
exploration. Example:

```
hooks/
├── pre-commit:
│   - gofmt check on staged .go files (or prettier for JS/TS)
│   - whitespace check (git diff-index --check --cached)
├── commit-msg:
│   - Conventional Commits validation (type(scope)!: desc)
│   - duplicate Signed-off-by check
├── pre-push:
│   - make lint
│   - make test
│     (or stricter: clean worktree checkout of the pushed SHA +
│      make lint test, to simulate CI on a pristine tree)
├── post-checkout / post-merge / post-rewrite:
│   - auto_update_hooks: detect hooks/ changes in HEAD vs HEAD@{1}
│   - update_dependencies: go mod tidy / npm install
│   - update_submodules: if .gitmodules exists
```

Ask only if the default doesn't match what exploration found; otherwise skip
to confirmation.

**Section C — Worktree isolation.** Only ask if `git worktree list` shows
multiple worktrees. If yes:

> Hook scripts live in `hooks/` and get symlinked to `.git/hooks/`.
> With multiple worktrees, a `.git/hooks/` symlinked to `hooks/install-hooks.sh`
> in one worktree might point to a different source from another worktree.
>
> Worktree-isolation approach: enable `extensions.worktreeConfig` and
> set `core.hooksPath` per worktree, so each worktree has its own hooks
> symlinked to its own `.git/worktrees/<name>/hooks/`.
>
> **Single worktree** — skip worktreesConfig, just symlink to
> `.git/hooks/` directly.
>
> **Multi worktree** — use the worktree-isolation approach above.

If git worktree list shows only one worktree, silently skip this section.
The `install-hooks.sh` will default to simple symlink mode.

### 3. Confirm and edit

Show the user a complete directory tree with file contents. Let them tweak
before writing.

### 4. Write

For each hook file, use the templates from `./templates/` directory as
starting point. Customise:

- **common.sh** — adapt `validate_commit_msg` if the project uses a different
  commit convention; add/remove shared functions
- **pre-commit.sh** — replace gofmt with the project's formatter
- **pre-push.sh** — replace `make lint test` with actual CI targets
- **post-checkout.sh / post-merge.sh / post-rewrite.sh** — keep the
  `auto_update_hooks` logic if included; it detects `hooks/*.sh` changes
  between the old and new HEAD and re-runs `install-hooks.sh` automatically.

Files to create:
- `hooks/common.sh` — shared functions (see template)
- `hooks/install-hooks.sh` — symlink installer (see template)
- `hooks/pre-commit.sh` — pre-commit check
- `hooks/commit-msg.sh` — commit message validation
- `hooks/pre-push.sh` — pre-push check
- `hooks/post-checkout.sh` — (optional)
- `hooks/post-merge.sh` — (optional)
- `hooks/post-rewrite.sh` — (optional)

Then add (or update in existing `Makefile`):
```makefile
.PHONY: setup
setup: ./hooks/install-hooks.sh  ## install git hooks
	@./hooks/install-hooks.sh
```

Only add `setup` target if no `setup` target already exists; if one exists
but doesn't call `install-hooks.sh`, ask the user whether to merge or rename.

### 5. Done

Tell the user:
- Which hooks were installed, and what they check
- That `make setup` (re)installs them
- That hook scripts in `hooks/` are committed to the repo and shared
  with other developers
- That a teammate can run `make setup` after pulling
- `post-checkout / post-merge / post-rewrite` auto-updates hooks on
  `git pull` / branch switch, so `make setup` may only be needed once