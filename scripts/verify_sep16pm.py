#!/usr/bin/env python3
"""Sep 16 PM run — first close after the Sep 16 01:45Z interactive walk.
1. Trading-day counts after the Sep 16 close.
2. Calibration: reproduce every Sep 16 AM published fair on the Sep 15 finals at T=11/75.
3. Fresh fairs on the Sep 16 closes (stockanalysis history pages, ~23:15Z pull —
   the Sep 12 lesson: a 23:1xZ pull can precede settled finals; next-morning pass locks them).
4. Edges vs the Sep 16 01:45Z walk mids (scripts/largest_books_sep16.txt — one session behind, disclosed).
5. P(+-5/wk); BTC ladder residuals vs the Sep 15 01:10Z walked mids (labeled color).
AUTODATA: Sep 16 22:45Z cron silent (34th missed feed run); 23:09Z poke touching
fetch/poke pushed via the extraheader path."""
import re
import numpy as np
from scipy.stats import norm

SH = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
NAMES = list(SH)
SIG_REL = 0.02
sig_d = SIG_REL / np.sqrt(2)

# ---- trading days after the Sep 16 close ----
T_SEP = int(np.busday_count('2026-09-17', '2026-10-01'))
T_DEC = int(np.busday_count('2026-09-17', '2027-01-01', holidays=['2026-11-26', '2026-12-25']))
print(f"T = {T_SEP} / {T_DEC}  (expect 10 / 74)")

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

# ---- CALIBRATION on the Sep 15 finals at T = 11/75 (the AM run's published fairs) ----
px15 = {'NVDA': 212.17, 'AAPL': 331.34, 'GOOGL': 344.98, 'MSFT': 497.12, 'AMZN': 248.42}
c15 = np.array([px15[k] * SH[k] for k in NAMES])
p1c, _, _ = rank_probs(c15, 75)
calD = p1c * 100 * 0.9925
r1c, r2c, r3c = rank_probs(c15, 11)
print("CAL Dec  :", {NAMES[i]: round(calD[i], 2) for i in range(5)}, " expect 57.90/34.77/5.87/0.71/0.00")
print("CAL crown:", {NAMES[i]: round(r1c[i]*100, 2) for i in range(5)}, " expect 79.03/20.94/0.03")
print("CAL 2nd  :", {NAMES[i]: round(r2c[i]*100, 2) for i in range(5)}, " expect 20.87-NVDA/77.75-AAPL/1.38-GOOGL")
print("CAL 3rd  :", {NAMES[i]: round(r3c[i]*100, 2) for i in range(5)}, " expect 0.10-NVDA/1.31-AAPL/95.97-GOOGL/2.62-MSFT")
assert abs(calD[0] - 57.90) < 0.02 and abs(calD[1] - 34.77) < 0.02, "Dec calibration failed"
assert abs(r1c[0]*100 - 79.03) < 0.02 and abs(r1c[1]*100 - 20.94) < 0.02, "crown calibration failed"

# ---- the Sep 16 closes (history pages ~23:15Z; % cross-checked against Sep 15 finals) ----
px = {'NVDA': 213.90, 'AAPL': 332.41, 'GOOGL': 342.87, 'MSFT': 490.30, 'AMZN': 245.96}
caps = {k: px[k] * SH[k] for k in NAMES}
for k in NAMES:
    print(f"  {k}: {px[k]} ({(px[k]/px15[k]-1)*100:+.2f}%)  cap ${caps[k]:.1f}B")
lead_pct = (caps['NVDA']/caps['AAPL']-1)*100; lead_b = caps['NVDA']-caps['AAPL']
cush_pct = (caps['AAPL']/caps['GOOGL']-1)*100; cush_b = caps['AAPL']-caps['GOOGL']
print(f"lead {lead_pct:.2f}% / ${lead_b:.1f}B (was 5.51%/$268.0B); cushion {cush_pct:.2f}% / ${cush_b:.1f}B (was 15.87%/$666.5B)")

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

# ---- edges vs the Sep 16 01:45Z walk mids (one session behind, disclosed) ----
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

# ---- BTC color (CoinGecko live primary; Kraken cross; Coinbase re-served the AM print — discarded) ----
S = 75981.82        # CoinGecko live (-1.10%/24h, range 75,038.12-76,901.55)
S_kr = 75862.00     # Kraken cross-check (-1.44%/24h)
S_am = 75868.26     # Sep 16 AM print (CoinGecko primary)
S_bake = 78414.25
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} (CoinGecko live; Kraken {S_kr}, {(S_kr/S-1)*100:+.2f}% apart; Coinbase snapshot-stale, discarded):")
print(f"  {(S/S_am-1)*100:+.2f}% vs the AM print; {(S/S_bake-1)*100:+.2f}% vs bake {S_bake}; T {T:.1f}d; needed touch {(85000/S-1)*100:+.1f}%")
mids_b = {85000: 68.0, 90000: 48.5, 95000: 34.5, 100000: 23.5, 110000: 12.0,
          60000: 27.5, 55000: 19.5, 50000: 14.0}
for H, mid in mids_b.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  walk-mid {mid:5.1f}  resid {mid-fair:+.1f}")
