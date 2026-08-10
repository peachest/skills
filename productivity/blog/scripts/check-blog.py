#!/usr/bin/env python3
"""Blog style guide checker — programmable checks only.

Usage: python3 check-blog.py <file.md> [<file2.md> ...]
Exit: 0 if all pass, 1 if any fail.
"""
import re
import sys
from pathlib import Path


class CheckResult:
    def __init__(self, name, passed, detail=""):
        self.name = name
        self.passed = passed
        self.detail = detail

    def __str__(self):
        icon = "✅" if self.passed else "❌"
        s = f"  {icon} {self.name}"
        if self.detail:
            s += f" — {self.detail}"
        return s


def check_blog(filepath: Path) -> list[CheckResult]:
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    results = []

    # --- 1. 元信息头 4 字段 blockquote (列表格式) ---
    meta_fields = ["面向", "目的", "信息来源", "调研日期"]
    found_fields = []
    for field in meta_fields:
        if re.search(rf'>\s*-\s*\*\*{field}\*\*[：:]', text):
            found_fields.append(field)
    missing = set(meta_fields) - set(found_fields)
    # also check old format (without -) to flag non-compliance
    old_format = []
    for field in meta_fields:
        if re.search(rf'^>\s*\*\*{field}\*\*[：:]', text, re.MULTILINE):
            if field not in found_fields:
                old_format.append(field)
    if missing:
        results.append(CheckResult("元信息头 4 字段", False, f"缺少: {', '.join(missing)}"))
    elif old_format:
        results.append(CheckResult("元信息头 4 字段", False, f"未用列表格式: {', '.join(old_format)}"))
    else:
        results.append(CheckResult("元信息头 4 字段", True))

    # --- 2. TL;DR 3-5 条带 §跳转 ---
    tldr_match = re.search(r'\*\*TL;DR\*\*', text)
    if not tldr_match:
        results.append(CheckResult("TL;DR 存在", False, "未找到 **TL;DR**"))
    else:
        # find the block after TL;DR until next ---
        tldr_start = tldr_match.end()
        tldr_end = text.find("\n---", tldr_start)
        tldr_block = text[tldr_start:tldr_end] if tldr_end != -1 else text[tldr_start:]
        bullets = re.findall(r'^- .+', tldr_block, re.MULTILINE)
        has_jumps = all("→ [§" in b or "→ [" in b for b in bullets) if bullets else False
        count = len(bullets)
        if count < 3 or count > 5:
            results.append(CheckResult(f"TL;DR 条数 ({count})", False, f"需要 3-5 条，当前 {count}"))
        elif not has_jumps:
            results.append(CheckResult("TL;DR §跳转", False, "部分条目缺少 → [§跳转]"))
        else:
            results.append(CheckResult(f"TL;DR ({count} 条带跳转)", True))

    # --- 3. H2 阿拉伯编号，无中文数字 ---
    h2_lines = [(i, l) for i, l in enumerate(lines) if l.startswith("## ") and not l.startswith("### ")]
    h2_errors = []
    chinese_nums = re.findall(r'##\s+[一二三四五六七八九十百]+、', text)
    if chinese_nums:
        h2_errors.append(f"发现中文数字编号: {chinese_nums[:3]}")
    for i, line in h2_lines:
        title = line[3:].strip()
        # allow "## 附：关键资源" and "## 备选标题" without numbers
        if title.startswith("附：") or title == "备选标题":
            continue
        if not re.match(r'^\d+\.\s', title):
            h2_errors.append(f"L{i+1}: '{title[:30]}' 缺少阿拉伯数字编号")
    if h2_errors:
        results.append(CheckResult("H2 阿拉伯编号", False, "; ".join(h2_errors[:3])))
    else:
        results.append(CheckResult("H2 阿拉伯编号", True))

    # --- 4. H3 父.子编号 ---
    h3_lines = [(i, l) for i, l in enumerate(lines) if l.startswith("### ") and not l.startswith("#### ")]
    h3_errors = []
    for i, line in h3_lines:
        title = line[4:].strip()
        # allow fixed conclusion subsections
        if title in ("核心结论", "建议的下一步", "待讨论的问题"):
            continue
        if not re.match(r'^\d+\.\d+\s', title):
            h3_errors.append(f"L{i+1}: '{title[:30]}' 缺少 N.M 编号")
    if h3_errors:
        results.append(CheckResult("H3 父.子编号", False, "; ".join(h3_errors[:3])))
    else:
        results.append(CheckResult("H3 父.子编号", True))

    # --- 5. 至少 1 个 callout ---
    callout_pattern = re.compile(r'^>\s*\*\*(💡|⚠️|📌)', re.MULTILINE)
    callouts = callout_pattern.findall(text)
    if len(callouts) < 1:
        results.append(CheckResult("Callout (≥1)", False, "未找到 💡/⚠️/📌 callout"))
    else:
        results.append(CheckResult(f"Callout ({len(callouts)})", True))

    # --- 6. 代码块标注语言 ---
    # Find all ``` blocks, check if the opening ``` has a language
    code_blocks = []
    in_code = False
    block_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                block_start = i
                lang = line.strip()[3:].strip()
                if not lang:
                    # could be ASCII art — check if block content looks like a diagram
                    code_blocks.append((i, lang))
            else:
                in_code = False
    # only flag code blocks that have language-detectable content (not ASCII art)
    missing_lang = []
    for start, lang in code_blocks:
        if lang:
            continue
        # check if block content looks like code (has common code patterns)
        block_content = "\n".join(lines[start+1:start+4])
        # ASCII art heuristic: contains box-drawing chars or lots of special chars
        is_ascii_art = any(c in block_content for c in "┌┐└┘├┤┬┴┼─│┌─└─")
        if not is_ascii_art:
            missing_lang.append(start + 1)
    if missing_lang:
        results.append(CheckResult("代码块语言标注", False, f"L{missing_lang[0]} 代码块缺少语言标注"))
    else:
        results.append(CheckResult("代码块语言标注", True))

    # --- 7. 图片有斜体图注 ---
    img_pattern = re.compile(r'^!\[.*\]\(.*\)', re.MULTILINE)
    img_matches = list(img_pattern.finditer(text))
    img_errors = []
    for m in img_matches:
        # find the line after the image
        pos = m.end()
        # skip empty lines
        while pos < len(text) and text[pos] in "\n\r":
            pos += 1
        next_line = text[pos:text.find("\n", pos)] if pos < len(text) else ""
        if not re.match(r'\*图\s*\d+', next_line):
            # get line number
            line_num = text[:m.start()].count("\n") + 1
            img_errors.append(f"L{line_num}")
    if img_errors:
        results.append(CheckResult("图片斜体图注", False, f"缺少图注: {', '.join(img_errors[:3])}"))
    elif not img_matches:
        results.append(CheckResult("图片斜体图注", True, "无图片"))
    else:
        results.append(CheckResult(f"图片图注 ({len(img_matches)})", True))

    # --- 8. 结论章 3 个 H3 子节 ---
    # find last numbered H2
    last_num_h2 = None
    for i, line in enumerate(lines):
        if re.match(r'^##\s+\d+\.\s', line):
            last_num_h2 = (i, line)
    if not last_num_h2:
        results.append(CheckResult("结论章", False, "未找到编号 H2"))
    else:
        # find H3s under this H2 until next H2
        h3s_under = []
        for i in range(last_num_h2[0] + 1, len(lines)):
            if lines[i].startswith("## ") and not lines[i].startswith("### "):
                break
            if lines[i].startswith("### ") and not lines[i].startswith("#### "):
                h3s_under.append(lines[i][4:].strip())
        required = {"核心结论", "建议的下一步", "待讨论的问题"}
        found = set(h3s_under) & required
        missing_h3 = required - found
        if missing_h3:
            results.append(CheckResult("结论章 3 个 H3", False, f"缺少: {', '.join(missing_h3)}"))
        else:
            results.append(CheckResult("结论章 3 个 H3", True))

    # --- 9. 附录标题 ---
    if re.search(r'^##\s*附：关键资源', text, re.MULTILINE):
        results.append(CheckResult("附录标题", True))
    else:
        results.append(CheckResult("附录标题", False, "未找到 '## 附：关键资源'"))

    # --- 10. 备选标题 3-5 条 ---
    alt_match = re.search(r'^##\s*备选标题', text, re.MULTILINE)
    if not alt_match:
        results.append(CheckResult("备选标题", False, "未找到 '## 备选标题'"))
    else:
        # count numbered items after this heading
        pos = alt_match.end()
        end = text.find("\n## ", pos)
        if end == -1:
            end = len(text)
        alt_block = text[pos:end]
        items = re.findall(r'^\d+\.\s', alt_block, re.MULTILINE)
        count = len(items)
        if count < 3 or count > 5:
            results.append(CheckResult(f"备选标题 ({count})", False, f"需要 3-5 条，当前 {count}"))
        else:
            results.append(CheckResult(f"备选标题 ({count} 条)", True))

    return results


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.md> [<file2.md> ...]")
        sys.exit(1)

    all_pass = True
    for arg in sys.argv[1:]:
        filepath = Path(arg)
        if not filepath.exists():
            print(f"❌ 文件不存在: {filepath}")
            all_pass = False
            continue
        print(f"\n{'='*60}")
        print(f"  {filepath.name}")
        print(f"{'='*60}")
        results = check_blog(filepath)
        for r in results:
            print(r)
        fails = [r for r in results if not r.passed]
        if fails:
            all_pass = False
            print(f"\n  → {len(fails)} 项未通过\n")
        else:
            print(f"\n  → 全部通过\n")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
