"""Shared runtime.conf loader — replaces 4 per-script copies.

Precedence: env var wins over runtime.conf (unchanged from all 4 copies).
Pure stdlib — importable by any script without pulling aiohttp.
"""
import os
import sys
from pathlib import Path

CONF_PATH = Path(__file__).resolve().parent.parent / "runtime.conf"


def parse_conf_file(path: Path | None = None) -> dict[str, str]:
    """Parse key=value lines; '#' comments and blank lines skipped; quotes stripped."""
    path = path or CONF_PATH
    conf: dict[str, str] = {}
    if not path.is_file():
        return conf
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        conf[k.strip()] = v.strip().strip('"').strip("'")
    return conf


def load_conf(*required: str, keys: tuple[str, ...] = ()) -> dict[str, str]:
    """Load config from env (wins) + runtime.conf; exit loudly on missing required.

    keys: full set to return (default: just *required). Each script passes its
    own key family so unrelated keys never leak between callers.
    """
    file_conf = parse_conf_file()
    wanted = keys or required
    conf = {k: os.environ.get(k) or file_conf.get(k, "") for k in wanted}
    missing = [k for k in required if not conf.get(k)]
    if missing:
        sys.exit(f"FAIL missing config: {missing} (env or runtime.conf)")
    return conf
