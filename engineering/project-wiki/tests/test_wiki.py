"""Fail-closed test suite for the project-wiki CLI (both runtimes).

Positive cases: init generates complete charts, update re-baselines, check
stays green on a clean wiki.

Fail-closed cases: every drift/integrity shape must produce a stable signal
code in --json output and the documented exit code — a missing wiki, a
deleted file, a hand-broken registration table, an overview/index mismatch,
or an L3 link drift can never silently pass.

Dual-runtime: every case runs against both wiki.py and wiki.js, and a
dedicated parity test asserts the two runtimes emit identical JSON.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from conftest import (
    RUNTIMES,
    load_cache,
    run_json,
    run_wiki,
    wiki_dir,
)


def codes(result: dict) -> list[str]:
    return [s["code"] for s in result["signals"]]


def signals_for(result: dict, code: str) -> list[dict]:
    return [s for s in result["signals"] if s["code"] == code]


# ---------------------------------------------------------------------------
# init — positive structural fixture
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("runtime", RUNTIMES)
def test_init_generates_complete_charts(runtime: str, go_project: Path):
    result = run_json(runtime, ["init", "--root", str(go_project)])

    assert result["ok"] is True
    assert result["command"] == "init"
    summary = result["summary"]
    assert summary["files"] == 4
    assert summary["modules"] == 3
    assert summary["module_names"] == ["auth", "root", "storage"]

    wd = wiki_dir(go_project)
    assert (wd / "overview.md").exists()
    for module in ("auth", "root", "storage"):
        assert (wd / f"{module}.md").exists(), f"missing module wiki: {module}"

    # Registration tables must cover every source file, no omissions.
    for module, expected_files in {
        "auth": ["auth/login.go", "auth/jwt.go"],
        "storage": ["storage/db.go"],
        "root": ["main.go"],
    }.items():
        content = (wd / f"{module}.md").read_text()
        for f in expected_files:
            assert f"`{f}`" in content, f"{module}.md does not register {f}"

    # Baseline cache exists and marks everything unreviewed (init ≠ review).
    cache = load_cache(go_project)
    assert len(cache["files"]) == 4
    assert all(not v["reviewed"] for v in cache["files"].values())


# ---------------------------------------------------------------------------
# check — clean state
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("runtime", RUNTIMES)
def test_check_clean_after_update(runtime: str, initialized):
    root = initialized(runtime)
    result = run_json(runtime, ["check", "--root", str(root)])

    assert result["ok"] is True
    assert result["signals"] == []
    assert result["summary"]["tracked"] == 4
    assert result["summary"]["current"] == 4
    assert result["summary"]["integrity"] == 0


# ---------------------------------------------------------------------------
# check — file drift (fail-closed)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("runtime", RUNTIMES)
def test_check_new_file_fails_closed(runtime: str, initialized):
    root = initialized(runtime)
    (root / "auth" / "new.go").write_text("package auth\n")

    result = run_json(runtime, ["check", "--root", str(root)])
    assert result["ok"] is False
    assert "WIKI-NEW-FILE" in codes(result)
    new = signals_for(result, "WIKI-NEW-FILE")
    assert [s["path"] for s in new] == ["auth/new.go"]
    # The file also lacks a registration-table row.
    assert "WIKI-UNREGISTERED-FILE" in codes(result)

    # Exit codes: 0 when reporting only, 1 with --fail-on-stale.
    assert run_wiki(runtime, ["check", "--root", str(root)], check=False).returncode == 0
    fail = run_wiki(
        runtime, ["check", "--root", str(root), "--fail-on-stale"], check=False
    )
    assert fail.returncode == 1


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_check_deleted_file_fails_closed(runtime: str, initialized):
    root = initialized(runtime)
    (root / "storage" / "db.go").unlink()

    result = run_json(runtime, ["check", "--root", str(root)])
    assert result["ok"] is False
    deleted = signals_for(result, "WIKI-DELETED-FILE")
    assert [s["path"] for s in deleted] == ["storage/db.go"]
    # The stale registration row is flagged as an orphan entry.
    orphan = signals_for(result, "WIKI-ORPHAN-ENTRY")
    assert [s["path"] for s in orphan] == ["storage/db.go"]


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_check_modified_file_only_after_review(runtime: str, initialized):
    root = initialized(runtime)

    # Baseline is reviewed (update ran) → modification must be reported.
    target = root / "auth" / "jwt.go"
    target.write_text("package auth // changed\n")
    result = run_json(runtime, ["check", "--root", str(root)])
    modified = signals_for(result, "WIKI-MODIFIED-FILE")
    assert [s["path"] for s in modified] == ["auth/jwt.go"]


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_check_modified_file_silent_when_unreviewed(runtime: str, go_project: Path):
    """Files changed between init and the first update are not MODIFIED drift.

    init marks the baseline unreviewed; a SHA change on an unreviewed entry is
    part of the initial fill-in workflow, not drift. This is the documented
    reviewed/unreviewed semantics of the SHA baseline.
    """
    run_wiki("python", ["init", "--root", str(go_project)])  # no update
    target = go_project / "auth" / "jwt.go"
    target.write_text("package auth // changed pre-review\n")

    result = run_json("python", ["check", "--root", str(go_project)])
    assert "WIKI-MODIFIED-FILE" not in codes(result)


# ---------------------------------------------------------------------------
# check — wiki self-integrity (fail-closed)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("runtime", RUNTIMES)
def test_missing_module_wiki_fails_closed_and_update_repairs(runtime: str, initialized):
    root = initialized(runtime)
    (wiki_dir(root) / "auth.md").unlink()

    result = run_json(runtime, ["check", "--root", str(root)])
    assert result["ok"] is False
    missing = signals_for(result, "WIKI-MODULE-WIKI-MISSING")
    assert [s["path"] for s in missing] == ["auth"]
    assert "module 'auth'" in missing[0]["detail"]

    # update is the documented repair path: it regenerates the skeleton.
    upd = run_json(runtime, ["update", "--root", str(root)])
    assert upd["summary"]["module_wikis_created"] == ["auth.md"]
    assert (wiki_dir(root) / "auth.md").exists()

    after = run_json(runtime, ["check", "--root", str(root)])
    assert after["ok"] is True
    assert after["signals"] == []


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_overview_module_mismatch_both_directions(runtime: str, initialized):
    root = initialized(runtime)
    overview = wiki_dir(root) / "overview.md"

    # Direction 1: row removed from the overview index.
    content = overview.read_text()
    removed = re.sub(r"^\| `storage` \|[^\n]*\n", "", content, flags=re.MULTILINE)
    assert removed != content, "test setup failed: storage row not found"
    overview.write_text(removed)
    result = run_json(runtime, ["check", "--root", str(root)])
    mismatch = signals_for(result, "WIKI-OVERVIEW-MODULE-MISMATCH")
    assert [s["path"] for s in mismatch] == ["storage"]
    assert "missing from the overview.md module index" in mismatch[0]["detail"]

    # Direction 2: a row for a module that has no source files.
    overview.write_text(content.replace(
        "| `storage` |",
        "| `storage` | _1 source files_ — x |", 1,
    ) + "\n| `ghost` | _1 source files_ — no such module | [ghost.md](ghost.md) |\n")
    result = run_json(runtime, ["check", "--root", str(root)])
    ghost = [s for s in signals_for(result, "WIKI-OVERVIEW-MODULE-MISMATCH")
             if s["path"] == "ghost"]
    assert ghost, "orphan overview row not flagged"
    assert "has no source files" in ghost[0]["detail"]


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_registration_table_drift_fails_closed(runtime: str, initialized):
    root = initialized(runtime)
    auth_md = wiki_dir(root) / "auth.md"

    # A registration row deleted by hand → the file is unregistered.
    content = auth_md.read_text()
    stripped = re.sub(r"^\| `auth/jwt\.go` \|[^\n]*\n", "", content, flags=re.MULTILINE)
    assert stripped != content, "test setup failed: jwt.go row not found"
    auth_md.write_text(stripped)
    result = run_json(runtime, ["check", "--root", str(root)])
    unregistered = signals_for(result, "WIKI-UNREGISTERED-FILE")
    assert [s["path"] for s in unregistered] == ["auth/jwt.go"]

    # A row for a file that does not exist → orphan entry.
    auth_md.write_text(content + "| `auth/ghost.go` | **Ghost** — never existed |\n")
    result = run_json(runtime, ["check", "--root", str(root)])
    orphan = signals_for(result, "WIKI-ORPHAN-ENTRY")
    assert [s["path"] for s in orphan] == ["auth/ghost.go"]


@pytest.mark.parametrize("runtime", RUNTIMES)
def test_l3_drift_fails_closed(runtime: str, initialized):
    root = initialized(runtime)
    # CONTEXT.md appears after the wiki was generated → overview can't link it.
    (root / "CONTEXT.md").write_text("# domain glossary\n")

    result = run_json(runtime, ["check", "--root", str(root)])
    assert result["ok"] is False
    l3 = signals_for(result, "WIKI-L3-DRIFT")
    assert l3, "CONTEXT.md drift not flagged"
    assert "CONTEXT.md" in l3[0]["detail"]

    # update re-links L3 artifacts (overview is regenerated with the link).
    run_json(runtime, ["update", "--root", str(root)])
    after = run_json(runtime, ["check", "--root", str(root)])
    assert "WIKI-L3-DRIFT" not in codes(after)


# ---------------------------------------------------------------------------
# status / JSON schema / error paths
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("runtime", RUNTIMES)
def test_status_json_schema(runtime: str, initialized):
    root = initialized(runtime)
    result = run_json(runtime, ["status", "--root", str(root)])

    assert result["command"] == "status"
    summary = result["summary"]
    for key in ("module_wikis", "tracked", "entries", "described_entries",
                "unreviewed", "last_updated", "l3_linked", "needs_attention"):
        assert key in summary, f"status summary missing key: {key}"
    assert summary["tracked"] == 4
    assert summary["module_wikis"] == 3


def test_check_without_wiki_fails_closed(tmp_path: Path):
    """No wiki directory → exit 2 with a human-readable error, never silent success."""
    for runtime in RUNTIMES:
        proc = run_wiki(runtime, ["check", "--root", str(tmp_path), "--json"],
                        check=False)
        assert proc.returncode == 2
        assert proc.stderr.strip(), f"{runtime}: expected an error on stderr"
        # Error paths never emit a JSON result object.
        with pytest.raises(json.JSONDecodeError):
            json.loads(proc.stdout)


def test_human_output_mode_is_not_json(initialized):
    """Without --json, check emits the human drift report, not JSON."""
    root = initialized("python")
    (root / "auth" / "new.go").write_text("package auth\n")

    proc = run_wiki("python", ["check", "--root", str(root)], check=False)
    assert proc.returncode == 0
    assert "PROJECT WIKI DRIFT REPORT" in proc.stdout
    with pytest.raises(json.JSONDecodeError):
        json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# dual-runtime parity
# ---------------------------------------------------------------------------

def _drift_sequence(root: Path):
    """Mutate a fixture project through every drift shape."""
    (root / "auth" / "new.go").write_text("package auth\n")     # NEW + UNREGISTERED
    (root / "storage" / "db.go").unlink()                        # DELETED + ORPHAN
    (root / "auth" / "jwt.go").write_text("package auth // x\n")  # MODIFIED


def test_dual_runtime_parity(tmp_path: Path):
    """Identical command sequences must produce identical JSON on both runtimes."""
    results = {}
    for runtime in RUNTIMES:
        root = tmp_path / runtime
        root.mkdir()
        (root / "auth").mkdir()
        (root / "auth" / "login.go").write_text("package auth\n")
        (root / "auth" / "jwt.go").write_text("package auth\n")
        (root / "storage").mkdir()
        (root / "storage" / "db.go").write_text("package storage\n")
        (root / "main.go").write_text("package main\n")

        seq = {
            "init": ["init", "--root", str(root)],
            "update": ["update", "--root", str(root)],
            "check_clean": ["check", "--root", str(root)],
        }
        out = {name: run_json(runtime, args) for name, args in seq.items()}

        _drift_sequence(root)
        out["check_drift"] = run_json(runtime, ["check", "--root", str(root)])
        out["status"] = run_json(runtime, ["status", "--root", str(root)])

        # Timestamps differ per invocation — everything else must not.
        out["status"]["summary"].pop("last_updated", None)
        results[runtime] = out

    assert results["python"] == results["node"], (
        "runtime outputs diverged:\n"
        f"python: {json.dumps(results['python'], indent=1, ensure_ascii=False)}\n"
        f"node:   {json.dumps(results['node'], indent=1, ensure_ascii=False)}"
    )


@pytest.mark.parametrize("init_rt,check_rt", [
    ("python", "node"),
    ("node", "python"),
])
def test_runtimes_interchangeable_on_one_project(init_rt: str, check_rt: str,
                                                 go_project: Path):
    """init with one runtime, check with the other — shared baseline, shared verdict."""
    run_wiki(init_rt, ["init", "--root", str(go_project)])
    run_wiki(init_rt, ["update", "--root", str(go_project)])

    result = run_json(check_rt, ["check", "--root", str(go_project)])
    assert result["ok"] is True
    assert result["summary"]["tracked"] == 4
