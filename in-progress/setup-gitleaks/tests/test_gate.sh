#!/usr/bin/env bash
# Self-check for the setup-gitleaks templates: the gate must FAIL on a seeded
# placeholder secret, PASS on a clean tree, and WARN (not silently pass) when
# gitleaks/config is missing. Run: bash tests/test_gate.sh
set -uo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d "$HOME/tmp/setup-gitleaks-test.XXXXXX")"
mkdir -p "$TMP"
trap 'rm -rf "$TMP"' EXIT
pass=0; fail=0
ok()   { echo "PASS: $1"; pass=$((pass+1)); }
bad()  { echo "FAIL: $1"; fail=$((fail+1)); }

# fixture repo: template config + gate + one clean file
git init -q "$TMP/repo" 2>/dev/null || { mkdir -p "$TMP/repo"; git init -q "$TMP/repo"; }
cp "$DIR/templates/gitleaks.toml" "$DIR/templates/sanitize-check.sh" "$TMP/repo/"
mkdir -p "$TMP/repo/scripts"; mv "$TMP/repo/sanitize-check.sh" "$TMP/repo/scripts/"
echo "nothing secret here" > "$TMP/repo/clean.txt"
git -C "$TMP/repo" add -A 2>/dev/null

# 1. clean tree exits 0
if (cd "$TMP/repo" && bash scripts/sanitize-check.sh >/dev/null 2>&1); then
    ok "clean tree exits 0"
else
    bad "clean tree should exit 0"
fi

# 2. seeded placeholder secret exits 1 with a GITLEAKS finding
echo 'api_key = "EXAMPLE-SECRET-PLACEHOLDER"' > "$TMP/repo/leak.txt"
git -C "$TMP/repo" add leak.txt 2>/dev/null
out=$(cd "$TMP/repo" && bash scripts/sanitize-check.sh 2>&1)
rc=$?
if [[ $rc -eq 1 ]] && grep -q 'GITLEAKS leak.txt.*example-credential' <<<"$out"; then
    ok "seeded secret -> exit 1 with rule-id finding"
else
    bad "seeded secret should exit 1 with finding (rc=$rc)"
fi

# 3. missing gitleaks config -> WARN + no false clean
rm "$TMP/repo/gitleaks.toml"
out=$(cd "$TMP/repo" && bash scripts/sanitize-check.sh 2>&1)
if grep -q 'WARN: gitleaks or config missing' <<<"$out"; then
    ok "missing config -> WARN, not silent pass"
else
    bad "missing config should WARN"
fi

echo "== $pass passed, $fail failed =="
[[ $fail -eq 0 ]]
