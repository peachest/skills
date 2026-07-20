---
name: commit-buddy
description: 你的 git commit 伙伴——分析变更、规划拆分、输出 CommitPlan JSON，调用脚本执行。手动触发。
disable-model-invocation: true
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

分析变更并按以下优先级将改动分组为 commit：

1. **功能意图**：同一个 feature 或 fix 的改动放一起（model + handler + test 属于同一组）
2. **文件类型**：无法判断意图时，按文件类型分组（`.go` / `_test.go` / `.md` / `.py`）
3. **目录暗示**：`docs/` → `docs:`、`test/` → `test:`、`hack/` → `chore:`、`prototype/` → `chore(prototype):`
4. **staged 优先**：已 staged 是用户挑选过的，优先成组

在同一文件内：按 hunk 内容判断意图，不同 hunk 可以分到不同 commit（如 feat + chore）。

**展示格式**：

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

### Step 2.5: 输出 CommitPlan JSON

按 `SCHEMA.md` 格式输出完整 CommitPlan：

```json
{
  "version": 1,
  "commits": [
    { "type": "feat", "summary": "...", "files": [...] }
  ],
  "snapshot": {
    "files": [
      { "path": "...", "head_sha": "...", "hunks": [...] }
    ],
    "created_at": "<now>",
    "source": "commit-buddy"
  }
}
```

snapshot 的 hunks 内容通过运行 `git diff HEAD -- <path>` 并逐行解析获取，跳过 diff header（`diff --git` / `index` / `---` / `+++` 行）。

对每个有 diff 的文件：
1. 运行 `git diff HEAD -- <file>`
2. 跳过 diff header 行，直到遇到第一个以 `@@` 开头的行 → 这是 hunk 0
3. 每个 `@@` 行标志着一个新 hunk 的开始（从 `@@` 到下一个 `@@` 之前或文件尾）
4. 对每个 hunk 的完整内容（含 `@@` 行和所有 +/-/context 行）计算 SHA256 指纹

注意：diff header 行（`diff --git`、`index`、`--- a/`、`+++ b/`）不计入 hunk，hunk 编号从第一个 `@@` 行开始为 0。

**新文件（untracked）**：`git diff HEAD` 不会输出其内容，snapshot 中该文件的 hunks 设为空数组。

**完成标准**：CommitPlan JSON 已写入 `<项目根目录>/commit-plan.json`。

### Step 3: 确认粒度

向用户展示 Commit 计划和 CommitPlan JSON 文件路径，用 `ask_user_question` 一次性询问：

- **粒度是否合适？**（确认 / 太粗需要拆分 / 太细需要合并）
- 太粗或太细时，追问哪个 commit 需要调整
- 是否有 hunk 需要跳过不提？

迭代直到用户确认。

**完成标准**：用户回复确认。

### Step 4: 执行

```bash
bash <skill-dir>/scripts/execute-plan.sh <项目根目录>/commit-plan.json
```

**完成标准**：脚本执行完毕。检查 `plan-result.json` 的 `ok` 字段。

### Step 5: 汇报

读取 `plan-result.json`，向用户汇报：

- 每个 commit 的 SHA 和 message
- stash pop 结果
- 是否有未分配的 hunk
- 如果有错误，说明错误

最后展示 `git log --oneline -n <N>` 确认最终结果。

若 stash pop 有冲突，指出冲突文件并暂停。