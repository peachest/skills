#!/usr/bin/env bash
# spawn-course — one tab + one teach-<course> herdr session + bootstrap prompt, in one call.
#   spawn-course.sh <academy-root> <course> [--prompt-file F] [--list]
# No --wait anywhere: receipts arrive as injected user messages (P-002).
# ponytail: duplicates ~10 lines of herdr-peer.sh plumbing (tab vs pane + academy
# bootstrap); if a second tab-spawn consumer appears, hoist into multi-agent-collab.
set -euo pipefail

HERDR="${HERDR_BIN:-herdr}"
usage() { echo "usage: spawn-course.sh <academy-root> <course> [--prompt-file F] [--list]" >&2; exit 1; }
jqget() { python3 -c "import json,sys; d=json.load(sys.stdin); print(eval(sys.argv[1]))" "$1"; }

[ $# -ge 2 ] || usage
ROOT="${1%/}"; COURSE="$2"; shift 2
PROMPT_FILE=""
MODE=spawn
while [ $# -gt 0 ]; do
  case "$1" in
    --prompt-file) PROMPT_FILE="$2"; shift 2 ;;
    --list) MODE=list; shift ;;
    *) usage ;;
  esac
done
DIR="$ROOT/courses/$COURSE"
NAME="teach-$COURSE"

if [ "$MODE" = list ]; then
  "$HERDR" agent list | python3 -c "
import json,sys
d=json.load(sys.stdin)
for a in d.get('result',{}).get('agents',[]):
    print(a.get('name'),'|',a.get('pane_id'),'|',a.get('agent_status'),'|',a.get('cwd',''))"
  exit 0
fi

[ -d "$DIR" ] || { echo "no such course dir: $DIR" >&2; exit 2; }

TAB_JSON=$("$HERDR" tab create --cwd "$DIR")
TAB_ID=$(printf '%s' "$TAB_JSON" | jqget "d['result']['tab']['tab_id']")
PANE_ID=$(printf '%s' "$TAB_JSON" | jqget "d['result']['root_pane']['pane_id']")

START_JSON=$("$HERDR" agent start "$NAME" --kind pi --pane "$PANE_ID")
STATUS=$(printf '%s' "$START_JSON" | jqget "d['result']['agent'].get('agent_status','?')")

if [ -n "$PROMPT_FILE" ]; then
  PROMPT=$(cat "$PROMPT_FILE")
else
  PROMPT="/skill:multi-agent-collab 【课程 bootstrap】你是 $NAME（课程 $COURSE，pane $PANE_ID）。确认你的 cwd = $DIR（/skill:teach 前先确认目录）。加载 /skill:teach。共享层：知识经 RESOURCES.md → ../../okb/，组件经 ../assets/（symlink → ../../assets）。今日目标以用户到场后的话为准；先回执：工作区状态 + 用户既有笔记预读结果 + 计划的 Probe 起点。"
fi
"$HERDR" agent prompt "$NAME" "$PROMPT" >/dev/null

echo "$NAME tab=$TAB_ID pane=$PANE_ID status=$STATUS prompt=sent (receipt arrives as injected message — do not wait)"
