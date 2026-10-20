====以下内容是给你 Agent 看的当前项目规范，**必须遵循，不能在压缩上下文时忘记**====

# 个人 skills 仓库

## 描述

当前仓库下放置了我需要的 skills 的代码仓库。

## 仓库资源索引（clone 后先看这里，避免重复查找）

| 资源 | 用途 | 备注 |
|------|------|------|
| `scripts/githooks/`（pre-commit / pre-push / post-commit） | gitleaks 凭证拦截 + 提交后自动重装变更的 skill | 依赖 `git config core.hooksPath scripts/githooks`，**该配置不入库，新 clone 必须手动执行一次**（或 `git config --local core.hooksPath scripts/githooks`）；gitleaks 自定义配置在 `~/data/benchmark/config/gitleaks.toml`，缺失时退化为默认规则 |
| `scripts/sanitize-check.sh` | 推送前脱敏检查（gitleaks + 内部标识 pattern 层） | 推送前必跑，见下方 Git 工作流 |
| `scripts/check-all-env.sh` | 换节点后的环境自检 | 新节点第一步 |
| `.github/workflows/tests.yml` | CI：push/PR main 时 `uv run pytest` | 绿是合并标准 |
| `docs/agents/` | install-skills / skill-authoring / issue-tracker / triage-labels / domain 五份 agent 文档 | 写 skill 前必读 skill-authoring.md |
| `wiki/` | skill 持久知识层（已知问题/被拒提案） | 改 skill 前后必走，见下方 Skill Wiki 节 |
| `vendor/mattpocock/` | 上游 subtree 镜像 | 同步规则见下方 Vendor 管理 |

## 新 skill 归属

新建 skill 一律放在 `in-progress/`，无任何例外，不需要判断主题或成熟度。只有用户明确要求时才移入正式分类目录（如 `productivity/`、`engineering/`）。

## 安装

安装或同步 skill 到全局 agent 时，必须用 `npx skills add -g ./<path> -a pi -y`，禁止手动 `cp`。完整规范见 `docs/agents/install-skills.md`。

## 安装副本与源仓的关系

- 直接修改 `~/.pi/agent/skills/<name>/`（安装副本）不会同步回本源仓。修 skill 必须改本仓源文件，改完 diff 源仓 vs 安装副本确认一致后，再 `npx skills add -g` 重装。
- skill "表现不对劲"时，先 `diff ~/.agents/skills/<name>/ <源仓路径>` 排除 stale 副本：`~/.pi` 下可能残留一个旧的真实目录（非 symlink），遮蔽了新版本。

## 测试

A skill may carry tests even though it is primarily documentation — `tests/` and a `pyproject.toml` sit beside the `SKILL.md`. After modifying any skill, run its tests if present. A green run is the completion criterion for the change; a skill with no tests is exempt. Test invocation follows the two-tier rule in `docs/agents/skill-authoring.md`（Python environment tiers）: pytest-only skills 用共享 venv（`uv run --project <repo-root> pytest <skill>/tests`），有运行时依赖的 skill 用自己的 `<SKILL_DIR>/.venv`（`uv run --project <SKILL_DIR> pytest tests`）。

## Git 工作流

多 session 共享本 checkout，直接在 `main` 上提交（无 wip 集成分支）。约定：
- 提交前 `git status` 确认工作区——只 `git add` 自己本次任务的文件，**禁止 `git add -A`**（会卷入其他 session 的进行中改动）。
- 提交信息不相关的东西不混入同一 commit（例如 sanitize 修复不与 feature 混提）。
- 推送前重跑 `bash scripts/sanitize-check.sh`（tracked 模式），含内部标识的文件先修再推。
- 历史遗留的 `feat/*`、`session-*` 分支不受此规范约束。

## Vendor 管理（mattpocock 上游）

`vendor/mattpocock/` 是 `git subtree add --squash` 导入的上游镜像，定制直接改 vendor 内文件，随本仓 commit 沉淀。

- **同步上游**：`git fetch mattpocock && git subtree pull --prefix vendor/mattpocock mattpocock main --squash`。冲突只会出现在双方改过同一文件时；对纯本地新增（add/add）与上游演进重合的文件，先 diff 裁决哪边更新再取。同步后对变更的 skill 重装（`npx skills add -g`）。
- **commit 分层**：pi 专属机械适配（`/skill:` 格式迁移、sanitize 脱敏、路径调整）与实质性功能改动分开成 commit——前者是每次同步可能重放的嫁接税，保持独立才好在冲突时快速重放；后者才值得挑出向上游提 PR。
- **重定制 skill 出 overlay**：改动深、每次同步冲突重的 skill（当前 teach、setup-matt-pocock-skills、wayfinder、diagnosing-bugs-with-docs fork）以 `in-progress/` 定制版为唯一安装源；vendor 内保留上游纯净版，保证 subtree pull 零冲突。误改 vendor 副本会在下次同步时以冲突形式暴露漂移。
- **禁止**为同步便利另建 fork 仓或 patch 层——subtree 的设计就是同一目录靠三方合并解纠缠。

## Skill Wiki（改 skill 前后必走）

`wiki/` 是持久知识层（条目格式、状态机、sanitize 规范见 `wiki/README.md`）。`<skill-name>` = skill 目录名（如 `engineering/mr-review-triage` → `wiki/mr-review-triage/`）。

- **改 skill 前**：`wiki/<skill-name>/` 存在时先读——`patterns.md` 的 open 条目是该 skill 已知问题（修改方案别与其冲突、能顺带吸收则吸收）；`skill-impact.md` 里的被拒提案不得无新证据重提。目录不存在 = 冷启动，直接动手。
- **改 skill 后（commit 时）**：向 `skill-impact.md` 追加一行（提案/落点/commit hash/验证）；用户否决的方案记 rejected（含理由）。行为性修改必记；纯错别字/排版豁免。无 wiki 目录则连同本次修改创建。
- **写入 sanitize**：wiki 在公共仓库——证据只写 `session-id#entry`，内网域名/项目名/凭证按 `docs/agents/skill-authoring.md` 占位符脱敏，commit 前跑 `bash scripts/sanitize-check.sh`（gitleaks + 内部标识 pattern 层）。

## 运行时与环境（脚本型 skill）

Script skill 的 runtime/环境约定（runtime.conf 模式、check-env.sh、敏感数据规则）全在 `docs/agents/skill-authoring.md`：创建或改造 script skill、把 skill 移出 in-progress、或提交任何含 endpoint/域名/配置的文件前必读（本仓库为 public）。换节点第一步：`bash scripts/check-all-env.sh`。

**写/改任何 skill 前必须先读 `docs/agents/skill-authoring.md`**（硬性前置，不是建议）：其中的 Pipeline discipline 节（subprocess 失败必须响、uv run 锁死、一键入口+聚合退出码、跨 skill import 声明、输出形状 e2e 验证）为 Required 级约定，reviewer 按此文逐条检查。

## Agent skills

### Issue tracker

Issues live in GitHub Issues on `github.com/peachest/skills`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles use default label strings. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout. See `docs/agents/domain.md`.

# Writing Skills 规范

skill.md 描述中使用 `<SKILL_DIR>` 和 `<PROJECT_DIR>` 占位符区别不同工作目录

====当前项目规范结束====