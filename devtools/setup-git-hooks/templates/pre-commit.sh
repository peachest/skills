#!/bin/bash
# pre-commit: 秒级检查，只看 staged 内容（git show :file，而非工作区文件，
# 保证 git add -p 部分暂存时检查的就是将要提交的内容）。
# 重检查（lint/test）在 pre-push；commit 信息格式校验在 commit-msg——本文件不重复。
# 凭证扫描请另装 gitleaks 并在此追加（除 gofmt/clang-format 工具链外零其他依赖、不内置任何扫描器；工具未装时对应检查会误报并拦截，r14 no117）

set -euo pipefail   # 入口自行声明（common.sh 不带副作用）；本钩子全部检查为 if/exit 结构，-e 可安全兜住未来新增检查的未防护失败
SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh"; exit 1; }

cd "$(git rev-parse --show-toplevel)" || exit 1

fail=0

# staged 内容先落临时文件再检查（r16 no165/no167）：命令替换剥尾换行、$( ) 丢 NUL、
# 且 git show 失败在管道/进程替换里会被静默吞掉（fail-open）——两条链路统一为
# fail-loud：读取失败即拦截，不再依赖 diff 双空判等
fmt_tmp=$(mktemp) || { echo "错误: 无法创建临时文件" >&2; exit 1; }
trap 'rm -f "$fmt_tmp" "$fmt_tmp.fmt"' EXIT   # .fmt 副文件一并清理（r18 no185）
# 文件清单先取再校验退出码：进程替换吞退出码会让 git 失败时静默跳过全部检查
# （fail-open 与本文件 fail-loud 原则矛盾，r18 no188）。
# 已知限制（r18 no187，同 install.sh 口径）：按行解析无法表示含换行的文件名；
# --no-renames（r18 no186）：rename 检测下 R 状态对被本过滤器整体排除，禁用后退化为
# D+A、新路径以 A 纳入检查；typechange（file<->symlink）仍不在检查范围
if ! files_go=$(git diff --cached --name-only --no-renames --diff-filter=ACM -- '*.go'); then
    log_error "无法读取 staged 文件清单（索引不可用？）"
    exit 1
fi
if ! files_c=$(git diff --cached --name-only --no-renames --diff-filter=ACM -- '*.c' '*.h'); then
    log_error "无法读取 staged 文件清单（索引不可用？）"
    exit 1
fi

# 工具链预检（r18 no184）：保持 fail-closed，但区分"工具缺失"与"格式不通过"——
# 缺工具时提示装工具或 --no-verify，而非误导性的"运行 make fmt"
go_files=$(printf '%s\n' "$files_go" | grep -c . || true)
c_files=$(printf '%s\n' "$files_c" | grep -c . || true)
if [ "${go_files:-0}" -gt 0 ] && ! command -v gofmt >/dev/null; then
    log_error "gofmt 未安装（staged 含 .go 文件）——请安装 Go 工具链，或 git commit --no-verify 跳过本次检查"
    exit 1
fi
if [ "${c_files:-0}" -gt 0 ] && ! command -v clang-format >/dev/null; then
    log_error "clang-format 未安装（staged 含 .c/.h 文件）——请安装 clang-format，或 git commit --no-verify 跳过本次检查"
    exit 1
fi

# 1. staged Go 文件 → gofmt 检查
while IFS= read -r f; do
    [ -z "$f" ] && continue
    if ! git show ":$f" > "$fmt_tmp" 2>/dev/null; then
        log_error "无法读取 staged 内容: $f（索引并发修改？请重新 git add）"
        fail=1
        continue
    fi
    if ! gofmt "$fmt_tmp" > "$fmt_tmp.fmt" 2>/dev/null || ! diff -q "$fmt_tmp" "$fmt_tmp.fmt" >/dev/null 2>&1; then
        log_error "gofmt 不通过: $f"
        gofmt "$fmt_tmp" 2>&1 | diff "$fmt_tmp" - 2>/dev/null | head -5 | sed 's/^/  /' >&2   # 差异摘要（r18 no189）
        fail=1
    fi
done <<< "$files_go"

# 2. staged C 文件 → clang-format 检查
while IFS= read -r f; do
    [ -z "$f" ] && continue
    # 同 Go 链路口径（r16 no167）：失败 fail-loud；临时文件保字节原样（r16 no165）
    if ! git show ":$f" > "$fmt_tmp" 2>/dev/null; then
        log_error "无法读取 staged 内容: $f（索引并发修改？请重新 git add）"
        fail=1
        continue
    fi
    if ! cf_err=$(clang-format --dry-run --Werror --assume-filename="$f" "$fmt_tmp" 2>&1); then
        log_error "clang-format 不通过: $f"
        printf '%s\n' "$cf_err" | head -5 | sed 's/^/  /' >&2   # 诊断摘要（r18 no189）
        fail=1
    fi
done <<< "$files_c"

if [ "$fail" -ne 0 ]; then
    log_error "请运行 make fmt 后重新 git add。"
    exit 1
fi

# 3. 空白符检查（行尾空白、tab/space 混用等，遵循 core.whitespace 配置）
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    against=HEAD
else
    against=$(git hash-object -t tree /dev/null)
fi
if ! git diff-index --check --cached "$against" --; then
    log_error "存在空白字符错误（行尾空白 / 缩进混用）。"
    exit 1
fi

log_info "pre-commit 检查通过。"
