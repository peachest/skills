---
name: mr-buddy
description: >
  Your merge-request buddy — split an oversized MR into a stacked chain of small,
  vertically-sliced MRs so reviewers can review incrementally on the GitLab webUI.
  Use when the user reports a MR is too large to review (MR 太大 / 拆分 MR / 拆 MR /
  split this MR / break up this MR), when a branch carries dozens of commits heading
  for one giant MR, or when asked to turn a big MR into a stacked chain. Complements
  commit-buddy (commit granularity) and to-tickets (vertical slice definition).
---

# MR Buddy

Split an oversized MR into a **stacked chain** of small MRs, each a **vertical slice** —
one capability cutting through all layers (code + tests + docs), reviewable and
verifiable alone. Reviewer sees one increment per MR; merge order = review order.

The stack: `slice-1 → target`, `slice-2 → slice-1` … Slice 1 lives on the **original
MR's branch** (the original MR shrinks to the first slice, its history is never lost);
slices 2..N are new branches, each targeting the previous slice's branch.

## Process

### Step 1: Gather the MR's shape

Given an MR URL/iid or a feature branch + target:

```bash
glab api "projects/<url-encoded-path>/merge_requests/<iid>"           # meta
glab api "projects/<url-encoded-path>/merge_requests/<iid>/commits?per_page=100"
glab api "projects/<url-encoded-path>/merge_requests/<iid>/changes"   # file list
```

Fetch the source branch locally (`git fetch`). If HTTP basic auth fails, switch the
remote to ssh or fix credentials — cherry-pick needs local objects; the API alone
cannot carry git history.

**Done when:** commit list, changed-file list, and target branch are all known, and
the source branch is checked out locally.

### Step 2: Plan the slices

Group commits into slices, coarse enough that one MR ≈ one review session:

1. **Capability first** — commits belonging to one feature capability (impl + tests +
   docs for that capability) go in the same slice. Most MRs fall out naturally here.
2. **Never one-commit-per-MR by default** — too fine; consecutive commits of one
   capability (e.g. a feature followed by its review-fix rounds) merge into one slice.
3. **Mixed commits → file-level fallback** — a commit touching two capabilities gets
   split by files: `git cherry-pick -n <sha>` then commit only the files of one
   slice. Only do this when a commit genuinely mixes capabilities; a commit with
   cross-slice files stays whole in the slice owning its dominant change, noted in
   the plan.
4. **Sizing** — a slice must build and pass verify **on top of the previous slice**;
   docs-only commits ride with the slice they document. Research/SPEC docs from the
   exploration phase can be their own leading slice (reviewers skim it first).

Dependencies decide order: a slice that another builds on comes first. If no clean
ordering exists, reorder slices before proceeding — never stack on an unmerged
dependency that sits above its dependent.

**Done when:** every commit (or split file-group) is assigned to exactly one slice,
in a dependency-respecting order.

### Step 3: Confirm the plan with the user

Present the stack as a table:

| # | branch | MR title (draft) | commits/files | target |
|---|--------|------------------|---------------|--------|

Ask: granularity right? order right? any slice to merge/split? Iterate until approved.
Also flag what happens to the original MR (shrinks to slice 1 via force-push of its
branch — get explicit confirmation for that force-push).

**Done when:** user approves the stack and the force-push.

### Step 4: Build, verify, push — one slice at a time

For each slice in order:

1. **Branch — one wt worktree per slice** (worktrunk-managed repos, per the
   Worktree 管理 rules in AGENTS.md: never hand-roll `git worktree add`):
   slice 1 — `wt switch <orig-branch>`, then rebuild it in place
   (`git reset --hard <target>` + `git cherry-pick <shas>` — this rebuild is the
   force-push that shrinks the original MR); slices 2..N —
   `wt switch -c <type>/<name>-<n> -b <prev-slice-branch>`, cherry-pick that
   slice's commit group onto the previous slice's tip. Each slice keeps its own
   worktree: verify runs in place (no checkout thrashing between slices),
   project hooks (`.config/wt.toml` pre-start) auto-install deps, and
   `wt list --full` tracks the whole stack's CI after push.
   Plain-git fallback for repos outside the wt system (e.g. `~/third-party/*`
   study clones): `git checkout -b` per slice in the one checkout, strictly
   sequential.
2. **Verify**: run the project's verify entry (per its AGENTS.md; `make verify` or
   equivalent) locally **before pushing**. Red → fix forward with commit-buddy-style
   commits inside the slice, re-verify.
3. **Push + create MR**: draft MR via the create-mr skill's conventions — `--draft`
   flag only, description written to a file first, `-R <full remote URL>` on glab,
   push confirmed. Target = previous slice's branch (slice 1 → original target).
   Description links the stack: `Part n of <stack> — merge in order. #1: <url> …`

**Done when:** every slice branch is pushed, verified green before push, and has a
draft MR; the original MR's description now carries the stack index (all MR links in
merge order).

### Step 5: Report and hand off

Report the stack table with MR URLs and merge order. Note GitLab behavior: merging
slice *n* and deleting its branch auto-retargets slice *n+1* to the merged target —
merge bottom-up, mark each ready (`glab mr ready <iid>`) as review passes.
After a slice merges, `wt remove <branch>` reclaims its worktree (or
`wt step prune` once the whole stack is in).

## Integration with the ticket pipeline

mr-buddy is the retrofit end of `to-tickets → implement → commit-buddy → create-mr`:
when that pipeline runs cleanly, commits are already vertical and mr-buddy only
groups them per ticket — the ideal case is one MR per ticket, blocked-by order
already given by the tickets. When a big MR already exists anyway (review-fix rounds
inflated it, work predates the pipeline), mr-buddy recuts it. Ticket ids, when
present, travel into each slice MR's description.

## Non-goals

- No CI babysitting — after push, pipelines are the project's own loop.
- No review of slice content — that is ocr / mr-review-triage territory.
