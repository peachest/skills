#!/usr/bin/env bash
# spawn-implementer — one call: wt worktree → orca worktree id → orchestration worker-start.
#   spawn-implementer.sh <repo-cwd> <branch> --spec-file F [--base <branch>] [--list]
# Fallback when orchestration is unavailable: terminal-create path, see SKILL.md §Process.
set -euo pipefail

usage() { echo "usage: spawn-implementer.sh <repo-cwd> <branch> --spec-file F [--base <branch>] [--list]" >&2; exit 1; }
ORCA="${ORCA_BIN:-orca-ide}"
if [ "${1:-}" = "--list" ]; then exec "$ORCA" worktree list --json; fi
[ $# -ge 2 ] || usage
REPO="${1%/}"; BRANCH="$2"; shift 2
BASE=""
SPEC_FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --spec-file) SPEC_FILE="$2"; shift 2 ;;
    --base) BASE="$2"; shift 2 ;;
    *) usage ;;
  esac
done

[ -f "$SPEC_FILE" ] || { echo "spec file not found: $SPEC_FILE" >&2; exit 2; }
[ -d "$REPO" ] || { echo "repo not found: $REPO" >&2; exit 2; }

# 1. worktree via wt (hooks install deps; cwd convention ~/projects/<repo>-<branch-slug>)
#    Skip creation if the branch already has a worktree.
WT_PATH=$(git -C "$REPO" worktree list --porcelain | awk -v b="refs/heads/$BRANCH" '
  $1=="worktree"{wt=$2} $1=="branch"&&$2==b{print wt; exit}')
if [ -z "$WT_PATH" ]; then
  if [ -n "$BASE" ]; then
    (cd "$REPO" && wt switch -c "$BRANCH" -b "$BASE") >/dev/null
  else
    (cd "$REPO" && wt switch -c "$BRANCH") >/dev/null
  fi
  WT_PATH=$(git -C "$REPO" worktree list --porcelain | awk -v b="refs/heads/$BRANCH" '
    $1=="worktree"{wt=$2} $1=="branch"&&$2==b{print wt; exit}')
fi
[ -n "$WT_PATH" ] || { echo "worktree for $BRANCH not found after wt switch" >&2; exit 3; }

# 2. resolve orca worktree id by path
WT_ID=$("$ORCA" worktree list --json | WT_PATH="$WT_PATH" python3 -c '
import json,sys,os
d=json.load(sys.stdin)
wts=d.get("worktrees") or d.get("result",{}).get("worktrees",[])
want=os.environ["WT_PATH"]
for w in wts:
    if (w.get("path") or w.get("dir") or "").rstrip("/") == want.rstrip("/"):
        print(w.get("id") or w.get("worktree_id")); break
')
[ -n "$WT_ID" ] || { echo "orca worktree id not resolved for $WT_PATH (worktree list follows)" >&2; "$ORCA" worktree list --json >&2; exit 4; }

# 3. orchestration: run + task + worker (verbs verified on orca app 1.4.205 — re-verify after upgrade)
#    worker-start binds the task explicitly (--task) — no auto-claim race.
RUN_ID=$(python3 - "$BRANCH" <<'PY'
import json,subprocess,sys,os
branch=sys.argv[1]
out=subprocess.run([os.environ.get("ORCA_BIN","orca-ide"),"orchestration","run-create",
  "--objective",f"implement {branch}","--json"],capture_output=True,text=True)
if out.returncode!=0: sys.stderr.write(out.stderr); sys.exit(5)
d=json.loads(out.stdout)
print(d.get("id") or d.get("run",{}).get("id",""))
PY
)
TASK_ID=$(ORCA="$ORCA" RUN_ID="$RUN_ID" SPEC_FILE="$SPEC_FILE" BRANCH="$BRANCH" python3 - <<'PY'
import json,subprocess,os
spec=open(os.environ["SPEC_FILE"]).read()
out=subprocess.run([os.environ["ORCA"],"orchestration","task-create",
  "--run",os.environ["RUN_ID"],"--spec",spec,"--json"],capture_output=True,text=True)
if out.returncode!=0: sys.stderr.write(out.stderr); sys.exit(6)
d=json.loads(out.stdout)
print(d.get("id") or d.get("task",{}).get("id",""))
PY
)
START_JSON=$(BRANCH_SLUG="${BRANCH//\//-}" "$ORCA" orchestration worker-start \
  --task "$TASK_ID" --worktree "id:$WT_ID" --agent pi \
  --name "impl-$BRANCH_SLUG" --json)
HANDLE=$(printf '%s' "$START_JSON" | python3 -c '
import json,sys
d=json.load(sys.stdin)
r=d.get("result",d)
w=r.get("worker") or r
print(w.get("id") or w.get("handle") or w.get("terminal",""))')

echo "branch=$BRANCH worktree=$WT_PATH wt_id=$WT_ID run=$RUN_ID task=$TASK_ID worker=$HANDLE status=dispatched (receipt arrives via worker_done — do not wait)"
