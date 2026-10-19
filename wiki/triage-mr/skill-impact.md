# skill-impact — triage-mr

提案台账。被拒提案必须保留并写明拒绝理由——后续提案撞形状时先翻此表。

| 提案 | 落点 | commit | 验证命令与结果 |
|------|------|--------|----------------|
| S1 ocr-verify-resolved.py：GitLab 判定从 notes[0] 改为线程内全部 resolvable note resolved，输出标注 [N/M notes open]（GitHub 侧本为线程级，未动） | mr-review-triage/scripts | 2a46367 | mock 4 例 ✓（head已resolve+reply open→报open；全resolve→closed；单note open 无后缀；非resolvable→跳过）；真实 MR 回归：与旧版在真实 open 线程上判定一致 |
| S2 fix skill"suggested fix is a second, independent claim"段搬回源仓并重装（peer session 只改了安装版） | fix skill | 2a46367 | diff 源仓=安装版 ✓ |
| D1 SKILL.md 正面表述五处：增量写 classified.json（第一条 verdict 即建文件）；script-first 排序+手动 fallback 两类限定；gate-observation 矛盾裁决规则；done 条件与 stale 警告去重；Reflect 降级并入 Wrap-up | triage-mr SKILL.md | 0ec0950 | 待下轮 diagnose 验证（对应 P-001/P-002/P-003） |
| S3 ocr-post-labels.py：线程 resolve 成功后 `_sweep_notes_gitlab` 扫尾剩余 resolvable note；失败降级 WARN（head 已 resolve，gate 兜底） | mr-review-triage/scripts | 0ec0950 | mock ✓：POST 回帖→PUT resolve→GET→扫 stale reply note；验证时序含新回帖 note |
| R1 拒绝：triage-mr frontmatter description 改一行摘要（user-invoked 规范建议） | frontmatter | — | 拒绝理由：流程式描述对人类记忆该 skill 的编排角色有正收益，且 user-invoked 下零 context load，无违规成本 |
| R2 拒绝：post-labels.py 补"独立处理 note 扫尾"子命令（与 S3 二选一） | mr-review-triage/scripts | — | 拒绝理由：S3 顺路扫尾更小 diff，独立子命令引入第二入口徒增维护面 |
| F1 SKILL.md 写明 scripts/reference 路径解析规则（相对本 SKILL.md 目录）；gitlab.md 增平台 resolve quirk 条目（discussion PUT 500 / notes POST 404 / note 级 PUT 配方）；ocr-post-labels.py `_sweep_notes_gitlab` 返回成功并兼作 discussion-PUT 失败时的 fallback resolve | mr-review-triage + triage-mr | bf6282b | mock ✓（500 场景 fallback 判 False、note PUT 成功场景判 True 且请求路径正确）；真实实例回归待下轮 triage 验证（对应 P-005/P-006） |
| S4 post-labels 加 `--classified <path>` 文件直读写模式，物理消灭 heredoc 双写（并入 spec #57 T1） | mr-review-triage/scripts + fix skill 文档 | 549c95b | pytest 全绿（CLI 层 hard-fail 分支 + `verdict --class Q` → post 消化端到端）；对应 P-002 refuted 复发（01a12f97#709/#805/#843/#909/#835） |
| S5 pull 脚本加 `--digest --against classified.json`（并入 spec #57 T3）；落地形态：输出仅新 findings（保留全量序号），人读摘要零 ID 形态（提案中 id8 形态被 P-008 家族结论否弃） | mr-review-triage/scripts | ad19321 | pytest（digest 只出新 findings、序号稳定、零截断形态、坏 against 文件 hard-fail）；对应 P-007（01a12f97#444,#470,#679,#819,#833,#931，6 次/3 形状） |
| T2 spec #57：verdict.py——classified.json 裁决语义字段唯一写入者（字节级复制 discussion_id + anchor 计算 + 原子读改写，per-item resolved 在 verdict 时刻记录，--force 才可覆盖，exit 0/1/2） | mr-review-triage/scripts/verdict.py | 9830bda | pytest（未知序号、缺 pull 文件、force 语义、回显 no+作者+首行全覆盖） |
| T4 spec #57：post 执行语义硬化——join+anchor 校验任何平台调用前 hard-fail、内容判重幂等（anchor 标记，覆盖手动旁路）、reply 失败禁止 resolve | mr-review-triage/scripts | 4f250ef | pytest 20 新例（截断/伪造 id、错锚点、posted 跳过、reply 失败阻断 resolve） |
| T5 spec #57：post 吸收 OCR summary 线程——🔍 start/✅ end·LGTM/⚠️ error 三模板（error 只回帖永不 resolve，gate 永红为有意 human-in-loop 设计）+ GitHub REST/GraphQL 双 ID 空间修复 | mr-review-triage/scripts | 89b7898 | pytest summary sweep 套件（error 轮 exit 非零、空轮统计、判重不重贴） |
| T6 spec #57：OCR_REMOTE 远端名收敛 + 启动认证探针（project path 比对，错误实例响亮失败）+ 0-findings stderr hint | mr-review-triage/scripts | 0908dab + e4631d3 | pytest remote probe 套件（OCR_REMOTE 生效、显式 origin 解析失败路径、探针跳过语义） |
| T7 spec #57：verify 展示去截断（序号/内容锚标注 + [N/M notes open] 保留）+ pipeline 完成检查进脚本（in-flight exit 2，--skip-pipeline-check 逃生门） | mr-review-triage/scripts | de91927 | pytest verify 套件（无 ID 形态断言、gate exit 2 语义） |
| Amendment Round 2 裁决记录：修订 A（Edge triage 默认 resolved:true 写 per-item、Q 仅显式才关、决策钉在 verdict 时刻）随 #59；修订 B（pipeline 门进脚本）随 #64；修订 C（Q alias 与 --classified 随 #58、--digest 命名随 #60）；端点真值定谳（discussion PUT 500 实为 id 截断，resolve-endpoint workstream 撤销，note 级 fallback 保留防御层） | spec #57 | 见上行 | MR !688 复现实验 |
| T8 spec #57：triage-mr SKILL.md 全流程重写——手动 fallback 段全删（脚本出错=修脚本或上报，无手写 API 路径）、verdict 循环 + 逐条即时落盘（P-002）、per-item resolved 语义、error-gate 永红设计写明、--digest 对账步骤（digest 检测 + 全量刷新）、OCR_REMOTE/OCR_PLATFORM + glab host 边界；reference gitlab/github/templates 调用点同步（--classified 形态、删死模板）；fix SKILL.md/CLASSIFICATION.md 双模契约一致性核对；reference 中内部实例昵称等 sanitize 命中标识清理（gitlab.md×5 + 脚本注释×1） | triage-mr SKILL.md + mr-review-triage reference + fix skill + README 行 | b73c8d8 | pytest 147 绿（mr-review-triage 全套件，#58-#64+ocr r1 后终态）；sanitize-check 本票涉及文件清零 |
| 2026-10-15 | ocr r1 F6：SKILL.md Step 1 注明 scripted verdict 流程下 pull 输出必须落在 `.triage/<MR>/issues.json`（verdict.py 读取的路径），/tmp 仅为旧流程 | SKILL.md Step 1 | 155e956 | pytest 全绿（docs-only，模板 JSON 块 python 校验通过）；完整 SKILL.md 重写在 #65 |
| R3 create-mr 触发率审计落地：triage-mr 收尾需建 MR 时一律转 /skill:create-mr（remote/target/draft 确认流程），禁裸 glab mr create / gh pr create——审计数据：2026-10-19 全库 96 session 裸建 MR 未触发 skill，其中 2 例失约点在 triage-mr 会话内 | triage-mr SKILL.md（Wrap up 节） | 4c59ea6 | 审计数据即验证（触发率 0 → 条款入文） |
