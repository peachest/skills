# Recheck scripts

Mining / diagnose / optimize sessions leave recheck scripts in `~/tmp`. This
directory is their registry: the committed home for scripts that verify a past
finding or fix is still holding, plus the trigger data for reruns.

## Contract

Write side (any session that would leave a recheck script in `~/tmp`):

- Commit the script here (`recheck/<name>.<ext>`) with a header comment:
  provenance session id, what it verifies, baseline numbers.
- Add one row to `INDEX.md`. If it cannot be committed (env-locked, one-off),
  say so in the delivery and label the tmp copy `shortcut: one-off, <date>`.

Read side (session-mining Close): after mining skill/tool X, check `INDEX.md`
for rows targeting X and rerun them; diff against the baseline column and
report drift (regression, improvement, or stale-script). A script that fails
for environmental reasons (not the verified behavior) is marked `dead` in
INDEX, not silently kept.

## Run semantics

- Exit 0 = verified holding; exit 1 = regression vs baseline; other = script
  error (never counts as regression).
- Scripts must be rerunnable from any cwd and touch only `~/.pi/agent/sessions`
  and their own outputs under `~/tmp/recheck/<name>/`.
