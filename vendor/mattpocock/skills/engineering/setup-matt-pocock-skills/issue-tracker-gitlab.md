# Issue tracker: GitLab

Issue 和 PRD 作为 GitLab issue 存储在对应仓库中。使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI 进行所有操作。

Remote: `<YOUR_GITLAB_REMOTE>`

## 约定

- **创建 issue**：`glab issue create --title "..." --description "..." --assignee @me`。多行描述使用 shell 变量传值`,`避免 `--description -` 触发编辑器。
- **读取 issue**：`glab issue view <number> --comments`。使用 `-F json` 获取机器可读输出。
- **列出 issue**：`glab issue list -F json`，配合 `--label` 过滤。
- **评论 issue**：`glab issue note <number> --message "..."`。GitLab 将评论称为 "notes"。
- **添加/移除标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签用逗号分隔或重复参数。
- **关闭**：**禁止** agent 直接调用 `glab issue close` 或 API 关闭 issue。所有 issue 必须通过 git commit message 关闭：在 commit body 或 MR description 中使用 closing pattern（`Closes #n` / `Fixes #n` / `Resolves #n` 等，全集见「自动关闭的边界」段），push/merge 到**默认分支**后 GitLab 自动 close。**仓库工作分支非默认分支时自动关闭永不触发**，此时 merge 后验证 + 手动关闭是常态而非例外（详见「自动关闭的边界」段）。关闭前 issue 应已标记 `status::resolved`（详见「状态管理」段），无需额外清理标签。**例外 1**：Map issue（`wayfinder:map`）无对应代码变更，全部子 ticket commit close 后，在创建 MR 时通过 MR description 中的 `Closes #<map>` 关闭。**例外 2**：MR merge 后 GitLab 未自动关闭（工作分支非默认分支、漏写 closing pattern 或 GitLab 未触发），agent 手动 `glab issue close <n>`（先 note 记录原因）。详见 MR 约定段的「merge 后验证」。
- **更新 issue body**：`glab issue update <n> --description "..."` 是**覆盖式**更新，不是 append。修一个 typo 也要传完整 body。heredoc 传多行：`--description "$(cat <<'EOF'\n...\nEOF\n)"`。
- **Merge Request**：GitLab 将 PR 称为 "merge request"。使用 `glab mr create`、`glab mr view`、`glab mr note` 等。

`glab` 在仓库中运行时自动推断项目。

## 自动关闭的边界（默认分支限制）

GitLab 官方规则：closing pattern 引用的 issue **仅在以下两种情况自动关闭**：

1. 含 closing pattern 的 **commit push 到默认分支**；
2. 含 closing pattern 的 **commit 或 MR merge 进默认分支**。

合入其他分支（如 `dev`）只产生 "mentioned in ..." 系统 note，**永不关闭** issue。

### Closing pattern 全集

关键词（含首字母大写/全小写两种形式）：`Close(s|d|ing)`、`Fix(es|ed|ing)`、`Resolve(s|d|ing)`、`Implement(s|ed|ing)`。

引用格式：本地 `#123`、跨项目 `group/project#123`、issue 完整 URL。

注意：`Related to #n`、`Part of #n` 只建立关联/mention，**不关闭** issue。

### 项目初始化检查（每个仓库必做）

```bash
glab api "projects/<PROJECT_ID>" | jq -r '.default_branch'
# 对照实际工作分支（MR target branch）
```

工作分支 ≠ 默认分支时，在 map 的 Notes 段记录这一事实，并选用以下策略之一：

| 策略 | 适用 | 做法 |
|------|------|------|
| MR 直指默认分支 | trunk-based 仓库 | 正常写 `Closes #n`，自动关闭可用 |
| 最终同步 MR 汇总 | 阶段性 dev→默认分支 回流 | 工作分支 MR 不期待关闭；回流 MR description 汇总全部 `Closes #n` |
| merge 后手动关闭 | 长期双分支仓库（如 HAMi：默认 `master`、工作 `dev`） | 每次 MR merge 后验证未关闭则手动 close（note 原因 + `glab issue close`） |

### 项目设置例外

项目设置「Settings → Repository → Branch defaults → Auto-close referenced issues on default branch」被取消勾选时，即使在默认分支上也不自动关闭。诊断自动关闭失效时除检查分支外还需排除此项。

## 状态管理

Ticket 执行状态用 GitLab **scoped label**（`status::` 前缀）管理。同一 scope 下互斥——添加新 label 时 GitLab 自动移除同 scope 旧 label，状态转换无需手动删除。

### 三个状态

| Label | 含义 | 配色 |
|-------|------|------|
| `status::open` | 已创建，未认领 | `#00aa00` 绿 |
| `status::claimed` | 已认领，执行中 | `#ffaa00` 黄 |
| `status::resolved` | 工作完成，待 commit close | `#6699cc` 蓝 |

`wontfix` 是 triage 维度的扁平 label，不属于 `status::` scope。Map issue 不打 status——其状态由子 ticket 聚合，关闭靠 GitLab 原生 closed。

### Setup（每个项目执行一次）

```bash
glab api "projects/<PROJECT_ID>/labels" -X POST -F "name=status::open"    -F "color=#00aa00"
glab api "projects/<PROJECT_ID>/labels" -X POST -F "name=status::claimed"  -F "color=#ffaa00"
glab api "projects/<PROJECT_ID>/labels" -X POST -F "name=status::resolved" -F "color=#6699cc"
```

### 状态转换

**创建 ticket → `status::open`**：创建时即打。后续 claim/resolve 靠 scoped 互斥自动替换。

**认领（open → claimed）**：assignee + `status::claimed` 同时设——assignee 管归属，label 管状态。

```bash
glab issue update <n> --assignee @me --label status::claimed
```

**解决（claimed → resolved）**：工作完成时设置。顺序：note 记录答案 → 设 `status::resolved` → commit `Closes #n`。

```bash
glab issue note <n> --message "<answer>"
glab issue update <n> --label status::resolved
# 然后 git commit -m "...\n\nCloses #n"
```

`status::resolved` 在 commit 创建时即设，填补「工作完成 → push/merge 关闭」之间的可见性盲区。issue 被 GitLab 自动关闭后 `status::resolved` 残留不清除——closed 是终态。

### Frontier 查询

Frontier = `status::open` + 未认领（无 assignee） + 未阻塞（`Blocked by` 行无开放 issue）。

```bash
glab issue list --label status::open -F json
# 再过滤：无 assignee + body 中 Blocked by 行无开放 issue
```

### 废弃 in-progress

旧的扁平 `in-progress` label 已被 `status::claimed` 取代。迁移存量 issue 后删除该 label：

```bash
# 查找所有打了 in-progress 的 open issue
glab issue list --label in-progress -F json | jq '.[].iid'
# 逐个替换
glab issue update <n> --label status::claimed
glab api "projects/<PROJECT_ID>/labels/in-progress" -X DELETE
```

### 过时 ticket 清理

停滞项目会遗留大量已失效的 open issue（map 停滞、目标分支从未落地、决策已废弃）。清理流程：

1. **盘点**：`glab issue list -F json` 列出全部 open issue，按 map 分组，对照各 map 的 Decisions-so-far 和分支实际存在性（`glab api "projects/<PROJECT_ID>/repository/branches"`）判断哪些已停滞。
2. **区分**：已完成但未关闭（如非默认分支 MR 合入后漏关）→ 手动关闭补账；项目停滞/废弃 → 与用户确认处置（全关、保留部分、逐个审查）。
3. **执行**：批量 close 前先向用户确认范围和方式（是否留 note、是否打 `wontfix`）。已停滞项目至少在 map 上留一条 note 说明废弃原因，子 ticket 可直接关闭。
4. **验证**：清理后重新 `glab issue list`，确认仅剩有效 ticket。

## CI/CD 操作 — Pipeline 与 Job 查询

- **列出 pipeline**：`glab ci list`。按 MR 过滤：`glab ci list 2>&1 | grep "merge-requests/<n>/head"`
- **查看 pipeline 状态**：`glab api "projects/<PROJECT_ID>/pipelines/<id>" | jq -r '.status'`
- **查看 pipeline 的 job 列表**：`glab api "projects/<PROJECT_ID>/pipelines/<id>/jobs" | jq -r '.[] | "\(.name) | \(.status) | \(.web_url)"'`
- **查看 job 日志**：`glab api "projects/<PROJECT_ID>/jobs/<job_id>/trace"`
- **轮询 pipeline 完成**：`while true; do status=$(glab api "projects/<PROJECT_ID>/pipelines/<id>" | jq -r '.status'); echo "$(date +%H:%M:%S) pipeline status: $status"; [ "$status" = "success" ] || [ "$status" = "failed" ] && break; sleep 15; done`（timeout 600s）
- **JSON 过滤**：管道外部 `jq`：`glab api "..." | jq -r '...'`

project_id 为 `<PROJECT_ID>`（见 `glab api projects` 或仓库设置）。Pipeline ID 和 Job ID 是全局唯一的，不等于 issue IID。

## Issue linking

- **创建 issue link 返回 409**：`Part of #<map>` 在 body 中已自动建立 `relates_to` 关联，手动 link 是冗余操作。遇到 409 直接忽略。

## MR 作为 triage 来源

**MR 作为 triage 来源：否。**

## 当技能说"发布到 issue tracker"

创建 GitLab issue。

## 当技能说"获取相关 ticket"

运行 `glab issue view <number> --comments`。

## 导航操作 — Used by /skill:wayfinder

**Map** 是带有子 issue 的单一 issue。

- **Map**：标记为 `wayfinder:map` 的单一 issue，包含 Notes / Decisions-so-far / Fog 正文。`glab issue create --label wayfinder:map`。**Map 不会因子 issue 关闭而自动关闭，需子 issue 全部 commit close 后，在创建 MR 时通过 MR description `Closes #<map>` 关闭。**
- **子 ticket**：描述顶部包含 `Part of #<map>` 且标签为 `wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）的 issue。领取后分配给执行开发者。
- **Blocking**：GitLab 无原生 blocking link，通过 issue body **第二行**（紧跟 `Part of`）的 `Blocked by: #<n>, #<m>` 文本 + 双向 `relates_to` 链接联合表达。当所有阻塞 issue 关闭后，ticket 解除阻塞。Body 格式：

  ```markdown
  Part of #<map>
  Blocked by: #<n>, #<m>

  ## What to build
  ...
  ```

  双向 `relates_to` link：

  ```bash
  # 链接子 issue 到 map
  glab api "projects/<PROJECT_ID>/issues/<child_iid>/links" \
    -X POST \
    -F "target_project_id=<PROJECT_ID>" \
    -F "target_issue_iid=<map_iid>" \
    -F "link_type=relates_to"

  # 查看 issue 的所有链接
  glab api "projects/<PROJECT_ID>/issues/<iid>/links"
  ```

- **Frontier 查询**：`glab issue list --label status::open -F json`，再过滤无 assignee + 未阻塞。详见「状态管理」段。
- **领取**：`glab issue update <n> --assignee @me --label status::claimed`。详见「状态管理」段。
- **解决**：先 `glab issue note <n> --message "<answer>"` 记录结果，再 `glab issue update <n> --label status::resolved` 标记完成，然后通过 commit message（`Closes #n`）关闭，最后将上下文指针追加到 map 的 Decisions-so-far。禁止直接调用 `glab issue close`，必须走 git commit 方式关闭。详见「状态管理」段。

## 实现操作 — Used by /skill:implement

- **前置检查**：实现任何 ticket 前，必须先加载 `/skill:tdd` skill 并评估是否适用。若 ticket 涉及非 trivial 逻辑（分支、循环、parser、money/security 路径），必须走 TDD 流程。仅纯声明式代码（常量定义、类型别名、纯转发方法）可跳过。
- **实现节奏**：一 ticket → note → `status::resolved` → 一 commit `Closes #n`。禁止一个 commit 关闭多个 ticket，也禁止一个 ticket 代码分散在多个 commit 中不打标。状态转换详见「状态管理」段。
- **测试门槛**：即使 ticket AC 只写了"编译通过"，也必须按 seams 写至少一个测试。AC 弱不代表不需要测试——没有测试的代码是债务，不因 AC 省略而豁免。

## 发券操作 — Used by /skill:to-tickets

- **创建评审 gate**：ticket 创建后，**先暂停**让用户评审粒度是否合适。评审通过前**不得** link 或 assign。

## Merge Request 约定

Agent 不主动创建 MR。用户说"提交 MR"或"创建 merge request"时，按以下规则操作：

- **时机**：一个 Map 的所有子 ticket 全部实现并 commit close 后。
- **MR 数量**：一个 Map 一个 MR。禁止多 Map 合并发 MR。
- **描述**：包含 Map 链接、已完成子 ticket 列表、`Closes #<map>`。
- **命令**：`glab mr create --title "<map title>" --description "$(cat <<'EOF'\n参见 #<map>。\n\n子 ticket：\n- #<n> <title>\n- #<m> <title>\n\nCloses #<map>\nEOF\n)" --target-branch main`。
- **确认**：创建前必须向用户展示 MR 描述并等待确认。
- **关闭 Map**：merge 后 GitLab 根据 MR description 中的 `Closes #<map>` 自动关闭（仅当 MR 目标分支为默认分支，见「自动关闭的边界」段）。
- **merge 后验证**：merge 完成后，agent 必须对 MR description 中所有 closing pattern 引用的 issue（含 Map 和子 ticket）运行 `glab api "projects/<PROJECT_ID>/issues/<iid>" | jq -r '.state'` 确认已 closed。若仍为 opened——常见原因：仓库工作分支非默认分支（GitLab 必然不触发，见「自动关闭的边界」段）、MR description 漏写 closing pattern——则手动关闭：先 `glab issue note <n> --message "..."` 记录原因，再 `glab issue close <n>`。此为 `glab issue close` 禁令的**第二例外**（第一例外见下文关闭约定）。

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

- 对标源码 / ADR / 相关 MR
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

### 对 mr background 的影响

mr 时可以根据 issue 信息构造背景信息：丢弃 `Part of` / `Blocked by` 顶行、`## References`、Map 的 `Notes` / `Decisions so far`。其余段落全部保留，段头未来变更不影响 OCR。
