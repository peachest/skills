---
name: dispatch-implement
description: Dispatch implementation sessions for design↔implement pairs on orca — owns only the spawn chain and message protocol. Trigger when the user says 派发实现 / 起 implement session / 并行派发实现 / dispatch-implement, or when a design session is ready to hand tickets to implementation sessions. Does NOT own the implement skill content, review skills, or MR creation.
---

# Dispatch Implement

Fixes two things and nothing else: **the spawn chain** (worktree → implement pi session) and **the protocol** (message shapes for dispatch, receipt, fix rounds, closure). Workflow order (when to review, when to create MR, when to clean up) lives in the user's process, not here. Protocol primitives (five-part prompt, receipts, waiting) come from `multi-agent-collab`; only the orca worktree specifics live here — reach it under the conditions in §Pitfalls.

## Scope boundary

| In scope | Out of scope |
|---|---|
| wt worktree creation + branch naming | what /skill:implement does inside the session |
| implement session bootstrap prompt (must load the work skill) | ticket splitting (to-tickets) and spec quality |
| orchestration dispatch/receipt shapes | review skills (ocr, code-review), create-mr |
| parallel-dispatch rules | docs update, wiki write-back (domain-modeling / okb) |

## Process — spawn one implement session

Run from the main (design) session's shell. Chain verified end-to-end 2026-09-22 (orca app 1.4.2xx, first live spawn):

```bash
# 1. worktree — wt owns branch naming (<type>/<ticket-slug>, e.g. fix/ctx-421-device-type)
#    and hooks (deps install). -b <base> for non-default base.
wt switch -c fix/ctx-421-device-type          # cwd follows into the new worktree

# 2. resolve the worktree's orca id (orca indexes ~/projects/* worktrees via fs-watch;
#    a freshly created worktree may lag a few seconds — retry before giving up)
orca-ide worktree list --json | jq '.result.worktrees[]? // .worktrees[]? | select(.path | contains("<branch-slug>")) | .id'

# 3. orchestration run + task (once per effort; skip if the Run exists)
#    run id = .result.run.id (run_* prefix) — top-level .id is the mutation-request uuid
orca-ide orchestration run-create --objective "<effort title>" --json
orca-ide orchestration task-create --run <run_id> --spec "<bootstrap prompt, see below>" --json

# 4. start the worker pi session in the worktree, bound to the task
#    NO creation flags (--name/--setup/--repo/...) — rejected for existing worktrees
orca-ide orchestration worker-start --task <task_id> --worktree "id:<wt-id>" --agent pi --json
```

**Run binding is per-coordinator-terminal and `run-create` rebinds it.** The probe run-create during drift repair silently rebound the coordinator terminal to the probe Run, fencing it from the real Run — the worker_done sat in the orphaned Run's inbox while every `check` failed `consumer_fenced`. Rules: never run `run-create` from the coordinator terminal mid-effort (use the worker side or a throwaway terminal for probes); after any fencing error, recover with `orchestration run-use --id <run_id> --from <coordinator-handle>` then `check --terminal <handle> --run <run_id> --types worker_done` and `--ack <delivery_id>`.

**Ambiguity rule (worker-start):** its success output is easy to misread — on any error from `worker-start`, run `orchestration dispatch-show --task <task_id> --json` BEFORE retrying. A first call that actually succeeded makes the retry the only failure, and the duplicate-dispatch error proves nothing about the first. `dispatch-show` (status + terminalHandle) is the delivery-evidence step, not an optional extra.

`scripts/spawn-implementer.sh <repo-cwd> <branch> --spec-file <file> [--base <branch>] [--run <run_id>] [--list]` wraps steps 1–4 in one call (idempotent-ish: skips `wt switch -c` if the branch's worktree already exists; `--run` reuses an existing Run instead of creating one). Prefer it — it also prints the handle/receipt line the coordinator needs.

**Fallback (orchestration unavailable):** `orca-ide terminal create --worktree "id:<wt-id>" --command 'pi' --json` → `terminal wait --terminal <handle> --for tui-idle` → bootstrap per the two-send sequence in §Bootstrap prompt (second send via a **temp file**: `terminal send --terminal <handle> --text "$(cat prompt.md)" --enter`). Never inline the prompt: quoting dies. Send may report `observation: unsupported` — confirm delivery via `terminal read` or the peer flipping to `working`, not the send exit code.

## Bootstrap prompt — the fixed part

pi expands `/skill:<name>` only at the **start of a user prompt** (prefix position). Orca's orchestration dispatch structurally breaks this: the spec arrives embedded after the worker preamble inside one user message, so `/skill:` there can never reach prefix position and never expands (verified live 2026-09-22: worker never loaded the skill, went straight to code). Typing is irrelevant — `herdr agent prompt`/`terminal send` messages expand fine when `/skill:` is their first line; the dispatch path cannot offer that position. The bootstrap therefore routes by channel:

**Orchestration path (spec message):** the orca worker preamble already carries the reply path and receipt discipline (worker contract, `--dispatch-capability` token) — the multi-agent-collab bootstrap is redundant there. Skill loading must be an explicit file-read instruction, not a slash prefix. The spec is ONE message:

```
[context] FIRST ACTION before any code work: read the implement skill file
  (~/.pi/agent/skills/implement/SKILL.md) and follow it as the work discipline.
  Repo: <repo-path> (worktree <branch>); ticket tracker at <tracker-location>; spec
  doc at <spec-link>; conventions that constrain the code (verified facts only).
[tasks] You own ticket <ID> ("<title>") and nothing else. Read the spec at <spec-link> and
  implement it under the implement skill's discipline. Touch only files inside the
  ticket's stated blast radius.
[output + reply] worker_done fields — ticket, outcome (succeeded/failed), branch tip,
  commits, files touched, blockers, notes. Raise blockers mid-task via orchestration
  ask with the preamble's dispatch-capability token; never go silent.
```

If the visible skill-expansion UI is wanted anyway, the message must start with `/skill:implement` at position 0 — via `terminal send` after `worker-start` — but the file-read instruction stays the deterministic guarantee; the typed send is cosmetic and may arrive mid-turn.

**Terminal-send fallback (two sends, skills before task):** no worker contract exists, so both skills are needed — as two sequential **typed** sends (typed = TUI path = expansion works). Order is fixed: skill loads first, tasking second; reversed, the worker starts working and the second skill arrives as mid-turn steering.

1. after `terminal wait --terminal <handle> --for tui-idle` returns, send: `/skill:implement` (expansion-only message)
2. after `terminal wait --terminal <handle> --for tui-idle` returns again, send the tasking message via a **temp file** — first line `/skill:multi-agent-collab`, then `[caller identity] / [context] / [tasks] / [output + reply]`, with `[tasks]` carrying the ticket assignment from the template above.

The first-action read instruction is what removes the "user has to tell the main session every time" failure — and the coordinator should verify it fired: the worker's transcript must show a read of the implement SKILL.md before any code edit.

## Protocol — the four message shapes

### 1. Receipt (implement → main)
The worker's `worker_done` (outcome `succeeded|failed`; flags follow the preamble's worker contract) — body carries the fields defined in the bootstrap `[output + reply]`. Coordinator consumes via `check --wait --types worker_done` then `check --ack <delivery_id>` (batch-aware: with N workers, one check call returns the pending batch).

### 2. Review feedback (main → implement)
Re-dispatch the same dispatch on the same worktree: `worker-start --retry-of <dispatch_id> --worktree id:<wt-id> --spec "<findings>"` (note: `--retry-of` takes the **dispatch id**, not the task id; `--spec` replaces the tasking with the findings message):

```
[caller identity] unchanged — the reply path is the worker preamble's, not a re-typed address
[context] review round <N> on branch <branch> — source: <ocr | code-review> report <path-or-link>
[tasks] fix exactly these findings; change nothing else:
1. [severity] file:line — issue — expected behavior
...
[output + reply] same worker_done fields as the bootstrap template.
```

### 3. CI failure (main → implement)
Same mechanism as review feedback — re-dispatch the failing dispatch (`worker-start --retry-of <dispatch_id> --worktree id:<wt-id> --spec "<ci-findings>"`), no new task. `[context]` carries `MR !N / branch / failed job <name> (<stage>) / log <link or tail excerpt>`. Findings list = one entry per failing check, error-first (first failure first).

### 4. Closure (main → implement)
Resolve the handle via `terminal list --json` (match the worktree — `terminal send` has no `--worktree` flag), then send: `stand-down: no further work; report uncommitted state in one line; worktree cleanup is the coordinator's job.` The session stays alive until `wt remove`; orca closes the terminal with the worktree (verified 2026-09-22: `terminal list` shows 0 matches after `wt remove` — no manual terminal close needed).

## Parallel dispatch

- **One worktree per implement session, one ticket per session.** Ticket IDs are assigned by the coordinator in `[tasks]` — never self-claimed from a shared tracker (double-claim race).
- All workers join one Run; tickets must be disjoint by construction (to-tickets guarantees this — if two tickets touch the same file, they are not parallelizable; sequence them instead).
- Spawn with `scripts/spawn-implementer.sh` N times on distinct branches: first spawn without `--run` (creates the Run), every later spawn passes the same `--run <run_id>`. Collect receipts with batch `check --wait --types worker_done`.
- `worker_done` names the branch tip — merge order is the coordinator's call (workflow, not protocol).

## First-use verify + version drift

Orchestration chain verified end-to-end 2026-09-22 on orca app 1.4.2xx (first live spawn: run → task → dispatch → worker terminal). After an orca upgrade, re-verify before the first dispatch:

```bash
orca-ide orchestration --help 2>&1 | head -30
orca-ide orchestration worker-start --help 2>&1 | head -15
```

If a verb/flag moved, fix `scripts/spawn-implementer.sh` + this file in the same commit, and log the drift in the **source repo's root wiki**: `~/skills/wiki/dispatch-implement/skill-impact.md` — a repo-root path, not relative to this skill's directory (a relative `wiki/` here ships the wiki inside every installed copy; that already happened once). Verify pass = `bash scripts/check-env.sh` ends PASS and the verb surface still shows every flag the script uses.

**Drift fixes land in the source repo** (`<SKILL_SRC>/`, i.e. `~/skills/in-progress/dispatch-implement/`) followed by `npx skills add -g ./in-progress/dispatch-implement -a pi -y` — never edit the installed copy under `<SKILL_DIR>/`, which the next reinstall silently overwrites.

## Pitfalls

Load `multi-agent-collab` → `references/orca-routing.md` §Tracked multi-agent work and §Bootstrap a peer on first use; transport-level pitfalls (idle-gate, observation-unsupported, cross-runtime addressing) are catalogued there and are not repeated here.

`scripts/check-env.sh` verifies the spawn chain's tool assumptions (wt, orca-ide, runtime reachable) — run it on a new node before the first spawn.
