# Fact-Check 测试规划

> 方案 D + B：合成文档靶向测试 + per-component 单元测试。
> 参考项目：truth（YAML fixture golden verdict）、fact-checker（pytest unit test）。

## 文件布局

```
tests/
├── README.md                     # 本文件
├── conftest.py                   # shared pytest fixtures
├── requirements.txt              # pytest, jsonschema
│
├── fixtures/                     # 方案 D：合成文档
│   ├── synth-auth.md             # 7 条 claim，覆盖 P0 verifier (DOI, repo, npm, SPDX, URL, gitee repo, gitlab issue)
│   ├── synth-bench.md            # 6 条 claim，覆盖 arXiv, PR, numerical, temporal, benchmark
│   ├── synth-decomp.md           # 8 条 claim，覆盖 7 种 catalog 拆解模式 + compound_embedded
│   ├── synth-judgment.md         # 5 条 claim，覆盖 REFUSED / hedging_factual / 社区归因边界
│   ├── synth-inference.md        # 4 条 claim，覆盖 INFERRED (causal, significance) + comparative
│   ├── synth-patent.md           # 7 条 claim，覆盖 Patent, IETF Draft, RFC, PMID, Git commit, Git tag, DOI
│   ├── synth-package.md          # 7 条 claim，覆盖 PyPI, Cargo, Go module, NuGet, Docker, HuggingFace, gitlab MR
│   └── synth-extension.md        # 5 条 claim，覆盖扩展层自动检测 (pricing, compliance, route, port)
│
├── golden/                       # Golden verdicts (手工标注)
│   ├── synth-auth.golden.json
│   ├── synth-bench.golden.json
│   ├── synth-decomp.golden.json
│   ├── synth-judgment.golden.json
│   ├── synth-inference.golden.json
│   ├── synth-patent.golden.json
│   ├── synth-package.golden.json
│   └── synth-extension.golden.json
│
├── test_parse.py                 # 方案 B：解析 [CLAIM] 块输出
├── test_regex_routing.py         # 方案 B：25 条 authority + judgment + interpretation 路由
├── test_rule_engine.py           # 方案 B：P0 确定性 verifier
├── test_hash.py                  # 方案 B：content_hash 计算 + VID 生成
├── test_schema.py                # 方案 B：JSON schema 校验 (A/B 级校验器)
├── test_ledger.py                # 方案 B：ledger append/query/carry-forward
├── test_report.py                # 方案 B：report.md 格式生成
└── test_decomposition.py         # 方案 B：7 种 catalog 模式拆分 + compound_embedded 检测
```

## 方案 D：合成文档靶向测试

### 覆盖矩阵

| 合成文档 | claims | 覆盖目标 |
|---------|--------|---------|
| `synth-auth.md` | 7 | P0: DOI, GitHub repo, npm package, SPDX license, URL, Gitee repo, GitLab issue |
| `synth-bench.md` | 6 | P0: arXiv ID, GitHub PR#; P2: numerical, temporal; 扩展层 code-api |
| `synth-decomp.md` | 8 | 7 种拆解模式 + compound_embedded 标记 |
| `synth-judgment.md` | 5 | REFUSED (纯价值), hedging_factual (含可验证原子), REFUSED (模糊推断), 社区归因 (web_search, T3), 边界: 含数字但无实体的"可能" |
| `synth-inference.md` | 4 | INFERRED (causal 使...可行), INFERRED (significance 关键), comparative, interpretation |
| `synth-patent.md` | 7 | P0: Patent (US/CN/WO), IETF Draft, RFC, PMID, Git commit, Git tag, DOI |
| `synth-package.md` | 7 | P0: PyPI package, Cargo crate, Go module, NuGet package, Docker image; P1: HuggingFace model, GitLab MR |
| `synth-extension.md` | 5 | 扩展层自动检测: pricing ($/token/定价), compliance (FedRAMP/合规), route (/api/), port (:8080), retry |

### 断言策略

每个合成文档对应一份 `golden.json`，跑完 Phase 1-3a 后对照断言：

```json
[
  {
    "claim_text": "We use MIT license",
    "expected_type": "authority",
    "expected_verdict": "SUPPORTED",
    "expected_verifier": "rule_engine.spdx_license"
  }
]
```

LLM 提取阶段的 `claim_text` 措辞可能变化 → golden 匹配用 **normalized_claim** + **type**，不精确匹配 claim_text。

### 运行方式

```bash
# 对单个合成文档跑 full pipeline（Phase 1-3a only，不触发搜索）
fact-check tests/fixtures/synth-auth.md --full --stop-at=phase3a

# 对比 golden
pytest tests/test_golden.py -v
```

## 方案 B：Per-Component 单元测试

| 测试文件 | 被测目标 | 测试数 | 断言类型 |
|---------|---------|--------|---------|
| `test_parse.py` | `parse_claims_output()` | 8 | 空输入 / 缺字段 / 多 claim / [CLAIM] 块交错 / claim_text 含冒号 / 空行 |
| `test_regex_routing.py` | 25 authority + 3 judgment + 2 interpretation 规则 | 30+ | 正向匹配 / 负向不匹配 / 优先级（url before repo）/ 中文输入 / hedging_factual guard |
| `test_rule_engine.py` | arxiv, doi, url, code_platform, npm, pypi, cargo, go_module, nuget, rfc, pmid, patent, ietf_draft, docker, spdx_license, git_commit, git_tag 各 verifier | 25+ | 返回值 shape / 已知存在的实体 → SUPPORTED / 不存在的实体 → CONTRADICTED / HTTP 错误 → UNVERIFIABLE |
| `test_hash.py` | `compute_content_hash()`, `generate_vid()` | 6 | 同文同 hash / 大小写不敏感 / hash 长度 / vid 格式 |
| `test_schema.py` | claims.json 的 JSON schema 校验 | 8 | 合法 claim / 缺必需字段 / type 枚举非法 / source_location 格式 / decomposition_mode 枚举 |
| `test_ledger.py` | ledger append / query / carry-forward / vid 覆盖 | 6 | append 计数 / 同 vid 后写覆盖 / 文件夹不存在创建 / 查询按 vid |
| `test_report.py` | markdown 报告格式生成 | 5 | summary 表 / 分区 / verdict 图标 / severity confidence 字段 / 空 claim |
| `test_decomposition.py` | 7 种 catalog 模式正则 + compound_embedded 检测 | 10 | and_enum 拆 / paren_append 拆 / paren_expand 拆 / from_to 拆 / clause_embed 拆 / ie_supplement 拆 / dash_supplement 拆 / compound_embedded 标记 / 非 catalog 复合不拆 / >25 词无匹配标记 |

### 运行方式

```bash
cd tests
pip install -r requirements.txt
pytest -v
```

## 与 examples/ 的关系

3 份 examples（冷启动报告、KV Cache 文章、ATaaS）不在本轮 D+B 计划中作为输入，而是作为 **素材库**：
- 合成文档的 claim 措辞和类型从这些 examples 中提取真实模式
- 规则引擎的测试 case 中使用的真实 arXiv ID、repo 路径等从 examples 中提取
- 等 D+B 稳定后，examples 可作为方案 A/C 的输入

## 验收标准

- [ ] 8 个合成文档各自 `pytest` 通过（golden verdict 命中率 ≥ 95%）
- [x] 8 个组件测试文件全部 `pytest` 通过（107 passed, 0 failures）
- [x] `test_regex_routing.py` 覆盖全部 25 条 authority 规则（1 case/docstring per rule）
- [x] `test_rule_engine.py` 至少覆盖 15 个 P0 verifier（存在/不存在/故障各 1 case）
- [x] 无测试文件依赖外部网络（rule_engine 测试 mock `_fetch_head`）

## xfail 映射（→ specs/todos.md）

| xfail test | 所属文件 | → R | 修复位置 |
|-----------|---------|-----|---------|
| `test_go_module` | test_regex_routing.py | **R2** | regex-rules.json：`go_module` 规则需要排在 `github_repo` 之前 |
| `test_patent_cn` | test_regex_routing.py | **R2** | regex-rules.json：patent 规则增加无 `\b` 锚定的中文上下文模式 |
| `test_opinion_vague_refused` | test_regex_routing.py | **R2** | regex-rules.json：opinion_vague patterns 补入 `大概` |
| `test_hedging_factual_web_search` | test_regex_routing.py | **R2** | regex-rules.json：`github_repo` 裸 name/name 模式误匹配硬件名（H100、A100），需限定或调序 |
| `test_hedging_no_atoms_refused` | test_regex_routing.py | **R1** | Phase 2 双通道路由：实现 `check_contains_verifiable_atoms` guard |
| `test_url_before_repo` | test_regex_routing.py | **R2** | regex-rules.json：`url` 规则需要排在 `github_repo` 之前 |
| `test_de_clause_cn` | test_decomposition.py | **R2** | regex-rules.json：`clause_embed` 模式去掉 `\b` 锚定，适配中文 |
