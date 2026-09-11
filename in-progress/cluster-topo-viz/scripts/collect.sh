#!/bin/bash
# Cluster topology collection — run on a bastion/master with kubectl + ssh to workers.
# Outputs to /tmp/cluster-topo/. Session-tested on the 93 production cluster.
set -u
OUT=/tmp/cluster-topo
mkdir -p "$OUT"

# 1. Node list (master kubeconfig may need export KUBECONFIG=...)
kubectl get nodes -o json > "$OUT/nodes.json" 2>/dev/null
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' > "$OUT/all_nodes.txt"

# 2. GPU node probe — no device plugin means no k8s GPU labels; must nvidia-smi every worker.
> "$OUT/gpu_nodes.txt"
while read -r n <&3; do
  case "$n" in *master*|ceph-*) continue;; esac   # adjust: skip known non-GPU nodes by name
  g=$(timeout 12 ssh -o BatchMode=yes -o ConnectTimeout=4 -o StrictHostKeyChecking=no root@"$n" \
        "nvidia-smi -L 2>/dev/null | wc -l" < /dev/null)
  if [ -n "$g" ] && [ "$g" != "0" ] 2>/dev/null; then
    echo "$n $g" >> "$OUT/gpu_nodes.txt"
  fi
done 3< "$OUT/all_nodes.txt"

# 3. Per-GPU-node topology. NOTE: echo markers MUST be quoted (zsh =word expansion).
while read -r n g <&3; do
  timeout 30 ssh -o BatchMode=yes -o StrictHostKeyChecking=no root@"$n" \
    "hostname; nvidia-smi -L; echo '===TOPO==='; nvidia-smi topo -m; echo '===IBSTAT-L==='; ibstat -l 2>/dev/null" \
    > "$OUT/gpu_${n}.txt" 2>&1 < /dev/null
done 3< "$OUT/gpu_nodes.txt"

# 4. IB fabric — run ONCE from the first node that has iblinkinfo (fabric-wide view via subnet manager).
IBNODE=""
while read -r n g <&3; do
  if timeout 10 ssh -o BatchMode=yes -o ConnectTimeout=4 root@"$n" "which iblinkinfo >/dev/null 2>&1" < /dev/null; then
    IBNODE="$n"; break
  fi
done 3< "$OUT/gpu_nodes.txt"
if [ -n "$IBNODE" ]; then
  timeout 90 ssh -o BatchMode=yes root@"$IBNODE" "iblinkinfo" > "$OUT/iblinkinfo.txt" 2>&1 < /dev/null
  timeout 90 ssh -o BatchMode=yes root@"$IBNODE" "ibstat"      > "$OUT/ibstat.txt" 2>&1 < /dev/null
  timeout 90 ssh -o BatchMode=yes root@"$IBNODE" "mst status"  > "$OUT/mst_status.txt" 2>&1 < /dev/null
fi

echo "done: $(ls "$OUT" | wc -l) files in $OUT"
