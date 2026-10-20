# Skill Authoring Conventions — Runtime, Environment, and Diagnostics

How skills in this repo declare and verify their runtime assumptions. Read this
when creating a new skill in `in-progress/`, promoting one to a category
directory, retrofitting an existing script-dependent skill, or committing
anything to this repo (the sensitive-data rules apply to every commit).

## Scope: which skills this applies to

Two classes of skills live here:

- **Pure-markdown skills** — guidance only, no scripts. Only the
  sensitive-data rules apply.
- **Script-dependent skills** — anything with `scripts/` or executable
  references. These depend on tools, python modules, network endpoints,
  credentials, or MCP servers, and the rest of this spec is about them.

## Convention strength

| Requirement | Strength | Applies to |
| --- | --- | --- |
| No internal endpoints/secrets in tracked files | **Required** | every skill |
| Python invocations locked to `uv run` (see Pipeline discipline) | **Required** | script skills with third-party deps |
| Subprocess failures must surface (see Pipeline discipline) | **Required** | script skills |
| Single orchestration entry when stages chain (see Pipeline discipline) | **Required** for multi-stage pipelines | script skills |
| Cross-skill script imports documented (see Pipeline discipline) | **Required** when one skill's script imports another's | script skills |
| `runtime.conf.example` when node-specific values exist | **Required** | script skills with external deps |
| `scripts/check-env.sh` | **Required** for heavy external deps (endpoints, credentials, CLIs with auth); suggested otherwise | script skills |
| Diagnose companion skill (`diagnose-<target>`) | **Suggested** — only when it earns its place | see criteria below |

## Python environment tiers

Skill venvs are either SHARED or skill-local — never one-off sprawl. Two
tiers cover every case (distilled from the 2026-10-20 venv audit: 46 venvs,
~1.4GB install-copy duplication, broken non-relocatable copies):

| Tier | Who | Where | Invocation |
| --- | --- | --- | --- |
| 1 — shared test venv | pytest-only skills (no runtime deps beyond pytest) | repo root `pyproject.toml` → `<repo-root>/.venv` | `uv run --project <repo-root> pytest <skill-dir>/tests` |
| 2 — skill-local venv | skills with real runtime deps (e.g. bilibili-transcriber: aiohttp/numpy/pillow) | `<SKILL_DIR>/.venv` via `uv sync` | `uv run --project <SKILL_DIR> ...` (locked by Pipeline discipline #2) |

Rules:

- **Never create a per-skill venv for pytest-only testing** — use tier 1.
  A new runtime dep that a pytest-only skill genuinely needs is a signal the
  skill moves to tier 2 (add it to its pyproject, `uv sync`).
- **Install copies never carry venvs.** venvs are non-relocatable (shebangs
  hardcode the source path — a copied `.venv` silently invokes the SOURCE
  repo's interpreter). `npx skills add` copies them anyway, so after any
  install/sync: `rm -rf ~/.agents/skills/*/.venv`. If a skill's scripts need
  python at runtime on the consuming side, that is tier-2 territory:
  document `uv sync` in its SKILL.md, don't ship the venv.
- **Discoverability**: `check-all-env.sh` (repo root) is the single sweep —
  it must keep working as skills migrate between tiers. Do not introduce a
  third location without updating this section first.

## Pipeline discipline (script skills)

Distilled from the bilibili-transcriber retro (2026-10-20, 41-session trace
analysis). Read this section BEFORE writing or modifying any script skill.

1. **Subprocess failures must surface.** Every `subprocess.run` whose failure
   changes the outcome must check the return code and exit non-zero. A script
   that "succeeds" with a degraded silent result (e.g. ffmpeg errored and the
   script continued with 1 frame instead of 12) is worse than a crash — the
   agent trusts the empty output. Verified pattern: check `r.returncode != 0`
   → `sys.exit(f"FAIL ...: {r.stderr[-500:]}")`.

2. **Lock python to `uv run`.** Never document or call bare `python3` for
   scripts with third-party deps — 41 sessions produced 529 bare-python3
   calls and 22 numpy ModuleNotFoundErrors before this rule. Canonical form:
   `uv run --project <SKILL_DIR> python scripts/<x>.py`; the orchestration
   entry auto-creates the venv (`uv sync`) when `.venv/bin/python` is missing.
   Do not add PYTHON= config keys — a unified entry makes them dead weight.

3. **One orchestration entry for multi-stage pipelines.** When a skill's
   stages must run in order (fetch → transcribe → merge), provide
   `scripts/run.sh <args>` that chains them, prints each artifact's absolute
   path, and defines aggregated exit codes (0 all ok / 2 partial / 3 nothing
   usable). For long tasks, write a completion marker containing the exit
   code (`.done` file) so subscription hooks get signal + verdict from one
   file. Keep per-stage sections in SKILL.md as manual/advanced fallback.

4. **Document cross-skill script imports.** If your script imports another
   skill's internal module (e.g. `sys.path.insert(0, ../fetch-article/scripts)`),
   the SKILL.md must say so AND name the breakage symptom when the dependency
   is missing. Sibling installs are a hidden dependency: agents cannot see it
   until it breaks at runtime.

5. **Doc-claimed output shapes need an e2e check.** When editing a skill whose
   docs describe another script's output format (paths, JSON keys), verify
   against the real output once (run the smallest stage) before trusting the
   prose. Docs rot silently: `raw_path` was documented as a directory while
   the code returns a file path — caught only by an end-to-end run.

## Sensitive data rules (required, every commit)

This repo is **public**. Never commit:

- Internal hostnames, IPs, or registry URLs — use `runtime.conf` or neutral
  examples (`gitlab.example.com`, `harbor.example.com`, TEST-NET addresses
  like `203.0.113.x`) in docs and tests.
- Credentials, tokens, or real runtime configuration (`runtime.conf`,
  `.env`) — only `*.example` templates are tracked.
- Fixtures containing internal data (trace logs, pipeline dumps) — sanitize
  them or leave them untracked.

`scripts/check-all-env.sh` sweeps the git history with gitleaks on every run
and FAILs on any finding, so a leak is caught before it spreads. The tuned
gitleaks config is node-specific and lives outside the repo
(`~/data/benchmark/config/gitleaks.toml`); if it or the `gitleaks` binary is
missing, the sweep reports WARN instead of FAIL.

Since 4e9bd07 this is a **hard rule at the tool level**: a `pre-push` hook
(`scripts/githooks/pre-push`, active via `core.hooksPath`) gitleak-scans the
exact commits being pushed and blocks the push on any finding. Manual
pre-commit scans remain good practice (earlier feedback), but the hook is
the enforcement of last resort — no longer "agent must remember".

## Runtime configuration (`runtime.conf`)

When a skill has node-specific values — service endpoints, credential file
paths, tool locations — they live in a dotenv file, never hardcoded:

```
<skill>/
├── runtime.conf.example   # tracked: KEY=value placeholders + discovery notes
├── runtime.conf           # gitignored, per-node, the real values
└── scripts/check-env.sh   # sources runtime.conf, verifies every assumption
```

- Format: `KEY=value`, one per line, shell-sourceable. Comments start with `#`.
- The `.example` template ships placeholder values plus instructions for
  discovering real values on a new node (see
  `research/bilibili-transcriber/runtime.conf.example` for the pattern: it
  documents how to find the ASR service on a Kubernetes cluster).
- Copying the example and running `check-env.sh` is the entire setup flow on
  a new node — the script's FAIL messages are the setup instructions.

## Environment self-check (`check-env.sh`)

`scripts/check-env.sh` verifies every runtime assumption the skill's scripts
depend on. Reference implementation:
`research/bilibili-transcriber/scripts/check-env.sh`.

Rules:

- One line per check: `PASS <item>` / `WARN <item> — why it's tolerable` /
  `FAIL <item> — what's missing and how to fix it`.
- Any FAIL → exit 1 after running all checks.
- Tools must be **executable**, not merely present. Python deps are checked by
  importing them. Endpoints get a short-timeout curl. Credentials are checked
  by the same probe the real script would use.
- Self-locating (`SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)`), no
  dependencies beyond bash + coreutils, idempotent, fast (<10s).
- Run it: on a new node, after a service moves, before a long batch.

## Diagnose companion skills (suggested, not mandatory)

A separate `diagnose-<target>` skill — one that owns the troubleshooting
workflow for a specific target system — is worth creating only when **all** of
these hold:

1. The target fails in **multi-layer ways** (CI pipeline layers, local
   sessions, LLM gateway, token throughput) that need a distinct diagnostic
   workflow, not just an env check.
2. Failures are **recurring** enough that a dedicated description-triggered
   skill beats inline troubleshooting.
3. Diagnosis needs its own reference material (failure taxonomies, log
   layouts, baseline metrics).

If the failure is "the script failed because the node lacks X", that's
`check-env.sh`'s job. Skill descriptions cost context in every session, so a
companion skill must clear all three bars.

## Environment migration flow

On a new node (or after re-imaging), in order:

1. `bash scripts/check-all-env.sh` (repo root) — runs every skill's
   `check-env.sh` in this repo (skipping `vendor/`) and sweeps the history
   with gitleaks; summarizes PASS/WARN/FAIL per skill.
2. Fix FAILs: copy the skill's `runtime.conf.example` to `runtime.conf` and
   fill in node values; install missing tools.
3. Re-run until green. Then install skills: `npx skills add -g ~/skills/
   --global -a pi -y` (see `docs/agents/install-skills.md`).

Node-level recovery (tools, kubectl, ssh targets) is a separate concern owned
by the `node-recovery` skill in the internal-skills repo; skill-level checks
assume the node works and verify the skill's own assumptions.

## Promotion checklist (in-progress → category directory)

Before promoting a script-dependent skill out of `in-progress/`:

- [ ] `runtime.conf.example` exists if any node-specific value is needed
- [ ] `scripts/check-env.sh` exists for heavy external deps, runs green on at
      least one node
- [ ] no internal endpoints or secrets in tracked files (check-all-env green)
- [ ] tests (if present) green: `uv run pytest` from the skill directory
