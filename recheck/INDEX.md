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
| edit-write-fail-scan.py | edit/write 失败率与失败模式基线（scan.py 全语料单遍 + aggregate/aggregate2 聚合，~/tmp/edit-write-fail/）：edit 29234 calls / 真实失败 8.5%（A 类 oldText 错配 71%，其中 53% 是自己先改过后锚文本漂移）/ write 13466 calls / 0.4%；n_edits 越多失败率越高（1 个 6.8% → 6+ 个 34.5%）；then_run 失败会被标 isError（81 条假阳性，2026-10-29 本 session） | 2026-10-29 | live |
| extract-triage-mrs.py + triage-rounds-{collect,diffsize,analyze}.py | triage-mr 评审轮次衰减基线（59 MR/1221 findings：round1 49.8%→round4 累计 89%；TP% 42→86 单调升；churn r=0.576 才是强预测变量，diff 大小 r=0.165 弱） | triage-rounds-REPORT.md（peer-fix-loop-cap 2026-10-26，143 session/771 pull）。注意：collect.py 的项目→remote 映射已脱敏为占位符，复跑前从 ~/tmp/triage-rounds-collect.py（不入库原件）恢复 URL_MAP，原始数据快照在 ~/tmp/triage-rounds/ | 2026-10-26 | live |
| toolshape-scans.py（~/tmp/toolshape/recheck/ 分片清单+6 scout JSON） | 工具调用形状基线（95.7% 单调用 / 40.4 万调用 / top 转换对）漂移检测：6 分片独立解析器重算，合计偏差 <0.1pp 为通过 | 379,821 msgs / 95.71% single / 404,288 calls（01a186f5, 2026-10-29） | 2026-10-29 | live |
| plainlang-broad-scan.py | 大白话/补上下文纠偏信号全库扫描（re-ask skill 的挖掘基座）：扫 user role 消息命中关键词集，按类别计数；初版 scan-broad.py 同源 | 183 hits（大白话 58 / 看不懂 55 / 解释清楚 22）；复跑 191 hits（01a1814f, 2026-10-30，语料自然增长） | 2026-10-30 | live |
| reask-pairs.py | 「重新问」触发前（agent 原问）后（重问产出）对照对提取：无参自动回溯定位的验证基座 | 29 pairs；复跑 31 pairs（01a1814f, 2026-10-30） | 2026-10-30 | live |
