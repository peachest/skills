# kanban — skill impact log

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-19 | 新建 skill（冷启动）：四板拓扑（agent/dev × wayfinder/execution）+ 列配方 + on-success/on-fail 自动链 + Ready 跨板门 + 派发契约 | — | 验证：实测同板 auto 链流转（Wayfinder→Grilling，run #15/#16 ok in 9s/41s）；跨板 on-success 实测被 CLI 拒绝 → Ready 门；bootstrap-boards.sh 幂等重跑通过（板 6/7/8/9 无重复列）；session 2026-10-19（本条目创建轮） |
| 2026-10-19 | 失败规范 F1-F10 沉淀。来源：run9（pi-events-daemon 板）历史失败 5 类 + 本轮实测 3 类（--board 静默失效、space_ref 过期、多 pane 歧义）+ 记忆条目（pipeline 模板 opus 陷阱） | — | 验证：F6 在本轮拓扑创建时实证（列全落到选中板），F7/F8 在 flow-test 卡 #14 实证；session 2026-10-19 |
| 2026-10-19 | （rejected/deferred）kanban.toml 项目覆盖机制：暂缓。理由：bootstrap 后直接 `column edit` 已覆盖"列集合与 prompt 调整"需求，配置文件解析器暂无第二消费者（2026-10-19 grilling Q6 裁定，用户确认默认模板 + CLI 微调路径） | — | — |
| 2026-10-19 | 迁移修正：runtime 按仓库归属（<platform> 业务仓→dev，个人工具仓→agent），xpu 卡 1/2/5 移到 dev-wayfinder board 8 + session=dev + space-ref=auto | — | 验证：双板 card list 核对通过；session 2026-10-19 |
| 2026-10-19 | 补 runtime 自探测：HERDR_SOCKET_PATH 的目录名即 runtime（sessions/<runtime>/herdr.sock），建卡前探测并与仓库归属规则交叉核对 | — | 验证：本 session socket=.../sessions/agent/herdr.sock → agent，与 agent list focused 条目一致；session 2026-10-19 |
| 2026-10-19 | 拓扑合并：wayfinder/execution 双板 → 每 runtime 单板 11 列（agent #6 / dev #8），Ready 门取消，Spec on-success 直连 Implement；board 7/9 归档（9 先 cancel awaiting 卡 14 + 迁移卡 14/15）。根因：TUI 拖动不跨板 + 跨板 on-success 不支持（F9），Ready 人工搬运成本高。新增 F11（column edit 无 --position，用 column reorder）、F12（有卡列删不掉/有 open run 板归档不了） | — | 验证：双板列清单核对（链/prompt 全就位），卡 14 comment 注记 cancel 副作用 |
| 2026-10-19 | xpu peer 实战迁移回灌：F6 升级为系统性表述（--board 对所有子命令含只读查询不可信，铁律=select+裸查+board_id 回验）；新增 F13 归档板吞卡（bootstrap 重建新板 id、归档板不进 list --all 但卡可寻址、救援=restore→move→re-archive）；F12 补实证（迁移注记使卡 14 run 正确只巡检不重建 MR） | — | 验证：卡 1/2/5 从归档板 8 救援至 board 11 Backlog（restore→move→re-archive 全链实测）；session 2026-10-19 |
| 2026-10-19 | daemon-owner 实战回灌（pi-events-daemon 五卡流水线）：新增 F14 并行派发 SpaceKey 互斥（boardd dispatch 键={session,space_kind,space_ref} 不含 cwd，源码 pass.rs:28-58+model.rs:85-99；并行配方=每卡独立 wt worktree+唯一 space_ref，3 路并行实锤）；F10 补根因（Review 列 model_override=opus → Bedrock 不可达路由 → idle_expired 假 failed，clear-model 修复）；新增 F15 人工推进 failed 残留（status=最后 run outcome 投影，move 不可改写；正典在 repo/issue 时删卡是唯一干净出口） | — | 验证：F14 实测 active_runs>1；来源 herdr:agent:w3:p1；session 2026-10-19 |
| 2026-10-19 | daemon-owner 回灌：新增「监控双轨」小节（pi-events-daemon 相位沿订阅 + bg_run 60s 轮询共享日志，双轨对照发现误报/漏报，不一致立 ticket），F5 补交叉引用 | — | 验证：五卡流水线实战；来源 herdr:agent:w3:p1；session 2026-10-19 |
| 2026-10-19 | 用户指出 retro 依赖 session 上下文：Retro 列 fresh→reuse-session（两板实测生效），prompt 改为"复用最近 run session + comment 链补齐更早阶段"，bootstrap 脚本同步；其余列保持 fresh（多卡并行不串台） | — | session 2026-10-19 |
