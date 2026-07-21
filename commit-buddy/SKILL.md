---
name: commit-buddy
description: 你的 git commit 伙伴——分析变更、规划拆分、按 Conventional Commits 提交。使用此 skill 处理所有和 git commit、提交、commit message 相关的任务——当用户提到 git、commit、提交、commit message、提交信息、变更分组、提交计划、conventional commits 时都应该触发。
---

commit-buddy 是你的 git commit 伙伴：拿到一堆变更后，先规划再动手，等你拍板粒度合适后才执行。

commit message 遵循 Conventional Commits 规范，参考 [conventional-commits skill](~/.claude/skills/conventional-commits/SKILL.md)。

## 流程

### Step 1: 收拢变更

```bash
git status --short
git diff --cached --stat
git diff --stat
```

**完成标准**：staged 和 unstaged 的所有变更文件已列出，无一遗漏。

### Step 2: 分析并规划

按以下优先级将变更文件分组为 commit：

1. **功能意图**：同一个 feature 或 fix 的改动放一起（model + handler + test 属于同一组）
2. **文件类型**：无法判断意图时，按文件类型分组（`.go` / `_test.go` / `.md` / `.py`）
3. **目录暗示**：`docs/` → `docs:`、`test/` → `test:`、`hack/` → `chore:`、`prototype/` → `chore(prototype):`
4. **staged 优先**：已 staged 是用户挑选过的，优先成组

每个分组的 commit message 按 Conventional Commits 格式：`type(scope): summary`。

展示格式：

```
### 变更分组

| 分组 | 文件 | 来源 |
|------|------|------|
| <分组名> | <文件列表> | staged/unstaged |

### Commit 计划

N. type(scope): summary
   - 改动子项 1
   - 改动子项 2
```

**完成标准**：所有变更文件都已归入某个 commit，无遗漏。部分文件因跨组依赖而出现在多个 commit 中时，说明原因。

### Step 3: 确认粒度

用 `ask_user_question` 一次性询问：

- **粒度是否合适？**（确认 / 太粗需要拆分 / 太细需要合并）
- 太粗或太细时，追问哪个 commit 需要调整

迭代直到用户确认。

**完成标准**：用户回复确认。

### Step 4: 执行

按 commit 顺序逐个执行。工作区有 unstaged 改动时，先 `git stash --keep-index`。

**单个 commit 的执行步骤**：

```bash
git reset HEAD                    # 清空 index，从零开始挑选
git add <commit 涉及的每个文件>
git commit -m "type(scope): summary" -m "<详细 body>"
```

所有 commit 执行完后，若之前 stash 过则 `git stash pop`。

**完成标准**：所有 commit 已执行。
展示 `git log --oneline -n <N>` 确认最终结果。
若 stash pop 有冲突，指出冲突文件并暂停。
