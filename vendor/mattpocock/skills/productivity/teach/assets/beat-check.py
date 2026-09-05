#!/usr/bin/env python3
"""beat-check.py — cognitive-progression self-check for teach lessons.

Mechanical half of the Cognitive Progression Self-Check. Extracts the lesson
HTML's visible prose, splits it into candidate beats, and checks the
structural invariants distilled from 52 human master-lesson skeletons
(~/research/teaching-structure/COGNITIVE-PROGRESSION-GUIDE.md):

  1. hook        — the lesson opens with a question or tension, not a definition
  2. callback    — the closing section references the opening hook or an
                   earlier example ("回到开头" / "现在你能解释" patterns)
  3. concrete-first — before the first formula/definition block there is
                   concrete material (numbers, a worked instance, an analogy)
  4. checkpoints — at least one reader-directed question or pause per lesson
  5. example-recall — some example is revisited after abstraction (coarse
                   proxy: an entity named early reappears in the last third)

What this script can NOT see (the human/LLM half of the check): whether the
abstraction ladder actually rises, whether analogies are load-bearing, whether
the hook genuinely creates a "why". Those stay in SKILL.md judgment criteria.

Usage: python3 beat-check.py lessons/0001-xxx.html
Exit 0 = all structural checks pass; exit 1 = findings. A finding is a prompt
to adjudicate, never authorization to edit (same contract as prose-freq-check).
"""

import re
import sys
from pathlib import Path

# question-shaped hook markers (zh + en), within the first 15% of prose
HOOK_PAT = re.compile(r"[？?]|为什么|凭什么|怎么会|问题在于|imagine|what if|why ", re.I)
# formula/formalization markers: KaTeX blocks, definition keywords
FORMAL_PAT = re.compile(r"\\begin\{|\\frac|\\sum|定义如下|形式化地|我们定义|definition:", re.I)
# concrete markers
CONCRETE_PAT = re.compile(r"[0-9]+\.[0-9]+|例如|比如|假设.{0,12}(MB|秒|条|次|个)|worked example|let's say", re.I)
# checkpoint markers
CHECK_PAT = re.compile(r"停下来|想一想|你能|试着|自己试|pause and|check yourself|你会怎么", re.I)
# callback markers in the last 25%
CALLBACK_PAT = re.compile(r"回到开头|回到最初|现在你能|回顾.{0,10}钩子|现在可以解释|还记得.{0,30}吗|回到.{0,12}问题|revisit|back to", re.I)


def visible_text(html: str) -> str:
    html = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    # keep KaTeX visible (formal material matters for concrete-first)
    return re.sub(r"<[^>]+>", " ", html)


def katex_text(html: str) -> str:
    parts = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", html, flags=re.S)
    return " ".join(a or b for a, b in parts)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: beat-check.py <lesson.html>")
        return 2
    html = Path(sys.argv[1]).read_text(encoding="utf-8")
    prose = visible_text(html)
    formal = katex_text(html) + " " + prose
    total = len(prose)
    if total < 300:
        print("SKIP: prose too short for beat analysis")
        return 0

    findings = []

    # 1. hook: question-shaped tension in the first 15%
    head = prose[: max(200, int(total * 0.15))]
    if not HOOK_PAT.search(head):
        findings.append("hook: 开头 15% 内未见问题式张力（？/为什么/imagine）——先定义后动机的典型信号")

    # 2/5. callback: closing ~30% (at least the last 400 chars) references
    # the opening or an early entity
    tail = prose[min(int(total * 0.70), max(0, total - 400)):]
    head_entities = set(re.findall(r"[\u4e00-\u9fff]{2,6}|[A-Za-z][A-Za-z0-9 -]{2,11}|\d+MB|\d+", head[: max(200, int(total * 0.2))]))
    recalled = [e for e in head_entities if e in tail and not re.fullmatch(r"[A-Za-z]{0,2}|我们|这里|它们", e)]
    if not CALLBACK_PAT.search(tail) and not recalled:
        findings.append("callback: 结尾 25% 未回扣开头实体或钩子——例子只用一遍、无第二遍重解的信号")

    # 3. concrete-first: concrete material before the first formalization
    first_formal = FORMAL_PAT.search(formal)
    if first_formal:
        pre = formal[: first_formal.start()]
        if not CONCRETE_PAT.search(pre):
            findings.append("concrete-first: 首个公式/定义前无具体材料（数值/例如/假设实例）——抽象先行的信号")

    # 4. checkpoints
    n_check = len(CHECK_PAT.findall(prose))
    if n_check == 0:
        findings.append("checkpoint: 全文无读者检查点（停下来/想一想/你能）——单向灌输的信号")
    elif total / max(n_check, 1) > 4000:
        findings.append(f"checkpoint: 平均每 {total // max(n_check, 1)} 字才一个检查点——节拍过长（人类教学 1-3 分钟一拍）")

    if findings:
        print(f"BEAT CHECK: {len(findings)} finding(s) in {Path(sys.argv[1]).name}")
        for f in findings:
            print(f"  - {f}")
        print("每条 finding 需就地裁决（保留有理由，或修复），不是零 finding 才交付")
        return 1
    print("BEAT CHECK: all structural checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
