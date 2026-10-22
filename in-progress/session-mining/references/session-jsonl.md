# Session JSONL Primer

Format facts for reading pi session logs. Raw files live at
`~/.pi/agent/sessions/<cwd-slug>/<timestamp>_<session-id>.jsonl`, several MB
each — never read one whole; navigate with the trace index or calls dump, then
read only the line ranges they point at.

## Entry structure

One JSON object per line. Relevant `type` values:

- `session` — first line: `{id, timestamp, cwd}`
- `model_change` / `thinking_level_change` — metadata, ignorable for analysis
- `message` — the conversation: `{message: {role, content[], usage?}, timestamp}`

Roles: `user` (may carry a skill injection), `assistant`, `toolResult`.

Content block types inside `message.content`:

| Block | Meaning |
|-------|---------|
| `text` | visible prose (`text` field) |
| `thinking` | reasoning trace (`thinking` field) |
| `toolCall` | `{id, name, arguments}` — the call with full args |
| `toolResult` | result block inside `toolResult`-role messages |

## Tool call / result pairing

Assistant content holds the call; a separate `toolResult`-role message holds
the outcome, linked by id:

```json
{"message": {"role": "toolResult", "toolCallId": "call_0d0c...",
             "toolName": "bash", "content": [{"type": "text", "text": "..."}],
             "isError": false, "timestamp": 1788955121397}}
```

- `isError: true` is the reliable failure signal — but it lives on the
  **message**, not the content block, and `isError: false` still hides runtime
  errors (reserved-label / UI-unavailable escapes observed); sample it.
- One assistant message may hold several parallel `toolCall` blocks, each
  pairing with its own result. A call with no result = session cut mid-call
  (not an error).
- Probe one real record before writing any parser — zero-row parsers shipped
  twice by guessing this shape.

## Skill injection marker

When a skill fires, the user message text contains
`<skill name="NAME" location="...">` followed by the body. In the raw JSONL
quotes are backslash-escaped: the marker is `<skill name=\"NAME\"`. Never match
the string `skill:<name>` — it appears inside other skills' injected bodies and
false-positives by the dozen. Negative finding worth remembering: compaction is
**not** a dedicated event type (hunt `tokensBefore` / `before_compact` strings).

## Session file organization

- Bucket = startup cwd slug (`--mnt-disk1-hyx-<path>--`), including wt branch
  paths — a removed worktree is still findable by slug.
- `wt switch` migrates the session to a new bucket's new file; the old file
  stays. Migration verdict: command timestamp vs new filename timestamp.
- First line carries **`parentSession`** (absolute path) — walk the chain to
  trace cross-bucket lineage.
- Resume forks cwd sources: tool-visible cwd (startup) vs bash pwd (actual);
  resumed sessions also carry a stale tools snapshot.
- Forks live in `forks/`; subagent runs in `<parent>/<runId>/run-0/session.jsonl`;
  subagent transcripts in `subagent-artifacts/` — transcripts are NOT session-
  indexed (mining them is a recipes job).
- Location fallback: `find ~/.pi/agent/sessions -name "*<id>*"` — guessing the
  bucket fails more often than it works.

## Cost accounting

`usage` on assistant messages: `{input, output, cacheRead, cacheWrite}`.

- **output** — what the model wrote that turn (prose + tool-call args); a
  re-emitted payload pays again per retry.
- **input + cacheRead** — what the model re-read; high `input` with collapsed
  `cacheRead` = full-price context re-read.

Known error families (detection strings in tool-call-diagnose's
`references/error-families.md`): schema validation, harness constraint
conflicts, shell exit codes, hook interception, ENOENT, network.
