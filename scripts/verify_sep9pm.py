#!/usr/bin/env python3
"""Sep 9 PM run: calibration first (reproduce Sep 8 PM published fairs from the
Sep 8 closes at T=16/80), then fresh fairs on the Sep 9 closes at T=15/79,
P(+-5/wk), and BTC ladder color at fresh spot + rolled T."""
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

def report(px, Tsep, Tdec, tag):
    caps = {k: px[k] * SH[k] for k in px}
    c = np.array([caps[k] for k in NAMES])
    print(f"\n===== {tag} =====")
    print("caps $B:", {k: round(v, 1) for k, v in caps.items()})
    print(f"lead {(caps['NVDA']/caps['AAPL']-1)*100:.2f}% / ${caps['NVDA']-caps['AAPL']:.1f}B; "
          f"AAPL cushion {(caps['AAPL']/caps['GOOGL']-1)*100:.2f}% / ${caps['AAPL']-caps['GOOGL']:.1f}B")
    p1, _, _ = rank_probs(c, Tdec)
    dec_pub = p1 * 100 * 0.9925  # 0.75 small-leg allowance, Dec legs only
    print("DEC raw  :", {NAMES[i]: round(p1[i]*100, 2) for i in range(5)})
    print("DEC pub  :", {NAMES[i]: round(dec_pub[i], 2) for i in range(5)})
    q1, q2, q3 = rank_probs(c, Tsep)
    print("SEP crown:", {NAMES[i]: round(q1[i]*100, 2) for i in range(5)})
    print("SEP 2nd  :", {NAMES[i]: round(q2[i]*100, 2) for i in range(5)})
    print("SEP 3rd  :", {NAMES[i]: round(q3[i]*100, 2) for i in range(5)})
    return c, dec_pub

# ---- calibration: Sep 8 closes, T = 16/80 -> must reproduce Sep 8 PM published ----
px8 = {'NVDA': 225.73, 'AAPL': 316.22, 'GOOGL': 338.36, 'MSFT': 493.95, 'AMZN': 256.97}
report(px8, 16, 80, "CALIBRATION (Sep 8 closes, T 16/80) — expect Dec 78.23/16.87/3.61/0.54/0.00, "
       "crown 97.86/2.12/0.01, 2nd 91.12/6.66/2.13, 3rd 85.95/7.38/6.67")

# ---- fresh: Sep 9 closes, T = 15/79 ----
px9 = {'NVDA': 223.67, 'AAPL': 315.34, 'GOOGL': 330.65, 'MSFT': 491.65, 'AMZN': 252.40}
c9, dec_pub9 = report(px9, 15, 79, "FRESH (Sep 9 closes, T 15/79)")

# ---- P(+-5pts / wk) for Dec legs (5-trading-day cap shock, MC) ----
rng = np.random.default_rng(7)
NMC = 4000
zshock = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(5)
lnc0 = np.log(c9)
zq = np.linspace(-8, 8, 241)
wq = norm.pdf(zq) * (zq[1] - zq[0])
sT = sig_d * np.sqrt(74)  # 74 trading days left after the week
cnt = np.zeros(5)
for m in range(NMC):
    lc = lnc0 + zshock[m]
    pr = np.zeros(5)
    for i in range(5):
        others = [j for j in range(5) if j != i]
        F = np.array([norm.cdf((lc[i] - lc[j]) / sT + zq) for j in others])
        pr[i] = (wq * F.prod(axis=0)).sum()
    fair = pr * 100 * 0.9925
    cnt += (np.abs(fair - dec_pub9) >= 5)
pm5 = cnt / NMC * 100
print("\nP(+-5/wk):", {NAMES[i]: round(pm5[i]) for i in range(5)})

# ---- stale-mid edges (last walked mids, Sep 1 03:59Z — labeled color) ----
stale = {'dec-NVDA': ('NVDA', 77.5), 'dec-AAPL': ('AAPL', 13.75), 'dec-GOOGL': ('GOOGL', 8.5)}
for k, (nm, mid) in stale.items():
    i = NAMES.index(nm)
    print(f"{k}: fair {dec_pub9[i]:.2f} vs stale mid {mid} -> edge {mid - dec_pub9[i]:+.2f}")
q1, q2, q3 = rank_probs(c9, 15)
print(f"sep2AAPL: fair {q2[1]*100:.2f} vs stale mid 81.5 -> edge {81.5 - q2[1]*100:+.2f}")
print(f"sep3NVDA: fair {q3[0]*100:.2f} vs stale mid 1.6 -> edge {1.6 - q3[0]*100:+.2f}")

# ---- BTC ladder color ----
S_bake = 78414.25
S = 78010.44            # CoinGecko live, this run (-0.60%/24h; 24h range 77832.79-79701.36)
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} vs Sep9AM 78815.99: {(S/78815.99-1)*100:+.2f}%  vs Sep8PM 78483.14: "
      f"{(S/78483.14-1)*100:+.2f}%  vs bake {S_bake}: {(S/S_bake-1)*100:+.2f}%")
print(f"T = {T:.1f} d   anchor needed touch {(85000/S-1)*100:+.1f}%")
mids = {85000: 70.5, 90000: 47.0, 95000: 34.5, 100000: 23.5, 60000: 26.5, 55000: 22.5, 50000: 14.5}
for H, mid in mids.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  mid {mid:5.1f}  resid {mid-fair:+.1f}")
