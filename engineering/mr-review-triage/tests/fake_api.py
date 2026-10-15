"""Offline platform-API stub, installed as fake curl/gh on PATH by conftest.

Emits responses in the `-i` wire shape (status line, blank line, JSON body)
that ocr_gitlab.curl() / ocr_github.curl() parse. The route table is a JSON
file at $FAKE_API_ROUTES mapping a URL substring to a fixture file (resolved
relative to the route file, first matching pattern wins). Unmatched URLs get
a 404 so best-effort calls (source-info lookup) degrade silently. Fully
offline — no sockets, no secrets; fixture ids are synthetic.

When $FAKE_API_LOG is set, every received request is appended there as JSON
lines (method/url/data) so tests can assert platform-call absence and inspect
posted bodies. Off by default — pull tests don't set it.
"""

import json
import os
import sys


def _log_request(argv, url):
    log_path = os.environ.get("FAKE_API_LOG")
    if not log_path:
        return
    entry = {"method": "GET", "url": url, "data": None}
    if "-X" in argv:
        entry["method"] = argv[argv.index("-X") + 1]
    if "-d" in argv:
        entry["data"] = argv[argv.index("-d") + 1]
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    routes_path = os.environ["FAKE_API_ROUTES"]
    with open(routes_path) as f:
        routes = json.load(f)
    base = os.path.dirname(routes_path)
    url = next(
        (a for a in sys.argv[1:] if a.startswith(("http://", "https://", "/"))),
        "",
    )
    _log_request(sys.argv[1:], url)
    for pattern, fixture in routes.items():
        if pattern in url:
            with open(os.path.join(base, fixture)) as f:
                body = f.read()
            sys.stdout.write(
                "HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + body + "\n"
            )
            return
    sys.stdout.write("HTTP/1.1 404 Not Found\nContent-Type: application/json\n\n{}\n")


if __name__ == "__main__":
    main()
