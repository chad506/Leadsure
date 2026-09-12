#!/usr/bin/env python3
"""Sep 12 AM run (Saturday) — the WEEKEND VERIFICATION PASS CATCHES A TRIPLE REVISION.
Saturday pre-open pass per the Sep 5 AM precedent: re-verify the Sep 11 finals against
the history pages. THREE of five REVISED upward from what the Sep 11 PM session baked
at 23:1xZ (NVDA 218.17 -> 218.29, GOOGL 338.41 -> 338.50, MSFT 495.59 -> 495.63; AAPL
332.27 and AMZN 256.78 confirmed; quote pages cross-check all three to the cent at
'Sep 11, 2026, 4:00 PM EDT'). Calibration first: reproduce every Sep 11 PM published
fair EXACTLY from the AS-PUBLISHED closes; then re-run on the REVISED finals at the
same T=13/77. BTC ladder color at the fresh CoinGecko spot + rolled T."""
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

# ---- calibration: the Sep 11 closes AS PUBLISHED Sep 11 PM (pre-revision), T = 13/77
#      -> must reproduce every Sep 11 PM published fair EXACTLY ----
px_pub = {'NVDA': 218.17, 'AAPL': 332.27, 'GOOGL': 338.41, 'MSFT': 495.59, 'AMZN': 256.78}
cp = np.array([px_pub[k] * SH[k] for k in NAMES])
p1, _, _ = rank_probs(cp, 77)
print("CAL Dec  :", {NAMES[i]: round(p1[i] * 100 * 0.9925, 2) for i in range(5)},
      " expect 64.21/30.75/3.73/0.56/0.00")
q1, q2, q3 = rank_probs(cp, 13)
print("CAL crown:", {NAMES[i]: round(q1[i]*100, 2) for i in range(5)}, " expect 86.24/13.76/0.01")
print("CAL 2nd  :", {NAMES[i]: round(q2[i]*100, 2) for i in range(5)}, " expect 85.30-AAPL/13.74-NVDA/0.96-GOOGL")
print("CAL 3rd  :", {NAMES[i]: round(q3[i]*100, 2) for i in range(5)}, " expect 93.11-GOOGL/5.93-MSFT/0.94-AAPL")

# ---- the REVISED Sep 11 finals (history pages Sep 12 13:1xZ; quote pages cross-check) ----
px_rev = {'NVDA': 218.29, 'AAPL': 332.27, 'GOOGL': 338.50, 'MSFT': 495.63, 'AMZN': 256.78}
caps = {k: px_rev[k] * SH[k] for k in NAMES}
print("\nREVISED caps $B:", {k: round(v, 1) for k, v in caps.items()})
print(f"  lead {(caps['NVDA']/caps['AAPL']-1)*100:.2f}% / ${caps['NVDA']-caps['AAPL']:.1f}B; "
      f"AAPL cushion {(caps['AAPL']/caps['GOOGL']-1)*100:.2f}% / ${caps['AAPL']-caps['GOOGL']:.1f}B")
cr = np.array([caps[k] for k in NAMES])

# ---- fresh fairs on the revision: T = 13 (Sep) / 77 (Dec), unchanged (no new session) ----
p1f, _, _ = rank_probs(cr, 77)
dec_pub = p1f * 100 * 0.9925  # 0.75 small-leg allowance, Dec legs only
print("\nDEC fair :", {NAMES[i]: round(dec_pub[i], 2) for i in range(5)})
r1, r2, r3 = rank_probs(cr, 13)
print("SEP crown:", {NAMES[i]: round(r1[i]*100, 2) for i in range(5)})
print("SEP 2nd  :", {NAMES[i]: round(r2[i]*100, 2) for i in range(5)})
print("SEP 3rd  :", {NAMES[i]: round(r3[i]*100, 2) for i in range(5)})

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
print("P(+-5/wk):", {NAMES[i]: round(cnt[i] / NMC * 100) for i in range(5)})

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

# ---- BTC ladder color: CoinGecko live Sep 12 13:1xZ ----
S_bake = 78414.25
S = 77278.23            # CoinGecko live (+0.60%/24h; range 76,392.55-79,607.48)
S_prev = 77372.48       # the Sep 11 PM print (the last published spot)
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} vs Sep11PM {S_prev}: {(S/S_prev-1)*100:+.2f}%  vs bake {S_bake}: {(S/S_bake-1)*100:+.2f}%")
print(f"T = {T:.1f} d   anchor needed touch {(85000/S-1)*100:+.1f}%")
mids = {85000: 70.5, 90000: 47.0, 95000: 34.5, 100000: 23.5, 60000: 26.5, 55000: 22.5, 50000: 14.5}
for H, mid in mids.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  mid {mid:5.1f}  resid {mid-fair:+.1f}")
