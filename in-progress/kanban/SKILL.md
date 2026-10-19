---
name: kanban
description: >-
  Wayfinder/execution effort 流水线看板：在 herdr-board 之上定义项目无关的四板拓扑
  （agent/dev × wayfinder/execution）、列配方、skill 注入、派发契约与失败规范。
  当用户要求建 effort 看板、派发 wayfinder/spec/implement 流水线卡、迁移或排查
  board 卡流转失败、或提到 kanban / 流水线板 / effort board 时使用。
  底层 CLI 操作规范见 herdr-board skill（本 skill 不重复，只管拓扑与配方）。
---

# Kanban — effort 流水线看板

在 herdr-board 之上的一层配方。**board 是执行视图，真相在 issue-tracker 和仓库**——
ticket 依赖图、spec、map 正典都在 GitLab/GitHub issue 与仓库文档里，board 卡只携带指针。

## 拓扑（单板池，project 无关）

一个专用 project（bootstrap 脚本建在 `<BOARDS_DIR>`，默认 `~/boards`）承载全部 effort，
**不在各代码仓内建板**。四块板按 runtime × 相位划分：

```
<BOARDS_DIR> project
├── agent-wayfinder：  Backlog → Wayfinder(auto) → Grilling(auto) → Spec(auto) → Ready(manual) → Blocked
├── agent-execution：  Implement(auto) → E2E Tests(auto) → Code Review(auto) → MR & Human Review(auto) → Retro(auto) → Done → Blocked
├── dev-wayfinder / dev-execution：列配方同上
```

- **给 effort 选 runtime**（agent/dev）后，卡就在该 runtime 的一对板里流转
- **一 effort 一卡起步**（map/grilling 阶段同卡前进），grilling 需并行多票时拆子卡、依赖写描述
- 仓 = 卡描述里的指针 + 卡的 space-cwd，不再是 project

## 列配方

| 列 | trigger | prompt 注入的流程 | on-success | on-fail |
|---|---|---|---|---|
| Backlog | manual | — | | |
| Wayfinder | auto, fresh | /skill:wayfinder → map 落仓，路径写 comment | Grilling | Blocked |
| Grilling | auto, fresh | /skill:grilling（pane 内多轮问用户），结论写 comment | Spec | Blocked |
| Spec | auto, fresh | /skill:to-spec → /skill:review-spec → /skill:to-tickets 串行 | Ready | Blocked |
| Ready | manual | —（跨板门，见流转规则） | | |
| Implement | auto, fresh | /skill:implement-spec-in-pipeline implementer | E2E Tests | Blocked |
| E2E Tests | auto, fresh | 本地构建（仓内 Dockerfile/Dockerfile.local + nerdctl + `<PROXY_URL>`）→ /skill:argocd-ops 部署 `<部署集群>` 验证 | Code Review | Blocked |
| Code Review | auto, fresh | ocr 评审；low 丢弃，critical/high/medium = fail | MR & Human Review | Blocked |
| MR & Human Review | auto, fresh | /skill:create-mr 建 draft MR，卡停 awaiting 等人 | （人拖 Retro） | Blocked |
| Retro | auto, fresh | /skill:retro 复盘，沉淀进 skill/wiki | Done | Blocked |
| Done / Blocked | manual | — | | |

所有 prompt 尾部带纪律：**先 `board comment` 再 `board done`；ok=目标达成、fail=未达成（自动入 Blocked）；禁止自行 move/cancel/retry 自己的卡。**

## 流转规则

1. **auto 链全自动**：run 完成 → `board done --outcome ok|fail` → daemon 按 on-success/on-fail 流转
2. **跨板门（Ready）**：board CLI 不支持跨板 on-success（实测拒绝 `board/column` 语法）。
   Spec 完成 → 卡停 Ready → 人或主 session `board card move <id> Implement --destination-board <execution板id>` 搬运（入 auto 列即派发）
3. **Code Review 不回 Implement**：评审发现问题 → fail 入 Blocked → 人确认修复方案 → 人手动拖回 Code Review 复审（人控循环，无死循环）
4. **MR 合并后人拖 Retro**，retro run 完成自动进 Done

## 建卡契约（派发三要素 + 指针）

```bash
board --project <BOARDS_DIR> board select <wayfinder板id>
board card create --title "<phase>：<一句话>" --column Backlog \
  --session <runtime> --space-kind new-workspace --space-cwd <目标仓绝对路径> \
  -d "输入指针：issue/spec/map 链接 + blocked-by + 完成判据"
```

- **session** = agent|dev（runtime）；**space 一律 new-workspace + space-cwd=目标仓**（勿复用多人 workspace，见 F8）
- 卡描述**只写输入指针**，不写流程 prompt（prompt 在列上）
- execution 板的卡从 Ready 搬入，指针在 wayfinder 阶段的 comment 里接力

## 失败规范（动手前对照，出现即按此处置）

- **F1 JSON 误判**：create 返回顶层就是卡字段（无包裹），按"失败"重试会重复建卡。验证一律 `board card list` 回读。
- **F2 选择态全局漂移**：不带 `--project` 的命令落到别的 session 切过的板。所有命令显式 `--project`。
- **F3 派发三要素**：session + space（ref/cwd）+ card 缺一 → run failed。修复：`card edit` 补齐后 `card run retry`。
- **F4 run 生命周期**：run open 时 `card edit` 被拒（先 cancel）；run done 后 run-scoped comment/done 被拒（"no longer open"）。汇报走 comment + issue 双路。
- **F5 完成检测**：真完成看 **run outcome**，不看 herdr agent_status（working 可能已 idle）。
- **F6 `--board` 标志静默失效**：子命令上 `--board <id>` 可能不改变目标，列/卡落到当前选中板。**建列/改列一律先 `board select <id>` 再操作，操作后 `board show <id>` 核对 board_id**（本拓扑创建时实证踩坑）。
- **F7 space_ref 过期**：卡引用已删 workspace → run failed，错误里列 known workspaces。修复：`card edit --space-kind new-workspace --space-cwd <repo>`。
- **F8 多 pane 歧义**：workspace 挂多个活跃 pane 时 dispatch 无法选 cwd → 失败。effort 卡一律专属 new-workspace。
- **F9 跨板 on-success 不支持**：CLI 拒绝 `board/column` 跨板语法。用 Ready 门 + `card move --destination-board`。
- **F10 勿用 `template apply pipeline`**：其 Review 列自带 model_override（不可达路由 → 假 failed 死壳）。本配方手建列，无此问题。

## Bootstrap（新节点重建拓扑）

```bash
bash <SKILL_DIR>/scripts/bootstrap-boards.sh   # 幂等；读同目录 runtime.conf（见 .example）
```

建 project（`<BOARDS_DIR>`）→ 四板 → 列 + trigger/链/prompt。prompt 中的环境值
（代理、部署集群）来自 `runtime.conf`，不入库。项目要微调列集合或 prompt 时，
bootstrap 后直接 `board select <板>` + `column edit/create/delete`——不做配置文件机制。

## 迁移旧板

旧仓内板的活跃卡：`card move <id> Backlog --destination-board <新板>` →
`card edit --session <runtime> --space-kind new-workspace --space-cwd <repo>` →
旧板 `board archive`。done 卡不迁（历史留在旧板）。
