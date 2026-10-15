"""Offline platform-API stub, installed as fake curl/gh on PATH by conftest.

Emits responses in the `-i` wire shape (status line, blank line, JSON body)
that ocr_gitlab.curl() / ocr_github.curl() parse. The route table is a JSON
file at $FAKE_API_ROUTES mapping a URL substring to a fixture file (resolved
relative to the route file, first matching pattern wins). Unmatched URLs get
a 404 so best-effort calls (source-info lookup) degrade silently. Fully
offline — no sockets, no secrets; fixture ids are synthetic.

When $FAKE_API_LOG is set, every received request is appended there as JSON
lines (method/url/data/vars) so tests can assert platform-call absence and
inspect posted bodies. `gh api graphql -f query=...` invocations carry no
URL: the route pattern matches against the query text and the payload is
emitted as bare JSON (real gh prints no header block on graphql); an
unmatched graphql query answers {"errors": [...]} so callers fail closed.
Off by default — pull tests don't set it.

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
    elif "--input" in argv:  # gh api POST/PUT bodies ride stdin (`--input -`)
        entry["data"] = sys.stdin.read()
    fvars = {}
    for i, a in enumerate(argv):
        if a == "-F" and i + 1 < len(argv) and "=" in argv[i + 1]:
            k, v = argv[i + 1].split("=", 1)
            fvars[k] = v
    if fvars:
        entry["vars"] = fvars
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def _graphql_query(argv):
    """The -f query=<text> payload of a `gh api graphql` invocation ('' if absent)."""
    for i, a in enumerate(argv):
        if a == "-f" and i + 1 < len(argv) and argv[i + 1].startswith("query="):
            return argv[i + 1][len("query="):]
    return ""


def main():
    routes_path = os.environ["FAKE_API_ROUTES"]
    with open(routes_path) as f:
        routes = json.load(f)
    base = os.path.dirname(routes_path)
    argv = sys.argv[1:]
    # `gh api graphql -f query=...` carries no URL and real gh prints the bare
    # JSON payload (no -i header block) — route patterns match against the
    # query text and the response is emitted without a status line (#62).
    is_graphql = "graphql" in argv
    if is_graphql:
        url = _graphql_query(argv)
        method = "GRAPHQL"
    else:
        url = next(
            (a for a in argv if a.startswith(("http://", "https://", "/"))),
            "",
        )
        method = request_method(argv)
    _log_request(argv, url, method)
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
            if is_graphql:
                sys.stdout.write(body)
            else:
                sys.stdout.write(
                    f"HTTP/1.1 {status} {_REASONS.get(status, 'Status')}\n"
                    "Content-Type: application/json\n\n" + body + "\n"
                )
            return
    if is_graphql:
        sys.stdout.write('{"errors": [{"message": "fake_api: no route matched this graphql query"}]}')
    else:
        sys.stdout.write("HTTP/1.1 404 Not Found\nContent-Type: application/json\n\n{}\n")


if __name__ == "__main__":
    main()
