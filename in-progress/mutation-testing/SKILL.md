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

1. **Detect language** — inspect the target directory for language markers.
2. **Run mutation tool** — apply AST-level mutations, run tests per mutation.
3. **Parse survivors** — collect mutations where tests did NOT fail.
4. **Report blind spots** — markdown report grouped by file, with original vs mutated code.

## Language adapters

| Language | Tool | How to run |
|----------|------|-----------|
| Go | `<SKILL_DIR>/scripts/go-mutation.go` | `go run <SKILL_DIR>/scripts/go-mutation.go -dir <pkg> -timeout 30` |
| Python | _(future ticket — `mutmut`)_ | — |
| TypeScript | _(future ticket — `Stryker`)_ | — |

Only Go is implemented in this first slice. Python and TypeScript adapters are follow-up tickets.

## Running on Go

```bash
go run <SKILL_DIR>/scripts/go-mutation.go -dir ./internal/myPackage -timeout 30
```

The script:

- Parses non-test `.go` files in the target dir (skips `vendor/`, `testdata/`, hidden dirs).
- Applies 8 operator-swap mutations (see [references/mutation-operators.md](references/mutation-operators.md)).
- For each mutation: reprints the file with the swap, runs `go test ./...`, restores original.
- Outputs JSON to stdout (array of mutations with `file`, `line`, `operator`, `original`, `mutated`, `status`).
- Outputs human-readable progress + summary to stderr (mutation score %).

### Flags

- `-dir` — target Go package directory (default `.`).
- `-timeout` — per-mutation test timeout in seconds (default `30`).
- `-parallel` — parallel test runs via temp copies (default `1`; >1 is slower per-mutation but higher throughput — use only if tests are fast and side-effect-free).

### Status taxonomy

| Status | Meaning |
|--------|---------|
| `killed` | Tests failed → test caught the mutation ✅ |
| `survived` | Tests passed → **test blind spot** ⚠️ |
| `timeout` | Test exceeded timeout — test too slow or mutation caused infinite loop 🔧 |
| `compile-error` | Mutation didn't compile (e.g. `+`→`-` on strings) — ignore ℹ️ |

## What to do with survivors

Each `survived` mutation is a finding: the test suite does not catch this change. For each survivor:

1. **Read the mutation** — what operator was flipped, where.
2. **Write a test** that would fail if the mutation were applied (i.e., a test that exercises the mutated condition with input that distinguishes original from mutated).
3. **Re-run mutation testing** to confirm the mutant is now killed.

Optionally, feed survivors into `/skill:fix` as findings — the `fix` skill's verify→grill→fix loop can work through them systematically.

## Glossary

- **Mutant** — a mutated copy of production code (one operator swap applied).
- **Surviving mutant** — a mutation that tests did NOT catch = a test blind spot.
- **Killed mutant** — a mutation that caused a test failure = test caught it.
- **Mutation score** — `killed / (killed + survived) × 100%`. `compile-error` and `timeout` excluded from denominator.

## Limitations (first slice)

- **Go only.** Python (mutmut) and TypeScript (Stryker) adapters are follow-up tickets.
- **8 operator swaps** (comparison + arithmetic). Boolean flips, constant mutation, and statement removal are not yet implemented — see [references/mutation-operators.md](references/mutation-operators.md) for rationale.
- **In-place mutation** with `-parallel 1` (default). The original file is briefly modified during each test run; the script restores it immediately after. Do not edit the file while mutation testing is running.
- **No `.gitignore` awareness.** The script mutates files in place; ensure you have no uncommitted changes to the target files before running (or `git stash` first).
