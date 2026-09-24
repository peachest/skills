
## 2026-09-15 steer/followUp 语义澄清
- 提案: 明确 herdr 发送消息进 running peer 的投递语义（pi steer 队列），补 followUp 缺失时的对策
- 落点: SKILL.md "Steer semantics" 小节 + pitfalls.md #24（agent prompt = text+Enter = steer；"做完当前的再做" 任务先 `agent wait --until idle` 再发）
- commit: 1b4e39e
- 验证: pi docs rpc.md/extensions.md 源码级确认；herdr agent send --help 无模式选项

## 2026-09-16 前缀重复注入修复（用户实测反馈）
- 提案: /skill:multi-agent-collab 前缀从「每条消息」改为「bootstrap 信号，每个 peer context 只发一次」；回执/闭环/澄清一律裸消息；内嵌 reply 模板去前缀、保留身份签名
- 落点: SKILL.md 五段模板注释 + 前缀规则 bullet 重写 + reply 模板 bullet 重写 + dispatch contract 第 1 条
- 验证: 用户实测——A 通知 B、B 回执、A 闭环三步各注入一次 skill，重复注入浪费 token；示例文本（examples.md）本就标注旧前缀，无需改
