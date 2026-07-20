# Fact-Check Skill Design Decisions

> 所有设计决策通过 grill-me 工作流收敛，21 个核心节点逐一确认。
> 核心哲学: 所有 verdict 都不是绝对真理，都是当前证据下的判断，可被更强证据推翻。

---

## 决策汇总

### DD-01 · 三档 Claim 边界

| 档 | 类型 | 验证方式 | 示例 |
|---|------|---------|------|
| **确权型** (authority) | arXiv ID, DOI, GitHub PR#, Issue#, 仓库名, URL | 规则引擎 (P0 脚本) | "arXiv:2605.18071 存在" |
| **关系验证型** (relationship) | benchmark 数据, 参数值, 日期, 命名 | anysearch 搜索 + LLM 交叉验证 | "EPYC 9474F 上跑 6.44 tok/s" |
| **判断型-纯价值** (judgment_value) | 第一人称评价 | 直接 `REFUSED` | "这个方案更好" |
| **判断型-社区归因** (judgment_attribution) | 社区共识描述 | web_search (T3) | "社区认为 llama.cpp 最活跃" |

**来源:** Grill Q1

---

### DD-02 · 规则引擎范围 (P0/P1/P2)

| 优先级 | Claim 类型 | 检测方式 | 备注 |
|--------|-----------|---------|------|
| **P0** | arXiv ID | `curl -sI https://arxiv.org/abs/<id>` | HTTP 状态码 200 |
| **P0** | DOI | `curl -sI https://doi.org/<doi>` | HTTP 状态码 200 |
| **P0** | 代码平台 PR/Issue/Repo | `glab` / `gh` / Gitee API 查状态 | GitHub/GitLab/Gitee/Gitea/Gitcode/Source Forge. 各平台 verifier 详情见 rule-engine 实现文档 |
| **P0** | URL | `curl -sI <url>` | HTTP 状态码 200 |
| **P0** | NPM 包名 | `npm view <pkg> name` 或 `curl -sI https://registry.npmjs.org/<pkg>` | 包存在性验证 |
| **P0** | PyPI 包名 | `curl -sI https://pypi.org/project/<pkg>/` | 包存在性验证 |
| **P0** | Cargo crate | `curl -sI https://crates.io/api/v1/crates/<name>` | Rust 生态，包存在性验证 |
| **P0** | Go module | `curl -sI https://pkg.go.dev/<module-path>` | Go 生态，模块存在性验证 |
| **P0** | NuGet 包名 | `curl -sI https://www.nuget.org/packages/<name>/` | .NET 生态，包存在性验证 |
| **P0** | Git commit hash | `gh api repos/:owner/:repo/commits/:sha` | 需 repo 上下文 + `gh` CLI |
| **P0** | RFC 编号 | `curl -sI https://www.rfc-editor.org/rfc/rfc<num>.txt` | HTTP 状态码 200 |
| **P0** | PubMed ID (PMID) | `curl -sI https://pubmed.ncbi.nlm.nih.gov/<pmid>/` | 生物医学文献标识符，HTTP 200 |
| **P0** | 专利号 | `curl -sI https://patents.google.com/patent/<country><num>/en` | US/CN/WO/EP/JP/KR 全支持，HTTP 200 |
| **P0** | IETF Internet-Draft | `curl -sI https://datatracker.ietf.org/doc/<draft-name>/` | RFC 前身，协议讨论高频 |
| **P0** | SPDX License | regex 匹配标识符 → 查 `package.json` / GitHub API `/license` | 技术文档最高频声明之一，需上下文（所属 repo） |
| **P1** | 版本号 | `gh release view <version> --repo <owner>/<repo>` | 迭代实现 |
| **P1** | HuggingFace 模型名 | HF API 查模型卡 | 迭代实现 |
| **P1** | Docker Hub 镜像 | `curl -sI https://hub.docker.com/v2/repositories/<ns>/<image>/tags/<tag>/` | 镜像存在性验证 |
| **P1** | Git tag（非 release） | `git ls-remote --tags <repo>` + grep | 轻量 tag，非 GitHub Release |
| **P2** | 论文引用数据比对 | 暂不实现，交搜索交叉验证 | HTML 解析+数值提取+比对复杂度高 |
| **P2** | 量化大小比对 | 暂不实现，交搜索交叉验证 | 迭代实现 |
| **P2** | Benchmark 数据比对 | 暂不实现 | 迭代实现 |

**来源:** Grill Q5

---

### DD-03 · 6 级 Verdict 体系

| Verdict | 图标 | 含义 | 典型场景 |
|---------|------|------|---------|
| `CONTRADICTED` | 🔴 | 来源明确反对该声明 | arXiv ID 不存在, PR 数据与声称不符 |
| `NUANCED` | 🟡 | 基本正确但遗漏关键限定条件 | M3 Ultra 数据缺少上下文标注 |
| `OUTDATED` | 🕐 | 曾经正确但已被新版本推翻 | V3.1 日期错误, 旧 benchmark |
| `UNVERIFIABLE` | ⚪ | 当前证据不足以判断 | 搜索引擎无法索引的 PR, 限流 fallback |
| `SUPPORTED` | 🟢 | ≥1 个独立来源确认一致 | PR 正文与声称一致 |
| `REFUSED` | ⛔ | 该声明类型不可验证（纯价值判断或过于模糊） | "这个方案更好", "可能和 NUMA 有关" |
| `INFERRED` | 💡 | 声明有可溯源的基础数据，但结论本身是从数据中推断出来的，推断逻辑不可直接验证 | "MLA 32x 压缩使 CPU 推理可行"（压缩数值可验证，但"使可行"是作者推断） |

**来源:** Grill Q3

---

### DD-04 · 证据层级

| Tier | 来源类型 | 最高 Verdict |
|------|---------|-------------|
| **T1** | GitHub PR/Issue/Discussion 正文, HuggingFace 模型卡, arXiv 论文摘要, 官方文档 | `SUPPORTED` |
| **T2** | 知名博客/评测站引用 PR 数据, 项目 README | `SUPPORTED` (数值偏差→降为 `NUANCED`) |
| **T3** | GitHub Discussion 个人实测, HN/Reddit 用户报告 | 最多 `NUANCED` |
| **T4** | 搜索不到出处, 非公开渠道 | 最多 `UNVERIFIABLE` |

**来源:** Grill Q17

---

### DD-05 · 审查检查点 (Review Checkpoint)

- **时机:** Phase 3b triage 后, Phase 5 深度验证前
- **展示内容:** 规则引擎已验证 claim + triage-escaped claim + 需深度搜索 claim + `compound_embedded` 警告
- **触发条件:** 新 claim > 3 条, OR 出现 `CONTRADICTED` / `NUANCED` / `UNVERIFIABLE` / `INFERRED`
- **跳过条件:** ≤ 3 条新 claim 且全部 `SUPPORTED`
- **操作:** 展示已验证结果 → 用户确认/跳过/查看详情/override triage（"这条别跳过，给我搜"）→ 决定是否继续深度验证

**来源:** Grill Q2, Q11；吸收自 fact-checker（triage 分流 + 用户 override）

---

### DD-06 · Claim 提取、分类与拆解

#### Phase 1: LLM 提取 + 分类 + Catalog 拆解

- **提取:** LLM 从文档提取所有可验证 claim (B schema)；prompt 含完整双语策略（语言检测、claim_text 原语保留、normalized_claim 同语归一化、混合文档独立处理）
- **分类:** LLM 标注 claim type，分类优先于拆解（子 claim 继承父 type）；Type Selection Guide 提供中英双语示例
- **拆解:** 复合 claim 按照 **fixed catalog** 拆分为原子 claim，LLM 只能从 catalog 中选择模式 + 决定深度，不能发明新模式
- **不匹配 catalog:** 无法匹配 catalog 的复合结构 → 不拆，标记 `compound_embedded`，Phase 5 搜索验证时 warning

#### 拆解 Catalog（7 种固定模式）

| 模式 | 触发条件 | 拆解规则 |
|------|---------|---------|
| **AND-枚举** | 包含 `and/和/以及/且/、` 连接 ≥2 个并列项 | 按并列项拆为独立 claim |
| **括号-补充** | 包含 `(...)` 或 `（...）`，括号内是时间/人名/数值 | 括号内拆为独立 claim |
| **括号-展开** | 包含 `（A，B，C）` 逗号分隔的多项 | 每项一个 claim |
| **FROM-TO** | 包含 `从 X 到 Y` / `from X to Y` / `X→Y` | 拆为 before + after 两个 claim |
| **从句嵌入** | claim > 25 词 + 包含 `which`/`that`/`的` 从句标记 | 拆为主句 claim + 从句 claim |
| **即-补充** | 包含 `X，即 Y，Z` / `X, i.e., Y, Z` | 拆为 X claim + Y claim |
| **破折号补充** | 包含 `——` 或 `--` 分隔的独立断言 | 破折号前后各为独立 claim |

#### Phase 2: 双通道路由（regex 优先 + LLM fallback）

路由同时利用两个信号源，覆盖 regex 模式匹配和 LLM 语义理解各自的盲区：

1. **regex 优先匹配**（确定性通道）—— 对 claim_text 和 normalized_claim 双字段匹配
   - **authority 规则**（25 条，中英文双语覆盖）→ 规则引擎，路由到对应 verifier
   - **judgment 规则** → 纯价值判断 `REFUSED`；社区归因 `web_search`；hedging factual（含可验证原子 + 模糊词）`web_search`
   - **interpretation 规则** → `INFERRED` verdict
2. **LLM 预期 fallback**（语义通道）—— regex 全部失配时，回退到 LLM 在 Phase 1 输出中的 `expected_verifier`
   - `rule_engine` → 规则引擎尝试通用检查（claim_text 含 URL 则 URL 检查；含 owner/repo 模式则代码平台 repo 检查；其余尝试全量 P0 校验器）
   - `refused` → `REFUSED`
   - `inferred` → `INFERRED`
   - 其它 → `web_search`

**为什么需要双通道:** regex 依赖模式枚举，覆盖不全（如 `"使用 react-virtualized"` 无法匹配 `npm install` 模式，LLM 知道这是 npm 包但 regex 漏掉）；LLM 依赖语义理解，但可能误判（如把普通 URL 误判为 academic citation）。regex 优先确保确定性不退化，LLM fallback 填补模式枚举盲区。

#### Phase 3b: Triage（可选增强）

- 双通道路由后仍入 `web_search` 的 claim 进入 triage，用 **不同 provider** 的 LLM 评估
- `CONFIDENT` → 跳过 Phase 5 深度搜索（triage-escaped）
- `UNCERTAIN/SUSPECT` → 进入 Phase 5 深度搜索
- triage 在 Phase 3a 规则引擎之后、Phase 4 检查点之前

#### Claim 类型分层

| 层 | 类型 | 加载方式 |
|----|------|---------|
| **核心层** | authority, numerical, temporal, factual, causal, comparative, code-api, citation, existence, interpretation, file_path, attribution | 始终启用 |
| **扩展层** | legal-med-fin, pricing, licensing, compliance, route, port, retry, timeout | 文档关键词自动检测：`$/user`→启 pricing，`FedRAMP`→启 compliance 等；增量运行时新增不删除 |

**来源:** Grill Q6, Q8；吸收自 groundcheck（复合拆解）、pi-hifi（fixed catalog）、fact-checker（triage + 扩展类型）、truth（regex-first 路由方法论）

---

### DD-07 · Claim 提取 Schema (B)

```json
{
  "claim_id": "C001",
  "claim_text": "DeepSeek V3.1 was released in September 2025",
  "normalized_claim": "DeepSeek V3.1 release date September 2025",
  "source_location": "report-1.md:42",
  "content_hash": "sha256:7d1e9f3a2b4c",
  "type": "temporal",
  "expected_verifier": "web_search",
  "atomicity_parent": null,
  "decomposition_mode": null,
  "compound_flag": null
}
```

**字段说明:**
- `claim_id`: 运行内唯一标识 (顺序 C001, C002...)
- `claim_text`: LLM 从文档提取的原文措辞
- `normalized_claim`: (可选) LLM 标准化后的表述
- `source_location`: 原始文档路径 + 定位
- `content_hash`: 校验器计算（非 LLM），`SHA256(trim(lowercase(原文 at source_location)))[:12]`
- `type`: 核心层 12 类（authority / numerical / temporal / factual / causal / comparative / code-api / citation / existence / interpretation / file_path / attribution）+ 扩展层 8 类
- `expected_verifier`: LLM 建议的验证器 (rule_engine / web_search / refused / inferred)
- `atomicity_parent`: 子 claim 指向父 claim id（sentence group id，非层级 tree）
- `decomposition_mode`: (可选) 拆解使用的 catalog 模式名（and_enum / paren_append / paren_expand / from_to / clause_embed / ie_supplement / dash_supplement）
- `compound_flag`: (可选) 无法匹配 catalog 的复合结构标记为 `compound_embedded`

**来源:** Grill Q8, GroundCheck schema；吸收自 pi-hifi（decomposition_mode）、fact-checker（扩展类型）、groundcheck（interpretation）

---

### DD-08 · Claim VID 生成

- **算法:** `SHA256(claim_text.trim().to_lowercase())[:12]`
- **不包含** source_location (避免行号偏移导致 vid 变化)
- **增量匹配:** 同文档、同措辞 → 同 vid → carry forward

**来源:** Grill Q13

---

### DD-09 · Ledger 存储: 按文档分文件

- **路径:** `documents/<document_key>.ledger.jsonl`
- **格式:** JSONL, append-only
- **覆盖:** 同 vid 的新行 (更晚 timestamp) 自然覆盖旧行
- **非显式链接:** 用 timestamp 自然排序, 不需要 `supersedes` 字段

```
{"vid":"3a8f2b1c","claim_text":"...","verdict":"CONTRADICTED","evidence_tier":"T1","timestamp":"2026-07-08T14:35:22Z","run":"run-20260708-143522"}
{"vid":"3a8f2b1c","claim_text":"...","verdict":"SUPPORTED","evidence_tier":"T1","timestamp":"2026-07-08T16:30:11Z","run":"run-20260708-163011"}
```

**来源:** Grill Q10, Q11

---

### DD-10 · Run 目录结构

```
fact-check/
├── run-{YYYYMMDD}-{HHMMSS}-{session_tag}/
│   ├── claims.json            # 结构化 claim (含最终 verdict)
│   ├── run.json               # 元数据 (session, 耗时, verdict 分布)
│   ├── report.md              # 综合报告 (B 风格卡片 + summary)
│   ├── handoff.md             # 修正指引
│   └── ledger.jsonl           # 本次运行的 ledger (可选)
├── run-{YYYYMMDD}-{HHMMSS}-{session_tag}/
│   └── ...
├── documents/
│   ├── llamacpp.ledger.jsonl   # 按文档分 ledger
│   └── kvcache-layer1.ledger.jsonl
└── total-stats.json            # 全局累计统计
```

**来源:** Grill Q7, Q9, Q11

---

### DD-11 · 检查点后 claims.json 同步

- 用户在检查点可能编辑 claims.json (跳过某条, 手动修改 claim_text)
- Phase 5 开始前 agent 必须重新读取 `claims.json` 获取最新状态
- `status=unconfirmed` → 用户确认后改为 `status=confirmed`

**来源:** Grill Q9 follow-up

---

### DD-12 · 规则引擎 Fallback

- **重试策略:** 2 次指数退避 (1s → 3s)
- **最终 Fallback:** 标记 `UNVERIFIABLE`, 建议用户手动确认 URL
- **不降级给 LLM 猜测** (确权型 claim 的确定性 LLM 给不了)

**来源:** Grill Q12

---

### DD-13 · 证据时效性标记

```json
{
  "evidence_date": "2026-03-31",       // 原始证据发布/合并日期
  "checked_at": "2026-07-08T10:00:05Z"  // 实际验证时间
}
```

- `checked_at` 新但 `evidence_date` 已超过 4 个月 → 自动标记 staleness warning
- 增量运行时: `checked_at` > 文档 last_modified → 无需重验

**来源:** GroundCheck schema, Grill Q 补充

---

### DD-14 · Claim 状态机

```
extracted → checked → [revised → rechecked →] resolved
                                   ↓
                              unresolved
```

| 状态 | 含义 |
|------|------|
| `extracted` | LLM 刚提取, 尚未验证 |
| `checked` | 已验证出 verdict |
| `revised` | 用户/agent 修改了文档中的该 claim |
| `rechecked` | 修正后重新验证 |
| `resolved` | 当前证据下的最终态, 可 carry forward |
| `unresolved` | 超过重验上限, 当前无法定论 |

**来源:** GroundCheck schema, 精简版

---

### DD-15 · Verdict 置信度双层

```
severity: low | medium | high     ← 错误影响程度
confidence: low | medium | high   ← checker 对 verdict 的确信度
```

| 场景 | Verdict | Severity | Confidence |
|------|---------|----------|------------|
| arXiv ID 不存在 | CONTRADICTED | high | high |
| Benchmark 数值偏移 | NUANCED | medium | medium |
| 命名找不到出处 | UNVERIFIABLE | low | medium |
| 证据 6 个月前的 SUPPORTED | SUPPORTED | low | low |

**来源:** GroundCheck schema

---

### DD-16 · 报告格式 (B 风格卡片 + Summary)

```markdown
# Fact-Check Report: <document_name>
**Run:** run-YYYYMMDD-HHMMSS-session_tag | **Checked:** YYYY-MM-DD

## Summary
| | Count |
|---|---|
| 🔴 CONTRADICTED | 1 |
| 🟡 NUANCED | 2 |
| ...

## Items to Fix (1)
## Items Needing Attention (3)
## Carried Forward (59)

---
### C001 — CONTRADICTED 🔴 severity:high confidence:high
- **Claim:** "..."
- **Location:** `document.md:42`
- **Evidence Tier:** T1 — evidence_url
- **Finding:** ...
- **Suggested Fix:** ...
- **Verdict ID:** `sha256:3a8f2b1c`
```

**来源:** Grill Q18

---

### DD-17 · 修正工作流 (Phase 8 Fix)

```
Phase 7 Deliver → 用户选择:
  [A] Agent 逐项修正 → 🛑 Fix Loop → 增量 recheck
  [M] 用户手动修复 → 出 checklist → 下次调用增量
  [V] 先看报告 → 任意时刻切回 A/M
```

- agent 只生成修正建议手稿, 人做决策
- 每项修正后记录到 claims.json 和 ledger

**来源:** Grill Q14, Q19, Q20

---

### DD-18 · 反证提交流程

- **正常路径:** 文档修改 → 增量 diff → 新 vid → 自然覆盖
- **争议路径:** 用户在 handoff.md 标记 "verdict wrong, counter evidence: url"
  → agent 下一轮读取 handoff → `append_overriding_vid` 写新行

**来源:** Grill Q16

---

### DD-19 · 完整流水线 (Phase 0–8)

```
Phase 0: Init         — 解析参数, 创建 run 目录, 检查增量, 文档域自动检测
Phase 1: Extract      — LLM 提取 + 分类 + catalog 拆解 + locate-claim（DD-33）+ check-atomicity（DD-34）+ validator loop（DD-22）
Phase 2: Classify     — 双通道路由: regex 优先匹配 + LLM expected_verifier fallback → authority/judgment/interpretation/web_search
Phase 3a: Rule Engine — 确定性验证器运行 (P0/P1)
Phase 3b: Triage      — 不同 provider LLM 评估 regex fallback claim → 分流逃逸/搜索
Phase 4: Checkpoint 🛑 — 用户确认（展示：规则引擎已验证 + triage-escaped + 需深度搜索）
Phase 5: Deep Verify  — anysearch 搜索 + 搜索精炼 Loop（DD-32）+ 交叉验证 + 证据 tier
Phase 6: Write        — claims.json, ledger, report.md, run.json, total-stats.json
Phase 7: Deliver      — 展示摘要 + handoff.md
Phase 8: Fix 🛑       — A/M/V 三条路径, agent 修正 or 手动
```

**来源:** Grill Q19

---

### DD-20 · Skill 文件位置

- **安装路径:** `~/.pi/agent/skills/fact-check/`
- **项目数据:** 每项目的 `fact-check/` 目录 (run 子目录, documents/, total-stats.json)

```
~/.pi/agent/skills/fact-check/
├── SKILL.md
├── references/
│   ├── design.md           ← 本文件
│   ├── schema.md
│   ├── verdict-policy.json
│   └── regex-rules.json
├── scripts/
│   ├── rule-engine.sh
│   └── ledger-query.sh
└── prompts/
    └── extract-claims.md
```

**来源:** Grill Q15

---

### DD-21 · 检查点触发阈值补充

- 阈值: ≤ 3 条新 claim + 全部 `SUPPORTED` → 自动跳过
- 否则: 必须停在检查点, 让用户决定
- `severity: high` + `CONTRADICTED` 必须打断, 即使只有一条
- `severity: low` + `UNVERIFIABLE` 可选择只显示警告不打断

**来源:** Grill Q11 (细化为敏感度阈)

---

### DD-22 · 四级 Validator + Validated Loop

Claim 提取后必须通过四级校验才能进入 Phase 2。校验器作为 loop 的唯一出口。

> **LLM JSON 模式：** 提取时启用 `response_format: { type: 'json_object' }`（DeepSeek/OpenAI 兼容）。DeepSeek 不支持严格 `json_schema` 约束，且官方文档承认偶发 empty response——A 级 `jq` 校验是必要安全网。

| 层级 | 检查项 | 触发 loop？ | 实现 |
|------|--------|------------|------|
| **A** JSON 语法 | 合法 parse | ✅ 语法错误 → 要求 LLM 重新输出完整 claims.json | `jq .` |
| **B** Schema 符合 | 字段/类型/枚举 | ✅ per-claim diff 修补（只修失败 entry） | `jsonschema` |
| **C1** source_location 有效 | 可读原文 | ✅ per-claim diff 修补（LLM 修正定位） | 读文件 |
| **C2** claim_text 匹配原文 | 逐字相同 | ✅ per-claim diff 修补（LLM 对齐措辞） | diff |
| **C3** content_hash 一致 | 三方一致 | ❌ 自动修正（校验器重写 hash） | hash 重算 |
| **D** 原子性 | 按 catalog 7 种模式检查复合拆解 | ✅ 未匹配 catalog 的复合 → 标记 `compound_embedded`；匹配但未拆 → per-claim diff 修补 | catalog regex + >25 词阈值 |

**D 级原子性检查规则:**
- 匹配 AND-枚举 / 括号-补充 / 括号-展开 / FROM-TO / 从句嵌入 / 即-补充 / 破折号补充 → 必须已拆为原子
- claim > 25 词 + 未匹配任何模式 → 标记 `compound_embedded`（不拆，Phase 5 warning）
- catalog 外模式 → 不触发 loop，标记 `compound_embedded`

**loop 参数:** max_retries=3, 通过即锁定, 只修失败 entry。三轮还不过→保留 claims.json + validation_errors.json 供用户手动介入。

**来源:** Grill Q1, Q2, 后续细化；吸收自 pi-hifi（fixed catalog）、groundcheck（复合拆解前置）

---

### DD-23 · Per-Claim Diff 修补 Loop

校验失败不要求 LLM 重新生成全部 claims.json，只传失败 entry + 错误原因给 LLM diff 修补：

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
        {"code": "TEXT_MISMATCH", "detail": "..."},
        {"code": "COMPOUND_CLAIM", "detail": "..."}
      ]
    }
  ],
  "auto_fixes": [
    {"claim_id": "C045", "fixed": "content_hash recalcd", "old_hash": "...", "new_hash": "..."}
  ]
}
```

- `TEXT_MISMATCH` / `INVALID_LOCATION` / `COMPOUND_CLAIM` / `MISSING_FIELD` → 触发 loop
- `HASH_MISMATCH` → 自动修正（无需 LLM）
- 每轮通过的 entry 锁定不动

**来源:** Grill Q2

---

### DD-24 · content_hash 字段

- **计算者:** 校验器（非 LLM）
- **算法:** `SHA256(trim(lowercase(原文 at source_location)).replace(/\s+/g, ' '))[:12]`
- **前缀:** `sha256:` 标记，为将来切换算法留空间
- **用途:**
  1. 校验器 C 级：验证 source_location 处原文和存储的 hash 一致
  2. 增量 diff：旧 content_hash 在新文档中搜索→命中→carry forward
  3. LLM 不参与计算；校验器在 validation loop 中计算并写入

**来源:** Grill followup

---

### DD-25 · source_location 三模式格式

```
doc.md:42              ← 整行
doc.md:42-45           ← 跨多行
doc.md:42:10-85        ← 行内字符范围
doc.md:42:10-44:30     ← 跨行 + 字符范围
```

一行内含多个 claim 时各自用字符范围分切 (`doc.md:42:10-35`, `doc.md:42:40-85`)。

**来源:** Grill followup

---

### DD-33 · locate-claim 工具 + 嵌套 Claim 模型

#### 设计动机

LLM 不擅长数字号、计算 hash。Phase 1 不应要求 LLM 产出 `source_location` 和 `content_hash`——这些是确定性计算。仿照 pi edit 工具的精确子串匹配设计，用 shell 脚本替代 LLM 的位置计算。

#### locate-claim.sh

```bash
locate-claim "<claim_text>" <doc_path>
```

**子串匹配（非逐行 grep）：** 将整个文件读为字符串，直接做 `indexOf(claim_text)`。多行文本正常处理。

**输出：**

```json
// 成功
{ "ok": true, "location": "doc.md:42:10-85", "content_hash": "sha256:a1b2c3d4e5f6" }

// 文本不在原文中
{ "ok": false, "error": "TEXT_NOT_FOUND", "closest_match": "原文中最相似的子串" }

// 多处匹配
{ "ok": false, "error": "AMBIGUOUS", "candidates": ["doc.md:42", "doc.md:156"] }
```

**source_location 格式（DD-25）：** 行号 + indexOf 算出 col 范围：
- 单行：`doc.md:42:10-85`
- 跨行：`doc.md:42:10-44:30`

**content_hash：** `SHA256(trim(lowercase(原文 at source_location)).replace(/\s+/g, ' '))[:12]`

**Agent 交互模式：**

```
Phase 1 per claim loop:
  locate-claim "$claim_text" $doc
    ├─ ok → 填入 source_location + hash → 继续
    ├─ TEXT_NOT_FOUND → agent 看 closest_match → 修正 claim_text → 重试（max 3）
    └─ AMBIGUOUS → agent 用 context_snippet 消歧义 → 重试
```

#### 嵌套 Claim 模型

根 claim（逐字原文）与子 claim（分解合成）地位不同：

| | 根 claim | 子 claim |
|---|---|---|
| claim_text 来源 | 原文逐字 | LLM 从根 claim 拆解合成 |
| source_location | locate-claim 定位 | 共享父级位置 |
| content_hash | locate-claim 计算 | 无（无独立原文） |
| locate-claim 处理 | ✅ | ❌ 跳过，标记 `derived: true` |
| validator C/D 级 | ✅ 全量校验 | ❌ 仅 B 级（schema） |

#### claim_id 分配策略

Workers 不输出 `claim_id`（多个 worker 并行会导致 ID 冲突）。合并时统一分配：

```
merge + assign IDs:
  1. 收集所有 chunk 产出的 claims
  2. 按 claim_text（trim + collapse whitespace）去重
  3. 按 source_location（原始文档行号）排序
  4. 分配: C001, C002, C003...
  5. 子 claim: C001a, C001b, C002a...
```

**去重：** 分片有 overlap 时，两个 chunk 可能提取到同一条 claim。merge 步骤去重保证无重复。

#### 数据结构

```json
{
  "claim_id": "C001",
  "claim_text": "PR #11049 by fairydreaming (merged 2025-01-04) added DeepSeek V3 support to llama.cpp",
  "source_location": "report.md:42:0-140",
  "content_hash": "sha256:a1b2c3d4e5f6",
  "type": "code-api",
  "decomposition": {
    "mode": "and_enum",
    "sub_claims": [
      {
        "sub_id": "C001a",
        "claim_text": "PR #11049 was merged 2025-01-04",
        "derived": true,
        "type": "temporal",
        "expected_verifier": "rule_engine"
      }
    ]
  }
}
```

**来源:** Grill review（e2e 测试发现 LLM 行号不准 + 改写 claim_text，回溯到 edit 工具设计）

---

### DD-34 · check-atomicity 工具

从 validate-claims.sh 的 D 级分离，Phase 1 即时反馈。

```bash
check-atomicity "<claim_text>"
```

**输出：**

```json
{
  "match": true,
  "pattern": "and_enum",
  "sub_items": ["expert_weights_norm", "sigmoid gating", "MLA optimization"],
  "word_count": 18
}
```

**处理规则：**
- `match: true` + `sub_items.length > 1` → agent 生成 sub_claims[]（派生，不需要 locate-claim）
- `match: true` + `sub_items.length == 1` → 不需拆
- `match: false` + `word_count > 25` → `compound_embedded`
- `match: false` + `word_count <= 25` → 原子 claim，无需处理

**与 validate-claims.sh D 级的关系：** check-atomicity 在提取阶段即时给出拆解提示。validator D 级仅做验证——检查 claim 实际标注的 `decomposition_mode` 是否与 check-atomicity 的结果一致，不一致输出 warning（不再强制执行）。

**来源:** Grill review（validator 规则不透明导致多跑 retry loop）

---

### DD-26 · 增量 Diff 逻辑（修正版）

以旧 claim 为锚，不用全量重提取：

```
Phase 0 Incremental:

  git diff --unified=0 旧文档 新文档 → changed_ranges（hunk 格式）
  # hunk = "@@ -旧起始行,旧行数 +新起始行,新行数 @@"

  对每条旧 claim（source_location: "file.md:行号"）：
    → 检查行号是否落在任意 hunk 的旧行范围内
    → 未落在任何 hunk 范围内 → 原文未改动 → carry forward ✅
      （可选验证：hash source_location 处的文本 == old content_hash）
    → 落在某 hunk 范围内 → change → 加入 re-extract queue
      （含 hunk 所在章节的上下文中所有相关新旧 claim）

  只有 queue 中的 claim 触发 LLM 重新提取。
```

**为什么不用 content_hash 搜索定位：** 不可能在新文档中对所有可能的子串切分计算 hash 进行比较（O(n²)）。

**为什么 hash 验证替代不了 hunk 检查：** hash 验证只能确认 carry forward 的 claim 内容没变（第二步），但第一步需要先知道**哪些旧 claim 可能仍然有效**——这正是 hunk 范围检查做的事。hunk 先筛选出未改动的行→carry forward→hash 确认。hunk 漏过的语义变化（行号没变但内容改了）由 hash catch。

**性能：** 不在 diff 中的 claim 零操作，只对变化区域重新提取 2-5 条。

**来源:** Grill followup

---

### DD-27 · 三方一致性校验

校验器 C 级执行三方一致性检查：

| 检查项 | 条件 | 失败 code |
|--------|------|----------|
| source_location 有效 | 可读原文 | INVALID_LOCATION |
| claim_text == 原文 | 逐字相同 | TEXT_MISMATCH |
| 实际 hash == content_hash | 三方一致 | HASH_MISMATCH |

- TEXT_MISMATCH / INVALID_LOCATION → per-claim diff 修补 loop
- HASH_MISMATCH → 自动修正（校验器重写为正确值）

**来源:** Grill followup

---

### DD-28 · REFUTED → CONTRADICTED 改名

`REFUTED` 与 `REFUSED` 视觉差异太小（差 1 个字母），容易混淆。改名后对齐 truth (blasrodri) 的命名：

- `REFUTED` → `CONTRADICTED` — 证据明确反对该声明
- `REFUSED` → 保持不变 — 声明类型不可验证

所有文件中的 verdict 名称已全局替换。

**来源:** Grill review

---

### DD-29 · 判断型细化：纯价值 vs 社区归因

原设计的"判断型直接 REFUSED"过于粗粒度。修正为三档：

| 子类 | 模式 | 处理 | 例子 |
|------|------|------|------|
| **纯价值判断** | `比.*更好`、`优于`、`is better than` | `REFUSED` | "这个方案更适合" |
| **社区归因** | `社区认为`、`根据.*称`、`according to`、`reported by` | `web_search` (T3) | "社区认为 llama.cpp 最活跃" |
| **模糊推断** | `可能`、`应该`、`may be` | `REFUSED` | "可能和 NUMA 有关" |

社区归因类进入 Phase 5 正常验证，证明"有人确实说过"而非"说的话是否正确"（T3 证据，最多 NUANCED）。

**来源:** Grill review

---

### DD-30 · CLI 精简 + Phase 0 自动检测

**3 条命令取代原有的 4 参数：**

| 调用 | 行为 |
|------|------|
| `/fact-check <path>` | 默认增量——无 ledger → 全量；有 ledger → 增量 |
| `/fact-check <path> --full` | 强制全量 |
| `/fact-check --status` | 累计统计 |

**Phase 0 自动检测：**
- `git remote` → 自动提取 owner/repo（GitHub P0 验证用）；非 git → NO_REPO
- `git branch` → 自动作为 session_tag
- `documents/<key>.ledger.jsonl` 存在性 + `--full` flag → 决定 full/incremental
- `git diff` → incremental 时检测 changed_ranges
- `<path>` 为目录 → 发现所有直接子 `.md` 文件 → 各自独立 run

**删除的参数：** `--incremental`（自动检测）、`--tag`（自动取 branch 名）、`--repo`（git remote）、`--dry-run`（Phase 4 等价）

**来源:** Grill review

---

### DD-31 · 子 Agent 并行化策略（能力驱动，自动检测）

#### 设计原则

- **不写死 agent 名称** — 不同用户的 pi 安装的子 agent extension 不同，写死 `anysearch-researcher` 会导致换一台机器就不可用
- **能力驱动映射** — 每个并行点定义"需要什么能力"，Phase 0 在运行时从已安装 agent 中匹配
- **自动检测 + 优雅降级** — Phase 0 检测 `pi-subagents` extension 是否存在；不存在则退化为单 session 串行

#### 能力 →Agent 映射表

| 能力 key | 含义 | 匹配规则 | 优先级 |
|----------|------|---------|--------|
| `extract_worker` | 能读文件、理解 prompt、输出结构化 JSON 的通用 LLM agent | agent 有 `read` + `bash` 工具，非 reviewer | `worker` → `delegate` → 首个非 oracle/scout agent |
| `web_searcher` | 有 web 搜索能力的 agent | agent 描述含 `search` / `web` / `research`，或 tool list 含 web_search | `anysearch-researcher` → `researcher` → 首个匹配 agent |
| `model_alt` | 能用不同 provider/model 的 LLM agent | `delegate` 且支持 model override | `delegate`（model override） → 跳过 triage |

#### Phase 0 检测流程

```
Phase 0 Init（扩展）:

  1. 尝试 subagent({ action: "list" })
     → 成功 → 记录 installed_agents = [...]
     → 失败（工具不存在） → subagents_available = false

  2. 如果 subagents_available:
     a. 按能力 key 匹配 agent
     b. 记录 capability_map = { extract_worker: "worker", web_searcher: "anysearch-researcher", ... }
     c. 注入到 run.json 的 agent_config 中
     d. 日志: "Subagents detected: ... (Phase 1/3b/5 parallelized)"

  3. 如果 !subagents_available:
     a. 日志: "Subagents not available, running single-session"
     b. 后续所有并行点执行 inline
```

#### 并行化阶段

| Phase | 并行粒度 | Concurrency | 子 agent Context | 失败处理 |
|-------|---------|-------------|-----------------|---------|
| **1 Extract** | 1 worker / 文档 | ≤ 4 | `fresh` | 单个 worker 失败不影响其他文档 |
| **3b Triage** | 1 delegate / batch | ≤ 2 | `fresh` | triage 失败→所有 escape 的 claim 回退到 Phase 5 |
| **5 Deep Verify** | 1 searcher / batch (4-5 claims) | ≤ 4 | `fresh` | batch 超时→该批 mark UNVERIFIABLE + 重试 1 次 |

#### Prompt 模板

见 `references/subagent-tasks.md` — 每个阶段定义了：输入文件、task prompt 模板、输出格式、失败处理。Agent 在运行时从模板动态生成 task。

**来源:** Grill review

---

### DD-32 · Phase 5 搜索精炼 Loop

Phase 5 深度验证引入质量反馈循环——第一轮搜索无高质量结果时，通过 LLM query 改写 + 重新搜索来迭代提升证据质量。采用 RAG 场景常见的 multi-query + step-back 手段。

#### 搜索策略：两阶段质量驱动

```
R0: normalized_claim 搜索
  ├─ T1/T2 结果 → grade → verdict ✅ exit
  ├─ 仅 T3 → R1: LLM 精炼 query（"找官方出处/论文/PR"）
  │   ├─ 搜到 T1/T2 → grade → verdict ✅
  │   └─ 仍仅 T3 → NUANCED（confidence=low）🟡
  └─ 零结果 → R1: LLM 生成 2 并行 multi-query（换措辞/step-back 放宽主题）
      ├─ 搜到 T1-T3 → grade → verdict ✅
      └─ 仍零结果 → UNVERIFIABLE ⚪
```

**零结果与仅 T3 走不同 R1 策略：** 零结果需要更宽泛的 query，仅 T3 需要更精确的指向（"找官方来源"）。

#### 查询生成手段

| 手段 | 做法 | 适用轮次 |
|------|------|---------|
| **Multi-Query** | 同一 claim 生成 2-3 个不同措辞的 query | R1（零结果场景） |
| **Step-Back** | 生成更抽象/宽泛的 query（去掉精确数值，保留主题词） | R1（零结果场景） |
| **精炼指向** | 针对 T3 结果，要求 LLM 生成"找官方出处"类 query | R1（仅 T3 场景） |

不使用 HyDE（先让 LLM 生成假想答案再用答案搜）——与 fact-check 的"不要猜"哲学冲突。

#### LLM 调用：全自动，单次 prompt

- 所有 claim 的 claim_text + 当前搜索结果（仅 T3 或无结果）作为输入
- LLM 一次调输出所有 R1 候选 query：`{ claim_id: [query1, query2], ... }`

#### 跨轮证据合并

所有轮次的结果全量保留，最高 tier 定 verdict，低 tier 保留在 evidence 数组作为 supplementary：

```json
{
  "verdict": "NUANCED",
  "evidence": [
    { "tier": "T2", "source": "Phoronix benchmark", "primary": true },
    { "tier": "T3", "source": "Reddit user report", "supplementary": true }
  ]
}
```

#### 与批处理并行的适配

```
Phase 5:
  1. batch（4-5 claims/组）×并行子 agent 跑 R0 搜索
  2. 子 agent 返回结果 + needs_refinement: true/false + fallback_reason: "no_results"|"t3_only"
  3. 父 agent 收集所有 R1 候选 → 一次 LLM 调用批量生成所有 R1 query
  4. R1 候选重新分组 batch → 并行子 agent 跑 R1 搜索
  5. 全量证据合并 + grade → 写入 claims.json
```

**来源:** Grill review（loop 设计）

以下项目设计已收敛，实现优先级在 `references/todos.md` 的 R6-R10：

- 非 markdown 文档的处理 (PDF, HTML, 纯文本) — R6
- 超大文档 (>50 条 claim) 的分片策略 — R7
- Phase 8 Agent Fix 的逐项交互与 handoff.md 格式规范 — R8/R9
- total-stats.json 自动聚合逻辑 — R10

已解决并文档化：LLM 提取 prompt（`prompts/extract-claims.md`）、正则路由规则（`references/regex-rules.json`）、校验器 loop（DD-22）、locate-claim 工具（DD-33）、check-atomicity 工具（DD-34）、嵌套 claim 模型（DD-33）、Phase 5 搜索精炼 Loop（DD-32）、增量 diff（DD-26）、CLI 精简（DD-30）、子 agent 并行化（DD-31）

## 参考来源

- [pi-skill-deep-research](https://github.com/Firstp1ck/npm-packages) — 证据 tier + policy.json 确定性裁决
- [machug/fact-checker](https://github.com/machug/fact-checker) — 7 步流水线 + NUANCED/OUTDATED verdict
- [blasrodri/truth](https://github.com/blasrodri/truth) — Refused/Unproven + 确定性验证哲学
- [pi-hifi](https://github.com/veschin/pi-hifi) — Observation vs Claim 分离 + Composer DAG
- [zhjai/groundcheck](https://github.com/zhjai/groundcheck) — Claim Ledger schema + 状态机 + 证据时效
- 本项目 17 份已有 fact-check 报告 — 实际错误类型和检测方法总结

---

## 横向对比：fact-check 与参考项目

> 评估 fact-check 对 5 个参考项目的吸收程度与增量价值。

### 一、各参考项目贡献与吸收方式

| 参考项目 | 核心贡献 | fact-check 吸收位置 | 吸收程度 |
|----------|---------|-------------------|---------|
| **pi-skill-deep-research** | evidence tier + policy.json 确定性裁决 | DD-04 证据层级、DD-02 规则引擎 P0/P1/P2 | 全量吸收，扩展至 20+ 条 P0 规则 |
| **machug/fact-checker** | 7 步流水线 + NUANCED/OUTDATED verdict + 多模型 triage | DD-19 流水线（扩为 9 阶段）、DD-03 verdict 体系、DD-06 Phase 3b triage | 吸收结构，扩展 verdict 数量（5→7），triage 降本优化（2-3 模型→1 个不同 provider） |
| **blasrodri/truth** | REFUSED/Unproven + 确定性验证哲学 + regex-first 路由方法论 | DD-03（REFUSED/UNVERIFIABLE）、DD-02 规则引擎、DD-06 双通道路由 | 吸收哲学与方法论；细化判断型为 4 子类；regex 从提取用途改为路由用途 |
| **pi-hifi** | Observation vs Claim 分离 + Composer DAG（fixed catalog） | DD-06 claim 分类、拆解 catalog（7 模式）、DD-22 D 级原子性校验 | 吸收 catalog 约束思想，改为 flat catalog 非多层 DAG |
| **zhjai/groundcheck** | Claim Ledger schema + 状态机 + 证据时效性 + 复合拆解前置 | DD-09/DD-10 ledger、DD-14 状态机、DD-13 时效性、DD-06 拆解前置 | 全量吸收，增量优化（hunk+hash diff、按文档分 ledger） |

### 二、系统整合价值

每个参考项目解决一个子问题。fact-check 是唯一把所有子问题整合进一条完整 end-to-end 流水线的：

```
Phase 0 自动检测 → Phase 1 提取+分类+拆解 → Phase 2 双通道路由
→ Phase 3a 规则引擎 → Phase 3b Triage → Phase 4 检查点
→ Phase 5 深度搜索 → Phase 6-8 输出+修正
```

参考项目各管一段：deep-research 只管证据分级，fact-checker 只管流水线结构，truth 只管裁决哲学，pi-hifi 只管结构分解，groundcheck 只管 ledger。**fact-check 是完整整车集成，不是又一个零件。**

### 三、对参考项目的关键优化

| 参考项目设计 | fact-check 的改进 |
|-------------|-----------------|
| truth 的"判断型直接拒绝" | 细化为 4 子类（纯价值/社区归因/模糊推断/事实性），社区归因进入搜索验证（T3），不直接 REFUSED |
| fact-checker 的 7 步流水线 + 2-3 模型 triage | 扩展为 9 阶段（补充校验器 loop、triage 分流、检查点交互、Phase 8 修正）；triage 降为 1 次不同 provider 调用 |
| pi-hifi 的 Composer DAG（LLM 自由拆解） | 改为固定 7 模式 catalog，LLM 只能选模式+定深度，不匹配→标记 `compound_embedded` 而非强行拆 |
| groundcheck 的全量重提取 | 增量 diff 双重验证：git hunk 范围筛选（廉价）+ content_hash 确认（精确），只对变化区域重新提取 |
| deep-research 的 4 参数 CLI | 精简为 3 条命令，Phase 0 自动检测 git context、ledger、--full flag |
| truth 的 regex 提取代码 claim | 改为 regex 路由用途：按 claim 类型分派到规则引擎/搜索/REFUSED，LLM 补 regex 语义盲区 |
| fact-checker 的多模型 triage | 吸收为 Phase 3b，规则引擎先行处理 authority，剩余 claim 才进入 triage，不浪费 LLM 调用 |

### 四、潜在弱点

1. **对参考项目的过度依赖** — 5 个参考项目贡献了设计的主体骨架。如果任何一个参考项目缺失，这个设计无法写成现在这样。
2. **复杂度过高** — 9 阶段流水线 + 4 级校验 + 双通道路由 + triage + 并行化 + 增量 diff。运行时失败模式多，调试难度大。
3. **pi 生态绑定** — 子 agent 并行化、checkpoint 交互、prompt 模板都深度依赖 pi agent 能力。迁移到其他平台需重写集成层。
4. **校验循环的成本边界** — per-claim diff 修补每次仍需调 LLM。50+ claim 文档的校验循环本身是可观开销。
5. **缺少实证验证** — 设计完整，但 triage、增量 diff、并行化在 17 份已有报告中的实际效果尚未量化。

### 五、结论

**fact-check 的独特价值不在于发明新范式，而在于系统整合 + 关键节点的工程优化。** 对 5 个参考项目的吸收是诚实的（所有设计决策标注出处），每一项决策都标记了 `来源: Grill Qx`。独特增量在：校验器 loop 的 per-claim diff 修补、增量 diff 双重验证（hunk+hash）、capability-driven 子 agent 并行化、CLI 自动检测精简——这些解决的不是"如何做事实核查"，而是"把这些零件拼在一起时产生的实际工程问题"。
