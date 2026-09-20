# Pitfalls — 27 failure modes (25 observed in real sessions, #24/#26/#27 partly doc/mining-derived)

Every row was observed in a real session (2026-08 ~ 2026-09). Grouped by category; CLI-mechanics rows cross-reference the `herdr` skill. Consult when a send fails, a parse crashes, or a peer seems stuck.

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
