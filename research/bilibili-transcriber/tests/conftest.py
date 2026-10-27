"""Shared fixtures for bilibili-transcriber test suite."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Scripts import shared modules (_conf, _llm) from their own directory;
# spec_from_file_location-loaded script modules need that dir on sys.path.
import sys
sys.path.insert(0, str(SCRIPTS_DIR))
