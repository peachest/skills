# Path B — sed fallback

Use when the decision tree routed here: **CGo file** or **cross-package unexport** or **gopls silently failed**.

## Phase 4B — Execute via sed

Use word-boundary matching. Treat the owning package and consuming packages separately:

```bash
# Within the owning package (bare name: device, Device):
sed -i 's/\b<OldName>\b/<newName>/g' <packageDir>/*.go

# In other packages (qualified: hgml.Device):
sed -i 's/<package>\.<OldName>\b/<package>.<newName>/g' <file1> <file2> ...
```

For unexporting (uppercase→lowercase), the second `sed` is critical — cross-package references use the exported form `pkg.OldName`.

Verify:

```bash
rg "\b<oldName>\b" --type go   # must be empty
```

Phase 3's reference list is your checklist — cross off each file as you verify it.

**Done when**: `rg` finds zero stale references.
