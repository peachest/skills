#!/usr/bin/env node
// Attach to a running playwright-cli daemon browser via CDP and stream its
// current page as an MJPEG feed. Change-driven: idle pages cost ~0 bandwidth.
//
// Usage: node screencast-mjpeg.js --cdp-port 9333 --listen 8081 [--quality 70] [--max-width 1280]
//
// Endpoints:
//   /         status page with embedded feed
//   /stream   multipart/x-mixed-replace MJPEG (open directly or via <img>)
//
// Never kills the daemon on exit (connectOverCDP detach only).

const { chromium } = require(process.env.PLAYWRIGHT_CLI_RUNNER
  ? process.env.PLAYWRIGHT_CLI_RUNNER + '/node_modules/playwright'
  : '/mnt/disk1/hyx/tools/playwright-runner/node_modules/playwright');
const http = require('http');

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : def;
}
const cdpPort = arg('cdp-port', '9333');
const listen = parseInt(arg('listen', '8081'), 10);
const quality = parseInt(arg('quality', '70'), 10);
const maxWidth = parseInt(arg('max-width', '1280'), 10);

(async () => {
  const browser = await chromium.connectOverCDP(`http://127.0.0.1:${cdpPort}`);
  const ctx = browser.contexts()[0];
  if (!ctx) { console.error('no context found on daemon (is it running?)'); process.exit(1); }

  let frameCount = 0, totalBytes = 0, clients = 0;
  let lastFrame = null; // latest JPEG buffer, sent to new clients immediately
  let activeCdp = null;  // CDP session of the currently streamed page
  const castParams = () => ({ format: 'jpeg', quality, maxWidth, maxHeight: Math.round(maxWidth * 0.625), everyNthFrame: 1 });

  function newSession(page) {
    const cdp = ctx.newCDPSession(page).then(async cdp => {
      cdp.on('Page.screencastFrame', async ev => {
        frameCount++; totalBytes += ev.data.length;
        const buf = Buffer.from(ev.data, 'base64');
        lastFrame = buf;
        // Chrome's multipart/x-mixed-replace parser only finalizes a part when it sees
        // the NEXT boundary — sending each frame twice makes every frame display
        // immediately (the 2nd copy's boundary finalizes the 1st).
        for (const res of waiters) {
          try {
            res.write(framePart(buf)); res.write(buf); res.write('\r\n');
            res.write(framePart(buf)); res.write(buf); res.write('\r\n');
          } catch {}
        }
        await cdp.send('Page.screencastFrameAck', { sessionId: ev.sessionId }).catch(() => {});
      });
      activeCdp = cdp;
      await cdp.send('Page.startScreencast', castParams());
      sessions.add(cdp);
    }).catch(() => {});
    return cdp;
  }

  // RFC 2046: the boundary delimiter must be preceded by CRLF — Chrome's MJPEG decoder
  // fails to find subsequent frames without the trailing CRLF after each JPEG body.
  const framePart = buf => `--frame\r\nContent-Type: image/jpeg\r\nContent-Length: ${buf.length}\r\n\r\n`;
  const waiters = new Set();
  const sessions = new Set();

  // screencast the active page; re-attach when pages change
  let currentPage = ctx.pages()[0];
  if (currentPage) newSession(currentPage);
  ctx.on('page', p => { currentPage = p; newSession(p); });

  const server = http.createServer((req, res) => {
    if (req.url === '/stream') {
      clients++;
      res.writeHead(200, { 'Content-Type': 'multipart/x-mixed-replace; boundary=frame', 'Cache-Control': 'no-cache', 'Connection': 'close' });
      waiters.add(res);
      // Idle pages are change-driven, and the FIRST frame after attach can be blank
      // (compositor not ready). Re-issuing startScreencast forces a fresh frame of
      // the CURRENT page state — every new client gets a real picture immediately.
      if (activeCdp) activeCdp.send('Page.startScreencast', castParams()).catch(() => {});
      // Belt and braces: last known frame right away (see double-send note above).
      if (lastFrame) { try {
        res.write(framePart(lastFrame)); res.write(lastFrame); res.write('\r\n');
        res.write(framePart(lastFrame)); res.write(lastFrame); res.write('\r\n');
      } catch {} }
      req.on('close', () => { waiters.delete(res); clients--; });
    } else if (req.url === '/status') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ cdpPort, page: currentPage ? currentPage.url() : null, frames: frameCount, kb: Math.round(totalBytes / 1024), clients }));
    } else {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>agent browser view</title></head>
<body style="margin:0;background:#111"><img src="/stream" style="width:100%">
<p style="color:#ccc;font-family:monospace">cdp=${cdpPort} frames=${frameCount} clients=${clients} <a style="color:#7af" href="/status">status</a></p></body></html>`);
    }
  });
  server.listen(listen, '0.0.0.0', () => {
    console.log(`MJPEG screencast: http://0.0.0.0:${listen}/ (attached to daemon CDP :${cdpPort})`);
  });

  const bye = async () => {
    for (const s of sessions) { try { await s.detach(); } catch {} }
    server.close(); process.exit(0);
  };
  process.on('SIGINT', bye); process.on('SIGTERM', bye);
})().catch(e => { console.error('FATAL:', e.message); process.exit(1); });
