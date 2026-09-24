"""Shared output-path helpers for fetch-article scripts.

All temp artifacts live under FETCH_ARTICLE_TMP_ROOT (default: ~/tmp),
never /tmp — /tmp sits on the root disk and can trigger disk-pressure
eviction on k8s nodes.
"""

import os
import tempfile
from pathlib import Path


def output_root() -> Path:
    """Return the base directory for fetch-article temp artifacts."""
    root = os.environ.get("FETCH_ARTICLE_TMP_ROOT", "").strip()
    base = Path(root).expanduser() if root else Path.home() / "tmp"
    base.mkdir(parents=True, exist_ok=True)
    return base


def default_output_dir(prefix: str) -> str:
    """Create and return a unique output dir under output_root()."""
    return tempfile.mkdtemp(prefix=prefix, dir=str(output_root()))
