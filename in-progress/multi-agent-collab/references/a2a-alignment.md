# A2A alignment — what the A2A v1.0 protocol gives this skill

A2A (a2a-protocol.org, Linux Foundation) is the industry-standard agent-to-agent
protocol. This is not a competing proposal: it validates this skill's
transport-agnostic layering and supplies vocabulary for its gaps. Full analysis
snapshot: `~/research/a2a-vs-multi-agent-collab/` (2026-09-24). Adopted here:
three protocol clauses, nothing more — no HTTP layer, no AgentCard infrastructure.

## Why the architectures agree

| This skill | A2A |
|---|---|
| transport-agnostic protocol + herdr/orca bindings | L1 proto / L2 abstract ops / L3 bindings ("semantic consistency, swappable bindings") |
| five-part prompt | Message + Parts |
| orca Run/Task/dispatch, worker_done | Task + TaskState events |
| orchestration ask / decision gates | TASK_STATE_INPUT_REQUIRED |
| check --wait / background-first | GetTask / push notifications |

## Adopted clause 1 — canonical task-state vocabulary

All receipts and status mentions map onto A2A's states, regardless of transport:

```
dispatch sent → submitted | worker started → working | blockers raised → input-required
worker_done succeeded → completed | worker_done failed → failed | canceled by coordinator → canceled
```

herdr `agent_status` and orca task statuses are bindings of these states, not
additional vocabulary. A receipt that cannot be mapped to one of the eight
states is malformed — the sender must restate it.

## Adopted clause 2 — correlation token across rounds

All rounds on one ticket (dispatch, review fix, CI fix) share one correlation
token: the ticket ID. Later rounds reference earlier ones by that token
(referenceTaskIds semantics). orca rounds additionally use
`worker-start --retry-of <dispatch_id>`; herdr rounds carry the token in
`[context]` (`round N of <ticket>`). A round without the token breaks receipt
correlation — coordinator cannot batch-match worker_done to tickets.

## Adopted clause 3 — dispatch idempotency

Treat every dispatch as carrying an implicit messageId (ticket + round + target).
Rules, in order:
1. **Ambiguity rule**: any `worker-start` error → `dispatch-show --task <id>`
   BEFORE retrying; the first call may have succeeded and the retry is the only failure.
2. Receipt consumption: ack takes the **delivery id** from check output —
   a message-id ack returns `stale_delivery` (harmless, but proves nothing).
3. Never claim "sent" without a tool result in the transcript (worker-side rule).

## Explicitly NOT adopted

- HTTP server lifecycle / AgentCard / well-known URI / registry — the peers are
  interactive TUI sessions with a human watching; A2A has no concept of a human
  observing the transport. A2A replaces nothing here until a peer must be
  callable as a headless service (no such consumer exists).
- OAuth2/mTLS/registries — cross-org fleet concerns; single-node human-orchestrated
  collaborations don't pay for them.

Replacement risk: low. If pi/orca ever implement A2A bindings natively, the
herdr/orca binding chapters here degrade to "yet another binding" while the
protocol layer (five-part prompt, receipts, waiting, human-in-loop) survives —
the layering is the resilience.
