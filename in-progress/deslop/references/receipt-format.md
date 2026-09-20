# Worker receipt contract

When a rewrite is dispatched to subagents (batch branch), each worker returns a receipt alongside the rewritten text. The orchestrator cross-checks receipts against the diff; a receipt that disagrees with the diff voids the run.

```json
{
  "section": "05-nemo-rl.md#L120-180",
  "rule_hits": {"ZH-4": 5, "ZH-10a": 1},
  "edits": [
    {"rule": "ZH-4", "line": 127, "action": "fixed",
     "note": "reveal-dash -> comma"},
    {"rule": "ZH-4", "line": 131, "action": "kept",
     "note": "term--definition dash, load-bearing"}
  ],
  "zero_hit_attestation": false
}
```

Rules:

1. `rule_hits` counts every flag the worker found, per rule id — including flags it decided to keep. A worker finding 0 hits in a section the orchestrator's audit flagged is an invalid run (the orchestrator re-checks with `scripts/audit.py`).
2. Every edit in the final diff must map to an `edits` entry, and every `action: fixed` entry must appear in the diff. Unclaimed edits and claimed-but-absent edits both void the receipt.
3. Every `action: kept` entry is a retained example: rule id + line + one-line reason. Retained examples are the deliverable that prevents punctuation-rule collapse — a worker that keeps nothing under a discretionary rule (ZH-4, ZH-5, EN-7, EN-3) must say so explicitly and the orchestrator spot-checks before accepting.
4. `action: fixed` entries carry the rule id they resolve. An edit citing no rule is a contract violation (unmatched text stays verbatim).
5. Balance guard: if punctuation-class rules (ZH-4, ZH-5, ZH-5b, EN-2, EN-7) are >50% of `action: fixed` entries, the run stops for re-adjudication of the content-rule flags before merge.
