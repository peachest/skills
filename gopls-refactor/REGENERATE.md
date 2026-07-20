# Regenerate

After renaming interfaces that `go:generate` comments reference, regenerate mock files.

### 1. Update go:generate comments

If Phase 0c found `go:generate` lines with the old interface name:

```bash
sed -i 's/go:generate moq .*<OldInterface>/go:generate moq ... <NewInterface>/' <file>
```

### 2. Run go generate

```bash
go generate ./<packageDir>/...
```

### 3. Fix compilation errors from stale generated code

```bash
go build ./...
```

Common: mock type names still use old interface. Fix by updating references in non-generated files (the generated ones were just refreshed):

```bash
sed -i 's/mock\.<OldInterface>/mock.<NewInterface>/g' <testFiles>
```

**Done when**: `go build ./...` passes after `go generate`.
