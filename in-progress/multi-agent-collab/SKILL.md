---
name: multi-agent-collab
description: "Collaboration protocol for coordinating peer pi sessions over Herdr — appoint a leader, bootstrap named agents, message with the five-part prompt, dispatch with the full-context contract, wait background-first without blocking, verify delivery, close loops with receipts. Use when the user mentions multi-agent work, peer sessions, 多个 session 协作/编排, 开 tab 共同完成, herdr session 间通信, or when a task spans multiple projects or branches and would benefit from parallel sessions. CLI mechanics live in the herdr skill."
---

# Multi-Agent Collaboration

The protocol layer on top of Herdr: who talks to whom, in what shape, and how to wait without deadlocking. CLI mechanics (command syntax, lifecycle states, ID rules) live in the `herdr` skill — that skill for driving the CLI, this one for the collaboration moves. Everything below was distilled from 32 real sessions; failure modes carry evidence in [pitfalls.md](references/pitfalls.md).

## Topology

Peer-ify when the task spans multiple projects, needs multiple branches/worktrees of one repo, or the user asks for parallel sessions. Below that, a single session with subagents is cheaper.

Three roles:

- **Leader** — orchestrates: inventory, bootstrap, dispatch, verify, close. **Appointed by the user, never self-elected.** At 3+ collaborating sessions a leader must exist, named by the user. Leaders defer timing decisions to the user ("notify peers now, or after the deploy finishes?").
- **Peer** — specialist worker (researcher, fixer, writer). Verifies incoming claims against sources before acting, pushes back with file:line evidence, and never answers a user-facing question aimed at another session's user — route it back instead.
- **Explorer** — solo session using herdr for inspection only. No protocol applies.

Bootstrap a named peer (names survive pane churn; pane IDs do not — see pitfalls #14):

```bash
herdr pane split --current --direction right --cwd <peer-repo> --no-focus
# parse .result.pane.pane_id, then:
herdr agent start <name> --kind pi --pane <pane-id>
```

Names must match `[a-z][a-z0-9_-]{0,31}`. Inventory with `herdr agent list` (pane agents — carries each peer's session-JSONL path) and `herdr session list` (server instances; a different, coarser level). Resolve self via `$HERDR_PANE_ID`; when the user hands you a session UUID, resolve it by substring-matching `agent_session.value` in `agent list` output. A finished peer's work is reachable without herdr at all: `session_read <uuid>` plus its artifact files — live conversation while it runs, post-hoc reuse after it ends.

Done when: the role split is stated (who leads, who peers) and every peer has a stable address.

## The message: five-part prompt

Every inter-session prompt has this shape — the receiver depends on it to learn the reply path:

```
/skill:herdr
[caller identity] I am <name> (pane wX:pY, cwd ~/repo; reach me at pane wX:pY)
[context] background, verified facts, data — mark what you verified yourself
[tasks] numbered, each independently checkable; include what NOT to redo
[output + reply] results to <file>; reply via herdr with the path and a summary
```

- The `/skill:herdr` prefix on the first message is mandatory: it triggers the receiver's skill injection, which is how the receiver learns the reply path.
- The explicit reply request at the end is mandatory — a prompt without it goes unanswered (persistent lesson).
- Embed a copy-paste reply command in dispatches. Receivers follow it verbatim, so write it complete: a template missing the prefix produces a reply missing the prefix.
- Address peers by name; sign requests with (name, pane) both.
- Cross-workspace dispatch works (w7 → w13 targets are fine).

### Quoting — three safe strategies, in order

1. Shell variable: `MSG=$(cat <<'EOF' ... EOF)` then `herdr agent prompt <target> "$MSG"`
2. Temp file: `cat > /tmp/task.md <<'EOF'` … then `"$(cat /tmp/task.md)"` — friendliest for versioned resends
3. CJK brackets 「」 wherever the body would otherwise need ASCII double quotes

An ASCII `"` inside the body closes the argument early and the tail parses as flags (`unknown option: <body text>`). A heredoc nested inside `$( )` is environment-sensitive (EOF errors) — use the two-step form. `--wait` is a valueless flag: `--wait false` is an error.

Done when: the message is sent and quoting survived (no `unknown option` in the result).

## Waiting: background-first

The rule: **keep this session concurrent — never park the current turn on a peer's long work.** A foreground `--wait` blocks the whole turn; a leader serially waiting three peers triples the idle time; a peer waiting for its next instruction while its leader waits for a reply deadlocks both.

Choose by expected duration:

| Duration | Strategy |
|---|---|
| >1 min (any real task) | `bg_run` the send: `herdr agent prompt <t> "..." --wait --timeout 1800000`, end the turn, resume on `<background-task-notification>` |
| broadcast, no reply needed | fire-and-forget (no flags); pull later via `agent get` + `agent read` |
| ack / receipt, ≤60s | foreground `--wait --timeout 60000` |
| scripted context, no bg_run | bounded bash poll loop on the settled trio (idle/done/blocked) |
| a specific state needed | `herdr agent wait <t> --until blocked --timeout ...` |

`--timeout` is **milliseconds** and requires `--wait`. There is no completion-subscription mechanism (`herdr notification` only shows) — background tasks and polling are the only waiting primitives. Keep the bash tool timeout above the herdr wait (e.g. 700000 > 600000).

### Delivery evidence — three levels, cheapest first

1. `agent get` → `revision` / `state_change_seq` bumped: machine-checkable receipt.
2. `herdr agent read <t> --source recent-unwrapped | grep -a Steering` — the steering marker proves the message reached the peer's screen.
3. Peer screen content showing it acting on your instructions — the strongest proof; status fields alone are not.

**A `timeout` error is not a delivery failure** — the message is already in the peer's steering queue. Recovery is always `agent get` + `agent read`, never a blind resend. Before resending anything, grep the peer's scrollback to check whether the earlier message arrived, and label the resend ("the previous one may not have arrived — resending").

Parse every response envelope before trusting it. Success: `{"result":{"agent":{...},"type":"agent_prompted"}}` with status at `result.agent.agent_status` (two levels of nesting). Error envelopes have no `result` key — branch on `error` first, or a parse crash reads as failure and triggers a duplicate send (a real incident).

Done when: delivery evidence is confirmed at level 1 or 2 — or the reply itself has arrived.

## The dispatch contract

A task dispatch to a fresh peer carries nine elements (omit only with a stated reason):

1. `/skill:herdr` prefix + caller identity + "your result is invisible unless you report back"
2. Pre-digested context: "Background (already investigated, trust this)" + verified code excerpts — saves the peer re-investigating
3. Anti-redundancy: what is already done — "do not re-diagnose"; "your first step is to compare, not design from scratch"
4. Anti-hallucination: "verify everything against the repo; do not trust this prompt blindly"
5. Precise numbered workflow: branch names, verification commands with expected values, commit conventions, MR template
6. Environment footguns inline: broken tool paths, dangerous flags ("the nix-profile helm is broken; use /usr/bin/helm")
7. Required report schema: branch / commit hash / MR URL / before-after counts — plus the blocked-case protocol: "if blocked, report what you completed and where you stopped"
8. Agreed artifact paths: "reply with the file path only"
9. Language directive: reports in English (for agents), conclusions in Chinese (for the user)

Sequenced tasks get an explicit gate: "task 1 first; report and confirm before task 2." Expect the peer to verify your ground truth and push back with file:line evidence — that is the protocol working, not a failure.

### Handoff currency and receipts

Commit hashes and MR URLs are the currency: peers hold commits for leader approval, the leader specs the commit message, and hashes echo back in acks. After consuming peer output, send an **integration receipt** — which decision adopted it, which ticket or file it landed in, where the full report is archived. Close every thread with a **closure signal**: 任务闭环 / no reply needed / stand down, with a recall clause when the peer may be needed again ("I'll re-contact if review has feedback"). A thread without a closure signal leaves a hanging peer.

When leadership transfers: quiz the successor on its inherited context first ("confirm you can see the map and the frontier"), then send the explicit handoff ("you are now the active X session; I am no longer active"), then `herdr workspace focus <new>` so the user lands on the new leader.

Done when: every dispatched thread has either a receipt or a closure signal on record.

## Shared state

For coordination that outlives individual messages, prefer files over message-passing:

- Maps and tickets: `map.md` + `issues/*.md` with `Status: open|claimed|resolved` and `Blocked by:` — both sides edit; a small renderer derives the frontier and drives dispatch order.
- Shared worktree: probe activity before touching the tree (`find . -newermt '3 hours ago'`), label stashes with ownership ("WIP: dev-sync changes (unrelated to the fix)"), split into separate worktrees once collisions start, and commit peers' uncommitted work before any history rewrite.
- Track pending replies as explicit todo items in each session so they are not forgotten.

## When something breaks

Consult [pitfalls.md](references/pitfalls.md) — 23 failure modes with real error output and fixes, grouped: quoting/envelopes, lifecycle, addressing, environment. Real prompt transcripts (dispatch, reply, integration receipt, termination): [examples.md](references/examples.md).
