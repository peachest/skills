# DEVELOPMENT.md — {project} Development Spec

<!-- Repo-root single file. Language: follow the repo's dominant prose. -->

> This file defines how to **develop** in {project}. Submission workflow, review rules, and test gates live in [`docs/contributing/`](docs/contributing/README.md) — everything this file doesn't cover follows those.

## 0. One-line principle

<!-- fork posture: "The less you modify original files and the cleaner the isolation, the cheaper upstream sync becomes." Every edit to an upstream file is a conflict to re-solve on every cherry-pick/upgrade. -->

## 1. Branch and remote model <!-- adapt per posture -->

### Remotes

<!-- fork: table of remotes — upstream (read-only, fetch tags, never push) vs internal (the only push target). Iron rule: never push to upstream. -->

### Branches

<!-- main maintenance branch, feature branch scheme (<org>/<short-desc>), upgrade branch -->

### Merge policy

<!-- all changes via MR from feature branches; protected main branch; merge strategy (squash/rebase for linear history) -->

## 2. Internal-change markers and isolation <!-- fork posture only -->

### Prefer not touching core files

Rank modification approaches by sync cost, always take the lowest that works:

1. New standalone file (new backend / allocator / kernel / model file) — zero conflict
2. Existing extension points (model registration, backend dispatch, env-var descriptors, server args)
3. Config/parameter default changes
4. Core-logic file edits — last resort, requires anchor comments

### Commit prefix

<!-- internal original changes carry [<org>] prefix — the only way to tell "our commits" from upstream's during sync. Cherry-picked upstream commits stay verbatim (git cherry-pick -x). -->

### Anchor comments

<!-- when a core file must change, wrap with greppable anchors; state WHY, not what:

```lang
# >>> <ORG>: reason (linked design record / issue)
... change ...
# <<< <ORG>
```
-->

## 3. Upstream sync strategy <!-- fork posture only -->

### Routine: cherry-pick fixes

```bash
git fetch {upstream} --tags
git cherry-pick -x <upstream_sha>
```

### Upgrades: moving to a new upstream version

<!-- create new branch from upstream tag, replay internal commits (listable via the prefix grep), run full tests + smoke before switching the maintenance branch; read each design record's "sync notes" column first -->

## 4. Design records <!-- fork posture only -->

<!-- when required (new backend/kernel/core-logic change/>N LOC), directory location (physically isolated from upstream docs to avoid sync conflicts), naming (NNNN-<slug>.md), index README. Minimal template: Problem / Proposal / Alternatives / Impact (new files + anchor list) / Test results / **Sync notes** (what upstream internals this depends on, where it will conflict, how to migrate). -->

## 5. Versioning <!-- fork posture only -->

<!-- internal tags suffixed with -<org>.N, never overwrite upstream tags -->

## 6. Code style and domain guards

<!-- code-style principles not covered by the linter (avoid duplication, keep hot paths lean, pure functions, file-size limits, security rules like no pickle on untrusted data) -->
<!-- domain guards: components that must not be touched without reading their guide first; where those guides live -->

## 7. Making agents follow this spec

<!-- pointer files: AGENTS.md / CLAUDE.md auto-load entry, rules dirs, plus hard constraints that don't rely on agent discipline (protected branches, commit-msg hooks) -->
