## What it does

`implement-spec` takes a [spec](https://www.aihero.dev/ai-coding-dictionary/spec) and its [tickets](https://www.aihero.dev/ai-coding-dictionary/ticket) and lands the whole thing in one run. The orchestrating [agent](https://www.aihero.dev/ai-coding-dictionary/agent) hands each ticket to an implementer [subagent](https://www.aihero.dev/ai-coding-dictionary/subagent) working in its own git worktree, merges each finished branch into a single **integration branch**, runs [code-review](https://aihero.dev/skills-code-review) over the result, and resolves the tickets.

It reads the tickets as a **task graph**, not a list. Blocking edges decide what can start, so at any moment there is a **frontier** of tickets whose blockers have all landed, and every ticket on the frontier runs at once. That is the difference from working the tickets one by one: the graph's shape, not its order on the tracker, sets the pace.

## When to reach for it

You invoke this by typing `/implement-spec`, and the agent won't reach for it on its own.

| Your situation | Reach for |
| --- | --- |
| A spec, split into tickets with blocking edges, that you want landed in one run | `/implement-spec` |
| One ticket at a time, in your own [context window](https://www.aihero.dev/ai-coding-dictionary/context-window), clearing between tickets | [implement](https://aihero.dev/skills-implement) |
| A spec that isn't split into tickets yet | [to-tickets](https://aihero.dev/skills-to-tickets) first |
| A small piece of work with no real graph to it | [implement](https://aihero.dev/skills-implement) directly |

## Prerequisites

- **An issue tracker.** The skill reads the tickets from, and resolves them on, the tracker [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) configured. If none has been configured, it stops and tells you to run that first rather than guessing.
- **Tickets with blocking edges**, as [to-tickets](https://aihero.dev/skills-to-tickets) writes them. Without edges the graph is flat and every ticket starts at once.
- **A [harness](https://www.aihero.dev/ai-coding-dictionary/harness) that runs subagents in the background and gives each one a git worktree.** The concurrency is the point; a harness that runs subagents one at a time gets a slower `implement`.

## The integration branch

Everything lands on one branch. Each implementer:

1. confirms its worktree is based on the integration branch before it starts,
2. builds its ticket with [tdd](https://aihero.dev/skills-tdd), red-green one slice at a time,
3. merges the integration branch tip into its own branch before reporting done, so landing it is a fast-forward.

Whether a pull request exists at all is the tracker's call. If your tracker closes work through PRs, or you ask for one, a draft PR opens after the first merge and is marked ready at the end. Otherwise the run stops on the integration branch with every ticket resolved the way your tracker closes work, which works fully offline against a local markdown tracker.

Implementers talk to the orchestrator through [context pointers](https://www.aihero.dev/ai-coding-dictionary/context-pointer) (the spec, the ticket, shared exploration notes, earlier commits) rather than pasted summaries, which keeps each subagent's prompt small and the orchestrator's window free for the graph.

## Common questions

**Does it need GitHub? I want it to stop at the branch.**

No. The goal is the integration branch. A PR is opened only when the configured tracker closes work through PRs or you ask for one, so on a local markdown tracker the run ends with every ticket resolved and the work merged on the branch.

**Blocked tickets never start, even after their blocker has merged.**

A known rough edge on GitHub. The tracker's blocked-by count only drops when a blocker *closes*, and tickets typically close when the PR merges, which is the end of the run. The tracker is the right source for the starting graph but a stale one mid-run. Tell the orchestrator to track which tickets have merged into the integration branch itself and compute the frontier from that.

**Does it drive tdd like implement does?**

Yes. Each implementer builds its ticket with `tdd`. There is no step where seams get agreed interactively, as there is in an `implement` session, so name the seams in the spec or the tickets if you want them pinned.

**Its review and fix loop ran for hours.**

The skill runs `code-review` once and sends every finding to one fix subagent, but it doesn't yet say when to stop after that fix, so an agent can treat the changed code as grounds for another full review. If you see a second broad review start, tell it to run focused checks for the fixed findings and stop.

**Two implementers running in parallel collided on the same file, or picked different names for the same thing.**

Each implementer sees only its own ticket and the shared notes, never the other's work in progress. When two frontier tickets touch one shared surface (a message catalogue, a config registry, a shared component), either tell the orchestrator to run them one after the other, or have the exploration notes fix the exact names each ticket adds.

**A ticket's key test was skipped inside its worktree, and it reported green.**

A worktree holds only what git tracks. Tests that read gitignored fixtures, local databases, or credentials can skip themselves there silently. For a ticket whose verification depends on untracked material, tell the orchestrator to run it in the main checkout instead.

## It's working if

- Several implementers are running at once whenever the graph allows, not one after another.
- A ticket starts as soon as its last blocker lands on the integration branch, not when the whole run ends.
- Every ticket's trace shows `tdd` running, with a failing test before the code.
- Merges into the integration branch are fast-forwards, not conflict resolutions.
- The run ends on one branch with every ticket resolved, and a PR only if your tracker wanted one.

## Where it fits

`implement-spec` is the build step of the main chain, as the parallel alternative to running [implement](https://aihero.dev/skills-implement) once per ticket:

```txt
grill-with-docs → to-spec → to-tickets → implement-spec
```

Its neighbours are [to-tickets](https://aihero.dev/skills-to-tickets), which declares the blocking edges it reads as a task graph, and [code-review](https://aihero.dev/skills-code-review), which it runs over the integration branch before closing out. [ask-matt](https://aihero.dev/skills-ask-matt) is the router over the whole set when you are not sure which flow you are in.
