#!/usr/bin/env bash
# install.sh — 一次性安装：core.hooksPath 指向本目录。
# hook 内容随分支文件走（旧分支没有本目录时 hook 自动不生效，fail-open），
# 配置写 clone 级共享配置——配一次，主检出与全部 worktree 同时生效。
# 撤销：git config --unset core.hooksPath
# 信任模型（r15 no134，接入文档须同步声明）：hook 内容随检出分支变化——检出不受信
# 分支（外部 PR/fork）后其自带钩子会在下次 commit/push 自动执行。opt-out：WT_NO_HOOKS=1
# 仅拦截 wt pre-start；make setup 无条件安装，不可信环境请勿运行任一安装路径
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
cd "$root"

HOOKS_DIR="tools/git-hooks"   # 必须相对路径：core.hooksPath 相对值按各 worktree 根解析，
                               # 这是"hook 内容随分支走、旧分支 fail-open"的前提；改绝对路径会全 worktree 共享一份
# 不变式固化（r9 no e9dd）：绝对路径会静默改变语义（全 worktree 共享一份、旧分支 fail-open 失效）
case "$HOOKS_DIR" in /*) echo "错误: HOOKS_DIR 必须为相对路径（见上方注释），得到: $HOOKS_DIR" >&2; exit 1 ;; esac

# 目录缺失在旧分支是 fail-open 设计内场景（exit 0 + 提示）；
# 真实错误（hooksPath 写失败）才 exit 1
[ -d "$HOOKS_DIR" ] || { echo "提示: $HOOKS_DIR 不存在（旧分支无钩子目录属预期），跳过安装" >&2; exit 0; }

# 先授权钩子文件再写任何配置：任何失败都不改动 hooksPath（原子性，r15 no133）——
# 否则 chmod 失败后配置已落盘，git 会静默跳过无执行位的钩子（检查反而被关闭），
# 且提前退出会短路末尾的聚合诊断报告。保留 chmod 错误输出便于诊断（只读挂载/EACCES）
# 遍历目录（钩子目录即事实源，新增钩子自动纳入）；非钩子文件跳过。
# git 只按精确文件名识别钩子（均无扩展名），*.sh 必为辅助脚本——排除即不变式，
# 新增辅助脚本无需维护清单
for hook in "$HOOKS_DIR"/*; do
    [ -f "$hook" ] || continue   # 跳过子目录（glob 字面量已被上方 -d 拦，防御空目录场景）
    case "${hook##*/}" in
        *.sh|*.md) continue ;;   # *.sh 辅助脚本；*.md 文档（r9 no 6b3a：文档不应被 chmod +x）
    esac
    chmod +x "$hook" || { echo "错误: chmod +x $hook 失败，钩子不会生效" >&2; exit 1; }   # 真实错误 exit 1（r13 no103）
    [ -x "$hook" ] || { echo "错误: $hook 不可执行，该钩子不会生效" >&2; exit 1; }
done

if old="$(git config --show-origin --get core.hooksPath 2>/dev/null)"; then
    origin="${old%%$'\t'*}"; old="${old#*$'\t'}"
    if [ "$old" != "$HOOKS_DIR" ]; then
        # worktree 级来源将被下方迁移清理而非覆盖（r12 no87 口径区分）
        case "$origin" in
            *config.worktree*) echo "注意: 发现 worktree 级 core.hooksPath（来自 ${origin#file:}）: $old——将随迁移清理" >&2 ;;
            *)                 echo "注意: 覆盖已有 core.hooksPath（来自 ${origin#file:}）: $old -> $HOOKS_DIR" >&2 ;;
        esac
    fi
fi
# porcelain 每块以空行结尾；先落盘再循环：进程替换的退出码不传播，pipefail 下 git 失败
# 会静默空循环（r9 no 9e3e）。清理与校验两个循环共用同一快照
wts=$(git worktree list --porcelain) || { echo "错误: git worktree list 失败" >&2; exit 1; }

# porcelain 共享解析：attached 块以 branch 行收尾，detached 块以 detached 行收尾，空行即块界。
# 块边界处理而非行特征触发（r8 no30a9）；末块 flush 非边角而是主路径（r11 no74）。
# 清理与校验两循环共用，防解析口径分叉（r12 no89）。回调返回非零不中断遍历，
# 由调用方聚合（CALLBACK_FAILED）；进程替换退出码不传播，故先落盘 wts（r9 no 9e3e）
CALLBACK_FAILED=0
each_wt() {  # $1 = 回调函数名（接受 worktree 路径参数）
    local wt_dir="" line
    while IFS= read -r line; do
        case "$line" in
            worktree\ *) wt_dir="${line#worktree }" ;;
            bare)        wt_dir="" ;;
            "")          [ -n "$wt_dir" ] && { "$1" "$wt_dir" || CALLBACK_FAILED=1; }; wt_dir="" ;;
        esac
    done <<< "$wts"
    if [ -n "$wt_dir" ]; then "$1" "$wt_dir" || CALLBACK_FAILED=1; fi
    return 0   # 显式 0：&& 短路状态不得成为函数返回值（set -e 会吞掉聚合，r14 no118）
}

# 迁移清理：旧 install-hooks.sh 是单 worktree 作用域——每个跑过旧脚本的
# worktree 都写了各自的 worktree 级 hooksPath（指向已悬空的 gitdir hooks），
# 优先级高于 clone 级配置。遍历全部 worktree 统一清理
if [ "$(git config --bool extensions.worktreeConfig 2>/dev/null)" = "true" ]; then
    clean_fail=0
    clean_wt() {  # $1 = worktree 路径：存在 worktree 级 hooksPath 则清除
        local old_val
        if old_val=$(git -C "$1" config --worktree --get core.hooksPath 2>/dev/null); then   # 单次调用探测+取值（r15 no135：消竞态）
            if git -C "$1" config --worktree --unset-all core.hooksPath; then
                echo "✓ 已清除 $1 的旧 worktree 级 hooksPath（原值: $old_val）"   # 带原值可追溯（r12 no88）
            else
                echo "警告: $1 清理失败" >&2
                return 1   # 显式失败：否则赋值 return 0，each_wt 聚合永远不触发（r13 no102·high）
            fi
        fi
    }
    # 旧 install-hooks.sh 残留形态即 gitdir hooks 路径；用户自意的其他 worktree 级配置
    # 也会被清——原值已在上条提示保留可恢复（r12 no88，取舍：迁移脚本语义即统一）
    each_wt clean_wt
    clean_fail=$CALLBACK_FAILED   # 共享遍历器的失败聚合（r12 no89）
    CALLBACK_FAILED=0
fi

git config core.hooksPath "$HOOKS_DIR"
# 写入后校验各 worktree 的实际生效值（worktree 级优先于 clone 级）：
# 清理失败或存量覆盖（extensions.worktreeConfig 未启用而 worktree config 已有值）都会让
# clone 级写入对个别 worktree 无效——逐仓校验并显式暴露，不做静默降级（r8 no8548）。
# porcelain 每块以空行结尾——空行即块主路径，末块 flush 并非边角兼容（r11 no74）
check_wt() {  # $1 = worktree 路径：校验实际生效值（悬空跳过并提示，r10 no e1a4）
    if [ ! -d "$1" ]; then
        echo "警告: $1 已不存在（悬空 worktree 元数据），跳过校验，建议 git worktree prune" >&2
        return 0
    fi
    if [ "$(git -C "$1" config core.hooksPath 2>/dev/null)" != "$HOOKS_DIR" ]; then
        echo "警告: $1 的 hooksPath 校验未通过（实际生效值非 $HOOKS_DIR——通常为 worktree 级覆盖残留），该 worktree 钩子不生效" >&2
        return 1
    fi
}
wt_mismatch=0
each_wt check_wt
wt_mismatch=$CALLBACK_FAILED   # 共享遍历器的失败聚合（r12 no89）
CALLBACK_FAILED=0
# 按行解析无法表示含换行的路径（git ≥2.36 才有 --porcelain -z）：此类极端路径不受支持（已文档化）

# 清理失败/校验不匹配 = 真实错误（与头部边界声明一致：仅目录缺失属 fail-open），exit 1
# 让 wt pre-start / Makefile setup 调用方能感知（r9 no 3627/5b6d）
if [ "${clean_fail:-0}" = 1 ] || [ "${wt_mismatch:-0}" = 1 ]; then
    echo "错误: 存在 worktree 级 hooksPath 覆盖未被清除（worktree 级优先，钩子不会指向 $HOOKS_DIR）——请手动：git -C <worktree> config --worktree --unset-all core.hooksPath" >&2   # 同键多值时单 --unset 必败（r12 no86）
    exit 1
fi
echo "✓ core.hooksPath = $HOOKS_DIR（本 clone 主检出与全部 worktree 生效）"
echo "  队友 clone 后跑一次 bash $HOOKS_DIR/install.sh；wt 用户由仓内 .config/wt.toml [pre-start] 自动装。"
echo "  注意: pre-start 仅在 worktree 首次创建时执行——已存在的 worktree 需手动跑一次本脚本。"
