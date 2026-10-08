# deslop — patterns

## P-001 audit.py 无 HTML 输入支持，直跑产生数量级假 flag
- 状态: absorbed-into-skill
- 现象: 对 lessons/*.html 直接跑 audit.py 测出 200-829 条 flag（标签属性当散文、DOCTYPE/导航行计入句长），全部为噪音；编排层被迫先用 teach 的 prose 提取逻辑（strip script/style/svg + 去标签）生成 deslop-audit/*.md 再审计
- 根因: contract gap——skill 文档只写了 .md 用法，无 HTML 模式
- 方案: audit.py 内建 HTML 支持（strip_html：strip 脚本/style/svg/head/注释 + td 单元格保行 + 去标签 + unescape）+ auto-detect + 数学保护区（$...$、\(..\)、\[...\] 掩码，词数/标点/语言判定全豁免）+ 句级语言判定改为 CJK 存在性优先（term-dense zh 句不再被公式掩码后误判 en）
- 验证数据（2026-10-08，7 课 + 0008）: 直跑 HTML vs 桥接 .md flag 数 6/7 课 ±2 内，0008 的 -13 为 .md 快照过期（课在 10-08 又改过）。残余 ±1-2 全部定位为桥接 .md 自身的转录损失（如把"的答案是，"规范化成"的答案是："），html-direct 更忠实
- passCheck: 对任一 lessons/*.html 跑 audit.py，flag 数与提取后 .md 的 flag 数一致（±0）
- 证据: 01a0bd84#2811
- 出现: 2026-10-06 diagnose#1
