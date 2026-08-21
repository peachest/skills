# Go mutation testing

## Tool choice

**Gremlins** is the primary tool — Go 1.26 compatible, non-invasive (uses coverage + temp mutations, never edits source files), actively maintained (391★, 2026-06).

Install once per machine:

```bash
go install github.com/go-gremlins/gremlins/cmd/gremlins@latest
```

The binary lands at `$GOPATH/bin/gremlins` (typically `~/go/bin/gremlins`).

## Run

Run from the **module root** (where `go.mod` lives), targeting a package path:

```bash
gremlins unleash ./pkg/models/
```

Gremlins first gathers coverage, then mutates only covered code (uncovered mutants are reported as `NOT COVERED` but not tested — testing them is pointless since no test reaches them).

### Flags

| Flag | Effect |
|------|--------|
| `--dry-run` / `-d` | Find mutations, don't run tests (fast scan to see candidate count) |
| `--tags string` | Comma-separated build tags |
| `--output-statuses string` | Print only specific statuses (chars: `l`=lived, `c`=killed, `t`=timed-out, `k`=not-viable, `v`=not-covered, `s`=skipped, `r`=runnable) |

### Output statuses

| Status | Meaning | Action |
|--------|---------|--------|
| `KILLED` | Tests failed → mutation caught | ✅ Good |
| `LIVED` | Tests passed → **test blind spot** | ⚠️ Add a test |
| `NOT COVERED` | No test executes this code | ⚠️ Add a test that reaches this line |
| `TIMED OUT` | Mutation caused infinite loop / test hang | 🔧 Investigate — may be a real bug the test should catch |
| `NOT VIABLE` | Mutation doesn't compile | ℹ️ Ignore |

### Efficacy vs coverage

Gremlins reports two numbers:

- **Test efficacy** — `killed / (killed + lived)`. How good tests are at catching mutations they *could* catch. 100% = tests catch every mutation they reach.
- **Mutator coverage** — `(killed + lived) / total`. How much mutated code tests reach at all. Low coverage = tests don't exercise much code.

A high efficacy + low coverage means tests are good where they exist but don't cover enough. A low efficacy means tests exist but are shallow.

## Fallback: self-rolled AST mutator

If gremlins is unavailable (can't install, corporate proxy blocks `go install`), use the bundled script:

```bash
go run <SKILL_DIR>/scripts/go-mutation.go -dir ./pkg/models -timeout 30
```

This is a minimal AST mutator (8 operator swaps: `==`↔`!=`, `<`↔`>`, `<=`↔`>=`, `+`↔`-`). It mutates in place, runs `go test`, restores the file. Unlike gremlins it does not distinguish `NOT COVERED` from `LIVED` — both report as `survived`, so the mutation score will be lower than gremlins' efficacy.

See [mutation-operators.md](mutation-operators.md) for the operator catalog.

## Limitations of the fallback

- No coverage gating — tests uncovered code too (all mutations run, wasting time on code no test reaches).
- No `NOT COVERED` distinction — a survived mutant might be untested code, not a shallow test.
- 8 operators only (gremlins has conditionals negation/boundary, arithmetic base, invert negatives).
- In-place mutation — don't edit the target files while the run is in progress.
