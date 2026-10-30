# glab-api — skill-impact log

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-12 | Merge 3 GENERAL lessons from pi-memory audit: ① `when:manual` retry creates new job ID → monitor pipeline-level; ② `sha=` filter needs full 40-char SHA (short SHA silently returns empty); ③ generalize curl fallback (any PUT/POST persistent 500/400, `-o` file against rtk) beyond discussion-resolve case（落点: SKILL.md quirks table (+2 rows) + decision ladder step 3） | 61e15b8 | none (docs-only skill, no tests) |
| 2026-10-29 | sanitize 存量泛化：retro #5 新 pattern 接线后全仓审计，SKILL.md 中内部 MR 号引用改 internal-MR 占位（行为零变化，纯脱敏）（落点: SKILL.md（引用占位）） | chore(sanitize): 泛化存量内部 MR 号引用与平台名（14 文件 23 处，历史残留接受） | git grep MR!\[0-9\] 归零；sanitize -a CLEAN；测试/文案未动行为 |
