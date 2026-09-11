# Session JSONL Primer

Format facts for reading pi session logs. The raw files live at
`~/.pi/agent/sessions/<cwd-slug>/<timestamp>_<session-id>.jsonl` and can be
several MB — never read one whole; navigate with the trace index from
`find-skill-sessions.py --index`, then read only the line ranges it points at.

## Entry structure

One JSON object per line. Relevant `type` values:

- `session` — first line: `{id, timestamp, cwd}`
- `model_change` / `thinking_level_change` — metadata, ignorable for analysis
- `message` — the conversation. Shape: `{message: {role, content[], usage?}, timestamp}`

Roles: `user` (may carry a skill injection in its text), `assistant`, `toolResult`.

Content block types inside `message.content`:

| Block | Meaning |
|-------|---------|
| `text` | visible prose (`text` field) |
| `thinking` | reasoning trace (`thinking` field) |
| `toolCall` | `{id, name, arguments}` — the tool call with its full args |
| `toolResult` | result block inside `toolResult`-role messages |

`usage` on assistant messages: `{input, output, cacheRead, cacheWrite}` —
token accounting for that one model call. Per-session totals come from summing
these (the triage stats in `find-skill-sessions.py` output already do).

## Skill injection marker

When a skill fires, the user message text contains
`<skill name="NAME" location="...">` followed by the skill body. Inside the
JSONL the quotes are backslash-escaped, so the raw-file marker is
`<skill name=\"NAME\"`. The injected body typically ends where the user's own
prompt begins (after the closing `</skill>`).

## Cost accounting

Read costs off the trace index's per-turn usage fields:

- **output** — what the model wrote that turn (prose + tool-call args). A
  duplicated large payload costs its output again every re-emission.
- **input + cacheRead** — what the model re-read. `cacheRead` is the cached
  portion; `input` is what was re-processed uncached. A turn with high `in=`
  and collapsed `cacheR` re-read the whole context at full price.
