"""Offline platform-API stub, installed as fake curl/gh on PATH by conftest.

Emits responses in the `-i` wire shape (status line, blank line, JSON body)
that ocr_gitlab.curl() / ocr_github.curl() parse. The route table is a JSON
file at $FAKE_API_ROUTES mapping a URL substring to a fixture file (resolved
relative to the route file, first matching pattern wins). Unmatched URLs get
a 404 so best-effort calls (source-info lookup) degrade silently. Fully
offline — no sockets, no secrets; fixture ids are synthetic.
"""

import json
import os
import sys


def main():
    routes_path = os.environ["FAKE_API_ROUTES"]
    with open(routes_path) as f:
        routes = json.load(f)
    base = os.path.dirname(routes_path)
    url = next(
        (a for a in sys.argv[1:] if a.startswith(("http://", "https://", "/"))),
        "",
    )
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
