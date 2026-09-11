# Collection playbook

Gather topology data from a live cluster over ssh. Entry points: a bastion/jump host with kubectl (`ssh root@<host>`), or direct node access.

## Step 1 — Recon the entry host

```bash
ssh root@$HOST 'hostname; hostname -I; nvidia-smi -L | head -3; which iblinkinfo ibstat kubectl'
```

- No kubeconfig at `~/.kube/config`? Find it: `find /etc/kubernetes /root -maxdepth 3 -name "*.conf" -o -name "kubeconfig*"`. A master running kube-apiserver has one (`ps aux | grep apiserver` confirms masters).
- kubectl errors `invalid character '<'` ⇒ stale/broken kubeconfig, not an API outage — find the real one.

## Step 2 — Write the probe script LOCALLY, scp it up, run it

Never inline loops/redirects in `ssh host '...'` — quoting breaks and iteration is painful. Script template (adjust node lists):

```bash
# probe: find GPU nodes (no device plugin ⇒ no k8s GPU labels — must nvidia-smi probe every worker)
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' > all_nodes.txt
while read -r n <&3; do
  g=$(timeout 12 ssh -o BatchMode=yes root@"$n" "nvidia-smi -L 2>/dev/null | wc -l")
  [ "$g" != "0" ] && echo "$n $g" >> gpu_nodes.txt
done 3< all_nodes.txt
# per GPU node: nvidia-smi -L + topo -m; find one with iblinkinfo, run it once (fabric-wide view)
```

See the session-tested full script: `scripts/collect.sh` in this skill's directory.

## Gotchas (each cost a real bug)

- **zsh `=word` expansion**: on zsh nodes, `echo ===TOPO===` fails ("not found") and silently kills the rest of the command line. Always quote: `echo '===TOPO==='`. Symptom: file has GPU list but empty TOPO section.
- **iblinkinfo is fabric-wide**: run it ONCE from any node with the binary — it reports every host and switch via the subnet manager. Don't loop it per node.
- **Dual perspective**: iblinkinfo emits CA blocks (host→switch, has GUID+LID) AND switch blocks (switch port→host, LID 65535 = unassigned). Same physical links, two views — dedup on (node, node_port, switch_port).
- **stdin in while-read loops**: any command in the loop body that reads stdin eats the input file. Use `while read <&3 ... 3< file` (already in the template).
- **scp multi-glob pull fails silently**: `scp host:/a/pat* host:/b/pat* .` can return 0 with files missing. Pull patterns one at a time in a loop.
- **IB tools absent ≠ no IB**: node-A had zero IB binaries; node-B had them all. Probe, don't assume; collect fabric data from whichever node has `iblinkinfo`.

## Password auth (no public key)

`sshpass -p '<password>' ssh -o StrictHostKeyChecking=no root@$HOST` — credentials from the user, session-scoped, never written to disk. BatchMode=yes must be OFF for password, ON for jump-host→worker hops that already share keys.

## What to save

Everything under `<cluster>-data/`: raw `iblinkinfo.txt`, per-node `gpu_<node>.txt` (with quoted `===TOPO===` markers), `nodes.json` (kubectl), `mst status`. Raw files are the cross-check ground truth — keep them next to the demo.
