# patterns — teach skill 已知问题

冷启动自 okb diagnose#1 的跨 skill 移交（trace 01a062a0，teach-lab session 中的 teach 域手工重复操作）。格式同 `../README.md`。

## P-T01 rep() 锚定 HTML 编辑 heredoc 手写
- 状态: open
- 现象: 同一 `def rep(old,new): assert old in html` 形状的 heredoc python 在单 trace 出现 7 次，其中 2 次是断言失败（锚点被前次编辑改变）后的重试，浪费 output ≈7.7K tokens
- 根因: teach 的 lesson HTML 编辑无工具支撑，agent 每次手拼替换脚本
- 方案: 沉淀 `lesson-edit.py`（锚点批量替换 + 失败时输出近似锚点建议），teach skill 引用
- passCheck: 编辑 lesson HTML 的工具调用不再是内联 rep() 定义，而是脚本调用
- 证据: 01a062a0#239 #251 #271 #334 #343 #349 #353 #357
- 出现: 2026-09-20 okb-diagnose#1 移交（源 trace 01a062a0，teach-lab session）

## P-T02 cat >> 手拼记账块
- 状态: open
- 现象: fact-check addendum / session-log / NOTES 等追加块用 cat >> 手写 7 次
- 根因: teach 的记账文件无 append 工具
- 方案: 随 P-T01 一并沉淀（`lesson-log.py --file --heading --lines`），或 teach SKILL.md 规定统一 append 模板
- passCheck: 追加记账的动作不逐字手拼 heredoc
- 证据: 01a062a0#241 #253 #275 #289 #294 #308 #359
- 出现: 2026-09-20 okb-diagnose#1 移交

## P-T03 五检链手敲
- 状态: open
- 现象: css→prose→beat→nav 检查命令链手拼 3 次；NOTES 里已文档化但每次仍要重新拼装
- 根因: 文档化的检查序列没有可执行入口
- 方案: `check-all.sh` 包装既有检查序列
- passCheck: 检查以单命令入口调用
- 证据: 01a062a0#343 #349 #357
- 出现: 2026-09-20 okb-diagnose#1 移交
## P-T04 edit 工具 CJK 归一化污染字节精确替换
- 状态: open
- 现象: spec-decoding 全课程 spec-audit（2026-10-06，session 01a11088 系）：③ worker 实锤 edit 工具对 lesson HTML 做全角→半角自动归一化，破坏字节精确替换锚点；worker 回滚改用 byte-precise replace 重做
- 根因: harness 层 edit 工具的规范化行为，skill 无法修
- 方案: 双头——① lesson-edit.py（P-T01）实现时用 Python 字节级 replace（不做 unicode normalize），规避此坑；② 向 pi harness 上报 edit 归一化行为，确认是否可关
- passCheck: 涉及全角/CJK 标点的 lesson 替换不再经 edit 工具（走 lesson-edit.py 或 python heredoc）
- 证据: spec-decoding session-log/0007-20260924.md「worker 自查发现 edit 工具全角→半角归一化污染，回滚重做」（commit de15bf4）
- 出现: 2026-10-06 spec-audit worker 自查

## P-T05 beat-check hook 15% 窗口边缘 case 反复出现
- 状态: open
- 现象: 两单独立 case（spec-decoding ④ 问句在 15.8%、43 字差窗口边缘；早期 lesson-0003 同类）被判 out-of-window 后走人工裁定——窗口是启发式，边界差 1-2% 导致的裁定税
- 根因: HOOK_PAT 扫描窗口 max(200, 15%·total) 是拍板值，无 advisory 过渡带
- 方案（待评估，攒着）: 15% 硬窗口 + 20% advisory 提示（"问句在 15-20% 带内，裁定时注意"），或放宽到 18%；需先看 15.8% 这类案例真实占比再定
- passCheck: 15-20% 带内问句不再硬 FAIL，改为带提示的 finding
- 证据: spec-decoding reviews/0004-spec-review.json（beat hook finding adjudicated kept，问句 15.8% vs 15% window）
- 出现: 2026-10-06 spec-audit；同 2026-09-24 lesson-0003
## P-T06 知识点覆盖缺口：paper 版本外的设计无抽取触发（知识工程盲区）
- 状态: open
- 现象: spec-decoding 课⑦ 漏讲 EAGLE-3 词表压缩（32k 子集 + d2t/t2t）——该设计不在 ACL 版 paper.tex（461 行逐行核零命中），只在 tech report 与代码（cnets.py:487、specforge/data/preprocessing.py:626-782）。学习者从工程课的六算法矩阵追问才暴露。回补已交付（课程 commit 80e8e93，五检全绿）
- 根因: 信源抽取以"论文管道"为单位（tex 五类清单），paper-外的机制性设计（tech report 独有、代码独有）没有对应的抽取触发点；PLAN 节点描述也是按论文口径写的，交付 gate 无"代码实现 vs 论文描述"覆盖对账
- 方案（分两层）: ① 开课 checklist（teach 侧，立即可做）：机制性设计逐条标注 论文仅/代码仅/两处——即"代码对账"从分歧处理升级为交付前置；② 知识点工程（结构层，待设计）：以 PLAN 节点为覆盖清单，对账三层信源的可用知识点（tex sections × repo modules × 解读文章），产出覆盖矩阵，交付 gate 校验"节点声明的主机制在每个有它的信源层都被抽取过"
- passCheck: 新开课时，课程引用的每个机制能在信源覆盖矩阵里找到"来源层"标注；仅代码有的设计默认进 coverage 对账而非依赖学习者追问暴露
- 证据: herdr 回执 w3:p2（01a0bd84，2026-10-08）；课程 commit 80e8e93；papers/2503.01840-eagle3/source/paper.tex 461 行 vocab 零命中
- 出现: 2026-10-08 spec-decoding 课⑦
## P-T07 验证 regime 按课型静态路由被证伪
- 状态: rejected
- 现象/提案: 第二轮增量的"验证流矩阵"（tex 主导课→anchor-check；code 主导课→fact-check worker）
- 否决证据: specforge trace（2026-10-08）——code-contract 课（0004/0006/0007/0008）恰是 anchor-check 最重度用户（21→1、40→1 收敛）；0007 同小时两种 regime 并用。按课型路由会跳过 quote/number 修复
- 裁定: anchor-check（机械 quote/number 复核）与 fact-check worker（claim 真假）每课都跑；课型只决定 sources 的 kind 分布。 challenger D3 记录于此防重提
- 证据: 967bea29 challenger report；FORGE jsonl 10:18-13:57

## P-T08 ledger CLI 过早（schema 未稳 + 4 动词覆盖率 61%）
- 状态: deferred
- 现象/提案: 4 动词 CLI（add-claim/patch-quote/add-source/verdict）折叠 ~163 个 anchors.json/ledger 编辑 heredoc
- 否决证据: 103 个真实 mutation heredoc 中 39% 是数据依赖的批量迁移（读上游算新值），CRUD 类仅 61% < 70% 自设线；schema 在 trace 内翻过面（claims dict→list）；疼痛集中两次爆发而非稳态
- 裁定: 降级为"schema 强制器"定位（okb 侧 load/write 核心 + heredoc 逃生口），等第二门课验证 schema 不变后再评估动词集。 folding 主张撤回
- 证据: d3eda845 challenger report（heredoc 聚类统计）
- 出现: 2026-10-08 challenger round
