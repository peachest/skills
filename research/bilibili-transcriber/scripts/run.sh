#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# run.sh — one-shot pipeline entry: fetch → ASR transcribe → slides → merge.
#
# Usage:
#   bash run.sh <bilibili-url> [outdir] [--no-slides] [--no-merge]
#
#   outdir defaults to ~/tmp/run-bilibili-<timestamp>/. All python stages run
#   through `uv run --project <SKILL_DIR>` (the .venv is auto-created via
#   `uv sync` if missing) — never call the stage scripts with bare python3.
#
# Exit codes (also written into <outdir>/.done for subscription hooks):
#   0  all stages succeeded
#   2  transcript succeeded, slides/merge failed (partial)
#   3  fetch or transcribe failed (nothing usable produced)
# ──────────────────────────────────────────────────────────────────────────────
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

URL=""; OUTDIR=""; NO_SLIDES=0; NO_MERGE=0
for arg in "$@"; do
  case "$arg" in
    --no-slides) NO_SLIDES=1 ;;
    --no-merge)  NO_MERGE=1 ;;
    *) if [ -z "$URL" ]; then URL="$arg"; elif [ -z "$OUTDIR" ]; then OUTDIR="$arg"; fi ;;
  esac
done
[ -n "$URL" ] || { echo "usage: $0 <bilibili-url> [outdir] [--no-slides] [--no-merge]" >&2; exit 3; }

# Workspace is bvid-addressed when the URL carries a BV id, so two sessions
# (or reruns) of the same video share one workspace: fetch reuses cached audio
# (cid-validated inside bilibili.py), and stages 2/3 skip when their products
# already exist. Non-BV URLs (b23.tv short links) fall back to a timestamp dir
# — no cache, resolved fresh each run.
BV_ARG=$(printf '%s' "$URL" | grep -oE 'BV[a-zA-Z0-9]+' | head -1)
OUTDIR="${OUTDIR:-$HOME/tmp/run-bilibili-${BV_ARG:-$(date +%Y%m%d-%H%M%S)}}"
mkdir -p "$OUTDIR"
DONE_MARK="$OUTDIR/.done"
finalize() { echo "$1" > "$DONE_MARK"; exit "$1"; }

cd "$OUTDIR" || finalize 3

# ── venv bootstrap (once, locked invocation for every python stage) ──
if [ ! -x "$SKILL_DIR/.venv/bin/python" ]; then
  echo "[env] .venv missing — uv sync"
  (cd "$SKILL_DIR" && uv sync) || finalize 3
fi
PY() { uv run --project "$SKILL_DIR" python "$@"; }
FETCH_PY="$SKILL_DIR/../fetch-article/scripts/fetch.py"

# ── Stage 1: fetch ──
echo "[1/4] fetch: $URL"
FETCH_JSON=$(PY "$FETCH_PY" "$URL" --json --output-dir "$OUTDIR") || { echo "✗ fetch failed"; finalize 3; }
# fetch.py's raw_path is its article.json FILE — the workspace is its dir
WORK_DIR=$(printf '%s' "$FETCH_JSON" | python3 -c "import sys,json,os; print(os.path.dirname(json.load(sys.stdin)['raw_path']))") \
  || { echo "✗ fetch JSON parse failed"; finalize 3; }
echo "  workspace: $WORK_DIR"

# ── Stage 2: transcribe (bash; loads runtime.conf itself) ──
# Skip when this workspace already has a raw ASR product — delete
# $WORK_DIR/faster-whisper/transcript.md to force a re-transcribe.
if [ -s "$WORK_DIR/faster-whisper/transcript.md" ]; then
  echo "[2/4] transcribe — cached transcript found, skipped"
else
  echo "[2/4] transcribe"
  bash "$SCRIPT_DIR/transcribe.sh" "$WORK_DIR" || { echo "✗ transcribe failed"; finalize 3; }
fi

# locate the transcript dir produced by this run (references/transcripts/**/<BV>)
BV=$(python3 -c "import json;print(json.load(open('$WORK_DIR/metadata.json')).get('bvid',''))")
TD=$(find "$OUTDIR/references/transcripts" -type d -name "*${BV}*" 2>/dev/null | tail -1)

# ── Stage 3: slides (optional; failures degrade to partial) ──
RC=0
if [ "$NO_SLIDES" -eq 0 ]; then
  # Skip when slides were already extracted — delete
  # $WORK_DIR/slides/slides.json to force a re-extract (OCR is the
  # most expensive stage; keyed to the audio's cid validity via fetch).
  if [ -s "$WORK_DIR/slides/slides.json" ]; then
    echo "[3/4] slides — cached slides.json found, skipped"
  else
    echo "[3/4] slides"
    PY "$SCRIPT_DIR/slides-extract.py" "$WORK_DIR" || RC=2
  fi
else
  echo "[3/4] slides skipped (--no-slides)"
fi

# ── Stage 4: merge (needs slides + transcript) ──
if [ "$NO_MERGE" -eq 0 ] && [ "$RC" -eq 0 ] && [ -f "$WORK_DIR/slides/slides.json" ]; then
  echo "[4/4] merge"
  [ -n "$TD" ] || { echo "✗ transcript dir not found for $BV"; finalize 2; }
  PY "$SCRIPT_DIR/merge-slides.py" "$WORK_DIR" --transcript-dir "$TD" || RC=2
else
  echo "[4/4] merge skipped"
fi

echo ""
echo "Done (exit $RC). Artifacts:"
[ -n "$TD" ] && echo "  transcript : $TD/transcript.md"
[ -f "$TD/transcript.final.md" ] && echo "  merged     : $TD/transcript.final.md"
[ -f "$TD/report.md" ] && echo "  report     : $TD/report.md (manifest+正文+附录，追溯入口)"
[ -f "$TD/llm-changes.jsonl" ] && echo "  llm log    : $TD/llm-changes.jsonl (LLM 改写 diff 日志)"
[ -f "$WORK_DIR/slides/slides.json" ] && echo "  slides     : $WORK_DIR/slides/slides.json"
echo "  workspace  : $WORK_DIR"
[ -f "$WORK_DIR/context.md" ] && echo "  context    : $WORK_DIR/context.md (简介+置顶+热门5+最新5评论)"
finalize "$RC"
