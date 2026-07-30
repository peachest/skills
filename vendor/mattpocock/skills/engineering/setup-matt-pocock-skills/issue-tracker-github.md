# Issue tracker: GitHub (Internal)

Issue 和 PRD 作为 GitHub issue 存储在对应仓库中。使用 [`gh`](https://cli.github.com/) CLI 进行所有操作。

Remote: `github.internal.example.com/org/repo.git`

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行 body 使用 shell heredoc：`--body "$(cat <<'EOF'\n...\nEOF\n)"`。
- **读取 issue**：`gh issue view <number> --comments`。使用 `--json` 获取机器可读输出。
- **列出 issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，配合 `--label` 和 `--state` 过滤。
- **评论 issue**：`gh issue comment <number> --body "..."`。
- **添加/移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`。多个标签用逗号分隔：`--add-label "wayfinder:map,triage"`。
- **关闭**：**禁止** agent 直接调用 `gh issue close` 或 API 关闭 issue。所有 issue 必须通过 git commit message 关闭：在 commit body 或 PR description 中使用 `Closes #n` / `Fixes #n` / `Resolves #n`，push 到默认分支后 GitHub 自动 close。关闭前通过 `gh issue edit <number> --remove-label "in-progress,ready-for-agent"` 清理工作流标签。**唯一例外**：Map issue（`wayfinder:map`）无对应代码变更，全部子 ticket commit close 后，在创建 PR 时通过 PR description 中的 `Closes #<map>` 关闭。
- **更新 issue body**：`gh issue edit <number> --body "..."` 是**覆盖式**更新，不是 append。修一个 typo 也要传完整 body。heredoc 传多行：`--body "$(cat <<'EOF'\n...\nEOF\n)"`。
- **Pull Request**：使用 `gh pr create`、`gh pr view`、`gh pr comment` 等。

`gh` 在仓库中运行时自动推断项目（通过 `git remote`）。

## PR 作为 triage 来源

**PR 作为 triage 来源：否。**

## 当技能说"发布到 issue tracker"

创建 GitHub issue。

## 当技能说"获取相关 ticket"

运行 `gh issue view <number> --comments`。

## 导航操作 — Used by /skill:wayfinder

**Map** 是带有子 issue 的单一 issue。

- **Map**：标记为 `wayfinder:map` 的单一 issue，包含 Notes / Decisions-so-far / Fog 正文。`gh issue create --label wayfinder:map`。**Map 不会因子 issue 关闭而自动关闭，需子 issue 全部 commit close 后，在创建 PR 时通过 PR description `Closes #<map>` 关闭。**
- **子 ticket**：描述顶部包含 `Part of #<map>` 且标签为 `wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）的 issue。领取后分配给执行开发者。
- **Blocking**：使用 GitHub **原生 issue dependencies**。通过 API 添加阻塞关系：

  ```bash
  # 获取 blocker 的数据库 ID（不是 issue number）
  BLOCKER_DB_ID=$(gh api repos/:owner/:repo/issues/<blocker_number> --jq .id)

  # 添加 blocked_by 依赖
  gh api --method POST repos/:owner/:repo/issues/<child_number>/dependencies/blocked_by \
    -F issue_id=$BLOCKER_DB_ID
  ```

  `gh api` 的退出码区分三类故障，处理策略不同：

  | 状况 | 表现 | 处理 |
  |------|------|------|
  | **503 / 502** (Service Unavailable) | `gh api` exit code 22，stderr 含 `Service Unavailable` | **重试**（最多 3 次，间隔 3s）。这是暂时性故障，不是功能缺失 |
  | **404 / 403** (Not Found / Forbidden) | exit code 22，HTTP 状态码 4xx | **回退**到 body 文本。端点不存在或无权限，重试无意义 |
  | **exit code 2** (用法错误) | stderr 含 `unknown command` 或 `flag needs an argument` | **修命令语法**。不是 API 问题，重试和回退都不会解决 |

  GitHub 的 `issue_dependencies_summary.blocked_by` 只返回**开放中的** blocker（即实时门控）。当 dependencies API 返回 404/403（端点不可用或无权限）时，回退到 body **第二行**（紧跟 `Part of`）的 `Blocked by: #<n>, #<m>` 文本。当所有阻塞 issue 关闭后，ticket 解除阻塞。Body 格式：

  ```markdown
  Part of #<map>
  Blocked by: #<n>, #<m>

  ## What to build
  ...
  ```

- **查询子 ticket**：**不要使用** `repos/:owner/:repo/issues/<n>/sub-issues` REST 端点——该端点不存在。GitHub sub-issues 功能没有公开的 REST API。改为通过以下方式获取子 ticket 列表：

  1. **首选**：`gh issue list --search "in:title \"Part of #<map>\"" --json number,title,labels,assignees,state` — 按 body 文本 `Part of #<map>` 搜索子 ticket
  2. **备选**：`gh issue view <map_number> --json subIssues` — 如果仓库开启了 sub-issues 功能，issue 对象上的 `subIssues` 字段会返回子 issue 列表（只读 summary，非独立端点）
  3. **兜底**：从 map body 的 task list / Decisions-so-far 文本中解析链接

  实际操作中，路径 1（body 文本搜索）是**最可靠的**主路径，因为 `Part of #<map>` 是所有子 ticket body 的约定首行。

- **Frontier 查询**：列出 map 的子 ticket（通过上述查询路径），排除 `Blocked by` 行中仍有开放 issue 的 ticket，或已分配人的 issue。
- **领取**：`gh issue edit <n> --add-assignee "@me"`。
- **解决**：先 `gh issue comment <n> --body "<answer>"` 记录结果，然后通过 commit message（`Closes #n`）关闭，最后将上下文指针追加到 map 的 Decisions-so-far。禁止直接调用 `gh issue close`，必须走 git commit 方式关闭。

## 实现操作 — Used by /skill:implement

- **前置检查**：实现任何 ticket 前，必须先加载 `/skill:tdd` skill 并评估是否适用。若 ticket 涉及非 trivial 逻辑（分支、循环、parser、money/security 路径），必须走 TDD 流程。仅纯声明式代码（常量定义、类型别名、纯转发方法）可跳过。
- **实现节奏**：一 ticket → 一 commit → 一 `Closes #n`。禁止一个 commit 关闭多个 ticket，也禁止一个 ticket 代码分散在多个 commit 中不打标。
- **测试门槛**：即使 ticket AC 只写了"编译通过"，也必须按 seams 写至少一个测试。AC 弱不代表不需要测试——没有测试的代码是债务，不因 AC 省略而豁免。

## 发券操作 — Used by /skill:to-tickets

- **创建评审 gate**：ticket 创建后，**先暂停**让用户评审粒度是否合适。评审通过前**不得** link 或 assign。

## Pull Request 约定

Agent 不主动创建 PR。用户说"提交 PR"或"创建 pull request"时，按以下规则操作：

- **时机**：一个 Map 的所有子 ticket 全部实现并 commit close 后。
- **PR 数量**：一个 Map 一个 PR。禁止多 Map 合并发 PR。
- **描述**：包含 Map 链接、已完成子 ticket 列表、`Closes #<map>`。
- **命令**：`gh pr create --title "<map title>" --body "$(cat <<'EOF'\n参见 #<map>。\n\n子 ticket：\n- #<n> <title>\n- #<m> <title>\n\nCloses #<map>\nEOF\n)" --base main`。
- **确认**：创建前必须向用户展示 PR 描述并等待确认。
- **关闭 Map**：merge 后 GitHub 根据 PR description 中的 `Closes #<map>` 自动关闭。

## Issue 模板

四种模板，覆盖 `/skill:to-spec`（spec）、`/skill:wayfinder`（map + decision ticket）、`/skill:to-tickets`（task）。模板以外的段落按内容保留（denylist 策略，机器友好）。

### 核心哲学

- **Spec**：对话综合产物，不写文件路径和代码（prototype 决策片段例外）。唯一 seams 来源，ticket 通过 `Part of` 继承。
- **Task ticket**：tracer-bullet 垂直切片，做完即交付。验收标准可机械验证，禁止写代码或文件路径。
- **Decision ticket**：只有一个问题，答案记在 resolution comment，不进 body。
- **Map**：索引不是仓库，决策只活在 ticket 里。

---

### 模板 1：Spec（`/skill:to-spec`）

适用 `to-spec` 或其他产生 PRD 的场景。标签：`ready-for-agent`。

```markdown
## Problem

用户/系统视角的问题。为什么现状不行。

## Solution

解法的形态，架构方向、对标物。

## Implementation Decisions

- 已敲定的技术决策：模块、接口、schema、契约
- 不写具体文件路径和代码（prototype 产出的决策性片段例外，裁剪到核心）

## Testing Decisions

- 在哪个 seam 测
- 参考现有哪类测试（prior art）

## Out of scope

本 spec 明确不做的。

## References

- 对标源码 / ADR / 相关 PR
```

### 模板 2：Map（`/skill:wayfinder`）

标记 `wayfinder:map`。段头严格按 `/skill:wayfinder` skill，不做变更。

```markdown
## Destination

<到达终点意味着什么——spec、决策或代码变更。一两行。>

## Notes

<领域知识、每个 session 应查阅的 skill、此期间的偏好。>

## Decisions so far

<!-- 索引——每行一个已关闭 ticket：要点 + 链接（答案在 tiket 的 resolution comment 中） -->

- [closed ticket title](link) — 一句话要点

## Not yet specified

<!-- 范围内的迷雾，目前还不能 ticketed -->

## Out of scope

<!-- 超出 destination 边界的工作 -->
```

### 模板 3：Task ticket（`/skill:to-tickets`）

标签按 `/skill:to-tickets` 或 `/skill:wayfinder` 约定。顶行 `Blocked by` 是 frontier 查询的 grep 目标，不得改成段落。

```markdown
Part of #<parent spec or map>
Blocked by: #<n>, #<m>

## What to build

端到端行为，做完后哪条路径能跑通。允许 ### 子结构。

## Acceptance criteria

- [ ] 可机械验证的标准（build/test 通过、符号存在/消失、输出匹配预期）

## Out of scope

本 ticket 故意不碰的。

## Testing

<!-- 可选。仅当无父 spec 或偏离其 Testing Decisions 时填写。 -->

在哪个 seam 测；参考现有哪类测试（prior art）。
```

### 模板 4：Decision ticket（`/skill:wayfinder`）

标记 `wayfinder:research` / `wayfinder:prototype` / `wayfinder:grilling` / `wayfinder:task`（非执行模式）。**答案记在 resolution comment，不改 body。**

```markdown
Part of #<map>
Blocked by: #<n>

## Question

这个 ticket 要解决的决策或调查。
```

### 对 PR background 的影响

PR 时可以根据 issue 信息构造背景信息：丢弃 `Part of` / `Blocked by` 顶行、`## References`、Map 的 `Notes` / `Decisions so far`。其余段落全部保留，段头未来变更不影响 OCR。
