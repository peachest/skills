---
name: comment-trim
description: Find functions whose doc comment is as long as or longer than the body, trim the redundant comment lines in place, and fold the result back — the full discover→classify→edit→verify workflow, not just an audit report. Use when the user says 清理冗余注释 / 简化注释 / comments longer than code, or before pushing a PR that introduced new files with doc comments.
---

# comment-trim

Trim redundant comments from PR-introduced code. The agent executes the whole
loop itself: scan → rule per comment → edit → verify → fold back. The output
is a cleaned-up diff, not a findings list.

## The four redundancy classes (delete these)

1. **Restates the signature or body** — nil handling ("nil pod returns
   Unset" when the code's first line is exactly that), return-value
   semantics a named type already carries, "the second return is false
   when not a valid bool".
2. **Duplicated elsewhere** — advice a package-level comment or the
   consuming file already covers in full (e.g. caching guidance in both
   the cache file and the util file). Keep one canonical location;
   elsewhere leave at most a one-line pointer. Canonical priority: ADR /
   decision record > authoritative implementation (the one others
   mirror) > follower implementation > MR description. If two copies
   could drift, expand only at the canonical spot — mirrored
   implementations and MR-round residue (each review round re-adding its
   own rationale for the same fact) are the same disease; merge the
   cluster to one fact, one place.
3. **Narrates the obvious** — "iterates over entries and appends".
4. **Expired facts** — the constraint is upheld by an external rollout
   (another repo's release, a CI image rebuild), not by an invariant of
   this code. Signal: the comment's subject is the rollout ("!33
   onward", "the rebuilt image picks this up") rather than something
   this file maintains. Once the event lands the warning is permanent
   noise. Handling: one-line pointer, or drop it and let the MR/issue
   trail carry the history. Ask "is this fact still true?" before "is
   it needed?" — and when the invariant matters but the stated fact
   went stale, **rewrite** it to the current truth; rewriting ranks
   equal to deletion.

## Load-bearing patterns (keep regardless of length)

- issue / decision references ("(#114)", "mirrors NVIDIA's gate in
  register.go") — they point to the *why* outside the code
- truth tables and lifecycle contracts ("remove: the node still carries
  the annotation but no fresh payload backs it")
- explicit decoupling rationale ("SCORE writes X, FULL_TOPOLOGY writes Y —
  neither implies the other")
- cross-implementation alignment/difference notes
- anti-simplification trap notes — the comment defends code that looks
  like an unnecessary guard ("explicit 0 is a valid enum value that
  `| default` would swallow"). The tell: it justifies why a *more
  elegant-looking* rewrite is wrong. Deleting it invites reviewers to
  simplify the code back into the bug.

Rule of thumb: every comment keeps its **one non-obvious fact** — the
invariant a reader cannot derive from the code. Zero non-obvious facts →
single summary line. A comment that survives with zero cuts is a valid
ruling; trimming is judgment, not a quota.

## Workflow

1. **Scan** the files the PR introduced:

   ```bash
   python3 scripts/scan.py <files-or-dirs> [--ratio 0.8] [--all]
   ```

   Prints `comment=N body=N ⚠️` per function. ⚠️ rows are **trim
   candidates** — each needs a keep/trim ruling, never an automatic cut.
   `--ratio 0.8` widens the net; on AI-authored codebases flag density is
   naturally high, expect a higher keep rate.

2. **Rule on every ⚠️ comment, sentence by sentence**: is the fact
   still true (expired → rewrite or pointer, class 4), which redundancy
   class, or the load-bearing fact? Verdict per comment: keep / trim to
   the fact / rewrite / drop entirely. Stale-but-load-bearing statements
   (e.g. an assert-count header an MR just invalidated) get corrected in
   place, not deleted.

3. **Apply the edits** with the edit tool, comment-only — never touch code
   lines in the same pass.

4. **Sweep for internal-reference leaks** while in there (same pass, near
   zero cost): grep the diff for internal node names, internal doc/ADR
   numbers, company domains — anything a public-repo reader cannot
   resolve. Found most often in comments and bench/test files.

5. **Verify**: build, test, lint the touched packages once — comment-only
   edits still run the checks; they catch a stray edit that hit code.

6. **Fold back**: if the trimmed files belong to an unpushed commit, fold
   via `git commit --fixup <sha>` + `git rebase -i --autosquash <base>`
   instead of a separate chore commit. For files on an already-pushed
   head, ask the user: separate `docs:`/`style:` commit vs history
   rewrite.

## Scope discipline

- Only files the PR introduces or heavily rewrites. Existing code with the
  same smell stays untouched — flag it to the user; it is a separate
  cleanup.
- Test comments are judged by "does it explain *why* this asserts that" —
  scenario-setting comments survive more often than doc comments.

## Limits

Go-specific (function detection via `^func` + brace balancing). The
classification rules transfer; the scanner needs a per-language function
matcher first.
