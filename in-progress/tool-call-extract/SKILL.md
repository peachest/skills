---
name: tool-call-extract
description: "Retrieve pi sessions containing calls of a given tool — filterable by args substring (e.g. 'glab api' inside bash commands) and errors-only — with per-session match/error stats, and dump paired toolCall-args + toolResult-text records for one session. Use when the user asks to 找出/检索 which sessions called or failed calling a tool (subagent workflowScript failures, bash glab api errors), before /skill:tool-call-diagnose needs a trace, or for any audit over session logs by tool call."
---

# Tool Call Extract

**Leading word:** the **calls dump** — one paired record per matching call (`call_entry` → `result_entry`, full args, result text, `is_error`). The compact map of a multi-MB session log's tool usage; build it once, the diagnose skill's axis sub-agents read the dump plus the trace index, never the raw jsonl.

Two modes:

1. **Search** — across all sessions: `<tool-name>` + optional `--args-contains` + optional `--errors-only`. Per match: counts, sample error texts, whether the last call still failed.
2. **Dump** — one session file: the paired records above, args clipped to 4000 chars by default (`--full-args` for the whole thing).

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
