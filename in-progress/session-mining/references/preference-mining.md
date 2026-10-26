# Preference Mining

Turn recurring user working preferences into durable rules — an AGENTS.md
preference section or `memory_remember` entries. The signal taxonomy and
evidence discipline are ported from the pstack `automate-me` skill (Step 1 +
Guardrails); its Cursor-bound output (a personal `-mode` skill) does not
travel — this repo routes the output to AGENTS.md / memory instead.

## The six signal classes

Hunt user messages and tool behavior for these; each line names its
observable trace in pi session JSONL (`references/session-jsonl.md` primer
first if raw):

1. **Response preferences** — length, tone, format, "explain it plainly"
   corrections. Trace: user-role entries reshaping output (「太长」「说人话」
   「用表格」), or the same question resubmitted after a rejected answer shape.
2. **Delegation habits** — what goes to subagents, which models, parallelism.
   Trace: `subagent`/`bg_delegate`/`herdr_send` toolCall patterns, fanout
   shapes, model fields.
3. **Verification posture** — what "done" means. Trace: toolCalls after a
   completion claim (pytest/build/live repro), review-skill invocations, user
   pushback like 「你没测就报完成」.
4. **Code and prose discipline** — style, cited principles, lint/format tools.
   Trace: user corrections citing style rules, repeated format/lint toolCalls,
   rejected-approach patterns across tasks.
5. **Process conventions** — worktrees, commits, PRs/MRs, review tooling.
   Trace: bash toolCall commit-message shapes, `wt`/branch patterns, skill
   routed vs bare `glab`/`git push` calls.
6. **Meta preferences** — fixing skills mid-task, proposing new ones, doc
   upkeep. Trace: user messages naming a skill followed by edits under the
   skills repo / wiki.

## Evidence discipline

- **Workspace scoping first**: mine only the workspace's session bucket
  (`~/.pi/agent/sessions/--<slug>--/`), never glob across projects — that
  reads unrelated private chats and cross-pollutes preferences. Attribute
  mined signals by the `cwd` field, not bucket name (resumed sessions lie).
- **Slice cross-check**: split the window into 3+ slices (one fresh lane per
  slice, skeleton step 5); a signal seen in **2+ slices** elevates. A lone
  signal is weak — usually dropped.
- **Overfit guard**: a preference stated once and contradicted another time
  is noise. Require multiple instances before codifying.
- **Dual dump for tool-based claims**: when a preference rests on tool usage
  (classes 2/3/5), dump calls with and without `--errors-only` and diff — the
  correction the user gave is often visible in the failed→retried pair.
- **Histogram, never re-read**: aggregate counts with `Counter`/`uniq -c`
  over the dump or pre-filtered lines; return counts + short samples, never
  walk the raw logs again per question. Human-verify counts before reporting.

## Incremental anchor

Re-mining an existing preference corpus mines only what changed since last
solidification: `git log -1 --format=%cI <AGENTS.md-or-doc-path>` for file
landings; a `memory_remember` entry's update time for memory landings. Mine
sessions after that timestamp only. Rerun the same scanner next period
instead of re-deriving (full-corpus recipe).

## Output routing

Pi has no established personal `-mode` skill convention — land findings as:

- **AGENTS.md preference/rules section** — repo-level durable rules the user
  wants every session in that repo to follow.
- **`memory_remember` fact entries** — cross-repo, cross-session preferences.
  Pass the four-question gate before each write (90 天后还成立吗 / 有更权威的
  家吗 / 能从别处推导吗 / 是更新而非新增吗); same topic → search, forget the
  old, write one entry — never multiple versions.

Before codifying anything, confirm with the user via structured questions
(mining misses intent that has not surfaced yet) and check the target skill's
`wiki/*/skill-impact.md` for rejected proposals — a previously rejected
preference needs new evidence, not a re-vote.

## When not to use

- Task-specific preference that mattered once (no cross-session durability).
- Anything derivable from `git log`, project files, or existing AGENTS.md
  text — mining it again is pollution (memory gate Q3).
- No user statements/corrections in the window — absence of signal is a
  result; do not invent preferences from tool noise alone.

(Origin: pstack vendor `automate-me` Step 1 signals + Guardrails, ported
2026-10-26; pi-session adaptation per this skill's skeleton.)
