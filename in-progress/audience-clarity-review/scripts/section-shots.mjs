#!/usr/bin/env node
// Section-level screenshots for audience-clarity-review.
//
// One fullPage shot plus one shot per top-level section, so a vision-capable
// reviewer sees each section at readable scale instead of one 8000px-tall
// image. Emits manifest.json mapping each shot to its heading text.
//
// Runtime: same as html-render-check — Playwright under PLAYWRIGHT_DIR
// (default ~/tools/playwright-runner), PW_SANDBOX=1 to allow sandbox.
//
// usage: section-shots.mjs --out-dir DIR <file.html>

import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import os from 'node:os';

const PLAYWRIGHT_DIR = process.env.PLAYWRIGHT_DIR ||
  path.join(os.homedir(), 'tools', 'playwright-runner');
const require2 = createRequire(path.join(PLAYWRIGHT_DIR, 'package.json'));
const { chromium } = require2('playwright');

const args = process.argv.slice(2);
const outDir = (() => {
  const i = args.indexOf('--out-dir');
  return i >= 0 ? args[i + 1] : null;
})();
const files = args.filter((a, i) => a !== '--out-dir' && args[i - 1] !== '--out-dir');
if (!outDir || files.length !== 1) {
  console.error('usage: section-shots.mjs --out-dir DIR <file.html>');
  process.exit(2);
}
fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({
  args: process.env.PW_SANDBOX === '1' ? [] :
    ['--no-sandbox', '--disable-dev-shm-usage'],
});

const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
await page.goto('file://' + path.resolve(files[0]), { waitUntil: 'load', timeout: 15000 });
await page.waitForTimeout(400);

const base = path.basename(files[0], '.html');
const manifest = { fullPage: `${base}.full.png`, sections: [] };

await page.screenshot({ path: path.join(outDir, manifest.fullPage), fullPage: true });

const sections = await page.$$('section, article');
if (sections.length === 0) {
  console.log('No <section>/<article> elements found; fullPage shot only.');
} else {
  for (let i = 0; i < sections.length; i++) {
    const heading = await sections[i].$('h1,h2,h3,h4');
    const title = heading ? (await heading.textContent()).trim().slice(0, 80) : `section ${i + 1}`;
    const file = `${base}.s${String(i + 1).padStart(2, '0')}.png`;
    try {
      await sections[i].screenshot({ path: path.join(outDir, file) });
      manifest.sections.push({ file, title });
    } catch (e) {
      console.log(`WARN shot failed for section ${i + 1}: ${String(e).slice(0, 100)}`);
    }
  }
}

fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify(manifest, null, 2));
console.log(`manifest: ${path.join(outDir, 'manifest.json')}`);
console.log(`sections: ${manifest.sections.length}, fullPage: ${manifest.fullPage}`);
await browser.close();
