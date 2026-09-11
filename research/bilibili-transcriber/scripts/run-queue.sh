#!/usr/bin/env bash
# run-queue.sh — batch fetch+transcribe queue for a video manifest.
#
# Usage:
#   bash run-queue.sh <workspace-dir> <manifest.json>
#
#   workspace-dir  working dir: per-video fetch dirs + references/transcripts/
#   manifest.json  output of enumerate-uploader.py (bvid/title/duration/...)
#
# Properties:
#   - Resumable: videos with an existing transcript are skipped.
#   - Ascending duration order: short videos land first, giant compilations last.
#   - Failures are recorded in <workspace>/status.jsonl and never block the queue.
#   - stdin is never inherited by loop children (a downloader once ate bytes
#     from the redirected input and truncated every following BV id).
#
# Requires on PATH: python3 with requests+numpy (e.g. a venv bin prepended),
# aria2c, ffmpeg. Validate first with: bash check-env.sh

set -u
if [ $# -ne 2 ]; then
  echo "usage: run-queue.sh <workspace-dir> <manifest.json>" >&2
  exit 2
fi
BASE=$(realpath "$1"); MANIFEST=$(realpath "$2")
SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
FETCH="$SKILL_DIR/../fetch-article/scripts/fetch.py"
TR="$SKILL_DIR/scripts/transcribe.sh"

mkdir -p "$BASE/workspaces"
touch "$BASE/status.jsonl"
cd "$BASE"

python3 - "$MANIFEST" > "$BASE/queue-order.txt" <<'PY'
import json, sys
items = json.load(open(sys.argv[1]))
for v in sorted(items, key=lambda x: x["duration"]):
    print(v["bvid"])
PY

total=$(wc -l < "$BASE/queue-order.txt"); i=0
while read -r BV <&3; do
  i=$((i+1))
  if compgen -G "$BASE/references/transcripts/bilibili/*-$BV/transcript.md" > /dev/null; then
    echo "[$i/$total] $BV SKIP (done)"
    continue
  fi
  echo "[$i/$total] $BV fetch..."
  mkdir -p "$BASE/workspaces/$BV"
  if ! python3 "$FETCH" "https://www.bilibili.com/video/$BV/" --json \
       --output-dir "$BASE/workspaces/$BV" < /dev/null > "$BASE/workspaces/$BV.fetch.log" 2>&1; then
    echo "[$i/$total] $BV FETCH-FAILED"
    echo "{\"bvid\":\"$BV\",\"status\":\"fetch_failed\"}" >> "$BASE/status.jsonl"
    continue
  fi
  if bash "$TR" "$BASE/workspaces/$BV" < /dev/null >> "$BASE/workspaces/$BV.tr.log" 2>&1; then
    echo "{\"bvid\":\"$BV\",\"status\":\"ok\"}" >> "$BASE/status.jsonl"
    echo "[$i/$total] $BV OK"
    rm -f "$BASE/workspaces/$BV"/*.wav "$BASE/workspaces/$BV"/faster-whisper/chunks/*.wav 2>/dev/null
  else
    echo "[$i/$total] $BV TRANSCRIBE-FAILED"
    echo "{\"bvid\":\"$BV\",\"status\":\"transcribe_failed\"}" >> "$BASE/status.jsonl"
  fi
  sleep 5
done 3< "$BASE/queue-order.txt"

ok=$(grep -c '"ok"' "$BASE/status.jsonl" || true)
fail=$(grep -c 'failed' "$BASE/status.jsonl" || true)
echo "QUEUE DONE: ok=$ok failed=$fail total=$total"
