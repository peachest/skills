# Recheck index

| name | verifies | baseline (source) | last run | status |
|------|----------|-------------------|----------|--------|
| wt-usage-scan.py | wt usage portrait drift (4-command concentration, error families) | 179 calls / switch 68% / errors 6 (01a15409, 2026-10-19) | 2026-10-22 | live |
| wt-usage-trend.py | wt command monthly trend shape | 99% of calls in 4 commands (01a15409) | 2026-10-22 | live |
| wt-usage-trend2.py | weekly trend + switch flag shapes; "switch switch" error family | duplicated-verb errors recurring 3 weeks (01a15409) | 2026-10-22 | live |
| subagent-calls-scan.py | subagent (pi-subagents) usage portrait drift; fork-dedup baked in ((ts, args) key) | raw 8111 / unique 2398 (dup 70%) / errors 112 / top agent worker 250 (01a1636b, 2026-10-22) | 2026-10-22 | live |
| solpi-report.py | SoL-Pi 收益基线（Observation Pack 归档量 + Action Fusion 轮次 + 免费模型下窗口/延迟收益） | 归档 255,733 obs / 11.1 亿 token 移出重放 / 融合 258 轮 / solpi-active 308 session（2026-10-23 本 session） | 2026-10-23 | live |
| solpi-recall-dump.py | obs_recall 真实取回（配对 toolResult，防 schema 噪声：字符串计数虚高 11 倍） | 真实 97 次 / 成功率 96/97 / 中位 16.5KB / 覆盖 47 session（2026-10-23 本 session） | 2026-10-23 | live |
| solpi-rerun-detector.py | 取回逃逸：归档后同参数重跑而不 obs_recall（需人工甄别 subagent 轮询/正当重读，见 solpi-rerun-final.py in ~/tmp） | 1245 条归档 / 17 起初筛 / 真逃逸 ~6-7 起（0.5%）（2026-10-23 本 session） | 2026-10-23 | live |
| mine-herdr-ops.py | herdr CLI error-rate baseline — absorbed into `in-progress/multi-agent-collab/references/mining/` | 1108 paired calls, direct-prompt 1% err (01a0c303) | rerun via its skill home | absorbed |
| test-bash-guards.py | bash-guards hook fixtures — superseded by packages/pi-bash-guards golden fixture suite | 5 cases (01a1590a, 2026-10-20) | — | absorbed |
| check-grafana-rooturl.sh | grafana root_url rendering (4 cases) | all green (01a07fc6, 2026-09-08) | never re-run after fix | dead |
| plainlang-scan.py | bro skill 匹配分析复跑（大白话偏好 6 类信号 + 去噪排除 peer 派发文本）；支撑 AGENTS.md Output Rules 已覆盖、不装 bro 的结论 | 去噪后 dabaihua 56 / jieshi 121 / zhankai 104 / jiandan 57 / pushback 57（2026-10-26 本 session，1964 files / 30455 msgs） | 2026-10-26 | live |
