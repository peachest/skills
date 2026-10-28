---
name: shell-review
description: Static shell-script review as a pre-LLM mechanical gate — orchestrates bash -n, shellcheck -S style, and shfmt -d in order, passes raw tool output through, and guides severity triage (error blocks, warning/style adjudicate per finding). Use when reviewing or fixing shell scripts before or alongside LLM code review (ocr), when the user says 静态检查 shell 脚本 / shellcheck 跑一遍 / shell review / review this shell script statically, or when a shell-script fix loop needs a mechanical quality gate.
---

# shell-review

Static review gate for bash scripts. **You are the orchestrator**: run three tools
in order, show their **raw output unmodified**, then classify and adjudicate the
findings. Do not build a formatted report; do not auto-fix formatting.

Design decisions live in `<SKILL_DIR>/docs/adr/` (read ADR-0001/0002/0003 before
changing toolset, positioning, or suppression policy). Glossary: `<SKILL_DIR>/GLOSSARY.md`.

## Scope (diff-aware)

1. If the user passed explicit `.sh` paths → review exactly those.
2. Otherwise, in a git repo: review `.sh` files changed between the current
   branch and its base (default `origin/dev`, fall back to `origin/main`):

   ```bash
   git diff --name-only --diff-filter=ACMR <base>...HEAD -- '*.sh'
   ```

3. No git repo, no base branch, empty diff → say so and ask, or fall back to
   explicit paths. No full-repo sweep mode (ADR-0004).

## Orchestration (fixed order, stop early on failure)

Run each stage on the full file list; **raw output passes through verbatim** —
show it, never summarize it away (ADR-0005):

1. **Syntax gate** — `bash -n <each file>`. Any failure: stop here, report,
   do not run the later stages.
2. **Defect layer** — `shellcheck -S style -f gcc <files>` (follow `source`s:
   add `-x` when files source siblings in the same tree). This is the only
   defect detector in the chain.
3. **Format advisory** — `shfmt -d <files>`. Report-only: **never** `shfmt -w`
   or otherwise rewrite files — in reproducible-build setups script bytes feed
   the artifact digest, any rewrite causes digest drift (GLOSSARY: digest
   敏感).

Tool install note: `shellcheck` and `shfmt` are single static binaries
(standard location `~/.local/bin`). If missing, fetch the official release
binary for the arch and re-run; note the install path in your reply.

## Severity semantics

- **error** (shellcheck severity `error`, e.g. SC2155 masking a return value):
  hard fail — the script must be fixed before LLM review.
- **warning / style** (e.g. SC2086, SC2206): report and pass, each with a
  triage recommendation (below).

## Triage guide (误报定谳)

For every warning/style hit, recommend exactly one of:

1. **真修** — e.g. SC2155 (`local x=$(cmd)` swallows the exit code), SC2115
   (`rm -rf "$var/$frag"` with a possibly-empty var).
2. **场景性误报** — e.g. SC2206 on `ARRAY=($(...))` where word splitting is
   intentional. Still recommend the explicit suppression (3) so the decision
   is recorded in code.
3. **`# shellcheck disable=SCxxxx` annotation** — the only suppression
   mechanism. Rules (ADR-0003): annotation sits on the line immediately
   before the finding; the directive line syntax is strict (key=value pairs
   only — put any Chinese/explanatory text on a separate ordinary comment
   line). No built-in whitelist, no `.shellcheckrc`.

## Position vs LLM review

This skill is the **mechanical gate before LLM review** (ADR-0002): it clears
syntax/defect/format noise so the LLM review spends its turns on contracts,
comments-vs-code drift, and semantics. It does not replace LLM review and must
say so in its closing summary. Evidence that the split works: shellcheck
catches classes (SC2155-style) that multi-round LLM review repeatedly missed;
LLM review catches cross-file contract issues no linter sees.

## Closing summary shape

One short block, no table gymnastics: files reviewed, per-stage raw verdict,
error findings (blocking), warning/style hits each with its triage
recommendation, and a one-line statement that LLM review is still required.
