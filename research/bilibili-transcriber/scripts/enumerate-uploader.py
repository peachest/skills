#!/usr/bin/env python3
"""enumerate-uploader.py — enumerate an uploader's videos into a batch manifest.

Given a video BV id (resolves the uploader) or a user mid, lists every video
on their channel into a manifest that run-queue.sh consumes:
    [{"bvid": "BV1...", "title": "...", "duration": <sec>, "created": <unix>}]

Requires bilibili-api-python, which ships in the bilibili-cli uv tool:
    ~/.local/share/uv/tools/bilibili-cli/bin/python <this-script> ...
A Bilibili credential is REQUIRED (anonymous space-API calls hit risk control
and return HTTP 412).

Output is sorted by upload time (oldest first); run-queue.sh re-sorts by
duration anyway. Filter the manifest to taste before queueing.
"""

import argparse
import json
import sys
from pathlib import Path


def dur_sec(length: str) -> int:
    sec = 0
    for part in (length or "0:00").split(":"):
        sec = sec * 60 + int(part)
    return sec


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--bv", help="a video of the uploader (resolves mid)")
    src.add_argument("--mid", type=int, help="uploader user mid directly")
    ap.add_argument("--out", default="manifest.json", help="output manifest path")
    ap.add_argument(
        "--credential",
        default=str(Path.home() / ".bilibili-cli" / "credential.json"),
        help="bilibili credential.json (default: ~/.bilibili-cli/credential.json)",
    )
    args = ap.parse_args()

    try:
        from bilibili_api import Credential, sync, user, video
    except ImportError:
        print(
            "bilibili_api not importable. Run with the bilibili-cli tool venv:\n"
            "  ~/.local/share/uv/tools/bilibili-cli/bin/python "
            + str(Path(__file__).resolve())
            + " ...",
            file=sys.stderr,
        )
        return 2

    cred_path = Path(args.credential)
    if not cred_path.is_file():
        print(f"credential not found: {cred_path} (login via `bili login`)", file=sys.stderr)
        return 2
    c = json.loads(cred_path.read_text(encoding="utf-8"))
    cred = Credential(
        sessdata=c["sessdata"],
        bili_jct=c["bili_jct"],
        buvid3=c.get("buvid3", ""),
        dedeuserid=str(c.get("dedeuserid", "")),
    )

    try:
        if args.bv:
            info = sync(video.Video(args.bv).get_info())
            mid, name = info["owner"]["mid"], info["owner"]["name"]
        else:
            mid, name = args.mid, f"mid:{args.mid}"

        u = user.User(mid, credential=cred)
        videos, page = [], 1
        while True:
            r = sync(u.get_videos(pn=page, ps=50))
            vlist = r["list"]["vlist"]
            if not vlist:
                break
            videos.extend(vlist)
            if page * 50 >= r["page"]["count"]:
                break
            page += 1
    except Exception as e:  # network / risk-control surfaced as text
        print(f"enumeration failed: {e}", file=sys.stderr)
        return 1

    out = [
        {
            "bvid": v["bvid"],
            "title": v["title"],
            "duration": dur_sec(v.get("length", "0:00")),
            "created": v.get("created", 0),
        }
        for v in videos
    ]
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    total_min = sum(v["duration"] for v in out) // 60
    print(f"{name} (mid {mid}): {len(out)} videos, {total_min} min -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
