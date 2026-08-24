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
- **Caching** — mutmut v3 stores results in `mutants/` (not `.mutmut-cache`). `mutmut run` resumes; delete `mutants/` to force a fresh run.

### Non-standard source layout (source NOT in `./`, `src/`, or `source/`)

mutmut v3 auto-adds `./`, `src/`, and `source/` to `sys.path` to resolve module paths. If your project uses a different source root (e.g. `scripts/`, `lib/`, `app/`), mutmut generates mutant keys from the file path relative to CWD, but tests import via the project's `pythonpath` config — causing a **key mismatch** that prevents any mutant from being killed (0% score, all "survived").

**Symptoms**:
- Error: `Stopping early, because tests recorded trampoline hits but none match any mutant key.`
- `mutmut results` shows all mutants as `survived` or `not checked`.
- `Recorded keys` (e.g. `transform.X`) ≠ `Expected keys` (e.g. `scripts.transform.X`).

**Fixes** (pick one):
1. **Run mutmut from the source root** — `cd scripts/` so file paths match module paths. BUT: if a parent `pyproject.toml` has `testpaths`/`pythonpath` config, pytest may fail to find tests from the subdirectory. Create a local `pytest.ini` overriding `testpaths` and `pythonpath`.
2. **Symlink** — `ln -s scripts src` so mutmut's default `src/` resolution works.
3. **Move source to `src/`** — the cleanest fix for new projects.

**Known incompatible layout**: source in `scripts/` with `pythonpath = ["scripts"]` in `pyproject.toml` (common in data/analysis projects). The `scripts/` directory is not in mutmut's auto-discovery list, and running from `scripts/` breaks pytest's config inheritance.
