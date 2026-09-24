"""Tests for the generic adapter (no network): jina parsing, CF detection,
and the shared output-root helper."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
ADAPTERS_DIR = SCRIPTS_DIR / "adapters"

sys.path.insert(0, str(ADAPTERS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR))

import generic  # noqa: E402
import paths  # noqa: E402


JINA_SAMPLE = """Title: OpenAI announces new model
URL Source: https://openai.com/index/example
Markdown Content:

# OpenAI announces new model

Some body text here with [a link](https://example.com).
"""


class TestParseJina:
    def test_parses_title_and_body(self):
        title, body = generic._parse_jina(JINA_SAMPLE)
        assert title == "OpenAI announces new model"
        assert body.startswith("# OpenAI announces new model")
        assert "URL Source:" not in body
        assert "Markdown Content:" not in body

    def test_no_markdown_header_returns_raw(self):
        raw = "Title: T\nURL Source: https://x\n\nplain text body that is long enough"
        title, body = generic._parse_jina(raw)
        assert title == "T"
        assert body == raw.strip()

    def test_empty_body(self):
        title, body = generic._parse_jina("Title: T\nMarkdown Content:\n\n")
        assert body == ""


class TestCfMarkers:
    def test_shell_page_has_markers(self):
        html = "<html><body>Enable JavaScript and cookies to continue</body></html>"
        assert any(m in html for m in generic._CF_MARKERS)

    def test_normal_page_has_no_markers(self):
        html = "<html><body>Hello world article content</body></html>"
        assert not any(m in html for m in generic._CF_MARKERS)


class TestOutputRoot:
    def test_env_override(self, tmp_path, monkeypatch):
        monkeypatch.setenv("FETCH_ARTICLE_TMP_ROOT", str(tmp_path / "custom"))
        root = paths.output_root()
        assert root == tmp_path / "custom"
        assert root.is_dir()

    def test_default_under_home(self, monkeypatch):
        monkeypatch.delenv("FETCH_ARTICLE_TMP_ROOT", raising=False)
        root = paths.output_root()
        assert root == Path.home() / "tmp"

    def test_default_output_dir_placed_under_root(self, tmp_path, monkeypatch):
        monkeypatch.setenv("FETCH_ARTICLE_TMP_ROOT", str(tmp_path))
        d = paths.default_output_dir("fetch-test-")
        assert Path(d).is_dir()
        assert Path(d).parent == tmp_path
        assert Path(d).name.startswith("fetch-test-")
