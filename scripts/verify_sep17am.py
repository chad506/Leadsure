#!/usr/bin/env python3
"""Sep 17 AM run — pre-open verification pass (Sep 4 AM precedent).
1. Trading-day counts (expect T = 10/74, unchanged after the Sep 16 close).
2. ALL FIVE Sep 16 finals re-confirmed against the history pages (no revisions).
3. Independent quadrature re-run must reproduce every Sep 16 PM published fair EXACTLY
   (Dec 59.68/34.14/4.95/0.48/0.00; crown 82.25/17.74/0.01; seat 81.60/17.72/0.68;
   3rd 97.76/1.55/0.66/0.03; P(+-5/wk) 61/60/5).
4. Premarket color (8:47-9:08 ET, labeled, never a model input).
5. BTC ladder residuals vs the Sep 15 01:10Z walked mids (labeled color).
AUTODATA: Sep 17 12:45Z cron silent (35th missed feed run); 13:12Z poke touching
fetch/poke pushed via the extraheader path."""
import numpy as np
from scipy.stats import norm

SH = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
NAMES = list(SH)
SIG_REL = 0.02
sig_d = SIG_REL / np.sqrt(2)

# ---- trading days (pre-open Sep 17: the Sep 16 close is the last print) ----
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

# ---- the Sep 16 finals, re-confirmed to the cent this morning (history pages ~13:1xZ) ----
px = {'NVDA': 213.90, 'AAPL': 332.41, 'GOOGL': 342.87, 'MSFT': 490.30, 'AMZN': 245.96}
caps = {k: px[k] * SH[k] for k in NAMES}
for k in NAMES:
    print(f"  {k}: {px[k]}  cap ${caps[k]:.1f}B")
lead_pct = (caps['NVDA']/caps['AAPL']-1)*100; lead_b = caps['NVDA']-caps['AAPL']
cush_pct = (caps['AAPL']/caps['GOOGL']-1)*100; cush_b = caps['AAPL']-caps['GOOGL']
print(f"lead {lead_pct:.2f}% / ${lead_b:.1f}B (expect 6.03%/$294.2B); cushion {cush_pct:.2f}% / ${cush_b:.1f}B (expect 16.96%/$707.9B)")

cr = np.array([caps[k] for k in NAMES])
p1f, _, _ = rank_probs(cr, T_DEC)
dec = p1f * 100 * 0.9925
r1, r2, r3 = rank_probs(cr, T_SEP)
crown = r1*100; seat = r2*100; third = r3*100
print("DEC fair :", {NAMES[i]: round(dec[i], 2) for i in range(5)}, " expect 59.68/34.14/4.95/0.48/0.00")
print("SEP crown:", {NAMES[i]: round(crown[i], 2) for i in range(5)}, " expect 82.25-NVDA/17.74-AAPL/0.01-GOOGL")
print("SEP 2nd  :", {NAMES[i]: round(seat[i], 2) for i in range(5)}, " expect 17.72-NVDA/81.60-AAPL/0.68-GOOGL")
print("SEP 3rd  :", {NAMES[i]: round(third[i], 2) for i in range(5)}, " expect 0.03-NVDA/0.66-AAPL/97.76-GOOGL/1.55-MSFT")
assert abs(dec[0] - 59.68) < 0.02 and abs(dec[1] - 34.14) < 0.02, "Dec calibration failed"
assert abs(crown[0] - 82.25) < 0.02 and abs(crown[1] - 17.74) < 0.02, "crown calibration failed"
assert abs(seat[1] - 81.60) < 0.02 and abs(seat[0] - 17.72) < 0.02, "seat calibration failed"
assert abs(third[2] - 97.76) < 0.02 and abs(third[3] - 1.55) < 0.02, "3rd calibration failed"

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
print("P(+-5/wk):", {NAMES[i]: round(cnt[i]/NMC*100) for i in range(5)}, " expect 61/60/5")

# ---- premarket color (labeled, never a model input) ----
pm = {'NVDA': (218.40, +2.10, '9:07'), 'AAPL': (334.16, +0.52, '9:02'),
      'GOOGL': (347.91, +1.47, '9:08'), 'MSFT': (496.04, +1.17, '8:47'),
      'AMZN': (251.15, +2.11, '8:49')}
pmcaps = {k: pm[k][0] * SH[k] for k in NAMES}
pml = (pmcaps['NVDA']/pmcaps['AAPL']-1)*100
print(f"\npremarket-implied lead {pml:.2f}% / ${pmcaps['NVDA']-pmcaps['AAPL']:.1f}B (finals 6.03%)")
for k in NAMES:
    print(f"  {k}: {pm[k][0]} ({pm[k][1]:+.2f}%, {pm[k][2]} ET)  cap ${pmcaps[k]:.1f}B")

# ---- BTC color (CoinGecko live primary; Kraken live cross) ----
S = 76424.22        # CoinGecko live (+1.2%/24h, range 75,161.24-76,682.57)
S_kr = 76144.00     # Kraken cross-check (-0.02%/24h)
S_pm = 75981.82     # Sep 16 PM print (CoinGecko primary)
S_bake = 78414.25
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} (CoinGecko live; Kraken {S_kr}, {(S_kr/S-1)*100:+.2f}% apart, both live, disclosed):")
print(f"  {(S/S_pm-1)*100:+.2f}% vs the PM print; {(S/S_bake-1)*100:+.2f}% vs bake {S_bake}; T {T:.1f}d; needed touch {(85000/S-1)*100:+.1f}%")
mids_b = {85000: 68.0, 90000: 48.5, 95000: 34.5, 100000: 23.5, 110000: 12.0,
          60000: 27.5, 55000: 19.5, 50000: 14.0}
for H, mid in mids_b.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  walk-mid {mid:5.1f}  resid {mid-fair:+.1f}")
