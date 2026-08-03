# Reuse pi's exported types instead of redefining

The base layer imports `SessionEntry`, `SessionHeader`, `CompactionEntry`, `SessionInfo`, `FileEntry`, and related types directly from `@earendil-works/pi-coding-agent` rather than defining its own. The base layer's own types (`SessionMetrics`, `CrossSessionMetrics`, `ToolProfile`, `UsageBreakdown`, `TimeTrends`) are aggregate result structures — they don't mirror JSONL entities. This revises the original #19 decision to define 6 entities; the discovery that pi already exports all of them made redefinition pure duplication.

**Considered alternatives**: Redefine all types for independence from pi's package (rejected — creates maintenance burden tracking pi's type changes, and the base layer's value is aggregation, not parsing). Define a compatibility layer mapping pi types to base types (rejected — unnecessary indirection with no benefit).
