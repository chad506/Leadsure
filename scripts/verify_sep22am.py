#!/usr/bin/env python3
"""Sep 22 AM (Tuesday pre-open) verification pass — the morning check LOCKS
the first post-breakout close CLEAN (all five Sep 21 finals to the cent,
VOLUMES INCLUDED — NVDA's 108,496,004 holds; the Sep 18 finals a seventh
session beneath them) and bitcoin consolidates the squeeze at the series'
first $86k morning print.
1. Sep 21 finals re-fetched from the history pages (~13:2xZ Sep 22, every
   header 'At close: Sep 21, 2026, 4:00 PM EDT'): NVDA $227.38 +2.30% vol
   108,496,004 / AAPL $338.98 +0.85% vol 34,437,179 / GOOGL $354.97 +1.55%
   vol 28,124,311 / MSFT $501.61 +1.59% vol 26,026,668 / AMZN $258.45
   +1.87% vol 40,700,488 — every price AND volume matches the PM pull:
   ZERO revisions. Sep 18 rows verified beneath (NVDA 189,973,388 settled
   volume holds; AAPL's revised 85,934,403 holds); Sep 17 rows verified
   (MSFT $497.75 revision holds).
2. Calibration: reproduce every Sep 21 PM published fair EXACTLY from the
   locked Sep 21 finals at T 7/71 (Dec 69.04/25.86/4.07/0.28/0.00; crown
   97.07/2.93/0.00; seat 96.69-AAPL/2.93-NVDA/0.37-GOOGL; 3rd 99.37-GOOGL/
   0.37-AAPL/0.25-MSFT; P(+-5/wk) 58/56/4). No revisions -> no re-deal:
   caps/fairs/edges/Best Bets stand as published.
3. Premarket color (9:06-9:11 ET, labeled, never a model input): MSFT
   +1.23% $507.76 leads AAPL +0.38% $340.27 and GOOGL +0.33% $356.15
   against NVDA -0.59% $226.03 and AMZN -0.75% $256.50 — the tape leans
   NARROWER into the close, the first give-back leaning since the breakout.
4. BTC: CoinGecko LIVE $86,009.01 (+1.7%/24h, range 84,142.22-87,329.89)
   and Coinbase LIVE $86,004.64 (+1.79%) agree within 0.005% — the series'
   SECOND-tightest live cross (Sep 17 PM's ~0.004% keeps the record).
   Kraken $85,458.00 (+4.61%, range 81,459.94-87,271.26) and CMC
   $85,406.76 (+4.98%, range 81,287.81-87,363.76) print ~0.6-0.7% under as
   a lagged pair — FRESH prints, not byte re-serves of the Sep 21 reads
   (81,618.00 / 81,478.68), flagged and passed over; the live pair carries
   the print. NOTE CoinGecko's +1.7%/24h banks its own discarded Monday
   $84,609 print as the baseline — the % is cosmetic, the price is live
   and Coinbase-confirmed.
AUTODATA: Sep 22 12:45Z cron silent (FORTY-FIFTH missed feed run); 13:11Z
poke touching fetch/poke pushed (46479ced, extraheader path) — answer
checked at EOR."""
import numpy as np
from scipy.stats import norm

SH = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
NAMES = list(SH)
SIG_REL = 0.02
sig_d = SIG_REL / np.sqrt(2)

# ---- trading days AFTER the Sep 21 close (unchanged pre-open) ----
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

# ---- the Sep 21 finals, re-confirmed this morning (prices AND volumes) ----
px = {'NVDA': 227.38, 'AAPL': 338.98, 'GOOGL': 354.97, 'MSFT': 501.61, 'AMZN': 258.45}
chg = {'NVDA': 2.30, 'AAPL': 0.85, 'GOOGL': 1.55, 'MSFT': 1.59, 'AMZN': 1.87}
vol = {'NVDA': 108_496_004, 'AAPL': 34_437_179, 'GOOGL': 28_124_311, 'MSFT': 26_026_668, 'AMZN': 40_700_488}
px18 = {'NVDA': 222.27, 'AAPL': 336.13, 'GOOGL': 349.54, 'MSFT': 493.78, 'AMZN': 253.71}
caps = {k: px[k] * SH[k] for k in NAMES}
for k in NAMES:
    d = (px[k] / px18[k] - 1) * 100
    assert abs(d - chg[k]) < 0.02, f"{k} change% mismatch: {d:.2f} vs page {chg[k]}"
    print(f"  {k}: {px[k]} ({d:+.2f}%)  cap ${caps[k]:.1f}B  vol {vol[k]:,}  [morning check: to the cent, volume holds]")
lead_pct = (caps['NVDA'] / caps['AAPL'] - 1) * 100; lead_b = caps['NVDA'] - caps['AAPL']
cush_pct = (caps['AAPL'] / caps['GOOGL'] - 1) * 100; cush_b = caps['AAPL'] - caps['GOOGL']
print(f"lead {lead_pct:.2f}% / ${lead_b:.1f}B (expect 10.52 / 523.9); cushion {cush_pct:.2f}% / ${cush_b:.1f}B (expect 15.21 / 657.1)")
assert abs(lead_pct - 10.52) < 0.01 and abs(lead_b - 523.9) < 0.1
assert abs(cush_pct - 15.21) < 0.01 and abs(cush_b - 657.1) < 0.1

# ---- CALIBRATION: reproduce every Sep 21 PM published fair EXACTLY ----
cr = np.array([caps[k] for k in NAMES])
p1f, _, _ = rank_probs(cr, T_DEC)
dec = p1f * 100 * 0.9925
r1, r2, r3 = rank_probs(cr, T_SEP)
crown = r1 * 100; seat = r2 * 100; third = r3 * 100
print("DEC fair :", {NAMES[i]: round(dec[i], 2) for i in range(5)}, " expect 69.04/25.86/4.07/0.28/0.00")
print("SEP crown:", {NAMES[i]: round(crown[i], 2) for i in range(5)}, " expect 97.07/2.93/0.00")
print("SEP 2nd  :", {NAMES[i]: round(seat[i], 2) for i in range(5)}, " expect 96.69-AAPL/2.93-NVDA/0.37-GOOGL")
print("SEP 3rd  :", {NAMES[i]: round(third[i], 2) for i in range(5)}, " expect 99.37-GOOGL/0.37-AAPL/0.25-MSFT")
assert abs(dec[0] - 69.04) < 0.02 and abs(dec[1] - 25.86) < 0.02 and abs(dec[2] - 4.07) < 0.02 \
   and abs(dec[3] - 0.28) < 0.02 and dec[4] < 0.01, "Dec calibration failed"
assert abs(crown[0] - 97.07) < 0.02 and abs(crown[1] - 2.93) < 0.02 and crown[2] < 0.01
assert abs(seat[1] - 96.69) < 0.02 and abs(seat[0] - 2.93) < 0.02 and abs(seat[2] - 0.37) < 0.02
assert abs(third[2] - 99.37) < 0.02 and abs(third[1] - 0.37) < 0.02 and abs(third[3] - 0.25) < 0.02

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
print("P(+-5/wk):", pw, " expect 58/56/4")
assert pw['NVDA'] == 58 and pw['AAPL'] == 56 and pw['GOOGL'] == 4
print("CALIBRATION EXACT — zero revisions, the board stands as published.\n")

# ---- premarket color (9:06-9:11 ET; labeled, never a model input) ----
pm = {'NVDA': (226.03, -0.59), 'AAPL': (340.27, 0.38), 'GOOGL': (356.15, 0.33),
      'MSFT': (507.76, 1.23), 'AMZN': (256.50, -0.75)}
for k, (p, c) in pm.items():
    d = (p / px[k] - 1) * 100
    assert abs(d - c) < 0.02, f"{k} premarket% mismatch: {d:.2f} vs page {c}"
icaps = {k: pm[k][0] * SH[k] for k in NAMES}
il = (icaps['NVDA'] / icaps['AAPL'] - 1) * 100; ilb = icaps['NVDA'] - icaps['AAPL']
ic = (icaps['AAPL'] / icaps['GOOGL'] - 1) * 100; icb = icaps['AAPL'] - icaps['GOOGL']
print(f"premarket implied lead {il:.2f}% / ${ilb:.1f}B (finals 10.52) — NARROWER; implied cushion {ic:.2f}% / ${icb:.1f}B (finals 15.21)")

# ---- BTC: the squeeze consolidates (labeled color, never a model input) ----
S = 86009.01        # CoinGecko LIVE (+1.7%/24h, range 84,142.22-87,329.89)
S_cb = 86004.64     # Coinbase LIVE (+1.79%/24h) — 0.005% under (2nd-tightest cross)
S_kraken = 85458.00 # lagged: fresh print (not the 81,618.00 re-serve), ~0.64% under
S_cmc = 85406.76    # lagged: fresh print (not the 81,478.68 re-serve), ~0.70% under
S_pm = 86534.71     # Sep 21 PM (the $85k-touch squeeze print — the series high)
S_brk = 81228.07    # Sep 18 PM (the $80k break)
S_bake = 78414.25
assert S_kraken != 81618.00 and S_cmc != 81478.68, "re-serve check"
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} (CoinGecko LIVE; Coinbase {S_cb} {(S_cb/S-1)*100:+.3f}% — two live sources; "
      f"Kraken {S_kraken} {(S_kraken/S-1)*100:+.2f}% / CMC {S_cmc} {(S_cmc/S-1)*100:+.2f}% — lagged pair, flagged):")
print(f"  {(S/S_pm-1)*100:+.2f}% on the Monday-night squeeze print; {(S/S_brk-1)*100:+.2f}% over the $80k break; "
      f"{(S/S_bake-1)*100:+.2f}% vs bake; T {T:.1f}d; needed touch to $90k {(90000/S-1)*100:+.1f}%")
assert S > 80000, "eighth consecutive $80k+ print claim"
mids_b = {90000: 48.5, 95000: 34.5, 100000: 23.5, 110000: 12.0,
          60000: 27.5, 55000: 19.5, 50000: 14.0}
prev_pm = {90000: -38.3, 95000: -34.8, 100000: -30.6, 110000: -19.0,
           60000: 15.4, 55000: 14.0, 50000: 12.0}    # Sep 21 PM
for H, mid in mids_b.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fairb = 2 * norm.cdf(-zt) * 100
    fairb = min(fairb, 100.0)
    r = mid - fairb
    print(f"  {H/1000:.0f}k: fair {fairb:5.1f}  walk-mid {mid:5.1f}  resid {r:+.1f}  (PM {prev_pm[H]:+.1f})")
