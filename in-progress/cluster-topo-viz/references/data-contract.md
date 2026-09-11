# Data contract

`topology.json` is the single normalized input the renderer consumes. All keys English; values as collected.

## Shape

```jsonc
{
  "fabric": {                          // inter-node IB (omit layer if no IB data)
    "nodes": {                          // keyed by host group name
      "h11": { "ports": [
        { "sw": "switch8", "sw_port": 12, "state": "Active" } ] }
    },
    "switches": {                       // keyed by switch name
      "switch8": { "lid": 2, "uplinks": 21, "active": 21, "hosts": ["h11", "..."] }
    }
  },
  "fabricA": ["switch8", "..."],       // plane membership; one array per fabric plane
  "fabricB": ["switch4", "..."],
  "gpuNodes": ["h11", "..."],           // every node with GPUs, sorted
  "gpu": {                              // keyed by node name
    "h11": { "gpus": 8, "model": "H100-80GB-HBM3",
              "nv": { "NV18": 56 } }    // nv kinds × count (bidirectional pairs counted twice)
  },
  "k8sNodes": ["ceph-03", "..."],       // optional: k8s membership for role marking
  "masters": ["ceph-03", "..."]
}
```

## Field semantics

- `nv` values: `NV18`/`NV12` (NVLink via NVSwitch — full mesh), `PIX`/`PXB` (same PCIe switch), `NODE` (same NUMA), `SYS` (cross socket). A degraded node (dead GPU) shows a MIX like `{"NV18":42,"PIX":1,"NODE":3,"SYS":3}` — that mix is the anomaly signal, keep it.
- `gpus < 8` (or < the node's slot count) marks a degraded node → red border, `--down` accents.
- `state`: `Active` (solid line), `Initialize` (dashed, `--init`) — physical link present, protocol not negotiated / LID unassigned.
- Switch `hosts` lists every host with ≥1 port on that switch — powers the rail-pattern visibility.

## Provenance fields (page header, not JSON)

Collection date, source host(s), tools used, ticket number. Render in `.sub`.

## Cross-checks (run before declaring done)

- GPU pair count: full 8-card mesh ⇒ each NV kind sums to 56 (28 pairs × 2 directions).
- Switch uplinks: sum of `uplinks` == count of link lines in iblinkinfo's CA blocks.
- Every `gpuNodes` entry appears in some fabric plane (unless the node genuinely has no IB).
