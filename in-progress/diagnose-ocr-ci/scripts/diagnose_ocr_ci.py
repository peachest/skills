# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Diagnose ocr-review runs: GitLab CI jobs (artifacts first, trace fallback),
group-level surveys, and local ocr sessions (~/.opencodereview/sessions).
Locate the failing layer of the layer ladder (pod -> before_script -> config
-> grouping -> per-file -> post -> artifacts).

Commands:
  jobs    <project>                    survey ocr-review jobs, failed first
  job     <project> <job-id>           single-job diagnosis (artifacts -> trace)
  durations <groups...>               success-job duration trend across groups
                                          (daily medians, optional --since split)
  analyze <path>                       analyze local ocr-result.json / ocr-stderr.log / trace files

Auth: token parsed from ~/.config/glab-cli/config.yml via yaml (regex parsing
is known to silently produce empty tokens -> 401).
"""

from __future__ import annotations

import argparse
import io
import os
import json
import re
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

GLAB_CONFIG = Path.home() / ".config" / "glab-cli" / "config.yml"
OCR_SESSIONS_DIR = Path.home() / ".opencodereview" / "sessions"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
RETRY_STATUS = {404, 429, 500, 502, 503, 504}
SLOW_REQUEST_MS = 120_000  # ≥2min with deadline error = timeout exhausted, not mid-stream cut
COMMON_REQUEST_TIMEOUTS_S = (60, 120, 180, 300, 600, 900, 1800)


def _infer_request_timeout_s(durs_ms: list[int]) -> int | None:
    """Infer the session's OCR_LLM_TIMEOUT from deadline-error durations:
    the largest cluster hugging a common timeout value."""
    best = None
    for d in durs_ms:
        for t in COMMON_REQUEST_TIMEOUTS_S:
            if d / 1000 >= t * 0.95:  # within 5% below/above
                best = max(best or 0, t)
    return best


PRIORITY = {
    "failed": 0,
    "canceled": 1,
    "success": 2,
    "running": 3,
    "pending": 4,
    "created": 4,
    "manual": 4,
    "skipped": 5,
}

# signature regex -> (layer_no, layer_name, diagnosis-zh)
# Post-processing rules (see analyze_text_signatures):
#   - L1 pod events are transient startup noise unless no deeper layer ever fired.
#   - L6 "posted N/N vs N/M" is refined with the captured counts.
TRACE_SIGNATURES: list[tuple[re.Pattern[str], int, str, str]] = [
    (
        re.compile(r"ContainersNotReady|init container .* not (ready|terminated)"),
        1,
        "Pod 调度",
        "runner pod 启动期事件：仅当后续层全部无输出（job 卡死在调度）时才是故障，否则为启动噪音",
    ),
    (
        re.compile(r"fatal: (repository .* not found|could not read from remote repository)"),
        2,
        "before_script",
        "git clone 失败：检查 common-ci 仓库权限或 CI_JOB_TOKEN",
    ),
    (
        re.compile(r"登录失败|获取 API Key 失败|vibecoding.*(failed|error)"),
        2,
        "before_script",
        "vibecoding_login.sh 登录失败：拿不到网关 API Key",
    ),
    (
        re.compile(r"Error: unknown provider field|Error: invalid.*config"),
        3,
        "ocr 配置",
        "ocr config set 报错：字段不在白名单或值非法",
    ),
    (
        re.compile(r"llm test.*(failed|✗)|Connection test failed|cannot connect"),
        3,
        "ocr 配置",
        "ocr llm test 连通性失败：网关 URL/token 配置错误",
    ),
    (
        re.compile(r"LLM grouping failed \(parse grouping JSON"),
        4,
        "grouping",
        "网关返回错误文本而非 JSON，grouping 失败已降级 per-file dispatch（非致命，但更慢）",
    ),
    (
        re.compile(r"Plan phase failed for group [\"'].+?[\"']"),
        5,
        "per-file 任务",
        "plan 阶段撞超时（context deadline exceeded），该组无 plan 继续执行",
    ),
    (
        re.compile(r"Subtask error for group [\"'].+?[\"'].*LLM completion error"),
        5,
        "per-file 任务",
        "该组主任务撞 per-file 超时（OCR_REVIEW_TIMEOUT），文件被切，run 为 partial",
    ),
    (
        re.compile(r"token budget.*reached|budget_exceeded|OCR_TOKENS_BUDGET"),
        5,
        "per-file 任务",
        "token 预算击穿：发布部分结果 exit 0，success 也可能是 partial",
    ),
    (
        re.compile(r"Successfully posted (\d+)/(\d+) inline comments"),
        6,
        "post 评论",
        "inline comment 发布结果",
    ),
]


def load_glab_hosts() -> list[tuple[str, str, str]]:
    """Return [(host, token, api_base)] for all hosts with tokens.
    Order: glab-config order by default; set OCR_CI_HOST_PRIORITY (comma-
    separated hostnames) to pin a preferred order.
    yaml only: regex token extraction is a known 401 trap."""
    cfg = yaml.safe_load(GLAB_CONFIG.read_text(encoding="utf-8"))
    hosts = cfg.get("hosts", {}) if isinstance(cfg, dict) else {}
    out: list[tuple[str, str, str]] = []
    for host, conf in hosts.items():
        token = conf.get("token") if isinstance(conf, dict) else None
        if not token:
            continue
        name = str(conf.get("host") or host).rstrip("/")
        base = name if "://" in name else f"https://{name}"
        out.append((str(host), str(token), f"{base}/api/v4"))
    if not out:
        raise SystemExit(f"no token found in {GLAB_CONFIG}")
    priority = [h for h in os.environ.get("OCR_CI_HOST_PRIORITY", "").split(",") if h]
    out.sort(key=lambda h: priority.index(h[0]) if h[0] in priority else len(priority))
    return out


def load_glab_auth() -> tuple[str, str]:
    """Single-host convenience: primary internal instance first."""
    _host, token, base = load_glab_hosts()[0]
    return token, base


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


class GitLabAPI:
    def __init__(self, host: str | None = None) -> None:
        all_hosts = load_glab_hosts()
        if host:
            match = [h for h in all_hosts if h[0] == host]
            if not match:
                names = ", ".join(h[0] for h in all_hosts)
                raise SystemExit(f"host {host!r} not in glab config (have: {names})")
            all_hosts = match
        self.hosts = all_hosts
        self.token, self.base = all_hosts[0][1], all_hosts[0][2]
        self.host = all_hosts[0][0]
        self.calls = 0

    def _get_on(self, base: str, token: str, path: str, retries: int = 5) -> tuple[int, bytes]:
        url = f"{base}/{path}"
        last_err: urllib.error.HTTPError | None = None
        for attempt in range(retries):
            req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": token})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    self.calls += 1
                    return resp.status, resp.read()
            except urllib.error.HTTPError as e:
                last_err = e
                # GitLab 404s flap; retry them briefly before believing them.
                if e.code in RETRY_STATUS and attempt < retries - 1:
                    time.sleep(min(2**attempt, 8))
                    continue
                return e.code, b""
            except OSError:
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
                raise
        assert last_err is not None
        return last_err.code, b""

    def get(self, path: str, retries: int = 5) -> tuple[int, bytes]:
        return self._get_on(self.base, self.token, path, retries)

    def get_json(self, path: str) -> object | None:
        status, body = self.get(path)
        if status != 200:
            return None
        return json.loads(body)

    def get_json_on(self, host: str, path: str, retries: int = 5) -> object | None:
        """GET json on a specific configured host (group survey scans multiple)."""
        match = [h for h in self.hosts if h[0] == host]
        if not match:
            return None
        _h, token, base = match[0]
        status, body = self._get_on(base, token, path, retries)
        if status != 200:
            return None
        return json.loads(body)

    def bind_host(self, host: str) -> None:
        match = [h for h in self.hosts if h[0] == host]
        if not match:
            raise SystemExit(f"host {host!r} not configured")
        self.host, self.token, self.base = match[0]

    def project_id(self, project: str) -> str:
        if project.isdigit():
            return project
        encoded = urllib.parse.quote(project, safe="")
        for host, token, base in self.hosts:
            req = urllib.request.Request(f"{base}/projects/{encoded}", headers={"PRIVATE-TOKEN": token})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    self.calls += 1
                    obj = json.load(resp)
                    self.host, self.token, self.base = host, token, base
                    assert isinstance(obj, dict)
                    return str(obj["id"])
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    raise
                continue
        raise SystemExit(
            f"project {project!r} not found on any configured host "
            f"({', '.join(h[0] for h in self.hosts)}); if the path has typos, "
            "try the numeric project ID (visible in runner pod names: runner-*-project-<ID>-*)"
        )


def extract_project_id_from_trace(trace: str) -> str | None:
    m = re.search(r"runner-\S*-project-(\d+)-concurrent", trace)
    return m.group(1) if m else None


# ── analyzers ──


def analyze_retry_report(rr: dict) -> list[str]:
    lines: list[str] = []
    for req in rr.get("requests", []):
        attempts = req.get("attempts", [])
        outcome = req.get("outcome", "?")
        task = req.get("task_type", "?")
        fpath = req.get("file_path", "?")
        codes = [a.get("status_code") for a in attempts]
        durs = [a.get("duration_to_headers_ms") for a in attempts]
        lines.append(
            f"  [{outcome}] {task} {fpath}: attempts={len(attempts)} status={codes} to_headers_ms={durs}"
        )
        for a in attempts:
            if a.get("error_class") == "timeout" and a.get("status_code") == 504:
                lines.append(
                    f"    → 504 且等满超时才断：网关挂死（duration_to_headers_ms={a.get('duration_to_headers_ms')}）"
                )
            if a.get("error_class") == "provider" and a.get("status_code") == 502 and outcome == "recovered":
                lines.append("    → 502 抖动后重试成功：SDK 重试兜住，非致命")
    return lines


def analyze_result_json(result: dict) -> list[str]:
    lines: list[str] = []
    status = result.get("status") or (result.get("manifest") or {}).get("terminal_state")
    cov = (result.get("manifest") or {}).get("coverage", {})
    s = result.get("summary", {})
    n_files = s.get("files_reviewed") or len(cov.get("selected", []))
    total_tokens = s.get("total_tokens", 0)
    tool_calls = (result.get("tool_calls") or {}).get("total", 0)
    lines.append(
        f"  terminal_state={status} files={n_files} comments={s.get('comments')} elapsed={s.get('elapsed')}"
    )
    if n_files:
        lines.append(
            f"  tokens/文件={total_tokens / n_files / 1000:.0f}k (基准 120–129k), "
            f"tool_calls/文件={tool_calls / n_files:.1f} (基准 ~10)"
        )
    for key in ("selected", "completed", "failed", "waived"):
        if cov.get(key):
            lines.append(f"  coverage.{key}: {len(cov[key])} 项")
    if cov.get("failed"):
        names = [
            str(i.get("label") or i.get("path") or i) if isinstance(i, dict) else str(i)
            for i in cov["failed"]
        ]
        lines.append(f"  失败文件: {', '.join(names[:10])}")
    rr = result.get("retry_report")
    if rr:
        lines.append(
            f"  retry_report: total={rr.get('total_requests')} retried={rr.get('retried_requests')} "
            f"recovered={rr.get('recovered_requests')} failed={rr.get('failed_requests')}"
        )
        lines.extend(analyze_retry_report(rr))
    if status == "partial":
        lines.append("  → run 为 partial：部分文件未完成但发布了部分结果")
    return lines


# progress markers (non-failure): how deep the job actually got.
PROGRESS_MARKERS: list[tuple[re.Pattern[str], int, str]] = [
    (re.compile(r"Connection test successful|LLM 连通性检查通过"), 3, "ocr 配置完成（llm test 通过）"),
    (
        re.compile(r"git fetch|FETCH_HEAD|Running.*review|\[ocr\]"),
        5,
        "进入 ocr 评审执行阶段",
    ),
    (re.compile(r"Successfully posted|Uploading artifacts"), 6, "评论发布/产物上传阶段"),
]


def name_by_pat(pat: re.Pattern[str]) -> str:
    for p, _l, n, _d in TRACE_SIGNATURES:
        if p is pat:
            return n
    return "?"


def analyze_text_signatures(text: str) -> tuple[list[str], int | None]:
    """Match layer signatures in stderr/trace. Returns (evidence lines, verdict layer)."""
    clean = strip_ansi(text)
    progress = 0
    progress_note = ""
    for pat, layer, note in PROGRESS_MARKERS:
        if pat.search(clean) and layer > progress:
            progress = layer
            progress_note = note
    hits: list[tuple[re.Pattern[str], int, int, str, list[str]]] = []  # (pat, layer, line_no, line, groups)
    for line_no, line in enumerate(clean.splitlines(), 1):
        for pat, layer, _name, _diag in TRACE_SIGNATURES:
            m = pat.search(line)
            if m:
                groups = [str(g) for g in m.groups() if g is not None]
                hits.append((pat, layer, line_no, line.strip()[:160], groups))
                break  # one signature per line
    deeper = [h for h in hits if h[1] > 1]
    lines: list[str] = []
    deepest: int | None = None
    seen: dict[re.Pattern[str], int] = {}
    diag_by_pat: dict[re.Pattern[str], str] = {p: d for p, _l, _n, d in TRACE_SIGNATURES}
    for pat, layer, line_no, line, groups in hits:
        seen[pat] = seen.get(pat, 0) + 1
        if layer == 1 and (deeper or progress >= 3):
            continue  # startup noise when the job clearly progressed past pod scheduling
        if seen[pat] > 1:
            continue  # dedupe: keep first occurrence, report count later
        is_failure = True
        if layer == 6 and len(groups) >= 2:
            n, m_tot = groups[0], groups[1]
            if n == m_tot:
                diag = f"inline comment 发布 {n}/{m_tot}：全部成功"
                is_failure = False
            else:
                diag = f"inline comment 发布 {n}/{m_tot}：部分失败（MR 已变更/权限/位置失效）"
        else:
            diag = diag_by_pat[pat]
        lines.append(f"  L{layer} {name_by_pat(pat)}: 行{line_no} 「{line}」 → {diag}")
        if is_failure:
            deepest = max(deepest or 0, layer)
    for pat, count in seen.items():
        if count > 1:
            layer = next(num for p, num, _n, _d in TRACE_SIGNATURES if p is pat)
            lines.append(f"  L{layer} 签名共命中 {count} 次（同类去重）")
    if progress:
        lines.append(f"  进度：到达 L{progress}（{progress_note}）")
    if deepest is None and progress >= 5:
        lines.append(
            f"  → trace 在 L{progress} 后无任何输出：--audience agent 陷阱（进度被丢）或网关挂死；"
            "结合 job duration 判断（~3600s = 旧 1h 硬超时）"
        )
        deepest = progress
    return lines, deepest


def hard_timeout_check(duration_s: float | int | None) -> list[str]:
    if duration_s and 3400 < duration_s < 3800:
        return [
            f"  job 时长 {duration_s:.0f}s ≈ 3600s → 旧配置 1h 硬超时签名（OCR_LLM_TIMEOUT=600 × 6 次尝试）"
        ]
    return []


# ── local ocr sessions (~/.opencodereview/sessions) ──


def _read_tail_json(path: Path, n: int = 3) -> list[dict]:
    """Read the last n JSON lines of a session file (cheap list-view probe)."""
    try:
        with path.open("rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 64_000))
            tail = f.read().decode("utf-8", errors="replace").strip().split("\n")
        out = []
        for line in tail[-n:]:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return out
    except OSError:
        return []


def _session_end_of(path: Path) -> dict | None:
    for j in reversed(_read_tail_json(path)):
        if j.get("type") == "session_end":
            return j
    return None


def find_local_session(target: str) -> Path:
    p = Path(target).expanduser()
    if p.is_file():
        return p
    matches = [f for f in OCR_SESSIONS_DIR.rglob("*.jsonl") if f.stem.startswith(target)]
    if not matches:
        raise SystemExit(f"no local ocr session matches {target!r} under {OCR_SESSIONS_DIR}")
    matches.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    if len(matches) > 1:
        print(f"{len(matches)} 个匹配，取最新：")
        for f in matches[:5]:
            print(f"  {f.parent.name}/{f.stem[:8]}")
    return matches[0]


def list_local_sessions(limit: int = 20) -> None:
    files = sorted(OCR_SESSIONS_DIR.rglob("*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        print(f"{OCR_SESSIONS_DIR} 下无 session")
        return
    rows = []
    for f in files[: max(limit * 3, 60)]:
        end = _session_end_of(f)
        if end is None:
            terminal = "中断"
            fails = -1
            dur = 0.0
        else:
            terminal = (end.get("run_manifest") or {}).get("terminal_state", "?")
            fails = end.get("llm_failures", 0)
            dur = end.get("duration_seconds", 0) or 0
        rows.append((terminal, f, fails, dur))
    order = {"failed": 0, "中断": 1, "partial": 2, "success": 3}
    rows.sort(key=lambda r: (order.get(r[0], 1), -r[1].stat().st_mtime))
    print(f"最近 {min(limit, len(rows))} 个本地 ocr session（失败优先）：")
    for terminal, f, fails, dur in rows[:limit]:
        mtime = time.strftime("%m-%d %H:%M", time.localtime(f.stat().st_mtime))
        proj = f.parent.name.replace("mnt-disk1-hyx-projects-", "")
        print(f"  {f.stem[:8]} [{terminal:7s}] fails={fails:>2} dur={dur:>6.0f}s {mtime} {proj}")


def analyze_local_session(path: Path) -> None:
    starts: list[dict] = []
    errors: list[dict] = []
    item_failed: list[dict] = []
    responses: list[dict] = []
    end: dict | None = None
    n_tool_calls = 0
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            j = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = j.get("type")
        if t == "session_start":
            starts.append(j)
        elif t == "llm_error":
            errors.append(j)
        elif t == "llm_response":
            responses.append(j)
        elif t == "review_item_failed":
            item_failed.append(j)
        elif t == "tool_call":
            n_tool_calls += 1
        elif t == "session_end":
            end = j

    print(f"== 本地 session {path.stem[:8]} ==")
    print(f"  文件: {path.parent.name}/{path.name}")
    if starts:
        s = starts[0]
        print(
            f"  开始: {str(s.get('timestamp', '?'))[:19]} cwd={s.get('cwd', '?')} "
            f"branch={s.get('gitBranch', '?')} model={s.get('model', '?')} "
            f"range={s.get('diffFrom', '?')}..{s.get('diffTo', '?')}"
        )

    lines: list[str] = []
    verdict: int | None = None
    deadline_durs = [
        e.get("duration_ms") or 0 for e in errors if "deadline exceeded" in str(e.get("error", ""))
    ]
    timeout_s = _infer_request_timeout_s(deadline_durs)
    if timeout_s:
        lines.append(f"  推断 OCR_LLM_TIMEOUT={timeout_s}s（从挂满时长聚类推断）")
    for e in errors:
        err = str(e.get("error", ""))
        dur = e.get("duration_ms") or 0
        task = e.get("taskType", "?")
        fpath = e.get("filePath", "?")
        if "deadline exceeded" in err and timeout_s and dur / 1000 >= timeout_s * 0.95:
            diag = f"L5 请求超时挂满 {dur / 1000:.0f}s（OCR_LLM_TIMEOUT={timeout_s}：网关挂死/TTFT 超限）"
            verdict = max(verdict or 0, 5)
        elif "deadline exceeded" in err and dur >= SLOW_REQUEST_MS:
            diag = f"L5 慢请求 {dur / 1000:.0f}s 被切（非请求超时挂满：per-file 循环期限到期取消或网关断流）"
            verdict = max(verdict or 0, 5)
        elif "deadline exceeded" in err:
            diag = f"L5 中途断流（{dur / 1000:.0f}s 即断，非等满超时：网关/流中断）"
            verdict = max(verdict or 0, 5)
        elif "grouping" in err and "parse" in err:
            diag = "L4 grouping 解析失败：网关返回错误文本而非 JSON，降级 per-file"
            verdict = max(verdict or 0, 4)
        elif "401" in err or "unauthorized" in err.lower():
            diag = "L3 鉴权失败：token 失效或未配置"
            verdict = max(verdict or 0, 3)
        elif "connect" in err.lower() or "refused" in err.lower() or "no route" in err.lower():
            diag = "L3 网络不通：网关地址错误或不可达"
            verdict = max(verdict or 0, 3)
        elif "429" in err or "rate" in err.lower():
            diag = "网关限流：降低 OCR_CONCURRENCY 或稍后重试"
        else:
            diag = f"未知错误类别（原文: {err[:60]}）"
        lines.append(f"  [llm_error] {task} {fpath}: {diag}")
    for it in item_failed:
        lines.append(f"  [item_failed] {it.get('filePath', '?')}: {str(it.get('error', ''))[:80]} → 文件被切")
        verdict = max(verdict or 0, 5)

    if responses:
        durs = sorted(r.get("duration_ms") or 0 for r in responses)
        mid = durs[len(durs) // 2]
        slow = sum(1 for d in durs if d >= SLOW_REQUEST_MS)
        toks = sum(
            (r.get("usage") or {}).get("prompt_tokens", 0)
            + (r.get("usage") or {}).get("completion_tokens", 0)
            for r in responses
        )
        n_files = len({r.get("filePath") for r in responses if r.get("filePath")}) or 1
        lines.append(
            f"  吞吐: {len(responses)} 次响应, 中位耗时 {mid / 1000:.0f}s, "
            f"≥120s 慢请求 {slow} 个, tokens≈{toks / 1000:.0f}k（{toks / n_files / 1000:.0f}k/文件, 基准 120–129k）, "
            f"tool_calls={n_tool_calls}（{n_tool_calls / n_files:.0f}/文件, 基准 ~10）"
        )
        if slow * 2 >= len(responses) and len(responses) >= 4:
            lines.append("  → 过半请求 ≥120s：网关侧延迟异常（对比正常 ~10-60s/请求）")
        per_file_k = toks / n_files / 1000
        if per_file_k > 260:
            lines.append(
                f"  → tokens/文件 {per_file_k:.0f}k 显著超基准 120–129k（>2x）：重复读文件/循环评审，值得抽查"
            )

    print("-- 错误与吞吐 --")
    for line in lines:
        print(line)

    print("-- 结局 --")
    if end is None:
        print("  无 session_end：进程被杀/手动中断（超时 kill 或 ctrl+c），未走到收尾")
    else:
        manifest = end.get("run_manifest") or {}
        terminal = manifest.get("terminal_state", "?")
        cov = manifest.get("coverage", {}) or {}
        print(
            f"  terminal_state={terminal} duration={end.get('duration_seconds', 0) or 0:.0f}s "
            f"files_reviewed={len(end.get('files_reviewed') or [])} llm_failures={end.get('llm_failures')}"
        )
        for key in ("selected", "completed", "failed", "waived"):
            if cov.get(key):
                print(f"  coverage.{key}: {len(cov[key])} 项")
        if terminal == "partial":
            print("  → partial：发布了部分结果（exit 0 语义）")
    if verdict:
        print(f"判定层级：L{verdict}（见 SKILL.md 层级表定位根因）")


def cmd_local(target: str | None, limit: int) -> None:
    if target is None:
        list_local_sessions(limit)
        return
    path = find_local_session(target)
    analyze_local_session(path)


# ── commands ──


def cmd_jobs(api: GitLabAPI, project: str) -> None:
    pid = api.project_id(project)
    jobs: list[dict] = []
    for page in (1, 2):
        chunk = api.get_json(f"projects/{pid}/jobs?per_page=100&page={page}")
        if not isinstance(chunk, list) or not chunk:
            break
        jobs.extend(chunk)
        if len(chunk) < 100:
            break
    ocr_jobs = [j for j in jobs if j.get("name") == "ocr-review"]
    ocr_jobs.sort(key=lambda j: (PRIORITY.get(j.get("status", ""), 9), -(j.get("id") or 0)))
    if not ocr_jobs:
        print(f"项目 {project} (id={pid}) 近 2 页无 ocr-review job")
        return
    print(f"项目 {project} (id={pid}) 的 {len(ocr_jobs)} 个 ocr-review job（失败优先）：")
    for j in ocr_jobs:
        print(
            f"  #{j['id']} [{j['status']:8s}] dur={float(j.get('duration') or 0):>7.0f}s "
            f"{j['created_at'][:16]} sha={j['commit']['id'][:8]} {j['commit']['title'][:50]}"
        )


def _fetch_artifacts(api: GitLabAPI, pid: str, job_id: int, out_dir: Path) -> Path | None:
    status, body = api.get(f"projects/{pid}/jobs/{job_id}/artifacts")
    if status != 200:
        return None
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(body)) as zf:
        zf.extractall(out_dir)
    return out_dir


def _analyze_files(named_texts: dict[str, str]) -> None:
    all_evidence: list[str] = []
    deepest: int | None = None
    for fname, text in named_texts.items():
        if fname.endswith("ocr-result.json"):
            print("-- ocr-result.json --")
            try:
                result = json.loads(text)
            except json.JSONDecodeError as e:
                print(f"  JSON 解析失败: {e}")
                continue
            all_evidence.extend(analyze_result_json(result))
        else:
            print(f"-- {fname} 签名 --")
            ev, layer = analyze_text_signatures(text)
            if not ev:
                print("  （无已知签名命中）")
            all_evidence.extend(ev)
            deepest = max(deepest or 0, layer) if layer else deepest
    print("-- 汇总 --")
    for line in all_evidence:
        print(line)
    if deepest:
        print(f"判定层级：L{deepest}（见 SKILL.md 层级表定位根因）")


def _analyze_dir(d: Path) -> None:
    named: dict[str, str] = {}
    for f in sorted(d.rglob("*")):
        if f.is_file() and (f.suffix in (".json", ".log") or f.name == "ocr-stderr.log"):
            named[f.name] = f.read_text(encoding="utf-8", errors="replace")
    if named:
        _analyze_files(named)


def cmd_job(api: GitLabAPI, project: str, job_id: int) -> None:
    pid = api.project_id(project)
    _diagnose_job(api, pid, job_id)


def _diagnose_job(api: GitLabAPI, pid: str, job_id: int) -> None:
    job = api.get_json(f"projects/{pid}/jobs/{job_id}")
    if not isinstance(job, dict):
        raise SystemExit(f"job {job_id} not found in project {pid}")
    print(f"== job #{job_id} ==")
    print(
        f"  status={job['status']} failure_reason={job.get('failure_reason')} "
        f"duration={job.get('duration')}s created={job['created_at']}"
    )
    print(f"  pipeline={job['pipeline']['id']} sha={job['commit']['id'][:12]} {job['commit']['title'][:60]}")
    for line in hard_timeout_check(job.get("duration")):
        print(line)
    out_dir = Path(f"/tmp/diagnose-ocr-ci/{job_id}")
    art_dir = _fetch_artifacts(api, pid, job_id, out_dir)
    if art_dir is not None:
        print(f"== artifacts（已解压 {art_dir}）==")
        for member in sorted(art_dir.rglob("*")):
            if member.is_file():
                print(f"  {member.relative_to(art_dir)} ({member.stat().st_size}B)")
        _analyze_dir(art_dir)
    else:
        print("== 无 artifacts（job 未走到上传步骤）→ 拉 trace ==")
        status, body = api.get(f"projects/{pid}/jobs/{job_id}/trace")
        if status != 200:
            raise SystemExit("trace 拉取失败")
        trace = strip_ansi(body.decode("utf-8", errors="replace"))
        out_dir.mkdir(parents=True, exist_ok=True)
        trace_file = out_dir / "trace.log"
        trace_file.write_text(trace, encoding="utf-8")
        print(
            f"  trace 已存 {trace_file}（{len(trace)}B, project_id 探测={extract_project_id_from_trace(trace)}）"
        )
        _analyze_files({"trace.log": trace})


# ── group survey ──


def _failure_class(job: dict) -> str:
    """Classify a failed job by failure_reason + duration signature."""
    fr = job.get("failure_reason") or ""
    dur = job.get("duration") or 0
    if fr == "job_execution_timeout":
        if 3400 <= dur <= 3800:
            return "job_execution_timeout≈3600s（旧配置 1h 硬超时签名）"
        if 7000 <= dur <= 7600:
            return "job_execution_timeout≈7200s（2h 硬超时签名）"
        return f"job_execution_timeout（{dur:.0f}s）"
    if fr == "runner_system_failure":
        return "runner_system_failure（L1 基础设施）"
    return fr or "unknown（需深诊）"


def _survey_project(api: GitLabAPI, host: str, project: dict) -> tuple[str, str, int, list[dict]] | None:
    jobs = api.get_json_on(host, f"projects/{project['id']}/jobs?per_page=100")
    if not isinstance(jobs, list):
        return None
    ocr = [j for j in jobs if j.get("name") == "ocr-review"]
    if not ocr:
        return None
    return (host, project["path_with_namespace"], project["id"], ocr)


def cmd_groups(api: GitLabAPI, groups: list[str], deep: int, pinned_host: str | None) -> None:
    hosts = [pinned_host] if pinned_host else [h[0] for h in api.hosts]
    # internal hosts only: gitlab.com is never the target of a group survey
    hosts = [h for h in hosts if not h.endswith("gitlab.com")]
    all_failed: dict[int, tuple[str, int, int]] = {}  # job_id -> (host, project_id, job_id), deduped
    for host in hosts:
        scanned, results = _scan_group_jobs(api, host, groups)
        n_jobs = sum(len(j) for _, _, _, j in results)
        label = "+".join(groups)
        print(
            f"== {host}/{label}：{scanned} 项目扫描（跨群组去重后），"
            f"{len(results)} 个有 ocr-review，{n_jobs} 个 job =="
        )
        if not results:
            continue
        rows = []
        failed_by_day: dict[str, int] = {}
        fail_classes: dict[str, int] = {}
        for host_, proj, pid, jobs in results:
            st: dict[str, int] = {}
            for j in jobs:
                st[j["status"]] = st.get(j["status"], 0) + 1
            rows.append((st.get("failed", 0), st.get("canceled", 0), proj, pid, jobs, st))
            for j in jobs:
                if j["status"] == "failed":
                    day = str(j["created_at"])[:10]
                    failed_by_day[day] = failed_by_day.get(day, 0) + 1
                    fc = _failure_class(j)
                    fail_classes[fc] = fail_classes.get(fc, 0) + 1
                    all_failed[j["id"]] = (host_, pid, j["id"])
        rows.sort(key=lambda r: (-r[0], -r[1], r[2]))
        print("-- 每项目状态（失败优先）--")
        for _n_failed, _n_canceled, proj, _pid, _jobs, st in rows:
            parts = " ".join(f"{k}={v}" for k, v in sorted(st.items()))
            print(f"  {proj:50s} {parts}")
        if fail_classes:
            print("-- 失败模式分类（时长签名聚类）--")
            for fc, n in sorted(fail_classes.items(), key=lambda kv: -kv[1]):
                print(f"  {n:>3} × {fc}")
        if failed_by_day:
            print("-- 按天失败分布（识别修复未合并窗口的持续损失）--")
            for day in sorted(failed_by_day):
                print(f"  {day}: {failed_by_day[day]}")
        running_long = [
            j
            for _, _, _, jobs in results
            for j in jobs
            if j["status"] == "running" and (j.get("duration") or 0) > 1800
        ]
        if running_long:
            print("-- 正在运行且超长 >30min（止损候选）--")
            for j in running_long:
                print(
                    f"  #{j['id']} dur={j.get('duration', 0):.0f}s {j['created_at'][:16]} {j['commit']['title'][:40]}"
                )
        print()
    if deep > 0 and all_failed:
        # most recent failed first: re-fetch with timestamps would cost another scan;
        # all_failed is in scan order, so just take the last N (scan is roughly chronological)
        print(f"== 深诊最近 {min(deep, len(all_failed))} 个失败 job ==")
        for host, pid, jid in list(all_failed.values())[-deep:]:
            api.bind_host(host)
            try:
                _diagnose_job(api, str(pid), jid)
            except SystemExit as e:
                print(f"  job {jid} 深诊失败: {e}")
            print()


def _scan_group_jobs(
    api: GitLabAPI, host: str, groups: list[str]
) -> tuple[int, list[tuple[str, str, int, list[dict]]]]:
    """Scan groups on one host, return (scanned_count, per-project ocr jobs, deduped)."""
    seen_pids: set[int] = set()
    results: list[tuple[str, str, int, list[dict]]] = []
    scanned = 0
    for group in groups:
        encoded = urllib.parse.quote(group, safe="")
        g = api.get_json_on(host, f"groups/{encoded}")
        if not isinstance(g, dict):
            print(f"== {host}/{group}：群组不存在，跳过 ==")
            continue
        projects: list[dict] = []
        for page in range(1, 11):
            chunk = api.get_json_on(
                host,
                f"groups/{g['id']}/projects?include_subgroups=true&simple=true&per_page=100&page={page}",
            )
            if not isinstance(chunk, list) or not chunk:
                break
            projects.extend(chunk)
            if len(chunk) < 100:
                break
        scanned += len(projects)

        def _survey_on(p: dict, _host: str = host) -> tuple[str, str, int, list[dict]] | None:
            return _survey_project(api, _host, p)

        with ThreadPoolExecutor(max_workers=12) as ex:
            for r in ex.map(_survey_on, projects):
                if not r:
                    continue
                _h, _proj, pid, _jobs = r
                if pid in seen_pids:
                    continue
                seen_pids.add(pid)
                results.append(r)
    return scanned, results


def cmd_durations(api: GitLabAPI, groups: list[str], since: str | None, pinned_host: str | None) -> None:
    """Success-job duration trend: is ocr-review getting faster or slower, and when did it shift."""
    from datetime import datetime

    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
        except ValueError as e:
            raise SystemExit(
                f"--since 无法解析: {since}（用 ISO 格式 2026-09-03T17:42 或 2026-09-03 17:42）"
            ) from e
        if since_dt.tzinfo is None:
            # job timestamps carry +08:00 on these internal GitLab instances;
            # a naive --since is interpreted as China time
            from datetime import timedelta, timezone

            since_dt = since_dt.replace(tzinfo=timezone(timedelta(hours=8)))

    hosts = [pinned_host] if pinned_host else [h[0] for h in api.hosts]
    hosts = [h for h in hosts if not h.endswith("gitlab.com")]
    for host in hosts:
        scanned, results = _scan_group_jobs(api, host, groups)
        succ = [
            (proj, j)
            for _h, proj, _pid, jobs in results
            for j in jobs
            if j.get("status") == "success" and j.get("duration")
        ]
        label = "+".join(groups)
        print(
            f"== {host}/{label}：{scanned} 项目扫描（跨群组去重后），"
            f"{len(results)} 个有 ocr-review，{len(succ)} 个成功 job 带时长 =="
        )
        if not succ:
            continue

        # daily medians — the primary speed-shift view
        print("-- 按天成功 job 时长中位数（min）--")
        byday: dict[str, list[float]] = {}
        for _proj, j in succ:
            byday.setdefault(str(j["created_at"])[:10], []).append(float(j["duration"]))
        for day in sorted(byday):
            ds = sorted(byday[day])
            p90 = ds[max(0, int(len(ds) * 0.9) - 1)]
            print(
                f"  {day}: n={len(ds):3d} median={statistics.median(ds) / 60:5.1f}  p90={p90 / 60:5.1f}  max={ds[-1] / 60:6.1f}"
            )

        if since_dt:

            def _parse(j: dict):
                return datetime.fromisoformat(str(j["created_at"]).replace("Z", "+00:00"))

            before = [(p, j) for p, j in succ if _parse(j) < since_dt]
            after = [(p, j) for p, j in succ if _parse(j) >= since_dt]

            def _stats(grp: list[tuple[str, dict]], name: str) -> None:
                if not grp:
                    print(f"{name}: 无数据")
                    return
                ds = sorted(float(j["duration"]) for _, j in grp)
                med = statistics.median(ds)
                p90 = ds[max(0, int(len(ds) * 0.9) - 1)]
                print(
                    f"  {name}: n={len(ds)} median={med / 60:.1f}min mean={statistics.mean(ds) / 60:.1f}min "
                    f"p90={p90 / 60:.1f}min max={ds[-1] / 60:.1f}"
                )

            print(f"-- since 分界（{since}）--")
            _stats(before, "BEFORE")
            _stats(after, "AFTER")
            if before and after:
                bm = statistics.median([float(j["duration"]) for _, j in before])
                am = statistics.median([float(j["duration"]) for _, j in after])
                ratio = bm / am if am else float("inf")
                verdict = "提速" if ratio > 1.3 else ("变慢" if ratio < 0.75 else "基本持平")
                print(f"  中位数变化: {bm / 60:.1f}min → {am / 60:.1f}min（{ratio:.1f}x，{verdict}）")

            # per-project after-period medians — locate the stragglers
            byproj: dict[str, list[float]] = {}
            for p, j in after:
                byproj.setdefault(p, []).append(float(j["duration"]))
            print("-- AFTER 期各项目中位数（min），最慢在前 --")
            for p, ds in sorted(byproj.items(), key=lambda kv: -statistics.median(kv[1])):
                print(f"  {p:50s} n={len(ds):3d} median={statistics.median(ds) / 60:5.1f}")
        print()


def cmd_analyze(path: Path) -> None:
    if path.is_dir():
        _analyze_dir(path)
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    _analyze_files({path.name: text})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", help="glab host to use (default: try internal hosts in order)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_jobs = sub.add_parser("jobs", help="survey ocr-review jobs of a project")
    p_jobs.add_argument("project")
    p_job = sub.add_parser("job", help="diagnose a single job")
    p_job.add_argument("project")
    p_job.add_argument("job_id", type=int)
    p_an = sub.add_parser("analyze", help="analyze local files (ocr-result.json / stderr / trace)")
    p_an.add_argument("path", type=Path)
    p_local = sub.add_parser("local", help="diagnose local ocr sessions (~/.opencodereview/sessions)")
    p_local.add_argument("target", nargs="?", help="session uuid prefix or jsonl path (omit to list recent)")
    p_local.add_argument("--limit", type=int, default=20)
    p_grp = sub.add_parser("groups", help="group-level survey: all ocr-review jobs across groups")
    p_grp.add_argument("groups", nargs="+", help="group paths, e.g. group-a group-b (cross-group dedup)")
    p_grp.add_argument("--deep", type=int, default=0, help="deep-diagnose the N most recent failed jobs")
    p_dur = sub.add_parser(
        "durations", help="success-job duration trend across groups (speed-shift detection)"
    )
    p_dur.add_argument("groups", nargs="+", help="group paths, e.g. group-a group-b")
    p_dur.add_argument(
        "--since",
        help="ISO timestamp split point (e.g. '2026-09-03 17:42' when a config merge landed)",
    )
    args = parser.parse_args()

    if args.cmd == "analyze":
        cmd_analyze(args.path)
        return
    if args.cmd == "local":
        cmd_local(args.target, args.limit)
        return
    api = GitLabAPI(host=args.host)
    if args.cmd == "groups":
        cmd_groups(api, args.groups, args.deep, args.host)
    elif args.cmd == "durations":
        cmd_durations(api, args.groups, args.since, args.host)
    elif args.cmd == "jobs":
        cmd_jobs(api, args.project)
    else:
        cmd_job(api, args.project, args.job_id)


if __name__ == "__main__":
    main()
