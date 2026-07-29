---
name: guardrail-optimizer
description: "Replay session tool calls through pi-guardrails path-access logic to reconstruct outside-cwd path accesses, analyze frequency and context, recommend allow-list entries, and update guardrail config. Use when the user says /skill:guardrail-optimizer or wants to reduce frequent guardrail allow prompts."
disable-model-invocation: true
---

# Guardrail Optimizer

**Leading word:** _allowlist_ — the set of outside-cwd paths the guardrail permits without prompting; this skill finds candidates and adds them.

## Prerequisites

- Node.js ≥ 24 (native TypeScript support via `--experimental-strip-types`)
- Session JSONL files under `~/.pi/agent/sessions/`

## Flow

### Step 1: Collect path-access data

Run the scanner to replay each tool call through pi-guardrails' path-access logic. Output can exceed 500KB; always redirect to a file.

```bash
node --experimental-strip-types <SKILL_DIR>/scripts/scan_paths.ts --sessions ~/.pi/agent/sessions --cwd <PROJECT_CWD> --limit 100 > /tmp/guardrail_scan.json
```

For `--global` mode (scans ALL projects' sessions, updates user-level config):

```bash
node --experimental-strip-types <SKILL_DIR>/scripts/scan_paths.ts --sessions ~/.pi/agent/sessions --cwd <PROJECT_CWD> --limit 100 --global > /tmp/guardrail_scan.json
```

`--global` scans all sessions across all projects (each session's outside-cwd paths are computed relative to that session's own cwd) and updates the user-level config at `~/.pi/agent/extensions/guardrails.json`.

**Completion criterion**: JSON output saved to file, contains all outside-cwd path accesses from scanned sessions.

### Step 2: Filter, consolidate, and recommend

Run the analysis script to mechanically filter noise, consolidate by parent directory, check broadness, handle version-specific paths, and scan for sensitive files:

```bash
python3 <SKILL_DIR>/scripts/analyze_paths.py /tmp/guardrail_scan.json --cap 15
```

The script outputs JSON with `recommended_entries[]` (capped at 15, sorted by frequency), `remaining_entries[]` (beyond the cap), `skipped_entries[]` (with reasons: `too_broad`, `already_allowed`), and `summary`.

Then, using the script output, perform semantic analysis **yourself**: for each recommended entry, classify the purpose (e.g., "shared skill definitions", "cross-project source", "research notes") and add a human-readable reason. This is the one step the script can't do — it requires understanding *why* the path is accessed.

**Completion criterion**: Recommendation table contains at most 15 consolidated entries, each with Path, Frequency, Tools, Reason, and security warning (if any). Paths already covered by existing allowlist entries, rejected as too broad, or beyond the cap are listed as skipped/remaining.

### Step 3: Generate report and confirm

Present the allowlist recommendations as a Markdown report: scope, config target, sessions scanned, current allowlist, recommended new paths, and skipped paths (with reasons). Ask the user to confirm before writing — let them respond freely (accept all, accept a subset by number, modify, or cancel).

**Completion criterion**: User has responded with accept (all or subset), modify, or cancel. If cancel, skill ends here.

### Step 4: Update guardrails.json

After user confirmation, update the guardrail config file:

- **Project scope** (default): `<cwd>/.pi/extensions/guardrails.json`
- **User scope** (`--global`): `~/.pi/agent/extensions/guardrails.json`

Merge new entries into the existing `pathAccess.allowedPaths` array. Preserve all other config fields. Validate the result with `python3 -m json.tool` after writing. If the file doesn't exist, create it with the `$schema` field and a minimal `pathAccess.allowedPaths` structure.

**Completion criterion**: guardrails.json is valid JSON, contains the confirmed new entries alongside existing ones, and the user is informed of the changes.
