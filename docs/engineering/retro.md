## What it does

`retro` looks back over a coding [session](https://www.aihero.dev/ai-coding-dictionary/session) and suggests improvements to the agent's **[environment](https://www.aihero.dev/ai-coding-dictionary/environment)**, so the next run goes better. It reads the session's own record (the current one by default, or one you point it at in the session logs), finds the moments the agent struggled, and hands you a list of candidate fixes, most severe first.

It changes the environment, not the code. The bug the agent shipped, the file it took twenty [tool calls](https://www.aihero.dev/ai-coding-dictionary/tool-call) to find, the rule the reviewer missed: `retro` doesn't fix any of them in place. It asks what about the repo let them happen, and proposes the check, the pointer, or the standard that stops them happening again. It also only proposes; nothing changes until you pick a candidate.

## When to reach for it

You invoke this by typing `/retro`, and the agent won't reach for it on its own.

Reach for it at the end of a session that felt harder than it should have: the agent went looking for something for too long, made a mistake a machine could have caught, or needed information it had no way to get. A smooth session has little to teach; a painful one is where the findings are. If what you want is a verdict on the code the session produced, use [code-review](https://aihero.dev/skills-code-review) instead.

## Where the findings land

Each candidate belongs to one category, and the category decides where the fix goes:

| What went wrong in the session | Fix it with |
| --- | --- |
| The agent took a long time to find a file or fact | A **navigation pointer** from a file it already reads |
| It made a mistake a tool could have caught | An **[automated check](https://www.aihero.dev/ai-coding-dictionary/automated-check)**: lint rule, type, test, pre-commit hook, CI job |
| The reviewer missed a judgement-call mistake | A rule in `CODING_STANDARDS.md` for the reviewer agent |
| `AGENTS.md` or `CLAUDE.md` is large | Move its steering out, into standards or checks |
| A tool call was expensive for what it returned | Streamline the tool, or replace it |
| A steering file is full of lines that change nothing | Delete the **no-ops** |
| The agent needed information it couldn't reach | Widen its access: tee the dev server log to a file, give read-only access to a service |

The leading idea is that standards belong to the **reviewer**, not the implementer. The implementing agent carries the most context pressure: it explores, writes code, and debugs failures. The reviewing agent receives a diff and nothing else. So a new rule goes where there is room to apply it, in review, and never in [AGENTS.md](https://www.aihero.dev/ai-coding-dictionary/agents-md), which loads into every session's [context window](https://www.aihero.dev/ai-coding-dictionary/context-window) whether it's relevant or not.

Before any rule gets written, the violation is classified. A **mechanical** one (a banned API, an import shape, a file-location rule) gets a deterministic check, because a check can fail and a sentence in a standards file can't. Only genuine judgement calls, the kind no linter could ever enforce, become prose. A repo with no guardrail at all (no pre-commit hook, no CI job running lint, typecheck, and tests) is reported as a finding in its own right.

## Common questions

**The agent keeps making the same mistake. Should I add a line to `CLAUDE.md`?**

Usually not, and that's the most common place `retro` pushes back. A line in `CLAUDE.md` is loaded into every session, dilutes everything else in the file, and drifts as the code changes. If the mistake is mechanical, the fix is a check that fails. If it's a judgement call, it goes in the coding standards the reviewer reads. `AGENTS.md` and `CLAUDE.md` are for navigation pointers, and little else.

**Can it clear the no-ops out of my steering files?**

Yes, within limits. No-ops (instructions that don't change what the agent does) are one of its categories, and it flags them when the steering files are large and unwieldy. It judges them against the session it is reading, though, so a line that looks dead in one session may matter in a task it didn't cover. Treat a no-op finding as a candidate for the deletion test, not a verdict.

## It's working if

- Every candidate points back to a specific moment in the session, not a generic best practice.
- Repeat mistakes turn into failing checks, and your `AGENTS.md` gets shorter over time rather than longer.
- A missing check that already existed but sat unwired shows up as the finding, rather than a proposal to build a new one.
- The next session on the same kind of task finds its way faster.

## Where it fits

`retro` is **periodic maintenance**: run it after a session worth learning from, not on a schedule.

- [code-review](https://aihero.dev/skills-code-review) is the reviewer agent `retro` most often tunes: new coding standards land where its Standards axis reads them.
- [writing-for-agents](https://aihero.dev/skills-writing-for-agents) sets the writing style for every steering file and skill `retro` proposes, and `retro` loads it before it starts.

[ask-matt](https://aihero.dev/skills-ask-matt) routes across the whole set when you are unsure which skill the situation wants.
