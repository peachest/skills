"""CLI-level harness for mr-review-triage script tests.

Single test seam per spec #57: tests invoke the real script as a subprocess;
the platform API is replaced by offline fixtures served through fake curl/gh
binaries placed first on PATH. No network, no secrets.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TESTS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = TESTS_DIR / "fixtures"
FAKE_BIN = TESTS_DIR / "fake_bin"

PULL_SCRIPT = SKILL_DIR / "scripts" / "ocr-pull-discussions.py"
POST_SCRIPT = SKILL_DIR / "scripts" / "ocr-post-labels.py"
VERDICT_SCRIPT = SKILL_DIR / "scripts" / "verdict.py"
VERIFY_SCRIPT = SKILL_DIR / "scripts" / "ocr-verify-resolved.py"


def _stub_env(platform, routes=None):
    """Env for a subprocess run against the offline API stub.

    routes: explicit route-table path. Pipeline-status tests bring their own
    per-state table because the GitLab pipeline status lives in the same
    MR-detail response the gate queries.
    """
    env = os.environ.copy()
    env["PATH"] = f"{FAKE_BIN}{os.pathsep}{env['PATH']}"
    env["OCR_PLATFORM"] = platform
    env["FAKE_API_ROUTES"] = str(
        routes or (FIXTURES_DIR / platform / "routes.json"))
    if platform == "gitlab":
        env["CI_PROJECT_ID"] = "22412"
    else:
        env["GITHUB_REPOSITORY"] = "owner/repo"
    return env

# ocr_platform (underscore name) is importable directly for unit-level checks
# of the exported triage_state_dir helper; hyphen-named scripts stay subprocess-only.
sys.path.insert(0, str(SKILL_DIR / "scripts"))


def run_pull(*args, platform="gitlab", routes=None, cwd=None):
    """Run ocr-pull-discussions.py against the offline API stub."""
    return subprocess.run(
        [sys.executable, str(PULL_SCRIPT), *args],
        capture_output=True,
        text=True,
        env=_stub_env(platform, routes),
        timeout=60,
        cwd=cwd,
    )


def run_verify(*args, platform="gitlab", routes=None, cwd=None):
    """Run ocr-verify-resolved.py against the offline API stub.

    cwd matters for the default pull state file — triage_state_dir() derives
    .triage/<MR>/issues.json from the working directory.
    """
    return subprocess.run(
        [sys.executable, str(VERIFY_SCRIPT), *args],
        capture_output=True,
        text=True,
        env=_stub_env(platform, routes),
        timeout=60,
        cwd=cwd,
    )


def run_post(*args, stdin_text="", platform="gitlab", api_log=None):
    """Run ocr-post-labels.py against the offline API stub.

    stdin_text is the payload for the stdin transport; --classified tests
    pass the state file via args instead. GitLab post tests serve the
    post_routes table (canned reply/resolve/sweep responses). When api_log
    (a path) is given, every fake-API request is journaled there as JSON
    lines so tests can assert call absence and posted bodies.
    """
    env = os.environ.copy()
    env["PATH"] = f"{FAKE_BIN}{os.pathsep}{env['PATH']}"
    env["OCR_PLATFORM"] = platform
    routes = "post_routes.json" if platform == "gitlab" else "routes.json"
    env["FAKE_API_ROUTES"] = str(FIXTURES_DIR / platform / routes)
    if api_log is not None:
        env["FAKE_API_LOG"] = str(api_log)
    if platform == "gitlab":
        env["CI_PROJECT_ID"] = "22412"
    else:
        env["GITHUB_REPOSITORY"] = "owner/repo"
    return subprocess.run(
        [sys.executable, str(POST_SCRIPT), *args],
        input=stdin_text,
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )


def run_verdict(*args):
    """Run verdict.py — pure local state script; touches no platform API."""
    return subprocess.run(
        [sys.executable, str(VERDICT_SCRIPT), *args],
        capture_output=True,
        text=True,
        timeout=60,
    )


def read_api_log(path):
    """Return journaled fake-API calls as dicts; missing log = zero calls."""
    try:
        with open(path) as f:
            return [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        return []
