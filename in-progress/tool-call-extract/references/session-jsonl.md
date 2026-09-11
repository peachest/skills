# Session JSONL Primer (tool-call focus)

Format facts for reading pi session logs. The raw files live at
`~/.pi/agent/sessions/<cwd-slug>/<timestamp>_<session-id>.jsonl` and can be
several MB — never read one whole; navigate with the calls dump and trace
index, then read only the entries they point at.

## Entry structure

One JSON object per line. Relevant `type` values:

- `session` — first line: `{id, timestamp, cwd}`
- `model_change` / `thinking_level_change` — metadata, ignorable
- `message` — the conversation. Shape: `{message: {role, content[], usage?}, timestamp}`

Roles: `user`, `assistant`, `toolResult`.

## Tool call / result shapes

An **assistant** message's content holds the call:

```json
{"type": "toolCall", "id": "call_0d0c...", "name": "bash", "arguments": {...}}
```

A separate **toolResult-role** message holds the outcome, linked by id:

```json
{"message": {"role": "toolResult", "toolCallId": "call_0d0c...",
             "toolName": "bash",
             "content": [{"type": "text", "text": "..."}],
             "isError": false, "timestamp": 1788955121397}}
```

- `isError: true` marks the failure — the only reliable failure signal.
- One assistant message may hold several `toolCall` blocks (parallel calls);
  each pairs with its own toolResult.
- A call with no matching result means the session was cut short mid-call.

Other content block types: `text` (visible prose), `thinking` (reasoning).

## Usage / cost accounting

`usage` on assistant messages: `{input, output, cacheRead, cacheWrite}` —
token accounting for that one model call. A retry loop costs one assistant
turn's `output` (re-emitted args) per attempt plus context re-reads.

## Known error families (observed in real logs)

Detection strings live in `/skill:tool-call-diagnose`'s `references/error-families.md`;
this list is only the orientation: schema validation failures, harness
constraint conflicts (e.g. combining incompatible subagent options), shell
exit codes, hook interception blocks, ENOENT, network errors.
