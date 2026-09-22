#!/usr/bin/env bash
# check-env — verify dispatch-implement's tool assumptions on this node.
# Output: PASS/WARN/FAIL <item> — why/fix. Exit 1 only on FAIL.
set -u
fail=0
chk() { # chk <status> <item> <why/fix>
  echo "$1: $2 — $3"
  [ "$1" = "FAIL" ] && fail=1
  return 0
}
have() { command -v "$1" >/dev/null 2>&1; }

have wt && chk PASS "wt" "on PATH" \
  || chk FAIL "wt" "not on PATH — install worktrunk (~/.local/bin/wt)"
have python3 && chk PASS "python3" "on PATH" \
  || chk FAIL "python3" "not on PATH — spawn script parsing needs it"
have jq || chk WARN "jq" "missing — only the manual-path commands in SKILL.md use it; the script path needs python3 only"

if have orca-ide; then
  if orca-ide status --json >/dev/null 2>&1; then
    chk PASS "orca-ide runtime" "reachable"
  else
    chk FAIL "orca-ide runtime" "unreachable — check orca-serve on this host"
  fi
  if orca-ide orchestration --help >/dev/null 2>&1; then
    chk PASS "orchestration verb" "present"
  else
    chk WARN "orchestration verb" "missing — verb is gated (Settings/experimental) or app predates 1.4.205; check orca-ide --version and the orca-routing.md gate notes"
  fi
else
  chk FAIL "orca-ide" "not on PATH — install the orca CLI (see orca-routing.md)"
fi

git worktree list --porcelain >/dev/null 2>&1 \
  && chk PASS "git worktree plumbing" "readable (spawn script parses porcelain list)" \
  || chk FAIL "git worktree plumbing" "unavailable — check git install"

[ "$fail" = 0 ] && echo "PASS" || echo "FAILED — resolve the FAIL lines above (see SKILL.md §First-use verify)"
exit "$fail"
