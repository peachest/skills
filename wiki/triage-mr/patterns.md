# patterns — triage-mr

来源：2026-09-11 手工核查（非 skill-call-diagnose 跑法：用户指认 peer session 偏离，人工读 trace 定位）。格式与状态机见 `../README.md`。

## P-001 gate 脚本只查线程首 note，假 gate=0 触发合理化
- 状态: absorbed-into-skill
- 现象: 线程 head 已 resolve 但回帖 note（裁决标签，resolvable=true, resolved=false）未 resolve 时，gate 仍报 0 open。agent 的独立扫描报 17 open 与 gate=0 矛盾，agent 判定自己的扫描"口径错误"、在 MR 上发错误勘误并宣告 done；用户纠正后才发现 gate 才是错的
- 根因: contract gap —— 平台 per-note resolve 语义未在脚本或 SKILL.md 中声明；且 SKILL.md 无"gate 与直接观察矛盾"的裁决规则，散文复述了脚本保证（"catches any inline thread whose resolve call silently failed"）而该保证不成立
- 方案: 脚本（落点 mr-review-triage）判定改为线程内全部 resolvable note resolved + 人类输出标注 [N/M notes open]；SKILL.md 增矛盾裁决规则（两边都别轻信，重查口径和盲区）
- 证据: 01a06643#3346,#3348,#3350（合理化+错误勘误）,#3355（用户纠正）,#3357（真修复）
- 出现: 2026-09-11 diagnose#1（同一 session 先后摔两次：误判"线程被重开"与误判"0 open 真值"）→ absent-this-run 2026-10-15 diagnose#2（触发条件覆盖：resolve 失败拉锯中双向核查合规，逐 id GET 查分页盲区未合理化任一边，01a12f97#849,#854）

## P-002 否定式指令无正向替代，两次被现场违反
- 状态: absorbed-into-skill
- 现象: "do not assemble it by hand at the end" 在连续两轮评审中都被违反——裁决全部完成后用 heredoc 一次性拼装 classified.json
- 根因: contract gap —— 禁止句无正向替代动作；"逐条定案后立即写"的行为未被写成可执行指令，agent 默认把 classified.json 当终产物而非过程产物
- 方案: SKILL.md 改正面表述：第一条 verdict 定案即创建文件、每条定案即时追加、end-of-run assembly 判流程违规；修复属 writing-for-agents 的 negation 失败模式实证
- 证据: 01a06643#3300（r11 heredoc 拼装）,#3351（r12 复犯）; 复发: 01a12f97#709→#805（R2.5 裁定到落盘滞后 35min）、#843→#909（R3 verdict 已贴远端 3.7min 后才入账）、#835,#843（stdin heredoc 直发 post-labels、classified.json 后补）
- 出现: 2026-09-11 diagnose#1（2/2 轮，零抑制力）→ refuted 2026-10-15 diagnose#2（正面表述落地后复发，轻度变体：由整轮末拼装降为分钟级滞后，但中断窗口内已贴 verdict 仍会丢）
- 方案(追加): post-labels 加 `--classified <path>` 文件直读写模式，物理消灭 heredoc 双写（台账 S4）

## P-003 脚本能力缺口把 agent 推向手动路径
- 状态: absorbed-into-skill
- 现象: post-labels 脚本无失败发生，agent 仍整轮绕过它，手写 API 循环发 note + resolve——批量 note 级 resolve 是脚本做不了的操作，能力缺口成为绕过的实际诱因；手动路径又放大了 P-001（自制扫描口径错误）
- 根因: contract gap —— SKILL.md 手动 fallback 写成"On failure"未限定为脚本失败+范围外操作两类，且未要求每轮先跑脚本；脚本侧缺 note 扫尾能力
- 方案: post-labels.py 成功 resolve 线程后自动扫尾剩余 resolvable note；SKILL.md 改正向排序"每轮先跑脚本，手动仅限两类情形"
- 证据: 01a06643#3302,#3304（手写循环）,#3221（脚本最后一次真实运行停在 r11）; 复发: 01a12f97#810（R2.5 零脚本宣成 false-done）、#945（R4 手工 urllib 且 verdict reply 整个省略）；R3 手动路径 #843-#906 属合法 fallback——脚本在该 GitLab 实例结构性失败，能力缺口已由 2026-10-15 note 级 fallback 修复（mr-review-triage，台账 F1）
- 出现: 2026-09-11 diagnose#1（1 轮全程绕过）→ refuted 2026-10-15 diagnose#2（script-first 排序规则仍被 R2.5/R4 违反；R3 手动属合法 fallback 不计违规）

## P-004 已安装 skill 被现场直接编辑，源仓未同步
- 状态: absorbed-into-skill
- 现象: peer session 分析评审建议误导性时，直接编辑了安装在 agent 目录的 fix skill（新增"suggested fix is a second, independent claim"段），源仓无此改动——重装即丢
- 根因: agent 即兴 —— skill 修改无"改源仓+重装"契约；edit 工具对已安装 skill 路径无约束
- 方案: 改动已搬回源仓并重装（本次修复）；通用规律候选 → 见 `_cross-skill/patterns.md` 后续观察
- 证据: 01a06643#3328,#3329（直接 edit 已安装 SKILL.md）
- 出现: 2026-09-11 diagnose#1（1 例）→ absent-this-run 2026-10-15 diagnose#2

## P-005 脚本目录无解析规则，安装位置迁移即断
- 状态: absorbed-into-skill
- 现象: SKILL.md 对 `<SCRIPTS_DIR>` 只写 "resolve it before running"，agent 硬编码安装路径侥幸命中；安装副本被清理后脚本 ENOENT，需 find 全盘探测才恢复。注：成本曾被高估为"约 10 次查找"，trace 证实为 3 次 ENOENT + 6 次定位轮（其余是目录删除前的成功调用）
- 根因: contract gap —— 无解析规则，也无"注入头自带 location"的利用指引
- 方案: mr-review-triage SKILL.md 写明解析规则（相对本 SKILL.md 目录解析，对照注入 location，勿搜其他 skill 根）
- 触发条件: trace 中出现脚本路径 ENOENT 或对 skill 目录的探测调用
- passCheck: SKILL.md 含解析规则段；后续 trace 中脚本路径失败后一步内恢复
- 证据: 01a12f97#815,#817,#819（ENOENT→find→重发，≈521 out tok）
- 出现: 2026-10-15 diagnose#2

## P-006 平台 resolve 端点非标，错误响应与实际状态不一致放大重试
- 状态: absorbed-into-skill
- 现象: 某内部 GitLab 实例 discussion 级 PUT 一律 500、notes POST 404；手工 saga 16 调用/3.5min 才试出 note 级 PUT 配方；notes 级 PUT 返回 404 却实际生效，错误语义与真实状态脱节进一步放大重试
- 根因: contract gap —— 平台 quirk 只进 memory 不进 reference 文档；脚本无 fallback
- 方案: mr-review-triage reference/gitlab.md 增 quirk 条目（症状/配方/端点表）；post-labels 的 note 扫尾函数兼作 discussion-PUT 失败时的 fallback resolve
- 触发条件: post-labels 或 resolve 调用返回 5xx/404/415
- passCheck: gitlab.md 含 quirk 节；post-labels 在该实例上 resolve 成功（stderr 出现 note-level fallback）
- 证据: 01a12f97#843-#906（500×6、404×6、415、400×3，≈227s ≈7.4K out tok）
- 出现: 2026-10-15 diagnose#2

## P-007 pull 结果摘要解析器每轮重写
- 状态: open
- 现象: 每轮 pull 后手写 python3 -c 摘要 findings/diff classified，同形 3 种写法重复 6 次
- 根因: contract gap —— pull 脚本不输出 digest，摘要逻辑无承载点
- 方案: ocr-pull-discussions.py 加 `--digest [--against classified.json]`，输出 "N total/M new + id8|file:line|body[:120]"（台账 S5）
- 触发条件: pull 命令后紧跟 python3 -c 摘要
- passCheck: 后续 trace 中 pull 后无手写摘要脚本
- 证据: 01a12f97#444,#470,#679,#819,#833,#931（≈900 out tok + 结果重读）
- 出现: 2026-10-15 diagnose#2
