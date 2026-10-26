---
name: setup-gitleaks
description: Set up a per-repo credential/sanitize gate with gitleaks — a custom rules file (gitleaks.toml), a two-layer sanitize-check.sh (gitleaks credentials + grep identifier patterns), an AGENTS.md pointer, and pre-push enforcement. Use when the user asks to 给仓库配置 gitleaks / 凭证闸门 / sanitize check / 脱敏检查 / 防泄漏 gate, or when a repo is about to be pushed, shared, or published and needs a leak gate. Covers public-repo, internal-repo, and desensitized-data validation shapes.
---

# Setup a gitleaks credential gate

`<SKILL_DIR>` = this skill directory. `<PROJECT_DIR>` = the repo being gated.

The gate is **two layers**, and the split is the design:

1. **gitleaks layer** — credentials only: passwords, tokens, API keys, private
   keys, connection strings. Custom `[[rules]]` because gitleaks' default rule
   set cannot know repo-specific secrets.
2. **pattern layer** — identifiers gitleaks cannot judge: internal domains,
   node names, project names, person names. A `grep -E` pass in the same gate
   script.

**gitleaks passing ≠ sanitize complete.** Rule files and checker output must
carry this boundary explicitly, or reviewers assume a green gate means clean.

## Step 1 — Harvest rule candidates

Secrets live where the repo's real workflow puts them. Collect patterns from:

- `git log -p` history — passwords/tokens committed before the gate existed
- credential files the repo expects: `.env`, `runtime.conf`, kubeconfig paths
- handoff docs, resource ledgers, scripts that ssh into known hosts

One `[[rules]]` entry per secret family, each with `id`, `description`,
`regex` (Go RE2, use `'''...'''` raw strings), and `tags`. Start from
`<SKILL_DIR>/templates/gitleaks.toml` — it ships only placeholder patterns;
replace them with the target repo's real ones. Real patterns belong in the
gated repo, never in a public repo or this skill.

## Step 2 — Adapt the gate script

Copy `<SKILL_DIR>/templates/sanitize-check.sh` into `<PROJECT_DIR>/scripts/`
and fill in:

- `PATTERNS` — the layer-1 `grep -E` alternation for this repo's identifiers.
  Word-bound tokens that are also common substrings (`\b<platform>\b`).
- `GITLEAKS_CONFIG` default — point at the repo's own `gitleaks.toml`.

Keep the three file-selection modes: tracked files (default), untracked +
modified (`-u`, pre-commit batch review), explicit paths. These modes decide
what the layers scan — a whole-tree scan flags vendored code and caches.

Keep these **allowlist** entries in `gitleaks.toml` (they exist for reasons
that recur in every repo):

- `gitleaks.toml` itself and `scripts/sanitize-check.sh` — both contain the
  patterns; otherwise the gate self-matches forever
- `.env` — credentials live there by design (see Step 3)
- caches and agent state: `.git/`, `__pycache__/`, `.venv/`, `.pi/`,
  `.pi-subagents/`, `.scratch/`
- vendored upstream trees and captured data artifacts — scanned separately or
  not at all, deliberately
- files whose content IS redaction patterns (anonymizer replacers) — patterns
  are not secrets

Every allowlist line gets a comment saying why. An uncommented allowlist entry
is an unreviewed hole.

## Step 3 — Credential placement contract

The gate only works with a home for secrets:

- secrets go in `<PROJECT_DIR>/.env` (gitignored), with a tracked
  `.env.example` template
- variable-based usage is fine: `sshpass -e` with `SSHPASS` from `.env`
- literal usage is a violation and gets its own rule (`inline-sshpass` in the
  template) so the fix is mechanical: switch to the variable form

State this contract in the repo's AGENTS.md next to the gate pointer.

## Step 4 — Wire the pointers

One line in `<PROJECT_DIR>/AGENTS.md` (or the repo's agent instructions):
when to run the gate (before push/commit/share), what the two layers are,
where the rules live, where secrets belong. The pointer wording decides
whether agents run the gate — front-load the trigger ("入库/分享前跑…").

## Step 5 — Enforcement ladder

Manual run → AGENTS.md pointer → **pre-push hook**. A rule enforced only by
agent memory is not enforced: agents follow fresh rules and abandon them days
later. Hard rules must be script gates. For git repos, install a `pre-push`
hook (`core.hooksPath`) that gitleak-scans the exact commits being pushed
(`git rev-list <remote>..<local>`) and blocks on any finding. Non-git trees
(data snapshots) keep the manual entry point and say so.

## Step 6 — Verify the gate

A gate that has never failed is unverified. Run `<SKILL_DIR>/tests/test_gate.sh`
after adapting the templates: it seeds a known placeholder secret and expects
exit 1 with the finding, expects exit 0 on a clean tree, and expects a WARN
(not a silent pass) when gitleaks or the config is missing. Re-run after any
rule change: bad fixtures must FAIL, the clean tree must stay green.

The template self-check proves the templates work, not that **your** adapted
rules catch this repo's real secret shapes. On the real repo, run a canary
pass before trusting the gate:

1. Seed a **real variant form** — a shape your rules should catch but the
   template placeholder never exercises (e.g. `VAR_PASSWORD="..."` with a
   variable-name prefix, or a literal from the repo's own CI/config style).
   The llmops-wiki 2026-10-26 case: `\\b(password)` left the `\\b` boundary
   dead in front of `_`, so `REDIS_PASSWORD=` passed clean until a canary
   with the prefix form caught it.
2. Put the canary **inside the repo**. A path outside the worktree makes
   `git add` fail with rc=1 — a git error masquerading as a block.
3. Assert a **positive hit**: the output must name the rule-id (e.g.
   `GITLEAKS <file>:<line> <rule-id>`). Exit codes alone prove nothing:
   rc=1 can come from a git failure, rc=0 from the check never running.
4. After a blocked hook run, confirm with `git log --oneline -1` that the
   canary commit **does not exist** — a silent hook is an unverified gate,
   and the seeded secret is now in history. Then remove the canary, re-run,
   expect CLEAN.

## Triage a finding before acting

A gitleaks hit — especially from a whole-tree `gitleaks dir` scan — is a
trigger to investigate, not a verdict. Before deleting a file or rewriting
history, verify in order: `git ls-files` (is the path actually tracked?),
`git log -p -- <path>` (does the secret exist in reachable history?), and
remote branches (`git branch -r` / the push target). A hit in an untracked
cache, a vendored tree, or a file never committed is not a leak — deleting
the file fixes nothing and may destroy the only copy. Action follows
verification, never the raw scan output.

## Scope shapes

| Repo shape | Pattern layer | gitleaks rules |
|---|---|---|
| public repo | internal identifiers + domain-placeholder allowlist | credentials only |
| internal repo | credentials only — internal hostnames/IPs are expected content, drop that layer | credentials only |
| desensitized-data validation | full internal check (domains, IPs, SSO/registry URLs) | credentials + structural leaks (connection strings) |

Derive from the consumer: a gate for a public audience must flag everything
internal; a gate for an internal-only repo would false-positive on its own
hostnames and teach reviewers to ignore it.
