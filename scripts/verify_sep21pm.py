#!/usr/bin/env python3
"""Sep 21 PM run — THE FIRST POST-BREAKOUT CLOSE LANDS: an all-green Monday
stretches the lead past 10% for the first time since Sep 10, and bitcoin
TOUCHES THE $85K RUNG on a Monday-afternoon squeeze to an 8-month high.
1. Sep 21 finals (history pages, ~23:1xZ): NVDA $227.38 +2.30% (vol
   108,496,004), AAPL $338.98 +0.85%, GOOGL $354.97 +1.55%, MSFT $501.61
   +1.59%, AMZN $258.45 +1.87% — every header 'At close: Sep 21, 2026'.
   Sep 18 finals re-confirmed to the cent beneath them a SIXTH session
   (NVDA $222.27 on 189,973,388 shares — the volume holds; ONE revision
   caught: AAPL's Sep 18 VOLUME prints 85,934,403 vs the 86,588,203 the
   Sep 19 AM run recorded — close untouched, model unaffected).
2. Calibration FIRST: reproduce every published fair from the locked Sep 18
   inputs at T 8/72 (Dec 65.98/28.69/4.27/0.30/0.00; crown 93.52/6.48/0.00;
   seat 93.09/6.47/0.43; 3rd 99.13/0.43/0.43/0.00; P(+-5/wk) 60/58/4)
   before trusting a new number.
3. Fresh fairs on the Sep 21 finals at T = 7 / 71.
4. BTC: Kraken AND CMC both re-served the AM snapshot to the cent
   (81,618.00/+1.48% and 81,478.68/+1.18%, same ranges) — BOTH DISCARDED
   as snapshot-stale. Coinbase LIVE $86,267.46 +6.53% and CoinGecko LIVE
   $86,534.71 +6.6% (range 80,907.13-87,329.89) agree within 0.31%, and
   the wire corroborates: 'surges past $85,000, 8-month high' (Yahoo/
   The National/Cointelegraph), 'tops $86,000' (CNBC), 'hits $87,000'
   (CoinDesk live). THE $85K RUNG TOUCHED TODAY — the ladder's first
   up-rung resolution event of the series; residuals below are color for
   the SURVIVING rungs only.
AUTODATA: Sep 21 22:45Z cron silent (FORTY-FOURTH missed feed run); 23:1xZ
poke touching fetch/poke pushed (e1091735, extraheader path — the plain
token path proxy-denied again) — answer checked at EOR."""
import numpy as np
from scipy.stats import norm

SH = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
NAMES = list(SH)
SIG_REL = 0.02
sig_d = SIG_REL / np.sqrt(2)

# ---- trading days AFTER the Sep 21 close ----
T_SEP = int(np.busday_count('2026-09-22', '2026-10-01'))
T_DEC = int(np.busday_count('2026-09-22', '2027-01-01', holidays=['2026-11-26', '2026-12-25']))
print(f"T = {T_SEP} / {T_DEC}  (expect 7 / 71)")
assert (T_SEP, T_DEC) == (7, 71)

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

# ---- CALIBRATION on the locked Sep 18 inputs at T 8/72 ----
px18 = {'NVDA': 222.27, 'AAPL': 336.13, 'GOOGL': 349.54, 'MSFT': 493.78, 'AMZN': 253.71}
c18 = np.array([px18[k] * SH[k] for k in NAMES])
p1c, _, _ = rank_probs(c18, 72)
decc = p1c * 100 * 0.9925
r1c, r2c, r3c = rank_probs(c18, 8)
print("CAL Dec  :", {NAMES[i]: round(decc[i], 2) for i in range(5)}, " expect 65.98/28.69/4.27/0.30/0.00")
print("CAL crown:", {NAMES[i]: round(r1c[i]*100, 2) for i in range(5)}, " expect 93.52/6.48/0.00")
print("CAL seat :", {NAMES[i]: round(r2c[i]*100, 2) for i in range(5)}, " expect 6.47-NVDA/93.09-AAPL/0.43-GOOGL")
print("CAL 3rd  :", {NAMES[i]: round(r3c[i]*100, 2) for i in range(5)}, " expect 99.13-GOOGL/0.43-MSFT/0.43-AAPL")
assert abs(decc[0] - 65.98) < 0.02 and abs(decc[1] - 28.69) < 0.02 and abs(decc[2] - 4.27) < 0.02 \
   and abs(decc[3] - 0.30) < 0.02 and decc[4] < 0.01, "Dec calibration failed"
assert abs(r1c[0]*100 - 93.52) < 0.02 and abs(r1c[1]*100 - 6.48) < 0.02, "crown calibration failed"
assert abs(r2c[1]*100 - 93.09) < 0.02 and abs(r2c[0]*100 - 6.47) < 0.02 and abs(r2c[2]*100 - 0.43) < 0.02
assert abs(r3c[2]*100 - 99.13) < 0.02 and abs(r3c[3]*100 - 0.43) < 0.02 and abs(r3c[1]*100 - 0.43) < 0.02

# ---- the Sep 21 finals ----
px = {'NVDA': 227.38, 'AAPL': 338.98, 'GOOGL': 354.97, 'MSFT': 501.61, 'AMZN': 258.45}
chg = {'NVDA': 2.30, 'AAPL': 0.85, 'GOOGL': 1.55, 'MSFT': 1.59, 'AMZN': 1.87}
vol = {'NVDA': 108_496_004, 'AAPL': 34_437_179, 'GOOGL': 28_124_311, 'MSFT': 26_026_668, 'AMZN': 40_700_488}
caps = {k: px[k] * SH[k] for k in NAMES}
for k in NAMES:
    d = (px[k] / px18[k] - 1) * 100
    assert abs(d - chg[k]) < 0.02, f"{k} change% mismatch: {d:.2f} vs page {chg[k]}"
    print(f"  {k}: {px[k]} ({d:+.2f}%)  cap ${caps[k]:.1f}B  vol {vol[k]:,}")
lead_pct = (caps['NVDA'] / caps['AAPL'] - 1) * 100; lead_b = caps['NVDA'] - caps['AAPL']
cush_pct = (caps['AAPL'] / caps['GOOGL'] - 1) * 100; cush_b = caps['AAPL'] - caps['GOOGL']
print(f"lead {lead_pct:.2f}% / ${lead_b:.1f}B; cushion {cush_pct:.2f}% / ${cush_b:.1f}B")

# ---- fresh fairs at T = 7 / 71 ----
cr = np.array([caps[k] for k in NAMES])
p1f, _, _ = rank_probs(cr, T_DEC)
dec = p1f * 100 * 0.9925
r1, r2, r3 = rank_probs(cr, T_SEP)
crown = r1 * 100; seat = r2 * 100; third = r3 * 100
print("DEC fair :", {NAMES[i]: round(dec[i], 2) for i in range(5)})
print("SEP crown:", {NAMES[i]: round(crown[i], 2) for i in range(5)})
print("SEP 2nd  :", {NAMES[i]: round(seat[i], 2) for i in range(5)})
print("SEP 3rd  :", {NAMES[i]: round(third[i], 2) for i in range(5)})

def p5wk(cr_, dec_, T_dec):
    rng = np.random.default_rng(7)
    NMC = 4000
    zshock = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(5)
    lnc0 = np.log(cr_)
    zq = np.linspace(-8, 8, 241); wq = norm.pdf(zq) * (zq[1] - zq[0])
    sT = sig_d * np.sqrt(T_dec - 5)
    cnt = np.zeros(5)
    for m in range(NMC):
        lc = lnc0 + zshock[m]
        pr = np.zeros(5)
        for i in range(5):
            others = [j for j in range(5) if j != i]
            F = np.array([norm.cdf((lc[i] - lc[j]) / sT + zq) for j in others])
            pr[i] = (wq * F.prod(axis=0)).sum()
        cnt += (np.abs(pr * 100 * 0.9925 - dec_) >= 5)
    return {NAMES[i]: round(cnt[i] / NMC * 100) for i in range(5)}
pw = p5wk(cr, dec, T_DEC)
print("P(+-5/wk):", pw)

# ---- BTC: the $85k touch + surviving-rung color (labeled, never a model input) ----
S = 86534.71        # CoinGecko LIVE (+6.6%/24h, range 80,907.13-87,329.89)
S_cb = 86267.46     # Coinbase LIVE (+6.53%/24h) — 0.31% under
S_kraken = 81618.00 # DISCARDED: byte-identical re-serve of the 13:0xZ AM print
S_cmc = 81478.68    # DISCARDED: byte-identical re-serve of the 13:0xZ AM print
S_am = 81618.00     # the AM print (Kraken, then-live)
S_hi_prev = 81706.31  # Sep 19 PM — the OLD series high
S_brk = 81228.07    # Sep 18 PM (the $80k break)
S_bake = 78414.25
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} (CoinGecko LIVE; Coinbase {S_cb} {(S_cb/S-1)*100:+.2f}% — two live sources, "
      f"0.31% apart; Kraken AND CMC re-served the AM prints to the cent — both DISCARDED):")
print(f"  {(S/S_am-1)*100:+.2f}% on the AM print; {(S/S_hi_prev-1)*100:+.2f}% OVER the old series high; "
      f"{(S/S_brk-1)*100:+.2f}% over the $80k-break print; {(S/S_bake-1)*100:+.2f}% vs bake; T {T:.1f}d")
assert S > 85000 and S_cb > 85000, "the touch claim needs both live reads over $85k"
assert S > S_hi_prev and S_cb > S_hi_prev, "the new-series-high claim needs both live reads over the old high"
print("  $85K RUNG: TOUCHED (day high 87,329.89 CoinGecko; wire: 'past $85,000' Yahoo/National/CT, "
      "'tops $86,000' CNBC, 'hits $87,000' CoinDesk) — resolution event, no longer a residual line")
mids_b = {90000: 48.5, 95000: 34.5, 100000: 23.5, 110000: 12.0,
          60000: 27.5, 55000: 19.5, 50000: 14.0}
prev_am = {90000: -19.5, 95000: -17.7, 100000: -15.6, 110000: -8.8,
           60000: 8.1, 55000: 9.9, 50000: 10.1}    # Sep 21 AM (85k was -18.4)
for H, mid in mids_b.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fairb = 2 * norm.cdf(-zt) * 100
    fairb = min(fairb, 100.0)
    r = mid - fairb
    print(f"  {H/1000:.0f}k: fair {fairb:5.1f}  walk-mid {mid:5.1f}  resid {r:+.1f}  (AM {prev_am[H]:+.1f})")
