---
name: triage-mr
description: Pull unresolved review comments from a remote MR/PR, delegate to /skill:fix for classification and repair, then post verdict labels and resolve threads.
disable-model-invocation: true
---

# Triage MR

Pull unresolved review comments from a remote MR or PR, hand them to `/skill:fix` for classification and repair, then post the verdicts back as labels and resolve the threads.

This skill is a thin orchestration layer. The classification, grilling, and fixing all live in `/skill:fix`. This skill owns only the remote-specific work: **pull**, **post labels**, and **resolve**.

## Architecture

```
/skill:triage-mr  (orchestration: pull → /fix → post labels → resolve)
    │
    ├── /fix  (classification + grill + fix + verify + report)
    │
    └── mr-review-triage  (scripts + platform reference docs)
```

## Platform support

GitLab and GitHub are both supported. The platform is auto-detected from `git remote get-url origin`:

- `github.com` in the remote URL → GitHub
- anything else → GitLab (self-hosted or gitlab.com)

Override with `OCR_PLATFORM=gitlab|github` env var.

The GitLab host, scheme (http/https), and token are derived automatically from the
git remote + glab config, so self-hosted instances (e.g. `internal.example.com`)
work without extra env vars. The OCR bot login is instance-specific — set
`OCR_BOT_LOGIN` when the bot isn't `gitblue.bot` (see the GitLab reference).

Platform-specific commands, API endpoints, and data formats:

- [GitLab reference](../mr-review-triage/reference/gitlab.md)
- [GitHub reference](../mr-review-triage/reference/github.md)

## Prerequisites

- MR/PR exists, CI pipeline has completed
- Platform CLI authenticated (GitLab: `glab`; GitHub: `gh`). For GitLab with
  multiple configured instances, confirm the target host is authenticated first:
  `glab auth status` — the scripts derive host + token from `git remote get-url
  origin` + glab config, and a wrong-instance token will 401.
- Current branch matches the MR/PR source branch
- `/skill:fix` skill installed

## Process

Scripts live in the **mr-review-triage** skill directory. `<SCRIPTS_DIR>` below refers to its `scripts/` folder — resolve it before running the commands.

A run is **not done** when post-labels returns ok. It is done when the closure gate (`ocr-verify-resolved.py`) exits 0 — every resolvable thread on the MR/PR resolved, including OCR summary discussions that the pull script intentionally skips (they carry only stats, but are resolvable threads). This is the single most common cause of a false "done".

### 1. Pull

```bash
python3 <SCRIPTS_DIR>/ocr-pull-discussions.py <MR_OR_PR_ID> > /tmp/issues.json 2>/tmp/pull-source.log
```

The script writes JSON to stdout and progress info to stderr — including the source MR/PR title, URL, and state, so the user can verify the pull came from the right MR. Keep them separate: **do not use `2>&1`**, which would corrupt the JSON output with progress text.

MR/PR ID not given? Derive it from the branch name — see the platform reference doc.

**Validate**: confirm the output is valid JSON and show the source identity:
```bash
# Show source identity (title, URL, state, finding count)
cat /tmp/pull-source.log
# Validate JSON
python3 -c "import json; d=json.load(open('/tmp/issues.json')); print(f'{len(d)} findings confirmed')"
```

**Completion criterion**: `/tmp/issues.json` exists, contains a valid JSON array, and the source MR/PR identity in `/tmp/pull-source.log` matches expectations.

### 2. Run /fix

Read `/skill:fix` and execute its full process (gather → recommend → verify → grill → fix → verify build → report) with `/tmp/issues.json` as input.

`/skill:fix` owns the classification logic — verdict definitions, the verify-before-grill ordering, the grilling process, and the fix workflow. Follow it as written. The verify-before-grill, grill-before-fix ordering is what makes verdicts trustworthy; shortcutting it produces shallow classifications.

The output is a classified list — each finding enriched with `classification`, `reason`, `fix_plan`, `priority`, and `resolved` fields. Build this file incrementally as each finding's verdict is finalized — do not assemble it by hand at the end. The fix skill defines the exact format.

**Isolate per MR.** Write state to `.triage/<MR_OR_PR_ID>/classified.json`, not a shared `.triage/classified.json`. A stale file from a prior MR or a prior round is the common cause of posting labels to the wrong discussion ids. `mkdir -p .triage/<MR_OR_PR_ID>`. Resuming an MR whose directory already exists is fine — `/skill:fix` skips already-resolved findings — but never reuse one MR's file for another.

`.triage/` is a per-user working directory, not project content. Add it to the **user's global** gitignore, not the project's `.gitignore`:
```bash
git config --global core.excludesfile ~/.gitignore_global 2>/dev/null
grep -qx '.triage/' ~/.gitignore_global 2>/dev/null || echo '.triage/' >> ~/.gitignore_global
```

**Completion criterion**: `.triage/<MR_OR_PR_ID>/classified.json` exists with a verdict for every finding.

### 3. Post labels + resolve

```bash
cat .triage/<MR_OR_PR_ID>/classified.json | python3 <SCRIPTS_DIR>/ocr-post-labels.py <MR_OR_PR_ID> --mode triage
```

For each finding: posts a reply with the verdict label + reason/fix-plan, and resolves the thread if the verdict's `resolved` flag is `true`.

`--mode triage` resolves TP (true-positive) findings, not the default "stay open for tracking". In a triage run the TP fix has already landed and been build-verified in-step, so leaving it open only creates a thread the closure gate will then fail on. Edge and Question stay open in both modes — they are genuinely unresolved.

On failure, fall back to manual commands — see the platform reference doc.

**Completion criterion**: every finding in `.triage/<MR_OR_PR_ID>/classified.json` has been posted (ok or failed count reported by the script).

### 4. Verify closure (the gate)

```bash
python3 <SCRIPTS_DIR>/ocr-verify-resolved.py <MR_OR_PR_ID>
```

Exits 0 only when **every resolvable thread** on the MR/PR is resolved. This catches OCR summary discussions that post-labels never touches (they are bot status notices with no finding to classify, so they are not in classified.json, yet they are resolvable threads). It also catches any inline thread whose resolve call silently failed.

**Completion criterion**: `ocr-verify-resolved.py` exits 0. This — not post-labels returning ok — is the done condition for the run.

If it exits 1: the script lists each open thread with a `[OCR summary]` tag where applicable. For OCR summary threads, reply with the fix/verdict context and resolve them (manual `glab api` / `gh api` — see the platform reference doc), then re-run the gate. Do not declare done while it exits 1.

### 5. Re-pull after push (detect new review rounds)

If you force-pushed commits during the run, the reviewer may post a new round of findings on the updated diff. Before declaring done, re-run Step 1 and compare the pulled discussion ids against `.triage/<MR_OR_PR_ID>/classified.json`:

- New ids not in the classified file → a new review round arrived. Run Steps 2–4 on the new findings (append to the same `.triage/<MR_OR_PR_ID>/classified.json`).
- No new ids → the run is genuinely complete.

A stale classified file from an earlier round is the common cause of posting labels to the wrong ids; the per-MR directory and this re-pull together close that gap.

### 6. Wrap up

Present the final state: fixed / failed / skipped counts, changed files, and the verify gate result. Leave changes in the working tree.

### 7. Reflect

If `/skill:fix` surfaced new FP patterns or coding insights, it writes them to `docs/agents/review-knowledge.md` and `docs/agents/coding-patterns.md` in the project. This step is `/skill:fix`'s responsibility; `/skill:triage-mr` only confirms it ran.

## Checkpoints

| # | When | Show | Decision |
|---|------|------|----------|
| 1 | After Step 1 | Source MR/PR identity + pulled finding count | Proceed to /fix? |
| 2 | After Step 4 (gate) | Verify result: 0 open threads, or N open with list | If N>0: resolve remaining, re-run gate. If 0: done. |

## Resuming

If `.triage/<MR_OR_PR_ID>/classified.json` from a prior run exists, `/skill:fix` loads it and skips already-resolved findings. Re-run Step 1 with `--all` to re-pull including resolved threads if needed.
