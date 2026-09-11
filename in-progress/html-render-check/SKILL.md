---
name: html-render-check
description: Verify generated HTML artifacts (teach lessons/reference docs, impeccable surface artifacts) in a real Chromium render via Playwright — layout geometry (SVG occlusion, text collision, text-escape, overflow), JS runtime errors, broken subresources, and full-page screenshot evidence. Use after static checks (css-self-check, nav-chain-check, prose checks) pass and before the learner or user sees the HTML.
---

# HTML Render Check

The **render check** is the rendering layer of HTML verification. Static checks (token compliance, nav chain, prose) read the file; this skill loads it in a **real Chromium engine** (Playwright + chromium-headless-shell) and asserts on what actually rendered: geometry, visibility, runtime errors, network, and pixels. A finding is an adjudication prompt, not authorization to edit — some overlaps are intentional design (badges, callouts, straddling markers).

## Position in the check stack

This skill owns two layers of HTML verification and runs **before** the artifact reaches the learner/user:

1. **Structure layer** (offline, parse-level; absorbed from the former html-review skill): DOCTYPE, head/body/title/charset, duplicate ids, tag closure (lxml cross-validation), external-resource inventory, inline event handlers. `scripts/validate_html.py`; `--strict` adds html5lib spec parsing + VNU W3C checker (optional deps).
2. **Render layer** (real Chromium): layout geometry, JS runtime errors, broken subresources, screenshot evidence — what parsing cannot see.

Between them sit the target skill's own static checks:

- **teach**: css-self-check / nav-chain-check / prose / beat checks run between the two layers; `check.sh` runs structure → render around them.
- **impeccable**: in the finish/inspect pass, when no real browser (chromium/chrome) is on PATH — this skill brings its own browser. It complements `impeccable detect` (which reads the file) with actual render evidence.

Structure expects complete documents (teach lessons, surface artifacts) — not fragments.

## Setup

```bash
bash scripts/check-env.sh
```

FAIL output is the setup instruction. Setup summary (once per node):

```bash
# playwright module (outside this repo — the skill repo is public)
mkdir -p ~/tools/playwright-runner && cd ~/tools/playwright-runner && npm init -y && npm install playwright
# chromium headless shell (~100-170MB; proxy if the network is restricted)
npx playwright install chromium --only-shell
# system libs (Debian/Ubuntu)
sudo apt install libgbm1 libxkbcommon0
```

Chromium binaries are shared via `~/.cache/ms-playwright`. Cluster/container nodes launch with `--no-sandbox` by default (override with `PW_SANDBOX=1`).

## Usage

```bash
bash scripts/check.sh [--shot-dir DIR] [--strict] <file.html> [<file.html>...]
```

Runs structure validation (stage 0, gates the run) then the render layer (stage 1) per file. Exits non-zero when hard findings exist. Output: one `render:` JSON verdict per file plus a full-page screenshot (`.render-check.png`).

### What the render layer checks

1. **Element presence smoke** — counts of svg/canvas/video/img/table; a lesson that references an animation should show a `video` count > 0. Broken images (`naturalWidth === 0`) are hard findings.
2. **JS runtime errors** — `console.error` output and uncaught page errors, captured via Playwright event channels (hard findings).
3. **Broken subresources** — failed document/stylesheet/script/image/font loads (hard); fetch/xhr failures are advisory (a `file://` origin cannot `fetch()` at all).
4. **HTML horizontal overflow** — `scrollWidth` > `clientWidth` by >2px on visible text-bearing elements (advisory — scroll containers are often intentional).
5. **SVG text×text collision** — pairwise `getBoundingClientRect` intersection, severity = overlap area / smaller text; ≥30% is hard.
6. **SVG shape×text occlusion** — filled shapes painted after (on top of) a text, occluding ≥35% of it. Box labels (≥85% contained), background shapes (painted first), stroke-only shapes, and hidden layers are excluded.
7. **SVG text-escape** — text whose bbox leaves its containing group's `rect` by >1px.

Because the engine is real Chromium, `getBoundingClientRect()` works on **every** element including SVG children and JS-generated DOM (D3 charts etc.) — no attribute-based geometry shortcuts.

### Page-specific batteries

Generic checks cannot know that `.arch` is the diagram or that `#modeFix` must be clicked first (mode-switching diagrams hide hotspot layers behind `opacity: 0` — the generic battery filters invisible elements, but your page's *visible* state may need a click to reach). For page-specific checks, extend the pattern in `render-check.mjs`: navigate, interact (`page.click`), then `page.evaluate` an IIFE returning a JSON string. `examples/` shows page-level battery structure (historical — its geometry calls predate the real-engine migration; prefer `scripts/battery.js` as the reference).

## Adjudication model (calibrated, not guessed)

Geometry severity is calibrated on a real before/after pair (same methodology as teach's prose-freq-check): an accepted artifact with straddling markers (骑线 design) as the pass oracle, and a real defect (circle marker centered on a label) as the fail oracle.

- **Design, not defect** (skipped or advisory): text ≥85% inside a shape (box label); shape painted **before** the text in DOM order (SVG paints in order — it is the background); `fill="none"` shapes (stroke only); hidden layers (`opacity: 0` hotspots, `display: none` tabs — common in mode-switching diagrams); edge touches <30% of the smaller text.
- **Hard finding**: a filled shape painted **after** the text occludes ≥35% of its area ("unreadable" — the defect class users actually report), or two texts collide over ≥30% of the smaller one, or a JS runtime error, or a broken subresource load.
- Everything else lands as `advisory: true` — reported, passable, adjudicated against the screenshot.

## Engine notes (verified on Playwright 1.63 + chromium-headless-shell)

- `file://` navigation is the default — relative asset paths (`../assets/base.css`) resolve naturally, no local HTTP server needed. `<link>`/`<script>`/`<img>` file loads work; `fetch()`/XHR against `file://` origins fail by Chromium design (hence advisory).
- Bounded verification: one settle beat (400ms) after `load`, one full-page screenshot, one verdict — not a loop.
- Launch on cluster/container nodes needs `--no-sandbox --disable-dev-shm-usage` (default); `PW_SANDBOX=1` restores the sandbox where userns is available.
- System deps on Debian/Ubuntu: `libgbm1`, `libxkbcommon0` (probe with `ldd` on the chrome-headless-shell binary; `check-env.sh` does this for you).

## Files

```
SKILL.md                    # this file
runtime.conf.example        # PLAYWRIGHT_DIR setup notes
runtime.conf                # gitignored, per-node
scripts/check-env.sh        # PASS/WARN/FAIL environment verification
scripts/check.sh            # orchestrator: structure → render → verdict
scripts/validate_html.py    # structure layer (DOCTYPE/dup-id/closure/resources; --strict: html5lib+VNU)
scripts/render-check.mjs    # render layer: Playwright runner (file://, console/network capture, screenshot)
scripts/battery.js          # render layer: generic JS check battery
examples/overlap-check.js   # page-specific battery example (structure reference; geometry calls are historical)
examples/overflow-check.js  # page-specific battery example (structure reference)
```

## History

This skill originally used the obscura headless browser (Rust+V8, no SVG layout engine — all SVG geometry APIs returned zeros, requiring an attribute-parsing + canvas-measureText workaround). Migrated to Playwright/Chromium 2026-09-08 for real geometry, console/network capture, and mainstream tooling. The obscura exploration record lives in `docs/research/html-render-check/` (repo root).
