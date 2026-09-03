#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# transcribe.sh — Transcribe audio via a whisper-asr service.
#
# Usage: bash <SKILL_DIR>/scripts/transcribe.sh <workspace-dir>
#
# Features:
#   - Loads ASR config from <SKILL_DIR>/runtime.conf (falls back to env vars)
#   - Auto-chunks large WAV files at silence boundaries (no overlap needed)
#   - Parallel chunk transcription (falls back to serial)
#   - verbose_json output with confidence metadata (avg_logprob, compression_ratio)
#
# Outputs:
#   Transcript (uncleaned final) → references/transcripts/<source>/<date>-<title>-<id>/transcript.md
#   Raw ASR output + metrics     → <workspace-dir>/<method>/  (intermediate)
#
# Environment variables (override runtime.conf):
#   WHISPER_ENDPOINT  — API base URL (e.g. http://host:30567/v1)
#   WHISPER_MODEL     — model ID (e.g. atom)
#   WHISPER_LANG      — language hint (default: zh)
#   METHOD            — intermediate subdirectory (default: faster-whisper)
#   CHUNK_SEC         — target chunk duration in seconds (default: 600)
#   SILENCE_DB        — silence detection threshold in dB (default: -30)
#   SILENCE_MIN_DUR   — min silence duration for detection in seconds (default: 0.5)
#   TOLERANCE         — search window for silence boundary (default: 60)
#   STRATEGY          — chunking strategy: dp|greedy|weighted|threshold (default: dp)
#   MIN_SILENCE_SCORE — min silence duration for threshold strategy (default: 1.5)
#   MAX_FILESIZE_MB   — WAV size threshold for chunking in MB (default: 25)
#   PARALLEL          — max parallel transcription requests (default: 4)
# ──────────────────────────────────────────────────────────────────────────────
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# References go to the project root (CWD), not the skill directory
PROJECT_ROOT="$(pwd)"
TRANSCRIPT_DIR="${PROJECT_ROOT}/references/transcripts"

# ── Load runtime.conf if it exists ──
RUNTIME_CONF="${SKILL_DIR}/runtime.conf"
if [ -f "$RUNTIME_CONF" ]; then
  # shellcheck source=/dev/null
  source "$RUNTIME_CONF"
fi

WHISPER_ENDPOINT="${WHISPER_ENDPOINT:?WHISPER_ENDPOINT not set. Configure in runtime.conf or set as env var.}"
WHISPER_MODEL="${WHISPER_MODEL:?WHISPER_MODEL not set. Configure in runtime.conf or set as env var.}"
WHISPER_LANG="${WHISPER_LANG:-zh}"
METHOD="${METHOD:-faster-whisper}"
CHUNK_SEC="${CHUNK_SEC:-600}"
SILENCE_DB="${SILENCE_DB:--30}"
SILENCE_MIN_DUR="${SILENCE_MIN_DUR:-0.5}"
TOLERANCE="${TOLERANCE:-60}"
STRATEGY="${STRATEGY:-dp}"
MIN_SILENCE_SCORE="${MIN_SILENCE_SCORE:-1.5}"
MAX_FILESIZE_MB="${MAX_FILESIZE_MB:-25}"
PARALLEL="${PARALLEL:-4}"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <workspace-dir>"
  echo "  e.g. $0 /tmp/fetch-article-xxx/"
  exit 1
fi

WORK_DIR="$1"
OUT_DIR="${WORK_DIR}/${METHOD}"

# ── Locate audio file ──
AUDIO_MP4="${WORK_DIR}/audio.mp4"

if [ ! -d "$WORK_DIR" ]; then
  echo "✗ Workspace not found: $WORK_DIR"
  exit 1
fi
if [ ! -f "$AUDIO_MP4" ]; then
  echo "✗ Audio file not found: $WORK_DIR/audio.mp4"
  echo "  Run fetch-article first to download the audio."
  exit 1
fi

# ── Determine title and BV id for reference path ──
TITLE_SLUG="unknown"
META_JSON="${WORK_DIR}/metadata.json"
META_MD="${WORK_DIR}/metadata.md"
if [ -f "$META_JSON" ]; then
  RAW_TITLE=$(python3 -c "import json; print(json.load(open('$META_JSON')).get('title',''))" 2>/dev/null || true)
  if [ -n "$RAW_TITLE" ]; then
    TITLE_SLUG=$(printf '%s' "$RAW_TITLE" | python3 "${SCRIPT_DIR}/slugify.py" 2>/dev/null || true)
  fi
elif [ -f "$META_MD" ]; then
  TITLE_LINE=$(grep "^| 标题" "$META_MD" | head -1 || true)
  if [ -n "$TITLE_LINE" ]; then
    RAW_TITLE=$(echo "$TITLE_LINE" | sed 's/.*| //; s/ |$//')
    TITLE_SLUG=$(printf '%s' "$RAW_TITLE" | python3 "${SCRIPT_DIR}/slugify.py" 2>/dev/null || true)
  fi
fi

BV_ID=""
if [ -f "$META_JSON" ]; then
  BV_ID=$(python3 -c "import json; print(json.load(open('$META_JSON')).get('bvid',''))" 2>/dev/null || true)
fi
if [ -z "$BV_ID" ]; then
  WORK_BASENAME="$(basename "$WORK_DIR")"
  if [[ "$WORK_BASENAME" =~ ^(BV[a-zA-Z0-9]+) ]]; then
    BV_ID="${BASH_REMATCH[1]}"
  fi
fi

TODAY="$(date +%Y%m%d)"
SOURCE="bilibili"
REF_DIR="${TRANSCRIPT_DIR}/${SOURCE}/${TODAY}-${TITLE_SLUG}-${BV_ID}"
mkdir -p "$OUT_DIR" "$REF_DIR"

# ── Step 1: Transcode ──
WAV_PATH="${OUT_DIR}/audio.wav"
echo "[1/3] Transcoding MP4 → 16kHz WAV"
T0=$(date +%s%N)
# Delegate to transcode.sh (includes -vn to ignore video streams)
TRANSCODE_OUT=$(bash "${SCRIPT_DIR}/transcode.sh" "$AUDIO_MP4" "$WAV_PATH")
TRANSCODE_S=$(echo "$TRANSCODE_OUT" | sed -n '1p')
WAV_SIZE=$(echo "$TRANSCODE_OUT" | sed -n '2p')
DURATION=$(echo "$TRANSCODE_OUT" | sed -n '3p')
WAV_SIZE_MB=$(echo "scale=1; $WAV_SIZE / 1048576" | bc)
echo "  → ${WAV_SIZE_MB}MB, transcode ${TRANSCODE_S}s"
echo "  duration: ${DURATION}s"

# ── Step 2: Transcribe (direct or silence-aware chunked) ──
echo "[2/3] Transcribing via whisper-asr (${WHISPER_ENDPOINT}, model=${WHISPER_MODEL})…"

T2=$(date +%s%N)

NEEDS_CHUNK=0
# compare raw BYTES, not the scale=1 display value: 25.0199MB truncates to
# 25.0, passes the "≤ 25" check, and the server rejects the upload at 25.0199
if [ "$(echo "$WAV_SIZE > $MAX_FILESIZE_MB * 1048576" | bc)" -eq 1 ]; then
  NEEDS_CHUNK=1
fi

RAW_TEXT_PATH="${OUT_DIR}/transcript_raw.txt"

if [ "$NEEDS_CHUNK" -eq 1 ]; then
  echo "  WAV ${WAV_SIZE_MB}MB > ${MAX_FILESIZE_MB}MB → silence-aware chunking"
  echo "  chunk=${CHUNK_SEC}s, silence_db=${SILENCE_DB}, tolerance=${TOLERANCE}s, parallel=${PARALLEL}"

  CHUNK_DIR="${OUT_DIR}/chunks"
  python3 "${SCRIPT_DIR}/chunk_transcribe.py" \
    --wav "$WAV_PATH" \
    --endpoint "$WHISPER_ENDPOINT" \
    --model "$WHISPER_MODEL" \
    --lang "$WHISPER_LANG" \
    --chunk-sec "$CHUNK_SEC" \
    --silence-db "$SILENCE_DB" \
    --silence-min-dur "$SILENCE_MIN_DUR" \
    --tolerance "$TOLERANCE" \
    --strategy "$STRATEGY" \
    --min-silence-score "$MIN_SILENCE_SCORE" \
    --max-filesize-mb "$MAX_FILESIZE_MB" \
    --parallel "$PARALLEL" \
    --output "$RAW_TEXT_PATH" \
    --chunk-dir "$CHUNK_DIR"

  if [ ! -f "$RAW_TEXT_PATH" ] || [ ! -s "$RAW_TEXT_PATH" ]; then
    echo "  Chunked transcription produced no output, falling back to direct"
    NEEDS_CHUNK=0
  fi
fi

if [ "$NEEDS_CHUNK" -eq 0 ]; then
  echo "  Direct transcription (WAV ${WAV_SIZE_MB}MB ≤ ${MAX_FILESIZE_MB}MB)"
  RESPONSE=$(curl -s --noproxy '*' \
    -X POST "${WHISPER_ENDPOINT}/audio/transcriptions" \
    -F "file=@$WAV_PATH" \
    -F "model=${WHISPER_MODEL}" \
    -F "language=${WHISPER_LANG}" \
    -F "response_format=verbose_json")

  TEXT=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('text',''))" 2>/dev/null)
  if [ -z "$TEXT" ]; then
    echo "✗ ASR failed. Response:"
    echo "$RESPONSE" | head -5
    exit 1
  fi
  echo "$TEXT" > "$RAW_TEXT_PATH"
fi

T3=$(date +%s%N)
ASR_S=$(echo "scale=3; ($T3 - $T2) / 1000000000" | bc)

TEXT=$(cat "$RAW_TEXT_PATH")
CHAR_COUNT=$(echo -n "$TEXT" | wc -c | tr -d ' ')
RTF=$(echo "scale=4; $ASR_S / $DURATION" | bc)
TOTAL_S=$(echo "scale=3; ($T3 - $T0) / 1000000000" | bc)
CHUNK_INFO=$([ "$NEEDS_CHUNK" -eq 1 ] && echo "silence-aware" || echo "direct")

echo "  ASR ${ASR_S}s, total ${TOTAL_S}s, RTF ${RTF}, ${CHAR_COUNT} chars, mode=${CHUNK_INFO}"

# ── Step 3: Save outputs ──

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
| 转录模式 | ${CHUNK_INFO} |

---

${TEXT}
EOF

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
| WAV 大小 | ${WAV_SIZE_MB}MB |
| 转码耗时 | ${TRANSCODE_S}s |
| 推理耗时 | ${ASR_S}s |
| 总耗时 | ${TOTAL_S}s |
| RTF | ${RTF} |
| 字符数 | ${CHAR_COUNT} |
| 转录模式 | ${CHUNK_INFO} |
| 分片策略 | ${STRATEGY} |
| 分片大小 | ${CHUNK_SEC}s |
| 静音阈值 | ${SILENCE_DB}dB |
| 并行度 | ${PARALLEL} |
EOF

FINAL_TRANSCRIPT_PATH="${REF_DIR}/transcript.md"
cp "$RAW_TRANSCRIPT_PATH" "$FINAL_TRANSCRIPT_PATH"

echo ""
echo "[3/3] Done!"
echo "  Raw ASR        → ${RAW_TRANSCRIPT_PATH}  (intermediate, in workspace)"
echo "  Final (unclean) → ${FINAL_TRANSCRIPT_PATH}  (edit this .md next)"
echo "  Metrics        → ${METRICS_PATH}"
echo ""
echo "  ⚠ Next: clean ${FINAL_TRANSCRIPT_PATH} — add paragraph breaks, fix homophones"
