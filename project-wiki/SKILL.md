---
name: project-wiki
description: Generate and maintain a three-level project wiki with SHA-based drift detection.
disable-model-invocation: true
---

# project-wiki

A self-maintaining codebase map that lets any AI session or new teammate
orient in seconds instead of grep-ing blindly.

> **Path convention**: `<SKILL_DIR>` is this skill's directory (holds
> `scripts/`, `references/`, `CONTEXT.md`). `<PROJECT_DIR>` is the project
> being documented (holds source code and receives `docs/project_wiki/`).

## What it produces

```
docs/project_wiki/
├── overview.md            # L1: module index table (name + responsibility + link)
├── <module-a>.md          # L2: file registration table for module-a
├── <module-b>.md          # L2: file registration table for module-b
├── ...
├── .review_cache.json     # SHA baseline (gitignored, not committed)
└── (optional)             # L3: semantic bridges — hand-curated by the user
    ├── glossary.md
    ├── api_mapping.md
    └── design_token_mapping.md
```

## The three levels

- **L1 — Overview** (`overview.md`): module index table, one line per
  module. Loaded into every AI context window; kept under 5 KB.
- **L2 — Module wikis** (`<module>.md`): file registration table per
  module — every source file with a one-line responsibility.
- **L3 — Semantic bridges** (optional): mappings from external
  vocabularies (design tokens, API fields, product terms) to code.
  Hand-curated by the user; this skill generates L1 and L2 only.
  If a `CONTEXT.md` (domain glossary) or `docs/adr/` (architectural
  decisions) exist at the project root — typically produced by the
  `/skill:domain-modeling` skill — `init` auto-detects them and links
  them from `overview.md` as the L3 domain-language layer.

Full format spec with examples: [references/wiki_format.md](./references/wiki_format.md).

## CLI tool

All deterministic operations are handled by `<SKILL_DIR>/scripts/wiki.py`.
`--root` defaults to the current directory; pass `--root <PROJECT_DIR>` to
run from elsewhere:

```bash
# Initialize: scan project, detect modules, generate wiki skeleton
python3 <SKILL_DIR>/scripts/wiki.py init [--root <PROJECT_DIR>] [--lang auto]

# Check: report drift (new / deleted / modified files since last review)
python3 <SKILL_DIR>/scripts/wiki.py check [--root <PROJECT_DIR>] [--fail-on-stale]

# Update: refresh SHA baseline after wiki has been reviewed/edited
python3 <SKILL_DIR>/scripts/wiki.py update [--root <PROJECT_DIR>]

# Status: show coverage summary
python3 <SKILL_DIR>/scripts/wiki.py status [--root <PROJECT_DIR>]
```

## Workflow

### 1. Initialize the wiki

```bash
python3 <SKILL_DIR>/scripts/wiki.py init --root <PROJECT_DIR>
```

Scans the project, detects the language, groups files into modules by
top-level directory, and generates:

- `<PROJECT_DIR>/docs/project_wiki/overview.md` — module index with placeholder descriptions
- `<PROJECT_DIR>/docs/project_wiki/<module>.md` — file registration tables with placeholder descriptions
- `<PROJECT_DIR>/docs/project_wiki/.review_cache.json` — SHA baseline (gitignored)

After `init`, **every file entry has a `<describe ...>` placeholder**.

**Completion criterion**: every `<module>.md` exists with a registration
table listing all source files in that module; `overview.md` lists every
module.

### 2. Fill in descriptions (AI-assisted)

For each module wiki:

1. Read the registered source files — package/interface declarations
   suffice; not every line.
2. **Register** each file with a one-line responsibility:

   ```
   | `src/auth/login.go` | **Login handler** — validates credentials, issues JWT |
   ```

   - **Bold role** (the file's primary purpose), then a dash and
     specifics.
   - One line — this is an index, not documentation.

3. Fill in `overview.md` module descriptions — one line per module.
4. Run `update` to mark the wiki as reviewed:

   ```bash
   python3 <SKILL_DIR>/scripts/wiki.py update --root <PROJECT_DIR>
   ```

**Completion criterion**: zero placeholder descriptions remain across all
module wikis and `overview.md`.

### 3. Ongoing maintenance — drift detection

As code changes, the wiki goes stale. The `check` command detects three
types of file drift plus L3 domain-language connectivity drift:

| Signal | Meaning | Action | Color |
| ------ | ------- | ------ | ----- |
| **NEW** | File in code, not in wiki/baseline | Register it in the module wiki | 🟡 |
| **DELETED** | File in wiki/baseline, gone from code | Remove its row from the module wiki | 🔴 |
| **MODIFIED** | SHA changed since last review | Update description if responsibility changed; else just re-`update` | 🟠 |
| **L3 DRIFT** | CONTEXT.md or ADRs exist but overview.md doesn't link (or vice versa) | Run `update` to re-link | 🔵 |

```bash
python3 <SKILL_DIR>/scripts/wiki.py check --root <PROJECT_DIR>
```

After resolving all stale signals, re-register the baseline:

```bash
python3 <SKILL_DIR>/scripts/wiki.py update --root <PROJECT_DIR>
```

**Completion criterion**: `check` reports zero stale signals.

### 4. Periodic audit

```bash
python3 <SKILL_DIR>/scripts/wiki.py status --root <PROJECT_DIR>
```

Shows module count, tracked files, described entries ratio, unreviewed
files, last-updated timestamp.

## When to use this skill

- **New project / codebase**: run `init` to generate the skeleton, then
  fill in descriptions.
- **Existing project without wiki**: same — `init` + fill.
- **Onboarding**: point new teammates (or AI sessions) at `overview.md`
  first, then the relevant `<module>.md`.
- **Before a big refactor**: ensure wiki is up to date so the AI has an
  accurate map.
- **After merging a large feature**: run `check`, update wiki for new
  files, run `update`.
- **CI integration**: `check --fail-on-stale` returns exit code 1 on
  drift, suitable for CI pipelines or git hooks (user-configured).

## Language support

Auto-detects: Go, Python, JavaScript/TypeScript, Vue, Rust, Java, Kotlin,
Swift, ObjC, C/C++, Ruby, PHP, C#, Scala, Elixir, Lua, Dart.

Override with `--lang <language>` or `--extensions .ext1,.ext2`.

Test files, generated files (`*.pb.go`, `zz_generated_*`), vendored
code, and build artifacts are automatically skipped.

## Domain language

Vocabulary: [CONTEXT.md](./CONTEXT.md). Architectural decisions:
[docs/adr/](./docs/adr/).
