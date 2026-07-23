---
name: mr-review-triage
description: Scripts and reference docs for pulling OCR review comments from GitLab MRs and GitHub PRs, posting classification labels, and resolving threads. Used by /skill:triage-mr.
disable-model-invocation: true
---

# MR Review Triage — Scripts & References

This skill holds the **platform-specific scripts and reference docs** consumed by `/skill:triage-mr`. It is not invoked directly — `/skill:triage-mr` orchestrates the flow, and `/skill:fix` handles classification and repair.

## Architecture

```
/triage-mr  (orchestration: pull → /fix → post labels → resolve)
    │
    ├── /fix  (classification + grill + fix + verify + report)
    │
    └── mr-review-triage  (this skill: scripts + platform reference docs)
```

## Scripts

All scripts auto-detect the platform (GitLab or GitHub) from `git remote`.

| Script | Purpose |
| ------ | ------- |
| `scripts/ocr-pull-discussions.py <MR_OR_PR_ID>` | Pull OCR bot review comments, deduplicated |
| `scripts/ocr-post-labels.py <MR_OR_PR_ID>` | Post verdict labels + resolve threads |

### Platform detection

`scripts/ocr_platform.py` — `detect_platform()` reads `git remote get-url origin`:
- `github.com` in URL → GitHub
- anything else → GitLab

Override with `OCR_PLATFORM=gitlab|github` env var.

### Backend modules

| Module | Platform |
| ------ | -------- |
| `scripts/ocr_gitlab.py` | GitLab API client (`curl`, `get_project_id`) |
| `scripts/ocr_github.py` | GitHub API client (`curl`, `graphql`, `get_project_id`) |

## Reference docs

- [GitLab operations](reference/gitlab.md) — glab commands, discussion API, MR ID derivation, fallback note format, environment variables
- [GitHub operations](reference/github.md) — gh commands, review comment API, GraphQL resolve, bot detection, environment variables
- [Label templates](reference/templates.md) — report format, checkpoint brief, label reply formats
