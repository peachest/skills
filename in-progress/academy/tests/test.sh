#!/usr/bin/env bash
# tests/test.sh — smoke test: fake academy + herdr stub replaying fixtures.
#   bash tests/test.sh  (from the academy skill dir) → exit 0 = green
set -uo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fails=0
ok() { echo "PASS $1"; }
bad() { echo "FAIL $1"; fails=$((fails+1)); }

# --- stub herdr: replay fixture JSON per subcommand ---
cat > "$TMP/herdr-stub" <<STUB
#!/usr/bin/env bash
case "\$1 \$2" in
  "tab create") cat "$SKILL_DIR/scripts/fixtures/tab-create.json" ;;
  "agent start") cat "$SKILL_DIR/scripts/fixtures/agent-start.json" ;;
  "agent prompt") cat "$SKILL_DIR/scripts/fixtures/agent-prompt.json" ;;
  "agent list") cat "$SKILL_DIR/scripts/fixtures/agent-list.json" ;;
  *) echo "stub: unhandled \$*" >&2; exit 9 ;;
esac
STUB
chmod +x "$TMP/herdr-stub"

# --- scaffold on a fake academy ---
mkdir -p "$TMP/academy/assets"
echo "# Curriculum" > "$TMP/academy/CURRICULUM.md"
echo "| course | dir | status | deps |" >> "$TMP/academy/CURRICULUM.md"
echo "|---|---|---|---|" >> "$TMP/academy/CURRICULUM.md"
bash "$SKILL_DIR/scripts/scaffold-course.sh" "$TMP/academy" demo --namespace demo-ns > "$TMP/scaffold.out" 2>&1 \
  && ok "scaffold runs" || { bad "scaffold runs"; cat "$TMP/scaffold.out"; }
[ -L "$TMP/academy/courses/demo/assets" ] && ok "assets symlink" || bad "assets symlink"
[ -f "$TMP/academy/courses/demo/MISSION.md" ] && ok "MISSION" || bad "MISSION"
grep -q "demo" "$TMP/academy/CURRICULUM.md" && ok "CURRICULUM registered" || bad "CURRICULUM registered"
# idempotence guard
bash "$SKILL_DIR/scripts/scaffold-course.sh" "$TMP/academy" demo --namespace x >/dev/null 2>&1 \
  && bad "re-scaffold refused" || ok "re-scaffold refused"

# --- verify-links: good state, then broken pointer ---
echo "see [notes](../../okb/demo-ns/x.md) and \`../../assets/y.css\`" > "$TMP/academy/courses/demo/RESOURCES.md"
mkdir -p "$TMP/academy/okb/demo-ns" "$TMP/academy/courses/demo/lessons" "$TMP/academy/assets"
touch "$TMP/academy/okb/demo-ns/x.md" "$TMP/academy/assets/y.css" "$TMP/academy/assets/z.js"
printf '<a href="../assets/z.js"></a>' > "$TMP/academy/courses/demo/lessons/l1.html"
bash "$SKILL_DIR/scripts/verify-course-links.sh" "$TMP/academy/courses/demo" > "$TMP/v1.out" 2>&1
grep -q "ALL PASS" "$TMP/v1.out" && ok "verify green on good tree" || { bad "verify green on good tree"; cat "$TMP/v1.out"; }
rm "$TMP/academy/okb/demo-ns/x.md"
bash "$SKILL_DIR/scripts/verify-course-links.sh" "$TMP/academy/courses/demo" > "$TMP/v2.out" 2>&1
[ $? -ne 0 ] && grep -q "x.md" "$TMP/v2.out" && ok "verify red on broken pointer" || { bad "verify red on broken pointer"; cat "$TMP/v2.out"; }

# --- spawn-course against the stub ---
out=$(HERDR_BIN="$TMP/herdr-stub" bash "$SKILL_DIR/scripts/spawn-course.sh" "$TMP/academy" demo 2>&1)
echo "$out" | grep -q "teach-demo tab=w1B:t8 pane=w1B:p9 status=idle prompt=sent" \
  && ok "spawn-course end-to-end" || { bad "spawn-course end-to-end"; echo "$out"; }
echo "$out" | grep -q -- "--wait" && bad "must not mention --wait as used" || ok "no --wait in output"
HERDR_BIN="$TMP/herdr-stub" bash "$SKILL_DIR/scripts/spawn-course.sh" a b --list | grep -q "w1:p2\|agents" \
  && ok "spawn-course --list" || bad "spawn-course --list"

[ "$fails" -eq 0 ] && echo "ALL GREEN" || echo "$fails FAILURE(S)"
exit $((fails > 0))
