#!/usr/bin/env python3
"""Sep 9 AM verification pass: reproduce Sep 8 PM published fairs (closes unchanged),
then BTC ladder color at fresh spot + rolled T."""
import numpy as np
from scipy.stats import norm

# ---- caps from Sep 8 closes (re-verified this run, unchanged) ----
px = {'NVDA': 225.73, 'AAPL': 316.22, 'GOOGL': 338.36, 'MSFT': 493.95, 'AMZN': 256.97}
sh = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
caps = {k: px[k] * sh[k] for k in px}
names = list(caps)
c = np.array([caps[k] for k in names])
print("caps $B:", {k: round(v, 1) for k, v in caps.items()})
lead = (caps['NVDA'] / caps['AAPL'] - 1) * 100
print(f"lead {lead:.2f}% / ${caps['NVDA']-caps['AAPL']:.1f}B; AAPL cushion "
      f"{(caps['AAPL']/caps['GOOGL']-1)*100:.2f}% / ${caps['AAPL']-caps['GOOGL']:.1f}B")

SIG_REL = 0.02          # pairwise relative sigma / day
sig_d = SIG_REL / np.sqrt(2)  # independent per-name daily sigma

def rank_probs(T):
    """Exact-rank probabilities via 481-node Gauss-Hermite-style quadrature.
    Returns (P_rank1, P_rank2, P_rank3) arrays over names."""
    s = sig_d * np.sqrt(T)
    z = np.linspace(-8, 8, 481)
    w = norm.pdf(z) * (z[1] - z[0])
    lnc = np.log(c)
    n = len(c)
    p1 = np.zeros(n); p2 = np.zeros(n); p3 = np.zeros(n)
    for i in range(n):
        others = [j for j in range(n) if j != i]
        # a_ij = (ln ci - ln cj)/s ; X_i - X_j = a_ij*s + s(Zi - Zj)
        F = np.array([norm.cdf((lnc[i] - lnc[j]) / s + z) for j in others])  # P(Xj < Xi | Zi=z)
        G = 1 - F
        prod_all = F.prod(axis=0)
        p1[i] = (w * prod_all).sum()
        # exactly one other beats i
        s2 = np.zeros_like(z)
        for a in range(len(others)):
            s2 += G[a] * prod_all / np.where(F[a] > 1e-300, F[a], 1e-300)
        p2[i] = (w * s2).sum()
        # exactly two others beat i
        s3 = np.zeros_like(z)
        for a in range(len(others)):
            for b in range(a + 1, len(others)):
                m = prod_all / np.where(F[a] * F[b] > 1e-300, F[a] * F[b], 1e-300)
                s3 += G[a] * G[b] * m
        p3[i] = (w * s3).sum()
    return p1, p2, p3

# ---- December, T = 80 trading days ----
p1, p2, p3 = rank_probs(80)
dec_raw = p1 * 100
dec_pub = dec_raw * 0.9925  # 0.75 small-leg allowance, Dec legs only
print("\nDEC raw  :", {names[i]: round(dec_raw[i], 2) for i in range(5)})
print("DEC pub  :", {names[i]: round(dec_pub[i], 2) for i in range(5)})
print("expected : NVDA 78.23 AAPL 16.87 GOOGL 3.61 MSFT 0.54 AMZN 0.00")

# ---- September, T = 16 trading days ----
q1, q2, q3 = rank_probs(16)
print("\nSEP crown:", {names[i]: round(q1[i] * 100, 2) for i in range(5)})
print("expected : NVDA 97.86 AAPL 2.12 GOOGL 0.01")
print("SEP 2nd  :", {names[i]: round(q2[i] * 100, 2) for i in range(5)})
print("expected : AAPL 91.12 GOOGL 6.66 NVDA 2.13")
print("SEP 3rd  :", {names[i]: round(q3[i] * 100, 2) for i in range(5)})
print("expected : GOOGL 85.95 MSFT 7.38 AAPL 6.67 NVDA 0.01")

# ---- P(+-5pts / wk) for Dec legs (5-trading-day cap shock, MC) ----
rng = np.random.default_rng(7)
NMC = 4000
zshock = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(5)
base = dec_pub.copy()
cnt = np.zeros(5)
c0 = c.copy()
lnc0 = np.log(c0)
zq = np.linspace(-8, 8, 241)
wq = norm.pdf(zq) * (zq[1] - zq[0])
sT = sig_d * np.sqrt(75)  # 75 trading days left after the week
for m in range(NMC):
    lc = lnc0 + zshock[m]
    pr = np.zeros(5)
    for i in range(5):
        others = [j for j in range(5) if j != i]
        F = np.array([norm.cdf((lc[i] - lc[j]) / sT + zq) for j in others])
        pr[i] = (wq * F.prod(axis=0)).sum()
    fair = pr * 100 * 0.9925
    cnt += (np.abs(fair - base) >= 5)
pm5 = cnt / NMC * 100
print("\nP(+-5/wk):", {names[i]: round(pm5[i]) for i in range(5)}, " expected 47/42/3/<1/0")

# ---- BTC ladder color ----
S_bake, T_bake = 78414.25, 122.1
S = 78815.99            # CoinGecko live, this run
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)  # Dec 31 midnight ET
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} vs Sep8PM 78483.14: {(S/78483.14-1)*100:+.2f}%  vs bake {S_bake}: {(S/S_bake-1)*100:+.2f}%")
print(f"T = {T:.1f} d   anchor needed touch {(85000/S-1)*100:+.1f}%")
mids = {85000: 70.5, 90000: 47.0, 95000: 34.5, 100000: 23.5, 60000: 26.5, 55000: 22.5, 50000: 14.5}
for H, mid in mids.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  mid {mid:5.1f}  resid {mid-fair:+.1f}")
