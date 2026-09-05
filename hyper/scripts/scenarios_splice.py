#!/usr/bin/env python3
"""Splice the generated Section 3 into hyper/index.html (run from a clean HEAD copy of index.html)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, '..', 'index.html')
s = open(p).read()
sec = open(os.path.join(HERE, 'scenarios_section.html')).read()
css_anchor = "  @media (max-width: 700px) { .hy-cards { grid-template-columns: 1fr; }"
assert s.count(css_anchor) == 1 and 'id="scenarios"' not in s
css_add = """  /* Section 3 — portfolio scenarios */
  .hy-scen th.hy-grp { text-align: center; border-bottom: 1px solid var(--color-border); }
  .hy-scen td.col-num { white-space: nowrap; }
  .hy-grid th, .hy-grid td { text-align: center !important; padding: 8px 6px; }
  .hy-grid th.hy-grid-corner { text-align: left !important; font-size: 0.72rem; color: var(--color-text-muted); white-space: nowrap; }
  .hy-grid tbody th.hy-grid-row { font-family: var(--font-display); font-weight: 700; white-space: nowrap; color: var(--color-text) !important; background: var(--color-surface-offset); }
  .hy-grid td { vertical-align: middle; min-width: 86px; }
  .hy-cell-o { display: block; font-family: var(--font-display); font-weight: 700; font-size: 0.9rem; font-variant-numeric: tabular-nums; }
  .hy-cell-h { display: block; font-size: 0.7rem; color: var(--color-text-muted); font-variant-numeric: tabular-nums; margin-top: 2px; }
  .hy-grid td.hy-up { background: color-mix(in srgb, var(--color-gain) 14%, transparent); }
  .hy-grid td.hy-up .hy-cell-o { color: var(--color-gain); }
  .hy-grid td.hy-dn { background: color-mix(in srgb, var(--color-loss) 12%, transparent); }
  .hy-grid td.hy-dn .hy-cell-o { color: var(--color-loss); }
  .hy-grid td.hy-liq { background: color-mix(in srgb, var(--color-loss) 32%, transparent); }
  .hy-grid td.hy-liq .hy-cell-o { color: var(--color-loss); letter-spacing: 0.08em; }
  .hy-grid td.hy-beta { box-shadow: inset 0 0 0 2px var(--color-primary); }
"""
s = s.replace(css_anchor, css_add + css_anchor, 1)
nav_anchor = '      <a href="#review" class="nav-tab">Trade Review</a>\n'
assert s.count(nav_anchor) == 1
s = s.replace(nav_anchor, nav_anchor + '      <a href="#scenarios" class="nav-tab">Scenarios</a>\n', 1)
old_hdr = '<span id="last-updated">Snapshot · Sep 2, 2026 03:56 UTC (Sep 1, 8:56 PM PT) · 233 Hyperliquid perps + 5 live HIP-3 venues walked · inputs: 10-year 4.79%, Sep 16 hike 57.5%, Brent $95 (+4.5%) · account 0xD71a…95Bc: $7,537 equity, short 72.7 ETH at 23×, 2.2% from liquidation</span>'
assert s.count(old_hdr) == 1
new_hdr = '<span id="last-updated">Sections 1–2 snapshot · Sep 2, 2026 03:56 UTC (Sep 1, 8:56 PM PT) · 233 Hyperliquid perps + 5 live HIP-3 venues walked · inputs: 10-year 4.79%, Sep 16 hike 57.5%, Brent $95 (+4.5%) · Section 3 scenarios · Sep 5, 2026 14:46 UTC (7:46 AM PT) · account 0xD71a…95Bc now: $27,567 equity, long 4.22 BTC + 1,181 HYPE at 15.8×, liquidation 75,285 (BTC alone) / 76,499 (HYPE on beta)</span>'
s = s.replace(old_hdr, new_hdr, 1)
old_cap = '<div class="cap">Opened and re-opened between 01:49Z and 03:31Z on Sep 2, with four 5-ETH covers at 2,417–2,423 in between (−$413 realised in 14 minutes). The direction agrees with this page; the size makes the page moot. See card #0.</div>'
assert s.count(old_cap) == 1
s = s.replace(old_cap, old_cap.replace('See card #0.</div>', 'See card #0. <em>As of the Sep 2 walk — the ETH short was closed on Sep 3 (−$3.8k realised) and the account is now long 4.22 BTC and 1,181 HYPE; the current book is priced in <a href="#scenarios">Section 3</a>.</em></div>'), 1)
main_anchor = "\n    </main>\n"
assert s.count(main_anchor) == 1
s = s.replace(main_anchor, "\n" + sec + main_anchor, 1)
old_title = "<title>Hyper — Hyperliquid Regime Book &amp; Trade Review | Leadsure</title>"
assert s.count(old_title) == 1
s = s.replace(old_title, "<title>Hyper — Hyperliquid Regime Book, Trade Review &amp; Portfolio Scenarios | Leadsure</title>", 1)
open(p, 'w').write(s)
print("spliced", len(s))
