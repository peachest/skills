#!/usr/bin/env bash
# scan-and-split-notes.sh — Scan note vaults, split by topic into workspaces
#
# Generic pipeline step 1: prepare source-notes/ for each workspace.
# Used by teach AFK batch generation, reusable by any skill that needs
# to split a note vault into topic-based workspaces.
#
# Usage:
#   scan-and-split-notes.sh <lab-root> <config-file>
#
# Config file format (one workspace per line):
#   <workspace-name>:<source-dir>:<keyword-regex>
#   # Lines starting with # are comments
#   # If keyword-regex is empty, all notes from source-dir go to this workspace
#
# Example:
#   go-core:~/obsidianNote/go:^(?!.*(controller|test|cli))
#   go-eng:~/obsidianNote/go:(test|ginkgo|gomega|mock|module)
#   go-tools:~/obsidianNote/go:(cli|cobra|gin|grpc|json|template)
#   go-k8s:~/obsidianNote/go:(controller|informer|reconcile|webhook|k8s|prometheus)
#   前端:~/obsidianNote/前端:
#   git:~/obsidianNote/git:
#
# The script:
# 1. Creates <lab-root>/<workspace>/source-notes/ for each workspace
# 2. Scans source-dir for *.md files (excluding assets/)
# 3. Classifies each note by filename matching against keyword-regex
# 4. Copies notes to the matching workspace, preserving subdirectory structure
# 5. Prints a summary table: workspace | notes | tokens

set -euo pipefail

LAB_ROOT="$1"
CONFIG_FILE="$2"

if [ -z "$LAB_ROOT" ] || [ -z "$CONFIG_FILE" ]; then
  echo "Usage: $0 <lab-root> <config-file>"
  exit 1
fi

# Expand ~ in paths
LAB_ROOT="${LAB_ROOT/#\~/$HOME}"

# Parse config and create workspaces
declare -a WS_NAMES WS_SRCS WS_REGEXS
while IFS=':' read -r name src regex; do
  # Skip comments and empty lines
  [[ "$name" =~ ^# ]] || [ -z "$name" ] && continue
  # Expand ~
  src="${src/#\~/$HOME}"
  
  WS_NAMES+=("$name")
  WS_SRCS+=("$src")
  WS_REGEXS+=("$regex")
  
  mkdir -p "$LAB_ROOT/$name/source-notes"
done < "$CONFIG_FILE"

# For each source dir, classify and copy notes
for i in "${!WS_NAMES[@]}"; do
  name="${WS_NAMES[$i]}"
  src="${WS_SRCS[$i]}"
  regex="${WS_REGEXS[$i]}"
  
  if [ ! -d "$src" ]; then
    echo "WARN: source dir not found: $src" >&2
    continue
  fi
  
  # If no regex, copy all notes from this source
  if [ -z "$regex" ]; then
    cd "$src"
    find . -name "*.md" -not -path "*/assets/*" -type f | while read -r f; do
      dir=$(dirname "$f")
      mkdir -p "$LAB_ROOT/$name/source-notes/$dir"
      cp "$f" "$LAB_ROOT/$name/source-notes/$dir/"
    done
  fi
done

# For workspaces with regex: scan shared source dirs and classify
# Group workspaces by source dir to avoid re-scanning
declare -A SRC_TO_WS
for i in "${!WS_NAMES[@]}"; do
  src="${WS_SRCS[$i]}"
  if [ -n "${WS_REGEXS[$i]}" ]; then
    SRC_TO_WS["$src"]+="${WS_NAMES[$i]}:${WS_REGEXS[$i]} "
  fi
done

for src in "${!SRC_TO_WS[@]}"; do
  if [ ! -d "$src" ]; then
    echo "WARN: source dir not found: $src" >&2
    continue
  fi
  
  # Parse workspace:regex pairs for this source
  pairs="${SRC_TO_WS[$src]}"
  
  find "$src" -name "*.md" -not -path "*/assets/*" -type f 2>/dev/null | while read -r filepath; do
    fname=$(basename "$filepath" .md)
    lname=$(echo "$fname" | tr '[:upper:]' '[:lower:]')
    
    # Find first matching workspace
    dest=""
    for pair in $pairs; do
      ws=$(echo "$pair" | cut -d: -f1)
      pattern=$(echo "$pair" | cut -d: -f2-)
      if echo "$lname" | grep -qiE "$pattern"; then
        dest="$ws"
        break
      fi
    done
    
    # If no match, use first workspace for this source as default
    if [ -z "$dest" ]; then
      dest=$(echo "$pairs" | cut -d' ' -f1 | cut -d: -f1)
    fi
    
    # Preserve relative path
    rel=$(echo "$filepath" | sed "s|$src/||")
    dir=$(dirname "$rel")
    mkdir -p "$LAB_ROOT/$dest/source-notes/$dir"
    cp "$filepath" "$LAB_ROOT/$dest/source-notes/$dir/"
  done
done

# Print summary
echo "=== Workspace summary ==="
printf "%-20s %5s %10s\n" "Workspace" "Notes" "Tokens"
printf "%-20s %5s %10s\n" "---------" "-----" "------"
for i in "${!WS_NAMES[@]}"; do
  name="${WS_NAMES[$i]}"
  count=$(find "$LAB_ROOT/$name/source-notes" -name "*.md" -type f 2>/dev/null | wc -l)
  size=$(find "$LAB_ROOT/$name/source-notes" -name "*.md" -type f -exec cat {} + 2>/dev/null | wc -c)
  printf "%-20s %5d %10d\n" "$name" "$count" "$((size / 3))"
done
