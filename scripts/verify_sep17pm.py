#!/usr/bin/env python3
"""Sep 17 PM run — the Thursday close re-deals the fairs (risk-on, NVIDIA leads).
1. Trading-day counts after the Sep 17 close (expect T = 9/73).
2. Calibration: reproduce every Sep 16 PM / Sep 17 AM published fair on the
   Sep 16 finals at T = 10/74 (Dec 59.68/34.14/4.95/0.48/0.00; crown 82.25/17.74/0.01;
   seat 81.60/17.72/0.68; 3rd 97.76/1.55/0.66/0.03; P(+-5/wk) 61/60/5).
3. Fresh fairs on the Sep 17 closes (history pages ~23:2xZ — the Sep 12 lesson:
   a 23:xxZ pull can precede settled finals; the next-morning pass locks them).
4. Edges + depth-at-fair vs the Sep 16 01:45Z walk ladders
   (scripts/largest_books_sep16.txt — two sessions behind, disclosed).
5. P(+-5/wk); BTC ladder residuals vs the Sep 15 01:10Z walked mids (labeled color).
AUTODATA: Sep 17 22:45Z cron silent (36th missed feed run); ~23:10Z poke touching
fetch/poke pushed via the extraheader path (cfb79667), unanswered."""
import re
import numpy as np
from scipy.stats import norm

SH = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
NAMES = list(SH)
SIG_REL = 0.02
sig_d = SIG_REL / np.sqrt(2)

# ---- trading days after the Sep 17 close ----
T_SEP = int(np.busday_count('2026-09-18', '2026-10-01'))
T_DEC = int(np.busday_count('2026-09-18', '2027-01-01', holidays=['2026-11-26', '2026-12-25']))
print(f"T = {T_SEP} / {T_DEC}  (expect 9 / 73)")

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

# ---- CALIBRATION on the Sep 16 finals at T = 10/74 (the AM run's re-confirmed fairs) ----
px16 = {'NVDA': 213.90, 'AAPL': 332.41, 'GOOGL': 342.87, 'MSFT': 490.30, 'AMZN': 245.96}
c16 = np.array([px16[k] * SH[k] for k in NAMES])
p1c, _, _ = rank_probs(c16, 74)
calD = p1c * 100 * 0.9925
r1c, r2c, r3c = rank_probs(c16, 10)
print("CAL Dec  :", {NAMES[i]: round(calD[i], 2) for i in range(5)}, " expect 59.68/34.14/4.95/0.48/0.00")
print("CAL crown:", {NAMES[i]: round(r1c[i]*100, 2) for i in range(5)}, " expect 82.25/17.74/0.01")
print("CAL 2nd  :", {NAMES[i]: round(r2c[i]*100, 2) for i in range(5)}, " expect 17.72-NVDA/81.60-AAPL/0.68-GOOGL")
print("CAL 3rd  :", {NAMES[i]: round(r3c[i]*100, 2) for i in range(5)}, " expect 0.03-NVDA/0.66-AAPL/97.76-GOOGL/1.55-MSFT")
assert abs(calD[0] - 59.68) < 0.02 and abs(calD[1] - 34.14) < 0.02, "Dec calibration failed"
assert abs(r1c[0]*100 - 82.25) < 0.02 and abs(r1c[1]*100 - 17.74) < 0.02, "crown calibration failed"
assert abs(r2c[1]*100 - 81.60) < 0.02 and abs(r2c[0]*100 - 17.72) < 0.02, "seat calibration failed"
assert abs(r3c[2]*100 - 97.76) < 0.02 and abs(r3c[3]*100 - 1.55) < 0.02, "3rd calibration failed"

# ---- the Sep 17 closes (history pages ~23:2xZ; % cross-checked against Sep 16 finals) ----
px = {'NVDA': 219.34, 'AAPL': 337.00, 'GOOGL': 347.33, 'MSFT': 497.66, 'AMZN': 251.19}
chg = {'NVDA': 2.54, 'AAPL': 1.38, 'GOOGL': 1.30, 'MSFT': 1.50, 'AMZN': 2.13}
caps = {k: px[k] * SH[k] for k in NAMES}
for k in NAMES:
    d = (px[k]/px16[k]-1)*100
    assert abs(d - chg[k]) < 0.02, f"{k} change% mismatch: {d:.2f} vs page {chg[k]}"
    print(f"  {k}: {px[k]} ({d:+.2f}%)  cap ${caps[k]:.1f}B")
lead_pct = (caps['NVDA']/caps['AAPL']-1)*100; lead_b = caps['NVDA']-caps['AAPL']
cush_pct = (caps['AAPL']/caps['GOOGL']-1)*100; cush_b = caps['AAPL']-caps['GOOGL']
print(f"lead {lead_pct:.2f}% / ${lead_b:.1f}B (was 6.03%/$294.2B); cushion {cush_pct:.2f}% / ${cush_b:.1f}B (was 16.96%/$707.9B)")

cr = np.array([caps[k] for k in NAMES])
p1f, _, _ = rank_probs(cr, T_DEC)
dec = p1f * 100 * 0.9925
r1, r2, r3 = rank_probs(cr, T_SEP)
crown = r1*100; seat = r2*100; third = r3*100
print("DEC fair :", {NAMES[i]: round(dec[i], 2) for i in range(5)})
print("SEP crown:", {NAMES[i]: round(crown[i], 2) for i in range(5)})
print("SEP 2nd  :", {NAMES[i]: round(seat[i], 2) for i in range(5)})
print("SEP 3rd  :", {NAMES[i]: round(third[i], 2) for i in range(5)})

# ---- P(+-5/wk), same seed/method ----
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
print("P(+-5/wk):", {NAMES[i]: round(cnt[i]/NMC*100) for i in range(5)})

# ---- edges + depth-at-fair vs the Sep 16 01:45Z walk ladders (two sessions behind, disclosed) ----
BK = {}
cur = None
for line in open('/home/claude/work/scripts/largest_books_sep16.txt'):
    line = line.rstrip('\n')
    if line.startswith('#'):
        cur = line[1:].split(' ')[0]; BK[cur] = {'B': [], 'A': []}
    elif line.startswith('B'):
        BK[cur]['B'] = [(float(a), float(b)) for a, b in re.findall(r'([\d.]+)x([\d.]+)', line)]
    elif line.startswith('A'):
        BK[cur]['A'] = [(float(a), float(b)) for a, b in re.findall(r'([\d.]+)x([\d.]+)', line)]
FAIR = {
 'dec-NVDA': dec[0], 'dec-AAPL': dec[1], 'dec-GOOGL': dec[2], 'dec-MSFT': dec[3], 'dec-AMZN': dec[4],
 'sep-crownNVDA': crown[0], 'sep-crownAAPL': crown[1],
 'sep-sep2AAPL': seat[1], 'sep-sep2NVDA': seat[0],
 'sep-sep3GOOGL': third[2], 'sep-sep3MSFT': third[3],
}
print(f"\n{'book':16s} {'bid':>6s} {'ask':>6s} {'mid':>6s} {'fair':>6s} {'edge':>7s} {'rvY':>5s}")
for k, f in FAIR.items():
    b = BK.get(k)
    if not b: print(f"{k:16s}  (not in walk)"); continue
    # snapshot file stores touch FIRST (B descending from best bid, A ascending from best ask)
    bid = b['B'][0][0]*100 if b['B'] else None
    ask = b['A'][0][0]*100 if b['A'] else None
    mid = ((bid or 0) + (ask or 0)) / 2 if (bid is not None and ask is not None) else (bid if bid is not None else ask)
    edge = mid - f
    print(f"{k:16s} {bid if bid is not None else float('nan'):6.2f} {ask if ask is not None else float('nan'):6.2f} {mid:6.2f} {f:6.2f} {edge:+7.2f} {f/mid if mid else float('nan'):5.2f}")

# depth-at-fair: dec-AAPL asks at/below fair, and inside fair-5
b = BK['dec-AAPL']
fair = dec[1]
at_fair = sum(p*q for p, q in b['A'] if p*100 <= fair)
in_band = sum(p*q for p, q in b['A'] if p*100 <= fair - 5)
print(f"\ndec-AAPL asks $ at-or-under fair {fair:.2f}: ${at_fair:,.0f}; at-or-under fair-5 ({fair-5:.2f}): ${in_band:,.0f}")
ask_t = b['A'][0][0]*100
print(f"dec-AAPL touch {ask_t:.1f}, edge {ask_t - fair:+.2f}, RV@ask {fair/ask_t:.2f}x, RV@mid {fair/((b['B'][0][0]*100+ask_t)/2):.2f}x")
# Apple crown: gate check for the ADD (fair-5 vs 13.0c limit and the 12.7 touch)
cf = crown[1]
print(f"Apple crown fair {cf:.2f}; fair-5 = {cf-5:.2f}; touch 12.7 -> edge {12.7-cf:+.2f}, RV {cf/12.7:.2f}x; ADD limit 13.0 {'CLEARS' if 13.0 <= cf-5 else 'GATED'}")
# MSFT 3rd leg (sell): bid side
b3 = BK['sep-sep3MSFT']
bid3 = b3['B'][0][0]*100
print(f"sep3MSFT bid {bid3:.1f} vs fair {third[3]:.2f} -> RV {third[3]/((bid3+b3['A'][0][0]*100)/2):.2f}x at mid")
# dec-NVDA NO-dollars at bids >= fair
bn = BK['dec-NVDA']
no_fair = 100 - dec[0]
no_dollars = sum((1-p)*q for p, q in bn['B'] if p*100 >= dec[0])
print(f"dec-NVDA NO fair {no_fair:.2f}; NO-dollars at YES-bids >= fair: ${no_dollars:,.0f}")

# ---- BTC color (CoinGecko live primary; Coinbase live cross; Kraken re-served the AM print — discarded) ----
S = 76541.77        # CoinGecko live (+0.50%/24h, range 75,601.71-77,024.38)
S_cb = 76545.18     # Coinbase cross-check (+0.46%/24h)
S_am = 76424.22     # Sep 17 AM print (CoinGecko primary)
S_bake = 78414.25
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} (CoinGecko live; Coinbase {S_cb}, {(S_cb/S-1)*100:+.3f}% apart; Kraken snapshot-stale at the AM cross 76,144.00, discarded):")
print(f"  {(S/S_am-1)*100:+.2f}% vs the AM print; {(S/S_bake-1)*100:+.2f}% vs bake {S_bake}; T {T:.1f}d; needed touch {(85000/S-1)*100:+.1f}%")
mids_b = {85000: 68.0, 90000: 48.5, 95000: 34.5, 100000: 23.5, 110000: 12.0,
          60000: 27.5, 55000: 19.5, 50000: 14.0}
for H, mid in mids_b.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  walk-mid {mid:5.1f}  resid {mid-fair:+.1f}")
