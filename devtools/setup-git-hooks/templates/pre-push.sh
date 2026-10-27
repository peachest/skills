#!/bin/bash
# pre-push: 对"将要推送的 commit"跑全量 make lint + make test，
# 模拟远程 CI。在 /tmp/build-<project>/ 下创建 worktree 和依赖子目录，
# 让 go.mod 的 replace => ../HAMi 自然解析到同级 HAMi/ 目录。
#
# Wiki drift 检测：project_wiki 源文件 SHA 漂移时暂停 push，交给 agent 更新。
#
# 跳过检查: git push --no-verify

set -uo pipefail   # 入口自行声明（common.sh 不带副作用）；不用 -e：pre-push 需捕获 wiki.py 的设计内退出码
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"   # cd+pwd -P 可移植（r12 no81/r19 no208/r23 no271：省 basename 往返）；不解析 $0 符号链接——install.sh 以 hooksPath 直指仓内目录
source "$SCRIPT_DIR/common.sh" || { echo "无法加载 common.sh" >&2; exit 1; }

repo_root=$(git rev-parse --show-toplevel) || exit 1
cd "$repo_root" || exit 1

zero=0000000000000000000000000000000000000000
checked=""
build_base="/tmp/build-ppu-device-plugin"

# 清理上次失败的残留
git worktree prune 2>/dev/null
rm -rf "$build_base"

# EXIT 时清理
trap 'rm -rf "$build_base"; git worktree prune 2>/dev/null' EXIT

# clone_replace_deps: 解析 go.mod 中的 replace => ../xxx 行，
# 从 GitLab clone 对应仓库到 build_base/xxx。
# 对标 common-ci/go-build.yml 的依赖拉取逻辑。
clone_replace_deps() {
    local go_mod="$1"

    while IFS= read -r line; do
        local dir_name
        dir_name=$(echo "$line" | sed 's|.*/||')
        local target="$build_base/$dir_name"

        if [ -d "$target" ]; then
            continue
        fi

        local gitlab_url="ssh://git@gitlab.example.com/<group>/${dir_name}.git"
        log_info "克隆依赖: $dir_name <- $gitlab_url (dev)"
        local clone_err
        if ! clone_err=$(git clone --quiet --depth 1 -b dev "$gitlab_url" "$target" 2>&1); then
            log_warn "克隆 $dir_name dev 分支失败: $clone_err"
            log_warn "尝试默认分支"
            if ! clone_err=$(git clone --quiet --depth 1 "$gitlab_url" "$target" 2>&1); then
                log_warn "无法克隆 $dir_name: $clone_err"
            fi
        fi
    done < <(grep 'replace.*=>.*\.\./' "$go_mod" 2>/dev/null)
}

# 确保 go 在 PATH 中：~/sdk/go 是无版本号的稳定入口（不写死版本目录，
# go1.26.5 之类升级后即消失）；~/go/bin 提供 golangci-lint 等 make 依赖。
# PATH 幂等，置于循环外只拼一次；删除远端分支的推送不需要 go，
# 故 command -v 检查放在循环内 skip 之后（见下）。
# 首段 GO 工具链（HOME 防未绑定）；末段缺省避免 PATH 未设时尾冒号（空元素=当前目录，r7 no2）
gopath_prefix="${HOME:+$HOME/sdk/go/bin:}${HOME:+$HOME/go/bin:}"
path_fallback="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export PATH="${gopath_prefix}${PATH:-$path_fallback}"

# stdin 每行: <local ref> <local sha> <remote ref> <remote sha>
while read -r _local_ref local_sha _remote_ref _remote_sha; do
    [ -z "$local_sha" ] || [ "$local_sha" = "$zero" ] && continue
    command -v go >/dev/null 2>&1 || { log_error "未找到 go 工具链（期望 ~/sdk/go/bin 或 PATH）"; exit 1; }
    case " $checked " in *" $local_sha "*) continue ;; esac
    checked="$checked $local_sha"

    rm -rf "$build_base"
    mkdir -p "$build_base"

    worktree_dir="$build_base/worktree"

    log_info "在干净 worktree 中检查 ${local_sha:0:8} （模拟远程 CI，忽略本地未提交变更）..."
    git worktree add --detach "$worktree_dir" "$local_sha" >/dev/null || exit 1

    # 从 GitLab clone go.mod replace 指向的依赖仓库到 build_base/ 下。
    # worktree 的 ../HAMi → build_base/HAMi，go.mod replace 路径自然解析。
    clone_replace_deps "$worktree_dir/go.mod"

    # 同步依赖：clone 的 HAMi dev 分支 go.mod 可能与 go.sum 不一致
    (cd "$worktree_dir" && go mod tidy) || { log_error "go mod tidy 失败"; exit 1; }

    # 校验 .gitlab-ci.yml 语法和 pipeline 创建
    log_info "校验 .gitlab-ci.yml..."
    if ! (cd "$worktree_dir" && glab ci lint --dry-run 2>/dev/null); then
        log_error ".gitlab-ci.yml 校验失败（针对已提交内容 ${local_sha:0:8}）。"
        log_error "修复后重新提交推送；确要跳过用 git push --no-verify。"
        exit 1
    fi

    if ! make -C "$worktree_dir" lint test; then
        log_error "make lint / test 失败（针对已提交内容 ${local_sha:0:8}）。"
        log_error "修复后重新提交推送；确要跳过用 git push --no-verify。"
        exit 1
    fi

    git worktree remove --force "$worktree_dir" >/dev/null 2>&1
    rm -rf "$build_base"
done

# ---------------------------------------------------------------------------
# Project wiki drift 检测
# ---------------------------------------------------------------------------
# 检测源文件 SHA 与 .review_cache.json 基线是否一致。
# 漂移即暂停 push，交给 agent 更新 wiki。
#
# wiki home (docs/home.md) 不需要检测——它在 .gitignore 中，
# CI sync job 每次从 docs/ 结构重新生成，永远不会过时。

wiki_py="$repo_root/hack/wiki.py"
wiki_stale=false
wiki_output=""

if [ -f "$wiki_py" ] && [ -d "$repo_root/docs/project_wiki" ]; then
    wiki_output=$(cd "$repo_root" && python3 "$wiki_py" check --root . --fail-on-stale 2>&1)
    rc=$?
    case $rc in
        1) wiki_stale=true ;;
        2) log_warn "docs/project_wiki/ 未初始化（返回码 2）— 跳过漂移检测"
           log_warn "首次使用请运行: python3 hack/wiki.py init --root ." ;;
    esac
else
    log_warn "hack/wiki.py 未找到 — 跳过漂移检测"
fi

if $wiki_stale; then
    echo ""
    log_error "═══════════════════════════════════════════════════════════════"
    log_error "Project wiki 漂移检测：源文件 SHA 已变化 — push 已暂停"
    log_error "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "$wiki_output" | sed 's/^/     /'
    echo ""
    log_info "修复步骤:"
    log_info "  # 审查并更新 docs/project_wiki/*.md 中变更文件的描述"
    log_info "  python3 hack/wiki.py update --root .                      # 刷新 SHA 基线"
    log_info "  git add docs/ && git commit && git push"
    echo ""
    log_warn "或交给 agent 处理: /skill:project-wiki"
    echo ""
    log_error "确要跳过用 git push --no-verify。"
    exit 1
fi

log_info "pre-push 检查通过。"
