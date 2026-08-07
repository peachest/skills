---
name: paper-translate
description: 将 LaTeX 论文源文件翻译为中文 Markdown 文档
type: general
---

# 论文翻译 Skill

## 使用场景

当前工作目录为论文目录，子目录下存放 arxiv 下载的 `.tex` 源文件。

## 执行流程

### 1. 定位主 tex 文件

在论文子目录中查找主 `.tex` 文件：
- 查找包含 `\documentclass` 和 `\begin{document}` 的文件
- 通常命名为 `paper.tex`、`main.tex`、`acl_latex.tex` 或目录名同名的 `.tex` 文件

### 2. 翻译 TeX 内容为中文 Markdown

#### 章节与结构
| LaTeX                               | Markdown                                 |
| ----------------------------------- | ---------------------------------------- |
| `\section{Title}`                   | `# Title`（翻译标题）                    |
| `\subsection{Title}`                | `## Title`（翻译标题）                   |
| `\subsubsection{Title}`             | `### Title`（翻译标题）                  |
| `\begin{abstract}...\end{abstract}` | `## 摘要`                                |
| `\appendix`                         | `## 附录`，后续章节变 `### 附录 A. 标题` |
| `\section*{Acknowledgements}`       | `## 致谢`                                |
| `\bibliography{}`                   | `## 参考文献`                            |

#### 公式处理
- 行内公式 `$...$` → `$...$` 保持原样
- Display 公式 `$$...$$` 或 `\[...\]` → `$$...$$`
- `\begin{equation}...\end{equation}` → `$$...$$`
- `\begin{align}...\end{align}` → `$$...$$`
- 公式内容**不翻译**，保留 LaTeX 格式

#### 交叉引用（超链接）
| LaTeX                                | Markdown                          |
| ------------------------------------ | --------------------------------- |
| `\label{sec:name}`                   | `{#sec:name}`（锚点，加在标题后） |
| `\ref{sec:name}`、`\cref{sec:name}`  | `[§名称](#sec:name)`              |
| `\ref{fig:1}`、`\autoref{fig:1}`     | `[图 1](#fig:1)`                  |
| `\ref{table:1}`、`\autoref{table:1}` | `[表 1](#table:1)`                |
| `\ref{eq:1}`、`\eqref{eq:1}`         | `[公式 (1)](#eq:1)`               |
| 范围引用 `\ref{a}--\ref{b}`          | `[§A](#a)~[§B](#b)`               |
| `\pageref{label}`                    | `(第 X 页)`                       |

#### 引用处理
| LaTeX              | Markdown                                                |
| ------------------ | ------------------------------------------------------- |
| `\cite{key}`       | `key[^cite-key]` + 文末 `[^cite-key]: 参考文献详细信息` |
| `\cite{key1,key2}` | `key1[^cite-key1],key2[^cite-key2]`                     |
| `\cite[p.10]{key}` | `key, p.10[^cite-key]`                                  |
| `\citet{key}`      | `作者名 [^cite-key]`                                    |

**示例**：
```latex
Previous work~\cite{smith2020deep,johnson2021learning} has shown...
```
→
```markdown
先前的工作 smith2020deep[^cite-smith2020deep],johnson2021learning[^cite-johnson2021learning] 表明...

[^cite-smith2020deep]: Smith et al. "Deep Learning for X". NeurIPS 2020.
```

#### 图片处理
```latex
\begin{figure}
  \includegraphics[options]{path/to/fig.png}
  \caption{Figure Caption}
\end{figure}
```
→
```markdown
![图片标题（翻译后）](path/to/fig.png)

*Figure: 图片标题（翻译后）*
```

**子图处理**：
```latex
\begin{figure}
  \begin{subfigure}
    \includegraphics{fig1a.png}
    \caption{子图 A}
  \end{subfigure}
  \begin{subfigure}
    \includegraphics{fig1b.png}
    \caption{子图 B}
  \end{subfigure}
  \caption{总标题}
\end{figure}
```
→
```markdown
![总标题](fig1a.png)
*子图 A: 子图 A 标题*

![总标题](fig1b.png)
*子图 B: 子图 B 标题*
```

#### 表格处理
```latex
\begin{table}
\begin{tabular}{|c|c|}
\hline
A & B \\ \hline
1 & 2 \\ \hline
\end{tabular}
\caption{Table Caption}
\end{table}
```
→
```markdown
**Table: 表格标题（翻译后）**

| A   | B   |
| --- | --- |
| 1   | 2   |
```

表格内文字需要翻译。

#### 文本命令
| 类别       | LaTeX                              | Markdown                       |
| ---------- | ---------------------------------- | ------------------------------ |
| 强调       | `\emph{text}`、`\textit{text}`     | `**text**`                     |
| 粗体       | `\textbf{text}`                    | `**text**`                     |
| 代码       | `\texttt{code}`                    | `` `code` ``                   |
| 上标       | `\textsuperscript{*}`              | `<sup>*</sup>`                 |
| 下划线     | `\underline{text}`                 | `<u>text</u>`                  |
| 高亮       | `\hl{text}`                        | `==text==`                     |
| 特殊符号   | `\&` `\%` `\$` `\{` `\}`           | `&` `%` `$` `{` `}`            |
| 商标       | `\textregistered` `\texttrademark` | `®` `™`                        |
| 缩写       | `\eg` `\ie` `\etal` `\etc`         | 「例如」「即」「等人」「等等」 |
| 自定义命令 | `\name` `\method` `\model`         | **本文提出的方法名称**         |

#### 定理与证明环境
| 环境                            | Markdown                             |
| ------------------------------- | ------------------------------------ |
| `theorem`、`lemma`、`corollary` | `> **定理/引理/推论 X**. 内容`       |
| `definition`、`assumption`      | `> **定义/假设 X**. 内容`            |
| `proof`                         | `> **证明**: 内容 □`                 |
| `algorithm`                     | 保留为代码块或「见原文 Algorithm 1」 |

#### 其他命令
| 命令                               | 处理                          |
| ---------------------------------- | ----------------------------- |
| `itemize`/`enumerate`              | Markdown 列表                 |
| `\footnote{text}`                  | `[^footnote-n]: text`（文末） |
| `\todo{text}`                      | 移除或 `<!-- TODO: text -->`  |
| `\vspace`、`\hspace`、`\smallskip` | 移除                          |
| `\\`                               | 根据上下文保留换行            |
| `~`                                | 普通空格                      |

#### 会议/期刊模板特殊命令
- **ACL/EMNLP**: `\newparagraph` → `####`
- **NeurIPS/ICML**: `acks` 环境 → `## 致谢`
- **CVPR/ICCV**: `\ie`、`\eg`、`\etal` 已定义为命令
- **arXiv**: `\arxiv{1234.5678}` → `arXiv:1234.5678`
- **IEEE**: `\thanks{}` → 脚注

#### 多文件项目
如果论文分布在多个 `.tex` 文件中：
- 识别主文件中的 `\input{}` 和 `\include{}` 命令
- 按顺序合并所有被引入的文件内容
- 图片路径相对于主文件解析

### 3. 输出中文 Markdown

在论文子目录生成 `<论文名>.md`，输出到当前目录下。不要输出到 tex 源代码子目录中，因此**注意引用源码中文件时的路径**正确。

```markdown
# [翻译后的标题]

**原文标题**: Original Title
**作者**: Author Name

---

## 摘要

[翻译后的摘要内容]

---

## 1. 引言

[翻译后的正文内容]

$$ E = mc^2 $$

![图片标题](figures/fig1.png)

| 表头 1 | 表头 2 |
| ------ | ------ |
| 内容 1 | 内容 2 |
```

## 输出要求

1. **章节结构**与原文保持一致
2. **公式**保持 LaTeX 格式不翻译
3. **图片路径**正确指向原文件
4. **表格**转为 Markdown 格式并翻译内容
5. **引用**使用脚注便于查阅
6. **定理/证明**使用引用块格式
7. **交叉引用**转换为 Markdown 超链接

## 自定义命令处理

### 识别自定义命令

扫描源文件中的 `\newcommand`、`\renewcommand`、`\def` 等定义：

```latex
\newcommand{\method}{OurMethod}
\newcommand{\R}{\mathbb{R}}
\newcommand{\norm}[1]{\|#1\|}
\def\eg{\textit{e.g.}}
```

### 替换规则

| 定义类型                                       | 处理方式                                |
| ---------------------------------------------- | --------------------------------------- |
| 简单文本替换 `\newcommand{\name}{Text}`        | 将所有 `\name` 替换为 `Text`            |
| 数学符号 `\newcommand{\R}{\mathbb{R}}`         | 保留定义，公式中直接展开为 `\mathbb{R}` |
| 带参数命令 `\newcommand{\norm}[1]{\|#1\|}`     | 将 `\norm{x}` 展开为 `\|x\|`            |
| 缩写命令 `\newcommand{\eg}{e.g.}`              | 按文本命令规则处理（→「例如」）         |
| 模型/方法名 `\newcommand{\model}{TransFormer}` | 保留为 **TransFormer** 或原文           |

### 处理步骤

1. **预扫描**：在翻译前先扫描所有 `.tex` 文件，收集自定义命令定义
2. **构建映射表**：建立命令名 → 展开形式的映射
3. **展开替换**：翻译前将正文和公式中的自定义命令展开
4. **保留语义**：对于表示方法名、模型名的命令，展开后添加加粗标记

**示例**：
```latex
% 源文件
\newcommand{\ourmethod}{\textbf{DeepLearn}}
\newcommand{\loss}{\mathcal{L}}

We propose \ourmethod with \loss function.
```
→
```markdown
我们提出 **DeepLearn** 方法，使用 $\mathcal{L}$ 损失函数。
```

---

## 边界情况处理

| 情况                           | 处理方式                     |
| ------------------------------ | ---------------------------- |
| 公式中的文本（如 `\text{if}`） | 保持原样                     |
| 未识别的命令                   | 从上下文推断，或保留为注释   |
| 图片文件找不到                 | 保留原始路径，添加注释       |
| 参考文献条目缺失               | 保留引用 key，标注「待补充」 |
| 复杂的 TikZ 图                 | 标注「见原图：Figure X」     |
| 自定义环境                     | 根据内容判断类型，适当转换   |
| 自定义命令未定义               | 保留原命令，添加注释说明     |

## 文件名约定

- 输入：`<name>.tex`
- 输出：`<中文标题>.md`
