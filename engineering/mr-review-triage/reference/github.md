# GitHub 操作参考

GitHub 平台的具体命令、API 端点和数据格式。

## 平台检测

远程地址含 `github.com` 时判定为 GitHub。环境变量：`GITHUB_REPOSITORY=owner/repo` 直接给定仓库（优先于 remote 推导；设置后认证探针跳过路径比对）、`OCR_REMOTE=<name>` 选哪个 remote 推导（默认 origin）、`OCR_PLATFORM=github` 强制平台。双实例/完整表：[gitlab.md 环境变量覆盖](gitlab.md#环境变量覆盖)。

```bash
git remote get-url origin
# git@github.com:owner/repo.git → GitHub
# https://github.com/owner/repo  → GitHub
```

## CLI 工具

使用 [`gh`](https://cli.github.com/) CLI。`gh` 在仓库中运行时自动推断 owner/repo。

认证要求：`gh auth login` 或设置 `GITHUB_TOKEN` / `GH_TOKEN` 环境变量。

## PR ID 推导

PR ID 未给时从分支名推导：

```bash
gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --json number --jq '.[0].number'
```

## 拉取 review comment

脚本自动使用 GitHub 后端：

```bash
python3 <SKILL_DIR>/scripts/ocr-pull-discussions.py <PR_NUMBER> > .triage/<PR_NUMBER>/issues.json
```

状态文件必须落在 `.triage/<PR_NUMBER>/issues.json`（verdict/post/verify 的 join 基底），不入 /tmp；CI 未完结时脚本 exit 2（pipeline 门）。流程编排见 triage-mr SKILL.md。

### GitHub review comment 数据结构

`gh api repos/{owner}/{repo}/pulls/{pr_number}/comments` 返回 JSON 数组，每个元素是一条 review comment：

```json
{
  "id": 12345678,
  "pull_request_review_id": 98765,
  "in_reply_to_id": null,
  "path": "path/to/file.go",
  "line": 50,
  "original_line": 50,
  "side": "RIGHT",
  "body": "issue text",
  "user": {"login": "github-actions[bot]", "type": "Bot"},
  "created_at": "2025-01-01T00:00:00Z"
}
```

### 线程模型

GitHub review comment 与 GitLab discussion 的关键差异：

| 概念 | GitLab | GitHub |
| ---- | ---- | ---- |
| 评论单元 | discussion（含 notes 数组） | review comment（单条） |
| 线程回复 | discussion 内的 notes | `in_reply_to_id` 链 |
| Resolve | `PUT /discussions/{id}` | GraphQL `resolveReviewThread` |
| 内联位置 | `notes[0].position.new_path/new_line` | `path` / `line` / `original_line` |

**线程根评论**：`in_reply_to_id == null` 的评论是线程根。有 `in_reply_to_id` 的是回复。

脚本将线程根评论映射为统一的 `{discussion_id, file, line, body, no}` 格式：

- `discussion_id` → review comment `id`（字符串）
- `file` → `path`
- `line` → `line`（fallback `original_line`）
- `body` → `body`
- `no` → 单轮 pull 文件内的去重后 API 首现序（1..N），verdict 落盘当场消费的临时指针；跨轮身份仍是 `discussion_id`

### 过滤规则

拉取 OCR bot 与人类评审者的 review comment（其他 bot 除外）：

| 类型 | 判定条件 | 是否进入 classified | 是否需 resolve |
| ---- | ---- | ---- | ---- |
| Inline issue（bot） | 作者为 `OCR_BOT_LOGIN` 配置的 bot，有 `path` + `line`，body 含具体问题 | ✅ | ✅（post-labels） |
| Inline issue（人类） | `user.type != "Bot"`，有 `path` + `line`，body 含具体问题 | ✅ | ✅（post-labels） |
| Fallback | body 以 `🔍 OpenCodeReview — issues` 开头 | ✅，解析子问题 | ✅（post-labels） |
| Summary | body 以 `🔍 OpenCodeReview found` 开头 | ❌（无 finding 可分类） | ✅（verify 门捕获） |
| LGTM | body 以 `✅ OpenCodeReview: No issues` 开头 | ❌ | ✅（verify 门捕获） |
| Error note | body 含 `⚠️ OpenCodeReview error` | ❌ | ✅（verify 门捕获） |

Summary/LGTM/Error 是 bot 状态通知，不含可分类的 finding，所以 pull 不拉取；但它们仍是 review thread，必须被 resolve。`ocr-verify-resolved.py` 是 closure gate，exit 0 才算 triage 完成。

Bot 识别：配置的 OCR bot（`OCR_BOT_LOGIN`，默认 `github-actions[bot]`）与人类（`type != "Bot"`）的评论都拉取；其他 bot（如 `dependabot[bot]`）的状态通知被丢弃。人类 inline 评论必须拉取——closure gate 统计所有未 resolve 的 review thread，与作者无关，若 pull 只收 bot 会重现 "0 findings 但 gate 报 open" 的错位。

### Fallback note 解析

格式与 GitLab 相同，见 [GitLab 参考 — Fallback note 解析](gitlab.md#fallback-note-解析)。

### 分页

`gh api` 自动处理分页（`--paginate` flag）。手动分页时检查 `Link` header 中的 `rel="next"`。

## 贴标签 + resolve conversation

脚本自动使用 GitHub 后端：

```bash
python3 <SKILL_DIR>/scripts/ocr-post-labels.py <PR_NUMBER> --mode triage \
  --classified .triage/<PR_NUMBER>/classified.json
```

`--mode triage` 的模式映射只兜底没有 per-item `resolved` 字段的旧条目；现行流程下每条是否 resolve 由 `verdict.py` 在 verdict 时刻写入 per-item `resolved`，post 只执行不重判。join + anchor 校验、内容判重、reply 失败不 resolve、OCR summary 线程扫尾（⚠️ error 只回帖永不 resolve，gate 永红为有意设计）与 posted 回写均在脚本内完成——无手动回退路径，脚本出错 = 修脚本或上报。

### 回复与 resolve 的 ID 空间

REST 回复目标是 comment databaseId，GraphQL resolve 目标是 thread node id——两个不可互换的 ID 空间。脚本在同一次 reviewThreads 读取内解析两者：任何 node id 都不进入 REST 路径，`ocr-verify-resolved.py --json` 输出的 thread node id 也不被消费。GraphQL resolve 的机制：

```bash
# 1. 获取 review thread node_id（需要 pull_request_review_id + comment_id）
#    通过 GraphQL 查询 PR 的 review threads
gh api graphql -f query='
query($pr: ID!) {
  node(id: $pr) {
    ... on PullRequest {
      reviewThreads(first: 100) {
        nodes { id isResolved comments(first: 1) { nodes { databaseId } } }
      }
    }
  }
}' -F pr="<PR_NODE_ID>"

# 2. Resolve thread
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { isResolved }
  }
}' -F threadId="<THREAD_NODE_ID>"
```

脚本内部完成上述 GraphQL resolve（含查不到 thread 时不再静默返回成功的修复）。

## 收尾验证（closure gate）

post-labels 返回 ok 不等于 triage 完成。OCR summary/LGTM/error 线程不在 classified.json 里，由 post 的扫尾逻辑处理（见上节）。必须跑 closure gate：

```bash
python3 <SKILL_DIR>/scripts/ocr-verify-resolved.py <PR_NUMBER>
# exit 0 = 全部 resolved（且 head CI 已完结）；exit 1 = 有残留或后端错误（fail closed，列在 stderr）；
# exit 2 = check runs 未完结（--skip-pipeline-check 覆盖）或用法错误
```

人读输出以序号/内容锚标注线程、不出现平台 id；残留 ⚠️ error 线程使 gate 保持红——有意的 human-in-loop 设计，上报用户裁决，不得自行 resolve 凑绿。

## API 端点参考

| 操作 | 端点 |
| ---- | ---- |
| 列出 review comments | `GET /repos/{owner}/{repo}/pulls/{pr_number}/comments` |
| 创建 review comment | `POST /repos/{owner}/{repo}/pulls/{pr_number}/comments` |
| 回复 review comment | `POST /repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies` |
| 列出 reviews | `GET /repos/{owner}/{repo}/pulls/{pr_number}/reviews` |
| 创建 review | `POST /repos/{owner}/{repo}/pulls/{pr_number}/reviews` |
| Resolve thread | `POST /graphql`（`resolveReviewThread` mutation） |

## 环境变量

| 变量 | 用途 |
| ---- | ---- |
| `GITHUB_TOKEN` / `GH_TOKEN` | GitHub 认证 |
| `OCR_BOT_LOGIN` | OCR bot 的 login（默认 `github-actions[bot]`）；人类评论始终拉取 |
