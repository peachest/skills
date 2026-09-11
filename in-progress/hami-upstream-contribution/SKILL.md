---
name: hami-upstream-contribution
description: >
  Contribute to Project-HAMi upstream (github.com/Project-HAMi/HAMi) — the
  six enforced AI contribution gates, issue-first workflow, stacked-PR setup,
  and CI lint internals (merge-ref testing, license header check, pinned
  golangci-lint). Use when preparing or reviewing a PR/issue for HAMi
  upstream, or when a HAMi PR's lint/CI check fails.
---

# HAMi Upstream Contribution

## Gates (CONTRIBUTING.md — enforced on all contributions)

1. **Author-understanding**: maintainers may ask how the change works; an
   author who cannot explain it gets the PR closed.
2. **Hardware validation**: changes affecting device allocation or
   in-container isolation must be validated on real hardware; the PR records
   device model and driver version. Scheduler-extender-only changes may use
   unit tests instead.
3. **Scope and commit messages**: large AI-generated PRs are rejected;
   anything beyond a small fix must start as an issue and be split into
   reviewable commits; **commit messages must be hand-written** —
   AI-generated messages are rejected.
4. **Review replies** must be hand-written and engage the specific point.
5. **Commit trailer hygiene**: no AI co-author/assisted-by trailers;
   disclosure belongs in the PR description only.
6. **No AI-generated comments** in review threads (translation/formatting
   assistance is fine when the technical assessment is the author's own and
   the output is verified).

AI assistance **must** be disclosed in the PR description, with extent
(docs only vs code generation).

## Process

- **Issue first** for anything beyond a small fix. The issue describes
  observed symptoms with a minimal reproduction; the root-cause analysis
  goes in the PR, not the issue. Attach hardware evidence (screenshots of
  real-cluster reproduction) — it satisfies gate 2 visibility.
- **Stack**: base the feat branch on the fix branch head; feat PR says
  "Depends on #<fix-PR>"; once the fix merges, the stacked diff
  auto-shrinks. A reworded fix commit has a new hash — rebase the stack
  onto it (`git rebase --onto <new> <old>`) or the stack keeps the stale
  base.
- **Local draft only**: prepare issue text, PR body, and any comment as
  local files for the user to review and publish via web UI. Never create
  or post anything upstream on the user's behalf.
- **Style**: AI-drafted issues/PRs are spotted by excess structure and
  detail — keep issues symptom-level, PR bodies short; the user hand-writes
  commit messages and adds `Signed-off-by` (DCO check runs).

## CI lint internals

- The `lint` job runs four steps: `hack/verify-license.sh` (addlicense) →
  `make tidy` → golangci-lint (version pinned in `.github/workflows/ci.yaml`)
  → `hack/verify-import-aliases.sh`. All four must pass; a failure in any
  one reports as "lint".
- New `.go` files need the Apache header
  (`Copyright 2024 The HAMi Authors.`) — verify-license fails without it.
- PR CI runs the **merge ref** (branch × latest master): upstream master
  breakage fails *your* PR's lint. Before debugging your diff, check
  upstream master's CI runs; if master is red, wait for the fix and re-run
  the failed checks. (Precedent: #2836 shipped a duplicate
  `effectivePodDeviceUsage` declaration, master CI red, every open PR's
  lint failed, 2026-09.)
- Merge gate (`tide`) needs `approved` + `lgtm` labels.

## Internal fork vs upstream polarity

The two targets have opposite conventions — never mix them up:

| | internal fork (team/platform/hami/HAMi) | Project-HAMi upstream |
|---|---|---|
| Copyright headers on new files | none (fork-owned) | required (Apache) |
| AI disclosure | not in commit messages | required in PR description |

Remotes in the main repo (`~/projects/HAMi`): `origin` = the internal fork,
`github` = upstream, `hyx-fork` = `git@github.com:peachest/HAMi.git`.

## Pre-publish checklist (every gate, every PR)

- New `.go` files carry the Apache header.
- Commit messages hand-written by the user, `Signed-off-by` present.
- PR body: `/kind`, what/why, `Fixes #`/`Depends on #`, hardware
  validation record, AI-assistance disclosure.
- Upstream master CI green (else the merge ref fails regardless of your
  diff).
- Issue and PR published by the user; agent supplied drafts only.
