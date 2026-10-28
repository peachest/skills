# skill-impact — review-spec

无 rejected 记录。

| 日期 | 提案 | 落点 | commit | 验证 |
|------|------|------|--------|------|
| 2026-09-21 | diagnose#1: P-001 派发模板 / P-002 round 计数口径 / P-003 等待指引 | 未实施 | — | — |
| 2026-09-22 | challenger 攻击：P-002 refuted（版本混淆，契约 ad6a273 已有计数规则）、P-003 closed-historical（native wake + execution-controls 一读可达）、P-001 裁减为一句（re-inspect 派发须列已裁决 findings） | engineering/review-spec/SKILL.md，已重装 | 1718fba | verified：grep 'adjudicated' 已装副本命中 1 次；challenger 后未复跑 review-spec，P-001 passCheck 仍 0/2 |
| 2026-09-24 | 导航词防泄漏：review 词汇（ground truth/bearing/waymark/route）描述过程，不得出现在用户可读报告；报告 gap 用"spec 说 X，代码做 Y"的平实句式而非过程标签（"bearing mismatch"）。来源：session 01a0ce0a 用户打回"不要用隐喻，不要用压缩术语"；分析见 ~/research/baihua/analysis.md | engineering/review-spec/SKILL.md ## Report 节 | 见 git log | 已重装；报告节含 project's output rules 指针 |
| 2026-10-10 | challenger 环节入契约，当日两次迭代（38ec8ce 初版→用户改设计后定稿）：判定 Held 后双车道并行——后台派 challenger 挑战非 grilling findings（async，terminal notification 唤醒），前台立刻把 grilling gaps 批量问用户；双车道合流后修复 spec，再入 round 2/2 复审。裁定规则沿用 01a12025#entry198：challenger 立场不替代用户裁定，仅带证据明确反驳的 finding 可撤销（报告中标注）。grilling 不再走 grill-with-docs 一问一答，Routing 中相应条目移除。challenger 轮不消耗 2 轮 inspect 预算 | engineering/review-spec/SKILL.md ## Challenger round | 见 git log | 待下次 review-spec 实跑验证 |
| 2026-10-10 | 01a11f50 challenger 实证回写三项：re-inspect diff-scoped（修正轮不重跑五轴全量）、challenger 攻击面加裁决论证（结论对理由错）、parent 收口前 terrain 抽查 challenger load-bearing 声称 | engineering/review-spec/SKILL.md ## Challenger round + ## Routing re-inspect 段 | 见 git log | 待下次 review-spec 实跑验证 |
| 2026-10-10 | 01a0aeb3 回写两项：Gap classification 补过度 grilling 化错误模式（可机械对齐的 gap 升级为用户裁定=分类错误）；Challenger lane 补 findings 落盘（session 压缩后先合并五份报告+裁决为文档再派发）。challenger 四轴任务书结构（漏检/终判轴扩展）被用户否决，未入契约 | engineering/review-spec/SKILL.md ## Gap classification + ## Challenger round | 见 git log | 待下次 review-spec 实跑验证 |
| 2026-10-10 | Challenger round 委托化：攻击方法（四轴/信任分/建议/收口核/裁决论证/压缩落盘）移交 challenge-audit skill 单一维护，本 skill 只留独有三件——双车道并行、裁定规则（audit 立场不替代用户裁定）、不消耗 inspect 预算。有条件放行的 mechanical closes 改经 Routing 走 task 确认，不直接落地 | engineering/review-spec/SKILL.md ## Challenger round | 见 git log | 待下次实跑验证（观察与内嵌轮是否重复劳动的边界已消解） |
