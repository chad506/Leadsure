#!/usr/bin/env python3
"""Sep 10 AM run (pre-open verification pass): re-confirm the Sep 9 finals against the
history pages, reproduce every Sep 9 PM published fair from them at T=15/79 (calibration),
then BTC ladder color at the fresh spot + rolled T. No new close pre-open — if calibration
holds, caps/fairs/edges stand as published."""
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

# ---- calibration: Sep 9 finals (re-confirmed to the cent Sep 10 13:2xZ, no revisions),
#      T = 15/79 -> must reproduce the Sep 9 PM published fairs ----
px9 = {'NVDA': 223.67, 'AAPL': 315.34, 'GOOGL': 330.65, 'MSFT': 491.65, 'AMZN': 252.40}
caps = {k: px9[k] * SH[k] for k in px9}
c9 = np.array([caps[k] for k in NAMES])
print("caps $B:", {k: round(v, 1) for k, v in caps.items()})
print(f"lead {(caps['NVDA']/caps['AAPL']-1)*100:.2f}% / ${caps['NVDA']-caps['AAPL']:.1f}B; "
      f"AAPL cushion {(caps['AAPL']/caps['GOOGL']-1)*100:.2f}% / ${caps['AAPL']-caps['GOOGL']:.1f}B")
p1, _, _ = rank_probs(c9, 79)
dec_pub = p1 * 100 * 0.9925  # 0.75 small-leg allowance, Dec legs only
print("DEC pub  :", {NAMES[i]: round(dec_pub[i], 2) for i in range(5)},
      " expect 77.99/17.85/2.85/0.56/0.00")
q1, q2, q3 = rank_probs(c9, 15)
print("SEP crown:", {NAMES[i]: round(q1[i]*100, 2) for i in range(5)}, " expect 97.79/2.21/0.00")
print("SEP 2nd  :", {NAMES[i]: round(q2[i]*100, 2) for i in range(5)}, " expect 94.22-AAPL/3.50-GOOGL/2.21-NVDA")
print("SEP 3rd  :", {NAMES[i]: round(q3[i]*100, 2) for i in range(5)}, " expect 86.06-GOOGL/10.41-MSFT/3.52-AAPL")

# ---- P(+-5pts / wk) re-run (same seed/method as Sep 9 PM -> expect 48/44/1) ----
rng = np.random.default_rng(7)
NMC = 4000
zshock = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(5)
lnc0 = np.log(c9)
zq = np.linspace(-8, 8, 241)
wq = norm.pdf(zq) * (zq[1] - zq[0])
sT = sig_d * np.sqrt(74)
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
print("P(+-5/wk):", {NAMES[i]: round(cnt[i] / NMC * 100) for i in range(5)}, " expect 48/44/1")

# ---- stale-mid edges (last walked mids, Sep 1 03:59Z — labeled color; fairs stand pre-open) ----
stale = {'dec-NVDA': ('NVDA', 77.5), 'dec-AAPL': ('AAPL', 13.75), 'dec-GOOGL': ('GOOGL', 8.5)}
for k, (nm, mid) in stale.items():
    i = NAMES.index(nm)
    print(f"{k}: fair {dec_pub[i]:.2f} vs stale mid {mid} -> edge {mid - dec_pub[i]:+.2f}")
print(f"sep2AAPL: fair {q2[1]*100:.2f} vs stale mid 81.5 -> edge {81.5 - q2[1]*100:+.2f}")
print(f"sep3NVDA: fair {q3[0]*100:.2f} vs stale mid 1.6 -> edge {1.6 - q3[0]*100:+.2f}")

# ---- BTC ladder color: CoinGecko live Sep 10 13:2xZ ----
S_bake = 78414.25
S = 76869.85            # CoinGecko live (-3.4%/24h; range 76748.30-79605.60); Kraken page 77957 (-1.35%) — sources ~1.4% apart, disclosed
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} vs Sep9PM 78010.44: {(S/78010.44-1)*100:+.2f}%  vs bake {S_bake}: {(S/S_bake-1)*100:+.2f}%")
print(f"T = {T:.1f} d   anchor needed touch {(85000/S-1)*100:+.1f}%")
mids = {85000: 70.5, 90000: 47.0, 95000: 34.5, 100000: 23.5, 60000: 26.5, 55000: 22.5, 50000: 14.5}
for H, mid in mids.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  mid {mid:5.1f}  resid {mid-fair:+.1f}")
