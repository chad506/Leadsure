#!/usr/bin/env python3
"""Brent-130-by-Oct-1 conditional model. Sep 10 2026 close basis.
Bootstraps Hyperliquid xyz:BRENTOIL daily (UTC calendar day) tuples (log return, up-overshoot, down-overshoot)
over the 20 calendar days Sep 11..Sep 30, conditions on the ICE Brent front month (Nov'26, 109.29 settle)
touching >= 130 on a business day, then pushes the conditioned Brent path through measured betas.
Outputs model_oil.json.  Usage: model_oil.py [N] [volscale] [kappa] [beta10] [betaspx] [tag]
"""
import sys, json, math, numpy as np
N      = int(sys.argv[1]) if len(sys.argv) > 1 else 1_500_000
VOLSC  = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
KAPPA  = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
B10    = float(sys.argv[4]) if len(sys.argv) > 4 else 0.60    # bp per 1% Brent (same day)
BSPX   = float(sys.argv[5]) if len(sys.argv) > 5 else -0.151
TAG    = sys.argv[6] if len(sys.argv) > 6 else 'base'
QSP    = float(sys.argv[7]) if len(sys.argv) > 7 else 109.29 - 103.93   # Brent Nov − WTI Oct: the front-vs-front (quality) spread, 5.36 on Sep 10
CSP    = 103.93 - 99.51   # WTI Oct − Nov calendar spread, 4.42
rng = np.random.default_rng(20260910)

# ---------- data ----------
raw = open('/tmp/oil/brent_hl.txt').read().strip().split(',')
d = [(x.split(':')[0], float(x.split(':')[1]), float(x.split(':')[2]), float(x.split(':')[3])) for x in raw]
dates = [x[0] for x in d]; C = np.array([x[1] for x in d]); H = np.array([x[2] for x in d]); L = np.array([x[3] for x in d])
r = np.diff(np.log(C))                                # 190 daily log returns
upo = np.log(H[1:] / np.maximum(C[:-1], C[1:]))       # overshoot of the day's high above max(prev close, close)
dno = np.log(np.minimum(C[:-1], C[1:]) / L[1:])       # undershoot below min(prev, close)
r = r - r.mean()                                      # demean (driftless futures)
sd_all = r.std(); sd_60 = r[-60:].std(); sd_30 = r[-30:].std()
TUP = np.stack([r * VOLSC, upo * VOLSC, dno * VOLSC], 1)

# ---------- calendar ----------
# Sep 11 (Fri) .. Sep 30 (Wed): 20 calendar days; business flags; CL active month: Oct through Sep 17, Nov from Sep 18
cal = list(range(11, 31))
biz = np.array([not (dd in (12, 13, 19, 20, 26, 27)) for dd in cal])
post_roll = np.array([dd >= 18 for dd in cal])
nB = int(biz.sum())  # 14 prints/sessions

B0 = 109.29; TARGET = 130.0
SPREAD_PRE = QSP                # Brent Nov - CL Oct (Sep 10 settles) = 5.36: quality spread, held fixed (the perp Brent-WTI spread sat 4.5-4.9 while Brent rose 17% in Aug-Sep)
SPREAD_POST = QSP + CSP         # Brent Nov - CL Nov = 9.78: quality + the Oct-Nov calendar spread; the calendar part scales with (Brent/109.29)^KAPPA

# ---------- simulate Brent ----------
idx = rng.integers(0, len(TUP), size=(N, 20))
R = TUP[idx, 0]; UO = TUP[idx, 1]; DO = TUP[idx, 2]
logC = np.log(B0) + np.cumsum(R, 1)
Cp = np.concatenate([np.full((N, 1), np.log(B0)), logC[:, :-1]], 1)
logH = np.maximum(Cp, logC) + UO
logL = np.minimum(Cp, logC) - DO
# business-day session high: fold the preceding weekend days into Monday's session
sessH = logH.copy(); sessL = logL.copy()
for j, dd in enumerate(cal):
    if dd in (14, 21, 28):
        sessH[:, j] = np.max(logH[:, j-2:j+1], 1); sessL[:, j] = np.min(logL[:, j-2:j+1], 1)
bizH = np.where(biz[None, :], sessH, -np.inf); bizL = np.where(biz[None, :], sessL, np.inf)
touch = (bizH.max(1) >= math.log(TARGET))
first_touch_j = np.argmax(bizH >= math.log(TARGET), 1)
close_ge = np.exp(logC[:, -1]) >= TARGET
p_touch = touch.mean(); p_close = close_ge.mean()
acc = np.where(touch)[0]
print(f'[{TAG}] N={N} volscale={VOLSC} sd_all={sd_all*100:.2f}% sd60={sd_60*100:.2f}% sd30={sd_30*100:.2f}%  P(touch 130)={p_touch*100:.2f}%  P(close>=130 Sep30)={p_close*100:.2f}%  accepted={len(acc)}')

# restrict to accepted paths
R = R[acc]; logC = logC[acc]; Cp = Cp[acc]; bizH = bizH[acc]; bizL = bizL[acc]; sessH = sessH[acc]; sessL = sessL[acc]
first_touch_j = first_touch_j[acc]; M = len(acc)
Bc = np.exp(logC)
# ---------- WTI active month ----------
def spread(j, blev):
    cal_part = CSP * (blev / B0) ** KAPPA if post_roll[j] else 0.0
    return QSP + cal_part
wH = np.full((M, 20), -np.inf); wL = np.full((M, 20), np.inf); wC = np.zeros((M, 20))
for j in range(20):
    nz = rng.normal(0, 1.5 if post_roll[j] else 1.0, M)
    lev = np.exp(sessH[:, j]); sp = spread(j, lev) + nz
    wH[:, j] = np.where(biz[j], lev - sp, -np.inf)
    levL = np.exp(sessL[:, j]); wL[:, j] = np.where(biz[j], levL - (spread(j, levL) + nz), np.inf)
    wC[:, j] = Bc[:, j] - spread(j, Bc[:, j])
wti_max = wH.max(1); wti_min = wL.min(1)
# ---------- 10Y / 5Y / 30Y  (business-day prints) ----------
# per-print Brent % change = sum of calendar-day returns since previous print
rp = np.zeros((M, nB)); k = 0; accum = np.zeros(M)
for j in range(20):
    accum += R[:, j]
    if biz[j]:
        rp[:, k] = accum * 100.0; accum[:] = 0; k += 1
eps10 = rng.normal(0, 3.74, (M, nB))            # residual bp
d10 = B10 * rp + eps10
Y10 = 4.95 + np.cumsum(d10, 1) / 100.0
Y10p = np.round(Y10 + 1e-9, 2)
d30 = 0.75 * d10 + rng.normal(0, 2.5, (M, nB)); Y30p = np.round(5.37 + np.cumsum(d30, 1) / 100.0 + 1e-9, 2)
d5 = 1.00 * d10 + rng.normal(0, 2.0, (M, nB));  Y5p = np.round(4.75 + np.cumsum(d5, 1) / 100.0 + 1e-9, 2)
# extend 10Y to Dec 31 (63 more prints, Brent driftless bootstrap continues on business days only)
NX = 62
idx2 = rng.integers(0, len(TUP), size=(M, NX))
rx = TUP[idx2, 0] * 100.0 * math.sqrt(1.4)   # ~1.4 calendar days per business day (sd scales with sqrt)
d10x = B10 * rx + rng.normal(0, 3.74, (M, NX))
Y10x = np.round(Y10[:, -1:] + np.cumsum(d10x, 1) / 100.0 + 1e-9, 2)
Y10all = np.concatenate([Y10p, Y10x], 1)
logBx = np.log(Bc[:, -1:]) + np.cumsum(rx / 100.0, 1)
UOx = TUP[idx2, 1] * math.sqrt(1.4); pcx = np.concatenate([np.log(Bc[:, -1:]), logBx[:, :-1]], 1); logHx = np.maximum(pcx, logBx) + UOx
bx_max = np.exp(np.maximum(logHx.max(1), bizH.max(1)))
wti_max_dec = np.maximum(wti_max, np.exp(logHx.max(1)) - QSP)
P_ath_sep = float((wti_max > 147.27).mean()); P_ath_dec = float((wti_max_dec > 147.27).mean())
d30x = 0.75 * d10x + rng.normal(0, 2.5, (M, NX)); Y30all = np.concatenate([Y30p, np.round(Y30p[:, -1:] + np.cumsum(d30x, 1)/100.0 + 1e-9, 2)], 1)
# ---------- assets (business days) ----------
def asset(S0, beta, vol_ann, lohi='both', n=nB):
    dsd = vol_ann / math.sqrt(252) * 100.0
    oil = beta * rp
    res_sd = math.sqrt(max(dsd**2 - (beta * 3.55 * VOLSC)**2, 0.1))
    rr = (oil + rng.normal(0, res_sd, (M, nB))) / 100.0
    lc = math.log(S0) + np.cumsum(rr, 1)
    pc = np.concatenate([np.full((M, 1), math.log(S0)), lc[:, :-1]], 1)
    # Brownian-bridge intraday extreme given endpoints, per day
    u = rng.uniform(1e-12, 1, (M, nB)); s2 = (dsd / 100.0) ** 2
    hi = (pc + lc) / 2 + np.sqrt(((lc - pc) ** 2) / 4 - s2 * np.log(u) / 2)   # max of bridge
    u2 = rng.uniform(1e-12, 1, (M, nB))
    lo = (pc + lc) / 2 - np.sqrt(((lc - pc) ** 2) / 4 - s2 * np.log(u2) / 2)
    return np.exp(lc), np.exp(hi), np.exp(lo)
spxC, spxH, spxL = asset(7591.70, BSPX, 0.158)
spyH = spxH / 10.0; spyL = spxL / 10.0; spyC = spxC / 10.0
xauC, xauH, xauL = asset(4320.0, -0.156, 0.23)
xagC, xagH, xagL = asset(63.50, -0.333, 0.43)
dxyC, dxyH, dxyL = asset(99.09, 0.045, 0.06)
btcC, btcH, btcL = asset(77127.0, -0.219, 0.32)
# ---------- unconditional reference (same machinery, no conditioning) on a fresh smaller sample ----------
def uncond(n=300_000):
    idx = rng.integers(0, len(TUP), size=(n, 20)); Ru = TUP[idx, 0]; UOu = TUP[idx, 1]; DOu = TUP[idx, 2]
    lc = np.log(B0) + np.cumsum(Ru, 1); pc = np.concatenate([np.full((n, 1), np.log(B0)), lc[:, :-1]], 1)
    lh = np.maximum(pc, lc) + UOu; ll = np.minimum(pc, lc) - DOu
    sh = lh.copy(); sl = ll.copy()
    for j, dd in enumerate(cal):
        if dd in (14, 21, 28): sh[:, j] = np.max(lh[:, j-2:j+1], 1); sl[:, j] = np.min(ll[:, j-2:j+1], 1)
    out = {}
    wh = np.full((n, 20), -np.inf); wl = np.full((n, 20), np.inf)
    for j in range(20):
        nz = rng.normal(0, 1.5 if post_roll[j] else 1.0, n); lev = np.exp(sh[:, j]); sp = spread(j, lev) + nz
        wh[:, j] = np.where(biz[j], lev - sp, -np.inf); levL = np.exp(sl[:, j]); wl[:, j] = np.where(biz[j], levL - (spread(j, levL) + nz), np.inf)
    wmax = wh.max(1); wmin = wl.min(1)
    for lvl in (105, 110, 115, 120, 125, 130, 140, 150): out[f'wti_hi_{lvl}'] = float((wmax >= lvl).mean())
    for lvl in (100, 95, 90, 85, 80): out[f'wti_lo_{lvl}'] = float((wmin <= lvl).mean())
    bmax = np.where(biz[None, :], sh, -np.inf).max(1)
    for lvl in (115, 120, 125, 130, 140): out[f'brent_hi_{lvl}'] = float((np.exp(bmax) >= lvl).mean())
    rpu = np.zeros((n, nB)); k = 0; ac = np.zeros(n)
    for j in range(20):
        ac += Ru[:, j]
        if biz[j]: rpu[:, k] = ac * 100; ac[:] = 0; k += 1
    d10u = B10 * rpu + rng.normal(0, 3.74, (n, nB)); y10 = np.round(4.95 + np.cumsum(d10u, 1) / 100 + 1e-9, 2)
    idx2 = rng.integers(0, len(TUP), size=(n, NX)); rxu = TUP[idx2, 0] * 100 * math.sqrt(1.4); d10xu = B10 * rxu + rng.normal(0, 3.74, (n, NX))
    y10x = np.round(y10[:, -1:] + np.cumsum(d10xu, 1) / 100 + 1e-9, 2); y10a = np.concatenate([y10, y10x], 1)
    lbx = np.log(np.exp(lc[:, -1:])) + np.cumsum(rxu / 100, 1); pcx = np.concatenate([lc[:, -1:], lbx[:, :-1]], 1); lhx = np.maximum(pcx, lbx) + TUP[idx2, 1] * math.sqrt(1.4)
    wmd = np.maximum(wmax, np.exp(lhx.max(1)) - QSP)
    out['ath_sep'] = float((wmax > 147.27).mean()); out['ath_dec'] = float((wmd > 147.27).mean())
    for lvl in (4.97, 5.00, 5.05, 5.10, 5.15, 5.20): out[f'y10_sep_{lvl:.2f}'] = float((y10.max(1) >= lvl - 1e-9).mean())
    for lvl in (4.76, 4.73, 4.70, 4.64, 4.61): out[f'y10_sep_lo_{lvl:.2f}'] = float((y10.min(1) < lvl - 1e-9).mean())
    for lvl in (5.00, 5.20, 5.50, 5.70, 6.00): out[f'y10_2026_{lvl:.2f}'] = float((y10a.max(1) >= lvl - 1e-9).mean())
    d30u = 0.75 * d10u + rng.normal(0, 2.5, (n, nB)); y30 = np.round(5.37 + np.cumsum(d30u, 1) / 100 + 1e-9, 2)
    d30xu = 0.75 * d10xu + rng.normal(0, 2.5, (n, NX)); y30a = np.concatenate([y30, np.round(y30[:, -1:] + np.cumsum(d30xu, 1)/100 + 1e-9, 2)], 1)
    out['y30_sep_5.40'] = float((y30.max(1) >= 5.40 - 1e-9).mean()); out['y30_2026_5.40'] = float((y30a.max(1) >= 5.40 - 1e-9).mean())
    out['y30_sep_lo_5.15'] = float((y30.min(1) < 5.15 - 1e-9).mean()); out['y30_sep_lo_5.12'] = float((y30.min(1) < 5.12 - 1e-9).mean())
    d5u = 1.0 * d10u + rng.normal(0, 2.0, (n, nB)); y5 = np.round(4.75 + np.cumsum(d5u, 1) / 100 + 1e-9, 2)
    out['y5_sep_4.78'] = float((y5.max(1) >= 4.78 - 1e-9).mean()); out['y5_sep_4.83'] = float((y5.max(1) >= 4.83 - 1e-9).mean())
    def ast(S0, beta, vol):
        dsd = vol / math.sqrt(252) * 100; res = math.sqrt(max(dsd**2 - (beta*3.55*VOLSC)**2, 0.1))
        rr = (beta * rpu + rng.normal(0, res, (n, nB))) / 100; lc = math.log(S0) + np.cumsum(rr, 1)
        pc = np.concatenate([np.full((n, 1), math.log(S0)), lc[:, :-1]], 1); s2 = (dsd/100)**2
        u = rng.uniform(1e-12, 1, (n, nB)); hi = (pc+lc)/2 + np.sqrt((lc-pc)**2/4 - s2*np.log(u)/2)
        u2 = rng.uniform(1e-12, 1, (n, nB)); lo = (pc+lc)/2 - np.sqrt((lc-pc)**2/4 - s2*np.log(u2)/2)
        return np.exp(lc), np.exp(hi), np.exp(lo)
    sc, shh, sll = ast(7591.70, BSPX, 0.158)
    for lvl in (750, 740, 730, 720, 710, 700): out[f'spy_lo_{lvl}'] = float((sll.min(1) / 10 <= lvl).mean())
    gc, gh, gl = ast(4320.0, -0.156, 0.23)
    for lvl in (4300, 4200, 4100, 4000): out[f'xau_lo_{lvl}'] = float((gl.min(1) <= lvl).mean())
    for lvl in (4500, 4600, 4700, 4800): out[f'xau_hi_{lvl}'] = float((gh.max(1) >= lvl).mean())
    ac_, ah, al = ast(63.5, -0.333, 0.43)
    for lvl in (62, 60, 58, 56): out[f'xag_lo_{lvl}'] = float((al.min(1) <= lvl).mean())
    out['xag_hi_70'] = float((ah.max(1) >= 70).mean())
    dc, dh, dl = ast(99.09, 0.045, 0.06)
    for lvl in (99.5, 100.0, 100.5): out[f'dxy_hi_{lvl}'] = float((dh.max(1) >= lvl).mean())
    for lvl in (98.5, 98.0): out[f'dxy_lo_{lvl}'] = float((dl.min(1) <= lvl).mean())
    out['spx_end'] = float(np.median(sc[:, -1])); out['brent_end'] = float(np.median(np.exp(lc[:, -1])))
    return out
U = uncond()
# ---------- conditional stats ----------
P = {}
for lvl in (105, 110, 115, 120, 125, 130, 140, 150): P[f'wti_hi_{lvl}'] = float((wti_max >= lvl).mean())
for lvl in (100, 95, 90, 85, 80): P[f'wti_lo_{lvl}'] = float((wti_min <= lvl).mean())
for lvl in (115, 120, 125, 130, 140): P[f'brent_hi_{lvl}'] = float((np.exp(bizH.max(1)) >= lvl).mean())
for lvl in (4.97, 5.00, 5.05, 5.10, 5.15, 5.20): P[f'y10_sep_{lvl:.2f}'] = float((Y10p.max(1) >= lvl - 1e-9).mean())
for lvl in (4.76, 4.73, 4.70, 4.64, 4.61): P[f'y10_sep_lo_{lvl:.2f}'] = float((Y10p.min(1) < lvl - 1e-9).mean())
for lvl in (5.00, 5.20, 5.50, 5.70, 6.00): P[f'y10_2026_{lvl:.2f}'] = float((Y10all.max(1) >= lvl - 1e-9).mean())
P['ath_sep'] = P_ath_sep; P['ath_dec'] = P_ath_dec
P['y30_sep_5.40'] = float((Y30p.max(1) >= 5.40 - 1e-9).mean()); P['y30_2026_5.40'] = float((Y30all.max(1) >= 5.40 - 1e-9).mean())
P['y30_sep_lo_5.15'] = float((Y30p.min(1) < 5.15 - 1e-9).mean()); P['y30_sep_lo_5.12'] = float((Y30p.min(1) < 5.12 - 1e-9).mean())
P['y5_sep_4.78'] = float((Y5p.max(1) >= 4.78 - 1e-9).mean()); P['y5_sep_4.83'] = float((Y5p.max(1) >= 4.83 - 1e-9).mean())
for lvl in (750, 740, 730, 720, 710, 700): P[f'spy_lo_{lvl}'] = float((spyL.min(1) <= lvl).mean())
for lvl in (4300, 4200, 4100, 4000): P[f'xau_lo_{lvl}'] = float((xauL.min(1) <= lvl).mean())
for lvl in (4500, 4600, 4700, 4800): P[f'xau_hi_{lvl}'] = float((xauH.max(1) >= lvl).mean())
for lvl in (62, 60, 58, 56): P[f'xag_lo_{lvl}'] = float((xagL.min(1) <= lvl).mean())
P['xag_hi_70'] = float((xagH.max(1) >= 70).mean())
for lvl in (99.5, 100.0, 100.5): P[f'dxy_hi_{lvl}'] = float((dxyH.max(1) >= lvl).mean())
for lvl in (98.5, 98.0): P[f'dxy_lo_{lvl}'] = float((dxyL.min(1) <= lvl).mean())
# path descriptors
ft_day = np.array(cal)[first_touch_j]
desc = {
  'brent_end_med': float(np.median(Bc[:, -1])), 'brent_end_p10': float(np.percentile(Bc[:, -1], 10)), 'brent_end_p90': float(np.percentile(Bc[:, -1], 90)),
  'brent_max_med': float(np.median(np.exp(bizH.max(1)))),
  'first_touch_day_med': float(np.median(ft_day)), 'touch_pre_roll_share': float((ft_day <= 17).mean()),
  'touch_by_sep16_share': float((ft_day <= 16).mean()),
  'brent_sep16_med': float(np.median(Bc[:, cal.index(16)])),
  'wti_max_med': float(np.median(wti_max)), 'wti_max_p10': float(np.percentile(wti_max, 10)), 'wti_max_p90': float(np.percentile(wti_max, 90)),
  'y10_sep30_med': float(np.median(Y10p[:, -1])), 'y10_sep30_p10': float(np.percentile(Y10p[:, -1], 10)), 'y10_sep30_p90': float(np.percentile(Y10p[:, -1], 90)),
  'y10_max_med': float(np.median(Y10p.max(1))), 'y10_sep16_med': float(np.median(Y10p[:, 3])),
  'y10_dec31_med': float(np.median(Y10all[:, -1])),
  'y30_sep30_med': float(np.median(Y30p[:, -1])), 'y5_sep30_med': float(np.median(Y5p[:, -1])),
  'spx_end_med': float(np.median(spxC[:, -1])), 'spx_min_med': float(np.median(spxL.min(1))), 'spx_end_p10': float(np.percentile(spxC[:, -1], 10)),
  'xau_end_med': float(np.median(xauC[:, -1])), 'xag_end_med': float(np.median(xagC[:, -1])), 'dxy_end_med': float(np.median(dxyC[:, -1])), 'btc_end_med': float(np.median(btcC[:, -1])),
  'brent_ret_to_sep30_med_pct': float(np.median(np.log(Bc[:, -1] / B0)) * 100),
  'sum_oil_bp_med': float(np.median(B10 * rp.sum(1))),
}
ret = Bc[:, -1] <= 120.0
RT = {'share': float(ret.mean()), 'y10_sep_5.00': float((Y10p[ret].max(1) >= 5.00 - 1e-9).mean()), 'y10_sep_5.10': float((Y10p[ret].max(1) >= 5.10 - 1e-9).mean()),
      'spy_lo_720': float((spyL[ret].min(1) <= 720).mean()), 'spy_lo_730': float((spyL[ret].min(1) <= 730).mean()), 'xau_lo_4100': float((xauL[ret].min(1) <= 4100).mean()),
      'dxy_hi_100.0': float((dxyH[ret].max(1) >= 100).mean()), 'wti_hi_125': float((wti_max[ret] >= 125).mean()), 'wti_hi_120': float((wti_max[ret] >= 120).mean()), 'wti_lo_100': float((wti_min[ret] <= 100).mean()),
      'y10_sep30_med': float(np.median(Y10p[ret][:, -1])), 'spx_end_med': float(np.median(spxC[ret][:, -1])), 'brent_end_med': float(np.median(Bc[ret][:, -1]))}
out = {'tag': TAG, 'retrace': RT, 'N': N, 'volscale': VOLSC, 'kappa': KAPPA, 'beta10': B10, 'betaspx': BSPX, 'p_touch': p_touch, 'p_close130': p_close,
       'accepted': int(M), 'sd_all': float(sd_all), 'sd60': float(sd_60), 'sd30': float(sd_30), 'spread_pre': SPREAD_PRE, 'spread_post': SPREAD_POST,
       'cond': P, 'uncond': U, 'desc': desc}
json.dump(out, open(f'/tmp/oil/model_oil_{TAG}.json', 'w'), indent=1)
print(json.dumps(desc, indent=1))
for k in P: print(f'{k:18s} cond {P[k]*100:6.1f}   uncond {U.get(k, float("nan"))*100:6.1f}')
