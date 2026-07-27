# project-wiki

A self-maintaining code knowledge base that gives AI sessions and new
teammates a structured, always-current map of the codebase's modules and
files. Drift between code and wiki is detected via SHA baseline comparison.

## Language

### Structure

**Wiki**:
The entire knowledge base — the `docs/project_wiki/` directory and everything
in it. The canonical artifact this skill produces and maintains.
_Avoid_: knowledge base, code map, documentation

**Overview**:
The L1 entry point file (`overview.md`). A single table indexing all
modules with one-line responsibilities. Loaded into every AI context
window; kept under 5 KB.
_Avoid_: index, summary, project description

**Module wiki**:
An L2 file (`<module>.md`) containing the file registration table for one
module. Each row is a source file with a one-line responsibility.
_Avoid_: module doc, file listing, module description

**Semantic bridge**:
An L3 file mapping an external vocabulary (design tokens, API fields,
product terms) to code identifiers. Hand-curated, not auto-generated.
Examples: `glossary.md`, `api_mapping.md`, `design_token_mapping.md`.
_Avoid_: mapping table, translation layer, lookup table

**Registration table**:
The two-column table (File | Description) inside a module wiki. Every
source file in the module must be registered — no omissions.
_Avoid_: file list, inventory, manifest

### Detection

**Module**:
A grouping of source files by top-level directory under the project root.
The first path component of a file's relative path determines its module.
Files at the repo root belong to the `root` module.
_Avoid_: package, namespace, component (those are language-native concepts)

**Drift**:
The state of the wiki being out of sync with the code. Detected by
comparing current file SHAs against the SHA baseline.
_Avoid_: discrepancy, mismatch, outdated

**Stale**:
A file exhibiting drift. A stale file is one that is new (in code, not in
baseline), deleted (in baseline, gone from code), or modified (SHA changed
since last review).
_Avoid_: dirty, pending, invalid

**SHA baseline**:
The snapshot of every tracked file's SHA1 at the moment it was last
reviewed. Stored in `.review_cache.json` (gitignored). Refreshed by the
`update` command after the wiki has been edited.
_Avoid_: cache, checksum store, hash table

**Triage**:
The three-color classification of stale files: 🟡 new, 🔴 deleted, 🟠
modified. Each color maps to a specific maintenance action.
_Avoid_: report, diff, status check

**Reviewed**:
The state of a tracked file whose SHA has been captured in the baseline
after the wiki was last edited. `update` marks all current files as
reviewed; new files found by `check` are unreviewed until the next
`update`.
_Avoid_: committed, synced, verified
