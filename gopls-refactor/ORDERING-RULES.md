# Ordering rules

When both a struct and an interface target the same name (e.g., `Device` struct → `device`, `DeviceInterface` → `Device`), rename in this order:

1. **Structs first** — unexport structs to free their names
2. **Interfaces second** — rename interfaces to claim the freed names
3. **Methods third** — rename methods on the renamed interfaces
4. **go generate last** — regenerate mocks after all interface names are final

Each step is a complete rename through Phases 1-6. Don't batch them — complete one (build + test passing) before starting the next.

Why: the struct holds the exportable name. Renaming it releases that name. If you rename the interface first, it claims a name that still conflicts with the struct.
