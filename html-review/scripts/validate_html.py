#!/usr/bin/env python3
"""验证 HTML 文件的结构完整性。

用法:
  python3 <skill_dir>/scripts/validate_html.py <file>         # 基础校验
  python3 <skill_dir>/scripts/validate_html.py --strict <file> # 含 html5lib 严格解析

校验项:
  - DOCTYPE, <html>, <head>, <body>, <title>
  - charset meta
  - 重复 id
  - 标签闭合（lxml vs html.parser 交叉验证）
  - 外链资源
  - 内联事件处理器
  - [--strict] html5lib HTML5 规范解析（检出 & 未转义实体等）
  - [--strict] VNU 离线 Jar (vnu.jar) W3C Nu Checker if available
"""

import sys
import os
import re
from html.parser import HTMLParser


class TagCountParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.ids = []
        self.urls = {"script": [], "style": []}

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attrs_dict = dict(attrs)
        if "id" in attrs_dict:
            self.ids.append(attrs_dict["id"])
        if tag == "script" and "src" in attrs_dict:
            self.urls["script"].append(attrs_dict["src"])
        if tag == "link" and attrs_dict.get("rel") == "stylesheet":
            self.urls["style"].append(attrs_dict.get("href", ""))


def check_html5lib(path):
    """html5lib 严格解析，按 HTML5 规范检出语法违规。"""
    errors = []
    try:
        import html5lib
        from html5lib import html5parser

        parser = html5parser.HTMLParser()
        with open(path, "rb") as f:
            parser.parse(f)
        for e in parser.errors:
            lineno, col = e[0] if len(e) > 0 else (0, 0)
            msg = e[1] if len(e) > 1 else "unknown"
            params = e[2] if len(e) > 2 else {}
            desc = {
                "expected-named-entity": "URL 中 & 未转义为 &amp;",
            }.get(msg, msg)
            errors.append(
                f"  L{lineno}:{col} [{msg}] {desc}"
                + (f" {params}" if params else "")
            )
        if not errors:
            print("  html5lib: ✅ HTML5 规范解析通过，无违规")
    except ImportError:
        print("  html5lib: ⚠️ 未安装 (pip install html5lib)")
    except Exception as e:
        errors.append(f"  html5lib 异常: {e}")
    return errors


def check_vnu(path):
    """W3C Nu Checker (vnu.jar). 查找 vnu.jar 在常见位置。"""
    candidates = [
        os.path.expanduser("~/.vnu/vnu.jar"),
        "/usr/local/share/vnu/vnu.jar",
        "/opt/vnu/vnu.jar",
        os.path.join(os.path.dirname(__file__), "vnu.jar"),
    ]
    jar = None
    for c in candidates:
        if os.path.isfile(c):
            jar = c
            break
    if not jar:
        print("  VNU: ⚠️ 未找到 vnu.jar（可下载到 ~/.vnu/vnu.jar）")
        return []

    import subprocess

    try:
        r = subprocess.run(
            ["java", "-jar", jar, "--format", "text", path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        out = (r.stdout or "") + (r.stderr or "")
        lines = [l for l in out.splitlines() if l.strip()]
        if not lines:
            print("  VNU: ✅ W3C 标准校验通过")
        else:
            print(f"  VNU: ⚠️ {len(lines)} 条警告/错误")
            return lines[:20]
    except FileNotFoundError:
        print("  VNU: ⚠️ java 未安装")
    except subprocess.TimeoutExpired:
        print("  VNU: ⚠️ 超时 (30s)")
    except Exception as e:
        print(f"  VNU: ⚠️ {e}")
    return []


def validate(path, strict=False):
    with open(path, "rb") as f:
        raw = f.read()

    text = raw.decode("utf-8")
    errors = []

    # ── 1. DOCTYPE ──
    if raw[:15] != b"<!DOCTYPE html>":
        errors.append("缺少或错误的 DOCTYPE（期望 <!DOCTYPE html>）")

    # ── 2. 标准库解析 ──
    parser = TagCountParser()
    parser.feed(text)

    # ── 3. 基础结构 ──
    head_count = sum(1 for t in parser.tags if t == "head")
    if head_count == 0:
        errors.append("缺少 <head>")
    elif head_count > 1:
        errors.append(f"多个 <head> ({head_count})")
    body_count = sum(1 for t in parser.tags if t == "body")
    if body_count == 0:
        errors.append("缺少 <body>")
    elif body_count > 1:
        errors.append(f"多个 <body> ({body_count})")

    # ── 4. title / charset ──
    if "title" not in parser.tags:
        errors.append("缺少 <title>")
    lower = text.lower()
    has_charset = (
        '<meta charset="utf-8"' in lower
        or '<meta charset="UTF-8"' in text
        or 'meta charset=utf-8' in lower
    )
    if not has_charset:
        errors.append("缺少 charset meta")

    # ── 5. 重复 id ──
    seen = {}
    dups = []
    for id_val in parser.ids:
        if id_val in seen:
            dups.append(id_val)
        seen[id_val] = True
    if dups:
        errors.append(f"重复 id: {sorted(set(dups))}")

    # ── 6. 标签闭合（lxml 交叉验证） ──
    try:
        from lxml import etree

        lxml_count = sum(1 for _ in etree.iterparse(path, html=True))
        hp_count = len(parser.tags)
        if lxml_count != hp_count:
            print(
                f"  ⚠️  lxml 元素数 ({lxml_count}) ≠ html.parser ({hp_count})，"
                f"可能有未闭合标签"
            )
        print(f"  元素数: {lxml_count if lxml_count else hp_count}")
    except ImportError:
        print(f"  元素数: {len(parser.tags)}（html.parser）")

    # ── 7. 外链资源 ──
    print(f"  外链 script: {len(parser.urls['script'])}")
    for u in parser.urls["script"]:
        print(f"    {u}")
    print(f"  外链样式表: {len(parser.urls['style'])}")
    for u in parser.urls["style"]:
        print(f"    {u}")

    # ── 8. 内联事件处理器 ──
    inline_count = len(re.findall(r"\bon\w+\s*=\s*[\"']", text, re.I))
    print(f"  内联事件处理器: {inline_count}")

    # ── 9. html5lib 严格校验（--strict） ──
    if strict:
        print()
        print("── html5lib HTML5 规范解析 ──")
        hl_errors = check_html5lib(path)
        if hl_errors:
            errors.append("html5lib 发现违规")
            for e in hl_errors:
                print(e)

        # ── 10. VNU W3C Nu Checker（--strict，自动检测 vnu.jar） ──
        print()
        print("── VNU W3C 标准校验 ──")
        vnu_issues = check_vnu(path)
        if vnu_issues:
            print("\n".join(vnu_issues[:10]))
            if len(vnu_issues) > 10:
                print(f"  ... 还有 {len(vnu_issues)-10} 条")

    # 输出
    print()
    if errors:
        print("❌ 发现问题:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("✅ 结构正常")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(1)
    strict = "--strict" in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    for f in files:
        if len(files) > 1:
            print(f"══ {f} ══")
        ok = validate(f, strict=strict)
        if len(files) > 1:
            print()
    sys.exit(0 if ok else 1)