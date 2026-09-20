"""conservation.py — LOST/ADDED detection and structure counts."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "conservation.py"
spec = importlib.util.spec_from_file_location("cons", SCRIPT)
cons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cons)

ORIG = """# 标题

系统处理时间从 120 秒缩短到 40 秒，提升了 `throughput` 约 65%。

"这是引用的原话，「这也是」。用户可能通常在高峰期重试。

| 列一 | 列二 |
|------|------|
| a    | b    |
"""


def test_clean_rewrite_passes():
    new = ORIG.replace("系统处理时间", "系统把处理时间")  # wording-only edit
    r = cons.check(ORIG, new)
    assert r["ok"], r


def test_number_loss_fails():
    new = ORIG.replace("65%", "").replace(" 40 秒", " 45 秒")
    r = cons.check(ORIG, new)
    assert not r["ok"]
    assert "65%" in r["numbers_lost"]


def test_hedge_removal_fails():
    new = ORIG.replace("可能通常", "总是")
    r = cons.check(ORIG, new)
    assert not r["ok"]
    assert "可能" in r["hedges_lost"] and "通常" in r["hedges_lost"]


def test_quote_loss_fails():
    new = ORIG.replace('"这是引用的原话，「这也是」。', "")
    r = cons.check(ORIG, new)
    assert not r["ok"]
    assert r["quotes_lost"]


def test_structure_shrink_fails():
    new = ORIG.split("| a    | b    |")[0] + "\n"
    r = cons.check(ORIG, new)
    assert not r["ok"]
    assert "table_rows" in r["structure_shrunk"]


def test_heading_level_loss_fails():
    new = ORIG.replace("# 标题\n", "\n")
    r = cons.check(ORIG, new)
    assert not r["ok"]
    assert "heading_level_1" in r["structure_shrunk"]


def test_additions_reported_but_not_fatal():
    new = ORIG + "\n补充：延迟 30ms。"
    r = cons.check(ORIG, new)
    assert "30" in r.get("numbers_added", [])
    # additions alone keep ok=True; the fix loop inspects them by adjudication
    assert r["ok"]


def test_en_hedges_tracked():
    orig = "This may fail under load, as users usually retry."
    new = "This fails under load, as users retry."
    r = cons.check(orig, new)
    assert not r["ok"]
    assert set(r["hedges_lost"]) == {"may", "usually"}
