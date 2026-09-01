# GitLab 操作参考

GitLab 平台的具体命令、API 端点和数据格式。

## 平台检测

远程地址含 `gitlab.com` 或自建 GitLab 实例（如 `internal.example.com`、`internal.example.com`）时判定为 GitLab。

```bash
git remote get-url origin
# git@gitlab.com:ns/proj.git              → GitLab
# git@internal.example.com:ns/proj.git    → GitLab (self-hosted)
# http://internal.example.com/ns/proj.git  → GitLab (self-hosted)
```

GitLab 实例（host）、协议（http/https）、token 均由脚本自动从 `git remote get-url origin` + glab config 推导，无需手动设置环境变量。

## CLI 工具

使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。多实例环境下 `glab` 必须带 `--hostname <host>` 指定实例，否则默认走 `gitlab.com`（导致返回空或 401）。

```bash
glab auth status   # 检查已配置的实例和认证状态
```

## 多实例认证（重要）

同一台机器可能配置多个 GitLab 实例（如 `gitlab.com`、`internal.example.com`、`internal.example.com`）。脚本按以下优先级解析实例上下文：

1. `CI_SERVER_URL` 环境变量（显式覆盖）
2. `git remote get-url origin` 的 host + glab config `hosts.<host>`（token、api_protocol、api_host）
3. 环境变量 token 兜底（`GITLAB__PERSONAL_ACCESS_TOKEN` > `GITLAB_API_TOKEN` > `CI_JOB_TOKEN`）

**token 优先取 glab config 里该 host 的 token**，避免误用别的实例的 token 导致 401。跑之前先 `glab auth status` 确认目标实例已认证。

OCR bot 登录名是**实例相关**的（如 `gitblue.bot` 或 `ai_bot001`），通过 `OCR_BOT_LOGIN` 环境变量指定：

```bash
export OCR_BOT_LOGIN=ai_bot001   # 目标实例的 OCR bot 用户名
```

`OCR_BOT_LOGIN` 为空时不过滤 bot（拉取全部 discussion）。

## MR ID 推导

MR ID 未给时从分支名推导（注意 `--hostname`）：

```bash
glab mr list --hostname internal.example.com \
  --source-branch="$(git rev-parse --abbrev-ref HEAD)" -F json | jq '.[0].iid'
```

## 拉取 review discussion

脚本自动使用 GitLab 后端：

```bash
python3 <SKILL_DIR>/scripts/ocr-pull-discussions.py <MR_IID> > /tmp/issues.json
```

### GitLab discussion 数据结构

`GET /projects/:id/merge_requests/:iid/discussions` 返回 JSON 数组，每个元素是一个 discussion（thread）：

```json
{
  "id": "abc123def456",
  "individual_note": false,
  "notes": [
    {
      "id": 12345,
      "body": "issue text",
      "author": {"username": "ai_bot001"},
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

只保留 OCR bot（`OCR_BOT_LOGIN`，默认不过滤）的 discussion：

| 类型 | 判定条件 | 是否进入 classified | 是否需 resolve |
| ---- | ---- | ---- | ---- |
| Inline issue | `notes[0].position != null`，body 含具体问题 | ✅ | ✅（post-labels） |
| Fallback | `notes[0].position == null`，body 以 `🔍 OpenCodeReview — issues` 开头 | ✅，解析子问题 | ✅（post-labels） |
| Summary | body 以 `🔍 OpenCodeReview found` 开头 | ❌（无 finding 可分类） | ✅（verify 门捕获） |
| LGTM | body 以 `✅ OpenCodeReview: No issues` 开头 | ❌ | ✅（verify 门捕获，若 resolvable） |
| Error note | body 含 `⚠️ OpenCodeReview error` | ❌ | ✅（verify 门捕获，若 resolvable） |
| System note | `notes[0].system == true`（commit push、description 变更等） | ❌ | N/A（不可 resolve） |

Summary/LGTM/Error discussion 是 bot 状态通知，不含可分类的 finding，所以 pull 不拉取它们；但它们在 GitLab 上是 `resolvable=True` 的线程，必须被 resolve。这就是 `ocr-verify-resolved.py` 的工作——它是 closure gate，exit 0 才算 triage 完成。

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

脚本内部用 `curl` 分页。不完整时回退到 `glab api`（注意 `--hostname`）：

```bash
glab api --hostname internal.example.com \
  /projects/:id/merge_requests/<MR_ID>/discussions?per_page=100&page=1
```

## 贴标签 + resolve discussion

脚本自动使用 GitLab 后端：

```bash
cat .triage/<MR_ID>/classified.json | python3 <SKILL_DIR>/scripts/ocr-post-labels.py <MR_IID> --mode triage
```

`--mode triage` 让 TP（真阳性）也 resolve——fix 已在本 run 落地并验证，不需要「stay open for tracking」。Edge/Question 保持 open。

### 回退命令

脚本失败时逐条回退（注意 `--hostname`）：

```bash
glab mr note create --hostname internal.example.com \
  <MR_ID> --reply <discussion_id_prefix> -m "..."
```

`--reply` 接受完整 discussion ID 或至少 8 字符的唯一前缀。

### Resolve discussion

```bash
glab api --hostname internal.example.com \
  -X PUT "/projects/:id/merge_requests/<MR_ID>/discussions/<discussion_id>" \
  -F "resolved=true"
```

## 收尾验证（closure gate）

post-labels 返回 ok 不等于 triage 完成。OCR summary discussion 是 `resolvable=True` 但不在 classified.json 里，post-labels 不会 resolve 它们。必须跑 closure gate：

```bash
python3 <SKILL_DIR>/scripts/ocr-verify-resolved.py <MR_IID>
# exit 0 = 全部 resolved；exit 1 = 有残留（列在 stderr）
```

残留的 OCR summary 线程手动回复 + resolve：

```bash
# 1) 回复
glab api --hostname internal.example.com \
  -X POST "/projects/:id/merge_requests/<MR_ID>/discussions/<discussion_id>/notes" \
  -f "body=✅ 已修复（commit <hash>）：..."
# 2) resolve
glab api --hostname internal.example.com \
  -X PUT "/projects/:id/merge_requests/<MR_ID>/discussions/<discussion_id>" \
  -F "resolved=true"
```

重跑 verify 直到 exit 0。

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
| `CI_SERVER_URL` | 显式覆盖 GitLab 实例 URL；缺省时从 git remote + glab config 推导 |
| `CI_PROJECT_ID` | 项目 ID（优先使用，跳过自动推导） |
| `OCR_BOT_LOGIN` | OCR bot 用户名（实例相关，如 `ai_bot001`）；空 = 不过滤 bot |
| `GITLAB__PERSONAL_ACCESS_TOKEN` | GitLab PAT 认证（兜底，优先用 glab config 该 host 的 token） |
| `GITLAB_API_TOKEN` | 旧版 token（fallback） |
| `CI_JOB_TOKEN` | CI Job Token 认证（CI 环境） |
