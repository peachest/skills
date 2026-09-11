# Baseline reference

Detail behind the cold-start rules in SKILL.md. Read when building a baseline or a diff; not needed between restates.

## Block template (full)

```
## <project> (<path>)
下一步: <inferred from session intent + MR blockers + todo state>
分支: <branch> (worktree: <-suffix>) · 未推送 N commits · 工作区<干净/脏>
MR: <!n> <open/merged> (<阻塞说明>) · ...
map: <#n> → frontier <#x,#y> (N open)   ← 仅有 open wayfinder map 时
上一 session: <compaction 意图摘要>       ← 仅有近期 session 时
```

**下一步** is the most valuable field and the hardest to read — infer it from the session's last compaction summary (what was I about to do), the MR blockers (what is gating me), and the todo list's last state. If no clear next action exists, say so: "无明确下一步，需确认方向". Guessing here manufactures a position you do not have.

## map: line and the limbo

Run `frontier.sh` (or `glab issue list --label wayfinder:map` / `gh issue list --label wayfinder:map`) per project, then follow its result — an open map produces its line; an empty result moves you straight on to the next data source. A written `map: 无 open wayfinder map` is a position error in both directions.

The frontier has a limbo state the label query misses: tickets whose code is complete but will close only when a referencing MR merges (`Closes #n`). These are open, not frontier (not takeable now), not closed. `frontier.sh` names them in its `pending:` field — carry that into the map line: `map: #108 → #109-#113 pending !25 merge`. A zero-frontier result is a query-method signal, not proof the map is done.

## Foreign changes

When a project's working tree holds changes this session did not make — files from a parallel session, stale untracked research, another agent's in-flight work — flag them with the `⚠️` prefix, not as generic dirty workspace: `⚠️ <project> 有非本 session 改动: <files>`. The `⚠️` prefix and the explicit "非本 session" framing are what keep foreign changes from being mistaken for this session's position. Do not act on them; name them.

## Collection scripts

Three scripts in the skill's `scripts/` dir; call them instead of hand-writing bash:

- `position.sh [repo...]` (**git truth**): one TSV line per worktree — `path|branch|upstream|ahead|dirty|untracked|last-commit`. One call covers every worktree of the repo, resolves the upstream chain (`@{u}` → `origin/<default>` → `internal/<default>`), and uses `/usr/bin/git` (PATH git may be wrapped).
- `mr-state.sh <repo> [--iid N]` (**MR truth**): open MRs or one MR — `iid|branch|state|merge_status|sha|title|url|blocking`, where `blocking` extracts a `Depends on !N` mention from the description. Derives the GitLab host from the remote (multi-instance safe), `glab api` only.
- `frontier.sh <repo>` (**wayfinder truth**): one line per open map — open tickets plus the pending limbo. Empty output is the no-map case; move on silently.
- **session JSONL compaction** (**intent truth**): the last-known "what was I doing" — read from the compaction summary in context.

GitHub-hosted repos use the `gh` equivalents (`gh pr list`, `gh issue list --label wayfinder:map`).

## Milestone restate detail (rule 2)

- **刚完成**: what now works, in concrete terms. Make the win visible — "Login now works with magic links", not "auth changes done".
- **下一步**: the single next action, doable now.
- **当前阻塞**: open MRs and their blockers, if any.

The checkpoint lives in the conversation only — do not write it to the todo tool. The todo tool is unreliable (agents forget to update it); the conversation plus compaction is the record.
