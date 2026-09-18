#!/usr/bin/env python3
"""Sep 18 PM run — the Friday quad-witching close: NVIDIA breaks out, the lead clears the
Sep 11 melt-up finals (widest since the Sep 10 close); Bitcoin breaks $80k.
1. Trading-day counts after the Sep 18 close (expect T = 8/72).
2. Calibration: reproduce every Sep 18 AM published fair on the LOCKED Sep 17 finals
   (MSFT 497.75) at T = 9/73 (Dec 62.51/31.93/4.40/0.42/0.00; crown 87.80/12.20/0.00;
   seat 87.37/12.19/0.44; 3rd 98.30/1.26/0.43/0.01; P(+-5/wk) 61/59/4).
3. Fresh fairs on the Sep 18 closes. NVDA SOURCE NOTE: the history-table row served
   $222.06 (+1.24%) at ~23:10Z while the same page's quote header AND the overview
   page both served $222.27 (+1.34%) "at close 4:00 PM EDT", with the live
   after-hours series ($222.42, 7:08 PM ET) keyed off 222.27 — on a quad-witching
   close the table snapshot lags the settle (the Sep 12/15/18-AM lesson), so 222.27
   is taken as the working final, the divergence disclosed, the AM pass re-verifies.
4. Edges + depth-at-fair vs the Sep 16 01:45Z walk ladders (THREE sessions behind).
5. Joint-payoff MC (Sep crown + Dec, Apple), validated on the Sep 17 inputs first.
6. BTC ladder residuals vs the Sep 15 01:10Z walked mids (labeled color) —
   spot $81,228.07 CoinGecko live, the series' first $80k+ print.
AUTODATA: Sep 18 22:45Z cron silent (38th missed feed run); ~23:09Z poke touching
fetch/poke pushed via the extraheader path (23c95f0e), unanswered."""
import re
import numpy as np
from scipy.stats import norm

SH = {'NVDA': 24.2, 'AAPL': 14.68736, 'GOOGL': 12.17456, 'MSFT': 7.42843, 'AMZN': 10.75711}
NAMES = list(SH)
SIG_REL = 0.02
sig_d = SIG_REL / np.sqrt(2)

# ---- trading days after the Sep 18 close ----
T_SEP = int(np.busday_count('2026-09-21', '2026-10-01'))
T_DEC = int(np.busday_count('2026-09-21', '2027-01-01', holidays=['2026-11-26', '2026-12-25']))
print(f"T = {T_SEP} / {T_DEC}  (expect 8 / 72)")

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

# ---- CALIBRATION on the LOCKED Sep 17 finals (AM revision MSFT 497.75) at T = 9/73 ----
px17 = {'NVDA': 219.34, 'AAPL': 337.00, 'GOOGL': 347.33, 'MSFT': 497.75, 'AMZN': 251.19}
c17 = np.array([px17[k] * SH[k] for k in NAMES])
p1c, _, _ = rank_probs(c17, 73)
calD = p1c * 100 * 0.9925
r1c, r2c, r3c = rank_probs(c17, 9)
print("CAL Dec  :", {NAMES[i]: round(calD[i], 2) for i in range(5)}, " expect 62.51/31.93/4.40/0.42/0.00")
print("CAL crown:", {NAMES[i]: round(r1c[i]*100, 2) for i in range(5)}, " expect 87.80/12.20/0.00")
print("CAL 2nd  :", {NAMES[i]: round(r2c[i]*100, 2) for i in range(5)}, " expect 12.19-NVDA/87.37-AAPL/0.44-GOOGL")
print("CAL 3rd  :", {NAMES[i]: round(r3c[i]*100, 2) for i in range(5)}, " expect 0.01-NVDA/0.43-AAPL/98.30-GOOGL/1.26-MSFT")
assert abs(calD[0] - 62.51) < 0.02 and abs(calD[1] - 31.93) < 0.02, "Dec calibration failed"
assert abs(r1c[0]*100 - 87.80) < 0.02 and abs(r1c[1]*100 - 12.20) < 0.02, "crown calibration failed"
assert abs(r2c[1]*100 - 87.37) < 0.02 and abs(r2c[0]*100 - 12.19) < 0.02, "seat calibration failed"
assert abs(r3c[2]*100 - 98.30) < 0.02 and abs(r3c[3]*100 - 1.26) < 0.02, "3rd calibration failed"

def p5wk(cr, dec, T_dec):
    rng = np.random.default_rng(7)
    NMC = 4000
    zshock = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(5)
    lnc0 = np.log(cr)
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
        cnt += (np.abs(pr * 100 * 0.9925 - dec) >= 5)
    return {NAMES[i]: round(cnt[i]/NMC*100) for i in range(5)}
print("CAL P(+-5/wk):", p5wk(c17, calD, 73), " expect 61/59/4")

# ---- the Sep 18 closes ----
# NVDA: quote header + overview 222.27 (+1.34%), history-table row 222.06 (+1.24%)
# at ~23:10Z — quad-witching close; 222.27 taken as working final (see docstring).
px = {'NVDA': 222.27, 'AAPL': 336.13, 'GOOGL': 349.54, 'MSFT': 493.78, 'AMZN': 253.71}
chg = {'NVDA': 1.34, 'AAPL': -0.26, 'GOOGL': 0.64, 'MSFT': -0.80, 'AMZN': 1.00}
caps = {k: px[k] * SH[k] for k in NAMES}
for k in NAMES:
    d = (px[k]/px17[k]-1)*100
    assert abs(d - chg[k]) < 0.02, f"{k} change% mismatch: {d:.2f} vs page {chg[k]}"
    print(f"  {k}: {px[k]} ({d:+.2f}%)  cap ${caps[k]:.1f}B")
d_alt = (222.06/px17['NVDA']-1)*100
print(f"  [NVDA divergent table row: 222.06 = {d_alt:+.2f}% — matches the page's +1.24; cap would be ${222.06*SH['NVDA']:.1f}B]")
lead_pct = (caps['NVDA']/caps['AAPL']-1)*100; lead_b = caps['NVDA']-caps['AAPL']
cush_pct = (caps['AAPL']/caps['GOOGL']-1)*100; cush_b = caps['AAPL']-caps['GOOGL']
print(f"lead {lead_pct:.2f}% / ${lead_b:.1f}B (was 7.24%/$358.4B; Sep 11 melt-up 8.25%); cushion {cush_pct:.2f}% / ${cush_b:.1f}B (was 17.05%/$721.1B)")

cr = np.array([caps[k] for k in NAMES])
p1f, _, _ = rank_probs(cr, T_DEC)
dec = p1f * 100 * 0.9925
r1, r2, r3 = rank_probs(cr, T_SEP)
crown = r1*100; seat = r2*100; third = r3*100
print("DEC fair :", {NAMES[i]: round(dec[i], 2) for i in range(5)})
print("SEP crown:", {NAMES[i]: round(crown[i], 2) for i in range(5)})
print("SEP 2nd  :", {NAMES[i]: round(seat[i], 2) for i in range(5)})
print("SEP 3rd  :", {NAMES[i]: round(third[i], 2) for i in range(5)})
print("P(+-5/wk):", p5wk(cr, dec, T_DEC))

# ---- edges + depth-at-fair vs the Sep 16 01:45Z walk ladders (THREE sessions behind) ----
BK = {}
cur = None
for line in open('scripts/largest_books_sep16.txt'):
    line = line.rstrip('\n')
    if line.startswith('#'):
        cur = line[1:].split(' ')[0]; BK[cur] = {'B': [], 'A': []}
    elif line.startswith('B'):
        BK[cur]['B'] = [(float(a), float(b)) for a, b in re.findall(r'([\d.]+)x([\d.]+)', line)]
    elif line.startswith('A'):
        BK[cur]['A'] = [(float(a), float(b)) for a, b in re.findall(r'([\d.]+)x([\d.]+)', line)]
FAIR = {
 'dec-NVDA': dec[0], 'dec-AAPL': dec[1], 'dec-GOOGL': dec[2], 'dec-MSFT': dec[3], 'dec-AMZN': dec[4],
 'sep-crownNVDA': crown[0], 'sep-crownAAPL': crown[1],
 'sep-sep2AAPL': seat[1], 'sep-sep2NVDA': seat[0], 'sep-sep2GOOGL': seat[2],
 'sep-sep3GOOGL': third[2], 'sep-sep3MSFT': third[3], 'sep-sep3AAPL': third[1], 'sep-sep3NVDA': third[0],
}
print(f"\n{'book':16s} {'bid':>6s} {'ask':>6s} {'mid':>6s} {'fair':>6s} {'edge':>7s} {'rvMid':>5s}")
for k, f in FAIR.items():
    b = BK.get(k)
    if not b: print(f"{k:16s}  (not in walk)"); continue
    bid = b['B'][0][0]*100 if b['B'] else None
    ask = b['A'][0][0]*100 if b['A'] else None
    mid = ((bid or 0) + (ask or 0)) / 2 if (bid is not None and ask is not None) else (bid if bid is not None else ask)
    edge = mid - f
    print(f"{k:16s} {bid if bid is not None else float('nan'):6.2f} {ask if ask is not None else float('nan'):6.2f} {mid:6.2f} {f:6.2f} {edge:+7.2f} {f/mid if mid else float('nan'):5.2f}")

b = BK['dec-AAPL']
fair = dec[1]
at_fair = sum(p*q for p, q in b['A'] if p*100 <= fair)
in_band = sum(p*q for p, q in b['A'] if p*100 <= fair - 5)
print(f"\ndec-AAPL asks $ at-or-under fair {fair:.2f}: ${at_fair:,.0f}; at-or-under fair-5 ({fair-5:.2f}): ${in_band:,.0f}")
ask_t = b['A'][0][0]*100
print(f"dec-AAPL touch {ask_t:.1f}, edge {ask_t - fair:+.2f}, RV@ask {fair/ask_t:.2f}x, RV@mid {fair/((b['B'][0][0]*100+ask_t)/2):.2f}x")
print(f"dec-AAPL sigma sweep (1.5/2/2.5/3 %/day):", end=' ')
for srel in (0.015, 0.02, 0.025, 0.03):
    s_save = sig_d
    globals()['sig_d'] = srel / np.sqrt(2)
    p1s, _, _ = rank_probs(cr, T_DEC)
    print(f"{p1s[1]*100*0.9925:.1f}", end=' ')
    globals()['sig_d'] = s_save
print()
# break-even sigma for the walked dec-AAPL mid
mid_dA = (b['B'][0][0]*100 + ask_t) / 2
lo, hi = 0.004, 0.02
for _ in range(40):
    m_ = (lo + hi) / 2
    globals()['sig_d'] = m_ / np.sqrt(2)
    p1s, _, _ = rank_probs(cr, T_DEC)
    v = p1s[1]*100*0.9925
    if v > mid_dA: hi = m_
    else: lo = m_
globals()['sig_d'] = SIG_REL / np.sqrt(2)
print(f"dec-AAPL break-even sigma for the {mid_dA:.2f} mid: {(lo+hi)/2*100:.2f}%/day")
# implied drift at sigma 2%: solve ln-gap shift d s.t. fair = mid
s = sig_d * np.sqrt(T_DEC)
lg = np.log(caps['AAPL']/caps['NVDA'])
# crude 2-name proxy consistent with prior runs' quoting: Phi((lg+d)/s)*0.9925*100 = mid
d_need = norm.ppf(mid_dA/100/0.9925)*s - lg
print(f"dec-AAPL implied NVDA-over-AAPL drift at sigma 2%: {-d_need*100:+.1f}% (2-name proxy)")

cf = crown[1]
print(f"Apple crown fair {cf:.2f}; fair-5 = {cf-5:.2f}; touch 12.7 -> edge {12.7-cf:+.2f}; mid 12.6 edge {12.6-cf:+.2f}, RV {cf/12.6:.2f}x")
# crown sigma sweep
print("Apple crown sigma sweep (1.5/2/2.5/3 %/day):", end=' ')
for srel in (0.015, 0.02, 0.025, 0.03):
    globals()['sig_d'] = srel / np.sqrt(2)
    r1s, _, _ = rank_probs(cr, T_SEP)
    print(f"{r1s[1]*100:.1f}", end=' ')
globals()['sig_d'] = SIG_REL / np.sqrt(2)
print()
b3 = BK['sep-sep3MSFT']
bid3 = b3['B'][0][0]*100
mid3 = (bid3 + b3['A'][0][0]*100)/2
print(f"sep3MSFT bid {bid3:.1f} vs fair {third[3]:.2f} -> edge@bid {bid3-third[3]:+.2f}, RV {third[3]/mid3:.2f}x at mid, {third[3]/bid3:.2f}x at bid")
bn = BK['dec-NVDA']
no_fair = 100 - dec[0]
yes_notional = sum(p*q for p, q in bn['B'] if p*100 >= dec[0])
no_dollars = sum((1-p)*q for p, q in bn['B'] if p*100 >= dec[0])
print(f"dec-NVDA NO fair {no_fair:.2f}; YES-notional of bids >= fair ${yes_notional:,.0f} = NO-dollars ${no_dollars:,.0f}")
bg = BK['sep-sep3GOOGL']
gf = third[2]
g_at = sum(p*q for p, q in bg['A'] if p*100 <= gf)
g_band = sum(p*q for p, q in bg['A'] if p*100 <= gf - 5)
print(f"sep3GOOGL asks <= fair {gf:.2f}: ${g_at:,.0f}; <= fair-5: ${g_band:,.0f}; ask edge {bg['A'][0][0]*100-gf:+.2f}")
bc = BK['sep-crownAAPL']
c_at = sum(p*q for p, q in bc['A'] if p*100 <= crown[1])
print(f"crownAAPL asks <= fair {crown[1]:.2f}: ${c_at:,.0f}")
bcn = BK['sep-crownNVDA']
cn_not = sum(p*q for p, q in bcn['B'] if p*100 >= crown[0])
print(f"crownNVDA YES-notional of bids >= fair {crown[0]:.2f}: ${cn_not:,.0f}")
b2a = BK['sep-sep2AAPL']
a2_at = sum(p*q for p, q in b2a['A'] if p*100 <= seat[1])
b2n = BK['sep-sep2NVDA']
n2_at = sum(p*q for p, q in b2n['A'] if p*100 <= seat[0])
b2g = BK.get('sep-sep2GOOGL')
g2_at = sum(p*q for p, q in b2g['A'] if p*100 <= seat[2]) if b2g else float('nan')
b3a = BK.get('sep-sep3AAPL')
a3_at = sum(p*q for p, q in b3a['A'] if p*100 <= third[1]) if b3a else float('nan')
print(f"sep2AAPL asks <= fair: ${a2_at:,.0f}; sep2NVDA asks <= fair: ${n2_at:,.0f}; sep2GOOGL asks <= fair: ${g2_at:,.0f}; sep3AAPL asks <= fair: ${a3_at:,.0f}")
b3m_at = sum(p*q for p, q in b3['B'] if p*100 >= third[3])
print(f"sep3MSFT bid-$ at-or-over fair: ${b3m_at:,.0f}")

# ---- joint-payoff MC (Sep crown + Dec, Apple) — validate on Sep 17 inputs first ----
def joint_mc(c0, Ts, Td, seed=11, NMC=200000):
    rng = np.random.default_rng(seed)
    lnc = np.log(c0)[None, :] + np.zeros((NMC, 5))
    sh_s = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(Ts)
    sh_d = rng.standard_normal((NMC, 5)) * sig_d * np.sqrt(Td - Ts)
    at_s = lnc + sh_s
    at_d = at_s + sh_d
    sep_win = (at_s.argmax(axis=1) == 1)
    dec_win = (at_d.argmax(axis=1) == 1)
    both = (sep_win & dec_win).mean()
    ps, pd = sep_win.mean(), dec_win.mean()
    corr = (both - ps*pd) / np.sqrt(ps*(1-ps)*pd*(1-pd))
    return ps, pd, both, corr, (both/ps if ps else 0), ((pd - both)/(1-ps))
ps, pd_, both, corr, d_given_s, d_given_ns = joint_mc(c17, 9, 73)
print(f"\nJOINT CAL (Sep 17 inputs): P(both) {both*100:.1f}% (page 6.6), P(Dec|Sep) {d_given_s*100:.0f}% (page 54), P(Dec|~Sep) {d_given_ns*100:.0f}% (page 29), corr {corr:.2f} (page 0.18)")
ps, pd_, both, corr, d_given_s, d_given_ns = joint_mc(cr, T_SEP, T_DEC)
print(f"JOINT (Sep 18):            P(both) {both*100:.1f}%, P(Dec|Sep) {d_given_s*100:.0f}%, P(Dec|~Sep) {d_given_ns*100:.0f}%, corr {corr:.2f}")

# ---- BTC color (CoinGecko live primary; Kraken live cross — both fresh) ----
S = 81228.07        # CoinGecko live (+6.2%/24h, range 76,205.16-81,304.24)
S_kr = 80996.00     # Kraken live cross (+5.85%/24h)
S_am = 77718.58     # Sep 18 AM print (CoinGecko primary)
S_bake = 78414.25
sig = 0.0235
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
end = datetime(2027, 1, 1, 5, 0, tzinfo=timezone.utc)
T = (end - now).total_seconds() / 86400
print(f"\nBTC spot {S} (CoinGecko live; Kraken {S_kr}, {(S_kr/S-1)*100:+.2f}% apart, both live):")
print(f"  {(S/S_am-1)*100:+.2f}% vs the AM print; {(S/S_bake-1)*100:+.2f}% vs bake {S_bake}; T {T:.1f}d; needed touch {(85000/S-1)*100:+.1f}%")
mids_b = {85000: 68.0, 90000: 48.5, 95000: 34.5, 100000: 23.5, 110000: 12.0,
          60000: 27.5, 55000: 19.5, 50000: 14.0}
for H, mid in mids_b.items():
    zt = abs(np.log(H / S)) / (sig * np.sqrt(T))
    fairb = 2 * norm.cdf(-zt) * 100
    print(f"  {H/1000:.0f}k: fair {fairb:5.1f}  walk-mid {mid:5.1f}  resid {mid-fairb:+.1f}")
