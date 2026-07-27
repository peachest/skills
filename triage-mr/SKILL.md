---
name: triage-mr
description: Pull unresolved review comments from a remote MR/PR, delegate to /skill:fix for classification and repair, then post verdict labels and resolve threads. Use when you want to triage and act on OCR bot review comments on a GitLab MR or GitHub PR.
disable-model-invocation: true
---

# Triage MR

Pull unresolved review comments from a remote MR or PR, hand them to `/skill:fix` for classification and repair, then post the verdicts back as labels and resolve the threads.

This skill is a thin orchestration layer. The classification, grilling, and fixing all live in `/skill:fix`. This skill owns only the remote-specific work: **pull**, **post labels**, and **resolve**.

## Platform support

GitLab and GitHub are both supported. The platform is auto-detected from `git remote get-url origin`:

- `github.com` in the remote URL → GitHub
- anything else → GitLab (self-hosted or gitlab.com)

Platform-specific commands, API endpoints, and data formats:

- [GitLab reference](../mr-review-triage/reference/gitlab.md)
- [GitHub reference](../mr-review-triage/reference/github.md)

## Prerequisites

- MR/PR exists, CI pipeline has completed
- Platform CLI authenticated (GitLab: `glab`; GitHub: `gh`)
- Current branch matches the MR/PR source branch
- `/skill:fix` skill installed

## Scripts

All scripts live in the `mr-review-triage` skill directory. Use `<SKILL_DIR>` to resolve them — both skills share the same scripts.

## Process

### 1. Pull

```bash
python3 <SKILL_DIR>/scripts/ocr-pull-discussions.py <MR_OR_PR_ID> > /tmp/issues.json
```

The script auto-detects the platform and pulls OCR bot review comments. Output: JSON array of `{discussion_id, file, line, body}`, deduplicated.

MR/PR ID not given? Derive it from the branch name — see the platform reference doc.

**Completion criterion**: `/tmp/issues.json` exists and contains a valid JSON array.

### 2. Delegate to /fix

Pass `/tmp/issues.json` to `/skill:fix`. The `/skill:fix` skill runs its full process:

1. Gather context (read code, ADRs, review-knowledge)
2. Recommend verdicts
3. Verify each claim
4. Grill fix plans
5. Fix TP + selected Edge
6. Verify (build/test)
7. Report

`/skill:fix` outputs `classified.json` — the findings enriched with verdicts, reasons, fix plans, and resolved flags.

**Completion criterion**: `classified.json` exists with a verdict for every finding.

### 3. Post labels + resolve

**Must execute.** Do not skip.

```bash
cat classified.json | python3 <SKILL_DIR>/scripts/ocr-post-labels.py <MR_OR_PR_ID>
```

The script auto-detects the platform. For each finding, it:

1. Posts a reply with the verdict label + reason/fix-plan
2. Resolves the thread if the verdict's `resolved` flag is `true`

On failure, fall back to manual commands — see the platform reference doc.

**Completion criterion**: every finding in `classified.json` has been posted (ok or failed count reported by the script).

### 4. Wrap up

Present the final state: fixed / failed / skipped counts, changed files, unresolved items. Do not auto-commit or push.

### 5. Reflect

If `/skill:fix` surfaced new FP patterns or coding insights, it writes them to `docs/agents/review-knowledge.md` and `docs/agents/coding-patterns.md` in the project. This step is `/skill:fix`'s responsibility; `/skill:triage-mr` only confirms it ran.

## Checkpoints

| # | When | Show | Decision |
|---|------|------|----------|
| 1 | After Step 1 | Pulled finding count | Proceed to /fix? |
| 2 | During /fix Step 2 | Verdict summary table | User confirms verdicts |
| 3 | During /fix Step 4 | Each TP fix plan | User confirms plan |
| 4 | During /fix Step 5 | Each TP/Edge: fix/discuss/skip | User chooses |
| 5 | After /fix Step 6 | Build/test result | User approves → post labels |
| 6 | After Step 3 | Final summary | User confirms done |

## Resuming

If `classified.json` from a prior run exists, `/skill:fix` loads it and skips already-resolved findings. Re-run Step 1 with `--all` to re-pull including resolved threads if needed.
