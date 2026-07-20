---
name: commit-buddy
description: git commit 伙伴——当用户提到 commit、提交、commit message、提交信息、变更分组、提交计划、conventional commits 时触发。
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

### Step 2.5: 输出方案并生成 CommitPlan

按 `SCHEMA.md` 中的简化方案格式输出 commit 分组（只含语义信息，不需要计算指纹）：

```json
{
  "version": 1,
  "commits": [
    {
      "type": "feat",
      "scope": "auth",
      "summary": "...",
      "files": [
        { "path": "...", "hunks": "all" },
        { "path": "...", "hunks": [0, 2] }
      ]
    }
  ]
}
```

写入临时文件后，调用脚本自动补全 snapshot（hunk 指纹、HEAD sha）：

```bash
mkdir -p <PROJECT_DIR>/.pi/commit-buddy
# 将方案 JSON 写入 <PROJECT_DIR>/.pi/commit-buddy/input.json
bash <skill-dir>/scripts/generate-plan.sh <PROJECT_DIR>/.pi/commit-buddy/input.json
```

脚本输出完整 CommitPlan 到 `<PROJECT_DIR>/.pi/commit-buddy/plan.json`。

**完成标准**：`plan.json` 已生成。

### Step 3: 确认粒度

向用户展示 Commit 计划，用 `ask_user_question` 一次性询问：

- **粒度是否合适？**（确认 / 太粗需要拆分 / 太细需要合并）
- 太粗或太细时，追问哪个 commit 需要调整
- 是否有 hunk 需要跳过不提？

迭代直到用户确认。用户确认后直接进入 Step 4，不需要重新生成 plan.json（execute-plan.sh 会在执行前校验指纹，如果确认期间代码被改动会中止）。

**完成标准**：用户回复确认。

### Step 4: 执行

```bash
bash <skill-dir>/scripts/execute-plan.sh <PROJECT_DIR>/.pi/commit-buddy/plan.json
```

**完成标准**：脚本执行完毕。检查 `<PROJECT_DIR>/.pi/commit-buddy/result.json` 的 `ok` 字段。

### Step 5: 汇报

读取 `<PROJECT_DIR>/.pi/commit-buddy/result.json`，向用户汇报：

- 每个 commit 的 SHA 和 message
- stash pop 结果
- 是否有未分配的 hunk
- 如果有错误，说明错误

最后展示 `git log --oneline -n <N>` 确认最终结果。

若 stash pop 有冲突，指出冲突文件并暂停。

### Step 6: 清理

删除 `<PROJECT_DIR>/.pi/commit-buddy/` 目录：

```bash
rm -rf <PROJECT_DIR>/.pi/commit-buddy/
```

**完成标准**：中间产物已清理。