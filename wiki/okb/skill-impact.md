# okb — Skill Impact Log

| Date | Proposal | Landing | Commit | Verification |
|------|----------|---------|--------|--------------|
| 2026-09-12 | Learn from nashsu/llm_wiki (Karpathy LLM Wiki pattern): ① split distill into route→write two passes ② silver notes link each other via Markdown hyperlinks (not `[[wikilink]]`), one-hop traversal at query ③ computable topology audit in Status (isolated / thinly linked / unlinked source-overlap pairs) ④ append-only `log.md` op record. NOT adopted (deliberate): purpose.md, Louvain/community clustering, vector search/LanceDB, cascade deletion, desktop features — overkill at OKB's scale; gold layer & 4-hop evidence chain stay as OKB's differentiators. | in-progress/okb/SKILL.md: Directory layout (log.md), Curation steps 2/4/5 | e776bde | no test suite in skill dir (exempt); full-file re-read after edit for coherence |
