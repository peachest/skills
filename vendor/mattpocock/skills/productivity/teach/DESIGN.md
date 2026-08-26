---
name: teach Lesson Design System
version: alpha
description: >-
  teach 课件的设计系统契约。令牌体系（字号 scale / 缓动 / 间距 / 密度 / 焦点 / 动画）
  借鉴 Anthropic CDS，callout 语义色保留 GitHub 风高饱和以适应教学场景的强区分需求。
  正文采用 serif（voice 字体）营造 editorial/academic 阅读感，与 teach 的「教学论文」
  性质契合。本文件是 base.css 改造与课件生成的目标契约。
colors:
  # ── 中性面（Anthropic ivory/ink 哲学，light-first） ──
  bg: "#ffffff"
  surface: "#ffffff"
  code-bg: "#f6f8fa"
  border: "#e1e4e8"
  text: "#1a1a1a"
  muted: "#6b6b6b"
  light: "#999999"
  # ── 品牌强调（Claude 血统，clay 用于 brand fill） ──
  accent: "#0366d6"
  accent-bg: "#0969da14"
  brand: "#d97757"
  brand-emphasized: "#c6613f"
  # ── 语义色（GitHub 风，教学场景强区分，保留） ──
  green: "#22863a"
  green-bg: "#f0fff4"
  red: "#cb2431"
  red-bg: "#ffeef0"
  orange: "#d97706"
  orange-bg: "#fffbdd"
  purple: "#6f42c1"
  purple-bg: "#f6f8fa"
  teal: "#2dd4bf"
  teal-bg: "#f0fdfa"
typography:
  # ── 字族（serif 作 voice，呼应 Anthropic --cds-font-voice） ──
  voice:
    fontFamily: "Georgia, 'Songti SC', 'Noto Serif SC', 'Times New Roman', serif"
    fontFeature: '"pnum" on, "lnum" on, "liga" on'
  ui:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Helvetica Neue', sans-serif"
  mono:
    fontFamily: "'SF Mono', 'Fira Code', 'Consolas', 'Liberation Mono', monospace"
  # ── 字号 scale（令牌化，收敛原 15 个 ad-hoc 值） ──
  display:
    fontFamily: "{typography.ui.fontFamily}"
    fontSize: "2.75rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  h1:
    fontFamily: "{typography.ui.fontFamily}"
    fontSize: "1.75rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  h2:
    fontFamily: "{typography.ui.fontFamily}"
    fontSize: "1.4rem"
    fontWeight: 600
    lineHeight: 1.35
  h3:
    fontFamily: "{typography.ui.fontFamily}"
    fontSize: "1.2rem"
    fontWeight: 600
    lineHeight: 1.4
  h4:
    fontFamily: "{typography.ui.fontFamily}"
    fontSize: "1.05rem"
    fontWeight: 600
    lineHeight: 1.45
  body:
    fontFamily: "{typography.voice.fontFamily}"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.75
  body-lg:
    fontFamily: "{typography.voice.fontFamily}"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.7
  small:
    fontFamily: "{typography.ui.fontFamily}"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.5
  caption:
    fontFamily: "{typography.ui.fontFamily}"
    fontSize: "0.75rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.04em"
  code:
    fontFamily: "{typography.mono.fontFamily}"
    fontSize: "0.9rem"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  pill: 1000px
spacing:
  sp-1: 4px
  sp-2: 8px
  sp-3: 12px
  sp-4: 16px
  sp-5: 24px
  sp-6: 32px
  sp-8: 48px
  sp-10: 64px
components:
  callout:
    backgroundColor: "{colors.accent-bg}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "{spacing.sp-4}"
  callout-tip:
    backgroundColor: "{colors.purple-bg}"
  callout-warning:
    backgroundColor: "{colors.orange-bg}"
  callout-success:
    backgroundColor: "{colors.green-bg}"
  callout-danger:
    backgroundColor: "{colors.red-bg}"
  quiz-option:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "{spacing.sp-3}"
  quiz-option-hover:
    backgroundColor: "{colors.accent-bg}"
    textColor: "{colors.accent}"
  quiz-option-selected:
    backgroundColor: "{colors.green-bg}"
    textColor: "{colors.green}"
  tech-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: "{spacing.sp-5}"
---

## Overview

teach 课件是**教学论文**，不是营销页。设计基调是 **editorial / academic / restrained**——
serif 正文营造印刷论文的阅读感，单列长文阅读栏，克制的中性面 + 仅在 callout/语义处用色。

令牌体系（字号 scale、缓动、间距、密度、焦点、动画）借鉴 Anthropic CDS（academy.claude.com
与 platform.claude.com 实证），但 **callout 语义色保留 GitHub 风高饱和**——教学场景需要
note/tip/warning/success/danger 之间有强视觉区分，Anthropic 的低饱和自然色在「快速辨识
类别」上不如高饱和色有效。

本文件是 base.css 改造与课件 HTML 生成的**目标契约**。生成课件时应优先引用此处的令牌，
而非裸写数值。

## Colors

色彩分三层，各有明确职责：

### 中性面（light-first）

- **bg `#ffffff` / surface `#ffffff`**：页面与卡片底，纯白。teach 课件白天阅读居多，保留 light-first（与 Anthropic Academy 的 dark-first 不同）。
- **code-bg `#f6f8fa`**：代码块底，微灰退后。
- **border `#e1e4e8`**：分隔线，低对比不抢戏。
- **text `#1a1a1a` / muted `#6b6b6b` / light `#999`**：三级文字层次。

### 品牌强调（Claude 血统）

- **brand `#d97757`（clay）/ brand-emphasized `#c6613f`**：Claude 标志色，用于 brand fill（按钮强调、品牌标识）。保留 `--accent #0366d6`（GitHub 蓝）作为链接色——teach 课件的链接沿用 GitHub 习惯，clay 作为品牌强调色补充。

### 语义色（GitHub 风，强区分，保留）

| 色 | 值 | 用途 |
|---|---|---|
| green | `#22863a` | success callout / quiz 正确 |
| red | `#cb2431` | danger callout / quiz 错误 |
| orange | `#d97706` | warning callout |
| purple | `#6f42c1` | tip callout |
| teal | `#2dd4bf` | 信息补充 |

每种语义色配套 `-bg` 浅底（如 `green-bg #f0fff4`）用于 callout 背景。**不采用** Anthropic
的低饱和自然色（cactus/heather/olive）做 callout——教学场景的快速类别辨识优先于审美克制。

## Typography

### 字族三件套

- **voice（serif）**：`Georgia, Songti SC, Noto Serif SC, …` ——正文语气字体。借鉴 Anthropic
  `--cds-font-voice` 语义，把「正文语气」独立成令牌。serif 营造印刷论文感，是 teach 课件
  的阅读基调。开启 `font-feature-settings: "pnum" on, "lnum" on, "liga" on`（比例数字 +
  lining 数字 + 连字），中英数字混排更整齐。
- **ui（sans）**：`-apple-system, PingFang SC, …` ——标题、导航、UI 元素。
- **mono**：`SF Mono, Fira Code, …` ——代码。

### 字号 scale（令牌化，收敛原 15 个 ad-hoc 值）

原 base.css 有 15 个互不相关的 rem 值（`0.72/0.8/0.88/0.95/1.05/1.2/1.35/1.9…`），无命名
无 scale 关系。收敛为 9 级令牌：

| 令牌 | 字号 | 字族 | 用途 |
|---|---|---|---|
| display | `2.75rem` | ui | 课件大标题（实现时可用 `clamp(2rem,5vw,2.75rem)` 流体缩放） |
| h1 | `1.75rem` | ui | 章标题 |
| h2 | `1.4rem` | ui | 节标题 |
| h3 | `1.2rem` | ui | 小节 |
| h4 | `1.05rem` | ui | 段首 |
| body | `1rem` | voice | 正文（默认） |
| body-lg | `1.125rem` | voice | 引言/重点段 |
| small | `0.875rem` | ui | 辅助说明 |
| caption | `0.75rem` | ui | 元数据/标签（+letter-spacing 0.04em） |
| code | `0.9rem` | mono | 代码 |

**display 用 `clamp()` 流体缩放**（借鉴 Anthropic），小字固定 px/rem 保证可读性。

### 行高与字距

- 行高令牌：`1.2/1.3/1.35/1.4/1.45/1.5/1.7/1.75`（display→caption 递增，正文 1.75 保留）。
- 字距：标题负字距（`-0.01em`~-`0.02em`），caption 正字距（`0.04em`）。

## Layout

- **单列长文阅读栏**：`--max-width: 680px`，居中。与 Anthropic `--text-column-max-width: 640px`
  接近，保留 680px（课件代码块/图表需稍宽）。
- **间距令牌**（`--sp-1`..`--sp-10`，4–64px 线性）：替换散落的 padding/margin 硬值。
- **断点**：补 `992px`（平板）介于现有 `600px` 与 `1024px` 之间，让流程图/矩阵/对比网格
  在平板有中间态。

## Elevation & Depth

借鉴 Anthropic 分层柔阴影（非单层硬阴影）：

- **shadow-sm**：`0 1px 2px #0000000a` ——卡片静止态，极淡。
- **shadow-md**：`0 1px 2px #0000000d, 0 4px 8px #00000014` ——卡片 hover 态，浮起。
- **shadow-focus**：`0 0 0 2px var(--bg), 0 0 0 4px var(--accent)` ——焦点 ring（双层，
  inset page-bg 隔离 + outset ring-color，借鉴 CDS `--cds-focus-shadow`）。

## Shapes

4 级圆角令牌：

| 令牌 | 值 | 用途 |
|---|---|---|
| sm | `4px` | 小元素（badge/tag/code inline） |
| md | `8px` | callout / quiz-option / 按钮 |
| lg | `12px` | tech-card / 大容器 |
| pill | `1000px` | 胶囊形 badge / chip |

原 `--radius: 6px` 收敛进 md（8px，对齐 Anthropic `--cds-radius`）。

## Animation & Motion

**这是本次优化重点**——原 base.css 仅 1 条 transition、0 个 keyframes。全面借鉴 Anthropic
缓动/时长体系 + clip-path 揭示动画。

### 缓动令牌（Anthropic 实证）

```
--ease-out:      cubic-bezier(.165, .84, .44, 1)   /* = ease-out-quart，默认 */
--ease-snap:     cubic-bezier(.32, .72, 0, 1)       /* 吸附，下拉/抽屉 */
--ease-overshoot:cubic-bezier(.34, 1.3, .64, 1)    /* 回弹，反馈出现 */
--ease-in-out-quart: cubic-bezier(.77, 0, .175, 1) /* 双向 */
```

### 时长令牌（对齐 CDS 五档）

```
--dur-fast: 60ms   /* 即时反馈（hover 色） */
--dur-snap: .12s   /* 吸附（下拉展开） */
--dur-base: .2s    /* 默认（卡片 hover） */
--dur-sheet: .3s   /* 大面展开（侧栏） */
--dur-slow: .45s   /* 揭示动画（内容出现） */
```

### 应用原则

1. **多属性同节奏**：`transition: background-color var(--dur-base) var(--ease-out), border-color var(--dur-base) var(--ease-out), color var(--dur-base) var(--ease-out)`——多属性共用时长与缓动，不错拍。
2. **仅交互元素加 transition**：链接/按钮/卡片/quiz-option 加；正文 `p/h1` 不加（避免果冻感）。
3. **clip-path 揭示**：内容出现用 `clip-path var(--dur-slow) var(--ease-out)`，比 opacity 渐变更精致（借鉴 academy.claude.com）。
4. **按压微交互**：按钮/卡片 `:active` 用 `transform: scale(.99)`（借鉴 CDS `--cds-card-press-sx`）。
5. **`prefers-reduced-motion` 兜底**：所有动画包进 `@media (prefers-reduced-motion: no-preference)`。

### @keyframes（语义命名，受 reduced-motion 约束）

- `callout-pulse`：callout 出现时极淡 pulse（box-shadow 闪一下）。
- `quiz-feedback`：答题反馈出现（translateY + opacity，配 `--ease-overshoot`）。
- `step-reveal`：步骤列表逐项揭示（clip-path 从上往下扫）。

## Components

teach 课件组件目录（沿用 CSS-CONVENTIONS.md，令牌化后规格）：

| 组件 | 类名 | 关键规格 |
|---|---|---|
| Callout | `.callout` + `.-note/-tip/-warning/-success/-danger` | padding sp-4/sp-5，左 4px 语义色边，radius md |
| Quiz | `.quiz-container > .quiz` + `.-option/-feedback/-score` | option: padding sp-3/4，hover→accent-bg，focus→shadow-focus |
| Compare | `.compare-grid > .compare-card` / `.compare-table` | 并排对比，card 用 radius lg |
| Pipeline | `.pipeline > .pipeline-stage` + `.pipeline-arrow` | 横向流程，stage 用 radius md |
| Flow | `.flow-diagram` + `.flow-box/-arrow/-step/-num` | 流程图，num 用 pill badge |
| Timeline | `.timeline > .timeline-item` | 纵向时间线 |
| Steps | `.step-list`（auto-numbered） | 编号步骤 |
| Architecture | `.arch-layer` + `.arch-arrow` | 分层架构 |
| Matrix | `.matrix-grid > .matrix-cell/-label` | 矩阵/象限 |
| Code | `.code-block` + `.keyword/.string`，`.code-compare` | 代码块，bg code-bg，radius md |
| Formula | `.formula-box` | KaTeX 容器 |
| Tree | `.tree` / `.file-tree` | 文件树/结构树 |
| Card | `.tech-card` + `.tech-badge` | 知识卡，hover→shadow-md + translateY(-1px) |
| Inline | `.badge/.highlight/.label/.tag/.arrow/.ref-link` | 行内元素 |

### 交互态契约（统一）

所有可交互组件（quiz-option / tech-card / callout / ref-link）遵循：

- **hover**：背景/边框色缓动变化（`var(--dur-base) var(--ease-out)`）。
- **focus-visible**：`box-shadow: var(--shadow-focus)`（双层 ring，不依赖 outline）。
- **active**：`transform: scale(.99)`（按压感）。

## Do's and Don'ts

### DO

- 引用令牌（`var(--fs-h2)`、`var(--sp-4)`、`var(--ease-out)`），禁止裸写数值。
- 正文用 serif（`var(--font-voice)`），UI/标题用 sans（`var(--font-ui)`）。
- callout 用语义色 + 配套 `-bg` 浅底，类别一眼可辨。
- transition 多属性同节奏、统一缓动。
- 加 `prefers-reduced-motion` 兜底。

### DON'T

- 裸写 `font-size: 1.05rem` / `padding: 13px`——用令牌。
- 给正文 `p` 加 transition——会变果冻感。
- 用 Anthropic 低饱和自然色做 callout——教学场景需强区分，保留 GitHub 风。
- 照搬 Anthropic 品牌字（Styrene/Tiempos 是商业授权）——teach 用系统字族。
- 用单层硬阴影——用分层柔阴影 token。
- 渐变背景 / drop-shadow 堆叠——破坏 editorial 克制感。
