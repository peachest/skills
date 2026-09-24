# skill-impact — review-spec

| 日期 | 提案 | 落点 | commit | 验证 |
|------|------|------|--------|------|
| 2026-09-21 | diagnose#1: P-001 派发模板 / P-002 round 计数口径 / P-003 等待指引 | 未实施 | — | — |
| 2026-09-22 | challenger 攻击：P-002 refuted（版本混淆，契约 ad6a273 已有计数规则）、P-003 closed-historical（native wake + execution-controls 一读可达）、P-001 裁减为一句（re-inspect 派发须列已裁决 findings） | engineering/review-spec/SKILL.md 1718fba，已重装 | verified：grep 'adjudicated' 已装副本命中 1 次；challenger 后未复跑 review-spec，P-001 passCheck 仍 0/2 |

无 rejected 记录。
| 2026-09-24 | 导航词防泄漏：review 词汇（ground truth/bearing/waymark/route）描述过程，不得出现在用户可读报告；报告 gap 用"spec 说 X，代码做 Y"的平实句式而非过程标签（"bearing mismatch"）。来源：session 01a0ce0a 用户打回"不要用隐喻，不要用压缩术语"；分析见 ~/research/baihua/analysis.md | engineering/review-spec/SKILL.md ## Report 节 | 见 git log | 已重装；报告节含 project's output rules 指针 |
