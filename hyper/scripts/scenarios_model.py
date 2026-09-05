#!/usr/bin/env python3
"""Portfolio scenario model for the Hyper tab (Section 3).
State as of 2026-09-05 14:46:52Z, pulled in-browser from api.hyperliquid.xyz (clearinghouseState,
frontendOpenOrders, webData2.twapStates, userFunding, candleSnapshot).
Two books per scenario: HOLD-AS-IS (today's positions marked at the scenario prices, nothing executes)
and WITH ORDERS (every resting instruction executes along a straight-line path from today's marks to the
scenario prices: reduce-only take-profit ladders, stop-markets, scale-in bids, and the two buy TWAPs).
"""
import json, os, math

AS_OF = "2026-09-05 14:46 UTC"
EQ0 = 27566.69
B0, PB0, BENT = 4.21507, 79691.0, 80812.7
H0, PH0, HENT = 1180.82, 85.1693, 85.1642
MM_B, MM_H = 0.0125, 0.05          # maintenance = half of 1/maxLev (BTC 40x, HYPE 10x)
IM_B, IM_H = 1/40, 1/10            # initial margin at the account's leverage settings
TAKER, MAKER = 0.00035, 0.00010
BETA = 1.32                        # HYPE daily beta to BTC, 60d (corr 0.68)
FUND_DAY = 96.33                   # last 24h funding paid (BTC 67.36 + HYPE 28.97)

# resting instructions (frontendOpenOrders / webData2, 14:46Z)
BTC_STOPS = [(79100,.1),(79050,.1),(79025,.1),(79005,.1),(78990,.1),(78980,.1)]              # stop-market, reduce-only
HYPE_STOPS = [(83.55,50),(83.5,50),(83.45,50),(83.35,50),(83.33,50),(83.32,50),(83.31,50)]
BTC_BIDS = [78435,78414,78394,78374,78353,78333,78312,78292,78272,78251,78231,78210,78190]     # 0.01 each, opening
HYPE_BIDS = [83.026,82.995,82.965,82.935,82.905,82.874,82.844,82.814,82.783,82.753,82.723,82.692,82.662,82.632,82.602,82.571,82.541,82.511,82.48,82.45]  # 6 each
# reduce-only take-profit ladders: cumulative (size, notional) at price levels (piecewise-linear between)
BTC_TP = [(80500,0,0),(81000,.015,1215),(81500,.195,15842),(82000,.375,30557),(82500,.57,46596),(83000,.8393,68897),
          (83500,1.7693,146321),(84000,2.7142,225470),(84500,2.8942,240635),(85000,3.0893,257163)]
HYPE_TP = [(85.5,0,0),(86,45,3864),(86.5,192,16543),(87,267,23049),(87.5,342,29593),(88,417,36175),(88.5,434,37676),
           (89,457,39717),(89.5,484,42126),(90,507,44190),(91,557,48713),(92,607,53287),(93,657,57911),(94,707,62586),
           (95,757,67312),(96,807,72087),(97,827,74017),(98,847,75967),(99,867,77937),(100,887,79927),(101,907,81938),
           (102,927,83969),(103,947,86020),(104,967,88091),(105,987,90182),(106,1007,92294),(107,1027,94425),(108,1047,96577)]
TW_B_REM, TW_H_REM = 1.0 - 0.33582, 500 - 167.86     # remaining TWAP size (BTC 1.0 / HYPE 500 over 7,230 min from Sep 3 22:18Z)
TW_MIN_REM = 7230 - 2429

def cum(ladder, p):
    """cumulative (size, notional) executed at or below price p (ladder sorted ascending)."""
    if p < ladder[0][0]: return 0.0, 0.0
    for i in range(1, len(ladder)):
        p0, s0, n0 = ladder[i-1]; p1, s1, n1 = ladder[i]
        if p <= p1:
            f = (p - p0) / (p1 - p0)
            return s0 + f*(s1-s0), n0 + f*(n1-n0)
    return ladder[-1][1], ladder[-1][2]

def hold(x, y):
    """hold-as-is along a straight path to (x,y). Equity and maintenance are both linear in the path
    parameter t, so the liquidation crossing (equity = maintenance) is solved exactly."""
    liq = None
    f0 = EQ0 - (MM_B*B0*PB0 + MM_H*H0*PH0)                      # buffer at t=0 (>0)
    f1 = (EQ0 + B0*(x-PB0) + H0*(y-PH0)) - (MM_B*B0*x + MM_H*H0*y)  # buffer at t=1
    if f1 < 0:
        t = f0/(f0-f1)
        liq = (PB0 + (x-PB0)*t, PH0 + (y-PH0)*t)
    eq = EQ0 + B0*(x-PB0) + H0*(y-PH0); mt = MM_B*B0*x + MM_H*H0*y
    return dict(eq=eq, pnl=eq-EQ0, b=B0, h=H0, maint=mt, liq=liq, ntl=B0*x+H0*y)

def orders(x, y, steps=2000, twap=True):
    """with resting orders along a straight path to (x,y). TWAP remainder spread evenly over the path (IM-gated)."""
    cash = EQ0 - B0*PB0 - H0*PH0
    b, h = B0, H0
    tp_b_done = tp_h_done = 0.0
    bstops = list(BTC_STOPS); hstops = list(HYPE_STOPS); bbids = list(BTC_BIDS); hbids = list(HYPE_BIDS)
    twb = TW_B_REM if twap else 0.0; twh = TW_H_REM if twap else 0.0
    twb_f = twh_f = 0.0; twb_ntl = twh_ntl = 0.0
    sold_b = sold_h = 0.0; sold_b_ntl = sold_h_ntl = 0.0
    liq = None; fees = 0.0
    im = lambda bb, hh, pb, ph: bb*pb*IM_B + hh*ph*IM_H
    for i in range(1, steps+1):
        pb = PB0 + (x-PB0)*i/steps; ph = PH0 + (y-PH0)*i/steps
        # TWAP slice (spread over the path)
        qb = twb/steps if twap else 0.0; qh = twh/steps if twap else 0.0
        if qb > 0 and cash + b*pb + h*ph >= im(b+qb, h, pb, ph):
            cash -= qb*pb*(1+TAKER); fees += qb*pb*TAKER; b += qb; twb_f += qb; twb_ntl += qb*pb
        if qh > 0 and cash + b*pb + h*ph >= im(b, h+qh, pb, ph):
            cash -= qh*ph*(1+TAKER); fees += qh*ph*TAKER; h += qh; twh_f += qh; twh_ntl += qh*ph
        # take-profit ladders (reduce-only limit sells, maker)
        if pb > PB0:
            s, n = cum(BTC_TP, pb)
            if s > tp_b_done:
                d = min(s - tp_b_done, b); dn = (n - sold_b_ntl) if d == s - tp_b_done else d*pb
                cash += dn*(1-MAKER); fees += dn*MAKER; b -= d; tp_b_done = s; sold_b += d; sold_b_ntl += dn
        if ph > PH0:
            s, n = cum(HYPE_TP, ph)
            if s > tp_h_done:
                d = min(s - tp_h_done, h); dn = (n - sold_h_ntl) if d == s - tp_h_done else d*ph
                cash += dn*(1-MAKER); fees += dn*MAKER; h -= d; tp_h_done = s; sold_h += d; sold_h_ntl += dn
        # stops (stop-market, reduce-only, taker; small slip)
        while bstops and pb <= bstops[0][0]:
            tp, q = bstops.pop(0); q = min(q, b); px = tp*(1-0.0003); cash += q*px*(1-TAKER); fees += q*px*TAKER; b -= q; sold_b += q; sold_b_ntl += q*px
        while hstops and ph <= hstops[0][0]:
            tp, q = hstops.pop(0); q = min(q, h); px = tp*(1-0.001); cash += q*px*(1-TAKER); fees += q*px*TAKER; h -= q; sold_h += q; sold_h_ntl += q*px
        # scale-in bids (opening, maker, IM-gated)
        while bbids and pb <= bbids[0]:
            p = bbids.pop(0)
            if cash + b*pb + h*ph >= im(b+.01, h, pb, ph): cash -= .01*p*(1+MAKER); fees += .01*p*MAKER; b += .01
        while hbids and ph <= hbids[0]:
            p = hbids.pop(0)
            if cash + b*pb + h*ph >= im(b, h+6, pb, ph): cash -= 6*p*(1+MAKER); fees += 6*p*MAKER; h += 6
        eq = cash + b*pb + h*ph; mt = MM_B*b*pb + MM_H*h*ph
        if eq < mt and liq is None: liq = (pb, ph); break
    eq = cash + b*x + h*y; mt = MM_B*b*x + MM_H*h*y
    return dict(eq=eq, pnl=eq-EQ0, b=b, h=h, maint=mt, liq=liq, ntl=b*x+h*y, fees=fees,
                sold_b=sold_b, sold_b_px=(sold_b_ntl/sold_b if sold_b else 0), sold_h=sold_h, sold_h_px=(sold_h_ntl/sold_h if sold_h else 0),
                twb=twb_f, twb_px=(twb_ntl/twb_f if twb_f else 0), twh=twh_f, twh_px=(twh_ntl/twh_f if twh_f else 0))

BTC_RUNGS = [70000, 75000, 80000, 85000, 90000, 95000, 100000]
HYPE_RUNGS = [70, 75, 80, 85, 90, 95, 100, 105, 110]

out = dict(as_of=AS_OF, eq0=EQ0, b0=B0, pb0=PB0, bent=BENT, h0=H0, ph0=PH0, hent=HENT, beta=BETA, fund_day=FUND_DAY,
           tw_b_rem=TW_B_REM, tw_h_rem=TW_H_REM, tw_min_rem=TW_MIN_REM,
           maint0=MM_B*B0*PB0 + MM_H*H0*PH0, ntl0=B0*PB0+H0*PH0)
buf0 = EQ0 - out['maint0']
out['liq_btc_only'] = PB0*(1 - buf0/(B0*PB0*(1-MM_B)))
out['liq_hype_only'] = PH0*(1 - buf0/(H0*PH0*(1-MM_H)))
out['liq_joint'] = PB0*(1 - buf0/(B0*PB0*(1-MM_B) + H0*PH0*BETA*(1-MM_H)))

# Table A: BTC ladder, HYPE flat; plus HYPE-at-beta variant
A = []
for x in BTC_RUNGS:
    y_beta = PH0*(1 + BETA*(x/PB0 - 1))
    A.append(dict(x=x, pct=x/PB0-1, y_beta=y_beta, hold=hold(x, PH0), ord=orders(x, PH0), hold_beta=hold(x, y_beta), ord_beta=orders(x, y_beta)))
# Table B: HYPE ladder, BTC flat
B = []
for y in HYPE_RUNGS:
    B.append(dict(y=y, pct=y/PH0-1, hold=hold(PB0, y), ord=orders(PB0, y)))
# Grid: with-orders and hold-as-is equity
G = []
for x in BTC_RUNGS:
    row = []
    for y in HYPE_RUNGS:
        row.append(dict(x=x, y=y, hold=hold(x, y), ord=orders(x, y)))
    G.append(row)
# TWAP sensitivities on the headline rungs (HYPE flat): cancelled / path-midpoint (the tables) / filled first at today's price
S = {x: orders(x, PH0, twap=False) for x in (85000, 90000, 95000, 100000)}
def orders_twap_first(x, y):
    """TWAP remainder filled at today's marks before the path starts (taker fee), then the path with no TWAP."""
    global EQ0, B0, H0
    e0, b0, h0 = EQ0, B0, H0
    fee = (TW_B_REM*PB0 + TW_H_REM*PH0)*TAKER
    EQ0, B0, H0 = e0 - fee, b0 + TW_B_REM, h0 + TW_H_REM
    try: r = orders(x, y, twap=False)
    finally: EQ0, B0, H0 = e0, b0, h0
    return r
TF = {x: orders_twap_first(x, PH0) for x in (75000, 85000, 90000, 95000, 100000)}
TF70 = orders_twap_first(70000, PH0)
TFH70 = orders_twap_first(PB0, 70)
# the book once the TWAPs are done with prices unchanged (fees only; funding not charged, as elsewhere)
bA, hA = B0 + TW_B_REM, H0 + TW_H_REM
eA = EQ0 - (TW_B_REM*PB0 + TW_H_REM*PH0)*TAKER
mA = MM_B*bA*PB0 + MM_H*hA*PH0
bufA = eA - mA
AFTER = dict(b=bA, h=hA, eq=eA, maint=mA, ntl=bA*PB0 + hA*PH0, lev=(bA*PB0 + hA*PH0)/eA,
             liq_btc_only=PB0*(1 - bufA/(bA*PB0*(1-MM_B))), liq_hype_only=PH0*(1 - bufA/(hA*PH0*(1-MM_H))),
             liq_joint=PB0*(1 - bufA/(bA*PB0*(1-MM_B) + hA*PH0*BETA*(1-MM_H))))
# joint trigger for a range of realised co-moves
COMOVE = {str(k): PB0*(1 - buf0/(B0*PB0*(1-MM_B) + H0*PH0*k*(1-MM_H))) for k in (0, 1, 1.32, 2, 3)}
# equity left at the first liquidation trigger (BTC alone): the maintenance margin at that price
EQ_AT_TRIGGER = MM_B*B0*out['liq_btc_only'] + MM_H*H0*PH0
out.update(A=A, B=B, G=G, S=S, TF=TF, TF70=TF70, TFH70=TFH70, AFTER=AFTER, COMOVE=COMOVE, eq_at_trigger=EQ_AT_TRIGGER)

def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, float): return round(o, 4)
    return o
json.dump(clean(out), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenarios_out.json'), 'w'), indent=1)

# console summary
print(f"as of {AS_OF}: eq {EQ0:,.0f}; BTC {B0} @ {PB0:,.0f} (entry {BENT:,.1f}); HYPE {H0} @ {PH0} (entry {HENT}); maint {out['maint0']:,.0f}; ntl {out['ntl0']:,.0f}; lev {out['ntl0']/EQ0:.1f}x")
print(f"liq: BTC-only {out['liq_btc_only']:,.0f} (HL quotes 75,285) | HYPE-only {out['liq_hype_only']:.2f} (HL 68.82) | joint {out['liq_joint']:,.0f}")
print("\nA) BTC ladder, HYPE flat @ %.2f | hold-as-is | with orders" % PH0)
for r in A:
    h, o = r['hold'], r['ord']
    hl = f"LIQ@{h['liq'][0]:,.0f}" if h['liq'] else f"{h['eq']:8,.0f} ({h['pnl']:+8,.0f})"
    ol = f"LIQ@{o['liq'][0]:,.0f}" if o['liq'] else f"{o['eq']:8,.0f} ({o['pnl']:+8,.0f}) BTC {o['b']:.3f} sold {o['sold_b']:.3f}@{o['sold_b_px']:,.0f} twap {o['twb']:.3f}@{o['twb_px']:,.0f} fees {o['fees']:,.0f}"
    hb, ob = r['hold_beta'], r['ord_beta']
    hbl = f"LIQ@{hb['liq'][0]:,.0f}" if hb['liq'] else f"{hb['eq']:8,.0f}"
    obl = f"LIQ@{ob['liq'][0]:,.0f}" if ob['liq'] else f"{ob['eq']:8,.0f}"
    print(f"  BTC {r['x']:>7,} ({r['pct']:+6.1%}) | {hl:>24} | {ol} || HYPE@beta {r['y_beta']:6.2f}: hold {hbl:>12} orders {obl:>12}")
print("\nB) HYPE ladder, BTC flat @ %.0f" % PB0)
for r in B:
    h, o = r['hold'], r['ord']
    hl = f"LIQ@{h['liq'][1]:.2f}" if h['liq'] else f"{h['eq']:8,.0f} ({h['pnl']:+8,.0f})"
    ol = f"LIQ@{o['liq'][1]:.2f}" if o['liq'] else f"{o['eq']:8,.0f} ({o['pnl']:+8,.0f}) HYPE {o['h']:.0f} sold {o['sold_h']:.0f}@{o['sold_h_px']:.2f} twap {o['twh']:.0f}@{o['twh_px']:.2f}"
    print(f"  HYPE {r['y']:>4} ({r['pct']:+6.1%}) | {hl:>24} | {ol}")
print("\nGrid (with orders equity; * = liquidated on path). rows BTC, cols HYPE")
print("        " + "".join(f"{y:>9}" for y in HYPE_RUNGS))
for row in G:
    print(f"{row[0]['x']:>7,} " + "".join((f"{'LIQ':>9}" if c['ord']['liq'] else f"{c['ord']['eq']:>9,.0f}") for c in row))
print("\nGrid (hold-as-is equity)")
for row in G:
    print(f"{row[0]['x']:>7,} " + "".join((f"{'LIQ':>9}" if c['hold']['liq'] else f"{c['hold']['eq']:>9,.0f}") for c in row))
print("\nTWAP sensitivity (HYPE flat): cancelled | path-midpoint (tables) | filled first at today's price")
for x in (85000, 90000, 95000, 100000):
    print(f"  BTC {x:,}: {S[x]['eq']:,.0f} | {A[BTC_RUNGS.index(x)]['ord']['eq']:,.0f} | {TF[x]['eq']:,.0f}")
print(f"  75k path liq: cancelled {'survives' if not S.get(75000) else ''} | tables {A[1]['ord']['liq']} | twap-first {TF[75000]['liq']}")
print(f"  70k path liq: tables {A[0]['ord']['liq']} | twap-first {TF70['liq']}")
print(f"  HYPE 70 (BTC flat): tables {B[0]['ord']['eq']:,.0f} liq {B[0]['ord']['liq']} | twap-first eq {TFH70['eq']:,.0f} liq {TFH70['liq']}")
print(f"\nAfter the TWAPs (prices unchanged): {AFTER['b']:.3f} BTC + {AFTER['h']:,.0f} HYPE, ntl {AFTER['ntl']:,.0f}, {AFTER['lev']:.1f}x, maint {AFTER['maint']:,.0f}; liq BTC-only {AFTER['liq_btc_only']:,.0f}, HYPE-only {AFTER['liq_hype_only']:.2f}, joint {AFTER['liq_joint']:,.0f}")
print("co-move joint triggers:", {k: round(v) for k, v in COMOVE.items()})
print(f"equity at first trigger (BTC alone): {EQ_AT_TRIGGER:,.0f}; 2/3 of it {EQ_AT_TRIGGER*2/3:,.0f}")
S75 = orders(75000, PH0, twap=False); print(f"75k with orders, TWAPs cancelled: eq {S75['eq']:,.0f} maint {S75['maint']:,.0f} liq {S75['liq']}")
