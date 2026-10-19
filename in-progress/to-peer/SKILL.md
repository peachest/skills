---
name: to-peer
description: "Create a peer agent session in a NEW herdr tab (never split pane). One command: tab create → agent start → optional bootstrap prompt. Use when the user asks to 创建 peer session / 开新 tab 派活 / to-peer / spawn a peer in a new tab. Message protocol (five-part dispatch, replies, closure) lives in multi-agent-collab — this skill owns creation only."
argument-hint: "<name> <cwd> [--workspace W] [--prompt-file F|-] [--machine M] [--runtime R] [--label L] [--focus]"
---

# to-peer — 在新 tab 创建 peer session

本 skill 只负责**创建**：一个新 tab + 一个 pi agent + 可选的首条 prompt。peer 起来之后的通信协议（五段消息、followUp 门、回执对账）由 **multi-agent-collab** skill 负责，创建完成后走那边。

**新建与复用的分工（用户拍板）**：to-peer = 每次都新建一个全新 peer session，不做复用判断。要把任务派给一个已存在的 session（复用），走 multi-agent-collab 并显式提供 session id 或名称。向已有 peer 投递新任务前，确认它没有自己的在办职责——`idle` 只表示 agent 空闲，不表示它没有已承接的任务线（case：wJ:p1 idle 但在忙自己的镜像检查任务，被误投后用户纠正）。

**父子回传义务（用户拍板）**：to-peer 派生的 session 本质上存在父子关系（派发方 = 父）。子 session 的 bootstrap prompt 必须含回传条款：**完成工作、与用户达成决策（尤其是推翻原任务方向的决策）、或任务暂停时，主动按五段格式通知父 session（地址取自 [caller identity]），不等用户提醒**。case：hami-fix peer 与用户讨论后关闭 MR !24，只向用户汇报即静默，用户主动提醒后才通知父 session。没写 prompt-file 时，后续用 multi-agent-collab 派任务时同规则附带此条款。

## 为什么是新 tab 而不是 split pane

用户拍板：peer session 一律开新 tab（`herdr tab create`），每个 peer 独占一整个 tab，不用 `pane split`。split pane 的旧路径（multi-agent-collab 的 `scripts/herdr-peer.sh`）仅在该 skill 自身被引用且无新 tab 要求时才考虑；用户明确提到 to-peer 或新 tab 时，走本 skill。

## 前置检查

herdr skill 规则：控制命令只能在 herdr 环境内执行。

```bash
test "${HERDR_ENV:-}" = 1
```

失败则说明不在 herdr 环境中，停止并告知用户。首次使用或换节点后可先跑 `bash <SKILL_DIR>/scripts/check-env.sh`。

## 创建 peer（一步）

```bash
bash <SKILL_DIR>/scripts/herdr-tab-peer.sh <name> [repo-cwd] [--workspace W] [--prompt-file F|-] [--label L] [--focus]
```

- `<name>`：peer 的 agent 名，`[a-z][a-z0-9_-]{0,31}`，必须全局唯一
- `[repo-cwd]`：peer 的工作目录，缺省用当前目录（`$PWD`）；跨项目派发时必须显式给目标仓路径
- `--workspace W`：可选。目标 workspace 的 id（`w4`）或 label（`<project-ws>`；精确匹配优先，其次片段匹配，歧义报错列出候选）。创建后脚本回读实际 ws id（daemon 迁移会改写前缀，如 `w1B:` → `w1:`），以回读值为准
- **ws 自动推断（2026-10-19 加固）**：省略 `--workspace` 时，脚本用 cwd 尾段匹配 ws label（`/…/skills` → `skills` ws）自动推断；匹配唯一则用之（stderr 提示推断结果），无匹配则 WARN 列出候选并落到 daemon 默认 ws。背景：daemon 的裸 `tab create` 默认落在最近活跃 ws，不是 cwd 对应的项目 ws（实证：三个 skills peer 落进了 pi-mypackage ws，cwd 是对的、ws 是错的）——**cwd 正确 ≠ ws 正确，两者独立校验**。label 同名歧义（如两个 speculative-training ws）不猜，报错列出候选。跨 runtime 派发时推断在目标 runtime 的 ws 列表上执行
- `--prompt-file F`：可选。`F` 为文件路径，或 `-` 从 stdin 读（`echo ... | ... --prompt-file -`，免 /tmp 中转）。prompt 内容若是 bootstrap，按 multi-agent-collab 五段模板写，并带 `/skill:multi-agent-collab` 前缀（仅首条）——**skill 名后必须紧跟空格**（首行 `/skill:multi-agent-collab <peer角色词>`，再换行写正文；换行/双换行分隔在 TUI 与 headless 路径均不可靠，pitfall #33），且必须含父子回传义务条款（见上）
- `--label L`：可选，tab 标签（默认用 name）
- `--focus`：可选，创建后聚焦新 tab（默认不抢焦点）
- `--runtime R`：可选。跨 herdr runtime 创建（`herdr --session R ...`），如从 default runtime 会话往 dev runtime 的目标项目 ws 派 peer；不带则打当前 runtime
- `--machine M`：可选（herdr ≥ 0.9.5）。在**已保存的 SSH 机器**上创建 peer（`herdr --machine M ...`，与 `--runtime` 互斥——machine 条目自带 session）。cwd 按**远端机器的路径**解释；本机 HERDR_ENV 门对此放宽（SSH 转发不依赖本机 pane）。输出 JSON 带 `machine` 字段；canonical 地址相应为 `herdr:<machine>:<session>:<pane>`。实测案例（2026-10-15）：`--machine wsl --cwd /home/peachest` 在 WSL 侧建出真实 pi peer。**已知坑（2026-10-18）**：跨机路径的 `--prompt-file` 注入只填充对端 pi 输入框、**不自动提交**（本机路径正常）——回执 `prompt: sent` + `status: idle` 不代表 peer 已开跑，需用户手动 Enter 或后续再推一条消息触发；疑似对端 herdr 版本问题（machine API 无法探测对端版本），待升级验证

成功输出一行 JSON：`{"name","tab_id","pane_id","workspace_id","cwd","status","prompt"}`。`workspace_id` 是创建后的实际值；跨 ws 派发时把回执和后续 `herdr:` 地址都用这个 ws 前缀拼。prompt 未带文件时为 `none`——之后用 multi-agent-collab 的发送通道（herdr_send 工具或其 `herdr-send.py`，followUp 门）派活。

## 完成判据

输出 JSON 中的 `pane_id` 存在、`herdr agent list`（本机）或 `herdr --machine M agent list`（跨机）能看到该 name 即创建完成。跨机 peer 的后续通信用 `herdr --machine M ...`（pitfall #27：pane id 是 machine-local 的）。`agent start` 默认等 30s readiness；超时返回 `agent_not_ready` 时 name 仍保留，等 peer idle 后再发首条消息（见 multi-agent-collab）。
