#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# transcode.sh — Extract the audio transcode step from transcribe.sh.
#
# Converts an input audio/video file to 16kHz mono WAV, ignoring any video
# stream (-vn). This is testable in isolation — it does NOT require
# WHISPER_ENDPOINT and does NOT invoke the ASR service.
#
# Usage: bash <SKILL_DIR>/scripts/transcode.sh <input-file> <output-wav>
#
# Outputs:
#   <output-wav>  — 16kHz mono s16 PCM WAV
#   stdout        — three lines: transcode_seconds, wav_size_bytes, duration_seconds
# ──────────────────────────────────────────────────────────────────────────────
set -eo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <input-file> <output-wav>"
  exit 1
fi

INPUT_FILE="$1"
WAV_PATH="$2"

if [ ! -f "$INPUT_FILE" ]; then
  echo "✗ Input file not found: $INPUT_FILE"
  exit 1
fi

T0=$(date +%s%N)
ffmpeg -y -i "$INPUT_FILE" -vn -ac 1 -ar 16000 -sample_fmt s16 "$WAV_PATH" -loglevel error
T1=$(date +%s%N)
TRANSCODE_S=$(echo "scale=3; ($T1 - $T0) / 1000000000" | bc)
WAV_SIZE=$(stat -c%s "$WAV_PATH" 2>/dev/null)

# Get duration (ffprobe preferred, ffmpeg fallback)
DURATION=""
if command -v ffprobe &>/dev/null; then
  DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$WAV_PATH" 2>/dev/null || true)
fi
if [ -z "$DURATION" ]; then
  RAW_DUR=$(ffmpeg -i "$WAV_PATH" 2>&1 | grep -oP 'Duration: \K[0-9:.]+' || true)
  DURATION=$(echo "$RAW_DUR" | awk -F: '{ print ($1*3600)+($2*60)+$3 }')
fi
DURATION=$(printf "%.1f" "$DURATION")

# Output machine-readable result for callers
echo "$TRANSCODE_S"
echo "$WAV_SIZE"
echo "$DURATION"
