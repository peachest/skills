#!/usr/bin/env bash
# check-env — verify dispatch-implement's tool assumptions on this node.
set -u
fail=0
need_bin() { command -v "$1" >/dev/null 2>&1 || { echo "FAIL: '$1' not on PATH"; fail=1; }; }
need_bin wt
need_bin orca-ide
need_bin python3
need_bin jq || true

if command -v orca-ide >/dev/null 2>&1; then
  orca-ide status --json >/dev/null 2>&1 \
    && echo "OK: orca-ide runtime reachable" \
    || { echo "FAIL: orca-ide runtime unreachable (check orca-serve on this host)"; fail=1; }
  orca-ide orchestration --help >/dev/null 2>&1 \
    && echo "OK: orchestration verb present" \
    || echo "WARN: 'orchestration' verb missing — orca app may predate 1.4.205; re-check after upgrade"
fi
git worktree list --porcelain >/dev/null 2>&1 \
  && echo "OK: git worktree readable (wt plumbing)" \
  || { echo "FAIL: git worktree unavailable"; fail=1; }

[ "$fail" = 0 ] && echo "PASS" || echo "FAILED — fix the FAIL lines above (see SKILL.md §First-use verify)"
exit "$fail"
