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
| `vendor/mattpocock/` | 上游 subtree 镜像 | 同步规则见 [`vendor/mattpocock/MIRROR.md`](vendor/mattpocock/MIRROR.md) |
| `vendor/pstack/` | pstack 上游 subtree 镜像（backnotprop 镜像，装精选子集） | 同步规则见 [`vendor/pstack/SYNC.md`](vendor/pstack/SYNC.md) |

## 新 skill 归属

新建 skill 一律放在 `in-progress/`，无任何例外，不需要判断主题或成熟度。只有用户明确要求时才移入正式分类目录（如 `productivity/`、`engineering/`）。

## 安装

安装或同步 skill 到全局 agent 时，必须用 `npx skills add -g ./<path> -a pi -y`，禁止手动 `cp`。完整规范见 `docs/agents/install-skills.md`。

## 安装副本与源仓的关系

- 安装链是单向的：本仓源文件 → `npx skills add -g` → `~/.agents/skills/<name>/`。pi 的 skill 扫描链同时覆盖 `~/.pi/agent/skills` 与 `~/.agents/skills`，但本仓 skill 只经 npx 装 ~/.agents，**不要往 ~/.pi/agent/skills 装本仓 skill 或建 symlink**（会双份加载）；该目录的正确用途是存放不属于本仓的第三方 skill（如 pack-leader）。
- 直接修改 `~/.agents/skills/<name>/`（安装副本）不会同步回本源仓。修 skill 必须改本仓源文件，改完 diff 源仓 vs 安装副本确认一致后，再 `npx skills add -g` 重装。
- skill “表现不对劲”时，先 `diff ~/.agents/skills/<name>/ <源仓路径>` 排除 stale 副本。

## 测试

A skill may carry tests even though it is primarily documentation — `tests/` and a `pyproject.toml` sit beside the `SKILL.md`. After modifying any skill, run its tests if present. A green run is the completion criterion for the change; a skill with no tests is exempt. Test invocation follows the two-tier rule in `docs/agents/skill-authoring.md`（Python environment tiers）: pytest-only skills 用共享 venv（`uv run --project <repo-root> pytest <skill>/tests`），有运行时依赖的 skill 用自己的 `<SKILL_DIR>/.venv`（`uv run --project <SKILL_DIR> pytest tests`）。

## Git 工作流

多 session 共享本 checkout，直接在 `main` 上提交（无 wip 集成分支）。约定：
- 提交前 `git status` 确认工作区——只 `git add` 自己本次任务的文件，**禁止 `git add -A`**（会卷入其他 session 的进行中改动）。
- sanitize-check DIRTY 命中非本任务文件时：`git log --oneline -2 -- <file>` 核实归属后留给所属 session 处置，禁止代改、也禁止改用全仓审计模式（`-a`）绕行。
- 提交信息不相关的东西不混入同一 commit（例如 sanitize 修复不与 feature 混提）。
- 推送前重跑 `bash scripts/sanitize-check.sh && git push origin main`（tracked 模式只扫未推送区间；全仓审计用 `bash scripts/sanitize-check.sh -a`）。门禁脚本必须独立运行并用 `&&` 串联检查退出码，**禁止放进管道**（`sanitize-check | tail` 的退出码来自 tail，DIRTY 被吞掉就会带病推送）。含内部标识的文件先修再推。
- 历史遗留的 `feat/*`、`session-*` 分支不受此规范约束。

## Vendor 管理（mattpocock 上游）

`vendor/mattpocock/` 是 `git subtree add --squash` 导入的上游镜像。同步操作、冲突处理、commit 分层与 overlay 规则全部见 [`vendor/mattpocock/MIRROR.md`](vendor/mattpocock/MIRROR.md)（本节不重复，改动同步策略时只改 MIRROR.md）。

## Skill Wiki（改 skill 前后必走）

`wiki/` 是持久知识层（条目格式、状态机、sanitize 规范见 `wiki/README.md`）。`<skill-name>` = skill 目录名（如 `engineering/mr-review-triage` → `wiki/mr-review-triage/`）。

- **改 skill 前**：`wiki/<skill-name>/` 存在时先读——`patterns.md` 的 open 条目是该 skill 已知问题（修改方案别与其冲突、能顺带吸收则吸收）；`skill-impact.md` 里的被拒提案不得无新证据重提。目录不存在 = 冷启动，直接动手。
- **改 skill 后**：原子提交——skill 本体变更与 `skill-impact.md` 台账行**同一 commit**，台账 commit 列写本次 commit 的 subject 原文（不用 hash：hash 对 filter-repo 改写不免疫且存在自引用死锁）。规则见 `wiki/README.md` 的 skill-impact 节，由 `scripts/githooks/` 三道闸门机械强制（pre-commit 配对 + commit-msg subject 一致 + pre-push 漂移检测）。确属纯排版/错别字修复用 --no-verify 跳过配对闸门。用户否决的方案记 rejected（含理由）。行为性修改必记。无 wiki 目录则连同本次修改创建。
- **写入 sanitize**：wiki 在公共仓库——证据只写 `session-id#entry`，内网域名/项目名/凭证按 `docs/agents/skill-authoring.md` 占位符脱敏，commit 前跑 `bash scripts/sanitize-check.sh`（gitleaks + 内部标识 pattern 层）。

## Recheck scripts

挖掘/诊断/优化 session 留在 `~/tmp` 的复跑验证脚本，收尾时提交到 `recheck/`（脚本 + INDEX.md 一行：验证目标、基线数字、来源 session）。复跑脚本不进 `~/tmp` 裸放；环境锁定或一次性的写明 `shortcut: one-off, <date>` 后留在 tmp。触发器在 session-mining 的 Close：挖到对应 skill/tool 时按 INDEX 复跑并对比基线。

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