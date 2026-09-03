# project-wiki vs doc-system-kb-builder 对比调查（2026-09-05）

> 调查快照：对比本地 skill `engineering/project-wiki` 与开源项目
> `buccaneermethodology/doc-system-kb-builder-skill`（doc-as-data 文档知识库），
> 结论已部分落地为 project-wiki 的代码改进（见文末"落地记录"）。

## 背景

- 文章：《把文档当代码一样治：doc-system-kb-builder 让"文档又和现实漂了"变成一件能跑回归的事》（Alan Hsu 公众号，2026-09）
  - 抓取快照：`/tmp/wx-article.md`（临时，重启即失）
- 仓库实际地址：`github.com/buccaneermethodology/doc-system-kb-builder-skill`（**文章里的链接少了 `-skill` 后缀，原地址 404**）
  - README 快照：`/tmp/dskb-readme.md`；全量 REFERENCE：`/tmp/dskb-ref.md`（临时）

## 核心结论：同一模式，方向相反

两者都是「唯一真相源 + 投影 + 漂移检测」架构，但箭头方向相反：

```
project-wiki:   代码 ──(SHA baseline)──> wiki 表格     源=代码，投影可人工编辑
dskb:           JSON ──(确定性渲染)──>  Markdown      源=JSON，投影禁止人工编辑
```

| 维度 | project-wiki | doc-system-kb-builder |
|---|---|---|
| 解决的问题 | 定向（orientation）：秒懂代码地形 | 文档治理：漂移、权威归属、演进记录 |
| 真相源 | 代码文件 + SHA baseline | `data/*.json`（owner/status/depends_on 元数据） |
| 投影 | 人工/AI 填写的 markdown 表格，允许编辑 | 渲染生成，手改即 drift（fail） |
| 漂移语义 | 代码变了地图没跟上（源驱动） | 投影被手改/没重渲染（投影驱动） |
| 来源分类 | 无 | canonical / strategy / evolution 三桶 + 执行状态禁入 |
| 检测的"真相接近度" | 更高：SHA 变必触发 | 只保证投影↔JSON 一致，JSON 错照渲染错的 |
| 测试 | （调查时）无 | fail-closed 正反例齐全 |

## 是否整合：不整合

1. **数据模型根本冲突**：dskb 核心契约"markdown 不可手改"，project-wiki 核心工作流"AI/人直接填表格行"。整合 = L1/L2 也要 JSON 渲染，工作流变重而表格行无复杂结构，收益为负。
2. **问题域不同**：代码地图（代码是真相）vs 知识库（JSON 是真相），强行统一会把轻量定向工具拖成文档治理系统。
3. **真正对味的场景另在**：dskb 思路更贴近 okb skill（bronze→silver→gold）和本仓库 `docs/agents/*.md` 规范文档——如果将来要让"agent 必读文档"防漂移，那是项目级引入 doc-as-data 的时机，不是改 project-wiki。

## 借鉴（已落地）

从 dskb 抄来的模式，按价值排序：

1. **fail-closed 测试套**（最大缺口）→ `tests/test_wiki.py`，27 个用例：正例 + 反例（每个信号码的触发形状）+ 双 runtime JSON parity + 交叉 runtime 互换。
2. **稳定错误码 + `--json`** → 8 个 `WIKI-*` 信号码成为公共契约（新增 additive，改名 breaking）；所有命令支持 `--json` 结构化输出供 CI/hook/agent 消费。
3. **wiki 自身完整性检查**（dskb 的 KB-RENDER-DRIFT 启发）→ 三方一致性断言：overview 索引 ↔ module wiki 文件 ↔ 注册表行。新增 4 个 🟣 信号码；`update` 增加"为缺失 module 生成骨架"修复路径。
4. **Evidence boundary 声明** → SKILL.md 明确：check 绿 = 结构覆盖一致，**≠** 描述准确（描述质量由填写工作流产生，工具不验证）。

明确**不抄**的：doc_type 三桶、owner/审批链元数据——那是文档治理的负担，定向工具不需要（过度工程）。

## dskb 关键事实备查

- 五个 finding codes：`KB-INVALID-SOURCE` / `KB-DUPLICATE-DOC-ID` / `KB-EXECUTION-STATE-IN-CANONICAL` / `KB-RENDER-DRIFT` / `KB-MIGRATION-PROVENANCE-MISSING`
- 渲染器只认 `narrative`/`definition`/`table` 三种 section kind；新增 kind = 契约扩展（校验+确定性渲染+正反例+排序）
- 迁移策略：`migrate_markdown.py` 产出**待审 JSON 草稿**（带 SHA-256 provenance），绝不直接进正式源；分批小步
- 关键警句（evidence boundary 原文）："Passing these checks proves only that the bundled data satisfies the documented structural rules and that its Markdown projection is consistent. It does not approve the content."

## 落地记录（2026-09-05）

改动文件（skill 目录 `engineering/project-wiki/`）：
- `scripts/wiki.py` / `scripts/wiki.js`：`--json` + 8 信号码 + 完整性检查 + update 骨架修复（双侧 lockstep，parity 测试强制）
- `tests/`（conftest + test_wiki）+ `pyproject.toml`：verify 入口 `uv run pytest`，27 passed
- `SKILL.md`：信号码表、JSON 形状、evidence boundary、Verify 章节
- 开发中抓到的真实 bug：JS `sortSignals()` 返回新数组未赋值 → 双 runtime 信号顺序不一致（正是 parity 测试要防的那类漂移）
