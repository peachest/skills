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

## Operational Notes

- **Script path**: `<SKILL_DIR>` is the single global install
  (`~/.pi/agent/skills/fetch-article/`). There is no project-local
  `.agent/skills/` copy — always invoke via the absolute `<SKILL_DIR>` path.
- **Timeouts**: `fetch.py` has no built-in timeout and bilibili downloads can
  exceed 2 min. Run long fetches (videos >30 min) through a background task
  with an explicit timeout (≥600s), not a foreground bash call.
- **Output root**: temp artifacts are written under `FETCH_ARTICLE_TMP_ROOT`
  (default `~/tmp`), never `/tmp`. Override the env var to relocate.
- **stdout purity**: with `--json`, stdout contains only the JSON payload;
  progress/diagnostic lines go to stderr, so `fetch.py <url> --json | jq`
  works directly.

## Output Format

```json
{
  "source": "weixin|bilibili|generic",
  "title": "Article title",
  "author": "Author/account name",
  "publish_time": "2026-06-03",
  "body_text": "# Title\n\nFull article in Markdown...",
  "images": ["https://..."],
  "md_path": "~/tmp/fetch-article-xxx/article.md",
  "duration_sec": 0,
  "raw_path": "~/tmp/fetch-article-xxx/"
}
```

Temp artifacts always go under `FETCH_ARTICLE_TMP_ROOT` (default `~/tmp`),
never `/tmp` — see Operational Notes.

## Domain Routing

| Pattern | Adapter | Strategy |
| --------- | --------- | ---------- |
| `mp.weixin.qq.com` | `adapters/weixin.py` | curl + Referer header → to_md.py (markitdown) |
| `bilibili.com/video` | `adapters/bilibili.py` | WBI-signed API → download audio only |
| `youtube.com` / `youtu.be` | `adapters/youtube.py` | yt-dlp subtitles if available, else best-audio download |
| anything else | `adapters/generic.py` | Scrapling CLI first, curl + html2text fallback, r.jina.ai reader proxy as last resort (Cloudflare bypass) |

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

### YouTube

yt-dlp based. Subtitles (manual preferred over auto) are the deliverable —
no audio download when present, the VTT is deduped into plain text. No
subtitles → downloads `bestaudio` as `audio.mp4` for ASR (set
`WHISPER_LANG=en` — the transcriber's default is zh). Proxy: export
`https_proxy` when YouTube is not directly reachable.

### Generic (Scrapling + curl + r.jina.ai)

Three-layer fallback chain:

1. `scrapling extract get <URL> content.md`
2. `curl` + HTML tag stripping — if the response is an anti-bot challenge
   page (Cloudflare "Enable JavaScript and cookies", "Just a moment", …),
   this layer reports failure and falls through
3. `r.jina.ai` reader proxy — `curl https://r.jina.ai/<URL>` returns the
   page as Markdown (`Title:` / `URL Source:` / `Markdown Content:`),
   bypassing Cloudflare-protected sites (verified against openai.com).
   No install needed; may rate-limit without a `JINA_API_KEY`.

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
- yt-dlp (for YouTube)
- scrapling (optional, for generic fallback with anti-bot)
- r.jina.ai (optional, no install — network fallback for Cloudflare-protected
  sites; set `JINA_API_KEY` to avoid anonymous rate limits)
- curl (system)

Install scrapling:

```bash
pip install "scrapling[all]"
scrapling install  # download browser dependencies
```
