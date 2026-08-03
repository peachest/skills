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

## API Interface (from #21)

See resolution comment: https://github.com/peachest/skills/issues/21#issuecomment-5165910302

### Key decisions:
- CLI: 分域子命令 + all (sessions / tools / usage / trends / all)
- Library API: 纯函数 (scanSessions, scanChildSessions, parseSession, aggregate.*)
- Extension points: 暴露原始 FileEntry[] via parseSession(), 无 hook 机制
- Child session: opt-in (--include-children flag, scanChildSessions(parentId))
- CLI flags: --sessions, --limit, --project, --include-children; trends: --bucket, --days
- Output: JSON to stdout (consistent with pi-insight / guardrail-optimizer)

## Prototype Stub (from #22)

See resolution comment: https://github.com/peachest/skills/issues/22#issuecomment-5166339357
Prototype branch: `session-profile-prototype-22` (throwaway, not merged to main)

### Key findings:
- API design from #21 is viable — all 5 subcommands + library import patterns work
- 7 pain points discovered (cwd not in entries, ESM require, package import, etc.)
- Recommendations for real impl: package.json, zod schemas, child session index, diff parsing

## Consumer-Driven Revision (from #26)

See resolution comment: https://github.com/peachest/skills/issues/26#issuecomment-5166799909
ADR: docs/adr/0003-enriched-scan-result.md

### Key decisions:
- scanSessions() returns SessionScanResult[] (metrics + toolCalls + subagentSpawns), not SessionMetrics[]
- ToolCallRecord: lightweight per-tool-call projection (name + arguments + error + timestamp)
- SubagentSpawnRecord: parsed from toolCall + toolResult pair (runId, agent, mode, taskText, childSessionPaths)
- Child session linking: from toolResult text, NOT from toolCall id field
- parseSession(): supplementary, not primary extension point
- aggregate.*() takes SessionScanResult[] instead of SessionMetrics[]
- Revises #20 (metrics catalog) and #21 (API interface)
