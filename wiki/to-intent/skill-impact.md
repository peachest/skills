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
