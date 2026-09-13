#!/usr/bin/env python3
"""Sep 13 AM run (Sunday) — WEEKEND AM PASS, A FIFTH CONFIRMATION OF THE FINALS.
No weekend close. The Sep 12 AM pass locked the Sep 11 finals (triple revision
caught); Sep 12 PM re-spot-checked the three revised prints; THIS run re-checked
ALL FIVE against the history pages — NVDA 218.29, AAPL 332.27, GOOGL 338.50,
MSFT 495.63, AMZN 256.78, every one unchanged — so caps/fairs/edges stand.
Calibration: reproduce every Sep 12 published fair EXACTLY from the finals.
BTC ladder color at the fresh CoinGecko spot + rolled T (per the Sep 5 PM precedent)."""
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

# ---- the Sep 11 FINALS (locked Sep 12 AM; ALL FIVE re-spot-checked this run — unchanged) ----
px = {'NVDA': 218.29, 'AAPL': 332.27, 'GOOGL': 338.50, 'MSFT': 495.63, 'AMZN': 256.78}
caps = {k: px[k] * SH[k] for k in NAMES}
print("caps $B:", {k: round(v, 1) for k, v in caps.items()})
print(f"  lead {(caps['NVDA']/caps['AAPL']-1)*100:.2f}% / ${caps['NVDA']-caps['AAPL']:.1f}B; "
      f"AAPL cushion {(caps['AAPL']/caps['GOOGL']-1)*100:.2f}% / ${caps['AAPL']-caps['GOOGL']:.1f}B")
cr = np.array([caps[k] for k in NAMES])

# ---- calibration: must reproduce every Sep 12 published fair EXACTLY (T = 13/77) ----
p1f, _, _ = rank_probs(cr, 77)
dec_pub = p1f * 100 * 0.9925  # 0.75 small-leg allowance, Dec legs only
print("DEC fair :", {NAMES[i]: round(dec_pub[i], 2) for i in range(5)},
      " expect 64.32/30.65/3.73/0.56/0.00")
r1, r2, r3 = rank_probs(cr, 13)
print("SEP crown:", {NAMES[i]: round(r1[i]*100, 2) for i in range(5)}, " expect 86.40/13.59/0.01")
print("SEP 2nd  :", {NAMES[i]: round(r2[i]*100, 2) for i in range(5)}, " expect 85.46-AAPL/13.57-NVDA/0.96-GOOGL")
print("SEP 3rd  :", {NAMES[i]: round(r3[i]*100, 2) for i in range(5)}, " expect 93.13-GOOGL/5.90-MSFT/0.95-AAPL")

# ---- P(+-5pts / wk) (same seed/method as prior runs) ----
rng = np.random.default_rng(7)
NMC = 4000
zshock = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(5)
lnc0 = np.log(cr)
zq = np.linspace(-8, 8, 241)
wq = norm.pdf(zq) * (zq[1] - zq[0])
sT = sig_d * np.sqrt(72)
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
print("P(+-5/wk):", {NAMES[i]: round(cnt[i] / NMC * 100) for i in range(5)}, " expect 59/58/3/0/0")

# ---- stale-mid edges (last walked mids, Sep 1 03:59Z — labeled color) ----
stale = {'dec-NVDA': ('NVDA', 77.5), 'dec-AAPL': ('AAPL', 13.75), 'dec-GOOGL': ('GOOGL', 8.5),
         'dec-MSFT': ('MSFT', 0.75), 'dec-AMZN': ('AMZN', 0.15)}
print()
for k, (nm, mid) in stale.items():
    i = NAMES.index(nm)
    rv = dec_pub[i] / mid if mid > 0 else float('nan')
    print(f"{k}: fair {dec_pub[i]:.2f} vs stale mid {mid} -> edge {mid - dec_pub[i]:+.2f}  RV {rv:.2f}x")
print(f"sep2AAPL: fair {r2[1]*100:.2f} vs stale mid 81.5 -> edge {81.5 - r2[1]*100:+.2f}")
print(f"sep3NVDA: fair {r3[0]*100:.2f} vs stale mid 1.6 -> edge {1.6 - r3[0]*100:+.2f}")

# ---- BTC ladder color: CoinGecko live Sep 13 ~13:1xZ; Coinbase cross-check 77,207.06 ----
S_bake = 78414.25
S = 77303.56            # CoinGecko live (24h range 77,054.68-77,479.13, +0.1%/24h)
S_pm = 77389.61         # the Sep 12 PM print
S_am12 = 77278.23       # the Sep 12 AM print (~24h ago)
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S}: {(S/S_pm-1)*100:+.2f}% vs PM print {S_pm}; "
      f"{(S/S_am12-1)*100:+.2f}% vs Sep12AM {S_am12}; {(S/S_bake-1)*100:+.2f}% vs bake {S_bake}")
print(f"T = {T:.1f} d   anchor needed touch {(85000/S-1)*100:+.1f}%")
mids = {85000: 70.5, 90000: 47.0, 95000: 34.5, 100000: 23.5, 60000: 26.5, 55000: 22.5, 50000: 14.5}
for H, mid in mids.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  mid {mid:5.1f}  resid {mid-fair:+.1f}")
