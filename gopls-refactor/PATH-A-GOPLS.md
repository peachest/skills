# Path A — gopls rename

Use when the decision tree routed here: **not** CGo, **not** a cross-package unexport.

## Phase 2 — Validate

```bash
gopls prepare_rename <filePath>:<line+1>:<character+1>
```

(gopls CLI uses 1-based positions — add 1 to your 0-based values.)

`prepare_rename` confirms two things: (1) the cursor is on an actual identifier, not whitespace or a keyword, and (2) the LSP server can rename at this position. If it fails ("no identifier"), the position is wrong — re-check with `grep`, don't just pick a different character.

**Done when**: `prepare_rename` succeeded, `range` confirms the identifier bounds.

## Phase 4A — Execute via gopls

First, preview:

```bash
gopls rename -d <filePath>:<line+1>:<character+1> <newName>
```

`-d` produces a diff without writing. **Verify the diff is non-empty.** If empty but Phase 3 found references, gopls silently failed — fall back to [PATH-B-SED.md](PATH-B-SED.md).

If the diff is valid, apply:

```bash
gopls rename <filePath>:<line+1>:<character+1> <newName>
```

(No `-d` — writes to disk.)

Verify no stale references:

```bash
rg "\b<oldName>\b" --type go
```

**Done when**: rename applied, `rg` confirms zero stale refs.
