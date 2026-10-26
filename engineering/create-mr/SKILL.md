---
name: create-mr
description: >
  Create a draft MR/PR for the current work — confirm remote, target branch, and
  feature branch with the user, then push and open a draft MR assigned to the user
  with a clean title. Use when the user asks to 创建 MR / 提 MR / 开 MR / 开一个 mr /
  建 mr / 开 draft MR / 创建 PR / 提 PR / 创建 merge request / create a merge
  request / open a pull request. Also applies when MR creation arrives indirectly:
  a peer/worker dispatch text that says push 后建 MR / 开 draft MR / MR !N, a
  ticket/implement flow whose closure step is opening the MR, or a fix/triage
  skill run that ends with an MR — do not fall back to bare `glab mr create`.
  (2026-10-19 audit: 96 sessions created MRs without this skill; ~31% trigger rate.)
---

# Create MR

Push the feature branch and open a **draft** MR/PR assigned to the user. The flow
is guardrails, not rules: branch, remote, and target judgments are yours to make
by exploring — the confirmations below are what you must not skip.

## The draft rule (why this skill exists)

Mark draft with the `--draft` flag **only**. **Never** hand-write `Draft:` or
`WIP:` in the title. On GitLab the draft state *is* the title prefix (glab adds
it via the flag); on GitHub `--draft` is a real state. Doing both double-marks
the MR and forces the reviewer to click "Mark as ready" twice. The title you
confirm with the user is always clean.

## Process

0. **Fresh contract, fresh run.** Second execution in one session, or any
   execution in a session older than ~a day: re-read this SKILL.md first.
   Adherence decays with staleness — the worst violations on record (skipped
   asks, hand-written `Draft:` prefixes, unconfirmed pushes) all came from
   running a days-old memory of this flow.

1. **Preflight, then select the remote.** Run
   `bash <SKILL_DIR>/scripts/preflight.sh [repo-dir]` — it emits one block per
   info class the next steps need: REMOTES, PLATFORM, BRANCH (unpushed counts
   + branch-consistency), TITLE_CANDIDATE, ASSIGNEE, EXISTING_MR (API-first),
   TARGET_CANDIDATES. One remote → use it. Several → ask the user which one —
   via ask, even when context makes one look obvious; self-judging the remote
   is the most recurring violation on record. `OCR_REMOTE` (if set) selects
   the remote preflight uses as primary — it is the default when no ask
   happened; an explicit user choice via ask always takes precedence over it.

2. **Detect the platform** from the selected remote's URL: `github.com` → `gh`;
   anything else → `glab` (self-hosted GitLab included). For GitLab, check
   `glab auth status` first — several instances are usually configured, and glab
   mr commands target the repo's git remote. On auth failure (401), stop and
   tell the user; never retry or work around.

   URL normalization (all forms → one form): `ssh://git@host:port/g/p.git`,
   `git@host:g/p`, `http://` all normalize to `https://host/g/p`. Cross-instance
   targeting uses `-R https://<host>/<path>` (full https URL, no `.git`) — never
   combine `--hostname` with `mr create` (glab rejects the flag pair), and never
   hand-derive the `-R` value with sed on the fly; `create-draft-mr.sh` below
   already does the normalization.

3. **Source-branch checkpoint.** The current branch is not necessarily a feature
   branch — it may be the target branch or another long-lived branch. Explore
   (branch name, recent commits, relation to candidate targets) and judge. If
   unsuitable, cut a `<type>/<name>` feature branch from the right base
   (`git checkout -b` carries uncommitted changes along). Explain your judgment
   to the user. Pushing the new branch waits for step 8's single confirmation.
   Uncommitted changes on a *suitable* branch are out of scope — direct the
   user to commit first (e.g. `/skill:commit-buddy`).

4. **Confirm the target branch** — always ask, never guess. Build candidates
   from the selected remote's branches sorted by recent activity, always
   including the remote's default branch. Let the user pick or type any branch
   name (e.g. `dev`, or a version branch like `llm-2.3`).

5. **Check for an existing MR.** Server-side query, works before first push
   (an unpushed branch simply has no MR) — the preflight script's EXISTING_MR
   block already did this API-first; only hand-roll a query if the preflight
   was skipped:

   ```bash
   glab mr list -R <selected-remote-full-URL> --source-branch <branch>
   gh pr list --head <branch>
   ```

   If an open MR exists, compare its scope (title, description, changed files)
   with the pending changes, present that analysis, and ask the user: update it
   (push + `glab mr update <id> -t "<title>" -d "<description>"` where needed)
   or create a new one. That answer also covers the push confirmation.

   Note: `--hostname` is only valid on `glab api` / `glab auth status`, **not**
   on `glab mr` subcommands — use `-R <full remote URL>` there instead.

   Two query traps, both on record: ① a **404 here is a URL/path form
   problem until proven otherwise** — a misspelled `-R` returned 404 and was
   once read as "no MR"; re-check via
   `glab api --hostname <host> projects/<url-encoded-path>/merge_requests?...`
   before concluding "no MR". ② repos in `tos/*`-style namespaces where glab
   fails **silently** (empty output, exit 0): go straight to the glab-api
   skill's API path; do not loop on `glab mr create`.

6. **Title** — derive, then confirm. The style is fixed:
   **behavior-change titles only** — state what the MR *does* (behavior
   before → after, or the symptom it fixes), not which files it touches. Do
   not offer commit-subject or branch-name transforms as alternatives; the
   preflight TITLE_CANDIDATE (first commit subject) is raw material for
   phrasing, never the title itself. Clean title, no draft prefix. Ask the
   user to confirm or edit.

7. **Description** — yours to write, no fixed skeleton (MRs are not all fixes).
   Cover what fits the change: background, approach, verification, files
   touched — organized to suit it.

   **Deferred work → tracking issue.** If this change deliberately defers part
   of the work — a partial fix, a skipped review finding, an accepted
   edge-case debt — ask the user, before creating the MR, whether to open a
   tracking issue for the deferred piece and link it in the MR description.
   A promise recorded only in prose (MR description, vault entry) has no
   handle to grab when the bug next appears; an issue does. Carry the
   reconnect context into the issue: symptom, candidate approaches already
   ruled out, and the unblock condition. No deferred work — no question.

8. **Push + create** — one explicit confirmation for the push (a standing user
   rule; never push unasked). A confirmation counts only as **explicit user
   input in this session** — an ask answer, or a direct instruction covering
   *this branch's* push+create. Prior branches' instructions, other sessions'
   precedent, and your own inference ("context makes it clear") do not count;
   when in doubt, ask. Then:

   ```bash
   bash <SKILL_DIR>/scripts/create-draft-mr.sh \
     --remote <remote> --source <branch> --target <target> \
     --title "<clean title>" --desc-file <file> \
     [--assignee <user>] [--no-push] [repo-dir]
   ```

   Write the description to a file first — never inline it in the command
   (transient failures then cost a full re-emission). The script normalizes the
   `-R` URL, scrubs any `Draft:`/`WIP:` prefix from the title, pushes (skip
   with `--no-push`), creates with `--draft`, and retries once on transient
   failures (5xx/empty output). Exit 3 = glab silent failure (`tos/*` quirk) —
   route to the glab-api skill's API path, checking for an existing MR first.

   Manual fallback (script unavailable) — the raw commands:

   ```bash
   # GitLab
   git push -u <remote> <branch>
   glab mr create -R <selected-remote-full-URL> \
     --source-branch <branch> --target-branch <target> \
     --title "<clean title>" --description "<description>" \
     --assignee <username> --draft --yes

   # GitHub
   git push -u <remote> <branch>
   gh pr create --head <branch> --base <target> \
     --title "<clean title>" --body "<description>" \
     --assignee "@me" --draft
   ```

   - Assignee = the current user: `glab auth status` shows the username per
     host; GitHub takes `@me` directly.
   - **Never use `glab mr create --fill`** — it implicitly pushes the branch,
     bypassing the push confirmation.
   - If glab still prompts despite `--yes`, all flags above are already
     supplied — answer the prompt and note it.

9. **Report** the MR URL back to the user.

10. **MR 闭环（CI 订阅 + 评审循环）** — confirm continuation before starting.
    After step 9, ask the user whether to run the closure loop for this MR
    (e.g. "要继续盯 CI 并处理评审意见吗？"). The confirm discipline is the same
    as step 8: only an explicit user input in this session counts — a direct
    instruction or dispatch text covering *this MR's* 闭环 (盯 CI / CI 红了修复 /
    拉 triage 意见) satisfies it; silence or an unrelated MR's instruction does
    not. Declined → stop at the MR URL report. Once confirmed:

    a. **Subscribe to CI completion** — read `/skill:pi-events-daemon` and
       subscribe in the template form. The `gitlab-pipeline` template's ci
       form needs the **pipeline URL**, not the MR page URL (an MR URL routes
       to the template's mr form — MR state, never CI): derive the head
       pipeline id first
       (`glab api --hostname <host> "projects/<url-encoded-path>/merge_requests/<iid>"`
       → `.head_pipeline.id`), then
       `subscribe({url: "<host>/<project>/-/pipelines/<pipeline_id>", opts: {template: "gitlab-pipeline", once: true}})`
       — daemon wakes this session at a terminal pipeline state (passed or
       failed; `once` closes the subscription on either). Subscription-first:
       for pipelines expected to run long, add the daemon skill's dual-track
       `bg_run` counterpart for traceability. If the subscribe fails (smoke
       report / daemon down), tell the user and ask whether to fall back to
       manual polling or stop the closure loop here.

    b. **CI red → fix first.** Read the failed job's log (trace retrieval via
       the glab-api skill), root-cause, fix on the same feature branch, push.
       Route the diagnosis by failure type to the existing skill — do not
       improvise: security-stage jobs (trivy image scan / SCAP / OSCA
       threshold) → `/skill:gitlab-security-job`; ocr-review CI job
       stall/timeout/failure → `/skill:diagnose-ocr-ci`; anything else → the
       project's normal debugging flow. The loop confirmation covers these
       CI-fix re-pushes (same branch, fixing the reported failure); a change
       beyond that scope returns to step 8's confirmation. Exit condition:
       when the fix is not yours to make (centralized `.trivyignore`, platform
       thresholds, upstream breakage) or two re-push rounds have not gone
       green, stop — report the failure history to the user and end the loop
       (the confirmation does not cover a third round). Otherwise
       re-subscribe (a) for the new pipeline.

    c. **CI green → review loop.** Read `/skill:triage-mr` and run its pull
       step (CI is at a terminal state, so the pipeline gate passes).
       `pull-source.log` identity correct + 0 findings = no review round → go
       straight to (d). Before acting on the findings, run
       `/skill:challenge-audit` on the pulled report — audit the review's
       quality first (invented findings, misclassifications); findings the
       audit kills are recorded through triage-mr's verdict semantics as ❌ FP
       (or 🔵 OOS for pre-existing issues), not fixed. Surviving findings go
       through `/skill:fix` in its triage mode (verdict → `verdict.py` per
       finding → fix the ✅ TPs) — the loop confirmation counts as fix's
       batch instruction, so its per-finding ask gates are waived. Then
       complete triage-mr's post + resolve half: post the round's verdicts
       (post is not CI-gated — post immediately after each verdict, per
       triage-mr's 追尾规则), fix what the verdicts demand, push, and let
       triage-mr's re-pull (its Step 5) consume the OCR bot's new review
       round. The loop confirmation covers these review-fix re-pushes (same
       branch, fixing adjudicated findings). After each push, re-subscribe (a)
       for the new pipeline — its wake is what unblocks the next verify (CI
       in-flight → exit 2); keep the pull → audit-informed fix → post →
       verify cycle until triage-mr's verify gate exits 0.

    d. **Close** — report the final state: CI outcome, findings triaged
       (fixed/FP/resolved counts), remaining open threads if the gate is
       intentionally red (⚠️ error-class rounds stay red by design).

## Non-goals

- No verify gate — the development phase owns verification. Step 10's closure
  loop owns *post-creation* CI and review closure only, not the development
  phase's own verification.
- No mechanical predicates (long-branch lists, candidate caps) — your judgment
  plus the confirmations above are the design.
