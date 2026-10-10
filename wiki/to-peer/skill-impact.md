# to-peer — skill-impact 台账

## 2026-09-24 创建 skill（用户指令）
- 提案: 新建 to-peer skill——创建 peer session 一律开**新 herdr tab**（`tab create --cwd` → `agent start`），不用 pane split（用户拍板）；herdr 适配器为 `scripts/herdr-tab-peer.sh`，支持 `--prompt-file/--label/--focus`；通信协议归 multi-agent-collab，本 skill 只管创建
- 落点: 新建 `in-progress/to-peer/`（SKILL.md + scripts/herdr-tab-peer.sh + scripts/check-env.sh + tests/test.sh）；multi-agent-collab SKILL.md bootstrap 小节加一行指路（新 tab 拓扑归 to-peer，pane split 降级为 legacy fallback）
- 验证: tests/test.sh 9/9（含 live smoke：真实建 tab + agent start + 关 tab）；check-env PASS；npx skills add -g 两个 skill 均装成功
- 状态: accepted
- 关联: academy/scripts/spawn-course.sh 的 ponytail 注释（"第二个 tab-spawn 消费者出现时上提"）——本 skill 即该消费者；academy 未改动，后续可考虑改走 to-peer

## 2026-09-24 --workspace 支持（用户需求实锤：跨项目派发）
- 提案: 用户 topology = 每项目一个 herdr ws，跨项目任务需把 peer 建到目标项目 ws（现场案例：<session-id> 需把 chart 更改派到 <project-ws> ws）。加 --workspace（id 或 label，精确→片段匹配，歧义报错列候选）；顺带吸收 call-extract 发现的两个缺口：cwd 缺省 $PWD、--prompt-file - 走 stdin（免 /tmp 中转）。创建后回读实际 workspace_id（daemon 前缀迁移 w1B:→w1: 教训），以回读值为准
- 落点: scripts/herdr-tab-peer.sh + SKILL.md 参数表 + tests/test.sh（11/11，含真实跨 ws smoke）
- 验证: live smoke 在 w1 建 tab + agent start + 关 tab；ws smoke 断言 workspace_id 回读一致
- 状态: accepted（判定段后经用户澄清重写，见下条）

## 2026-09-24 --runtime 跨 runtime（现场案例补全）
- 提案: 现场案例落实时发现目标 ws 在另一个 herdr runtime（dev），脚本默认只打当前 runtime；加 --runtime R（herdr --session R）支持跨 runtime 建 peer。同 label 多 ws（<project-ws> w6/wJ）由 workspace 歧义报错路径兜住，人工消歧后用 id
- 落点: scripts/herdr-tab-peer.sh（hr() 包装）+ SKILL.md；tests 11/11
- 状态: accepted

## 2026-09-24 新建 vs 复用判定（现场误投案例）
- 现象: <session-id>（<project-repo>）向 <project-ws> peer wJ:p1 投递 chart 任务，delivered=true；但 wJ:p1 有自己的在办职责（harborblue 镜像检查），用户纠正后 via to-peer 新建 vendor-ascend（wJ:p2）重新派发
- 根因: agent 即兴——agent 查了 agent_status=idle 就投递，但 idle ≠ 无在办职责；"查状态" ≠ "查职责"。状态机里没有"该 peer 是否已被占用"的判据
- 方案: SKILL.md 加"新建 vs 复用"判定：跨项目/跨职责派发默认新建 peer；同任务线追加工作才发给已有 peer
- 触发条件: 向已存在的 peer 投递新任务前的 target 选择
- passCheck: SKILL.md 含"新建 vs 复用"段；后续 dispatch 决策 trace 中出现"职责"判定
- 证据: <session-id>#348,#351,#352-#358
- 出现: 2026-09-24（人工判定，非 diagnose 流程）

## 2026-09-24 分工修正（用户澄清原意）
- 提案: 用户澄清 to-peer 契约 = 恒新建，不做复用判断；复用路径归 multi-agent-collab（用户显式给 session id/名称）。上一条"跨项目/跨职责默认新建"的判定写复杂了——那不是 to-peer 里的决策，误投案例的教训是"复用已有 session 前确认职责"，归属 multi-agent-collab 侧的复用路径
- 落点: SKILL.md "新建与复用的分工" 段重写
- 状态: accepted
