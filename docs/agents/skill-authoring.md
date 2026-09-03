# Skill Authoring Conventions — Runtime, Environment, and Diagnostics

How skills in this repo declare and verify their runtime assumptions. Read this
when creating a new skill in `in-progress/`, promoting one to a category
directory, or retrofitting an existing script-dependent skill.

## Scope: which skills this applies to

Two classes of skills live here:

- **Pure-markdown skills** — guidance only, no scripts. Nothing in this spec
  applies beyond the sensitive-data rules.
- **Script-dependent skills** — anything with `scripts/` or executable
  references. These depend on tools, python modules, network endpoints,
  credentials, or MCP servers, and the rest of this spec is about them.

## Convention strength

| Requirement | Strength | Applies to |
| --- | --- | --- |
| No internal endpoints/secrets in tracked files | **Required** | every skill |
| `runtime.conf.example` when node-specific values exist | **Required** | script skills with external deps |
| `scripts/check-env.sh` | **Required** for heavy external deps (endpoints, credentials, CLIs with auth); suggested otherwise | script skills |
| Diagnose companion skill (`diagnose-<target>`) | **Suggested** — only when it earns its place | see criteria below |
| Run `scripts/check-all-env.sh` on a new node | **Required** as step one of environment migration | the human/agent operating the node |

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
- `runtime.conf` and any `.env` file are gitignored repo-wide; `*.example`
  templates are the tracked source of truth.
- Copying the example and running `check-env.sh` is the entire setup flow on a
  new node — the script's FAIL messages are the setup instructions.

## Environment self-check (`check-env.sh`)

`scripts/check-env.sh` verifies every runtime assumption the skill's scripts
depend on. Reference implementation:
`research/bilibili-transcriber/scripts/check-env.sh`.

Rules:

- One line per check: `PASS <item>` / `WARN <item> — why it's tolerable` /
  `FAIL <item> — what's missing and how to fix it`.
- Any FAIL → exit 1 after running all checks (never stop at the first).
- Tools must be **executable**, not merely present. Python deps are checked by
  importing them. Endpoints get a short-timeout curl. Credentials are checked
  by the same probe the real script would use.
- Self-locating (`SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)`), no
  dependencies beyond bash + coreutils, idempotent, fast (<10s).
- Run it: on a new node, after a service moves, before a long batch.

## Diagnose companion skills (suggested, not mandatory)

A separate `diagnose-<target>` skill (see `in-progress/diagnose-ocr-ci` for
the exemplar) is worth creating only when **all** of these hold:

1. The target system fails in **multi-layer ways** (CI pipeline layers, local
   sessions, LLM gateway, token throughput) that need a distinct diagnostic
   workflow, not just an env check.
2. Failures are **recurring** enough that a dedicated description-triggered
   skill beats inline troubleshooting.
3. Diagnosis needs its own reference material (failure taxonomies, log
   layouts, baseline metrics).

If the answer is "the script failed because the node lacks X", that's
`check-env.sh`'s job — do not create a companion skill for it. Do not
mechanically pair every skill with a diagnose skill; skill descriptions cost
context in every session.

## Environment migration flow

On a new node (or after re-imaging), in order:

1. `bash scripts/check-all-env.sh` (repo root) — runs every installed skill's
   `check-env.sh`, summarizes PASS/WARN/FAIL per skill.
2. Fix FAILs: copy the skill's `runtime.conf.example` to `runtime.conf` and
   fill in node values; install missing tools.
3. Re-run until green. Then install skills: `npx skills add -g ~/skills/
   --global -a pi -y` (see `docs/agents/install-skills.md`).

Node-level recovery (tools, kubectl, ssh targets) is a separate concern owned
by the `node-recovery` skill in the internal-skills repo; skill-level checks
assume the node works and verify the skill's own assumptions.

## Sensitive data rules (required, all skills)

This repo is **public**. Never commit:

- Internal hostnames, IPs, or registry URLs — use `runtime.conf` (gitignored)
  or neutral examples (`gitlab.example.com`, `harbor.example.com`,
  TEST-NET addresses like `203.0.113.x`) in docs and tests.
- Credentials, tokens, `.env` files, real `runtime.conf`.
- Fixtures containing internal data (trace logs, pipeline dumps) — sanitize
  them or leave them untracked.

When in doubt, run `gitleaks dir . --config
~/data/benchmark/config/gitleaks.toml` before committing.

## Promotion checklist (in-progress → category directory)

Before promoting a script-dependent skill out of `in-progress/`:

- [ ] `runtime.conf.example` exists if any node-specific value is needed
- [ ] `scripts/check-env.sh` exists for heavy external deps, runs green on at
      least one node
- [ ] no internal endpoints or secrets in tracked files (gitleaks clean)
- [ ] tests (if present) green: `uv run pytest` from the skill directory
