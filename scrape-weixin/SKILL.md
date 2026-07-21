---
name: scrape-weixin
description: |
  Extract structured content from saved WeChat (微信) article HTML files
  (mp.weixin.qq.com). Use when the user wants to scrape web content from
  WeChat public accounts (微信公众号), or mentions: scrape, weixin, 爬取,
  微信公众号, 微信文章, 公众号文章. The actual fetching is handled by
  fetch-article skill — this skill only does the extraction step.
---

# WeChat Article Extractor

Extract structured content from a saved WeChat article HTML file.

## When to Use

You have a `.html` file already saved (from curl, browser, etc.) containing a
WeChat public account (微信公众号) article. This script extracts:

- **Title** — from `og:title` meta tag or `<h1 class="rich_media_title">`
- **Account name** — from `og:article:author` meta tag or `#js_name`
- **Publish date** — from `#publish_time` or `#meta_content`
- **Body text** — from `<div id="js_content">`, with HTML tags stripped
- **Images** — all `<img>` URLs from the content div

## Usage

```bash
python3 .agent/skills/scrape-weixin/scripts/extract.py /path/to/article.html
python3 .agent/skills/scrape-weixin/scripts/extract.py /path/to/article.html --json
python3 .agent/skills/scrape-weixin/scripts/extract.py /path/to/article.html --json --images
```

## Fetching the HTML

To fetch a WeChat article before extracting, use the fetch-article skill:

```bash
python3 .agent/skills/fetch-article/scripts/fetch.py \
  "https://mp.weixin.qq.com/s/xxx" \
  --json
```

fetch-article handles the full pipeline: curl with Referer header → save
HTML → call this extract.py. See [fetch-article](../fetch-article/SKILL.md).

## Background

WeChat's anti-bot detection runs entirely in JavaScript. The key insight:
WeChat articles are server-rendered (SSR). If you don't execute JS, you get
the full HTML without triggering the captcha (`wappoc_appmsgcaptcha`).

The `Referer: https://mp.weixin.qq.com/` header is critical — WeChat checks
it to prevent hotlinking.

## Failure Signs

| What you see | What it means |
|---|---|
| `wappoc_appmsgcaptcha` in HTML | JS captcha triggered — use curl instead of browser |
| `环境异常` in page text | Same — use curl |
| 301/302 redirect | Missing or wrong Referer header |
| 403 Forbidden | IP blocked or rate-limited |
| Empty body | HTML structure may have changed — inspect raw HTML |

## Limitations

- Comments and reading counts are loaded via XHR — not in static HTML
- Embedded videos/audio do not render in text output
- Heavy scraping triggers IP-based rate limiting