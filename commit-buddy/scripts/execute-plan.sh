#!/usr/bin/env bash
set -euo pipefail

# execute-plan.sh - 校验并执行 CommitPlan JSON
# Usage: execute-plan.sh <plan.json>
# 输出: <PROJECT_DIR>/.pi/commit-buddy/result.json

if [ $# -ne 1 ]; then
  echo "Usage: execute-plan.sh <plan.json>" >&2
  exit 1
fi

PLAN_FILE="$1"
[ -f "$PLAN_FILE" ] || { echo "ERROR: file not found: $PLAN_FILE" >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

PLAN_DIR="$(cd "$(dirname "$PLAN_FILE")" && pwd)"
RESULT_FILE="$PLAN_DIR/result.json"

TMPDIR=$(mktemp -d /tmp/commit-buddy-exec-XXXXXXXXXX)
trap 'rm -rf "$TMPDIR"' EXIT

HEAD_SHA=$(git rev-parse HEAD)
COMMITS_COUNT=$(jq '.commits | length' "$PLAN_FILE")

# ----- 校验前提取所有文件 hunk（供 Rule 3 用） -----

declare -A HUNK_COUNTS

for row in $(jq -c '.snapshot.files[]' "$PLAN_FILE"); do
  path=$(echo "$row" | jq -r '.path')
  count=$(echo "$row" | jq '.hunks | length')
  if [ "$count" -gt 0 ]; then
    extract_hunks "$path" "$TMPDIR" hcount
    HUNK_COUNTS["$path"]=$hcount
  else
    HUNK_COUNTS["$path"]=0
  fi
done

# ----- helpers -----

fail() {
  cat > "$RESULT_FILE" <<-JSON
{
  "ok": false,
  "commits": [],
  "errors": ["$1"]
}
JSON
  exit 1
}

# 从 git diff 输出中提取所有 hunk 的独立 patch 文件。
# 跳过 diff header（diff --git, index, ---, +++ 等），
# 每个 hunk 从 @@ 行开始，包含完整上下文到下一个 @@ 行之前或文件尾。
# 输出: 写入 $TMPDIR/hunks/<filepath>/<idx>.patch
# 输出: 全局数组 HUNK_COUNTS["<path>"] = hunk 数量
extract_hunks() {
  local path="$1"
  local safename="${path//\//_}"   # / → _ 用于文件名
  local hunk_dir="$TMPDIR/hunks/$safename"
  mkdir -p "$hunk_dir"

  local infile="$TMPDIR/diff-$safename.diff"
  # --no-pager 避免 delta/color 等格式化器污染原始 diff 格式
  git --no-pager diff HEAD -- "$path" > "$infile" 2>/dev/null || true

  if [ ! -s "$infile" ]; then
    # 可能是未跟踪文件，无 diff
    HUNK_COUNTS["$path"]=0
    return
  fi

  local idx=0
  local outfile=""
  local in_hunk=false

  while IFS= read -r line; do
    case "$line" in
      *"@@"*"-"*","*"+"*)
        # 新 hunk 开始，关闭上一个
        if [ "$in_hunk" = true ] && [ -n "$outfile" ]; then
          echo "--- a/$path" > "$outfile.tmp"
          echo "+++ b/$path" >> "$outfile.tmp"
          cat "$outfile" >> "$outfile.tmp"
          mv "$outfile.tmp" "$outfile"
        fi
        outfile="$hunk_dir/$idx.patch"
        printf '%s\n' "$line" > "$outfile"
        in_hunk=true
        idx=$((idx + 1))
        ;;
      *)
        if [ "$in_hunk" = true ] && [ -n "$outfile" ]; then
          printf '%s\n' "$line" >> "$outfile"
        fi
        # diff header 行（diff --git, index, ---, +++）在被 @@ 之前的行直接跳过
        ;;
    esac
  done < "$infile"

  # 关闭最后一个 hunk
  if [ "$in_hunk" = true ] && [ -n "$outfile" ]; then
    echo "--- a/$path" > "$outfile.tmp"
    echo "+++ b/$path" >> "$outfile.tmp"
    cat "$outfile" >> "$outfile.tmp"
    mv "$outfile.tmp" "$outfile"
  fi

  HUNK_COUNTS["$path"]=$idx
}

# 计算一个 hunk patch 文件的 SHA256 指纹（完整内容）
compute_hunk_fingerprint() {
  local patch_file="$1"
  sha256sum "$patch_file" | cut -d' ' -f1
}

# ----- parse plan -----

COMMITS_COUNT=$(jq '.commits | length' "$PLAN_FILE")
HEAD_SHA=$(git rev-parse HEAD)

# 预提取所有文件 hunks（验证和应用共用）
declare -A HUNK_COUNTS

for row in $(jq -c '.snapshot.files[]' "$PLAN_FILE"); do
  path=$(echo "$row" | jq -r '.path')
  hunk_count=$(echo "$row" | jq '.hunks | length')

  if [ "$hunk_count" -eq 0 ]; then
    # 未跟踪文件或新文件，无 diff
    HUNK_COUNTS["$path"]=0
  else
    extract_hunks "$path"
  fi
done

# ----- validation -----

echo "=== Validation ==="

# Rule 1: 每个 path 必须在工作区存在
for row in $(jq -c '.snapshot.files[]' "$PLAN_FILE"); do
  path=$(echo "$row" | jq -r '.path')
  if [ ! -f "$path" ]; then
    fail "Rule 1: file not found: $path"
  fi
done
echo "  Rule 1 OK: all files exist"

# Rule 2: 每个文件的 HEAD sha 一致
for row in $(jq -c '.snapshot.files[]' "$PLAN_FILE"); do
  path=$(echo "$row" | jq -r '.path')
  plan_head=$(echo "$row" | jq -r '.head_sha')
  if [ -n "$plan_head" ] && [ "$plan_head" != "$HEAD_SHA" ]; then
    fail "Rule 2: HEAD has changed for $path (plan: $plan_head, actual: $HEAD_SHA)"
  fi
done
echo "  Rule 2 OK: HEAD unchanged ($HEAD_SHA)"

# Rule 3: 已分配 hunk 的 fingerprint 一致
ALL_ERRORS=""

for row in $(jq -c '.snapshot.files[]' "$PLAN_FILE"); do
  path=$(echo "$row" | jq -r '.path')
  count="${HUNK_COUNTS[$path]:-0}"

  for hunk_row in $(echo "$row" | jq -c '.hunks[]'); do
    idx=$(echo "$hunk_row" | jq '.index')
    plan_fp=$(echo "$hunk_row" | jq -r '.fingerprint_sha256')

    is_allocated=$(jq --arg path "$path" --argjson idx "$idx" '
      [.commits[].files[] |
        select(.path == $path) |
        if .hunks == "all" then true
        elif (.hunks | type) == "array" then (.hunks | index($idx) != null)
        else false end
      ] | any
    ' "$PLAN_FILE")

    [ "$is_allocated" != "true" ] && continue

    [ "$idx" -ge "$count" ] && { ALL_ERRORS="${ALL_ERRORS}Rule 3: hunk $path:$idx out of range (file has $count hunks)\n"; continue; }

    safename="${path//\//_}"
    patch_file="$TMPDIR/hunks/$safename/$idx.patch"
    [ ! -f "$patch_file" ] && { ALL_ERRORS="${ALL_ERRORS}Rule 3: hunk $path:$idx patch file not found\n"; continue; }

    current_fp=$(compute_hunk_fingerprint "$patch_file")
    [ "$current_fp" != "$plan_fp" ] && { ALL_ERRORS="${ALL_ERRORS}Rule 3: hunk $path:$idx fingerprint mismatch\n"; }
  done
done

[ -n "$ALL_ERRORS" ] && fail "$ALL_ERRORS"
echo "  Rule 3 OK"

DUPE=$(jq '
  [.commits[].files[] |
    select(.hunks != "all" and (.hunks | type) == "array") |
    .path as $p | .hunks[] | "\($p):\(.)"
  ] | group_by(.) | map(select(length > 1)) | flatten
' "$PLAN_FILE")
[ "$DUPE" != "[]" ] && [ -n "$DUPE" ] && fail "Rule 4: duplicate hunk assignments: $(echo "$DUPE" | jq -r '. | join(", ")')"
echo "  Rule 4 OK"

for row in $(jq -c '.commits[].files[] | select(.untracked == true)' "$PLAN_FILE"); do
  path=$(echo "$row" | jq -r '.path')
  status=$(git status --short -- "$path" | head -1 | cut -c1-2 || true)
  [ "$status" != "??" ] && fail "Rule 5: file marked untracked but status is '$status': $path"
done
echo "  Rule 5 OK"

echo ""
echo "=== Validation passed, executing ==="

# ----- execute -----

STASHED=false
[ -n "$(git status --short)" ] && {
  git stash push --keep-index --message "commit-buddy-auto-stash" 2>/dev/null || true
  STASHED=true
}

COMMITTED_FILE=$(mktemp -p "$TMPDIR" committed.XXXXXX)
ALLOCATED_MAP=$(mktemp -p "$TMPDIR" alloc.XXXXXX)

jq -r '
  .snapshot.files as $snap |
  [.commits[].files[] |
    .path as $p |
    if .hunks == "all" then
      ($snap[] | select(.path == $p) | .hunks[].index | "\($p):\(.)")
    elif (.hunks | type) == "array" then
      .hunks[] | "\($p):\(.)"
    else empty end
  ] | .[]
' "$PLAN_FILE" | sort | uniq > "$ALLOCATED_MAP"

for i in $(seq 0 $((COMMITS_COUNT - 1))); do
  echo "--- Commit $((i + 1))/$COMMITS_COUNT ---"

  spec=$(jq ".commits[$i]" "$PLAN_FILE")
  type=$(echo "$spec" | jq -r '.type')
  scope=$(echo "$spec" | jq -r '.scope // empty')
  summary=$(echo "$spec" | jq -r '.summary')
  body=$(echo "$spec" | jq -r '.body // empty')
  breaking=$(echo "$spec" | jq -r '.breaking // false')
  signoff=$(echo "$spec" | jq -r '.signoff // false')

  msg="${type}${scope:+($scope)}: ${summary}"
  [ "$breaking" = "true" ] && msg="${msg}\n\nBREAKING CHANGE: ${body}" || [ -n "$body" ] && msg="${msg}\n\n${body}"

  commit_args=(-m "$msg")
  [ "$signoff" = "true" ] && commit_args+=("--signoff")

  git reset HEAD > /dev/null 2>&1 || true

  file_count=$(echo "$spec" | jq '.files | length')
  for j in $(seq 0 $((file_count - 1))); do
    fspec=$(echo "$spec" | jq ".files[$j]")
    path=$(echo "$fspec" | jq -r '.path')
    untracked=$(echo "$fspec" | jq -r '.untracked // false')
    hunks=$(echo "$fspec" | jq -r '.hunks | type' 2>/dev/null || echo "string")

    if [ "$untracked" = "true" ]; then
      echo "  git add $path (untracked)"
      git add "$path"
      continue
    fi

    if [ "$hunks" = "string" ]; then
      # hunks: "all" — apply all pre-extracted patches
      echo "  apply all hunks for $path"
      safename="${path//\//_}"
      hunk_dir="$TMPDIR/hunks/$safename"
      if [ -d "$hunk_dir" ]; then
        for patch_file in "$hunk_dir"/*.patch; do
          [ -f "$patch_file" ] && cat "$patch_file" | git apply --cached --unidiff-zero --whitespace=nowarn 2>/dev/null || true
        done
      fi
    else
      hunk_list=$(echo "$fspec" | jq -r '.hunks[]')
      echo "  $path hunks: $(echo "$hunk_list" | tr '\n' ' ')"

      safename="${path//\//_}"
      hunk_dir="$TMPDIR/hunks/$safename"
      for h_idx in $hunk_list; do
        patch_file="$hunk_dir/$h_idx.patch"
        [ -f "$patch_file" ] && cat "$patch_file" | git apply --cached --unidiff-zero --whitespace=nowarn 2>/dev/null || true
      done
    fi
  done

  if [ -z "$(git diff --cached --stat)" ]; then
    echo "  WARNING: no changes staged for commit, skipping"
    continue
  fi

  git commit "${commit_args[@]}"

  sha=$(git rev-parse HEAD)
  jq -n --arg sha "$sha" --arg msg "$msg" '{sha: $sha, message: $msg}' >> "$COMMITTED_FILE"
  echo "  committed: $sha"
done

# ----- stash pop -----
STASH_POP_OK=true
STASH_CONFLICTS=""

if [ "$STASHED" = "true" ]; then
  stash_pop_output=$(git stash pop 2>&1 || true)
  if echo "$stash_pop_output" | grep -qi "conflict"; then
    STASH_POP_OK=false
    STASH_CONFLICTS=$(echo "$stash_pop_output" |
      grep -oP '(?<=both modified: |both added: |deleted by us: |deleted by them: |added by us: |added by them: ).*' |
      paste -sd ',' -)
  fi
fi

# ----- 收集未分配 hunk -----
ALL_HUNKS=$(mktemp -p "$TMPDIR" all.XXXXXX)
jq -r '[.snapshot.files[] | .path as $p | .hunks[].index | "\($p):\(.)"] | .[]' "$PLAN_FILE" | sort > "$ALL_HUNKS"

UNALLOCATED_RESULT=$(comm -23 "$ALL_HUNKS" "$ALLOCATED_MAP" 2>/dev/null |
  head -20 |
  while IFS= read -r line; do
    if [ -n "$line" ]; then
      path="${line%%:*}"
      idx="${line##*:}"
      echo "{\"path\":\"$path\",\"hunks\":[$idx]}"
    fi
  done | jq -s '.' 2>/dev/null || echo "[]")

# ----- 输出 PlanResult -----

COMMITTED_JSON=$(jq -s '.' "$COMMITTED_FILE" 2>/dev/null || echo "[]")

jq -n \
  --argjson ok true \
  --argjson commits "$COMMITTED_JSON" \
  --argjson unallocated "$UNALLOCATED_RESULT" \
  --argjson stash_pop_ok "$STASH_POP_OK" \
  --arg stash_conflicts "${STASH_CONFLICTS:-}" \
  '{
    ok: $ok,
    commits: $commits,
    unallocated_hunks: $unallocated,
    stash_pop_ok: $stash_pop_ok
  }
  + if $stash_conflicts != "" then {stash_conflicts: [$stash_conflicts]} else {} end
  ' > "$RESULT_FILE"

echo ""
echo "=== Done ==="
echo "Result: $RESULT_FILE"
jq '.' "$RESULT_FILE"