---
name: guardrail-optimizer
description: "Find paths and commands that trigger guardrail prompts, recommend allowlist entries, and update guardrail config."
disable-model-invocation: true
---

# Guardrail Optimizer

**Leading word:** _allowlist_ — the set of outside-cwd paths AND dangerous-command patterns the guardrail permits without prompting; this skill finds candidates and adds them.

## Prerequisites

- Node.js ≥ 24 (native TypeScript support via `--experimental-strip-types`)
- Python3 available (helper scripts are stdlib-only)
- Session JSONL files under `~/.pi/agent/sessions/`

## Flow

The skill analyzes two independent dimensions of guardrail friction:

1. **Path access** — outside-cwd paths that trigger `pathAccess` prompts
2. **Command execution** — bash commands that trigger `permissionGate` prompts

Both scanners share the same `--sessions`, `--cwd`, `--limit`, and `--global` flags. Run them in parallel for efficiency.

### Step 1: Collect scan data

Run **both** scanners. Output can exceed 500KB; always redirect to files.

**Path-access scanner** (replays each tool call through pi-guardrails' path-access logic):

```bash
node --experimental-strip-types <SKILL_DIR>/scripts/scan_paths.ts --sessions ~/.pi/agent/sessions --cwd <PROJECT_CWD> --limit 100 > /tmp/guardrail_scan.json
```

**Command-execution scanner** (replays bash commands through pi-guardrails' dangerous-command matchers):

```bash
node --experimental-strip-types <SKILL_DIR>/scripts/scan_commands.ts --sessions ~/.pi/agent/sessions --cwd <PROJECT_CWD> --limit 100 > /tmp/guardrail_cmd_scan.json
```

For `--global` mode (scans ALL projects' sessions, updates user-level config), add `--global` to both commands. `--global` scans all sessions across all projects (each session's outside-cwd paths are computed relative to that session's own cwd) and updates the user-level config at `~/.pi/agent/extensions/guardrails.json`.

**Completion criterion**: Both JSON output files exist and are non-empty. The path scan contains `outside_paths[]`; the command scan contains `dangerous_commands[]`. If either scan returns an empty array, that dimension has no candidates — skip the corresponding analysis step and note it in the report.

### Step 2: Analyze paths

Run the path analysis script to mechanically filter noise, consolidate by parent directory, check broadness, handle version-specific paths, and scan for sensitive files:

```bash
python3 <SKILL_DIR>/scripts/analyze_paths.py /tmp/guardrail_scan.json --cap 15
```

The script outputs JSON with `recommended_entries[]` (capped at 15, sorted by frequency), `remaining_entries[]` (beyond the cap), `skipped_entries[]` (with reasons: `too_broad`, `already_allowed`), and `summary`.

Then, using the script output, perform semantic analysis **yourself**: for each recommended entry, classify the purpose (e.g., "shared skill definitions", "cross-project source", "research notes") and add a human-readable reason. This is the one step the script can't do — it requires understanding *why* the path is accessed.

**Completion criterion**: Path recommendation table contains at most 15 consolidated entries, each with Path, Frequency, Tools, Reason, and security warning (if any). Skipped/remaining paths listed with reasons.

### Step 3: Analyze commands

Run the command analysis script to group dangerous commands by family, generate candidate patterns, and filter out inherently dangerous commands:

```bash
python3 <SKILL_DIR>/scripts/analyze_commands.py /tmp/guardrail_cmd_scan.json --cap 15
```

The script outputs JSON with `recommended_entries[]`, `remaining_entries[]`, `skipped_entries[]` (reasons: `inherently_dangerous`, `too_broad`, `already_allowed`), and `summary`.

Then, using the script output, perform semantic analysis **yourself**:

1. **Refine patterns**: The script generates candidate patterns (substring or simple regex). For `sudo`/`doas`/`pkexec` commands, craft a **constrained regex** that only allows safe subcommands — never use a bare substring like `"sudo nerdctl "` which would also allow `sudo nerdctl run --privileged`. Anchor with `^` and enumerate allowed subcommands.
2. **Assess safety**: For each recommendation, determine if the command family is truly safe to auto-allow. Even read-looking commands can have side effects (e.g., `sudo nerdctl restart`).
3. **Add descriptions**: Every `allowedPatterns` entry should have a human-readable `description` explaining what it allows and why it's safe.

**Safety rules**:
- Commands in `skipped_entries` with reason `inherently_dangerous` stay skipped — do not override the script's filtering.
- For `sudo`/`doas`/`pkexec` commands, always generate a **regex** pattern (not substring) that constrains the allowed subcommands.
- Only allow `sudo`/`doas`/`pkexec` patterns that constrain subcommands to a known-safe list; shell escapes (`sudo bash`, `sudo sh`, `sudo su`, `sudo python`) must never appear in that list.

**Completion criterion**: Command recommendation table contains at most 15 entries, each with Pattern, Regex flag, Description, Frequency, and security warning (if any). Inherently dangerous, too-broad, and already-allowed commands listed as skipped.

### Step 4: Generate report and confirm

Present **both** path and command recommendations as a Markdown report:

- Scope, config target, sessions scanned
- **Path access section**: current allowlist, recommended new paths, skipped paths (with reasons)
- **Command execution section**: current allowedPatterns, recommended new patterns, skipped commands (with reasons)
- Summary: total prompts that would be eliminated

Ask the user to confirm before writing — let them respond freely (accept all, accept a subset by number, modify, or cancel). The user can accept path and command recommendations independently.

**Completion criterion**: User has responded with accept (all or subset, for paths and/or commands), modify, or cancel. If cancel, skill ends here.

### Step 5: Update guardrails.json

After user confirmation, update the guardrail config file:

- **Project scope** (default): `<cwd>/.pi/extensions/guardrails.json`
- **User scope** (`--global`): `~/.pi/agent/extensions/guardrails.json`

**Path entries**: Merge new entries into the existing `pathAccess.allowedPaths` array.

**Command entries**: Merge new entries into the existing `permissionGate.allowedPatterns` array. Each entry should have `pattern`, `regex` (bool), and `description` fields.

Preserve all other config fields. Validate the result with `python3 -m json.tool` after writing. If the file doesn't exist, create it with the `$schema` field and minimal `pathAccess.allowedPaths` and `permissionGate.allowedPatterns` structures.

**Completion criterion**: guardrails.json is valid JSON, contains the confirmed new entries (paths and/or patterns) alongside existing ones, and the user is informed of the changes.
