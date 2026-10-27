# Syncing this mirror

This directory is a `git subtree add --squash` mirror of [`backnotprop/pstack`](https://github.com/backnotprop/pstack) (remote `pstack`), which is itself the standalone mirror of upstream [`cursor/plugins/pstack`](https://github.com/cursor/plugins/tree/main/pstack) (Lauren Tan's engineering skill stack).

Why vendor the mirror instead of the Cursor upstream: the Cursor repo is a plugins monorepo (subtree would import all plugins), while backnotprop/pstack is exactly the `pstack/` folder and keeps a documented sync flow (`MIRROR.md` in that repo: `upstream` branch holds Cursor's files, `main` adds harness-neutral rewrites) plus a Cursor→neutral mapping table in `skills/poteto-mode/SKILL.md`.

Sync rules mirror `vendor/mattpocock/MIRROR.md`; pstack-specific notes below.

## Sync steps

0. File-name check before creating anything inside `vendor/pstack/`: upstream already ships files like `MIRROR.md` — a same-name file here makes every future subtree pull conflict. Check the upstream tree first; if the name exists, pick another (this repo uses `SYNC.md`).

1. Fetch and merge:

   ```bash
   git fetch pstack
   git subtree pull --prefix vendor/pstack pstack main --squash
   ```

2. We do not edit vendor/pstack files — no overlay, no 嫁接税 commits here. Conflicts should not happen; if one does, it means someone edited vendor/pstack directly: resolve by taking upstream and moving the change to an overlay under `in-progress/`.

3. Reinstall changed skills we use (see install list below) and verify:

   ```bash
   npx skills add -g ./vendor/pstack/skills/<name> -a pi -y
   diff -r ~/.agents/skills/<name>/ vendor/pstack/skills/<name>/
   ```

4. Upstream check (optional, when a pstack bug fix matters): check whether backnotprop has shipped the fix; if not, check cursor/plugins upstream before patching locally.

## Installed subset

Only these skills are installed to the global agent (install list is the source of truth):

`how`, `why`, `blast-radius`, `correct`, `benchmark-checklist`, `statechart`, `arena`, `sharpen`, `ketchup`, `no-comments`

Machine check — run after any install/uninstall or sync:

```bash
bash vendor/pstack/check-installed.sh   # SYNC.md list vs ~/.agents/skills, missing/drift/unlisted
```

Known gap: `blast-radius` references `unslop` (arena was installed 2026-10-26), which is intentionally not installed — its instructions mention it but degrade gracefully; install it too if the reference becomes noisy.
