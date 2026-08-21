---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model, logic, API contract, CLI shape, data model, or performance characteristic feels right before committing to a real implementation.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape — the agent picks whatever form best exposes the answer: a script, a single endpoint, a benchmark, an HTML page, a REPL session, whatever. No prescribed branches.

## State the question first

Before writing code, write down the single design question this prototype must settle. One sentence. A prototype that answers the wrong question is pure waste — make the question explicit so it can be checked later, whether the user is watching now or returning to it AFK.

## Rules

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious — but name it so a casual reader can see it's a prototype, not production.
2. **Trivial to run.** One command, no setup rabbit hole. `go run`, `python`, `pnpm`, `curl`, double-click — whatever the project already uses. No thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action, print or render the full relevant state so the user can see what changed.
6. **Capture it when done.** Fold any validated decision into the real code, then capture the prototype itself as a **primary source**: commit it to a throwaway branch, out of main, and leave a context pointer to that branch on the implementation issue. Capture the answer too — the verdict and the question it settled — in the issue or a commit. The main branch keeps only the validated decision.
