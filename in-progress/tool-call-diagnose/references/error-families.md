# Error Families — detection strings & blame defaults

Classification baseline for the failure axis. Families were derived from real
session logs (2.2k sessions, ~40k error toolResults); signatures are matched
against toolResult text. Blame is the *default* — the surrounding trace can
overturn it (e.g. an ENOENT caused by an earlier harness failure).

| Family | Signature in toolResult text | Default blame |
|--------|------------------------------|---------------|
| schema-validation | `Validation failed for tool` / `must have required properties` / `unexpected additional properties` / `must be equal to one of the allowed values` / `Expected parameters` | agent-usage |
| harness-constraint | `cannot be combined with` / `is rejected` / `invalid key` / `requires` (option-conflict wording from the tool itself, not a JSON schema error) | agent-usage |
| edit-mismatch | `oldText must match exactly` / `Could not find edits[` / `must match a unique` | agent-usage |
| not-found | `ENOENT` / `No such file or directory` / `not found` | agent-usage |
| exit-code | `Command exited with code N` (bash; the tool ran, the command failed) | depends on command — inspect args; shell-level mistakes (bad path, failed pipe) are agent-usage, upstream service errors are environment |
| hook-block | `Use context-mode MCP tools` / `[pi-permission-system]` / other hook interjections that replace the command's output | agent-usage (policy the agent should comply with) — but a *wrongly-firing* hook is harness |
| network | `Network error` / `Access to private/internal IP address` / `ETIMEDOUT` / `ECONNREFUSED` / `rate limit` / `429` / `502` / `503` | environment |
| timeout | `timed out` / `Timeout` / `exceeded` (time) | environment if the agent set a sane timeout; agent-usage if it omitted one the tool offers |
| permission | `User denied tool` / permission-refusal wording | agent-usage (wrong ask), note the user's stated reason |

Unknown signatures → family `uncategorized`, blame `unknown` — list them in the
report; recurring `uncategorized` families are themselves a finding (extend
this table when diagnosing).

## Blame categories

- **agent-usage** — the agent misused the tool: wrong shape, wrong option
  combination, missing required arg, ignoring a documented rule. Fixable by
  companion skill / behavior.
- **harness** — the tool or harness itself (ambiguous schema error, hook
  misfire, tool bug). Route to the user; nothing the skill can absorb.
- **environment** — network, provider, host state. Route to the user.
- **upstream-tool** — the called command/service failed correctly-reported.
  The agent's usage was fine; the target was broken.

## Pit-documented check

For `agent-usage` failures, the companion skill cross-check has three verdicts:

- `pit-documented-not-read` — companion skill documents this pit; trace shows
  the agent never loaded the SKILL.md before failing. Route: agent-behavior.
- `pit-documented-ignored` — agent read the skill earlier and hit the pit
  anyway. Route: agent-behavior (stronger nudge), possibly skill-doc if the
  doc buries the rule too deep.
- `pit-undocumented` — companion skill exists but misses this pit. Route:
  skill-doc.
