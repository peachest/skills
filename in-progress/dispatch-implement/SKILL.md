---
name: dispatch-implement
description: Fix the spawn process and message protocol for design↔implement session pairs on orca — main session creates a worktree via wt, starts an implement pi session there, dispatches tickets, and runs the review/CI-failure feedback loop over orca orchestration. Supports parallel dispatch (N implement sessions, one ticket each). Use when the user says 派发实现 / 起 implement session / 创建实现 session / 并行派发实现 / dispatch-implement, or when a design session is ready to hand tickets to implementation sessions. Does NOT own the implement skill content, review skills, or MR creation — only the spawn chain and protocol shapes.
---

# Dispatch Implement

Fixes two things and nothing else: **the spawn chain** (worktree → implement pi session) and **the protocol** (message shapes for dispatch, receipt, fix rounds, closure). Workflow order (when to review, when to create MR, when to clean up) lives in the user's process, not here. Protocol primitives (five-part prompt, receipts, waiting) come from `multi-agent-collab` — read it first; this skill only adds the orca worktree specifics.

## Scope boundary

| In scope | Out of scope |
|---|---|
| wt worktree creation + branch naming | what /skill:implement does inside the session |
| implement session bootstrap prompt (must load the work skill) | ticket splitting (to-tickets) and spec quality |
| orchestration dispatch/receipt shapes | review skills (ocr, code-review), create-mr |
| parallel-dispatch rules | docs update, wiki write-back (domain-modeling / okb) |

## Process — spawn one implement session

Run from the main (design) session's shell. Verified chain (2026-09-21, orca app 1.4.205):

```bash
# 1. worktree — wt owns branch naming (<type>/<ticket-slug>, e.g. fix/ctx-421-device-type)
#    and hooks (deps install). -b <base> for non-default base.
wt switch -c fix/ctx-421-device-type          # cwd follows into the new worktree

# 2. resolve the worktree's orca id (orca indexes ~/projects/* worktrees automatically)
orca-ide worktree list --json | jq '.worktrees[] | select(.path | contains("<branch-slug>")) | .id'

# 3. orchestration run + task (once per effort; skip if the Run exists)
orca-ide orchestration run-create --objective "<effort title>" --json
orca-ide orchestration task-create --run <run_id> --spec "<bootstrap prompt, see below>" --json

# 4. start the worker pi session in the worktree, bound to the task
orca-ide orchestration worker-start --task <task_id> --worktree "id:<wt-id>" --agent pi --name impl-<branch-slug> --json
```

`scripts/spawn-implementer.sh <repo-cwd> <branch> --spec-file <file> [--base <branch>]` wraps steps 1–4 in one call (idempotent-ish: skips `wt switch -c` if the branch's worktree already exists). Prefer it — it also prints the handle/receipt line the coordinator needs.

**Fallback (orchestration unavailable):** `orca-ide terminal create --worktree "id:<wt-id>" --command 'pi' --json` → `terminal wait --terminal <handle> --for tui-idle` → send the bootstrap prompt via a **temp file** (`terminal send --terminal <handle> --text "$(cat prompt.md)" --enter`). Never inline the prompt: quoting dies. Send may report `observation: unsupported` — confirm delivery via `terminal read` or the peer flipping to `working`, not the send exit code.

## Bootstrap prompt — the fixed part

Every implement session's first message MUST start with the skill-load directives, then the five-part shape. The skill-load lines are non-negotiable: they are what removes the "user has to tell the main session every time" failure.

```
/skill:multi-agent-collab
/skill:implement
[caller identity] I am <coordinator name> (orca:<coordinator-wt-id>, branch <branch>).
  Reply through the orchestration worker contract: exactly one worker_done per dispatch;
  raise blockers mid-task via orchestration ask, never by going silent.
[context] repo + worktree path; ticket tracker location; spec doc link (issue tracker);
  conventions that constrain the code (verified facts only).
[tasks] You own ticket <ID> ("<title>") and nothing else. Read the spec at <link>,
  load /skill:implement, implement it. Do NOT claim other tickets; do NOT touch
  files outside the ticket's stated blast radius.
[output + reply] worker_done fields — ticket, outcome (succeeded/failed), branch tip,
  commits, files touched, blockers, notes.
```

## Protocol — the four message shapes

### 1. Receipt (implement → main)
`worker_done --outcome succeeded|failed --task <task_id>` — text body carries the fixed fields: `ticket / outcome / branch tip / commits / files touched / blockers / notes`. Coordinator consumes via `check --wait --types worker_done` then `check --ack <delivery_id>` (batch-aware: with N workers, one check call returns the pending batch).

### 2. Review feedback (main → implement)
Re-dispatch on the same worktree with `worker-start --retry-of <dispatch_id> --worktree id:<wt-id>` (note: `--retry-of` takes the **dispatch id**, not the task id), spec:

```
[caller identity] as bootstrap (unchanged reply path)
[context] review round <N> on branch <branch> — source: <ocr | code-review> report <path-or-link>
[tasks] fix exactly these findings; change nothing else:
1. [severity] file:line — issue — expected behavior
...
[output + reply] same worker_done fields as bootstrap.
```

### 3. CI failure (main → implement)
New task on the same Run; re-dispatch same as review feedback (`worker-start --retry-of <dispatch_id>`). `[context]` carries `MR !N / branch / failed job <name> (<stage>) / log <link or tail excerpt>`. Findings list = one entry per failing check, error-first (first failure first).

### 4. Closure (main → implement)
Terminal-send only (no new task): `stand-down: no further work; report uncommitted state in one line; worktree cleanup is the coordinator's job.` Implementation session stays alive until `wt remove` — orca closes its terminal automatically when the worktree goes.

## Parallel dispatch

- **One worktree per implement session, one ticket per session.** Ticket IDs are assigned by the coordinator in `[tasks]` — never self-claimed from a shared tracker (double-claim race).
- All workers join one Run; tickets must be disjoint by construction (to-tickets guarantees this — if two tickets touch the same file, they are not parallelizable; sequence them instead).
- Spawn with `scripts/spawn-implementer.sh` N times (distinct branches), then one `run-create` + N `task-create`, then N `worker-start`. Collect receipts with batch `check --wait --types worker_done`.
- `worker_done` names the branch tip — merge order is the coordinator's call (workflow, not protocol).

## First-use verify + version drift

Orchestration verbs verified 2026-09-21 on orca app **1.4.205**. After an orca upgrade, re-verify before the first dispatch:

```bash
orca-ide orchestration --help 2>&1 | head -30
orca-ide orchestration worker-start --help 2>&1 | head -15
```

If a verb/flag moved, fix `scripts/spawn-implementer.sh` + this file in the same commit, and log the drift in `wiki/dispatch-implement/skill-impact.md`.

## Pitfalls

Load `multi-agent-collab` → `references/orca-routing.md` §Tracked multi-agent work and §Bootstrap a peer on first use; transport-level pitfalls (idle-gate, observation-unsupported, cross-runtime addressing) are catalogued there and are not repeated here.

`scripts/check-env.sh` verifies the spawn chain's tool assumptions (wt, orca-ide, runtime reachable) — run it on a new node before the first spawn.
