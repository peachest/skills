# skill-impact

| 日期 | 提案 | 落点 | commit | 验证 |
|---|---|---|---|---|
| 2026-10-09 | 新增 doc-usage 模式（matrix/echo 子命令）：peer session 01a11aa5 的三轮文档消费扫描经验回灌。吸收：bash cat/grep 比 read 工具多 ~40 倍须合并统计；READ/WRITE/MENTION 三分类；嵌套 session（forks/、run-0/）递归发现；python one-liner 改文件 = WRITE-like；escape-rate 逆检验；read 调用只是弱证据，echo（assistant 文本回显 doc 特征 token，锚定首个 read-like 事件、排除 write-only 自回显）为强证据 | scripts/doc-usage.py、tests/test_doc_usage.py（7+4 用例）、SKILL.md doc-usage 章节 + evidence ladder | (本次) | uv run pytest 21 passed；真实数据复扫 speculative-training 127 个 session，matrix/escape/echo 输出与 peer 手工三轮结论一致 |
