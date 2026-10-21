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
- 落地: bf6282b（解析规则段）→ #65 triage-mr SKILL.md 重写同步同规则并补充 .triage/ 状态路径 cwd/realpath 说明
- 触发条件: trace 中出现脚本路径 ENOENT 或对 skill 目录的探测调用
- passCheck: SKILL.md 含解析规则段；后续 trace 中脚本路径失败后一步内恢复
- 证据: 01a12f97#815,#817,#819（ENOENT→find→重发，≈521 out tok）
- 出现: 2026-10-15 diagnose#2

## P-006 平台 resolve 端点非标，错误响应与实际状态不一致放大重试
- 状态: absorbed-into-skill
- 现象: 某内部 GitLab 实例 discussion 级 PUT 一律 500、notes POST 404；手工 saga 16 调用/3.5min 才试出 note 级 PUT 配方；notes 级 PUT 返回 404 却实际生效，错误语义与真实状态脱节进一步放大重试
- 根因: contract gap —— 平台 quirk 只进 memory 不进 reference 文档；脚本无 fallback
- 方案: mr-review-triage reference/gitlab.md 增 quirk 条目（症状/配方/端点表）；post-labels 的 note 扫尾函数兼作 discussion-PUT 失败时的 fallback resolve
- 落地: bf6282b（quirk 节 + note 级 fallback）；#61/#62 post 语义硬化后 fallback 保留；#65 删除 reference 中手动 resolve 配方段并替换内部实例昵称为中性表述（脚本内 fallback 为唯一路径）
- 触发条件: post-labels 或 resolve 调用返回 5xx/404/415
- passCheck: gitlab.md 含 quirk 节；post-labels 在该实例上 resolve 成功（stderr 出现 note-level fallback）
- 证据: 01a12f97#843-#906（500×6、404×6、415、400×3，≈227s ≈7.4K out tok）
- 出现: 2026-10-15 diagnose#2

## P-007 pull 结果摘要解析器每轮重写
- 状态: absorbed-into-skill
- 现象: 每轮 pull 后手写 python3 -c 摘要 findings/diff classified，同形 3 种写法重复 6 次
- 根因: contract gap —— pull 脚本不输出 digest，摘要逻辑无承载点
- 方案: ocr-pull-discussions.py 加 `--digest [--against classified.json]`，输出 "N total/M new + id8|file:line|body[:120]"（台账 S5）
- 落地: #60 ad19321（`--digest --against`，digest 输出保留全量 pull 序号、人读摘要零 ID 形态）；#65 写入 SKILL.md 对账步骤（digest 检测 + 全量刷新——post 的 join 基底须含全部已分类 id，digest-only 覆写会炸 round-1 entry）
- 触发条件: pull 命令后紧跟 python3 -c 摘要
- passCheck: 后续 trace 中 pull 后无手写摘要脚本
- 证据: 01a12f97#444,#470,#679,#819,#833,#931（≈900 out tok + 结果重读）
- 出现: 2026-10-15 diagnose#2 → absorbed 2026-10-15 spec #57 #60/#65

## P-008 LLM 手抄不透明长 ID 家族（截断/手写/模糊回填）
- 状态: absorbed-into-skill
- 现象: discussion_id 在展示层打印时截断（8 位前缀，同族 3 例）、组装 classified.json 时手写 `id:null` 占位、用 (file,line) 模糊匹配回填线程身份——裁决贴错线程或静默失配
- 根因: contract gap —— 让 agent 搬运不透明长 ID 的环节必然出错；逐条加规则（"必须全量复制"、"展示不得截断"）零抑制力
- 方案: ID 生命周期全部收回脚本内——verdict.py 按序号从 pull 文件字节级复制 discussion_id 并计算 anchor，agent 界面收敛为序号+裁决语义（#59）；post 对每条 entry 做 join+anchor 校验，失配在任何平台调用前 hard-fail（#61）；pull --digest 对账与 verify 人读输出零 ID 形态（#60/#64）；triage-mr SKILL.md 全删手动 fallback（#65）
- 触发条件: trace 中出现 ID 截断形态、手写 id 落盘或 (file,line) 回填
- passCheck: classified.json 无 agent 手写痕迹（verdict.py 唯一写者）；join 校验拦截截断 id
- 证据: spec #57 problem statement（截断家族第五例触发本 spec）；peer 诊断 01a13ea6 / 01a12f97（截断×3、id:null 手写、(file,line) 模糊回填）；MR !688 复现实验定谳"端点 500"实为 8 位前缀截断（Amendment R2）
- 出现: 2026-10-15 spec #57 立项事故 → absorbed 2026-10-15 spec #57 #59/#61/#65

## P-009 post 调用点文档漂移
- 状态: absorbed-into-skill
- 现象: templates.md 残留 bare-array 输入死模板（post 已 hard-fail 拒绝无 schema 文件）——照文档构造的输入必炸；同类：调用点文档的 heredoc 形态、Edge/Q resolve 旧语义在脚本演进后未同步
- 根因: contract gap —— post 的输入/调用契约散落多处调用点文档，脚本演进无同步义务
- 方案: 调用点文档收敛并点名——triage-mr SKILL.md（流程权威）、reference/gitlab.md、github.md（平台命令形态）、templates.md（输入 schema 与回帖正文）；改 post 契约的 ticket 必须四处同步（#65 全量核对为执行样例）
- 触发条件: 改 post 输入契约/回帖语义的 PR 未同步调用点文档
- passCheck: 调用点文档的 CLI flag 与 schema 与实现一致（本票后以 ocr review 复核）
- 证据: ocr review r1 F6（templates.md bare-array 死模板，155e956 修复）
- 出现: 2026-10-15 ocr r1 → absorbed 2026-10-15 spec #57 #65

## P-010 post 追尾：CI 门挡住每轮 post，裁决积压三轮
- 状态: absorbed-into-skill
- 现象: "裁决→修复→push"型 MR（每轮修复即 push）上，post 被推迟到 CI 终态之后——而每次 push 又触发新 pipeline + OCR bot 新一轮评审，post 永远排队。实证：ascend MR !6 六轮 146 findings，三轮裁决（47 条）只躺在本地 classified.json，post 仅在 r2 后跑过一次，47 线程零回复滞留远端，用户看出"一直没有 resolve"
- 根因: 流程语义错误——把 CI 门当成了所有 post 的前置（SKILL.md 原文 "pull and verify run a pipeline timing gate" 被 agent 泛化到 post），而 post 的 join/anchor 校验只针对 pull 快照，与 CI 无关；bot 每-push-追评的机制使"等 CI 再 post"在修复型 MR 上结构性不可满足
- 方案: SKILL.md 追尾规则——每轮 verdict 后立即 post 当轮条目（post 本就不设 CI 门；`--skip-pipeline-check` 是 pull/verify 的逃生门，与 post 无关），CI 门只挡 verify 与跨轮 pull；push 触发的新评审由下轮 pull 消费。修复后实测：post 一次清空 47 条积压（145/145 ok）
- 证据: session 01a15884 r3-r6（post 调用 13 次中多为 gate exit 2；146 resolvable / 47 open / verdict 145 落盘 99 上墙）
- 出现: 2026-10-21 diagnose（01a15884 peer 自报"跑步机"）

## P-011 /tmp 暂存 pull 快照：并发覆盖 → discussion_id 编造级联
- 状态: absorbed-into-skill
- 现象: triage 第一轮 pull 把 issues.json 重定向到 /tmp/issues.json，被另一并发 session 冲掉；后续步骤找不到状态文件后，agent 编造 discussion_id 继续走流程（而不是停下来修上游），二次失误触发 post join 校验 hard-fail
- 根因: 两层——①规则违反：SKILL.md 早已规定 stage 到 `.triage/<MR>/issues.json`（该精确路径是 verdict.py/post/verify 的 join 依据），/tmp 既是并发碰撞点又断了脚本寻址；②失败处置错误：脚本 hard-fail = 状态问题，正解是修上游（重 pull / 补 verdict），任何形式的"编造输入继续跑"都会把一个可恢复错误升级为污染
- 方案: 规则本体已在 triage SKILL.md Step 1（"never /tmp" + join 依据说明）；本条目存违反后果实例供 peer 复盘引用。post.md failure taxonomy 已写死处置铁律："fix upstream (verdict.py / re-pull)"，hand-written API 绕过 = 重造 P-002 事故家族
- 触发条件: agent 为图方便把 pull stdout 重定向到共享路径；或 hard-fail 后选择编造而非修上游
- passCheck: `.triage/<MR>/issues.json` 存在且 verdict/post/verify 都以它 join；post join 对编造 id 的 byte-match hard-fail 有效（已实证拦截）
- 证据: peer 复盘（并发 session 覆盖 /tmp 快照 → discussion_id 编造 → post 退出码拦截）
- 出现: 2026-10-21 peer triage 复盘
