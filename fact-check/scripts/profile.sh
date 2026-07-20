#!/bin/bash
# profile.sh — Event logger for run observability (T10)
# Usage: bash profile.sh <run-dir> <event> [key=value ...]
# Events: phase_start, phase_end, llm_call, script, network, retry, subagent
# Appends JSON line to <run-dir>/profile.jsonl

set -euo pipefail

RUN_DIR="${1:-}"
EVENT="${2:-}"
shift 2 || true

if [ -z "$RUN_DIR" ] || [ -z "$EVENT" ]; then
  echo '{"error":"usage: profile.sh <run-dir> <event> [key=value ...]"}' >&2
  exit 1
fi

PROFILE_FILE="$RUN_DIR/profile.jsonl"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TIMESTAMP_MS=$(date +%s%3N)

# Build JSON from key=value args
python3 - "$EVENT" "$TIMESTAMP" "$TIMESTAMP_MS" "$PROFILE_FILE" "$@" << 'PYEOF'
import json, os, sys

event = sys.argv[1]
timestamp = sys.argv[2]
timestamp_ms = sys.argv[3]
profile_file = sys.argv[4]
kv_args = sys.argv[5:]

entry = {"event": event, "timestamp": timestamp, "timestamp_ms": int(timestamp_ms)}

for kv in kv_args:
    if "=" in kv:
        k, v = kv.split("=", 1)
        # Try to convert to number
        try:
            v = int(v)
        except ValueError:
            try:
                v = float(v)
            except ValueError:
                pass
        entry[k] = v

os.makedirs(os.path.dirname(profile_file) or ".", exist_ok=True)
with open(profile_file, "a") as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
PYEOF
