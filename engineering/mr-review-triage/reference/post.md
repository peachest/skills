# post-labels — verdict posting, resolve execution, summary sweep

Reads a schema-2 classified state file and for each entry: validates, replies
with the verdict, resolves per the verdict-time decision. One call — there is
no manual fallback and no hand-written-API path anywhere in the triage flow.

## Invocation

```bash
python3 <SCRIPTS_DIR>/ocr-post-labels.py <MR_OR_PR_ID> --mode triage \
    --classified .triage/<MR>/classified.json [--pull-file <path>] [--force]
```

- `--classified <path>`: schema-2 state file; stdin is an alternative
  **transport** — schema-2 validation applies identically to both, a
  versionless input hard-fails with filename + missing-field list either way.
- `--pull-file <path>`: pull state file for join validation (default
  `.triage/<MR>/issues.json`).
- `--force`: operator override for "reply failed → resolve anyway" (a thread
  must not close without its verdict reason on the wall).
- Post runs **no CI gate** — its join/anchor validation targets the pull
  snapshot, not live platform state. Run it per verdict round; the pipeline
  gate belongs to pull and verify.

## Validation (hard-fail before any platform call)

- **Join**: every unposted entry's `discussion_id` must byte-match an id in
  the pull file; mismatch exits naming the entry's `no` + the closest real id.
  Entries already `posted: true` are historical (validated when posted) and
  skip the join — next-round contract.
- **Anchor**: entry anchor must equal `sha256(pull body)[:16]` recomputed from
  the same pull file. A reviewer editing the live comment mid-run does not
  false-reject (both sides read the same stale snapshot). A body that changed
  between pulls = genuinely stale entry → re-run `verdict.py` for it.

## Execution semantics

1. Reply with classification label + reason/fix-plan — skipped when the thread
   already carries this entry's anchor marker + verdict revision fingerprint
   (content dedup; covers manual-curl bypass where `posted` is absent). A
   body-anchor match with a different revision fingerprint = a **revised
   verdict** (`verdict.py --force`) → re-post; the superseded reply stays as
   history.
2. Resolve iff the entry's per-item `resolved` field says so — post executes
   the verdict-time decision, never re-judges. Legacy entries without the
   field fall back to mode maps (`--mode triage`: TP+FP+OOS resolve, Edge/Q
   stay open; default mode: TP stays open for tracking, FP/OOS resolve).
   Mode-map contents: ocr-post-labels.py `_DEFAULT_RESOLVED` / `_TRIAGE_RESOLVED`. A thread is
   never resolved when its reply failed (exit non-zero; `--force` overrides).
   On GitLab a 2xx resolve PUT is intent, not state — the platform state is
   confirmed by a GET read-back (one PUT+read retry on a still-open result,
   then the item fails closed); GitHub asserts `thread.isResolved` from the
   mutation response itself. `ok` counts confirmed resolutions only.
3. `posted: true` written back to the `--classified` file on success.

## OCR summary sweep (after the classified entries)

Three template classes off the thread's root-note body:

| class | reply | resolve |
|-------|-------|---------|
| 🔍 start | confirmation note, no statistics | only when a ✅ end thread completed this run AND the classified phase had zero failed items |
| ✅ end / LGTM | statistics (TP/FP/Edge/OOS/Q counts + TP fix files) | yes |
| ⚠️ error | fixed escalation note | **never** — its presence fails the run (exit non-zero); the closure gate staying red is intentional human-in-loop design |

Every sweep reply embeds the summary thread's own anchor marker → re-running
post on an already-swept MR posts nothing.

## Failure taxonomy

- join/anchor hard-fail → state problem, fix upstream (`verdict.py` / re-pull).
- platform call failure → item counts as fail, exit non-zero; re-run post
  (idempotent via content dedup).
- ⚠️ error summary present → expected non-zero; report and stop (never force
  green).
