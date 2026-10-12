# ocr — Skill Impact Log

| Date | Proposal | Landing | Commit | Verification |
|------|----------|---------|--------|--------------|
| 2026-10-12 | pi-memory global audit: sediment 4 GENERAL lessons into ocr skill — ① review background must carry architecture knowledge + concrete review checklist (never generic "review for bugs") ② every LLM finding verified against source before reporting (hallucinated / stale / mislocated) ③ full scan: `--no-plan --no-summary` saves ~30% time ④ fixed output contract `--format json` + `--audience agent`. | in-progress/ocr/SKILL.md: ch3 `-b` row + new `--format json` parameter rule + canonical invocation, ch5 verification bullet, ch6 scan flags | (this commit) | no tests in skill dir (exempt); sanitize-check clean on changed files |
