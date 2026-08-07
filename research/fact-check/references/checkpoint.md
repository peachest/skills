# Review Checkpoint Template (Phase 4, DD-05)

Agent displays this template after Phase 3b triage, before Phase 5 deep verify.

## Display Template

```
🛑 Review Checkpoint — run-{datetime}-{branch}
   {N} claims extracted, {M} verified, {K} remaining

┌──────────────────────────────────────────────────────┐
│ [Rule Engine Verified]  {N1} claims                  │
│   Verdicts already determined                        │
│   C001 SUPPORTED  arXiv:2605.18071 exists            │
│   C003 SUPPORTED  npm package found                  │
│   C005 CONTRADICTED  RFC 99999 not found             │
├──────────────────────────────────────────────────────┤
│ [Triage-Escaped]  {N2} claims (skipping search)      │
│   C007 CONFIDENT  "vLLM supports FP8"                │
├──────────────────────────────────────────────────────┤
│ [Needs Deep Search]  {N3} claims                     │
│   C008 UNCERTAIN  "EPYC 9474F runs 6.44 tok/s"       │
│   C009 SUSPECT    "KTransformers 17K stars"          │
├──────────────────────────────────────────────────────┤
│ [Compound Embedded]  {N4} warnings                   │
│   ⚠ C012 compound_embedded: >25 words, no catalog    │
├──────────────────────────────────────────────────────┤
│ [INFERRED]  {N5} claims (no verification needed)     │
│   💡 C015 MLA compression makes CPU inference viable │
└──────────────────────────────────────────────────────┘

Continue with deep search? [y/n]
Commands: skip <id> | view <id> | search <id> | edit <id>
```

## Skip/Break Thresholds (DD-21)

```
if new_claims <= 3 AND all_verdicts == SUPPORTED:
    auto_skip_checkpoint()

if any(severity == "high" AND verdict == "CONTRADICTED"):
    force_break_checkpoint()
```

## User Commands

| Command | Behavior |
|---------|----------|
| `y` | Continue to Phase 5 deep verify |
| `n` | Abort, save current state |
| `skip C001` | Skip specific claim, remove from deep search queue |
| `view C001` | Show full claim details (text, location, triage result) |
| `search C001` | Override triage: force triage-escaped claim into Phase 5 |
| `edit C001` | Allow manual edit of claim_text or routing before search |

## Synchronization (DD-11)

After checkpoint interaction:
1. Re-read `documents/<key>/claims.json` to pick up any user edits
2. Claims with `status=unconfirmed` → user confirmed → set `status=confirmed`
3. Proceed to Phase 5 only with confirmed claims in deep search queue
