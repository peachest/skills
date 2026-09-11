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

    return JSON.stringify({
      ok: !issues.some((i) => !i.advisory),
      title: document.title,
      counts, issues,
    });
  } catch (e) {
    return 'EXC:' + e.message;
  }
})()
