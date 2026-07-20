# 模板参考

## 本地报告模板

生成 `mr-review-plan-<MR_ID>.md`：

```markdown
# MR !<ID> Review 分类与修复计划

源分支: <branch>
目标分支: <target>
OCR pipeline: <pipeline URL>

## 汇总

| 分类 | 数量 | 优先级分布 |
| ---- | ---- | ---- |
| ✅ 真阳性 | N | 🚨 x / ⚠️ x / 🟢 x |
| ❌ 假阳性 | N | - |
| 🟡 边缘 | N | - |
| 🔵 非本 MR 范围 | N | - |
| ⏸️ 需讨论 | N | - |

## 详情

### ✅ 真阳性（待修复）

#### #1 <问题简述>

- **文件**: `path/file.go:123`
- **分类**: ✅ 🚨
- **修复方案**: <具体方案>
- **风险**: <影响的调用方>
- **状态**: ⏳ 待确认

### ❌ 假阳性

#### #1 <问题简述>
- **文件**: `path/file.go:456`
- **分类**: ❌ FP
- **原因**: <为什么不是问题>
- **ADR**: docs/adr/0003-xxx.md（如有）

### 🟡 边缘

#### #1 <问题简述>
- **文件**: `path/file.go:789`
- **原因**: vendor 文件

### 🔵 非本 MR 范围

#### #1 <问题简述>
- **文件**: `path/file.go:101`
- **说明**: 属于预存代码，非本 MR 的变更

### ⏸️ 需讨论

#### #1 <问题简述>
- **文件**: `path/file.go:202`
- **不确定点**: 修复方案可能影响 XXX
```

## 检查点 Brief 模板

```markdown
### Review 分类摘要

| 分类 | 数量 | 优先级 |
| ---- | ---- | ---- |
| ✅ 真阳性 | N | 🚨 x / ⚠️ x / 🟢 x |
| ❌ 假阳性 | N | - |
| 🟡 边缘 | N | - |
| 🔵 非本 MR 范围 | N | - |
| ⏸️ 需讨论 | N | - |

### ✅ 真阳性（按优先级排列）

#### 🚨 #1 Makefile:29 — `lint` target 不存在
   - 当前状态: `all: fmt vet lint test build` 引用未定义的 `lint`
   - 方案: 从 `all` 依赖中删除 `lint`
   - 风险: 无

#### ⚠️ #2 server.go:46 — Stop() Shutdown NULL ptr
   ...
```

P0（🚨）排最前，⚠️ 中，🟢 低。

## 贴回 MR 标签格式

### 阶段一（不变分类）

```markdown
### ❌ 假阳性

**原因**: 设计意图 (`GOSUMDB=off`)
**ADR**: docs/adr/0002-offline-build.md
```

```markdown
### 🔵 非本 MR 范围

**原因**: 属于预存代码 pre-existing
```

```markdown
### ⏸️ 需讨论

不确定是否保留 `CGO_ENABLED=1` 的默认值，需团队确认
```

### 阶段二（最终状态）

| 最终状态 | 格式 |
| ---- | ---- |
| ✅ 已修复 | `### ✅ 已修复 — changes pending in working tree` |
| ⚠️ 跳过 (FIXME) | `### ⚠️ 跳过 — FIXME 注释已添加\n\n**说明**: <原因>` |
| 📝 跳过 (NOTE) | `### 📝 设计决策 — NOTE 注释已添加\n\n**说明**: <原因>` |
| 🔄 重分类 | `### 🔄 重分类：<新分类>\n\n**原因**: <说明>` |
| ❌ 修复失败 | `### ❌ 修复失败 — 需人工处理\n\n**原因**: <说明>` |

## 脚本输入格式

`ocr-post-labels.py` 输入 JSON：

```json
[
  {
    "discussion_id": "def...",
    "classification": "FP",
    "reason": "设计意图 (`GOSUMDB=off`)",
    "adr": "docs/adr/0002-offline-build.md"
  }
]
```
