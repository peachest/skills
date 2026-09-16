# hf-download — Skill Impact Log

| Date | Proposal | Landing | Commit | Verification |
|------|----------|---------|--------|--------------|
| 2026-09-16 | Extracted from peer session 01a0a3b3 (DFlash2 checkpoint download): tool ladder hfd → hf download → aria2c single-file → curl-loop-last-resort (lesson recorded twice in that session after user corrections); hfd script sourced from ~/obsidianNote note (public hf-mirror script), shipped at scripts/hfd; gotcha: hfd --help exits 1, install checks must grep the banner not the exit code. | in-progress/hf-download/SKILL.md (new), scripts/{hfd,check-env.sh,runtime.conf.example} | (this commit) | check-env.sh PASS on workstation (curl 8.21/aria2c 1.37/jq/hfd/reachable); smoke-test procedure kept in SKILL.md |
