#!/usr/bin/env python3
"""Sep 15 PM run — TWO CLOSES AT ONCE, AGAIN (the Sep 14 PM and Sep 15 AM scheduled
sessions never ran: no commit, no poke — the outage's second double gap).
This run ingests the Sep 14 close (the first post-melt-up close: NVDA −3.36%,
GOOGL +3.22%) AND the Sep 15 close (broad red: AAPL −0.52%, GOOGL −1.26%,
MSFT −1.68%, AMZN −2.02%, NVDA +0.57% alone green).
ALL FIVE Sep 11 finals re-spot-checked beneath them (SIXTH consecutive session,
every one unchanged). Calibration first: reproduce every Sep 12 published fair
EXACTLY from the finals at T=13/77 before any new number is trusted.
NEW this run: the odds column re-marks to the Sep 15 01:10Z interactive walk
(scripts/leaderboard_books_sep15.csv, 226 CLOB books through the reader's Chrome)
— the first fresh equity mids on the Analysis tab since Sep 1 03:59Z."""
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

# ---- CALIBRATION on the Sep 11 finals (re-confirmed a SIXTH session tonight) ----
px_fin = {'NVDA': 218.29, 'AAPL': 332.27, 'GOOGL': 338.50, 'MSFT': 495.63, 'AMZN': 256.78}
cf = np.array([px_fin[k] * SH[k] for k in NAMES])
p1c, _, _ = rank_probs(cf, 77)
print("CAL Dec  :", {NAMES[i]: round(p1c[i]*100*0.9925, 2) for i in range(5)}, " expect 64.32/30.65/3.73/0.56/0.00")
r1c, r2c, r3c = rank_probs(cf, 13)
print("CAL crown:", {NAMES[i]: round(r1c[i]*100, 2) for i in range(5)}, " expect 86.40/13.59/0.01")
print("CAL 2nd  :", {NAMES[i]: round(r2c[i]*100, 2) for i in range(5)}, " expect 13.57-NVDA/85.46-AAPL/0.96-GOOGL")
print("CAL 3rd  :", {NAMES[i]: round(r3c[i]*100, 2) for i in range(5)}, " expect 0.02-NVDA/0.95-AAPL/93.13-GOOGL/5.90-MSFT")

# ---- the TWO new closes (stockanalysis.com history pages, fetched Sep 15 ~23:2xZ) ----
px_sep14 = {'NVDA': 210.96, 'AAPL': 333.08, 'GOOGL': 349.39, 'MSFT': 505.41, 'AMZN': 253.54}
px = {'NVDA': 212.17, 'AAPL': 331.34, 'GOOGL': 344.98, 'MSFT': 496.91, 'AMZN': 248.42}
# cross-check the printed day-changes against the prior close
for k in NAMES:
    d14 = (px_sep14[k]/px_fin[k]-1)*100
    d15 = (px[k]/px_sep14[k]-1)*100
    print(f"  {k}: Sep14 {px_sep14[k]} ({d14:+.2f}%)  Sep15 {px[k]} ({d15:+.2f}%)")
c14 = {k: px_sep14[k]*SH[k] for k in NAMES}
caps = {k: px[k]*SH[k] for k in NAMES}
print("Sep14 caps $B:", {k: round(v,1) for k,v in c14.items()},
      f"  lead {(c14['NVDA']/c14['AAPL']-1)*100:.2f}% / ${c14['NVDA']-c14['AAPL']:.1f}B")
print("Sep15 caps $B:", {k: round(v,1) for k,v in caps.items()})
print(f"  lead {(caps['NVDA']/caps['AAPL']-1)*100:.2f}% / ${caps['NVDA']-caps['AAPL']:.1f}B; "
      f"AAPL cushion {(caps['AAPL']/caps['GOOGL']-1)*100:.2f}% / ${caps['AAPL']-caps['GOOGL']:.1f}B")
cr = np.array([caps[k] for k in NAMES])

# ---- fresh fairs: T = 11 trading days to Sep 30, 75 to Dec 31 (after the Sep 15 close) ----
T_SEP, T_DEC = 11, 75
p1f, _, _ = rank_probs(cr, T_DEC)
dec_pub = p1f * 100 * 0.9925   # 0.75 small-leg allowance, Dec legs only
print("DEC fair :", {NAMES[i]: round(dec_pub[i], 2) for i in range(5)})
r1, r2, r3 = rank_probs(cr, T_SEP)
print("SEP crown:", {NAMES[i]: round(r1[i]*100, 2) for i in range(5)})
print("SEP 2nd  :", {NAMES[i]: round(r2[i]*100, 2) for i in range(5)})
print("SEP 3rd  :", {NAMES[i]: round(r3[i]*100, 2) for i in range(5)})

# ---- P(+-5pts / wk), same seed/method as prior runs (5-day shock, T-5 re-price) ----
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
print("P(+-5/wk):", {NAMES[i]: round(cnt[i] / NMC * 100) for i in range(5)})

# ---- edges vs the Sep 15 01:10Z WALKED mids (leaderboard_books_sep15.csv) ----
# bid/ask from the CSV: dec-NVDA 68/69, dec-AAPL 23/23.8, dec-GOOGL 7/8,
# dec-MSFT 0.5/0.6, dec-AMZN 0.1/0.2, sep-sep3NVDA bidless/0.1
mids = {'dec-NVDA': ('NVDA', 68.5), 'dec-AAPL': ('AAPL', 23.4), 'dec-GOOGL': ('GOOGL', 7.5),
        'dec-MSFT': ('MSFT', 0.55), 'dec-AMZN': ('AMZN', 0.15)}
print()
for k, (nm, mid) in mids.items():
    i = NAMES.index(nm)
    rv = dec_pub[i] / mid if mid > 0 else float('nan')
    print(f"{k}: fair {dec_pub[i]:.2f} vs Sep15-walk mid {mid} -> edge {mid - dec_pub[i]:+.2f}  RV {rv:.2f}x")
i = NAMES.index('NVDA')
print(f"sep3NVDA: fair {r3[i]*100:.2f} vs walk mid 0.05 (bidless, ask 0.1) -> edge {0.05 - r3[i]*100:+.2f}")
print(f"sep2AAPL: fair {r2[1]*100:.2f} vs STALE Sep 1 mid 81.5 -> edge {81.5 - r2[1]*100:+.2f} (book NOT in the Sep 15 walk)")
print(f"crown NVDA: fair {r1[0]*100:.2f} (crown book NOT in the Sep 15 walk; Apple crown leg traded 5.7-21.7c Sep 10-14 per activity)")
print(f"AAPL crown leg fair: {r1[1]*100:.2f}")

# ---- Sep 14 close fairs (color only — the close this run also ingests) ----
cr14 = np.array([c14[k] for k in NAMES])
p1x, _, _ = rank_probs(cr14, 76)
r1x, r2x, _ = rank_probs(cr14, 12)
print("\nSep14-close Dec fairs (color):", {NAMES[i]: round(p1x[i]*100*0.9925, 2) for i in range(5)})
print(f"Sep14-close crown NVDA {r1x[0]*100:.2f} / AAPL {r1x[1]*100:.2f}; seat AAPL {r2x[1]*100:.2f}")

# ---- BTC color: Coinbase primary, CMC cross; CoinGecko discarded (see run notes) ----
S_bake = 78414.25
S = 77000.77          # Coinbase live (-0.94%/24h)
S_cmc = 77389.10      # CoinMarketCap cross-check (+0.25%/24h)
S_am = 77666.24       # Sep 14 AM print (CoinGecko)
S_walk = 77794.00     # Sep 15 01:10Z interactive walk spot
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} (Coinbase; CMC {S_cmc}, {(S_cmc/S-1)*100:+.2f}% apart; CoinGecko 75,643 DISCARDED): "
      f"{(S/S_am-1)*100:+.2f}% vs Sep14AM print; {(S/S_walk-1)*100:+.2f}% vs the 01:10Z walk; {(S/S_bake-1)*100:+.2f}% vs bake {S_bake}")
print(f"T = {T:.1f} d   anchor needed touch {(85000/S-1)*100:+.1f}%")
# residuals vs the Sep 15 01:10Z WALKED mids (first fresh-mid BTC color of the outage)
mids_b = {85000: 68.0, 90000: 48.5, 95000: 34.5, 100000: 23.5, 110000: 12.0,
          60000: 27.5, 55000: 19.5, 50000: 14.0}
for H, mid in mids_b.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fair = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fair:5.1f}  walk-mid {mid:5.1f}  resid {mid-fair:+.1f}")
