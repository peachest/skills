# TypeScript / JavaScript mutation testing

## Tool: Stryker

**Stryker** (`@stryker-mutator/core`) is the standard mutation tester for JS/TS (actively maintained, framework-aware). It supports Jest, Mocha, Jasmine, Vitest, and more.

Install as a dev dependency in the target project:

```bash
npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner
# or for Vitest:
npm install --save-dev @stryker-mutator/core @stryker-mutator/vitest-runner
```

## Configure

Create `stryker.conf.json` in the project root:

```json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "packageManager": "npm",
  "testRunner": "jest",
  "coverageAnalysis": "perTest",
  "mutate": [
    "src/**/*.ts",
    "!src/**/*.spec.ts",
    "!src/**/*.test.ts"
  ]
}
```

Key fields:

| Field | Purpose |
|-------|---------|
| `testRunner` | `"jest"`, `"mocha"`, `"vitest"`, etc. Must install the matching `@stryker-mutator/<runner>` package. |
| `coverageAnalysis` | `"perTest"` (fastest — only tests covering the mutated line run) or `"off"` (all tests per mutant). |
| `mutate` | Glob array of files to mutate. Prefix `!` to exclude. Exclude test files themselves. |
| `thresholds` | Quality gate — e.g. `{"high": 80, "low": 60, "break": 50}` exits non-zero below `break`. |

## Run

```bash
npx stryker run
```

Stryker uses the project's existing test command (from `package.json` scripts or the configured runner). It does not modify source files — it compiles mutants in memory.

### Useful flags

| Flag | Effect |
|------|--------|
| `--mutate src/calc.ts` | Override `mutate` glob (one-off) |
| `--concurrency 4` | Parallel mutation runs |
| `--logLevel info` | Less verbose |
| `--dryRun` | Find mutations, don't test (fast scan) |

## Output

Stryker writes an HTML report to `reports/mutation/mutation.html` and prints a summary:

```
# Final mutation score 78.4%
Killed: 156 (78.4%)
Survived: 23 (11.6%)
Timeout: 12 (6.0%)
No coverage: 8 (4.0%)
```

Open the HTML report for per-mutant diffs:

```bash
open reports/mutation/mutation.html
# or: xdg-open reports/mutation/mutation.html
```

## Status taxonomy

| Status | Meaning | Action |
|--------|---------|--------|
| Killed | Tests failed → mutation caught | ✅ |
| Survived | Tests passed → **test blind spot** | ⚠️ Add a test |
| Timeout | Mutation caused test hang (>2s default) | 🔧 Investigate |
| No coverage | No test executes this code | ⚠️ Add a test that reaches this line |
| Runtime error | Mutation crashed before tests ran | ℹ️ May be invalid mutant |

Mutation score: `killed / (killed + survived + timeout) × 100%`. Stryker excludes `No coverage` from the denominator by default.

## Gotchas

- **`perTest` coverage requires a supported runner** — Jest and Vitest support it; Mocha does not (falls back to `off`, slower).
- **TypeScript checker plugin** — install `@stryker-mutator/typescript-checker` to skip mutants that cause type errors (reduces noise).
- **Large projects** — use `--mutate` to scope to one module first. Full-project runs can take 30+ minutes on big codebases.
- **CI integration** — `stryker run` exits non-zero if score < `thresholds.break`. Use in CI as a quality gate.
