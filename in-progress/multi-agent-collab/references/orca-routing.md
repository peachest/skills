# Orca routing — orca counterparts for every herdr-bound move

Load this when the environment probe resolved to `orca` (see SKILL.md §Environment & routing).
Protocol discipline (five-part prompt, dispatch contract, receipts, closure signals) is
unchanged — only the transport commands differ. Deep CLI mechanics live in the installed
`orca-cli` and `orchestration` skills; load the live guide with `orca skills get <topic> --full`.

On Linux resolve the CLI as `orca-ide` (bare `orca` is the GNOME screen reader outside
Orca-managed terminals). Below, `orca` is a placeholder for the resolved binary.

Orchestration is Experimental and must be enabled in the client's Settings before any
`orca orchestration` command works. Verify once: `orca orchestration --help`.

## Addressing

| herdr | orca |
|---|---|
| pane `w3:p2` | worktree selector: `active` / `id:<id>` / `path:<abs-server-path>` |
| agent name (survives pane churn) | worktree id (survives restarts; from `orca worktree list --json`) |
| broadcast | group addresses: `@all` `@idle` `@codex` `@worktree:<id>` — never for worker_done/heartbeat |
| self via `$HERDR_PANE_ID` | self via `orca worktree current --json` |

For remote runtimes prefer full server-side selectors (`path:<absolute-server-path>`) —
the client-side cwd does not exist on the runtime [orca-cli skill: selectors].

## Bootstrap a peer

Peers live in worktrees, not panes:

```bash
orca worktree create --name <task-slug> --agent pi --prompt "<five-part prompt>" --json
# parse .id — the worktree id is the peer's stable address for its whole life
```

- Names follow the same `[a-z][a-z0-9_-]` discipline (it becomes branch + worktree name).
- Orca places worktrees under `~/orca/workspaces/<repo>/<name>` [measured 2026-09-20] —
  `go.mod replace ../X` relative deps BREAK in that layout. Fix (POC-verified): symlink the
  dep repo into the worktree's parent directory; automate it once per repo via the repo's
  `hookSettings.scripts.setup` (orca repo metadata) instead of per-worktree manual glue.
- `--prompt` carries the five-part prompt as the first message. The `/skill:multi-agent-collab`
  bootstrap prefix still applies — orca delivers it, but the protocol injection is ours.
- A finished peer's work: `session_read <uuid>` still works — pi transcripts stay in
  `~/.pi/agent/sessions` regardless of transport.

## Sending and steering

`terminal send` has NO `--worktree` flag (verified 2026-09-21: validFlags = enter/environment/interrupt/json/pairing-code/retry-request/terminal/text/wait-submit) — bridge worktree → handle via `terminal list` first:

```bash
# worktree → terminal handle bridge
orca terminal list --json | python3 -c "
import json,sys
d=json.load(sys.stdin)
res=d.get('result') or {}
for t in (res.get('terminals') or res.get('list') or []):
    if 'expense' in json.dumps(t): print(t['handle'])"   # adapt filter to your field names

orca terminal send --terminal <handle> --text "<message>" --enter --json
orca terminal wait --for tui-idle --terminal <handle> --timeout-ms 30000 --json
orca terminal read --terminal <handle> --json   # ground truth when detection is unsure
```

POC-verified against pi (2026-09-20): send may report `observation: unsupported` — fall back to `terminal read` for delivery confirmation instead of trusting the send result. Delivery evidence for a notification: peer flips to `working` right after send (it consumed the message); `wait --for tui-idle` timing out while peer is working is EXPECTED — do not resend.

### Peer migrated herdr → orca

When a peer moves from herdr to orca mid-effort, `herdr-resolve.py` returns count=0 across ALL runtimes — that miss IS the migration signal. Fallback flow (verified 2026-09-21, kueue session): `orca worktree list --json` → find the peer's repo path → `terminal list` → handle → send with `[caller identity]` naming the herdr source address (`herdr:<session>:<pane>`). The reply comes back over the peer's own transport.

## Tracked multi-agent work: use Orchestration, not terminal send

Plain `terminal send` is the fire-and-forget tier. For dispatched work with receipts, use
the orchestration layer — this is the herdr dispatch contract, productized:

```bash
# coordinator side
orca orchestration run-start --json                      # Run = persistent namespace + inbox
orca orchestration task-add --run <id> --spec ... --json # Task = spec + deps + six states
orca orchestration dispatch --task <id> --worktree <sel> --json

# consumption: FIFO replay-until-ack — a timeout never means "lost"
orca orchestration check --wait --types worker_done --ack --json
orca orchestration check --peek --json                   # look without consuming

# blocking Q&A (contact_supervisor equivalent)
# worker side: ask is only valid inside an ACTIVE dispatch — pass the
# --dispatch-capability token from your worker preamble
orca orchestration ask --dispatch-capability <token-from-preamble> --options "a,b,c" --timeout-ms 600000
# coordinator side: resolve the gate the ask created
orca orchestration gate-resolve --gate <id> --choice <c>
```

Worker contract replaces our manual receipt discipline: exactly one `worker_done
--outcome succeeded|failed` per dispatch (task+dispatch ids prevent stale retries),
heartbeats for long work, `--retry-of` for explicit re-dispatch.

Environment caveat (POC-verified): orca's status hooks install as user-level pi extensions
(`orca-agent-status.ts`), so EVERY pi session on the host — including herdr tabs — reports
status to orca. Harmless, but orca's agent views will mix in non-orca sessions; treat
`orca agent hooks status` as unreliable for pi coverage.

## Waiting: background-first

The rule is unchanged; the mechanism improves. Orca messages persist in the Run inbox
with replay-until-ack, so dispatch → end turn → `check --wait` on the next wake is the
native background-first pattern — no bg_run wrapper needed for the send itself.
Foreground `check --wait` / `terminal wait` only for the ≤60s receipt tier.

## Delivery evidence — three levels, cheapest first

1. `worker_done` consumed via `check --ack` — machine-checkable, exactly-once.
2. `check --peek` showing the message sitting in the peer's inbox / heartbeat fresh.
3. `orca terminal read --terminal <handle>` showing the peer acting on the instructions.

No quoting hell: orchestration messages are structured (spec/JSON), not shell-embedded
text. The three quoting strategies in SKILL.md apply only to `terminal send --text`
one-liners — prefer temp-file two-step there too.

## Handoff and closure

- No `workspace focus` equivalent: leadership transfer = dispatch a coordinator-role
  message to the Run inbox (the quiz-first discipline from SKILL.md still applies).
- Closure: for tracked work, `worker_done` + coordinator ack **is** the closure signal —
  add the recall clause as a message when needed. For terminal-send conversations, keep
  the textual 任务闭环 / stand-down signal.

## Failover

If the runtime is unreachable (`orca status --json` fails) mid-collaboration, the peer
sessions on the same host are still alive (server owns them). Re-check serve: on the
runtime host run `orca-serve status` (or the host's service manager), then re-probe.
