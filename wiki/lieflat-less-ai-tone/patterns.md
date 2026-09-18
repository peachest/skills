# lieflat-less-ai-tone — patterns

## P-001 逐规则命中无机器核验，标点规则机械全覆盖、内容规则空转
- 状态: open
- 现象: 一次多 worker 批量去AI味改写中，约 44 处改动里破折号（R4）33 处占 75%，加冒号（R5）≈77% 为标点类；内容规则（R1/R2/R10）仅 5 处，R3/R8 零命中且系 worker 自报未经验证。不同 worker 对同类"术语——释义"破折号裁定相反（一个全改自称零保留，另两个保留功能性用法 4/7 处），违反"没有把握时保持原文"；一个 worker 直接回吐原文（diff=0），靠编排器人肉 diff 才发现；SKILL.md 22 项验收清单无人执行（限定词抹除、语气强度加重两项零检查）。编排器自认"约 80% 修改是揭晓式破折号"。
- 根因: contract gap——SKILL.md 验收全为 prose 清单，无逐规则命中的机器核验，也无 worker 回执格式要求；标点规则（R4/R5）触发标记最易机检，模型自然向其坍缩。
- 方案: ①新增 `scripts/audit-hits.py`：输入改写前后两份 md，输出逐规则命中行清单 + "改动但未命中任何规则"的句级 diff（正则复用 check-translationese.py 已有 BASELINE 定义）；②SKILL.md 增补：worker 回执必须含逐规则命中计数与"保留例"清单，标点规则须逐处裁定、禁止全文无差别替换。
- passCheck: 对任意一次改写的 orig/new 跑 `audit-hits.py`，输出的改动-规则映射中标点类（R4/R5）占比 <50%，且"改动未命中规则"项为 0；worker 回执含逐规则计数。
- 证据: 01a0a415-7d22#78,#80,#82,#88
- 出现: 2026-09-18 diagnose#1

## P-002 信息守恒校验跨会话手搓三套口径
- 状态: open
- 现象: 同一验收意图（硬边界"信息守恒"）在三处手工实现且指标互不相同：逐文件 diff 对原始副本、结构计数（标题/表格行/代码块/em-dash）、python Counter 对比反引号引用 LOST/ADDED；弱口径（计数）还需额外下钻补查。每次执行改写都要现场重写这套校验。
- 根因: contract gap——skill 自带三个脚本全是语料级测量（compare-human-ai/check-structure/check-translationese），没有"对这一篇改写产物跑验收"的入口。
- 方案: 新增 `scripts/conservation-check.py`：输入 orig/new 两文件，输出引用、数字、限定词（可能/通常/据说）的 LOST/ADDED 清单 + 标题层级/表格行/代码块/行数结构差，作为改写必过项；即手搓 Counter 思路与结构计数的合并。
- passCheck: `conservation-check.py orig.md new.md` 输出引用/数字/限定词零 LOST 且结构计数一致；该命令写入 SKILL.md 验收清单作为机检项。
- 证据: 01a0a415-7d22#78,#107,#109,#115
- 出现: 2026-09-18 diagnose#1
