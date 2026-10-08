// Generic render-check battery — runs in a REAL browser engine (Chromium via
// Playwright). All geometry APIs are live: getBoundingClientRect() works on
// every element including SVG children, computed styles are reliable.
//
// Contract: IIFE with explicit return of a JSON string; try/catch wrapper
// (the runner treats a non-JSON verdict as a failure).
//
// Adjudication model (calibrated on a real before/after pair — an accepted
// artifact with straddling markers as the pass oracle, a real defect
// [marker centered on a label] as the fail oracle):
//   - design, not defect: text ≥85% inside a shape (box label); shape painted
//     BEFORE the text (SVG paints in document order — background); fill="none"
//     shapes; hidden layers (opacity=0 hotspots, display:none tabs); edge
//     touches < 30% of the smaller text.
//   - hard finding: filled shape painted after the text occluding ≥35% of it,
//     or two texts colliding over ≥30% of the smaller one.
(() => {
  try {
    const issues = [];
    const MAX_REPORT = 20;

    // ---- 1. Element presence smoke ----------------------------------------
    const counts = {
      svg: document.querySelectorAll('svg').length,
      canvas: document.querySelectorAll('canvas').length,
      video: document.querySelectorAll('video').length,
      img: document.querySelectorAll('img').length,
      table: document.querySelectorAll('table').length,
      brokenImgs: [...document.querySelectorAll('img')]
        .filter((i) => i.complete && i.naturalWidth === 0).length,
    };
    // DOM truncation census (added 2026-10-09, eagle3 span-in-svg incident):
    // an HTML tag (e.g. <span>) inside <svg> makes the parser relocate all
    // following content out of the SVG namespace — silently dropping whole
    // subtrees while geometry checks pass on the remainder (false green).
    // Direct evidence in-DOM: HTML-namespace children inside svg.
    // Heuristic (browser has no source access): an HTML tag inside <svg>
    // (e.g. <span>) makes the parser relocate ALL following content — svg
    // siblings appear as orphan HTML elements (rect/text as html tags, svg
    // closed early). Detect: svg-namespace tag names existing outside any
    // svg, or an html child inside svg.
    const isSvgTagName = (t) => /^(svg|rect|circle|ellipse|line|polyline|polygon|path|text|tspan|g|defs|marker|use|symbol|title|desc)$/.test(t);
    for (const el of document.body.querySelectorAll('*')) {
      if (el.closest('svg')) continue; // inside a real svg — fine
      if (isSvgTagName(el.tagName.toLowerCase())) {
        issues.push({kind: 'orphan-svg-content', tag: el.tagName.toLowerCase(),
          hint: 'an HTML tag (span/b/...) inside <svg> closed it early; move it to tspan',
          advisory: false});
        break;
      }
    }
    for (const img of document.querySelectorAll('img')) {
      if (img.complete && img.naturalWidth === 0) {
        issues.push({kind: 'broken-image', src: (img.getAttribute('src') || '').slice(0, 80)});
        if (issues.length >= MAX_REPORT) break;
      }
    }

    // ---- helpers ------------------------------------------------------------
    const bboxOf = (el) => {
      const r = el.getBoundingClientRect();
      return (r.width > 0 || r.height > 0) ? {x: r.x, y: r.y, width: r.width, height: r.height} : null;
    };
    function describe(el) {
      const tag = el.tagName.toLowerCase();
      const id = el.id ? '#' + el.id : '';
      const cls = (typeof el.getAttribute === 'function' && el.getAttribute('class'))
        ? '.' + el.getAttribute('class').split(/\s+/).slice(0, 2).join('.') : '';
      return tag + id + cls;
    }
    // Real engine: computed styles are reliable for the full ancestor walk.
    function visible(el) {
      let n = el;
      while (n && n.nodeType === 1) {
        const cs = window.getComputedStyle(n);
        if (cs.display === 'none' || cs.visibility === 'hidden' ||
            parseFloat(cs.opacity) === 0) return false;
        n = n.parentNode;
      }
      return true;
    }
    function intersect(a, b) {
      const ix = Math.max(0, Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x));
      const iy = Math.max(0, Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y));
      return {ix, iy};
    }
    // Fraction of t's area inside s (viewport-space rects).
    function containedFrac(s, t) {
      const {ix, iy} = intersect(s, t);
      const tArea = t.width * t.height;
      return tArea > 0 ? (ix * iy) / tArea : 0;
    }
    // "Same group" = same parent <g> (a tight label group). Two direct
    // children of the <svg> root are NOT a group.
    const sameGroup = (a, b) => a.parentNode === b.parentNode &&
      a.parentNode && a.parentNode.tagName &&
      a.parentNode.tagName.toLowerCase() === 'g';

    const renderedSvgs = [...document.querySelectorAll('svg')]
      .filter((s) => visible(s) && bboxOf(s));
    const visTexts = (svg) => [...svg.querySelectorAll('text')]
      .filter((t) => visible(t)).map((t) => ({t, b: bboxOf(t)})).filter((x) => x.b);
    const visShapes = (svg) => [...svg.querySelectorAll('circle, rect, ellipse, polygon, path')]
      .filter((s) => visible(s)).map((s) => ({s, b: bboxOf(s)})).filter((x) => x.b);

    // ---- 2. HTML horizontal overflow ---------------------------------------
    for (const el of document.body.querySelectorAll('*')) {
      if (!visible(el)) continue;
      if (el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 2 &&
          el.textContent && el.textContent.trim().length > 0) {
        // Horizontal scroll containers may be intentional; advisory.
        issues.push({kind: 'html-overflow', el: describe(el),
          scrollWidth: el.scrollWidth, clientWidth: el.clientWidth,
          advisory: true});
        if (issues.length >= MAX_REPORT) break;
      }
    }

    // ---- 3. SVG text x text collision ---------------------------------------
    for (const svg of renderedSvgs) {
      const texts = visTexts(svg);
      for (let i = 0; i < texts.length; i++) {
        for (let j = i + 1; j < texts.length; j++) {
          const a = texts[i], c = texts[j];
          if (sameGroup(a.t, c.t)) continue;
          const {ix, iy} = intersect(a.b, c.b);
          if (ix > 2 && iy > 2) {
            const frac = (ix * iy) /
              Math.max(1, Math.min(a.b.width * a.b.height, c.b.width * c.b.height));
            issues.push({kind: 'svg-text-overlap',
              a: a.t.textContent.slice(0, 16), b: c.t.textContent.slice(0, 16),
              overlap: Math.round(ix) + 'x' + Math.round(iy),
              occlusion: Math.round(frac * 100) / 100, advisory: frac < 0.3});
            if (issues.length >= MAX_REPORT) break;
          }
        }
        if (issues.length >= MAX_REPORT) break;
      }
      if (issues.length >= MAX_REPORT) break;
    }

    // ---- 4. SVG shape x text occlusion --------------------------------------
    if (issues.length < MAX_REPORT) {
      for (const svg of renderedSvgs) {
        const shapes = visShapes(svg);
        const texts = visTexts(svg);
        for (const sh of shapes) {
          for (const te of texts) {
            if (sameGroup(sh.s, te.t)) continue; // number in its own circle
            const {ix, iy} = intersect(sh.b, te.b);
            if (ix > 2 && iy > 2) {
              if (containedFrac(sh.b, te.b) >= 0.85) continue; // box label
              // SVG paints in document order: a shape drawn AFTER the text
              // occludes it; before = background the text sits on.
              const shapeOnTop = !!(te.t.compareDocumentPosition(sh.s) &
                Node.DOCUMENT_POSITION_FOLLOWING);
              const noFill = sh.s.getAttribute('fill') === 'none' ||
                window.getComputedStyle(sh.s).fill === 'none';
              const occl = (ix * iy) / Math.max(1, te.b.width * te.b.height);
              issues.push({kind: 'svg-shape-over-text', shape: describe(sh.s),
                text: te.t.textContent.slice(0, 16),
                overlap: Math.round(ix) + 'x' + Math.round(iy),
                occlusion: Math.round(occl * 100) / 100,
                shapeOnTop: shapeOnTop, advisory: !shapeOnTop || noFill || occl < 0.35});
              if (issues.length >= MAX_REPORT) break;
            }
          }
          if (issues.length >= MAX_REPORT) break;
        }
        if (issues.length >= MAX_REPORT) break;
      }
    }

    // ---- 5. SVG text-escape (text straddling its group's rect) -------------
    // A group may hold MANY rects (a bar row: one small rect per slot, each
    // with its own label) — compare the text against EVERY direct rect, not
    // just the first. A caption fully below a box does not intersect anything
    // (design); a contained label is fine; only a straddler (partial
    // intersection, not contained) is reported — and as advisory: the generic
    // layer cannot distinguish "caption near the edge" from "text spilling
    // out"; strict escape checks belong to page-specific batteries that know
    // the semantics (e.g. hotspot label must sit inside its box).
    if (issues.length < MAX_REPORT) {
      for (const svg of renderedSvgs) {
        const groups = [...svg.querySelectorAll('g')].filter((g) =>
          g.querySelector(':scope > rect') && g.querySelector('text') && visible(g));
        for (const g of groups) {
          const rects = [...g.querySelectorAll(':scope > rect')]
            .map((r) => bboxOf(r)).filter(Boolean);
          for (const t of g.querySelectorAll('text')) {
            if (!visible(t)) continue;
            const tb = bboxOf(t);
            if (!tb) continue;
            let intersects = false, contained = false;
            for (const rb of rects) {
              const {ix, iy} = intersect(rb, tb);
              if (ix > 1 && iy > 1) intersects = true;
              if (containedFrac(rb, tb) >= 0.95) contained = true;
              if (intersects && contained) break;
            }
            if (intersects && !contained) {
              issues.push({kind: 'svg-text-escape', text: t.textContent.slice(0, 16),
                textX: [Math.round(tb.x), Math.round(tb.x + tb.width)],
                advisory: true});
              if (issues.length >= MAX_REPORT) break;
            }
          }
          if (issues.length >= MAX_REPORT) break;
        }
        if (issues.length >= MAX_REPORT) break;
      }
    }

    // ---- 6. SVG broken-arrow: dangling endpoints ----------------------------
    // Edge candidates: stroked line/path/polyline with an arrowhead marker, or
    // a fill-less elongated path (freehand edge). Node candidates: filled or
    // stroked shapes with ≥150px² bbox (manual arrowhead polygons are smaller).
    const EDGE_TAGS = 'line, path, polyline';
    const NODE_TAGS = 'rect, circle, ellipse, polygon, path';
    const isDef = (el) => !!el.closest('defs, marker');
    const hasMarker = (el) => {
      const cs = window.getComputedStyle(el);
      return (el.getAttribute('marker-end') || cs.markerEnd || '') !== 'none' &&
             ((el.getAttribute('marker-end') || cs.markerEnd || '') !== '' &&
              (el.getAttribute('marker-end') || cs.markerEnd || '') !== 'none') ||
             ((el.getAttribute('marker-start') || cs.markerStart || '') !== 'none' &&
              (el.getAttribute('marker-start') || cs.markerStart || '') !== '');
    };
    const nodeArea = (b) => b.width * b.height;
    const toViewport = (el, pt) => {
      const m = el.getScreenCTM();
      if (!m) return null;
      const p = new DOMPoint(pt.x, pt.y).matrixTransform(m);
      return {x: p.x, y: p.y};
    };
    const nearAnyNode = (vp, nodes, pad) => nodes.some((n) =>
      vp.x >= n.b.x - pad && vp.x <= n.b.x + n.b.width + pad &&
      vp.y >= n.b.y - pad && vp.y <= n.b.y + n.b.height + pad);

    if (issues.length < MAX_REPORT) {
      for (const svg of renderedSvgs) {
        // Nodes first (shapes that are not edges themselves).
        const nodeEls = [...svg.querySelectorAll(NODE_TAGS)]
          .filter((s) => visible(s) && !isDef(s) &&
            !(s.hasAttribute('marker-end') || s.hasAttribute('marker-start')));
        const nodes = nodeEls.map((s) => ({s, b: bboxOf(s)})).filter((x) =>
          x.b && nodeArea(x.b) >= 150);
        // Edge candidates.
        const edges = [...svg.querySelectorAll(EDGE_TAGS)].filter((e) => {
          if (!visible(e) || isDef(e)) return false;
          const b = bboxOf(e);
          if (!b || (b.width < 1 && b.height < 1)) return false;
          if (e.hasAttribute('marker-end') || e.hasAttribute('marker-start')) return true;
          const cs = window.getComputedStyle(e);
          if (cs.stroke === 'none' || cs.strokeWidth === '0') return false;
          // Marker-less: only fill-less elongated shapes count as edges.
          const elong = Math.max(b.width, b.height) /
            Math.max(1, Math.min(b.width, b.height));
          return (cs.fill === 'none' || e.getAttribute('fill') === 'none') && elong >= 2.5;
        });
        for (const e of edges) {
          if (typeof e.getTotalLength !== 'function') continue;
          let len = 0;
          try { len = e.getTotalLength(); } catch (_) { continue; }
          if (len < 4) continue;
          const marked = hasMarker(e);
          let dangling = 0;
          for (const t of [0, len]) {
            const vp = toViewport(e, e.getPointAtLength(t));
            if (vp && !nearAnyNode(vp, nodes, 6)) dangling++;
          }
          if (dangling > 0) {
            issues.push({kind: 'broken-arrow-dangling', edge: describe(e),
              endpoints: [0, len].map((t) => {
                const vp = toViewport(e, e.getPointAtLength(t));
                return vp ? [Math.round(vp.x), Math.round(vp.y)] : null;
              }),
              marked, advisory: !marked});
            if (issues.length >= MAX_REPORT) break;
          }
        }
        if (issues.length >= MAX_REPORT) break;
      }
    }

    // ---- 7. SVG edge-through-box --------------------------------------------
    // An edge crossing the interior of a node it does not connect to. Sample
    // along the edge; ≥4 interior samples = hard pass-through, 2–3 = grazing
    // (advisory). Source/target nodes (endpoints inside) are exempt.
    if (issues.length < MAX_REPORT) {
      for (const svg of renderedSvgs) {
        const nodeEls = [...svg.querySelectorAll(NODE_TAGS)]
          .filter((s) => visible(s) && !isDef(s) &&
            !(s.hasAttribute('marker-end') || s.hasAttribute('marker-start')));
        // fill=none shapes are open containers (group frames), not solid
        // nodes — an edge passing through a container is legitimate layout.
        const nodes = nodeEls.map((s) => ({s, b: bboxOf(s)})).filter((x) =>
          x.b && nodeArea(x.b) >= 150 &&
          x.s.getAttribute('fill') !== 'none' &&
          window.getComputedStyle(x.s).fill !== 'none');
        const edges = [...svg.querySelectorAll(EDGE_TAGS)].filter((e) => {
          if (!visible(e) || isDef(e)) return false;
          const b = bboxOf(e);
          return b && (b.width >= 1 || b.height >= 1) &&
            (e.hasAttribute('marker-end') || e.hasAttribute('marker-start'));
        });
        for (const e of edges) {
          let len = 0;
          try { len = e.getTotalLength(); } catch (_) { continue; }
          if (len < 8) continue;
          const vps = [0, len].map((t) => toViewport(e, e.getPointAtLength(t)));
          const inside = (vp, pad) => vp && nodes.some((n) =>
            vp.x > n.b.x + pad && vp.x < n.b.x + n.b.width - pad &&
            vp.y > n.b.y + pad && vp.y < n.b.y + n.b.height - pad);
          const linked = new Set();
          vps.forEach((vp, i) => {
            if (vp) nodes.forEach((n, j) => {
              if (vp.x >= n.b.x - 6 && vp.x <= n.b.x + n.b.width + 6 &&
                  vp.y >= n.b.y - 6 && vp.y <= n.b.y + n.b.height + 6) linked.add(j);
            });
            void i;
          });
          const steps = Math.min(200, Math.max(8, Math.round(len / 10)));
          const crossings = new Map(); // node index -> interior sample count
          for (let k = 1; k < steps; k++) {
            const vp = toViewport(e, e.getPointAtLength((len * k) / steps));
            if (!vp) continue;
            nodes.forEach((n, j) => {
              if (linked.has(j)) return;
              if (vp.x > n.b.x + 2 && vp.x < n.b.x + n.b.width - 2 &&
                  vp.y > n.b.y + 2 && vp.y < n.b.y + n.b.height - 2) {
                crossings.set(j, (crossings.get(j) || 0) + 1);
              }
            });
          }
          for (const [j, cnt] of crossings) {
            if (cnt < 2) continue;
            issues.push({kind: 'edge-through-box', edge: describe(e),
              through: describe(nodes[j].s), samples: cnt,
              advisory: cnt < 4});
            if (issues.length >= MAX_REPORT) break;
          }
          if (issues.length >= MAX_REPORT) break;
        }
        if (issues.length >= MAX_REPORT) break;
      }
    }

    

    // ---- 8. SVG text-out-of-viewport -----------------------------------------
    // Text whose bbox extends beyond its svg's viewport (even 1px). Stricter
    // than text-escape (which needs a straddling group rect): catches footnote
    // lines that run off the right edge of the canvas. Advisory — long labels
    // near the edge are often intentional crops; the author decides.
    if (issues.length < MAX_REPORT) {
      for (const svg of renderedSvgs) {
        const vb = bboxOf(svg);
        if (!vb) continue;
        for (const {t, b} of visTexts(svg)) {
          const over = Math.max(0, b.x + b.width - (vb.x + vb.width)) +
                       Math.max(0, vb.x - b.x) +
                       Math.max(0, b.y + b.height - (vb.y + vb.height)) +
                       Math.max(0, vb.y - b.y);
          if (over > 1) {
            issues.push({kind: 'svg-text-out-of-viewport', text: t.textContent.slice(0, 16),
              overhang: Math.round(over), advisory: true});
            if (issues.length >= MAX_REPORT) break;
          }
        }
        if (issues.length >= MAX_REPORT) break;
      }
    }

    // ---- 9. Dark-theme contrast (prefers-color-scheme: dark) ----------------
    // Simulate dark scheme: if the page defines dark tokens, verify svg text
    // won't be dark-on-dark. Heuristic: parse CSS custom properties under a
    // dark media query and check that --ink-like vars are light. Advisory —
    // only meaningful for artifacts meant to be embedded in themed hosts.
    if (issues.length < MAX_REPORT) {
      for (const svg of renderedSvgs) {
        const texts = visTexts(svg);
        if (!texts.length) continue;
        const fills = texts.map((x) => window.getComputedStyle(x.t).fill);
        const rgb = (f) => { const m = f && f.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/); return m ? [ +m[1], +m[2], +m[3] ] : null; };
        // WCAG 2.x relative luminance (linearized sRGB), not a naive weighted
        // sum — naive luma over-rejects mid-luminance semantic colors like red
        // #f85149 on dark panels (actual 5.37:1, readable).
        const srgb = (c) => c.map((v) => { v /= 255; return v <= 0.04045 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
        const lum = (c) => { if (!c) return null; const [r,g,b] = srgb(c); return 0.2126*r + 0.7152*g + 0.0722*b; };
        const bgLum = lum(rgb(window.getComputedStyle(svg).backgroundColor)) ?? lum(rgb(window.getComputedStyle(document.body).backgroundColor));
        if (bgLum === null || bgLum > 0.5) continue; // light background — not a dark-theme page
        let worst = null;
        for (const f of fills) {
          const l = lum(rgb(f));
          if (l === null) continue;
          const ratio = (Math.max(l, bgLum) + 0.05) / (Math.min(l, bgLum) + 0.05);
          if (!worst || ratio < worst.ratio) worst = { ratio, fill: f };
        }
        if (worst && worst.ratio < 3) {
          issues.push({kind: 'svg-dark-contrast', worstRatio: Math.round(worst.ratio * 100) / 100,
            worstFill: worst.fill, svgBgLum: Math.round(bgLum * 100) / 100, advisory: true});
        }
      }
    }

    // ---- 10. CSS var sanity: used-vars ⊆ defined-vars ----------------------
    // For each svg: collect var(--x) referenced in attributes/styles, check
    // each resolves to a non-empty custom property under the CURRENT scheme.
    // Catches: var referenced but never defined (silent fallback to inherited
    // black or nothing), and self-referential definitions (--x: var(--x))
    // which make the property guaranteed-invalid at computed-value time.
    if (issues.length < MAX_REPORT) {
      for (const svg of renderedSvgs) {
        const inner = svg.innerHTML || '';
        const used = new Set();
        for (const m of inner.matchAll(/var\((--[-\w]+)\s*(?:,([^)]*))?\)/g)) used.add(m[1]);
        for (const v of used) {
          const val = window.getComputedStyle(svg).getPropertyValue(v).trim();
          if (!val) {
            issues.push({kind: 'css-var-undefined', var: v, advisory: true});
            if (issues.length >= MAX_REPORT) break;
          }
        }
        if (issues.length >= MAX_REPORT) break;
      }
    }

    return JSON.stringify({
      ok: !issues.some((i) => !i.advisory),
      title: document.title,
      counts, issues,
    });
  } catch (e) {
    return 'EXC:' + e.message;
  }
})()
