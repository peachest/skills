# teach skill-impact

| Date | Proposal | Landing | Commit | Verification |
|------|----------|---------|--------|--------------|
| 2026-09-24 | KaTeX dependency completeness check in css-self-check (math delimiters in prose but head missing bundle → FAIL with exact lines to add); wider CHECK_PAT vocabulary in beat-check (先问自己/自问/问自己/先问/试着回答) | in-progress/teach/assets/css-self-check.py (has_math/katex_missing + KATEX_ASSETS), assets/beat-check.py (CHECK_PAT + 口径注释), SKILL.md CSS Self-Check section, tests +9 cases | d5d35b4 | uv run pytest → 39 passed; real-world: lessons/0005-eagle2.html (post-fix) passes, sed-stripped head correctly FAILs listing all 4 files |
