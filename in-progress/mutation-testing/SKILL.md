---
name: mutation-testing
description: Run mutation testing to validate test quality — find surviving mutants that reveal test blind spots. Use when the user says "mutation test", "变异测试", "validate tests", "test quality", or after writing tests (TDD) before code review, to check whether the tests actually catch the bugs they should.
---

# Mutation Testing

Mutation testing mutates production code and checks whether tests fail — **surviving mutants** are test blind spots. TDD guarantees tests exist; mutation testing guarantees they actually catch bugs.

## When to run

- After `/skill:tdd`, before `/skill:code-review` — validate the tests you just wrote.
- Standalone: "are my tests any good?"
- When an agent wrote tests and you want to check they're not shallow.

## Pipeline

1. **Detect language** — inspect the target directory for language markers (below).
2. **Load the language reference** — read the matching `references/<lang>.md` for tool choice, install, and run commands.
3. **Run mutation tool** — apply mutations, run tests per mutation.
4. **Parse survivors** — collect mutations where tests did NOT fail.
5. **Report blind spots** — markdown report grouped by file, with original vs mutated code.

## Detect language

Pick the reference by what the target directory contains:

| Markers in target dir | Language | Reference |
|-----------------------|----------|-----------|
| `go.mod` | Go | [references/go.md](references/go.md) |
| `pyproject.toml` or `setup.py` or `setup.cfg` + `.py` files | Python | [references/python.md](references/python.md) |
| `package.json` + `.ts`/`.tsx`/`.js`/`.jsx` files | TypeScript / JavaScript | [references/typescript.md](references/typescript.md) |

If the target is a monorepo with mixed languages, run the matching reference per sub-directory. If no markers match, ask the user which language the target is.

## What to do with survivors

Each surviving mutant is a finding: the test suite does not catch this change. For each survivor:

1. **Read the mutation** — what operator was flipped, where.
2. **Write a test** that would fail if the mutation were applied.
3. **Re-run mutation testing** to confirm the mutant is now killed.

Optionally, feed survivors into `/skill:fix` as findings — the `fix` skill's verify→grill→fix loop can work through them systematically.

## Glossary

- **Mutant** — a mutated copy of production code (one operator swap applied).
- **Surviving mutant** (aka **lived**) — a mutation that tests did NOT catch = a test blind spot.
- **Killed mutant** — a mutation that caused a test failure = test caught it.
- **Not covered** — a mutation at a code location no test executes at all (gremlins distinguishes this from lived).
- **Mutation score** / **efficacy** — `killed / (killed + survived) × 100%`. Tool-specific terms vary; see each reference.
