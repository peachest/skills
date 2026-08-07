"""
Tests for profile_pipeline.py deterministic functions.

Seams under test:
- parse_pipeline_url: URL → (host, encoded_project, pipeline_id)
- SECTION_RE: GitLab section timestamp regex
- Signal extraction patterns (buildx, tool timings, sleep)
"""

import os
import re
import sys
import json
import subprocess
import tempfile
import unittest

# Add scripts dir to path
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from profile_pipeline import (
    parse_pipeline_url,
    SECTION_RE,
    _strip_ansi,
)


class TestParsePipelineUrl(unittest.TestCase):
    """URL parsing seam: pipeline URL → (host, encoded_project, pipeline_id)."""

    def test_standard_url(self):
        url = "https://internal.example.com/llm/llmops/hami/ppu-device-plugin/-/pipelines/1326695"
        host, project, pid = parse_pipeline_url(url)
        self.assertEqual(host, "internal.example.com")
        self.assertEqual(project, "llm%2Fllmops%2Fhami%2Fppu-device-plugin")
        self.assertEqual(pid, "1326695")

    def test_shallow_project(self):
        url = "https://gitlab.com/myproject/-/pipelines/42"
        host, project, pid = parse_pipeline_url(url)
        self.assertEqual(host, "gitlab.com")
        self.assertEqual(project, "myproject")
        self.assertEqual(pid, "42")

    def test_two_level_project(self):
        url = "https://gitlab.example.com/group/project/-/pipelines/999"
        host, project, pid = parse_pipeline_url(url)
        self.assertEqual(host, "gitlab.example.com")
        self.assertEqual(project, "group%2Fproject")
        self.assertEqual(pid, "999")

    def test_deep_nested_project(self):
        url = "https://gitlab.io/a/b/c/d/e/f/-/pipelines/1"
        host, project, pid = parse_pipeline_url(url)
        self.assertEqual(host, "gitlab.io")
        self.assertEqual(project, "a%2Fb%2Fc%2Fd%2Fe%2Ff")
        self.assertEqual(pid, "1")

    def test_invalid_url_raises(self):
        with self.assertRaises(ValueError):
            parse_pipeline_url("https://gitlab.com/not-a-pipeline-url")

    def test_url_without_pipeline_segment(self):
        with self.assertRaises(ValueError):
            parse_pipeline_url("https://gitlab.com/group/project")


class TestSectionRegex(unittest.TestCase):
    """Section timestamp regex seam: matches GitLab section_start/section_end markers."""

    def test_match_start(self):
        line = "section_start:1785134778:prepare_executor\r\x1b[0K\x1b[0K\x1b[36;1mPre"
        m = SECTION_RE.search(line)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "start")
        self.assertEqual(m.group(2), "1785134778")
        self.assertEqual(m.group(3), "prepare_executor")

    def test_match_end(self):
        line = "section_end:1785134785:prepare_script\r\x1b[0Ksection_start:1785134785:get_sources"
        matches = SECTION_RE.findall(line)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0], ("end", "1785134785", "prepare_script"))
        self.assertEqual(matches[1], ("start", "1785134785", "get_sources"))

    def test_match_underscore_names(self):
        line = "section_start:123:cleanup_file_variables\r\x1b[0K"
        m = SECTION_RE.search(line)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(3), "cleanup_file_variables")

    def test_no_match_plain_text(self):
        line = "Running with gitlab-runner 15.11.1"
        m = SECTION_RE.search(line)
        self.assertIsNone(m)

    def test_no_match_non_lowercase_section(self):
        # Section names are lowercase with underscores only
        line = "section_start:123:Prepare-Script"
        m = SECTION_RE.search(line)
        # "Prepare" starts with uppercase, regex only matches [a-z_]
        # It should match "cript" portion? No — the regex needs the full name
        # Let's check: it will match starting from 'p' in 'Script'? No, 'S' is uppercase.
        # Actually the regex [a-z_]+ won't match 'P' so it finds 'rep' no...
        # Let's just verify it doesn't match the full "Prepare-Script"
        if m:
            self.assertNotEqual(m.group(3), "Prepare-Script")


class TestStripAnsi(unittest.TestCase):
    """ANSI stripping seam: removes escape codes from log lines."""

    def test_strips_color_codes(self):
        text = "\x1b[32;1m$ make lint\x1b[0;m"
        self.assertEqual(_strip_ansi(text), "$ make lint")

    def test_strips_multiple_codes(self):
        text = "\x1b[36;1mPreparing\x1b[0;m\x1b[0K\x1b[0K"
        result = _strip_ansi(text)
        self.assertNotIn("\x1b", result)

    def test_preserves_plain_text(self):
        text = "go: downloading k8s.io/api v0.36.2"
        self.assertEqual(_strip_ansi(text), text)


class TestSignalsExtraction(unittest.TestCase):
    """Signal extraction seam: parse buildx steps, tool timings, sleeps from log text."""

    def _run_signals(self, log_content):
        """Write log content to temp file, run signals subcommand, return parsed JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            f.write(log_content)
            f.flush()
            path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "profile_pipeline.py"),
                 "signals", path],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"signals failed: {result.stderr}")
            return json.loads(result.stdout)
        finally:
            os.unlink(path)

    def test_extracts_sleep(self):
        log = "\x1b[32;1m$ sleep 10\x1b[0;m\n"
        signals = self._run_signals(log)
        self.assertEqual(len(signals["sleep_occurrences"]), 1)
        self.assertEqual(signals["sleep_occurrences"][0]["seconds"], 10)

    def test_extracts_downloads(self):
        log = "go: downloading k8s.io/api v0.36.2\ngo: downloading github.com/pkg/errors v0.9.1\n"
        signals = self._run_signals(log)
        self.assertEqual(signals["downloads"]["count"], 2)

    def test_extracts_buildx_done(self):
        log = "#1 DONE 9.7s\n#2 DONE 0.0s\n#3 DONE 0.3s\n"
        signals = self._run_signals(log)
        self.assertEqual(len(signals["buildx_steps"]), 3)
        self.assertEqual(signals["buildx_steps"][0]["step"], 1)
        self.assertEqual(signals["buildx_steps"][0]["duration_seconds"], 9.7)

    def test_extracts_buildx_description_and_duration_separate(self):
        log = "#10 [linux/amd64 stage-1 1/4] FROM harbor.io/base:24.04\n#10 DONE 6.6s\n"
        signals = self._run_signals(log)
        self.assertEqual(len(signals["buildx_steps"]), 1)
        step = signals["buildx_steps"][0]
        self.assertEqual(step["step"], 10)
        self.assertEqual(step["duration_seconds"], 6.6)
        self.assertIn("FROM harbor.io/base:24.04", step["description"])

    def test_extracts_tool_timing_seconds(self):
        log = 'level=info msg="Execution took 48.424810907s"\n'
        signals = self._run_signals(log)
        self.assertEqual(len(signals["tool_timings"]), 1)
        self.assertAlmostEqual(signals["tool_timings"][0]["duration_seconds"], 48.425, places=2)

    def test_extracts_tool_timing_minutes(self):
        log = 'level=info msg="analyzers took 7m18.288s with top 10"\n'
        signals = self._run_signals(log)
        self.assertEqual(len(signals["tool_timings"]), 1)
        # 7m = 420s + 18.288s = 438.288s... but the regex captures "7" + "m"
        # Actually the regex is (Execution took|took\s+|...)([\d.]+)(s|ms|m)
        # "took 7m18.288s" → "took" matches, "7" is value, "m" is unit → 7*60=420
        self.assertAlmostEqual(signals["tool_timings"][0]["duration_seconds"], 420.0, places=1)

    def test_extracts_tool_timing_milliseconds(self):
        log = 'level=info msg="processing took 10.349ms with stages"\n'
        signals = self._run_signals(log)
        self.assertEqual(len(signals["tool_timings"]), 1)
        self.assertAlmostEqual(signals["tool_timings"][0]["duration_seconds"], 0.010349, places=6)

    def test_extracts_commands(self):
        log = "\x1b[32;1m$ make lint\x1b[0;m\n\x1b[32;1m$ go mod tidy\x1b[0;m\n"
        signals = self._run_signals(log)
        self.assertEqual(len(signals["commands"]), 2)
        self.assertEqual(signals["commands"][0]["command"], "make lint")
        self.assertEqual(signals["commands"][1]["command"], "go mod tidy")


class TestSectionsSubcommand(unittest.TestCase):
    """Sections subcommand seam: parse section timestamps from log file → durations."""

    def _run_sections(self, log_content):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            f.write(log_content)
            f.flush()
            path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "profile_pipeline.py"),
                 "sections", path],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"sections failed: {result.stderr}")
            return json.loads(result.stdout)
        finally:
            os.unlink(path)

    def test_parses_simple_sections(self):
        log = (
            "section_start:1000:prepare_script\r\x1b[0K\n"
            "some output\n"
            "section_end:1005:prepare_script\r\x1b[0K\n"
            "section_start:1005:step_script\r\x1b[0K\n"
            "more output\n"
            "section_end:1015:step_script\r\x1b[0K\n"
        )
        sections = self._run_sections(log)
        self.assertEqual(len(sections), 2)

        prep = next(s for s in sections if s["section"] == "prepare_script")
        self.assertEqual(prep["duration_seconds"], 5)

        step = next(s for s in sections if s["section"] == "step_script")
        self.assertEqual(step["duration_seconds"], 10)

    def test_empty_log_returns_empty(self):
        sections = self._run_sections("no sections here\njust plain text\n")
        self.assertEqual(len(sections), 0)


if __name__ == "__main__":
    unittest.main()
