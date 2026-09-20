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
