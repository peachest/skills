# skill-impact

| 日期 | 提案 | 落点 | commit | 验证 |
|---|---|---|---|---|
| 2026-10-09 | 新增 doc-usage 模式（matrix/echo 子命令）：peer session 01a11aa5 的三轮文档消费扫描经验回灌。吸收：bash cat/grep 比 read 工具多 ~40 倍须合并统计；READ/WRITE/MENTION 三分类；嵌套 session（forks/、run-0/）递归发现；python one-liner 改文件 = WRITE-like；escape-rate 逆检验；read 调用只是弱证据，echo（assistant 文本回显 doc 特征 token，锚定首个 read-like 事件、排除 write-only 自回显）为强证据 | scripts/doc-usage.py、tests/test_doc_usage.py（7+4 用例）、SKILL.md doc-usage 章节 + evidence ladder | c29a100 | uv run pytest 21 passed；真实数据复扫 <project-a> 127 个 session，matrix/escape/echo 输出与 peer 手工三轮结论一致 |
| 2026-10-09 | 拆分：doc-usage 模式迁出为独立 skill `doc-consumption`（职责不同：文档消费判定 vs 工具调用检索）；本 skill 回退为纯检索 + SKILL.md 留指针，description 指路 doc-consumption | scripts/doc-usage.py、tests/test_doc_usage.py → in-progress/doc-consumption/ | 715d4fb | 两 skill pytest 分别 7/14 passed |
| 2026-10-16 | Relay enrichment（可选）：dump 模式后新增 relay-enrich.py 调用指引，为每 tool call 附 duration_s/attempt_index/status（ATIF 源，no-relay-data 非阻塞） | SKILL.md step 3b（relay-enrich 指引）+ references | 121584c | 全量测试通过 |
| 2026-10-20 | 新增 step 5 交接规则：dump 含错误时默认直接接续 tool-call-diagnose（不再询问）；零错误纯取数才收尾留一行指针。证据：27 次 extract 仅 4 次进入 diagnose（15%），错误型 dump 常被弃置 | (hash lost in 10-26 filter-repo) | feat(tool-call): diagnose axis 4 (contract & competition) + extract default-on diagnose handoff | |

| 2026-10-22 退役：与兄弟 extract skill 合并为 in-progress/session-mining（路由表统一入口，脚本/测试整体迁移，消费者已重指向）。理由与证据见 wiki/session-mining/skill-impact.md | — | 0f739d5 | 46 tests green | |
