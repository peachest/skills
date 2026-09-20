# patterns — okb skill 已知问题

每次 diagnose 增量合并。条目格式见 `../README.md`。状态机: open → (fix landed + 2 连续 absent) → closed。

## P-001 curation 工件全靠手工装配，无脚本支撑
- 状态: open
- 现象: bronze 快照（arXiv curl+sha256）同型脚本单 trace 写 4 遍；三层 frontmatter 对照旧课模板手写；index.md 分布表手数文件；链接可达性 python 手写——深度 bug（`../../`）跨 namespace 复发
- 根因: skill 只定义了契约（frontmatter 字段、完成准则），零脚本——每一步机械操作都留给 agent 即兴
- 方案: 沉淀脚本组 `scripts/okb-snapshot`（source→bronze 正文+frontmatter）、`okb-new --layer --topic`（骨架笔记）、`okb-index-regen`（扫三层生成 index.md + --check-links）
- passCheck: 跑一轮 curation 后 grep 工具调用，无同型 heredoc 快照/frontmatter 装配脚本出现（脚本被调用替代）
- 证据: 01a062a0#219 #221 #223 #225 #231 #234 #237 #253 #255 #359 #361
- 出现: 2026-09-20 diagnose#1（01a062a0）

## P-002 distill/factcheck 合并成一趟，draft→stable 提升链被跳过
- 状态: open
- 现象: silver 与 gold 同批写入、silver 直写 `status: stable` + `verified` 预填；gold 用了契约未定义的 `type: verification` 自造结构
- 根因: 契约描述了两个步骤各自的完成准则，但未写成不可绕过的 gate（无脚本强制 frontmatter 状态）；两步连续执行时 agent 把中间态优化掉了
- 方案: skill-doc——契约加一句硬规则"silver 的 `status`/`verified` 只能由 factcheck 步骤写入"；或 P-001 的 okb-new 脚本只产出 `status: draft`，stable 由 factcheck 脚本提升
- passCheck: trace 中 distill 写入的 silver frontmatter `status: draft`，stable 提升仅出现在 factcheck 条目之后
- 证据: 01a062a0#234
- 出现: 2026-09-20 diagnose#1（01a062a0）

## P-003 bronze 快照保真度不足导致 factcheck 证据链断在半路
- 状态: open
- 现象: bronze 只存 arXiv 摘要（核心数学断言在正文），gold verified 事件的 evidence 指向课内文档/代数推导而非 origin——验证链没走完 bronze→origin
- 根因: 契约要求 verbatim 快照但未定义"保真度下限"（摘要 vs 全文）；agent 拿到什么存什么
- 方案: skill-doc——ingest 准则加一条：bronze 须覆盖被 distill 提炼的断言所在段落；摘要不足以支撑后续 factcheck 时先取全文
- passCheck: factcheck 的每条 verified 事件 evidence 可沿 sources[].resource 走到包含该断言的 bronze 内容
- 证据: 01a062a0#231 #234
- 出现: 2026-09-20 diagnose#1（01a062a0）

## P-004 ingests_since_status 计数器从未建立，Status 触发门永久失效
- 状态: open
- 现象: ingest 完成后 index.md 无计数器字段（agent 手写整体重写 index 也没建）
- 根因: 与 P-001 同源（index.md 靠手写）+ 当时契约对 index.md 格式无 spec（已在 fced0c0 补上 schema）
- 方案: P-001 的 okb-index-regen 自动维护计数器；契约侧已修（fced0c0 定义了 index.md schema），待脚本落地
- passCheck: ingest 后 index.md 含 `ingests_since_status` 且值递增
- 证据: 01a062a0#237
- 出现: 2026-09-20 diagnose#1（01a062a0）
