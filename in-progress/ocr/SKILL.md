---
name: ocr
description: >
  Company-adapted wrapper for the `ocr` CLI (open-code-review) against the internal
  internal-gw LLM gateway. Use when the user asks to review code changes (workspace,
  commit, or branch diff), audit existing code without a diff (ocr scan), resume or
  look up a previous review session, re-review after fixes, or set up / verify /
  troubleshoot the ocr LLM provider (LLM timeouts, concurrency, thinking-disable).
  Enforces gateway-safe defaults (OCR_LLM_TIMEOUT=600, --timeout 30 locked,
  concurrency tuned to diff size), persists results as ocr sessions, and hands
  findings to /skill:fix. Prefer this over the generic open-code-review skill.
---

# ocr — company-adapted code review

Local wrapper for the `ocr` CLI (open-code-review). The active provider is the
internal `internal-gw` gateway, preconfigured once per machine in
`~/.opencodereview/config.json`. Review results persist automatically in
`~/.opencodereview/sessions/` — ocr's own directory, so repo `.gitignore` is
never a concern and past reviews stay queryable per repo. `language` is set to
中文, so ocr emits Chinese comments natively.

## 1. Prerequisites

```bash
which ocr || npm i -g --prefix ~/.npm-global @alibaba-group/open-code-review
ocr llm test
```

Baseline is ocr **v1.11.1+** — `--effort` presets, effort-scaled timeouts, and the
rule.json arbitrary-file-read fix need it.

**Done when** `ocr llm test` reports success. On failure → chapter 2.

## 2. LLM provider (internal gateway)

The provider (`internal-gw`) is configured globally at `~/.opencodereview/config.json`.
Two facts govern every config decision:

- **`ocr config` only supports `set`** — there is no `get`. Inspect the config
  file with python instead, and redact any `api_key`/`auth_token` values before
  showing them.
- **When `provider <name>` is active, every `llm.*` setting is ignored.** The
  resolver takes the provider path and returns; `ocr config set llm.extra_body`
  is a silent no-op (ocr prints a WARNING). This exact mistake has propagated
  through many sessions. `extra_body` must live at
  `custom_providers.<name>.extra_body`.

Fresh-machine setup (get the gateway URL, model, and API key from the user;
never reuse or echo old keys):

```bash
ocr config set custom_providers.internal-gw.url <gateway-url>
ocr config set custom_providers.internal-gw.api_key <API_KEY>
ocr config set custom_providers.internal-gw.protocol openai
ocr config set custom_providers.internal-gw.model <model>
# GLM-5.3 models (glm53-*): thinking cannot be disabled — reasoning_effort is the only knob
ocr config set custom_providers.internal-gw.extra_body '{"chat_template_kwargs": {"reasoning_effort": "low"}}'
ocr config set provider internal-gw
ocr config set language 中文
```

Thinking control is **model-version specific** (measured on GLM-5.3 official docs
+ live gateway, 2026-09-03):

- **GLM-5.3** (`glm53-*`): `thinking:{"type":"disabled"}` errors on the official
  API, and `chat_template_kwargs:{"enable_thinking":false}` is **silently
  ignored** — thinking always runs, default effort `max`. The only knob is
  `chat_template_kwargs:{"reasoning_effort":"low"}` (low/high/max): `low` measured
  5.5× faster (91s→16.5s, 2048→369 tokens). ocr v1.11 preserves provider
  reasoning across turns (#1070), so `max` effort also bloats multi-round context.
- **GLM-5.2 and below**: `thinking:{"type":"disabled"}` and
  `enable_thinking:false` both work as intended (effort values none/minimal).

Without control the model emits long chains of thought, time-to-first-token
exceeds the request timeout, and reviews fail. A slow-review pattern blamed on
the gateway may really be `max`-effort thinking.
Verify the config actually reaches the wire:

```bash
bash <SKILL_DIR>/scripts/check-config.sh
```

It replays the real config against a local fake server and inspects the
captured request body. **Done when** it prints `PASS`. Note this is **L1 only**
(the parameter was sent) — on GLM-5.3 a sent parameter can still be silently
ignored. For **L2** effect verification (assert real latency/tokens/
reasoning_content against a live endpoint) use the ocr-image repo's
`diagnostics/test-ocr-config.sh` S7 scenario (`REAL_LLM_URL`/`REAL_LLM_TOKEN`).

## 3. Parameter rules (every invocation)

| Parameter | Value | Rule |
|---|---|---|
| `OCR_LLM_TIMEOUT` | `300` | Export on every invocation. Per-LLM-request timeout in seconds; the only knob for it (`timeout_sec` is not in the `ocr config set` whitelist). Measured healthy-request p99 ≤ 276s across 19.5k local requests; the SDK hardcodes 5 retries, so the worst chain is 6× this value — 300s bounds that at 30 min instead of a full hour. |
| `--timeout 30` | locked | Per-file-group agentic-loop timeout in minutes. The agent never changes this value. (v1.11 default is 15, scaled by effort — our explicit 30 stays the safe upper bound.) |
| `--concurrency` | 2 default | Gateway is shared — high concurrency queues requests until they time out. Judge the scope first with `--preview`: ≤5 files → 4; 6–15 → 2–4 (e2e: 12 files at 4 with `--effort low` finished in ~16 min); >15 → 1–2. Whole-repo scan → 1. |
| `--effort medium` | default | Review rounds per file: low=1, medium=2, high=3. Medium for the first full review. Use `low` when verification matters more than depth: re-review after `/skill:fix`, large scopes (>15 files), quick pre-MR sanity checks — it halves the LLM work. |
| `--max-tokens-budget` | optional | Runaway-cost guard for very large scopes. Measured ~129k tokens/file — input-dominated by agent-loop context accumulation (file_read / code_search), far above naive diff-size estimates. E.g. `--max-tokens-budget 4000000` for a ~30-file diff. When exceeded, dispatch stops, partial results still publish, exit 0. |
| `--audience agent` | always | Summary-only output on stdout. |
| `-b` / `--background` | agent-written | Write 1–3 sentences from the current session context: what the change does, why, and key constraints. You already hold the full context — compose it yourself. |
| `--exclude` | as needed | doublestar full-path match — bare patterns (`*_mock.go`) only match the repo root, deep matches need a `**/` prefix. v1.11's built-in default list (46 patterns) already excludes tests / `*.gen.go` / `*.pb.go` / testdata / fixtures — only fill gaps: `'**/*_mock.go,**/mock_*.go,**/go.sum,**/go.mod'`, lockfiles, `'**/*.min.js'`. |

Canonical invocation:

```bash
OCR_LLM_TIMEOUT=300 ocr review --audience agent --timeout 30 --concurrency <n> --effort <low|medium> -b "<background>"
```

## 4. Scenario routing

| User intent | Command |
|---|---|
| Review my changes / working copy | `ocr review` (staged + unstaged + untracked) |
| Review commit abc123 | `ocr review -c abc123` |
| Review branch / MR | `ocr review --from <base> --to <head>` |
| Continue a previous review | `ocr review --from <base> --to <head> --resume <session-id>` |
| Audit existing code (no diff) | `ocr scan ...` → chapter 6 |

Resume is a **flag on `review`/`scan`**. There is no `ocr continue` command —
never look for one; get the session id via `ocr session list` (chapter 7).

## 5. Result handling and the fix loop

- Each comment carries native `severity` (critical / high / medium / low) and
  `category`. Report to the user in Chinese, grouped by severity. Discard `low`
  — likely false positives or nitpicks.
- A comment with `start_line` and `end_line` both `0` failed positioning:
  locate the right spot yourself from the comment text and the target file.
- After reporting, hand the findings list (critical/high/medium) to
  `/skill:fix`. This skill never drives fixes itself.
- **Re-review hook**: once `/skill:fix` completes, offer to re-run review on
  the new diff with `--effort low` — verification needs one round, and it
  catches "fixed but fixed wrong". The old session stays in
  `~/.opencodereview/sessions/` for comparison.

## 6. ocr scan (audit existing code)

Use when the user asks to audit / 检查 / scan existing code without a diff.

```bash
OCR_LLM_TIMEOUT=300 ocr scan --audience agent --timeout 30 --concurrency <n> --effort low \
  -b "<background>" --path <files-or-dirs> --exclude '**/*_mock.go,**/*.min.js'
```

- Run `--preview` first to count files → set concurrency per chapter 3.
- `--no-plan`: skips the per-file PLAN pre-pass — faster on small scopes and
  re-scans.
- `--batch by-directory | by-language | none`: choose `by-directory` for
  repo-layout-driven audits; `none` for single-file scans.
- Findings flow into the same severity report and `/skill:fix` handoff as
  review (chapter 5).

## 7. Session query (find past reviews)

Sessions are the single source of results — pass `--output` only when the user
asks for a file copy.

```bash
ocr session list                     # sessions for the current repo
ocr session show <session-id>        # metadata + per-file items
ocr session comments <session-id>    # structured comments
ocr session comments <id> > x.md     # markdown copy when needed
ocr session compare <id1> <id2>      # diff findings across two sessions (e.g. before/after fix)
ocr review --resume <session-id>     # continue a range review
```

When the main session needs "what did the last review find", start with
`ocr session list` in the project repo.

## 8. Troubleshooting

Work the layers in order: **config → `ocr llm test` → grouping → per-file → post-processing**. The strongest evidence source is the `retry_report` in the result JSON (schema `ocr.llm-retry-report/v1`: per-request `attempts[{status_code, error_class, duration_to_headers_ms, failure_phase}]` plus total/retried/recovered/failed) — one run reconstructs the whole failure history. Capture it with `--format json -o /tmp/r.json` (with `--audience human`, progress still streams to stderr).

**Normal baselines** (v1.11, effort=medium, internal gateway): ~120–129k tokens/file (input-dominated, but cache_read is 55–90% of input — real cost is far below raw input), ~10 tool_calls/file, a 5-file MR in 15–17 min. These were measured on the now-retired `glm53-test` before `reasoning_effort` control existed — with `reasoning_effort:"low"` (chapter 2) expect faster, lighter runs; treat them as an upper bound and re-baseline from fresh session data. ≥3× baseline is a real anomaly; ~1.2× is noise. tokens/file >2× baseline with low comment yield signals the repeated-file-read pattern (large diff re-reading the same files) — narrow the scope or split the review.

| Symptom | Meaning | Action |
|---|---|---|
| `504` + `duration_to_headers_ms` ≈ `OCR_LLM_TIMEOUT`×1000 | Gateway held the request a full timeout period, then 504'd — a gateway hang, not a client problem; retries likely hang again | Gateway-side investigation; the per-file timeout keeps the remaining files alive |
| Non-504 header timeout (`duration_to_headers_ms` ≈ timeout, no HTTP status) | Thinking running on the wire — on GLM-5.3 `enable_thinking:false` is silently ignored, so check the `reasoning_effort` knob too | Run `bash <SKILL_DIR>/scripts/check-config.sh` (L1), then L2-verify against a real endpoint per chapter 2 |
| `LLM grouping failed (parse grouping JSON: invalid character L...)` | Gateway returned an error page as the body; ocr degraded to per-file dispatch — non-fatal, just slower. (v1.11.1+ skips grouping for small change sets — no grouping signature on a small diff is normal) | Root cause is the gateway, not ocr; proceed, and treat frequent occurrences as a gateway problem |
| `context deadline exceeded` (no HTTP status) | The per-file clock expired — a different clock from the per-request timeout. Cutting the **plan phase** is non-fatal (`Plan phase failed ... continuing without plan`); cutting the **main task** loses the file (`Subtask error: LLM completion error ...`) | Surviving files stay in the session — re-run lost files with `--resume`; if frequent, the per-file budget is too tight for this model's speed |
| Reviews keep timing out across every parameter combination | Model/gateway choice dominates parameters — measured: vibecoding+glm-5 ~4 min/file vs internal-gateway glm53-test finishing 12 files in ~16 min with the same flags | Switch model/gateway (chapter 2) before tuning anything else |
| Per-file failures on a large project | Concurrency too high for the shared gateway | Drop concurrency to 1, keep `OCR_LLM_TIMEOUT=600` and `--timeout 30` |
| No progress visible while a review runs | `--audience agent` discards progress lines entirely | Debug-run with `--audience human --format json -o /tmp/r.json 2>/tmp/ocr-stderr.log` — progress goes to stderr, stdout stays pure JSON |
| A review hangs past `--timeout` and never finishes | Comment-relocation LLM calls run under `context.WithoutCancel` — they escape the per-file timeout entirely (upstream bug, unfixed in v1.11.2, `internal/llmloop/loop.go:383`) | Interrupt and re-run with `--resume <session-id>`; a wall-clock `timeout` wrapper is the CI-side workaround |
| Want fewer per-file LLM rounds | `--max-tools` cannot go below the per-group template default (v1.11: default 100, min clamp 50) — it is not a knob for reducing tool rounds | Use `--effort low` instead (halves full review rounds); `--no-filter` additionally skips the per-file REVIEW_FILTER_TASK post-processing (~4% of requests) at the cost of noise |
| An `--exclude` pattern doesn't take effect | Matching is doublestar full-path, not gitignore basename — bare patterns only match the repo root | Check `ocr review --preview --format json` first: the `exclude_reason` field shows whether a file fell to `default_path` (built-in list) or `user_exclude` (your pattern) — faster than guessing pattern syntax |
| `provider "internal-gw" is active and takes precedence over llm.*` warning | `llm.*` settings are ignored | Move the setting to `custom_providers.internal-gw.*` |

Deep-dive tooling (fake server, config test matrix, resolver source notes):
`~/projects/ocr-image/diagnostics/`. The `diagnose-ocr-ci` skill automates mining
`~/.opencodereview/` session jsonl for latency baselines.
