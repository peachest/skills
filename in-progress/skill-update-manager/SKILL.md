---
name: skill-update-manager
description: >
  Manage and update globally installed agent skills across the two install
  chains — check third-party GitHub skills for upstream updates, update them
  via `npx skills update`, sync local skills installed from the ~/skills
  source repo, and clean lock residue. Use when the user asks to 检查 skill
  更新 / 更新第三方 skill / 同步本地 skill, or when `npx skills update`
  reports every skill outdated (the lock hash-scheme gap).
---

# Skill Update Manager

Two install chains, each with its own update path. Identify which chain a
skill belongs to before touching it:

| | Chain 1: third-party | Chain 2: local source |
|---|---|---|
| Installed from | GitHub `owner/repo` via `npx skills add -g` | `~/skills/<category>/<name>` via `npx skills add -g <path>` |
| Storage | `~/.agents/skills/` + symlinks in `~/.pi/agent/skills/` | real directories in `~/.pi/agent/skills/` |
| Tracking | `~/.agents/.skill-lock.json` (source, skillPath, hash) | the `~/skills` git repo itself |
| Update flow | `npx skills update [names] -g` | edit source → `npx skills add -g <path> -a pi -y` |

A symlink in `~/.pi/agent/skills/` means chain 1; a real directory means
chain 2 (or a chain-1 skill installed before symlink mode, converted to
symlink on its next update). `readlink` tells them apart.

## Phase 0 — Check environment

```bash
bash scripts/check-env.sh
```

All FAILs resolved before proceeding. WARNs mean that chain's mode will SKIP.

## Phase 1 — Check for updates (read-only, always start here)

```bash
python3 scripts/check-updates.py all     # both chains
python3 scripts/check-updates.py remote  # third-party only
python3 scripts/check-updates.py local   # ~/skills source only
```

Outputs per skill: `OK` / `OUTDATED` (with file-level change summary) /
`GONE` (removed upstream) / `MISSING` (lock residue) / `ERROR`, plus the
exact commands for the next phase. Completion criterion: every skill lands
in exactly one bucket and you can name what changed for each OUTDATED one.

The script downloads upstream tarballs and diffs file content — it ignores
the lock's recorded hash on purpose:

**Hash-scheme gap** (verified in CLI ≤ 1.5.23): entries written by older CLI
versions store a local content sha256 (64 hex chars), while `update` compares
GitHub tree SHAs (40 hex chars). The two schemes never match, so a lock
entry in the old scheme reads as "outdated" forever, regardless of the
actual upstream state. Consequences:

- `npx skills update -g` with no skill names reinstalls every skill in the
  old scheme — harmless (content unchanged) but slow, and it migrates those
  entries to the new scheme as a side effect.
- To know what *actually* changed, trust the tarball diff from
  `check-updates.py`, never the update command's "Found N updates" count.
- A full-reinstall run is the one-time fix that unifies the scheme; after
  it, plain `npx skills update -g` behaves accurately.

## Phase 2 — Apply updates, per chain

**Chain 1 (third-party):** run the `npx skills update <names> -g` command
the checker printed. Two guards first:

- Real-directory installs of chain-1 skills get replaced by symlinks during
  update. If the local copy has custom edits (diff it against the Phase 1
  upstream tarball to tell edits from mere age), back it up first:
  `cp -a ~/.pi/agent/skills/<name> <backup-dir>/`.
- `GONE` skills were removed upstream — ask the user whether to drop them
  (`npx skills remove <name> -g -y`) or pin the last good ref.

`MISSING` entries are lock residue (skill already uninstalled): remove with
`npx skills remove <name> -g -y`.

**Chain 2 (local source):** for each name the checker reported as
source-changed, reinstall from source, one path per invocation:

```bash
npx skills add -g ~/skills/<category>/<name> -a pi -y
```

Chain 2 skills are outside the lock file; `npx skills update` never touches
them, so upstream updates and local edits cannot clobber each other across
chains.

## Phase 3 — Verify

Re-run the same `check-updates.py` mode from Phase 1. Completion criterion:
0 OUTDATED, 0 GONE, 0 MISSING for every chain you touched. A skill still
OUTDATED after update usually means the GitHub tarball fetch hit flakiness —
rerun; the script already retries once per repo.
