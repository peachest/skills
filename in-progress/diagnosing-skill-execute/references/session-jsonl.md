# Session JSONL Primer

Format facts every axis analyst needs. The raw files live at
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
token accounting for that one model call.

## Skill injection marker

When a skill fires, the user message text contains
`<skill name="NAME" location="...">` followed by the skill body. Inside the
JSONL the quotes are backslash-escaped, so the raw-file marker is
`<skill name=\"NAME\"`. The injected body typically ends where the user's own
prompt begins (after the closing `</skill>`).

## Waste signals (what to look for, with entry indices)

1. **Re-emission** — the same large payload written into tool-call arguments
   across multiple turns (e.g. a full claim set, file content, plan). Detect:
   repeated `CALL ... argLen=<large>` entries with near-identical sizes, or the
   same distinct tokens (IDs, keys) recurring in args. Cost = sum of the
   duplicate rounds' `output` tokens.
2. **Prefix-cache collapse** — `cacheR` on an assistant message drops sharply
   vs the previous one (e.g. 60K → 27K) while `in=` spikes: the whole context
   was re-read uncached. Big `in=` with low `cacheR` on adjacent turns marks
   the re-read; the entry that grew the context usually sits just before it.
3. **Tool failure loops** — same tool called repeatedly with similar args;
   results containing error/exception text. Count rounds until first success.
4. **Verbose error echo** — one tool result re-stating the same error per item
   (e.g. 30 identical validation failures). Cost = result bytes re-read every
   subsequent turn.
5. **Wall-clock stalls** — large gaps between adjacent entry timestamps with
   no tool call in between (model thinking / retry) or one tool call taking
   minutes.

## Cost accounting

Per-session totals come from summing `usage` across assistant messages
(`find-skill-sessions.py` reports them). Waste estimates should name their
arithmetic: "turns [31] and [37] each emitted the 30-claim set; output 3668 +
2347 tokens, the second round was pure waste" is a good finding; "a lot of
tokens were wasted" is not.
