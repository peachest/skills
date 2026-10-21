#!/bin/bash
# 用法: shot-real.sh <P1|P2> <cnt>  — 前提: 对应 profile 已生效
# 截图内容 = 真实 kubectl 输出，零人工改写（长输出用真实管道截断）
set -e
P=$1; CNT=$2
SH=~/tmp/ppu-topo-test/shots-real
sed "s/PHASE/p$P/; s/CNT/$CNT/" ~/tmp/ppu-topo-test/test-pod-template.yaml | sudo kubectl apply -f - >/dev/null
while [ "$(sudo kubectl get pod ppu-topo-p$P-$CNT -o jsonpath='{.status.phase}' 2>/dev/null)" = "Pending" ]; do sleep 3; done
PHASE=$(sudo kubectl get pod ppu-topo-p$P-$CNT -o jsonpath='{.status.phase}')
# ── 段1: 真实 ConfigMap score 段（head 截断，不伪造）──
{
  echo "hyx@<node-a>:~$ sudo kubectl get cm mock-ppu-config -n llm-system -o yaml | sed -n '/score:/,\$p' | head -20"
  sudo kubectl get cm mock-ppu-config -n llm-system -o yaml | sed -n '/score:/,$p' | head -20
  echo "...  # 共 56 条双向 pair，完整内容见 evidence/mock-config-P$P.yaml"
} > /tmp/seg1.txt
# ── 段2: 真实 node annotation（完整 JSON）──
{
  echo "hyx@<node-a>:~$ sudo kubectl get node <node-a> -o jsonpath='{.metadata.annotations.hami\\.io/node-ppu-score}' | python3 -m json.tool"
  sudo kubectl get node <node-a> -o jsonpath='{.metadata.annotations.hami\.io/node-ppu-score}' | python3 -m json.tool
} > /tmp/seg2.txt
# ── 段3: 真实 pod annotations + resources（JSON 完整）──
{
  echo "hyx@<node-a>:~$ sudo kubectl get pod ppu-topo-p$P-$CNT -o jsonpath='{.metadata.annotations}' | python3 -m json.tool   # pod phase: $PHASE"
  sudo kubectl get pod ppu-topo-p$P-$CNT -o jsonpath='{.metadata.annotations}' | python3 -m json.tool
  echo "hyx@<node-a>:~$ sudo kubectl get pod ppu-topo-p$P-$CNT -o jsonpath='{.spec.containers[0].resources.limits}'"
  sudo kubectl get pod ppu-topo-p$P-$CNT -o jsonpath='{.spec.containers[0].resources.limits}' | python3 -m json.tool
} > /tmp/seg3.txt
sudo kubectl delete pod ppu-topo-p$P-$CNT >/dev/null 2>&1 || true
while sudo kubectl get pod ppu-topo-p$P-$CNT &>/dev/null; do sleep 3; done
cat /tmp/seg1.txt /tmp/seg2.txt /tmp/seg3.txt > $SH/p$P-$CNT-raw.txt
~/.local/bin/freeze --window --language bash -o $SH/p$P-$CNT.svg < $SH/p$P-$CNT-raw.txt
node ~/tools/playwright-runner/svg2png.mjs $SH/p$P-$CNT.svg $SH/p$P-$CNT.png
echo "DONE p$P-$CNT png=$(wc -c < $SH/p$P-$CNT.png) bytes"
sleep 12
