# Syncing this mirror

This directory is a `git subtree add --squash` mirror of [`mattpocock/skills`](https://github.com/mattpocock/skills) (remote `mattpocock`), with local edits layered on top. Sync rules live in the repo root `AGENTS.md` (Vendor 管理 section); this file is the operational checklist.

Two-layer contract (do not break it):

- Upstream files may carry only pi-specific mechanical adaptations (嫁接税): `/skill:` command-format migrations, sanitize rewrites, path adjustments. Keep these commits separate from substantive changes so they replay cleanly on conflict; substantive fixes are worth picking out for an upstream PR instead.
- Substantive customization goes to an overlay under `in-progress/`, which becomes the sole install source for that skill. The vendor copy stays upstream-pure. Current overlays: teach, setup-matt-pocock-skills, wayfinder, diagnosing-bugs-with-docs fork. Do NOT fork the vendor into a separate repo or patch layer — subtree's design is exactly this directory resolving entanglement via three-way merge.

## Sync steps

1. Fetch and merge upstream:

   ```bash
   git fetch mattpocock
   git subtree pull --prefix vendor/mattpocock mattpocock main --squash
   ```

   On add/add or both-sides-changed conflicts: diff and decide which side is newer; vendor copy must never silently drift (误改 vendor 副本会在这里以冲突形式暴露).

2. Replay mechanical adaptations if a conflict touched them. Find them via:

   ```bash
   git log --oneline --follow -- vendor/mattpocock | grep -iE 'sanitize|/skill:|adapt|format'
   ```

3. Reinstall changed skills and verify install copy == source:

   ```bash
   npx skills add -g ./vendor/mattpocock/skills/<changed-skill> -a pi -y
   diff -r ~/.agents/skills/<changed-skill>/ vendor/mattpocock/skills/<changed-skill>/
   ```

4. Ledger: after landing, add one `skill-impact.md` line per changed skill per the two-phase commit rule in `wiki/README.md`.

5. Push gate: `bash scripts/sanitize-check.sh && git push origin main` (no pipes — exit code must come from the gate itself).
