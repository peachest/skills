# daily-recap — Skill Impact

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-30 | SKILL.md 引用的工具名 ask_user_question 已失效（vendor fork 改名为 ask_user），agent 按 skill 指引调用不存在的工具名——全部改为 ask_user；daily-recap 读史场景保留旧名注记（落点: SKILL.md ask_user 引用行） | fix(skills): rename stale ask_user_question tool references to ask_user — vendor fork pi-ask-question renamed the tool, stale names pointed agents at a nonexistent tool | grep SKILL.md 零残留旧名（daily-recap 注记除外）；post-commit hook 自动重装安装副本 |
