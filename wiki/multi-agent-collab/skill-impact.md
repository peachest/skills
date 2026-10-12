
## 2026-09-15 steer/followUp 语义澄清
- 提案: 明确 herdr 发送消息进 running peer 的投递语义（pi steer 队列），补 followUp 缺失时的对策
- 落点: SKILL.md "Steer semantics" 小节 + pitfalls.md #24（agent prompt = text+Enter = steer；"做完当前的再做" 任务先 `agent wait --until idle` 再发）
- commit: 1b4e39e
- 验证: pi docs rpc.md/extensions.md 源码级确认；herdr agent send --help 无模式选项

## 2026-09-16 前缀重复注入修复（用户实测反馈）
- 提案: /skill:multi-agent-collab 前缀从「每条消息」改为「bootstrap 信号，每个 peer context 只发一次」；回执/闭环/澄清一律裸消息；内嵌 reply 模板去前缀、保留身份签名
- 落点: SKILL.md 五段模板注释 + 前缀规则 bullet 重写 + reply 模板 bullet 重写 + dispatch contract 第 1 条
- 验证: 用户实测——A 通知 B、B 回执、A 闭环三步各注入一次 skill，重复注入浪费 token；示例文本（examples.md）本就标注旧前缀，无需改
- 2026-09-24 | A2A 对照研究收尾（用户裁决）：v3 不立项——净产出仅 ~10 行 diff（身份段 2 字段/REJECTED 词/round N 标注），降级为 patch 候选清单；feat/a2a-alignment 分支与 feat/fetch-article-optimize 已合并/清理 | evidence: challenger 8 findings + Brown Dwarkesh transcript 一手核校 + 56 协议 session 回执形态扫描（自然语言+hash 锚点已稳定涌现，零状态词汇可行） | 研究快照 ~/research/a2a-vs-multi-agent-collab/ 保留全部否决记录 | status: accepted

## 2026-09-24 peer 拓扑切换新 tab（用户拍板）
- 提案: peer 创建默认从 pane split 改为开新 tab，指向新 to-peer skill（herdr-tab-peer.sh）；SKILL.md bootstrap 小节加一行，pane split 降级为用户显式要求时的 legacy fallback
- 落点: SKILL.md "Bootstrap a named peer" 首行重写
- 验证: to-peer tests/test.sh 9/9 + live smoke；两个 skill 均重装全局
- 状态: accepted

## 2026-09-24 回报触发面补全（现场静默案例 + 用户指正归属）
- 现象: to-peer 派生的子 session 与用户讨论后做出关闭 MR 的决策，只向用户汇报即静默，用户主动提醒后才回传父 session
- 归属修正: 上一版把"父子回传义务"写进了 to-peer；用户指正协议义务的源头在 multi-agent-collab（五段消息/闭环信号都定义在此，子 session 被注入的是本协议）——to-peer 保留派发者侧的 prompt 构造提醒即可
- 提案: dispatch contract 加 "Report-back trigger surface" 段：回报义务覆盖 完成工作/与用户中途达成决策（尤其推翻原方向）/任务暂停 三类触发面，目标地址取 bootstrap [caller identity]，不等用户提醒
- 落点: SKILL.md dispatch contract；to-peer SKILL.md 父子段已先行（eb094b8），形成 双侧约束：协议定义义务（本条）+ 创建器写 prompt（to-peer）
- 证据: <session-id>#187,#190,#191（脱敏）
- 状态: accepted

## 2026-10-12 herdr daemon 重启行为沉淀（pi-memory 审计回流）
- 提案: 把 daemon 切换的三个后果（workspace id 前缀整体迁移 w1B:*→w1:*、agent 状态重置 revision=1/seq 归零、session UUID 不变）与三步恢复（重枚举 agent list 按 UUID 尾段重建映射、向活跃 peer 广播新地址、不拿旧 seq 对比新状态）写成 pitfall
- 落点: pitfalls.md #31（Addressing 组）+ 头部计数 30→31 + SKILL.md 触发清单补 "addresses stopped working after a herdr daemon restart" 与计数
- commit: 97355fe
- 验证: uv run pytest 4 passed 4 skipped；sanitize-check CLEAN
