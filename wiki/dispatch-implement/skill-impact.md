# dispatch-implement

## skill-impact

- 2026-09-22 | proposal: initial skill (spawn chain + orchestration protocol for design↔implement pairs) | landing: SKILL.md + scripts/spawn-implementer.sh + scripts/check-env.sh, installed global | evidence: session 01a0c742-9d9a (orca routing doc work), verb surface verified via `orchestration --help` on app 1.4.205; worktree-id resolution smoke-tested against 21 live orca worktrees | status: accepted
- 2026-09-22 | correction (user): pi expands only the FIRST /skill: per prompt — dual-prefix bootstrap was broken | landing: SKILL.md §Bootstrap prompt rewritten, channel-routed (orchestration = /skill:implement only, worker preamble carries protocol; terminal fallback = two sends, skills before task) | commit 29c5660 | status: accepted
- 2026-09-22 | review round (2 fresh-context subagents, writing+accuracy): 1 blocker (BRANCH_SLUG env-prefix crash under set -u), 4 major (result-envelope parsing, one-Run contradiction, verified-chain overstatement, stale [caller identity] cross-ref) + minors all accepted | landing: script error-guarded parsing + --run reuse flag + lowercase slug; SKILL.md channel-routed bootstrap, retry-of on dispatch_id with --spec, closure terminal-list bridge + UNVERIFIED auto-close marker, description trimmed to pointer discipline; check-env PASS/WARN/FAIL format | commit pending | status: accepted
