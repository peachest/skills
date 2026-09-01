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

1. **Select the remote** (`git remote -v`). One remote → use it. Several → ask
   the user which one. Everything below runs against the *selected* remote.

2. **Detect the platform** from the selected remote's URL: `github.com` → `gh`;
   anything else → `glab` (self-hosted GitLab included). For GitLab, check
   `glab auth status` first — several instances are usually configured, and glab
   mr commands target the repo's git remote. On auth failure (401), stop and
   tell the user; never retry or work around.

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
   (an unpushed branch simply has no MR):

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

6. **Title** — derive, then confirm. First commit of `<target>..HEAD`, subject
   line; if none, transform the branch name (`<type>/<name>` → `Type: name`).
   Clean title, no draft prefix. Ask the user to confirm or edit.

7. **Description** — yours to write, no fixed skeleton (MRs are not all fixes).
   Cover what fits the change: background, approach, verification, files
   touched — organized to suit it.

8. **Push + create** — one explicit confirmation for the push (a standing user
   rule; never push unasked). Then:

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
