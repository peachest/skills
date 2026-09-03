#!/usr/bin/env bash
# check-all-env.sh — umbrella entry: run every skill's check-env.sh.
#
# Step one of environment migration (see docs/agents/skill-authoring.md).
# Exit code 1 if any skill FAILs.

set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
total_fail=0
ran=0
skipped=0

# find check-env.sh in tracked and untracked skills alike, skip vendor
while IFS= read -r -d '' check; do
  skill_dir=$(dirname "$(dirname "$check")")
  skill=$(basename "$skill_dir")
  echo "=== $skill ==="
  if out=$(bash "$check" 2>&1); then
    printf '%s\n' "$out" | grep -E '^FAIL' && total_fail=$((total_fail+1)) || true
    printf '%s\n' "$out" | grep -cE '^PASS' | sed 's/^/  PASS count: /'
    warns=$(printf '%s\n' "$out" | grep -cE '^WARN' || true)
    [ "$warns" -gt 0 ] && printf '  WARN count: %s\n' "$warns"
    echo "  OK"
  else
    printf '%s\n' "$out"
    echo "  FAILED"
    total_fail=$((total_fail+1))
  fi
  ran=$((ran+1))
done < <(find "$ROOT" -name check-env.sh -not -path "*/vendor/*" -not -path "*/.git/*" -not -path "*/deprecated/*" -print0 | sort -z)

echo ""
echo "checked $ran skill(s), $total_fail failing"
exit $([ "$total_fail" -eq 0 ] && echo 0 || echo 1)
