---
name: to-peer
description: "Create a peer agent session in a NEW herdr tab (never split pane). One command: tab create → agent start → optional bootstrap prompt. Use when the user asks to 创建 peer session / 开新 tab 派活 / to-peer / spawn a peer in a new tab. Message protocol (five-part dispatch, replies, closure) lives in multi-agent-collab — this skill owns creation only."
argument-hint: "<name> <cwd> [--prompt-file F] [--label L] [--focus]"
---

# to-peer — 在新 tab 创建 peer session

本 skill 只负责**创建**：一个新 tab + 一个 pi agent + 可选的首条 prompt。peer 起来之后的通信协议（五段消息、followUp 门、回执对账）由 **multi-agent-collab** skill 负责，创建完成后走那边。

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
- `--workspace W`：可选。目标 workspace 的 id（`w4`）或 label（`<project-ws>`；精确匹配优先，其次片段匹配，歧义报错列出候选）。**跨项目派发必带**：peer 必须落在目标项目的 ws 里，落错 ws 用户的 topology 就乱了。创建后脚本回读实际 ws id（daemon 迁移会改写前缀，如 `w1B:` → `w1:`），以回读值为准
- `--prompt-file F`：可选。`F` 为文件路径，或 `-` 从 stdin 读（`echo ... | ... --prompt-file -`，免 /tmp 中转）。prompt 内容若是 bootstrap，按 multi-agent-collab 五段模板写，并带 `/skill:multi-agent-collab` 前缀（仅首条）
- `--label L`：可选，tab 标签（默认用 name）
- `--focus`：可选，创建后聚焦新 tab（默认不抢焦点）
- `--runtime R`：可选。跨 herdr runtime 创建（`herdr --session R ...`），如从 default runtime 会话往 dev runtime 的目标项目 ws 派 peer；不带则打当前 runtime

成功输出一行 JSON：`{"name","tab_id","pane_id","workspace_id","cwd","status","prompt"}`。`workspace_id` 是创建后的实际值；跨 ws 派发时把回执和后续 `herdr:` 地址都用这个 ws 前缀拼。prompt 未带文件时为 `none`——之后用 multi-agent-collab 的发送通道（herdr_send 工具或其 `herdr-send.py`，followUp 门）派活。

## 完成判据

输出 JSON 中的 `pane_id` 存在、`herdr agent list` 能看到该 name 即创建完成。`agent start` 默认等 30s readiness；超时返回 `agent_not_ready` 时 name 仍保留，等 peer idle 后再发首条消息（见 multi-agent-collab）。
