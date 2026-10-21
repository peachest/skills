---
name: terminal-screenshot
description: Generate terminal-style screenshots of real command output for reports, evidence, or customer demos using freeze — one command per image, real kubectl/shell output only, no summaries. Use when the user asks to 截图/截图留痕/生成终端截图/terminal screenshot, when report evidence must look like real terminal output, or when a headless node (no DISPLAY) needs command-output images. Also fires for fixing cut-off or truncated terminal images (右侧裁切/太窄).
---

# Terminal Screenshot（freeze 工具链）

目标：给报告/客户演示生成**看起来像真实终端**的命令输出截图。本节点（<node-a>）无 DISPLAY，走 freeze SVG → Playwright PNG 两段。

## 铁律：证据截图必须真实（用户不会信摘要）

1. **一图一命令一输出**：每张截图只放一个命令及其真实输出。不拼接多段（拼接图又长又宽，客户看不懂）；不做人工摘要/改写（`"高分域: 0-3 两两 100"` 这种描述性文字一眼假）。
2. **先跑真命令，抓 raw 原文**：把每个用例的真实输出（`kubectl ... -o yaml | python3 -m json.tool` 等）原样存 `*-raw.txt`。截图从 raw 生成，raw 与截图逐字可比对——这是可信度保障。
3. **允许的截断只有一种**：超长输出用真实管道截断（如 `| sed -n '/score:/,$p' | head -20`），截断发生在**命令管道里**（截图内容仍是真实命令行为），且图上注明"完整见 <文件>"并附完整文件。
4. **核心对照并排**：如果有"同一输入不同配置→不同输出"的对照（如拓扑 profile 切换），单独成对引用两张图，不合成一张。

## 工具链

```bash
# 安装位置: ~/.local/bin/freeze（单文件二进制）
# 基本用法: raw 原文 → SVG（终端窗口样式）
freeze --window --language bash -o out.svg < raw.txt
# SVG → PNG（报告/Word 嵌入用）
node ~/tools/playwright-runner/svg2png.mjs out.svg out.png
```

## 三个已踩的坑（必读）

1. **PNG 后端 panic**：v0.2.2 的 PNG 输出在 headless 无字体栈节点上直接 panic（goroutine dump）。**永远输出 SVG**，再走 `~/tools/playwright-runner/svg2png.mjs` 转 PNG。该脚本需在 playwright-runner 目录内运行（依赖其 node_modules）。
2. **`--width` 是像素不是字符列**：传 `--width 160` 会把图设成 160px 宽，正文右侧全部被裁。**不传 `--width`**，freeze 按最长行自适应宽度。宽 JSON（几百列）出宽图是正常的，信息完整优先于好看；客户嫌宽给 raw txt。
3. **版本**：GitHub `releases/latest` 是 v0.2.2（不是 1.2.0），tar 包内层目录是 `freeze_<ver>_Linux_x86_64/freeze`，解压后二进制在子目录里。

## SVG→PNG 的坑

- `svg2png.mjs` 必须用**绝对路径**传 SVG（相对路径 `file://` 解析失败 ERR_INVALID_URL）
- 截 `locator('svg').first()`（外层带尺寸的），`.last()` 会截到内层 49×12 小图；`fullPage: true` 会 fonts 超时——都已固定在脚本里
- 脚本位置：`~/tools/playwright-runner/svg2png.mjs`（丢了按 skill 说重建：chromium.launch({args:['--no-sandbox']}) + goto file:// + svg.first().screenshot）

## 批量流程（对照实验类证据）

1. 每个用例跑真命令，`<case>-raw.txt` 落盘
2. `freeze --window --language bash -o <case>.svg < <case>-raw.txt`
3. `node ~/tools/playwright-runner/svg2png.mjs <abs>.svg <abs>.png`
4. 自检脚本三查（`scripts/shot-verify.sh <dir> <expectations-file>`，退出码 0/1）：**宽度**（SVG width >= 最长行×6.6px 预算，抓像素误用裁切；实测能抓 160px 坏图）、**完整性**（expectations 文件逐行 `<png名> <数量> <UUID...>` 核关键 UUID 在场）、**一致性**（PNG 与 SVG 重渲染 cmp，抓陈旧交付包）。expectations 生成方式：从各用例 raw 原文 grep UUID 集合拼出。
5. 交付包随最新图同步：改图后重刷下载目录/tar（三查的第 3 查即为此设计，md5/cmp 比对 canonical 源，不要肉眼）
