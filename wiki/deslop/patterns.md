# deslop — patterns

## P-001 audit.py 无 HTML 输入支持，直跑产生数量级假 flag
- 状态: open
- 现象: 对 lessons/*.html 直接跑 audit.py 测出 200-829 条 flag（标签属性当散文、DOCTYPE/导航行计入句长），全部为噪音；编排层被迫先用 teach 的 prose 提取逻辑（strip script/style/svg + 去标签）生成 deslop-audit/*.md 再审计
- 根因: contract gap——skill 文档只写了 .md 用法，无 HTML 模式
- 方案: audit.py 增加 HTML 输入支持（内置 strip 脚本/style/svg/head/注释 + 去标签 + unescape，同 teach prose 提取），或 SKILL.md 写明桥接脚本
- passCheck: 对任一 lessons/*.html 跑 audit.py，flag 数与提取后 .md 的 flag 数一致（±0）
- 证据: 01a0bd84#2811
- 出现: 2026-10-06 diagnose#1
