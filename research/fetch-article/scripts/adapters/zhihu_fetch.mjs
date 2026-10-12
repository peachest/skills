// Zhihu zhuanlan fetcher — run by adapters/zhihu.py via node.
// Loads login cookies from ZHIHU_COOKIE_FILE, fetches the article in
// Chromium (playwright resolved from ZHIHU_RUNNER_DIR/node_modules),
// outputs one JSON object to stdout.
//
// Why this shape: zhihu blocks non-browser TLS fingerprints (curl → 403)
// and serves {"code":40362} to cookie-less headless browsers. Working
// recipe (2026-09-23): real Chromium + injected cookies + NO proxy env
// (the local proxy fails with ERR_TUNNEL_CONNECTION_FAILED to zhihu).
import { createRequire } from 'module';
import { readFileSync } from 'fs';

const runnerDir = process.env.ZHIHU_RUNNER_DIR;
const cookieFile = process.env.ZHIHU_COOKIE_FILE;
const articleId = process.env.ZHIHU_ARTICLE_ID;

const fail = (error) => { console.log(JSON.stringify({ error })); process.exit(0); };

if (!runnerDir || !cookieFile || !articleId) fail('missing ZHIHU_RUNNER_DIR / ZHIHU_COOKIE_FILE / ZHIHU_ARTICLE_ID env');

let cookieStr;
try {
  cookieStr = readFileSync(cookieFile, 'utf8').trim();
} catch {
  fail(`cookie file not readable: ${cookieFile}`);
}
if (!cookieStr) fail(`cookie file is empty: ${cookieFile}`);

const require = createRequire(runnerDir + '/');
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch (e) {
  fail(`playwright not loadable from ${runnerDir}: ${e.message.split('\n')[0]}`);
}

const cookies = cookieStr.split('; ').map((p) => {
  const i = p.indexOf('=');
  return { name: p.slice(0, i), value: p.slice(i + 1), domain: '.zhihu.com', path: '/' };
});

const browser = await chromium.launch({ args: ['--no-sandbox'] });
try {
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0',
    viewport: { width: 1366, height: 900 },
    locale: 'zh-CN',
  });
  await ctx.addCookies(cookies);
  const page = await ctx.newPage();
  const resp = await page.goto(`https://zhuanlan.zhihu.com/p/${articleId}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(2500);

  const bodyText = await page.evaluate(() => document.body.innerText);
  if ((resp && resp.status() !== 200) || bodyText.includes('安全验证') || bodyText.includes('"code":40362')) {
    fail('zhihu blocked the fetch (40362/CAPTCHA) — login cookie likely expired; ask user for a fresh cookie (z_c0, d_c0, __zse_ck)');
  }

  const data = await page.evaluate(() => {
    const pick = (sel) => document.querySelector(sel)?.innerText.trim() || '';
    const title = pick('h1.Post-Title');
    const author = pick('.AuthorInfo-name');
    const timeRaw = pick('.ContentItem-time'); // e.g. "发布于 2026-09-20"
    const htmlEl = document.querySelector('.Post-RichTextContainer .RichText, .Post-RichTextContainer, .RichText');
    return {
      title,
      author,
      publish_time: timeRaw.replace(/^发布于\s*/, ''),
      html: htmlEl ? htmlEl.innerHTML : '',
    };
  });

  if (!data.html || !data.title) fail('article nodes not found — page layout may have changed or cookie rejected');
  console.log(JSON.stringify({ ...data, http_status: resp ? resp.status() : 0 }));
} finally {
  await browser.close();
}
