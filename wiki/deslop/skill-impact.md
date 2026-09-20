# deslop — impact ledger

| date | proposal | landing | verification |
|------|----------|---------|--------------|
| 2026-09-18 | Initial skill: bilingual (zh/en) AI-slop audit+fix. Design inputs: lieflat corpus-validated zh rules (regex shared with its check-translationese.py), ASD-STE100 mechanical subset for en (no 900-word dictionary — measured 87% noise on a technical wiki), teach dash-density calibration (25/100 lines). Failure-mode-driven: audit-first verdict floor (prevents wasted dispatches), per-rule hit receipts (prevents no-op workers), conservation machine gate + balance guard (prevents punctuation-rule collapse diagnosed in wiki/lieflat-less-ai-tone P-001/P-002). | in-progress/deslop/ | uv run pytest 20 passed; smoke on 3 real docs (en silver note: 12 hits/15 sentences incl. semicolons+caps; zh transcript: 24 hits/213 sentences, dash 18.8<25; conservation correctly FAILs on deleted 1986×3) |
