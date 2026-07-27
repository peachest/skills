# Skills 同步管理

当前仓库下放置了我需要的 skills 的代码仓库。

## 同步规则

每个 skill 仓库下有一个 `.sync-rules.json` 文件（已加入 `.gitignore`，不纳入版本控制），定义了该仓库中每个 skill 的黑白名单：

```json
{
  "whitelist": ["skill-a", "skill-b"],
  "blacklist": ["skill-c"]
}
```

## 同步流程

当我提出 "同步" 请求时，按以下步骤执行：

1. 进入每个 skill 仓库，用 git 同步拉取远程仓库中的更新（使用代理 `http://INTERNAL_PROXY_IP:3128`）。

2. 读取该仓库下的 `.sync-rules.json`，对仓库中的每个 skill 目录执行黑白名单校验：

   - **白名单**（whitelist）：需要同步。如果 `~/.pi/agent/skills/` 下不存在，则拷贝；如果存在更新则覆盖。
   - **黑名单**（blacklist）：跳过同步。如果 `~/.pi/agent/skills/` 下已存在，则删除。
   - **未归类**（既不在白名单也不在黑名单）：跳过同步，并提示用户将其加入白名单或黑名单。

3. 向用户汇报本次同步的变更摘要。

## 安装 skill 到本地 agent

使用 `npx skills` CLI 将当前仓库下的 skill 安装到全局（所有 agent，包括 Pi）：

```bash
# 安装单个 skill（交互式选择 agent）
npx skills add -g ./<skill-name>

# 安装单个 skill（跳过确认，安装到所有 agent）
npx skills add -g -y ./<skill-name>

# 列出已安装的全局 skill
npx skills list -g

# 移除
npx skills remove -g <skill-name>
```

安装后，skill 文件存放在 `~/.agents/skills/<skill-name>/`，各 agent（包括 Pi）通过符号链接引用：

```
~/.agents/skills/<skill-name>/        ← npx skills 的全局存储（实际文件）
    ↑ symlink
~/.pi/agent/skills/<skill-name>       ← Pi agent 读取 skills 的目录
```

## Agent skills

### Issue tracker

Issues live in GitHub Issues on `github.com/peachest/skills`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles use default label strings. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout. See `docs/agents/domain.md`.

# Writing Skills

skill.md 描述中使用 `<SKILL_DIR>` 和 `<PROJECT_DIR>` 占位符区别不同工作目录