#!/usr/bin/env bash
# verify-course-links — Migrate step 7 as a tool: every RESOURCES.md pointer and
# lesson ../assets/ link resolves; assets is a symlink to ../../assets.
#   verify-course-links.sh <course-dir>   → pass/fail list, exit 1 on any failure
set -uo pipefail
[ $# -eq 1 ] || { echo "usage: verify-course-links.sh <course-dir>" >&2; exit 1; }
DIR="${1%/}"
[ -d "$DIR" ] || { echo "no such dir: $DIR" >&2; exit 1; }

fails=0
check() { # check <desc> <path>
  if [ -e "$2" ]; then echo "PASS $1"; else echo "FAIL $1 → $2"; fails=$((fails+1)); fi
}

# assets must be a symlink resolving into the academy layer
if [ -L "$DIR/assets" ] && [ -d "$DIR/assets/" ]; then
  echo "PASS assets symlink → $(readlink "$DIR/assets")"
else
  echo "FAIL assets is not a resolving symlink → $DIR/assets"; fails=$((fails+1))
fi

# RESOURCES.md: every relative path/link target resolves (from the course dir)
if [ -f "$DIR/RESOURCES.md" ]; then
  while IFS= read -r target; do
    [ -n "$target" ] || continue
    case "$target" in
      ../*|./*|okb/*) check "RESOURCES → $target" "$DIR/$target" ;;
      *) : ;;
    esac
  done < <(grep -oE '\]\(([^)# ]+)' "$DIR/RESOURCES.md" | sed 's/^](//' ; \
           grep -oE '^\s*-?\s*`?(\./|\.\./|okb/)[^` ]+' "$DIR/RESOURCES.md" | sed 's/^\s*-?\s*`//')
  # stale course-local okb pointers (should be ../../okb/ after migration)
  if grep -qE '(\[|\()`?okb/' "$DIR/RESOURCES.md" && [ ! -d "$DIR/okb" ]; then
    echo "FAIL RESOURCES has course-local okb/ pointers but no $DIR/okb — rewrite to ../../okb/"
    fails=$((fails+1))
  fi
else
  echo "FAIL no RESOURCES.md in $DIR"; fails=$((fails+1))
fi

# lessons: every ../assets/ href resolves through the symlink
while IFS= read -r ref; do
  lesson="${ref%%::*}"; asset="${ref#*::}"
  check "$lesson → $asset" "$DIR/lessons/$(dirname "$lesson")/$asset"
done < <(find "$DIR/lessons" -name '*.html' -printf '%P\n' 2>/dev/null | while IFS= read -r l; do
  grep -oE '(href|src)="(\.\./)*assets/[^"]+"' "$DIR/lessons/$l" 2>/dev/null | sed 's/^[a-z]*="//;s/"$//' | sed "s|^|$l::|"
done)

[ "$fails" -eq 0 ] && echo "ALL PASS" || echo "$fails FAILURE(S)"
exit $((fails > 0))
