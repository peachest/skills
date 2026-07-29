# GitLab 操作参考

GitLab 平台的具体命令、API 端点和数据格式。

## 平台检测

远程地址含 `gitlab.com` 或自建 GitLab 实例（如 `internal.example.com`）时判定为 GitLab。

```bash
git remote get-url origin
# git@gitlab.com:ns/proj.git          → GitLab
# git@internal.example.com:ns/proj.git → GitLab (self-hosted)
```

## CLI 工具

使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。`glab` 在仓库中运行时自动推断项目。

认证要求：`glab auth login` 或设置 `GITLAB__PERSONAL_ACCESS_TOKEN` + `CI_SERVER_URL` 环境变量。

## MR ID 推导

MR ID 未给时从分支名推导：

```bash
glab mr list --source-branch="$(git rev-parse --abbrev-ref HEAD)" -F json | jq '.[0].iid'
```

## 拉取 review discussion

脚本自动使用 GitLab 后端：

```bash
python3 <SKILL_DIR>/scripts/ocr-pull-discussions.py <MR_IID> > /tmp/issues.json
```

### GitLab discussion 数据结构

`glab api /projects/:id/merge_requests/:iid/discussions` 返回 JSON 数组，每个元素是一个 discussion（thread）：

```json
{
  "id": "abc123def456",
  "individual_note": false,
  "notes": [
    {
      "id": 12345,
      "body": "issue text",
      "author": {"username": "gitblue.bot"},
      "position": {
        "position_type": "text",
        "new_path": "path/to/file.go",
        "new_line": 50
      },
      "resolved": false
    }
  ]
}
```

### 过滤规则

只保留 `author.username == "gitblue.bot"` 的 discussion：

| 类型 | 判定条件 | 是否保留 |
| ---- | ---- | ---- |
| Inline issue | `notes[0].position != null`，body 含具体问题 | ✅ |
| Fallback | `notes[0].position == null`，body 以 `🔍 OpenCodeReview — issues` 开头 | ✅，解析子问题 |
| Summary | body 以 `🔍 OpenCodeReview found` 开头 | ❌ |
| LGTM | body 以 `✅ OpenCodeReview: No issues` 开头 | ❌ |
| Error note | body 含 `⚠️ OpenCodeReview error` | ❌ |

### Fallback note 解析

Body 格式固定：

```
🔍 OpenCodeReview — issues that could not be posted inline:

---

### `path/to/file.go` (L1-L1)

text

---

### `path/to/file2.go` (L45-L60)

text...

---
```

用正则 `### \`(.+)\`` 取文件名，`(L\d+)` 取行号，段落正文取到下一个 `---` 为止。这些 issue 的 `discussion_id` 是 fallback note 的 discussion id。

### Resolved 状态

GitLab 将 resolved 状态存储在 discussion 的第一个 note 上（`notes[0].resolved`）。通过 `PUT /discussions/{id}` 传 `{"resolved": true}` 来 resolve。

### 分页

`glab mr note list` 内部处理分页。不完整时回退到 `glab api`：

```bash
glab api /projects/:id/merge_requests/<MR_ID>/discussions?per_page=100&page=1
```

检查 `Link` header 是否有 `rel="next"`，继续请求直到当前页返回空数组。

## 贴标签 + resolve discussion

脚本自动使用 GitLab 后端：

```bash
cat classified.json | python3 <SKILL_DIR>/scripts/ocr-post-labels.py <MR_IID>
```

### 回退命令

脚本失败时逐条回退：

```bash
glab mr note create <MR_ID> --reply <discussion_id_prefix> -m "..."
```

`--reply` 接受完整 discussion ID 或至少 8 字符的唯一前缀。

### Resolve discussion

```bash
glab api -X PUT "/projects/:id/merge_requests/<MR_ID>/discussions/<discussion_id>" \
  -F "resolved=true"
```

## API 端点参考

| 操作 | 端点 |
| ---- | ---- |
| 创建 inline discussion | `POST /projects/:id/merge_requests/:iid/discussions` |
| 创建普通 note | `POST /projects/:id/merge_requests/:iid/notes` |
| 回复 discussion | `POST /projects/:id/merge_requests/:iid/discussions/:discussion_id/notes` |
| 列出 discussions | `GET /projects/:id/merge_requests/:iid/discussions` |
| Resolve discussion | `PUT /projects/:id/merge_requests/:iid/discussions/:discussion_id` |

## 环境变量

| 变量 | 用途 |
| ---- | ---- |
| `CI_SERVER_URL` | GitLab 实例 URL（默认 `http://internal.example.com`） |
| `CI_PROJECT_ID` | 项目 ID（优先使用，跳过自动推导） |
| `GITLAB__PERSONAL_ACCESS_TOKEN` | GitLab PAT 认证 |
| `GITLAB_API_TOKEN` | 旧版 token（fallback） |
| `CI_JOB_TOKEN` | CI Job Token 认证（CI 环境） |
