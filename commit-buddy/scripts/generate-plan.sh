#!/usr/bin/env bash
set -euo pipefail

# generate-plan.sh - 接收简化方案 JSON，自动补全 snapshot，输出完整 CommitPlan
# Usage: generate-plan.sh <input.json>
# 输出: <PROJECT_DIR>/.pi/commit-buddy/plan.json

if [ $# -ne 1 ]; then
  echo "Usage: generate-plan.sh <input.json>" >&2
  exit 1
fi

INPUT_FILE="$1"
[ -f "$INPUT_FILE" ] || { echo "ERROR: file not found: $INPUT_FILE" >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$(cd "$(dirname "$INPUT_FILE")" && pwd)"
OUTPUT_FILE="$OUTPUT_DIR/plan.json"

# source 共享的 extract_hunks
source "$SCRIPT_DIR/common.sh"

TMPDIR=$(mktemp -d /tmp/commit-buddy-gen-XXXXXXXXXX)
trap 'rm -rf "$TMPDIR"' EXIT

HEAD_SHA=$(git rev-parse HEAD)

# 提取所有文件 hunk
ALL_PATHS=$(jq -r '[.commits[].files[].path] | unique | .[]' "$INPUT_FILE")

HUNK_COUNTS=""
for path in $ALL_PATHS; do
  extract_hunks "$path" "$TMPDIR" count
  safename="${path//\//_}"
  echo "$safename:$count" >> "$TMPDIR/counts"
done

# 构建 snapshot
SNAPSHOT_JSON='[]'
for path in $ALL_PATHS; do
  safename="${path//\//_}"
  count=$(grep "^$safename:" "$TMPDIR/counts" 2>/dev/null | cut -d: -f2 || echo 0)

  if [ "$count" -eq 0 ]; then
    SNAPSHOT_JSON=$(echo "$SNAPSHOT_JSON" | jq --arg p "$path" --arg s "$HEAD_SHA" \
      '. + [{path: $p, head_sha: $s, hunks: []}]')
  else
    HUNKS_JSON='[]'
    for ((i=0; i<count; i++)); do
      patch_file="$TMPDIR/hunks/$safename/$i.patch"
      if [ -f "$patch_file" ]; then
        fp=$(compute_hunk_fingerprint "$patch_file")
        HUNKS_JSON=$(echo "$HUNKS_JSON" | jq --argjson idx "$i" --arg fp "$fp" \
          '. + [{index: $idx, fingerprint_sha256: $fp}]')
      fi
    done
    SNAPSHOT_JSON=$(echo "$SNAPSHOT_JSON" | jq --arg p "$path" --arg s "$HEAD_SHA" --argjson h "$HUNKS_JSON" \
      '. + [{path: $p, head_sha: $s, hunks: $h}]')
  fi
done

CREATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

jq -n \
  --argjson commits "$(jq '.commits' "$INPUT_FILE")" \
  --argjson snapshot "$SNAPSHOT_JSON" \
  --arg created_at "$CREATED_AT" \
  '{
    version: 1,
    commits: $commits,
    snapshot: {
      files: $snapshot,
      created_at: $created_at,
      source: "commit-buddy"
    }
  }' > "$OUTPUT_FILE"

echo "Generated: $OUTPUT_FILE"