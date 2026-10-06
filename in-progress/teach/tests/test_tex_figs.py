"""Tests for tex-figs.py — synthetic LaTeX sources, no real paper content."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "assets" / "tex-figs.py"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


def make_paper(source: Path, tex_body: str, figs: dict[str, bytes] | None = None) -> None:
    source.mkdir(parents=True, exist_ok=True)
    (source / "main.tex").write_text(tex_body)
    for name, content in (figs or {}).items():
        p = source / name
        p.parent.mkdir(parents=True, exist_ok=True)
        # minimal-but-valid one-page PDF via raw bytes is fragile; tests only
        # need the file to exist with a size, and pdf rendering is covered by
        # an integration skip when pypdfium2 is absent. Use tiny valid PDFs.
        p.write_bytes(content)


TINY_PDF = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj
xref
0 4
trailer<</Size 4/Root 1 0 R>>
startxref
9
%%EOF
"""


class TestFigureMap:
    def test_maps_captions_in_document_order(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, r"""
\begin{figure}\includegraphics{figs/arch.pdf}\caption{The system architecture}\end{figure}
\begin{figure}\includegraphics[width=.9\textwidth]{figs/ablation.pdf}
\caption{Ablation over depth}\end{figure}
""", {"figs/arch.pdf": TINY_PDF, "figs/ablation.pdf": TINY_PDF})
        out = tmp_path / "out"
        r = run(str(src), "--out", str(out))
        assert r.returncode == 0, r.stdout + r.stderr
        fmap = json.loads((out / "figure-map.json").read_text())
        files = [f["file"] for f in fmap["figures"]]
        assert files == ["figs/arch.pdf", "figs/ablation.pdf"]
        caps = [f["caption"] for f in fmap["figures"]]
        assert "system architecture" in caps[0]
        assert "Ablation over depth" in caps[1]
        assert (out / "arch.png").exists() and (out / "ablation.png").exists()

    def test_includegraphics_without_caption(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, "\\includegraphics{loose.pdf}\n",
                   {"loose.pdf": TINY_PDF})
        r = run(str(src), "--out", str(tmp_path / "out"))
        fmap = json.loads((tmp_path / "out" / "figure-map.json").read_text())
        assert fmap["figures"][0]["caption"] == ""
        assert r.returncode == 0

    def test_extension_optional_and_dedup(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, "\\includegraphics{dup.pdf}\\includegraphics{dup}\n",
                   {"dup.pdf": TINY_PDF})
        r = run(str(src), "--out", str(tmp_path / "out"))
        fmap = json.loads((tmp_path / "out" / "figure-map.json").read_text())
        assert len(fmap["figures"]) == 1
        assert r.returncode == 0

    def test_missing_figure_flagged(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, "\\includegraphics{ghost.pdf}\n")
        r = run(str(src), "--out", str(tmp_path / "out"))
        assert r.returncode == 0
        assert "MISSING" in r.stdout


class TestCompositeWarning:
    def test_caption_naming_two_regions_flagged(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, "\\begin{figure}\\includegraphics{scatter.pdf}"
                        "\\caption{Left: T=0. Right: T=1.}\\end{figure}\n",
                   {"scatter.pdf": TINY_PDF})
        r = run(str(src), "--out", str(tmp_path / "out"))
        assert r.returncode == 0
        assert "COMPOSITE" in r.stdout

    def test_split_subfiles_flagged(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, "\\includegraphics{panel-a.pdf}\n",
                   {"panel-a.pdf": TINY_PDF, "panel-b.pdf": TINY_PDF})
        r = run(str(src), "--out", str(tmp_path / "out"))
        assert "COMPOSITE" in r.stdout

    def test_plain_caption_not_flagged(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, "\\begin{figure}\\includegraphics{one.pdf}"
                        "\\caption{Single overview figure.}\\end{figure}\n",
                   {"one.pdf": TINY_PDF})
        r = run(str(src), "--out", str(tmp_path / "out"))
        assert "COMPOSITE" not in r.stdout


class TestNoOverwrite:
    def test_second_run_without_force_fails_listing_conflicts(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, "\\includegraphics{fig.pdf}\\includegraphics{other.pdf}\n",
                   {"fig.pdf": TINY_PDF, "other.pdf": TINY_PDF})
        out = tmp_path / "out"
        assert run(str(src), "--out", str(out)).returncode == 0
        # simulate a second article rendering different bytes into same out dir
        src2 = tmp_path / "src2"
        make_paper(src2, "\\includegraphics{fig.pdf}\n", {"fig.pdf": TINY_PDF})
        r = run(str(src2), "--out", str(out))
        assert r.returncode == 1
        assert "fig.png" in r.stdout
        assert "--force" in r.stdout

    def test_force_allows_overwrite(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, "\\includegraphics{fig.pdf}\n", {"fig.pdf": TINY_PDF})
        out = tmp_path / "out"
        run(str(src), "--out", str(out))
        r = run(str(src), "--out", str(out), "--force")
        assert r.returncode == 0


class TestContactSheet:
    def test_sheet_written_when_requested(self, tmp_path):
        src = tmp_path / "src"
        make_paper(src, "\\includegraphics{a.pdf}\\includegraphics{b.pdf}\n",
                   {"a.pdf": TINY_PDF, "b.pdf": TINY_PDF})
        r = run(str(src), "--out", str(tmp_path / "out"), "--contact-sheet")
        assert r.returncode == 0
        assert "contact-sheet" in r.stdout
        assert (tmp_path / "out" / "contact-sheet.png").exists()


class TestUsage:
    def test_no_main_tex_fails(self, tmp_path):
        (tmp_path / "empty").mkdir()
        r = run(str(tmp_path / "empty"), "--out", str(tmp_path / "out"))
        assert r.returncode != 0
        assert "FAIL" in (r.stdout + r.stderr)
