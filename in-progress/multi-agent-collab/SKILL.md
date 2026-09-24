---
name: multi-agent-collab
description: "Collaboration protocol for peer pi sessions over herdr or orca — environment probe, leader appointment, dispatch contracts, background-first waiting, delivery verification, closure receipts. Use when the user mentions 多个 session 协作/编排, 开 tab 共同完成, peer sessions, herdr/orca session 间通信, or a task spanning multiple projects or branches that would benefit from parallel sessions. CLI mechanics live in the herdr skill (herdr env) or the orca-cli/orchestration skills (orca env)."
allowed-tools: [Bash, Read, Env]
---

# Multi-Agent Collaboration

The protocol layer for multi-session collaboration: who talks to whom, in what shape, and how to wait without deadlocking. It runs over herdr or orca — probe the environment first, route the transport by result. Everything below was distilled from 32 real sessions; failure modes carry evidence in [pitfalls.md](references/pitfalls.md).

Task-state vocabulary, round correlation, and dispatch idempotency follow the A2A v1.0 protocol's semantics — see [a2a-alignment.md](references/a2a-alignment.md) before inventing a receipt field or retry rule.

## Environment & routing

Probe once at session start, before any send:

```bash
if [ -n "${HERDR_PANE_ID:-}" ]; then ENV=herdr
elif [ -n "${ORCA_CLI_COMMAND:-}" ] || orca-ide status --json >/dev/null 2>&1 \
  || orca status --json >/dev/null 2>&1; then ENV=orca
else ENV=none; fi
```

- **herdr** — inline commands below are herdr-shaped; CLI syntax lives in the `herdr` skill.
- **orca** — load [orca-routing.md](references/orca-routing.md) once and follow it for the session; deep mechanics live in the installed `orca-cli`/`orchestration` skills (`orca skills get <topic> --full`).
- **none** — no multiplexer detected: fall back to pi subagents; the protocol sections below still govern how you brief and verify them.

### Cross-runtime addressing (multi-herdr + orca)

Multiple runtimes may be live at once (herdr named sessions + orca). Two rules:

- **Know your own runtime**: herdr → `$HERDR_SESSION` (empty = `default`); orca → `orca worktree current --json`.
- **Qualify peers across runtimes** — canonical address `herdr:<session>:<pane>` (e.g. `herdr:dev:w3:p1`) / `orca:<worktree-id>`; unqualified = current runtime. Pane ids are runtime-local: `w1:p2` in `dev` and in `default` are different sessions (pitfall #27).

Cross-runtime ops need no special channel — every herdr CLI accepts `--session <name>` from any shell (`herdr --session dev agent prompt w3:p1 ...`), and orca's CLI reaches its runtime from anywhere too. Enumeration: `herdr session list` (name/status/socket). The bundled tools are runtime-aware: `herdr-resolve.py` scans **all running runtimes by default** (matches carry a `runtime` field for global addressing; `--runtime NAME` narrows), `herdr-send.py --runtime NAME`. Caller identity in the five-part prompt signs with (name, runtime, pane). Cross-runtime receipts are identical; waiting/steer semantics are unchanged (they belong to the transport, not the runtime).

The protocol itself — topology, five-part prompt, dispatch contract, receipts, shared state — is transport-agnostic and applies unchanged in both environments. Sections below carry a `→ orca:` pointer at each herdr-bound spot; follow it once, on first need.

### Choosing the transport for new peers (dual-primary)

Detection tells you where you are; this rule tells you where new peers should live — both transports are first-class, pick per repo:

- **orca** — the repo has multi-worktree development (parallel tasks/branches on one repo): per-peer worktrees, checkpoints, and orchestration receipts are the payoff.
- **herdr** — the repo has no multi-worktree needs, or the flow is lightweight (single-task peers, quick dispatches): orca's runtime overhead buys nothing there.
- Already inside an environment with peers running? Keep the session's transport for the running collaboration; the rule only decides where NEW peers are bootstrapped.

## Topology

Peer-ify when the task spans multiple projects, needs multiple branches/worktrees of one repo, or the user asks for parallel sessions. Below that, a single session with subagents is cheaper.

Three roles:

- **Leader** — orchestrates: inventory, read each peer's existing work before dispatching, dispatch, verify, close. **Appointed by the user, never self-elected.** At 3+ collaborating sessions a leader must exist, named by the user. Leaders defer timing decisions to the user ("notify peers now, or after the deploy finishes?").
- **Peer** — specialist worker (researcher, fixer, writer). Verifies incoming claims against sources before acting, pushes back with file:line evidence, and never answers a user-facing question aimed at another session's user — route it back instead. When a peer's work is being systematically undone by another session (directional conflict, not an accidental touch), it stops, asks the other session's goal over herdr, and treats the answer as conflicting directives rather than hostility — resolve jointly or escalate to the user; a peer that keeps pushing harder converts a routing problem into a turf war.
- **Explorer** — solo session using the multiplexer (whichever environment resolved) for inspection only. No protocol applies.

Bootstrap a named peer (names survive pane churn; pane IDs do not — see pitfalls #16). One step: `scripts/herdr-peer.sh <name> <repo-cwd> [right|down]` (wraps split + start + pane_id parse). Manual form → orca: peers live in worktrees, not panes — [orca-routing.md §Bootstrap a peer](references/orca-routing.md#bootstrap-a-peer):

```bash
# right for a wide caller pane, down for a tall one (see the herdr skill's geometry rule)
herdr pane split --current --direction right --cwd <peer-repo> --no-focus
# parse .result.pane.pane_id, then:
herdr agent start <name> --kind pi --pane <pane-id>
```

Names must match `[a-z][a-z0-9_-]{0,31}`. Inventory with `herdr agent list` (pane agents — carries each peer's session-JSONL path) and `herdr session list` (server instances; a different, coarser level). Resolve self via `$HERDR_PANE_ID`; when the user hands you a session UUID, resolve it by substring-matching `agent_session.value` in `agent list` output. A finished peer's work is reachable without herdr at all: `session_read <uuid>` plus its artifact files — live conversation while it runs, post-hoc reuse after it ends.

Done when: the role split is stated (who leads, who peers) and every peer has a stable address.

## The message: five-part prompt

Every inter-session prompt has this shape — the receiver depends on it to learn the reply path:

```
/skill:multi-agent-collab   ← bootstrap only (first contact); later messages start at [caller identity]
[caller identity] I am <name> (pane wX:pY, cwd ~/repo; reach me at pane wX:pY)
[context] background, verified facts, data — mark what you verified yourself
[tasks] numbered, each independently checkable; include what NOT to redo
[output + reply] results to <file>; reply via herdr with the path and a summary
```

- The `/skill:multi-agent-collab` prefix is a **bootstrap signal, sent once per peer context**: the injection teaches the receiver this whole protocol — reply shape, closure signals, waiting behavior — and it reaches the herdr skill for CLI mechanics when it needs to send. (Before this skill existed the prefix was `/skill:herdr`, which only taught the CLI.) Every later message in the thread — reply, receipt, clarification, closure — goes **bare, no prefix**: both sides already hold the protocol, and a repeated injection burns the receiver's context for nothing. Re-prefix only when the peer's protocol context may be gone (rebooted agent, fresh re-bootstrap).
- The explicit reply request at the end is mandatory — a prompt without it goes unanswered (persistent lesson).
- **Bare means prefix-omitted only, not shape-omitted**: later messages in a thread skip the `/skill:` prefix but keep the five-section shape. An improvised `From:/To:` variant silently drops the pane-addressed reply path and forces the receiver to re-derive your identity via `agent list` (real case, pitfall #28). Easiest compliance: `scripts/herdr-send.py --from "name (pane)"` prepends `[caller identity]` and appends the reply command for you.
- Embed a copy-paste reply command in dispatches. Receivers follow it verbatim, so write it complete — identity signature in, protocol prefix out (the receiver was just injected by your dispatch; a prefixed reply would re-inject you, who already holds the skill):
  `herdr agent prompt <my-pane> "<receiver-name> (pane wX:pY) → <result summary + artifact path>"`
- Address peers by name; sign requests with (name, pane) both.
- Cross-workspace dispatch works.

### Quoting — three safe strategies, in order

Default path: `scripts/herdr-send.py <pane> <msg-file>` handles quoting AND envelope parsing AND the delivery receipt in one step — prefer it over hand-rolled sends (40+ parse crashes mined from real sessions motivated it). → orca: structured orchestration messages need none of this; it applies only to `terminal send --text` one-liners ([orca-routing.md](references/orca-routing.md)).

1. Temp file (the two-step form — most robust, friendliest for versioned resends): write first, send second:
   ```bash
   cat > /tmp/task.md <<'EOF'
   ...body with any quotes...
   EOF
   herdr agent prompt <target> "$(cat /tmp/task.md)"
   ```
2. Shell variable (works when a heredoc inside `$( )` parses cleanly in your shell — that nesting is environment-sensitive and may EOF-error):
   `MSG=$(cat <<'EOF' ... EOF)` then `herdr agent prompt <target> "$MSG"`
3. CJK brackets 「」 inside the body wherever it would otherwise need ASCII double quotes

An ASCII `"` inside the body closes the argument early and the tail parses as flags (`unknown option: <body text>`). A heredoc nested inside `$( )` is environment-sensitive (EOF errors) — use the two-step form. `--wait` is a valueless flag: `--wait false` is an error.

Done when: the message is sent and quoting survived (no `unknown option` in the result).

### Steer semantics: what a send to a busy peer means

`agent prompt` types text + Enter into the peer's TUI. In pi, Enter during a running turn queues the message into the peer's **steering queue** — injected after the current tool batch, before the next LLM call. herdr has no followUp mode (queue-until-idle), so a dispatch to a busy peer always lands inside its active task context and the peer may weave both tasks together. **The steering queue is lossy under two verified conditions (pitfall #30)**: the peer's turn aborts mid-queue (partial silent loss), or the peer's pane/agent dies (`agent is no longer running in the target pane` — the whole queue goes with it). Gate-level messages therefore never ride raw steer. → orca: same TUI semantics via `terminal send`; tracked work should use orchestration messages instead — [orca-routing.md §Tracked multi-agent work](references/orca-routing.md#tracked-multi-agent-work-use-orchestration-not-terminal-send). Two mitigations:

Default is followUp (`scripts/herdr-send.py <pane> <file>`): polls until idle/done (bounded, default 30min via `HERDR_FOLLOWUP_MS`), then delivers as a clean new task; designed to run under `bg_run` so the turn stays free. Timeout → exit 4, nothing sent. The idle window can be narrow (a turn boundary is enough) — followup catches it. Pass `--steer` ONLY for corrections/blockers/answers you WANT seen mid-task — never for messages a peer will BLOCK on (ACK/GATE decisions/rulings): steer into a long turn can be silently lost (pitfall #30). → orca: orchestration messages queue natively (replay-until-ack), no gate needed.
- **Corrections, blockers, answers to its questions** → send directly. Steer is exactly right there — you *want* it seen mid-task.

## Waiting: background-first

→ orca: the table below is herdr's; orca's inbox replay-until-ack makes dispatch → end turn → `check --wait` native ([orca-routing.md §Waiting](references/orca-routing.md#waiting-background-first)).

The rule: **keep this session concurrent — never park the current turn on a peer's long work.** A foreground `--wait` blocks the whole turn; a leader serially waiting three peers triples the idle time; a peer waiting for its next instruction while its leader waits for a reply deadlocks both.

Choose by expected duration:

| Duration | Strategy |
|---|---|
| >1 min (any real task) | `bg_run` the send: `herdr agent prompt <t> "..." --wait --timeout 1800000`, end the turn, resume on `<background-task-notification>` |
| broadcast, no reply needed | fire-and-forget (no flags); pull later via `agent get` + `agent read` |
| ack / receipt, ≤60s | foreground `--wait --timeout 60000` |
| scripted context, no bg_run | bounded bash poll loop on the settled trio (idle/done/blocked) |
| "after you finish" (default) | `bg_run` + `scripts/herdr-send.py <t> <file>` — polls idle/done then sends; no reply-blocking |
| steer mid-task (corrections/blockers) | `scripts/herdr-send.py <t> <file> --steer` — skip the idle gate |
| a specific state needed | `herdr agent wait <t> --until blocked --timeout ...` |

`--timeout` is **milliseconds** and requires `--wait`. There is no completion-subscription mechanism (`herdr notification` only shows) — background tasks and polling are the only waiting primitives. Keep the bash tool's timeout above the herdr wait, both in milliseconds (e.g. herdr `--timeout 600000` needs a bash tool timeout of 700000).

Replies arrive on their own as injected user messages — **push, not pull**. A `--wait` return value is a settled-state convenience, and a background send's notification only tells you the *send* settled; the peer's reply lands later as its own message. So do other work and let the reply interrupt; polling for a reply wastes the concurrency the background-first rule bought you.

A failed or expired background-task notification means the send did not settle — it says nothing about the peer's work. Verify deliverables directly (`agent read`, artifact files) before resending; a blind resend duplicates the task.

A stuck peer escalates in three steps: nudge once with a short prompt; if silent, re-dispatch the task to another peer or take it over yourself; re-bootstrap (fresh named agent) only as a last resort — it costs all accumulated context.

### Delivery evidence — three levels, cheapest first

→ orca: `worker_done` + `check --ack` is level 1 by construction — [orca-routing.md §Delivery evidence](references/orca-routing.md#delivery-evidence--three-levels-cheapest-first). herdr level 1 is free via `scripts/herdr-send.py` (its receipt carries `agent_status`/`revision`/`state_change_seq`); hand-rolled sends must reproduce the error-first branch (pitfall #5).

1. `agent get` → `revision` / `state_change_seq` bumped: machine-checkable receipt.
2. `herdr agent read <t> --source recent-unwrapped | grep -a Steering` — the steering marker proves the message reached the peer's screen.
3. Peer screen content showing it acting on your instructions — the strongest proof; status fields alone are not.

**A `timeout` error is not a delivery failure** — the message is already in the peer's steering queue. Recovery is always `agent get` + `agent read`, never a blind resend. Before resending anything, grep the peer's scrollback to check whether the earlier message arrived, and label the resend ("the previous one may not have arrived — resending"). Exception: if the peer's turn aborted or its pane died meanwhile, the queued message IS gone (pitfall #30) — resend unconditionally after recovery, then verify by grep.

Parse every response envelope before trusting it. Success: `{"result":{"agent":{...},"type":"agent_prompted"}}` with status at `result.agent.agent_status` (two levels of nesting). Error envelopes have no `result` key — branch on `error` first, or a parse crash reads as failure and triggers a duplicate send (a real incident).

Done when: delivery evidence is confirmed at level 1 or 2 — or the reply itself has arrived.

## The dispatch contract

A task dispatch to a fresh peer carries nine elements (omit only with a stated reason):

1. Bootstrap prefix (first contact with this peer only — later messages bare) + caller identity + "your result is invisible unless you report back"
2. Pre-digested context: "Background (already investigated, trust this)" + verified code excerpts — saves the peer re-investigating
3. Anti-redundancy: what is already done — "do not re-diagnose"; "your first step is to compare, not design from scratch"
4. Anti-hallucination: "verify everything against the repo; do not trust this prompt blindly"
5. Precise numbered workflow: branch names, verification commands with expected values, commit conventions, MR template
6. Environment footguns inline: broken tool paths, dangerous flags ("the nix-profile helm is broken; use /usr/bin/helm")
7. Required report schema: branch / commit hash / MR URL / before-after counts — plus the blocked-case protocol: "if blocked, report what you completed and where you stopped"
8. Agreed artifact paths: "reply with the file path only"
9. Language directive: reports in English (for agents), conclusions in Chinese (for the user)

Sequenced tasks get an explicit gate: "task 1 first; report and confirm before task 2." Expect the peer to verify your ground truth and push back with file:line evidence — that is the protocol working, not a failure. Expect mid-task clarification questions too: answer them promptly with verified facts — an unanswered question parks the peer for the duration.

### Handoff currency and receipts

Commit hashes and MR URLs are the currency: peers hold commits for leader approval, the leader specs the commit message, and hashes echo back in acks. After consuming peer output, send an **integration receipt** — which decision adopted it, which ticket or file it landed in, where the full report is archived. Before writing the receipt, check for a **dissenting peer**: one whose conclusion contradicts the rest. A dissent is evidence to weigh, not a vote to outcount — ask the dissenter for its evidence chain and evaluate it on file:line merit; group consensus that silently drops a peer's unique finding is the classic multi-agent failure (groups score far below their best member when unique information never gets pressed against the prior). With exactly two peers there is no majority to lean on — a disagreement stays unresolved until evidence or a third check breaks the tie. Close every thread with a **closure signal**: 任务闭环 / no reply needed / stand down, with a recall clause when the peer may be needed again ("I'll re-contact if review has feedback"). A thread without a closure signal leaves a hanging peer.

When leadership transfers: quiz the successor on its inherited context first ("confirm you can see the map and the frontier"), then send the explicit handoff ("you are now the active X session; I am no longer active"), then `herdr workspace focus <new>` so the user lands on the new leader. → orca: no focus equivalent — dispatch a coordinator-role message to the Run inbox ([orca-routing.md §Handoff](references/orca-routing.md#handoff-and-closure)).

Done when: every dispatched thread has either a receipt or a closure signal on record.

## Shared state

For coordination that outlives individual messages, prefer files over message-passing:

- Maps and tickets: `map.md` + `issues/*.md` with `Status: open|claimed|resolved` and `Blocked by:` — both sides edit; a small renderer derives the frontier and drives dispatch order.
- Shared worktree: probe activity before touching the tree (`find . -newermt '3 hours ago'`), label stashes with ownership ("WIP: dev-sync changes (unrelated to the fix)"), split into separate worktrees once collisions start, and commit peers' uncommitted work before any history rewrite.
- Track pending replies as explicit todo items in each session so they are not forgotten.

## Deterministic tools

`scripts/` (this skill) wraps the recurring fragile flows — prefer them over inline CLI + python parsing:

| Script | Replaces | Kills |
|---|---|---|
| `herdr-resolve.py <uuid\|pane\|cwd\|title>` | `agent list` + substring match + envelope parse (136 calls mined, only 3 bare) | KeyError 'result'/'agents' class; session-UUID → address friction |
| `herdr-send.py <pane> <file> [--wait ms]` | `agent prompt` + temp-file quoting + receipt parse | quoting tail-as-flags; envelope conflation; delivery-evidence boilerplate |
| `herdr-peer.sh <name> <cwd>` | `pane split` + `agent start` two-step | pane_id parse boilerplate |

`scripts/check-env.sh` verifies the herdr-side assumptions only (python3, herdr binary, current-runtime envelope, scripts executable) — the orca branch has no scripts to check. Raw CLI remains valid for anything the scripts don't cover. The mining that sized these tools is re-runnable: `references/mining/mine-herdr-ops.py` (baseline in `mining-evidence-2026-09-20.md`). → orca: no script equivalents — orchestration receipts replace them (see orca-routing §Tracked multi-agent work).

## When something breaks

Open [pitfalls.md](references/pitfalls.md) the moment one of these fires — not after the third retry: a send returns non-zero or prints `unknown option`; a python/JSON parse over herdr output crashes (KeyError/JSONDecodeError); a peer seems stuck or its pane vanished; `pane_not_found`/`timeout` in any envelope. 30 failure modes with real error output and fixes, grouped: quoting/envelopes, lifecycle, addressing, environment. For calibration of tone and density when composing or closing — real transcripts of dispatch, reply, integration receipt, termination, peer-to-peer exchange, and the background-first send pattern: [examples.md](references/examples.md).
