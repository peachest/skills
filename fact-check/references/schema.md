# Claim Extraction Schema

LLM 从文本文档中提取结构化 claim 的 JSON schema。

## 提取格式

```json
[
  {
    "claim_id": "C001",
    "claim_text": "DeepSeek V3.1 was released in September 2025",
    "normalized_claim": "DeepSeek V3.1 release date September 2025",
    "source_location": "report-1.md:42:10-63",
    "content_hash": "sha256:7d1e9f3a2b4c",
    "type": "temporal",
    "expected_verifier": "web_search",
    "atomicity_parent": null,
    "decomposition_mode": null,
    "compound_flag": null
  }
]
```

## 字段说明

| 字段 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `claim_id` | ✅ | string | 运行内唯一标识, 格式 `C{NNN}` (C001, C002...) |
| `claim_text` | ✅ | string | LLM 从文档中提取的原文措辞, **保持原样不做 reword** |
| `normalized_claim` | ⭕ | string | 可选, LLM 标准化后的表述 (去除口头化、补全隐含信息) |
| `source_location` | ✅ | string | 原始文档路径 + 定位，三模式：`doc.md:42` (整行) / `doc.md:42-45` (跨行) / `doc.md:42:10-85` (行内字符范围) |
| `content_hash` | ⭕ | string | **校验器计算**（非 LLM），SHA256(trim(lowercase(原文 at source_location)))[:12]，前缀 `sha256:` |
| `type` | ✅ | enum | 见下方分类（核心层 12 类 + 扩展层 8 类） |
| `expected_verifier` | ⭕ | enum | LLM 建议的验证器: `rule_engine` / `web_search` / `refused` / `inferred`; 规则引擎可能覆盖 |
| `atomicity_parent` | ⭕ | string | 子 claim 指向父 claim_id（sentence group id，非层级 tree），复合声明拆解时使用 |
| `decomposition_mode` | ⭕ | enum | 拆解使用的 catalog 模式: `and_enum` / `paren_append` / `paren_expand` / `from_to` / `clause_embed` / `ie_supplement` / `dash_supplement` |
| `compound_flag` | ⭕ | string | 无法匹配 catalog 的复合结构标记为 `compound_embedded` |

## type 枚举

### 核心层（始终启用，12 类）

| 值 | 说明 | 示例 |
|----|------|------|
| `authority` | 确权型声明 | "PR #11049", "arXiv:2605.18071" |
| `numerical` | 数值性声明 | "6.44 tok/s on EPYC 9474F" |
| `temporal` | 日期/时间性声明 | "V3.1 was released in September 2025" |
| `factual` | 简单事实描述 | "llama.cpp 支持 DeepSeek V3" |
| `causal` | 因果或相关性声明 | "双路比单路降 32-38% 因 NUMA 开销" |
| `comparative` | 比较性声明 | "vLLM 比 SGLang 快 36%" |
| `code-api` | API/代码接口声明 | "PR #11049 新增 expert_weights_norm" |
| `citation` | 引用声明（论文/编号） | "arXiv:2605.18071 存在" |
| `interpretation` | 解释性/推导性声明 → `INFERRED` verdict | "MLA 压缩到 ~1/32 使 CPU 推理可行" |
| `existence` | 存在性声明（产品/项目） | "KTransformers 有 17K GitHub stars" |
| `file_path` | 文件路径声明 | "src/config.rs 中定义了 MAX_RETRIES" |
| `attribution` | 社区归因声明 | "社区认为 llama.cpp 最活跃" |

### 扩展层（文档自动检测，新增不删除，8 类）

| 值 | 说明 | 自动检测关键词 |
|----|------|--------------|
| `legal-med-fin` | 法律/医疗/金融高风险声明 | 法律/医疗/金融术语 |
| `pricing` | 定价声明 | `$/token`, `$/user/month`, `cost` |
| `capability` | 产品能力声明 | `supports`, `includes`, `integrates` |
| `date` | 日期声明（产品发布、GA） | `GA`, `announced`, `released` |
| `licensing` | 许可声明 | `license`, `E5`, `included in` |
| `compliance` | 合规声明 | `FedRAMP`, `ISO`, `certified` |
| `architecture` | 架构声明 | `uses X for Y`, `routes through` |
| `status` | 状态声明 | `preview`, `GA`, `deprecated` |

## 复合 Claim 拆解规则（Fixed Catalog）

LLM 只能从以下 7 种 catalog 模式中选择拆解。不匹配 catalog 的复合结构 → 不拆，标记 `compound_flag: "compound_embedded"`。

| 模式 | `decomposition_mode` | 触发条件 | 拆解规则 | 示例 |
|------|---------------------|---------|---------|------|
| **AND-枚举** | `and_enum` | 包含 `and/和/以及/且/、` 连接 ≥2 个并列项 | 按并列项拆为独立 claim | "supports A, B, and C" → 3 claims |
| **括号-补充** | `paren_append` | 包含 `(...)` 或 `（...）`，括号内是时间/人名/数值 | 括号内拆为独立 claim | "PR #11049 (merged 2025-01-04)" → 2 claims |
| **括号-展开** | `paren_expand` | 包含 `（A，B，C）` 逗号分隔的多项 | 每项一个 claim | "V3.1（2025年9月发布，128K 上下文）" → 2 claims |
| **FROM-TO** | `from_to` | 包含 `从 X 到 Y` / `from X to Y` / `X→Y` | 拆为 before + after 两个 claim | "从 20 分钟压缩到 7 秒" → 2 claims |
| **从句嵌入** | `clause_embed` | claim > 25 词 + 包含 `which`/`that`/`的` 从句标记 | 拆为主句 claim + 从句 claim | "PR #11049, which was merged..., adds V3" → 2 claims |
| **即-补充** | `ie_supplement` | 包含 `X，即 Y，Z` / `X, i.e., Y` | 拆为 X claim + Y claim | "MLA，即 Multi-head Latent Attention，压缩 KV" → 2 claims |
| **破折号补充** | `dash_supplement` | 包含 `——` 或 `--` 分隔的独立断言 | 破折号前后各为独立 claim | "Q4_K_M 量化——约 404GB——在 EPYC 上可达 6.44 tok/s" → 2 claims |

每个子 claim 设置 `atomicity_parent` 指向逻辑父组（同一句的所有子 claim 共享同一个 parent id），`decomposition_mode` 标记使用的模式。

## content_hash 计算规则

- **计算者:** 校验器（Phase 1 validation loop），LLM 不参与
- **输入:** 源文档 `source_location` 指向的原文
- **算法:** `SHA256(trim(lowercase(原文)).replace(/\s+/g, ' '))[:12]`
- **格式:** 前缀 `sha256:` 后跟 12 字符 hex，如 `sha256:7d1e9f3a2b4c`
- **用途:** 校验器三方一致性检查，增量 diff 时 match 旧 claim

## 不可提取为 claim 的内容

以下类型的文本不必提取为 claim:
- 纯 opinional 的表达（"这个方案更好"、"建议读者参考"）
- 文档标题、目录结构描述
- 过渡句、无具体信息的上下文铺垫
- 作者自述或不涉及外部事实的内容

## 提取质量控制

- 单次提取不超过 50 条 claim; 超过则分段提取
- 每条 claim 的 claim_text 必须可追溯到原文的完整句子
- 不要改写、补全、或推断原文未明确写出的数字
- 对原文引用他人数据的声明, 保持引用原文的措辞而非数据本身
