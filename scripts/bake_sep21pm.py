#!/usr/bin/env python3
"""Sep 21 PM bake — THE FIRST POST-BREAKOUT CLOSE re-marks the Largest-Company
tab: all five green, NVDA +2.30% on top, the lead runs through 10% (fifth
straight widening: 5.51 → 6.03 → 7.24 → 8.95 → 10.52), T 7 / 71, and every
fair re-dealt from scripts/verify_sep21pm.py (calibration reproduced every
Sep 18-input fair exactly first). Ladders = the unchanged Sep 16 01:45Z walk
(FOUR sessions behind and pre-breakout, disclosed on every touched surface).
Off-board: BTC TOUCHED THE $85K RUNG (Coinbase $86,267.46 / CoinGecko
$86,534.71 live; Kraken AND CMC re-served the AM prints to the cent and were
discarded; wire corroboration on the touch). Every replacement asserts
exactly one occurrence."""
import io

P = 'polymarket/index.html'
html = io.open(P, encoding='utf-8').read()
n0 = len(html)
R = []

def rep(old, new):
    R.append((old, new))

# ---------- A. hero ----------
rep('id="hero-lead-cap">$5.379T<', 'id="hero-lead-cap">$5.503T<')
rep('id="hero-chal-cap">$4.937T<', 'id="hero-chal-cap">$4.979T<')
rep('id="hero-gap">8.95% · $442B<', 'id="hero-gap">10.52% · $524B<')

rep('The tape (caps = the Sep 18 closes, history pages ~23:1xZ — NVDA&rsquo;s $222.27 final LOCKED Sep 19 (re-confirmed to the cent through the Sep 21 morning pass — five consecutive sessions) — the table&rsquo;s $222.06 settled to the header overnight · equity mids = the <strong>Sep 16 01:45Z interactive walk, THREE sessions behind — re-check the touch before acting</strong> · autodata DOWN — no cloud book walk)',
    'The tape (caps = the Sep 21 closes, history pages ~23:1xZ — the Sep 18 finals re-confirmed to the cent beneath them a sixth session, NVDA&rsquo;s $222.27 / 190.0M settled volume holds; one revision: AAPL&rsquo;s Sep 18 VOLUME prints 85.93M vs the 86.59M first recorded — close untouched · equity mids = the <strong>Sep 16 01:45Z interactive walk, FOUR sessions behind and pre-breakout — re-check the touch before acting</strong> · autodata DOWN — no cloud book walk)')

HERO_NEW = ('<strong>SEP 21 23:3xZ PM (THE FIRST POST-BREAKOUT CLOSE): ALL FIVE GREEN, NVIDIA ON TOP — THE LEAD RUNS '
 'THROUGH 10%.</strong> The close the whole lock series pointed at went the leader&rsquo;s way: NVDA '
 '<strong>+2.30% ($227.38, $5,502.6B) on 108.5M shares</strong> over AMZN +1.87% ($2,780.2B), MSFT +1.59% '
 '($3,726.2B), GOOGL +1.55% ($4,321.6B) and AAPL +0.85% ($4,978.7B). The lead re-widens a <strong>FIFTH '
 'straight close, 8.95% → 10.52% / $523.9B</strong> (the series since the melt-up finals: 5.51 → 6.03 → 7.24 → '
 '8.95 → 10.52); Apple&rsquo;s #2 cushion narrows to 15.21% / $657.1B (Alphabet outran Apple again); T '
 '<strong>7 / 71</strong>. The model follows the tape: crown 93.52 → <strong>97.07</strong>, seat 96.69, Dec '
 '65.98 → <strong>69.04</strong> — and for the first time in the fade file&rsquo;s life the stale 68.5 '
 'December mid sits UNDER fair (−0.54). Every edge below is a fresh fair against the SAME four-session-old '
 'pre-breakout ladders — no badge flips, the September cheap trio just widens further: re-walk queue, not '
 'ticket queue. Off-board, <strong>bitcoin TOUCHED THE $85K RUNG</strong> this afternoon — a squeeze to an '
 '8-month high ($86.5k on two live sources, day high $87.3k; the wire prints &ldquo;past $85,000&rdquo; to '
 '&ldquo;$87,000&rdquo;) — the ladder&rsquo;s first up-rung resolution of the series, on a tab still wearing '
 'its Sep 1 bake. <em>Morning text, kept:</em> ')
rep('data-longform-label="More"><strong>SEP 21 13:3xZ AM (MONDAY PRE-OPEN): THE LOCK HOLDS A FIFTH PASS',
    'data-longform-label="More">' + HERO_NEW + '<strong>SEP 21 13:3xZ AM (MONDAY PRE-OPEN): THE LOCK HOLDS A FIFTH PASS')

# ---------- B. KPI ----------
rep('id="kpi-edge">sep2AAPL −8.59<', 'id="kpi-edge">sep2AAPL −12.19<')
rep('Best RV · Whole Complex (Sep 18 close vs 01:45Z walk)</div><div class="kpi-value">dec-AAPL 1.20×<',
    'Best RV · Whole Complex (Sep 21 close vs 01:45Z walk)</div><div class="kpi-value">sep2AAPL 1.14×<')

# ---------- C. Best Bets ----------
rep('Walk: Sep 16, 2026 · 01:45 UTC · fairs re-run on the Sep 18 closes at 23:1xZ (T 8 / 72) — touches are THREE sessions behind and predate the breakout: re-walk before acting',
    'Walk: Sep 16, 2026 · 01:45 UTC · fairs re-run on the Sep 21 closes at 23:3xZ (T 7 / 71) — touches are FOUR sessions behind and predate the breakout: re-walk before acting')

BB_NEW = ('<strong>Sep 21 23:3xZ PM: the first post-breakout close re-deals every row against ladders now FOUR '
 'sessions old. What moved: the lead runs 8.95% → 10.52% (a fifth straight widening), every September fair '
 'goes near-terminal (crown 97.07, seat 96.69, 3rd 99.37) so every September &ldquo;cheap&rdquo; below is '
 'stale-book width, not a ticket; #1&rsquo;s stand-down HOLDS a second close (fair 25.86, −1.96 at the stale '
 'touch); #2&rsquo;s hold now marks 4× model (fair 2.93); #3&rsquo;s fade loses its last leg — the stale 68 '
 'bid sits UNDER the 69.04 fair; #4&rsquo;s sell strengthens a fifth session (fair 0.25); the watch '
 'row&rsquo;s ask is 5× fair. Off-board, BTC touched the $85k rung this afternoon ($86.5k spot) — the '
 'Bitcoin tab&rsquo;s Sep 1 bake now carries a resolved rung.</strong> · ')
rep('"Read the full note"><strong>Sep 18 23:1xZ PM: the quad-witching close (lead 8.95%, past the melt-up finals) re-deals every row',
    '"Read the full note">' + BB_NEW + '<strong>Sep 18 23:1xZ PM: the quad-witching close (lead 8.95%, past the melt-up finals) re-deals every row')

# --- row #1 dec-AAPL ---
rep('data-bb-touch="dec-AAPL">23.9¢</td>\n                <td class="col-num">28.69%</td>\n                <td class="col-num">−4.79</td>\n                <td class="col-num">1.20× (1.20×)</td>\n                <td class="col-num">$0 <span class="pm-note">inside fair−5 (23.69) — nothing on the walked book clears it · $1,631 ≤ fair</span></td>',
    'data-bb-touch="dec-AAPL">23.9¢</td>\n                <td class="col-num">25.86%</td>\n                <td class="col-num">−1.96</td>\n                <td class="col-num">1.08× (1.08×)</td>\n                <td class="col-num">$0 <span class="pm-note">inside fair−5 (20.86) — nothing on the walked book clears it · $1,127 ≤ fair</span></td>')
rep('$625 at the 23.9¢ touch (2,616 sh) · $1,018 ≤ 25¢ · $1,631 ≤ the 28.69 fair',
    '$625 at the 23.9¢ touch (2,616 sh) · $1,018 ≤ 25¢ · $1,127 ≤ the 25.86 fair')
rep('<strong>STAND DOWN — the ticket&rsquo;s own stop fired tonight:</strong> the rule written into it was &ldquo;retire on fair &lt; mid + 5&rdquo;, and the breakout close puts the fair (28.69) 4.84 under the walked 23.85 mid — the first inside-band print since Sep 11. No buy at 23.9¢. Re-arm only if a fresh walk prints a touch ≤ 23.69 (fair−5) or the fair re-crosses mid + 5. New position — the account holds none.',
    '<strong>STAND DOWN HOLDS a second close:</strong> the rule is &ldquo;retire on fair &lt; mid + 5&rdquo;, and the first post-breakout close pulls the fair to 25.86 — just 2.01 over the walked 23.85 mid, deep inside the band (−1.96 at the stale 23.9¢ touch). No buy. Re-arm only if a fresh walk prints a touch ≤ 20.86 (fair−5) or the fair re-crosses mid + 5. New position — the account holds none.')
rep('The fair is still the most robust number on the tab: 24.3 / 28.7 / 30.8 / 31.6 at σ 1.5 / 2 / 2.5 / 3%/day',
    'The fair is still the most robust number on the tab: 20.8 / 25.9 / 28.5 / 29.7 at σ 1.5 / 2 / 2.5 / 3%/day')
rep('The market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 1.47%/day to be right — or, at σ 2%, <strong>essentially no drift view at all (≈0.1%)</strong>: after tonight the market and the model price this coin the same.',
    'The market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 1.76%/day to be right — or, at σ 2%, an expected <strong>≈+1.2% NVDA-vs-AAPL drift</strong> over the window: the market and the model still price this coin nearly the same.')
rep('Realized σ<sub>rel</sub> on the NVDA/AAPL pair over the six daily returns Sep 8–15 was ~2.5%/day (2.7 without the Sep 8 print) — six observations, one of them the −5.9% melt-up day: it supports the direction, not the digit.',
    'Realized σ<sub>rel</sub> on the pair over the four sessions since Sep 15 is ~1.2%/day RMS — but all four prints are one-signed (NVIDIA outran Apple every session): what the tape is showing is drift, the one thing the model refuses to price.')
rep('72 trading days for an 8.95% gap.', '71 trading days for a 10.52% gap.')

# --- row #2 sep-crownAAPL ---
rep('data-bb-touch="sep-crownAAPL">12.7¢</td>\n                <td class="col-num">6.48%</td>\n                <td class="col-num">+6.22</td>\n                <td class="col-num">0.51× (0.51×)</td>',
    'data-bb-touch="sep-crownAAPL">12.7¢</td>\n                <td class="col-num">2.93%</td>\n                <td class="col-num">+9.77</td>\n                <td class="col-num">0.23× (0.23×)</td>')
rep('$0 of asks at or under the 6.48 fair · twin: NVIDIA-crown 87.15 mid vs a 93.52 fair (−6.37) — the stale pair (99.75 summed) prices the pre-breakout crown, not tonight&rsquo;s',
    '$0 of asks at or under the 2.93 fair · twin: NVIDIA-crown 87.15 mid vs a 97.07 fair (−9.92) — the stale pair (99.75 summed) prices the pre-breakout crown, not tonight&rsquo;s')
rep('<strong>HOLD the 22,532 sh (5.86¢ avg) — the mark is RICH tonight:</strong> the breakout cut the crown fair 12.20 → 6.48 (lead 8.95%), so the stale 12.6 mid sits +6.12 ABOVE fair — the model would now SELL this mid, but the mid is three sessions old and the exit reality is what it was: the bid ladder takes 1,295 sh at 10¢ or better, ≈$892 for the whole position, and only $275 of bids rest at or over the 6.48 fair — the $2,839 mark is not a liquidation value. The position still rides to resolution; <strong>a fresh walk, not this stale print, decides whether the 12.4–12.5¢ bids are worth hitting.</strong>',
    '<strong>HOLD the 22,532 sh (5.86¢ avg) — the mark is now 4× model:</strong> the first post-breakout close cuts the crown fair again, 6.48 → 2.93 (lead 10.52%), so the stale 12.6 mid sits +9.67 ABOVE fair — on tonight&rsquo;s numbers every bid on the stale ladder down to 3¢ beats the model ($672 rests at or over the 2.93 fair), but the ladder is four sessions old and the exit reality it printed is unchanged: 1,295 sh at 10¢ or better, ≈$892 for the whole position — the $2,839 mark is not a liquidation value. The position still rides to resolution; <strong>a fresh walk, not this stale print, decides whether the exit bids are worth hitting.</strong>')
rep('The rank is history, not edge: the tab&rsquo;s biggest position now marks at TWICE its model value — 6.48 fair vs the stale 12.6 mid — one close after marking at fair. The number is still the least robust here: 2.2 / 6.5 / 11.3 / 15.6 across the same σ sweep — at σ 2.5%/day the mark is nearly fair again, at σ 1.5% it is 6× rich. Eight trading days for an 8.95% gap; the position rides to resolution because the exit bid, not the model, says so.',
    'The rank is history, not edge: the tab&rsquo;s biggest position now marks at FOUR TIMES its model value — 2.93 fair vs the stale 12.6 mid. The number is still the least robust here: 0.6 / 2.9 / 6.5 / 10.4 across the same σ sweep — at σ 3%/day the stale mid is close to fair, at σ 1.5% it is 20× rich. Seven trading days for a 10.52% gap; the position rides to resolution because the exit bid, not the model, says so.')

# --- row #3 dec-NVDA NO ---
rep('<td class="col-num">65.98% <span class="pm-note">(NO 34.02)</span></td>',
    '<td class="col-num">69.04% <span class="pm-note">(NO 30.96)</span></td>')
rep('<td class="col-num">+2.02 <span class="pm-note">(mid +2.52)</span></td>',
    '<td class="col-num">−1.04 <span class="pm-note">(mid −0.54)</span></td>')
rep('<td class="col-num">NO 1.06× (1.08×)</td>', '<td class="col-num">NO 0.97× (0.98×)</td>')
rep('<td class="col-num">$423 NO <span class="pm-note">NO-dollars ≤ the 34.02 NO-fair ($853 YES-notional of bids ≥ 65.98)</span></td>',
    '<td class="col-num">$0 NO <span class="pm-note">no bid ≥ the 69.04 fair rests on the walked book (top bid 68.0)</span></td>')
rep('<span class="pm-badge pm-cheap">DEEP</span> <span class="pm-note">$77 of NO at 32¢ (the 68 bid × 240.8 sh), then 33¢ × 615.5 — buy NO = sell YES into the bid, one book</span>',
    '<span class="pm-badge pm-watch">DEEP · OVER FAIR</span> <span class="pm-note">the first NO costs 32¢ against a 30.96 NO-fair (the 68 bid × 240.8 sh) — every rung on the stale ladder now pays over model for the fade</span>')
rep('tonight&rsquo;s close KILLED the fade (fair 62.51 → 65.98 — the RICH badge comes off at +2.52, as the Sep 17 note said one more session like this would do; the December book is all inside the band)',
    'the post-breakout close BURIES the fade (fair 65.98 → 69.04 — the stale 68 bid now sits UNDER fair: for the first time in the fade file&rsquo;s life the model would not sell this book at its own touch)')
rep('because NO also pays on the Alphabet/Microsoft legs the model prices at 4.6 combined.',
    'because NO also pays on the Alphabet/Microsoft legs the model prices at 4.4 combined.')

# --- row #4 sep-sep3MSFT ---
rep('data-bb-touch="sep-sep3MSFT">4.5¢ bid</td>\n                <td class="col-num">0.43%</td>\n                <td class="col-num">+4.07</td>',
    'data-bb-touch="sep-sep3MSFT">4.5¢ bid</td>\n                <td class="col-num">0.25%</td>\n                <td class="col-num">+4.25</td>')
rep('<td class="col-num">0.10× (0.09×) <span class="pm-note">YES side held; the NO side handed to the buyer is 1.04×</span></td>',
    '<td class="col-num">0.06× (0.05×) <span class="pm-note">YES side held; the NO side handed to the buyer is 1.04×</span></td>')
rep('<td class="col-num">$205</td>', '<td class="col-num">$263</td>')
rep('Microsoft needs to pass Alphabet (13.8% below it) in eight sessions — and tonight the gap widened again (GOOGL +0.64%, MSFT −0.80%, the board&rsquo;s worst close).',
    'Microsoft needs to pass Alphabet (13.8% below it) in seven sessions — tonight it finally outran Alphabet by a hair (MSFT +1.59% vs GOOGL +1.55%), a rounding error against the gap.')
rep('Small, but the only held leg on the tab priced at 0.10× its model value with a bid that takes all of it — the close cut the fair again (1.26 → 0.43), so the sell strengthens a fourth straight session, the strongest print yet.',
    'Small, but the only held leg on the tab priced at 0.06× its model value with a bid that takes all of it — the close cut the fair again (0.43 → 0.25), so the sell strengthens a fifth straight session, the strongest print yet.')

# --- watch row sep-sep2NVDA ---
rep('data-bb-touch="sep-sep2NVDA">14.3¢</td>\n                <td class="col-num">6.47%</td>\n                <td class="col-num">+7.83</td>\n                <td class="col-num">0.45× (0.50×)</td>',
    'data-bb-touch="sep-sep2NVDA">14.3¢</td>\n                <td class="col-num">2.93%</td>\n                <td class="col-num">+11.37</td>\n                <td class="col-num">0.20× (0.23×)</td>')
rep('11.6 / 14.3 — $0 of asks at or under the 6.47 fair', '11.6 / 14.3 — $0 of asks at or under the 2.93 fair')
rep('<strong>No ticket — and the premium doubled tonight:</strong> the breakout pulls the fair to 6.47, HALF the 14.3¢ ask (+7.83) — there is no price on this book the model would pay. The account already holds 1,009.68 sh at 4.95¢ (+$80.8 open).',
    '<strong>No ticket — the ask is now 5× fair:</strong> the post-breakout close pulls the fair to 2.93, a FIFTH of the 14.3¢ ask (+11.37) — there is no price on this book the model would pay. The account already holds 1,009.68 sh at 4.95¢ (marked at the stale 12.95 mid).')
rep('Listed so nobody buys it thinking it is a second idea: NVIDIA finishing 2nd ≈ Apple finishing 1st (6.47 vs 6.48). The seat&rsquo;s other side — sep2AAPL 84.5 vs 93.09, −8.59 with $805 of asks inside fair−5 — is tonight&rsquo;s widest print, and it is a THREE-session-old pre-breakout ladder: it heads the re-walk queue, not the ticket queue.',
    'Listed so nobody buys it thinking it is a second idea: NVIDIA finishing 2nd ≈ Apple finishing 1st (2.93 vs 2.93 — the same coin to the basis point tonight). The seat&rsquo;s other side — sep2AAPL 84.5 vs 96.69, −12.19 with $1,285 of asks inside fair−5 — is the board&rsquo;s widest print a second straight close, and it is a FOUR-session-old pre-breakout ladder: it heads the re-walk queue, not the ticket queue.')

# --- honesty line ---
rep('(8.95% / $442.1B at the Sep 18 close)', '(10.52% / $523.9B at the Sep 21 close)')
rep('pay together only 3.4% of the time (P(Dec | Sep) 53% vs P(Dec | not Sep) 27%, payoff correlation ≈0.14)',
    'pay together only 1.6% of the time (P(Dec | Sep) 53% vs P(Dec | not Sep) 25%, payoff correlation ≈0.11)')
rep('#2&rsquo;s ADD is dead — nothing on the walked book beats the 6.48 fair',
    '#2&rsquo;s ADD is dead — nothing on the walked book beats the 2.93 fair')

# ---------- D. analysis table ----------
FOOT_NEW = ('<strong>Sep 21 23:3xZ PM — the first post-breakout close stretches the lead through 10%.</strong> '
 'Monday&rsquo;s closes (history pages ~23:1xZ; the Sep 18 finals re-confirmed to the cent beneath them a '
 'sixth session — NVDA&rsquo;s $222.27 on 190.0M settled shares holds; one revision caught: AAPL&rsquo;s '
 'Sep 18 VOLUME prints 85.93M vs the 86.59M first recorded, close untouched): NVDA <strong>+2.30% to $227.38 '
 '($5,502.6B) on 108.5M shares</strong> leads an all-green board — AMZN +1.87% ($2,780.2B), MSFT +1.59% '
 '($3,726.2B), GOOGL +1.55% ($4,321.6B), AAPL +0.85% ($4,978.7B). The lead re-widens a FIFTH straight close, '
 '8.95% → <strong>10.52% / $523.9B</strong> (the series since the melt-up finals: 5.51 → 6.03 → 7.24 → 8.95 → '
 '10.52); Apple&rsquo;s cushion over Alphabet narrows 16.01% → 15.21% / $657.1B; T <strong>7 / 71</strong>. '
 'Fairs re-dealt (calibration reproduced every Sep 18-input fair exactly first): Dec 69.04 / 25.86 / 4.07 / '
 '0.28 / 0.00; crown 97.07 / 2.93; seat 96.69-AAPL / 2.93-NVDA; 3rd 99.37-GOOGL / 0.37-AAPL / 0.25-MSFT; '
 'P(±5/wk) 58 / 56 / 4. Every edge below is marked against the SAME Sep 16 01:45Z ladders, now FOUR sessions '
 'old and pre-breakout — <strong>no badge flips tonight</strong>: the September cheap trio just widens '
 'further on stale books (re-walk first), dec-AAPL&rsquo;s stand-down holds (−2.01), and dec-NVDA&rsquo;s '
 'stale 68.5 mid slips UNDER fair (−0.54) for the first time. · ')
rep('"Read the full analysis"><strong>Sep 18 23:1xZ PM — the quad-witching breakout stands the flagship down.</strong>',
    '"Read the full analysis">' + FOOT_NEW + '<strong>Sep 18 23:1xZ PM — the quad-witching breakout stands the flagship down.</strong>')

SEPGRP_NEW = ('<strong>Sep 21 23:3xZ PM: the first post-breakout close makes the partition near-terminal — crown '
 '97.07 / 2.93, seat 96.69-AAPL / 2.93-NVDA, 3rd 99.37-GOOGL / 0.25-MSFT. Every September edge below is a '
 'fresh fair against a FOUR-session-old pre-breakout ladder — the stale-ladder cheap trio widens again '
 '(crownNVDA −9.92 with $6,844 inside fair−5, sep2AAPL −12.19 with $1,285, sep3GOOGL −6.37 with $835 at the '
 '94.0 ask): re-walk queue, not ticket queue.</strong> · ')
rep('SEPTEMBER 30 · T = 8 trading days · <strong>Sep 18 23:1xZ PM: the breakout hands the partition to the leaders',
    'SEPTEMBER 30 · T = 7 trading days · ' + SEPGRP_NEW + '<strong>Sep 18 23:1xZ PM: the breakout hands the partition to the leaders')

DECGRP_NEW = ('<strong>Sep 21 23:3xZ PM: the close pushes the December leader UNDER its own fair for the first '
 'time — dec-NVDA 68.5 stale mid vs 69.04 (−0.54), dec-AAPL eases to −2.01 (stand-down holds), dec-GOOGL '
 '+2.43, dec-MSFT +0.27: the whole book inside the band on four-session-old mids.</strong> · ')
rep('DECEMBER 31 — 72 TRADING DAYS · <strong>Sep 18 23:1xZ PM: the December book goes ALL-FAIR',
    'DECEMBER 31 — 71 TRADING DAYS · ' + DECGRP_NEW + '<strong>Sep 18 23:1xZ PM: the December book goes ALL-FAIR')

# --- caps + gaps ---
rep('data-cap="NVDA-sep">5,378.9<', 'data-cap="NVDA-sep">5,502.6<')
rep('data-cap="AAPL-sep">4,936.9<', 'data-cap="AAPL-sep">4,978.7<')
rep('data-gap="AAPL-sep">−8.22%<', 'data-gap="AAPL-sep">−9.52%<')
rep('data-cap="NVDA-dec">5,378.9<', 'data-cap="NVDA-dec">5,502.6<')
rep('data-cap="AAPL-dec">4,936.9<', 'data-cap="AAPL-dec">4,978.7<')
rep('data-gap="AAPL-dec">−8.22%<', 'data-gap="AAPL-dec">−9.52%<')
rep('data-cap="GOOGL-dec">4,255.5<', 'data-cap="GOOGL-dec">4,321.6<')
rep('data-gap="GOOGL-dec">−20.89%<', 'data-gap="GOOGL-dec">−21.46%<')
rep('data-cap="MSFT-dec">3,668.0<', 'data-cap="MSFT-dec">3,726.2<')
rep('data-gap="MSFT-dec">−31.81%<', 'data-gap="MSFT-dec">−32.28%<')
rep('data-cap="AMZN-dec">2,729.2<', 'data-cap="AMZN-dec">2,780.2<')
rep('data-gap="AMZN-dec">−49.26%<', 'data-gap="AMZN-dec">−49.48%<')

# --- model rows: fair / edge / rv (+ $ cells and notes on live rows) ---
rep('data-fair="sep-crownNVDA">93.52%</td><td class="col-num" data-edge="sep-crownNVDA">−6.37</td><td class="col-num" data-pm-rv>1.07×</td><td class="col-num"><span class="pm-badge pm-fair">$8,606</span></td>',
    'data-fair="sep-crownNVDA">97.07%</td><td class="col-num" data-edge="sep-crownNVDA">−9.92</td><td class="col-num" data-pm-rv>1.11×</td><td class="col-num"><span class="pm-badge pm-fair">$20,048</span></td>')
rep('stale-ladder print ($2,713 inside fair−5) — the 01:45Z book predates the breakout: re-walk first',
    'stale-ladder print ($6,844 inside fair−5) — the 01:45Z book predates the breakout: re-walk first')
rep('data-fair="sep-crownAAPL">6.48%</td><td class="col-num" data-edge="sep-crownAAPL">+6.12</td><td class="col-num" data-pm-rv>0.51×</td><td class="col-num"><span class="pm-badge pm-rich">$275</span></td>',
    'data-fair="sep-crownAAPL">2.93%</td><td class="col-num" data-edge="sep-crownAAPL">+9.67</td><td class="col-num" data-pm-rv>0.23×</td><td class="col-num"><span class="pm-badge pm-rich">$672</span></td>')
rep('the 22,532-sh hold marks 2× model on a stale mid — rides to resolution (Best Bets #2)',
    'the 22,532-sh hold marks 4× model on a stale mid — rides to resolution (Best Bets #2)')
rep('data-fair="sep-sep2AAPL">93.09%</td><td class="col-num" data-edge="sep-sep2AAPL">−8.59</td><td class="col-num pm-pos" data-pm-rv>1.10×</td><td class="col-num"><span class="pm-badge pm-fair">$3,074</span></td>',
    'data-fair="sep-sep2AAPL">96.69%</td><td class="col-num" data-edge="sep-sep2AAPL">−12.19</td><td class="col-num pm-pos" data-pm-rv>1.14×</td><td class="col-num"><span class="pm-badge pm-fair">$13,280</span></td>')
rep('82 / 87 WIDE — tonight&rsquo;s widest print, on a pre-breakout ladder ($805 inside fair−5): re-walk first',
    '82 / 87 WIDE — the board&rsquo;s widest print a second straight close, on a pre-breakout ladder ($1,285 inside fair−5): re-walk first')
rep('data-fair="sep-sep2NVDA">6.47%</td><td class="col-num" data-edge="sep-sep2NVDA">+6.48</td><td class="col-num" data-pm-rv>0.50×</td><td class="col-num"><span class="pm-badge pm-watch">$24</span></td>',
    'data-fair="sep-sep2NVDA">2.93%</td><td class="col-num" data-edge="sep-sep2NVDA">+10.02</td><td class="col-num" data-pm-rv>0.23×</td><td class="col-num"><span class="pm-badge pm-watch">$351</span></td>')
rep('THIN · 11.6 / 14.3 · the ask is 2× fair', 'THIN · 11.6 / 14.3 · the ask is 5× fair')
rep('data-fair="sep-sep2GOOGL">0.43%</td><td class="col-num" data-edge="sep-sep2GOOGL">+1.22</td><td class="col-num" data-pm-rv>0.26×</td>',
    'data-fair="sep-sep2GOOGL">0.37%</td><td class="col-num" data-edge="sep-sep2GOOGL">+1.28</td><td class="col-num" data-pm-rv>0.22×</td>')
rep('data-fair="sep-sep3GOOGL">99.13%</td><td class="col-num" data-edge="sep-sep3GOOGL">−6.13</td><td class="col-num" data-pm-rv>1.07×</td>',
    'data-fair="sep-sep3GOOGL">99.37%</td><td class="col-num" data-edge="sep-sep3GOOGL">−6.37</td><td class="col-num" data-pm-rv>1.07×</td>')
rep('92 / 94 WIDE — the 94.0 ask itself is −5.13 tonight ($835 inside fair−5): the partition&rsquo;s first executable-looking cheap print, on a three-session-old book — re-walk first',
    '92 / 94 WIDE — the 94.0 ask itself is −5.37 tonight ($835 inside fair−5): still the partition&rsquo;s only executable-looking cheap print, now on a four-session-old book — re-walk first')
rep('data-fair="sep-sep3MSFT">0.43%</td><td class="col-num" data-edge="sep-sep3MSFT">+4.12</td><td class="col-num" data-pm-rv>0.09×</td><td class="col-num"><span class="pm-badge pm-fair">$205</span></td>',
    'data-fair="sep-sep3MSFT">0.25%</td><td class="col-num" data-edge="sep-sep3MSFT">+4.30</td><td class="col-num" data-pm-rv>0.05×</td><td class="col-num"><span class="pm-badge pm-fair">$263</span></td>')
rep('data-fair="sep-sep3AAPL">0.43%</td><td class="col-num" data-edge="sep-sep3AAPL">+1.17</td><td class="col-num" data-pm-rv>0.27×</td>',
    'data-fair="sep-sep3AAPL">0.37%</td><td class="col-num" data-edge="sep-sep3AAPL">+1.23</td><td class="col-num" data-pm-rv>0.23×</td>')
rep('data-fair="dec-NVDA">65.98%</td><td class="col-num" data-edge="dec-NVDA">+2.52</td><td class="col-num" data-pm-rv>0.96×</td><td class="col-num"><span class="pm-badge pm-fair">$853</span></td>',
    'data-fair="dec-NVDA">69.04%</td><td class="col-num" data-edge="dec-NVDA">−0.54</td><td class="col-num" data-pm-rv>1.01×</td><td class="col-num"><span class="pm-badge pm-fair">$466</span></td>')
rep('data-verdict="dec-NVDA">FAIR</span> <span class="pm-note">RICH badge off — the fade dies on its own fair</span></td><td class="col-num">60%</td>',
    'data-verdict="dec-NVDA">FAIR</span> <span class="pm-note">the stale mid slips UNDER fair — the fade has no model support at any walked price</span></td><td class="col-num">58%</td>')
rep('data-fair="dec-AAPL">28.69%</td><td class="col-num" data-edge="dec-AAPL">−4.84</td><td class="col-num" data-pm-rv>1.20×</td><td class="col-num"><span class="pm-badge pm-fair">$1,631</span>',
    'data-fair="dec-AAPL">25.86%</td><td class="col-num" data-edge="dec-AAPL">−2.01</td><td class="col-num" data-pm-rv>1.08×</td><td class="col-num"><span class="pm-badge pm-fair">$1,127</span>')
rep('data-verdict="dec-AAPL">FAIR</span> <span class="pm-note">CHEAP badge off — Best Bets #1 stands down on its own stop</span></td><td class="col-num">58%</td>',
    'data-verdict="dec-AAPL">FAIR</span> <span class="pm-note">CHEAP badge off — Best Bets #1&rsquo;s stand-down holds a second close</span></td><td class="col-num">56%</td>')
rep('data-fair="dec-GOOGL">4.27%</td><td class="col-num" data-edge="dec-GOOGL">+2.23</td><td class="col-num" data-pm-rv>0.66×</td>',
    'data-fair="dec-GOOGL">4.07%</td><td class="col-num" data-edge="dec-GOOGL">+2.43</td><td class="col-num" data-pm-rv>0.63×</td>')
rep('data-fair="dec-MSFT">0.30%</td><td class="col-num" data-edge="dec-MSFT">+0.25</td><td class="col-num" data-pm-rv>0.55×</td>',
    'data-fair="dec-MSFT">0.28%</td><td class="col-num" data-edge="dec-MSFT">+0.27</td><td class="col-num" data-pm-rv>0.51×</td>')

# ---------- E. Top Trades #1 pointer ----------
rep('<strong>Sep 18 23:1xZ PM:</strong> the quad-witching breakout (lead 8.95%, past the melt-up finals) pulls the fair 31.93 → 28.69',
    '<strong>Sep 21 23:3xZ PM:</strong> the first post-breakout close widens the lead to 10.52% and pulls the fair 28.69 → 25.86 — the stand-down HOLDS a second close (−1.96 at the stale 23.9¢ touch, RV 1.08×, $0 inside fair−5, $1,127 ≤ fair); re-arm now needs a fresh walk printing ≤ 20.86 or a fair back over mid + 5. <strong>Sep 18 23:1xZ PM:</strong> the quad-witching breakout (lead 8.95%, past the melt-up finals) pulls the fair 31.93 → 28.69')

# ---------- F. header tape append ----------
TAPE_NEW = (' · <strong>Sep 21 23:3xZ — THE FIRST POST-BREAKOUT CLOSE: ALL FIVE GREEN, THE LEAD RUNS THROUGH 10%, '
 'AND BITCOIN TOUCHES THE $85K RUNG:</strong> autodata is down a <strong>FORTY-FOURTH</strong> consecutive '
 'feed run (the Sep 21 22:45Z cron silent; this run&rsquo;s 23:1xZ poke touching fetch/poke, e1091735, '
 'unanswered — the Actions disablement stands, one manual visit to github.com/chad506/Leadsure/actions '
 'revives it). The close the lock series pointed at went the leader&rsquo;s way: NVDA <strong>+2.30% '
 '($227.38, $5,502.6B) on 108.5M shares</strong> over AMZN +1.87%, MSFT +1.59%, GOOGL +1.55% and AAPL +0.85% '
 '($4,978.7B) — the lead re-widens a <strong>fifth straight close, 8.95% → 10.52% / $523.9B</strong> (5.51 → '
 '6.03 → 7.24 → 8.95 → 10.52 since the melt-up finals), the cushion narrows to 15.21% / $657.1B, T '
 '<strong>7 / 71</strong> (the Sep 18 finals re-confirmed to the cent beneath the new rows a sixth session; '
 'one revision: AAPL&rsquo;s Sep 18 volume prints 85.93M vs the 86.59M first recorded — close untouched). '
 'Fairs re-dealt on the fresh caps (calibration exact on the locked inputs first): crown 93.52 → '
 '<strong>97.07</strong>, seat 96.69-AAPL / 2.93-NVDA, 3rd 99.37-GOOGL; Dec 65.98 → <strong>69.04</strong> / '
 '25.86-AAPL / 4.07-GOOGL; P(±5/wk) 58 / 56 / 4 — and for the first time in the fade file&rsquo;s life the '
 'stale 68.5 December mid sits UNDER fair (−0.54). No badge flips: every September &ldquo;cheap&rdquo; is '
 'four-session-old ladder width (crownNVDA −9.92, sep2AAPL −12.19, sep3GOOGL −6.37) — re-walk queue, not '
 'ticket queue; Best Bets #1 stand-down holds (fair 25.86, −1.96 at the stale touch), #2 marks 4× model, #4 '
 'sell strengthens a fifth session. <strong>BTC TOUCHES THE $85K RUNG — A MONDAY-AFTERNOON SQUEEZE TO AN '
 '8-MONTH HIGH: $86,534.71</strong> (CoinGecko LIVE, +6.6%/24h, day range $80,907&ndash;$87,330; Coinbase '
 'LIVE $86,267.46 +6.53%, ~0.31% under — two live sources; Kraken AND CMC re-served their 13:0xZ morning '
 'prints to the cent — $81,618.00/+1.48% and $81,478.68/+1.18%, same ranges — both DISCARDED as '
 'snapshot-stale, the morning&rsquo;s roles exactly reversed; the wire corroborates the touch: &ldquo;past '
 '$85,000&rdquo; Yahoo/The National/Cointelegraph, &ldquo;tops $86,000&rdquo; CNBC, &ldquo;hits '
 '$87,000&rdquo; CoinDesk live), <strong>+6.02% on the morning print, +5.91% OVER the old series high, '
 '+10.36% over the Sep 1 bake</strong>; T 101.2d. The $85k rung is a RESOLUTION EVENT, not a residual line — '
 'and every surviving rung&rsquo;s color vs the pre-breakout Sep 15 walk mids blows past the series wides '
 'into new territory ($90k −38.3, $95k −34.8, $100k −30.6, $110k −19.0; dips $60k +15.4, $55k +14.0, $50k '
 '+12.0; needed touch to $90k +4.0%): those mids are archaeology now — <strong>the BTC tab&rsquo;s re-bake '
 'goes from the loudest want on the page to a need</strong>; its Sep 1 01:27Z stamps stay until a real walk. '
 'Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No '
 'trades placed.')
rep('keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.</span>',
    'keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.' + TAPE_NEW + '</span>')

# ---------- G. sync bar ----------
LATEST_OLD_HEAD = '<strong>Latest: Sep 21 13:3xZ AM pass (Monday pre-open)'
LATEST_NEW = ('<strong>Latest: Sep 21 23:3xZ PM pass — THE FIRST POST-BREAKOUT CLOSE: all five green, NVDA +2.30% '
 '($227.38, $5,502.6B) on top — the lead re-widens a fifth straight close to 10.52% / $523.9B (5.51 → 6.03 → '
 '7.24 → 8.95 → 10.52), the cushion narrows to 15.21%, T 7 / 71; fairs re-dealt: crown 97.07 / 2.93, seat '
 '96.69 / 2.93, 3rd 99.37, Dec 69.04 / 25.86 / 4.07, P(±5/wk) 58 / 56 / 4 — the stale 68.5 dec-NVDA mid sits '
 'UNDER fair for the first time, no badge flips, the September cheap trio widens on four-session-old books '
 '(re-walk first), Best Bets #1 stand-down holds, #2 marks 4× model, #4 sell strengthens a fifth session. '
 'BTC TOUCHED THE $85K RUNG: $86,534.71 (CoinGecko live +6.6%; Coinbase live $86,267.46 ~0.31% under; Kraken '
 'and CMC re-served the morning prints to the cent — both discarded; the wire prints &ldquo;past '
 '$85,000&rdquo;&ndash;&ldquo;$87,000&rdquo;) — +5.91% over the old series high, +10.36% over the Sep 1 '
 'bake, day high $87,330: the ladder&rsquo;s first up-rung resolution, every surviving-rung residual past '
 'the series wides ($90k −38.3) — the Bitcoin tab re-bake is now a NEED. Autodata DOWN a 44th feed run; tab '
 'bakes: Oil Sep 10, Treasuries Sep 9 close, Largest-Company fairs Sep 21 23:3xZ on the Sep 16 01:45Z walk '
 'mids, Bitcoin Sep 1, Iran Sep 1; Leaderboard re-marked Sep 15 01:10Z.</strong>')

CHRON_NEW = (' <strong>Sep 21 23:3xZ PM run (the first post-breakout close): all five green — NVDA +2.30% '
 '$227.38 / $5,502.6B, AMZN +1.87%, MSFT +1.59%, GOOGL +1.55%, AAPL +0.85% $4,978.7B — the lead re-widens a '
 'fifth straight close, 8.95% → 10.52% / $523.9B; cushion 15.21%; T 7 / 71; the Sep 18 finals re-confirmed '
 'to the cent beneath the new rows a sixth session (one revision: AAPL&rsquo;s Sep 18 volume 86.59M → '
 '85.93M, close untouched). Fairs re-dealt on the fresh caps, calibration exact first: crown 97.07 / 2.93, '
 'seat 96.69 / 2.93, 3rd 99.37 / 0.25; Dec 69.04 / 25.86 / 4.07 / 0.28; P(±5/wk) 58 / 56 / 4. The stale '
 '68.5 dec-NVDA mid sits UNDER the 69.04 fair — the fade file&rsquo;s first such print; dec-AAPL&rsquo;s '
 'stand-down holds at −2.01; the September partitions go near-terminal and their cheap prints (crownNVDA '
 '−9.92, sep2AAPL −12.19, sep3GOOGL −6.37) are four-session-old ladder width: re-walk queue. BTC TOUCHED '
 'THE $85K RUNG on a Monday-afternoon squeeze to an 8-month high: $86,534.71 CoinGecko live / $86,267.46 '
 'Coinbase live (0.31% apart; Kraken and CMC re-served their 13:0xZ prints to the cent and were discarded '
 'as snapshot-stale — the morning&rsquo;s roles exactly reversed; wire: &ldquo;past $85,000&rdquo; '
 'Yahoo/The National/Cointelegraph, &ldquo;tops $86,000&rdquo; CNBC, &ldquo;hits $87,000&rdquo; CoinDesk), '
 '+6.02% on the morning print, +5.91% over the old series high, +6.53% over the $80k-break print, +10.36% '
 'over the Sep 1 bake, day high $87,329.89; T 101.2d — the $85k rung is a resolution event, and every '
 'surviving rung&rsquo;s residual vs the pre-breakout Sep 15 mids lands past the series wides ($90k −38.3, '
 '$95k −34.8, $100k −30.6, $110k −19.0; dips $60k +15.4, $55k +14.0, $50k +12.0): the BTC tab re-bake is '
 'now a need, its Sep 1 stamps stay until a real walk. Autodata DOWN a FORTY-FOURTH feed run (22:45Z cron '
 'silent; 23:1xZ poke touching fetch/poke, e1091735, unanswered — the Actions-disablement diagnosis '
 'stands). Mids/books/balances keep the Sep 16 01:45Z stamps; the ledger still owes the 61 swept fills. No '
 'trades placed.</strong>')
rep('the ledger still owes the 61 swept fills. No trades placed.</strong><span id="sync-ago"',
    'the ledger still owes the 61 swept fills. No trades placed.</strong>' + CHRON_NEW + '<span id="sync-ago"')

# ---------- apply ----------
import re as _re
m = _re.search(_re.escape(LATEST_OLD_HEAD) + r'.*?Leaderboard re-marked\s+Sep 15 01:10Z\.</strong>', html, _re.S)
assert m, "Latest head not found"
html = html[:m.start()] + LATEST_NEW + html[m.end():]

fails = []
for old, new in R:
    c = html.count(old)
    if c != 1:
        fails.append((c, old[:120]))
        continue
    html = html.replace(old, new, 1)
if fails:
    for c, o in fails:
        print(f"FAIL count={c}: {o}")
    raise SystemExit(1)
io.open(P, 'w', encoding='utf-8').write(html)
print(f"OK — latest-head + {len(R)} reps applied; {n0} → {len(html)} chars (+{len(html)-n0})")

# ---------- H. analysis caps-note prepend (second pass, same run) ----------
html = io.open(P, encoding='utf-8').read()
NOTE_NEW = ('<strong>Sep 21 23:3xZ PM: caps are the SEP 21 CLOSES (history pages ~23:1xZ; the Sep 18 finals '
 're-confirmed to the cent beneath them a sixth session — 190.0M NVDA settled volume holds; one revision: '
 'AAPL&rsquo;s Sep 18 volume 86.59M → 85.93M, close untouched): NVDA $5,502.6B ($227.38, +2.30%, 108.5M '
 'shares) / AAPL $4,978.7B ($338.98, +0.85%, the board&rsquo;s laggard) / GOOGL $4,321.6B ($354.97, +1.55%) '
 '/ MSFT $3,726.2B ($501.61, +1.59%) / AMZN $2,780.2B ($258.45, +1.87%) — all five green; the lead '
 're-widens a FIFTH straight close, 8.95% → 10.52% / $523.9B (5.51 → 6.03 → 7.24 → 8.95 → 10.52 since the '
 'melt-up finals); the cushion narrows to 15.21%; T = 7 / 71. Every fair, edge, RV, verdict and '
 'tradeable-at-fair below re-ran on these closes (calibration reproduced every locked-input fair exactly) '
 'against the UNCHANGED Sep 16 01:45Z walk mids — now FOUR sessions behind and pre-breakout: re-walk before '
 'acting. What moved: NO badge flips — the December book stays inside the band with the stale dec-NVDA mid '
 'now UNDER fair (−0.54, the fade file&rsquo;s first such print) and dec-AAPL at −2.01; the September '
 'partitions go near-terminal (crown 97.07, seat 96.69, 3rd 99.37) and their cheap prints widen on stale '
 'books only.</strong> · ')
_old = '"Read the full note"><strong>Sep 18 23:1xZ PM: caps are the SEP 18 CLOSES'
if html.count(_old) == 1:
    html = html.replace(_old, '"Read the full note">' + NOTE_NEW + '<strong>Sep 18 23:1xZ PM: caps are the SEP 18 CLOSES', 1)
    io.open(P, 'w', encoding='utf-8').write(html)
    print('caps-note prepend applied')
else:
    assert NOTE_NEW in html, 'caps-note neither pending nor applied'
    print('caps-note prepend already present')

# ---------- I. adversarial-review fixes (third pass, same run) ----------
# Confirmed blocker: "first time in the fade file's life" contradicted the Sep 4 PM
# record (dec-NVDA −2.31 — a prior under-fair print). Re-worded on every surface to
# the verifiable "first sign-flip since the Sep 16 walk (+10.6 → +8.8 → +6.0 → +2.5
# → −0.5 at the mid)". Plus two hedges: BTC "resolved/resolution" → "touched/touch"
# (resolution is the market's call, not this page's), and the CHRON discard
# parenthetical no longer calls CMC an exchange.
html = io.open(P, encoding='utf-8').read()
FIXES = [
('— and for the first time in the fade file&rsquo;s life the stale 68.5 December mid sits UNDER fair (−0.54). No badge flips:',
 '— and the stale 68.5 December mid slips UNDER fair (−0.54), the fade&rsquo;s first sign-flip since the Sep 16 walk. No badge flips:'),
('— and for the first time in the fade file&rsquo;s life the stale 68.5 December mid sits UNDER fair (−0.54).',
 '— and the stale 68.5 December mid slips UNDER fair (−0.54): the fade&rsquo;s sign flips for the first time since the Sep 16 walk (+10.6 → +8.8 → +6.0 → +2.5 → −0.5 at the mid).'),
('<strong>Sep 21 23:3xZ PM: the close pushes the December leader UNDER its own fair for the first time — dec-NVDA 68.5 stale mid vs 69.04 (−0.54), dec-AAPL eases to −2.01',
 '<strong>Sep 21 23:3xZ PM: the close pushes the stale December mid UNDER the leader&rsquo;s fair — dec-NVDA 68.5 vs 69.04 (−0.54), the fade&rsquo;s first sign-flip since the Sep 16 walk (+10.6 → +8.8 → +6.0 → +2.5 → −0.5 at the mid); dec-AAPL eases to −2.01'),
('dec-NVDA&rsquo;s stale 68.5 mid slips UNDER fair (−0.54) for the first time. · ',
 'dec-NVDA&rsquo;s stale 68.5 mid slips UNDER fair (−0.54), the fade&rsquo;s first sign-flip since the Sep 16 walk. · '),
('The stale 68.5 dec-NVDA mid sits UNDER the 69.04 fair — the fade file&rsquo;s first such print;',
 'The stale 68.5 dec-NVDA mid sits UNDER the 69.04 fair — the fade&rsquo;s first sign-flip since the Sep 16 walk (+10.6 → +8.8 → +6.0 → +2.5 → −0.5 at the mid);'),
('the stale 68.5 dec-NVDA mid sits UNDER fair for the first time, no badge flips,',
 'the stale 68.5 dec-NVDA mid sits UNDER fair (the fade&rsquo;s first sign-flip since the Sep 16 walk), no badge flips,'),
('for the first time in the fade file&rsquo;s life the model would not sell this book at its own touch',
 'for the first time since the Sep 16 walk the model would not sell this book at its own touch'),
('the Bitcoin tab&rsquo;s Sep 1 bake now carries a resolved rung.', 'the Bitcoin tab&rsquo;s Sep 1 bake now carries a touched rung.'),
('— the ladder&rsquo;s first up-rung resolution of the series, on a tab still wearing ', '— the ladder&rsquo;s first up-rung touch of the series, on a tab still wearing '),
('day high $87,330: the ladder&rsquo;s first up-rung resolution, every surviving-rung residual', 'day high $87,330: the ladder&rsquo;s first up-rung touch, every surviving-rung residual'),
('as snapshot-stale — the morning&rsquo;s roles exactly reversed; wire:', 'as snapshot-stale — the morning&rsquo;s discard pattern reversed, tonight&rsquo;s live reads being the aggregator and Coinbase; wire:'),
]
_applied = 0
for _o, _n in FIXES:
    c = html.count(_o)
    if c == 1:
        html = html.replace(_o, _n, 1); _applied += 1
    else:
        assert _n in html, f'review fix neither pending nor applied: {_o[:80]}'
if _applied:
    io.open(P, 'w', encoding='utf-8').write(html)
print(f'review fixes: {_applied} applied (rest already present)')
