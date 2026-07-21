---
name: fetch-article
description: |
  Universal article fetcher. Route URL to the right adapter, output
  structured JSON. Supports WeChat (mp.weixin.qq.com), Bilibili video
  (dl only, no transcribe), and any other URL via Scrapling CLI with
  curl fallback.
---

# fetch-article

Fetch any URL → standard structured output. Adapts to each site's anti-bot
mechanisms.

## Quick Start

```bash
# Fetch any article
python3 .agent/skills/fetch-article/scripts/fetch.py \
  "https://mp.weixin.qq.com/s/xxx" \
  --json

# Fetch a generic webpage
python3 .agent/skills/fetch-article/scripts/fetch.py \
  "https://example.com/article" \
  --json

# Just get body text (no JSON wrapper)
python3 .agent/skills/fetch-article/scripts/fetch.py \
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
  "body_text": "Full article text...",
  "images": ["https://..."],
  "duration_sec": 0,
  "raw_path": "/tmp/fetch-article-xxx/"
}
```

## Domain Routing

| Pattern | Adapter | Strategy |
| --------- | --------- | ---------- |
| `mp.weixin.qq.com` | `adapters/weixin.py` | curl + Referer header → extract.py |
| `bilibili.com/video` | `adapters/bilibili.py` | WBI-signed API → download audio only |
| anything else | `adapters/generic.py` | Scrapling CLI first, curl + html2text fallback |

## Adapters

### WeChat (微信公众号)

Uses curl with a Referer header (critical — WeChat hotlink protection). Does
NOT execute JavaScript, which avoids the anti-bot captcha. Then calls
weixin-scraper's extract.py for structured output.

### Bilibili

Downloads audio via WBI-signed API. Only downloads — does NOT transcribe.
If CC subtitles are available, saves them directly (skip ASR).
Output includes `duration_sec` and `subs_available` fields.

See [bilibili-transcriber](../bilibili-transcriber/SKILL.md) for ASR.

### Generic (Scrapling + curl)

Try `scrapling extract get <URL> content.md` first. If Scrapling is not
installed or fails, fall back to `curl` + HTML tag stripping.

Scrapling handles:

- Cloudflare Turnstile / interstitial bypass
- TLS fingerprint simulation
- Auto Markdown output

Requires: `pip install "scrapling[all]"`

## Requirements

- Python 3.10+
- requests (for WBI-signed Bilibili API)
- scrapling (optional, for generic fallback with anti-bot)
- curl (system)

Install scrapling:

```bash
pip install "scrapling[all]"
scrapling install  # download browser dependencies
```
