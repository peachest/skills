# Session Profile — Decision Record

## Data Model (from #19)

See resolution comment: https://github.com/peachest/skills/issues/19#issuecomment-5163760170

### Key decisions:
- Language: TypeScript (pi ecosystem native), zod for runtime validation
- 6 entities: Session, Message, ContentBlock (union), Usage, ModelChange, ThinkingLevelChange, CustomEvent
- Child sessions: flat parent_id + run_id + run_index fields
- Project grouping: only cwd exposed
- Parse boundary: parseSession/parseSessions only, query goes to #21
