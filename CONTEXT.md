# Glossary

## Guardrail Optimizer

- **Outside-cwd path**: An absolute path that falls outside the session's working directory (`cwd`). Pi-guardrails' path-access extension intercepts tool calls targeting such paths and prompts the user to allow or deny. Synonym: "outside-workspace path" (the term used in the guardrail TUI prompt).

- **Path access replay**: Re-running pi-guardrails' `targetsForTool` + `checkPathAccess` logic against historical tool calls recorded in session JSONL files, using empty `allowedPaths` to reconstruct which paths would have triggered a prompt. This is a *reconstruction*, not a reading of stored interception records — guardrail prompts are interactive TUI events and are not persisted to session files.

- **Path hit**: A single instance of a tool call targeting an outside-cwd path, as detected by replay. One path may accumulate many hits across sessions.

- **Noise path**: A path that triggers detection but is not a meaningful access target — e.g., `/dev/null` (bash redirect), glob patterns (`*.jsonl`), `/proc/` virtual filesystem entries. These should be filtered before semantic analysis.

- **Allowed path**: An entry in `guardrails.json` under `pathAccess.allowedPaths` that pre-authorizes agent access to a specific file or directory, bypassing the interactive prompt. Has an explicit `kind` of `file` (exact match) or `directory` (prefix match including descendants).

- **Grant granularity**: The choice between `file` and `directory` kind for a recommended allowed path. File grants are narrower (safer); directory grants are broader (more convenient, fewer future prompts).
