# skill-impact — session-mining

提案台账。被拒提案必须保留并写明拒绝理由——后续提案撞形状时先翻此表。

| 提案 | 落点 | commit | 验证命令与结果 |
|------|------|--------|----------------|
| 2026-10-22 合并诞生：skill-call-extract + tool-call-extract 合并为单一路由 skill。证据（30 个历史挖掘 session 考古，~/tmp/mining-mine/SYNTHESIS.md）：①两个同形 extract skill 造成误注入（01a0c303 按"提取"注入 skill-call-extract 实际需 tool-call-extract）与已注入仍绕过（01a0d23f orca 形状聚类）；②11 类挖掘问题中 5 类在两个脚本语义之外（形状聚类/单 session 解剖/时序增量/全量语义扫/自定义事件 grep），681 个游击挖掘 session 从未触发任何 extract；③六步骨架在 4 个 SKILL.md 重复维护。方案：SKILL.md 收敛为路由表+六步骨架；9 条手挖配方进 references/recipes.md；两份 primer 合并（含负面结论：compaction 非事件类型、isError:false 藏运行时错误）；4 脚本+46 测试整体迁移。被否替代案：保留双 skill 加 router（4 份骨架仍漂移）、只写 AGENTS.md 路由段（每次全量注入成本最高）。旧两 skill 退役，4 个消费者（两个 diagnose、replay-compare、doc-consumption）已重指向 | SKILL.md（路由表+骨架）、references/{recipes,session-jsonl}.md、scripts/×4、tests/×4 | 32ba779 | `uv run --project in-progress/session-mining pytest in-progress/session-mining/tests`：46 passed；gitleaks clean；post-commit 自动重装并 diff 源仓=安装副本 |
