#!/usr/bin/env python3
"""Render Section 3 (Portfolio Scenarios) for hyper/index.html from _scen_out.json."""
import json, os
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenarios_out.json')))
EQ0 = d['eq0']; PB0 = d['pb0']; PH0 = d['ph0']; B0 = d['b0']; H0 = d['h0']

def usd(v, dp=0):
    s = f"{abs(v):,.{dp}f}"
    return ("−" if v < 0 else "") + "$" + s
def sgn(v, dp=0):
    s = f"{abs(v):,.{dp}f}"
    return ("−" if v < 0 else "+") + "$" + s
def pct(v, dp=1):
    return ("−" if v < 0 else "+") + f"{abs(v)*100:.{dp}f}%"
def cls(v): return "pm-pos" if v > 0 else ("pm-neg" if v < 0 else "")
def k(v): return f"{v/1000:.0f}k" if v >= 1000 else f"{v:,.0f}"

# ---------- Table A: BTC ladder ----------
rowsA = []
for r in d['A']:
    x, h, o, hb, ob = r['x'], r['hold'], r['ord'], r['hold_beta'], r['ord_beta']
    move = f"<td class=\"col-num {cls(r['pct'])}\">{pct(r['pct'])}</td>"
    if h['liq']:
        hold_cells = f"<td class=\"col-num pm-neg\" colspan=\"3\"><strong>Liquidated</strong> at {h['liq'][0]:,.0f}</td>"
    else:
        hold_cells = f"<td class=\"col-num\"><strong>{usd(h['eq'])}</strong></td><td class=\"col-num {cls(h['pnl'])}\">{sgn(h['pnl'])}</td><td class=\"col-num {cls(h['pnl'])}\">{pct(h['pnl']/EQ0, 0)}</td>"
    if o['liq']:
        ord_cells = f"<td class=\"col-num pm-neg\" colspan=\"5\"><strong>Liquidated</strong> at {o['liq'][0]:,.0f}</td>"
        delta = "<td class=\"col-num\">—</td>"
    else:
        sold = f"{o['sold_b']:.3f} @ {o['sold_b_px']:,.0f}" if o['sold_b'] > 0 else "none"
        tw = f"{o['twb']:.3f} @ {o['twb_px']:,.0f}"
        ord_cells = (f"<td class=\"col-num\">{o['b']:.3f}</td><td class=\"col-num\">{sold}</td><td class=\"col-num\">{tw}</td>"
                     f"<td class=\"col-num\"><strong>{usd(o['eq'])}</strong></td><td class=\"col-num {cls(o['pnl'])}\">{sgn(o['pnl'])}</td>")
        dl = o['eq'] - h['eq']
        delta = f"<td class=\"col-num {cls(dl)}\">{sgn(dl)}</td>"
    hbv = f"<span class=\"pm-neg\">liq {hb['liq'][0]:,.0f}</span>" if hb['liq'] else usd(hb['eq'])
    obv = f"<span class=\"pm-neg\">liq {ob['liq'][0]:,.0f}</span>" if ob['liq'] else usd(ob['eq'])
    beta_cells = f"<td class=\"col-num\">{r['y_beta']:.2f}</td><td class=\"col-num\">{hbv}</td><td class=\"col-num\">{obv}</td>"
    rowsA.append(f"<tr><td class=\"pm-co\"><strong>{x:,}</strong></td>{move}{hold_cells}{ord_cells}{delta}{beta_cells}</tr>")

# ---------- Table B: HYPE ladder ----------
rowsB = []
for r in d['B']:
    y, h, o = r['y'], r['hold'], r['ord']
    move = f"<td class=\"col-num {cls(r['pct'])}\">{pct(r['pct'])}</td>"
    if h['liq']:
        hold_cells = f"<td class=\"col-num pm-neg\" colspan=\"3\"><strong>Liquidated</strong> at {h['liq'][1]:.2f}</td>"
    else:
        hold_cells = f"<td class=\"col-num\"><strong>{usd(h['eq'])}</strong></td><td class=\"col-num {cls(h['pnl'])}\">{sgn(h['pnl'])}</td><td class=\"col-num {cls(h['pnl'])}\">{pct(h['pnl']/EQ0, 0)}</td>"
    if o['liq']:
        ord_cells = f"<td class=\"col-num pm-neg\" colspan=\"5\"><strong>Liquidated</strong> at {o['liq'][1]:.2f}</td>"; delta = "<td class=\"col-num\">—</td>"
    else:
        sold = f"{o['sold_h']:,.0f} @ {o['sold_h_px']:.2f}" if o['sold_h'] > 0 else "none"
        tw = f"{o['twh']:,.0f} @ {o['twh_px']:.2f}"
        ord_cells = (f"<td class=\"col-num\">{o['h']:,.0f}</td><td class=\"col-num\">{sold}</td><td class=\"col-num\">{tw}</td>"
                     f"<td class=\"col-num\"><strong>{usd(o['eq'])}</strong></td><td class=\"col-num {cls(o['pnl'])}\">{sgn(o['pnl'])}</td>")
        dl = o['eq'] - h['eq']; delta = f"<td class=\"col-num {cls(dl)}\">{sgn(dl)}</td>"
    rowsB.append(f"<tr><td class=\"pm-co\"><strong>{y}</strong></td>{move}{hold_cells}{ord_cells}{delta}</tr>")

# ---------- Grid ----------
HY = [70, 75, 80, 85, 90, 95, 100, 105, 110]
beta_col = {}
for r in d['A']:
    yb = r['y_beta']; nearest = min(HY, key=lambda c: abs(c - yb))
    if abs(nearest - yb) <= 3.5: beta_col[r['x']] = nearest
gridrows = []
for row in d['G']:
    x = row[0]['x']
    cells = []
    for c in row:
        o, h = c['ord'], c['hold']; y = c['y']
        mark = " hy-beta" if beta_col.get(x) == y else ""
        if o['liq']:
            hv = "liq" if h['liq'] else usd(h['eq'])
            cells.append(f"<td class=\"hy-liq{mark}\"><span class=\"hy-cell-o\">LIQ</span><span class=\"hy-cell-h\">hold {hv}</span></td>")
        else:
            tint = "hy-up" if o['pnl'] > 0 else "hy-dn"
            hv = "liq" if h['liq'] else usd(h['eq'])
            cells.append(f"<td class=\"{tint}{mark}\"><span class=\"hy-cell-o\">{usd(o['eq'])}</span><span class=\"hy-cell-h\">hold {hv}</span></td>")
    gridrows.append(f"<tr><th class=\"hy-grid-row\">{x:,}</th>{''.join(cells)}</tr>")
gridhead = "".join(f"<th>{y}</th>" for y in HY)

A = {r['x']: r for r in d['A']}; B = {r['y']: r for r in d['B']}
a85, a90, a100 = A[85000], A[90000], A[100000]
ladder_cost_100 = a100['hold']['eq'] - a100['ord']['eq']
ladder_cost_90 = a90['hold']['eq'] - a90['ord']['eq']
ladder_cost_85 = a85['hold']['eq'] - a85['ord']['eq']
b110 = B[110]
S = d['S']
hype_cap_beta = (a100['hold_beta']['eq'] - a100['ord_beta']['eq']) - ladder_cost_100
TF = d['TF']; AFTER = d['AFTER']; CM = d['COMOVE']; EQT = d['eq_at_trigger']
pure85 = a85['hold']['eq'] - S['85000']['eq']; pure90 = a90['hold']['eq'] - S['90000']['eq']; pure100 = a100['hold']['eq'] - S['100000']['eq']
twap_gain100 = a100['ord']['eq'] - S['100000']['eq']
hype_ladder_gross = 1047*113.82 - 96577
a75 = A[75000]; b70 = B[70]
hold70_buffer = b70['hold']['eq'] - b70['hold']['maint']

html = f"""
      <!-- ===================== SECTION 3 ===================== -->
      <div class="fund-header hy-anchor" id="scenarios">
        <h2 class="fund-title">Section 3 · Portfolio Scenarios — The Book From 70k to 100k</h2>
        <div class="hy-inputs"><span class="hy-input">Book · <strong>long {B0:.3f} BTC</strong> at {d['bent']:,.0f} · <strong>long {H0:,.0f} HYPE</strong> at {d['hent']:.2f} (both cross, 40× / 10×)</span><span class="hy-input">Equity · <strong>{usd(EQ0)}</strong> · {usd(d['ntl0'])} notional · {d['ntl0']/EQ0:.1f}× effective</span><span class="hy-input">Marks · <strong>BTC {PB0:,.0f}</strong> · <strong>HYPE {PH0:.2f}</strong></span><span class="hy-input">Liquidation · <strong>{d['liq_btc_only']:,.0f}</strong> BTC alone · <strong>{d['liq_joint']:,.0f}</strong> if HYPE follows at β 1.32</span><span class="hy-input">As of · <strong>{d['as_of']}</strong></span></div>
        <p class="hy-lede">You asked what the Hyperliquid book is worth if BTC goes to 100k in $5k steps, and the same for HYPE. Every rung below is priced two ways. <strong>Hold as-is</strong> marks today’s {B0:.3f} BTC and {H0:,.0f} HYPE at the scenario price with nothing executing. <strong>With orders</strong> lets everything resting in the account execute on a straight-line path from today’s marks to the rung: the {d['A'][3]['ord']['sold_b']:.2f}-BTC take-profit ladder at 81,000–85,000, the 1,047-HYPE ladder at 85.72–108, the stops (0.6 BTC at 78,980–79,100, 350 HYPE at 83.31–83.55), the scale-in bids, and the remainder of the two buy TWAPs (0.66 BTC and 332 HYPE, ~80 hours left). The gap between the two columns is the price of the order book you have chosen — mostly the take-profit ladders, which cap the upside long before 100k.</p>
        <ul class="hy-findings">
          <li><strong>At 100k</strong>Hold as-is is worth <em>{usd(a100['hold']['eq'])}</em> ({sgn(a100['hold']['pnl'])}, {pct(a100['hold']['pnl']/EQ0,0)} on today’s equity) with HYPE flat. With your orders it is <em>{usd(a100['ord']['eq'])}</em> ({sgn(a100['ord']['pnl'])}): the ladder has sold {a100['ord']['sold_b']:.3f} BTC at an average {a100['ord']['sold_b_px']:,.0f} and you arrive at 100k holding {a100['ord']['b']:.2f} BTC — the {B0 - a100['ord']['sold_b']:.2f} the ladder leaves plus the TWAP’s {a100['ord']['twb']:.2f}. Depending on when the TWAP fills, the with-orders figure runs {usd(S['100000']['eq']/1000)}k–{usd(TF['100000']['eq']/1000)}k (method block).</li>
          <li><strong>The ladder’s price</strong>On its own the take-profit ladder costs {usd(pure85)} at 85k, {usd(pure90)} at 90k and <em>{usd(pure100)}</em> at 100k against holding; the buy TWAP claws back {usd(twap_gain100)} of that at 100k, which is why the with-orders column ends {usd(ladder_cost_100)} behind hold-as-is rather than {usd(pure100)}. Each rung above 85k adds only {sgn(a90['ord']['eq']-a85['ord']['eq'])} with orders versus {sgn(a90['hold']['eq']-a85['hold']['eq'])} holding: 1.79 BTC × $5,000 is $8,950, less the TWAP filling $2,500 higher on every longer path.</li>
          <li><strong>Both legs together</strong>If HYPE follows BTC at its measured beta (1.32× the percentage move, so 113.82 at BTC 100k), hold as-is reaches <em>{usd(a100['hold_beta']['eq'])}</em> and with orders <em>{usd(a100['ord_beta']['eq'])}</em>. The HYPE ladder sells all 1,047 by 108 and forgoes about $22.6k there, offset by the HYPE TWAP’s $4.8k gain — {usd(hype_cap_beta)} net on top of the BTC ladder’s cap.</li>
          <li><strong>The other side of 80k</strong>75k and 70k are both liquidations. BTC alone crosses maintenance at {d['liq_btc_only']:,.0f}; with HYPE moving on beta the trigger is {d['liq_joint']:,.0f}. At the trigger the account is down to its maintenance margin, about <em>{usd(EQT)}</em>; the exchange then closes the book by market in 20% chunks and returns what is left, and only a backstop liquidation (equity under two-thirds of maintenance, ≈{usd(EQT*2/3)}) takes everything. So one $5k rung down costs roughly two-thirds of the account, not all of it — and 75,000 itself is a knife-edge, {usd(d['liq_btc_only']-75000)} below the hold-as-is trigger. The stops do not change this: they sell 0.6 BTC at ≈79,000, and by 78,200 the bids and the TWAP have bought a third to a half of it back.</li>
          <li><strong>HYPE on its own</strong>With BTC flat, HYPE at 110 (+29%) is {usd(b110['hold']['eq'])} holding and {usd(b110['ord']['eq'])} with orders — the 1,047-HYPE ladder sells out at an average {b110['ord']['sold_h_px']:.2f} and you keep {b110['ord']['h']:,.0f}. HYPE at 70 (−18%) with BTC flat is {usd(b70['hold']['eq'])} holding today’s book — survivable, but only {usd(hold70_buffer)} above the HYPE-alone trigger of {d['liq_hype_only']:.2f}, and if the TWAPs finish first (they have ~80 hours) that trigger moves to {AFTER['liq_hype_only']:.2f}, so 70 becomes a liquidation.</li>
          <li><strong>The TWAPs</strong>Two buy TWAPs still have 0.66 BTC and 332 HYPE to buy over ~80 hours regardless of price. On the way up they help: cancelling them turns 100k from {usd(a100['ord']['eq'])} into {usd(S['100000']['eq'])} on the page’s path assumption, and had they already filled near today’s price 100k would be worth {usd(TF['100000']['eq'])} — so at that rung the TWAPs are worth {usd((a100['ord']['eq']-S['100000']['eq'])/1000,1)}k–{usd((TF['100000']['eq']-S['100000']['eq'])/1000,1)}k. On the way down they buy into the liquidation until initial margin runs out near 77,500. And if prices simply sit still for those 80 hours, the finished TWAPs leave a {AFTER['b']:.2f} BTC + {AFTER['h']:,.0f} HYPE book at {AFTER['lev']:.1f}× whose triggers are {AFTER['liq_btc_only']:,.0f} (BTC alone), {AFTER['liq_joint']:,.0f} (on beta) and {AFTER['liq_hype_only']:.2f} (HYPE alone) — the account’s own instructions raise the BTC trigger by about ${AFTER['liq_btc_only']-d['liq_btc_only']:,.0f}.</li>
        </ul>
      </div>

      <section class="kpi-grid" aria-label="Portfolio scenario key stats">
        <div class="kpi-card" data-accent="cyan"><div class="kpi-label">Equity · notional · leverage</div><div class="kpi-value">{usd(EQ0)} · {usd(d['ntl0']/1000)}k · {d['ntl0']/EQ0:.1f}×</div></div>
        <div class="kpi-card" data-accent="cyan"><div class="kpi-label">BTC leg · entry · open P&amp;L</div><div class="kpi-value">{B0:.3f} · {d['bent']:,.0f} · {sgn(B0*(PB0-d['bent']))}</div></div>
        <div class="kpi-card" data-accent="cyan"><div class="kpi-label">HYPE leg · entry · open P&amp;L</div><div class="kpi-value">{H0:,.0f} · {d['hent']:.2f} · {sgn(H0*(PH0-d['hent']))}</div></div>
        <div class="kpi-card" data-accent="peach"><div class="kpi-label">Liq · BTC alone · on beta · HYPE alone</div><div class="kpi-value">{d['liq_btc_only']:,.0f} · {d['liq_joint']:,.0f} · {d['liq_hype_only']:.2f}</div></div>
        <div class="kpi-card" data-accent="peach"><div class="kpi-label">Maint · buffer · buffer/notional</div><div class="kpi-value">{usd(d['maint0'])} · {usd(EQ0-d['maint0'])} · {(EQ0-d['maint0'])/d['ntl0']*100:.1f}%</div></div>
        <div class="kpi-card" data-accent="slate"><div class="kpi-label">Take-profit ladders resting</div><div class="kpi-value">3.089 BTC · 1,047 HYPE</div></div>
        <div class="kpi-card" data-accent="slate"><div class="kpi-label">Stops · TWAP left (BTC · HYPE)</div><div class="kpi-value">0.6 · 350 · 0.66 · 332</div></div>
        <div class="kpi-card" data-accent="teal"><div class="kpi-label">100k · hold · with orders · gap</div><div class="kpi-value">{usd(a100['hold']['eq']/1000)}k · {usd(a100['ord']['eq']/1000)}k · {usd(ladder_cost_100/1000)}k</div></div>
      </section>

      <section class="table-section" aria-label="BTC scenario ladder">
        <div class="table-header-row">
          <h2 class="section-title">BTC in $5k Steps — Hold As-Is vs With Orders (HYPE flat at {PH0:.2f}), Plus HYPE on Beta</h2>
          <span class="price-note">Hold as-is: today’s positions marked at the rung. With orders: the take-profit ladder, stops, scale-in bids and the TWAP remainder execute on a straight path from {PB0:,.0f} to the rung; “Sold” is what the ladder and stops sell and the average price; “TWAP adds” is what the buy TWAP fills and its average price. ROE is P&amp;L on today’s {usd(EQ0)}. The last three columns repeat the exercise with HYPE moving 1.32× BTC’s percentage move. On the two downside rungs the stops sell 0.6 BTC at ≈79,000, the bids buy 0.13 back at 78,190–78,435 and the TWAP keeps buying until initial margin runs out — on the page’s path assumption the book is liquidated $90–$320 lower than hold-as-is, not saved; if the TWAP has already filled, the trigger is {TF['75000']['liq'][0]:,.0f}, above hold-as-is; with the TWAPs cancelled the 75k rung survives (equity {usd(9746)} against {usd(8539)} of maintenance).</span>
        </div>
        <div class="table-wrapper">
          <table class="pm-table hy-table hy-scen">
            <thead><tr><th rowspan="2">BTC</th><th rowspan="2" class="col-num">Move</th><th colspan="3" class="hy-grp">Hold as-is</th><th colspan="5" class="hy-grp">With orders</th><th rowspan="2" class="col-num">Orders vs hold</th><th colspan="3" class="hy-grp">HYPE on beta</th></tr>
            <tr><th class="col-num">Equity</th><th class="col-num">P&amp;L</th><th class="col-num">ROE</th><th class="col-num">BTC held</th><th class="col-num">Sold @ avg</th><th class="col-num">TWAP adds @ avg</th><th class="col-num">Equity</th><th class="col-num">P&amp;L</th><th class="col-num">HYPE</th><th class="col-num">Hold</th><th class="col-num">With orders</th></tr></thead>
            <tbody>
              {chr(10).join('              ' + r for r in rowsA)}
            </tbody>
          </table>
        </div>
      </section>

      <section class="table-section" aria-label="HYPE scenario ladder">
        <div class="table-header-row">
          <h2 class="section-title">HYPE in $5 Steps — Hold As-Is vs With Orders (BTC flat at {PB0:,.0f})</h2>
          <span class="price-note">Same construction. The HYPE ladder is 316 reduce-only sells from 85.72 to 108 (45 by 86, 507 by 90, 757 by 95, 887 by 100, all 1,047 by 108); the stops sell 350 at 83.31–83.55 and the bids buy 120 back at 82.45–83.03. HYPE is 23% of the book’s notional, so a HYPE drop with BTC flat is survivable to {d['liq_hype_only']:.2f} on today’s book even though HYPE carries 5% maintenance against BTC’s 1.25%; once the TWAPs have finished, that trigger is {AFTER['liq_hype_only']:.2f}.</span>
        </div>
        <div class="table-wrapper">
          <table class="pm-table hy-table hy-scen">
            <thead><tr><th rowspan="2">HYPE</th><th rowspan="2" class="col-num">Move</th><th colspan="3" class="hy-grp">Hold as-is</th><th colspan="5" class="hy-grp">With orders</th><th rowspan="2" class="col-num">Orders vs hold</th></tr>
            <tr><th class="col-num">Equity</th><th class="col-num">P&amp;L</th><th class="col-num">ROE</th><th class="col-num">HYPE held</th><th class="col-num">Sold @ avg</th><th class="col-num">TWAP adds @ avg</th><th class="col-num">Equity</th><th class="col-num">P&amp;L</th></tr></thead>
            <tbody>
              {chr(10).join('              ' + r for r in rowsB)}
            </tbody>
          </table>
        </div>
      </section>

      <section class="table-section" aria-label="Joint scenario grid">
        <div class="table-header-row">
          <h2 class="section-title">Both Legs — Equity With Orders (Hold As-Is Beneath), BTC Down the Side, HYPE Across</h2>
          <span class="price-note">Each cell: equity with orders on a straight path to that BTC/HYPE pair, and hold-as-is equity underneath. LIQ = the path crosses maintenance margin before arriving. Outlined cells sit closest to the beta-consistent pair (HYPE moving 1.32× BTC); at BTC 100k the beta-consistent HYPE is 113.82, off the right edge.</span>
        </div>
        <div class="table-wrapper">
          <table class="pm-table hy-table hy-grid">
            <thead><tr><th class="hy-grid-corner">BTC ↓ · HYPE →</th>{gridhead}</tr></thead>
            <tbody>
              {chr(10).join('              ' + r for r in gridrows)}
            </tbody>
          </table>
        </div>
      </section>

      <section class="table-section" aria-label="Scenario methodology">
        <div class="table-header-row"><h2 class="section-title">How the Scenarios Are Built — and What They Leave Out</h2></div>
        <div class="pm-method">
          <div class="pm-method-block"><span class="pm-method-h">The book, as read</span><p>clearinghouseState, frontendOpenOrders, webData2 (TWAP states) and userFunding for 0xD71a…95Bc, fetched in-browser from app.hyperliquid.xyz at {d['as_of']}. Long 4.21507 BTC at {d['bent']:,.1f} (40× cross) and 1,180.82 HYPE at {d['hent']} (10× cross); equity {usd(EQ0,2)}; maintenance {usd(d['maint0'])} (BTC at 1.25% of notional, HYPE at 5% — half the initial margin at each asset’s maximum leverage). The model’s liquidation prices, {d['liq_btc_only']:,.0f} for BTC alone and {d['liq_hype_only']:.2f} for HYPE alone, reproduce the two liquidationPx figures the exchange reports for the account to the dollar — which pins down the maintenance fractions, though not what happens after the trigger.</p></div>
          <div class="pm-method-block"><span class="pm-method-h">Hold as-is</span><p>Equity at a rung = today’s equity + 4.21507 × (BTC − {PB0:,.0f}) + 1,180.82 × (HYPE − {PH0}). The rung is marked liquidated if equity falls below maintenance anywhere on the straight path from today’s marks to the rung (for the BTC-alone table, HYPE is held at {PH0}); both are linear in the path, so the crossing is solved exactly. ROE is the P&amp;L divided by today’s equity.</p></div>
          <div class="pm-method-block"><span class="pm-method-h">With orders</span><p>The path is walked in 2,000 steps. Reduce-only limit sells fill at their limit price when the mark reaches it (the BTC ladder’s cumulative size and notional were read at $500 intervals from 81,000 to 85,000 and the HYPE ladder’s at $0.50–$1 intervals from 85.72 to 108; fills are interpolated within an interval — none of the $5k / $5 rungs falls inside a ladder, but the HYPE-on-beta points of 92.66, 99.71 and 106.77 do, so those cells carry a few dollars of interpolation). Stop-markets fill at their trigger less 0.03% (BTC) / 0.1% (HYPE) of slippage. Scale-in bids fill at their limit. A buy that would exceed initial margin at the account’s leverage settings is skipped, as the exchange would skip it; a reduce-only sell never exceeds the position. Fees are assumed at 0.035% taker (stops, TWAP slices) and 0.010% maker (limit fills) — the base schedule would lower every with-orders figure by $15–25. Funding is not charged.</p></div>
          <div class="pm-method-block"><span class="pm-method-h">TWAP timing — the biggest single assumption</span><p>The tables spread the remainder of each TWAP (0.664 BTC, 332 HYPE) evenly along the path, so it fills at the average of today’s price and the rung, and a longer path buys less of it by any given level. That is the middle of three cases. With HYPE flat, the with-orders figure at 85k / 90k / 95k / 100k is {usd(S['85000']['eq']/1000,1)}k / {usd(S['90000']['eq']/1000,1)}k / {usd(S['95000']['eq']/1000,1)}k / {usd(S['100000']['eq']/1000,1)}k if the TWAPs are cancelled, {usd(a85['ord']['eq']/1000,1)}k / {usd(a90['ord']['eq']/1000,1)}k / {usd(A[95000]['ord']['eq']/1000,1)}k / {usd(a100['ord']['eq']/1000,1)}k on the path assumption (the tables), and {usd(TF['85000']['eq']/1000,1)}k / {usd(TF['90000']['eq']/1000,1)}k / {usd(TF['95000']['eq']/1000,1)}k / {usd(TF['100000']['eq']/1000,1)}k if they finish near today’s price before the move — the likelier case for a +25% move, since the TWAPs end in ~80 hours. On the downside the same choice moves the with-orders trigger from {a75['ord']['liq'][0]:,.0f} (tables) to {TF['75000']['liq'][0]:,.0f} (TWAPs done first), and with the TWAPs cancelled the 75k rung is survived; HYPE at 70 with BTC flat is {usd(b70['ord']['eq'])} on the tables and a liquidation at {d['TFH70']['liq'][1]:.2f} if the TWAPs finish first. Today’s liquidation prices expire with the TWAPs: at unchanged prices the finished book is {AFTER['b']:.3f} BTC + {AFTER['h']:,.0f} HYPE ({usd(AFTER['ntl']/1000)}k, {AFTER['lev']:.1f}×) with triggers {AFTER['liq_btc_only']:,.0f} / {AFTER['liq_joint']:,.0f} / {AFTER['liq_hype_only']:.2f}.</p></div>
          <div class="pm-method-block"><span class="pm-method-h">HYPE on beta</span><p>Ordinary least squares of HYPE’s daily log return on BTC’s over the last 60 days gives β 1.32 with correlation 0.68 — an R² of 0.46, so the beta line explains less than half of HYPE’s daily variance. “HYPE on beta” moves HYPE by 1.32× BTC’s simple percentage move (on log returns the 100k point would be 114.9 rather than 113.82). On the three large BTC days of Sep 1–4 HYPE moved 1.2×, 1.3× and 1.7× BTC’s percentage. The joint trigger depends on the co-move actually realised: {CM['0']:,.0f} if HYPE sits still, {CM['1']:,.0f} at 1×, {CM['1.32']:,.0f} at the measured beta, {CM['2']:,.0f} at 2× and {CM['3']:,.0f} at 3×.</p></div>
          <div class="pm-method-block"><span class="pm-method-h">What is not modelled</span><p>Liquidation is treated as the end of the scenario, not as a cash flow: on Hyperliquid a cross account that crosses maintenance is closed by market orders (20% of the position at a time above $100k of notional), any collateral left after the closes stays with the trader, and only a backstop liquidation — equity under two-thirds of maintenance without a successful close on the book — forfeits the lot, so the two downside rungs are worth somewhere between nothing and the ≈{usd(EQT)} of maintenance margin the account holds at the trigger. The path is a straight line; a round trip that touches the stops and then rallies (the BTC stops sit 0.7–0.9% below the mark and the HYPE stops 1.9–2.2% below; at this summer’s realised volatility levels that close get touched roughly two days in three) would leave the book smaller on the way up than the table shows. Funding is left out, and its horizon matters: at the last-24h rate of {usd(d['fund_day'])} a day the 80-hour TWAP window costs about $320, but a month-long path to 100k costs about $2,900. Nothing here is a forecast of where BTC or HYPE go — the rungs are the question you asked, priced.</p></div>
        </div>
      </section>
"""
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenarios_section.html'), 'w').write(html)
print("section written:", len(html), "chars;", len(rowsA), "BTC rows,", len(rowsB), "HYPE rows,", len(gridrows), "grid rows; beta cols", beta_col)
