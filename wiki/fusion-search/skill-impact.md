# fusion-search — Skill Impact

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-27 | 新建 skill:两路检索融合(anysearch + DeepSeek Search → 去重 → RRF → judge 重排 → top-k),封装 ~/research/deepseek-search-fetch/02-fusion-experiment.md 的验证流水线 | dbe67f7 | 单测 6/6;e2e 单查 exit 0(融合 3.0 vs 单路 2.6/1.2)+ 降级 exit 2(degraded:true)+ batch 双查 both 共识标记;check-env GREEN |

## 已知问题 / 设计取舍

- judge 端点走 gitignored runtime.conf,内部网关 IP 不入库;example 用占位符,新节点需手动填(否则脚本 exit 3 并指向 example)
- 兄弟 skill 依赖:anysearch CLI 固定用系统 python(/usr/bin/python3)执行——`uv run` 会把自身 venv 插 PATH 前端,裸 python3 解析到无 requests 的 venv python(实证坑,已用 ANYSEARCH_PYTHON 配置化)
- 凭证注入按命令文本触发:SKILL.md quick start 的 `DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY` 前缀是该机制的显式触发形态
