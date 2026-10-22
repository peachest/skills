# Mining Recipes

Hand-mining patterns for questions the scripts cannot express. Each recipe
names its evidence source — a real mining session — so the pitfall lists are
paid-for knowledge, not cautionary decoration.

## Shape clustering (what does command Z look like)

Regex the bash `arguments` for the CLI prefix, group by first ~60 chars,
dedupe with ≤6 samples per group. **Doc-noise filter is mandatory**: lines
quoting SKILL.md/AGENTS.md bodies dominate round one — require live-call
markers (`--command`, `--text `, `| pi\b`) and exclude fenced-quote lines.
Refine the regex once, then stop. (orca spawn-chain mining)

## Single-session dissection (known id)

Retrieval is worth zero — skip it. `find ~/.pi/agent/sessions -name "*<id>*"`
→ `wc -l` / `du -h` → inline python `Counter` over types / bash-command
classes / error families / timeline → confirm structure → fan fresh lanes
(edit / user / source / check / collab) over the same file, reports to
`subagent-artifacts/`. Two-phase beats reading: coarse stats first, lanes
only for the themes the stats surface. (teach dissection)

## Time-window tailing (peer's latest round)

Cross-bucket locate (herdr pane list → bucket grep), then anchor: find the
line index of the last known phrase, print the window after it, `grep -n
<pattern> | cut -c1-120` for a speed pass. Line numbers are 0/1-mixed across
tools — comment the base in the script. extract covers "all sessions"; this
covers "since then". (triage-mr increment)

## Full-corpus semantic mining (no retrieval key)

No script signal exists — write a replayable scanner to `~/tmp/<topic>/`:
glob all buckets, per-file single-line pre-filter, extract the signal class
(first-command rituals, correction words, command bigrams…), attribute by the
**cwd field** (bucket names lie for resumed sessions), human-verify counts
before reporting. Multi-day fan-out: per-repo reports land on disk, worker
counts scale with budget (18 workers / 616 sessions observed). Rerun the same
scanner for the next period instead of re-deriving. (hook-candidate mining)

## Custom-event signature grep

Harness events (guardrails blocks, compaction, approval prompts) appear as
domain strings, not toolCalls — script routes are structurally blind. Grep
the signature (`guardrails:action:blocked`, `tokensBefore`), `grep -rl` for
the file list, then fixate into a small scanner with `--global` mode when the
question recurs. (guardrail-optimizer origin)

## Transcript paging (no-bash contexts)

Subagent transcripts exceed the 50KB single-line read cap. Feel: probe with
`limit: 20`, then step 4–6 lines per read sized to observed line width (~40
reads for a 237-line transcript). `jq -r '.recordType+" / "+(.role//"-")' |
sort | uniq -c` probes structure when bash exists. (researcher-transcript
recovery)

## Recovery-chain diff

For "why does X fail": dump with **and** without `--errors-only`, per failure
session print the full call sequence, diff each failed entry against the
adjacent successful one — the fix (a missing flag, an ordering constraint) is
usually already executed somewhere. Strip business-logic exit≠0 from the
error set by hand. (wt failure history → AGENTS.md rules)

## Monthly baseline

errors-only triage → enumerate → loop `--dump` into `~/tmp/<topic>/` →
attribute every error → write the baseline numbers (N errors / M sessions /
K root causes) into an evidence doc → next month, rerun and diff. Root causes
feed resident rules (AGENTS.md), not the mining report. Same incident in main
session + fork counts once. (subagent 28-error baseline)

## Bucket navigation quickset

`find ~/.pi/agent/sessions -name "*<id>*"` beats guessing buckets ·
`parentSession` first-line field walks cross-bucket lineage · wt-migration =
command timestamp vs filename timestamp · `npm view <pkg> time --json` dates
upstream drift · sqlite read-only queries over `store.db` reach state the
JSONL never held.
