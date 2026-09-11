# article sources — skill 的原始文章来源账本

个人 skills 中一部分概念源自公开博客/文章/视频，开发时未记录出处。此文件是回溯账本
（2026-09-11 从 `~/.pi/agent/sessions/` 的 fetch-article 调用提取，范围 `~/skills` 与
`~/research` 项目下的 session；2026-09-12 二次评审，用 git 创建 commit 时间交叉校验，
修正了"评估型 session 误记为来源"的错误——**拿文章对照既有 skill 的 session 不算来源**）。

新 skill 若有文章来源，开发时即记入此处。归属判定顺序：git `--diff-filter=A` 找创建
commit → 定位创建 session → 查该 session 的实际输入；文章只在演进/评估 session 出现的，
归入"演进来源"。

## 创建来源（文章/视频 → 同 session 创建 skill）

| skill | 原始文章/视频 | 佐证 session |
|-------|--------------|--------------|
| mda-slo | 《Auto Research又进化了：贝叶斯联手大模型，AI自己设计关键实验》 mp.weixin.qq.com/s/LiWbRSI1c3zf7LGzTAB34A | 019fffa3-d6db-7f41-be63-4c68a08e14a2（2026-08-14 同 session 创建 + 文章，概念强匹配：贝叶斯×实验设计=MDA）。注：源不在本 repo，仅存已安装副本 ~/.pi/agent/skills/mda-slo |
| okb | 《AI智能体的记忆，终于有人认真研究"文件系统"这条路了》 mp.weixin.qq.com/s/oBhZWoS3GCcLFKgozprj_Q | 01a03c01-5a8d-7127-a49b-c15fb4a010e7#322（创建 commit 85be07f 2026-08-26 = 文章同 session）；01a062c0-556c-77f9-a761-7fcf7b3f97e1（gold 层讨论 + 30+ 篇公众号 corpus，落 research/weixin-ontology） |
| multi-agent-collab | 《Anthropic最新多智能体研究来了！》 mp.weixin.qq.com/s/KW5vvF2w1pkkBW36lLDcAg + anthropic.com/research/multiagent-systems 原文 | 01a07f11-6d78-737f-bc71-940fe6c06622#205（创建 commit ac94d25 2026-09-08 = 文章同 session；herdr 实践为既有基础，文章驱动协议化） |
| dynamic-workflow | 《谈点反共识的事情：我们不需要新造 Dynamic Workflows 这个概念》 mp.weixin.qq.com/s/gB06Q4A_R437jqBAkXf3EQ | 01a03e3c-06f7-7039-bd19-3740a786e1cc#4（创建 commit a1d293d 2026-08-26 = 文章同 session，skill 是对该文的 Unix 式回应）。注：已移出本 repo，仅存已安装副本 |
| to-intent | INTENT.md 开放格式规范 v1.0 www.intentdocs.com/intent-md（产品模式：四级 intent + 稳定 story id）；《The AI-Native SDLC playbook》 claude.com/blog/the-ai-native-sdlc-playbook（effort 模式：intent/<slug>.md intake + Open questions 分流） | 01a07ce2-4265-7369-a2da-260a37df6eab#4（首写 to-intent，产品模式）；#83（playbook 对照分析 → effort 模式落地） |
| wiki/ 本身（WikiSkill 设计） | 《超越SkillOpt！谷歌发布 WikiSkill：技能进化配上持久知识库，9B 反超 27B模型》 mp.weixin.qq.com/s/fXdxOo0ghm6-B9VNUdr23Q（arXiv 2608.27454） | 01a056bb-31b8-750d-a403-9ac9585eb3b2#4（落 research/skill-eval-landscape，设计判定见本地 `~/research/skill-eval-landscape/03-wikiskill-skill-evolution.md`） |

## 演进来源（skill 先存在，文章/视频驱动后续改版）

| skill | 创建 | 演进来源 |
|-------|------|---------|
| project-wiki | 2026-07-27（7cd5fad），无文章来源 | 《把文档当代码一样治：doc-system-kb-builder…》 mp.weixin.qq.com/s/AnTt7VYePOucu6si9g8RsQ —— 01a06682-3218-7bec-866c-7116e2d06560#12（2026-09-03 对比整合） |
| teach（vendor/mattpocock） | mattpocock 上游 | 视频《我是怎么用AI学东西的 - Eero Alvar》 bilibili.com/video/BV1cSbi62Eu5（学习循环设计输入，session 内 28 处内容引用）—— 01a01dcb-9758-7da8-bae3-0d9e8fe6ce5e；视频《Anthropic开始授课！所有AI课程免费学》 bilibili.com/video/BV1TohP6zETj（TA Adventure 功能落地）—— 01a03d80-f5f3-71bd-8751-4343728a1c5d |
| mutation-testing | 2026-08-21（2f28a1f），session 01a02243-8420-7e52-8d0f-86d1231bc147，输入为视频《Matt Pocock 直播：对话〈代码整洁之道〉作者，AI 时代软件基本功还重要吗》 bilibili.com/video/BV1NFbf6JEj 转录（"对比我的 skills 找启发"） | 《AI改代码快如闪电，传统测试崩了？试试JiTTesting！》 mp.weixin.qq.com/s/pca8KHNpiPN5XIxYjIogIg —— 01a08a77-129e-72fd-9137-7e352b41328f#4（2026-09-10 纯评估，未改 skill 文件，仅参考） |
| review-spec | 2026-08-05（a020da1），无文章来源 | 《阿里 SkillWeaver：跳过加载全部工具，Agent Token 消耗直降 99%》 mp.weixin.qq.com/s/ZMHTVLsarxvQGA8xorLoOA + mp.weixin.qq.com/s/sSeiJsPBRD99LIG-okgDXQ —— 01a08975-1b01-75ff-b888-f478f59f1465#4（2026-09-10 DAG 适配 to-intent/wayfinder 生态时更新） |
| wayfinder（vendor/mattpocock） | mattpocock 上游同步 | 同上 SkillWeaver 文章 —— 01a08975 本地适配（discovery-routing 等） |

## 间接链条（文章 → research → skill，非直接创建）

| skill | 直接触发 | 间接来源 |
|-------|---------|---------|
| skill-call-extract / skill-call-diagnose | 2026-09-07（62bfc5a/8a4adff），session 01a07d09-4d95-77b4-9251-cd82935eb8a2：诊断 peer session 调用 fact-check skill 的 token 浪费摩擦 | 《阿里开源了一套 skill 验证的全流程方法》 mp.weixin.qq.com/s/CIryyflljZlVS4trTbCSDw（2026-08-26，01a03e36/01a03e3c-7a73 → research/skill-eval-landscape，02-session-log-to-eval.md 为概念桥梁） |

## 无文章来源

| skill | 说明 |
|-------|------|
| bilibili-transcriber | 创建 commit 2898805 2026-07-21，无外部文章；唯一外部参考是 FunASR 官方文档（github.com/modelscope/FunASR docs/tutorial），用于 2026-08-17 chunking 演进（01a00e86-ea5b-7a74-978a-11bc658da63c） |

## 排除（research-only，非 skill 来源）

token-factory/kvcache、pdd、attention、okf、kserver、afd、weixin-connector 等目录下的
session 抓取均为领域调研（KV Cache、PD 分离、Attention 变体、RAG、KServe、vLLM AFD 等），
产出在 `~/research/<topic>/`，与 skill 开发无关，不入此账本。
