#!/usr/bin/env python3
"""Sep 16 AM run — pre-open verification pass (the Sep 4 AM precedent).
The Sep 16 01:45Z interactive session walked the Largest-Company complex and
revised MSFT's Sep 15 final to $497.12; this morning's pass re-checks ALL FIVE
Sep 15 finals against the history pages (every one confirmed, incl. the MSFT
revision — the history page now serves $497.12 itself) and re-reproduces every
published fair (Dec 57.90/34.77/5.87/0.71; crown 79.03/20.94/0.03; seat
77.75/20.87/1.38; 3rd 95.97/2.62/1.31/0.10; P(+-5/wk) 61/60/7) before
anything is restamped. Premarket + BTC are labeled color, never model inputs.
AUTODATA: 33rd consecutive missed feed run (Sep 16 12:45Z cron silent; the
13:08Z poke touching fetch/poke pushed via the extraheader path, unanswered)."""
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

# ---- Sep 15 FINALS re-checked this morning (stockanalysis history pages, ~13:15Z):
# NVDA 212.17 +0.57%, AAPL 331.34 -0.52%, GOOGL 344.98 -1.26%,
# MSFT 497.12 -1.64% (the 01:45Z revision HOLDS on the history page itself),
# AMZN 248.42 -2.02% -- ALL FIVE unchanged vs the Sep 16 01:45Z bake.
px = {'NVDA': 212.17, 'AAPL': 331.34, 'GOOGL': 344.98, 'MSFT': 497.12, 'AMZN': 248.42}
caps = {k: px[k] * SH[k] for k in NAMES}
cr = np.array([caps[k] for k in NAMES])
print("caps $B:", {k: round(v, 1) for k, v in caps.items()})
print(f"lead {(caps['NVDA']/caps['AAPL']-1)*100:.2f}% / ${caps['NVDA']-caps['AAPL']:.1f}B; "
      f"AAPL cushion {(caps['AAPL']/caps['GOOGL']-1)*100:.2f}% / ${caps['AAPL']-caps['GOOGL']:.1f}B")

# ---- calibration: reproduce every published fair at T = 11 / 75 ----
T_SEP, T_DEC = 11, 75
p1f, _, _ = rank_probs(cr, T_DEC)
dec_pub = p1f * 100 * 0.9925
print("DEC fair :", {NAMES[i]: round(dec_pub[i], 2) for i in range(5)},
      " expect 57.90/34.77/5.87/0.71/0.00")
r1, r2, r3 = rank_probs(cr, T_SEP)
print("SEP crown:", {NAMES[i]: round(r1[i]*100, 2) for i in range(5)}, " expect 79.03/20.94/0.03")
print("SEP 2nd  :", {NAMES[i]: round(r2[i]*100, 2) for i in range(5)},
      " expect 20.87-NVDA/77.75-AAPL/1.38-GOOGL")
print("SEP 3rd  :", {NAMES[i]: round(r3[i]*100, 2) for i in range(5)},
      " expect 0.10-NVDA/1.31-AAPL/95.97-GOOGL/2.62-MSFT")

# ---- P(+-5pts / wk), same seed/method as prior runs ----
rng = np.random.default_rng(7)
NMC = 4000
zshock = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(5)
lnc0 = np.log(cr)
zq = np.linspace(-8, 8, 241)
wq = norm.pdf(zq) * (zq[1] - zq[0])
sT = sig_d * np.sqrt(T_DEC - 5)
cnt = np.zeros(5)
for m in range(NMC):
    lc = lnc0 + zshock[m]
    pr = np.zeros(5)
    for i in range(5):
        others = [j for j in range(5) if j != i]
        F = np.array([norm.cdf((lc[i] - lc[j]) / sT + zq) for j in others])
        pr[i] = (wq * F.prod(axis=0)).sum()
    fair = pr * 100 * 0.9925
    cnt += (np.abs(fair - dec_pub) >= 5)
print("P(+-5/wk):", {NAMES[i]: round(cnt[i] / NMC * 100) for i in range(5)}, " expect 61/60/7")

# ---- premarket color (9:09-9:12 ET, stockanalysis quote pages; NEVER a model input) ----
pm = {'NVDA': 213.93, 'AAPL': 332.95, 'GOOGL': 345.93, 'MSFT': 495.25, 'AMZN': 248.80}
pmc = {k: pm[k] * SH[k] for k in NAMES}
print("\npremarket:", {k: f"{pm[k]} ({(pm[k]/px[k]-1)*100:+.2f}%)" for k in NAMES})
print(f"premarket-implied lead {(pmc['NVDA']/pmc['AAPL']-1)*100:.2f}% / ${pmc['NVDA']-pmc['AAPL']:.1f}B "
      f"(finals 5.51%); implied cushion {(pmc['AAPL']/pmc['GOOGL']-1)*100:.2f}%")

# ---- BTC color: CoinGecko live primary again (fresh + 0.06% from Coinbase cross);
#      Coinbase cross 75,826.24 (-2.04%/24h). Sep 15 PM primary was Coinbase 77,000.77.
S_bake = 78414.25
S = 75868.26          # CoinGecko live (-1.40%/24h, range 75,038.12-77,162.60)
S_cb = 75826.24       # Coinbase cross-check
S_pm = 77000.77       # Sep 15 PM print (Coinbase primary)
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} (CoinGecko live; Coinbase {S_cb}, {(S_cb/S-1)*100:+.2f}% apart): "
      f"{(S/S_pm-1)*100:+.2f}% vs the Sep15 PM print; {(S/S_bake-1)*100:+.2f}% vs bake {S_bake}")
print(f"T = {T:.1f} d   anchor needed touch {(85000/S-1)*100:+.1f}%")
# residuals vs the Sep 15 01:10Z WALKED mids (the freshest BTC books on the page)
mids_b = {85000: 68.0, 90000: 48.5, 95000: 34.5, 100000: 23.5, 110000: 12.0,
          60000: 27.5, 55000: 19.5, 50000: 14.0}
for H, mid in mids_b.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  walk-mid {mid:5.1f}  resid {mid-fair:+.1f}")
