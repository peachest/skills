#!/usr/bin/env bash
# Sanitize gate for the public skills repo (rules: docs/agents/skill-authoring.md).
#
# gitleaks covers credentials/keys only. This adds the manual-checklist layer —
# internal domains, node names, project names, CRD names — that gitleaks rules
# don't cover ("gitleaks 通过 ≠ 脱敏完成"). Exit 0 = clean, 1 = findings.
#
# Usage:
#   bash scripts/sanitize-check.sh              # tracked files (committed state)
#   bash scripts/sanitize-check.sh -u           # untracked + modified files (pre-commit batch review)
#   bash scripts/sanitize-check.sh <paths...>   # explicit files/dirs
#
# New internal identifier surfaced in review → append to PATTERNS below.
# Domain placeholder allowlist (must never match): gitlab.blue.example,
# gitlab.red.example, harbor.example.com, internal.example.com, 203.0.113.x.
set -uo pipefail

GITLEAKS_CONFIG="${GITLEAKS_CONFIG:-$HOME/data/benchmark/config/gitleaks.toml}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# grep -E pattern. Word-bounded where the token is also a common substring.
PATTERNS='gitblue|ai_bot001|transwarp|harbor\.trans|\bllmops\b|\bllm1[0-9]\b|\bdev(17|32|119)\b|172\.1[6-9]\.|\bnodexpu\b|NodeXpu|ppu-device|\bkvtop\b|\bbase-charts\b|\bSMG\b|\bsmg\b|applied-ai|aip-mm|\bcvat\b|icc\.io'

mode="tracked"
if [[ "${1:-}" == "-u" ]]; then mode="untracked"; shift; fi

if [[ $# -gt 0 ]]; then
    mapfile -t files < <(find "$@" -type f 2>/dev/null)
elif [[ "$mode" == "untracked" ]]; then
    mapfile -t files < <(git status --porcelain -uall | cut -c4-)
else
    mapfile -t files < <(git ls-files)
fi

rc=0

# Layer 1: manual-checklist patterns
echo "== pattern scan (${#files[@]} files, mode=$mode) =="
hits=0
for f in "${files[@]}"; do
    [[ "$f" == scripts/sanitize-check.sh ]] && continue   # checker contains PATTERNS by construction
    while IFS= read -r line; do
        echo "PATTERN  $line"
        hits=$((hits+1))
    done < <(grep -nEH "$PATTERNS" -- "$f" 2>/dev/null)
done
[[ $hits -gt 0 ]] && rc=1
echo "pattern findings: $hits"

# Layer 2: gitleaks (credentials) — full-repo scan, findings filtered to targets
echo "== gitleaks scan =="
if [[ -f "$GITLEAKS_CONFIG" ]] && command -v gitleaks >/dev/null 2>&1; then
    report=$(mktemp)
    if gitleaks dir . --config "$GITLEAKS_CONFIG" --report-format json --report-path "$report" >/dev/null 2>&1; then
        echo "gitleaks findings: 0"
    else
        out=$(python3 -c "
import json
finds = json.load(open('$report'))
targets = set('''${files[*]}'''.split())
mine = [f for f in finds if f['File'] in targets]
for f in mine: print(f\"GITLEAKS {f['File']}:{f['StartLine']} {f['RuleID']}\")
print('FINDINGS ' + str(len(mine)))")
        echo "$out" | grep -v '^FINDINGS'
        n=$(echo "$out" | grep '^FINDINGS' | cut -d' ' -f2)
        [[ "$n" != "0" ]] && rc=1
    fi
    rm -f "$report"
else
    echo "WARN: gitleaks or config missing ($GITLEAKS_CONFIG) — credential layer skipped" >&2
fi

echo "== result: $([[ $rc -eq 0 ]] && echo CLEAN || echo DIRTY) =="
exit $rc
