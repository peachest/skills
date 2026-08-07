---
name: gopls-refactor
description: >
  Go symbol rename using gopls. Use when the user asks to rename a symbol
  (rename X to Y, 改名, 重命名), fix naming conventions or align names with
  a reference (命名对齐, naming alignment), or unexport a type (私有化,
  make private). Also use when an implement ticket describes a rename.
---

# gopls Refactoring

**gopls** is Go's LSP server. It renames symbols with semantic precision — scope, packages, and interface implementations all handled correctly.

Three blind spots, each with a known fallback to `sed`:

- **CGo files** (`import "C"`) — gopls's type-checker cannot parse the C preamble, so it cannot rename inside these files.
- **Unexporting** (uppercase→lowercase) when other packages reference the symbol — gopls's visibility rules treat this as illegal, so it refuses.
- **`go:generate` comments** — gopls renames Go identifiers, not comment text, so lines like `//go:generate moq ... DeviceInterface` must be updated by hand.

See [WORKED-EXAMPLE.md](WORKED-EXAMPLE.md) for an end-to-end walkthrough (renaming `DeviceInterface`→`Device` in the hgml package).

## Phase 0 — Collect facts

Run all four checks. Don't decide the path yet — you need Phase 3's reference list first.

### 0a. CGo?

```bash
head -5 <file> | grep 'import "C"'
```

If yes: gopls will fail on this file. You'll use `sed` in Phase 4.

### 0b. Unexport?

```bash
echo <oldName> | grep -q '^[A-Z]' && echo <newName> | grep -q '^[a-z]' && echo "UNEXPORT"
```

If yes: gopls may refuse if cross-package refs exist. Phase 3 resolves this.

### 0c. go:generate?

```bash
rg "go:generate.*<oldName>" <packageDir>/
```

If yes: these comments must be updated manually before running `go generate` in Phase 6.

### 0d. Struct + interface pair?

Same-name struct and interface being renamed together? Structs must go first — see [ORDERING-RULES.md](ORDERING-RULES.md).

**Done when**: all four answers recorded.

## Phase 1 — Locate

For non-CGo:

```bash
gopls definition <file>:#<symbolName>
```

The `#` prefix tells gopls to search by name rather than position. Character in output is 1-based — subtract 1.

For CGo, or when `gopls definition` returns nothing:

```bash
grep -n "^type <name> \|^func.* <name>(" <file>
```

**Done when**: absolute `filePath`, 0-based `line`, 0-based `character`.

## Phase 3 — Blast radius

```bash
gopls references <filePath>:<line+1>:<character+1>
```

(gopls CLI uses 1-based positions — add 1.)

For unexport candidates (Phase 0b = yes): also grep cross-package references — gopls may miss these when the symbol is being unexported.

```bash
rg "\.<oldName>\b" --type go
```

Pause if 10+ files. **Done when**: you know every file that changes, and whether cross-package refs exist.

## Phase 4 — Choose path and execute

Now you have all facts. Route:

```
CGo? ── yes ──► Path B (sed)
  │ no
Unexport AND cross-pkg refs exist? ── yes ──► Path B (sed)
  │ no ──► Path A (gopls)
```

- **Path A** → [PATH-A-GOPLS.md](PATH-A-GOPLS.md)
- **Path B** → [PATH-B-SED.md](PATH-B-SED.md)

One rename at a time. If Phase 0d fires (struct+interface pair), rename the struct first.

## Phase 5 — Method renames

If renaming methods on the already-renamed type → [METHOD-RENAMES.md](METHOD-RENAMES.md).

## Phase 6 — Rebuild

### 6a. Regenerate

If Phase 0c found `go:generate` lines → [REGENERATE.md](REGENERATE.md).

### 6b. Build + test

```bash
go build ./...
go test ./...
```

Expected errors and their fixes:

| Error pattern | Fix |
|--------------|-----|
| `mock.OldInterface undefined` in non-generated files | `sed -i 's/mock\.Old/mock.New/g' <testFiles>` — `go generate` only refreshes generated files, not hand-written references |
| Method `OldName not found` | Rerun Phase 5 — method rename was missed |
| `imported and not used` | `goimports -w <file>` |
| Generated file still has old names | `go generate` didn't run or `go:generate` comments weren't updated — back to 6a |

**Done when**: `go build ./...` and `go test ./...` both pass.

## Emergency exits

| Symptom | Why | Action |
|---------|-----|--------|
| `gopls: command not found` | Tool not installed | `go install golang.org/x/tools/gopls@latest` |
| CGo file `prepare_rename` fails | gopls can't parse C preamble | Expected — Path B |
| `prepare_rename` fails on non-CGo | Cursor not on an identifier | Re-check position with `grep` |
| `gopls rename -d` produces empty diff but Phase 3 found refs | gopls silently failed (CGo or cross-pkg visibility) | Fall back to Path B |
| Diff includes unexpected files | The symbol has callers you didn't anticipate | Show diff, ask user before applying |
