#!/usr/bin/env python3
"""Largest-Company tab re-bake, Sep 16 2026 01:45Z interactive session.
1. Re-verify the Sep 15 finals (stockanalysis history pages + CNBC restQuote, two sources):
   MSFT REVISED 496.91 -> 497.12 (-1.64%, not -1.68%); NVDA/AAPL/GOOGL/AMZN confirmed to the cent.
2. Calibration: reproduce every Sep 15 PM published fair from the Sep 15 PM inputs before trusting a new number.
3. Fresh fairs on the settled finals at T = 11 / 75.
4. Edges / RV / executable size against the Sep 16 01:45Z book walk (scripts/largest_books_sep16.txt):
   twenty books — all five Dec names + SpaceX/Tesla/Aramco tails, the September crown (NVDA/AAPL/GOOGL/MSFT),
   seat (AAPL/NVDA/GOOGL/MSFT) and 3rd-place (GOOGL/MSFT/AAPL/NVDA) partitions — the crown and seat books'
   first walk since Sep 1.
Outputs a JSON blob the bake step reads."""
import json, re, sys
import numpy as np
from scipy.stats import norm

SH = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
NAMES = list(SH)
SIG_REL = 0.02
sig_d = SIG_REL / np.sqrt(2)

def rank_probs(c, T):
    s = sig_d * np.sqrt(T)
    z = np.linspace(-8, 8, 481)
    w = norm.pdf(z) * (z[1] - z[0])
    lnc = np.log(c)
    n = len(c)
    p1 = np.zeros(n); p2 = np.zeros(n); p3 = np.zeros(n)
    for i in range(n):
        others = [j for j in range(n) if j != i]
        F = np.array([norm.cdf((lnc[i] - lnc[j]) / s + z) for j in others])
        G = 1 - F
        prod_all = F.prod(axis=0)
        p1[i] = (w * prod_all).sum()
        s2 = np.zeros_like(z)
        for a in range(len(others)):
            s2 += G[a] * prod_all / np.where(F[a] > 1e-300, F[a], 1e-300)
        p2[i] = (w * s2).sum()
        s3 = np.zeros_like(z)
        for a in range(len(others)):
            for b in range(a + 1, len(others)):
                m = prod_all / np.where(F[a] * F[b] > 1e-300, F[a] * F[b], 1e-300)
                s3 += G[a] * G[b] * m
        p3[i] = (w * s3).sum()
    return p1, p2, p3

# ---- CALIBRATION on the Sep 15 PM run's own inputs (MSFT 496.91 as it used) ----
px_pm = {'NVDA': 212.17, 'AAPL': 331.34, 'GOOGL': 344.98, 'MSFT': 496.91, 'AMZN': 248.42}
cpm = np.array([px_pm[k] * SH[k] for k in NAMES])
p1c, _, _ = rank_probs(cpm, 75)
r1c, r2c, r3c = rank_probs(cpm, 11)
cal = {'dec': [round(x*100*0.9925, 2) for x in p1c], 'crown': [round(x*100, 2) for x in r1c],
       'r2': [round(x*100, 2) for x in r2c], 'r3': [round(x*100, 2) for x in r3c]}
print("CAL Dec  :", dict(zip(NAMES, cal['dec'])), " expect 57.90/34.77/5.87/0.70/0.00")
print("CAL crown:", dict(zip(NAMES, cal['crown'])), " expect 79.03/20.94/0.03")
print("CAL 2nd  :", dict(zip(NAMES, cal['r2'])), " expect 20.87-NVDA/77.75-AAPL/1.38-GOOGL")
print("CAL 3rd  :", dict(zip(NAMES, cal['r3'])), " expect 0.10-NVDA/1.31-AAPL/96.01-GOOGL/2.58-MSFT")
assert abs(cal['dec'][0]-57.90) < 0.02 and abs(cal['dec'][1]-34.77) < 0.02 and abs(cal['crown'][0]-79.03) < 0.02, "calibration failed"

# ---- the SETTLED Sep 15 finals (two sources agree; MSFT revised) ----
px_sep14 = {'NVDA': 210.96, 'AAPL': 333.08, 'GOOGL': 349.39, 'MSFT': 505.41, 'AMZN': 253.54}
px = {'NVDA': 212.17, 'AAPL': 331.34, 'GOOGL': 344.98, 'MSFT': 497.12, 'AMZN': 248.42}
caps = {k: px[k] * SH[k] for k in NAMES}
for k in NAMES:
    print(f"  {k}: {px[k]} ({(px[k]/px_sep14[k]-1)*100:+.2f}%)  cap ${caps[k]:.1f}B")
lead_pct = (caps['NVDA']/caps['AAPL']-1)*100; lead_b = caps['NVDA']-caps['AAPL']
cush_pct = (caps['AAPL']/caps['GOOGL']-1)*100; cush_b = caps['AAPL']-caps['GOOGL']
print(f"lead {lead_pct:.2f}% / ${lead_b:.1f}B; cushion {cush_pct:.2f}% / ${cush_b:.1f}B")
cr = np.array([caps[k] for k in NAMES])
T_SEP, T_DEC = 11, 75
p1f, _, _ = rank_probs(cr, T_DEC)
dec = p1f * 100 * 0.9925
r1, r2, r3 = rank_probs(cr, T_SEP)
crown = r1*100; seat = r2*100; third = r3*100
print("DEC fair :", {NAMES[i]: round(dec[i], 2) for i in range(5)})
print("SEP crown:", {NAMES[i]: round(crown[i], 2) for i in range(5)})
print("SEP 2nd  :", {NAMES[i]: round(seat[i], 2) for i in range(5)})
print("SEP 3rd  :", {NAMES[i]: round(third[i], 2) for i in range(5)})

# ---- P(+-5pts / wk) ----
rng = np.random.default_rng(7)
NMC = 4000
zshock = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(5)
lnc0 = np.log(cr)
zq = np.linspace(-8, 8, 241); wq = norm.pdf(zq) * (zq[1] - zq[0])
sT = sig_d * np.sqrt(T_DEC - 5)
cnt = np.zeros(5)
for m in range(NMC):
    lc = lnc0 + zshock[m]
    pr = np.zeros(5)
    for i in range(5):
        others = [j for j in range(5) if j != i]
        F = np.array([norm.cdf((lc[i] - lc[j]) / sT + zq) for j in others])
        pr[i] = (wq * F.prod(axis=0)).sum()
    cnt += (np.abs(pr * 100 * 0.9925 - dec) >= 5)
p5 = {NAMES[i]: round(cnt[i] / NMC * 100) for i in range(5)}
print("P(+-5/wk):", p5)

# ---- books ----
BK = {}
cur = None
for line in open('/home/claude/Leadsure/scripts/largest_books_sep16.txt'):
    line = line.rstrip('\n')
    if line.startswith('#'):
        cur = line[1:].split(' ')[0]; BK[cur] = {'ts': int(line.split('ts=')[1]), 'B': [], 'A': []}
    elif line.startswith('B ') or line == 'B':
        BK[cur]['B'] = [(float(a), float(b)) for a, b in re.findall(r'([\d.]+)x([\d.]+)', line)]
    elif line.startswith('A ') or line == 'A':
        BK[cur]['A'] = [(float(a), float(b)) for a, b in re.findall(r'([\d.]+)x([\d.]+)', line)]

def walk(levels, limit, side):
    """USD and shares available at prices that still beat `limit` (fair, in ¢/100)."""
    usd = sh = 0.0
    for p, s in levels:
        if (side == 'buy' and p <= limit) or (side == 'sell' and p >= limit):
            usd += p * s; sh += s
    return usd, sh

def vwap(levels, usd_cap, limit, side):
    spent = sh = 0.0
    for p, s in levels:
        if not ((side == 'buy' and p <= limit) or (side == 'sell' and p >= limit)): break
        take = min(s, (usd_cap - spent) / p)
        if take <= 0: break
        spent += take * p; sh += take
        if spent >= usd_cap - 1e-9: break
    return spent, sh, (spent / sh if sh else float('nan'))

FAIR = {
 'dec-NVDA': dec[0], 'dec-AAPL': dec[1], 'dec-GOOGL': dec[2], 'dec-MSFT': dec[3], 'dec-AMZN': dec[4],
 'dec-SPCX': 0.0, 'dec-TSLA': 0.0, 'dec-ARMCO': 0.0,
 'sep-crownNVDA': crown[0], 'sep-crownAAPL': crown[1], 'sep-crownGOOGL': crown[2], 'sep-crownMSFT': crown[3],
 'sep-sep2AAPL': seat[1], 'sep-sep2NVDA': seat[0], 'sep-sep2GOOGL': seat[2], 'sep-sep2MSFT': seat[3],
 'sep-sep3GOOGL': third[2], 'sep-sep3MSFT': third[3], 'sep-sep3AAPL': third[1], 'sep-sep3NVDA': third[0],
}
out = {'px': px, 'caps': caps, 'lead_pct': lead_pct, 'lead_b': lead_b, 'cush_pct': cush_pct, 'cush_b': cush_b,
       'dec': dict(zip(NAMES, dec.tolist())), 'crown': dict(zip(NAMES, crown.tolist())),
       'seat': dict(zip(NAMES, seat.tolist())), 'third': dict(zip(NAMES, third.tolist())), 'p5': p5, 'rows': {}}
print()
print(f"{'book':16s} {'bid':>6s} {'ask':>6s} {'mid':>6s} {'fair':>6s} {'edge':>7s} {'RV':>6s} {'usd@fair':>9s} side")
for k, f in FAIR.items():
    b = BK[k]
    bid = b['B'][0][0]*100 if b['B'] else None; ask = b['A'][0][0]*100 if b['A'] else None
    if bid is None and ask is None: continue
    mid = (bid + ask)/2 if bid is not None else ask/2
    edge = mid - f
    rv_yes = f/mid if mid > 0 else float('nan')
    rv_no = (100-f)/(100-mid) if mid < 100 else float('nan')
    # executable: cheap => buy YES asks <= fair ; rich => sell YES into bids >= fair (== buy NO)
    if edge < 0:
        usd, sh = walk(b['A'], f/100, 'buy'); side = 'BUY YES (asks ≤ fair)'
    else:
        usd, sh = walk(b['B'], f/100, 'sell'); side = 'SELL YES / BUY NO (bids ≥ fair)'
    out['rows'][k] = dict(bid=bid, ask=ask, mid=mid, fair=f, edge=edge, rv_yes=rv_yes, rv_no=rv_no, usd_at_fair=usd, sh_at_fair=sh,
                          nb=len(b['B']), na=len(b['A']), usd_b=sum(p*s for p, s in b['B']), usd_a=sum(p*s for p, s in b['A']), side=side)
    print(f"{k:16s} {bid if bid is not None else float('nan'):6.2f} {ask if ask is not None else float('nan'):6.2f} {mid:6.2f} {f:6.2f} {edge:+7.2f} {rv_yes:6.2f} {usd:9.0f} {side}")
json.dump(out, open('/tmp/largest_sep16.json', 'w'), indent=1, default=float)
print("\nwrote /tmp/largest_sep16.json")
