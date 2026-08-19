# 安装与管理本地 Skill

本仓库下的 skill 通过 [`npx skills`](https://github.com/vercel-labs/agent-skills) CLI 安装到本地 agent。

## 安装

```bash
# 安装单个 skill（交互式选择 agent）
npx skills add -g ./<skill-name>

# 批量安装当前仓库所有 skill 到 Pi
npx skills add ~/skills/ --global -a pi -y

# 安装 vendor 下的 mattpocock skill
npx skills add ~/skills/vendor/mattpocock --global -a pi -y
```

## 管理

```bash
# 列出已安装的全局 skill
npx skills list -g

# 移除
npx skills remove -g <skill-name>
```
