# HTML Render Check — obscura exploration & engine migration (2026-09-08)

Investigation snapshot: deep exploration of the obscura headless browser's
testing-relevant capabilities, a landscape survey of alternative tools, and the
decision to migrate the `html-render-check` skill from obscura to
Playwright/Chromium. Authoritative current usage lives in the skill's SKILL.md.

## 1. obscura capability inventory (probe-verified, v0.2.2)

| Capability | Invocation | Notes for testing |
|---|---|---|
| Render + eval + screenshot | `obscura fetch URL --allow-private-network -e <js> -s out.png` | The skill's original CLI mode |
| CDP server | `obscura serve --port N [--allow-file-access]` | Standard CDP 1.3 (advertises Chrome/145). Console error forwarding (`Runtime.consoleAPICalled`), network events (`Network.*`), `Page.captureScreenshot`, file:// navigation. Page-level WS endpoints reject commands — requires `Target.createTarget` + `Target.attachToTarget {flatten:true}` |
| MCP server | `obscura mcp --stealth [--http]` | 37 `browser_*` tools; needs `--allow-private-network` added to args to reach localhost |
| Sub-resource dump | `fetch --dump assets` | JSON list of every referenced sub-resource URL |
| Raw body dump | `fetch --dump original` | Binary-safe raw HTTP body (images/JSON/JS) |
| Batch modes | `scrape URLS... -e <js>` (rendered), `fetch --file list --concurrency N` (raw) | Engine-identical to single fetch |
| Selector extraction | `fetch --selector <css> --dump text` | Rendered-DOM CSS extraction |
| V8 flags | `--v8-flags "..."` | Raw V8 flags at startup |

### Engine limits (definitive — verified through all three modes)

**No SVG layout engine.** All SVG computed-geometry APIs return zeros or fail
in `fetch -e`, `scrape -e`, AND CDP `Runtime.evaluate` (so it is engine-level,
not a CLI sandbox artifact):

- `getBBox()` → all zeros
- `getBoundingClientRect()` on SVG children → all zeros (works on the `<svg>` root — it is HTML-embedded)
- `getComputedTextLength()` → 0; `getExtentOfChar()` → zeros
- `Range.getBoundingClientRect()` on SVG text → zeros; `getScreenCTM` → not a function

Working channels: HTML element layout (`scrollWidth`/`clientWidth`/gBCR),
`getComputedStyle` (some SVG properties return `""`), canvas
`measureText` — but the canvas font string must OMIT the weight prefix
(`"400 16px Times"` yields garbage ~240px/char; `"16px Times"` is correct).

**Blind spot**: JS-generated SVG (D3 charts etc.) has no geometry attributes
to parse — an attribute-based battery cannot see it.

**Other eval quirks** (fetch -e): IIFE arrow without explicit `return` →
`null`; exceptions swallowed → `null` (wrap in try/catch, return
`'EXC:'+e.message`); `console.log` not forwarded; long payloads occasionally
re-serialized into a table format; numbers come back as floats;
`Script killed after 5s timeout` WARN is benign (non-quiescent pages still
load and screenshot); SSRF guard blocks loopback without
`--allow-private-network` (file:// unverified in fetch mode).

## 2. Tool landscape (web survey 2026-09-08)

| Tool | Verdict |
|---|---|
| **Playwright + chromium-headless-shell** | ✅ adopted — real engine, mainstream, full geometry/console/network/file:// |
| Lightpanda | Same class as obscura (Rust, official "no graphical rendering") — no advantage for geometry |
| jsdom / happy-dom / linkedom | No layout at all (gBCR zeros) — useless for geometry; structure already covered by validate_html.py |
| PhantomJS / SlimerJS | Unmaintained |
| Cypress / Percy / visual-regression suites | Web-app test runners / SaaS — wrong shape for artifact verification |

## 3. Playwright feasibility record (this node, llm12)

1. `npm install playwright` — works via corporate proxy (http://172.16.80.252:3128).
2. `npx playwright install chromium --only-shell` — downloads to `~/.cache/ms-playwright` (~266MB incl. ffmpeg).
3. System libs required: `libgbm1`, `libxkbcommon0` (`sudo apt install`). Probe more with `ldd` on the chrome-headless-shell binary.
4. Launch on cluster/container nodes requires `--no-sandbox --disable-dev-shm-usage`.
5. Verified capabilities on a known-defect fixture: real `getBBox()`/gBCR on
   SVG children (96px / 72.79px where obscura returned 0), console.error +
   pageerror capture, response status + requestfailed events, file://
   navigation (relative `../assets` paths resolve — no HTTP server needed,
   unlike an http.server rooted at the artifact's directory),
   fullPage screenshots, ~500ms load for a 67KB artifact.

Playwright module installed outside the skill repo (repo is public):
`~/tools/playwright-runner`.

## 4. Migration deltas in the skill

- `scripts/battery.js` — attribute-parsing + measureText workaround replaced by
  real `getBoundingClientRect()` on all elements; JS-generated SVG now
  covered; `path` elements included in shape occlusion checks; computed-style
  visibility walk (reliable in Chromium).
- `scripts/render-check.mjs` (new) — Playwright runner: file:// navigation,
  console/pageerror capture (hard), broken subresource loads (hard; fetch/xhr
  advisory — file:// origins cannot fetch at all), fullPage screenshot,
  bounded settle (one 400ms beat, not a loop).
- text-escape check re-scoped: compares each text against EVERY direct rect
  of its group (a group may be a bar row with one rect per slot); only
  straddlers (partial intersection, not contained) are reported, and as
  advisory — strict escape checks belong to page-specific batteries that know
  the semantics. (This killed 12 false hards on the calibration artifact:
  multi-rect groups + captions straddling box edges by design.)
- `scripts/check-env.sh` — playwright module / chromium cache / system-lib
  ldd probe / sandbox feasibility; obscura checks removed.
- Calibration preserved: bad fixture FAIL (occlusion 1.0 / 0.58 hard),
  accepted artifact PASS 3/3 (0 hard, 3 advisory).

## 5. Why not dual-backend (obscura fallback)?

Considered and rejected: keeping obscura as a lightweight fallback doubles the
geometry code paths (real APIs vs attribute workaround) for little gain — the
node already carries the Chromium download, and a single mainstream engine is
cheaper to maintain than two engines plus a translation layer. obscura remains
installed for its original scraping purpose; the skill no longer depends on it.
