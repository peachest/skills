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

Platform-specific commands, API endpoints, and data formats:

- [GitLab reference](../mr-review-triage/reference/gitlab.md)
- [GitHub reference](../mr-review-triage/reference/github.md)

## Prerequisites

- MR/PR exists, CI pipeline has completed
- Platform CLI authenticated (GitLab: `glab`; GitHub: `gh`)
- Current branch matches the MR/PR source branch
- `/skill:fix` skill installed

## Process

Scripts live in the **mr-review-triage** skill directory. `<SCRIPTS_DIR>` below refers to its `scripts/` folder — resolve it before running the commands.

### 1. Pull

```bash
python3 <SCRIPTS_DIR>/ocr-pull-discussions.py <MR_OR_PR_ID> > /tmp/issues.json
```

Pulls OCR bot review comments. Output: JSON array of `{discussion_id, file, line, body}`, deduplicated.

MR/PR ID not given? Derive it from the branch name — see the platform reference doc.

**Completion criterion**: `/tmp/issues.json` exists and contains a valid JSON array.

### 2. Delegate to /fix

Invoke `/skill:fix` with `/tmp/issues.json` as input. Do not classify, verify, or fix findings yourself — that is `/skill:fix`'s job. `/skill:fix` runs its full process (gather → recommend → verify → grill → fix → verify build → report) and outputs `classified.json` — findings enriched with verdicts, reasons, fix plans, and resolved flags.

**Completion criterion**: `classified.json` exists with a verdict for every finding.

### 3. Post labels + resolve

```bash
cat classified.json | python3 <SCRIPTS_DIR>/ocr-post-labels.py <MR_OR_PR_ID>
```

For each finding: posts a reply with the verdict label + reason/fix-plan, and resolves the thread if the verdict's `resolved` flag is `true`.

On failure, fall back to manual commands — see the platform reference doc.

**Completion criterion**: every finding in `classified.json` has been posted (ok or failed count reported by the script).

### 4. Wrap up

Present the final state: fixed / failed / skipped counts, changed files, unresolved items. Leave changes in the working tree.

### 5. Reflect

If `/skill:fix` surfaced new FP patterns or coding insights, it writes them to `docs/agents/review-knowledge.md` and `docs/agents/coding-patterns.md` in the project. This step is `/skill:fix`'s responsibility; `/skill:triage-mr` only confirms it ran.

## Checkpoints

| # | When | Show | Decision |
|---|------|------|----------|
| 1 | After Step 1 | Pulled finding count | Proceed to /fix? |
| 2 | After Step 3 | Final summary | User confirms done |

## Resuming

If `classified.json` from a prior run exists, `/skill:fix` loads it and skips already-resolved findings. Re-run Step 1 with `--all` to re-pull including resolved threads if needed.
