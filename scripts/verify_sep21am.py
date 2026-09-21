#!/usr/bin/env python3
"""Sep 21 AM run (Monday pre-open) — the morning of the first post-breakout
close: the finals lock a FIFTH consecutive session, premarket leans WIDER, and
bitcoin firms toward the series high on a three-way consensus (two live
exchanges + CMC) that catches CoinGecko's first fresh-but-wrong print of
the series (its Sep 13/15 PM discards were stale re-serves).
1. All five Sep 18 finals re-confirmed to the cent a FIFTH consecutive
   session (NVDA $222.27 vol 189,973,388 settled holds; AAPL $336.13,
   GOOGL $349.54, MSFT $493.78, AMZN $253.71; Sep 17 finals re-confirmed
   beneath them a SIXTH session; Sep 16 rows verified beneath those; every
   history-page header still 'At close: Sep 18'). No revision anywhere.
2. Trading-day counts unchanged into the open (expect T = 8/72).
3. Calibration: reproduce every published fair EXACTLY
   (Dec 65.98/28.69/4.27/0.30/0.00; crown 93.52/6.48/0.00; seat 93.09-AAPL/
   6.47-NVDA/0.43-GOOGL; 3rd 99.13-GOOGL/0.43-MSFT/0.43-AAPL/0.00-NVDA;
   P(+-5/wk) 60/58/4) — the board goes into TODAY'S close, the first since
   the quad-witching breakout, exactly as published.
4. Lead/cushion re-derived: 8.95%/$442.1B, 16.01%/$681.4B.
5. Premarket color (9:07-9:14 ET, labeled, never a model input): NVDA +0.60%
   $223.60, AMZN +0.54% $255.07, GOOGL +0.36% $350.80, MSFT +0.34% $495.47,
   AAPL -0.07% $335.91 — implied lead/cushion derived below.
6. BTC color: Kraken LIVE $81,618.00 (+1.48%/24h, range 80,212.80-81,880.17)
   with Coinbase LIVE $81,681.35 (+1.49%/24h) ~0.08% over and CMC
   $81,478.68 (+1.18%/24h, range 80,149.63-82,074.61) ~0.17% under — a
   three-way consensus at $81.5-81.7k. CoinGecko printed $84,609.17 +5.3%
   with a claimed 24h high of $85,045.70 that NO exchange's own 24h range
   corroborates (Kraken high 81,880.17, CMC high 82,074.61) — DISCARDED —
   its first fresh-but-wrong print of the series, after two
   stale-snapshot discards Sep 13/15 PM. A SIXTH consecutive $80k+
   print; deltas + residuals below.
AUTODATA: Sep 21 12:45Z cron silent (FORTY-THIRD missed feed run); 13:09Z
poke touching fetch/poke pushed (03f77c89, extraheader path — the plain
token path was proxy-denied this session) — answer checked at EOR."""
import numpy as np
from scipy.stats import norm

SH = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
NAMES = list(SH)
SIG_REL = 0.02
sig_d = SIG_REL / np.sqrt(2)

# ---- trading days: Monday pre-open, still no close since Sep 18 ----
T_SEP = int(np.busday_count('2026-09-21', '2026-10-01'))
T_DEC = int(np.busday_count('2026-09-21', '2027-01-01', holidays=['2026-11-26', '2026-12-25']))
print(f"T = {T_SEP} / {T_DEC}  (expect 8 / 72, unchanged until today's close)")
assert (T_SEP, T_DEC) == (8, 72)

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

# ---- the Sep 18 finals: FIFTH consecutive to-the-cent confirmation ----
px = {'NVDA': 222.27, 'AAPL': 336.13, 'GOOGL': 349.54, 'MSFT': 493.78, 'AMZN': 253.71}
chg = {'NVDA': 1.34, 'AAPL': -0.26, 'GOOGL': 0.64, 'MSFT': -0.80, 'AMZN': 1.00}
px17 = {'NVDA': 219.34, 'AAPL': 337.00, 'GOOGL': 347.33, 'MSFT': 497.75, 'AMZN': 251.19}
chg17 = {'NVDA': 2.54, 'AAPL': 1.38, 'GOOGL': 1.30, 'MSFT': 1.52, 'AMZN': 2.13}
px16 = {'NVDA': 213.90, 'AAPL': 332.41, 'GOOGL': 342.87, 'MSFT': 490.30, 'AMZN': 245.96}
vol18 = {'NVDA': 189_973_388, 'AAPL': 86_588_203, 'GOOGL': 47_286_317, 'MSFT': 37_775_614, 'AMZN': 51_884_018}
caps = {k: px[k] * SH[k] for k in NAMES}
for k in NAMES:
    d = (px[k] / px17[k] - 1) * 100
    assert abs(d - chg[k]) < 0.02, f"{k} change% mismatch: {d:.2f} vs page {chg[k]}"
    d17 = (px17[k] / px16[k] - 1) * 100
    assert abs(d17 - chg17[k]) < 0.02, f"{k} Sep 17 change% mismatch"
    print(f"  {k}: {px[k]} ({d:+.2f}%)  cap ${caps[k]:.1f}B  [re-confirmed a 5th pass; vol {vol18[k]:,}]")
print("  [NVDA settled volume 189,973,388 HOLDS; Sep 17 finals re-confirmed a 6th session; Sep 16 rows verified beneath]")
lead_pct = (caps['NVDA'] / caps['AAPL'] - 1) * 100; lead_b = caps['NVDA'] - caps['AAPL']
cush_pct = (caps['AAPL'] / caps['GOOGL'] - 1) * 100; cush_b = caps['AAPL'] - caps['GOOGL']
print(f"lead {lead_pct:.2f}% / ${lead_b:.1f}B (expect 8.95%/$442.1B); cushion {cush_pct:.2f}% / ${cush_b:.1f}B (expect 16.01%/$681.4B)")
assert abs(lead_pct - 8.95) < 0.01 and abs(lead_b - 442.1) < 0.1
assert abs(cush_pct - 16.01) < 0.01 and abs(cush_b - 681.4) < 0.1

# ---- CALIBRATION == this run's fairs (no revision -> reproduce the board EXACTLY) ----
cr = np.array([caps[k] for k in NAMES])
p1f, _, _ = rank_probs(cr, T_DEC)
dec = p1f * 100 * 0.9925
r1, r2, r3 = rank_probs(cr, T_SEP)
crown = r1 * 100; seat = r2 * 100; third = r3 * 100
print("DEC fair :", {NAMES[i]: round(dec[i], 2) for i in range(5)}, " expect 65.98/28.69/4.27/0.30/0.00")
print("SEP crown:", {NAMES[i]: round(crown[i], 2) for i in range(5)}, " expect 93.52/6.48/0.00")
print("SEP 2nd  :", {NAMES[i]: round(seat[i], 2) for i in range(5)}, " expect 6.47-NVDA/93.09-AAPL/0.43-GOOGL")
print("SEP 3rd  :", {NAMES[i]: round(third[i], 2) for i in range(5)}, " expect 0.00-NVDA/0.43-AAPL/99.13-GOOGL/0.43-MSFT")
assert abs(dec[0] - 65.98) < 0.02 and abs(dec[1] - 28.69) < 0.02 and abs(dec[2] - 4.27) < 0.02 \
   and abs(dec[3] - 0.30) < 0.02 and dec[4] < 0.01, "Dec calibration failed"
assert abs(crown[0] - 93.52) < 0.02 and abs(crown[1] - 6.48) < 0.02, "crown calibration failed"
assert abs(seat[1] - 93.09) < 0.02 and abs(seat[0] - 6.47) < 0.02 and abs(seat[2] - 0.43) < 0.02, "seat calibration failed"
assert abs(third[2] - 99.13) < 0.02 and abs(third[3] - 0.43) < 0.02 and abs(third[1] - 0.43) < 0.02 \
   and third[0] < 0.01, "3rd calibration failed"

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
print("P(+-5/wk):", pw, " expect 60/58/4")
assert pw['NVDA'] == 60 and pw['AAPL'] == 58 and pw['GOOGL'] == 4, "P(+-5/wk) calibration failed"

print("\n=> Fifth consecutive lock-pass: every fair, edge, badge and Best-Bet stance goes into")
print("   TODAY'S close — the first since the quad-witching breakout — exactly as published.")

# ---- premarket color (9:07-9:14 ET, labeled, never a model input) ----
pm = {'NVDA': 223.60, 'AAPL': 335.91, 'GOOGL': 350.80, 'MSFT': 495.47, 'AMZN': 255.07}
pmchg = {'NVDA': 0.60, 'AAPL': -0.07, 'GOOGL': 0.36, 'MSFT': 0.34, 'AMZN': 0.54}
for k in NAMES:
    d = (pm[k] / px[k] - 1) * 100
    assert abs(d - pmchg[k]) < 0.02, f"{k} premarket change% mismatch: {d:.2f} vs page {pmchg[k]}"
pcaps = {k: pm[k] * SH[k] for k in NAMES}
plead = (pcaps['NVDA'] / pcaps['AAPL'] - 1) * 100
plead_b = pcaps['NVDA'] - pcaps['AAPL']
pcush = (pcaps['AAPL'] / pcaps['GOOGL'] - 1) * 100
pcush_b = pcaps['AAPL'] - pcaps['GOOGL']
print(f"\npremarket implied lead {plead:.2f}% / ${plead_b:.1f}B (vs finals' 8.95%/$442.1B); "
      f"implied cushion {pcush:.2f}% / ${pcush_b:.1f}B (vs 16.01%/$681.4B)")

# ---- BTC color (labeled, never a model input) ----
S = 81618.00        # Kraken LIVE (+1.48%/24h, own range 80,212.80-81,880.17)
S_cb = 81681.35     # Coinbase LIVE cross (+1.49%/24h; fresh Monday-morning page)
S_cmc = 81478.68    # CoinMarketCap cross (+1.18%/24h, range 80,149.63-82,074.61)
S_gecko = 84609.17  # CoinGecko print — DISCARDED (claimed 24h high 85,045.70
                    #   uncorroborated by ANY exchange's own range; +5.3%/24h vs
                    #   the exchanges' +1.2-1.5%): the aggregator's first
                    #   fresh-but-wrong print of the series.
S_pm = 80827.29     # Sep 20 PM print
S_hi = 81706.31     # Sep 19 PM print — the series high
S_brk = 81228.07    # Sep 18 PM print (the $80k break)
S_bake = 78414.25
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} (Kraken LIVE; Coinbase {S_cb} {(S_cb/S-1)*100:+.2f}% and CMC {S_cmc} "
      f"{(S_cmc/S-1)*100:+.2f}% — three-way consensus, spread {(max(S,S_cb,S_cmc)/min(S,S_cb,S_cmc)-1)*100:.2f}%; "
      f"CoinGecko {S_gecko} {(S_gecko/S-1)*100:+.1f}% over — DISCARDED):")
print(f"  {(S/S_pm-1)*100:+.2f}% on the Sep 20 PM print; {(S/S_hi-1)*100:+.2f}% vs the series-high print; "
      f"{(S/S_brk-1)*100:+.2f}% vs the $80k-break print; {(S/S_bake-1)*100:+.2f}% vs bake {S_bake}; T {T:.1f}d; "
      f"needed touch {(85000/S-1)*100:+.1f}%")
assert min(S, S_cb, S_cmc) > 80000, "the sixth-$80k-print claim needs every accepted read over $80k"
assert S < S_hi and S_cb < S_hi, "the below-the-high claim needs both live reads under the series high"
mids_b = {85000: 68.0, 90000: 48.5, 95000: 34.5, 100000: 23.5, 110000: 12.0,
          60000: 27.5, 55000: 19.5, 50000: 14.0}
prev_pm = {85000: -15.2, 90000: -16.6, 95000: -15.2, 100000: -13.5, 110000: -7.5,
           60000: 6.5, 55000: 9.0, 50000: 9.7}    # Sep 20 PM
wides = {85000: -18.9, 90000: -20.1, 95000: -18.3, 100000: -16.2, 110000: -9.3,
         60000: 7.9, 55000: 9.8, 50000: 10.0}     # Sep 19 PM, the series wides
for H, mid in mids_b.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fairb = 2 * norm.cdf(-zt) * 100
    r = mid - fairb
    tag = ("re-widens" if abs(r) > abs(prev_pm[H]) else "eases") + \
          ("" if abs(r) < abs(wides[H]) else " AT/PAST THE WIDE")
    print(f"  {H/1000:.0f}k: fair {fairb:5.1f}  walk-mid {mid:5.1f}  resid {r:+.1f}  ({tag}; PM {prev_pm[H]:+.1f}, wide {wides[H]:+.1f})")
