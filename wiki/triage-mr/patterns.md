# patterns — triage-mr

来源：2026-09-11 手工核查（非 skill-call-diagnose 跑法：用户指认 peer session 偏离，人工读 trace 定位）。格式与状态机见 `../README.md`。

## P-001 gate 脚本只查线程首 note，假 gate=0 触发合理化
- 状态: absorbed-into-skill
- 现象: 线程 head 已 resolve 但回帖 note（裁决标签，resolvable=true, resolved=false）未 resolve 时，gate 仍报 0 open。agent 的独立扫描报 17 open 与 gate=0 矛盾，agent 判定自己的扫描"口径错误"、在 MR 上发错误勘误并宣告 done；用户纠正后才发现 gate 才是错的
- 根因: contract gap —— 平台 per-note resolve 语义未在脚本或 SKILL.md 中声明；且 SKILL.md 无"gate 与直接观察矛盾"的裁决规则，散文复述了脚本保证（"catches any inline thread whose resolve call silently failed"）而该保证不成立
- 方案: 脚本（落点 mr-review-triage）判定改为线程内全部 resolvable note resolved + 人类输出标注 [N/M notes open]；SKILL.md 增矛盾裁决规则（两边都别轻信，重查口径和盲区）
- 证据: 01a06643#3346,#3348,#3350（合理化+错误勘误）,#3355（用户纠正）,#3357（真修复）
- 出现: 2026-09-11 diagnose#1（同一 session 先后摔两次：误判"线程被重开"与误判"0 open 真值"）

## P-002 否定式指令无正向替代，两次被现场违反
- 状态: absorbed-into-skill
- 现象: "do not assemble it by hand at the end" 在连续两轮评审中都被违反——裁决全部完成后用 heredoc 一次性拼装 classified.json
- 根因: contract gap —— 禁止句无正向替代动作；"逐条定案后立即写"的行为未被写成可执行指令，agent 默认把 classified.json 当终产物而非过程产物
- 方案: SKILL.md 改正面表述：第一条 verdict 定案即创建文件、每条定案即时追加、end-of-run assembly 判流程违规；修复属 writing-for-agents 的 negation 失败模式实证
- 证据: 01a06643#3300（r11 heredoc 拼装）,#3351（r12 复犯）
- 出现: 2026-09-11 diagnose#1（2/2 轮，零抑制力）

## P-003 脚本能力缺口把 agent 推向手动路径
- 状态: absorbed-into-skill
- 现象: post-labels 脚本无失败发生，agent 仍整轮绕过它，手写 API 循环发 note + resolve——批量 note 级 resolve 是脚本做不了的操作，能力缺口成为绕过的实际诱因；手动路径又放大了 P-001（自制扫描口径错误）
- 根因: contract gap —— SKILL.md 手动 fallback 写成"On failure"未限定为脚本失败+范围外操作两类，且未要求每轮先跑脚本；脚本侧缺 note 扫尾能力
- 方案: post-labels.py 成功 resolve 线程后自动扫尾剩余 resolvable note；SKILL.md 改正向排序"每轮先跑脚本，手动仅限两类情形"
- 证据: 01a06643#3302,#3304（手写循环）,#3221（脚本最后一次真实运行停在 r11）
- 出现: 2026-09-11 diagnose#1（1 轮全程绕过；诱因链条：能力缺口→手动→口径错误→P-001 合理化）

## P-004 已安装 skill 被现场直接编辑，源仓未同步
- 状态: absorbed-into-skill
- 现象: peer session 分析评审建议误导性时，直接编辑了安装在 agent 目录的 fix skill（新增"suggested fix is a second, independent claim"段），源仓无此改动——重装即丢
- 根因: agent 即兴 —— skill 修改无"改源仓+重装"契约；edit 工具对已安装 skill 路径无约束
- 方案: 改动已搬回源仓并重装（本次修复）；通用规律候选 → 见 `_cross-skill/patterns.md` 后续观察
- 证据: 01a06643#3328,#3329（直接 edit 已安装 SKILL.md）
- 出现: 2026-09-11 diagnose#1（1 例）
