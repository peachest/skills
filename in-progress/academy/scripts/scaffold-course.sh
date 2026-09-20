#!/usr/bin/env bash
# scaffold-course — Create-a-course as a tool: dir tree, assets symlink, RESOURCES,
# CURRICULUM registration. MISSION stays hand-written (mission-first rule).
#   scaffold-course.sh <academy-root> <name> --namespace <ns> [--mission-file F]
set -euo pipefail
usage() { echo "usage: scaffold-course.sh <academy-root> <name> --namespace <ns> [--mission-file F]" >&2; exit 1; }
[ $# -ge 3 ] || usage
ROOT="${1%/}"; NAME="$2"; shift 2
NS=""; MISSION_FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --namespace) NS="$2"; shift 2 ;;
    --mission-file) MISSION_FILE="$2"; shift 2 ;;
    *) usage ;;
  esac
done
[ -n "$NS" ] || usage
DIR="$ROOT/courses/$NAME"
[ -e "$DIR" ] && { echo "already exists: $DIR" >&2; exit 2; }
[ -f "$ROOT/CURRICULUM.md" ] || { echo "not an academy root (no CURRICULUM.md): $ROOT" >&2; exit 2; }

mkdir -p "$DIR"/{lessons,session-log,reference,learning-records}
ln -s ../../assets "$DIR/assets"

if [ -n "$MISSION_FILE" ]; then
  cp "$MISSION_FILE" "$DIR/MISSION.md"
else
  printf '# Mission: %s\n\n(one paragraph — why this course exists, what "done" means)\n' "$NAME" > "$DIR/MISSION.md"
fi

cat > "$DIR/RESOURCES.md" <<EOF
# Resources

## Shared OKB
- Pointers into \`../../okb/$NS/\` (curate via the okb skill when this list is thin)

## User notes
- (existing user notes relevant to this course — open questions are Probe-start gold)

## To read
- (articles handed over or in the user's TOREAD list)
EOF

printf '| %s | courses/%s | new | — |\n' "$NAME" "$NAME" >> "$ROOT/CURRICULUM.md"
echo "scaffolded $DIR (namespace $NS; registered in CURRICULUM.md; fill MISSION.md and RESOURCES.md next)"
