# mr-buddy — impact ledger

| date | proposal | landing | verification |
|------|----------|---------|--------------|
| 2026-09-11 | Split oversized MRs into stacked chains of vertical-slice MRs (user request after kube-nodexpu-manager MR !12 hit 54 files / 54 commits). Design decisions from user: stacked chain topology; commit-first grouping with file-level fallback for mixed commits (never one-commit-per-MR); original MR shrinks to slice 1 via force-push; local verify per slice before push. | in-progress/mr-buddy/SKILL.md (initial) | Cold start, no tests carried. Not yet installed globally, not yet run against MR !12 — first real run is the acceptance gate. |
