#!/usr/bin/env bash
# common.sh - commit-buddy 脚本共享的 hunk 提取逻辑
# 被 generate-plan.sh 和 execute-plan.sh source

# 从 git diff 输出中提取所有 hunk 的独立 patch 文件。
# 跳过 diff header（diff --git, index, ---, +++ 等），
# 每个 hunk 从 @@ 行开始，包含完整上下文到下一个 @@ 行之前或文件尾。
#
# 参数:
#   $1: path — 文件路径
#   $2: tmpdir — 临时目录根
#   $3: outvar — 用于回传 hunk 数量的变量名
#
# 副作用:
#   在 $TMPDIR/hunks/<safename>/ 下生成 <idx>.patch 文件
#   每个 patch 文件包含 --- a/<path> / +++ b/<path> 头 + hunk 内容
extract_hunks() {
  local path="$1"
  local tmpdir="$2"
  local outvar="$3"
  local safename="${path//\//_}"
  local hunk_dir="$tmpdir/hunks/$safename"
  mkdir -p "$hunk_dir"

  local infile="$tmpdir/diff-$safename.diff"
  git --no-pager diff HEAD -- "$path" > "$infile" 2>/dev/null || true

  if [ ! -s "$infile" ]; then
    printf '%s' 0 > "$tmpdir/count-$safename"
    eval "$outvar=0"
    return
  fi

  local idx=0
  local outfile=""
  local in_hunk=false

  while IFS= read -r line; do
    case "$line" in
      *"@@"*"-"*","*"+"*)
        if [ "$in_hunk" = true ] && [ -n "$outfile" ]; then
          _close_hunk "$outfile" "$path"
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
        ;;
    esac
  done < "$infile"

  if [ "$in_hunk" = true ] && [ -n "$outfile" ]; then
    _close_hunk "$outfile" "$path"
  fi

  eval "$outvar=$idx"
}

# 关闭一个 hunk patch：在内容前补上 --- / +++ 头
_close_hunk() {
  local outfile="$1"
  local path="$2"
  echo "--- a/$path" > "${outfile}.tmp"
  echo "+++ b/$path" >> "${outfile}.tmp"
  cat "$outfile" >> "${outfile}.tmp"
  mv "${outfile}.tmp" "$outfile"
}

# 计算一个文件的 SHA256 指纹
# 参数: $1 = patch 文件路径
# 输出: SHA256 哈希值（无文件名）
compute_hunk_fingerprint() {
  sha256sum "$1" | cut -d' ' -f1
}