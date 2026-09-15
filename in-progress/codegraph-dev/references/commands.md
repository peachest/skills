# codegraph command surface

Version observed: 1.6.0 (`@colbymchenry/codegraph`, npm). Verify with `codegraph --version`; behavior below matches that release.

## Lifecycle

| Command | Purpose | Notes |
|---|---|---|
| `codegraph init [path]` | build initial index | `-y` for non-interactive; creates `.codegraph/` in the project |
| `codegraph index [path]` | full rebuild | same result as fresh init |
| `codegraph sync [path]` | incremental sync since last index | `-q` suppresses output — the flag exists for git hooks |
| `codegraph status [path]` | index stats | `-j` JSON (files, nodes, edges, freshness) |
| `codegraph uninit [path]` | remove `.codegraph/` | |
| `codegraph unlock [path]` | clear stale index lock | when a crashed daemon blocks indexing |

### Git hook freshness

```bash
# .git/hooks/post-commit (and post-checkout if you switch branches often)
exec git rev-parse --show-toplevel >/dev/null 2>&1 && \
  (cd "$(git rev-parse --show-toplevel)" && codegraph sync -q)
```

Stale-index symptom: `affected`/`impact` results that don't mention files you just changed. Run `codegraph status -j`, then `sync` (or `index` for a rebuild).

## Queries

| Command | Answers | Key options |
|---|---|---|
| `codegraph query <search>` | where is this symbol | `-k <kind>` filter (function/class/method/type/interface/route/component), `-l <n>`, `-j` |
| `codegraph explore <query...>` | an area: relevant symbols' source + call paths in one shot | `--max-files <n>` (default 12) |
| `codegraph context <task...>` | task → relevant symbols + relationships + code blocks | `--no-code` for structure only, `-n <n>` max nodes, `-f json` |
| `codegraph node [name]` | one symbol: source + caller/callee trail; or file mode | `-f <file>` file mode with `--offset/--limit`, `--symbols-only` |
| `codegraph files` | project structure from the index | `--format tree|flat|grouped`, `--filter <dir>`, `--pattern <glob>`, `--max-depth`, `--no-metadata` |
| `codegraph callers <symbol>` | who calls this | `-l <n>` (default 20) |
| `codegraph callees <symbol>` | what this calls | `-l <n>` |
| `codegraph impact <symbol>` | blast radius of changing this | `-d <depth>` (default 2; use 3 for config/struct changes) |
| `codegraph affected [files...]` | changed source files → test files affected | `--stdin` (one path per line), `-d <depth>` (default 5), `-f <glob>` custom test filter, `-q` paths only |

All query commands take `-p <path>` to address another indexed project without cd-ing.

## MCP tools ↔ CLI

The pi `codegraph_*` tools are the same engines: `codegraph_search`≈query, `codegraph_explore`≈explore, `codegraph_node`≈node, `codegraph_files`≈files, `codegraph_callers`/`codegraph_callees`≈callers/callees, `codegraph_impact`≈impact. MCP tools add `projectPath` for cross-project addressing; CLI is better inside pipes and git hooks.

`codegraph install` wires the MCP server into other agents (Claude Code, Cursor, Codex CLI, ...). pi already has the tools — only needed for other tools.
