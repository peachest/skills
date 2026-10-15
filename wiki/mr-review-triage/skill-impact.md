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

## 2026-10-15 — spec #57 / ticket #58: post state-file foundation

- Proposal: spec #57 (triage-mr scripted redesign), ticket #58 — post gets
  the schema 2 state-file contract; absorbs peer proposal S4 (P-002
  方案追加: `--classified <path>` file transport kills the heredoc
  double-write).
- Landing: `scripts/ocr-post-labels.py` — `--classified <path>` plus stdin
  as transport only (identical validation); versionless/schema-1 input
  hard-fails with filename + missing-field list + rebuild hint before any
  platform call; classification vocabulary pinned — `Q` normalized to
  `Question` before label/resolved lookups, unknown/missing classification
  hard-fails with zero platform calls (silent FP downgrade removed);
  priority is the high|medium|low string enum, present-but-invalid values
  hard-fail (int coercion removed); `triage_state_dir()` exported from
  `ocr_platform.py` (cwd/realpath, never $HOME — verdict.py #59 reuses).
  fix SKILL.md/CLASSIFICATION.md synced to schema 2 + dual-mode contract
  (triage mode = semantics only via verdict.py; standalone = direct write).
  Shared harness: env-gated `FAKE_API_LOG` request journal added to
  fake_api.py (off by default, pull tests untouched).
- Commit: 549c95b (branch feat/triage-t58-post-foundation)
- Verification: 37 pytest cases green (uv run pytest, incl. #60's 11 pull
  cases) covering both transports × valid/versionless/schema-1, Q/Question
  alias + unknown/missing hard-fail with empty API journal, priority enum
  accept/reject, triage-mode resolve semantics, verdict-shaped entry
  digest, cwd/realpath state-dir vs $HOME, unreadable path.
