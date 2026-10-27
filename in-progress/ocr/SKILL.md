---
name: ocr
description: >
  Company-adapted wrapper for the `ocr` CLI (open-code-review) against the internal
  internal-gw LLM gateway. Use when the user asks to review code changes (workspace,
  commit, or branch diff), audit existing code without a diff (ocr scan), resume or
  look up a previous review session, re-review after fixes, or set up / verify /
  troubleshoot the ocr LLM provider (LLM timeouts, concurrency, thinking-disable).
  Enforces gateway-safe defaults (OCR_LLM_TIMEOUT=300, --timeout 30 locked,
  concurrency tuned to diff size), persists results as ocr sessions, and hands
  findings to /skill:fix. Reviews run in the background (bg_run) or via a
  subagent so they never block the foreground task. Prefer this over the
  generic open-code-review skill.
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

Baseline is ocr **v1.13.3** (audited 2026-10-27; chapter 9 assumes it). `--effort`
presets need v1.11.1+. If `ocr version` is older than v1.13, reinstall first:
`npm i -g --prefix ~/.npm-global @alibaba-group/open-code-review`.

**Done when** `ocr llm test` reports success. On failure → chapter 2.

## 2. LLM provider (internal gateway)

The provider (`internal-gw`) is configured globally at `~/.opencodereview/config.json`.
Two facts govern every config decision:

- **`ocr config` has `set` and `unset` but no `get`.** `unset` removes a whole
  `custom_providers.<name>` / `mcp_servers.<name>` entry — it cannot delete
  individual leaf keys (measured v1.13.3). Inspect the config file with python
  instead, and redact any `api_key`/`auth_token` values before showing them.
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
| `OCR_LLM_TIMEOUT` | `300` | Export on every invocation. Per-LLM-request timeout in seconds. Since v1.12 a per-provider `custom_providers.<name>.timeout_sec` is also settable, but the env var wins when both are set (measured v1.13.3: `OCR_LLM_TIMEOUT=60` beat `timeout_sec=5` against a 30s-delay fake server). Measured healthy-request p99 ≤ 276s across 19.5k local requests; the SDK hardcodes 5 retries, so the worst chain is 6× this value — 300s bounds that at 30 min instead of a full hour. |
| `--timeout 30` | locked | Per-file-group agentic-loop timeout in minutes. The agent never changes this value. (v1.11 default is 15, scaled by effort — our explicit 30 stays the safe upper bound.) |
| `--concurrency` | 2 default | Gateway is shared — high concurrency queues requests until they time out. Judge the scope first with `--preview`: ≤5 files → 4; 6–15 → 2–4 (e2e: 12 files at 4 with `--effort low` finished in ~16 min); >15 → 1–2. Whole-repo scan → 1. |
| `--effort medium` | default | Review rounds per file: low=1, medium=2, high=3. Medium for the first full review. Use `low` when verification matters more than depth: re-review after `/skill:fix`, large scopes (>15 files), quick pre-MR sanity checks — it halves the LLM work. |
| `--max-tokens-budget` | optional | Runaway-cost guard for very large scopes. Measured ~129k tokens/file — input-dominated by agent-loop context accumulation (file_read / code_search), far above naive diff-size estimates. E.g. `--max-tokens-budget 4000000` for a ~30-file diff. When exceeded, dispatch stops, partial results still publish, exit 0. |
| `--audience agent` | always | Summary-only output on stdout. |
| `--format json` + `-o <file>` | always | Machine-readable findings land in a file (also gives `retry_report` for troubleshooting); sessions dir remains the source of truth. Never parse the stdout summary. |
| `-b` / `--background` | agent-written | Write 1–3 sentences from the current session context: what the change does, why, and key constraints. You already hold the full context — compose it yourself. The background must carry real architecture knowledge and a concrete review checklist (modules touched, invariants at risk, what to look for) — never a generic "review for bugs"; a vague background yields vague findings. |
| `--exclude` | as needed | doublestar full-path match — bare patterns (`*_mock.go`) only match the repo root, deep matches need a `**/` prefix. v1.11's built-in default list (46 patterns) already excludes tests / `*.gen.go` / `*.pb.go` / testdata / fixtures — only fill gaps: `'**/*_mock.go,**/mock_*.go,**/go.sum,**/go.mod'`, lockfiles, `'**/*.min.js'`. |

Canonical invocation:

```bash
OCR_LLM_TIMEOUT=300 ocr review --audience agent --format json -o <file> --timeout 30 --concurrency <n> --effort <low|medium> -b "<background>"
```

## 4. Scenario routing

### Run mode: background by default, never block the foreground

A full review takes 15–30+ min (chapter 8 baselines). A foreground bash call
freezes the session for the whole duration. Route by context:

| Context | How to run |
|---|---|
| pi session (default) | `bg_run` background shell task. Continue the foreground conversation; handle results when the completion notification arrives. |
| Findings should be verified/reported without loading this session (parallel work, peer handoff, context isolation) | Spawn a `delegate`/`worker` subagent (pi-subagents rules) whose task is: run the ocr command, then perform the chapter-5 verification and report findings grouped by severity. The subagent absorbs both the wait and the token-heavy verification. |
| Foreground is fine | Only quick operations: `ocr session list/show/comments`, `ocr llm test`, `--preview`, config checks — seconds, not minutes. |

Background invocation (pi):

```
bg_run: OCR_LLM_TIMEOUT=300 ocr review ... --format json -o <abs-path>.json
```

- `-o` must be an absolute path you can locate after the task ends; the
  sessions dir (`ocr session list`) remains the source of truth either way.
- One review at a time per repo: if the previous round is still running, let
  it finish — its result covers the interim changes (same rule as the rolling
  review in implement-spec-in-pipeline).
- On the completion notification, run chapter 5 against the JSON. If the task
  failed, feed the captured output into the chapter-8 troubleshooting table.
- Rollback rule: if `ocr` itself keeps failing (auth, gateway timeouts), hand
  the same diff to a `reviewer` subagent for a read-only review — the
  review-runs-while-work-continues shape matters more than the engine.

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

- When the review ran in the background or in a subagent (chapter 4), this
  whole section runs at completion time — on the task notification for
  `bg_run`, or as the subagent's report — not synchronously in the
  dispatching turn.
- **Verify every finding against the source before reporting** — LLM findings
  must never be relayed verbatim. Check each one against the actual code; the
  three failure classes to filter out: hallucinated (no such code path),
  stale (code was fixed after the diff), mislocated (real issue, wrong
  file/line). Drop what fails verification.
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
- **Full-repo scan: add `--no-plan --no-summary` — measured ~30% time
  saved.**
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
| A review hangs past `--timeout` and never finishes | Comment-relocation LLM calls run under `context.WithoutCancel` — they escape the per-file timeout entirely (upstream bug, still unfixed in v1.13.3, `internal/llmloop/loop.go:826`) | Interrupt and re-run with `--resume <session-id>`; a wall-clock `timeout` wrapper is the CI-side workaround |
| Want fewer per-file LLM rounds | `--max-tools` cannot go below the per-group template default (v1.11: default 100, min clamp 50) — it is not a knob for reducing tool rounds | Use `--effort low` instead (halves full review rounds); `--no-filter` additionally skips the per-file REVIEW_FILTER_TASK post-processing (~4% of requests) at the cost of noise |
| An `--exclude` pattern doesn't take effect | Matching is doublestar full-path, not gitignore basename — bare patterns only match the repo root | Check `ocr review --preview --format json` first: the `exclude_reason` field shows whether a file fell to `default_path` (built-in list) or `user_exclude` (your pattern) — faster than guessing pattern syntax |
| `provider "internal-gw" is active and takes precedence over llm.*` warning | `llm.*` settings are ignored | Move the setting to `custom_providers.internal-gw.*` |

## 9. New surface in v1.12 → v1.13 (audited 2026-10-27 against installed v1.13.3)

Everything below arrived after this skill's v1.11 baseline. Verified against
`--help` output and the upstream changelog; the timeout precedence claim was
additionally A/B-measured against a delay fake server.

| Surface | What it does | When to reach for it |
|---|---|---|
| `ocr review -B <file>` (`--background-file`) | Requirement context from a Markdown file; takes precedence over `-b` | Long review checklists — write a file instead of cramming `-b` |
| `--provider <p> --model <m>` | Per-run LLM override, no config change | A/B a candidate model on one review before switching the gateway default |
| `--format sarif` | SARIF output alongside text/json | CI security-gate ingestion |
| `ocr delegate preview` / `delegate rule` | Prints the would-be-reviewed file list + resolved rules with **no LLM call** | Cheap scope check before dispatching a real review; hand the rule set to a pi subagent that runs its own LLM review |
| `ocr viewer` | WebUI over saved sessions at `localhost:5483` | Browsing long session history in a browser instead of `session show` |
| `ocr session export [id] -o x.html` | Self-contained offline HTML of one session (viewer assets inlined) | Archiving CI review evidence. **Caution: embeds source excerpts — run sanitize-check before the artifact leaves the machine** |
| `ocr session rm <id> [--yes]` | Delete a saved session (irrecoverable; confirms first without `--yes`) | Cleaning garbage sessions out of `~/.opencodereview/sessions/` |
| `ocr rules check <path>` | Shows which review rule matches a file | Debugging rule/exclude assignment without a full `--preview` |
| `ocr scan --no-dedup --no-summary` | Skip per-batch DEDUP and post-run PROJECT_SUMMARY | Extra scan cost knobs beyond `--no-plan` (chapter 6) |
| `review/scan --max-git-procs` | Cap concurrent git subprocesses (default 16) | Huge repos or busy machines |
| `custom_providers.<name>.timeout_sec`, `mcp_servers.<name>` config | Per-provider request timeout; MCP servers reachable from the review tool loop | timeout: only when the env var can't be set (env wins — chapter 3); MCP: give the reviewer repo-specific tools |
| New rule packs: Rego, PowerShell, Nushell, shader languages | Auto-applied review rules | Nothing to do — just explains new finding categories |

Known-bug recheck in the same audit: the comment-relocation `WithoutCancel`
timeout escape (chapter 8) is **still present in v1.13.3** — the workaround
there remains valid.

Deep-dive tooling (fake server, config test matrix, resolver source notes):
`~/projects/ocr-image/diagnostics/`. The `diagnose-ocr-ci` skill automates mining
`~/.opencodereview/` session jsonl for latency baselines.
