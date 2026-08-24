---
name: fetch-article
description: |
  Universal article fetcher. Route URL to the right adapter, output
  Markdown for machine reading. Supports WeChat (mp.weixin.qq.com),
  Bilibili video (dl only, no transcribe), and any other URL via
  Scrapling CLI with curl fallback.
---

# fetch-article

Fetch any URL → Markdown output. Adapts to each site's anti-bot
mechanisms.

## Quick Start

```bash
# Fetch a WeChat article → Markdown JSON
python3 <SKILL_DIR>/scripts/fetch.py \
  "https://mp.weixin.qq.com/s/xxx" \
  --json

# Fetch a generic webpage
python3 <SKILL_DIR>/scripts/fetch.py \
  "https://example.com/article" \
  --json

# Just get body Markdown (no JSON wrapper)
python3 <SKILL_DIR>/scripts/fetch.py \
  "https://example.com/article" \
  --text
```

## Output Format

```json
{
  "source": "weixin|bilibili|generic",
  "title": "Article title",
  "author": "Author/account name",
  "publish_time": "2026-06-03",
  "body_text": "# Title\n\nFull article in Markdown...",
  "images": ["https://..."],
  "md_path": "/tmp/fetch-article-xxx/article.md",
  "duration_sec": 0,
  "raw_path": "/tmp/fetch-article-xxx/"
}
```

## Domain Routing

| Pattern | Adapter | Strategy |
| --------- | --------- | ---------- |
| `mp.weixin.qq.com` | `adapters/weixin.py` | curl + Referer header → to_md.py (markitdown) |
| `bilibili.com/video` | `adapters/bilibili.py` | WBI-signed API → download audio only |
| anything else | `adapters/generic.py` | Scrapling CLI first, curl + html2text fallback |

## Adapters

### WeChat (微信公众号)

Uses curl with a Referer header (critical — WeChat hotlink protection). Does
NOT execute JavaScript, which avoids the anti-bot captcha. Then calls
`to_md.py` which uses `markitdown` to convert HTML to Markdown and `bs4` to
extract metadata (title, author, publish_time, images).

### Bilibili

Downloads audio via WBI-signed API. Only downloads — does NOT transcribe.
If CC subtitles are available, saves them directly (skip ASR).
Output includes `duration_sec`, `stream_type`, `content_length`, and `subs_available` fields.

See [bilibili-transcriber](../bilibili-transcriber/SKILL.md) for ASR.

### Generic (Scrapling + curl)

Try `scrapling extract get <URL> content.md` first. If Scrapling is not
installed or fails, fall back to `curl` + HTML tag stripping.

Scrapling handles:

- Cloudflare Turnstile / interstitial bypass
- TLS fingerprint simulation
- Auto Markdown output

Requires: `pip install "scrapling[all]"`

## HTML → Markdown Conversion

The `to_md.py` script is a reusable HTML→Markdown converter:

```bash
python3 <SKILL_DIR>/scripts/to_md.py /path/to/article.html --images
```

It uses `markitdown` CLI for body conversion and `beautifulsoup4` for
metadata extraction. Currently used by the WeChat adapter; other adapters
can adopt it as needed.

## Requirements

- Python 3.10+
- markitdown (`pip install markitdown`)
- beautifulsoup4 (`pip install beautifulsoup4`)
- requests (for WBI-signed Bilibili API)
- scrapling (optional, for generic fallback with anti-bot)
- curl (system)

Install scrapling:

```bash
pip install "scrapling[all]"
scrapling install  # download browser dependencies
```
