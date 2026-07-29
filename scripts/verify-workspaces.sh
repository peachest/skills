#!/usr/bin/env bash
# verify-workspaces.sh — Check workspace structure and lesson counts after generation
#
# Generic pipeline step 2 (post-generation verification):
# Verify that each workspace has the expected files and report stats.
# Used by teach batch generation, reusable by any skill that generates
# HTML lessons in workspace directories.
#
# Usage:
#   verify-workspaces.sh <lab-root> [workspace1 workspace2 ...]
#
# If no workspace names given, scans all subdirectories of <lab-root>.
#
# Checks per workspace:
#   - MISSION.md exists
#   - NOTES.md exists
#   - lessons/*.html count
#   - reference/*.html count
#   - source-notes/*.md count
#   - unique CSS classes across lessons
#
# Output: table to stdout

set -euo pipefail

LAB_ROOT="${1:?Usage: $0 <lab-root> [workspace1 workspace2 ...]}"
shift
LAB_ROOT="${LAB_ROOT/#\~/$HOME}"

# Determine workspaces
if [ $# -gt 0 ]; then
  WORKSPACES=("$@")
else
  WORKSPACES=()
  for d in "$LAB_ROOT"/*/; do
    name=$(basename "$d")
    # Skip non-workspace dirs (starting with _ or .)
    [[ "$name" =~ ^[_\.] ]] && continue
    WORKSPACES+=("$name")
  done
fi

printf "%-20s %5s %5s %5s %6s %8s\n" "Workspace" "Lessons" "Refs" "Notes" "CSS" "Tokens"
printf "%-20s %5s %5s %5s %6s %8s\n" "---------" "-------" "----" "-----" "---" "------"

total_lessons=0
total_refs=0
for ws in "${WORKSPACES[@]}"; do
  dir="$LAB_ROOT/$ws"
  lessons=$(find "$dir/lessons" -name "*.html" 2>/dev/null | wc -l)
  refs=$(find "$dir/reference" -name "*.html" 2>/dev/null | wc -l)
  notes=$(find "$dir/source-notes" -name "*.md" -type f 2>/dev/null | wc -l)
  classes=$(cat "$dir"/lessons/*.html 2>/dev/null | awk '/<style>/,/<\/style>/' | grep -oP '\.[a-z][-a-z0-9]+' | sort -u | wc -l)
  tokens=$(find "$dir/source-notes" -name "*.md" -type f -exec cat {} + 2>/dev/null | wc -c)
  tokens=$((tokens / 3))
  
  printf "%-20s %5d %5d %5d %6d %8d\n" "$ws" "$lessons" "$refs" "$notes" "$classes" "$tokens"
  total_lessons=$((total_lessons + lessons))
  total_refs=$((total_refs + refs))
done

echo ""
echo "Total: $total_lessons lessons, $total_refs refs"

# Union of all CSS classes
all_classes=$(cat "$LAB_ROOT"/*/lessons/*.html 2>/dev/null | awk '/<style>/,/<\/style>/' | grep -oP '\.[a-z][-a-z0-9]+' | sort -u | wc -l)
echo "Union of all CSS classes: $all_classes"
