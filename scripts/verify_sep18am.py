#!/usr/bin/env python3
"""Sep 18 AM run — pre-open verification pass (Sep 4/Sep 12 AM precedents): MSFT REVISED.
1. Trading-day counts (expect T = 9/73, unchanged after the Sep 17 close).
2. Sep 17 finals vs the history pages: NVDA/AAPL/GOOGL/AMZN re-confirmed to the cent;
   MSFT REVISED $497.66 (+1.50%) -> $497.75 (+1.52%) — the Sep 12 lesson again: a
   ~23:2xZ history-page pull can precede the settled finals; the morning pass locks them.
3. Calibration: reproduce every Sep 17 PM published fair EXACTLY on the PM inputs
   (Dec 62.51/31.93/4.40/0.42/0.00; crown 87.80/12.20/0.00; seat 87.37/12.19/0.44;
   3rd 98.30-GOOGL/1.25-MSFT/0.43-AAPL/0.01-NVDA; P(+-5/wk) 61/59/4).
4. Fresh fairs on the REVISED finals; re-mark only what moves at 2dp.
5. Premarket color (8:59-9:10 ET, labeled, never a model input) — GOOGL +2.23% the tape's story.
6. BTC ladder residuals vs the Sep 15 01:10Z walked mids (labeled color).
AUTODATA: Sep 18 12:45Z cron silent (37th missed feed run); 13:09Z poke touching
fetch/poke pushed via the extraheader path (ac19e8cf)."""
import re
import numpy as np
from scipy.stats import norm

SH = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
NAMES = list(SH)
SIG_REL = 0.02
sig_d = SIG_REL / np.sqrt(2)

# ---- trading days (pre-open Sep 18: the Sep 17 close is the last print) ----
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

# ---- CALIBRATION on the Sep 17 PM inputs (MSFT 497.66 as pulled ~23:2xZ) ----
pxPM = {'NVDA': 219.34, 'AAPL': 337.00, 'GOOGL': 347.33, 'MSFT': 497.66, 'AMZN': 251.19}
cPM = np.array([pxPM[k] * SH[k] for k in NAMES])
p1c, _, _ = rank_probs(cPM, T_DEC)
calD = p1c * 100 * 0.9925
r1c, r2c, r3c = rank_probs(cPM, T_SEP)
print("CAL Dec  :", {NAMES[i]: round(calD[i], 2) for i in range(5)}, " expect 62.51/31.93/4.40/0.42/0.00")
print("CAL crown:", {NAMES[i]: round(r1c[i]*100, 2) for i in range(5)}, " expect 87.80/12.20/0.00")
print("CAL 2nd  :", {NAMES[i]: round(r2c[i]*100, 2) for i in range(5)}, " expect 12.19-NVDA/87.37-AAPL/0.44-GOOGL")
print("CAL 3rd  :", {NAMES[i]: round(r3c[i]*100, 2) for i in range(5)}, " expect 0.01-NVDA/0.43-AAPL/98.30-GOOGL/1.25-MSFT")
assert abs(calD[0] - 62.51) < 0.02 and abs(calD[1] - 31.93) < 0.02, "Dec calibration failed"
assert abs(r1c[0]*100 - 87.80) < 0.02 and abs(r1c[1]*100 - 12.20) < 0.02, "crown calibration failed"
assert abs(r2c[1]*100 - 87.37) < 0.02 and abs(r2c[0]*100 - 12.19) < 0.02, "seat calibration failed"
assert abs(r3c[2]*100 - 98.30) < 0.02 and abs(r3c[3]*100 - 1.25) < 0.02, "3rd calibration failed"

# ---- P(+-5/wk) calibration on the PM inputs ----
def p5wk(cr, dec):
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
    return {NAMES[i]: round(cnt[i]/NMC*100) for i in range(5)}
print("CAL P(+-5/wk):", p5wk(cPM, calD), " expect 61/59/4")

# ---- the REVISED Sep 17 finals (history pages 13:1xZ Sep 18) ----
px = {'NVDA': 219.34, 'AAPL': 337.00, 'GOOGL': 347.33, 'MSFT': 497.75, 'AMZN': 251.19}
px16 = {'NVDA': 213.90, 'AAPL': 332.41, 'GOOGL': 342.87, 'MSFT': 490.30, 'AMZN': 245.96}
chg = {'NVDA': 2.54, 'AAPL': 1.38, 'GOOGL': 1.30, 'MSFT': 1.52, 'AMZN': 2.13}
caps = {k: px[k] * SH[k] for k in NAMES}
for k in NAMES:
    d = (px[k]/px16[k]-1)*100
    assert abs(d - chg[k]) < 0.02, f"{k} change% mismatch: {d:.2f} vs page {chg[k]}"
    print(f"  {k}: {px[k]} ({d:+.2f}%)  cap ${caps[k]:.1f}B")
lead_pct = (caps['NVDA']/caps['AAPL']-1)*100; lead_b = caps['NVDA']-caps['AAPL']
cush_pct = (caps['AAPL']/caps['GOOGL']-1)*100; cush_b = caps['AAPL']-caps['GOOGL']
print(f"lead {lead_pct:.2f}% / ${lead_b:.1f}B (PM published 7.24%/$358.4B); cushion {cush_pct:.2f}% / ${cush_b:.1f}B (PM 17.05%/$721.1B)")

cr = np.array([caps[k] for k in NAMES])
p1f, _, _ = rank_probs(cr, T_DEC)
dec = p1f * 100 * 0.9925
r1, r2, r3 = rank_probs(cr, T_SEP)
crown = r1*100; seat = r2*100; third = r3*100
print("DEC fair :", {NAMES[i]: round(dec[i], 2) for i in range(5)})
print("SEP crown:", {NAMES[i]: round(crown[i], 2) for i in range(5)})
print("SEP 2nd  :", {NAMES[i]: round(seat[i], 2) for i in range(5)})
print("SEP 3rd  :", {NAMES[i]: round(third[i], 2) for i in range(5)})
print("P(+-5/wk):", p5wk(cr, dec))

# deltas vs the PM published fairs at 2dp
pubD = {'NVDA': 62.51, 'AAPL': 31.93, 'GOOGL': 4.40, 'MSFT': 0.42, 'AMZN': 0.00}
for i, k in enumerate(NAMES):
    if round(dec[i], 2) != pubD[k]:
        print(f"  MOVED dec-{k}: {pubD[k]} -> {round(dec[i],2)}")
pub3 = {'NVDA': 0.01, 'AAPL': 0.43, 'GOOGL': 98.30, 'MSFT': 1.25, 'AMZN': 0.00}
for i, k in enumerate(NAMES):
    if round(third[i], 2) != pub3[k]:
        print(f"  MOVED 3rd-{k}: {pub3[k]} -> {round(third[i],2)}")
pubC = {'NVDA': 87.80, 'AAPL': 12.20, 'GOOGL': 0.00}
for i, k in enumerate(NAMES[:3]):
    if round(crown[i], 2) != pubC[k]:
        print(f"  MOVED crown-{k}: {pubC[k]} -> {round(crown[i],2)}")
pubS = {'NVDA': 12.19, 'AAPL': 87.37, 'GOOGL': 0.44}
for i, k in enumerate(NAMES[:3]):
    if round(seat[i], 2) != pubS[k]:
        print(f"  MOVED seat-{k}: {pubS[k]} -> {round(seat[i],2)}")

# ---- premarket color (labeled, never a model input) ----
pm = {'NVDA': (219.01, -0.15, '9:06'), 'AAPL': (337.01, +0.00, '9:07'),
      'GOOGL': (355.06, +2.23, '8:59'), 'MSFT': (497.79, +0.01, '9:10'),
      'AMZN': (251.55, +0.14, '9:08')}
pmcaps = {k: pm[k][0] * SH[k] for k in NAMES}
pml = (pmcaps['NVDA']/pmcaps['AAPL']-1)*100
pmcu = (pmcaps['AAPL']/pmcaps['GOOGL']-1)*100
print(f"\npremarket-implied lead {pml:.2f}% / ${pmcaps['NVDA']-pmcaps['AAPL']:.1f}B (finals 7.24%); cushion {pmcu:.2f}% / ${pmcaps['AAPL']-pmcaps['GOOGL']:.1f}B (finals 17.05%)")
for k in NAMES:
    print(f"  {k}: {pm[k][0]} ({pm[k][1]:+.2f}%, {pm[k][2]} ET)  cap ${pmcaps[k]:.1f}B")

# ---- BTC color (CoinGecko live primary; Kraken live cross — both fresh this run) ----
S = 77718.58        # CoinGecko live (+1.7%/24h, range 75,971.64-77,760.47)
S_kr = 77961.00     # Kraken live cross (+1.37%/24h)
S_pm = 76541.77     # Sep 17 PM print (CoinGecko primary)
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
