import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def run(script, *args, cwd=None):
    env = dict(os.environ)
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True, env=env, cwd=cwd,
    )


def test_snapshot_from_file(tmp_path):
    okb = tmp_path / "okb"
    src = tmp_path / "article.md"
    src.write_text("# Full Text\n\nclaims live here", encoding="utf-8")
    r = run("okb_snapshot.py", "--root", str(okb), "--topic", "llm-wiki-pattern",
            "--from-file", str(src), "--title", "Karpathy LLM Wiki Pattern",
            "--author", "A. Karpathy", "--source-url", "https://gist.example/x")
    assert r.returncode == 0, r.stderr
    out = list((okb / "bronze" / "llm-wiki-pattern").glob("*.md"))[0]
    text = out.read_text(encoding="utf-8")
    assert "source: https://gist.example/x" in text
    assert "author: A. Karpathy" in text
    assert "sha256: " in text
    assert "# Full Text" in text  # verbatim


def test_snapshot_dedup_same_sha(tmp_path):
    okb = tmp_path / "okb"
    src = tmp_path / "a.md"
    src.write_text("same bytes", encoding="utf-8")
    for _ in range(2):
        r = run("okb_snapshot.py", "--root", str(okb), "--topic", "t",
                "--from-file", str(src), "--title", "Same Title")
        assert r.returncode == 0, r.stderr
    files = list((okb / "bronze" / "t").glob("*.md"))
    assert len(files) == 1
    assert "skip" in run("okb_snapshot.py", "--root", str(okb), "--topic", "t",
                         "--from-file", str(src), "--title", "Same Title").stdout


def test_new_silver_is_draft_gold_has_no_body(tmp_path):
    okb = tmp_path / "okb"
    r = run("okb_new.py", "--root", str(okb), "--layer", "silver",
            "--topic", "t", "--slug", "compiled-knowledge",
            "--title", "Compiled Knowledge", "--description", "k is compiled once",
            "--stale-after", "2027-09-01")
    assert r.returncode == 0, r.stderr
    silver = (okb / "silver" / "t" / "compiled-knowledge.md").read_text(encoding="utf-8")
    assert "status: draft" in silver
    assert "verified: []" in silver
    assert "generated:" in silver

    r = run("okb_new.py", "--root", str(okb), "--layer", "gold",
            "--topic", "t", "--slug", "compiled-knowledge")
    assert r.returncode == 0, r.stderr
    gold = (okb / "gold" / "t" / "compiled-knowledge.md").read_text(encoding="utf-8")
    assert gold.count("---") == 2  # frontmatter only, no body after close
    assert gold.rstrip().endswith("---")

    # refuses overwrite without --force
    assert run("okb_new.py", "--root", str(okb), "--layer", "gold",
               "--topic", "t", "--slug", "compiled-knowledge").returncode != 0


def _mk_silver(okb, topic, slug, body="x", sources=""):
    d = okb / "silver" / topic
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{slug}.md").write_text(
        f"---\ntype: concept\ntitle: {slug}\nstatus: draft\nsources: {sources}\n---\n{body}\n",
        encoding="utf-8")


def test_index_regen_preserves_counter(tmp_path):
    okb = tmp_path / "okb"
    _mk_silver(okb, "t", "a")
    okb.joinpath("index.md").write_text("## t\n\ningests_since_status: 7\n", encoding="utf-8")
    r = run("okb_index_regen.py", "--root", str(okb))
    assert r.returncode == 0, r.stderr
    idx = (okb / "index.md").read_text(encoding="utf-8")
    assert "ingests_since_status: 7" in idx  # carried forward, not reset
    assert "silver/a.md" in idx


def test_check_links_finds_broken(tmp_path):
    okb = tmp_path / "okb"
    _mk_silver(okb, "t", "a", body="[b](./b.md)")
    _mk_silver(okb, "t", "b", body="[a](./a.md)")
    # a source edge pointing at a nonexistent bronze file
    p = okb / "silver" / "t" / "b.md"
    p.write_text(p.read_text(encoding="utf-8").replace("sources:", "sources: []\nbroken-edge:\n  resource: ../bronze/t/nope.md\n"), encoding="utf-8")
    r = run("okb_index_regen.py", "--root", str(okb), "--check-links")
    assert r.returncode == 1
    assert "a.md -> ./b.md" not in r.stdout  # a->b and b->a both exist: fine
    assert "nope.md" in r.stdout

    # fix the broken edge -> clean
    p.write_text(p.read_text(encoding="utf-8").replace("resource: ../bronze/t/nope.md\n", ""), encoding="utf-8")
    r = run("okb_index_regen.py", "--root", str(okb), "--check-links")
    assert r.returncode == 0, r.stdout
    assert "all reachable" in r.stdout
