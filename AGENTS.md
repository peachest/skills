====以下内容是给你 Agent 看的当前项目规范，**必须遵循，不能在压缩上下文时忘记**====

# 个人 skills 仓库

## 描述

当前仓库下放置了我需要的 skills 的代码仓库。

## 新 skill 归属

新建 skill 一律放在 `in-progress/`，无任何例外，不需要判断主题或成熟度。只有用户明确要求时才移入正式分类目录（如 `productivity/`、`engineering/`）。

## 安装

安装或同步 skill 到全局 agent 时，必须用 `npx skills add -g ./<path> -a pi -y`，禁止手动 `cp`。完整规范见 `docs/agents/install-skills.md`。

## 测试

A skill may carry tests even though it is primarily documentation — `tests/` and a `pyproject.toml` sit beside the `SKILL.md`. After modifying any skill, run its tests if present (`uv run pytest` from the skill directory). A green run is the completion criterion for the change; a skill with no tests is exempt.

## Git 工作流

多 session 共享本 checkout，直接在 `main` 上提交（无 wip 集成分支）。约定：
- 提交前 `git status` 确认工作区——只 `git add` 自己本次任务的文件，**禁止 `git add -A`**（会卷入其他 session 的进行中改动）。
- 提交信息不相关的东西不混入同一 commit（例如 sanitize 修复不与 feature 混提）。
- 推送前重跑 `bash scripts/sanitize-check.sh`（tracked 模式），含内部标识的文件先修再推。
- 历史遗留的 `feat/*`、`session-*` 分支不受此规范约束。

## Skill Wiki（改 skill 前后必走）

`wiki/` 是持久知识层（条目格式、状态机、sanitize 规范见 `wiki/README.md`）。`<skill-name>` = skill 目录名（如 `engineering/mr-review-triage` → `wiki/mr-review-triage/`）。

- **改 skill 前**：`wiki/<skill-name>/` 存在时先读——`patterns.md` 的 open 条目是该 skill 已知问题（修改方案别与其冲突、能顺带吸收则吸收）；`skill-impact.md` 里的被拒提案不得无新证据重提。目录不存在 = 冷启动，直接动手。
- **改 skill 后（commit 时）**：向 `skill-impact.md` 追加一行（提案/落点/commit hash/验证）；用户否决的方案记 rejected（含理由）。行为性修改必记；纯错别字/排版豁免。无 wiki 目录则连同本次修改创建。
- **写入 sanitize**：wiki 在公共仓库——证据只写 `session-id#entry`，内网域名/项目名/凭证按 `docs/agents/skill-authoring.md` 占位符脱敏，commit 前跑 `bash scripts/sanitize-check.sh`（gitleaks + 内部标识 pattern 层）。

## 运行时与环境（脚本型 skill）

Script skill 的 runtime/环境约定（runtime.conf 模式、check-env.sh、敏感数据规则）全在 `docs/agents/skill-authoring.md`：创建或改造 script skill、把 skill 移出 in-progress、或提交任何含 endpoint/域名/配置的文件前必读（本仓库为 public）。换节点第一步：`bash scripts/check-all-env.sh`。

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