# to-peer — skill-impact 台账

## 2026-09-24 创建 skill（用户指令）
- 提案: 新建 to-peer skill——创建 peer session 一律开**新 herdr tab**（`tab create --cwd` → `agent start`），不用 pane split（用户拍板）；herdr 适配器为 `scripts/herdr-tab-peer.sh`，支持 `--prompt-file/--label/--focus`；通信协议归 multi-agent-collab，本 skill 只管创建
- 落点: 新建 `in-progress/to-peer/`（SKILL.md + scripts/herdr-tab-peer.sh + scripts/check-env.sh + tests/test.sh）；multi-agent-collab SKILL.md bootstrap 小节加一行指路（新 tab 拓扑归 to-peer，pane split 降级为 legacy fallback）
- 验证: tests/test.sh 9/9（含 live smoke：真实建 tab + agent start + 关 tab）；check-env PASS；npx skills add -g 两个 skill 均装成功
- 状态: accepted
- 关联: academy/scripts/spawn-course.sh 的 ponytail 注释（"第二个 tab-spawn 消费者出现时上提"）——本 skill 即该消费者；academy 未改动，后续可考虑改走 to-peer
