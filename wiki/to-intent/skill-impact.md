# skill-impact — to-intent

提案台账。被拒提案必须保留并写明拒绝理由——后续提案撞形状时先翻此表。

| 提案 | 落点 | commit | 验证命令与结果 |
|------|------|--------|----------------|
| S1 产品模式：INTENT.md（intentdocs 格式 v1.0，手写无 Sync 节），四级 intent（Product/Release/Story/Acceptance criterion），稳定 story id，完成 story 滚出地图 | SKILL.md product mode | 48df71d | 无（纯文档 skill 豁免）；真实用例验证见下 D1/D2 行 |
| S2 wayfinder 集成（单侧，vendor 不动）：fog check（Done-when 不可锐化 = fog → park 或交 wayfinder）+ hand off 步骤（sharp→to-spec / foggy→wayfinder / 整图→to-tickets） | SKILL.md product mode 步骤 3/5 | 48df71d | peer session 01a07b54（<project>）update pass 实测：fog check 逐 story 核查通过，hand off 表格被用户跟随执行 |
| D1 词表 Map 条目补 two-altitudes 交叉引用 | CONTEXT.md | 140db74 | grep 单一事实源确认 |
| D2 peer 实测暴露的区分：雾（认知性未知，Done-when 写不出）vs 外部前置（how 已知但依赖他人）——peer 裁决 R3 为外部前置而非雾，比 skill 文本更细。暂不回写，若后续 update pass 误判再收紧定义 | （未落点，观察中） | — | 01a07b54 session 5:38PM wayfinder 判据检验 + 5:49PM update pass |
| D3 effort 模式：intent/<slug>.md intake 工件（Problem/Proposed outcome/Constraints/Open questions，committed，status draft→accepted→done），Open questions 为分流路由（sharp→decision tickets / unsharp→Not yet specified / 空→to-spec 直通），三层栈 stories/effort/decisions | SKILL.md effort mode + effort-template | 5276f25 | 无（纯文档 skill 豁免）；待下一个真实 effort 用例验证 |
| R1 曾考虑替换产品模式为 Anthropic effort 粒度——被否：Anthropic 模型无产品地图/稳定 story id/release 排序，而 story id 是 token 链枢纽（<project> 实测）；两种粒度共存（three altitudes） | CONTEXT.md 词表（共存设计） | 5276f25 | 01a07b54 <project> 案例回溯分析 |
| D4 effort mode 三处加固（真实失败驱动）：① intro 加 write-first 原则——用户已陈述的意图先落盘，agent 核查属下游（进 Constraints/Open questions），"调查完毕但文件没写 = 失败 run"；② step 1 收窄为"读一个文件 + 判 origin"，执行级调查显式排除；③ step 3 quiz 限定四字段（执行问题属下游）+ step 4 落位硬锚（只有两处，todo/plans/ 对话不算持久化） | SKILL.md effort mode | cb40528 | 待下个真实 effort 用例验证；失败案例：peer session 01a0a3b3（2026-09-15）——/to-intent 调用后 24 分钟执行调查挤掉 quiz+write，todo×3+口头总结替代落盘，用户提醒两次才修正，且第一次仍落错位置（plans/ 而非 INTENT.md）。根因三洞：step 1 无停止边界 / quiz 被执行问题劫持 / 落位规范不敌 todo 工具默认吸引力 |
