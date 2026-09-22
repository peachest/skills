# dispatch-implement

## skill-impact

- 2026-09-22 | proposal: initial skill (spawn chain + orchestration protocol for design↔implement pairs) | landing: SKILL.md + scripts/spawn-implementer.sh + scripts/check-env.sh, installed global | evidence: session 01a0c742-9d9a (orca routing doc work), verb surface verified via `orchestration --help` on app 1.4.205; worktree-id resolution smoke-tested against 21 live orca worktrees | status: accepted
- 2026-09-22 | correction (user): pi expands only the FIRST /skill: per prompt — dual-prefix bootstrap was broken | landing: SKILL.md §Bootstrap prompt rewritten, channel-routed (orchestration = /skill:implement only, worker preamble carries protocol; terminal fallback = two sends, skills before task) | commit 29c5660 | status: accepted
