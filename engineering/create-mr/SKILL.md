---
name: create-mr
description: >
  Create a draft MR/PR for the current work — confirm remote, target branch, and
  feature branch with the user, then push and open a draft MR assigned to the user
  with a clean title. Use when the user asks to 创建 MR / 提 MR / 开 MR / 创建 PR /
  提 PR / create a merge request / open a pull request.
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
   is the most recurring violation on record.

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

6. **Title** — derive, then confirm. Offer a short descriptive title naming
   the behavior change or symptom (recommended: what the MR *does*, not which
   files it touches), alongside the first commit's subject line of
   `<target>..HEAD` as the alternative. If neither works, transform the branch
   name (`<type>/<name>` → `Type: name`). Clean title, no draft prefix. Ask the
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

## Non-goals

- No verify gate — the development phase owns verification.
- No mechanical predicates (long-branch lists, candidate caps) — your judgment
  plus the confirmations above are the design.
