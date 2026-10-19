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
**不在各代码仓内建板**。每 runtime 一块 11 列单板（全流程同板流转，TUI 可拖全程）：

```
<BOARDS_DIR> project
├── agent：Backlog → Wayfinder(auto) → Grilling(auto) → Spec(auto) → Implement(auto) → E2E Tests(auto)
│         → Code Review(auto) → MR & Human Review(auto) → Retro(auto) → Done(manual) → Blocked(manual)
└── dev：列配方同上
```

- **给 effort 选 runtime**（agent/dev）后，卡就在该 runtime 的板里流转
- **一 effort 一卡起步**（map/grilling 阶段同卡前进），grilling 需并行多票时拆子卡、依赖写描述
- 仓 = 卡描述里的指针 + 卡的 space-cwd，不再是 project
- 历史教训（2026-10-19 拍板合并）：曾拆 wayfinder/execution 双板，但 TUI 拖动不跨板 +
  跨板 on-success 不支持（F9），Ready 门增加人工搬运成本 → 合并单板

## 列配方

| 列 | trigger | prompt 注入的流程 | on-success | on-fail |
|---|---|---|---|---|
| Backlog | manual | — | | |
| Wayfinder | auto, fresh | /skill:wayfinder → map 落仓，路径写 comment | Grilling | Blocked |
| Grilling | auto, fresh | /skill:grilling（pane 内多轮问用户），结论写 comment | Spec | Blocked |
| Spec | auto, fresh | /skill:to-spec → /skill:review-spec → /skill:to-tickets 串行 | Implement | Blocked |
| Implement | auto, fresh | /skill:implement-spec-in-pipeline implementer | E2E Tests | Blocked |
| E2E Tests | auto, fresh | 本地构建（仓内 Dockerfile/Dockerfile.local + nerdctl + `<PROXY_URL>`）→ /skill:argocd-ops 部署 `<部署集群>` 验证 | Code Review | Blocked |
| Code Review | auto, fresh | ocr 评审；low 丢弃，critical/high/medium = fail | MR & Human Review | Blocked |
| MR & Human Review | auto, fresh | /skill:create-mr 建 draft MR，卡停 awaiting 等人 | （人拖 Retro） | Blocked |
| Retro | auto, fresh | /skill:retro 复盘，沉淀进 skill/wiki | Done | Blocked |
| Done / Blocked | manual | — | | |

所有 prompt 尾部带纪律：**先 `board comment` 再 `board done`；ok=目标达成、fail=未达成（自动入 Blocked）；禁止自行 move/cancel/retry 自己的卡。**

## 流转规则

1. **auto 链全自动**：run 完成 → `board done --outcome ok|fail` → daemon 按 on-success/on-fail 流转
2. **Code Review 不回 Implement**：评审发现问题 → fail 入 Blocked → 人确认修复方案 → 人手动拖回 Code Review 复审（人控循环，无死循环）
3. **MR 合并后人拖 Retro**，retro run 完成自动进 Done
4. **跳相位**：spec 已就绪的 effort 卡直接从 Backlog 拖进 Implement；wayfinder/grilling 完成后的卡停在原列，由人判断去向

## 建卡契约（派发三要素 + 指针）

```bash
RT=$(basename "$(dirname "$HERDR_SOCKET_PATH")")   # 自探测 runtime（非 herdr 内则显式传参或问用户）
board --project <BOARDS_DIR> board select <runtime> 板 id
board card create --title "<phase>：<一句话>" --column Backlog \
  --session "$RT" --space-kind new-workspace --space-cwd <目标仓绝对路径> \
  -d "输入指针：issue/spec/map 链接 + blocked-by + 完成判据"
```

- **session** = agent|dev（runtime），**按仓库归属**：skills/pi-mypackage/research 等个人工具仓 → agent；HAMi/HAMi-WebUI/kube-nodexpu-manager 等 llmops 业务仓 → dev（用户 2026-10-19 拍板，新仓拿不准就问）
- **自探测 runtime**（在 herdr session 内建卡时先做）：`basename "$(dirname "$HERDR_SOCKET_PATH")"`（socket 路径 `~/.config/herdr/sessions/<runtime>/herdr.sock` 即含 runtime 名）；结果与仓库归属规则交叉核对，不一致或取不到 → 问用户，不要静默猜
- **space 一律 new-workspace + space-cwd=目标仓 + space-ref=auto**（勿复用多人 workspace 见 F8；勿留旧 ref 见 F7）
- 卡描述**只写输入指针**，不写流程 prompt（prompt 在列上）
- **跳相位**：spec 已就绪的卡直接从 Backlog 拖进 Implement，输入指针写在卡描述

## 失败规范（动手前对照，出现即按此处置）

- **F1 JSON 误判**：create 返回顶层就是卡字段（无包裹），按"失败"重试会重复建卡。验证一律 `board card list` 回读。
- **F2 选择态全局漂移**：不带 `--project` 的命令落到别的 session 切过的板。所有命令显式 `--project`。
- **F3 派发三要素**：session + space（ref/cwd）+ card 缺一 → run failed。修复：`card edit` 补齐后 `card run retry`。
- **F4 run 生命周期**：run open 时 `card edit` 被拒（先 cancel）；run done 后 run-scoped comment/done 被拒（"no longer open"）。汇报走 comment + issue 双路。
- **F5 完成检测**：真完成看 **run outcome**，不看 herdr agent_status（working 可能已 idle）。
- **F6 `--board` 标志系统性不可信**：任何带 `--board` 的子命令（含 `card list`/`card show` 等只读查询）都可能静默落到别的板，结果看起来正常但数据是别板的（2026-10-19 xpu 迁移两次实锤）。**铁律：一律 `board select <id>` 后裸查/裸操作，查完用返回体的 board_id 字段回验**。
- **F7 space_ref 过期**：卡引用已删 workspace → run failed，错误里列 known workspaces。修复：`card edit --space-kind new-workspace --space-cwd <repo>`。
- **F8 多 pane 歧义**：workspace 挂多个活跃 pane 时 dispatch 无法选 cwd → 失败。effort 卡一律专属 new-workspace。
- **F9 跨板操作双堵（TUI+CLI）**：TUI 拖动不跨板；跨板 on-success 语法 CLI 拒绝；`--destination-board` 用板名报 io error，**用板 id**。跨板搬运唯一路径 = `card move <id> <列> --destination-board <板id>`——这也是 2026-10-19 拍板合并单板的根因。
- **F10 勿用 `template apply pipeline`**：其 Review 列自带 model_override（不可达路由 → 假 failed 死壳）。本配方手建列，无此问题。
- **F11 `column edit` 不支持 `--position`**：列重排用 `board column reorder <COL> <pos>`。
- **F12 有卡列删不掉 / 有 open run 板归档不了**：`column delete` 报 has cards（先安置卡或 `--move-cards-to`）；`board archive` 报 open run（先 cancel）。迁移 awaiting 卡时 cancel 会让状态变 failed——comment 注记真实语义防误读（agent 读注记后行为正确：卡 14 run 只做 CI 巡检未重复建 MR）。
- **F13 归档板吞卡**：bootstrap 重建会建**新板 id**（旧 id 作废）；归档前不清卡则卡困死在归档板上——归档板不出现在 `board list --all`，但卡 id 仍可 `card show` 寻址；直接 move 报 `archived board must be restored first`。救援路径：`board board restore <id>` → 逐卡 move → 重新 archive。**归档/重建前必须先 `card list` 清点并安置全部卡**。

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
