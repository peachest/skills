# re-ask — Skill Impact

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-30 | 新建 skill（in-progress/re-ask）：会话/文档双模式重问（四段中立模板）+ 重解释（三段模板），仅手动触发，无参数自动回溯最近提问/产出；病型四类入 references/pitfalls.md；进度重述显式拒接（orient 域）。动机：全库挖掘 183 条纠偏消息（重问 50 + 重解释 104），同一形态跨 session 复发（「重新问问题」9 连发）；模板正典 = peer 客户答疑会问题清单四段式重构 | feat(skills): add re-ask — question/produce rewrite with explicit implicit context | 人工核对：双分支模板对挖掘病型逐条覆盖（P-001~P-004）；diff 源仓 vs 安装副本一致 |
| 2026-10-30 | skill 里 3 处工具名引用写的是 ask_user——工具最终定名 ask_user_question（本仓 8155b7f 对齐上游、skills 仓 450bc55/00c7674 revert 中间态改名），统一到最终名（落点: in-progress/re-ask/SKILL.md 3 处） | fix(skills): re-ask stale ask_user references — tool was renamed back to ask_user_question, align skill to the final name | grep re-ask/SKILL.md 零残留 ask_user 裸名 |
