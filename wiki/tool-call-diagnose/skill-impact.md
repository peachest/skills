# tool-call-diagnose — impact ledger

| date | proposal | landing | verification |
|------|----------|---------|--------------|
| 2026-10-16 | Relay enrichment 接入（可选路径）：step 1 增 relay-enrich.py 调用（仅用户明确要求延迟/重试深度分析时）；Axis 1 brief 增文本+时序双重证据要求（duration_s/status）；Axis 2 brief 增 LLM 级 attempt 重试（attempt_index>0，区别于 agent 发起重试）与延迟长尾量化 | 442dafc | 冷启动建账；SKILL.md diff 人工核对三轴 brief 结构未破坏 |
