# patterns — reckon

来源：2026-09-10 diagnose#1（4 trace / 13 次注入，覆盖原版契约 2 次 + 强化版 11 次、单项目到 5 项目、轻 1 次到重 6 次/会话）。格式与状态机见 `../README.md`。

## P-001 重注入无策略：over-comply 或 under-comply 两极漂移
- 状态: open
- 现象: session 进行中被重注入（位置刚在 N 轮内陈述过且无 compaction）时，契约把注入一律当冷启动，agent 行为分裂——要么 over-comply 重跑全量多仓基线采集（与 1-3 分钟前的位置完全重叠），要么 under-comply 直接跳过/改形 cold-start（改形为里程碑表格或只有工具调用无基线文本）。同一根因的两种失败面
- 根因: contract gap —— 契约无"重注入策略"条款：位置新鲜 + 无 compaction 时该做什么（增量 diff？直接续用？）未定义，全靠模型自觉
- 方案: skill-doc——补"位置新鲜短路"条款：重注入时若 N 轮内已陈述位置且无 compaction，跳过全量重建，仅增量 diff（或声明位置未变直接续用）
- 证据: 01a0435a#1193,#2114,#2238; 019fd573#1630,#2483,#2813
- 出现: 2026-09-10 diagnose#1（over-comply 3 例 ≈7.2K out + 15 轮浪费；under-comply 3 例含 1 次整体跳过）

## P-002 compaction 后重建基线系统性缺失
- 状态: open
- 现象: compaction 发生后首个响应未重建基线（契约 rule 4 强制）。重 trace 五次 compaction 0 次重建（间隔 19h/3 天位置无修复）；另两条 trace 各 1 违反；唯一正例是 agent 自报"按 rule 4 重建"
- 根因: contract gap —— compaction 检测条件模糊（"context feels truncated"无操作化判据），agent 难以自查是否刚被压缩
- 方案: skill-doc——把 compaction 检测操作化：compaction 事件在 JSONL 有显式 entry，若上下文缺近期 turn 记录/出现压缩摘要即触发重建；或契约改为"每次注入都重建"（用简单换可靠，代价是 P-001 的浪费面）
- 证据: 01a0435a#341,#798,#1068,#1637,#2682; 019fd573#3289; 01a0610e#431; 正例 01a04249#1417
- 出现: 2026-09-10 diagnose#1（7 违反 / 1 正例）

## P-003 禁写格式在否定条款下仍复现
- 状态: open
- 现象: `map: 无 open wayfinder map` 写法被契约明文禁止（"Writing it is the same error as omitting..."），仍在 3 次基线出现（2 条 trace 系统性）。否定条款（don't write X）强度不足以覆盖默认倾向
- 根因: agent 即兴 —— "无 map"被当成值得陈述的状态而非沉默；否定条款无正向替代动作
- 方案: skill-doc——补正向替代：检测无 open map 后直接检查下一数据源（跳过行为），把"沉默"写成动作而非禁令
- 证据: 019fd573#2488,#2816; 01a0610e#430
- 出现: 2026-09-10 diagnose#1（3/13 次，违反强化版明文条款）

## P-004 状态采集三脚本缺口（skill 为纯规则形态）
- 状态: open
- 现象: 每次 baseline 手写 bash 采集位置，合计 36 调用 / ~33K args / ~36K 结果重读，~80% 是三个重复形状：①逐仓 git 位置（13/13 次，上游 ref 三种写法漂移，双 remote origin/internal 混淆致 4 次失败恢复）②MR/pipeline 状态（≥12 次，4 种变体含手写 token 内联）③wayfinder map/票闭环态（3 种风格 + 闭环循环逐字重复）。环境怪癖（git 全路径避 rtk 污染、PATH 补 glab）逐 trace 重新发现
- 根因: contract gap —— 纯规则契约把可脚本化采集留给即兴，glab-api skill 的决策梯知识未回流
- 方案: skill-script——`scripts/position.sh`（一行一仓：path|branch|ahead|dirty|last-3，内固化 remote 解析链与全路径）> `scripts/mr-state.sh`（glab api 零手写 token）> `scripts/frontier.sh`（map→open/pending 输出）；退路：三段 canonical 命令片段写死进 SKILL.md
- 证据: 01a019fd573#1473,#2484,#2814; 01a0435a#475,#1194,#1203-1211,#2115,#2239; 01a04249#1046,#1048,#1050,#1054,#1056; 01a0610e#426,#428
- 出现: 2026-09-10 diagnose#1（29/36 调用可脚本化）

## P-005 模板字段 step n/m 从未被使用
- 状态: open
- 现象: 单行 restate 模板的 step n/m 段 0/13 次出现，全部被状态描述符（tip sha/MR 状态/任务短语）替代——字段是 no-op，不改变 agent 行为
- 根因: 知识提取 —— 模板字段无先验支撑（模型不倾向维护 step 计数）
- 方案: skill-doc——从模板删除 step n/m，改用状态描述符占位（写 agent 实际会填的东西）
- 证据: 01a0435a#2113; 019fd573#2888
- 出现: 2026-09-10 diagnose#1（0/13 使用）

## P-006 项目/worktree 发现凭记忆硬编码
- 状态: open
- 现象: 契约写明的 `git rev-parse --git-common-dir` 只在 1 次失败尝试出现后即弃，其余 12 次 baseline 项目集从会话记忆硬编码路径，worktree 归并靠命名约定而非 git 事实；项目集漂移（2 仓→4 仓）时无机制发现新项目；采集传输形态（批量工具）可用性漂移致 worktree 字段丢失
- 根因: contract gap —— 项目发现无持久载体（注册表），每 session 从零重推
- 方案: skill-doc（或 skill-script）——baseline 末尾维护项目注册表文件，注入先读注册表再增量发现新项目
- 证据: 01a04249#1046,#1048; 019fd573#2488; 01a0435a#481
- 出现: 2026-09-10 diagnose#1（12/13 凭记忆）
