# fetch-article — impact ledger

| date | proposal | landing | verification |
|------|----------|---------|--------------|
| 2026-09-20 | Trace diagnosis over 5 sessions (skill-call-extract, 261-session full scan): two chronic adherence gaps. ① Agents looked for a project-local `.agent/skills/fetch-article/scripts/fetch.py` that does not exist (13 misses / 9 sessions) — `<SKILL_DIR>` is the single global install. ② No timeout guidance: `fetch.py` has no built-in timeout, bilibili downloads exceeded 2 min and got killed by agent-side foreground timeouts (14 hits / 8 sessions). Also confirmed HTTP 412 is a ghost bug (last seen 2026-06 era, before WBI signing + credential landed). | SKILL.md new "Operational Notes" section (unique absolute path + background-task ≥600s for videos >30 min) | SKILL.md doc-only change; no scripts touched. |
