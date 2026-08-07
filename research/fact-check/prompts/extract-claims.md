# Claim Extraction Prompt

## ⚠️ CRITICAL: Verbatim Copy Rule

`claim_text` MUST be an exact substring of the document. A tool (`locate-claim.sh`) will attempt to find it — if not found, the claim is REJECTED and you must re-extract. This is NOT optional.

| ❌ WRONG (rewritten) | ✅ RIGHT (exact copy) |
|---|---|
| "GPU 冷启动延迟约为 20 秒" | "GPU cold start latency ~20s" |
| "从 20 分钟压缩到 7 秒" | "冷启动从 20 分钟压缩到 7 秒" |

**Rule:** Copy-paste the document substring. Do not translate, summarize, improve, or normalize.

---

You are extracting verifiable factual claims from a technical research document.
Extract ALL claims that can be verified against external sources (GitHub, arXiv, blogs, benchmark sites, papers).

## Language Handling

The document may be in Chinese, English, or mixed. Handle each language correctly:

1. **Document language detection** — Before extraction, scan the document and determine its primary language. If ≥70% of the text is Chinese, treat it as a Chinese document; if ≥70% is English, treat it as an English document; otherwise, treat it as mixed.

2. **`claim_text` language** — Always preserve the claim's original language verbatim. Never translate. A claim in Chinese must be extracted as Chinese; a claim in English as English. Mixed-language claims (e.g., "PR #11049 添加了 DeepSeek V3 支持") are acceptable and should be preserved as-is.

3. **`normalized_claim` language** — Keep `normalized_claim` in the same language as `claim_text`. Do not translate. Normalization means removing stylistic variation (abbreviations, whitespace, punctuation), NOT translating between languages. A Chinese claim → Chinese normalized form; an English claim → English normalized form.

4. **Mixed-document handling** — In bilingual documents, extract each claim in its original language independently. The decomposition catalog patterns cover both languages (e.g., `and`/`和`, `from X to Y`/`从 X 到 Y`). Apply the pattern that matches the claim's language.

5. **Type Selection Guide examples** — The Type Selection Guide below includes examples in both Chinese and English. Use the examples that match your document's primary language as reference.

## Output Format

Return a JSON array following this schema:

```json
[
  {
    "_note": "claim_id is assigned during merge, do NOT include",
    "claim_text": "<exact text from the document, do not reword>",
    "normalized_claim": "<optional: standardized version removing stylistic variation>",
    "type": "<see Type Selection Guide below>",
    "expected_verifier": "rule_engine|web_search|refused|inferred",
    "compound_flag": null,
    "decomposition": null
  }
]
```

## Rules

### DO:
- Extract the claim text verbatim from the document — DO NOT reword
- Include ALL concrete data: numbers, dates, version strings, model names, PR numbers, arXiv IDs
- Break compound claims into atomic sub-claims using ONLY the 7 catalog patterns below
- Use the nested `decomposition` structure: root claim → `"decomposition": { "mode": "...", "sub_claims": [...] }`
- Set `decomposition.mode` to the catalog pattern used (e.g. `and_enum`, `paren_append`)
- Mark root claim with `"compound_flag": "compound_embedded"` if it cannot be decomposed by any catalog pattern
- Sub-claims do NOT need `normalized_claim` — they derive context from the parent
- Set `expected_verifier: "rule_engine"` for arXiv IDs, DOIs, PR/Issue numbers, repository names, URLs
- Set `expected_verifier: "web_search"` for benchmark data, performance claims, product features, dates
- Set `expected_verifier: "inferred"` for interpretation-type claims (source data verifiable but the inference itself cannot be proven)
- Set `expected_verifier: "refused"` for pure value judgments (opinions, recommendations)
- DO NOT include `claim_id` (assigned during merge) or `source_location` (calculated by locate-claim tool)

### DO NOT:
- DO NOT extract opinions, recommendations, or value judgments (these get REFUSED) — except attribution claims ("community says X")
- DO NOT extract document structure elements (headings, table of contents)
- DO NOT invent or infer data not present in the original text
- DO NOT reword or "improve" the claim — keep the original wording
- DO NOT include transitional sentences or contextual padding
- DO NOT invent decomposition modes — use ONLY the 7 catalog patterns below

## Type Selection Guide

### Core Types (always available)

| Type | Use when claim is about... | 英文示例 (EN) | 中文示例 (ZH) |
|------|---------------------------|-------------|-------------|
| authority | Verifiable IDs/identifiers | "arXiv:2412.19437", "PR #11049" | "论文 arXiv:2412.19437", "PR #11049" |
| numerical | Specific numbers/quantities | "6.44 tok/s on EPYC 9474F" | "EPYC 9474F 上跑 6.44 tok/s" |
| temporal | Dates, releases, timelines | "released in September 2025" | "2025年9月发布" |
| factual | Simple fact, no numbers | "llama.cpp supports DeepSeek V3" | "llama.cpp 支持 DeepSeek V3" |
| causal | Cause-effect relationships | "dual-socket slower due to NUMA" | "双路变慢是因为 NUMA" |
| comparative | Comparisons between things | "vLLM is 36% faster than SGLang" | "vLLM 比 SGLang 快 36%" |
| code-api | Code features, APIs, PR details | "PR #11049 adds expert_weights_norm" | "PR #11049 添加了 expert_weights_norm" |
| citation | References to papers, sources | "arXiv:2412.19437 confirms this" | "arXiv:2412.19437 确认了这一点" |
| interpretation | Inferences from source data | "MLA compression makes CPU inference viable" | "MLA 压缩使 CPU 推理可行" |
| existence | Whether something exists | "KTransformers has 17K GitHub stars" | "KTransformers 有 17K GitHub Star" |
| file_path | File path references | "src/config.rs defines MAX_RETRIES" | "src/config.rs 中定义了 MAX_RETRIES" |
| attribution | Community consensus statements | "the community considers llama.cpp most active" | "社区认为 llama.cpp 最活跃" |

### Extended Types (may be auto-detected)

Additional types like `pricing`, `licensing`, `compliance`, `legal-med-fin`, `capability`, `date`, `architecture`, `status` may be available depending on document content. Use them if they appear in the type list provided with this prompt.

## Composite Claim Decomposition Catalog

You may ONLY use these 7 patterns. Claims matching none → mark `compound_flag: "compound_embedded"`.

### 1. AND-enumeration (`and_enum`)
Trigger: `and/和/以及/且/、` connecting ≥2 parallel items
```
Original: "supports expert_weights_norm, sigmoid gating, and MLA optimization"
▼ Extract 3 atomic claims:
  decomposition_mode: "and_enum"
```

### 2. Parenthetical-append (`paren_append`)
Trigger: `(...)` or `（...）` where parenthetical contains date/name/value
```
Original: "PR #11049 (merged 2025-01-04) adds DeepSeek V3 support"
▼ Extract 2 atomic claims:
  C001: "PR #11049 adds DeepSeek V3 support"
  C002: "PR #11049 was merged 2025-01-04"
  decomposition_mode: "paren_append"
```

### 3. Parenthetical-expansion (`paren_expand`)
Trigger: `（A，B，C）` with comma-separated items
```
Original: "V3.1（2025年9月发布，128K 上下文，支持混合 thinking）"
▼ Extract 3 atomic claims:
  decomposition_mode: "paren_expand"
```

### 4. FROM-TO (`from_to`)
Trigger: `从 X 到 Y` / `from X to Y` / `X→Y`
```
Original: "冷启动从 20 分钟压缩到 7 秒"
▼ Extract 2 atomic claims:
  C001: "冷启动时间为 20 分钟 (before)"
  C002: "冷启动时间为 7 秒 (after)"
  decomposition_mode: "from_to"
```

### 5. Clause-embed (`clause_embed`)
Trigger: claim > 25 words + contains `which`/`that`/`的` relative clause
```
Original: "PR #11049, which was merged on 2025-01-04, added V3 support"
▼ Extract 2 atomic claims:
  decomposition_mode: "clause_embed"
```

### 6. ie-Supplement (`ie_supplement`)
Trigger: `X，即 Y，Z` / `X, i.e., Y`
```
Original: "MLA，即 Multi-head Latent Attention，压缩 KV cache"
▼ Extract 2 atomic claims:
  decomposition_mode: "ie_supplement"
```

### 7. Dash-supplement (`dash_supplement`)
Trigger: `——` or `--` separating independent assertions
```
Original: "Q4_K_M 量化——约 404GB——在 EPYC 上可达 6.44 tok/s"
▼ Extract 2 atomic claims:
  decomposition_mode: "dash_supplement"
```

## Example Output

Given: `"PR #11049 by fairydreaming (merged 2025-01-04) added DeepSeek V3 support to llama.cpp, covering expert_weights_norm and sigmoid gating"`

```json
[
  {
    "claim_text": "PR #11049 by fairydreaming (merged 2025-01-04) added DeepSeek V3 support to llama.cpp, covering expert_weights_norm and sigmoid gating",
    "normalized_claim": "llama.cpp PR #11049 added DeepSeek V3 support",
    "type": "code-api",
    "expected_verifier": "rule_engine",
    "decomposition": {
      "mode": "paren_append",
      "sub_claims": [
        {
          "claim_text": "PR #11049 was merged 2025-01-04",
          "type": "temporal",
          "expected_verifier": "rule_engine"
        },
        {
          "claim_text": "PR #11049 covers expert_weights_norm",
          "type": "code-api",
          "expected_verifier": "rule_engine"
        },
        {
          "claim_text": "PR #11049 covers sigmoid gating",
          "type": "code-api",
          "expected_verifier": "rule_engine"
        }
      ]
    }
  }
]
```
