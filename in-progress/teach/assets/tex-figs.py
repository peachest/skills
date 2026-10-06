#!/usr/bin/env python3
"""tex-figs.py — extract figure assets from a LaTeX paper's source tree.

Given a paper's source directory (containing the main .tex and figure files)
and an output directory, produces:

  1. a figure map (JSON): includegraphics order -> {file, caption, out_png}
  2. rendered PNGs for every vector figure (PDF/PS/EPS -> PNG via pypdfium2,
     width-adaptive scale so narrow figures stay legible)
  3. a composite-figure completeness warning: figures that ship as multiple
     subfiles (foo.pdf, foo-a.pdf ... or a caption referencing "left/right/
     top/bottom") are flagged so every subfigure gets rendered — a lesson
     that embeds only the left half of a two-part figure is a defect
  4. --contact-sheet: one PIL grid image of all rendered PNGs with filenames,
     for human visual review (the model cannot see the images)

Never overwrites an existing output file: a name collision is exit 1 with
the conflict list (re-scraping a second article into the same directory
previously overwrote embedded lesson assets; regeneration must be explicit
via --force).

Usage:
  python3 tex-figs.py <source-dir> --out <out-dir> [--tex <main.tex>]
                      [--contact-sheet] [--force] [--map-out FILE.json]
Exit 0 = clean; exit 1 = conflicts or nothing extracted; 2 = usage/env error.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

# \includegraphics[opts]{path} — brace path, ignore optional args
INC_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
# figure environments carry the caption that names the figure
FIG_ENV_RE = re.compile(
    r"\\begin\{figure\}.*?\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}.*?"
    r"\\caption\{(.*?)\}", re.S)
CAPTION_CLEAN = re.compile(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{)|\}")
# subfile hints: authors split composites as stem-a/stem-b or stem1/stem2
SUBFILE_RE = re.compile(r"[-_.](?:[a-z]|\d+)\.(?:pdf|eps|ps|png|jpe?g)$", re.I)
# caption words that imply a multi-part figure
COMPOSITE_WORDS = re.compile(
    r"\b(left|right|top|bottom|middle)\b.*\b(left|right|top|bottom|middle)\b"
    r"|\bsub-?figures?\b|\b(left|right)[- ](and|&)[ -](right|left)\b", re.I)


def _clean_caption(cap: str) -> str:
    cap = CAPTION_CLEAN.sub("", cap)
    return re.sub(r"\s+", " ", cap).strip()[:120]


def find_main_tex(source_dir: pathlib.Path, explicit: str | None) -> pathlib.Path:
    if explicit:
        p = source_dir / explicit
        if not p.exists():
            sys.exit(f"FAIL: --tex {explicit} not found under {source_dir}")
        return p
    texs = sorted(source_dir.rglob("*.tex"),
                  key=lambda p: (len(p.parts), p.name != "main.tex"))
    if not texs:
        print(f"FAIL: no .tex under {source_dir}", file=sys.stderr)
        sys.exit(1)
    # prefer the tex with the most \includegraphics (the real document body)
    scored = [(len(INC_RE.findall(p.read_text(errors="ignore"))), p) for p in texs]
    scored.sort(reverse=True)
    return scored[0][1]


def extract_figures(main_tex: pathlib.Path) -> list[dict]:
    """Ordered (document order) figure list: includegraphics entries merged
    with figure-environment captions (caption wins when both exist)."""
    text = main_tex.read_text(errors="ignore")
    caps: dict[str, str] = {}
    for m in FIG_ENV_RE.finditer(text):
        caps.setdefault(m.group(1), _clean_caption(m.group(2)))
    figs: list[dict] = []
    seen: set[str] = set()
    for m in INC_RE.finditer(text):
        raw = m.group(1)
        if raw in seen:
            continue
        seen.add(raw)
        figs.append({"file": raw, "caption": caps.get(raw, ""), "composite": False})
    return figs


def resolve_file(source_dir: pathlib.Path, fig: dict) -> pathlib.Path | None:
    """Locate the figure file; LaTeX extensions are optional in \\includegraphics."""
    base = source_dir / fig["file"]
    for cand in (base,
                 *[base.with_suffix(e) for e in (".pdf", ".png", ".jpg", ".eps", ".ps")]):
        if cand.exists():
            return cand
    return None


def render_pdf(pdf: pathlib.Path, out_png: pathlib.Path) -> None:
    try:
        import pypdfium2 as pdfium
    except ImportError:
        sys.exit("FAIL: pypdfium2 missing — run: uv run --with pypdfium2 --with pillow "
                 "python3 tex-figs.py ...")
    try:
        doc = pdfium.PdfDocument(str(pdf))
    except Exception as e:
        print(f"  RENDER-ERROR: {pdf.name} — unreadable PDF ({str(e).splitlines()[0][:80]})")
        raise
    page = doc[0]
    w = page.get_width()
    scale = 3.0 if w < 400 else 2.2   # narrow figures need a bigger scale
    bitmap = page.render(scale=scale)
    bitmap.to_pil().save(out_png)


def contact_sheet(pngs: list[pathlib.Path], out: pathlib.Path, cols: int = 4) -> None:
    from PIL import Image, ImageDraw
    cell_w, cell_h, pad = 420, 320, 24
    rows = (len(pngs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cell_w + pad) + pad,
                              rows * (cell_h + pad + 18) + pad), "white")
    draw = ImageDraw.Draw(sheet)
    for i, p in enumerate(pngs):
        img = Image.open(p)
        img.thumbnail((cell_w, cell_h))
        x = pad + (i % cols) * (cell_w + pad)
        y = pad + (i // cols) * (cell_h + pad + 18)
        sheet.paste(img, (x, y))
        draw.text((x, y + cell_h + 2), p.name[:44], fill="black")
    sheet.save(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("source_dir", help="paper source directory (main .tex + figures)")
    ap.add_argument("--out", required=True, help="output directory for PNGs + map")
    ap.add_argument("--tex", help="main tex file name (default: auto-detect)")
    ap.add_argument("--contact-sheet", action="store_true",
                    help="also write a review grid image")
    ap.add_argument("--force", action="store_true", help="overwrite existing outputs")
    ap.add_argument("--map-out", help="write figure map JSON here (default: <out>/figure-map.json)")
    args = ap.parse_args()

    source_dir = pathlib.Path(args.source_dir)
    out_dir = pathlib.Path(args.out)
    if not source_dir.is_dir():
        sys.exit(f"FAIL: {source_dir} is not a directory")

    main_tex = find_main_tex(source_dir, args.tex)
    figs = extract_figures(main_tex)
    if not figs:
        print(f"{main_tex}: no \\includegraphics found")
        return 1

    # dedupe by output filename: the same graphic included twice (with and
    # without extension) is one figure — without this the second include
    # sees the first's output as a name collision and aborts the run.
    deduped: list[dict] = []
    seen_out: set[str] = set()
    for fig in figs:
        out_name = pathlib.Path(fig["file"]).stem + ".png"
        if out_name in seen_out:
            continue
        seen_out.add(out_name)
        deduped.append(fig)
    figs = deduped

    out_dir.mkdir(parents=True, exist_ok=True)
    conflicts, rendered, composites = [], [], []
    for fig in figs:
        src = resolve_file(source_dir, fig)
        if src is None:
            fig["out_png"] = None
            fig["missing"] = True
            continue
        out_png = out_dir / (pathlib.Path(fig["file"]).stem + ".png")
        if out_png.exists() and not args.force:
            conflicts.append(str(out_png))
            fig["out_png"] = str(out_png)
            continue
        if src.suffix.lower() == ".pdf":
            try:
                render_pdf(src, out_png)
            except Exception:
                fig["out_png"] = None
                fig["render_error"] = True
                continue
        elif src.suffix.lower() in (".png", ".jpg", ".jpeg"):
            out_png.write_bytes(src.read_bytes())
        else:  # eps/ps — delegate to ghostscript if present
            rc = subprocess.run(["gs", "-dSAFER", "-dBATCH", "-dNOPAUSE",
                                 f"-sOutputFile={out_png}", "-sDEVICE=png16m",
                                 "-r200", str(src)], capture_output=True)
            if rc.returncode != 0:
                fig["out_png"] = None
                fig["render_error"] = True
                continue
        fig["out_png"] = str(out_png)
        rendered.append(out_png)
        # composite heuristics: split subfiles (shared stem prefix family),
        # or a caption naming two regions
        stem = src.stem
        prefix = stem.rsplit("-", 1)[0] if "-" in stem else stem
        sub_siblings = [p for p in src.parent.glob(prefix + "*")
                        if p != src and SUBFILE_RE.search(p.name)]
        if COMPOSITE_WORDS.search(fig["caption"]) or len(sub_siblings) >= 1:
            fig["composite"] = True
            composites.append(fig)

    if conflicts:
        print(f"FAIL: {len(conflicts)} existing output(s) would be overwritten — "
              "use --force or a fresh --out:")
        for c in conflicts:
            print(f"  {c}")
        return 1

    map_path = pathlib.Path(args.map_out) if args.map_out else out_dir / "figure-map.json"
    map_path.write_text(json.dumps(
        {"main_tex": str(main_tex), "figures": figs}, ensure_ascii=False, indent=1))

    print(f"{main_tex}: {len(figs)} figure(s), {len(rendered)} rendered -> {map_path}")
    for fig in composites:
        print(f"  COMPOSITE: {fig['file']} — caption implies multiple parts "
              f"({fig['caption'][:60]}...); render every subfigure, a half-embedded "
              "figure is a learner-caught defect")
    for fig in figs:
        if fig.get("missing"):
            print(f"  MISSING: {fig['file']} (referenced, not in source tree)")
        if fig.get("render_error"):
            print(f"  RENDER-ERROR: {fig['file']} (unreadable at render time)")
    if args.contact_sheet and rendered:
        sheet = out_dir / "contact-sheet.png"
        contact_sheet(rendered, sheet)
        print(f"  contact sheet: {sheet} (for human visual review)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
