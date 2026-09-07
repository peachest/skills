#!/usr/bin/env bash
# html-render-check orchestrator: serve the artifact over http, run the generic
# battery (plus optional page-specific battery) and capture a screenshot per
# artifact via obscura, then report a verdict.
#
# Usage:
#   bash check.sh [options] <file.html> [<file.html>...]
# Options:
#   --port N        http port (default $CHECK_PORT or 8742)
#   --shot-dir DIR  screenshot output dir (default: artifact's own directory)
#   --extra-js F    page-specific battery JS file (IIFE returning JSON string)

set -u

SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
CONF="$SKILL_DIR/runtime.conf"
[ -f "$CONF" ] && . "$CONF"
OBSCURA_BIN="${OBSCURA_BIN:-obscura}"
PORT="${CHECK_PORT:-8742}"
SHOT_DIR=""
EXTRA_JS=""

while [ $# -gt 0 ]; do
  case "$1" in
    --port) PORT="$2"; shift 2 ;;
    --shot-dir) SHOT_DIR="$2"; shift 2 ;;
    --extra-js) EXTRA_JS="$2"; shift 2 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) break ;;
  esac
done

[ $# -ge 1 ] || { echo "usage: check.sh [--port N] [--shot-dir DIR] [--extra-js FILE] <file.html>..." >&2; exit 2; }

command -v "$OBSCURA_BIN" >/dev/null 2>&1 || { echo "FAIL obscura not on PATH — run scripts/check-env.sh first" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "FAIL python3 missing — run scripts/check-env.sh" >&2; exit 1; }

BATTERY="$SKILL_DIR/scripts/battery.js"

# Serve each artifact's directory. Artifacts may live in different dirs; we
# restart the server per unique directory (simplest correct approach).
declare -a FILES=("$@")
declare -a FAILED=()

run_battery() {
  # $1 = obscura binary, $2 = URL. Echoes the JSON verdict line (or EXC:...).
  local js
  js=$(cat "$BATTERY")
  "$1" fetch "$2" --allow-private-network -e "$js" 2>/dev/null \
    | grep -E '^\{' | tail -1
}

run_extra() {
  # $1 = obscura binary, $2 = URL, $3 = extra-js path.
  "$1" fetch "$2" --allow-private-network -e "$(cat "$3")" 2>/dev/null \
    | grep -E '^\{' | tail -1
}

take_shot() {
  # $1 = obscura binary, $2 = URL, $3 = output png path.
  "$1" fetch "$2" --allow-private-network -s "$3" >/dev/null 2>&1
  [ -f "$3" ]
}

prev_dir=""
srv_pid=""
cleanup() { [ -n "$srv_pid" ] && kill "$srv_pid" 2>/dev/null; }
trap cleanup EXIT

for f in "${FILES[@]}"; do
  [ -f "$f" ] || { echo "FAIL $f — file not found"; FAILED+=("$f"); continue; }
  dir=$(cd "$(dirname "$f")" && pwd)
  base=$(basename "$f")

  # ---- Stage 0: structure validation (offline, parse-level) ----------------
  # Absorbed from the former html-review skill. Duplicate ids / broken
  # structure also break the render battery's assumptions, so gate on it.
  echo "== $f"
  struct_out=$(python3 "$SKILL_DIR/scripts/validate_html.py" "$f" 2>&1)
  struct_rc=$?
  echo "$struct_out" | sed 's/^/  struct| /'
  if [ "$struct_rc" -ne 0 ]; then
    FAILED+=("$f"); echo "  struct: FAIL — skipping render pass"
    continue
  fi
  if [ "$dir" != "$prev_dir" ]; then
    cleanup; srv_pid=""
    (cd "$dir" && nohup python3 -m http.server "$PORT" >/dev/null 2>&1 &) 
    # Wait for the server to accept connections.
    for _ in $(seq 1 20); do
      if python3 -c "import socket,sys; s=socket.socket(); s.settimeout(0.3)
sys.exit(0 if s.connect_ex(('127.0.0.1', $PORT))==0 else 1)" 2>/dev/null; then
        srv_pid=$(pgrep -f "http.server $PORT" | tail -1); break
      fi
      sleep 0.25
    done
    [ -n "$srv_pid" ] || { echo "FAIL local server — could not start on port $PORT"; FAILED+=("$f"); continue; }
    prev_dir="$dir"
  fi

  url="http://127.0.0.1:$PORT/$base"
  shot_target="${SHOT_DIR:-$dir}/${base%.html}.render-check.png"

  echo "== $f"
  verdict=$(run_battery "$OBSCURA_BIN" "$url")
  # Transient failures (server startup race, obscura hiccup) get one retry.
  if [ -z "$verdict" ]; then
    sleep 1
    verdict=$(run_battery "$OBSCURA_BIN" "$url")
  fi
  if [ -z "$verdict" ]; then
    echo "FAIL $f — battery returned no JSON after retry (page did not load, or eval died; see quirks in SKILL.md)"
    FAILED+=("$f"); continue
  fi
  echo "battery: $verdict"

  ok=$(python3 - "$verdict" <<'EOF'
import json, sys
try:
    d = json.loads(sys.argv[1])
    issues = d.get("issues")
    # Defensive: obscura occasionally re-serializes long payloads into a
    # table format where `issues` arrives as a string — treat as unparseable.
    if isinstance(issues, str):
        print("bad")
    else:
        print("yes" if d.get("ok") else "no")
except Exception:
    print("bad")
EOF
)
  if [ "$ok" = "bad" ]; then
    echo "WARN $f — verdict JSON unparseable (long-payload table serialization quirk); re-run once, adjudicate manually if it persists"
  elif [ "$ok" != "yes" ]; then
    FAILED+=("$f")
  fi

  if [ -n "$EXTRA_JS" ]; then
    [ -f "$EXTRA_JS" ] || { echo "FAIL extra-js — $EXTRA_JS not found"; FAILED+=("$f"); continue; }
    extra=$(run_extra "$OBSCURA_BIN" "$url" "$EXTRA_JS")
    echo "extra:   ${extra:-<no JSON>}"
    case "$extra" in
      ""|*'EXC:'*) FAILED+=("$f") ;;
      *'"ok":false'*|*'"ok": false'*) FAILED+=("$f") ;;
    esac
  fi

  if take_shot "$OBSCURA_BIN" "$url" "$shot_target"; then
    echo "shot:    $shot_target"
  else
    echo "WARN screenshot failed for $f (geometry findings above still stand)"
  fi
done

echo "---"
if [ "${#FAILED[@]}" -eq 0 ]; then
  echo "RESULT: PASS (${#FILES[@]} artifact(s), findings=0 or advisory-only)"
  exit 0
else
  echo "RESULT: FAIL (${#FAILED[@]} artifact(s) with findings: ${FAILED[*]})"
  echo "Findings are adjudication prompts — inspect the screenshot evidence before editing."
  exit 1
fi
