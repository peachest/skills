---
name: mr-review-triage
description: 对 MR 的 OCR review inline discussion 进行拉取、分类、修复。手动触发。
disable-model-invocation: true
---

拉取 MR 中 OCR 产生的 inline discussion，分类为 TP/FP/Edge/OOS/Question，修复 TP 和选定的 Edge，贴标签回 MR。

mr-review-triage 是**状态机编排层**。代码分析（分类依据、影响面、设计意图）委托给 `code-review` skill。

## 分类体系

| 标记 | 分类 | 操作 |
| ---- | ---- | ---- |
| ✅ TP | 真实缺陷 | 需修复 |
| ❌ FP | 误判/设计意图 | 不处理 |
| 🟡 Edge | 真实但低优先级 | 可选修复 |
| 🔵 OOS | 预存代码/非本 MR | 不修 |
| ⏸️ Question | 不确定 | 停顿确认 |

TP 优先级：🚨 高（安全/崩溃）/ ⚠️ 中（逻辑/竞态）/ 🟢 低（清理/文档）。

## 前置条件

- MR 已创建，CI pipeline 已完成
- glab 已认证 gitblue.transwarp.io
- 当前分支与 MR source branch 一致

## 流程

### Step 1: 拉取

```bash
python3 scripts/ocr-pull-discussions.py <MR_ID> > /tmp/issues.json
```

输出字段：`discussion_id`、`file`、`line`、`body`。脚本内置去重（精确匹配 file+line+body）。

MR ID 未给时从分支名推导：

```bash
glab mr list --source-branch="$(git rev-parse --abbrev-ref HEAD)" -F json | jq '.[0].iid'
```

**完成标准**：JSON 数组就绪，已去重。

### Step 2: 分类

#### 2a. 预读 ADR

读取 `docs/adr/*.md`，提取架构决策摘要供匹配。

#### 2b. 预分类

脚本按 file pattern + `docs/agents/review-knowledge.md` 批量预分类，输出 `classified.json`。

条目格式：

```json
{
  "discussion_id": "abc...",
  "classification": "TP|FP|Edge|OOS|Question",
  "reason": "分类原因",
  "fix_plan": "修复方案（TP 必填）",
  "priority": "high|medium|low（TP 必填）",
  "adr": "关联 ADR 编号（FP 可选）",
  "resolved": true/false
}
```

`resolved` 的默认值：TP=False, FP=True, Edge=False, OOS=True, Question=False。Step 4 修复或跳过后，须为已处理的 TP 和 Edge 设 `"resolved": true`。

#### 2c. 分类决策树

对预分类不确定的 issue，逐级匹配：

1. 预存代码/非本 MR 变更范围 → 🔵 OOS
2. 无法确认 → ⏸️ Question
3. vendor/第三方代码 → 🟡 Edge (vendor)
4. 原型/实验性代码 → 🟡 Edge (prototype)
5. 代码已重构 → ❌ FP (already fixed)
6. 已知设计决策（有 ADR → `docs/adr/NNN-xxx.md`，无 ADR → design intent）→ ❌ FP
7. 风格/可读性 → 🟡 Edge (style)
8. 真实缺陷 → ✅ TP（附优先级）

委托 `code-review` 做 Standards + Spec 分析辅助判定。

#### 2d. 生成报告

输出 `mr-review-plan-<ID>.md`，含汇总表 + 详情。模板见 [`reference/templates.md`](reference/templates.md)。

**完成标准**：每项有 `classification` `reason`，报告已生成。

### Step 3: 确认

展示汇总表 + 每个 TP 修复方案。用户逐项确认分类和方案后，询问"是否进入 Step 4？"。

### Step 4: 修复

按 🚨 → ⚠️ → 🟢 顺序逐条。每条用 `ask_user_question` 工具提供结构化选项：

- **选项 1**：修复 — 直接按推荐方案修
- **选项 2**：深入讨论 — 委托 code-review 做双轴分析
- **选项 3**：跳过 — 补注释（FIXME/NOTE）或不做处理

每次只发一条 `ask_user_question`，等用户选择后再动手。用户主动给批量指令时例外。

#### 出口 1 — 修复

委托 `code-review` 分析影响面 → 编辑 → `go vet/build` → 展示 diff → 更新报告。

#### 出口 2 — 深入讨论

委托 `code-review` 做 Standards + Spec 双轴分析，展示报告 + 推荐方案 → 用户选方案。若最终转为 FP 且源码对应位置缺少解释设计意图的注释，补一行 `// NOTE:` 注释说明此处为何看似缺陷实为有意为之。

#### 出口 3 — 跳过

补注释：

| 前缀 | 场景 |
|------|------|
| `// FIXME:` | 真实待修复 |
| `// NOTE:` | 设计决策 |

---

TP 全部清完后处理 Edge：

先分组用 `ask_user_question` 让用户选子类别，再对展开的每条 Edge 发 `ask_user_question`：

- **选项 1**：修复
- **选项 2**：深入讨论
- **选项 3**：跳过+FIXME
- **选项 4**：判为 FP
- **选项 5**：保持 SKIP+NOTE

**完成标准**：所有 TP + 选定 Edge 已处理，报告已更新；已处理的 TP 和 Edge 在 classified.json 中设 `"resolved": true`（脚本据此 resolve discussion）。

### Step 5: 验证

```bash
go vet ./... && go build ./... && go test ./...
```

失败则标记 ❌ 修复失败。

### Step 6: 贴标签

**必须执行**，agent 不允许跳过。

```bash
cat classified.json | python3 scripts/ocr-post-labels.py <MR_ID>
```

输入即 Step 2b 的 `classified.json`。脚本自动生成分类标签并 resolve。格式见 [`reference/templates.md`](reference/templates.md)。

失败时逐条回退：`glab mr note create <MR_ID> --reply <id> -m "..."`。

### Step 7: 收尾

展示最终结果：修复成功/失败/跳过数、改动文件、未修复项。不自动 commit/push。

### Step 8: 反思

新 FP 模式 → `docs/agents/review-knowledge.md`，编码规范 → `docs/agents/coding-patterns.md`。没有则跳过。

## 检查点

| # | 时机 | 展示 | 决策 |
|---|------|------|------|
| 1 | Step 3 | 汇总表 + 分类理由 | 用户确认分类 |
| 2 | Step 3 | 每个 TP 方案 | 用户逐项确认 |
| 3 | Step 3 末 | "进入 Step 4？" | 用户确认 |
| 4 | 每条 TP | ask_user_question 三选一 | 修复/深入/跳过 |
| 5 | 深入讨论后 | 双轴报告 + 方案 | 用户选方案 |
| 6 | Edge 分组 | 子类别汇总 | 用户选组 |
| 7 | 每条 Edge | ask_user_question 五选一 | 修复/深入/FIXME/FP/SKIP |
| 8 | Step 5 后 | 验证结果 | 用户 approve → 贴标签 |
| 9 | Step 8 后 | 总结 + 更新文件 | 用户确认 |

## 参考

- [GitLab API 回退方案](reference/gitlab-api.md)
- [贴标签格式模板](reference/templates.md)
