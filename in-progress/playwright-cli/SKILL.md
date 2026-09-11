---
name: playwright-cli
description: Drive a headless browser from the agent node via the Playwright CLI (@playwright/cli daemon) — page interaction, storage state, tracing, and live MJPEG screencast observation. Use when the task needs to open, click, read, or watch a real browser on any internal or external web app, when a web platform must be logged into and operated, or when browser behavior (console/network/rendering) must be inspected. Also use when a Playwright CLI command fails unexpectedly on this node (proxy hijack, --config scope, sandbox flags).
---

# playwright-cli — agent browser control on cluster nodes

Playwright CLI (`@playwright/cli`) is a daemon-based browser driver designed for coding agents: the first command starts a persistent browser process, every command prints a trimmed page state plus an accessibility-tree snapshot file with element refs (`f1e10`), and follow-up commands operate on those refs deterministically.

**Upstream usage doc is the single source of truth for command syntax** — read it before writing any command you have not used before:

- `~/tools/playwright-cli/node_modules/@playwright/cli/skills/playwright-cli/SKILL.md` (all commands, quick start)
- Same directory `references/`: `session-management.md`, `storage-state.md`, `tracing.md`, `running-code.md` (one file per topic, load only the one you need)

This skill adds what the upstream doc does not know: running headless on a proxied cluster node, attaching observation tooling to the daemon, and the raw-script fallback.

## Setup facts (this node)

- Binary: `~/tools/playwright-cli/node_modules/.bin/playwright-cli` (npm-installed latest; version check in `scripts/check-env.sh`)
- Playwright library for scripts: `require('~/tools/playwright-runner/node_modules/playwright')` (v1.63, chromium headless shell in `~/.cache/ms-playwright`)
- Cluster nodes require `--no-sandbox`; internal portals use self-signed certs (`ignoreHTTPSErrors`)

## Node pitfalls (verified by experiment — do not rediscover)

1. **Proxy hijack.** The node may export an `http_proxy` pointing at the corporate proxy. Chromium picks it up and CONNECT-tunnels internal IPs; the proxy cuts some tunnels mid-TLS (`net::ERR_CONNECTION_CLOSED`), while curl looks fine. `--no-proxy-server` **does not work** (daemon still proxies, confirmed via netlog). Fixes, either one:
   - target IPs are in `no_proxy` (preferred, persistent in `~/.config/proxy.env`; verify with `curl -s --noproxy '*' <url>` first), or
   - sanitize the env at spawn time: `http_proxy= https_proxy= HTTP_PROXY= HTTPS_PROXY= all_proxy= playwright-cli open <url>`
2. **`--config` only applies to commands that (re)launch the browser** (`open`, `state-load`+`open`). Plain `snapshot`/`goto`/`tab-list` reject it — config is baked into the daemon at open time.
3. **`open` is a one-shot launcher.** Calling `open <url>` a second time on a running session kills the daemon and respawns it WITHOUT the config (defaults to a missing `chrome` and dies). After the initial `open`, navigate with `goto <url>` only.
4. **`--remote-debugging-port` coexists with playwright's pipe.** Adding it to `launchOptions.args` in the config file opens a standard CDP HTTP endpoint on the daemon browser, which observation scripts attach to (`chromium.connectOverCDP`). This is how screencast sees the same page the CLI operates.
5. **Daemon browsers die with their parent session** — do not expect a daemon started in one agent session to survive into another. Storage state files are the persistence layer, not the daemon.

## Standard flow

```bash
PW=~/tools/playwright-cli/node_modules/.bin/playwright-cli

# 1. launch daemon with a config (headless, no-sandbox, cert-tolerant, CDP port for observation)
$PW --config=<config.json> -s=<session-name> open <url>

# 2. operate via snapshot refs
$PW -s=<session-name> snapshot        # prints yaml with refs
$PW -s=<session-name> fill <ref> <text>
$PW -s=<session-name> click <ref>

# 3. credentials: either load a saved storage state then open, or fill the login form by ref
$PW -s=<session-name> state-load <state.json> && $PW -s=<session-name> open <url>

# 4. teardown when done (frees the browser process)
$PW -s=<session-name> close
```

`-s=<name>` isolates parallel browsers (one per target site). Config file shape:

```json
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": { "headless": true, "args": ["--no-sandbox", "--remote-debugging-port=<cdp-port>"] },
    "contextOptions": { "ignoreHTTPSErrors": true }
  }
}
```

## Live observation (screencast + trace)

While a daemon runs with a CDP port open, attach and stream what it renders:

```bash
node <skill-dir>/scripts/screencast-mjpeg.js --cdp-port <cdp-port> --listen <mjpeg-port>
```

- Serves `http://<node>:<mjpeg-port>/` — a status page plus `<img src="/stream">` MJPEG feed. Forward the port (VS Code Ports panel) and open it in a local browser to watch the agent's headless page in real time.
- Frames are change-driven: an idle page costs zero bandwidth; interaction bursts stream at sub-second latency.
- `chromium.connectOverCDP` attach/detach never kills the daemon browser.
- Known MJPEG behaviors baked into the script (do not "simplify" them away): every frame is written twice — Chrome's multipart parser only displays a part after it sees the NEXT boundary; each part needs a trailing CRLF before the boundary; on client connect the script re-issues `Page.startScreencast` because the first frame after attach can be blank and idle pages never produce another one.
- A long-idle SPA tab can render blank (compositor drops state) — if the feed shows white, `goto` any URL to force a repaint before suspecting the stream.

For post-hoc or live **traces**, use the CLI's built-in tracing (`tracing-start` / operate / `tracing-stop`), or attach `context.tracing.start({live: true})` to the daemon like `~/.cache/platform-browser/live-trace.js` does. Serve a **live trace** with:

```bash
# CRITICAL: pass the artifacts DIRECTORY, not the .trace file — the viewer's
# service worker only unzips .trace.zip files; raw .trace streams need the
# directory backend (server joins the tracesDirMarker itself).
(cd <artifacts-dir> && npx playwright show-trace . --host 0.0.0.0 --port 9323)
```

Refresh the viewer tab to pick up newly written trace entries.

For platform-specific orchestration (login state per cluster, session registry, start/stop lifecycle) use the `platform-browser` skill, which wraps this one.

## Raw-script fallback

When the CLI cannot express the task (bulk capture, response-body harvesting, WebSocket frames, performance metrics), write a one-off node script against the playwright library instead of fighting the CLI:

```js
const { chromium } = require(process.env.RUNNER + '/node_modules/playwright'); // RUNNER=~/tools/playwright-runner
const env = { ...process.env, http_proxy: '', https_proxy: '', HTTP_PROXY: '', HTTPS_PROXY: '', all_proxy: '', ALL_PROXY: '' };
const browser = await chromium.launch({ args: ['--no-sandbox'], env });
const ctx = await browser.newContext({ ignoreHTTPSErrors: true });
```

Same proxy sanitization rules apply. For diagnostics capture (console/network/HAR/metrics harness), see the `platform-browser` skill.

## Environment checks

`bash scripts/check-env.sh` verifies binary presence, version, playwright-runner, and chromium install. Run it first when browser commands misbehave.
