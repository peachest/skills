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

Route-table expressiveness (#61): a pattern may be method-scoped ("POST /notes"
matches only POSTs — GET and POST share URL substrings, so scoping is the only
way to fail a reply while the dedup/resolve GETs succeed), and a value may be
a dict {"status": 422, "file": "..."} to serve a non-200 status. Plain string
values keep the original 200 behavior.
"""


_HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
_REASONS = {200: "OK", 201: "Created", 404: "Not Found",
            422: "Unprocessable Entity", 500: "Internal Server Error"}

import json
import os
import sys


def request_method(argv):
    """Infer the HTTP method: curl passes -X (writes only, GET implied),
    gh api always passes --method."""
    for flag in ("-X", "--method"):
        if flag in argv:
            return argv[argv.index(flag) + 1].upper()
    if "-d" in argv or "--data" in argv:
        return "POST"  # curl -d implies POST
    return "GET"


def _log_request(argv, url, method):
    log_path = os.environ.get("FAKE_API_LOG")
    if not log_path:
        return
    entry = {"method": method, "url": url, "data": None}
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
    method = request_method(sys.argv[1:])
    _log_request(sys.argv[1:], url, method)
    for pattern, fixture in routes.items():
        route_method = None
        head, _, rest = pattern.partition(" ")
        if head in _HTTP_METHODS and rest:
            route_method, pattern = head, rest
        if pattern in url and route_method in (None, method):
            status = 200
            if isinstance(fixture, dict):
                status = fixture.get("status", 200)
                fixture = fixture.get("file")
            body = "{}"
            if fixture:
                with open(os.path.join(base, fixture)) as f:
                    body = f.read()
            sys.stdout.write(
                f"HTTP/1.1 {status} {_REASONS.get(status, 'Status')}\n"
                "Content-Type: application/json\n\n" + body + "\n"
            )
            return
    sys.stdout.write("HTTP/1.1 404 Not Found\nContent-Type: application/json\n\n{}\n")


if __name__ == "__main__":
    main()
