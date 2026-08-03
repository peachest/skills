# No caching in the base layer

The base layer does not cache parsed sessions or computed aggregates. `scanSessions()` re-parses every call; `aggregate.*()` recomputes every call. Caching is the consumer's responsibility. This diverges from all 6 existing third-party insight extensions (observal, supi, diwu, etc.), which implement dual-layer caching (Meta permanent + Facet refreshable).

The base layer is a library, not an extension. Extensions have a natural lifecycle (command invocation → compute → display → discard) where caching across invocations is valuable. A library's caching policy depends on the consumer's context — a CLI one-shot doesn't need it; a long-running TUI dashboard does. Forcing a caching policy on all consumers would be wrong for half of them. The pure-function API (`scanSessions()` → `SessionMetrics[]`, then `aggregate.*()`) makes it trivial for consumers to add their own cache: store the `SessionMetrics[]`, reuse it across `aggregate.*()` calls.
