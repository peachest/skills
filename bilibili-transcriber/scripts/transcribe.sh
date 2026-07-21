#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# transcribe.sh — Transcribe audio via a whisper-asr service.
#
# Usage: bash scripts/transcribe.sh <workspace-dir>
#
# Outputs:
#   Transcript (*cleaned* final) → references/transcripts/<source>/<date>-<title>-<id>/transcript.md
#   Raw ASR output + metrics     → <workspace-dir>/<method>/                          (intermediate)
#
# Environment variables:
#   WHISPER_ENDPOINT  — API base URL (REQUIRED, e.g. http://host:port/openai/v1)
#   WHISPER_MODEL     — model name (REQUIRED, e.g. whisper-large-v3)
#   WHISPER_LANG      — language hint (default: zh)
#   METHOD            — intermediate subdirectory (default: faster-whisper)
# ──────────────────────────────────────────────────────────────────────────────
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
AGENT_DIR="$(dirname "$SKILL_DIR")"
PROJECT_ROOT="$(dirname "$AGENT_DIR")"
TRANSCRIPT_DIR="${PROJECT_ROOT}/references/transcripts"

WHISPER_ENDPOINT="${WHISPER_ENDPOINT:?}"
WHISPER_MODEL="${WHISPER_MODEL:?}"
WHISPER_LANG="${WHISPER_LANG:-zh}"
METHOD="${METHOD:-faster-whisper}"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <workspace-dir>"
  echo "  e.g. $0 video/BV1ahVr6gERA-your-title/"
  exit 1
fi

WORK_DIR="$1"
RAW_DIR="${WORK_DIR}/raw"
OUT_DIR="${WORK_DIR}/${METHOD}"
AUDIO_MP4="${RAW_DIR}/audio.mp4"

# Validate
if [ ! -d "$WORK_DIR" ]; then
  echo "✗ Workspace not found: $WORK_DIR"
  exit 1
fi
if [ ! -f "$AUDIO_MP4" ]; then
  echo "✗ Audio file not found: $AUDIO_MP4"
  echo "  Run dl.py first to download the audio."
  exit 1
fi

# ── Parse workspace dir name for source/date/title/id ──
# We need the BV number from workspace dir (named {BV}-{title}).
# Derive it for the reference path; fallback to a unique timestamp dir.
WORK_BASENAME="$(basename "$WORK_DIR")"
# Extract leading BV-like pattern (e.g., "BV1ahVr6gERA" from "BV1ahVr6gERA-...")
BV_ID=""
if [[ "$WORK_BASENAME" =~ ^(BV[a-zA-Z0-9]+) ]]; then
  BV_ID="${BASH_REMATCH[1]}"
fi

# Read title from metadata if available
META_PATH="${WORK_DIR}/metadata.md"
TITLE_SLUG="unknown"
if [ -f "$META_PATH" ]; then
  TITLE_LINE=$(grep "^| 标题" "$META_PATH" | head -1 || true)
  if [ -n "$TITLE_LINE" ]; then
    RAW_TITLE=$(echo "$TITLE_LINE" | sed 's/.*| //; s/ |$//')
    TITLE_SLUG=$(echo "$RAW_TITLE" | sed 's/[\\/:*?"<>|]/_/g' | head -c 60)
  fi
fi

TODAY="$(date +%Y%m%d)"
# Determine source from metadata
SOURCE="bilibili"

# Build reference dir: references/transcripts/<source>/<date>-<title>-<id>/
REF_DIR="${TRANSCRIPT_DIR}/${SOURCE}/${TODAY}-${TITLE_SLUG}-${BV_ID}"
mkdir -p "$OUT_DIR" "$REF_DIR"

# ── Step 1: Transcode ──
WAV_PATH="${OUT_DIR}/audio.wav"
echo "[1/3] Transcoding MP4 → 16kHz WAV"
T0=$(date +%s%N)
ffmpeg -y -i "$AUDIO_MP4" -ac 1 -ar 16000 -sample_fmt s16 "$WAV_PATH" -loglevel error
T1=$(date +%s%N)
TRANSCODE_S=$(echo "scale=3; ($T1 - $T0) / 1000000000" | bc)
WAV_SIZE=$(stat -c%s "$WAV_PATH" 2>/dev/null)
echo "  → $((WAV_SIZE / 1048576))MB, transcode ${TRANSCODE_S}s"

# Get audio duration (ffprobe or fallback to ffmpeg parse)
DURATION=""
if command -v ffprobe &>/dev/null; then
  DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$WAV_PATH" 2>/dev/null || true)
fi
if [ -z "$DURATION" ]; then
  RAW=$(ffmpeg -i "$WAV_PATH" 2>&1 | grep -oP 'Duration: \K[0-9:.]+' || true)
  DURATION=$(echo "$RAW" | awk -F: '{ print ($1*3600)+($2*60)+$3 }')
fi
DURATION=$(printf "%.1f" "$DURATION")
echo "  duration: ${DURATION}s"

# ── Step 2: Whisper ASR ──
echo "[2/3] Transcribing via whisper-asr (${WHISPER_ENDPOINT})…"
T2=$(date +%s%N)
RESPONSE=$(curl -s --noproxy '*' \
  -X POST "${WHISPER_ENDPOINT}/audio/transcriptions" \
  -F "file=@$WAV_PATH" \
  -F "model=${WHISPER_MODEL}" \
  -F "language=${WHISPER_LANG}" \
  -F "response_format=json")
T3=$(date +%s%N)
ASR_S=$(echo "scale=3; ($T3 - $T2) / 1000000000" | bc)

# Parse response
TEXT=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('text',''))" 2>/dev/null)
STATUS=$?
if [ $STATUS -ne 0 ] || [ -z "$TEXT" ]; then
  echo "✗ ASR failed. Response:"
  echo "$RESPONSE" | head -5
  exit 1
fi

CHAR_COUNT=$(echo -n "$TEXT" | wc -c | tr -d ' ')
RTF=$(echo "scale=4; $ASR_S / $DURATION" | bc)
TOTAL_S=$(echo "scale=3; ($T3 - $T0) / 1000000000" | bc)
echo "  ASR ${ASR_S}s, total ${TOTAL_S}s, RTF ${RTF}, ${CHAR_COUNT} chars"

# ── Step 3: Save outputs ──

# 3a. Raw ASR output → workspace (intermediate)
RAW_TRANSCRIPT_PATH="${OUT_DIR}/transcript.md"
cat > "$RAW_TRANSCRIPT_PATH" << EOF
# 转录结果

| 字段 | 值 |
|------|-----|
| 方法 | ${METHOD} |
| 模型 | ${WHISPER_MODEL} |
| 端点 | ${WHISPER_ENDPOINT} |
| 音频时长 | ${DURATION}s |
| 转码耗时 | ${TRANSCODE_S}s |
| 推理耗时 | ${ASR_S}s |
| RTF | ${RTF} |
| 字符数 | ${CHAR_COUNT} |

---

${TEXT}
EOF

# Metrics → workspace
METRICS_PATH="${OUT_DIR}/metrics.md"
cat > "$METRICS_PATH" << EOF
# 性能指标

| 指标 | 值 |
|------|-----|
| 方法 | ${METHOD} |
| 模型 | ${WHISPER_MODEL} |
| 音频 | ${AUDIO_MP4} |
| 音频时长 | ${DURATION}s |
| 原始大小 | $(echo "scale=2; $(stat -c%s "$AUDIO_MP4" 2>/dev/null || echo 0) / 1048576" | bc)MB |
| WAV 大小 | $(echo "scale=2; $WAV_SIZE / 1048576" | bc)MB |
| 转码耗时 | ${TRANSCODE_S}s |
| 推理耗时 | ${ASR_S}s |
| 总耗时 | ${TOTAL_S}s |
| RTF | ${RTF} |
| 字符数 | ${CHAR_COUNT} |
EOF

# 3b. Final transcript → references (to be cleaned)
FINAL_TRANSCRIPT_PATH="${REF_DIR}/transcript.md"
cp "$RAW_TRANSCRIPT_PATH" "$FINAL_TRANSCRIPT_PATH"

echo ""
echo "[3/3] Done!"
echo "  Raw ASR        → ${RAW_TRANSCRIPT_PATH}  (intermediate, in workspace)"
echo "  Final (unclean) → ${FINAL_TRANSCRIPT_PATH}  (edit this .md next)"
echo "  Metrics        → ${METRICS_PATH}"
echo ""
echo "  ⚠ Next: clean ${FINAL_TRANSCRIPT_PATH} — add paragraph breaks, fix homophones"