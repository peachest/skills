# GitLab API & glab 参考

## 手动拉取 discussions

回退到手动方式（脚本不可用时）：

```bash
glab mr note list <MR_ID> -F json
```

输出为 JSON 数组，每个元素是一个 discussion（thread）：

```json
[
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
        }
      }
    ]
  }
]
```

## 过滤规则

只保留 `author.username == "gitblue.bot"` 的 discussion：

| 类型 | 判定条件 | 是否保留 |
| ---- | ---- | ---- |
| Inline issue | `notes[0].position != null`，body 含具体问题 | ✅ |
| Fallback | `notes[0].position == null`，body 以 `🔍 OpenCodeReview — issues` 开头 | ✅，解析子问题 |
| Summary | body 以 `🔍 OpenCodeReview found` 开头 | ❌ |
| LGTM | body 以 `✅ OpenCodeReview: No issues` 开头 | ❌ |
| Error note | body 含 `⚠️ OpenCodeReview error` | ❌ |

## Fallback note 解析

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

## 分页

`glab mr note list` 内部处理分页。不完整时回退到 `glab api`：

```bash
glab api /projects/:id/merge_requests/<MR_ID>/discussions?per_page=100&page=1
```

检查 `Link` header 是否有 `rel="next"`，继续请求直到当前页返回空数组。

## 回复 discussion

```bash
glab mr note create <MR_ID> --reply <discussion_id_prefix> -m "<文本>"
```

`--reply` 接受完整 discussion ID 或至少 8 字符的唯一前缀。

## API 端点参考

| 操作 | 端点 |
| ---- | ---- |
| 创建 inline discussion | `POST /projects/:id/merge_requests/:iid/discussions` |
| 创建普通 note | `POST /projects/:id/merge_requests/:iid/notes` |
| 回复 discussion | `POST /projects/:id/merge_requests/:iid/discussions/:discussion_id/notes` |
| 列出 discussions | `GET /projects/:id/merge_requests/:iid/discussions` |
