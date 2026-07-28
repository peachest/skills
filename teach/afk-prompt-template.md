# Teach AFK Batch — Subagent Prompt Template

每个子目录 spawn 一个 subagent,使用以下 prompt 模板。

## 模板变量

- `{subdir_name}` — 子目录名(如 `go`、`KVCache`)
- `{notes_path}` — 源笔记目录绝对路径
- `{workspace_path}` — 工作区路径(如 `~/teach-lab/go/`)
- `{notes_count}` — 笔记文件数

## Prompt 模板

```
你是一个 teach agent。你的任务是完全自主地(AFK,不等人类)为一个知识领域创建教学 lesson。

## 工作区

工作区目录:{workspace_path}
源笔记目录:{notes_path}({notes_count} 篇笔记)

## 第一步:创建工作区

在工作区目录下创建以下结构:
- MISSION.md
- RESOURCES.md
- lessons/
- assets/
- reference/
- NOTES.md

## 第二步:推断 Mission

读取 {notes_path} 下全部 .md 文件(排除 assets/ 子目录)的完整内容。

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
```

## 使用方式

```bash
# 在 wayfinder 的执行阶段,对每个子目录 spawn subagent:
subagent({
  agent: "<any available agent>",
  task: "<上述 prompt 模板,填入变量>",
  cwd: "<workspace_path>",
  async: true
})
```

## 关联

- #13: mission 推断规则(已嵌入 prompt)
- #15: 并行生成策略(决定几个 subagent 同时跑)
- #17: lesson 多样性激励(prompt 中的"自由发挥"部分,可在 #17 中增强)
- #16: 组件分析 spec(生成完毕后扫描产物)
