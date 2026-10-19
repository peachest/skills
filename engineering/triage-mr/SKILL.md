---
name: triage-mr
description: Pull unresolved review comments from a remote MR/PR, delegate to /skill:fix for classification and repair, then post verdict labels and resolve threads.
disable-model-invocation: true
---

# Triage MR

Run a scripted triage pipeline over a remote MR or PR: pull unresolved review
comments into per-MR state, classify each finding via `/skill:fix`, record
verdicts with `verdict.py`, post labels + resolve threads, and close with a
verify gate. The agent's working interface is **ordinals + verdict semantics** —
opaque platform ids never pass through human hands or human-readable output.

## Architecture

```
/skill:triage-mr  (orchestration: pull → /fix + verdict loop → post → verify)
    │
    ├── /fix  (classification + grill + fix + verify + report)
    │
    └── mr-review-triage  (scripts + platform reference docs)
```

## Platform support

GitLab and GitHub are both supported. The platform is auto-detected from
`git remote get-url origin`:

- `github.com` in the remote URL → GitHub
- anything else → GitLab (self-hosted or gitlab.com)

Environment overrides (read by the scripts at startup):

- `OCR_PLATFORM=gitlab|github` — force the platform. Also skips the startup
  auth probe, since the remote→host derivation the probe validates is bypassed.
- `OCR_REMOTE=<name>` — which git remote the platform/host/token derivation
  reads (default `origin`). Fork-type repos — `origin` pointing at the public
  upstream, the review instance on another remote — must set this, or the
  scripts silently pull unrelated upstream data that looks like "0 findings".

The GitLab host, scheme (http/https), and token are derived automatically from
the selected remote + glab config, so self-hosted instances (e.g.
`gitlab.red.example`) work without extra env vars. A startup auth probe
compares the derived instance's project path against the local remote, so a
valid token on the wrong instance fails before the first data call.

**Boundary**: `glab mr` subcommands infer the host from the cwd git remote and
cannot be redirected by env vars. In a fork repo, derive the MR id through the
script API path or `glab mr list -R <full remote URL>` — see the GitLab
reference. GitHub bot detection uses `OCR_BOT_LOGIN` (default
`github-actions[bot]`); GitLab no longer filters by author.

Platform-specific commands, API endpoints, and data formats:

- [GitLab reference](../mr-review-triage/reference/gitlab.md)
- [GitHub reference](../mr-review-triage/reference/github.md)

## Prerequisites

- MR/PR exists and CI on the head ref has finished — pull and verify run a
  pipeline timing gate and exit 2 while it is in flight
  (`--skip-pipeline-check` is the explicit escape hatch).
- Platform CLI authenticated (GitLab: `glab`; GitHub: `gh`). For GitLab with
  multiple configured instances, confirm the target host is authenticated first:
  `glab auth status` — the scripts derive host + token from the selected
  remote + glab config, and a wrong-instance token will 401.
- Current branch matches the MR/PR source branch
- `/skill:fix` skill installed

## Process

Scripts live in the **mr-review-triage** skill directory. `<SCRIPTS_DIR>` below
refers to its `scripts/` folder — resolve it against the mr-review-triage
location shown when the skill is injected (its own SKILL.md states the full
rule); do not search other skill roots.

```
pull (pipeline gate; stage to .triage/<MR>/issues.json, never /tmp)
  → loop { /fix 产出裁决语义 → verdict.py <MR> <no> ... 逐条即时落盘 }
  → post --mode triage --pull-file（join/anchor/dedup/summary sweep 全脚本内）
  → verify --pull-file（pipeline 完结后再跑；exit 0 = done）
force-push 后：pull --digest --against 对账 → 新 findings 回到循环
```

State lives in `.triage/<MR_OR_PR_ID>/`: `issues.json` is written by pull,
`classified.json` is written by `verdict.py` (post updates only its `posted`
flags). All scripts resolve `.triage/` against the current working directory
(realpath) — run every command from the same checkout root you staged state in.

A run is **not done** when post-labels returns ok. It is done when the closure
gate (`ocr-verify-resolved.py`) exits 0 — every resolvable thread on the MR/PR
resolved, including OCR summary discussions that the pull script intentionally
skips (they carry only stats, but are resolvable threads; post sweeps them).
This is the single most common cause of a false "done".

### 1. Pull

```bash
mkdir -p .triage/<MR_OR_PR_ID>
python3 <SCRIPTS_DIR>/ocr-pull-discussions.py <MR_OR_PR_ID> \
  > .triage/<MR_OR_PR_ID>/issues.json 2> .triage/<MR_OR_PR_ID>/pull-source.log
```

The script writes the JSON findings array to stdout and progress to stderr —
including the source MR/PR title, URL, and state, so you can verify the pull
came from the right MR. Keep them separate: **do not use `2>&1`**, which would
corrupt the JSON. Stage the JSON at `.triage/<MR_OR_PR_ID>/issues.json`, never
/tmp — that exact path is what `verdict.py`, post, and verify join against.
While CI on the head ref is still running, the script exits 2; re-run after it
completes or pass `--skip-pipeline-check` explicitly.

MR/PR ID not given? Derive it from the branch name — see the platform
reference doc (fork repos: mind the glab host-inference boundary above).

**Validate**: confirm the source identity and the JSON shape:
```bash
# Source identity (platform, title, URL, state, counts)
cat .triage/<MR_OR_PR_ID>/pull-source.log
# Validate JSON
python3 -c "import json; d=json.load(open('.triage/<MR_OR_PR_ID>/issues.json')); print(f'{len(d)} findings, no 1..{len(d)}')"
```

0 findings is not automatically good news — the log names the derived
platform/target. A fork repo with a wrong derivation pulls the wrong repo and
prints "0 findings"; point `OCR_REMOTE` at the remote hosting the review
instance and re-pull.

**Completion criterion**: `.triage/<MR_OR_PR_ID>/issues.json` exists, contains
a valid JSON array, and the source identity in the log matches expectations.

**Scope note**: the pull includes comments from both the OCR bot and human
reviewers — inline findings, fallback notes, and general (non-inline) reviewer
threads (`file="(general)"`, `line=0`). This keeps the pull aligned with the
closure gate, which counts every resolvable thread regardless of author. OCR
summary/LGTM/error status threads are excluded (no finding to classify) but are
resolvable — post sweeps them in Step 3.

### 2. Classify: /fix + the verdict.py loop

Read `/skill:fix` and execute its full process (gather → recommend → verify →
grill → fix → verify build → report) with
`.triage/<MR_OR_PR_ID>/issues.json` as input. In triage mode `/skill:fix` owns
the verdict logic — verdict definitions, the verify-before-grill ordering, the
grilling process, and the fix workflow — but produces **verdict semantics
only**: the ordinal, classification, reason, fix plan, priority. It never
writes `classified.json` itself.

The moment each verdict is finalized, call:

```bash
python3 <SCRIPTS_DIR>/verdict.py <MR_OR_PR_ID> <no> --class TP \
  --reason "confirmed: <evidence>" --fix-plan "<plan>" --priority high
```

`verdict.py` is the **sole writer** of
`.triage/<MR_OR_PR_ID>/classified.json`: it copies the finding's
`discussion_id` byte-exact from `issues.json`, computes the body anchor
(`sha256(body)[:16]`), and atomically appends or replaces exactly one schema 2
entry per call. Hand-writing or hand-editing that file is a process violation.
Calling `verdict.py` once in a batch at the end of the run instead of per
finalized verdict is the same violation (P-002) — the point is that an
interrupted run leaves no unrecorded verdicts.

| Flag | Meaning |
|------|---------|
| `--class TP\|FP\|Edge\|OOS\|Q` | required; `Q` is the stored form of Question |
| `--reason` | required; carries the verifying evidence |
| `--fix-plan` | required for TP (post skips TP entries without one) |
| `--priority high\|medium\|low` | TP only |
| `--resolved true\|false` | per-item resolve decision; default Edge=true, Q=false, others unset |
| `--force` | replace an existing verdict for the same finding |

Per-item `resolved` semantics — the close-after-verification decision is made
at **verdict time** and post only executes it: Edge defaults to resolved (real
but low-priority; leaving it open would keep the gate red forever), Question
stays open unless you explicitly pass `--resolved true`, and TP/FP/OOS leave
the field unset so post applies its mode map (in triage mode TP resolves — the
fix has already landed and been build-verified in-step).

Success echoes `no + author + first body line` — check it against the finding
you meant before moving on; a misremembered ordinal is caught here, not on the
MR. Exit codes: 0 ok · 1 state error (missing pull file, unknown ordinal,
existing verdict without `--force`) · 2 usage error.

**Isolate per MR.** State lives in `.triage/<MR_OR_PR_ID>/`, never a shared
`.triage/classified.json`. A stale file from a prior MR or a prior round is the
common cause of posting verdicts to the wrong threads. Resuming an MR whose
directory already exists is fine (see Resuming), but never reuse one MR's
directory for another.

`.triage/` is a per-user working directory, not project content. Add it to the
**user's global** gitignore, not the project's `.gitignore`:
```bash
git config --global core.excludesfile ~/.gitignore_global 2>/dev/null
grep -qx '.triage/' ~/.gitignore_global 2>/dev/null || echo '.triage/' >> ~/.gitignore_global
```

**Completion criterion**: `.triage/<MR_OR_PR_ID>/classified.json` exists with a
verdict for every finding.

### 3. Post labels + resolve

```bash
python3 <SCRIPTS_DIR>/ocr-post-labels.py <MR_OR_PR_ID> --mode triage \
  --classified .triage/<MR_OR_PR_ID>/classified.json
```

One script call does everything — there is no manual fallback:

- **Join + anchor validation** before any platform call: every entry's
  `discussion_id` must byte-match the pull state file and its anchor must
  reproduce from the same file's body. A truncated or hand-typed id dies here,
  loudly, naming the entry's ordinal — never reach the platform.
- **Reply** with the verdict label + reason/fix-plan, skipped when the thread
  already carries the entry's anchor marker (content dedup — re-runs are
  idempotent, including where the `posted` flag is missing).
- **Resolve** iff the entry's per-item `resolved` field says so — post executes
  the verdict-time decision, it never re-judges. A thread whose reply failed is
  never resolved (`--force` overrides at the operator's risk).
- **Summary sweep**: after the classified entries, the script sweeps the
  remaining resolvable OCR summary threads itself — 🔍 start threads get a
  confirmation note, ✅ end/LGTM threads get this round's verdict statistics
  then resolve, ⚠️ error threads get a fixed escalation note and are **never
  resolved** (post exits non-zero).
- **posted flags** are written back to the `--classified` file.

Both post and verify join against `.triage/<MR_OR_PR_ID>/issues.json` by
default; pass `--pull-file <path>` only when state was staged elsewhere.

Script errors are script bugs: fix the script or report the failure — never
work around them with hand-written `glab api` / `gh api` calls. A hand-written
call bypasses join validation, dedup, and posted bookkeeping, and re-creates
the incident family this pipeline exists to prevent.

**Completion criterion**: post exits 0 — every finding replied (or deduped) and
resolved per its verdict, summary sweep clean.

### 4. Verify closure (the gate)

```bash
python3 <SCRIPTS_DIR>/ocr-verify-resolved.py <MR_OR_PR_ID>
```

Exits 0 only when every resolvable thread is resolved and CI on the head ref
has finished. Exit 1 = open threads or a backend error (fail closed), listed on
stderr; exit 2 = CI still in flight (`--skip-pipeline-check` overrides) or a
usage error. Human output labels threads by pull-file ordinal (`no=<N>`) or, for
threads outside the pull file, a short content anchor — never by platform id;
the `[N/M notes open]` annotation is load-bearing.

The gate staying red on an ⚠️ error round is **intentional human-in-loop
design**: an error summary announces that the review round itself failed, and
auto-resolving it would advertise success. Report it to the user and let them
decide (e.g. re-run the review); resolving it yourself to force the gate green
is a process violation.

When the gate's output contradicts your own observation, trust neither blindly
— re-examine the scan's counting rules and the script's blind spots before
concluding. Resolving the contradiction by rationalizing one side away is a
process violation.

**Completion criterion**: `ocr-verify-resolved.py` exits 0.

### 5. Re-pull after push (detect new review rounds)

If you force-pushed commits during the run, the reviewer may post a new round
on the updated diff. Reconcile before declaring done:

```bash
python3 <SCRIPTS_DIR>/ocr-pull-discussions.py <MR_OR_PR_ID> \
  --digest --against .triage/<MR_OR_PR_ID>/classified.json > /dev/null
```

stderr reports `N pulled, M already classified, K new` and names new findings
by ordinal:

- **K = 0** → no new round; the run is genuinely complete.
- **K > 0** → refresh the full pull file
  (`ocr-pull-discussions.py <MR_OR_PR_ID> > .triage/<MR_OR_PR_ID>/issues.json`),
  run the Step-2 loop on the new ordinals, then re-run Steps 3–4. The refresh
  must be a **full** pull, not the digest output: post join-validates *every*
  classified entry against the pull file, and a digest-only file (new findings
  only) would fail the round-1 entries. Ordinals are stable across re-pulls;
  if a `verdict.py` echo names the wrong author or first line, an ordinal
  shifted — re-check the finding and use `--force` to replace a stale verdict.

The per-MR directory plus this reconciliation together close the
stale-classified-file gap.

### 6. Wrap up

Present the final state: fixed / failed / skipped counts, changed files, and
the verify gate result. Leave changes in the working tree. If `/skill:fix`
surfaced no new FP patterns or coding insights, skip the reflect step — it is
`/skill:fix`'s responsibility, not this skill's.

**MR 创建一律转 `/skill:create-mr`**：修复结论需要落地为 MR/PR 时，走
create-mr 的确认流程（remote / target branch / draft），不要裸 `glab mr create`
或 `gh pr create`。审计背景（2026-10-19）：全库 96 个 session 裸建 MR 未走
create-mr，其中 2 个失约点就发生在 triage-mr 会话内（修复顺手裸建）。

## Checkpoints

| # | When | Show | Decision |
|---|------|------|----------|
| 1 | After Step 1 | Source MR/PR identity + pulled finding count | Proceed to /fix? |
| 2 | After Step 3 | Post result: per-item replied/deduped/failed + summary sweep outcome | Any failed item? Fix the cause, re-run post (idempotent). |
| 3 | After Step 4 (gate) | Verify result: 0 open threads, or N open with list | N>0: handle per gate output, re-run gate. 0: done. |

## Resuming

A prior run's `.triage/<MR_OR_PR_ID>/` is resumable: re-run Step 1 (add `--all`
to re-pull including resolved threads) and continue the loop. `verdict.py`
refuses to double-record a finding that already has an entry — matched by
thread + body anchor, not ordinal, because ordinals reshuffle across pulls —
and prints the existing entry's ordinal; pass `--force` to replace a stale
verdict deliberately. Never reuse one MR's directory for another.
