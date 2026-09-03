---
name: mr-review-triage
description: Scripts and reference docs for pulling OCR review comments from GitLab MRs and GitHub PRs, posting classification labels, and resolving threads.
disable-model-invocation: true
---

# MR Review Triage — Scripts & References

Platform-specific scripts and reference docs for GitLab MR and GitHub PR review triage.

## Scripts

| Script | Purpose |
| ------ | ------- |
| `scripts/ocr-pull-discussions.py` | Pull review comments (OCR bot + human reviewers), deduplicated |
| `scripts/ocr-post-labels.py` | Post verdict labels + resolve threads |
| `scripts/ocr-verify-resolved.py` | Closure gate: exit 0 only when every resolvable thread is resolved |

## Backend modules

| Module | Platform |
| ------ | -------- |
| `scripts/ocr_platform.py` | Platform detection |
| `scripts/ocr_gitlab.py` | GitLab API client |
| `scripts/ocr_github.py` | GitHub API client |

## Reference docs

- [GitLab operations](reference/gitlab.md) — glab commands, discussion API, MR ID derivation, fallback note format, environment variables
- [GitHub operations](reference/github.md) — gh commands, review comment API, GraphQL resolve, bot detection, environment variables
- [Label templates](reference/templates.md) — report format, checkpoint brief, label reply formats
