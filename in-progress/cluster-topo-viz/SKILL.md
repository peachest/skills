---
name: cluster-topo-viz
description: Visualize GPU cluster topology as a single-file static HTML demo — intra-node GPU interconnect (NVLink/NVSwitch/NUMA, from nvidia-smi topo or device-topology CRs) plus inter-node InfiniBand fabric (from iblinkinfo/ibstat). Use when the user asks to 可视化集群/拓扑/topology, collect cluster topology data (iblinkinfo, ibstat, nvidia-smi topo) from remote nodes over ssh, or build a topology demo/prototype page. Also fires for extending an existing topo demo with more nodes or a new fabric.
---

Render a GPU cluster topology in three layers, as a single static HTML file with embedded data. No framework, no server, no interaction — open in a browser and see it.

## Workflow

1. **Collect** — gather raw data from the live cluster. Reach [collection.md](references/collection.md) when collecting via ssh (probe script, zsh gotcha, dual-perspective iblinkinfo dedup). Skip when the user already has data files.
2. **Parse** — normalize raw outputs into the data contract. Reach [data-contract.md](references/data-contract.md) for the exact JSON shape. Completion: `topology.json` validates — every node, switch, and GPU pair present, no raw regex leftovers.
3. **Render** — copy [templates/topo-demo.html](templates/topo-demo.html) and [assets/topo-base.css](assets/topo-base.css) into the output directory, embed the JSON at the `/*__DATA__*/` slot, adjust the three layer sections to what the data actually has. Completion: browser opens the file and renders every layer with no JS console errors; numbers in the stats bar match the data (`grep`-checkable, not eyeball).
4. **Cross-check** — spot-verify against sources: GPU pair count vs `nvidia-smi topo -m` matrix, switch uplink counts vs `iblinkinfo` line count, degraded nodes vs nodes with `< 8` GPUs. Completion: every discrepancy explained or fixed.

## The three layers

Always render top-down; each layer reads the one below it:

- **Stats bar** — cluster totals (nodes, GPUs, switches, links). One `.stat` card per number.
- **Fabric layer** — one block per IB fabric plane. Switch cards on top, host cards below, links as low-opacity bezier curves (rail structure becomes visible at ~0.2 opacity without spaghetti). Host cards show GPU slot chips (8 slots, NUMA-colored, red for failed GPUs).
- **Node layer** — compact grid of all GPU nodes (degraded nodes get a red border), then ONE representative node expanded: GPUs in two NUMA rows around a central NVSwitch bar. Full-mesh NVLink is drawn as GPU→NVSwitch spokes, never as n² pairwise lines — the NVSwitch IS the mesh's correct abstraction.

## Visual language (tokens live in topo-base.css)

| Meaning | Token |
|---|---|
| NUMA 0 / NUMA 1 | `--numa0` blue / `--numa1` amber |
| NVLink / GPU node accent | `--nvlink` purple |
| IB link, fabric A / fabric B | `--iblink` teal, `--fabric-a` / `--fabric-b` |
| Link state Active / Initialize / Down | `--active` / `--init` / `--down` |
| Panel / border / text on dark bg | `--panel` / `--border` / `--text` / `--muted` |

Semantic variations use token overrides, never new classes. A new pattern that appears in two different renders gets extracted into topo-base.css; until then it stays inline in the page.

## Output conventions

- Deliverable path follows `~/research/<topic>/` (e.g. `demo.html`, `demo-<cluster>.html`), raw data alongside in `data/` or `<cluster>-data/`.
- Page header carries provenance: collection date, source node(s), tools used, and the ticket number when one exists.
- Chinese for user-facing content (titles, labels, subtitles); English for code and data keys.
