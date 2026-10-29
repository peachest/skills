#!/usr/bin/env python3
"""wiki ledger (skill-impact.md) 校验 — 三模式共用：

  pre-commit   ①skill↔wiki 配对：skill 目录有 staged 变更则对应 wiki/<name>/skill-impact.md
                 必须同时 staged（纯排版/错别字修复用 --no-verify 跳过）
               ②staged ledger 新增行格式：四列表格、无占位符、commit 列禁裸 hash
  commit-msg   台账新行（date==今天）且同 commit 改了对应 skill 文件 →
               commit 列必须等于本 commit subject 原文（subject 锚点一致性）
  pre-push     锚点可检索性（防漂移）：
               date>=EFFECTIVE 行：commit 列必须能 `git log -F --grep` 命中（subject 锚点）
               date<  EFFECTIVE 行：commit 列裸 hash 必须仍存在（filter-repo drift 检测）

约定（见 wiki/README.md skill-impact 节）：
  - 新行 commit 列 = 本 commit subject 原文（多锚点用 "; " 分隔）
  - `—`/空/(above)/"见 git log" 为豁免值
  - date < EFFECTIVE(2026-10-28) 的行是 legacy，不做 subject 检查
"""
import os
import re
import subprocess
import sys
import time

EFFECTIVE = "2026-10-28"
TODAY = time.strftime("%Y-%m-%d")
SKILL_ROOTS = ("in-progress", "engineering", "research", "productivity")
EXEMPT_COL3 = {"—", "-", "", "(above)"}
LEDGER_ROW = re.compile(r"^\|\s*20\d\d-\d\d-\d\d\s*\|")
# 裸 hash：前后不是 hex/路径字符；排除 range 左端（c55ee46..49dd158 的左值）
HASH_RE = re.compile(r"(?<![0-9a-zA-Z./])[0-9a-f]{7,40}(?!\.|[0-9a-zA-Z])")
# pi session id 形态（01a0xxxx/01a1xxxx，uuid v7 前缀）不是 commit hash
SESSION_ID_RE = re.compile(r"\b01a[0-9a-f]{5}\b")
PLACEHOLDER_RE = re.compile(r"\(this commit\)|（this commit）|「this commit」|\(本次\)", re.I)
LEDGER_RE_PATH = re.compile(r"^wiki/[^/]+/skill-impact\.md$")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def staged_files():
    out = git("diff", "--cached", "--name-only").stdout
    return [l.strip() for l in out.splitlines() if l.strip()]


def skill_of(path):
    parts = path.split("/")
    if len(parts) >= 3 and parts[0] in SKILL_ROOTS and parts[1]:
        return parts[1]
    return None


def added_ledger_lines(path):
    """staged 台账行变更 [(line_body, is_new)]。
    is_new：以 date 列为配对键 —— 同 diff 内存在同 date 的删除行则为修改行（回填/考据），
    否则为真正新增行（subject 锚点规则的校验对象）。"""
    if not os.path.exists(path):
        return []
    out = git("diff", "--cached", "--unified=0", "--", path).stdout
    removed_dates = set()
    added = []
    for line in out.splitlines():
        if line.startswith("-") and not line.startswith("---"):
            m = LEDGER_ROW.match(line[1:])
            if m:
                cells = re.split(r"(?<!\\)\|", line[1:])
                if len(cells) > 1:
                    removed_dates.add(cells[1].strip())
        elif line.startswith("+") and not line.startswith("+++"):
            body = line[1:]
            if LEDGER_ROW.match(body):
                added.append(body)
    rows = []
    for body in added:
        cells = re.split(r"(?<!\\)\|", body)
        date = cells[1].strip() if len(cells) > 1 else ""
        rows.append((body, date not in removed_dates))
    return rows


def split_row(line):
    """| date | ... | commit | verification | → cells（容忍单元格内转义 |）。
    schema 无关取列：4 列正典与 5 列变体（含 Landing 列）的 commit 列均为 cells[-3]，
    verification 均为 cells[-2]。"""
    return re.split(r"(?<!\\)\|", line)


def resolves_subject(text):
    """git 全历史按固定串检索 commit message；命中返回 True"""
    r = git("log", "-F", "--grep", text, "-1", "--format=%h")
    return r.returncode == 0 and r.stdout.strip()


def hash_exists(h):
    return git("cat-file", "-e", h + "^{commit}").returncode == 0


def pre_commit():
    errors = []
    files = staged_files()
    skills = {s for f in files if (s := skill_of(f))}

    # ① 配对：skill 目录 staged → 对应台账必须 staged
    for s in sorted(skills):
        ledger = f"wiki/{s}/skill-impact.md"
        if ledger not in files:
            errors.append(
                f"[wiki-pair] skill 目录 '{s}/' 有 staged 变更，但 {ledger} 未同时变更。\n"
                f"           补一行台账（commit 列写本次 commit subject），\n"
                f"           或确认是纯排版/错别字修复后用 git commit --no-verify 跳过。"
            )

    # ② staged ledger 新增行格式
    for f in files:
        if not LEDGER_RE_PATH.match(f):
            continue
        for body, is_new in added_ledger_lines(f):
            if PLACEHOLDER_RE.search(body):
                errors.append(f"[wiki-fmt] {f}: 台账行含占位符（this commit/本次）——commit 列写本 commit 的 subject 原文")
            cells = split_row(body)
            if len(cells) < 5:
                errors.append(f"[wiki-fmt] {f}: 台账行需 4 列（date|proposal|commit|verification）: {body[:80]}")
                continue
            date = cells[1].strip()
            col3 = cells[-3].strip()
            col4 = cells[-2].strip()
            if is_new and date >= EFFECTIVE:
                if col3 not in EXEMPT_COL3 and "git log" not in col3:
                    bare = [m.group() for m in HASH_RE.finditer(col3) if not SESSION_ID_RE.fullmatch(m.group())]
                    if bare:
                        errors.append(f"[wiki-fmt] {f}: 新规范行 commit 列禁止裸 hash（{bare[0]}）——写 commit subject 原文")
            if is_new and not col4:
                errors.append(f"[wiki-fmt] {f}: 台账行 verification 列为空——写验证方式与结果")

    return errors


def commit_msg(msgfile):
    errors = []
    subject = None
    for line in open(msgfile, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if line.strip() and not line.startswith("#"):
            subject = line.strip()
            break
    if not subject:
        return []  # 空 message 让 git 自己报错

    files = staged_files()
    skills_staged = {s for f in files if (s := skill_of(f))}

    for f in files:
        if not LEDGER_RE_PATH.match(f):
            continue
        skill = f.split("/")[1]
        if skill not in skills_staged:
            continue  # wiki-only 维护 commit（legacy 回填/归一）不查相等性
        for body, is_new in added_ledger_lines(f):
            if not is_new:
                continue  # 修改行（回填/考据）不受 subject 相等约束
            cells = split_row(body)
            if len(cells) < 5:
                continue
            date = cells[1].strip()
            col3 = cells[-3].strip().replace("\\|", "|")  # unescape cell-escaped pipes
            if date == TODAY and col3 not in EXEMPT_COL3 and col3 != subject:
                errors.append(
                    f"[wiki-anchor] {f}: 台账新行 commit 列与本次 commit subject 不一致。\n"
                    f"  行内: {col3[:90]}\n"
                    f"  应为: {subject}\n"
                    f"  （回填历史行请把 date 写成被记账 commit 的日期，不要写今天）"
                )
    return errors


def pre_push():
    errors = []
    for f in git("ls-tree", "-r", "--name-only", "HEAD").stdout.splitlines():
        if not LEDGER_RE_PATH.match(f):
            continue
        content = git("show", f"HEAD:{f}").stdout
        for i, line in enumerate(content.splitlines(), 1):
            if not LEDGER_ROW.match(line):
                continue
            cells = split_row(line)
            if len(cells) < 5:
                continue
            date = cells[1].strip()
            col3 = cells[-3].strip()
            if col3 in EXEMPT_COL3 or col3.startswith("见 git log"):
                continue
            if date >= EFFECTIVE:
                # subject 锚点：整体可检索（多锚点 "; " 分隔）
                for anchor in col3.split(";"):
                    anchor = anchor.strip().replace("\\|", "|")  # unescape cell-escaped pipes (same as wiki-anchor)
                    if not anchor or anchor in EXEMPT_COL3 or anchor.startswith("见 git log"):
                        continue
                    bare = [m.group() for m in HASH_RE.finditer(anchor) if not SESSION_ID_RE.fullmatch(m.group())]
                    if bare:
                        errors.append(f"[wiki-drift] {f}:{i} 新规范行含裸 hash，应改为 subject: {col3[:70]}")
                    elif not resolves_subject(anchor):
                        errors.append(
                            f"[wiki-drift] {f}:{i} commit 列在 git 历史中检索不到（漂移/笔误），请重新维护：\n"
                            f"    「{anchor[:90]}」\n"
                            f"    用 git log --oneline 找到真实 subject；若历史被 filter-repo 改写，参考 .git/filter-repo/commit-map"
                        )
            else:
                # legacy 行：hash 存在性检查（filter-repo / squash drift 检测）
                for m in HASH_RE.finditer(col3):
                    h = m.group()
                    if SESSION_ID_RE.fullmatch(h):
                        continue  # subject 里嵌的 pi session id，非 commit 引用
                    if not hash_exists(h):
                        errors.append(
                            f"[wiki-drift] {f}:{i} legacy 行 hash {h} 在本仓已不存在（历史改写/squash？），请重新维护：\n"
                            f"    参考 .git/filter-repo/commit-map 做新旧映射，或按 message/内容考据"
                        )
    return errors


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "pre-commit":
        errors = pre_commit()
    elif mode == "commit-msg":
        errors = commit_msg(sys.argv[2]) if len(sys.argv) > 2 else []
    elif mode == "pre-push":
        errors = pre_push()
    else:
        print(f"usage: {sys.argv[0]} pre-commit|commit-msg <msgfile>|pre-push", file=sys.stderr)
        return 2
    for e in errors:
        print(f"BLOCKED — {e}", file=sys.stderr)
    if errors:
        print(f"\n({len(errors)} 个 wiki 校验错误；确属误报/特例可用 --no-verify 跳过，但请在台账说明)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
