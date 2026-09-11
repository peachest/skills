# Discovery routing — judgment tests and worked example

Supports the [Discovery routing](../SKILL.md#discovery-routing) section. Read when a work
session surfaces something the current map cannot hold and the branch is not obvious.

## Why this exists

Charts are static but work is not. Without a routing rule, execution-time discoveries
get handled ad hoc — usually a single issue opened in the moment, then manually folded
days later — and the relationship between maps lives only in one person's memory. Two
maps end up sharing a design surface (e.g. the same CRD field shaped by both) with no
structural record of it, so rework risk is invisible until it lands.

The rule: a discovery is **routed**, never silently absorbed, never silently chartered
around. Four branches, tested in order — first hit wins.

## The four judgment tests (in order)

### 1. External ownership test

**Ask:** who does the work if we route it right?

If the answer is "a party outside this map" — another team, an upstream project, a
vendor — then no ticket exists, regardless of how big the finding is. This map's only
decisions are *timing* ones (can we proceed, on what assumption, until the external
work lands). Record one line in the map body: the dependency and the timing decision.

Getting this right first matters because the other three branches all create
structure inside *our* tracker; structure for someone else's work goes stale and
misleads the frontier.

### 2. Sub-ticket test

**Ask:** can the finding be stated as one sharp question, and does its answer leave
every other open ticket's premises intact?

Both halves must hold. "How should X be designed" is sharp, but if its answer changes
what an open ticket already assumes, it fails the second half — that is branch 3. A
true sub-ticket is local: wire `blocked_by` to whatever it depends on and let the
frontier absorb it.

### 3. New-map test

**Ask:** does the finding change premises of open tickets, or does the work sit at a
different altitude than this map's destination?

Either is enough. "Different altitude" in practice means: the finding needs its own
destination — its own spec, its own decision set — rather than being one decision on
someone else's route. Charter via the normal Chart flow, then bind the two maps:

- New map's **Notes** open with `Spawned from: <parent map/ticket link> — one line why`.
- Parent map gains a **Spawned maps** line: link + gist.
- Cross-map blocking: any parent open ticket whose design the new map will overturn
  is blocked on the new map's corresponding ticket. On trackers with native blocking
  (GitLab: any issue can block any issue), use it — the frontier query then hides the
  at-risk ticket automatically. The local-markdown tracker's `blocked_by` is
  map-scoped; degrade to a body `Blocked by: <map-slug>#<id>` line and check it by
  eye when working the parent map.

### 4. Not-yet-gradeable

**Ask:** is even the branch assignment unknown?

Open one `research` ticket in the current map whose deliverable is precisely the
grading: enough facts to run tests 1-3. Its resolution comment routes the finding.
If a temporary issue was created before grading (often by an execution session in
the moment), it **folds**: close it with a `Folded into <link>` comment and a
relates_to link. Folding, not deleting — the investigation trail is worth more than
the closure is worth.

## HITL gate

The agent proposes the branch (with the test that fired); the human confirms before
anything is created. An agent that charters a new map unilaterally has broken this
protocol, the same way a grilling agent that answers its own questions has broken
its ticket.

## Worked example (real, 2026-09)

HA-refactor map (#15) on example-manager, mid-execution:

1. A design question about a newly-added status field led to the discovery that the
   project had not aligned with upstream HAMi v2.10's initContainer design.
2. First reaction — a standalone issue (#36) to investigate. That was branch 4,
   executed without the protocol: correct destination, no grading deliverable named.
3. A new constraint surfaced (the internal fork would sync to v2.10), which blew the
   fog wide: 98-file delta, +40971/−7032 lines, private patches to rebase. The
   finding now failed test 2 (it reshaped CRD design premises) — branch 3.
4. A new map (#37) was chartered; #36 folded into it. What was *missing*, and what
   this protocol now requires: the spawned-from/parent links, and the HA map's open
   tickets whose field design depended on v2.10 semantics being blocked on #37's
   decisions — they were left takeable, and the dependency lived only in memory.
5. The fork-sync-to-v2.10 work itself was correctly recognized as someone else's
   (branch 1): no ticket, external dependency, timing decisions only.
