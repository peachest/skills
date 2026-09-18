---
name: pi-events-doctor
description: >-
  pi-events-daemon 的风险登记与生产期事后诊断。Use when the daemon has been running
  in real usage for a while and needs a health/pathology pass, when the user says
  "daemon 用了一段时间/做个诊断/风险复盘", when a daemon anomaly appears
  (parked 积压、dead-letter 增长、wake 失败、采纳率异常), or periodically as a
  scheduled review. Carries the risk register so discovered risks are never
  re-derived from scratch.
---

# pi-events-doctor

对 pi-events-daemon 做风险登记与生产期诊断。设计态裁定见 #29/#30 与 ADR 0001-0005；
本 skill 的职责是**记住已知风险**（references/risks.md）并**在真实使用一段时间后逐项诊断**。

## 何时触发

- daemon 进入实际使用后（实现落地 + 日常使用 ≥1 周）的定期复盘
- 用户报告 daemon 异常：事件没送达 / parked 堆积 / dead-letter / 唤醒失灵 / reckon 答过时信息
- 重大外部变化后复查（pi harness 升级、orca 迁移、profile 新增）

## 诊断流程（四步）

1. **取证据**：按 references/checks.md 对每条风险跑检查（daemon 自身 SQLite 查询 +
   运行日志审计（B3）+ transcript 抽样）。daemon 无 telemetry（裁定后置），证据全部来自
   它自己的持久层与日志——这是设计使然，不是缺陷。
2. **逐风险判定**：对 references/risks.md 每行给出 verdict：
   `healthy | degraded(证据) | triggered(证据 + 影响面)`。只报有证据的结论，禁止凭感觉。
3. **修复或挂账**：可立即修的（如 FTS5 索引重建、dead-letter 清理）给出操作；
   结构性的升级为 issue（peachest/pi-packages）并在 risks.md 标注 issue 链接。
4. **回写登记表**：每条风险的 status/check 结果/日期更新进 references/risks.md；
   新发现的风险当场入表（这是"记住风险"的机制：每次诊断都让登记表更完整）。
   确诊的故障按 diagnosing-bugs-with-docs 流程写 ~/ops 诊断库（diag-write）。

## 检查工具约定

- 证据收集优先用只读 SQL（`sqlite3 <daemon.db> 'SELECT ...'`）——具体库路径与 schema
  以 v2 spec 定稿为准，见 references/checks.md 的占位标记。
- transcript 抽样用 jq/grep 对 `~/.pi/agent/sessions/**/*.jsonl`（I9 验证面同源）。
- 禁止在诊断中执行 checker/副作用操作——本 skill 只读，修复动作单独列出并征得确认。

## 边界

- 不做编排、不自动修复（裁定：daemon 及其配套只感知不指挥）
- 遥测不存在：所有"指标"都是事后批量查询，不是流式监控——如需实时告警属于
  post-MVP telemetry 议题，进 #30 讨论而非本 skill 自造

详细风险登记表与检查项见 [references/risks.md](references/risks.md) 与
[references/checks.md](references/checks.md)。
