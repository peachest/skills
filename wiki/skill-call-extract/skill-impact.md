# skill-impact — skill-call-extract

提案台账。被拒提案必须保留并写明拒绝理由——后续提案撞形状时先翻此表。

| date | proposal | commit | verification |
|---|---|---|---|
|  | S1 版本锚定：injection body / read-load toolResult 内容哈希 → 源仓库 git 历史逐 blob 解析 → commit / uncommitted（含幽灵版本检测 matches_current_file:false）/ third-party 三态裁决。不在 SKILL.md 加 version 字段（共享 checkout 下手动 bump 必漂移；内容哈希是"实际跑的字节"的 ground truth，版本字段只是声称） | scripts/version-anchor.py + SKILL.md 步骤 5 + 交付物 4 + Done-when 第 4 条 | ea8c0ff | `uv run pytest`：29 passed（8 新测试 + 真实形态收敛测试）；真实 session 冒烟（<project> 会话锚定 to-intent）：17:47 注入正确解析到 48df71d，17:26 注入正确判为幽灵版本（未提交的集成前版本，仅存于 session log） |
|  | R1 SKILL.md frontmatter 加 version 字段——被否：多 session 共享 checkout（本仓库现实）下靠人记得 bump 必然漂移；git blob 哈希已是无歧义版本源，字段是对环境的冗余 cache（skill-authoring 规范：cache 只存环境查不到的东西） | —（采纳 S1 替代） | — | 本 session 论证：version 字段只告诉"声称是 v3"，无法回答"该 session 当时实际生效哪版"——后者只有内容哈希能答 |
| 2026-10-16 | NeMo Relay enrichment（可选深入分析路径，用户拍板 relay 不作默认必经）：新增 scripts/relay-enrich.py（pi session id→ATIF trajectory join，re-entry 多实例合并、token 总量+cache 命中率、per-step 延迟/model/usage、per-tool-call duration/attempt_index/status、no-relay-data 静默降级、大文件字节扫描 final_metrics）；SKILL.md 新增 step 6 + deliverable 第 5 项 | lost-hash | uv run pytest 10/10 新增 + 39/39 全量；真实数据冒烟（01a06643 4 实例 join，cache_hit_rate 0.853）；no-relay-data 路径冒烟通过；结果: uv run pytest 10/10 新增 + 39/39 全量；真实数据冒烟（01a06643 4 实例 join，cache_hit_rate 0.853）；no-relay-data 路径冒烟通过 |
| 2026-10-22 | 退役：与兄弟 extract skill 合并为 in-progress/session-mining（路由表统一入口，脚本/测试整体迁移，消费者已重指向）。理由与证据见 wiki/session-mining/skill-impact.md | 0f739d5 | 46 tests green；结果: 46 tests green |
