---
name: to-peer
description: "Create a peer agent session in a NEW herdr tab (never split pane). One command: tab create → agent start → optional bootstrap prompt. Use when the user asks to 创建 peer session / 开新 tab 派活 / to-peer / spawn a peer in a new tab. Message protocol (five-part dispatch, replies, closure) lives in multi-agent-collab — this skill owns creation only."
argument-hint: "<name> <cwd> [--workspace W] [--prompt-file F|-] [--machine M] [--runtime R] [--label L] [--focus] [--caller-ws] [--description D]"
---

# to-peer — 在新 tab 创建 peer session

本 skill 只负责**创建**：一个新 tab + 一个 pi agent + 可选的首条 prompt。peer 起来之后的通信协议（五段消息、followUp 门、回执对账）由 **multi-agent-collab** skill 负责，创建完成后走那边。

**新建与复用的分工（用户拍板）**：to-peer = 每次都新建一个全新 peer session，不做复用判断。要把任务派给一个已存在的 session（复用），走 multi-agent-collab 并显式提供 session id 或名称。向已有 peer 投递新任务前，确认它没有自己的在办职责——`idle` 只表示 agent 空闲，不表示它没有已承接的任务线（case：wJ:p1 idle 但在忙自己的镜像检查任务，被误投后用户纠正）。

**父子回传义务（用户拍板）**：to-peer 派生的 session 本质上存在父子关系（派发方 = 父）。子 session 的 bootstrap prompt 必须含回传条款：**完成工作、与用户达成决策（尤其是推翻原任务方向的决策）、或任务暂停时，主动按五段格式通知父 session（地址取自 [caller identity]），不等用户提醒**。case：hami-fix peer 与用户讨论后关闭 MR !24，只向用户汇报即静默，用户主动提醒后才通知父 session。没写 prompt-file 时，后续用 multi-agent-collab 派任务时同规则附带此条款。

**worktree 归属：谁负责这个工作，worktree 就跟谁（用户拍板 2026-10-22，源自 peer 01a1627d 案例）**：派 peer 修的目标分支不是父 session 当前检出所在的分支时，父 session **不要带迁移地 switch**——用 `wt switch -c <branch> -b <base> --no-cd` 建好 worktree（`--no-cd`：分支/检出/pre-start 装依赖照常，唯独 pi session 不迁移），`wt list` 验证 `@ <路径>` 存在后，把该路径写进 dispatch 文本/`[repo-cwd]`，父 session 留在自己的任务线。带迁移的 switch（无 --no-cd）仅当**父 session 自己要在这个 worktree 里继续工作**时才用——case：01a1627d 在 llm-3.0 worktree 里接到“修 dev 分支 CVE”任务，先无 --no-cd switch 到新建的 dev worktree（父 session 的 llm-3.0 语境被顶掉），再从那里建 peer；正确形态是 --no-cd 建树 → 派发，两步不变换父 session 位置。另：`-b origin/<分支>` 允许基于远端分支建 worktree，无需本地已有同名分支。

**建树后、派发前（2026-10-22 拍板，源自 fix-chain/events 两案）**：① 分支 base 必须是任务票的基线分支（如 feature 分支），默认 main 会漏掉票依赖的已有实现（实证：fix worktree 从 main 建导致 40+ 票实现缺失）；② 预置依赖再派发——node_modules 等装好或从主 checkout 软链，基线测试跑绿（假红会让 peer 把环境问题当代码 bug 排查）；③ 环境预案写进 prompt（registry fallback、corepack 等已知 footgun，<pkgfix>-cve 靠预埋预案省一轮试错）。

## 为什么是新 tab 而不是 split pane

用户拍板：peer session 一律开新 tab（`herdr tab create`），每个 peer 独占一整个 tab，不用 `pane split`。`herdr_peer` 工具已对齐此契约（2026-10-26）：内部改为调本 skill 脚本、默认在**当前 herdr workspace** 开新 tab，split 形态已移除。multi-agent-collab 的 `scripts/herdr-peer.sh`（pane split）降级为 legacy fallback，仅在该 skill 自身被引用且无新 tab 要求时才考虑。

## 失败即回 skill（红线，2026-10-26 拍板，源自 10-26 绕过案）

任何创建报错（agent 重名、identity_conflict、ws 断言失败等）时，**唯一合法动作是带着脚本的结构化错误回到本 skill 的路径重试或向用户升级**——禁止绕过 skill 手打裸 `herdr tab create` / `agent start`。实证：2026-10-26 一案，skill 护栏齐全（ws 推断+WARN+回读），但 herdr_peer 重名报错后 agent 图省事裸打 CLI 不带 --workspace，tab 落进非目标项目 ws（最近活跃 ws），把修复过的 lesson 犯了第二遍。知识护栏在重试压力下会失效——重名的正确处置是：脚本已自动报出已有持有者，**复用 vs 新名字由用户裁决**，不要自行选路。

## 身份登记（2026-10-26）

创建脚本融合了 SPEC（`~/.agents/agents/SPEC.md`）身份登记：peer 创建成功且活性验证通过后，自动在**身份 workspace**（`.agents/agents/` 所在目录树，与 herdr workspace 是正交概念）登记：写 AGENT.json + charter.md 存根 + sessions.log 追加当值行（`endedAt: null`，sessionId 取自 agent list 回执，非手写）。落点解析：cwd 是 git worktree 时优先主 checkout（wt 是一次性生态，身份是常驻资产，SPEC §2 特例）。三态语义：

- `identity: registered`（exit 0）— 已登记
- `identity: needs-workspace-init`（**exit 4**）— peer 已建好干活，但解析不到身份 workspace。**向用户提问是否初始化 `.agents/agents/`**（SPEC §2：新建 workspace 必须用户确认），不静默跳过、不代建
- `identity: skipped-remote-machine` — 跨机 peer，远端文件系统不在掌控内，v1 不登记

同名身份已存在 → **exit 3 conflict**，创建前中止（不留下半成品）；复用已有 peer、换名、还是显式接班，由用户裁决——与 agent 重名同构。

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
- **ws 自动推断（2026-10-19 加固）**：省略 `--workspace` 时，脚本用 cwd 尾段匹配 ws label（`/…/skills` → `skills` ws）自动推断；匹配唯一则用之（stderr 提示推断结果），无匹配则 WARN 列出候选并落到 daemon 默认 ws。背景：daemon 的裸 `tab create` 默认落在最近活跃 ws，不是 cwd 对应的项目 ws（实证：三个 skills peer 落进了 pi-mypackage ws，cwd 是对的、ws 是错的）——**cwd 正确 ≠ ws 正确，两者独立校验**。label 同名歧义（如两个 <project-a> ws）不猜，报错列出候选。跨 runtime 派发时推断在目标 runtime 的 ws 列表上执行。**agent 看到 WARN 或推断失败时，先向用户确认目标 ws 再继续，不静默落默认 ws（2026-10-22 补，源自 ascend 案例：WARN 后未确认，peer 落错 ws 未纠正）**
- `--prompt-file F`：可选。`F` 为文件路径，或 `-` 从 stdin 读（`echo ... | ... --prompt-file -`，免 /tmp 中转）。prompt 内容若是 bootstrap，按 multi-agent-collab 五段模板写，并带 `/skill:multi-agent-collab` 前缀（仅首条）——**skill 名后必须紧跟空格**（首行 `/skill:multi-agent-collab <peer角色词>`，再换行写正文；换行/双换行分隔在 TUI 与 headless 路径均不可靠，pitfall #33），且必须含父子回传义务条款（见上）
- **父地址必须写字面值（2026-10-22 拍板，源自 <pkgfix>-cve 案例）**：bootstrap [caller identity] 与回传条款里的父 pane 地址必须是显式字面值（`herdr:<session>:<pane>`，用 `herdr_resolve` 或 `herdr agent list` 实测后拼入），禁止写「地址见 caller identity」这类依赖运行时注入的表述——`--prompt-file` 投递**不注入** caller identity，peer 只能靠项目名+时间猜父 pane（实证：<pkgfix>-cve 猜中属侥幸；spectraining 首派回报地址写错）
- `--label L`：可选，tab 标签（默认用 name）
- `--focus`：可选，创建后聚焦新 tab（默认不抢焦点）
- `--caller-ws`：可选。把 tab pin 到**调用者 pane 所在的 herdr workspace**（从 `$HERDR_PANE_ID` 解析），而不是按 cwd 尾段推断目标项目 ws。herdr_peer 工具默认传此旗标（对齐"当前 ws 建 peer"语义）；skill 手动调用时通常**不要**传——派活 peer 应落目标项目 ws
- `--description D`：可选，一句话 peer 职责，写入 AGENT.json
- `--runtime R`：可选。跨 herdr runtime 创建（`herdr --session R ...`），如从 default runtime 会话往 dev runtime 的目标项目 ws 派 peer；不带则打当前 runtime
- `--machine M`：可选（herdr ≥ 0.9.5）。在**已保存的 SSH 机器**上创建 peer（`herdr --machine M ...`，与 `--runtime` 互斥——machine 条目自带 session）。cwd 按**远端机器的路径**解释；本机 HERDR_ENV 门对此放宽（SSH 转发不依赖本机 pane）。输出 JSON 带 `machine` 字段；canonical 地址相应为 `herdr:<machine>:<session>:<pane>`。实测案例（2026-10-15）：`--machine wsl --cwd /home/peachest` 在 WSL 侧建出真实 pi peer。**已知坑（2026-10-18）**：跨机路径的 `--prompt-file` 注入只填充对端 pi 输入框、**不自动提交**（本机路径正常）——回执 `prompt: sent` + `status: idle` 不代表 peer 已开跑，需用户手动 Enter 或后续再推一条消息触发；疑似对端 herdr 版本问题（machine API 无法探测对端版本），待升级验证

成功输出一行 JSON：`{"name","tab_id","pane_id","workspace_id","cwd","status","prompt","identity","session_id"}`。`workspace_id` 是创建后的实际值；跨 ws 派发时把回执和后续 `herdr:` 地址都用这个 ws 前缀拼。prompt 未带文件时为 `none`——之后用 multi-agent-collab 的发送通道（herdr_send 工具或其 `herdr-send.py`，followUp 门）派活。

**退出码**：`0` 成功（含 registered/skipped-remote-machine）· `1` 用法/校验 · `2` herdr 错误或验证失败（ws 断言不符时脚本已自动关 tab，不残留）· `3` 冲突（agent 重名 / 同名身份已存在；stdout JSON 报已有持有者，用户裁决）· `4` peer 已创建但缺身份 workspace（问用户是否初始化）。

**融合验证**：创建后脚本内建有界活性轮询（`agent list` 确认 agent 存活 + 抓取 pi session UUID），无需 agent 自行组装"建完再查"管道。验证失败自动关 tab 并 exit 2。

## 完成判据

输出 JSON 中的 `pane_id` 存在、`status` 为 idle/working（融合验证已确认）、`herdr agent list`（本机）或 `herdr --machine M agent list`（跨机）能看到该 pane 即创建完成。exit 4 时 peer 已创建但需向用户提问身份 workspace 初始化（见上）。跨机 peer 的后续通信用 `herdr --machine M ...`（pitfall #27：pane id 是 machine-local 的）。`agent start` 默认等 30s readiness；超时返回 `agent_not_ready` 时 name 仍保留，等 peer idle 后再发首条消息（见 multi-agent-collab）。
