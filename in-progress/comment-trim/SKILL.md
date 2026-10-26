---
name: comment-trim
description: Find functions whose doc comment is as long as or longer than the body, trim the redundant comment lines in place, and fold the result back — the full discover→classify→edit→verify workflow, not just an audit report. Also sweeps author-environment traces (machine names, local paths, intranet endpoints) out of comments and commit messages before they enter the remote repo. Use when the user says 清理冗余注释 / 简化注释 / comments longer than code, 清理本地环境痕迹 / 本地信息泄漏 / environment traces, or before pushing a PR that introduced new files with doc comments.
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
   this file maintains. **Status snapshots belong here too**: "image is
   at 0 CVE (scanned 2026-10-23)", "currently 0 vulnerabilities" —
   the subject is an external object's scanned state, not something
   this file maintains, and a snapshot ages into a lie, not just noise
   (readers trust it after reality moved on). Once the event lands the
   warning is permanent noise. Handling: one-line pointer, or drop it
   and let the MR/issue trail carry the history. Ask "is this fact
   still true?" before "is it needed?" — and when the invariant
   matters but the stated fact went stale, **rewrite** it to the
   current truth; rewriting ranks equal to deletion. Rewrite needs a
   stable invariant to carry: a status snapshot has none (security
   posture drifts by design), so snapshots are deleted, never
   "updated" to a newer snapshot. **Mechanism-lock test before
   deleting**: if the evidence is pinned by a mechanism (version in
   go.mod, a contract test, an upstream branch), the "measured X"
   comment is proof of an invariant and survives ("verified against
   vendored apimachinery v0.36.4"); if the evidence is a bare date or
   a one-off run, it is a countdown. A cheaply re-runnable check may
   keep the claim only with date + trigger condition; an unreproducible
   mental state is deleted outright.

**History lives in git, not comments.** Authorship, dates, change
history, and "which MR/commit produced this" are one blame away —
editors surface per-line blame and agents can trace the log — so
comments shed those duties entirely. A comment whose only job is
documenting the change that produced the code gets deleted; the blame
*is* that record. Action narrations on config lines ("tighten to a
blocking gate", "re-enable after the rebuild") are the same disease in
miniature — the diff beside the comment *is* the action — and they live
on yaml/CI lines where the scanner is blind, so the sweep catches them
by eye. Comments carry only what is not derivable from the surrounding
context, the docs, or the git history: the decision that cannot be
reverse-engineered.

## Load-bearing patterns (keep regardless of length)

- issue / decision references ("(#114)", "mirrors NVIDIA's gate in
  register.go") — they point to the *why* outside the code. Only
  resolvable forms qualify: full-path refs (org/repo#N) and external-repo
  MR/issue numbers are durable; the **own MR's number and "pre-!N" change
  history never go into resident comments** (unresolvable after merge —
  they belong in the commit message / MR description); short-form spec
  refs with no repo path ("spec #39") do not either.
- truth tables and lifecycle contracts ("remove: the node still carries
  the annotation but no fresh payload backs it")
- explicit decoupling rationale ("SCORE writes X, FULL_TOPOLOGY writes Y —
  neither implies the other")
- implicit cross-file coupling — the fact's readers live in another file
  than its cause ("every value in this map — including the legacy alias —
  is also claimed by the extender managedResources", where the extender
  template is a different file). The side effect is not derivable from
  this file alone.
- cross-implementation alignment/difference notes
- semantic anchors — the natural-language description of the problem the
  code exists to solve ("kubelet restarts mid-registration"). Retrieval
  precedes understanding: an AI (or newcomer) starts from the user's
  words, not from your identifiers. Test: would this line hit when
  someone who doesn't know this repo searches with their original
  question? If yes, it is a legitimate index term.
- anti-simplification trap notes — the comment defends code that looks
  like an unnecessary guard ("explicit 0 is a valid enum value that
  `| default` would swallow"). The tell: it justifies why a *more
  elegant-looking* rewrite is wrong. Deleting it invites reviewers to
  simplify the code back into the bug.

Rule of thumb: every comment keeps its **one non-obvious fact** — the
invariant a reader cannot derive from the code. Zero non-obvious facts →
single summary line. A comment that survives with zero cuts is a valid
ruling; trimming is judgment, not a quota.

Two density corollaries. **Anchor density is a signal**: once AI can
generate unlimited comments, the presence of a comment itself claims a
non-obvious fact — low comment density is what makes the real guards
carry weight, so delete-side discipline and write-side value are the
same policy. **Anti-vacuum quota**: the rules are not delete-only —
core logic with zero why-level comments over ~200 lines is a finding
(flag it to the author); agents have no context window for git
archaeology, and a human at 3am reading six-month-old code needs the
anchor present, not reconstructible.

Expiry-hook form for verification claims: on security- or
correctness-sensitive lines, "verified <date>, re-verify when <trigger>"
is a commitment, not a snapshot — keep it in that shape (the trigger,
not the date, is what keeps it from aging into a myth). Gate for config/CI one-liners
(scanner-blind zone): a comment earns its place by being a decision or
an explanation that cannot be obtained directly — never a status
snapshot and never an action narration.

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
   place, not deleted. Rewrite direction for assertion comments: state
   the invariant plus the regression-guard reason ("a legacy pin here
   would degrade split requests to whole-card semantics"), never the
   change history.

3. **Apply the edits** with the edit tool, comment-only — never touch code
   lines in the same pass.

4. **Sweep for environment traces and unresolvable references** while in
   there (same pass, near zero cost). Two families:

   **Environment traces** — anything that only resolves on the author's
   machine and must not enter the remote repo. Grep the PR-introduced
   files (`grep -rnE` with the patterns below); hits get a ruling like
   any ⚠️ row, not an automatic cut:

   - machine/node identifiers and their qualifier words — hostnames,
     node names, 本机 / 本节点 / 本地节点 / "local machine". Rewrite
     to the neutral fact that still holds ("本机有 buildkit 0.32.2" →
     "buildkit 0.32.2 on dev machines"); delete the sentence when the
     machine name was the only content.
   - personal absolute paths (/Users/<you>, /home/<you>, /mnt/...,
     C:\Users\...) — replace with the repo-relative path or "the
     project checkout".
   - intranet-only endpoints — internal IPs, registry URLs, domains
     that do not resolve outside the dev environment.
   - author residue — local usernames, machine-specific tool paths,
     local service ports.

   Prefer rewrite over delete: generalize the wording, keep the
   technical fact.

   **Unresolvable references** — company domains, short-form spec refs
   without a repo path, local-process references (grilling Q numbers,
   local tracker map/ticket ids, wayfinder), and review-finding hashes
   (for the latter, state the problem it solved directly instead of the
   pointer). Review-attribution residue follows the same rule: if the
   comment's beneficiary is the author or the review bot of that round,
   it is conversation history misplaced — cut it; the real invariant
   hiding behind it gets kept and rewritten in place. The residue
   breeds: AI never forgets and faithfully reproduces old justifications
   into the next edit. Keep: full-path refs (org/repo#N) and
   external-repo MR/issue numbers — durable cross-repo facts. When the
   same decision is commented in several repos (shared template), the
   fix is one canonical location plus explicit cross-repo coupling
   statements ("mirrors common-ci !N — change together"), not identical
   copies that drift separately. Found most often in
   comments, bench/test files, script headers, and docs (README,
   AGENTS.md).

   **Commit messages carry the same traces** ("verified on 本机...",
   local paths in reproduction steps) and travel with the repo the same
   way — sweep `git log --format=%B <base>..HEAD` with the same
   patterns. Unpushed commits: reword inside the step-6 autosquash
   rebase. Already pushed: same rule as files — ask the user first
   (rewriting published history is a force-push).

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
matcher first. For YAML/shell/helm templates there is no scanner — run
the ruling pass manually over the PR-introduced files (this is how the
helm-chart run that produced the class 2/4 rules was done).
