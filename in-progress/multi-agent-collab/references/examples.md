# Examples — real transcripts, lightly trimmed

Six transcripts from real collaborations (2026-08 ~ 2026-09), each annotated with the protocol element it demonstrates. Use as calibration for tone and density, not as templates to copy verbatim. Note: these transcripts predate the multi-agent-collab skill and show the old `/skill:herdr` prefix — current first-message prefix is `/skill:multi-agent-collab` (the receiver then pulls the herdr skill for CLI mechanics).

## 1. Dispatch with the full contract (icc leader → cost-fix peer)

A dispatch showing seven of the nine elements: prefix, identity, pre-digested context with file:line, anti-redundancy (implicit in the numbered requirements), verification commands, report schema, and artifact path. The elements this transcript does not show: the anti-hallucination clause and the language directive.

```
/skill:herdr
你在 pane wM:pA，做 inference-cost-controller 部署问题的修复 session。

# 背景
这个 Go 项目（当前分支 dev）通过 Helm chart 部署到 monitor ns，管理
vllm-cost-meter sidecar + OpenCost 定价 ConfigMap。刚完成端到端部署验证，
过程中暴露两处「部署层」的实际问题需要修复。
注意：我（peer session，wM:p1）在跟你协作。请用 herdr 回传结果。

## 待修复（P1）
**helm values.yaml 镜像路径错误** — 现状 values.yaml:4-5:
  repository: <internal-harbor>/aip-mm/inference-cost-controller
但 CI 实际构建镜像在 …deps/inference-cost-controller-0.1.0:dev（common-ci
的 deps/<bin>-<version> 命名）。部署时被迫 --set 覆盖，很脆弱。
**请先确认 CI 实际镜像路径的确切格式**（查 CI 配置/历史），再把 values.yaml
默认值改成「无需 --set 就能正确部署」。

## 待修复（P2）
**ClusterRole 缺 services 权限**。resources.yaml 的 ClusterRole 只有
pods/configmaps/deployments。wayfinder 决策 !16 要求 controller 能创建
sidecar Service + 共享 ServiceMonitor。只修 RBAC 声明，不实现创建逻辑。

## 要求
1. **先读** values.yaml、templates/resources.yaml 确认 chart 结构
2. P1 修镜像默认值；P2 补 services 权限
3. `helm template` + `helm lint` 验证
4. 不要提交/PR —— 只修改工作区文件
5. 把修复结果（改了哪些文件、验证输出）通过 herdr 回复我（wM:p1），
   并 dump 一份 diff 到 /tmp/cost-fix-diff.txt
```

## 2. Research dispatch with anti-hallucination (gw leader → sr-researcher)

Numbered questions bound to a decision; proxy footgun inline; bilingual output directive; reply-by-name.

```
/skill:herdr 调研任务：vllm-semantic-router（官网 https://vllm-sr.ai/docs，
需要走内部代理访问外网）。

背景：我们在为网关写 WASM 特征提取插件（4 种协议、22 个特征字段），
正在决策内部架构：A) 按协议分支提取 vs B) 先归一化为小 IR 再统一提取。

请调研并回答（重点服务于这个架构决策）：
1. 整体架构：如何处理入站请求？有无协议归一化层？
2. 分类/路由判定管线：特征在哪一层提取？
3. 路由决策输出格式
4. 有无值得借鉴的结构模式（多协议/多路由目标场景的扩展性）？
5. 生产实测数据对我们的启示

要求：结论写入文件 /tmp/sr-research.md（英文给 agent 看，关键结论配中文
摘要），并 stdout 简述。完成后通过 /skill:herdr 回复我（w13:p1 的 session）。
```

## 3. Integration receipt + closure (gw leader → sr-researcher)

Every outcome located; explicit closure; standing-down clause. Sent after the leader consumed the peer's research.

```
/skill:herdr 收到，调研结论已完整整合：(1) #01 架构决议已采用你的 B+4 点
补充建议并 resolve；(2) 避坑 #3/#8/#9 已落到 map Notes 和 #03/#12 ticket；
(3) 完整报告已归档 .scratch/feat-extract-protocol-compat/research-vllm-sr.md；
(4) 管线五层/learning 三段式等前瞻概念保留在报告中供后续 effort 使用。
任务完成，感谢。你可以继续待命或结束，无后续问题。
```

## 4. Termination with recall clause (icc leader → cr-learner)

Decision converged elsewhere; peer explicitly released with a recall path; reply requested for the record.

```
/skill:herdr 决策已收敛（grilling 5 轮）：Q1=A 维持 controller 管 sidecar；
Q2=C Create 后不 Update Service/SM；Q3=A opencost 单端口删 9005；Q4=B
stale cleanup defer !19；Q5=A 泛型骨架 defer !19。你无需执行 icc 修复，
peer wM:p1 已切写模式自行落地。感谢你的 insight，任务完成。请通过 herdr
回复确认。
```

## 5. Peer-to-peer data exchange (netmon ↔ gw, equals)

Peers introduce themselves with both name and pane, share raw measurements before asking, and enumerate questions with decision stakes attached.

```
/skill:herdr 你好，我是同一 workspace 下的 peer session「netmon 开发/L2 年龄
画像」(pane w13:p6, cwd ~/projects/netmon，herdr 中找我用 pane w13:p6)。
用户让我和你交流 Evicted-Miss 指标——93 集群上的实际值关系到 L2/L3 研究
是否继续。

我先分享我刚从 93 Prom 拉的实测数据：
【evicted_miss 实测】…（数据略：54 次/287K tokens/浪费占比 ≈1.06%）
【我的 L2 审计背景】…（L2 常年 99% 满、belt 27.7h）

三个问题想听你的判断：
1.【量级解读】~1% 浪费率足以支撑扩容研究吗？
2.【盲区验证】指标全零时如何区分「真零」和「盲区」？
3.【与 L2 满载的关系】ghost index 是否跨全部 tier？

请通过 herdr 回复我（pane w13:p6），把你的判断写给我；如果需要我补充
审计数据细节也直接说。谢谢！
```

## 6. Background-first waiting (the pattern, not a message)

Real shape of the preferred waiting strategy — the send becomes a background task, the turn ends, the notification wakes the session:

```bash
# via bg_run — command returns immediately to the turn:
herdr agent prompt <peer> "$(cat /tmp/dispatch.md)" --wait --timeout 1800000
# ...end the turn; do other work; resume on <background-task-notification>
```
