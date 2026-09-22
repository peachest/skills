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
