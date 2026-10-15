# mr-review-triage — skill impact ledger

Ledger for behavioral changes to this skill. Sanitized per repo rules: no
internal hosts/projects/credentials; tickets reference public GitHub issues.

## 2026-10-15 — spec #57 / ticket #60: pull ordinal + digest reconciliation

- Proposal: spec #57 (triage-mr scripted redesign), ticket #60 — add stable
  per-finding ordinal `no` to pull output; add `--digest --against
  classified.json` new-round detection (absorbs peer proposal S5: pull
  summary parser rewritten per round).
- Landing: `scripts/ocr-pull-discussions.py` — `no` = deduped API first-seen
  order (1..N, no sorting key); `--digest --against` emits only new findings
  (original ordinals kept) to stdout as bare JSON, human summary to stderr
  with zero truncated-ID shapes; missing `--against` file = first round (not
  an error); corrupt/unrecognized `--against` shape hard-fails. Both
  classified.json shapes accepted (schema-2 entries / flat array).
  Reference docs updated (gitlab.md, github.md). New CLI-level test suite
  `tests/` with offline fixture API (fake curl/gh on PATH, no network).
- Commit: ad19321 (branch feat/triage-t60-pull-digest)
- Verification: 11 pytest cases green (uv run pytest) covering ordinal
  ordering/stability (both platforms), digest mixed old/new ids, schema-2
  against file, missing against file, no-ID human output, usage errors,
  fail-closed malformed against file.
