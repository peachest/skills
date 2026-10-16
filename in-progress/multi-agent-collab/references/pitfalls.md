# Pitfalls — 32 failure modes (observed in real sessions 2026-08 ~ 2026-10; #24/#26-#32 partly doc/mining-derived)

Every row was observed in a real session (2026-08 ~ 2026-09). Grouped by category; mechanics rows cross-reference the `herdr` skill (herdr branch) or orca-routing.md (orca branch). Consult when a send fails, a parse crashes, or a peer seems stuck.

## Quoting and envelopes

| # | Pitfall | Symptom (real output) | Fix |
|---|---------|----------------------|-----|
| 1 | ASCII double quote in prompt body | `unknown option: 整体容量够用，对吗？` — body tail parsed as flags | Shell variable / temp file / 「」 (SKILL.md quoting strategies) |
| 2 | `--wait false` | `unknown option: false` | `--wait` is valueless; drop the value |
| 3 | Heredoc nested in `$( )` | `unexpected EOF while looking for matching ')'` (environment-sensitive — same shape worked elsewhere) | Two-step: write file, then `"$(cat file)"` |
| 4 | `\'` inside double quotes | literal backslashes delivered in the message | Use CJK quotes or the variable strategy |
| 5 | Success/error envelopes conflated | `KeyError: 'result'` on error envelope → misread as send failure → duplicate send (real incident) | Branch on `d.get('error')` first |
| 6 | `agent get` nesting depth | `result.agent_status` → `None` silently (it's `result.agent.agent_status`) | Two levels: `result.agent.*` |
| 7 | `agent list` schema drift | `TypeError: string indices must be integers` in list comprehension | Inspect raw output before parsing; lenient parsing |
| 8 | `agent read` / `pane read` piped to `json.load` | `json.decoder.JSONDecodeError` — read output is terminal text, not JSON | Only `agent list/get/prompt` return JSON envelopes; pipe reads to `tail -N` or a file |
| 9 | `workspace create --name` | nonexistent flag → usage text → downstream `JSONDecodeError` | Use `--label` |
| 10 | Unbounded pipe output | multi-KB JSON dumps flooding context | Cap every herdr call: `2>&1 \| head -N` / `tail -N` |
| 25 | "Command aborted" counted as a tool error | user aborted the bash call mid-run; herdr never answered | Not a herdr failure — never cite it as evidence of send/wait breakage; re-run only if the task still needs it (mining: 7/138 `agent get` "errors" were these) |
| 26 | Envelope-parse crashes recur despite #5/#7/#8 | `KeyError: 'result'/'agents'`, `JSONDecodeError` mined across 5 op classes and 4 months (40+ crashes) — the docs were read ~never (1 read-load in 29 sessions) | Stop hand-rolling: `scripts/herdr-resolve.py` / `herdr-send.py` branch error-first internally. Raw-CLI parsing only for shapes the scripts don't cover. Re-audit anytime: `references/mining/mine-herdr-ops.py` (baseline: `mining-evidence-2026-09-20.md`) |
| 27 | Pane ids assumed global across runtimes; bare `herdr` aliases to the current runtime | with herdr default/dev/agent + orca live at once, `agent prompt w1:p2` may hit the wrong runtime's peer or `pane_not_found` — same address exists in several runtimes (real case: peer in agent runtime pane-read `w6:p1` while the target lived at `w1B:p1` in default). Worse: a bare `herdr agent list` follows `HERDR_SOCKET_PATH` and silently queries the CURRENT runtime — a wrapper that omits `--session` for the "default" runtime never queries it (this exact bug made herdr-resolve.py miss targets for a day) | Know your runtime (`$HERDR_SESSION` / `orca worktree current`); qualify cross-runtime targets (`herdr:<session>:<pane>`, `orca:<worktree-id>`); when scripting, pass `--session <name>` EXPLICITLY for every runtime including `default`; resolve globally (default): `herdr-resolve.py` scans all runtimes and tags matches |
| 28 | Improvised dispatch format drops the reply path | sender used `From:/To:/## Task/## Background` instead of the five-section shape — no pane address, no reply instruction; receiver burned 3 `agent list` calls (one crashing) to re-derive the caller before it could send the receipt (session 01a07ce2, 2026-09-21) | Bare = prefix-omitted ONLY; the five-section shape survives in every later message. Or let the tool enforce it: `herdr-send.py --from "name (pane)"` prepends `[caller identity]` and appends the reply command |
| 29 | Reply path lost after a peer migrated transports | orca peer sent inbound with a stale herdr pane (`wE:p1`) + vague "走 orca 可达" fallback; herdr receiver's reply → `agent_not_found`, blind resent once, groped `herdr --help` for an orca bridge (none exists), then wrote a handoff file instead of replying (session 01a0ae43, 2026-09-21) | `[caller identity]` names the sender's CURRENT transport address (`herdr:<session>:<pane>` / `orca:<worktree-id>`) + a concrete reply instruction; receiver fallback: `herdr-resolve.py` miss → `orca worktree list` → `terminal list` → `send --terminal` (orca-routing.md §Reply path); never resend before verifying the target still exists |
| 30 | Steer deliveries silently lost when the peer's turn aborts or its pane dies | two verified modes (2026-09-21/22, speculative worktree): ① turn-abort interleave — two messages queued during one long turn (8002s tool call), only one injected after abort, the other vanished with no error (lead's ACK never arrived; peer idled 2h+ waiting for a GATE decision); ② pane death — `herdr agent wait` reports `agent is no longer running in the target pane` while sends logged OK through jq pipes, re-sends inject only after pane recovery (session 01a0cce0) | Deliverables that peers BLOCK on (ACK/GATE decisions/rulings) go through herdr_send's idle-gate (followUp default), never raw steer; if you must steer, verify landing afterwards: `herdr-resolve.py` + grep the peer session for the message head. `agent is no longer running in the target pane` = the peer pi process is GONE — queued messages are lost; wait for pane recovery or respawn (herdr_peer), then resend |
| 32 | `herdr agent prompt --wait` 状态确认超时被误读为投递失败（herdr_send steer+wait_ms 路径同样中招） | steer 路径 text+Enter 瞬间完成，`--wait` 等 peer 状态翻转；working 中的 peer 不给状态回报 → 短 wait_ms（2-30s）必超时，错误说 "timed out waiting for agent status"。实测对账：17 发 19 落、未落地 0，但 lead 误判失败重发 6 次 → peer 收到 2-3 份副本 （base-charts session 01a12f97，2026-10-15 对账） | 短 wait_ms 的 timeout = 消息已入队、仅状态确认未达（pitfall #11 的 herdr_send 版）；对账唯一手段 = grep peer session；需要"确认送达"语义就给足 wait_ms（分钟级）或事后对账，不要重发。另：herdr CLI `agent prompt` 传长文本会被 arg parsing 吃掉（`unknown option: -`，不支持 `--` 分隔符）——正式回报一律走 herdr_send 工具（message 参数化，无此坑） |
| 33 | `/skill:<name>` 头部的 bootstrap 静默不展开 | bootstrap 第一行 `/skill:multi-agent-collab` 后直接换行（无空格），pi `_expandSkillCommand` 用全文第一个空格切分 skill 名 → 名字被解析成 `multi-agent-collab\n[caller...` 不匹配任何 skill → 原文透传，session 里零 `<skill>` 注入标记（pi 源码级确认 agent-session.js:1666-1672；hami-fix 01a12513 与 dflash-obs 01a13e66 两个 peer 均中招，靠 peer 手动 read SKILL.md 补救） | bootstrap 首行写成 `/skill:multi-agent-collab <摘要词>`（名字后必须有空格，args 任意）再换行写正文；或放弃首行前缀，改用 bootstrap 末尾让 peer 自己 `/skill:multi-agent-collab`。验证：grep peer session 首条 user 消息是否含 `<skill name=` 标记。**2026-10-16 补充**：TUI 命令路径（herdr pane 交互 pi）连 `\n\n` 分隔也不可靠——同格式两案例一败一成（FAIL 01a13d9d/01a13e8b 自举 vs OK 01a13ee2，首部字节完全一致）；headless `pi -p` 实测空格版注入、1/2 换行版均透传。空格分隔是唯一全路径可靠格式，勿依赖换行 |

## Lifecycle and waiting

| # | Pitfall | Symptom | Fix |
|---|---------|---------|-----|
| 11 | `--wait` timeout read as delivery failure | `{"error":{"code":"timeout","message":"timed out waiting for agent status"}}` + exit 1 | Timeout ≠ failure — message is queued. Recovery: `agent get` + `agent read` |
| 12 | `--timeout` unit confusion | `--timeout 30` (meant 30s) fails immediately; `--timeout` without `--wait` → syntax error | Milliseconds; 60000 = 60s; pair with `--wait` |
| 13 | `agent_blocked` misread | submission rejected, nothing delivered — target sits at an approval/question UI | Inspect the blocked UI, ask the user; do not resend blindly |
| 14 | Long-task foreground `--wait` | whole turn parked while a peer works minutes; peers idle in series | Background-first: bg_run the send with `--timeout 1800000` (SKILL.md waiting table) |
| 15 | Misleading `|| echo ok` fallback | printed `status= ok` on a real timeout | Delete fallbacks that mask failures |
| 24 | Mid-task dispatch lands in the peer's steering queue | message injected between tool calls → peer may weave task A and B together (pi `steer` semantics; herdr `agent prompt` = text + Enter, no followUp mode) | `herdr-send.py` defaults to followUp (idle/done gate + send, one step; the idle window can be a turn boundary — it's enough). Corrections/blockers: `--steer` — steer is the right semantics there. (pi docs rpc.md/extensions.md, not session-observed) |

## Addressing

| # | Pitfall | Symptom | Fix |
|---|---------|---------|-----|
| 16 | Pane ID churn | "Pane ID 变了" after restart / cross-workspace move; broadcast hits stale targets | Address by agent name; on failure re-enumerate `agent list` and filter by cwd/title |
| 17 | `agent start` false-ready | `interactive_ready: true` but pi sits at its session picker → later `agent_not_found`, pane missing from `agent list` | Restart from a clean shell pane |
| 18 | Name constraints | `[a-z][a-z0-9_-]{0,31}` — a Chinese course dir name forced a rename ("以符合 herdr agent 命名规则") | ASCII-only names from the start |
| 31 | herdr daemon restart migrates workspace ids and resets agent state | daemon switch moved the whole workspace-id prefix (`w1B:*` → `w1:*`) and reset agent state (`revision=1`, `state_change_seq` back to 0); sends to old pane addresses fail or silently miss; comparing a pre-restart seq against post-restart state misreads progress. Session UUIDs are UNCHANGED — they are the stable identity (memory-derived, 2026-09-23) | After a daemon restart: ① re-enumerate `herdr agent list` and rebuild the address map by matching session-UUID tails ② broadcast your new address to all active peers (their old copy of it is dead) ③ never diff an old `state_change_seq` against the new state |

## Environment

| # | Pitfall | Symptom | Fix |
|---|---------|---------|-----|
| 19 | Alternate-screen reads | `--lines` cannot recover rows that left the alternate screen | Fallback: peer writes full response to a file and replies with the path only |
| 20 | `pane run` is shell-mode | sending "n" executed the `nerdctl` alias into a TUI | TUI keys go through `agent send-keys` / `pane send-keys`, not `pane run` |
| 21 | intercom broker crash | `Failed to spawn intercom broker: spawn node ENOENT` | herdr CLI is the fallback channel (talks to the server socket) |
| 22 | `HERDR_ENV` gate blocks scheduled agents | bare `herdr` connects fine without env vars | The gate is for interactive sessions inside a pane (the herdr skill's rule); scripts and scheduled jobs that invoke the herdr binary directly should probe connectivity instead of hard-gating on `test $HERDR_ENV = 1` |
| 23 | forked subagents have no herdr | fork sessions carry zero herdr commands (no terminal) | fork = pi channel (results via stdout/files); herdr = terminal channel; never mix expectations |

## Deprecated API (historical)

`herdr mention` / `herdr reply` / `herdr cross` appear only in old memory phrasing; live usage converged on `agent prompt/get/read/list/start` before 2026-08-21. Treat any other verb as suspect.
| 34 | `herdr-send returned non-JSON: `（空 stderr）被当成"未知失败"盲重试；实为 pi.exec SIGKILL 丢缓冲 | herdr_send 作为工具调用时脚本内部 followUp 门默认 30min，而扩展 pi.exec 在 (90s tool gate + 3min buffer) 处杀 python——SIGKILL 丢掉全部缓冲 stdout（memory 教训复现）→ raw 空 → 扩展抛 non-JSON 空。对账 lead session 01a13e8b：3 次触发（10-15 11:39 / 10-16 06:47、07:04），全部未落地，lead 各自 steer 重发补救成功（零重复投递，重发方向正确但属于盲操作） | 根因修复（扩展）：用 env(1) 把 HERDR_FOLLOWUP_MS=90000 传给脚本（ExecOptions 无 env 字段），脚本在 90s 内返回结构化 exit-4 receipt，扩展"NOT sent"分支接住 → delivered=false + advice。工具调用再遇 non-JSON 空 = 真异常（查 herdr server），steer 重发仍是安全动作（未落地才会 non-JSON？否——steer 瞬时投递不走 30min 门，天然免疫） |
