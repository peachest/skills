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