---
name: skill-call-extract
description: "Retrieve pi sessions that invoked a given skill, with per-session stats (tool histogram, token usage, run state) and a compact per-entry trace index. Search by skill name via the skill-injection marker, or resolve an explicit session id. Use when the user asks to 找出/检索/列出 which sessions called a skill, before /skill:skill-call-diagnose needs a trace, or for any backfill/audit over session logs by skill."
---

# Skill Call Extract

**Leading word:** the **trace index** — one line per session entry (role, tool calls with arg sizes, result sizes, per-turn usage). The compact map of a multi-MB session log; build it once, navigate the raw file only where it points.

Two retrieval modes:

1. **By skill name** — two signals, either qualifies a session:
   - the **skill-injection marker** (automatic trigger), or
   - a **read-load**: a `read` tool call whose path argument ends in `/<name>/SKILL.md` (the agent manually loaded the contract — the marker cannot see this; matches both the installed layout and source checkouts)
2. **By session id** — resolve an id the user already has (reports even without either signal; the user already knows it ran the skill)

## Process

### 1. Resolve inputs

Skill name (as written in its SKILL.md frontmatter) for marker mode; session id or filename prefix for direct mode. Both given → id mode, but record the marker count anyway. Neither → ask; do not guess a skill name.

### 2. Search

```bash
python3 scripts/find-skill-sessions.py <skill-name>                  # marker search
python3 scripts/find-skill-sessions.py <skill-name> --session <id>   # explicit id
```

The marker is the **skill injection tag** (`<skill name=\"NAME\"` in the raw JSONL — backslash-escaped quotes), never the string `skill:<name>`: that string appears inside other skills' injected bodies and false-positives by the dozen. Subagent fork sessions carry the marker too — include them.

The read-load signal parses actual `toolCall` entries (name `read`), so a session that merely mentions the path in prose does not match. `selected_via` reports which signal(s) hit: `marker` / `read` / `marker+read` / `explicit-id`.

### 3. Present the triage list

Per match: file path, first/last timestamp, entries, message counts, tool-call histogram, usage totals (`input`/`output`/`cacheRead`), marker/read counts, `likely_running`. Zero matches → report and stop.

Selection guidance when the user defers: default to the longest **finished** run (most entries, closing assistant summary, `likely_running: false`). A day of retries yields many sessions on one skill — that is expected; the consumer diagnoses the fullest one and cites the rest as corroboration.

**Done when**: exactly one trace file chosen and stated (or an explicit empty result).

### 4. Build the trace index

```bash
python3 scripts/find-skill-sessions.py --index <trace-file> > trace-index.json
```

**Done when**: the trace index exists as a file, with `truncated: false` (or the truncation noted — cap 600 entries).

## Deliverable contract

The consumer (typically `/skill:skill-call-diagnose`) receives:

1. The **trace file** path — the raw session jsonl
2. The **trace index** path — the per-entry map
3. Per-session stats from the triage list (usage totals feed cost estimates)

`references/session-jsonl.md` is the format primer (entry structure, marker, usage fields) — consumers reading the raw trace should read it too.

## Done when

- [ ] Every match presented with verdict (chosen / skipped with reason)
- [ ] Chosen trace file stated
- [ ] Trace index built and its path stated
