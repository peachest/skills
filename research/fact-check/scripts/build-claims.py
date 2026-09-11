#!/usr/bin/env python3
"""build-claims.py — Claim assembly tool (R24: single-emission contract).

Why this exists: before this tool, agents hand-wrote full claims.json
(claim_id + source_location + content_hash + ...). One schema drift meant
re-emitting ALL claims. Observed cost: 2 full 30-claim rewrites (~6K output
tokens) in a single run.

Contract:
  - The LLM emits ONLY minimal claim fields (claim_text, type, expected_verifier).
  - This script assigns claim_id, runs locate-claim + check-atomicity, fills
    source_location/content_hash, and writes claims.json.
  - Failed claims (locate errors) are NOT written; they are echoed back so the
    agent re-emits ONLY the failures.
  - Input arrives via stdin (JSON array or JSONL) — no shell quoting, so
    claim_text containing backticks/`$()` is safe.

Usage:
  # Assemble (append to existing claims.json, or create):
  cat seed.jsonl | python3 scripts/build-claims.py --doc <doc.md> --out <claims.json> [--replace]

  # Incremental patch — fix only failed claims, never re-emit the whole set:
  cat patches.json | python3 scripts/build-claims.py --doc <doc.md> --out <claims.json> --merge

Assemble input (each item):
  {"claim_text": "<verbatim excerpt>", "type": "<valid type>", "expected_verifier": "web_search",
   "normalized_claim": "optional", "decomposition": {"mode": "...", "sub_claims": [...]}, "compound_flag": null}

Merge input (each item, at least one of patch fields / "delete"):
  {"claim_id": "C001", "patch": {"claim_text": "...", "type": "...", "expected_verifier": "...",
                                  "source_location": "manual:<...>" | "relocate": true, ...}}
  {"claim_id": "C002", "delete": true}

Output (stdout, compact):
  {"written": N, "total_in_file": M, "next_id": "C031",
   "located": N, "failed": [{"claim_id", "error", "closest_match", "claim_text_head"}],
   "validation": {"passed": P, "failed": F, "failure_groups": [...]}}
Exit: 0 all ok; 1 some claims failed; 2 input format error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

# Keep in sync with scripts/validate-claims.sh VALID_TYPES (DD-06).
VALID_TYPES = {
    "authority", "numerical", "temporal", "factual", "causal",
    "comparative", "code-api", "citation", "existence", "interpretation",
    "file_path", "attribution",
    "legal-med-fin", "pricing", "licensing", "compliance",
    "capability", "date", "architecture", "status",
}
VALID_VERIFIERS = {"rule_engine", "web_search", "refused", "inferred"}
# local_repo is not a pipeline verifier but is a legal expected_verifier value:
# validate-claims.sh does not enforce the verifier enum, and code-anchor claims
# verified against a local checkout need a marker. Pass through silently.
EXTRA_VERIFIERS = {"local_repo"}

MAX_CLAIM_ID = 999


def die(msg: str, code: int = 2) -> None:
    print(json.dumps({"error": msg}, ensure_ascii=False), file=sys.stderr)
    sys.exit(code)


def run_script(name: str, args: list[str]) -> dict:
    """Run a sibling script, return parsed stdout JSON ({} on parse failure)."""
    result = subprocess.run(
        ["bash", str(SCRIPTS_DIR / name), *args],
        capture_output=True, text=True, timeout=30,
    )
    out = result.stdout.strip()
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"error": f"PARSE_FAIL", "stderr": result.stderr[:200]}


def load_stdin_claims() -> list[dict]:
    raw = sys.stdin.read().strip()
    if not raw:
        die("empty stdin: pipe a JSON array or JSONL of claims")
    items: list[dict] = []
    if raw.startswith("["):
        try:
            items = json.loads(raw)
        except json.JSONDecodeError as e:
            die(f"invalid JSON array on stdin: {e}")
    else:
        for i, line in enumerate(raw.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as e:
                die(f"invalid JSONL on line {i}: {e}")
    if not isinstance(items, list) or not items:
        die("stdin must contain a non-empty array/JSONL of claim objects")
    for it in items:
        if not isinstance(it, dict):
            die(f"claim entry is not an object: {it!r}")
    return items


def load_existing(out_path: Path) -> list[dict]:
    if out_path.exists():
        try:
            data = json.loads(out_path.read_text())
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return []


def next_claim_id(existing: list[dict]) -> int:
    max_n = 0
    for c in existing:
        m = re.match(r"^C(\d{3})$", str(c.get("claim_id", "")))
        if m:
            max_n = max(max_n, int(m.group(1)))
    return max_n + 1


def head(text: str, n: int = 60) -> str:
    return (text[:n] + "…") if len(text) > n else text


def validate_seed(c: dict, idx: int) -> None:
    """Fail fast on format drift — the exact failure mode build-claims exists to prevent."""
    where = f"stdin item {idx}"
    text = c.get("claim_text")
    if not isinstance(text, str) or not text.strip():
        die(f"{where}: missing/empty claim_text. Required minimal fields: "
            "claim_text (verbatim document excerpt), type, expected_verifier. "
            "Do NOT include claim_id / source_location / content_hash — this script assigns them.")
    typ = c.get("type")
    if typ not in VALID_TYPES:
        die(f"{where}: invalid type {typ!r}. Valid types: {sorted(VALID_TYPES)}")
    ev = c.get("expected_verifier", "web_search")
    if not isinstance(ev, str) or not ev.strip():
        die(f"{where}: expected_verifier must be a non-empty string")


def locate(claim_text: str, doc: str) -> dict:
    return run_script("locate-claim.sh", [claim_text, doc])


def atomicity(claim_text: str) -> dict:
    r = run_script("check-atomicity.sh", [claim_text])
    # Treat parse failure as "no pattern"
    if r.get("error") or "match" not in r:
        return {"match": False, "pattern": "none", "sub_items": [], "word_count": 0}
    return r


def build_full_claim(cid: str, seed: dict, loc: dict, atom: dict) -> dict:
    claim = {
        "claim_id": cid,
        "claim_text": seed["claim_text"],
        "normalized_claim": seed.get("normalized_claim"),
        "source_location": loc["location"],
        "content_hash": loc["hash"],
        "type": seed["type"],
        "expected_verifier": seed.get("expected_verifier", "web_search"),
        "atomicity_parent": None,
        "decomposition_mode": None,
        "compound_flag": None,
    }
    decomp = seed.get("decomposition")
    if isinstance(decomp, dict) and decomp.get("mode"):
        claim["decomposition_mode"] = decomp["mode"]
        claim["decomposition"] = decomp
    elif atom.get("match") and atom.get("pattern") != "none":
        claim["decomposition_mode"] = atom["pattern"]
    if not claim["decomposition_mode"]:
        if not atom.get("match") and atom.get("word_count", 0) > 25:
            claim["compound_flag"] = "compound_embedded"
    if seed.get("compound_flag"):
        claim["compound_flag"] = seed["compound_flag"]
    return claim


def validate_file(out_path: Path, doc: str) -> dict:
    r = run_script("validate-claims.sh", [str(out_path), doc])
    if r.get("error"):
        return {"passed": 0, "failed": -1, "failure_groups": [
            {"code": "VALIDATE_RUN_FAIL", "count": 1, "claim_ids": [], "detail": r["error"]}]}
    groups: dict[str, dict] = {}
    for f in r.get("failures", []):
        for e in f.get("errors", []):
            code = e.get("code", "UNKNOWN")
            g = groups.setdefault(code, {"code": code, "count": 0, "claim_ids": [], "detail": e.get("detail", "")})
            g["count"] += 1
            g["claim_ids"].append(f.get("claim_id", "UNKNOWN"))
    summary = {
        "passed": r.get("passed", 0),
        "failed": r.get("failed", 0),
        "failure_groups": sorted(groups.values(), key=lambda g: -g["count"]),
        "auto_fixes": r.get("auto_fixes", []),
    }
    return summary


def mode_assemble(seeds: list[dict], doc: str, out_path: Path, replace: bool) -> int:
    existing = [] if replace else load_existing(out_path)
    if replace and out_path.exists():
        out_path.unlink()
    n = next_claim_id(existing)
    if n > MAX_CLAIM_ID:
        die(f"claim_id space exhausted (next would be C{n:03d} > C{MAX_CLAIM_ID})")

    located: list[dict] = []
    failed: list[dict] = []
    for i, seed in enumerate(seeds, 1):
        validate_seed(seed, i)
        loc = locate(seed["claim_text"], doc)
        if loc.get("ok"):
            atom = atomicity(seed["claim_text"])
            cid = f"C{n:03d}"
            n += 1
            located.append(build_full_claim(cid, seed, loc, atom))
        else:
            failed.append({
                "claim_id": f"NEW-{i}",
                "error": loc.get("error", "LOCATE_FAIL"),
                "closest_match": loc.get("closest_match", ""),
                "candidates": loc.get("candidates", []),
                "claim_text_head": head(seed["claim_text"]),
            })

    if located:
        merged = existing + located
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2))

    validation = validate_file(out_path, doc) if located else {"passed": 0, "failed": 0, "failure_groups": []}
    print(json.dumps({
        "written": len(located),
        "total_in_file": len(existing) + len(located),
        "next_id": f"C{n:03d}",
        "located": len(located),
        "failed": failed,
        "validation": validation,
    }, ensure_ascii=False))
    return 1 if (failed or validation.get("failed")) else 0


PATCHABLE = {"claim_text", "type", "expected_verifier", "normalized_claim",
             "compound_flag", "decomposition", "source_location", "content_hash"}


def mode_merge(patches: list[dict], doc: str, out_path: Path) -> int:
    existing = load_existing(out_path)
    if not existing:
        die(f"claims file empty or missing: {out_path} (merge requires an existing set)")
    by_id = {c.get("claim_id"): c for c in existing if isinstance(c, dict)}

    failed: list[dict] = []
    deleted: list[str] = []
    patched: list[str] = []

    for i, p in enumerate(patches, 1):
        cid = p.get("claim_id")
        if cid not in by_id:
            failed.append({"claim_id": cid, "error": "CLAIM_NOT_FOUND",
                           "closest_match": "", "claim_text_head": head(str(p))})
            continue
        claim = by_id[cid]
        if p.get("delete"):
            existing.remove(claim)
            del by_id[cid]
            deleted.append(cid)
            continue
        patch = p.get("patch")
        if not isinstance(patch, dict) or not patch:
            failed.append({"claim_id": cid, "error": "EMPTY_PATCH",
                           "closest_match": "", "claim_text_head": ""})
            continue
        bad = set(patch) - PATCHABLE
        if bad:
            failed.append({"claim_id": cid, "error": "UNPATCHABLE_FIELDS",
                           "closest_match": ", ".join(sorted(bad)), "claim_text_head": ""})
            continue
        if "type" in patch and patch["type"] not in VALID_TYPES:
            failed.append({"claim_id": cid, "error": "INVALID_TYPE",
                           "closest_match": str(patch["type"]), "claim_text_head": ""})
            continue
        claim.update(patch)
        # Re-locate when text changed, or when explicitly requested (e.g. after AMBIGUOUS)
        if "claim_text" in patch or patch.get("source_location") == "relocate":
            claim.pop("source_location", None) if claim.get("source_location") == "relocate" else None
            loc = locate(claim["claim_text"], doc)
            if loc.get("ok"):
                claim["source_location"] = loc["location"]
                claim["content_hash"] = loc["hash"]
            else:
                failed.append({"claim_id": cid, "error": loc.get("error", "LOCATE_FAIL"),
                               "closest_match": loc.get("closest_match", ""),
                               "claim_text_head": head(claim["claim_text"])})
                continue
        patched.append(cid)

    out_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    validation = validate_file(out_path, doc)
    print(json.dumps({
        "written": len(patched),
        "patched": patched,
        "deleted": deleted,
        "total_in_file": len(existing),
        "failed": failed,
        "validation": validation,
    }, ensure_ascii=False))
    return 1 if (failed or validation.get("failed")) else 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Assemble/patch claims.json from minimal LLM output")
    ap.add_argument("--doc", required=True, help="source document path")
    ap.add_argument("--out", required=True, help="claims.json path")
    ap.add_argument("--merge", action="store_true", help="patch mode: stdin = [{claim_id, patch|delete}]")
    ap.add_argument("--replace", action="store_true", help="assemble mode: discard existing claims.json first")
    args = ap.parse_args()

    if not Path(args.doc).is_file():
        die(f"source doc not found: {args.doc}")

    items = load_stdin_claims()
    if args.merge:
        sys.exit(mode_merge(items, args.doc, Path(args.out)))
    sys.exit(mode_assemble(items, args.doc, Path(args.out), args.replace))


if __name__ == "__main__":
    main()
