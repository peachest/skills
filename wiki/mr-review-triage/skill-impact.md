# mr-review-triage — skill impact ledger

Ledger for behavioral changes to this skill. Sanitized per repo rules: no
internal hosts/projects/credentials; tickets reference public GitHub issues.

## 2026-10-15 — spec #57 / ticket #59: verdict.py, classified.json sole writer

- Proposal: spec #57 (triage-mr scripted redesign), ticket #59 — the agent
  never touches discussion ids or state files during classification; it only
  produces ordinal + verdict semantics, and the script does the copying.
- Landing: new `scripts/verdict.py` — `verdict.py <MR> <no> --class
  TP|FP|Edge|OOS|Q --reason ... [--fix-plan] [--priority high|medium|low]
  [--resolved true|false] [--force]`. Copies the full discussion_id
  byte-exact from `.triage/<MR>/issues.json` (pull stdout redirect), stores
  anchor = sha256(body)[:16], writes schema 2 entries to
  `.triage/<MR>/classified.json` via `triage_state_dir` (cwd/realpath) with
  atomic read-modify-write (tmp + os.replace). Exit codes: 0 ok / 1 state
  error (missing pull file, unknown no, existing verdict without --force,
  corrupt or non-schema-2 state files) / 2 usage (argparse: missing flags,
  bad enums, non-integer or <1 ordinal, unsafe state-dir name, TP without
  --fix-plan). Per-item resolved decided at verdict time per Amendment R2
  修订 A: Edge defaults resolved=true (overridable), Q defaults open (only
  explicit --resolved true closes), TP/FP/OOS leave the field unset so post
  applies its mode map. Refuses same-ordinal re-verdict and same-finding
  (thread + anchor) re-append under a reshuffled ordinal without --force;
  --force replaces the slot in place (no stale fields). Fallback-note
  sub-issues sharing one discussion_id still append (different anchors).
  Success echo = no + author + first body line; the id never reaches
  human-readable output (no full or truncated shapes). New
  tests/test_verdict.py (28 CLI-level cases) incl. the #58-recorded Q
  end-to-end acceptance through ocr-post-labels and Edge/Q resolved
  propagation through post in triage mode; conftest gains `run_verdict`.
- Commit: 9830bda (branch feat/triage-t59-verdict)
- Verification: 80 pytest cases green (uv run pytest; 52 pre-existing + 28
  new), ruff clean on the touched files, fake-API e2e asserts Q stays open
  and Edge resolves via post --mode triage.

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

## 2026-10-15 — spec #57 / ticket #64: verify display de-truncation + pipeline timing gate

- Proposal: spec #57 Amendment R2 修订 B + 展示层纪律 — verify human output
  drops the `discussion_id[:12]` truncation (P-005 script-side self-bite);
  pipeline completion check moves into the scripts (P-002: no agent
  ritual checks).
- Landing: `scripts/ocr-verify-resolved.py` — human thread labels are
  `no=<ordinal>` (mapped from the pull state file, default
  `.triage/<MR>/issues.json`, override `--pull-file`) or `anchor=<sha256(body)[:8]>`
  for threads outside the pull file (OCR summaries / no pull run); corrupt
  pull file = WARN + anchor degradation, never blocks the gate; `[N/M notes
  open]` annotation kept; `--json` keeps full ids (internal `_body` field
  projected out). `run_pipeline_gate()` in `ocr_platform.py` +
  `head_pipeline_status()` (ocr_gitlab.py) / `check_runs_status()`
  (ocr_github.py): in-flight CI → exit 2 on pull AND verify,
  `--skip-pipeline-check` escape hatch; terminal/unknown/no-CI → stderr
  note + proceed (thread check still fails closed). SKILL.md gate wording
  itself is ticket #65 scope.
- Commit: de91927 (branch feat/triage-t64-verify-gate)
- Verification: 102 pytest cases green (80 pre-existing + 22 new
  CLI-level: ordinal/anchor display, annotation, corrupt/missing pull
  file, --json ids, gate running/skip/terminal/no-CI × gitlab+github ×
  pull+verify).
