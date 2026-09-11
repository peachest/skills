---
name: diagnose-ocr-ci
description: Diagnose ocr-review failures — GitLab CI jobs (which layer a job stalled or failed at, why inline comments partially posted, retry_report reading), ocr-review speed-shift attribution (review 变快/变慢了、为什么提速，duration trend across groups), and local ocr sessions under ~/.opencodereview/sessions (llm_error classification, timeout inference, token throughput vs baseline). Use when the user mentions an ocr-review job that failed, hung, timed out, was canceled, posted N/M comments, produced no artifacts, or a local `ocr review` run that keeps failing, or asks to analyze ocr sessions/logs/artifacts/retry reports on the internal GitLab (or any GitLab with glab-cli auth), or asks whether ocr-review got faster or slower recently.
---

Diagnose `ocr-review` runs by walking the **layer ladder** — seven layers the run climbs from pod scheduling to artifact upload (CI) or its local subset (config → grouping → per-file). Every failure lives at exactly one layer; the diagnosis is the answer to "which rung did the run stop on, and which signature proves it".

## Procedure

1. **Identify the target.** One of:
   - a GitLab project (survey all its ocr-review jobs) or a specific job ID;
   - a **local session** — `~/.opencodereview/sessions/<project>/<uuid>.jsonl`, addressed by uuid prefix or path (`local` command), or "the ocr run that kept failing today" (list with `local`, pick the failed entries);
   - pasted log/artifact files (`analyze`).
   If the user gave none of these, ask.
2. **Fetch evidence with the script** (see below). For CI jobs, artifacts (`ocr-result.json` + `ocr-stderr.log`) are primary; the trace is the fallback when artifacts are absent. For local sessions, the jsonl is the single source.
3. **Locate the layer.** Map the extracted signatures to the ladder. The verdict layer is the *deepest* layer reached with a failure signature — deeper layers must show no failure signatures, else the diagnosis is incomplete.
4. **Verify against baselines** before calling a run abnormal (see Baselines).
5. **Report using the conclusion template.** Output is Chinese for the user.

Completion criterion: every signature the script extracted is either explained by the verdict layer or explicitly ruled incidental — an unexplained 504 is an unfinished diagnosis, not noise.

## Local sessions

`~/.opencodereview/sessions/<munged-cwd>/<uuid>.jsonl` records every local `ocr review` run: `session_start` (cwd/branch/model/range), `llm_request`/`llm_response` (duration_ms + usage), `llm_error`, `tool_call`, `review_item_failed`, `session_end` (terminal_state + run_manifest, same manifest schema as CI's ocr-result.json). The script's `local` command classifies every `llm_error` and infers the effective `OCR_LLM_TIMEOUT` from the deadline-duration cluster:

- **挂满** (duration ≈ inferred timeout) → gateway hang: request waited the full timeout. Same class as CI's 504-at-timeout signature.
- **慢请求被切** (≥2min, below timeout) → per-file loop deadline cancelled the request mid-flight, or gateway cut the stream.
- **断流** (<2min) → gateway/stream broke early.
- `grouping_task` parse errors → the L4 gateway-returns-error-text signature; `401`/connection errors → L3.
- No `session_end` entry → the process was killed or interrupted (timeout kill / ctrl+c).
- tokens/file > 2× baseline → repeated file reads or looped review — worth a manual look even when the run "succeeded".

## The layer ladder

| # | Layer | Failure signatures | Verdict |
|---|-------|--------------------|---------|
| 1 | Pod scheduling | `ContainersNotReady`, init-permissions stuck | runner-side, not ocr's fault |
| 2 | before_script | clone `common-ci` failed, `vibecoding_login.sh` login failed | infra/credentials |
| 3 | ocr config | `ocr config set` error output, `ocr llm test` failed | gateway URL/token wrong |
| 4 | grouping | `LLM grouping failed (parse grouping JSON: invalid character ...)` | gateway returned error text instead of JSON; falls back to per-file (slower, not fatal) |
| 5 | per-file tasks | `Plan phase failed for group X: ... context deadline exceeded`, `Subtask error for group X: LLM completion error: context deadline exceeded` | per-group `OCR_REVIEW_TIMEOUT` hit; files cut, run is partial |
| 6 | post comments | `Successfully posted N/N` vs `posted N/M` | N/M = partial posting (MR moved / permissions); N/N = ok |
| 7 | artifacts upload | no artifacts at all | job died before upload → trace-only diagnosis |

## Reading retry_report (from `ocr-result.json`, schema `ocr.llm-retry-report/v1`)

- `504` + `duration_to_headers_ms ≈ OCR_LLM_TIMEOUT × 1000` → gateway hang: the request waited the full timeout before the gateway cut it. Not a client-side problem.
- `502` followed by retry `200` → gateway jitter; SDK `WithMaxRetries(5)` absorbs it. Incidental unless frequent.
- `context deadline exceeded` (no HTTP status) → the *per-file* review timeout expired mid-agentic-loop, distinct from the per-request timeout above. Two different clocks.
- `token_budget_reached` / `budget_exceeded` → `OCR_TOKENS_BUDGET` exhausted; ocr publishes partial results and exits 0 — a *success* job can still be partial.
- Job killed at exactly ~3600s → legacy 1h hard-timeout signature (`OCR_LLM_TIMEOUT=600` × 6 attempts = 3600s). Config-era fingerprint.
- Job log nearly empty but ran long → `--audience agent` trap: progress went to a sink the trace never shows. Retry the diagnosis via artifacts, not the log.

## Duration trend & speed-shift attribution

`durations` reports daily medians/p90/max of *success* jobs across groups, an optional `--since` before/after split (naive timestamps are interpreted as +08:00), and after-period per-project medians to locate stragglers. Per-project cap is 100 jobs (survey machinery) — trend counts are a lower bound.

Speed-shift attribution protocol (the shift day is the anchor, not the answer):

1. **Read the shift day from the daily table**, then check what landed near it — a common-ci merge, an ocr image bump (`ocr version` in a slow vs fast job trace; `latest` follows the ocr-image repo bump), a gateway change.
2. **Deep-diagnose one slow + one fast job from the same project** (`job` command) and compare **behavior**, not just duration: tokens/file and tool_calls/file dropped together with duration → the review *work itself* changed (config/model/image); same tokens/file but faster → infra (gateway latency) recovered.
3. **Credit trap**: a config merge landing near the shift gets credit for free. Verify with a real-endpoint test (same prompt, default vs your extra_body vs effort=low, compare latency/completion_tokens/reasoning_content) before attributing speed to config. Gateway recovery can mimic config effect — and it can regress back, so the config fix still lands.

Verified example (2026-09-08): 09-01~09-04 slow era (median 15.5min, plan request 300s no-header, tokens/file 189k) → 09-05 drop to 3.3min. Attribution: gateway recovery (real-endpoint test showed default still thinking but responding in 18-24s), not the budget-guard merge (09-03, no speed effect) — budget-guard only stopped the 1h hard-timeout losses.

## Frozen-config trap

A retried job does **not** re-resolve `include:`. If `pipeline.created_at` predates the common-ci merge that fixed the config, the retry still runs the old config — no signature will match the new behavior. Check pipeline timestamps against the common-ci commit before concluding "config didn't take effect". The fix is a new pipeline (push), never a retry.

## Baselines (normal, v1.11.x, effort=medium)

~120–129k tokens per file, ~10 tool_calls per file (`file_read` + `code_search` dominant), a 5-file MR takes 15–17min. A job at 3× these numbers is a real anomaly; at 1.2× it is not.

## Script

```bash
uv run scripts/diagnose_ocr_ci.py jobs <project-path-or-id>          # survey one project's CI jobs, failed first
uv run scripts/diagnose_ocr_ci.py job <project-path-or-id> <job-id>  # single CI job, artifacts→trace
uv run scripts/diagnose_ocr_ci.py groups <grp> [grp...] [--deep N]   # group survey, cross-group dedup
uv run scripts/diagnose_ocr_ci.py durations <grp> [--since ISO]     # success-job duration trend, speed-shift detection
uv run scripts/diagnose_ocr_ci.py local [uuid-prefix|path]           # local sessions: list, or diagnose one
uv run scripts/diagnose_ocr_ci.py analyze <file-or-dir>              # local ocr-result.json / stderr / trace
```

## Group survey

`groups` scans every project under one or more groups (both internal instances by default, reported separately), 12-way concurrent, < 3min for ~560 projects. It outputs: per-project status counts (failed first), failure-mode clustering by duration signature, failed-by-day loss distribution, over-long running jobs (stop-loss candidates). `--deep N` deep-diagnoses the N most recent failed jobs inline.

Group-survey knowledge baked in:
- **Cross-group dedup is mandatory**: a project shared across groups (e.g. a project shared between two groups) is returned by every group query — without dedup, failures double-count.
- Group IDs are **not unique across instances** (the same numeric group ID can resolve to different groups on gitlab.blue.example vs gitlab.red.example) and instance contents differ — never assume a group ID or its project list transfers.
- The survey stage alone classifies most failures via duration signatures: `job_execution_timeout` + duration ≈ 3600s → old-config 1h hard timeout (L5 config-era fingerprint); ≈ 7200s → 2h timeout; `runner_system_failure` → L1 infra. Deep-diagnose a handful of representative samples to confirm, then extrapolate to the group.
- Report template (Chinese): ①scope（X 项目扫描/Y 有 ocr-review）②主导失败模式 ③每项目失败表 ④按天损失 ⑤建议动作（重跑需 push 新提交防冻结配置陷阱，勿 retry）。

Script mechanics baked in (do not re-implement): glab-cli token parsed from `~/.config/glab-cli/config.yml` via **yaml, never regex**; multiple GitLab hosts tried in order (glab-config order; set `OCR_CI_HOST_PRIORITY` to pin the order, `--host` to pin one); every API call retried (GitLab 404s flap); project path URL-encoded with numeric-ID fallback (the ID is visible in runner pod names `runner-*-project-<ID>-*`); ANSI stripped from traces before matching. The script reports both failure signatures (which layer failed) and progress markers (how deep the job got) — a trace that reaches L5 then goes silent with zero `[ocr]` lines is the `--audience agent` trap, not a clean run.

## Conclusion template (Chinese, for the user)

```
## 诊断结论：job <id>（<project>，status=<status>，dur=<duration>s）
- 卡点层级：第 N 层（<层名>）
- 证据：<log/产物原文行，含行号或 JSON 路径>
- 根因：<为什么这一层失败>
- 建议动作：<重跑 / 调参（变量名+新值）/ 网关侧排查 / 等 common-ci 修复传播（新 pipeline 而非 retry）>
```

One recommendation per root cause; name the exact env var or config key to change.
