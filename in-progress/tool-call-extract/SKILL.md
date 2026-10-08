---
name: tool-call-extract
description: "Retrieve pi sessions containing calls of a given tool — filterable by args substring (e.g. 'glab api' inside bash commands) and errors-only — with per-session match/error stats, and dump paired toolCall-args + toolResult-text records for one session. Also: doc-usage mode — did the agent actually consume project docs (read-like vs write-like vs mention matrix, escape-rate check, content-echo verification). Use when the user asks to 找出/检索 which sessions called or failed calling a tool (subagent workflowScript failures, bash glab api errors), before /skill:tool-call-diagnose needs a trace, for any audit over session logs by tool call — or asks 某文档 agent 有没有真的在用 / doc usage / 文档消费统计."
---

# Tool Call Extract

**Leading word:** the **calls dump** — one paired record per matching call (`call_entry` → `result_entry`, full args, result text, `is_error`). The compact map of a multi-MB session log's tool usage; build it once, the diagnose skill's axis sub-agents read the dump plus the trace index, never the raw jsonl.

Two modes:

1. **Search** — across all sessions: `<tool-name>` + optional `--args-contains` + optional `--errors-only`. Per match: counts, sample error texts, whether the last call still failed.
2. **Dump** — one session file: the paired records above, args clipped to 4000 chars by default (`--full-args` for the whole thing).
3. **Doc-usage matrix** — which project docs does the agent actually consume, vs which are only maintained (`scripts/doc-usage.py`, below).

## Doc-usage mode: did the agent really consume these docs?

Trigger phrases: 某文档有没有真的被用 / doc consumption / 文档消费统计 / fake-useful docs. Never answer this by counting `read` tool calls alone — proven pitfalls:

- **bash cat/grep outnumbers the read tool ~40:1** in real projects (measured: bash 6413 vs read 170 in one 127-session project). Read-only counts are meaningless.
- **Write ≠ read.** A doc written 30× and read 0× is sediment, not value. Classify every hit as READ-like / WRITE-like / MENTION and report both sides.
- **Agents fall back to python one-liners to edit files when `edit` fails** (`python3 -c "...open('f','w').write(src.replace(...))"`) — these are WRITE-like, not read; likewise heredocs (`cat > f <<EOF`) and `sed -i`.
- **Nested session files exist** (`<session>/forks/*.jsonl`, `<session>/<uuid>/run-0/session.jsonl`) — a top-level `*.jsonl` glob misses entire sub-agent populations.
- **A read call is weak evidence.** Verification that content was consumed uses an evidence ladder (below).

### Usage

```bash
# matrix: per-target READ/WRITE/MENTION + verdict. Targets via TSV (name\tpattern)
# or inline comma list. Scan is recursive (forks/run-0 included).
python3 scripts/doc-usage.py matrix --sessions-dir <dir> --patterns 'CONTEXT.md,gpu-ledger'
python3 scripts/doc-usage.py matrix --sessions-dir <dir> --targets targets.tsv

# escape-rate: sessions doing the ACTION (signature regex) without touching ANY target —
# the contrapositive of compliance: 'held GPU but never booked the ledger'
python3 scripts/doc-usage.py matrix ... --escape 'nvidia-smi|torchrun' --escape-min 3

# echo verification: does assistant text/thinking AFTER a read-like touch echo
# distinctive tokens from the doc on disk? Strongest cheap consumption evidence.
python3 scripts/doc-usage.py echo --doc /proj/docs/RULES.md \
  --sessions-dir <dir> --target 'RULES.md' [--json]
```

`read+res` counts read-like calls whose toolResult was non-empty — a read that returned nothing consumed nothing. Echo anchors on the **first read-like event** per session; a write-only session echoing its own content is excluded (`sessions_touch_but_no_read` reports how many were skipped this way).

### Evidence ladder (strongest last)

1. **Touch** — target substring in any tool args (weak: could be mention or maintenance)
2. **Read-like with result** — read/bash-classified call whose result was non-empty
3. **Echo** — assistant text/thinking after a read-like event contains distinctive doc tokens (`doc-usage.py echo`)
4. **Action follows rules** — project-specific; the escape check tests its contrapositive

Verdicts in matrix output: `consumed` (≥3 reads), `weak-read`, `only-maintained (fake-useful)` (writes with zero reads — deletion candidates), `never-touched`. Present the matrix, then drill into `only-maintained` targets with `echo` before recommending deletion — a doc can be genuinely consumed via bash reads the matrix still classifies correctly, but a zero-echo zero-read doc is safe to flag.

## Process

### 1. Resolve inputs

Tool name as it appears in tool definitions (`bash`, `subagent`, `edit`, ...). A user symptom like "glab api 经常失败" resolves to `bash --args-contains 'glab api'`; "subagent workflowScript 挂了" resolves to `subagent --errors-only` (optionally narrowed with `--args-contains workflowScript`). Neither tool name nor session given → ask; do not guess.

### 2. Search

```bash
python3 scripts/find-tool-calls.py <tool> [--args-contains SUBSTR] [--errors-only]
```

Failures are `toolResult` messages with `isError: true`; a call whose result never arrived (session cut short) is not an error. Malformed JSONL lines are skipped, never abort the scan. Zero matches → report and stop; suggest loosening the filter (`--errors-only` off, substring dropped) before concluding absence.

### 3. Present the triage list

Per match: file path, timestamps, tool total calls, matched calls/errors, sample error texts, `last_match_error`, `likely_running`. Selection guidance when the user defers: the session with the most matched errors that is **finished** (`likely_running: false`); among equals, the most recent. A day of retries yields many sessions with the same failure — expected; the consumer diagnoses the fullest one and cites the rest as corroboration.

**Done when**: exactly one session file chosen and stated (or an explicit empty result).

### 4. Build the calls dump

```bash
python3 scripts/find-tool-calls.py --dump <session-file> --tool <tool> \
  [--args-contains SUBSTR] [--errors-only] [--full-args] > calls.json
```

For diagnosing *how the agent used* the tool, run a second dump without `--errors-only` — successes and fallback workarounds are evidence too; produce both when in doubt.

**Done when**: the dump file exists with the expected `matched_calls` count.

## Deliverable contract

The consumer (typically `/skill:tool-call-diagnose`) receives:

1. The **session file** path — the raw trace
2. The **calls dump** path(s) — paired call/result records
3. Per-session stats from the triage list (counts feed scope estimates)

For the surrounding-turn map (what the agent did between calls), the consumer builds a trace index with the extract skill's sibling: `python3 ~/.pi/agent/skills/skill-call-extract/scripts/find-skill-sessions.py --index <session-file> > trace-index.json`.

`references/session-jsonl.md` is the format primer (entry structure, toolCall/toolResult shapes, usage fields) — consumers reading the raw trace should read it too.

## Done when

- [ ] Every match presented with verdict (chosen / skipped with reason)
- [ ] Chosen session file stated
- [ ] Calls dump built and its path stated (plus the no-filter dump if run)
- [ ] Doc-usage runs: matrix presented; every `only-maintained` target double-checked with `echo` before a deletion recommendation; escape-rate run when the doc encodes an action rule
