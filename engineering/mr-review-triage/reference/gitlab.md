# GitLab 操作参考

GitLab 平台的具体命令、API 端点和数据格式。

## 平台检测

远程地址含 `gitlab.com` 或自建 GitLab 实例（如 `gitlab.blue.example`、`gitlab.red.example`）时判定为 GitLab。

```bash
git remote get-url origin
# git@gitlab.com:ns/proj.git              → GitLab
# git@gitlab.blue.example:ns/proj.git    → GitLab (self-hosted)
# http://gitlab.red.example/ns/proj.git  → GitLab (self-hosted)
```

GitLab 实例（host）、协议（http/https）、token 均由脚本自动从 `git remote get-url origin` + glab config 推导，无需手动设置环境变量。

## CLI 工具

使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。多实例环境注意：`--hostname` 只对 `glab api` / `glab auth status` 有效；`glab mr` 子命令**不支持** `--hostname`（会报 `Unknown flag`），它们从 cwd 的 git remote 推导 host，或用 `-R <完整 remote URL 或 GROUP/PROJECT 路径>` 显式指定实例。

```bash
glab auth status   # 检查已配置的实例和认证状态
```

## 多实例认证（重要）

同一台机器可能配置多个 GitLab 实例（如 `gitlab.com`、`gitlab.blue.example`、`gitlab.red.example`）。脚本按以下优先级解析实例上下文：

1. `CI_SERVER_URL` 环境变量（显式覆盖）
2. `git remote get-url origin` 的 host + glab config `hosts.<host>`（token、api_protocol、api_host）
3. 环境变量 token 兜底（`GITLAB__PERSONAL_ACCESS_TOKEN` > `GITLAB_API_TOKEN` > `CI_JOB_TOKEN`）

**token 优先取 glab config 里该 host 的 token**，避免误用别的实例的 token 导致 401。跑之前先 `glab auth status` 确认目标实例已认证。

OCR bot 登录名是实例相关的（如 `review-bot` 或 `ai-bot-001`）。

> **注**：GitLab 后端已不再按作者过滤（`OCR_BOT_LOGIN` 对 GitLab 已废弃）——人类
> 评审的 general 评论同样拉取，否则 pull 与 closure gate 口径不一致（gate 统计所有
> resolvable 线程）。噪声靠 body 过滤规则排除。

## MR ID 推导

MR ID 未给时从分支名推导（注意用 `-R`，不是 `--hostname`）：

```bash
glab mr list -R https://gitlab.red.example/<group>/<project> \
  --source-branch="$(git rev-parse --abbrev-ref HEAD)" -F json | jq '.[0].iid'
```

## 拉取 review discussion

脚本自动使用 GitLab 后端：

```bash
python3 <SKILL_DIR>/scripts/ocr-pull-discussions.py <MR_IID> > .triage/<MR_IID>/issues.json
```

输出为统一的 `{discussion_id, file, line, body, no}` finding 数组。`no` 是单轮 pull 文件内的去重后 API 首现序（1..N），verdict 落盘当场消费的临时指针；跨轮身份仍是 `discussion_id`（精确字节比对）。状态文件必须落在 `.triage/<MR_IID>/issues.json`（verdict/post/verify 的 join 基底），不入 /tmp；CI 未完结时脚本 exit 2（pipeline 门，`--skip-pipeline-check` 显式逃生）。流程编排见 triage-mr SKILL.md。

新轮检测：重拉时加 `--digest --against .triage/<MR_IID>/classified.json`，stdout 只输出 classified 文件中不存在的新 findings（保留原 `no`），人读摘要走 stderr（零长 ID 形态）。`--against` 文件缺失视为首轮（全部为新增），不报错。

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
      "author": {"username": "ai-bot-001"},
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

拉取所有非 system 且内容像评审的 discussion（OCR bot + 人类评审者，不按作者过滤）：

| 类型 | 判定条件 | 是否进入 classified | 是否需 resolve |
| ---- | ---- | ---- | ---- |
| Inline issue | `notes[0].position != null`，body 含具体问题 | ✅ | ✅（post-labels） |
| Fallback | `notes[0].position == null`，body 以 `🔍 OpenCodeReview — issues` 开头 | ✅，解析子问题 | ✅（post-labels） |
| General reviewer comment | `notes[0].position == null`，`resolvable == true`，非 summary/junk body（常见为人类评审的总帖/杂项帖） | ✅，`file="(general)"`、`line=0` | ✅（post-labels） |
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

GitLab 将 resolved 状态存储在 discussion 的第一个 note 上（`notes[0].resolved`）。标准路径是 `PUT /discussions/{id}` 传 `{"resolved": true}`。

**平台怪癖（部分内部 GitLab 实例，如 gitlab.red.example）**：discussion 级 PUT 一律返回 500，`POST /discussions/{id}/notes`（回复）返回 404——两个标准端点在该实例上结构性不可用。唯一可靠的 resolve 路径是 **note 级 PUT**：

```bash
PUT /projects/:id/merge_requests/<MR_ID>/discussions/<discussion_id>/notes/<note_id>?resolved=true
```

`ocr-post-labels.py` 已内置 fallback：discussion 级 PUT 失败时自动逐 note resolve（含刚贴的 verdict reply note）——无需手动干预。

### 分页

脚本内部用 `curl` 分页。不完整时回退到 `glab api`（注意 `--hostname`）：

```bash
glab api --hostname gitlab.red.example \
  /projects/:id/merge_requests/<MR_ID>/discussions?per_page=100&page=1
```

## 贴标签 + resolve discussion

脚本自动使用 GitLab 后端：

```bash
python3 <SKILL_DIR>/scripts/ocr-post-labels.py <MR_IID> --mode triage \
  --classified .triage/<MR_IID>/classified.json
```

`--mode triage` 的模式映射只兜底没有 per-item `resolved` 字段的旧条目；现行流程下每条是否 resolve 由 `verdict.py` 在 verdict 时刻写入 per-item `resolved`（Edge 默认 resolve、Q 默认留开、triage 模式 TP resolve），post 只执行不重判。

以下全部在脚本内完成，无手动回退路径（脚本出错 = 修脚本或上报）：

- **join + anchor 校验**：任何平台调用前，每条 entry 的 `discussion_id` 必须与 pull 文件字节一致、anchor 必须可由同一文件 body 复算——截断/手抄 id 在此处响亮失败；
- **内容判重**：回帖内嵌 anchor 标记，重跑自动跳过已回帖线程（幂等，含 posted 标志缺失场景）；
- **回复失败不 resolve**（`--force` 显式覆盖）——裁决理由必须先上墙；
- **summary 线程扫尾**：🔍 start 回确认帖、✅ end/LGTM 回当轮统计后 resolve、⚠️ error 只回帖**永不 resolve** 且使运行非零退出（gate 永红为有意 human-in-loop 设计）；
- **posted 标志**回写 `--classified` 文件。

stdin（`< state.json`）仅作传输方式保留，schema 2 校验同等适用。

## 收尾验证（closure gate）

post-labels 返回 ok 不等于 triage 完成。OCR summary discussion 是 `resolvable=True` 但不在 classified.json 里。必须跑 closure gate：

```bash
python3 <SKILL_DIR>/scripts/ocr-verify-resolved.py <MR_IID>
# exit 0 = 全部 resolved（且 head CI 已完结）；exit 1 = 有残留或后端错误（fail closed，列在 stderr）；
# exit 2 = pipeline 未完结（--skip-pipeline-check 覆盖）或用法错误
```

summary 线程由 post 的扫尾逻辑处理（见上节），无需手动回复。人读输出以序号/内容锚标注线程、不出现平台 id；残留 ⚠️ error 线程使 gate 保持红——那是有意的 human-in-loop 设计（本轮 review 未跑成），上报用户裁决，不得自行 resolve 凑绿。

## API 端点参考

| 操作 | 端点 |
| ---- | ---- |
| 创建 inline discussion | `POST /projects/:id/merge_requests/:iid/discussions` |
| 创建普通 note | `POST /projects/:id/merge_requests/:iid/notes` |
| 回复 discussion | `POST /projects/:id/merge_requests/:iid/discussions/:discussion_id/notes` |
| 列出 discussions | `GET /projects/:id/merge_requests/:iid/discussions` |
| Resolve discussion | `PUT /projects/:id/merge_requests/:iid/discussions/:discussion_id`（部分内部实例 500，脚本自动降级到下行） |
| Resolve 单个 note（同上实例可用） | `PUT /projects/:id/merge_requests/:iid/discussions/:discussion_id/notes/:note_id` |

## 环境变量

| 变量 | 用途 |
| ---- | ---- |
| `CI_SERVER_URL` | 显式覆盖 GitLab 实例 URL；缺省时从 git remote + glab config 推导 |
| `CI_PROJECT_ID` | 项目 ID（优先使用，跳过自动推导） |
| `OCR_BOT_LOGIN` | 已废弃（GitLab 不再按作者过滤，人类评论同样拉取） |
| `GITLAB__PERSONAL_ACCESS_TOKEN` | GitLab PAT 认证（兜底，优先用 glab config 该 host 的 token） |
| `GITLAB_API_TOKEN` | 旧版 token（fallback） |
| `CI_JOB_TOKEN` | CI Job Token 认证（CI 环境） |
