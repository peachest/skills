# Fact-Check Run: 文件生命周期

> 追踪 `/fact-check <path>` 一次运行在 8 个阶段中每个文件从创建到消亡的全过程。
> 按 Design Decisions（DD-01~DD-31）逐阶段推导，非实现观察。

---

## Document Key 方案

claims.json 和 ledger.jsonl 均为 per-document。它们的路径由**文档的相对路径**推导而来。

### Key 推导规则

```
document_key = relative_path_from_project_root, 其中 / → --
```

| 文档在项目中的位置 | document_key |
|-------------------|-------------|
| `README.md`（项目根目录） | `README.md` |
| `docs/research/04-llama.cpp框架.md` | `docs--research--04-llama.cpp框架.md` |
| `src/benchmarks/kvcache/report.md` | `src--benchmarks--kvcache--report.md` |

**路径解析基准：** 项目根目录 = `git rev-parse --show-toplevel`（git 仓库）或 `<path>` 的最近公共祖先（非 git）。

### 文件位置

```
fact-check/
└── documents/
    └── <document_key>/
        ├── claims.json             # 本轮 claim 全量数据（原地覆盖）
        └── ledger.jsonl            # 跨 run verdict 历史（append-only）
```

### 重命名处理（Git Rename Detection）

文档被 `git mv` 或改名后，新路径 → 新 document_key → `documents/<新 key>/` 不存在。此时 Phase 0 执行：

```
git log --diff-filter=R --follow --name-only --format="" -- <新路径> | tail -1
```

- 找到 rename 前路径 → 推导旧 document_key → 将 `documents/<旧 key>/` 下全部内容复制到 `documents/<新 key>/`
- 未找到 rename 记录 → 按新文档全量处理（旧 ledger 保留为历史孤儿）

此检测只在 `documents/<新 key>/` 不存在时触发，不影响常规路径的性能。

---

## Phase 0: Init

**入口输入：** `/fact-check <path>` 或 `/fact-check <path> --full` 或 `/fact-check --status`

**只读操作（不产出文件）：**

| 读什么 | 用途 | 设计来源 |
|--------|------|---------|
| `git rev-parse --show-toplevel` | 确定项目根目录 | — |
| `git remote` | 提取 owner/repo，GitHub P0 验证用；非 git → NO_REPO | DD-30 |
| `git branch` | 自动作为 `session_tag` | DD-30 |
| `realpath --relative-to=<root> <path>` | 计算文档相对路径 → 推导 document_key | — |
| `documents/<key>/ledger.jsonl` 存在性 | 配合 `--full` flag 决定 full/incremental | DD-30 |
| `git diff --unified=0`（增量时） | 检测 changed_ranges | DD-26 |
| `<path>` 所指文件或目录 | 路径是目录→扫描直接子 `.md` 文件；每个文件各自独立 run | DD-30 |
| `subagent({ action: "list" })` | 检测子 agent 扩展存在性→构建 capability_map | DD-31 |
| `git log --diff-filter=R --follow ...`（新 key 无 ledger 时） | rename detection | — |

**文件创建：**

```
fact-check/run-YYYYMMDD-HHMMSS-{branch}/
└── run.json                                # 创建 · 初始元数据
```

**`run.json` 初始内容（DD-10, DD-31）：**

```json
{
  "session_tag": "feat-kvcache",
  "mode": "full",
  "repo": "kvcache-ai/ktransformers",
  "repo_source": "git",
  "document_key": "docs--research--04-llama.cpp框架.md",
  "documents": ["docs/research/04-llama.cpp框架.md"],
  "started_at": "2026-07-10T10:00:00Z",
  "subagents_available": true,
  "capability_map": {
    "extract_worker": "worker",
    "web_searcher": "anysearch-researcher",
    "model_alt": "delegate"
  }
}
```

**增量模式下额外操作（无新文件）：**
- 读 `documents/<key>/claims.json` 获取旧 claim → 按 **`git diff` hunk 范围**判断哪些 claim 的 `source_location` 行号落在未改动区域→carry forward；落在改动区域内→加入 re-extract queue
- content_hash 在此用作**验证**（不为搜索）：carry forward 后 hash source_location 处文本，如果 mismatch 也加入 re-extract（应对 diff 未捕获的语义变化）
- `total-stats.json` 已存在则读取上次运行信息

---

## Phase 1: Extract + Validator Loop

**只读操作：**

| 读什么 | 用途 |
|--------|------|
| `prompts/extract-claims.md` | LLM 提取 prompt 模板 |
| `references/schema.md` | claim JSON schema 定义 |
| 目标文档（如 `docs/research/04-llama.cpp框架.md`） | 提取源 |
| `mdq --output json '# *' <文档>`（mdq 可用时） | 获取文档章节结构→指导分片 |
| `mdq --output json '[]()' <文档>`（mdq 可用时） | 提取全部链接→LLM 提取时作为锚定点，减少遗漏 |
| `mdq --output json '```' <文档>`（mdq 可用时） | 提取代码块→code-api 类 claim 的预检 |

**文件操作：**

```
fact-check/
├── documents/<key>/
│   └── claims.json                     # 创建 · LLM 提取结果（首次写入）
└── run-{...}/
    └── validation_errors.json          # 创建 · 仅当 A/B/C/D 四级校验循环 3 轮仍失败
```

**文档分片（mdq 驱动）：**

- mdq `--output json '# *'` 获取文档的 `##`/`###` 章节结构
- 按章节切分（不是纯行号分割）
- 大章节（> 100 行或 > 4000 tokens）按段落进一步切分
- 每个分片独立送入 LLM 提取，避免 lost-in-the-middle
- mdq 不可用时退化到行号分割

**链接预提取（mdq 驱动）：**

| mdq 命令 | 产出 | 用途 |
|---------|------|------|
| `mdq --output json '[]()'` | 全部链接列表 | Phase 2 直接路由到 rule_engine，不需 LLM 猜测 |
| `mdq --output json '```'` | 代码块列表 | code-api 类 claim 的 source_location 锚定 |
| `mdq --output json '# *'` | 章节结构 | 分片边界 + source_location 的 heading 上下文 |

预提取的链接作为元数据注入到 extraction prompt：`"文档中有 N 个链接，以下是列表..."`，让 LLM 提取 claim 时参考。
mdq 不可用时跳过预提取，LLM 自行发现链接。

**`claims.json` 的 4 级验证器 loop（DD-22, DD-23）：**

| 层级 | 检查项 | 失败触发 loop？ | 失败处理 |
|------|--------|----------------|---------|
| A | JSON 语法合法 parse | ✅ | 要求 LLM 重新输出完整 claims.json |
| B | Schema 字段/类型/枚举 | ✅ | per-claim diff 修补（只修失败 entry） |
| C1 | `source_location` 有效可读 | ✅ | per-claim diff 修补（LLM 修正定位） |
| C2 | `claim_text` 与原文逐字相同 | ✅ | per-claim diff 修补（LLM 对齐措辞） |
| C3 | content_hash 三方一致 | ❌ 自动修正 | 校验器重写 hash |
| D | 原子性（catalog 7 模式检查） | ✅ | 未匹配→`compound_embedded`；匹配未拆→diff 修补 |

- `max_retries=3`，每轮通过的 entry 锁定不动
- 3 轮仍失败 → 保留 `validation_errors.json`，供用户手动介入

**validator 的 per-claim diff 修补报告格式（DD-23）：**

```json
{
  "passed": 40,
  "failed": 5,
  "retry_count": 1,
  "max_retries": 3,
  "failures": [
    {
      "claim_id": "C003",
      "errors": [
        {"code": "TEXT_MISMATCH", "detail": "claim_text differs from source at doc.md:42"}
      ]
    }
  ],
  "auto_fixes": [
    {"claim_id": "C045", "fixed": "content_hash recalcd", "old_hash": "...", "new_hash": "sha256:a1b2c3d4e5f6"}
  ]
}
```

**`claims.json` 首次写入的 claim 示例（DD-07）：**

```json
{
  "claim_id": "C001",
  "claim_text": "DeepSeek V3.1 was released in September 2025",
  "normalized_claim": "DeepSeek V3.1 release date September 2025",
  "source_location": "docs/research/04-llama.cpp框架.md:42",
  "content_hash": "sha256:7d1e9f3a2b4c",
  "type": "temporal",
  "expected_verifier": "web_search",
  "atomicity_parent": null,
  "decomposition_mode": null,
  "compound_flag": null
}
```

**字段说明（DD-07 协议）：**
- `content_hash`: 校验器计算（非 LLM），`SHA256(trim(lowercase(原文)).replace(/\s+/g, ' '))[:12]`，前缀 `sha256:`
- `source_location`: 三模式格式（DD-25）：`doc.md:42` / `doc.md:42-45` / `doc.md:42:10-85`
- `expected_verifier`: LLM 建议值，Phase 2 可能被 regex 覆盖

---

## Phase 2: Classify

**只读操作：**

| 读什么 | 用途 |
|--------|------|
| `references/regex-rules.json` | 25 条 authority 规则 + 3 条 judgment 规则 + 2 条 interpretation 规则 |

**文件操作：**

```
fact-check/documents/<key>/
└── claims.json                             # 更新 · 各 claim 获得 route 和 verifier 字段
```

**双通道路由（DD-06）：**

```
route_claim(claim_text + normalized_claim) → 双字段匹配

  regex 优先匹配（确定性通道）：
    ├── authority 规则命中（25 条）         → route: "rule_engine", verifier: "rule_engine.{type}"
    ├── judgment_纯价值 命中                 → route: "refused", verdict: "REFUSED"
    ├── judgment_社区归因 命中               → route: "web_search", verifier: "web_search"
    ├── judgment_hedging_factual 命中        → route: "web_search", verdict: "web_search"
    └── interpretation 规则命中              → route: "inferred", verdict: "INFERRED"

  LLM expected_verifier fallback（语义通道，regex 全失配时）：
    ├── expected_verifier == "rule_engine"  → 规则引擎尝试通用检查（URL→URL 检查；owner/repo→repo 检查；其余全量 P0 校验器）
    ├── expected_verifier == "refused"      → route: "refused", verdict: "REFUSED"
    ├── expected_verifier == "inferred"     → route: "inferred", verdict: "INFERRED"
    └── 其它                                → route: "web_search"
```

正则对 `claim_text` 和 `normalized_claim` 双字段匹配，避免 LLM 缩写/补全导致漏过。

---

## Phase 3a: Rule Engine

**只读操作：**

| 读什么 | 用途 |
|--------|------|
| `scripts/rule-engine.sh` | 执行 shell 脚本 |
| 系统 CLI: `curl`, `gh`, `glab` | 外部验证工具 |

**文件操作：**

```
fact-check/documents/<key>/
└── claims.json                             # 更新 · 各 authority claim 获得 verdict + evidence + evidence_url
```

**规则引擎调度（DD-02）：**

`rule-engine.sh <documents/<key>/claims.json>` 读取、过滤 `expected_verifier == "rule_engine" | route == "rule_engine"` 的行，按 25 条 authority 规则 dispatch：

| Verifier | 检测方式 | 成功 verdict | 失败 verdict |
|----------|---------|-------------|-------------|
| `rule_engine.arxiv` | `curl -sI https://arxiv.org/abs/<id>` → 200 | SUPPORTED | CONTRADICTED |
| `rule_engine.doi` | `curl -sI https://doi.org/<doi>` → 200/302/303 | SUPPORTED | CONTRADICTED |
| `rule_engine.code_platform_pr` | `gh pr view <num>` 或 `glab mr` | SUPPORTED | CONTRADICTED |
| `rule_engine.code_platform_issue` | `gh issue view <num>` | SUPPORTED | CONTRADICTED |
| `rule_engine.code_platform_repo` | `gh repo view <owner/repo>` | SUPPORTED | CONTRADICTED |
| `rule_engine.url` | `curl -sI <url>` → 200/301/302 | SUPPORTED | CONTRADICTED |
| `rule_engine.npm` | `curl -sI https://registry.npmjs.org/<pkg>` | SUPPORTED | CONTRADICTED |
| `rule_engine.pypi` | `curl -sI https://pypi.org/project/<pkg>/` | SUPPORTED | CONTRADICTED |
| `rule_engine.cargo` | `curl -sI https://crates.io/api/v1/crates/<name>` | SUPPORTED | CONTRADICTED |
| `rule_engine.go_module` | `curl -sI https://pkg.go.dev/<path>` | SUPPORTED | CONTRADICTED |
| `rule_engine.nuget` | `curl -sI https://www.nuget.org/packages/<name>/` | SUPPORTED | CONTRADICTED |
| `rule_engine.git_commit` | `gh api repos/:owner/:repo/commits/:sha` | SUPPORTED | CONTRADICTED |
| `rule_engine.rfc` | `curl -sI https://www.rfc-editor.org/rfc/rfc<num>.txt` | SUPPORTED | CONTRADICTED |
| `rule_engine.pmid` | `curl -sI https://pubmed.ncbi.nlm.nih.gov/<pmid>/` | SUPPORTED | CONTRADICTED |
| `rule_engine.patent` | `curl -sI https://patents.google.com/patent/<id>/en` | SUPPORTED | CONTRADICTED |
| `rule_engine.ietf_draft` | `curl -sI https://datatracker.ietf.org/doc/<name>/` | SUPPORTED | CONTRADICTED |
| `rule_engine.docker` | `curl -sI https://hub.docker.com/v2/repositories/<ns>/<image>/tags/<tag>/` | SUPPORTED | CONTRADICTED |
| `rule_engine.spdx_license` | 查 `package.json` / GitHub API `/license` | SUPPORTED | CONTRADICTED |
| `rule_engine.git_tag` | `git ls-remote --tags <repo>` + grep | SUPPORTED | CONTRADICTED |

**错误处理（DD-12）：** 2 次指数退避重试（1s → 3s）→ 仍失败则标记 `UNVERIFIABLE`。不降级给 LLM 猜测。

---

## Phase 3b: Triage

**只读操作：**

| 读什么 | 用途 |
|--------|------|
| `references/verdict-policy.json` | triage 判定规则 |

**文件创建：**

```
fact-check/
├── run-{...}/
│   └── triage_results.json               # 创建 · 不同 provider LLM 的 triage 结果
└── documents/<key>/
    └── claims.json                       # 更新 · 添加 triage_result 字段
```

**工作方式（DD-06, DD-31）：**
- 输入：Phase 2 双通道路由后仍入 `web_search` 的 claim
- 调用不同 provider 的 LLM（subagent `model_alt`，或 inline model override）
- 每次评估一个 batch

```json
{
  "triage_batch": [
    {"claim_id": "C003", "triage_result": "CONFIDENT"},
    {"claim_id": "C005", "triage_result": "UNCERTAIN"},
    {"claim_id": "C007", "triage_result": "SUSPECT"}
  ]
}
```

**分流结果（DD-05）：**
- `CONFIDENT` → 跳过 Phase 5 深度搜索（triage-escaped）
- `UNCERTAIN / SUSPECT` → 进入 Phase 5 深度搜索
- triage 不可用（subagent 缺失）→ 跳过 Phase 3b，所有 fallback claim 进入 Phase 5

---

## Phase 4: Checkpoint 🛑

**无文件创建或修改。**

**读取：** `claims.json`（检查点后重新读取，DD-11）

**交互流程（DD-05, DD-21）：**

```
agent 展示分区:
  [规则引擎已验证]     claim 清单（verdict 已定）
  [triage-escaped]     claim 清单（CONFIDENT，跳过搜索）
  [需深度搜索]         claim 清单（UNCERTAIN/SUSPECT）
  [compound_embedded]  警告（未拆解的复合声明）
  [INFERRED 声明]      无验证意图的推断声明

用户输入 (任意):
  y                    → 继续 Phase 5
  n                    → 终止（标记中断）
  skip C001            → 跳过特定 claim
  view C001            → 查看 claim 详情
  edit C001            → 手动修改 claim_text/routing
  search C001          → override triage，拉入 Phase 5
```

**跳过阈值（DD-21）：**
- ≤ 3 条新 claim + 全部 `SUPPORTED` → 自动跳过检查点
- `severity: high` + `CONTRADICTED` → 必须打断，即使只有一条
- `severity: low` + `UNVERIFIABLE` → 可选择只显示警告不打断

**同步协议（DD-11）：** 用户在检查点可能编辑 `documents/<key>/claims.json`，Phase 5 前 agent 必须重新读取以获得最新状态。

---

## Phase 5: Deep Verify

**只读操作：**

| 读什么 | 用途 |
|--------|------|
| `references/verdict-policy.json` | 证据层级判定规则 |
| `claims.json`（重新读取后） | 检查点后用户可能编辑 |

**文件创建（每个 batch）：**

```
fact-check/
├── run-{...}/
│   ├── verify-batch-0001.json            # 创建 · batch 1 搜索结果
│   ├── verify-batch-0002.json            # 创建 · batch 2 搜索结果
│   ├── verify-batch-0003.json            # 创建 · batch 3 搜索结果
│   └── ...                               # 每 4-5 claims 一个 batch
└── documents/<key>/
    └── claims.json                       # 更新 · 各 search claim 获得完整 verdict
```

**并行模式（DD-31）：**
- 子 agent 模式：4-5 claims/batch，≤ 4 concurrency，`fresh` context
- CLI fallback 模式：`anysearch batch_search`，同一 batch 大小

**`verify-batch-{N}.json` 格式：**

```json
[
  {
    "claim_id": "C005",
    "verdict": "SUPPORTED",
    "evidence_tier": "T1",
    "evidence_url": "https://github.com/ggerganov/llama.cpp/pull/11049",
    "evidence_text": "PR #11049 merged 2025-01-04 adds DeepSeek V3 support",
    "evidence_date": "2025-01-04",
    "confidence": "high",
    "severity": "low"
  }
]
```

**证据层级判定（DD-04）：**

| Tier | 来源 | 最高 verdict |
|------|------|-------------|
| T1 | GitHub PR/Issue/Discussion 正文, arXiv 摘要, 官方文档 | SUPPORTED |
| T2 | 知名博客引用 PR 数据, 项目 README | SUPPORTED（数值偏差→NUANCED） |
| T3 | GitHub Discussion 个人实测, HN/Reddit 用户报告 | 最多 NUANCED |
| T4 | 搜索不到出处 | 最多 UNVERIFIABLE |

**交叉验证逻辑（DD-03, DD-15）：**
- 多源一致 → `SUPPORTED` + `confidence: high`
- 单源 + T1 → `SUPPORTED` + `confidence: medium`
- 源间矛盾 → `NUANCED` 或 `CONTRADICTED`（取决于哪方更强）
- 证据 > 6 个月 → 维持 verdict + `staleness_warning` 标记

**失败处理（DD-12, DD-31）：**
- batch 超时 → 该批标记 `UNVERIFIABLE` + 重试 1 次
- 仍失败 → 保留 `UNVERIFIABLE`，在 `handoff.md` 注明
- 子 agent 不可用 → 退化为父 session inline 调用 anysearch CLI

---

## Phase 6: Write

**最终文件输出（DD-10, DD-16, DD-17）：**

```
fact-check/
├── run-YYYYMMDD-HHMMSS-{branch}/
│   ├── run.json                    # 更新 · 补全：耗时、verdict 分布、stopped_at
│   ├── report.md                   # 创建 · B 风格综合报告
│   ├── handoff.md                  # 创建 · 修正指引
│   ├── validation_errors.json      # (Phase 1 带入)
│   ├── triage_results.json         # (Phase 3b 带入)
│   └── verify-batch-*.json         # (Phase 5 带入)
├── documents/<key>/
│   ├── claims.json                 # 更新 · 最终版，含所有 verdict + evidence
│   └── ledger.jsonl                # append · 跨 run 持久化 verdict 历史
└── total-stats.json                # 创建/更新 · 全局累计统计
```

### `claims.json`（最终版）

**增量更新的字段：**

| Phase | 新增/更新字段 |
|-------|-------------|
| Phase 1 | `claim_id`, `claim_text`, `normalized_claim`, `source_location`, `content_hash`, `type`, `expected_verifier`, `atomicity_parent`, `decomposition_mode`, `compound_flag` |
| Phase 2 | `route`, `matched_verifier`, `matched_rule` |
| Phase 3a | `verdict`, `evidence`, `evidence_url`, `checked_at` |
| Phase 3b | `triage_result` |
| Phase 5 | `verdict`, `evidence_tier`, `evidence_url`, `evidence_text`, `evidence_date`, `checked_at`, `confidence`, `severity`, `staleness_warning` |
| Phase 6 | `status: "resolved" / "unresolved"` |
Vid 在最终版中与每个 claim 关联（DD-08）：`SHA256(claim_text.trim().to_lowercase())[:12]`

### `report.md`（DD-16）

```markdown
# Fact-Check Report: 04-llama.cpp框架.md
**Run:** run-20260710-100000-main | **Checked:** 2026-07-10

## Summary
| | Count |
|---|---|
| 🔴 CONTRADICTED | 1 |
| 🟡 NUANCED | 2 |
| 🕐 OUTDATED | 0 |
| ⚪ UNVERIFIABLE | 1 |
| 🟢 SUPPORTED | 59 |
| ⛔ REFUSED | 3 |
| 💡 INFERRED | 2 |

## Items to Fix (1)
## Items Needing Attention (3)
## Carried Forward (59)

---
### C001 — CONTRADICTED 🔴 severity:high confidence:high
- **Claim:** "arXiv:2605.18071 不存在"
- **Location:** `04-llama.cpp框架.md:42`
- **Evidence Tier:** T1 — https://arxiv.org/abs/2605.18071
- **Finding:** arXiv page returns 404
- **Suggested Fix:** 确认 arXiv ID 或移除该引用
- **Verdict ID:** `sha256:3a8f2b1c`
```

### `handoff.md`（DD-17）

只包含需要修正的项目（`CONTRADICTED` / `NUANCED`）。用户可用争议标记 `verdict wrong, counter evidence: <url>` 触发反证提交流程（DD-18）。

### `run.json`（最终版）

```json
{
  "session_tag": "feat-kvcache",
  "mode": "full",
  "repo": "kvcache-ai/ktransformers",
  "documents": ["04-llama.cpp框架.md"],
  "started_at": "2026-07-10T10:00:00Z",
  "completed_at": "2026-07-10T10:12:35Z",
  "duration_seconds": 755,
  "total_claims": 68,
  "verdict_distribution": {
    "SUPPORTED": 59, "CONTRADICTED": 1, "NUANCED": 2,
    "UNVERIFIABLE": 1, "REFUSED": 3, "INFERRED": 2
  },
  "subagents_available": true,
  "capability_map": {
    "extract_worker": "worker",
    "web_searcher": "anysearch-researcher",
    "model_alt": "delegate"
  }
}
```

### `documents/<key>/ledger.jsonl`（DD-09）

`append-only` JSONL，同 **`run_seq`**（单调递增整数）覆盖，不依赖时间戳。增量运行时 Phase 0 读此文件判断模式。

```jsonl
{"vid":"3a8f2b1c","claim_text":"...","verdict":"CONTRADICTED","evidence_tier":"T1","run_seq":2,"timestamp":"2026-07-08T14:35:22Z","run":"run-20260708-143522-main"}
{"vid":"3a8f2b1c","claim_text":"...","verdict":"SUPPORTED","evidence_tier":"T1","run_seq":3,"timestamp":"2026-07-10T10:12:35Z","run":"run-20260710-100000-main"}
```

**覆盖逻辑：** 对同一 vid，取 `run_seq` 最大的一行。`tac ./ledger.jsonl | awk -F'"run_seq":' '!seen[$1]++'` 可获得每个 vid 的最新状态。

`run_seq` 来自 `total-stats.json` 的 `total_runs`（每次 run 自增 1），写入新 ledger 行前先读取 +1。

**记录格式字段（对比 claims.json）：**

| 字段 | ledger 中始终存在 | claims.json 中对应 |
|------|-------------------|-------------------|
| `vid` | ✅ | 每个 claim 的 vid（DD-08 算法） |
| `claim_text` | ✅ | 同字段 |
| `verdict` | ✅ | 同字段 |
| `evidence_tier` | ✅ | 同字段 |
| `evidence_url` | ⭕ 有则记 | 同字段 |
| `timestamp` | ✅ | Phase 5 `checked_at`（可读参考，覆盖不用它） |
| `run_seq` | ✅ | total-stats.json 的 `total_runs`（单调递增，覆盖唯一依据） |
| `run` | ✅ | run.json 中的 run id |
| `claim_id` | ❌ | 仅在 claims.json 中有效（每次 run 重新编号） |
| `source_location` | ❌ | 仅在 claims.json 中有效（行号随版本漂移） |
| `type` / `route` | ❌ | 仅在 claims.json 中有效 |

**设计理由（DD-08, DD-09）：** ledger 只记录跨 run 不变的标识（vid、claim_text）和可累积的字段（verdict、run_seq、timestamp），不记录每次 run 可能变化的临时数据（claim_id 重新编号、source_location 行号漂移）。

**不依赖时间戳的原因：** 系统时钟不可信（clock skew、时区偏移、同一秒多次运行）。`run_seq` 源自 `total-stats.json` 的 `total_runs` 自增计数，单调递增可排序，按此覆盖才是可靠的。timestamp 保留为可读参考，不参与覆盖逻辑。

### `total-stats.json`

```json
{
  "total_runs": 3,
  "total_claims_verified": 187,
  "latest_run": "run-20260710-100000-main",
  "verdict_distribution": {"SUPPORTED": 159, "CONTRADICTED": 5, "NUANCED": 8, "UNVERIFIABLE": 3, "REFUSED": 7, "INFERRED": 5},
  "outstanding_fixes": 2,
  "unresolved_claims": 1
}
```

---

## Phase 7: Deliver

**无文件操作。** Agent 输出摘要给用户：

```
📊 Fact Check Complete — run-20260710-100000-main
   🔴 CONTRADICTED:  1    🟡 NUANCED:  2    🕐 OUTDATED:  0
   ⚪ UNVERIFIABLE:  1   🟢 SUPPORTED: 59   ⛔ REFUSED:  3   💡 INFERRED: 2

Items to fix:   1  (open report.md for details)
Needs attention: 3
Carried forward: 59

Phase 8: [A] Agent auto-fix  [M] Manual fix  [V] View report
```

---

## Phase 8: Fix 🛑

**A 路径（Agent 修正） — 有文件修改：**

| 文件 | 操作 |
|------|------|
| 源文档（如 `docs/research/04-llama.cpp框架.md`） | 原地编辑，agent 逐项修正 |
| `documents/<key>/claims.json` | 更新：`status: "extracted" → "revised" → "rechecked" → "resolved"` |
| `documents/<key>/ledger.jsonl` | append 新行（修正后的 verdict） |

**M 路径（手动） — 无文件操作。** 输出 checklist 给用户，下次调用增量时自然覆盖。

**V 路径（先看报告） — 无文件操作。** 用户任意时刻切回 A 或 M。

**争议路径（DD-18）：** 用户在 `handoff.md` 标记 `verdict wrong, counter evidence: <url>` → 下一轮 agent 读取 handoff → `append_overriding_vid` 写新行到 ledger。

---

## 完整文件产出拓补图

```
fact-check/
├── run-{datetime}-{branch}/
│   ├── run.json               P0──────P6────→ (创建 → 补完)
│   ├── report.md              P6──────────→ (创建)
│   ├── handoff.md             P6──────────→ (创建)
│   ├── validation_errors.json P1──────────→ (仅失败时)
│   ├── triage_results.json    P3b─────────→ (仅启用时)
│   ├── verify-batch-*.json    P5──────────→ (搜索 batch)
│   ├── profile.jsonl          P0→P1→P2→P3a→P3b→P4→P5→P6→  (追加事件)
│   └── profile-summary.json   P6──────────→ (聚合报告)
│
├── documents/<key>/
│   ├── claims.json            P1→P2→P3a→P3b→P5→P6→P8  (创建 → 逐阶段增量更新)
│   └── ledger.jsonl           P6→P8→                    (append)
│
└── total-stats.json           P6──────────────────────→ (创建/更新)
```

**颜色约定：**
- `P0──→` 表示在 Phase 0 首次写入，后续某 phase 可能更新
- `P6→P8→` 表示多次 append
- `(仅失败时)` 表示仅条件触发时创建

---

## Script Pipeline（确定性通道）

约 70% 的 phase 步骤可以脚本化执行。Agent 负责 LLM 调用（提取、triage、搜索）和编排脚本执行。
脚本负责所有确定性操作：校验、路由、分级、生成报告。

### 新增 4 个脚本

```
scripts/
├── rule-engine.sh            ← 已有 (Phase 3a)
├── ledger-query.sh           ← 已有 (ledger 查询)
├── init.sh                   ← 新增：Phase 0 初始化
├── validate-claims.sh        ← 新增：A/B/C/D 四级校验
├── route-claims.sh           ← 新增：Phase 2 确定性正则路由
├── grade-evidence.sh         ← 新增：证据分级 + 交叉验证 + 时效性标记
└── generate-report.sh        ← 新增：从 claims.json 生成报告
```

### `init.sh`（Phase 0）

```
# 输入：<path> <project-root>
# 输出：stdout json
# {
#   "document_key": "docs--research--04-llama.cpp框架.md",
#   "mode": "full|incremental",
#   "repo": "kvcache-ai/ktransformers|NO_REPO",
#   "session_tag": "feat-kvcache",
#   "is_directory": false
# }
```

| 功能 | 实现 |
|------|------|
| `git rev-parse --show-toplevel` | 确定项目根目录 |
| `realpath --relative-to=<root> <path>` | 文档相对路径 → `/` 替换为 `--` |
| `git remote get-url origin` | 提取 repo owner/name |
| `git branch --show-current` | session_tag |
| 检测 `documents/<key>/ledger.jsonl` 存在性 | 决定 full vs incremental |
| 检测 `<path>` 是文件还是目录 | 文件→单文档；目录→扫描 `*.md` |
| `git log --diff-filter=R --follow`（新 key 时） | rename detection |
| `stat --printf="%s" <path>` | 文件大小 → 分片策略决策依据 |

### `validate-claims.sh`（Phase 1）

```
# 输入：<claims.json> <source-document>
# 输出：stdout json
# {
#   "passed": 40,
#   "failed": 5,
#   "failures": [
#      {"claim_id": "C001", "errors": [{"code": "TEXT_MISMATCH", "detail": "..."}]}
#   ],
#   "auto_fixes": [
#      {"claim_id": "C045", "fixed": "content_hash recalcd"}
#   ]
# }
```

| 校验层级 | 实现方式 |
|----------|---------|
| A (JSON 语法) | `python3 -c "json.load(sys.stdin)"` 或 `echo | jq .` |
| B (Schema) | python 逐字段检查 `claim_id`/`claim_text`/`type` 等存在 + 枚举值合法 |
| C1 (source_location) | `awk 'NR==<行号>' <源文档>` 检查行存在；区间格式检查起止行 |
| C2 (claim_text 原文匹配) | 从 source_location 提取对应原文段落，trim/compress 后全等比较 |
| C3 (content_hash) | `printf '%s' "$text" | sha256sum | cut -c1-12` 对比 |
| D (原子性) | 7 种 catalog 模式正则匹配 `claim_text`：and-list / or-list / condition / compare / if-then / cause / embedded |

**设计要点：**
- 所有校验是**纯确定性**的，不需要 LLM
- 校验器只标记错误，不修改 claims.json（和 LLM 的职责分离）
- agent 收到校验结果后，如果失败 > 0，决定是否重试 LLM

### `route-claims.sh`（Phase 2 确定性通道）

```
# 输入：<claims.json> <references/regex-rules.json>
# 输出：stdout json （更新后的 claims + 路由统计）
# {
#   "claims": [...],  # 每个 claim 新增 route/match_verifier/matched_rule
#   "stats": {
#     "authority_hit": 12,
#     "judgment_refused": 2,
#     "judgment_community": 1,
#     "judgment_hedging": 3,
#     "interpretation": 1,
#     "unmatched": 4
#   }
# }
```

| 功能 | 实现 |
|------|------|
| 对 `claim_text` + `normalized_claim` 双字段匹配 25 条 authority 规则 | `grep -E` / python `re.match()` |
| 3 条 judgment 规则匹配 | 纯价值 / 社区归因 / hedging_factual |
| 2 条 interpretation 规则匹配 | 推断类正则 |
| 未匹配的 claim 标记为 `unmatched` | LLM fallback 通道（不可脚本化） |
| 写回 `route`/`matched_verifier`/`matched_rule` 字段 | `jq` update |

### `grade-evidence.sh`（Phase 5）

```
# 输入：<verify-batch-*.json> 或 stdin lines
# 每行格式：{"claim_id": "...", "evidence_url": "...", "evidence_text": "..."}
# 输出：stdout json （增加 evidence_tier / confidence / staleness_warning）
```

| 判定 | 规则 |
|------|------|
| 证据 Tier | evidence_url 域名 → T1/T2/T3/T4 映射 |
| 交叉验证 | 多源同 URL → 去重；多源不同 URL 同 verdict → `confidence: high` |
| 时效性 | `evidence_date` < 6 个月 → 添加 `staleness_warning` |

### `generate-report.sh`（Phase 6）

```
# 输入：<claims.json> <run.json> <run-dir>
# 输出：写入文件，stdout 无输出
# - <run-dir>/report.md
# - <run-dir>/handoff.md
# - <run-dir>/run.json （补全统计字段）
# - ledger.jsonl （append）
# - total-stats.json （更新）
```

| 产出 | 模板 |
|------|------|
| report.md | Markdown 模板 + jq 填充 claim 表格 |
| handoff.md | 只含 CONTRADICTED/NUANCED claim，包含 `<!-- handoff-claim C001 -->` 机器可读标记 |
| ledger.jsonl append | `jq -c '{vid, claim_text, verdict, evidence_tier, evidence_url, timestamp, run}'` |
| total-stats.json | 读取历史 + 合并本次 verdict 分布 |

### Agent 对脚本的调用模式

```
# Agent 只做三件事：
# 1. LLM 调用（提取、triage、搜索）
# 2. 调用脚本处理确定性步骤
# 3. 展示结果 + 用户交互

# 典型 pipeline：
init_json=$(bash scripts/init.sh "$path")           # P0 脚本
llm_result=$(llm_extract "$chunked_doc")             # P1 LLM
validation=$(bash scripts/validate-claims.sh "$tmp_claims" "$src")  # P1 脚本
route_result=$(bash scripts/route-claims.sh "$claims" "$references") # P2 脚本
bash scripts/rule-engine.sh "documents/.../claims.json"               # P3a 脚本
# ... P3b LLM（triage）... P5 LLM（搜索）...
search_output=$(llm_search "$batch")                                  # P5 LLM
graded=$(bash scripts/grade-evidence.sh <<< "$search_output")         # P5 脚本
bash scripts/generate-report.sh "$claims" "$run_json" "$run_dir"   # P6 脚本
```

Agent 不做的事情：
- 不会用 python 临时写校验脚本
- 不会手写 Markdown 报告
- 不会手动计算 hash

**原则：** 所有确定性操作 → 脚本；所有判断性操作 → LLM。

---

## Profiling（运行可观测性）

为长运行任务提供性能分析数据，帮助定位瓶颈（LLM 延迟、网络请求、脚本耗时）。

### 文件

```
fact-check/run-YYYYMMDD-HHMMSS-{branch}/
└── profile.jsonl                # 创建 · 追加写入的事件流
└── profile-summary.json         # 创建 · Phase 6 生成的聚合报告
```

### 事件类型

每条记录一个事件，JSON Lines 格式（每行完整 JSON，支持管道处理）：

| 事件 | 触发时机 | 关键字段 |
|------|---------|---------|
| `phase_start` | 每个 Phase 开始时 | `phase`, `started_at` |
| `phase_end` | 每个 Phase 结束时 | `phase`, `duration_ms` |
| `llm_call` | 每次 LLM 调用 | `type`, `model`, `duration_ms`, `input_tokens`, `output_tokens` |
| `script` | 每次脚本调用 | `name`, `phase`, `duration_ms`, `exit_code` |
| `network` | 每次 curl/gh/glab | `target`, `verifier`, `duration_ms`, `status_code` |
| `retry` | 每轮重试 | `phase`, `reason`, `retry_count` |
| `subagent` | 子 agent 调用 | `agent_name`, `task_type`, `duration_ms` |

### 示例

```jsonl
{"event":"phase_start","phase":"P0","started_at":"2026-07-10T10:00:00Z"}
{"event":"script","name":"init.sh","phase":"P0","duration_ms":45,"exit_code":0}
{"event":"phase_end","phase":"P0","duration_ms":150}
{"event":"phase_start","phase":"P1","started_at":"2026-07-10T10:00:01Z"}
{"event":"llm_call","type":"extract","chunk":1,"model":"claude-sonnet-4","duration_ms":12300,"input_tokens":5200,"output_tokens":1800}
{"event":"llm_call","type":"extract","chunk":2,"model":"claude-sonnet-4","duration_ms":9800,"input_tokens":4100,"output_tokens":1500}
{"event":"script","name":"validate-claims.sh","phase":"P1","duration_ms":320,"exit_code":0}
{"event":"retry","phase":"P1","validator_level":"C2","retry_count":1}
{"event":"phase_end","phase":"P1","duration_ms":35000}
{"event":"network","target":"arxiv.org/abs/2605.18071","verifier":"rule_engine.arxiv","duration_ms":870,"status_code":200}
{"event":"subagent","agent_name":"anysearch-researcher","task_type":"deep_verify","duration_ms":28500}
```

### 聚合计算（Phase 6 由 generate-report.sh 生成）

```json
{
  "total_duration_ms": 755000,
  "phases": [
    {"phase":"P0","duration_ms":150,"pct":0.02},
    {"phase":"P1","duration_ms":35000,"pct":4.6},
    {"phase":"P2","duration_ms":200,"pct":0.03},
    {"phase":"P3a","duration_ms":45000,"pct":6.0},
    {"phase":"P3b","duration_ms":12000,"pct":1.6},
    {"phase":"P4","duration_ms":30000,"pct":4.0},
    {"phase":"P5","duration_ms":580000,"pct":76.8},
    {"phase":"P6","duration_ms":500,"pct":0.07},
    {"phase":"P7","duration_ms":200,"pct":0.03}
  ],
  "llm_calls": {
    "total":12,
    "total_duration_ms":320000,
    "pct":42.4,
    "total_input_tokens":130000,
    "total_output_tokens":48000,
    "avg_duration_ms":26667,
    "by_type":{"extract":4,"triage":2,"search":6}
  },
  "scripts": {
    "total":8,
    "total_duration_ms":1200,
    "pct":0.16
  },
  "network_requests": {
    "total":25,
    "total_duration_ms":45000,
    "pct":6.0
  },
  "retries": {
    "total":2,
    "by_reason":{"C2_text_mismatch":1,"D_atomicity":1}
  }
}
```

### 用法

Profiling 在 run-output 中占位但**不需要 agent 主动实现**——它只是插入时间戳 + 写 JSONL 的机械操作。实际做法：

- Agent 在每个 Phase 开始/结束时调用 `date +%s%3N` 记录毫秒时间戳
- 脚本调用时用 `time` 前缀：`{ time bash script.sh 2>&1; }` 捕获耗时
- LLM 调用后从 API 响应读取 token 计数
- 所有事件写入 `run-{...}/profile.jsonl`（shell `>>` 追加）

---

## 增量运行 vs 全量运行的差异

增量运行时文件结构**完全相同**，只有 Phase 0 的处理逻辑不同：

| 维度 | 全量 | 增量 |
|------|------|------|
| Phase 0 决策 | `--full` flag 或 ledger 不存在 | 默认（`documents/<key>/ledger.jsonl` 存在） |
| Phase 1 提取 | 所有文档重新提取 | 旧 claim 读取→按 `git diff` hunk 范围判断 source_location 是否未改动→carry forward；content_hash 验证；只对 diff 区域 re-extract |
| Phase 6 write | claims.json 完全覆盖 + ledger append 全量 vid | 只 append 增量变化的 vid 到 ledger；carry forward 的旧行 timestamp 不变 |
| 性能 | O(N) 全量 LLM | O(Δ) 只处理变化区域 2-5 条 |

---

## 引用

| 设计决策 | 内容 | 在本文件中的体现 |
|---------|------|----------------|
| DD-06 | Claim 提取、分类与拆解 | Phase 1 提取 + Phase 2 双通道路由 |
| DD-07 | Claim 提取 Schema (B) | claims.json 格式 |
| DD-08 | VID 生成 | handoff.md / report.md 中的 vid |
| DD-09 | Ledger 存储（per-document） | documents/<key>/ledger.jsonl |
| DD-10 | Run 目录结构（claims.json 移至 documents/） | 所有文件的目录位置 + document key 方案 |
| DD-11 | 检查点后 claims.json 同步 | Phase 4 重读协议 |
| DD-12 | 规则引擎 Fallback | Phase 3a 错误处理 |
| DD-13 | 证据时效性标记 | claims.json 中 evidence_date + staleness_warning |
| DD-14 | Claim 状态机 | claims.json 中 status 字段变化 |
| DD-15 | Verdict 置信度双层 | severity + confidence 字段 |
| DD-16 | 报告格式 | report.md |
| DD-17 | 修正工作流 | Phase 8 A/M/V 三条路径 |
| DD-18 | 反证提交流程 | handoff.md 争议标记 |
| DD-19 | 完整流水线 | 8 个 Phase 的完整拓补 |
| DD-20 | Skill 文件位置 | 文件路径根 |
| DD-21 | 检查点触发阈值 | Phase 4 跳过/打断条件 |
| DD-22 | 四级 Validator | Phase 1 validation_errors.json |
| DD-23 | Per-Claim Diff 修补 Loop | Phase 1 循环协议 |
| DD-24 | content_hash 字段 | claims.json content_hash 计算规则 |
| DD-25 | source_location 三模式格式 | claims.json 中定位格式 |
| DD-26 | 增量 Diff 逻辑 | 增量运行时 Phase 0/1 差异 |
| DD-27 | 三方一致性校验 | Phase 1 校验器 C 级检查 |
| DD-28 | REFUTED → CONTRADICTED 改名 | verdict 命名 |
| DD-29 | 判断型细化 | Phase 2 路由 |
| DD-30 | CLI 精简 + Phase 0 自动检测 | Phase 0 自动检测逻辑 |
| DD-31 | 子 Agent 并行化策略 | Phase 1/3b/5 并行模式 |
