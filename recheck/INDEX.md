# Recheck index

| name | verifies | baseline (source) | last run | status |
|------|----------|-------------------|----------|--------|
| wt-usage-scan.py | wt usage portrait drift (4-command concentration, error families) | 179 calls / switch 68% / errors 6 (01a15409, 2026-10-19) | 2026-10-22 | live |
| wt-usage-trend.py | wt command monthly trend shape | 99% of calls in 4 commands (01a15409) | 2026-10-22 | live |
| wt-usage-trend2.py | weekly trend + switch flag shapes; "switch switch" error family | duplicated-verb errors recurring 3 weeks (01a15409) | 2026-10-22 | live |
| subagent-calls-scan.py | subagent (pi-subagents) usage portrait drift; fork-dedup baked in ((ts, args) key) | raw 8111 / unique 2398 (dup 70%) / errors 112 / top agent worker 250 (01a1636b, 2026-10-22) | 2026-10-22 | live |
| mine-herdr-ops.py | herdr CLI error-rate baseline — absorbed into `in-progress/multi-agent-collab/references/mining/` | 1108 paired calls, direct-prompt 1% err (01a0c303) | rerun via its skill home | absorbed |
| test-bash-guards.py | bash-guards hook fixtures — superseded by packages/pi-bash-guards golden fixture suite | 5 cases (01a1590a, 2026-10-20) | — | absorbed |
| check-grafana-rooturl.sh | grafana root_url rendering (4 cases) | all green (01a07fc6, 2026-09-08) | never re-run after fix | dead |
