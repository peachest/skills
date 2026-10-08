#!/usr/bin/env bash
# run-checks.sh — orchestrator for the teach check family. Runs the requested
# checks, writes every finding (check-prefixed) to reviews/checks-<lesson>.txt,
# prints a one-line per-check verdict table as the LAST output (survives | tail -1),
# and exits by the check family's own contract:
#   fix-class (css/nav/resource): any finding  → exit 1
#   adjudication-class (beat/prose): findings are FLAGs → always exit 0;
#     adjudication is a human action, the script has no authority to fail them.
#   anchor: exit 1 only on open (non-adjudicated) findings.
#
# Usage: run-checks.sh [--only css,beat,...] [--lesson N] <lesson-dir>
#   --only   comma list from: css nav resource beat prose anchor
#   --lesson lesson number filter (e.g. 3 → lessons/0003-*)
#
# Completion criteria are NOT restated here — each check's own section in
# SKILL.md owns its criterion; this script only runs them and reports.
set -u

SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
ONLY="" LESSON="" DIR=""
while [ $# -gt 0 ]; do
  case "$1" in
    --only) ONLY="$2"; shift 2 ;;
    --lesson) LESSON="$2"; shift 2 ;;
    -h|--help) echo "usage: run-checks.sh [--only css,nav,resource,beat,prose,anchor] [--lesson N] <lesson-dir>"; exit 0 ;;
    *) DIR="$1"; shift ;;
  esac
done
[ -n "${DIR:-}" ] || { echo "usage: run-checks.sh [--only ...] [--lesson N] <lesson-dir>" >&2; exit 2; }
[ -d "$DIR" ] || { echo "FAIL: $DIR is not a directory" >&2; exit 2; }

LESSION_FILES=()
if [ -n "$LESSON" ]; then
  mapfile -t LESSION_FILES < <(ls "$DIR"/$(printf "%04d" "$LESSON")-*.html 2>/dev/null)
else
  mapfile -t LESSION_FILES < <(ls "$DIR"/*.html 2>/dev/null | grep -v render-check)
fi
[ ${#LESSION_FILES[@]} -gt 0 ] || { echo "no lesson files in $DIR"; exit 0; }

WANT() { [ -z "$ONLY" ] || printf '%s\n' "$ONLY" | tr ',' '\n' | grep -qx "$1"; }

OUTDIR="$(dirname "$DIR")/reviews"
mkdir -p "$OUTDIR"
TAG="all"; [ -n "$LESSON" ] && TAG="$LESSON"
REPORT="$OUTDIR/checks-$TAG.txt"
: > "$REPORT"

declare -A VERDICT
run_check() { # name, class, files...
  local name="$1" class="$2"; shift 2
  local out rc=0
  out=$( "$@" 2>&1 ); rc=$?
  # prefix every finding line with the check name
  printf '%s\n' "$out" | sed "s|^|$name: |" >> "$REPORT"
  if [ "$class" = fix ] && [ "$rc" -ne 0 ]; then VERDICT[$name]="FAIL"
  elif [ "$class" = adjudicate ]; then
    if printf '%s\n' "$out" | grep -qi "flag\|finding"; then VERDICT[$name]="FLAG"; else VERDICT[$name]="PASS"; fi
    rc=0  # adjudication-class never fails the battery
  else VERDICT[$name]="PASS"; fi
  return 0
}

if WANT css; then
  for f in "${LESSION_FILES[@]}"; do run_check css fix python3 "$SKILL_DIR/assets/css-self-check.py" "$f"; done
fi
if WANT nav; then
  run_check nav fix python3 "$SKILL_DIR/assets/nav-chain-check.py" "$DIR"
fi
if WANT resource; then
  run_check resource fix python3 "$SKILL_DIR/assets/resource-check.py" "$DIR"
fi
if WANT beat; then
  for f in "${LESSION_FILES[@]}"; do run_check beat adjudicate python3 "$SKILL_DIR/assets/beat-check.py" "$f"; done
fi
if WANT prose; then
  for f in "${LESSION_FILES[@]}"; do run_check prose adjudicate python3 "$SKILL_DIR/assets/prose-freq-check.py" "$f"; done
fi
if WANT anchor; then
  AJ="$(dirname "$DIR")/anchors.json"
  if [ -f "$AJ" ]; then
    for f in "${LESSION_FILES[@]}"; do run_check anchor fix python3 "$SKILL_DIR/assets/anchor-check.py" "$AJ" "$f"; done
  else
    echo "anchor: SKIPPED — no anchors.json next to $DIR (extraction checklist not run?)" | tee -a "$REPORT"
    VERDICT[anchor]="SKIP"
  fi
fi

# ---- verdict table: the LAST output, designed to survive | tail -1 ---------
ORDER=(css nav resource beat prose anchor)
line="CHECKS:"
fail=0
for k in "${ORDER[@]}"; do
  [ -n "${VERDICT[$k]:-}" ] || continue
  line+=" $k=${VERDICT[$k]}"
  [ "${VERDICT[$k]}" = "FAIL" ] && fail=1
done
echo "$line"
echo "full findings: $REPORT"
exit $fail
