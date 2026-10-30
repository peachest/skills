# fix — Skill Impact

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-27 | 路由指针：大量新鲜评审意见先走 challenge-and-fix fanout 定谳，fix 只修 ACCEPT/PROPOSE 存活项（verify-before-fix 原则不变）（落点: engineering/fix/SKILL.md 开头） | 78e6724 | 安装副本 sync-ok |
| 2026-10-30 | 同上：SKILL.md 工具名引用 ask_user_question → ask_user（vendor fork 改名的遗留失效引用）（落点: SKILL.md ask_user 引用行） | fix(skills): rename stale ask_user_question tool references to ask_user — vendor fork pi-ask-question renamed the tool, stale names pointed agents at a nonexistent tool | grep 零残留；post-commit hook 自动重装 |
