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

Platform detection, env overrides (`OCR_PLATFORM`, `OCR_REMOTE`), the auth
probe, and the `glab mr` host-inference boundary: [platform reference](../mr-review-triage/reference/gitlab.md).

## Prerequisites

- MR/PR exists. CI 门语义：**post 不设门**（join/anchor 校验针对 pull 快照，
  与 CI 无关；每轮裁决后直接跑，见追尾规则）；**pull 与 verify 受门**：
  CI in-flight 时 exit 2（`--skip-pipeline-check` 是这两个脚本的逃生门）。
- Platform CLI authenticated (`glab` / `gh`; multi-instance: `glab auth status`
  first). Current branch matches the MR/PR source branch. `/skill:fix` installed.

## Process

`<SCRIPTS_DIR>` = the mr-review-triage skill's `scripts/` folder — resolve
against the injected skill location; do not search other skill roots.

```
pull (pipeline gate; stage to .triage/<MR>/issues.json, never /tmp)
  → loop { /fix 产出裁决语义 → verdict.py <MR> <no> ... 逐条即时落盘
          → post 当轮已裁决条目（post 不设门，不等 CI） }
  → verify --pull-file（pipeline 完结后再跑；exit 0 = done）
force-push 后：pull --digest --against 对账 → 新 findings 回到循环
```

**追尾规则**：OCR bot 对每次 push 追评一轮，而修复本身又触发新 pipeline。
post 推迟到 CI 终态之后 = 裁决→push→新 pipeline→gate 拦截→再 push 的死循环
（MR !6 积压 47 条未 resolve 线程）。正确节奏：**每轮 verdict 落盘后立即
post 当轮条目**，CI 门只挡 verify 与跨轮 pull；push 触发的新一轮评审由下一
次 pull 消费。Full evidence: patterns.md P-010.

State lives in `.triage/<MR_OR_PR_ID>/`: `issues.json` written by pull,
`classified.json` written by `verdict.py` (post updates only `posted` flags).
All scripts resolve `.triage/` against the current working directory (realpath)
— run every platform call from the same checkout root you staged state in
(wrong cwd surfaces as 404 from platform endpoints — fix the cwd, the endpoint
is not broken). A run is
**not done** when post returns ok — only when the verify gate exits 0.

### 1. Pull

```bash
mkdir -p .triage/<MR_OR_PR_ID>
python3 <SCRIPTS_DIR>/ocr-pull-discussions.py <MR_OR_PR_ID> \
  > .triage/<MR_OR_PR_ID>/issues.json 2> .triage/<MR_OR_PR_ID>/pull-source.log
```

Keep stdout and stderr separate — **`2>&1` corrupts the JSON**. Stage at
`.triage/<MR_OR_PR_ID>/issues.json`, never /tmp: that exact path is what
verdict.py, post, and verify join against. CI in-flight → exit 2; re-run after
it completes or pass `--skip-pipeline-check`. MR id derivation from the branch
name: platform reference doc.

**Completion criterion**: `pull-source.log` shows the expected source identity
(0 findings is a platform-derivation red flag — check `OCR_REMOTE`), and
`issues.json` is a valid JSON array.

### 2. Classify: /fix + the verdict.py loop

Read `/skill:fix` and run its process with `issues.json` as input. In triage
mode /fix produces **verdict semantics only** (ordinal, classification, reason,
fix plan, priority) — it never writes `classified.json`.

The moment each verdict is finalized, call:

```bash
python3 <SCRIPTS_DIR>/verdict.py <MR_OR_PR_ID> <no> --class TP \
  --reason "confirmed: <evidence>" --fix-plan "<plan>" --priority high
```

`verdict.py` is the **sole writer** of `classified.json` — byte-exact
`discussion_id` copy, anchor, atomic schema-2 append. Hand-writing or batch-at-
end assembly is a process violation (P-002). Flag table, per-item `resolved`
semantics (decided at verdict time: Edge defaults resolved, Q stays open
unless explicit, TP/FP/OOS defer to post's mode map), and exit codes: see the
[verdict reference](../mr-review-triage/reference/verdict.md). Success echoes
`no + author + first line` — check it against the finding you meant.

**Isolate per MR.** One `.triage/<MR_OR_PR_ID>/` per MR, never shared or
reused across MRs (stale state = verdicts posted to wrong threads). Add
`.triage/` to the user's global gitignore.

**Completion criterion**: `classified.json` has a verdict for every finding.

### 3. Post labels + resolve

```bash
python3 <SCRIPTS_DIR>/ocr-post-labels.py <MR_OR_PR_ID> --mode triage \
  --classified .triage/<MR_OR_PR_ID>/classified.json
```

One call does everything — there is no manual fallback: join + anchor
validation before any platform call, content-dedup idempotent replies,
per-item resolve execution, OCR summary sweep (🔍 confirm / ✅ stats+resolve /
⚠️ escalate and **never resolve**), `posted` write-back. Script semantics and
failure taxonomy: [post reference](../mr-review-triage/reference/post.md).

Script errors are script bugs: fix the script or report — a hand-written
`glab api` bypasses join validation and dedup, re-creating the incident family
this pipeline exists to prevent.

**Completion criterion**: exit 0, then run `verify --json` immediately and read
the open count（resolve 校验不依赖 CI，这一步不等 pipeline）——ok 计数经读回确认，
但 verify 的 open 计数是唯一平台侧终态。A non-zero exit caused **solely** by
⚠️ error-class summary threads is expected (gate stays red, human-in-loop by
design) — proceed to Step 4 and report. Failed classified items → fix the
cause, re-run (idempotent).

### 4. Verify closure (the gate)

```bash
python3 <SCRIPTS_DIR>/ocr-verify-resolved.py <MR_OR_PR_ID>
# machine-readable open-thread list: append --json
# --pull-file <path> overrides the default .triage/<MR>/issues.json mapping source
```

Exit 0 = every resolvable thread resolved + CI finished. Exit 1 = open threads
or backend error (fail closed); exit 2 = CI in flight or usage error. Threads
are labeled by pull-file ordinal or content anchor — never platform id. The
gate staying red on an ⚠️ error round is **intentional human-in-loop design**
— report it; resolving it yourself to force green is a violation. When the
gate contradicts your own observation, trust neither blindly — re-examine both
counting rules before concluding.

**Completion criterion**: exit 0.

### 5. Re-pull after push (detect new review rounds)

```bash
python3 <SCRIPTS_DIR>/ocr-pull-discussions.py <MR_OR_PR_ID> \
  --digest --against .triage/<MR_OR_PR_ID>/classified.json > /dev/null
```

stderr reports `N pulled, M already classified, K new`:

- **K = 0** → the run is genuinely complete.
- **K > 0** → refresh with a **full** pull (post join-validates *every*
  classified entry against the pull file — a digest-only file fails the
  round-1 entries), run the Step-2 loop on the new ordinals, re-run Steps 3–4.
  Ordinals are single-round pointers; cross-round identity is
  `discussion_id` + anchor. A wrong-author echo = the pull file changed under
  you — full re-pull, re-check before any `--force`.

### 审查循环上限（hard rule）

re-pull 会把复审轮次接回循环，但对**同一 finding**（跨轮身份 = `discussion_id`
+ anchor）的「修复 → 复审」往复最多 **2 轮**。第 2 轮复审仍提出同一问题时停下：

- verdict 保持该 finding 的诚实裁决，**不得为凑绿改判**（TP 改 OOS/FP 之类）；
  状态如实记 fix failed，gate 保持红是有意设计。
- 上报用户：**blocked** + 已尝试的每轮修复（每轮一行）+ 剩余分歧点，由用户裁决
  下一步；禁止静默开始第 3 轮。

与既有机制的关系：verdict.py 的拒重复记录是**状态去重**、不是轮数控制，两者不
重复计数；Edge 默认 resolved 只发生在 verdict 时刻，不受本上限影响；复审轮中
的**新** finding（不同 discussion_id/anchor）照常进入循环，不计入同 finding
的 2 轮上限。

### 6. Wrap up

Present the final state: fixed / failed / skipped counts, changed files, and
the verify gate result. **MR 创建一律转 `/skill:create-mr`**（remote/target/
draft 确认流程），禁裸 `glab mr create` / `gh pr create`（审计：96 session
裸建，2 例失约点在本 skill 会话内）。

## Checkpoints

| # | When | Show | Decision |
|---|------|------|----------|
| 1 | After Step 1 | Source MR/PR identity + pulled finding count | Proceed to /fix? |
| 2 | After Step 3 | Post result: replied/deduped/failed + summary sweep outcome | Failed item → fix cause, re-run (idempotent). |
| 3 | After Step 4 (gate) | Verify result: 0 open, or N open with list | N>0: an open `no=` that never went through Step 2 → return to Step 2 for that finding; otherwise fix per gate output, re-run gate. 0: done. |

## Resuming

A prior run's `.triage/<MR_OR_PR_ID>/` is resumable: re-run Step 1 (add `--all`
to include resolved threads) and continue the loop. `verdict.py` refuses to
double-record a finding — matched by thread + body anchor, not ordinal (ordinals
reshuffle across pulls) — and prints the existing entry's ordinal; `--force`
replaces a stale verdict deliberately. Never reuse one MR's directory for
another.
