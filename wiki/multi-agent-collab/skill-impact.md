
## 2026-09-15 steer/followUp 语义澄清
- 提案: 明确 herdr 发送消息进 running peer 的投递语义（pi steer 队列），补 followUp 缺失时的对策
- 落点: SKILL.md "Steer semantics" 小节 + pitfalls.md #24（agent prompt = text+Enter = steer；"做完当前的再做" 任务先 `agent wait --until idle` 再发）
- commit: 1b4e39e
- 验证: pi docs rpc.md/extensions.md 源码级确认；herdr agent send --help 无模式选项
