# Teach AFK Batch — Subagent Prompt Template

每个子目录 spawn 一个 subagent,使用以下 prompt 模板。

## ⚠️ 前置步骤(父 agent 执行,在 spawn subagent 之前)

Subagent 沙箱限制所有文件访问到 CWD 内。父 agent **必须**在 spawn 前把源笔记复制到工作区:

```bash
mkdir -p ~/teach-lab/<subdir>/source-notes
cd <notes_path>
find . -name '*.md' -not -path '*/assets/*' | while read f; do
  dir=$(dirname "$f")
  mkdir -p "~/teach-lab/<subdir>/source-notes/$dir"
  cp "$f" "~/teach-lab/<subdir>/source-notes/$dir/"
done
```

这会保留子目录结构(如 `source-notes/llamaIndex/LlamaIndex.md`)。Subagent 从 `source-notes/` 读取笔记,而非原始路径。

**冒烟测试验证**(RAG,4 篇笔记):此方案可行,subagent 成功读取全部笔记并生成了 3 课 + 1 reference。

## 模板变量

- `{subdir_name}` — 子目录名(如 `go`、`KVCache`)
- `{notes_path}` — 源笔记目录绝对路径(仅父 agent 使用,用于预复制)
- `{workspace_path}` — 工作区路径(如 `~/teach-lab/go/`)
- `{notes_count}` — 笔记文件数

## Prompt 模板

```
你是一个 teach agent。你的任务是完全自主地(AFK,不等人类)为一个知识领域创建教学 lesson。

## 工作区

工作区目录:{workspace_path}
源笔记目录:source-notes/({notes_count} 篇笔记,已由父 agent 预复制到工作区内)

## 第一步:创建工作区

在工作区目录下创建以下结构(如果尚不存在):
- MISSION.md
- RESOURCES.md
- lessons/
- assets/
- reference/
- NOTES.md

注意:source-notes/ 目录已存在,里面是源笔记。不要修改它。

## 第二步:推断 Mission

读取 source-notes/ 下全部 .md 文件的完整内容。

从笔记内容推断 MISSION.md:

- **Why**: 从笔记内容推断用户为什么记这些笔记。是什么真实世界目标驱动了这些笔记?避免抽象的"理解 X",推到具体结果。
- **Success looks like**: 从笔记覆盖的主题提取 3-5 个可观测的能力目标。
- **Constraints**: 固定填写:"从零开始,基于已有笔记,AFK 自动生成,lesson 数量由 AI 自行决定"
- **Out of scope**: 从子目录边界推断相邻但不涉及的主题。

使用 MISSION-FORMAT.md 的格式。

## 第三步:生成 Lesson

根据笔记内容和 mission,生成 lesson HTML 文件。

### Lesson 规则

- 每课一个自包含 HTML 文件,保存到 lessons/ 目录,文件名 0001-<dash-case-name>.html,编号递增
- 每课聚焦一个 tightly-scoped 的知识点,与 mission 直接相关
- lesson 应该简短,可快速完成,给学习者一个 tangible win
- 包含推荐阅读资源链接
- 包含"有任何不清楚的地方,直接问我"的提示
- 如果适合,加入自测 quiz(用 data-quiz JSON 声明式格式)

### CSS 与组件:自由发挥

不强制使用任何 CSS 框架。你可以:
- 自定义 inline <style> 或独立 CSS 文件
- 根据内容性质选择最合适的呈现方式(流程图、对比表、步骤引导、伪终端、图示、证明链等)
- 创造你认为最适合这个内容的视觉呈现方式
- 不需要和其他子目录的 lesson 风格一致

目标:通过多样化的内容呈现,暴露尽可能多的组件模式。

### Lesson 数量

由你自行决定。原则:
- 覆盖笔记中的核心知识点
- 每课一个清晰的主题,不贪多
- 宁可少而精,不要多而泛

## 第四步:创建 Reference 文档

如果主题适合,创建 reference/ 下的参考文档(速查卡、术语表等)。这些是跨 lesson 复用的压缩知识。

## 第五步:记录

在 NOTES.md 中记录:
- 生成了几课,每课的主题
- 使用了哪些 CSS 组件/模式
- 有什么值得注意的设计决策

## 不要做的事

- 不要等待人类确认或输入
- 不要尝试和人类对话
- 不要打开 lesson 文件(不需要 CLI 命令)
- 不要创建 learning-records/(AFK 模式下没有学习者)
- **绝对不要向工作区目录之外的路径写任何文件**。所有文件(MISSION.md、RESOURCES.md、NOTES.md、lessons/、reference/)都必须写在工作区目录内。如果 write 工具失败,用 `cat > 文件名 <<'EOF'` heredoc 写文件时,确保文件名是相对路径(如 `lessons/0001-xxx.html`),不要用绝对路径或 `~/` 前缀。先 `cd` 到工作区目录再写文件。
```

## 使用方式

```bash
# 在 wayfinder 的执行阶段,对每个子目录:

# 1. 父 agent 预复制源笔记到工作区(保留子目录结构)
mkdir -p ~/teach-lab/<subdir>/source-notes
cd <notes_path>
find . -name '*.md' -not -path '*/assets/*' | while read f; do
  dir=$(dirname "$f")
  mkdir -p "~/teach-lab/<subdir>/source-notes/$dir"
  cp "$f" "~/teach-lab/<subdir>/source-notes/$dir/"
done

# 2. Spawn subagent with CWD = workspace
subagent({
  agent: "<any available agent>",
  task: "<上述 prompt 模板,填入变量>",
  cwd: "~/teach-lab/<subdir>",
  async: true
})
```

## 冒烟测试发现 (#14 验证)

RAG 子目录(4 篇笔记)冒烟测试结果:

- ✅ **Prompt 可行**:subagent 15 分钟内自主完成全部流程
- ✅ **Mission 推断正确**:从笔记内容提取了 RAG pipeline 的 Why/Success/Out-of-scope
- ✅ **CSS 多样性自然产生**:3 课产出 77 个不同 CSS class,含 pipeline 流程图、暗色主题、融合可视化等
- ✅ **Quiz 声明式格式**:3 课都用 data-quiz JSON
- ✅ **NOTES.md 组件记录**:为 #16 组件分析提供了结构化输入
- ⚠️ **大目录 token 消耗**:go(231 篇)全读可能超出 context,需在 #15 并行策略中考虑分批

### 值得注意的设计行为

- AI 自行决定每课不同视觉风格(暖色/暗色/多彩),多样性激励(#17)可能不需要额外干预
- AI 自行决定了 3 课(而非更多),覆盖了笔记的核心知识点
- lesson 2 主动使用了暗色主题 — 这是 #4 的 #11(暗色模式)没有预期的发现

## 并行生成策略 (#15)

### 大目录按主题拆分

大目录(go/k8s/KVCache)按主题拆分为多个独立工作区,每个工作区一个 subagent。每个工作区有自己的 MISSION.md 和 lessons/。

### 工作区清单(12 个 subagent + RAG 已完成)

| 批次 | 工作区 | 来源 | ~Tokens |
|---|---|---|---|
| 1 | `teach-lab/go-core` | go 语言核心+并发 | ~100K |
| 1 | `teach-lab/go-eng` | go 测试+工程实践 | ~90K |
| 1 | `teach-lab/go-tools` | go 工具链+设计模式 | ~80K |
| 1 | `teach-lab/go-k8s` | go K8s controller+可观测性 | ~110K |
| 2 | `teach-lab/k8s-scheduling` | k8s 调度+DRA+资源管理 | ~85K |
| 2 | `teach-lab/k8s-ops` | k8s 部署+运维+网络 | ~85K |
| 2 | `teach-lab/KVCache-quant` | KVCache 量化方法 | ~80K |
| 2 | `teach-lab/KVCache-sys` | KVCache 系统与缓存管理 | ~80K |
| 3 | `teach-lab/前端` | 前端 20 篇 | ~27K |
| 3 | `teach-lab/函数式编程` | 8 篇 | ~30K |
| 3 | `teach-lab/git` | 7 篇 | ~10K |
| 3 | `teach-lab/attention` | 7 篇 | ~3K |

RAG 已完成(冒烟测试),跳过。

### 调度规则

- **每批 4 个 subagent 并行**,共 3 批
- 每批等全部完成再跑下一批
- 预计总时间 ~45-60 分钟(每批 ~15-20 分钟)
- 父 agent 负责预分割笔记到各工作区的 `source-notes/`

### 父 agent 预分割流程

对每个大目录,父 agent:
1. 读取全部笔记文件名
2. 按主题分类(用上方表格的分组)
3. 为每个工作区创建 `source-notes/` 并复制对应笔记
4. Spawn subagent

## 关联

- #13: mission 推断规则(已嵌入 prompt)
- #15: 并行生成策略(已确定:4 个一批,大目录按主题拆分)
- #17: lesson 多样性激励(prompt 中的"自由发挥"部分,可在 #17 中增强)
- #16: 组件分析 spec(生成完毕后扫描产物)

## 多样性激励决策 (#17)

**不激励——"自由发挥"已足够。**

冒烟测试证据(RAG,3 课):
- 3 种背景色(暖米白/暗色/暖白)
- 77 个不同 CSS class,16-42 个独有 per lesson
- 共享的 22 个全是基础排版(callout/quiz/meta)
- 独有的全是内容驱动领域组件(pipeline/decision-matrix/fusion-viz/tree-diagram)

AI 的随机性 + 主题差异 = 自然多样性。无需额外激励。
