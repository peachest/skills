#!/bin/bash
# pre-commit: 秒级检查，只看 staged 内容（git show :file，而非工作区文件，
# 保证 git add -p 部分暂存时检查的就是将要提交的内容）。
# 重检查（lint/test）在 pre-push；commit 信息格式校验在 commit-msg——本文件不重复。
# 凭证扫描请另装 gitleaks 并在此追加（除 gofmt/clang-format 工具链外零其他依赖、不内置任何扫描器；工具缺失/版本过旧由下方预检拦截并给出指引，r14 no117/r20 no222）

set -euo pipefail   # 入口自行声明（common.sh 不带副作用）；本钩子全部检查为 if/exit 结构，-e 可安全兜住未来新增检查的未防护失败
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"   # cd+pwd -P 可移植（r12 no81/r19 no208/r23 no271：省 basename 往返）；不解析 $0 符号链接——install.sh 以 hooksPath 直指仓内目录
source "$SCRIPT_DIR/common.sh" || { echo "无法加载 common.sh" >&2; exit 1; }

cd "$(git rev-parse --show-toplevel)" || exit 1

fail=0
read_fail=0   # 读取失败与格式失败分列，末尾提示按因区分（r19 no209/r26 no17）
fmt_fail=0

# staged 内容先落临时文件再检查（r16 no165/no167）：命令替换剥尾换行、$( ) 丢 NUL、
# 且 git show 失败在管道/进程替换里会被静默吞掉（fail-open）——两条链路统一为
# fail-loud：读取失败即拦截，不再依赖 diff 双空判等
fmt_tmp=$(mktemp) || { echo "错误: 无法创建临时文件" >&2; exit 1; }
trap 'rm -f "$fmt_tmp"' EXIT   # 第一个文件创建即挂清理（r22 no252：消除后续 mktemp 失败的泄漏窗口）
fmt_out=$(mktemp) || { echo "错误: 无法创建临时文件" >&2; exit 1; }   # 0600 副文件（r20 no220：重定向创建为 644 且有 symlink 竞争窗口）
list_go=$(mktemp) || { echo "错误: 无法创建临时文件" >&2; exit 1; }
list_c=$(mktemp) || { echo "错误: 无法创建临时文件" >&2; exit 1; }
trap 'rm -f "$fmt_tmp" "$fmt_out" "$list_go" "$list_c"' EXIT   # 兜底清理
trap 'rm -f "$fmt_tmp" "$fmt_out" "$list_go" "$list_c"; exit 130' INT TERM HUP   # 信号清理后显式退出（r20 no220/r21 no236）
# 文件清单先取再校验退出码：进程替换吞退出码会让 git 失败时静默跳过全部检查
# （fail-open 与本文件 fail-loud 原则矛盾，r18 no188）。
# 已知限制（r18 no187，同 install.sh 口径）：按行解析无法表示含换行的文件名；
# --no-renames（r18 no186）：rename 检测下 R 状态对被本过滤器整体排除，禁用后退化为
# D+A、新路径以 A 纳入检查；typechange（file<->symlink）仍不在检查范围
# --raw 一次拿到模式列（r22 no249·perf medium：省去逐文件 ls-files 子进程）；
# 行格式：:100644 100644 <sha> <sha> M\t<path>。quotePath=off：非 ASCII 文件名按
# 字面输出，否则 git show 必失败（r19 no206）
# -z：路径原样输出（消除换行/引号/控制字符文件名限制，r24 no280·medium）；NUL 经
# 命令替换会丢，故直接落临时文件再解析
# --ita-visible-in-index：iTA（git add -N）条目默认对 diff --cached 不可见——
# 提交时却携带工作区内容，构成格式检查绕过（r26 no38·medium）；可见化后零 sha 走单列提示
if ! git diff --cached --raw -z --no-renames --ita-visible-in-index --diff-filter=ACM -- '*.go' > "$list_go"; then
    log_error "无法读取 staged 文件清单（索引不可用？）"
    exit 1
fi
if ! git diff --cached --raw -z --no-renames --ita-visible-in-index --diff-filter=ACM -- '*.c' '*.h' > "$list_c"; then
    log_error "无法读取 staged 文件清单（索引不可用？）"
    exit 1
fi

# 工具链预检（r18 no184）：保持 fail-closed，但区分"工具缺失"与"格式不通过"——
# 缺工具时提示装工具或 --no-verify，而非误导性的"运行 make fmt"
go_files=$(grep -c . "$list_go" || true)
c_files=$(grep -c . "$list_c" || true)
if [ "${go_files:-0}" -gt 0 ]; then
    if ! command -v gofmt >/dev/null; then
        log_error "gofmt 未安装（staged 含 .go 文件）——请安装 Go 工具链，或 git commit --no-verify 跳过本次检查"
        exit 1
    fi
    # 能力探测（r22 no250·medium，与 clang-format 探测对齐）：旧工具链遇新语法解析
    # 失败会被误诊为"WIP 语法错误"——预检时即区分
    # 泛型片段探测（r22 no250/r26 no18）：旧工具链不认识泛型语法，预检即暴露
    if ! printf 'package p\n\nfunc f[T any](x T) T { return x }\n' | gofmt -l >/dev/null 2>&1; then
        log_error "gofmt 不可用或版本过旧（不认识泛型语法，本仓需要 Go 1.18+ 工具链）"
        exit 1
    fi
fi
if [ "${c_files:-0}" -gt 0 ]; then
    if ! command -v clang-format >/dev/null; then
        log_error "clang-format 未安装（staged 含 .c/.h 文件）——请安装 clang-format，或 git commit --no-verify 跳过本次检查"
        exit 1
    fi
    # 能力探测（r20 no221·medium）：旧版（如 clang-format 3.4）不支持 --dry-run/--Werror，
    # 会把所有 .c/.h 稳定误报为"不通过"——预检阶段即区分
    if ! printf '' | clang-format --dry-run --Werror --assume-filename=a.c - >/dev/null 2>&1; then   # stdin 形态探测（r26 no42：/dev/null 输入绕过 --assume-filename 语义）
        log_error "clang-format 版本过旧或异常（不支持 --dry-run/--Werror）——请升级后重试"
        exit 1
    fi
fi

# 1. staged Go 文件 → gofmt 检查（-z 记录解析：meta\tpath，r22 no249/r24 no280）
while IFS= read -r -d '' meta && IFS= read -r -d '' f; do
    # -z 格式：meta 与 path 以 NUL 分隔（无 tab），交替成对出现
    [ -z "$meta" ] && continue
    newmode="${meta#* }"; newmode="${newmode%% *}"   # 纯 bash 取第二字段（新模式，r26 no2/no19/no41：省 awk 子进程）
    case "$newmode" in
        120000|160000) continue ;;   # symlink/gitlink（r21 no235）：show 输出目标路径/commit 内容，格式检查无意义且必误拦
    esac
    if ! git show ":$f" > "$fmt_tmp" 2>/dev/null; then
        log_error "无法读取 staged 内容: $f（索引并发修改？请重新 git add）"
        read_fail=1
        fail=1
        continue
    fi
    # 空内容单列（r26 no38·medium）：--ita-visible-in-index 下 iTA（git add -N）条目
    # 的 show 输出为空（空 blob）——空 .go/.c 无可检查内容，单列提示而非误诊"语法错误"
    # （真 0 字节文件同为该形态，提示覆盖两种情况）
    if [ ! -s "$fmt_tmp" ]; then
        log_error "staged 内容为空（intent-to-add？请 git add 完整内容）: $f"
        read_fail=1
        fail=1
        continue
    fi
    # 2>&1 在 > 之前：stderr 进命令替换、stdout 落文件（r21 no234·medium：原顺序把
    # stderr 一并写文件，gofmt_err 恒空，语法错误分支不可达）
    gofmt_err=$(gofmt "$fmt_tmp" 2>&1 > "$fmt_out") || true
    if [ -n "$gofmt_err" ]; then
        # 语法错误与格式差异区分（r20 no223）：make fmt 修不了语法错误
        log_error "gofmt 解析失败（语法错误/WIP 用 --no-verify；也可能是 Go 工具链过旧）: $f"   # 归因补充（r22 no250）
        fmt_fail=1
        printf '%s\n' "$gofmt_err" | head -5 | sed "s|$fmt_tmp|$f|g" | sed 's/^/  /' >&2 || true   # 路径替换（r26 no3）
        fail=1
    elif ! diff -q "$fmt_tmp" "$fmt_out" >/dev/null 2>&1; then
        log_error "gofmt 不通过: $f"
        fmt_fail=1
        # || true 兜底（r19 no204·medium）：diff 发现差异返回 1 + head 截断 SIGPIPE，
        # set -e 下会中止整个钩子、截断后续检查
        diff "$fmt_tmp" "$fmt_out" 2>/dev/null | head -5 | sed "s|$fmt_tmp|$f|g;s|$fmt_out|$f (formatted)|g" | sed 's/^/  /' >&2 || true   # 摘要 /tmp 路径换回真实文件名（r26 no3）
        fail=1
    fi
done < "$list_go"

# 2. staged C 文件 → clang-format 检查
while IFS= read -r -d '' meta && IFS= read -r -d '' f; do
    [ -z "$meta" ] && continue
    newmode="${meta#* }"; newmode="${newmode%% *}"   # 纯 bash（r26 no2/no19/no41）
    case "$newmode" in
        120000|160000) continue ;;   # symlink/gitlink（r21 no235）
    esac
    # 同 Go 链路口径（r16 no167）：失败 fail-loud；临时文件保字节原样（r16 no165）
    if ! git show ":$f" > "$fmt_tmp" 2>/dev/null; then
        log_error "无法读取 staged 内容: $f（索引并发修改？请重新 git add）"
        read_fail=1
        fail=1
        continue
    fi
    if ! cf_err=$(clang-format --dry-run --Werror --assume-filename="$f" "$fmt_tmp" 2>&1); then
        log_error "clang-format 不通过: $f"
        fmt_fail=1
        printf '%s\n' "$cf_err" | head -5 | sed 's/^/  /' >&2 || true   # 诊断摘要（r18 no189；head SIGPIPE 兜底 r19 no205）
        fail=1
    fi
done < "$list_c"

if [ "$fail" -ne 0 ]; then
    # 提示按失败原因区分（r19 no209）：读取失败应重新 add 而非 make fmt；
    # make fmt 只覆盖 hgml/ 范围，仓外 .c/.h 需手动格式化
    [ "${read_fail:-0}" = 1 ] && log_error "部分 staged 内容读取失败——请重新 git add 后重试。"
    [ "${fmt_fail:-0}" = 1 ] && log_error "存在格式不通过的文件——请运行 make fmt 后重新 git add（make fmt 仅覆盖 Go 与 hgml/*.h，其余 .c/.h 请手动 clang-format -i）。"
    exit 1
fi

# 3. 空白符检查（行尾空白、tab/space 混用等，遵循 core.whitespace 配置）。
# 排除 *.md（r26 no37·medium：行尾双空格是 Markdown 硬换行的合法语义，全量检查误拦）；
# .go/.c/.h 的空白已由上方格式检查覆盖（gofmt/clang-format 会规范化），本检查的
# 独立价值在其余文本文件（yaml/py/txt 等）
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    against=HEAD
else
    against=$(git hash-object -t tree /dev/null)
fi
ws_rc=0
git diff-index --check --cached "$against" -- . ':(exclude)*.md' || ws_rc=$?
if [ "$ws_rc" -ge 128 ]; then
    log_error "git diff-index --check 自身失败（rc=$ws_rc，索引锁/对象库损坏？）——非空白问题"   # 区分 git 故障（r26 no1）
    exit 1
elif [ "$ws_rc" -ne 0 ]; then
    log_error "存在空白字符错误（行尾空白 / 缩进混用；*.md 豁免——行尾双空格是硬换行）。"
    exit 1
fi

log_info "pre-commit 检查通过。"
