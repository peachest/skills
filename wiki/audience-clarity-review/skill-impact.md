# audience-clarity-review — Impact Log

One line per behavioral change: proposal / landing / commit / verification.

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-09-11 | (above)（落点: (above)） | lost-hash | section-shots.mjs run against real artifact (cxl-bench cxl-l2-blueprint.html, 128K): 9 sections shot with correct Chinese headings, fullPage + manifest.json emitted |
| 2026-09-11 | First real run (peer session 01a08f6d, cxl-l2-blueprint.html) exposed: doc-reviewer's tools contract declares bash but review-role allowlist omits it → all six children died as lane infrastructure failure; peer fell back to builtin delegate (passed). Switched step 5 to dispatch via `delegate` with the doc-reviewer ban + rationale inline.（落点: SKILL.md step 5 rewritten） | fix(audience-clarity-review): dispatch via builtin delegate — doc-reviewer bash tool contract unsatisfiable for review fan-out | Peer session full trace audited: six axes completed via delegate, findings files persisted, report spot-checked against HTML source (helper bare-use s01, "Index 刚启动" bare-use, "回源" single-occurrence all confirmed). Report verdict count corrected on-site (table 5 high + 17 low vs claimed 6/16) |
| 2026-10-30 | 同上：SKILL.md 工具名引用 ask_user_question → ask_user（vendor fork 改名的遗留失效引用）（落点: SKILL.md ask_user 引用行） | fix(skills): rename stale ask_user_question tool references to ask_user — vendor fork pi-ask-question renamed the tool, stale names pointed agents at a nonexistent tool | grep 零残留；post-commit hook 自动重装 |
