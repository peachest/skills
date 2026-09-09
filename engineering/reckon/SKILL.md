---
name: reckon
description: "Recover your position after time away — dead-reckon current progress across every project this session touches. Invoke with /reckon; stays on until \"stop reckon\". Use when position is lost: returning after a break, resuming a session, or losing track of which project/branch/MR you are on."
disable-model-invocation: true
---

# reckon

After time away your exact position is lost. **Reckoning** recovers it the way dead reckoning does: from the last known fix (what the session remembers) plus the distance traveled since (what git and the tracker record). Orient reads terrain (what is here); reckon reads the wake you left (where did I get to).

## Persistence

These rules apply to every response for the rest of the session. Turn them off only when the reader says "stop reckon" or "normal mode"; confirm in one line and return to your default behavior.

Pi `--resume` carries the session forward; compaction's Constraints section preserves the activation. A fresh session starts clean — reckon is opt-in.

## Cold start

**Query, never recall.** An injection of reckon is a query trigger. Every invocation re-collects state from the live sources — answering from session memory is a position error: memory holds where you were, the sources hold where you are. Collection is one script call per project (`scripts/position.sh`, `mr-state.sh`, `frontier.sh` — interfaces in [`references/baseline.md`](references/baseline.md)); there is no expensive shortcut to save.

How much to emit rides on one binary test: **is the last position statement (baseline or restate) still present in the context above?**

- **Absent** — first invocation, or compaction took it (a compaction summary sits in context, or recent turns are missing): establish the full **baseline**.
- **Present**: the queries are still mandatory; the re-emission is not. Queries confirm nothing moved → one line, `位置未变（已复核）`. Queries show a change → emit only the diff.

A session touches a project if it changed cwd there, ran bash against its paths, or operated its worktree. Multiple worktrees of one repository are one project; distinct repositories are distinct projects, each gets its own block. Block template, `map:`/limbo rules, foreign-change alerts (`⚠️`), and script interfaces: [`references/baseline.md`](references/baseline.md).

Each block leads with the next action — not context, not a plan. The action. If no clear next action exists, say so; guessing manufactures a position you do not have.

Cross-repository dependencies — one MR waiting on another repo's MR — are stated in prose within the relevant block: "MR !9 阻塞于 HAMi MR !2".

## In-session rules

### 1. Refresh on change, not every turn

Restate position only when the current turn produced a state change — a commit landed, a file was edited, the cwd moved, a todo item updated. Pure question-and-answer turns do not restate. The restate is one line for the active project:

`[<project> · <branch> · <状态描述符>] 下一步: <action>`

The status descriptor is what the work actually shows — tip sha, MR state, the current task phrase: `[hami · MR !14 open + CI 监控中 · wiring 完成]`.

If other projects this session touches have items needing attention (an MR awaiting merge, unpushed commits), append one line: `另有: <project> <!n> 待合并, <project> N 未推送`. No attention items — no appended line.

### 2. Milestone restate on objective signals

An objective signal fired — a todo item completed, a wayfinder ticket closed (`Closes #n`), a commit landed, an MR merged — output the full **milestone restate** (刚完成 / 下一步 / 当前阻塞 — format in [`references/baseline.md`](references/baseline.md)), not the one-liner. It lives in the conversation only; rule 1's change-driven restate is the safety net between milestones.

### 3. Anchor on project or worktree switch

The cwd moved to a different project, or a bash command operated on another repository's paths — the moment position is most likely lost. Append one anchor line carrying the project, its branch, and the open-MR count:

`→ 切到 <project> · <branch> · 还有 N 个待合并 MR`
