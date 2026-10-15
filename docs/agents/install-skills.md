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

## 目录级变更的陷阱（2026-10-15 教训）

settings.json 的 `skills` 数组条目（`skills/xxx` 或 `.pi/agent/skills/xxx` 形式）以 **agentDir（`~/.pi/agent`）为解析基准**。目录级变更后必须 grep settings.json 检查资源路径引用——失配的条目**静默失效不报错**：

- `~/.pi/agent/skills/` 整体删除后：所有相对条目成死条目；指向已删目录的 `+` 强制包含条目同步删除；auto-discover（`~/.agents/skills`）覆盖的重复条目无需恢复
- 备份：改 settings.json 前 `cp ~/.pi/agent/settings.json ~/tmp/settings.json.bak-<date>`
- 安装后验证：headless 起一个 pi（`pi --mode json -p "..."`），确认 skill 注入正常
