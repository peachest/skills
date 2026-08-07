# Method renames

After renaming a type, its method names may also need changing (e.g., `GetDeviceCount` → `DeviceGetCount` to align with a new naming convention).

gopls handles receiver-type changes automatically. Method **names** are separate — rename them one by one, repeating Phases 1-4 for each method.

When multiple methods follow the same pattern (e.g., all `Get*` → drop the `Get` prefix), `sed` is faster than gopls per method:

```bash
sed -i 's/\.GetCount\b/.Count/g' <files>
sed -i 's/\.GetHandle\b/.Handle/g' <files>
```

Always verify with `go build ./...` after the batch.

**Done when**: all method renames applied, `go build ./...` passes.
