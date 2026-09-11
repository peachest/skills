# article sources — skill 的原始文章来源账本

个人 skills 中一部分概念源自公开博客/文章/视频，开发时未记录出处。此文件是回溯账本
（2026-09-11 从 `~/.pi/agent/sessions/` 的 fetch-article 调用提取，范围 `~/skills` 与
`~/research` 项目下的 session）。新 skill 若有文章来源，开发时即记入此处。

回溯口径：session 中出现 fetch-article 抓取 + 同 session write/edit 了该 skill 的文件。
"启发"表示文章是概念来源但 skill 非该 session 直接产出。

## 已确认来源

| skill | 原始文章/视频 | 佐证 session |
|-------|--------------|--------------|
| mda-slo | 《Auto Research又进化了：贝叶斯联手大模型，AI自己设计关键实验》 mp.weixin.qq.com/s/LiWbRSI1c3zf7LGzTAB34A | 019fffa3-d6db-7f41-be63-4c68a08e14a2（同 session 写 mda-slo SKILL + references） |
| multi-agent-collab | 《Anthropic最新多智能体研究来了！》 mp.weixin.qq.com/s/KW5vvF2w1pkkBW36lLDcAg + anthropic.com/research/multiagent-systems 原文 | 01a07f11-6d78-737f-bc71-940fe6c06622#205（同 session 写 multi-agent-collab SKILL + references） |
| okb | 《AI智能体的记忆，终于有人认真研究"文件系统"这条路了——新论文给出五个反直觉答案》 mp.weixin.qq.com/s/oBhZWoS3GCcLFKgozprj_Q | 01a03c01-5a8d-7127-a49b-c15fb4a010e7#322（首写 okb SKILL）；01a062c0-556c-77f9-a761-7fcf7b3f97e1（gold 层讨论 + 30+ 篇公众号 corpus，落 research/weixin-ontology） |
| dynamic-workflow | 《谈点反共识的事情：我们不需要新造 Dynamic Workflows 这个概念》 mp.weixin.qq.com/s/gB06Q4A_R437jqBAkXf3EQ | 01a03e3c-06f7-7039-bd19-3740a786e1cc#4（同 session 写 dynamic-workflow SKILL） |
| project-wiki | 《把文档当代码一样治：doc-system-kb-builder 让"文档又和现实漂了"变成一件能跑回归的事》 mp.weixin.qq.com/s/AnTt7VYePOucu6si9g8RsQ | 01a06682-3218-7bec-866c-7116e2d06560#12（对比后整合，同 session 写 project-wiki） |
| mutation-testing | 《AI改代码快如闪电，传统测试崩了？试试JiTTesting！》 mp.weixin.qq.com/s/pca8KHNpiPN5XIxYjIogIg | 01a08a77-129e-72fd-9137-7e352b41328f#4（启发既有 skill；作者 session 01a02243-8420-7e52-8d0f-86d1231bc147） |
| review-spec / wayfinder（vendor） | 《阿里 SkillWeaver：跳过加载全部工具，Agent Token 消耗直降 99%》 mp.weixin.qq.com/s/ZMHTVLsarxvQGA8xorLoOA + mp.weixin.qq.com/s/sSeiJsPBRD99LIG-okgDXQ | 01a08975-1b01-75ff-b888-f478f59f1465#4（同 session 写 wayfinder/review-spec） |
| to-intent | INTENT.md 开放格式规范 v1.0 www.intentdocs.com/intent-md（产品模式：四级 intent + 稳定 story id）；《The AI-Native SDLC playbook》 claude.com/blog/the-ai-native-sdlc-playbook（effort 模式：intent/<slug>.md intake + Open questions 分流） | 01a07ce2-4265-7369-a2da-260a37df6eab#4（首写 to-intent，产品模式）；#83（playbook 对照分析 → effort 模式落地） |
| skill-call-extract / skill-call-diagnose | 《阿里开源了一套 skill 验证的全流程方法》 mp.weixin.qq.com/s/CIryyflljZlVS4trTbCSDw | 01a03e36-fece-7cb7-b4f6-d81cef1fcceb（写 skill-call-extract）；01a03e3c-7a73-7ee2-9b06-c7d1bdb744a0（落 research/skill-eval-landscape） |
| wiki/ 本身（WikiSkill 设计） | 《超越SkillOpt！谷歌发布 WikiSkill：技能进化配上持久知识库，9B 反超 27B模型》 mp.weixin.qq.com/s/fXdxOo0ghm6-B9VNUdr23Q（arXiv 2608.27454） | 01a056bb-31b8-750d-a403-9ac9585eb3b2#4（落 research/skill-eval-landscape，设计判定见本地 `~/research/skill-eval-landscape/03-wikiskill-skill-evolution.md`） |
| teach（vendor/mattpocock） | 视频《我是怎么用AI学东西的 - Eero Alvar》 bilibili.com/video/BV1cSbi62Eu5；视频《Anthropic开始授课！所有AI课程免费学》 bilibili.com/video/BV1TohP6zETj（TA Adventure 落地） | 01a01dcb-9758-7da8-bae3-0d9e8fe6ce5e、01a03d80-f5f3-71bd-8751-4343728a1c5d |
| bilibili-transcriber | 无文章来源：bilibili 视频 + FunASR 官方文档（github.com/modelscope/FunASR docs/tutorial） | 01a00e86-ea5b-7a74-978a-11bc658da63c、01a00db9-f9f2-7636-8f6f-2ed5c2a2ec4e |

## 排除（research-only，非 skill 来源）

token-factory/kvcache、pdd、attention、okf、kserver、afd、weixin-connector 等目录下的
session 抓取均为领域调研（KV Cache、PD 分离、Attention 变体、RAG、KServe、vLLM AFD 等），
产出在 `~/research/<topic>/`，与 skill 开发无关，不入此账本。
