"""Shared async OpenAI-compatible chat client — replaces 4 per-script copies.

Covers: /chat/completions URL join, optional Bearer auth, reasoning-effort
knob (chat_template_kwargs), retry ladder (linear backoff 2s, 4s, …), and
markdown-fence stripping. Vision payloads: the caller puts image_url parts
in messages — this client never inspects message content.
"""
import asyncio

import aiohttp


def chat_url(baseurl: str) -> str:
    return baseurl.rstrip("/") + "/chat/completions"


def build_headers(key: str = "") -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    return headers


def build_payload(model: str, messages: list, *, temperature: float = 0.0,
                  max_tokens: int = 32000, extra: dict | None = None,
                  effort: str = "") -> dict:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if extra:
        payload.update(extra)
    if effort:
        # GLM-5.3 reasoning knob: thinking cannot be disabled; low effort is
        # the only speed lever (5.5x measured). Harmless to omit otherwise.
        payload["chat_template_kwargs"] = {"reasoning_effort": effort}
    return payload


def strip_fence(text: str) -> str:
    if text.startswith("```"):
        text = text.strip("`").lstrip("\n")
    return text


async def chat(sess: aiohttp.ClientSession, *, baseurl: str, model: str,
               key: str = "", messages: list, temperature: float = 0.0,
               max_tokens: int = 32000, effort: str = "",
               extra: dict | None = None, timeout: int = 300,
               retries: int = 3) -> str:
    """One chat completion with the shared retry ladder. Raises after the last attempt."""
    payload = build_payload(model, messages, temperature=temperature,
                            max_tokens=max_tokens, extra=extra, effort=effort)
    headers = build_headers(key)
    url = chat_url(baseurl)
    for attempt in range(retries):
        try:
            async with sess.post(url, json=payload, headers=headers,
                                 timeout=aiohttp.ClientTimeout(total=timeout)) as r:
                if r.status != 200:
                    raise RuntimeError(f"HTTP {r.status}: {(await r.text())[:200]}")
                out = (await r.json())["choices"][0]["message"]["content"].strip()
            return strip_fence(out)
        except Exception:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(2 * (attempt + 1))


async def chat_once(*args, **kwargs) -> str:
    """Ephemeral-session variant for sync callers (slides OCR): one call on its
    own ClientSession. Wrap in asyncio.run()."""
    async with aiohttp.ClientSession() as sess:
        return await chat(sess, *args, **kwargs)
