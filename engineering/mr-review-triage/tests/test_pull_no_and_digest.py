"""Ticket #60 CLI-level tests: pull `no` ordinal + --digest reconciliation.

Spec #57 test seam: real script subprocess, platform API replaced by offline
fixtures (fake curl/gh binaries first on PATH, synthetic ids only). All
assertions observe external behavior only — the stdout bare-JSON contract
and the stderr human output.
"""

import json
import re

import pytest

from conftest import FIXTURES_DIR, run_pull

# Post-dedup API first-seen order; the fixture carries a duplicate between
# first and last, plus stale id f0e1d2c3b4a59687 only in the against file.
GITLAB_IDS = ["a1b2c3d4e5f60718", "c3d4e5f607181920"]
GITHUB_IDS = ["9876543210001", "9876543210003"]
STALE_ID = "f0e1d2c3b4a59687"

TRUNCATION_SHAPE = re.compile(r"\b[0-9a-f]{8}\b")


def test_pull_assigns_no_in_deduped_api_first_seen_order_gitlab():
    proc = run_pull("9")
    assert proc.returncode == 0
    findings = json.loads(proc.stdout)  # stdout stays bare JSON
    assert [f["discussion_id"] for f in findings] == GITLAB_IDS
    assert [f["no"] for f in findings] == [1, 2]  # 1..N, duplicate dropped


def test_pull_assigns_no_in_deduped_api_first_seen_order_github():
    proc = run_pull("9", platform="github")
    assert proc.returncode == 0
    findings = json.loads(proc.stdout)
    assert [f["discussion_id"] for f in findings] == GITHUB_IDS
    assert [f["no"] for f in findings] == [1, 2]


@pytest.mark.parametrize("platform,expected_ids", [
    ("gitlab", GITLAB_IDS),
    ("github", GITHUB_IDS),
])
def test_pull_no_is_stable_across_repull(platform, expected_ids):
    first = json.loads(run_pull("9", platform=platform).stdout)
    second = json.loads(run_pull("9", platform=platform).stdout)
    assert [(f["discussion_id"], f["no"]) for f in first] == \
        [(f["discussion_id"], f["no"]) for f in second]


def test_digest_outputs_only_new_findings():
    against = FIXTURES_DIR / "against" / "flat_old.json"
    proc = run_pull("9", "--digest", "--against", str(against))
    assert proc.returncode == 0
    new = json.loads(proc.stdout)
    # Only the discussion_id absent from the classified file; exact byte match.
    assert [f["discussion_id"] for f in new] == [GITLAB_IDS[1]]
    # Keeps its pull-file ordinal — not renumbered within the digest output.
    assert new[0]["no"] == 2


def test_digest_accepts_schema2_against_file():
    against = FIXTURES_DIR / "against" / "schema2_old.json"
    proc = run_pull("9", "--digest", "--against", str(against))
    assert proc.returncode == 0
    assert [f["discussion_id"] for f in json.loads(proc.stdout)] == [GITLAB_IDS[1]]


def test_digest_missing_against_file_is_first_round(tmp_path):
    proc = run_pull("9", "--digest", "--against", str(tmp_path / "classified.json"))
    assert proc.returncode == 0  # not an error
    findings = json.loads(proc.stdout)
    assert [f["discussion_id"] for f in findings] == GITLAB_IDS
    assert [f["no"] for f in findings] == [1, 2]
    assert "first round" in proc.stderr


def test_digest_human_summary_has_no_id_or_truncation_shapes():
    plain = run_pull("9")
    digest = run_pull(
        "9", "--digest", "--against", str(FIXTURES_DIR / "against" / "flat_old.json")
    )
    for proc in (plain, digest):
        assert proc.stderr
        for full_id in [*GITLAB_IDS, *GITHUB_IDS, STALE_ID]:
            assert full_id not in proc.stderr
        assert not TRUNCATION_SHAPE.search(proc.stderr)
    assert "2 pulled, 1 already classified, 1 new" in digest.stderr
    assert "new findings no 2" in digest.stderr


def test_digest_without_against_is_usage_error():
    proc = run_pull("9", "--digest")
    assert proc.returncode != 0
    assert "--against" in proc.stderr


def test_against_without_digest_is_usage_error():
    proc = run_pull("9", "--against", "classified.json")
    assert proc.returncode != 0


def test_malformed_against_file_fails_closed(tmp_path):
    # A corrupt classified file must hard-fail, never read as "first round".
    bad = tmp_path / "classified.json"
    bad.write_text("{not json")
    proc = run_pull("9", "--digest", "--against", str(bad))
    assert proc.returncode != 0
    assert "classified.json" in proc.stderr  # names the file
