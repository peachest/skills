"""Zhihu adapter tests — routing, script presence, error paths (no browser)."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def test_classify_url_routes_zhihu():
    import fetch

    assert fetch.classify_url("https://zhuanlan.zhihu.com/p/2054242266215084545") == "zhihu"
    assert fetch.classify_url("https://ZHUILAN.zhihu.com/p/1".replace("ZHUILAN", "zhuanlan")) == "zhihu"
    # non-article zhihu URLs stay generic
    assert fetch.classify_url("https://www.zhihu.com/question/123") == "generic"


def test_adapter_module_loads():
    import adapters.zhihu as zhihu

    assert callable(zhihu.fetch)


def test_fetch_rejects_non_article_url(tmp_path):
    import adapters.zhihu as zhihu

    result = zhihu.fetch("https://www.zhihu.com/question/123", output_dir=str(tmp_path))
    assert "error" in result and "zhuanlan" in result["error"]


def test_fetch_errors_without_cookie_file(tmp_path, monkeypatch):
    import adapters.zhihu as zhihu

    monkeypatch.setenv("ZHIHU_COOKIE_FILE", str(tmp_path / "nope.txt"))
    result = zhihu.fetch("https://zhuanlan.zhihu.com/p/123", output_dir=str(tmp_path))
    assert "error" in result and "cookie" in result["error"]


def test_fetch_mjs_exists():
    mjs = SCRIPTS_DIR / "adapters" / "zhihu_fetch.mjs"
    assert mjs.exists()
    text = mjs.read_text()
    # the three known-failure signatures must be guarded
    assert "40362" in text
    assert "安全验证" in text
