# Python mutation testing

## Tool: mutmut

**mutmut** is the standard Python mutation tester (actively maintained, v3 released 2024). It mutates Python source AST and runs the test suite per mutation.

Install into the project's venv:

```bash
pip install mutmut
```

## Run

Run from the project root (where `pyproject.toml` or `setup.py` lives):

```bash
mutmut run
```

mutmut auto-detects the test runner (pytest, unittest, hammett). It caches results — subsequent runs skip already-killed mutants.

### Key commands

| Command | Effect |
|---------|--------|
| `mutmut run` | Run full mutation testing (first run is slow; caches) |
| `mutmut results` | List surviving mutants (after a run) |
| `mutmut show <id>` | Show a specific mutant's diff |
| `mutmut show all` | Show all surviving mutants' diffs |
| `mutmut run --use-coverage` | Only mutate lines covered by tests (faster; requires coverage data) |
| `mutmut junitxml` | Export results as JUnit XML |

### Configuring the mutation scope

By default mutmut mutates all `.py` files. To restrict scope, add to `setup.cfg` or `pyproject.toml`:

```ini
# setup.cfg
[mutmut]
paths_to_mutate=src/mypackage/
tests_dir=tests/
runner=python -m pytest -x -q
```

```toml
# pyproject.toml
[tool.mutmut]
paths_to_mutate = ["src/mypackage/"]
tests_dir = "tests/"
runner = "python -m pytest -x -q"
```

## Output

mutmut stores results in `.mutmut-cache`. After `mutmut run`:

```
⠋ 2.  Knife: a.  Applying mutation...
   2. mutmut survived!
```

`mutmut results` lists surviving mutant IDs:

```
Surviving mutants (5):
    src/mypackage/calc.py:12
    src/mypackage/calc.py:18
    ...
```

`mutmut show src/mypackage/calc.py:12` prints the diff:

```diff
-     if x > 0:
+     if x >= 0:
```

## Status taxonomy

| Status | Meaning | Action |
|--------|---------|--------|
| killed | Tests failed → mutation caught | ✅ |
| survived | Tests passed → **test blind spot** | ⚠️ Add a test |
| timeout | Mutation caused test hang | 🔧 Investigate |
| skipped | Mutant not tested (e.g. compile error) | ℹ️ |

Mutation score: `killed / (killed + survived) × 100%`.

## Gotchas

- **Fork support required** — mutmut uses multiprocessing fork; doesn't work on Windows without WSL.
- **Slow first run** — mutmut runs the full test suite per mutation. Use `--use-coverage` to skip uncovered code (run `pytest --cov` first to generate `.coverage`).
- **Test runner must be fast** — if the suite takes 30s, and there are 200 mutants, that's 100 minutes. Keep the suite tight or scope mutations to one module.
- **Caching** — `.mutmut-cache` persists; `mutmut run` resumes. Delete the cache to force a fresh run.
