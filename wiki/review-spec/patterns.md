# patterns — review-spec

诊断史：每次 `/skill:skill-call-diagnose` 对 review-spec 的诊断发现沉淀于此。
证据格式 `session-id#entry`；条目号 = trace index 行号。

## P-001 re-inspect 派发缺少"已裁决事实锁定"要求（reduced-adopted）

- 状态: accepted-reduced（challenger 攻击后裁减，待落一句；passCheck 0/2）
- 触发条件: gap 修复后的 re-inspect 派发
- 现象: 01a0c2e3 在 round-2 派发 brief 中嵌入三项已裁决事实（防止 children 重翻已定案），该行为是当日执行中最有价值且契约中唯一缺失的；但原提案的 dispatch 模板/bundle 约定被 challenger 否决——两个实际 dispatch 文件仅共享 ~15 行，其价值恰在每次按 run 偏离模板（不同 TERRAIN、run 特有 watchpoints、仅 round-2 存在的裁决锁定），模板只会造成与 SKILL.md 五 check body 的第二份漂移副本
- 诊断教训（版本混淆）: 原 P-001/002/003 的证据主体来自 01a018e7（2026-08-19，pre-cap 旧契约版本）——诊断把契约版本差异误读为执行缺陷。跨 session 对比必须先版本锚定并核对契约引入时间（本条为 methodology 复盘）
- 方案（裁减后）: Routing/re-inspect 段落加一句——re-inspect 派发的 task 文本必须列出已裁决 findings，children 不得重翻。不加模板、不加 bundle 目录约定
- 证据: 01a0c2e3（round-2 brief 锁定三项裁决）；challenger 攻击记录 01a0c727#challenger
- 出现: 2026-09-21 diagnose#1 → 2026-09-22 challenger 攻击裁减

## P-002 inspect round 计数歧义 — refuted（版本混淆）

- 状态: refuted（2026-09-22 challenger）
- 原发现: 01a018e7 单 invocation 派发 3 次 inspect vs 01a0c2e3 计数 round 1/2、2/2，判为契约歧义
- 证伪: 01a018e7 跑 08-20 pre-cap 版本（无任何轮次上限，d032273 世代）；"at most twice + Count rounds explicitly" 由 ad6a273（2026-08-21）引入，01a0c2e3 行为与当前契约完全一致。无歧义，无需修改。旧 trace 的 3 连发反而是 cap 引入必要性的证据
- 教训: 跨 session 行为对比前，先 version-anchor 并核对契约条款的引入 commit 时间，避免把"契约演进"记成"执行缺陷"

## P-003 异步等待期间 polling/steer — historical（已过时）

- 状态: closed-historical（2026-09-22 challenger）
- 原发现: 01a018e7 re-inspect 等待期间 8 次计划外 poll + 1 interrupt + 2 steer
- 结论: 证据来自 08-19（native async wake 引入前）；当前 pi-subagents 契约明确 native wake 且 review-spec Step 3 强制读 execution-controls.md，等待指引一读可达。interrupt 是否净收益不可知（也可能及时解卡）。不加规则；保留作历史行为记录
## P-004 challenger 实证攻击模式（2026-10-10，session 01a11f50）

- 状态: accepted → 已落契约（三项）
- 触发条件: challenger 轮收口
- 现象: 01a11f50 两次 challenger——①攻击两轮 review 裁决链：0 A/4 B，裁决结论全部站住但 4 处论证被证伪，含"结论对理由错"（setter 裁决存留但其 wrapper 论证被 server.go:191 指针绑定实证推翻）与两轮联合漏报（异构 pod 并发写同 key 丢更新）；②攻击流程本身：1A/3B/2C，判决"30-40% 可剪"——round-1 的 14 gap 中 12 条是 spec v2 发布压缩细节自造（发布即降级，非 review 功劳）；decision-trace 3 次全绿、bearing 2 次空手
- 落契约: ①re-inspect 改 diff-scoped（修正轮只审 diff + findings 闭环，五轴全量只在首轮）②challenger 攻击面加裁决论证 ③parent 收口前对 load-bearing 声称做 terrain 抽查
- 证据: 01a11f50#271/#276/#282（裁决链挑战）/ #355/#366（流程挑战）
- 附带教训（route 发布侧）: spec 全文发布 + diff 复审可把 4 轮压 2 轮——属 spec 撰写侧而非本 skill，已在作者 memory 沉淀
## P-005 challenger 落盘与分类审计（2026-10-10，session 01a0aeb3）

- 状态: accepted-reduced（四轴任务书结构未采纳——用户裁定，见 skill-impact rejected 记录）
- 触发条件: challenger 派发 / gap 分类
- 现象: 01a0aeb3 对 pi-events-daemon 12 份 spec 两轮 review 意见做 challenger 审计，可信度 78/100 有条件放行，9 项发现（2A/5B/2C）全真。两个可吸收点：①session 已压缩、五份报告不在手上——parent 先把两轮 findings+裁决合并落盘 review-findings.md 再派发，challenger 需要可交叉审阅的文档而非重建记忆；②分类轴战果——SQLite 裁定被判"过度 grilling 化"（terrain vs terrain 可机械对齐，#31 头部 declared 单一权威来源），accept。round-1/2 复盘 task 占绝大多数、grilling 仅 2 项其中 1 项属过度升级
- 未采纳: challenger 四轴任务书结构（假 gap/漏检/分类/终判）。本次战果主力在漏检轴（五轴集体漏掉的 7/9 项），但现有契约的逐条攻击+裁决论证攻击已覆盖主要面，四轴扩展被用户否决——无新证据不得重提
- 落契约: ①Gap classification 补"过度 grilling 化是分类错误"②Challenger lane 补"报告不在手上先落盘合并文档"
- 证据: 01a0aeb3#2007（任务书）/ #2016-2017（挑战挑战者 grep 核实）/ review-findings.md Challenger 审计节
