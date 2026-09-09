# Skill Wiki — 持久知识层

灵感来自 WikiSkill（arXiv 2608.27454）：在一次性执行轨迹（raw）和可回滚的 skill 文件
（skills）之间，加一层**持续累积、永不回滚**的结构化知识。诊断不白做——每次的发现
增量合并进这里，下一次诊断站在已有知识之上，skill 编辑提案在此记账。

设计判定（哪些搬哪些不搬）：本地 `~/research/skill-eval-landscape/03-wikiskill-skill-evolution.md`。

## 目录结构

```
wiki/
├── _cross-skill/patterns.md   # 跨 skill 通用规律
└── <skill-name>/              # 与 skill frontmatter name 一致
    ├── patterns.md            # 模式条目（根因级）
    ├── logs.md                # 诊断运行日志（每次一行）
    └── skill-impact.md        # skill 编辑提案台账（含被拒提案）
```

## 写入者

- `skill-call-diagnose` step 5.5（合并 findings）与 step 6（提案记账）
- 非 diagnose 来源（人工整理、外部知识提取如 herdr-extract）可直接写入，条目可直接以任意合法状态入库（如 absorbed-into-skill），但必须走同样的 sanitize 规则

## patterns.md 条目格式

```markdown
## P-### 标题
- 状态: open | absorbed-into-skill | closed
- 现象: 可观察的行为（脱敏后）
- 根因: contract gap | agent 即兴（无契约缺口，含 repeated pattern）| 环境问题 | 知识提取
- 方案: 对应的沉淀方向（脚本/文档/上游）
- 证据: <session-id>#<entry>[,<entry>...]   ← 多 session 用逗号分隔；跨条目引用用 `<skill> P-###` 或 `<skill> diagnose#n`；知识提取来源可用裸 session-id 列表（无 entry，附本地去向说明）
- 出现: <日期> diagnose#<n> [→ absent-this-run <日期> #<n> ...]   ← diagnose#n = 该 skill logs.md 第 n 行（含表头）
```

### 状态机

- `open` → `absorbed-into-skill`：对应修复已进入 skill 本体（SKILL.md / scripts）
- `open`/`absorbed-into-skill` → `closed`：修复落地且连续 2 轮 `absent-this-run`，
  **用户确认后**才能关闭（合并是记账，关闭是判断）
- 条目永不删除——closed/absorbed 条目是 skill-impact.md 台账的锚点

### 合并语义（增量合并，不是追加）

- 新 finding 与已有条目**同根因** → 更新该条目（追加证据、出现记录，必要时融合更优方案）
- 全新根因 → 新条目，ID 递增
- 本轮 trace 未复现的 open 条目 → 出现行追加 `absent-this-run` 标记

## sanitize 规则（公共仓库，写入前强制）

1. 内网域名 / IP → 占位符（`docs/agents/skill-authoring.md`：
   `gitlab.example.com` / `harbor.example.com` / TEST-NET 地址）
2. 内部项目名 → 泛化描述（"一个多 remote 的内部仓库"）
3. 凭证 / token → 只写行为（"凭证内联在 tool-call 参数"），永不写值
4. 证据只存 `session-id#entry` 引用：不贴命令原文、不存绝对路径、不存 raw 摘录
5. commit 前从仓库根跑 gitleaks（`gitleaks dir . --config ~/data/benchmark/config/gitleaks.toml`）

**gitleaks 通过 ≠ 脱敏完成**：gitleaks 只覆盖凭证/密钥类；规则 1-4（域名、项目名、凭证行为、证据格式）是人工 checklist，逐条确认后才能 commit。

## 引用格式

`<session-id>#<entry>`，如 `01a06bcd#718`。session-id 可在本地
`~/.pi/agent/sessions/` 定位原文（raw 层永不入库——它属于 pi 自身管理的 session 日志）。

## 与 raw / skills 层的边界

- **raw**（session jsonl）：pi 自身管理，永不入库，永不拷贝进 wiki
- **skills**（SKILL.md + scripts）：可回滚（git），仓库其余目录
- **wiki**（本目录）：持续累积，永不回滚条目，只追加与更新
