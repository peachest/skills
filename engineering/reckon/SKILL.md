---
name: reckon
description: "Recover your position after time away — dead-reckon current progress across every project this session touches. Invoke with /reckon; stays on until \"stop reckon\". Use when position is lost: returning after a break, resuming a session, or losing track of which project/branch/MR you are on."
disable-model-invocation: true
---

# reckon

After time away — overnight, a weekend, a context switch — your exact position is lost. You know the terrain exists, but not where on it you stand. **Reckoning** recovers position the way dead reckoning does: from the last known fix (what the session remembers) plus the distance traveled since (what git and the tracker record).

Orient reads terrain to produce a bearing. Reckon reads the wake you left — commits, MRs, tickets, session memory — to fix your position. They are orthogonal: orient is spatial (what is here), reckon is temporal (where did I get to).

## Persistence

These rules apply to every response for the rest of the session. Turn them off only when the reader says "stop reckon" or "normal mode"; confirm in one line and return to your default behavior.

Pi `--resume` carries the session forward; the compaction's Constraints section preserves the fact that reckon is active, so the rules survive a resume without re-invocation. If a compaction drops the activation, the first response after compaction re-establishes the baseline (see rule 4). A fresh session (not resumed) starts clean — reckon is opt-in.

## What this changes

Five facts drive every rule below:

1. Multiple projects run in parallel. The one not on screen is the one forgotten.
2. A branch with unpushed commits is work in limbo — it survived the weekend, but only locally.
3. An open MR blocked by another MR is a chain, not a single task. "Waiting on review" has a shape.
4. The session's last compaction summary holds intent, not just state — "I was about to wire the HAMi scheduler" is a position, not a fact about files.
5. The wayfinder frontier — open tickets takeable now — is the part of the map that matters this morning. The rest is context.

## Cold start — the baseline

The first response after `/reckon` establishes the **baseline**: a position fix across every project this session touches. A session touches a project if it changed cwd there, ran bash against its paths, or operated its worktree. Multiple worktrees of one repository are one project; distinct repositories are distinct projects, each gets its own block.

Each block leads with the next action — not context, not a plan. The action.

```
## <project> (<path>)
下一步: <inferred from session intent + MR blockers + todo state>
分支: <branch> (worktree: <-suffix>) · 未推送 N commits · 工作区<干净/脏>
MR: <!n> <open/merged> (<阻塞说明>) · ...
map: <#n> → frontier <#x,#y> (N open)   ← 仅有 wayfinder map 时
上一 session: <compaction 意图摘要>       ← 仅有近期 session 时
```

**下一步** is the most valuable field and the hardest to read — infer it from the session's last compaction summary (what was I about to do), the MR blockers (what is gating me), and the todo list's last state. If no clear next action exists, say so: "无明确下一步，需确认方向". Guessing here manufactures a position you do not have.

Cross-repository dependencies — one MR waiting on another repo's MR — are described in prose within the relevant block, inferred from session context. If the context reveals a dependency, state it: "MR !9 阻塞于 HAMi MR !2".

The `map:` line is mandatory, not optional-when-convenient. A project with an open wayfinder map always gets the line — query the tracker (`glab issue list --label wayfinder:map` / `gh issue list --label wayfinder:map`) as part of the baseline, do not skip it because the session did not recently touch the map. A project with no open map gets no line; a project with a closed map gets no line. Writing `map: 无 open wayfinder map` is the same error as omitting the line for a project that has one — silence is the correct expression of "no map here", a line is not. Omitting the line for a project that has an open map is a position error — the frontier is part of where you stand.

The frontier has a limbo state the label query misses: tickets whose code is complete but will close only when a referencing MR merges (`Closes #n` in the commit message). These are open, not frontier (not takeable now), not closed. When the map line would otherwise show `frontier 0 open` but open tickets exist, check whether they are pending MR-merge closure — if so, name them: `map: #108 → #109-#113 pending !25 merge`. A zero-frontier result from a label query is a query-method signal, not proof the map is done.

When a project's working tree holds changes this session did not make — files from a parallel session, stale untracked research, another agent's in-flight work — flag them with the `⚠️` prefix, not as generic dirty workspace: `⚠️ <project> 有非本 session 改动: <files>`. A bare "工作区脏" line that happens to list foreign files is not the alert — the `⚠️` prefix and the explicit "非本 session" framing are what keep foreign changes from being mistaken for this session's position. Do not act on them; name them. Session-scoped means the baseline fixes *this* session's position, and foreign changes are noise in that fix.

Data sources are pure reconstruction — no handoff file, no second source of truth:

- **git** (local state truth): branch, unpushed commits, working tree. Worktrees resolved via `git rev-parse --git-common-dir` to the shared repository root.
- **glab / gh** (MR and wayfinder truth): open MRs, merge status, wayfinder map frontier query.
- **session JSONL compaction** (intent truth): the last-known "what was I doing".

## In-session rules

### 1. Refresh on change, not every turn

The baseline is established once. After that, restate position only when the current turn produced a state change — a commit landed, a file was edited, the cwd moved, a todo item updated. Pure question-and-answer turns (a lookup, a clarification) do not trigger a restate. The restate is one line for the active project:

`[<project> · <branch> · step <n>/<m>] 下一步: <action>`

If other projects this session touches have items needing attention (an MR awaiting merge, unpushed commits), append one line:

`另有: <project> <!n> 待合并, <project> N 未推送`

No attention items — no appended line. Clean state is silent.

### 2. Milestone restate on objective signals

When an objective signal fires — a todo item completed, a wayfinder ticket closed (`Closes #n`), a commit landed, an MR merged — output the full **milestone restate**, not the one-liner. The milestone restate is three:

- **刚完成**: what now works, in concrete terms. Make the win visible — "Login now works with magic links", not "auth changes done".
- **下一步**: the single next action, doable now.
- **当前阻塞**: open MRs and their blockers, if any.

This is the checkpoint. It lives in the conversation only — do not write it to the todo tool. The todo tool is unreliable (agents forget to update it); the conversation plus compaction is the record. Rule 1's change-driven restate, running on every turn that moves work, is the safety net that carries the position forward between milestones.

### 3. Anchor on project or worktree switch

When the cwd changes to a different project, or a bash command operates on a different repository's paths, the switch is the moment position is most likely lost. Append one anchor line before continuing the work:

`→ 切到 <project> · <branch> · 还有 N 个待合并 MR`

### 4. Re-establish baseline after compaction

If the turn begins and the context feels truncated — recent turns are missing, the baseline is gone — a compaction just happened. Re-run the cold start: output the full baseline across all projects the session touches. Compaction loss only costs the position since the last change; rule 1's restate fills the rest back in.
