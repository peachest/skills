// Generic render-check battery for obscura fetch -e.
//
// ENGINE REALITY (probed 2026-09-07 on obscura 0.2.2 — trust this over any
// API doc; each line below was verified by direct probe):
//   - SVG computed-geometry APIs are ALL dead in fetch -e, even with --wait
//     or combined with -s: getBBox() and getComputedTextLength() return 0,
//     getExtentOfChar() and Range.getBoundingClientRect() return zeros,
//     getScreenCTM does not exist. This is not a timing issue.
//   - HTML layout APIs WORK (scrollWidth/clientWidth/getComputedStyle return
//     real values). Only the SVG surface is dead.
//   - Canvas 2D works: measureText() gives real text width with the actual
//     font metrics (±font-fallback error, ~10%).
//   - SVG shapes carry explicit geometry attributes (x/y/width/height,
//     cx/cy/r, points) — readable via getAttribute().
// => Geometry strategy: shapes from attributes, text width from canvas
//    measureText, text height ~ font-size (y attr is the baseline).
//
// Other contract rules:
//   - IIFE with explicit return; the returned string is the only output channel.
//   - try/catch wrapper: exceptions are swallowed to null otherwise.
//   - The <svg> ROOT's getBoundingClientRect() works (it is HTML-embedded);
//     use it to filter to actually-rendered SVGs (hidden tab SVGs excluded).
//   - Translated elements: only translate(x,y) is honored; other transforms
//     mark the element skipped (reported in counts.transformSkipped).
(() => {
  try {
    const issues = [];
    const MAX_REPORT = 20;

    // ---- 1. Element presence smoke --------------------------------------
    const counts = {
      svg: document.querySelectorAll('svg').length,
      canvas: document.querySelectorAll('canvas').length,
      video: document.querySelectorAll('video').length,
      img: document.querySelectorAll('img').length,
      table: document.querySelectorAll('table').length,
      transformSkipped: 0,
    };

    // ---- 2. HTML horizontal overflow (HTML layout APIs work) -------------
    for (const el of document.body.querySelectorAll('*')) {
      if (el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 2 &&
          el.textContent && el.textContent.trim().length > 0) {
        const cs = window.getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        // Horizontal scroll containers may be intentional; report as advisory.
        issues.push({kind: 'html-overflow', el: describe(el),
          scrollWidth: el.scrollWidth, clientWidth: el.clientWidth,
          advisory: true});
        if (issues.length >= MAX_REPORT) break;
      }
    }

    // ---- helpers ----------------------------------------------------------
    function describe(el) {
      const tag = el.tagName.toLowerCase();
      const id = el.id ? '#' + el.id : '';
      const cls = (typeof el.getAttribute === 'function' && el.getAttribute('class'))
        ? '.' + el.getAttribute('class').split(/\s+/).slice(0, 2).join('.') : '';
      return tag + id + cls;
    }
    const num = (el, name, dflt) => {
      const v = parseFloat(el.getAttribute(name));
      return isFinite(v) ? v : dflt;
    };
    // Visibility walk: hidden layers (opacity="0" hotspot toggles, display
    // none tabs) are design state, not defects — their geometry is excluded.
    // Covers both the SVG opacity ATTRIBUTE and computed style, because this
    // engine's computed style returns "" for some SVG properties.
    function visible(el, svgRoot) {
      let n = el;
      while (n && n.nodeType === 1) {
        if (n.getAttribute && (n.getAttribute('display') === 'none' ||
            parseFloat(n.getAttribute('opacity') || '1') === 0)) return false;
        const cs = window.getComputedStyle(n);
        if (cs.display === 'none' || cs.visibility === 'hidden' ||
            (cs.opacity !== '' && parseFloat(cs.opacity) === 0)) return false;
        if (n === svgRoot) break;
        n = n.parentNode;
      }
      return true;
    }
    // Accumulated translate() from the element and its ancestors (SVG root
    // exclusive). Any other transform => null (element is skipped).
    function translateOf(el, svgRoot) {
      let tx = 0, ty = 0;
      let n = el;
      while (n && n !== svgRoot && n.nodeType === 1) {
        const tr = n.getAttribute && n.getAttribute('transform');
        if (tr) {
          if (!/^translate\(\s*[-\d.]+\s*[, ]\s*[-\d.]+\s*\)$/.test(tr.replace(/\s+/g, ' ').trim()) &&
              !/^translate\(\s*[-\d.]+\s*\)$/.test(tr.trim())) return null;
          const m = tr.match(/[-\d.]+/g) || [];
          tx += parseFloat(m[0]) || 0;
          ty += parseFloat(m[1]) || 0;
        }
        n = n.parentNode;
      }
      return {tx, ty};
    }
    function shapeBBox(el, svgRoot) {
      const tag = el.tagName.toLowerCase();
      let b = null;
      if (tag === 'rect') b = {x: num(el, 'x', 0), y: num(el, 'y', 0),
        width: num(el, 'width', 0), height: num(el, 'height', 0)};
      else if (tag === 'circle') { const r = num(el, 'r', 0);
        b = {x: num(el, 'cx', 0) - r, y: num(el, 'cy', 0) - r, width: 2 * r, height: 2 * r}; }
      else if (tag === 'ellipse') { const rx = num(el, 'rx', 0), ry = num(el, 'ry', 0);
        b = {x: num(el, 'cx', 0) - rx, y: num(el, 'cy', 0) - ry, width: 2 * rx, height: 2 * ry}; }
      else if (tag === 'polygon' || tag === 'polyline') {
        const pts = (el.getAttribute('points') || '').trim().split(/[\s,]+/).map(Number)
          .filter((v) => isFinite(v));
        if (pts.length >= 4) {
          const xs = pts.filter((_, i) => i % 2 === 0), ys = pts.filter((_, i) => i % 2 === 1);
          const x0 = Math.min(...xs), y0 = Math.min(...ys);
          b = {x: x0, y: y0, width: Math.max(...xs) - x0, height: Math.max(...ys) - y0};
        }
      }
      if (!b || (b.width <= 0 && b.height <= 0)) return null;
      const tr = translateOf(el, svgRoot);
      if (!tr) { counts.transformSkipped++; return null; }
      return {x: b.x + tr.tx, y: b.y + tr.ty, width: b.width, height: b.height};
    }
    // Shared canvas for text measurement.
    const mctx = document.createElement('canvas').getContext('2d');
    function textBBox(t, svgRoot) {
      const cs = window.getComputedStyle(t);
      const fs = parseFloat(cs.fontSize) || 16;
      const anchor = (t.getAttribute('text-anchor') || cs.textAnchor || 'start').trim();
      let w = 0;
      try {
        // Engine quirk: a font string WITH a weight prefix ("400 16px Times")
        // makes measureText return garbage (~240px/char). The weightless
        // form ("16px Times") measures correctly; bold slop is covered by
        // the overlap tolerance.
        mctx.font = cs.fontSize + ' ' + cs.fontFamily;
        w = mctx.measureText(t.textContent).width;
      } catch (e) { /* fall through to estimate */ }
      if (!isFinite(w) || w <= 0) {
        // Fallback estimate: CJK/full-width ~1em, others ~0.55em.
        let units = 0;
        for (const ch of t.textContent)
          units += ch.charCodeAt(0) > 0x2e7f ? 1 : 0.55;
        w = units * fs;
      }
      const x = num(t, 'x', 0), y = num(t, 'y', 0);
      let x0 = x;
      if (anchor === 'middle') x0 = x - w / 2;
      else if (anchor === 'end') x0 = x - w;
      const tr = translateOf(t, svgRoot);
      if (!tr) { counts.transformSkipped++; return null; }
      // y is the text baseline: top ~ y - 0.8*fs, height ~ fs.
      return {x: x0 + tr.tx, y: y - fs * 0.8 + tr.ty, width: w, height: fs};
    }
    function intersect(a, b) {
      const ix = Math.max(0, Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x));
      const iy = Math.max(0, Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y));
      return {ix, iy};
    }
    // Fraction of `t`'s area inside `s` — a box label inside its box is design
    // (contained), a marker covering part of an unrelated label is a defect.
    function containedFrac(s, t) {
      const ix = Math.max(0, Math.min(s.x + s.width, t.x + t.width) - Math.max(s.x, t.x));
      const iy = Math.max(0, Math.min(s.y + s.height, t.y + t.height) - Math.max(s.y, t.y));
      const tArea = t.width * t.height;
      return tArea > 0 ? (ix * iy) / tArea : 0;
    }
    // "Same group" means same parent <g> (a tight label group, e.g. a number
    // inside its own circle). Two direct children of the <svg> root are NOT a
    // group — the svg root is a container, and unrelated labels that are both
    // its direct children must still be checked against each other.
    const sameGroup = (a, b) => a.parentNode === b.parentNode &&
      a.parentNode && a.parentNode.tagName && a.parentNode.tagName.toLowerCase() === 'g';

    // Only SVGs that are actually rendered (root gBCR works).
    const renderedSvgs = [...document.querySelectorAll('svg')].filter(
      (s) => { const r = s.getBoundingClientRect(); return r.width > 0 || r.height > 0; });
    // Texts/shapes that are visible (opacity/display walk up to the svg root).
    const visTexts = (svg) => [...svg.querySelectorAll('text')]
      .filter((t) => visible(t, svg))
      .map((t) => ({t, b: textBBox(t, svg)})).filter((x) => x.b);
    const visShapes = (svg) => [...svg.querySelectorAll('circle, rect, ellipse, polygon')]
      .filter((s) => visible(s, svg))
      .map((s) => ({s, b: shapeBBox(s, svg)})).filter((x) => x.b);

    // ---- 3. SVG text x text overlap (different groups) --------------------
    for (const svg of renderedSvgs) {
      const texts = visTexts(svg);
      for (let i = 0; i < texts.length; i++) {
        for (let j = i + 1; j < texts.length; j++) {
          const a = texts[i], c = texts[j];
          if (sameGroup(a.t, c.t)) continue;
          const {ix, iy} = intersect(a.b, c.b);
          if (ix > 2 && iy > 2) {
            // Severity = overlap area / smaller text area. Text width comes
            // from measureText with font-fallback error (~±10%), so edge
            // touches (<30% of the smaller text) are advisory; substantial
            // collisions are hard findings. Calibrated on a real accepted
            // artifact vs. a real defect (circle centered on a label).
            const aArea = a.b.width * a.b.height, cArea = c.b.width * c.b.height;
            const frac = (ix * iy) / Math.max(1, Math.min(aArea, cArea));
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

    // ---- 4. SVG shape x text overlap (markers covering labels) ------------
    if (issues.length < MAX_REPORT) {
      for (const svg of renderedSvgs) {
        const shapes = visShapes(svg);
        const texts = visTexts(svg);
        for (const sh of shapes) {
          for (const te of texts) {
            if (sameGroup(sh.s, te.t)) continue; // number in its own circle
            const {ix, iy} = intersect(sh.b, te.b);
            if (ix > 2 && iy > 2) {
              // A text ≥85% inside the shape is a box label (design).
              if (containedFrac(sh.b, te.b) >= 0.85) continue;
              // SVG paints in document order: a shape drawn AFTER the text
              // occludes it; a shape drawn BEFORE it is the background the
              // text sits on (label-in-box design). A stroke-only shape
              // (fill="none") never occludes either.
              const shapeOnTop = !!(te.t.compareDocumentPosition(sh.s) &
                Node.DOCUMENT_POSITION_FOLLOWING);
              const noFill = sh.s.getAttribute('fill') === 'none';
              const occl = (ix * iy) / Math.max(1, te.b.width * te.b.height);
              const advisory = !shapeOnTop || noFill || occl < 0.35;
              issues.push({kind: 'svg-shape-over-text', shape: describe(sh.s),
                text: te.t.textContent.slice(0, 16),
                overlap: Math.round(ix) + 'x' + Math.round(iy),
                contained: Math.round(containedFrac(sh.b, te.b) * 100) / 100,
                occlusion: Math.round(occl * 100) / 100,
                shapeOnTop: shapeOnTop, advisory: advisory});
              if (issues.length >= MAX_REPORT) break;
            }
          }
          if (issues.length >= MAX_REPORT) break;
        }
        if (issues.length >= MAX_REPORT) break;
      }
    }

    // ---- 5. SVG text-escape (text leaving its group's rect, 1px tol) ------
    if (issues.length < MAX_REPORT) {
      for (const svg of renderedSvgs) {
        const groupRects = [...svg.querySelectorAll('g')].filter((g) =>
          g.querySelector(':scope > rect') && g.querySelector('text') && visible(g, svg));
        for (const g of groupRects) {
          const rb = shapeBBox(g.querySelector(':scope > rect'), svg);
          if (!rb) continue;
          for (const t of g.querySelectorAll('text')) {
            const tb = textBBox(t, svg);
            if (!tb) continue;
            if (tb.x < rb.x - 1 || tb.x + tb.width > rb.x + rb.width + 1 ||
                tb.y < rb.y - 1 || tb.y + tb.height > rb.y + rb.height + 2) {
              issues.push({kind: 'svg-text-escape', text: t.textContent.slice(0, 16),
                textX: [Math.round(tb.x), Math.round(tb.x + tb.width)],
                boxX: [Math.round(rb.x), Math.round(rb.x + rb.width)]});
              if (issues.length >= MAX_REPORT) break;
            }
          }
          if (issues.length >= MAX_REPORT) break;
        }
        if (issues.length >= MAX_REPORT) break;
      }
    }

    return JSON.stringify({
      // ok = no hard findings; advisory-only (font-fallback slack, intentional
      // scroll containers) passes and is reported for the record.
      ok: !issues.some((i) => !i.advisory),
      title: document.title,
      counts, issues,
    });
  } catch (e) {
    return 'EXC:' + e.message;
  }
})()
