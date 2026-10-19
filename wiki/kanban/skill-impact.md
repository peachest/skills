# kanban — skill impact log

## Proposals & changes

- 2026-10-19 | 新建 skill（冷启动） | 四板拓扑（agent/dev × wayfinder/execution）+ 列配方 + on-success/on-fail 自动链 + Ready 跨板门 + 派发契约 | 验证：实测同板 auto 链流转（Wayfinder→Grilling，run #15/#16 ok in 9s/41s）；跨板 on-success 实测被 CLI 拒绝 → Ready 门；bootstrap-boards.sh 幂等重跑通过（板 6/7/8/9 无重复列） | session 2026-10-19（本条目创建轮）
- 2026-10-19 | 失败规范 F1-F10 沉淀 | 来源：run9（pi-events-daemon 板）历史失败 5 类 + 本轮实测 3 类（--board 静默失效、space_ref 过期、多 pane 歧义）+ 记忆条目（pipeline 模板 opus 陷阱） | 验证：F6 在本轮拓扑创建时实证（列全落到选中板），F7/F8 在 flow-test 卡 #14 实证 | session 2026-10-19

## Rejected / deferred

- kanban.toml 项目覆盖机制：暂缓。理由：bootstrap 后直接 `column edit` 已覆盖"列集合与 prompt 调整"需求，配置文件解析器暂无第二消费者（2026-10-19 grilling Q6 裁定，用户确认默认模板 + CLI 微调路径）。
- 2026-10-19 | 迁移修正：runtime 按仓库归属（<platform> 业务仓→dev，个人工具仓→agent），xpu 卡 1/2/5 移到 dev-wayfinder board 8 + session=dev + space-ref=auto | 验证：双板 card list 核对通过 | session 2026-10-19
- 2026-10-19 | 补 runtime 自探测：HERDR_SOCKET_PATH 的目录名即 runtime（sessions/<runtime>/herdr.sock），建卡前探测并与仓库归属规则交叉核对 | 验证：本 session socket=.../sessions/agent/herdr.sock → agent，与 agent list focused 条目一致 | session 2026-10-19
