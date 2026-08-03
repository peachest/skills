# Session Profile — Decision Record

## Data Model (from #19)

See resolution comment: https://github.com/peachest/skills/issues/19#issuecomment-5163760170

### Key decisions:
- Language: TypeScript (pi ecosystem native), zod for runtime validation
- 6 entities: Session, Message, ContentBlock (union), Usage, ModelChange, ThinkingLevelChange, CustomEvent
- Child sessions: flat parent_id + run_id + run_index fields
- Project grouping: only cwd exposed
- Parse boundary: parseSession/parseSessions only, query goes to #21

## Metrics Catalog (from #20)

See resolution comment: https://github.com/peachest/skills/issues/20#issuecomment-5165751064

### Key decisions:
- 5 aggregation categories: Session-level Meta (precomputed) + Cross-session + Tool profiles + Usage breakdown + Time trends (all lazy)
- Child session mapping (base layer unique — pi doesn't do this)
- Base layer does NOT cache — caching is consumer's responsibility
- Time trends include advanced analysis: decay weighting, week-over-week, trajectory, anomaly detection
- Compaction entity: reuse pi's CompactionEntry type (not redefine)
- Key discovery: pi already exports SessionManager + parseSessionEntries + all types — base layer reuses these
