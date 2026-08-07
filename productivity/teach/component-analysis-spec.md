# Component Analysis Spec — AI 粗筛方法 (#16, map #12)

## 目标

批量生成完毕后,AI 扫描所有 lesson,粗筛可复用组件候选清单,输出 Markdown 报告供人精筛。

## 两层扫描

### 层 1:NOTES.md 语义标注

每个工作区的 NOTES.md 包含 worker 自行记录的"CSS 组件/模式"段落。

扫描方法:
```bash
# 提取所有工作区的 NOTES.md 中组件相关段落
for dir in ~/teach-lab/*/; do
  echo "=== $(basename $dir) ==="
  sed -n '/CSS 组件/,/设计决策/p' "$dir/NOTES.md" 2>/dev/null
done
```

### 层 2:inline CSS class 提取

扫描所有 lesson HTML 的 `<style>` 块,提取 class 名和关键 CSS 规则。

扫描方法:
```bash
# 提取所有 lesson 的 inline CSS class 并集
find ~/teach-lab -name "*.html" -path "*/lessons/*" | while read f; do
  workspace=$(echo "$f" | grep -oP 'teach-lab/\K[^/]+')
  awk '/<style>/,/<\/style>/' "$f" | grep -oP '\.[a-z][-a-z0-9]+' | sort -u | while read cls; do
    echo "$workspace|$cls"
  done
done | sort > /tmp/component-raw.txt

# 频率统计:每个 class 出现在多少个工作区
cut -d'|' -f2 /tmp/component-raw.txt | sort | uniq -c | sort -rn
```

## 语义归类

按功能分类(不是按 CSS 结构):

| 类别 | 语义 | 典型 class 前缀/关键词 |
|---|---|---|
| 流程图 | 横向/纵向流程可视化 | pipeline, flow, diagram, arch, stage |
| 卡片 | 信息容器,带标题/标签 | card, layer, box, mode |
| 可视化 | 数据/结构可视化 | fusion, tree, chart, viz, score |
| 决策 | 可折叠/展开的判断组件 | decision, verdict, mode-card |
| 终端 | 伪命令行输出 | cmd, terminal, prompt, output |
| 步骤 | 编号步骤引导 | step, num, counter |
| 基础排版 | 通用元素 | callout, quiz, meta, footer, tag |
| 主题 | 颜色方案 | --bg, dark, theme |

## 输出格式

Markdown 报告 `~/teach-lab/_component-analysis.md`,包含:

### 1. 组件频率表

| 组件名 | 语义类别 | 出现工作区数 | 出现 lesson 数 | 候选? |
|---|---|---|---|---|
| .callout-note | 基础排版 | 8/12 | 25/40 | ✅ |
| .pipeline | 流程图 | 2/12 | 3/40 | ✅ |
| .fusion-viz | 可视化 | 1/12 | 1/40 | ❌ |

### 2. 语义归类清单

按类别分组,列出每个组件 + CSS 规则摘要 + 出现位置。

### 3. 候选抽取清单(粗筛标准)

- **候选**:出现 ≥2 个工作区 OR ≥3 个 lesson
- **不候选**:只出现在 1 个工作区 1 个 lesson(专用组件)

每个候选标注:
- 组件名 + 语义类别
- CSS 规则摘要(关键属性,非完整代码)
- 出现位置列表
- AI 建议:抽取 / 待定 / 不抽取 + 理由

### 4. 跨工作区 CSS 变量对比

对比各工作区的 CSS 变量(--bg, --accent, --text 等),识别:
- 共识变量(所有工作区都定义了)
- 分歧变量(值不同)
- 建议统一值

## 人精筛流程

1. 人阅读 `~/teach-lab/_component-analysis.md`
2. 人浏览随机 lesson(可选,验证组件实际效果)
3. 人在对话里告诉 AI 最终决定:哪些抽取、哪些不抽取
4. AI 根据决定更新 #4 的 base.css 和 #10 的 resolution

## 反馈回 #4

精筛结果以 resolution comment 形式回传到 #10:
- 抽取的组件清单 + CSS 代码
- 不抽取的组件 + 理由
- 对 base.css 的更新建议
