# GitHub 操作参考

GitHub 平台的具体命令、API 端点和数据格式。

## 平台检测

远程地址含 `github.com` 时判定为 GitHub。

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
python3 <SKILL_DIR>/scripts/ocr-pull-discussions.py <PR_NUMBER> > /tmp/issues.json
```

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

脚本将线程根评论映射为统一的 `{discussion_id, file, line, body}` 格式：

- `discussion_id` → review comment `id`（字符串）
- `file` → `path`
- `line` → `line`（fallback `original_line`）
- `body` → `body`

### 过滤规则

只保留 OCR bot 发出的 review comment：

| 类型 | 判定条件 | 是否进入 classified | 是否需 resolve |
| ---- | ---- | ---- | ---- |
| Inline issue | `user.type == "Bot"`，有 `path` + `line`，body 含具体问题 | ✅ | ✅（post-labels） |
| Fallback | `user.type == "Bot"`，body 以 `🔍 OpenCodeReview — issues` 开头 | ✅，解析子问题 | ✅（post-labels） |
| Summary | body 以 `🔍 OpenCodeReview found` 开头 | ❌（无 finding 可分类） | ✅（verify 门捕获） |
| LGTM | body 以 `✅ OpenCodeReview: No issues` 开头 | ❌ | ✅（verify 门捕获） |
| Error note | body 含 `⚠️ OpenCodeReview error` | ❌ | ✅（verify 门捕获） |

Summary/LGTM/Error 是 bot 状态通知，不含可分类的 finding，所以 pull 不拉取；但它们仍是 review thread，必须被 resolve。`ocr-verify-resolved.py` 是 closure gate，exit 0 才算 triage 完成。

Bot 识别：GitHub Actions bot 的 login 为 `github-actions[bot]`，`type` 为 `Bot`。如使用其他 bot（如自定义 App），在环境变量 `OCR_BOT_LOGIN` 中指定。

### Fallback note 解析

格式与 GitLab 相同，见 [GitLab 参考 — Fallback note 解析](gitlab.md#fallback-note-解析)。

### 分页

`gh api` 自动处理分页（`--paginate` flag）。手动分页时检查 `Link` header 中的 `rel="next"`。

## 贴标签 + resolve conversation

脚本自动使用 GitHub 后端：

```bash
cat .triage/<PR_NUMBER>/classified.json | python3 <SKILL_DIR>/scripts/ocr-post-labels.py <PR_NUMBER> --mode triage
```

`--mode triage` 让 TP（真阳性）也 resolve——fix 已在本 run 落地并验证。Edge/Question 保持 open。

### 回复 review comment

```bash
gh api -X POST repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments/<comment_id>/replies \
  -f body="..."
```

### Resolve conversation

GitHub 的 resolve 操作需要通过 **GraphQL API** 完成。REST API 不直接支持 resolve。

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

脚本内部处理 GraphQL resolve 逻辑。如脚本不支持 resolve，则仅贴标签，不 resolve。

## 收尾验证（closure gate）

post-labels 返回 ok 不等于 triage 完成。OCR summary/LGTM/error discussion 不在 classified.json 里，post-labels 不会 resolve 它们，但它们仍是 review thread。必须跑 closure gate：

```bash
python3 <SKILL_DIR>/scripts/ocr-verify-resolved.py <PR_NUMBER>
# exit 0 = 全部 resolved；exit 1 = 有残留（列在 stderr）
```

残留线程手动回复 + resolve（GraphQL）：

```bash
# 1) 回复
gh api -X POST repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments/<comment_id>/replies \
  -f body="✅ 已修复（commit <hash>）：..."
# 2) resolve thread（需先查 review thread node_id，见上）
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { isResolved }
  }
}' -F threadId="<THREAD_NODE_ID>"
```

重跑 verify 直到 exit 0。

### 回退命令

脚本失败时逐条回退：

```bash
gh pr comment <PR_NUMBER> --body "..."  # 普通 PR comment
# 或回复 review comment thread：
gh api -X POST repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments/<comment_id>/replies \
  -f body="..."
```

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
| `OCR_BOT_LOGIN` | OCR bot 的 login（默认 `github-actions[bot]`） |
