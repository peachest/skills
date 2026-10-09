---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Load and follow /skill:tdd at pre-agreed seams — write the failing test first (red), then implement (green).

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /skill:code-review to review the work.

Use /skill:commit-buddy to commit your work to the current branch.
