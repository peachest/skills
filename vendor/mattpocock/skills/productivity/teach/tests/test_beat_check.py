"""beat-check.py — structural invariant tests + a real before/after lesson."""

import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "assets" / "beat-check.py"
spec = importlib.util.spec_from_file_location("bc", SCRIPT)
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)


def run(tmp_path: Path, body: str) -> tuple[int, str]:
    f = tmp_path / "lesson.html"
    f.write_text(f"<html><body>{body}</body></html>", encoding="utf-8")
    import subprocess
    r = subprocess.run([sys.executable, str(SCRIPT), str(f)], capture_output=True, text=True)
    return r.returncode, r.stdout


GOOD = """
<h2>为什么 KV cache 这么占显存？</h2>
<p>想象一个 70B 的模型，每生成一个 token 都要重新算一遍所有注意力。这怎么可能快？</p>
<p>比如 batch=1 时，每层要存 4096×32 个头的历史向量。假设序列长度 2048，那就是
例如 512MB 的显存开销。让我们停下来想一想：这仨数字哪个最容易被砍？</p>
<p>我们定义 KV cache 为 \(C = 2 \\cdot n_{layer} \\cdot d \\cdot s\)。</p>
<p>现在你能解释开头 512MB 是怎么来的了吗？回到开头的问题：快的代价就是这块缓存。</p>
<p>想一想，如果序列长度翻倍，C 会怎么变？这个问题的答案就是下一讲的起点。</p>
<p>这个取舍空间正是 PagedAttention 等技术的立足点：不改变三个自由度本身，而是改变它们的组织方式。</p>
"""

BAD = """
<h2>KV Cache 的定义</h2>
<p>我们定义 KV cache 为 \\(C = 2 \\cdot n_{layer} \\cdot d \\cdot s\\)，其中各项为标准参数。</p>
<p>它是推理加速的核心机制。它的存在使注意力计算得以增量进行。它的容量规划是关键工程问题。</p>
<p>在实际的推理系统中，工程师需要根据模型规模和负载特征对缓存进行合理的容量规划与性能调优。</p>
<p>它的管理涉及显存分配、淘汰策略与量化压缩等多个方面，彼此耦合、相互制约。</p>
<p>此外，KV cache 的预热、迁移与多副本一致性也是生产环境中的常见工程课题，值得深入探讨与系统性地权衡。</p>
<p>在云原生部署形态下，这些课题进一步与弹性伸缩、成本核算相互交织，构成完整的容量管理体系。</p>
<p>总结：KV cache 很重要，需要认真对待。它是推理系统的核心组件之一。</p>
"""


def test_good_lesson_passes(tmp_path):
    rc, out = run(tmp_path, GOOD)
    assert rc == 0, out


def test_bad_lesson_flags_all(tmp_path):
    rc, out = run(tmp_path, BAD)
    assert rc == 1
    assert "concrete-first" in out
    assert "checkpoint" in out
    assert "callback" in out or "hook" in out


def test_definition_first_flagged(tmp_path):
    # has hook + checkpoint + callback, but formula before any concrete material
    body = BAD.replace("<h2>KV Cache 的定义</h2>", "<h2>为什么快？</h2>")
    rc, out = run(tmp_path, body)
    assert "concrete-first" in out


def test_short_prose_skipped(tmp_path):
    rc, out = run(tmp_path, "<p>太短</p>")
    assert rc == 0 and "SKIP" in out
