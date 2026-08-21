# Mutation Operators

The Go mutator (`scripts/go-mutation.go`) applies AST-level mutations to binary
expressions. Each operator swap is one mutation; the tool reprints the full file
with the swap applied, runs `go test`, and restores the original.

## Current operators (8 swaps, 4 pairs)

| # | Mutation | Token swap | What it catches |
|---|----------|-----------|-----------------|
| 1 | `== → !=` | `EQL → NEQ` | Tests that assert equality but never check the inequality path |
| 2 | `!= → ==` | `NEQ → EQL` | Tests that assert inequality but never check the equality path |
| 3 | `> → <` | `GTR → LSS` | Tests that check "greater than" but not the boundary flip |
| 4 | `< → >` | `LSS → GTR` | Tests that check "less than" but not the boundary flip |
| 5 | `>= → <=` | `GEQ → LEQ` | Boundary condition tests missing the inclusive flip |
| 6 | `<= → >=` | `LEQ → GEQ` | Boundary condition tests missing the inclusive flip |
| 7 | `+ → -` | `ADD → SUB` | Arithmetic tests that don't distinguish addition from subtraction |
| 8 | `- → +` | `SUB → ADD` | Arithmetic tests that don't distinguish subtraction from addition |

## Why these 8

These are the **highest-signal** mutations for the lowest implementation cost:

- **Comparison flips** (1-6) are the most common mutation testing operators
  across all languages. They expose tests that check one direction of a
  condition but not the other.
- **Arithmetic flips** (7-8) catch tests that verify a result without checking
  the operation itself — e.g., `TestAdd(2,3)==5` kills `+ → -` (gives `-1`),
  but `TestAdd(0,0)==0` would survive it (both `0+0` and `0-0` are `0`).

## Why `==`↔`!=` and `<`↔`>` are "always killed" if exercised

A negation flip (`==`↔`!=`, `<`↔`>`) takes the **opposite branch** for any input.
So if a test exercises the condition at all, the mutation is killed. These only
**survive** when the test never reaches the mutated branch — which is exactly
the blind spot mutation testing is designed to find.

## What's NOT included (and why)

- **`*` → `/`** — division by zero crashes are noisy; skip for the minimal set.
- **Boolean flips** (`&&`→`||`) — lower signal, more complex AST handling.
- **Constant mutation** (`5`→`6`) — high noise, needs type-aware filtering.
- **Statement removal** — requires control-flow analysis to avoid compile errors.
- **String mutations** — Go's `+` on strings can't become `-` (compile error).

These can be added in follow-up tickets once the core pipeline is proven.

## Status taxonomy

| Status | Meaning | Action |
|--------|---------|--------|
| `killed` | Tests failed after mutation — test caught it | ✅ Good |
| `survived` | Tests passed after mutation — test blind spot | ⚠️ Add a test |
| `timeout` | `go test` exceeded the per-mutation timeout | 🔧 Test too slow, or possible infinite loop from mutation |
| `compile-error` | Mutated code didn't compile | ℹ️ Mutation is invalid for this type (e.g. `+`→`-` on strings); ignore |

## Mutation score

```
mutation score = killed / (killed + survived) × 100%
```

`compile-error` and `timeout` are excluded from the denominator — they're not
test-quality signals. A score of 100% means every valid mutation was caught.
