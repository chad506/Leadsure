#!/usr/bin/env python3
"""Sep 17 PM bake — re-mark the Largest-Company tab on the Sep 17 closes.
Fairs from scripts/verify_sep17pm.py (calibration reproduced every Sep 16 PM fair
exactly). Ladders = the unchanged Sep 16 01:45Z walk (TWO sessions behind, disclosed).
Every replacement asserts exactly one occurrence."""
import sys

P = 'polymarket/index.html'
html = open(P).read()
n0 = len(html)
R = []  # (old, new)

def rep(old, new):
    R.append((old, new))

# ---------- A. hero ----------
rep('id="hero-lead-cap">$5.176T<', 'id="hero-lead-cap">$5.308T<')
rep('id="hero-chal-cap">$4.882T<', 'id="hero-chal-cap">$4.950T<')
rep('id="hero-gap">6.03% · $294B<', 'id="hero-gap">7.24% · $358B<')
rep('The tape (caps = the Sep 16 finals, re-confirmed to the cent at the Sep 17 13:2xZ AM pass — no revisions · equity mids = the <strong>Sep 16 01:45Z interactive walk, one session behind tonight&rsquo;s close — re-check the touch before acting</strong> · autodata DOWN — no cloud book walk · every fair reproduced exactly at the AM pass)',
    'The tape (caps = the Sep 17 closes, history pages ~23:2xZ — the Sep 12 lesson applies, tomorrow&rsquo;s pass re-verifies · equity mids = the <strong>Sep 16 01:45Z interactive walk, TWO sessions behind tonight&rsquo;s close — re-check the touch before acting</strong> · autodata DOWN — no cloud book walk)')

HERO_NEW = ('<strong>SEP 17 23:2xZ PM: THE RISK-ON CLOSE RE-WIDENS THE LEAD — AND THE CROWN HOLD MARKS AT FAIR.</strong> '
 'Thursday delivered what the premarket promised: all five names closed green — NVDA <strong>+2.54% ($219.34, $5,308.0B)</strong> with AMZN +2.13% ($2,702.1B), MSFT +1.50% ($3,696.8B), AAPL +1.38% ($337.00, $4,949.6B), GOOGL +1.30% ($4,228.6B) — the lead re-widens 6.03% → <strong>7.24% / $358.4B</strong> (premarket implied 7.69%; the widest close since the Sep 11 melt-up finals&rsquo; 8.25%), Apple&rsquo;s #2 cushion 17.05% / $721.1B, T <strong>9 / 73</strong>. '
 'Calibration first (every AM fair reproduced exactly), then fresh fairs: Dec <strong>62.51 / 31.93 / 4.40 / 0.42</strong>, crown <strong>87.80 / 12.20</strong>, seat 87.37-AAPL / 12.19-NVDA, 3rd 98.30-GOOGL / 1.25-MSFT; P(±5/wk) 61 / 59 / 4. '
 'Against the 01:45Z walk&rsquo;s own mids (now TWO sessions behind — re-check the touch): <strong>dec-AAPL 23.85 vs 31.93 = −8.08 CHEAP, RV 1.34× — Best Bets #1 stands, narrower: $2,090 at or under fair, $1,244 inside fair−5</strong>; '
 '<strong>the Apple-crown HOLD loses its edge — 12.6 vs a 12.20 fair is +0.40: the CHEAP badge comes off, the ADD stays dead, and the 22,532-sh position becomes a resolution ride</strong>; '
 'crownNVDA swings to −0.65 (a hair under fair), the seat goes quiet (sep2AAPL −2.87, sep2NVDA flips over fair at +0.76); sep3GOOGL prints the pass&rsquo;s one new mid-CHEAP (−5.30 on a 92 / 94 book, $0 inside fair−5 — not actionable); '
 'dec-NVDA <strong>+5.99 RICH by a whisker</strong> (NO fair 37.49, $981 of NO-dollars at bids ≥ fair — still no ticket under the catalyst clause); the sep3MSFT sell leg strengthens again (4.5¢ bid vs a 1.25 fair, RV 0.28×). '
 '<em>The AM and earlier text follows, kept for the record; where it conflicts with the above, the above is current.</em> ')
rep('data-longform-label="More"><strong>SEP 17 13:2xZ AM (pre-open): the finals lock clean.</strong>',
    'data-longform-label="More">' + HERO_NEW + '<strong>SEP 17 13:2xZ AM (pre-open): the finals lock clean.</strong>')

CAT_NEW = ('<strong>Sep 17 23:2xZ PM: ten days become nine.</strong> Next close Friday Sep 18 (T 9 / 73). The chore list re-prices on tonight&rsquo;s fairs: '
 '<strong>(1) the dec-AAPL ticket STANDS — −8.03 at the walked 23.9¢ touch, RV 1.34×, $1,244 inside fair−5 ($2,090 at or under the 31.93 fair)</strong>; '
 '(2) the Apple-crown HOLD marks AT FAIR (+0.40 at the 12.6 mid) — the ADD is dead and the hold is a resolution ride; a fresh walk, not this pass, decides anything further; '
 '(3) dec-NVDA&rsquo;s fade compresses to +5.99 at the mid — one more session like this and the RICH badge follows the September three off the board; '
 'then the 61-fill ledger bake and a fresh book walk, both still owed to the next interactive pass. '
 'Autodata is DOWN a <strong>THIRTY-SIXTH</strong> feed run (the Sep 17 22:45Z cron silent, this run&rsquo;s ~23:10Z poke touching fetch/poke unanswered — the fix is still one visit to github.com/chad506/Leadsure/actions). '
 'BTC held its overnight bid ($76,542, +0.15% on the AM print, −2.39% vs the Sep 1 bake); the ladder sits inside ±4 everywhere but the $50k tail (+6.3) — the Bitcoin tab re-bake stays the outage&rsquo;s standing want. '
 '<em>AM text, kept:</em> ')
rep('<strong>Sep 17 13:2xZ AM: tonight&rsquo;s close is the catalyst.</strong>',
    CAT_NEW + '<strong>Sep 17 13:2xZ AM: tonight&rsquo;s close is the catalyst.</strong>')

# ---------- B. KPI ----------
rep('id="kpi-edge">dec-AAPL −10.29<', 'id="kpi-edge">dec-AAPL −8.08<')
rep('Best RV · Whole Complex (Sep 16 close vs 01:45Z walk)</div><div class="kpi-value">dec-AAPL 1.43×<',
    'Best RV · Whole Complex (Sep 17 close vs 01:45Z walk)</div><div class="kpi-value">dec-AAPL 1.34×<')

# ---------- C. Best Bets ----------
rep('Walk: Sep 16, 2026 · 01:45 UTC · fairs re-run on the Sep 16 closes at 23:2xZ (T 10 / 74) — touches are one session behind, re-check before acting',
    'Walk: Sep 16, 2026 · 01:45 UTC · fairs re-run on the Sep 17 closes at 23:2xZ (T 9 / 73) — touches are TWO sessions behind, re-check before acting')

rep('<strong>Sep 16 23:2xZ PM: every fair, edge, RV and $-at-fair below is re-run on the Sep 16 closes (T 10 / 74) against the SAME 01:45Z ladders — the touches are one session old. What moved: #1&rsquo;s fair eases 34.77 → 34.14 (ticket stands, the 34.4–34.5¢ wall now sits above fair); #2&rsquo;s ADD is GATED (−5.04 at the touch, the ≤13.0¢ limit no longer clears fair−5 — HOLD stands); #3&rsquo;s fade compresses to +8.32 at the bid (still RICH, still no ticket); #4 strengthens (fair 1.55); the watch row falls inside the band (−3.42 at the ask).</strong>',
    '<strong>Sep 17 23:2xZ PM: every fair, edge, RV and $-at-fair below is re-run on the Sep 17 closes (T 9 / 73) against the SAME 01:45Z ladders — the touches are now TWO sessions old. What moved: the all-green close re-widened the lead to 7.24%, so every NVIDIA leg rose and every Apple leg fell — #1&rsquo;s fair eases 34.14 → 31.93 (ticket stands at −8.03, RV 1.34×); #2&rsquo;s edge is GONE (+0.40 at the 12.6 mid — CHEAP badge off, ADD dead, the HOLD is a resolution ride); #3&rsquo;s fade compresses to +5.49 at the bid (RICH by a whisker at the mid, still no ticket); #4 strengthens again (fair 1.25); the watch row flips over fair (+2.11 at the ask).</strong>')

# --- row #1 dec-AAPL ---
rep('data-bb-touch="dec-AAPL">23.9¢</td>\n                <td class="col-num">34.14%</td>\n                <td class="col-num pm-pos">−10.24</td>\n                <td class="col-num pm-pos">1.43× (1.43×)</td>\n                <td class="col-num">$1,774 <span class="pm-note">inside fair−5 · $3,831 ≤ fair — the 34.4–34.5¢ wall ($37.9k) now sits ABOVE the 34.14 fair and no longer counts</span></td>',
    'data-bb-touch="dec-AAPL">23.9¢</td>\n                <td class="col-num">31.93%</td>\n                <td class="col-num pm-pos">−8.03</td>\n                <td class="col-num pm-pos">1.34× (1.34×)</td>\n                <td class="col-num">$1,244 <span class="pm-note">inside fair−5 (26.93) · $2,090 ≤ fair — the 34.4–34.5¢ wall stays above fair and does not count</span></td>')
rep('$625 at the 23.9¢ touch (2,616 sh) · $1,018 ≤ 25¢ · $1,774 ≤ 29.14¢',
    '$625 at the 23.9¢ touch (2,616 sh) · $1,018 ≤ 25¢ · $1,244 ≤ 26.93¢')
rep('23.9¢ × 1,255 sh (touch one session old — re-check)', '23.9¢ × 1,255 sh (touch two sessions old — re-check)')
rep('the fair is the most robust number on the tab: 31.5 / 34.1 / 35.0 / 34.9 at σ 1.5 / 2 / 2.5 / 3%/day',
    'the fair is the most robust number on the tab: 28.4 / 31.9 / 33.3 / 33.7 at σ 1.5 / 2 / 2.5 / 3%/day')
rep('The market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 0.95%/day to be right — or, at σ 2%, an expected <strong>≈+6% NVIDIA-over-Apple drift</strong> to Dec 31',
    'The market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 1.17%/day to be right — or, at σ 2%, an expected <strong>≈+4.6% NVIDIA-over-Apple drift</strong> to Dec 31')
rep('74 trading days for a 6.03% gap.', '73 trading days for a 7.24% gap.')

# --- row #2 Apple crown ---
rep('<td><span class="pm-badge pm-cheap">#2</span></td>', '<td><span class="pm-badge pm-fair">#2</span></td>')
rep('data-bb-touch="sep-crownAAPL">12.7¢</td>\n                <td class="col-num">17.74%</td>\n                <td class="col-num pm-pos">−5.04</td>\n                <td class="col-num pm-pos">1.40× (1.41×)</td>\n                <td class="col-num">$3,054</td>',
    'data-bb-touch="sep-crownAAPL">12.7¢</td>\n                <td class="col-num">12.20%</td>\n                <td class="col-num">+0.50</td>\n                <td class="col-num">0.96× (0.97×)</td>\n                <td class="col-num">$0</td>')
rep('<td><span class="pm-badge pm-fair">OK</span> <span class="pm-note">$59 at 12.7 — the only level inside fair−5 (12.74) · twin: NVIDIA-crown NO at 13.0¢ (RV 1.37× on the 17.75 NO-fair; $5,605 YES-notional of bids ≥ the 82.25 fair)</span></td>',
    '<td><span class="pm-badge pm-watch">AT FAIR</span> <span class="pm-note">$0 of asks at or under the 12.20 fair · twin: NVIDIA-crown 87.15 mid vs an 87.80 fair (−0.65) — the pair now prices the crown almost exactly</span></td>')
rep('<td><strong>HOLD the 22,532 sh (5.86¢ avg, +$1,518 open) — the ADD is GATED tonight:</strong> the ≤13.0¢ limit no longer clears fair−5 (17.74 − 5 = 12.74), and the walked book holds only $59 at or under 12.7¢ — under the $100 cap, so NOT ACTIONABLE on this book; re-arm only if a fresh walk prints a touch ≤ 12.7¢. <strong>Exit is by resolution only:</strong> the bid ladder takes 1,295 sh at 10¢ or better and ≈$892 for the whole position — the $2,839 mark is not a liquidation value; that, not RV, is why there is no trim.</td>',
    '<td><strong>HOLD the 22,532 sh (5.86¢ avg, +$1,518 open) — the edge is GONE tonight:</strong> the close cut the crown fair 17.74 → 12.20 (the lead re-widened to 7.24%), so the 12.6 mid sits +0.40 ABOVE fair — there is no price on this book the model would pay, and the ADD is dead (was gated). <strong>Exit is by resolution only:</strong> the bid ladder takes 1,295 sh at 10¢ or better and ≈$892 for the whole position — the $2,839 mark is not a liquidation value; that, not RV, is why there is no trim. Re-decide only on a fresh walk.</td>')
rep('<td>Still a strong multiple — but the close cut the crown fair 20.94 → 17.74 (NVIDIA re-widened the lead to 6.03%), it is already the tab&rsquo;s biggest position, and the number is the least robust here: 10.9 / 17.7 / 22.9 / 26.7 across the same σ sweep (break-even σ ≈1.6%/day, or a +1.5% NVIDIA-over-Apple drift in ten sessions at σ 2%). Ten trading days for a 6.03% gap: a coin the model calls 17.7% and the market 12.6.</td>',
    '<td>The rank is history, not edge: tonight is the first close of the outage where the tab&rsquo;s biggest position marks AT its model fair — 12.20 vs the 12.6 mid, a coin the model and the market now price the same. The number is still the least robust here: 6.0 / 12.2 / 17.6 / 21.8 across the same σ sweep — at σ 2.5%/day the hold is cheap again, at σ 1.5% it is twice rich. Nine trading days for a 7.24% gap; the position rides to resolution because the exit bid, not the model, says so.</td>')

# --- row #3 dec-NVDA NO ---
rep('<td class="col-num">59.68% <span class="pm-note">(NO 40.32)</span></td>', '<td class="col-num">62.51% <span class="pm-note">(NO 37.49)</span></td>')
rep('<td class="col-num">+8.32 <span class="pm-note">(mid +8.82)</span></td>', '<td class="col-num">+5.49 <span class="pm-note">(mid +5.99)</span></td>')
rep('<td class="col-num">NO 1.26× (1.28×)</td>', '<td class="col-num">NO 1.17× (1.19×)</td>')
rep('<td class="col-num">$1,177 NO <span class="pm-note">NO-dollars ≤ the 40.32 NO-fair ($2,185 YES-notional of bids ≥ 59.68)</span></td>',
    '<td class="col-num">$981 NO <span class="pm-note">NO-dollars ≤ the 37.49 NO-fair ($1,887 YES-notional of bids ≥ 62.51)</span></td>')
rep('(≈310 sh over two levels, VWAP 32.2¢); tonight&rsquo;s close compressed the fade a fifth (fair 57.90 → 59.68).',
    '(≈310 sh over two levels, VWAP 32.2¢); tonight&rsquo;s close compressed the fade again (fair 59.68 → 62.51 — the RICH print survives by 0.99 at the mid).')
rep('because NO also pays on the Alphabet/Microsoft legs the model prices at 5.4 combined.',
    'because NO also pays on the Alphabet/Microsoft legs the model prices at 4.8 combined.')

# --- row #4 sep3MSFT ---
rep('data-bb-touch="sep-sep3MSFT">4.5¢ bid</td>\n                <td class="col-num">1.55%</td>\n                <td class="col-num">+2.95</td>\n                <td class="col-num">0.34× (0.34×) <span class="pm-note">YES side held; the NO side handed to the buyer is 1.03×</span></td>\n                <td class="col-num">$93</td>',
    'data-bb-touch="sep-sep3MSFT">4.5¢ bid</td>\n                <td class="col-num">1.25%</td>\n                <td class="col-num">+3.25</td>\n                <td class="col-num">0.28× (0.27×) <span class="pm-note">YES side held; the NO side handed to the buyer is 1.03×</span></td>\n                <td class="col-num">$100</td>')
rep('Microsoft needs to pass Alphabet (12.7% below it) in ten sessions — and MSFT was the board&rsquo;s worst close tonight (−1.37%).',
    'Microsoft needs to pass Alphabet (12.6% below it) in nine sessions — tonight both closed green (MSFT +1.50%, GOOGL +1.30%) and the gap barely moved.')
rep('the only held leg on the tab priced at 0.34× its model value with a bid that takes all of it — the close cut the fair 2.62 → 1.55, so the sell strengthens.',
    'the only held leg on the tab priced at 0.28× its model value with a bid that takes all of it — the close cut the fair again (1.55 → 1.25), so the sell strengthens a third straight session.')

# --- watch row sep2NVDA ---
rep('data-bb-touch="sep-sep2NVDA">14.3¢</td>\n                <td class="col-num">17.72%</td>\n                <td class="col-num pm-pos">−3.42</td>\n                <td class="col-num pm-pos">1.24× (1.37×)</td>\n                <td class="col-num">$58</td>',
    'data-bb-touch="sep-sep2NVDA">14.3¢</td>\n                <td class="col-num">12.19%</td>\n                <td class="col-num">+2.11</td>\n                <td class="col-num">0.85× (0.94×)</td>\n                <td class="col-num">$0</td>')
rep('11.6 / 14.3 — $58 of asks at or under the 17.72 fair', '11.6 / 14.3 — $0 of asks at or under the 12.19 fair')
rep('<strong>No ticket — and the case weakened:</strong> tonight&rsquo;s close pulls the fair to 17.72, so the ask-side edge is −3.42, inside the band.',
    '<strong>No ticket — the case DIED tonight:</strong> the close pulls the fair to 12.19, UNDER the 14.3¢ ask (+2.11) — there is no price on this book the model would pay.')
rep('Listed so nobody buys it thinking it is a second idea: NVIDIA finishing 2nd ≈ Apple finishing 1st (17.72 vs 17.74). The seat&rsquo;s other side — sep2AAPL 84.5 vs 81.60, +2.90 — fell inside the band tonight too: the fade candidacy dies on its own fair, not just the arming rule ($126 sits at 81–82 against the ≥$300 bar).',
    'Listed so nobody buys it thinking it is a second idea: NVIDIA finishing 2nd ≈ Apple finishing 1st (12.19 vs 12.20). The seat&rsquo;s other side — sep2AAPL 84.5 vs 87.37, −2.87 — sits inside the band from below: both seat legs are quiet, and the walked 82 / 87 spread is wider than either edge.')

# --- honesty line ---
rep('(6.03% / $294.2B at the Sep 16 close)', '(7.24% / $358.4B at the Sep 17 close)')
rep('pay together only 9.7% of the time (P(Dec | Sep) 55% vs P(Dec | not Sep) 30%, payoff correlation ≈0.20)',
    'pay together only 6.6% of the time (P(Dec | Sep) 54% vs P(Dec | not Sep) 29%, payoff correlation ≈0.18)')
rep('That is why #1 (the December leg, no exposure yet, the most σ-robust fair) outranks #2 (the better multiple, the bigger existing position, the less robust fair).',
    'That is why #1 (the December leg, no exposure yet, the most σ-robust fair) outranks #2 — which tonight is not a bet at all but the book&rsquo;s biggest holding marking at fair.')
rep('(#1 at one level; #2&rsquo;s ADD no longer clears it and is gated)',
    '(#1 at one level; #2&rsquo;s ADD is dead — nothing on the walked book beats the 12.20 fair)')

# ---------- D. analysis table ----------
NOTE_NEW = ('<strong>Sep 17 23:2xZ PM: caps are the SEP 17 CLOSES (history pages, ~23:2xZ pull — the Sep 12 lesson applies, tomorrow&rsquo;s pass re-verifies; all five Sep 16 finals re-confirmed beneath them): '
 'NVDA $5,308.0B ($219.34, +2.54%, the board&rsquo;s best) / AAPL $4,949.6B ($337.00, +1.38%) / GOOGL $4,228.6B ($347.33, +1.30%) / MSFT $3,696.8B ($497.66, +1.50%) / AMZN $2,702.1B ($251.19, +2.13%) — ALL FIVE GREEN, the outage&rsquo;s first sweep; the lead re-widens 6.03% → 7.24% / $358.4B, the cushion 17.05%; T = 9 / 73. '
 'Every fair, edge, RV, verdict and tradeable-at-fair below re-ran on these closes (calibration reproduced every Sep 16 PM fair exactly) against the UNCHANGED Sep 16 01:45Z walk mids — now TWO sessions behind, re-check the touch. '
 'What moved: the Apple-crown CHEAP comes off (+0.40 — the hold marks at fair), sep3GOOGL prints a new mid-CHEAP (−5.30 on a 92 / 94 book, $0 inside fair−5 — not actionable), dec-AAPL −8.08 CHEAP (RV 1.34×) stands, dec-NVDA compresses to +5.99 RICH.</strong> '
 '· <em>The Sep 16 PM note follows, kept — its caps, fairs and T counts are superseded above:</em> ')
rep('<strong>Sep 16 23:2xZ PM: caps are the SEP 16 CLOSES', NOTE_NEW + '<strong>Sep 16 23:2xZ PM: caps are the SEP 16 CLOSES')

SEPGRP_NEW = ('SEPTEMBER 30 · T = 9 trading days · <strong>Sep 17 23:2xZ PM: fairs re-run on the Sep 17 closes — the all-green sweep (lead 7.24%) hands the partition further to NVIDIA: '
 'crown 87.80 / 12.20 (Apple&rsquo;s leg +0.40 vs the 12.6 walked mid — the CHEAP badge comes off, the Best Bets #2 ADD is dead), seat 87.37 / 12.19 (sep2NVDA flips over fair, +0.76), 3rd 98.30-GOOGL / 1.25-MSFT — '
 'sep3GOOGL −5.30 mid-CHEAP on a 92 / 94 book ($0 inside fair−5, not actionable), sep3MSFT&rsquo;s sell strengthens (4.55 vs 1.25, RV 0.27×)</strong> · <em>the Sep 16 PM text, kept:</em> <strong>Sep 16 23:2xZ PM:')
rep('SEPTEMBER 30 · T = 10 trading days · <strong>Sep 16 23:2xZ PM:', SEPGRP_NEW)

DECGRP_NEW = ('DECEMBER 31 — 73 TRADING DAYS · <strong>Sep 17 23:2xZ PM: fairs re-run on the Sep 17 closes against the unchanged 01:45Z walk mids (two sessions behind) — '
 'dec-AAPL 23.85 vs 31.93 = −8.08 CHEAP (RV 1.34×; $2,090 at or under fair, $1,244 inside fair−5 — the 34.4–34.5¢ wall stays above fair), '
 'dec-NVDA 68.5 vs 62.51 = +5.99 RICH by a whisker ($1,887 YES-notional of bids ≥ fair = $981 of NO-dollars; NO fair 37.49 — Best Bets #3, still no ticket), '
 'dec-GOOGL +2.10 and dec-MSFT +0.13 inside the band</strong> · <em>the Sep 16 PM text, kept:</em> <strong>Sep 16 23:2xZ PM:')
rep('DECEMBER 31 — 74 TRADING DAYS · <strong>Sep 16 23:2xZ PM:', DECGRP_NEW)

# --- caps + gaps ---
rep('data-cap="NVDA-sep">5,176.4<', 'data-cap="NVDA-sep">5,308.0<')
rep('data-cap="AAPL-sep">4,882.2<', 'data-cap="AAPL-sep">4,949.6<')
rep('data-gap="AAPL-sep">−5.68%<', 'data-gap="AAPL-sep">−6.75%<')
rep('data-cap="NVDA-dec">5,176.4<', 'data-cap="NVDA-dec">5,308.0<')
rep('data-cap="AAPL-dec">4,882.2<', 'data-cap="AAPL-dec">4,949.6<')
rep('data-gap="AAPL-dec">−5.68%<', 'data-gap="AAPL-dec">−6.75%<')
rep('data-cap="GOOGL-dec">4,174.3<', 'data-cap="GOOGL-dec">4,228.6<')
rep('data-gap="GOOGL-dec">−19.36%<', 'data-gap="GOOGL-dec">−20.34%<')
rep('data-cap="MSFT-dec">3,642.2<', 'data-cap="MSFT-dec">3,696.8<')
rep('data-gap="MSFT-dec">−29.64%<', 'data-gap="MSFT-dec">−30.35%<')
rep('data-cap="AMZN-dec">2,645.8<', 'data-cap="AMZN-dec">2,702.1<')
rep('data-gap="AMZN-dec">−48.89%<', 'data-gap="AMZN-dec">−49.09%<')

# --- 14 model rows: fair/edge/RV/$/verdict chunks ---
rep('data-fair="sep-crownNVDA">82.25%</td><td class="col-num" data-edge="sep-crownNVDA">+4.90</td><td class="col-num" data-pm-rv>0.94×</td><td class="col-num"><span class="pm-badge pm-fair">$5,605</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-crownNVDA">FAIR</span> <span class="pm-note">RICH badge off — +4.90</span></td>',
    'data-fair="sep-crownNVDA">87.80%</td><td class="col-num" data-edge="sep-crownNVDA">−0.65</td><td class="col-num" data-pm-rv>1.01×</td><td class="col-num"><span class="pm-badge pm-fair">$2,531</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-crownNVDA">FAIR</span> <span class="pm-note">first sub-fair print since the walk — −0.65</span></td>')
rep('data-fair="sep-crownAAPL">17.74%</td><td class="col-num" data-edge="sep-crownAAPL">−5.14</td><td class="col-num pm-pos" data-pm-rv>1.41×</td><td class="col-num"><span class="pm-badge pm-cheap">$3,054</span></td><td><span class="pm-badge pm-cheap" data-verdict="sep-crownAAPL">CHEAP</span> <span class="pm-note">by 0.14 — ADD gated</span></td>',
    'data-fair="sep-crownAAPL">12.20%</td><td class="col-num" data-edge="sep-crownAAPL">+0.40</td><td class="col-num" data-pm-rv>0.97×</td><td class="col-num"><span class="pm-badge pm-fair">$24</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-crownAAPL">FAIR</span> <span class="pm-note">CHEAP badge off — the 22,532-sh hold marks at fair</span></td>')
rep('data-fair="sep-sep2AAPL">81.60%</td><td class="col-num" data-edge="sep-sep2AAPL">+2.90</td><td class="col-num" data-pm-rv>0.97×</td><td class="col-num"><span class="pm-badge pm-fair">$16</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep2AAPL">FAIR</span> <span class="pm-note">82 / 87 — WIDE · RICH badge off</span></td>',
    'data-fair="sep-sep2AAPL">87.37%</td><td class="col-num" data-edge="sep-sep2AAPL">−2.87</td><td class="col-num" data-pm-rv>1.03×</td><td class="col-num"><span class="pm-badge pm-fair">$27</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep2AAPL">FAIR</span> <span class="pm-note">82 / 87 — WIDE</span></td>')
rep('data-fair="sep-sep2NVDA">17.72%</td><td class="col-num" data-edge="sep-sep2NVDA">−4.77</td><td class="col-num pm-pos" data-pm-rv>1.37×</td><td class="col-num"><span class="pm-badge pm-watch">$58</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep2NVDA">FAIR</span> <span class="pm-note">THIN · 11.6 / 14.3 · CHEAP badge off</span></td>',
    'data-fair="sep-sep2NVDA">12.19%</td><td class="col-num" data-edge="sep-sep2NVDA">+0.76</td><td class="col-num" data-pm-rv>0.94×</td><td class="col-num"><span class="pm-badge pm-watch">$0</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep2NVDA">FAIR</span> <span class="pm-note">THIN · 11.6 / 14.3 · flipped over fair</span></td>')
rep('data-fair="sep-sep2GOOGL">0.68%</td><td class="col-num" data-edge="sep-sep2GOOGL">+0.97</td><td class="col-num" data-pm-rv>0.41×</td><td class="col-num"><span class="pm-badge pm-fair">$5</span></td>',
    'data-fair="sep-sep2GOOGL">0.44%</td><td class="col-num" data-edge="sep-sep2GOOGL">+1.21</td><td class="col-num" data-pm-rv>0.27×</td><td class="col-num"><span class="pm-badge pm-fair">$10</span></td>')
rep('data-fair="sep-sep3GOOGL">97.76%</td><td class="col-num" data-edge="sep-sep3GOOGL">−4.76</td><td class="col-num" data-pm-rv>1.05×</td><td class="col-num"><span class="pm-badge pm-fair">$21,963</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep3GOOGL">FAIR</span></td>',
    'data-fair="sep-sep3GOOGL">98.30%</td><td class="col-num" data-edge="sep-sep3GOOGL">−5.30</td><td class="col-num" data-pm-rv>1.06×</td><td class="col-num"><span class="pm-badge pm-fair">$28,148</span></td><td><span class="pm-badge pm-cheap" data-verdict="sep-sep3GOOGL">CHEAP</span> <span class="pm-note">92 / 94 WIDE — the 94.0 ask is −4.30, inside the band; $0 inside fair−5: a spread artifact, not a ticket</span></td>')
rep('data-fair="sep-sep3MSFT">1.55%</td><td class="col-num" data-edge="sep-sep3MSFT">+3.00</td><td class="col-num" data-pm-rv>0.34×</td><td class="col-num"><span class="pm-badge pm-fair">$93</span></td>',
    'data-fair="sep-sep3MSFT">1.25%</td><td class="col-num" data-edge="sep-sep3MSFT">+3.30</td><td class="col-num" data-pm-rv>0.27×</td><td class="col-num"><span class="pm-badge pm-fair">$100</span></td>')
rep('data-fair="sep-sep3AAPL">0.66%</td><td class="col-num" data-edge="sep-sep3AAPL">+0.94</td><td class="col-num" data-pm-rv>0.41×</td><td class="col-num"><span class="pm-badge pm-fair">$14</span></td>',
    'data-fair="sep-sep3AAPL">0.43%</td><td class="col-num" data-edge="sep-sep3AAPL">+1.17</td><td class="col-num" data-pm-rv>0.27×</td><td class="col-num"><span class="pm-badge pm-fair">$16</span></td>')
rep('data-fair="sep-sep3NVDA">0.03%</td><td class="col-num" data-edge="sep-sep3NVDA">+0.22</td><td class="col-num" data-pm-rv>0.12×</td>',
    'data-fair="sep-sep3NVDA">0.01%</td><td class="col-num" data-edge="sep-sep3NVDA">+0.24</td><td class="col-num" data-pm-rv>0.04×</td>')
rep('data-fair="dec-NVDA">59.68%</td><td class="col-num" data-edge="dec-NVDA">+8.82</td><td class="col-num" data-pm-rv>0.87×</td><td class="col-num"><span class="pm-badge pm-rich">$2,185</span></td>',
    'data-fair="dec-NVDA">62.51%</td><td class="col-num" data-edge="dec-NVDA">+5.99</td><td class="col-num" data-pm-rv>0.91×</td><td class="col-num"><span class="pm-badge pm-rich">$1,887</span></td>')
rep('data-fair="dec-AAPL">34.14%</td><td class="col-num" data-edge="dec-AAPL">−10.29</td><td class="col-num pm-pos" data-pm-rv>1.43×</td><td class="col-num"><span class="pm-badge pm-cheap">$3,831</span> <span class="pm-note">$1,774 ≤ fair−5 · the 34.4–34.5¢ wall sits above fair</span></td><td><span class="pm-badge pm-cheap" data-verdict="dec-AAPL">CHEAP</span></td><td class="col-num">60%</td>',
    'data-fair="dec-AAPL">31.93%</td><td class="col-num" data-edge="dec-AAPL">−8.08</td><td class="col-num pm-pos" data-pm-rv>1.34×</td><td class="col-num"><span class="pm-badge pm-cheap">$2,090</span> <span class="pm-note">$1,244 ≤ fair−5 · the 34.4–34.5¢ wall sits above fair</span></td><td><span class="pm-badge pm-cheap" data-verdict="dec-AAPL">CHEAP</span></td><td class="col-num">59%</td>')
rep('data-fair="dec-GOOGL">4.95%</td><td class="col-num" data-edge="dec-GOOGL">+1.55</td><td class="col-num" data-pm-rv>0.76×</td><td class="col-num"><span class="pm-badge pm-fair">$734</span></td><td><span class="pm-badge pm-fair" data-verdict="dec-GOOGL">FAIR</span></td><td class="col-num">5%</td>',
    'data-fair="dec-GOOGL">4.40%</td><td class="col-num" data-edge="dec-GOOGL">+2.10</td><td class="col-num" data-pm-rv>0.68×</td><td class="col-num"><span class="pm-badge pm-fair">$734</span></td><td><span class="pm-badge pm-fair" data-verdict="dec-GOOGL">FAIR</span></td><td class="col-num">4%</td>')
rep('data-fair="dec-MSFT">0.48%</td><td class="col-num" data-edge="dec-MSFT">+0.07</td><td class="col-num" data-pm-rv>0.87×</td>',
    'data-fair="dec-MSFT">0.42%</td><td class="col-num" data-edge="dec-MSFT">+0.13</td><td class="col-num" data-pm-rv>0.76×</td>')
# dec-AMZN edge +0.15 / RV 0.00 unchanged

FOOT_NEW = ('<strong>Sep 17 23:2xZ PM — the all-green sweep re-widens the lead.</strong> Thursday&rsquo;s closes (history pages, ~23:2xZ — the Sep 12 lesson applies, the next pass re-verifies; all five Sep 16 finals re-confirmed beneath them to the cent): '
 'the outage&rsquo;s first all-green board — NVDA <strong>+2.54% to $219.34 ($5,308.0B), the board&rsquo;s best</strong>, AMZN +2.13% ($2,702.1B), MSFT +1.50% ($3,696.8B), AAPL +1.38% ($337.00, $4,949.6B), GOOGL +1.30% ($4,228.6B) — '
 'the lead re-widens 6.03% → <strong>7.24% / $358.4B, the widest close since the Sep 11 melt-up finals</strong> (a third consecutive re-widening close), the cushion 17.05% / $721.1B, T <strong>9 / 73</strong>. '
 'Calibration first (the quadrature reproduces every Sep 16 PM fair exactly), then fresh fairs: Dec <strong>62.51 / 31.93 / 4.40 / 0.42 / 0.00</strong>; crown <strong>87.80 / 12.20 / 0.00</strong>; seat <strong>87.37-AAPL / 12.19-NVDA / 0.44-GOOGL</strong>; 3rd <strong>98.30-GOOGL / 1.25-MSFT / 0.43-AAPL / 0.01-NVDA</strong>; P(±5/wk) <strong>61 / 59 / 4</strong>. '
 'The mids are the UNCHANGED Sep 16 01:45Z walk (no fresh books from a scheduled session — autodata down a 36th feed run), so every edge is fresh-fair-vs-a-TWO-session-old touch: '
 '<strong>dec-AAPL −8.08 CHEAP (RV 1.34×) — the ticket stands, narrower: $2,090 at or under the 31.93 fair, $1,244 inside fair−5</strong>; '
 '<strong>dec-NVDA compresses to +5.99 RICH — the leader&rsquo;s badge survives by 0.99</strong> (bids ≥ fair $1,887 YES-notional / $981 NO-dollars); '
 '<strong>the Apple-crown CHEAP comes off (+0.40) — the tab&rsquo;s biggest position marks AT its model fair for the first time in the outage</strong>: the ADD is dead and the hold rides to resolution on the exit-bid logic, not the model; '
 'sep2NVDA flips over fair (+0.76); sep3GOOGL prints −5.30 mid-CHEAP on a 92 / 94 book ($0 inside fair−5 — the 94.0 ask is −4.30, inside the band: a spread artifact, not a ticket); '
 'sep3MSFT&rsquo;s sell leg strengthens a third straight session (fair 1.55 → 1.25, RV 0.27×). '
 '<em>The Sep 16 PM text follows, kept for the record — its caps, fairs, T counts and depth figures are superseded above.</em> ')
rep('<strong>Sep 16 23:2xZ PM — the close re-deals the fairs.</strong>', FOOT_NEW + '<strong>Sep 16 23:2xZ PM — the close re-deals the fairs.</strong>')

# ---------- E. Top Trades #1 pointer ----------
rep('fair 34.14 at the Sep 16 PM re-run — the ticket stands', 'fair 31.93 at the Sep 17 PM re-run — the ticket stands')
rep('<strong>Sep 16 23:2xZ PM:</strong> the Sep 16 close eases the fair 34.77 → 34.14',
    '<strong>Sep 17 23:2xZ PM:</strong> the all-green close re-widens the lead to 7.24% and eases the fair again, 34.14 → 31.93 — the ticket STANDS a third session: −8.03 at the walked 23.9¢ touch (now two sessions old), RV 1.34×, $1,244 inside fair−5, $2,090 at or under fair; the σ-band holds 28.4–33.7 across 1.5–3%/day. <strong>Sep 16 23:2xZ PM:</strong> the Sep 16 close eases the fair 34.77 → 34.14')

# ---------- F. header tape append ----------
TAPE_NEW = (' · <strong>Sep 17 23:2xZ — THE THURSDAY CLOSE RE-WIDENS THE LEAD, THE CROWN HOLD MARKS AT FAIR:</strong> autodata is down a <strong>THIRTY-SIXTH</strong> consecutive feed run (the Sep 17 22:45Z cron silent; this run&rsquo;s ~23:10Z poke touching fetch/poke unanswered — the Actions disablement stands). '
 'Caps-only on the Sep 17 closes (history pages ~23:2xZ; all five Sep 16 finals re-confirmed beneath them): the outage&rsquo;s first all-green board — NVDA +2.54% ($219.34, $5,308.0B) leads AMZN +2.13%, MSFT +1.50%, AAPL +1.38% ($4,949.6B), GOOGL +1.30% — <strong>the lead re-widens 6.03% → 7.24% / $358.4B, the widest close since the Sep 11 melt-up finals</strong>; cushion 17.05% / $721.1B, T 9 / 73. '
 'Calibration first, then fresh fairs: Dec 62.51 / 31.93 / 4.40 / 0.42, crown 87.80 / 12.20, seat 87.37 / 12.19, 3rd 98.30 / 1.25; P(±5/wk) 61 / 59 / 4. '
 'Against the unchanged Sep 16 01:45Z walk mids (TWO sessions behind): <strong>dec-AAPL −8.08 CHEAP RV 1.34× — Best Bets #1 stands, narrower ($1,244 inside fair−5)</strong>; <strong>the Apple-crown CHEAP comes off (+0.40 at the 12.6 mid) — the ADD is dead, the 22,532-sh HOLD becomes a resolution ride</strong>; dec-NVDA +5.99 RICH by a whisker (NO-dollars $981, still no ticket); sep2NVDA flips over fair; sep3GOOGL −5.30 on a 92 / 94 book ($0 inside fair−5 — not actionable); sep3MSFT&rsquo;s sell strengthens (fair 1.25, RV 0.28×). '
 'BTC color: spot $76,541.77 (CoinGecko live, +0.50%/24h, range $75,602–$77,024; Coinbase live cross $76,545.18 ~0.004% over — the tightest cross of the series; <strong>Kraken re-served the AM cross to the cent — snapshot-stale, discarded, the series&rsquo; fifth rotation</strong>), +0.15% on the AM print, −2.39% vs the Sep 1 bake; T 105.2d: vs the Sep 15 walk mids the ladder pulls inside ±4 everywhere but the $50k tail ($85k +1.6, $90k −1.7, $95k −2.5, $100k −3.2, $110k −1.3, $60k −3.7, $55k +2.5, $50k +6.3; needed touch +11.1%) — labeled color, the BTC tab keeps its Sep 1 01:27Z stamps. '
 'Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.')
OLD_TAPE_END = 'the $60k dip comes back INSIDE the −5 line (−5.5 → −4.2; $90k −1.3, $95k −2.3, $100k −3.1, $110k −1.2, $55k +2.2, $50k +6.1; needed touch +11.2%) — labeled color, the BTC tab keeps its Sep 1 01:27Z stamps. Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.'
rep(OLD_TAPE_END, OLD_TAPE_END + TAPE_NEW)

# ---------- G. sync bar ----------
LATEST_NEW = ('<strong>Latest: Sep 17 23:2xZ PM pass (the Thursday close) — the outage&rsquo;s first ALL-GREEN board re-widens the lead 6.03% → 7.24% / $358.4B (NVDA +2.54% $219.34, $5,308.0B over AAPL +1.38% $337.00, $4,949.6B; the widest close since the Sep 11 melt-up finals; T 9 / 73): fresh fairs Dec 62.51 / 31.93, crown 87.80 / 12.20, seat 87.37 / 12.19, 3rd 98.30 / 1.25, P(±5/wk) 61 / 59 / 4 — against the unchanged Sep 16 01:45Z walk mids (TWO sessions behind), dec-AAPL −8.08 CHEAP RV 1.34× stands as Best Bets #1 (narrower: $1,244 inside fair−5), the Apple-crown CHEAP comes off (+0.40 — the 22,532-sh HOLD marks at fair, the ADD is dead), dec-NVDA +5.99 RICH by a whisker, sep3GOOGL −5.30 mid-CHEAP on a 92 / 94 book ($0 inside fair−5 — not actionable). BTC $76,542 (CoinGecko live; Coinbase cross $76,545 — the series&rsquo; tightest; Kraken snapshot-stale, discarded), +0.15% on the AM print; the ladder sits inside ±4 everywhere but the $50k tail (+6.3). Autodata DOWN a 36th feed run; tab bakes: Oil Sep 10, Treasuries Sep 9 close, Largest-Company fairs Sep 17 23:2xZ on the Sep 16 01:45Z walk mids, Bitcoin Sep 1, Iran Sep 1; Leaderboard re-marked Sep 15 01:10Z.</strong>')
# old Latest strong: from '<strong>Latest: Sep 17 13:2xZ AM pass' to the first '</strong>' after it
i = html.index('<strong>Latest: Sep 17 13:2xZ AM pass')
j = html.index('</strong>', i) + len('</strong>')
OLD_LATEST = html[i:j]
R.append((OLD_LATEST, LATEST_NEW))

CHRON_NEW = (' <strong>Sep 17 23:2xZ PM run (the Thursday close): the outage&rsquo;s first ALL-GREEN board — NVDA +2.54% ($219.34, $5,308.0B) leads AMZN +2.13%, MSFT +1.50%, AAPL +1.38% ($4,949.6B), GOOGL +1.30% — the lead re-widens 6.03% → 7.24% / $358.4B, the widest close since the Sep 11 melt-up finals; cushion 17.05%, T 9 / 73. Calibration reproduced every Sep 16 PM fair exactly, then fresh fairs on the Sep 17 closes: Dec 62.51 / 31.93 / 4.40 / 0.42, crown 87.80 / 12.20, seat 87.37 / 12.19, 3rd 98.30 / 1.25, P(±5/wk) 61 / 59 / 4. Against the unchanged Sep 16 01:45Z walk ladders (TWO sessions behind, disclosed on every touched surface): dec-AAPL −8.08 CHEAP RV 1.34× (#1 stands; $2,090 at or under fair, $1,244 inside fair−5), the Apple-crown CHEAP comes off (+0.40 — the hold marks at fair, the ADD is dead), dec-NVDA compresses to +5.99 RICH (NO-dollars $981; catalyst clause still gates), sep2NVDA flips over fair (+0.76), sep3GOOGL −5.30 mid-CHEAP on a 92 / 94 book ($0 inside fair−5 — not actionable), sep3MSFT&rsquo;s sell strengthens (fair 1.25). BTC $76,541.77 (CoinGecko live +0.50%/24h; Coinbase cross $76,545.18 ~0.004% over, the series&rsquo; tightest; Kraken re-served the AM cross to the cent — snapshot-stale, discarded, the fifth rotation), +0.15% on the AM print, −2.39% vs the Sep 1 bake; T 105.2d — ladder residuals inside ±4 everywhere but the $50k tail (+6.3). Autodata DOWN a THIRTY-SIXTH feed run (22:45Z cron silent; ~23:10Z poke unanswered). Balances/cards/velocity/ledgers keep their stamps (61 fills owed). No trades placed.</strong>')
rep('<span id="sync-ago"', CHRON_NEW + '<span id="sync-ago"')

# ---------- apply ----------
fails = []
for old, new in R:
    c = html.count(old)
    if c != 1:
        fails.append((c, old[:110]))
        continue
    html = html.replace(old, new, 1)
if fails:
    for c, o in fails:
        print(f"FAIL count={c}: {o}")
    sys.exit(1)
open(P, 'w').write(html)
print(f"OK — {len(R)} replacements applied; {n0} -> {len(html)} bytes")
