---
name: python-design
description: Python project design patterns for data models, validation, pipeline composition, plugin architecture, serialization, and state context. Use when structuring a Python project or module, choosing between dataclass/TypedDict/Protocol/BaseModel, designing validation or error-aggregation strategy, building a pipeline or processor chain, creating a plugin or extension system, propagating context implicitly, or choosing between Protocol/ABC, sync/async, or eager/lazy validation.
---

# Python Design

Design patterns extracted from 35 mainstream Python projects. The patterns database (`references/patterns-db.json`) contains 425 patterns across 11 dimensions; this skill surfaces the **60 high-frequency patterns** (≥3 project validations) as actionable reference.

## Workflow

1. Identify the design dimension.
2. Load the matching reference file for concrete patterns with code.
3. Consult [decisions.md](references/decisions.md) for trade-off guides (dataclass vs TypedDict, Protocol vs ABC, eager vs lazy, sync/async strategies).
4. Consult [CONTEXT.md](CONTEXT.md) for pattern glossary, cross-cutting concerns, and dimension definitions.

## Pattern reference by dimension

| Dimension | Key question | File |
|-----------|-------------|------|
| Data modeling, Validation, Serialization | How to model, validate, and serialize data? | [data.md](references/data.md) |
| Pipeline composition, Error strategy, Sync/async | How to chain stages, handle errors, bridge sync/async? | [flow.md](references/flow.md) |
| Interface design, Module organization | Protocol vs ABC? Public vs internal? | [structure.md](references/structure.md) |
| Plugin architecture, Config management, State context | How to extend, configure, and propagate context? | [extension.md](references/extension.md) |

## References

- [decisions.md](references/decisions.md) — 10 decision guides for common design trade-offs
- [CONTEXT.md](CONTEXT.md) — Pattern glossary, cross-cutting concerns, dimension definitions
- [patterns-db.json](references/patterns-db.json) — Full database (425 patterns, 35 projects, 944 occurrences)
- [principles.md](references/principles.md) — Exploration principles for subagents
- [patterns-db.schema.json](references/patterns-db.schema.json) — JSON Schema for DB and subagent output
- [subagent-output.schema.json](references/subagent-output.schema.json) — outputSchema for structured subagent output
- [projects.md](references/projects.md) — File maps and pattern sources per project
