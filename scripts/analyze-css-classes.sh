#!/usr/bin/env bash
# analyze-css-classes.sh — Scan HTML files for inline CSS classes, output frequency report
#
# Generic pipeline step 3: analyze generated HTML for CSS patterns.
# Used by teach component analysis, reusable by any skill that needs
# to discover CSS patterns across generated HTML files.
#
# Usage:
#   analyze-css-classes.sh <lab-root> [--baseline <baseline-css>]
#
# Output:
#   - <lab-root>/_css-analysis.txt        — workspace|class pairs (raw data)
#   - <lab-root>/_css-frequency.txt       — frequency table (class count, sorted)
#   - <lab-root>/_css-baseline-diff.txt   — classes not in baseline, >=2 workspaces
#   - stdout: summary stats
#
# What it scans:
#   - All *.html files under <lab-root>/*/lessons/
#   - Extracts class names from <style> blocks (not from class= attributes)
#   - Counts unique classes per workspace
#   - If --baseline given, filters out classes already in the baseline CSS

set -euo pipefail

LAB_ROOT="$1"
BASELINE=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --baseline)
      BASELINE="$2"
      shift 2
      ;;
    *)
      LAB_ROOT="$1"
      shift
      ;;
  esac
done

if [ -z "$LAB_ROOT" ]; then
  echo "Usage: $0 <lab-root> [--baseline <baseline-css>]"
  exit 1
fi

LAB_ROOT="${LAB_ROOT/#\~/$HOME}"

# If baseline provided, extract its classes
BASELINE_FILE=""
if [ -n "$BASELINE" ]; then
  BASELINE="${BASELINE/#\~/$HOME}"
  BASELINE_FILE=$(mktemp)
  grep -oP '\.[a-z][-a-z0-9]+' "$BASELINE" | sort -u > "$BASELINE_FILE"
  echo "Baseline: $(wc -l < "$BASELINE_FILE") classes from $BASELINE"
fi

# Step 1: Extract workspace|class pairs
RAW_FILE="$LAB_ROOT/_css-analysis.txt"
find "$LAB_ROOT"/*/lessons -name '*.html' -type f 2>/dev/null | while read -r f; do
  ws=$(echo "$f" | grep -oP "$LAB_ROOT/\K[^/]+")
  awk '/<style>/,/<\/style>/' "$f" | grep -oP '\.[a-z][-a-z0-9]+' | sort -u | while read -r cls; do
    echo "$ws|$cls"
  done
done | sort > "$RAW_FILE"

TOTAL_CLASSES=$(cut -d'|' -f2 "$RAW_FILE" | sort -u | wc -l)
echo "Total unique CSS classes: $TOTAL_CLASSES"

# Step 2: Frequency table
FREQ_FILE="$LAB_ROOT/_css-frequency.txt"
cut -d'|' -f2 "$RAW_FILE" | sort | uniq -c | sort -rn > "$FREQ_FILE"
echo "Frequency table: $FREQ_FILE"

# Step 3: Baseline diff (if baseline provided)
if [ -n "$BASELINE_FILE" ]; then
  DIFF_FILE="$LAB_ROOT/_css-baseline-diff.txt"
  : > "$DIFF_FILE"
  
  cut -d'|' -f2 "$RAW_FILE" | sort | uniq -c | sort -rn | awk '$1 >= 2' | while read -r count cls; do
    if ! grep -q "^${cls}$" "$BASELINE_FILE"; then
      echo "$count $cls" >> "$DIFF_FILE"
    fi
  done
  
  DIFF_COUNT=$(wc -l < "$DIFF_FILE")
  echo "Baseline diff (>=2 ws, not in baseline): $DIFF_COUNT candidates → $DIFF_FILE"
fi

# Step 4: CSS variable analysis
echo ""
echo "=== CSS variable frequency ==="
find "$LAB_ROOT"/*/lessons -name '*.html' -type f 2>/dev/null -exec cat {} + | \
  awk '/<style>/,/<\/style>/' | \
  grep -oP -- '--[a-z][-a-z0-9]*' | sort | uniq -c | sort -rn | head -15

# Step 5: Dark/light theme count
echo ""
echo "=== Theme distribution ==="
dark=0; light=0; total=0
for f in $(find "$LAB_ROOT"/*/lessons -name '*.html' -type f 2>/dev/null); do
  total=$((total + 1))
  bg=$(awk '/<style>/,/<\/style>/' "$f" | grep -oP -- '--bg:\s*#\K[0-9a-f]{6}' | head -1)
  if [ -n "$bg" ]; then
    r=$((16#${bg:0:2}))
    g=$((16#${bg:2:2}))
    b=$((16#${bg:4:2}))
    brightness=$(( (r*299 + g*587 + b*114) / 1000 ))
    if [ "$brightness" -lt 128 ]; then
      dark=$((dark + 1))
    else
      light=$((light + 1))
    fi
  fi
done
echo "Dark: $dark, Light: $light, Total: $total"

# Cleanup
[ -n "$BASELINE_FILE" ] && rm -f "$BASELINE_FILE"
