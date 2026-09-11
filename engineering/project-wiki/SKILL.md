---
name: project-wiki
description: Survey the codebase terrain once, keep the chart current with SHA-based drift detection, so orienting starts from a map instead of a blank.
disable-model-invocation: true
---

# project-wiki

A self-maintaining codebase **chart** that lets any AI session or new teammate
**orient** in seconds instead of surveying blindly. Survey the terrain once,
keep the chart current, and every subsequent orient begins from a map.

> **Path convention**: `<SKILL_DIR>` is this skill's directory (holds
> `scripts/`, `references/`, `CONTEXT.md`, and the machine-specific
> `runtime.conf`). `<PROJECT_DIR>` is the project being documented (holds
> source code and receives `docs/project_wiki/`).

## What it produces

```
docs/project_wiki/
├── overview.md            # L1: module index table (name + responsibility + link)
├── <module-a>.md          # L2: file registration table for module-a
├── <module-b>.md          # L2: file registration table for module-b
├── ...
├── .review_cache.json     # SHA baseline (gitignored, not committed)
└── (optional)             # L3: legend — hand-curated by the user
    ├── glossary.md
    ├── api_mapping.md
    └── design_token_mapping.md
```

## The three levels

- **L1 — Overview** (`overview.md`): module index table, one line per
  module. The master chart, loaded into every AI context window; kept under 5 KB.
- **L2 — Module charts** (`<module>.md`): file registration table per
  module — every source file with a one-line responsibility.
- **L3 — Legend** (optional): mappings from external
  vocabularies (design tokens, API fields, product terms) to code symbols.
  Hand-curated by the user; this skill generates L1 and L2 only.
  If a `CONTEXT.md` (domain glossary) or `docs/adr/` (architectural
  decisions) exist at the project root — typically produced by the
  `/skill:domain-modeling` skill — `init` auto-detects them and links
  them from `overview.md` as the L3 legend layer.

Full format spec with examples: [references/wiki_format.md](./references/wiki_format.md).

## CLI tool

All deterministic operations are handled by a bundled CLI. The skill ships
**two interchangeable runtimes** — Python (`scripts/wiki.py`) and Node.js
(`scripts/wiki.js`, zero external dependencies) — that produce identical
wikis and share the same SHA baseline, so they can be mixed freely on one
project (e.g. `init` with Python, then `check` with Node).

`<cmd>` below is the resolved CLI command — resolve it once per
*Platform Detection & CLI Routing* below (`runtime.conf` is the fast
path; detection is the fallback). `--root` defaults to the current
directory; pass `--root <PROJECT_DIR>` to run from elsewhere.

```bash
# Survey: scan project, detect modules, generate chart skeleton
<cmd> init [--root <PROJECT_DIR>] [--lang auto] [--json]

# Resurvey: report drift (new / deleted / modified files since last survey)
<cmd> check [--root <PROJECT_DIR>] [--fail-on-stale] [--json]

# Re-baseline: refresh SHA baseline after chart has been reviewed/edited
<cmd> update [--root <PROJECT_DIR>] [--json]

# Coverage: show chart coverage summary
<cmd> status [--root <PROJECT_DIR>] [--json]
```

`--json` emits one machine-readable JSON object on stdout instead of the
human report — for CI, git hooks, and other agents. Shape:

```json
{
  "command": "check",
  "ok": false,
  "summary": {"tracked": 5, "in_wiki": 5, "current": 6, "new": 1,
               "deleted": 0, "modified": 0, "l3_drift": 0, "integrity": 2},
  "signals": [{"code": "WIKI-NEW-FILE", "path": "src/x.go",
               "detail": "in code, not yet in wiki"}]
}
```

## Stable signal codes

Every stale/finding carries a stable code (`WIKI-*`). Codes are a public
contract: adding new ones is additive, renaming is a breaking change.

| Code | Fires when | Signal |
| ---- | ---------- | ------ |
| `WIKI-NEW-FILE` | File in code, not in SHA baseline | 🟡 |
| `WIKI-DELETED-FILE` | In baseline, gone from code | 🔴 |
| `WIKI-MODIFIED-FILE` | SHA changed since last review | 🟠 |
| `WIKI-L3-DRIFT` | CONTEXT.md / ADRs exist but overview.md doesn't link (or vice versa) | 🔵 |
| `WIKI-MODULE-WIKI-MISSING` | Module has source files but no `<module>.md` registration table | 🟣 |
| `WIKI-OVERVIEW-MODULE-MISMATCH` | overview.md module index ≠ actual module set | 🟣 |
| `WIKI-UNREGISTERED-FILE` | Source file missing from its module's registration table | 🟣 |
| `WIKI-ORPHAN-ENTRY` | Registration row for a file not present in code | 🟣 |

The four 🟣 **wiki self-integrity** codes assert three-way consistency:
overview module index ↔ module wiki files ↔ registration-table rows. They
fire even when the SHA baseline itself is clean — e.g. someone hand-deleted
a registration row or an overview module row. `update` repairs
`WIKI-MODULE-WIKI-MISSING` (it regenerates missing module skeletons) and
`WIKI-OVERVIEW-MODULE-MISMATCH` (it regenerates the overview); registration
rows are filled in by the AI/human workflow, never auto-generated with
descriptions.

Exit codes (all commands): `0` = ok, `1` = drift detected with
`--fail-on-stale` (check only), `2` = error (e.g. no wiki initialized).

## Platform Detection & CLI Routing

### Pre-detected Runtime

If `<SKILL_DIR>/runtime.conf` exists, read the `Runtime` and `Command`
values from it and skip detection — this is the fast path for routine
calls. The file is machine-specific (gitignored; see
`runtime.conf.example` for the template). If it is absent or the
configured command fails, fall back to the full detection procedure.

### Detection Procedure

At first use, detect the best available runtime. Priority order:

```
Python  >  Node.js
```

Run these checks in order. The first success determines the active CLI:

**Step 1 — Check Python**

```bash
python3 --version 2>&1   # need >= 3.6
python --version 2>&1    # also valid on some systems
```

- If `python3` (or `python`) exists → use
  `python3 <SKILL_DIR>/scripts/wiki.py`
- No external dependencies (stdlib only).

**Step 2 — Check Node.js** (if Python failed)

```bash
node --version 2>&1      # need >= 12
```

- If exit code 0 → use `node <SKILL_DIR>/scripts/wiki.js`
- No external dependencies (built-in `fs` / `crypto` / `path` only).

### CLI Invocation

Once the active CLI is determined, all commands use the same subcommand
syntax:

| Runtime | Invocation |
|---------|-----------|
| Python  | `python3 <SKILL_DIR>/scripts/wiki.py <command> [options]` |
| Node.js | `node <SKILL_DIR>/scripts/wiki.js <command> [options]` |

### Fallback & Error Handling

- If the selected CLI fails with a runtime error, fall through to the
  next runtime in priority order.
- If **all** runtimes fail, report that no compatible runtime was found
  and list the minimum requirements (Python 3.6+ or Node.js 12+).

## Workflow

### 1. Survey the terrain

```bash
<cmd> init --root <PROJECT_DIR>
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

### 2. Fill in the chart (AI-assisted)

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
   <cmd> update --root <PROJECT_DIR>
   ```

**Completion criterion**: zero placeholder descriptions remain across all
module wikis and `overview.md`.

### 3. Ongoing maintenance — survey drift

As code changes, the wiki goes stale. The `check` command detects three
types of file drift plus L3 domain-language connectivity drift:

| Signal | Meaning | Action | Color |
| ------ | ------- | ------ | ----- |
| **NEW** | File in code, not on the chart | Register it in the module chart | 🟡 |
| **DELETED** | File on the chart, gone from code | Remove its row from the module chart | 🔴 |
| **MODIFIED** | SHA changed since last survey | Update description if responsibility changed; else just re-`update` | 🟠 |
| **L3 DRIFT** | CONTEXT.md or ADRs exist but overview.md doesn't link (or vice versa) | Run `update` to re-link | 🔵 |
| **INTEGRITY** | overview index ↔ module wikis ↔ registration tables are out of sync (see signal codes above) | `update` for skeletons/overview; hand-sync registration rows | 🟣 |

```bash
<cmd> check --root <PROJECT_DIR>
```

After resolving all stale signals, re-register the baseline:

```bash
<cmd> update --root <PROJECT_DIR>
```

**Completion criterion**: `check` reports zero stale signals — including
the 🟣 integrity signals (zero placeholders is not enough; the three-way
overview ↔ module wiki ↔ registration-table consistency must also hold).
In CI or hooks, use `check --fail-on-stale --json` for a machine-readable,
fail-closed gate.

### 4. Periodic resurvey

```bash
<cmd> status --root <PROJECT_DIR>
```

Shows module count, tracked files, described entries ratio, unreviewed
files, last-updated timestamp.

## When to use this skill

- **New project / codebase**: run `init` to survey the terrain, then
  fill in the chart.
- **Existing project without a chart**: same — `init` + fill.
- **Onboarding**: point new teammates (or AI sessions) at `overview.md`
  first, then the relevant `<module>.md`.
- **Before a big refactor**: ensure the chart is current so orienting
  starts from accurate terrain.
- **After merging a large feature**: run `check`, update the chart for new
  files, run `update`.
- **CI integration**: `check --fail-on-stale` returns exit code 1 on
  drift, suitable for CI pipelines or git hooks (user-configured).

## Language support

Auto-detects: Go, Python, JavaScript/TypeScript, Vue, Rust, Java, Kotlin,
Swift, ObjC, C/C++, Ruby, PHP, C#, Scala, Elixir, Lua, Dart.

Override with `--lang <language>` or `--extensions .ext1,.ext2`.

Test files, generated files (`*.pb.go`, `zz_generated_*`), vendored
code, and build artifacts are automatically skipped.

## Evidence boundary

A green `check` proves only that the chart **structurally covers** the code:
the registration tables list every tracked file, the overview index matches
the actual module set, and the SHA baseline is current. It does **not** prove
that any one-line description is accurate — description quality is produced
by the fill-in workflow (step 2), not verified by this tool. A wrong or stale
description on an unchanged file will never be flagged. Treat `check` as a
coverage/consistency gate, not a correctness oracle.

## Verify

This skill carries a fail-closed test suite covering both runtimes (positive
drift shapes, negative fail-closed shapes, and Python↔Node JSON parity):

```bash
cd <SKILL_DIR> && uv run pytest
```

Run it after modifying `scripts/wiki.py` or `scripts/wiki.js`. When touching
one runtime, keep the other in lockstep — the parity tests enforce it.

## Domain language

Vocabulary: [CONTEXT.md](./CONTEXT.md). Architectural decisions:
[docs/adr/](./docs/adr/).
