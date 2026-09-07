---
name: diag-extract
description: Mine historical pi sessions for diagnosing-bugs runs and persist each finished diagnosis into the ~/ops vault via diag-write. Use when backfilling the vault from session history, or when the user asks to 挖掘/提取 historical diagnoses from past sessions.
---

# Diag Extract

Harvest finished diagnoses from session history into the vault. Two passes: a dry-run that lists every candidate with a verdict, then extraction one session at a time through `/skill:diag-write`.

## Step 1 — Discover candidates

The invocation marker is the **skill injection**, not the string `skill:diagnosing-bugs` — that string appears inside other skills' injected bodies and produces false positives by the dozen:

```bash
rg -l '<skill name=\\"diagnosing-bugs\\"' ~/.pi/agent/sessions --glob '*.jsonl'
```

Note the backslash-escaped quotes: the injection lives inside a JSON string. Include subagent fork sessions (they carry the marker too when the diagnosis ran in a child).

## Step 2 — Dry-run: triage every candidate

For each candidate, read the session's entries and assign a verdict — **no vault writes in this pass**:

- **Extract** — finished: a fix applied and verified, or an explicit root-cause conclusion in the closing assistant messages (Phase 5/6 material present)
- **Skip: no conclusion** — the diagnosis ran but never closed; note how far it got
- **Skip: meta** — the session is about the diag tooling itself (building the vault or the skills)
- **Extract, degraded** — early phases hidden behind a compaction summary: the summary usually preserves symptom + root cause; extract what survives and mark the missing sections 未记录

Present the full list — session path, one-line subject, verdict, reason — and get the user's confirmation on the extract set. A day of retries on one bug yields many sessions; that is expected, the dedup in the next step absorbs it.

## Step 3 — Reconstruct and write, one session at a time

Per confirmed session, gather from the entries:

- **Symptom** — the user's statement at or after the injection point, quoted
- **Trail** — feedback-loop commands and their red/green outputs (tool calls + results), the surviving hypothesis and the fix (closing assistant messages)
- **Environment** — from the session's cwd and any version commands shown; 未记录 where absent

Then run `/skill:diag-write` per diagnosis. Its find-or-create step is the dedup: multiple sessions on one issue produce one entry, updated in place.

## Done when

- [ ] Every candidate from the dry-run list carries a verdict (extracted / skipped with reason)
- [ ] Every extracted entry satisfies diag-write's done-when
- [ ] Sessions on the same issue converged into a single vault entry
