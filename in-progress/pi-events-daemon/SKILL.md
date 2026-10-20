---
name: pi-events-daemon
description: 使用 pi-events-daemon 事件守护进程——订阅外部实体状态（GitLab MR/CI、k8s pod、文件水位、任意 check）、发布状态、接收 wake 通知，替代手写轮询脚本。当任务需要等待外部条件（MR 合并、CI 通过、服务就绪、文件阈值）、跨 session 传递状态、或用户提到事件订阅/daemon/实体状态时使用。
---

# pi-events-daemon — 实体状态机事件底座

实体（GitLab MR、k8s pod、文件、任意 check）带封闭状态集，状态转换产生事件；你订阅实体，状态翻转时 daemon 通过长连接 wake 你——**不再手写轮询脚本**。

## 架构（三条事实）

1. **全局唯一 daemon / 机器**：`pidfile+flock` 单实例，store（SQLite+FTS5）是唯一真相源。所有 herdr session 共享它——session 是客户端，不是 daemon 宿主。
2. **session 侧只装 extension**：`pi install ./packages/pi-events-daemon-extension` 后，9 个 op 工具自动注册进 pi 会话；daemon 由 extension **首操作惰性拉起**（spawn `bin/pi-events-daemon.ts`），无需手动启动。
3. **crash 自愈**：daemon kill -9 后重启即自愈（全槽重探/catch_up_one/幂等收口），store 是唯一真相源。

仓库：`~/projects/pi-mypackage`（主检出，main）。正典：GitHub issue #31 + `docs/wiki/pi-events-daemon/known-unresolved.md`（遗留台账）。

## 安装

```bash
cd ~/projects/pi-mypackage
pi install ./packages/pi-events-daemon-extension   # session 客户端（9 op 工具）
# daemon 无需手动装——extension 首操作惰性拉起 bin/pi-events-daemon.ts
# install 后新工具在**下一个 session** 生效（无热注册）；settings.json 包路径指向的目录必须存在
# 手动启动（可选）：setsid nohup node --experimental-transform-types packages/pi-events-daemon/bin/pi-events-daemon.ts（裸 nohup & 会随 shell 退出被杀）
```

数据布局：store `~/.pi/data/pi-events/store.db`；socket `~/.pi/run/pi-events.sock`（env `PI_EVENTS_SOCK` 优先）。

## 9 个 op（pi 会话内即模型可见工具）

| op | 用途 | 关键参数 |
|---|---|---|
| `subscribe` | 建站立兴趣 | `{entityRef \| url \| check 恰好其一, opts}`——三形态见下；所有开关在 opts 内勿拍平 |
| `cancel` | 关订阅 | |
| `query` | 读实体状态/backlog/deadLetters/children | `{entityRef? \| scope? \| session?}` |
| `publish` | 发布实体状态（agent 是合法写入者） | `{entityRef \| type+key, to, contentIdentity?, payload?}` |
| `drain` | 重投 parked（session 掉线补投） | |
| `evidence` | 证据解引用 | |
| `status` | 登记处写入（任意实体状态登记，自动发事件） | `{type, key, state?, payload?}` |
| `validate` | check 语法/参数校验（不落订阅） | |
| `templates` | 列可用模板 | |

**entityRef 线格式 = `type:key` 全串**，如 `gitlab:mr:project/https://gitlab.example/group/pipe/-/merge_requests/42`。key 前缀三选一：`external/`（外部系统）、`project/`（项目级）、`user/`（用户级）——由 profile 的 key generator 生成，**agent 不铸造不解析**。

## 订阅三形态

**模板形态**（推荐）：`subscribe({url: "...", opts: {template: "<名字>"}})`——URL 按 urlPattern 命名捕获组路由，key/schedule/check 全由模板生成（host/项目 id 从 URL 自动提取）。内置模板：`gitlab-pipeline`（mr/ci/ticket 三域）、`k8s-pod`、`fs-watermark`。`templates` op 列全部。

**ad-hoc 形态**：`subscribe({check: "shell 命令", opts: {schedule: {type:"interval", every:60000}}})`——任意 shell 命令，默认 60s interval；退出码 0=passed / 2=failed 断言 / 其他=waiting。**缺省跑 smoke 预检**（syntax+live-run 失败不建订阅并返回报告；确信要建传 `opts.smoke: false`——checker 环境注意 glab 需 `--hostname <内部 GitLab host>`——缺省回落 gitlab.com 必 401）。

**opts 公共**：`{on（状态谓词）, once（首 passed 自动关）, flip（持续监视翻转沿）, readyCheck（两阶段）, ttl, failureThreshold/successThreshold（默认 1/1）, sessionId}`。**sessionId 缺省 = 当前连接声明**（transport 自动注入，一般无需传；短连接脚本直连要显式传目标 session）。**opts 不含 shell/schedule（模板形态）**——schedule 归模板资产。

## 投递语义（边界要知道）

- 两段式 ack：`pending → accepted`（推送尽力而为）`→ verified`（你的 transcript 里出现 notificationId 才算）
- session 掉线：投递转 `parked`，重连 SESSION_START 自动 drain 补投
- **wake 不保证 exactly-once**（至多一次 + notificationId 去重兜底）；单机单实例（不做分布式）；checker env 白名单（PATH/HOME/no_proxy，不见 daemon 全环境）
- cron/interval 调度 MVP 全 UTC（tz 字段保留未消费）；`on-transition` 编排已实现（profile 声明转换后自动 subscribe/close）

## 监控长流水线：订阅 + bg_run 双轨对照（实践）

监控 board 流水线/长任务时，**挂订阅的同时启动一个 bg_run 轮询对照**（2026-10-19 五卡流水线实战确立）：

- **订阅轨**：相位沿 ad-hoc once 订阅（如 `board card show <CID> --json` 判 column_id），到达即 wake——零轮询心智
- **对照轨**：`bg_run` 一个轮询脚本（60s 记录状态到 /tmp 日志），负责：①发现订阅误报/漏报（沿时间戳对不上）②daemon 故障时的兜底可见性 ③给其他 agent session 提供共享证据（日志文件可被任意 session 读）
- 双轨发现的设计问题 → 立需求 ticket（对照实验本身也是吃狗粮测试）
- **实测记分（2026-10-19，5 卡 board 流水线全程监控）**：订阅轨 wake 6 次全及时、误报 0；轮询轨因脚本自身 bug 漏报 1 次（重写后全录）。订阅覆盖面=挂载时选定的关键沿（E2E/MR），轮询天然覆盖全部中间沿（Code Review 等未挂订阅的流转）。**结论：双轨互补非竞争**——订阅负责"按需唤醒人"，轮询负责"全量留痕供追溯"；只挂单轨时要么打断过多（全轮询）、要么盲区无痕（全订阅）。

## 脚本直连（非 pi 会话）

JSON-RPC 单行帧 over unix socket（`transport/client.ts` 的 `connectEvents`）。**帧必须带 epoch**（读 `~/.pi/run/pi-events.sock.epoch` 旁车）——不匹配会回 `-32001 epoch mismatch: daemon=X frame=Y` 错误（照提示重连取新 epoch 即可，不会静默挂死）。

## 已知遗留（用前过一眼）

`docs/wiki/pi-events-daemon/known-unresolved.md`：probe evidence 落盘链已接（票 47）、ad-hoc 清理域已接（票 48）、url keyGenerator 已接（票 49）——台账现余 1 项：高负载偶发真进程时序 flake（观测项）。

## 深入

正典 spec：GitHub #31（peachest/pi-packages）；12 份模块 spec 与已知遗留：仓库 `.scratch/pi-events-daemon/` + `docs/wiki/pi-events-daemon/`；非 pi 会话脚本消费：JSON-RPC 单行帧 over unix socket（`transport/client.ts` 的 `connectEvents`）。
