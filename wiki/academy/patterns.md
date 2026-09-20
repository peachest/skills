# academy patterns

## P-001 academy 收口后越界做课程层技术裁决
- 状态: open
- 现象: N/N 回执收口、声称 step back 之后，academy session 继续对课程主题做源码级深挖复核，并以"批准行动"口吻向课程 session 下发教程修法与 lesson 设计指导——编排层做了课程层的技术裁决
- 根因: contract gap——SKILL.md 写了 "It never teaches"，但没有定义课程内容勘误/技术分歧的处理路径，agent 即兴发明了"academy 复核→分工回写"流转
- 方案: skill-doc——在 Roles 或 Incubate 收口步补一条硬边界：收口后 academy 只做编排（CURRICULUM/路由/进度），课程内容问题一律转交对应 course session 或只读 subagent 复核，academy 转述结论而非亲自产出技术内容；为勘误定义一条 documented 路径
- passCheck: 取 trace 中最后一次 N/N 回执回执之后的全部 assistant 消息，不含对课程主题源码/教程内容的技术分析输出（可 grep 课程技术关键词验证；编排类 CURRICULUM 编辑不算）
- 证据: 01a0bce0#262,#274（越界复核+下发修法），#287（勘误经即兴路径回写成功）
- 出现: 2026-09-20 diagnose#1

## P-002 herdr agent prompt --wait 空等（回执实际走注入通道）
- 状态: open
- 现象: bootstrap/通报用 `herdr agent prompt --wait` 等回执，stdout 只回 `status: done/None`，真实回执经 herdr 以 user 消息异步注入；一次 wait 等满 180s 超时（status None）后回执 8 分钟才经注入到达——等待零收益
- 根因: contract gap——SKILL.md 把 "bootstrap prompt (sent with --wait)" 写成流程步骤 + 环境问题——herdr CLI 的 --wait stdout 不携带回执内容
- 方案: skill-doc——改写 Course session protocol 与 Incubate 步 6/7：prompt 发送不带 --wait（或仅作发送确认），回执一律按注入消息计数；明确"发完即返回，收口以注入回执 N/N 为准"
- passCheck: trace 中所有 `herdr agent prompt` 调用不带 --wait 参数（或带时等待 <10s 且明确仅作发送确认），收口判断引用注入回执而非 wait stdout
- 证据: 01a0bce0#237,#240,#274,#289（wait 调用），#239,#259,#277,#291（回执均走注入）；量化：5 次 wait 合计约 9min 墙钟，其中一次整 180s 纯阻塞
- 出现: 2026-09-20 diagnose#1

## P-003 课程派生三步循环逐次手写 JSON 解析
- 状态: open
- 现象: tab create → agent start → agent prompt 的同形管道在一次孵化中重复 8 次，每次都内联 `python3 -c "import json,sys;…"` 手排 pane_id/status
- 根因: contract gap——SKILL.md 的 Course session protocol 只有 prose，无脚本；skill 目录无 scripts/
- 方案: skill-script——`scripts/spawn-course.sh <academy-root> <course>`：tab create → agent start → bootstrap 模板（自动填 cwd/共享层路径）→ 发送，输出 tab/pane/status 一行摘要；附 --prompt 变体覆盖非 bootstrap 通报；写死前先固化 herdr list/start/prompt 的 JSON 样例作夹具
- passCheck: skill 安装目录存在 spawn-course 脚本且带 JSON 夹具；后续孵化 trace 中同形内联 json 解析不再出现
- 证据: 01a0bce0#227,#231,#233,#235,#237,#240,#274,#278
- 出现: 2026-09-20 diagnose#1

## P-004 迁移后链接修复与验证全手工
- 状态: open
- 现象: 课程迁移后连续 4 次 sed -i 改 okb/资源相对路径 + grep 逐条验证 + 手建 symlink，Migrate 步 7 "verify every link resolves" 无工具支撑
- 根因: contract gap——Migrate 步骤 3/4/7 均为 prose
- 方案: skill-script——`scripts/verify-course-links.sh <course-dir>`：RESOURCES 指针规范化检查、assets symlink 解析、lesson href 全量校验输出通过/失败清单；可与既有 nav-chain-check 合并
- passCheck: skill 安装目录存在链接校验脚本；迁移类 trace 中不再出现连续 sed -i 改路径 + 手工 grep 验证的组合
- 证据: 01a0bce0#195,#197,#199,#201,#209
- 出现: 2026-09-20 diagnose#1

## P-005 课程脚手架 write×N 手工搭建
- 状态: open
- 现象: Create-a-course 的 6 目录 + assets symlink + MISSION/RESOURCES + CURRICULUM 注册全手工；本 trace 仅 2 课未到痛感阈值，6 课孵化场景即 write×12
- 根因: contract gap——Create a course 章节纯 prose
- 方案: skill-script——`scripts/scaffold-course.sh <academy> <name> --namespace <ns> --mission-file <f>`：建目录树、assets symlink、RESOURCES 指向共享 okb、追加 CURRICULUM 行；3+ 课孵化才回本，可与 P-003 脚本合并交付
- passCheck: skill 安装目录存在脚手架脚本；后续孵化 trace 中建目录+symlink+CURRICULUM 注册不再逐条手工执行
- 证据: 01a0bce0#190,#193,#203,#207,#209,#211,#215
- 出现: 2026-09-20 diagnose#1
