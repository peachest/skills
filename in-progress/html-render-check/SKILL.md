---
name: html-render-check
description: Verify generated HTML artifacts (teach lessons/reference docs, impeccable surface artifacts) in a real headless-browser render using obscura — layout geometry (SVG overlap, text-escape, overflow), element presence, JS smoke, and screenshot evidence. Use after static checks (css-self-check, nav-chain-check, prose checks) pass and before the learner or user sees the HTML, or when an impeccable finish pass has no real browser on PATH.
---

# HTML Render Check

The **render check** is the rendering layer of HTML verification. Static checks (token compliance, nav chain, prose) read the file; this skill loads it in a real browser engine (obscura headless browser) and asserts on what actually rendered: geometry, visibility, runtime JS, and pixels. A finding is an adjudication prompt, not authorization to edit — some overlaps are intentional design (badges, callouts).

## Position in the check stack

Run **after** static checks pass, **before** the artifact reaches the learner/user:

- **teach**: after `css-self-check.py` and `nav-chain-check.py` (and prose/beat checks), before the learner sees the lesson.
- **impeccable**: in the finish/inspect pass, when no real browser (chromium/chrome) is on PATH — obscura *is* the browser. It complements `impeccable detect` (which reads the file) with actual render evidence.

## Setup

```bash
bash scripts/check-env.sh
```

FAIL output is the setup instruction. The heavy dependency is the **obscura** headless browser (Rust, V8 + Chrome DevTools Protocol), installed at `~/.local/bin/obscura` + `~/.local/bin/obscura-worker`. If missing, reinstall:

```bash
cd <tmpdir> && curl -sLO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-x86_64-linux-stealth.tar.gz
tar xzf obscura-x86_64-linux-stealth.tar.gz && cp obscura obscura-worker ~/.local/bin/ && chmod +x ~/.local/bin/obscura*
```

## Usage (CLI mode — primary)

```bash
bash scripts/check.sh <file.html> [<file.html>...]
```

Options via env or flags: `--port N` (http port, default from `runtime.conf`), `--shot-dir DIR` (default: beside the artifact), `--extra-js FILE` (page-specific battery, see below). The script serves the artifact's directory over `python3 -m http.server`, runs the battery + takes a screenshot per file, and exits non-zero when findings exist. Output: one JSON verdict line per file plus a summary.

### What the generic battery checks

1. **Element presence smoke** — counts of svg/canvas/video/img; a lesson that references an animation should show a `video` count > 0.
2. **HTML horizontal overflow** — elements whose `scrollWidth` exceeds `clientWidth` by >2px (visible, text-bearing, top 10; advisory — scroll containers are often intentional).
3. **SVG text×text collision** — pairwise text bbox intersection, severity = overlap area / smaller text; ≥30% is a hard finding.
4. **SVG shape×text occlusion** — filled shapes drawn after (on top of) a text, occluding ≥35% of it. Box labels (≥85% contained), background shapes (painted first), stroke-only shapes, and hidden layers are excluded.
5. **SVG text-escape** — text whose bbox leaves its containing group's `rect` by >1px.

A screenshot (`.render-check.png` beside the artifact) is captured as evidence for every run — geometry findings plus the pixel proof is what makes this layer persuasive.

### Page-specific batteries (`--extra-js`)

Generic checks cannot know that `.arch` is the diagram or that `#modeFix` must be clicked first (mode-switching diagrams hide hotspot layers behind `opacity="0"` — the generic battery filters invisible elements, but your page's *visible* state may need a click to reach). Write the page's own battery as a JS file: an IIFE that sets up state, then `return JSON.stringify(...)` its findings, same shape as the generic battery. Copy the geometry functions from `scripts/battery.js` (attribute-based — see quirks); `examples/` shows the structure of a page battery but its `getBBox` calls are a historical API mistake, do not copy them.

## Engine quirks (probe-verified on obscura 0.2.2 — trust these over any API doc)

**SVG geometry APIs are dead in `fetch -e`** (not a timing issue — verified with `--wait`, after screenshot, and after settle):

1. `getBBox()`, `getComputedTextLength()`, `getExtentOfChar()` all return **zeros**; `Range.getBoundingClientRect()` on SVG text returns zeros; `getScreenCTM` does not exist. **HTML layout APIs work fine** (`scrollWidth`/`clientWidth`/`getComputedStyle` return real values) — only the SVG surface is dead. The `<svg>` *root*'s `getBoundingClientRect()` works (it is HTML-embedded) — use it to filter rendered SVGs.
2. **Working geometry channels**: shape geometry from raw attributes (`x/y/width/height`, `cx/cy/r`, `points`), text width from **canvas `measureText()`**, text height ≈ font-size (the `y` attribute is the baseline). `scripts/battery.js` implements exactly this — copy its functions, do not reach for SVG APIs.
3. **Canvas font string must omit the weight prefix**: `"400 16px Times"` makes `measureText` return garbage (~240px/char); `"16px Times"` measures correctly. Bold slop is covered by tolerance.
4. `getComputedStyle` on SVG elements returns `""` for some properties (e.g. `textAnchor`) — falsy-string-safe fallback chains or attribute reads are required.

**Eval contract:**

5. Eval of an IIFE arrow without explicit `return` yields `null` — always `return` the JSON string.
6. Exceptions inside eval are swallowed silently → `null` — wrap the body in try/catch and `return 'EXC:'+e.message`.
7. `console.log` is NOT forwarded to stdout — the eval return value is the only output channel in CLI mode. Console output requires MCP mode (`browser_console_messages`).
8. Long return payloads are occasionally re-serialized into a table format (`"issues":"[20]{kind:string,...}`) — parse defensively; a re-run usually returns proper JSON.
9. Numbers come back as floats (`6.0`, `42.0`) — don't string-match on integer formatting.
10. `Script killed after 5s timeout` WARN is benign — a non-quiescent page (IntersectionObserver, animations) still loads and screenshots fine.

**Network:**

11. SSRF guard blocks loopback — local HTML must be served over `http://127.0.0.1:<port>/` with `--allow-private-network` (proven path: `python3 -m http.server`; `file://` unverified). The MCP server needs `--allow-private-network` added to its args in `~/.pi/agent/mcp.json` to reach localhost.

## Adjudication model (calibrated, not guessed)

Geometry severity is calibrated on a real before/after pair (same methodology as teach's prose-freq-check): an accepted artifact with straddling markers (骑线 design) as the pass oracle, and a real defect (circle marker centered on a label) as the fail oracle.

- **Design, not defect** (skipped or advisory): text ≥85% inside a shape (box label); shape drawn **before** the text in DOM order (SVG paints in order — it is the background); `fill="none"` shapes (stroke only); hidden layers (`opacity="0"` hotspots, `display:none` tabs — common in mode-switching diagrams); edge touches from measureText font-fallback error (~±10% width).
- **Hard finding**: a filled shape drawn **after** the text occludes ≥35% of its area ("unreadable" — the defect class users actually report), or two texts collide over ≥30% of the smaller one.
- Everything else lands as `advisory: true` — reported, passable, adjudicated against the screenshot.

## MCP mode (alternative)

When the obscura MCP server is configured (`~/.pi/agent/mcp.json`, command `obscura mcp --stealth`, lazy lifecycle), connect with `mcp({connect:"obscura"})` → ~37 tools including `browser_evaluate`, `browser_screenshot`, `browser_console_messages`, `browser_navigate`. Use MCP mode when you need **console error inspection** (CLI mode cannot read console output) or multi-step interaction (navigate → click → re-check). CLI mode is preferred for scriptable, repeatable verification.

## Files

```
SKILL.md                    # this file
runtime.conf.example        # OBSCURA_BIN, CHECK_PORT, PI_MCP_CONFIG
runtime.conf                # gitignored, per-node
scripts/check-env.sh        # PASS/WARN/FAIL environment verification
scripts/check.sh            # orchestrator: serve → battery → screenshot → verdict
scripts/battery.js          # generic JS check battery
examples/overlap-check.js   # page-specific battery example (shape×text, real defect catch)
examples/overflow-check.js  # page-specific battery example (text-escape + text×text)
```
