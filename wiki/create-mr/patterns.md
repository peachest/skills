# patterns — create-mr

来源：2026-09-09 diagnose#1（3 trace / 6 次执行）。格式与状态机见 `../README.md`。

## P-001 预检信息收集每次即兴拼装
- 状态: open
- 现象: create 前需要 remote/平台/分支状态/已有 MR/target 候选/标题六类信息，每次以不同形状手工收集，无统一入口
- 根因: contract gap —— skill 无 preflight 步骤或脚本
- 方案: S1 preflight.sh，结构化一行一节输出六类信息
- 证据: 01a06bcd#131,133,718; 01a07f1f#149; 01a07fc6#229
- 出现: 2026-09-09 diagnose#1

## P-002 已有 MR 查询的 remote 形式变体
- 状态: open
- 现象: skill 给的是 `glab mr list -R <url>`，实际出现三种变体——双 GitLab 实例环境需 `GITLAB_HOST=<host>` 前缀；ssh:// 形式 remote 的 `-R` 需原样带 `.git` 后缀；另有直接改走 `glab api "projects/<path>/merge_requests?source_branch=…"` 绕过 mr list
- 根因: contract gap —— remote 形式矩阵（https/http/ssh）未入契约
- 方案: S3 文档补丁（两条怪癖入 SKILL.md step 2/5，对齐 glab-api skill 怪癖表风格）；长期统一走 glab api
- 证据: 01a06bcd#718; 01a07f1f#149; 01a07fc6#233
- 出现: 2026-09-09 diagnose#1

## P-003 assignee 用户名获取无统一命令
- 状态: open
- 现象: skill 说 `glab auth status` 可看 username，实际各次凭记忆或不同的过滤方式获取，无一次用统一命令
- 根因: contract gap —— 未给规范命令
- 方案: 并入 S1 preflight.sh 输出
- 证据: 01a06bcd#139,250,644,720; 01a07f1f#149; 01a07fc6#229
- 出现: 2026-09-09 diagnose#1

## P-004 MR description 整段经 tool-call 参数重发
- 状态: open
- 现象: 数 KB 描述内联在 bash 参数里（每次 out 529–833 tokens）；后改 heredoc 写临时文件再 `cat`——同一问题两种即兴解法并存
- 根因: contract gap —— 无 description 文件化约定
- 方案: S2 create-draft-mr.sh 收编（`--desc-file` 参数）
- 证据: 01a06bcd#139,250,644,720; 01a07f1f#159; 01a07fc6#241
- 出现: 2026-09-09 diagnose#1

## P-005 create 命令模板手工复刻
- 状态: open
- 现象: 6 次手工拼 `git push -u … && glab mr create -R … --source/--target/--title/--description/--assignee/--draft/--yes`；`-R` 的 URL 形式（https/http/ssh）每次现场推导
- 根因: contract gap —— 只给了文字模板，未提供脚本
- 方案: S2 create-draft-mr.sh 收编（内部做 remote URL 归一化）
- 证据: 01a06bcd#139,250,644,720; 01a07f1f#159; 01a07fc6#241
- 出现: 2026-09-09 diagnose#1

## P-006 python run() 包装器逐字重写
- 状态: open
- 现象: create 前后 git/glab 编排的 `def run(subprocess, shell=True)` 包装器在同一 session 内近逐字重写 7 次
- 根因: repeated pattern —— 无对应契约缺口，随 S1/S2 脚本落地自然消灭
- 方案: 由 S1/S2 顺带吸收（无独立方案）
- 证据: 01a06bcd#604,606,616,618,640,646,718
- 出现: 2026-09-09 diagnose#1

## P-007 glab api JSON 解析 inline python
- 状态: open
- 现象: `glab api … | python3 -c "for j in json.load(sys.stdin): print(...)"` 形状一致地多次出现
- 根因: repeated pattern —— 环境已有 jq 但契约未文档化规范命令
- 方案: 文档化一条 jq 规范命令（S4 独立脚本方案已裁定 rejected，见 skill-impact.md）
- 证据: 01a06bcd#178,180,186; 01a07f1f#161
- 出现: 2026-09-09 diagnose#1
