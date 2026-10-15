# implement-spec — Skill Impact

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-15 | fork vendor implement-spec (upstream 49dd158) into in-progress overlay: rolling review after every merger merge (ocr bg_run on main checkout, full accumulated diff, medium→low effort), findings triaged by severity (critical/high block dependent frontier tickets + fixer; medium/low folded into next implementer task text), final step-7 code-review kept unchanged as cross-ticket consistency backstop. Motivation: frontier implementers copy patterns from merged code, so late single review makes rework multiplicative; large end-of-branch diffs degrade review quality. Rolling shape pre-validated in pi-arena (2026-10-12 review-pipeline decision). | (this commit) | not yet executed in a real spec run; fallback rule documented (ocr failure → read-only reviewer subagent on same diff) |
