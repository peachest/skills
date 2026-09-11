# patterns — multi-agent-collab

## M-001 herdr 多 session 协作协议模式（2026-09-08 批量提取）
- 状态: absorbed-into-skill
- 现象: 从 32 个含 herdr CLI 调用的 session（53 个 marker 匹配）中提取的协作协议——五段式 prompt 结构（/skill:herdr 前缀 + 自我介绍 + 背景 + 编号任务 + 回复路径）、长 prompt 先写文件再发送、--wait 超时经验值（ack 60s / 一般 180-300s / 重任务 600s）、pane id 与命名 agent 两种寻址、leader 编排模式
- 根因: ——（这是知识提取，非故障模式）
- 方案: 已蒸馏进 multi-agent-collab skill 本体（SKILL.md + references/pitfalls.md 的 23 条失败模式）
- 证据: 01a023e5, 01a03e1c, 01a06b3e, 01a07b54（知识提取来源，无单 entry 锚点；全保真产物存本地 ~/tmp/herdr-extract/，含内网信息不入库）
- 出现: 2026-09-08 herdr-extract（skill-call-extract 执行#1）
