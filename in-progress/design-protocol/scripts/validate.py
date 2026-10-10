#!/usr/bin/env python3
"""Gate for design-protocol: validate protocol files against their layer schemas.

Usage:
  validate.py <protocol-dir>          # e.g. design/protocol/
  validate.py --self-test             # run built-in samples, exit 0 iff gate works
Exit codes: 0 all pass, 1 violations found, 2 setup/usage error.
"""
import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("FAIL: python3 -m pip install jsonschema", file=sys.stderr)
    sys.exit(2)

SKILL_DIR = Path(__file__).resolve().parent.parent
SCHEMA_DIR = SKILL_DIR / "schemas"

# file basename -> schema file (basename may carry suffixes: tokens.json, components/button.json)
LAYER_MAP = [
    (r"^tokens.*\.json$", "l1-tokens.schema.json"),
    (r"^l1.*\.json$", "l1-tokens.schema.json"),
    (r"^l2.*\.json$", "l2-component.schema.json"),
    (r"^l3.*\.json$", "l3-direction.schema.json"),
    (r"^l4.*\.json$", "l4-scene.schema.json"),
    (r"^l5.*\.json$", "l5-page.schema.json"),
    (r"^l6.*\.json$", "l6-exhibition.schema.json"),
    (r"^l7.*\.json$", "l7-template.schema.json"),
    (r"^direction.*\.json$", "l3-direction.schema.json"),
    (r"^scene.*\.json$", "l4-scene.schema.json"),
    (r"^page.*\.json$", "l5-page.schema.json"),
    (r"^exhibition.*\.json$", "l6-exhibition.schema.json"),
    (r"^template.*\.json$", "l7-template.schema.json"),
]
# components/ dir => L2 regardless of file name
DIR_MAP = {"components": "l2-component.schema.json"}
ENABLED_KEYS = {"L1": "tokens", "L2": "components", "L3": "direction", "L4": "scene",
                "L5": "page", "L6": "exhibition", "L7": "template"}


def schema_for(path: Path):
    if path.parent.name in DIR_MAP:
        return SCHEMA_DIR / DIR_MAP[path.parent.name]
    for pat, schema in LAYER_MAP:
        if re.match(pat, path.name):
            return SCHEMA_DIR / schema
    return None


def collect_files(root: Path, layers: dict):
    files = []
    for path in sorted(root.rglob("*.json")):
        if path.name == "protocol.json":
            continue
        sf = schema_for(path)
        if sf is None:
            continue
        layer = sf.name[:2].upper()
        if layers and not layers.get(layer, True):
            continue
        files.append((path, sf))
    return files


def validate(root: Path):
    proto = root / "protocol.json"
    layers = {}
    if proto.exists():
        layers = json.loads(proto.read_text()).get("layers", {})
        for key in layers:
            if key not in ENABLED_KEYS:
                print(f"WARN protocol.json: unknown layer {key}")

    failures = 0
    for path, sf in collect_files(root, layers):
        try:
            data = json.loads(path.read_text())
            jsonschema.validate(data, json.loads(sf.read_text()))
            print(f"OK   {path.relative_to(root.parent)}")
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            failures += 1
            msg = getattr(e, "message", str(e))
            print(f"FAIL {path.relative_to(root.parent)}: {msg}")
    return failures


def self_test():
    import tempfile
    base = Path(tempfile.mkdtemp(prefix="dp-selftest-"))
    cases = [
        ("tokens.json", {"spacing": {"sm": {"$type": "dimension", "$value": "8px"}}}, True),
        ("tokens.json", {"spacing": {"sm": {"$value": "8px"}}}, False),  # missing $type
        ("components/button.json",
         {"name": "button", "category": "interaction", "variants": ["default"],
          "props": {"size": {"type": "enum", "values": ["sm", "md"]}}}, True),
        ("components/button.json",
         {"name": "Button", "category": "interaction", "variants": [], "props": {}}, False),
        ("direction.json",
         {"name": "tech-future", "mood": "clean", "color_strategy": "x",
          "density": "compact", "motion": "subtle"}, True),
        ("direction.json",
         {"name": "tech-future", "mood": "clean", "color_strategy": "x",
          "density": "loud", "motion": "subtle"}, False),  # bad enum
    ]
    ok = True
    for name, data, expect in cases:
        d = base / ("pass" if expect else "fail")
        (d / "components").mkdir(parents=True, exist_ok=True)
        (d / name).write_text(json.dumps(data))
        result = validate(d)
        got_ok = result == 0
        if got_ok != expect:
            print(f"SELFTEST FAIL: {name} expect={'pass' if expect else 'fail'} got={result} failures")
            ok = False
        else:
            print(f"selftest {name} ({'pass' if expect else 'fail'}): ok")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"FAIL: not a directory: {root}", file=sys.stderr)
        sys.exit(2)
    sys.exit(1 if validate(root) else 0)
