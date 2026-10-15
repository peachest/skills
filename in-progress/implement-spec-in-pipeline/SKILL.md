---
name: implement-spec-in-pipeline
description: "Implement the result of /to-spec and /to-tickets in code, with a rolling review pipeline instead of a single end-of-branch review. Fork of /skill:implement-spec."
disable-model-invocation: true
---

> **Forked from** `vendor/mattpocock/skills/engineering/implement-spec` at upstream `49dd158` (upstream sync 2026-10-15; renamed `implement-spec-in-pipeline` to keep both installable side by side). Identical to the vendor skill except the integration points marked **[rolling-review]** below: a background rolling review fires after every merger merge and its findings are triaged by severity, instead of discovering all problems at step 7. Keep the fork's drift to those marks only; anything else belongs upstream.

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec and tickets to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of main can't open one), marked as closing the spec and tickets.

4. Use **implementer subagents** to implement each ticket, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `tdd` to build the ticket;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

   **[rolling-review]** When a merge conflicts, adjudicate three recurring classes before resolving mechanically: (1) two workers each added functions to the same file — usually keep both, and let the next rolling review judge the joined result; (2) a later ticket's new validation correctly rejects an earlier ticket's test payload — this is the design working, fix the payload, not the validator; (3) append-only ledger/log files both sides touched — keep both, dedupe only identical lines. Anything outside these classes goes to the user.

   **[rolling-review]** Immediately after each merge, kick off a **rolling review** of the integration branch in the background (see below), then continue with step 6 without waiting for it. Record the review task so its findings are triaged when they arrive (step 5.5).

5.5. **[rolling-review]** When a rolling review completes, triage its findings by severity:
   - **critical / high**: do not dispatch frontier tickets that touch the affected code area until the finding is fixed. Dispatch a **fixer implementer subagent** on the integration branch (or route through `/skill:fix`), merge the fix, then unblock those tickets. A critical finding that is ignored here gets copied by every later implementer — the rework is multiplicative, not additive. A fix batch larger than ~10 findings exceeds a single fixer's token budget (empirically times out around 400k+ tokens): split into batches of ≤ 8 findings and run fixers in parallel instead of one long-running worker.
   - **medium / low**: fold into the task text of the next implementer subagent you dispatch as an additional context pointer. Findings must not accumulate silently between merges.
   - **noise / duplicate** (already reported and fixed in an earlier round): drop.
   - The rolling review covers the **full accumulated diff** from the base branch to the integration tip — not just the latest ticket. Cross-ticket drift (naming, shared helpers growing inconsistently) is caught this way. Dedupe against the triage of previous rounds.

5.6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, call the Skill tool with `code-review` on the integration branch. Fix all issues raised by the code review in a single **implementer subagent**. **[rolling-review]** This final review stays full-scope and is the backstop for cross-ticket consistency (module boundaries, spec adherence) that single-diff rolling reviews cannot judge; rolling findings already fixed should not resurface here.

8. If a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work, and report the integration branch.

9. Clean up all **implementer subagent** worktrees.

## [rolling-review] Running the rolling review

Run the `ocr` CLI on the **main checkout** (not inside any worktree — implementers own those) via a background shell task, so it runs concurrently with the next frontier implementers:

```
bg_run: OCR_LLM_TIMEOUT=300 ocr review --from <base-branch> --to <integration-branch> \
  --effort medium   # first round; subsequent rounds --effort low (smaller marginal diff) \
  --audience agent --format json -o <scratch-dir>/rolling-review-r<N>.json
```

- `<base-branch>` is the branch the integration branch was cut from (usually `main`).
- One review task at a time: if the previous round's review is still running when the next merge lands, let it finish and let its result cover both merges.
- **[rolling-review]** Instruct the review to verify API shapes against the platform's official docs, not just the code: offline fixtures only prove internal self-consistency — real runs have each hidden a mock-invisible contract mismatch (a nonexistent endpoint, mixed id namespaces) that doc-checking catches.
- Rollback rule: if `ocr` itself fails repeatedly (auth, gateway timeouts), fall back to a **reviewer subagent** doing a read-only review of the same accumulated diff — the pipeline shape (review-during-implement, severity triage) matters more than the engine.
- See `/skill:ocr` for CLI troubleshooting.
