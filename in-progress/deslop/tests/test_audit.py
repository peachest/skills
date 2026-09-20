"""audit.py — rule-hit, language-routing, and verdict tests."""

import importlib.util
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "audit.py"
spec = importlib.util.spec_from_file_location("audit", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def hits_by_rule(report):
    d = {}
    for f in report["flags"]:
        d.setdefault(f["rule"], []).append(f)
    return d


def test_zh_rules_fire():
    doc = """
真正的壁垒不是技术，而是认知。这明明说得通：采集、存储、展示，一条龙。

答案是：专注。——种稀缺品不好说。值得注意的是，这个方法很好。

对于早期团队来说，招人是最难的。
然而，成本也很高。

这听起来像一条功能描述。说白了，预算不足。

看起来很简单，做起来难。

他就像一位智慧的导师。新系统实现了效率的提升。
"""
    r = audit.audit_text(doc)
    h = hits_by_rule(r)
    assert "ZH-1" in h          # 不是…而是
    assert "ZH-2" in h          # 采集、存储、展示
    assert "ZH-4" in h          # ——
    assert "ZH-5" in h          # 答案：
    assert "ZH-8" in h          # 效率的提升
    assert "ZH-9" in h          # 说白了
    assert "ZH-10b" in h        # 对于…来说
    assert "ZH-10c" in h        # 然而，
    assert "ZH-11" in h         # 段首零主语（这听起来 是回指 → 不会命中，但 听起来 句缺回指会）
    assert "ZH-7" in h          # 像一位智慧的导师


def test_zh_referring_paragraph_not_flagged():
    doc = "上一段说了配置。\n\n这听起来像一条功能描述，其实不是。"
    r = audit.audit_text(doc)
    assert "ZH-11" not in hits_by_rule(r)


def test_zh6_needs_three_consecutive_numbered_headings():
    two = "## 一、甲\n\ntext\n\n## 二、乙\n\ntext"
    assert audit.numbered_heading_run(two) == []
    three = "## 一、甲\n\ntext\n\n## 二、乙\n\ntext\n\n## 三、丙\n\ntext"
    assert len(audit.numbered_heading_run(three)) == 1  # flags from the 3rd onward


def test_zh5b_idle_colon_needs_list_below():
    with_list = "我见过的几种典型场景：\n\n- 场景甲\n- 场景乙"
    r = audit.audit_text(with_list)
    assert "ZH-5b" in hits_by_rule(r)
    without_list = "我见过的几种典型场景：\n\n具体见下文分析。"
    assert "ZH-5b" not in hits_by_rule(audit.audit_text(without_list))


def test_code_blocks_masked():
    doc = "```\nnot code —— but inside a fence\n```\n\n正文这里没有破折号。"
    r = audit.audit_text(doc)
    assert "ZH-4" not in hits_by_rule(r)


def test_en_rules_fire():
    doc = """
This design is seamless and robust. You may spin up a cluster in one command;
the dashboard makes a decision for you. It was a cutting-edge — really an
effortless — rollout, and teams reach out to us about it.
"""
    r = audit.audit_text(doc)
    h = hits_by_rule(r)
    assert "EN-2" in h      # semicolon
    assert "EN-3" in h      # may
    assert "EN-4" in h      # seamless/robust/cutting-edge
    assert "EN-5" in h      # spin up / reach out
    assert "EN-6" in h      # makes a decision
    assert "EN-7" in h      # em-dash


def test_en1_sentence_length_mode():
    sent = "The system " + "provides data " * 6 + "today."  # 15 words
    long = "The system " + "provides data " * 8 + "today."  # 19 words
    assert audit.audit_text(sent)["flags"] == []
    flavor = audit.audit_text(long, mode="flavor")
    strict = audit.audit_text(long, mode="strict")
    assert "EN-1" not in hits_by_rule(flavor)   # 19 words: passes 25, fails 20? no — 19 <= 20
    assert "EN-1" not in hits_by_rule(strict)
    longer = "The system " + "provides data " * 12 + "today."  # 27 words
    assert "EN-1" in hits_by_rule(audit.audit_text(longer, mode="flavor"))


def test_mixed_document_routes_by_paragraph():
    doc = "这一段是中文，说的是端侧部署的取舍。\n\nThis paragraph is pure English prose about deployment tradeoffs."
    r = audit.audit_text(doc)
    langs = {f["lang"] for f in r["flags"]}
    assert langs <= {"zh", "en"}
    # no cross-language rule leakage: zh-only rules never fire on the en paragraph
    zh_only = {f for f in r["flags"] if f["rule"].startswith("ZH")}
    assert all(f["lang"] == "zh" for f in zh_only)


def test_verdict_floor():
    clean = "这一段文字没有任何问题，句句平实，材料扎实，读来清爽。" * 3
    r = audit.audit_text(clean)
    assert r["verdict"].startswith("skip")


def test_dash_density_guard():
    # many dashes spread over few prose lines -> rewrite-warranted even if
    # individual hits stay under the floor via per-100-sentence score
    doc = "\n".join(f"要点{i}——说明{i}" for i in range(12))
    r = audit.audit_text(doc)
    assert r["verdict"] == "rewrite-warranted"


def test_midfile_divider_not_frontmatter():
    # regression: a --- divider between header and body must not mask the body
    doc = "| 字段 | 值 |\n|---|---|\n\n---\n\n正文说：这不是而是那不是。'"
    r = audit.audit_text(doc)
    assert "ZH-1" in hits_by_rule(r)


def test_leading_frontmatter_masked():
    doc = "---\ntitle: x\n---\n\n正文没有触发词。"
    r = audit.audit_text(doc)
    assert r["flags"] == []
