// Page-specific battery EXAMPLE (shape and structure reference only).
//
// WARNING — engine reality (verified by probe on obscura 0.2.2): getBBox()
// returns all zeros in `obscura fetch -e`. These scripts were written against
// the standard SVG API and NEVER produced real values in this engine. When
// writing your own page-specific battery, copy the geometry functions from
// scripts/battery.js (attribute-based shapes + canvas measureText text),
// not the getBBox calls below.
//
(() => {
  try {
    document.getElementById('modeFix').click();
    const svg = document.querySelector('.arch svg');
    const circles = [...svg.querySelectorAll('circle')];
    const texts = [...svg.querySelectorAll('text')];
    const overlaps = [];
    for (const c of circles) {
      for (const t of texts) {
        if (c.parentNode === t.parentNode) continue;
        const cb = c.getBBox(), tb = t.getBBox();
        const ix = Math.max(0, Math.min(cb.x+cb.width, tb.x+tb.width) - Math.max(cb.x, tb.x));
        const iy = Math.max(0, Math.min(cb.y+cb.height, tb.y+tb.height) - Math.max(cb.y, tb.y));
        if (ix > 2 && iy > 2) overlaps.push('C' + Math.round(cb.x) + ',' + Math.round(cb.y) + ' x "' + t.textContent.slice(0,16) + '" ' + Math.round(ix) + 'x' + Math.round(iy));
      }
    }
    const own = circles.map(c => {
      const n = c.parentNode.querySelector('text');
      const cb = c.getBBox(), nb = n.getBBox();
      const inside = nb.x >= cb.x && nb.y >= cb.y && nb.x+nb.width <= cb.x+cb.width && nb.y+nb.height <= cb.y+cb.height;
      return inside ? null : 'NUM' + n.textContent + '_OUT';
    }).filter(Boolean);
    return JSON.stringify({overlaps, own});
  } catch (e) { return 'EXC:' + e.message }
})()