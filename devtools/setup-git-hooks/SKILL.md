---
name: setup-git-hooks
description: Set up local git hooks via `core.hooksPath` pointing at an in-repo hooks directory (`tools/git-hooks/` by default), with a policy-driven commit-msg script shared by local hook and CI backstop job. Supports pre-commit, commit-msg, and pre-push (base-branch drift check + CI simulation). Plain bash, shared `common.sh`.
disable-model-invocation: true
---

# Setup Git Hooks

Scaffold a repo-local git hooks system: plain bash hooks in an in-repo
directory, activated by `core.hooksPath` (one config line — no symlinks,
no `.git/hooks` copies, works across all worktrees of the clone):

```
tools/git-hooks/          # path follows the repo's existing script-dir convention
├── common.sh             # shared logging + utilities
├── install.sh            # two lines: git config core.hooksPath + chmod
├── commit-msg            # policy-driven format check (config block at top)
├── pre-commit            # git identity, staged-format (check-only), whitespace
└── pre-push              # base-branch drift check + CI simulation (lint/test)
```

Optional CI backstop (generated separately, reads the same commit-msg):

```
.gitlab-ci.yml  ←  tw-commit-check job (stage .pre) via ci-commit-check.yml template
```

This is a **prompt-driven skill**, not a deterministic script. Explore, present
what you found, confirm with the user, then scaffold.

## Design principles (do not re-litigate)

- **脚本即事实源**：commit 格式/前缀/豁免规则的正典实现 = `commit-msg` 头部配置块。
  本地钩子（L1）与 CI 兜底 job（L2）调同一个脚本（`--ci` 模式），口径天然一致，
  不存在"两处同步"。不建独立 policy 文件——那会把"写 hook"变成"扩 schema"。
- **core.hooksPath 而非 symlink/.git/hooks 拷贝**：hooks 目录随分支文件走；
  旧分支没有该目录时 hook 自动不生效（fail-open，安全方向）。配置是 clone 级
  共享的，一次设置主检出与全部 worktree 生效。
- **格式检查只查不写**：pre-commit 校验 `git show :file`（staged 内容），
  自动 `-w` 写回会破坏 `git add -p` 部分暂存。
- **三层强制模型**（详述见 setup-dev-and-contributing 的 DEVELOPMENT.md 模板 §7）：
  L0 文档 → L1 本地钩子（本 skill）→ L1.5 wt `[pre-start]` 检出即装 → L2 CI 兜底。
  K8s 等大生态只做服务端（per-clone 分发率注定趋零）；内部仓用 L1.5 把分发率
  拉到近 100%，L1/L2 才值得做。

## Process

### 1. Explore

- `git remote -v` — fork posture（影响 commit-prefix，见步骤 2 的 Section A）
- `DEVELOPMENT.md` §2.2（若存在）— 已定义的 commit prefix / 豁免规则，吸收不重复
- `Makefile` — lint/test targets；`hack/` vs `tools/` 哪个是本仓的脚本目录约定
- `go.mod` / `package.json` 等 — 语言与默认检查命令；`go.mod` 有 `replace => ../`
  相对依赖时 pre-push 建议用 isolated 模式
- 既有 hooks：`git config core.hooksPath`、`.git/hooks/`、仓内 `hooks/`、
  `.config/wt.toml` 的 `[pre-start]`
- 主检出是否有 wt（`wt list` / `.config/wt.toml`）——决定要不要写 L1.5 配置

### 2. Present findings and ask

**Section A — Repo posture（影响 commit-msg 配置块）**：
- upstream OSS / internal-only → `COMMIT_PREFIX=""`，纯 conventional（或不启用格式约束）
- internal fork → `COMMIT_PREFIX="[<ORG>]"`（从 DEVELOPMENT.md §2.2 或用户处取 org）；
  EXEMPT 保持模板默认（merge/revert/fixup!/上游 cherry-pick -x 尾注）
- 若 DEVELOPMENT.md 已存在：**不要问 prefix**——直接回填其 §2.2 定义，并在 §7
  三层表更新 L1/L2 的实现指向

**Section B — Hook set**（默认全装三个，逐项确认删减）：

| Hook | 检查 | 备注 |
|------|------|------|
| `commit-msg` | prefix（fork）+ conventional + 豁免 | 配置块在脚本头部 |
| `pre-commit` | git 身份、gofmt（staged、只查）、空白符 | 秒级 |
| `pre-push` | base-branch drift（落后基分支即阻断）+ `make lint test` | drift 需 fetch，故放 push 不放 commit |

**Section C — CI 兜底（L2，默认生成）**：是否附带 `tw-commit-check` job
（`ci-commit-check.yml` 模板合入 `.gitlab-ci.yml`）。默认生成——堵 `--no-verify`
与未装钩子的检出。需要 bash 镜像（alpine/git 不含 bash）。

**Section D — pre-push 模式**：`SIM_MODE=simple`（当前仓直接 make）为默认；
仓有 `replace => ../` 相对依赖或需要防"本地脏状态假绿"时用 `isolated`
（临时 worktree 检出推送 SHA + clone 依赖——参考 <device-plugin-repo>
`hooks/pre-push.sh` 的 `clone_replace_deps` 实现，按仓定制）。

### 3. Confirm and edit

Show the complete directory tree with file contents (templates from `./templates/`
with repo facts filled in). Let the user tweak before writing.

### 4. Write

Files to create (copy from `./templates/`, adapt):

- `tools/git-hooks/common.sh`
- `tools/git-hooks/install.sh`（若仓的脚本目录是 `hack/`，把 `HOOKS_DIR` 改为
  `hack/git-hooks` 并把目录放 hack/ 下——跟随仓内既有约定，不引入第二套脚本目录）
- `tools/git-hooks/commit-msg`（填 Section A 的配置块）
- `tools/git-hooks/pre-commit`（formatter 按语言换：gofmt/prettier/black…）
- `tools/git-hooks/pre-push`（`SIM_MAKE_TARGETS` 换成真实 make 目标）
- Section C 选是 → 把 `ci-commit-check.yml` 合入 `.gitlab-ci.yml`

Then wire up:

1. **Makefile**：无 `setup` target 则加：
   ```makefile
   .PHONY: setup
   setup:  ## install git hooks (core.hooksPath)
   	@bash tools/git-hooks/install.sh
   ```
   已有 setup 但不含 install.sh 则问用户合并或改名。
2. **L1.5（wt 用户）**：主检出 `.config/wt.toml` 加
   `[pre-start] hooks = "bash tools/git-hooks/install.sh"`（该文件有意不入库——
   per-clone 本地配置）。非 wt 队友：README/DEVELOPMENT.md 写一行
   "clone 后跑 `bash tools/git-hooks/install.sh`"。
3. **文档指针**：若 DEVELOPMENT.md 存在，§7 三层表补 L1/L2 实现路径；
   fork 仓在 §2.2 加一行"规则正典实现 = tools/git-hooks/commit-msg 配置块，
   改规则先改脚本（L1/L2 自动同源）"。

### 5. Done

Tell the user:
- 装了哪些 hook、各自检查什么；`make setup` 或 `bash tools/git-hooks/install.sh` 重装
- L2 job 是否已合入 CI；豁免语义（存量历史不回溯）
- base-branch drift 的绕过方式（`HOOKS_ALLOW_BASE_DRIFT=1` 单次 / `--no-verify`）
- 多 worktree 无需再装（clone 级配置 + 目录随分支走）；新 clone 跑一次 install.sh
