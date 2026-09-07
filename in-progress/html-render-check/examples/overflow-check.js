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
    // check every hotspot text stays inside its group's rect-box
    const issues = [];
    for (const g of svg.querySelectorAll('.hot')) {
      const rect = g.querySelector('.hot-box');
      const texts = [...g.querySelectorAll('text')].filter(t => t !== g.querySelector('circle + text') || true);
      if (!rect) continue;
      const rb = rect.getBBox();
      for (const t of texts) {
        const tb = t.getBBox();
        if (tb.x < rb.x - 1 || tb.x + tb.width > rb.x + rb.width + 1 || tb.y < rb.y - 1 || tb.y + tb.height > rb.y + rb.height + 2) {
          issues.push('hot' + g.dataset.hot + ' text "' + t.textContent.slice(0,14) + '" escapes box (t=' + Math.round(tb.x) + ',' + Math.round(tb.x+tb.width) + ' box=' + Math.round(rb.x) + ',' + Math.round(rb.x+rb.width) + ')');
        }
      }
    }
    // check all svg texts pairwise overlap (excluding same-parent)
    const allT = [...svg.querySelectorAll('text')];
    const tt = [];
    for (let i = 0; i < allT.length; i++) for (let j = i+1; j < allT.length; j++) {
      const a = allT[i], b = allT[j];
      if (a.parentNode === b.parentNode) continue;
      const ab = a.getBBox(), bb = b.getBBox();
      const ix = Math.max(0, Math.min(ab.x+ab.width, bb.x+bb.width) - Math.max(ab.x, bb.x));
      const iy = Math.max(0, Math.min(ab.y+ab.height, bb.y+bb.height) - Math.max(ab.y, bb.y));
      if (ix > 2 && iy > 2) tt.push('"' + a.textContent.slice(0,10) + '" x "' + b.textContent.slice(0,10) + '"');
    }
    return JSON.stringify({boxEscapes: issues, textText: tt});
  } catch (e) { return 'EXC:' + e.message }
})()