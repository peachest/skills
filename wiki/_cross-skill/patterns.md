# patterns — 跨 skill 通用规律

对多个 skill 的诊断都成立的规律。证据分散在各 skill 的 wiki 目录。

## X-001 skill 注入新鲜度决定遵循度
- 状态: open
- 现象: 长会话中 skill 仅首次调用时注入，后续执行凭数天前的记忆复跑——强制确认类步骤的违规随执行次数递增（第 3-4 次执行时 agent 以"先例/上下文明确"替代显式确认，甚至违反 never-push-unasked 级硬规则）；单主题短会话（skill 当轮注入）完全遵循
- 根因: 注入机制 + 会话结构——长多主题会话中 skill 契约不在上下文里
- 方案: 方向性启示（非单点修复）：多主题长会话中需要再次调用某 skill 时，重新注入或显式 read 其 SKILL.md；skill 作者可将硬规则写成不可绕过的 gate（脚本强制）而非依赖 agent 记忆
- 证据: create-mr diagnose#1（01a06bcd 长会话 4 次执行递增违规 vs 01a07f1f/01a07fc6 短会话零违规）
- 出现: 2026-09-09 diagnose#1（create-mr）
