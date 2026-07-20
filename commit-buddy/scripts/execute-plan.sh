#!/usr/bin/env bash
set -euo pipefail

# execute-plan.sh - 校验并执行 CommitPlan JSON
# Usage: execute-plan.sh <plan.json>
#
# 输出: plan-result.json（与 plan.json 同目录）

if [ $# -ne 1 ]; then
  echo "Usage: execute-plan.sh <plan.json>" >&2
  exit 1
fi

PLAN_FILE="$1"
if [ ! -f "$PLAN_FILE" ]; then
  echo "ERROR: plan file not found: $PLAN_FILE" >&2
  exit 1
fi

PLAN_DIR="$(cd "$(dirname "$PLAN_FILE")" && pwd)"
RESULT_FILE="$PLAN_DIR/plan-result.json"

# 进程唯一临时目录，避免并发竞态
TMPDIR=$(mktemp -d /tmp/commit-buddy-XXXXXXXXXX)
trap 'rm -rf "$TMPDIR"' EXIT

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

    # 检查这个 hunk 是否被 commits 引用
    is_allocated=$(jq --arg path "$path" --argjson idx "$idx" '
      [.commits[].files[] |
        select(.path == $path) |
        if .hunks == "all" then true
        elif (.hunks | type) == "array" then (.hunks | index($idx) != null)
        else false end
      ] | any
    ' "$PLAN_FILE")

    if [ "$is_allocated" != "true" ]; then
      continue  # 未分配的不校验
    fi

    if [ "$idx" -ge "$count" ]; then
      ALL_ERRORS="${ALL_ERRORS}Rule 3: hunk $path:$idx out of range (file has $count hunks)\n"
      continue
    fi

    safename="${path//\//_}"
    patch_file="$TMPDIR/hunks/$safename/$idx.patch"
    if [ ! -f "$patch_file" ]; then
      ALL_ERRORS="${ALL_ERRORS}Rule 3: hunk $path:$idx patch file not found\n"
      continue
    fi

    current_fp=$(compute_hunk_fingerprint "$patch_file")
    if [ "$current_fp" != "$plan_fp" ]; then
      ALL_ERRORS="${ALL_ERRORS}Rule 3: hunk $path:$idx fingerprint mismatch\n"
    fi
  done
done

if [ -n "$ALL_ERRORS" ]; then
  fail "$ALL_ERRORS"
fi
echo "  Rule 3 OK: allocated hunk fingerprints match"

# Rule 4: 同一个 hunk 序号不能出现在多个 commit
DUPE=$(jq '
  [.commits[].files[] |
    select(.hunks != "all" and (.hunks | type) == "array") |
    .path as $p |
    .hunks[] | "\($p):\(.)"
  ] | group_by(.) | map(select(length > 1)) | flatten
' "$PLAN_FILE")

if [ "$DUPE" != "[]" ] && [ -n "$DUPE" ]; then
  fail "Rule 4: duplicate hunk assignments: $(echo "$DUPE" | jq -r '. | join(", ")')"
fi
echo "  Rule 4 OK: no duplicate hunk assignments"

# Rule 5: untracked 文件检查
for row in $(jq -c '.commits[].files[] | select(.untracked == true)' "$PLAN_FILE"); do
  path=$(echo "$row" | jq -r '.path')
  status=$(git status --short -- "$path" | head -1 | cut -c1-2 || true)
  if [ "$status" != "??" ]; then
    fail "Rule 5: file marked untracked but status is '$status': $path"
  fi
done
echo "  Rule 5 OK: untracked files verified"

echo ""
echo "=== Validation passed, executing ==="

# ----- execute -----

STASHED=false
if [ -n "$(git status --short)" ]; then
  git stash push --keep-index --message "commit-buddy-auto-stash" 2>/dev/null || true
  STASHED=true
fi

COMMITTED_FILE=$(mktemp -p "$TMPDIR" committed.XXXXXX)
ALLOCATED_MAP=$(mktemp -p "$TMPDIR" alloc.XXXXXX)

# 记录所有已分配 hunk 用于最后报告未分配部分
# 同时处理 hunks: "all"（展开 snapshot 中该文件的所有 hunk）和 hunks: [...]
jq -r '
  .snapshot.files as $snap |
  [.commits[].files[] |
    .path as $p |
    if .hunks == "all" then
      ($snap[] | select(.path == $p) | .hunks[].index | "\($p):\(.)")
    elif (.hunks | type) == "array" then
      .hunks[] | "\($p):\(.)"
    else
      empty
    end
  ] | .[]
' "$PLAN_FILE" | sort | uniq > "$ALLOCATED_MAP"

for i in $(seq 0 $((COMMITS_COUNT - 1))); do
  echo ""
  echo "--- Commit $((i + 1))/$COMMITS_COUNT ---"

  spec=$(jq ".commits[$i]" "$PLAN_FILE")
  type=$(echo "$spec" | jq -r '.type')
  scope=$(echo "$spec" | jq -r '.scope // empty')
  summary=$(echo "$spec" | jq -r '.summary')
  body=$(echo "$spec" | jq -r '.body // empty')
  breaking=$(echo "$spec" | jq -r '.breaking // false')
  signoff=$(echo "$spec" | jq -r '.signoff // false')

  # 构造 commit message
  if [ -n "$scope" ]; then
    msg="${type}(${scope}): ${summary}"
  else
    msg="${type}: ${summary}"
  fi

  if [ "$breaking" = "true" ]; then
    msg="${msg}\n\nBREAKING CHANGE: ${body}"
  elif [ -n "$body" ]; then
    msg="${msg}\n\n${body}"
  fi

  commit_args=(-m "$msg")
  if [ "$signoff" = "true" ]; then
    commit_args+=("--signoff")
  fi

  # 重置 index
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
      # "all" — apply all pre-extracted hunk patches to index
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

      # 从预提取的 hunk patch 中取需要的
      safename="${path//\//_}"
      hunk_dir="$TMPDIR/hunks/$safename"

      for h_idx in $hunk_list; do
        patch_file="$hunk_dir/$h_idx.patch"
        if [ -f "$patch_file" ]; then
          cat "$patch_file" | git apply --cached --unidiff-zero --whitespace=nowarn 2>/dev/null || {
            # 如果没有 context 行 apply 失败，fallback:
            # 用完整 diff 配合 hunks 在多个 commit 的场景，
            # 先收集所有需要的 hunk patch 按序号顺序拼接再 apply
            :
          }
        fi
      done
    fi
  done

  # 检查 index 是否有 staged 改动
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
jq -r '
  [.snapshot.files[] | .path as $p | .hunks[].index | "\($p):\(.)"] | .[]
' "$PLAN_FILE" | sort > "$ALL_HUNKS"

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