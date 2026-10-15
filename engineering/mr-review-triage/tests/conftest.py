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


def run_pull(*args, platform="gitlab"):
    """Run ocr-pull-discussions.py against the offline API stub."""
    env = os.environ.copy()
    env["PATH"] = f"{FAKE_BIN}{os.pathsep}{env['PATH']}"
    env["OCR_PLATFORM"] = platform
    env["FAKE_API_ROUTES"] = str(FIXTURES_DIR / platform / "routes.json")
    if platform == "gitlab":
        env["CI_PROJECT_ID"] = "22412"
    else:
        env["GITHUB_REPOSITORY"] = "owner/repo"
    return subprocess.run(
        [sys.executable, str(PULL_SCRIPT), *args],
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )
