# Enrich scanSessions() return value with tool call records and spawn records

`scanSessions()` returns a composite `SessionScanResult` — session metrics + tool call records + subagent spawn records — rather than just `SessionMetrics[]`. This was driven by consumer analysis: 2 of 3 known consumers (guardrail-optimizer, subagent profiler) need tool call arguments, which `SessionMetrics` discards after counting. Without enriched return values, these consumers must call `parseSession()` to re-parse each session file, causing triple parsing (scan + aggregate + consumer) and making `parseSession()` the de-facto primary API instead of `scanSessions()`.

The trade-off: a richer return type means more memory per session (tool call records for 1000+ sessions), but eliminates redundant parsing. Consumers who truly need only metrics (pi-insight) can ignore the extra fields. `parseSession()` remains as a supplementary escape hatch for non-tool entry types, not the primary extension point.

This also fixes child session linking: spawn records are parsed from toolCall + toolResult pairs (the actual data source), not from the `id` field in toolCall arguments (which only exists on management calls, not spawn calls).
