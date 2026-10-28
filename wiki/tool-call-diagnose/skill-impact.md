# tool-call-diagnose — impact ledger

| date | proposal | landing | verification |
|------|----------|---------|--------------|
| 2026-10-16 | Relay enrichment 接入（可选路径）：step 1 增 relay-enrich.py 调用（仅用户明确要求延迟/重试深度分析时）；Axis 1 brief 增文本+时序双重证据要求（duration_s/status）；Axis 2 brief 增 LLM 级 attempt 重试（attempt_index>0，区别于 agent 发起重试）与延迟长尾量化 | feat: NeMo Relay enrichment for extract/diagnose skills (optional path) | 冷启动建账；SKILL.md diff 人工核对三轴 brief 结构未破坏 |
| 2026-10-20 | 新增 Axis 4 契约与替代（来自 worktrunk 工具审计复盘）：bash 旁路占比（grep bash args 中目标工具 CLI 名）、schema 契合度（enum 漏值/重复动词/冗余重发）、description→行为鸿沟（同形态误用跨天重复 = 描述失效，修复路线是 schema 层收紧而非重述规则）；三轴扩为四轴 | feat(tool-call): diagnose axis 4 (contract & competition) + extract default-on diagnose handoff | SKILL.md diff 人工核对；四轴 brief 结构一致，done-when/aggregate/routing 同步 |

| 2026-10-22 联动优化（4-lane 诊断执行挖掘，ada69ba）：①step-5 交接改 attribution vs portrait 二分（证据：17 个 post-landing extract session 0 真实联动；01a15e93 当天注入规则仍绕开=触发语义错配非送达失败）；②skill-call-diagnose 多 trace 一等公民（01a055e6 4-trace 手工适配先例收编）+ challenger 对抗轮进契约（01a0c727 幽灵版本论据连杀两案，原为用户发起）；③tool-call-diagnose 接受多 session dump 矩阵（axis lanes）；④description 净瘦身（scd 93→76 / tcd 120→79 词）并分流分析型请求（01a07d42 误注入负例）；⑤recipes 记 ctx_execute 读契约双盲区 + 月度基线附 extract→diagnose 转化率指标（step-5 生效性） | session-mining SKILL.md Close + recipes；两 diagnose SKILL.md | ada69ba | 46 tests green；description 词数核减；gitleaks clean |
