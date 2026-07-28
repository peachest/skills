/**
 * KaTeX Auto-Render — 声明式公式渲染
 *
 * Usage: 在 lesson 的 <head> 或 <body> 末尾引入:
 *   <link rel="stylesheet" href="../assets/katex.min.css">
 *   <script src="../assets/katex.min.js" defer></script>
 *   <script src="../assets/auto-render.min.js" defer></script>
 *   <script src="../assets/render.js" defer></script>
 *
 * 支持的定界符:
 *   $$...$$  → display math (块级,居中)
 *   $...$    → inline math (行内)
 *
 * 在正文中用 $ 包裹 LaTeX 公式即可,auto-render 自动扫描并渲染。
 */

document.addEventListener("DOMContentLoaded", function () {
  if (typeof renderMathInElement !== "function") return;

  renderMathInElement(document.body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false },
    ],
    throwOnError: false,
    ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
    ignoredClasses: ["no-math"],
  });
});
