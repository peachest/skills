# 安装 Skill 到本地 Agent

本仓库下的 skill 通过 [`skills`](https://github.com/vercel-labs/agent-skills) CLI 安装到本地 agent。

## 安装

```bash
# 安装单个 skill 到全局（所有 agent，包括 Pi）
npx skills add -g -y ./<skill-name>

# 安装单个 skill（交互式选择 agent）
npx skills add -g ./<skill-name>

# 批量安装当前仓库所有 skill 到 Pi
npx skills add ~/skills/ --global --all -a pi -y

# 安装 vendor 下的 mattpocock skill
npx skills add ~/skills/vendor/mattpocock --global --all -a pi -y
```

## 管理

```bash
# 列出已安装的全局 skill
npx skills list -g

# 移除
npx skills remove -g <skill-name>
```

## 存储结构

安装后，skill 文件统一存放在 `~/.agents/skills/`，各 agent 通过符号链接引用：

```
~/.agents/skills/<skill-name>/        ← skills CLI 的全局存储（实际文件）
    ↑ symlink
~/.pi/agent/skills/<skill-name>       ← Pi agent 读取 skills 的目录
```

`--global`（`-g`）安装到全局；不加 `-g` 则安装到当前项目的 `.skills/` 目录下。
