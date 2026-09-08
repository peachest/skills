#!/usr/bin/env node
// Playwright runner for html-render-check (render layer).
//
// Per artifact: load via file:// (relative asset paths resolve naturally —
// unlike an http.server rooted at the artifact's own directory, ../assets
// works), collect console/page errors and failed subresources, evaluate the
// generic battery, capture a full-page screenshot.
//
// Engine: real Chromium (headless shell). All geometry APIs work
// (getBoundingClientRect on SVG children included). Launch requires
// --no-sandbox on cluster/container nodes.
//
// Env:
//   PLAYWRIGHT_DIR   dir containing node_modules/playwright (default
//                    ~/tools/playwright-runner) — the skill repo is public
//                    and cannot ship node_modules.
//   PW_SANDBOX       "1" to allow the sandbox (default: --no-sandbox).
//   PW_VIEWPORT      WxH (default 1280x800).

import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import os from 'node:os';
import url from 'node:url';

const PLAYWRIGHT_DIR = process.env.PLAYWRIGHT_DIR ||
  path.join(os.homedir(), 'tools', 'playwright-runner');
const require2 = createRequire(path.join(PLAYWRIGHT_DIR, 'package.json'));
const { chromium } = require2('playwright');

// URL('.', import.meta.url) already resolves to the scripts directory
// (with trailing slash) — do NOT wrap in path.dirname, which strips the last
// segment of a trailing-slash path.
const SCRIPTS_DIR = url.fileURLToPath(new URL('.', import.meta.url));

// ---- args ------------------------------------------------------------------
const args = process.argv.slice(2);
const shotDir = (() => {
  const i = args.indexOf('--shot-dir');
  return i >= 0 ? args[i + 1] : null;
})();
const files = args.filter((a, i) => a !== '--shot-dir' && args[i - 1] !== '--shot-dir');
if (files.length === 0) {
  console.error('usage: render-check.mjs [--shot-dir DIR] <file.html>...');
  process.exit(2);
}

const batterySrc = fs.readFileSync(path.join(SCRIPTS_DIR, 'battery.js'), 'utf8');

// ---- main ------------------------------------------------------------------
const browser = await chromium.launch({
  args: process.env.PW_SANDBOX === '1' ? [] :
    ['--no-sandbox', '--disable-dev-shm-usage'],
});
let failed = 0;

for (const f of files) {
  if (!fs.existsSync(f)) {
    console.error(`FAIL ${f} — file not found`);
    failed++;
    continue;
  }
  const abs = path.resolve(f);
  const fileUrl = 'file://' + abs;
  const shotPath = path.join(shotDir || path.dirname(abs),
    path.basename(f, '.html') + '.render-check.png');

  const page = await browser.newPage({
    viewport: (() => {
      const m = (process.env.PW_VIEWPORT || '1280x800').match(/^(\d+)x(\d+)$/);
      return m ? { width: +m[1], height: +m[2] } : null;
    })(),
  });

  // Runtime evidence channels — attach before navigation.
  const jsErrors = [];      // console.error + uncaught page errors (hard)
  const netIssues = [];     // failed subresource loads
  page.on('console', (m) => { if (m.type() === 'error') jsErrors.push(m.text()); });
  page.on('pageerror', (e) => jsErrors.push('PAGEERROR: ' + e.message));
  page.on('response', (r) => {
    // fetch/xhr failures are advisory (a file:// origin cannot fetch() at
    // all, and self-contained lessons do not depend on them); broken
    // document/stylesheet/script/image loads are hard findings.
    const rt = r.request().resourceType();
    const hard = ['document', 'stylesheet', 'script', 'image', 'font'].includes(rt);
    if (r.status() >= 400) {
      netIssues.push({url: r.url().slice(0, 120), status: r.status(),
        type: rt, advisory: !hard});
    }
  });
  page.on('requestfailed', (r) => {
    const rt = r.resourceType();
    const hard = ['document', 'stylesheet', 'script', 'image', 'font'].includes(rt);
    netIssues.push({url: r.url().slice(0, 120), status: 0,
      error: (r.failure() || {}).errorText, type: rt, advisory: !hard});
  });

  let verdict = null;
  try {
    await page.goto(fileUrl, { waitUntil: 'load', timeout: 15000 });
    // Settle: animations/observers get a beat; bounded (one pass, not a loop).
    await page.waitForTimeout(400);
    verdict = JSON.parse(await page.evaluate(batterySrc));
  } catch (e) {
    console.error(`FAIL ${f} — load/eval error: ${String(e).slice(0, 200)}`);
    failed++;
    await page.close();
    continue;
  }

  // Merge runner-side evidence into the battery verdict.
  verdict.jsErrors = jsErrors;
  verdict.network = netIssues;
  const hardNet = netIssues.some((n) => !n.advisory);
  const ok = verdict.ok && jsErrors.length === 0 && !hardNet;

  try {
    await page.screenshot({ path: shotPath, fullPage: true });
  } catch (e) {
    console.error(`WARN screenshot failed for ${f}: ${String(e).slice(0, 100)}`);
  }
  await page.close();

  console.log(`== ${f}`);
  console.log(`render: ${JSON.stringify(verdict)}`);
  console.log(`shot:   ${shotPath}`);
  if (!ok) failed++;
}

await browser.close();
console.log('---');
if (failed === 0) {
  console.log(`RESULT: PASS (${files.length} artifact(s))`);
  process.exit(0);
} else {
  console.log(`RESULT: FAIL (${failed}/${files.length} artifact(s) with hard findings)`);
  console.log('Findings are adjudication prompts — inspect the screenshot evidence before editing.');
  process.exit(1);
}
