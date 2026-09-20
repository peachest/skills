# en rules (machine-auditable subset)

Source: ASD-STE100 mechanical rules (sentence caps, punctuation, modals) plus the slop habits from "The cure for AI slop is a 1986 aircraft manual" (Vusal Ismayilov). The 900-word approved-dictionary is deliberately excluded — measured on a technical wiki, dictionary checks were 87% of hits and mostly noise; full-STE is reserved for `strict` mode via the installed `ste100` skill's `ste_checker.py`.

**Rewrite contract**: unmatched sentences stay verbatim; a hit is a flag awaiting adjudication — load-bearing stays, decorative gets a minimal fix.

## Machine-checked (audit.py EN-*)

| id | name | trigger | fix | adjudication notes |
|----|------|---------|-----|--------------------|
| EN-1 | sentence >25 words (flavor) / >20 (strict) | computed per sentence | split at the natural joint; one idea per sentence | STE rule 6.3/5.1 hard caps; code spans and headings excluded from word counts |
| EN-2 | semicolon | `;` | period or comma | STE 8.1 bans outright; no adjudication — always fix |
| EN-3 | ambiguous modal | `may` / `might` | permission → `must`; ability → `can`; uncertainty → restate the fact | the STE modal ban: may is ambiguous between permission/ability/prediction |
| EN-4 | marketing adjective | seamless/robust/powerful/cutting-edge/effortless/enterprise-grade/game-changing/revolutionary/best-in-class/world-class | claim → demonstrate: state what it does, with the number or mechanism | dictionary-locked in STE; in prose, keep only where the claim is shown in the same sentence |
| EN-5 | chatty phrasal verb | spin up / reach out / dive into / delve into / kick off / touch base / leverage | use the plain verb (start, contact, examine, begin, use) | STE 9.3 spirit: one verb for the action |
| EN-6 | nominalized verb | perform an analysis (of) / provide assistance / make a decision / make use of / conduct a review of | restore the verb: analyze, assist, decide, use, review | STE 3.7: "perform an analysis" is illegal, "analyze" is the law |
| EN-7 | em-dash | — / – | complete sentence, or comma/period | adjudicate each: reveal-dashes get fixed, appositive/definition dashes stay with a recorded retained-example |

## Human-only

- **Synonym rotation** (slop habit #1): one thing named three ways in a passage (user/customer/client). Approximate detection is high-noise; adjudicate by reading. Fix: one name per thing (STE 1.11).
- **Run-on stitching** beyond the length cap: 4 ideas joined by dashes/semicolons that should be 4 sentences. EN-1/EN-2 catch most; the rest is a read judgment.
- **Conservation boundary**: quotes, numbers, hedges (may/might/possibly/perhaps/usually), and structure must survive. Machine gate: `python3 <SKILL_DIR>/scripts/conservation.py orig.md new.md`.

## strict mode addition

For procedures, error messages, and agent output: if the `ste100` skill is installed, also run its checker (`python3 ~/.pi/agent/skills/ste100/scripts/ste_checker.py --file <f> --type procedure`) and treat its rule hits as flags under the same adjudication contract. Without it, EN-1..EN-7 are the full strict surface — the subset already covers the cap/punctuation/modal rules; only the 900-word dictionary lock is lost.
