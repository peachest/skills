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

## 2026-10-15 — spec #57 / ticket #63: OCR_REMOTE convergence + startup auth probe

- Proposal: spec #57 (triage-mr scripted redesign), ticket #63 — remote name
  overridable via `OCR_REMOTE` env (default origin) collected into ONE
  helper; startup auth probe comparing the derived host+token's project
  against the local remote path before the first business API call (token
  existence ≠ right instance — fork repos with a GitHub origin silently
  pulled the upstream and reported "0 findings").
- Landing: `scripts/ocr_platform.py` — `_git_remote_url()` is now the single
  remote lookup (OCR_REMOTE, default origin; explicit-but-unknown OCR_REMOTE
  exits 2 instead of silently falling back) plus `run_auth_probe()`
  dispatcher. `scripts/ocr_gitlab.py` / `scripts/ocr_github.py` drop their
  inline copies and gain `probe_auth()`: one project lookup, returned
  path_with_namespace / full_name compared against the local remote path
  (case-insensitive), mismatch → exit 2 naming OCR_REMOTE. Probe wired into
  pull/post/verify uniformly. Skips (no error) when there is no local-path
  anchor: GITHUB_REPOSITORY env precedence (github) and OCR_PLATFORM forced
  platform (either) — the latter keeps operator overrides and #60's test
  conftest valid. 0-findings pull prints derived platform + host +
  OCR_REMOTE hint on stderr. New tests/test_remote_probe.py: 15 CLI-seam
  cases with self-contained offline fakes (coexists with #60's conftest
  harness; consolidation left for a follow-up if the reviewer wants one
  fake-bin).
- Commit: 0908dab (branch feat/triage-t63-remote-probe; integration merge
  resolved at 93fe838 — pull 0-findings hint composes with #60's
  no/digest block, probe skips under OCR_PLATFORM)
- Verification: 26 pytest cases green after merge (15 #63 + 11 #60).
