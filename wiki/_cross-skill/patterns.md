# patterns — 跨 skill 通用规律

对多个 skill 的诊断都成立的规律。证据分散在各 skill 的 wiki 目录。

## X-001 skill 注入新鲜度决定遵循度
- 状态: open
- 现象: 长会话中 skill 仅首次调用时注入，后续执行凭数天前的记忆复跑——强制确认类步骤的违规随执行次数递增（第 3-4 次执行时 agent 以"先例/上下文明确"替代显式确认，甚至违反 never-push-unasked 级硬规则）；单主题短会话（skill 当轮注入）完全遵循
- 根因: 注入机制 + 会话结构——长多主题会话中 skill 契约不在上下文里
- 方案: 方向性启示（非单点修复）：多主题长会话中需要再次调用某 skill 时，重新注入或显式 read 其 SKILL.md；skill 作者可将硬规则写成不可绕过的 gate（脚本强制）而非依赖 agent 记忆
- 证据: create-mr diagnose#1（01a06bcd 长会话 vs 01a07f1f/01a07fc6 短会话对照，无单 entry 锚点）
- 出现: 2026-09-09 diagnose#1（create-mr）→ absent-this-run 2026-09-10 #1（reckon：4 trace/13 注入，多日长会话中规则跨天不衰减，采集全执行） → 2026-09-20 diagnose#1（okb：部分复现——01a062a0#359 #361，skill 单次注入 3 天后凭记忆复跑约定，链接深度写错靠翻旧课自救，无强制确认类硬违规） → absent-this-run 2026-09-20 #1（academy：同轮注入 #173 立即执行，跨 2.5h+ 空档与多轮协议复跑不衰减）
