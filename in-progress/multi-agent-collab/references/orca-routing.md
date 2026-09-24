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

Stale handle (verified 2026-09-21): prompting a dead/replaced terminal returns `{"code":"terminal_handle_stale", ...}` whose data carries `--retry-request <id> --wait-submit <seconds>` — orca's own replay-until-submit protocol. Recovery = re-issue the EXACT same command with those two flags added (never a fresh request without the ID; that would duplicate the message if the first one landed). Extension users get this handled as a structured error from `orca_send`.

### Peer migrated herdr → orca

When a peer moves from herdr to orca mid-effort, `herdr-resolve.py` returns count=0 across ALL runtimes — that miss IS the migration signal. Fallback flow (verified 2026-09-21, kueue session): `orca worktree list --json` → find the peer's repo path → `terminal list` → handle → send with `[caller identity]` naming the herdr source address (`herdr:<session>:<pane>`). The reply comes back over the peer's own transport.

### Reply path for migrated peers (both directions)

Identity in `[caller identity]` must name the sender's CURRENT transport address, not a historical one — a stale herdr pane plus a vague "走 orca 可达" fallback cost a real reply (verified 2026-09-21, <peer-repo> session: `agent_not_found`, blind resend, groping `herdr --help` for an orca bridge, then a handoff file instead of a reply). Rules:

- orca peer writing to herdr peers: identity carries `orca:<worktree-id>` (displayName) and a reply instruction — reply via `orca terminal list` (worktree → handle) then `orca terminal send --terminal <handle> --enter`.
- herdr peer replying to a migrated orca peer: use the same fallback flow as above (resolve miss → `orca worktree list` → `terminal list` → send). `herdr --help` has no orca bridge — do not grope there.
- Before ANY resend, verify the target: `herdr-resolve.py` (herdr) or `orca terminal list` (orca). Blind resends into a migrated peer's old address are always lost.

## Locating an orca worktree (repo/task → id)

Worktree identity is the canonical selector: `id:<repo-id>::<path>` — every other selector (identity:, name:, branch:, issue:, path:) derives from it. Find one by repo/task fragment (verified 2026-09-21, expense session):

```bash
orca-ide worktree list --json | python3 -c "
import sys, json
d = json.load(sys.stdin)
wts = d.get('worktrees') or d.get('result', {}).get('worktrees', [])
for w in wts:
    path = w.get('path') or w.get('dir') or ''
    if '<repo-slug>' in path:   # ← your repo/task fragment
        print(json.dumps(w, ensure_ascii=False))"
```

A worktree created OUTSIDE orca (e.g. via `wt switch -c` in a herdr session) still shows up here — orca watches the filesystem. `--json` shape: `{id: "<repo-id>::<path>", path, displayName, branch, hostId}`; `identity.key` is OPTIONAL (present on managed/child rows, absent on main-repo rows). On Linux the binary is `orca-ide` — that is the SOLE probe (`orca-ide status --json`); bare `orca` is the GNOME screen reader on hosts without the dispatcher shim, so never chain-probe `orca status`.

## Starting a pi session in an orca worktree

Two paths, chosen by whether the worktree already exists:

**A. Existing worktree** (created by herdr-side `wt switch -c`, or reused): create a pi terminal in it, wait for the TUI, then dispatch the bootstrap prompt (verified 2026-09-21, expense session — full chain):

```bash
orca-ide terminal create --worktree "id:<repo-id>::<path>" --command 'pi' --json
#   → parse the handle from the result (field name is undocumented; check
#     result.id AND result.handle). NOTE: --command 'pi' starts a bare pi; pass your
#     bootstrap prompt via terminal send AFTER tui-idle, not via create.
#     Omit --title unless you WANT a pinned tab title — a custom title blocks
#     native pi-title/spinner mirroring (verified 2026-09-16).
orca-ide terminal wait --terminal <handle> --for tui-idle --timeout-ms 90000 --json   # TUI ready
orca-ide terminal send --terminal <handle> --text "$(cat /tmp/bootstrap.md)" --enter --json
sleep 45; orca-ide terminal read --terminal <handle>   # confirm the peer picked it up
```

**B. New worktree + agent in one step** (fresh task from a charted map):

```bash
orca-ide worktree create --name <ticket-slug> --repo id:<repo-id> \
  --agent pi --prompt "<five-part bootstrap>" --setup inherit --json
```

- `--prompt` carries the five-part bootstrap (map link, which ticket to claim, reply path). `--setup inherit` honors repo setup hooks — this is where `hookSettings.scripts.setup` (e.g. the go.mod-replace symlink fix) runs.
- Selector sanity: use the SAME transport as the peer — a herdr wayfinder session can call `orca-ide` directly from its shell (same machine); no cross-transport gymnastics needed for creation, only for ongoing conversation.

Wayfinder integration (dev/default-branch session charts the map → implementation sessions claim tickets): after the map/tickets exist, path B is the one-step spawn; path A is for reusing a worktree that already holds prepared state (uncommitted fix, claimed branch).

**The bootstrap prompt (`--prompt` / the send-after-create message) MUST carry `[caller identity]` + a reply instruction** — a peer spawned without it cannot deliver results at all (verified 2026-09-21: an orca-spawned research peer guessed a stale herdr pane, got `agent_not_found`, and only a manual bridge delivered its report). Identity form: `orca:<worktree-id>` when the peer will reply over orca; include the dispatcher's terminal handle or the `terminal list` bridge recipe.

## Tracked multi-agent work: use Orchestration, not terminal send

Plain `terminal send` is the fire-and-forget tier. For dispatched work with receipts, use the orchestration layer — this is the herdr dispatch contract, productized. **Verbs verified live on app 1.4.205 (2026-09-21); earlier drafts of this section listed imagined commands — re-verify with `orca-ide orchestration <verb> --help` after any orca upgrade:**

```bash
# coordinator side
orca orchestration run-create --objective "<goal>" --json          # Run = persistent namespace + inbox
orca orchestration task-create --spec "<spec>" --run <run_id> --json   # Task = spec + states
orca-ide worker-start --worktree <selector|new-child> --json        # placement lives on worker-start, not dispatch

# consumption: FIFO replay-until-ack — a timeout never means "lost"
orca orchestration check --wait --types worker_done --json           # returns the batch incl. delivery ids
orca orchestration check --ack <delivery_id> --json                  # ack needs the delivery id
orca orchestration check --peek --json                               # look without consuming

# blocking Q&A (contact_supervisor equivalent)
# worker side: ask is only valid inside an ACTIVE dispatch — pass the
# --dispatch-capability token from your worker preamble; --question is REQUIRED
orca orchestration ask --dispatch-capability <token-from-preamble> --question "<text>" --options "a,b,c" --timeout-ms 600000
# coordinator side: resolve the gate the ask created
orca orchestration gate-resolve --id <gate_id> --resolution "<text>"
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
