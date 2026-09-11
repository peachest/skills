#!/usr/bin/env python3
"""Fake OpenAI-compatible server that captures what ocr actually sends.

Logs one JSON line per request (method, path, auth, parsed body) so callers can
prove whether extra_body fields (thinking-disable) reach the wire — reading
config files alone cannot prove this, because ocr silently ignores `llm.*`
settings when a provider is active.

Adapted from ~/projects/ocr-image/diagnostics/fake-llm-server.py.

Usage:
    python3 fake-llm-server.py [port] [log-path]
    # defaults: 8765, /tmp/fake-llm-requests.jsonl
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

LOG_PATH = "/tmp/fake-llm-requests.jsonl"


class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _handle(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8", "replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = {"_raw": raw[:200]}
        rec = {
            "method": self.command,
            "path": self.path,
            "auth": self.headers.get("Authorization", ""),
            "body": body,
        }
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        model = body.get("model", "fake") if isinstance(body, dict) else "fake"
        if isinstance(body, dict) and body.get("stream"):
            chunks = [
                {"id": "chatcmpl-fake", "object": "chat.completion.chunk", "created": 1,
                 "model": model, "choices": [{"index": 0, "delta": {"role": "assistant", "content": "ok"}, "finish_reason": None}]},
                {"id": "chatcmpl-fake", "object": "chat.completion.chunk", "created": 1,
                 "model": model, "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]},
            ]
            payload = "".join("data: " + json.dumps(c) + "\n\n" for c in chunks) + "data: [DONE]\n\n"
            data = payload.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        resp = {"id": "chatcmpl-fake", "object": "chat.completion", "created": 1, "model": model,
                "choices": [{"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}
        data = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        self._handle()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"data":[]}')


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    if len(sys.argv) > 2:
        LOG_PATH = sys.argv[2]
    open(LOG_PATH, "w").close()  # truncate on start so each run is clean
    server = HTTPServer(("127.0.0.1", port), H)
    print(f"listening on {port} (logging to {LOG_PATH})", flush=True)
    server.serve_forever()
