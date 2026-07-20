---
description: "Extract verifiable claims from documents, route to rule engines or web search, produce evidence-backed verdicts. Use when user says \"/fact-check\" / \"fact check this\" / \"verify this document\" / \"check this report for accuracy\" / \"are these claims true\"."
---

# Fact-Check

**Leading word:** _claim_ — the unit of verification throughout the pipeline.

Agent follows `references/workflow.md` step by step through 8 phases:

| Phase | Action | Tool |
|-------|--------|------|
| **P0 Init** | git/branch/ledger → run.json, detect subagents | `scripts/init.sh` |
| **P1 Extract** | LLM → locate-claim → check-atomicity → validate loop (max 3) | `scripts/locate-claim.sh`, `scripts/check-atomicity.sh`, `scripts/validate-claims.sh` |
| **P2 Classify** | regex route + LLM fallback for unmatched | `scripts/route-claims.sh` |
| **P3a Rule Engine** | 20+ HTTP verifiers for authority claims | `scripts/rule-engine.sh` |
| **P3b Triage** | alt-provider LLM confidence eval | (LLM) |
| **P4 Checkpoint** 🛑 | user reviews partition before search | `references/checkpoint.md` |
| **P5 Deep Verify** | web search → grade evidence tier | `scripts/grade-evidence.sh` |
| **P6 Write** | report, handoff, ledger, stats, profile-summary | `scripts/generate-report.sh` |
| **P7 Deliver** | summary table + fix options | — |
| **P8 Fix** 🛑 | agent/manual/view, incremental recheck | `scripts/incremental-diff.sh` |

## Invocation

- `/fact-check <path>` — incremental if ledger exists, else full
- `/fact-check <path> --full` — force full re-check
- `/fact-check --status` — cumulative stats from `total-stats.json`

## Task Tracking

8 phases across multiple tools — track progress. If a `todo` / `goal` / task-list tool exists, create one item per phase at the start and tick them off as each completes.

## Subagent Detection

Phase 0 calls `subagent({ action: "list" })`. When available:
- **P1 Extract**: parallel workers (≤4, fresh context)
- **P3b Triage**: alt-model delegate for triage
- **P5 Deep Verify**: web search agents (≤4, fresh context)

## Files

```
~/.pi/agent/skills/fact-check/    # skill (global)
<project>/fact-check/              # per-project
├── run-{datetime}-{branch}/       # report.md, handoff.md, run.json
├── documents/<key>/               # claims.json, ledger.jsonl
└── total-stats.json               # cumulative
```

## References

Load on demand: `references/workflow.md` (phase steps), `references/checkpoint.md` (P4 template), `references/schema.md` (claim schema), `references/regex-rules.json` (routing), `references/verdict-policy.json` (evidence tiers), `prompts/extract-claims.md` (extraction prompt).
