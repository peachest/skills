---
name: fusion-search
description: Two-lane web search with fusion and LLM rerank — anysearch + DeepSeek Search recalled in parallel, deduped, RRF-fused, then judge-model reranked to top-k. Use for report-grade deep research, 深度检索/融合检索, cross-checking a suspicious single-engine result, or cheap batch search pipelines (measured +0.4 relevance over the best single lane). Plain anysearch stays the default for quick interactive lookups — fusion costs ~10s per query.
---

# fusion-search

Two search engines disagree more than they overlap: measured top-10 overlap is ~5%,
and which engine wins rotates with query type. This skill runs both lanes, merges,
and lets a judge model rerank — one call, three uses (reranker, fusion order, and
the relevance scores every consumer reads).

## Quick start

```bash
# single query -> fused top-5 (human summary on stdout, full JSON at --out)
DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY uv run --project <SKILL_DIR> \
  python scripts/fusion_search.py "query" --out ~/tmp/fusion-out.json

# batch: one query per line, one JSON per query
DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY uv run --project <SKILL_DIR> \
  python scripts/fusion_search.py --batch queries.txt --out-dir ~/tmp/fusion-batch/
```

Done when stdout prints the fused top-k with per-doc source tags (`A`/`D`/`both`)
and the JSON path exists — parse the JSON, not stdout.

## When fusion earns its cost

- **Report-grade research**: agent writing a report, comparing approaches, or answering where a wrong top-1 poisons everything downstream.
- **Cross-check**: a single-engine result looks off (off-topic hits, empty lane, suspected anti-bot noise) — run fusion and read the `both` tags.
- **Batch pipelines**: ¥0.005/search-lane + free judge rerank; acceptable for automated data collection.

Quick lookups, "what is X", anything where anysearch already answered — stay on plain anysearch.

## Output contract

JSON at `--out` / `--out-dir/<slug>.json`:

- `query`, `lanes`: per-lane `{ok, latency, n, err}` — read these before trusting results
- `top`: fused top-k, each `{title, url, src, both, rrf, llm, ds_score}`
  — `llm` is the judge relevance score 0–3 (3 = directly answers); `both: true` means both engines returned this URL (strong signal)
- `rel`: `{fused, anysearch, deepseek}` mean judge scores per top-5 — fusion should never lose to the best single lane; if it does, treat the query as anomalous

Exit codes: **0** both lanes ok · **2** one lane failed (results still produced, `degraded: true` in JSON) · **3** nothing usable.

## Judge model

The judge is any OpenAI-compatible chat endpoint, configured in `<SKILL_DIR>/runtime.conf`
(see `runtime.conf.example`; the default in there is a placeholder — a real internal
gateway IP must never be tracked). Reasoning-capable models need the effort-lowering
extra body from the example. The judge doubles as the only relevance measure in the
output; a different judge changes the numbers, not the ranking method.

## Setup on a new node

```bash
bash scripts/check-env.sh   # FAIL lines are the install instructions
```

Requires: `DEEPSEEK_API_KEY` in the environment, a reachable judge endpoint in
`runtime.conf`, and the sibling anysearch skill installed
(`~/.agents/skills/anysearch/scripts/anysearch_cli.py`; if its lane comes back
empty with "No such file", the anysearch skill is the thing to fix).

## Failure semantics

Each lane retries with backoff; a lane that stays empty degrades the run (exit 2)
instead of failing it — single-lane output is still fused and scored. Both lanes
empty on the same query is usually a local transient (network, proxy), not an
engine problem: retry once before diagnosing.
