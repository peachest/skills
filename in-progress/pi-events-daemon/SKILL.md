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

仓库：`~/projects/pi-mypackage-feat-pi-events-daemon`（分支 feat/pi-events-daemon）。正典：GitHub issue #31 + `packages/pi-events-daemon/docs/wiki/pi-events-daemon/known-unresolved.md`（遗留台账）。

## 安装

```bash
cd ~/projects/pi-mypackage-feat-pi-events-daemon
pi install ./packages/pi-events-daemon-extension   # session 客户端（9 op 工具）
# daemon 无需手动装——extension 首操作惰性拉起 bin/pi-events-daemon.ts
# 手动启动（可选）：npx tsx packages/pi-events-daemon/bin/pi-events-daemon.ts
```

数据布局：store `~/.pi/data/pi-events/store.db`；socket `~/.pi/run/pi-events.sock`（env `PI_EVENTS_SOCK` 优先）。

## 9 个 op（pi 会话内即模型可见工具）

| op | 用途 | 关键参数 |
|---|---|---|
| `subscribe` | 建站立兴趣 | `{url \| check, opts}`——两种形态见下 |
| `cancel` | 关订阅 | |
| `query` | 读实体状态/backlog/deadLetters/children | `{entityRef? \| scope? \| session?}` |
| `publish` | 发布实体状态（agent 是合法写入者） | `{entityRef \| type+key, to, contentIdentity?, payload?}` |
| `drain` | 重投 parked（session 掉线补投） | |
| `evidence` | 证据解引用 | |
| `status` | 登记处写入（任意实体状态登记，自动发事件） | `{type, key, state?, payload?}` |
| `validate` | check 语法/参数校验（不落订阅） | |
| `templates` | 列可用模板 | |

**entityRef 线格式 = `type:key` 全串**，如 `gitlab:mr:project/https://gitlab.example/group/pipe/-/merge_requests/42`。key 前缀三选一：`external/`（外部系统）、`project/`（项目级）、`user/`（用户级）——由 profile 的 key generator 生成，**agent 不铸造不解析**。

## 订阅两种形态

**模板形态**（推荐）：`subscribe({url: "...", template: "gitlab-pipeline", opts})`——URL 路由到 profile，key/schedule/check 全由模板生成。内置模板：`gitlab-pipeline`（mr/ci/ticket 三域）、`k8s-pod`、`fs-watermark`。`templates` op 列全部。

**ad-hoc 形态**：`subscribe({check: "shell 命令", opts: {schedule: {type:"interval", every:60000}}})`——任意 shell 命令，默认 60s interval；退出码 0=passed / 2=failed 断言 / 其他=waiting。

**opts 公共**：`{on（状态谓词）, once（首 passed 自动关）, flip（持续监视翻转沿）, readyCheck（两阶段）, ttl, failureThreshold/successThreshold（默认 1/1）}`。**opts 不含 shell/schedule（模板形态）**——schedule 归模板资产。

## 投递语义（边界要知道）

- 两段式 ack：`pending → accepted`（推送尽力而为）`→ verified`（你的 transcript 里出现 notificationId 才算）
- session 掉线：投递转 `parked`，重连 SESSION_START 自动 drain 补投
- **wake 不保证 exactly-once**（至多一次 + notificationId 去重兜底）；单机单实例（不做分布式）；checker env 白名单（PATH/HOME/no_proxy，不见 daemon 全环境）
- cron/interval 调度 MVP 全 UTC（tz 字段保留未消费）；`on-transition` 编排已实现（profile 声明转换后自动 subscribe/close）

## 已知遗留（用前过一眼）

`docs/wiki/pi-events-daemon/known-unresolved.md`：probe evidence 落盘链未接（evidence op 的 probe 路径解引用空）、url 多参数 keyGenerator 未接、query scope/session 过滤部分接入、高负载偶发时序 flake。

## 深入

正典 spec：GitHub #31（peachest/pi-packages）；12 份模块 spec 与已知遗留：仓库 `.scratch/pi-events-daemon/` + `docs/wiki/pi-events-daemon/`；非 pi 会话脚本消费：JSON-RPC 单行帧 over unix socket（`transport/client.ts` 的 `connectEvents`）。
