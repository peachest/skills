# patterns — create-mr

来源：2026-09-09 diagnose#1（3 trace / 6 次执行）；2026-09-10 diagnose#2（6 trace / 20 次执行，含 skill 诞生 session dogfood）。格式与状态机见 `../README.md`。

## P-001 预检信息收集每次即兴拼装
- 状态: open
- 现象: create 前需要 remote/平台/分支状态/已有 MR/target 候选/标题六类信息，每次以不同形状手工收集，无统一入口
- 根因: contract gap —— skill 无 preflight 步骤或脚本
- 方案: S1 preflight.sh，结构化一行一节输出六类信息
- 证据: 01a06bcd#131,133,718; 01a07f1f#149; 01a07fc6#229; 01a0574c#121; 01a0614d#128,130; 01a06683#155,157; 01a06682#199,201; 01a06130#284,432; 01a08014#1769
- 出现: 2026-09-09 diagnose#1 → 2026-09-10 diagnose#2（6/6 session 复发）
- 备注: T7 外来 commit 混入提示预检还需分支一致性节（local HEAD vs upstream vs rebase range），并入 S1 规格

## P-002 已有 MR 查询的 remote 形式变体
- 状态: open
- 现象: skill 给的是 `glab mr list -R <url>`，实际出现三种变体——双 GitLab 实例环境需 `GITLAB_HOST=<host>` 前缀；ssh:// 形式 remote 的 `-R` 需原样带 `.git` 后缀；另有直接改走 `glab api "projects/<path>/merge_requests?source_branch=…"` 绕过 mr list
- 根因: contract gap —— remote 形式矩阵（https/http/ssh）未入契约
- 方案: S3 文档补丁（两条怪癖入 SKILL.md step 2/5，对齐 glab-api skill 怪癖表风格）；长期统一走 glab api
- 证据: 01a06bcd#718; 01a07f1f#149; 01a07fc6#233; 01a0614d#130,326; 01a06683#157,163; 01a06130#438,440,636,700,768,794,839; 01a08014#1769
- 出现: 2026-09-09 diagnose#1 → 2026-09-10 diagnose#2（加剧：双实例 -R/--repo/--hostname 混用致失败重试；ssh remote sed 推导 404 → 去 -R 裸跑逃生；existing-MR 检查 URL 拼错 404 被解读为"无 MR"）

## P-003 assignee 用户名获取无统一命令
- 状态: open
- 现象: skill 说 `glab auth status` 可看 username，实际各次凭记忆或不同的过滤方式获取，无一次用统一命令
- 根因: contract gap —— 未给规范命令
- 方案: 并入 S1 preflight.sh 输出
- 证据: 01a06bcd#139,250,644,720; 01a07f1f#149; 01a07fc6#229; 01a0614d#132,326; 01a06683#163; 01a06130（10 次全部）; 01a08014#1771
- 出现: 2026-09-09 diagnose#1 → 2026-09-10 diagnose#2（9/9 复发，仅 01a06683#155 一次用 auth status）

## P-004 MR description 整段经 tool-call 参数重发
- 状态: open
- 现象: 数 KB 描述内联在 bash 参数里（每次 out 482–999 tokens）；后改 heredoc 写临时文件再 `cat`——同一问题三种即兴解法并存（内联参数 / heredoc 内联 / 写临时文件+$(cat)）
- 根因: contract gap —— 无 description 文件化约定
- 方案: S2 create-draft-mr.sh 收编（`--desc-file` 参数）；失败重试时全文重发的实证（503/415/503 类瞬时失败）使该方案从省 token 升级为防重发
- 证据: 01a06bcd#139,250,644,720; 01a07f1f#159; 01a07fc6#241; 01a0614d#132,326; 01a06683#163; 01a06682#207,209; 01a06130#292,438,440,636,700,768,794,839; 01a0574c#125; 01a08014#1771
- 出现: 2026-09-09 diagnose#1 → 2026-09-10 diagnose#2（16/20 次 create 内联，16/20 → 3 种解法并存）

## P-005 create 命令模板手工复刻
- 状态: open
- 现象: 6+10+4 次（两轮共 20 次）手工拼 `git push -u … && glab mr create -R … --source/--target/--title/--description/--assignee/--draft/--yes`；`-R` 的 URL 形式（https/http/ssh）每次现场推导。新后果：手工复刻 10 连发中 title 手写 `Draft:` 前缀且丢 `--draft` 旗标——文字模板在长链路中被稀释，核心规则漂移
- 根因: contract gap —— 只给了文字模板，未提供脚本
- 方案: S2 create-draft-mr.sh 收编（内部做 remote URL 归一化 + title 清洗：拒绝 Draft:/WIP: 前缀并自动转 --draft + 瞬时失败重试）——脚本不仅是省 token，更是核心规则的执行器
- 证据: 01a06bcd#139,250,644,720; 01a07f1f#159; 01a07fc6#241; 01a0574c#127; 01a0614d#132,326; 01a06683#163; 01a06682#207,209; 01a06130#292,438,440,634,636,696,700,768,794,839; 01a08014#1771
- 出现: 2026-09-09 diagnose#1 → 2026-09-10 diagnose#2（20/20 复发，新增 draft 规则漂移后果）

## P-006 python run() 包装器逐字重写
- 状态: open
- 现象: create 前后 git/glab 编排的 `def run(subprocess, shell=True)` 包装器在同一 session 内近逐字重写 7 次
- 根因: repeated pattern —— 无对应契约缺口，随 S1/S2 脚本落地自然消灭
- 方案: 由 S1/S2 顺带吸收（无独立方案）
- 证据: 01a06bcd#604,606,616,618,640,646,718
- 出现: 2026-09-09 diagnose#1 → 2026-09-10 diagnose#2 absent-this-run（T4–T9 六 trace 零出现；可能是采样差异，不结论为消灭）

## P-007 glab api JSON 解析 inline python
- 状态: open
- 现象: `glab api … | python3 -c "for j in json.load(sys.stdin): print(...)"` 形状一致地多次出现
- 根因: repeated pattern —— 环境已有 jq 但契约未文档化规范命令
- 方案: 文档化一条 jq 规范命令（S4 独立脚本方案已裁定 rejected，见 skill-impact.md）
- 证据: 01a06bcd#178,180,186; 01a07f1f#161; 01a0614d#332; 01a06130#797
- 出现: 2026-09-09 diagnose#1 → 2026-09-10 diagnose#2（2 次复发：bg_run pipeline 轮询、python urllib API 调用[属 glab-api 域]）
