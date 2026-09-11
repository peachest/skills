#!/usr/bin/env bash
# check-all-env.sh — umbrella entry: run every skill's check-env.sh, then
# sweep the git history with gitleaks.
#
# Step one of environment migration (see docs/agents/skill-authoring.md).
# Exit code 1 if any skill FAILs or the gitleaks sweep finds a leak.

set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
total_fail=0
ran=0

# find check-env.sh in tracked and untracked skills alike, skip vendor
while IFS= read -r -d '' check; do
  skill_dir=$(dirname "$(dirname "$check")")
  skill=$(basename "$skill_dir")
  echo "=== $skill ==="
  if out=$(bash "$check" 2>&1); then
    printf '%s\n' "$out" | grep -E '^FAIL' && total_fail=$((total_fail+1)) || true
    printf '%s\n' "$out" | grep -cE '^PASS' | sed 's/^/  PASS count: /'
    warns=$(printf '%s\n' "$out" | grep -cE '^WARN' || true)
    [ "${warns:-0}" -gt 0 ] && printf '  WARN count: %s\n' "$warns"
    echo "  OK"
  else
    printf '%s\n' "$out"
    echo "  FAILED"
    total_fail=$((total_fail+1))
  fi
  ran=$((ran+1))
done < <(find "$ROOT" -name check-env.sh -not -path "*/vendor/*" -not -path "*/.git/*" -not -path "*/deprecated/*" -print0 | sort -z)

# gitleaks sweep over committed history (the tuned config is node-specific,
# lives outside the repo; missing tool/config degrades to WARN, not FAIL)
echo "=== gitleaks sweep ==="
GITLEAKS_CONF="$HOME/data/benchmark/config/gitleaks.toml"
if command -v gitleaks >/dev/null 2>&1 && [ -f "$GITLEAKS_CONF" ]; then
  if gitleaks git "$ROOT" --config "$GITLEAKS_CONF" --redact --no-banner \
      --report-format json --report-path /tmp/check-all-env-gitleaks.json >/dev/null 2>&1; then
    echo "  PASS  no leaks in history"
  else
    python3 -c "import json; [print(f'  FAIL  {f[\"File\"]} ({f[\"RuleID\"]})') for f in json.load(open('/tmp/check-all-env-gitleaks.json'))[:10]]" 2>/dev/null
    echo "  FAILED  leaks found — see /tmp/check-all-env-gitleaks.json"
    total_fail=$((total_fail+1))
  fi
else
  echo "  WARN  gitleaks or $GITLEAKS_CONF missing — leak sweep skipped"
fi

echo ""
echo "checked $ran skill(s), $total_fail failing"
exit $([ "$total_fail" -eq 0 ] && echo 0 || echo 1)
