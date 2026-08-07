# Worked example — hgml naming alignment

Walkthrough of ticket #21: rename hgml types to match go-nvml conventions.

## The rename plan

| Current | Target | Type |
|---------|--------|------|
| `Device` struct | `device` | unexport |
| `DeviceInterface` interface | `Device` | export (claims freed name) |
| `GpuInstance` struct | `gpuInstance` | unexport |
| `GpuInstanceInterface` interface | `GpuInstance` | export |
| `ComputeInstance` struct | `computeInstance` | unexport |
| `ComputeInstanceInterface` interface | `ComputeInstance` | export |
| `GetDeviceCount()` | `DeviceGetCount()` | method |
| `GetDeviceHandle(index)` | `DeviceGetHandleByIndex(index)` | method |

## Execution order (ORDERING-RULES.md)

Structs first, then interfaces, then methods, then go generate:

1. `Device` struct → `device` (Path B — CGo file)
2. `DeviceInterface` interface → `Device` (Path A — pure Go, no cross-pkg unexport issue since we just freed the name)
3. `GpuInstance` struct → `gpuInstance` (Path B)
4. `GpuInstanceInterface` → `GpuInstance` (Path A)
5. `ComputeInstance` struct → `computeInstance` (Path B — has cross-pkg refs in mock files)
6. `ComputeInstanceInterface` → `ComputeInstance` (Path A)
7. `GetDeviceCount` → `DeviceGetCount` (Path A — method rename on pure Go interface)
8. `GetDeviceHandle` → `DeviceGetHandleByIndex` (Path A)
9. Update `go:generate` comments, run `go generate`, fix compilation

## Step-by-step: rename #1 (Device struct → device)

**Phase 0**: `hgml/hgml.go` has `import "C"` → CGo → will use Path B. Not an unexport (uppercase→uppercase? no — Device→device IS uppercase→lowercase → unexport = yes). But struct unexporting is in the owning package only — cross-pkg refs unlikely. Let Phase 3 confirm.

**Phase 1**: `gopls definition hgml/hgml.go:#Device` → `hgml/hgml.go:313:6` → line=312, char=5 (0-based).

**Phase 3**: `gopls references hgml/hgml.go:313:6` → 30 references, all in `hgml/hgml.go` — no cross-package refs. But CGo → Path B regardless.

**Phase 4B** (sed):
```bash
sed -i 's/\bDevice\b/device/g' hgml/hgml.go
```

Wait — this would also rename field names like `Device` in struct definitions! Need more precision. The references list tells us: only the type definition and receiver types use bare `Device`. Let's use the reference list as our guide:

```bash
# Type definition only (line 313):
sed -i '313s/^type Device /type device /' hgml/hgml.go
# All receiver patterns (*Device) → (*device):
sed -i 's/(d \*Device)/(d *device)/g; s/(\*Device)/(*device)/g' hgml/hgml.go
```

Actually, gopls `references` works even for CGo files to locate positions. Use the reference list's line numbers to construct precise sed commands, or simpler: just replace all occurrences and verify.

```bash
sed -i 's/\*Device\b/*device/g; s/^type Device /type device /' hgml/hgml.go
rg '\bDevice\b' hgml/hgml.go  # verify — only field name Device remains
```

**Phase 6b**: `go build ./hgml/...` → passes. Struct freed.

## Step-by-step: rename #2 (DeviceInterface → Device)

**Phase 0**: `hgml/lib.go` — pure Go, no CGo. Not unexport (DeviceInterface→Device stays uppercase). No go:generate in this rename (that's a separate concern).

**Phase 1**: `gopls definition hgml/lib.go:#DeviceInterface` → `hgml/lib.go:10:6`.

**Phase 3**: `gopls references hgml/lib.go:11:6` → refs in `lib.go`, `mock/mock.go`, `hglib/hglib.go`, `server.go`, `util/ppu.go` — ~15 refs, all within same workspace. No cross-package visibility issues since we already freed `Device` in step 1.

**Phase 4A** (gopls):
```bash
gopls rename -d hgml/lib.go:11:6 Device  # preview
gopls rename hgml/lib.go:11:6 Device     # apply
```

**Phase 6b**: `go build ./...` → passes. `go test ./...` → passes.

## Key lesson from this example

The "struct first, interface second" ordering is critical. Renaming `DeviceInterface`→`Device` in step 2 only works because step 1 already released the name `Device` from the struct. If we had tried step 2 first, gopls would have failed with a name conflict.
