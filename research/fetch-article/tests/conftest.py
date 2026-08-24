"""Shared fixtures for fetch-article test suite."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def nav_response() -> dict:
    return _load_json(FIXTURES_DIR / "nav.json")


@pytest.fixture
def view_response() -> dict:
    return _load_json(FIXTURES_DIR / "view.json")


@pytest.fixture
def playurl_response() -> dict:
    return _load_json(FIXTURES_DIR / "playurl.json")


@pytest.fixture
def player_v2_response() -> dict:
    return _load_json(FIXTURES_DIR / "player_v2.json")
