#!/usr/bin/env python3
"""Sep 18 PM bake — the Friday quad-witching close re-marks the Largest-Company tab.
Fairs from scripts/verify_sep18pm.py (calibration reproduced every Sep 18 AM fair
exactly). Ladders = the unchanged Sep 16 01:45Z walk (THREE sessions behind, disclosed).
Every replacement asserts exactly one occurrence."""
import sys

P = 'polymarket/index.html'
html = open(P).read()
n0 = len(html)
R = []

def rep(old, new):
    R.append((old, new))

# ---------- A. hero ----------
rep('id="hero-lead-cap">$5.308T<', 'id="hero-lead-cap">$5.379T<')
rep('id="hero-chal-cap">$4.950T<', 'id="hero-chal-cap">$4.937T<')
rep('id="hero-gap">7.24% · $358B<', 'id="hero-gap">8.95% · $442B<')
rep('The tape (caps = the Sep 17 FINALS — re-verified on the Sep 18 morning pass, MSFT revised $497.66 → $497.75 · equity mids = the <strong>Sep 16 01:45Z interactive walk, TWO sessions behind — re-check the touch before acting</strong> · autodata DOWN — no cloud book walk)',
    'The tape (caps = the Sep 18 closes, history pages ~23:1xZ — NVDA&rsquo;s own page split $222.27 header / $222.06 table, the header taken, the morning pass re-verifies · equity mids = the <strong>Sep 16 01:45Z interactive walk, THREE sessions behind — re-check the touch before acting</strong> · autodata DOWN — no cloud book walk)')

HERO_NEW = ('<strong>SEP 18 23:1xZ PM: THE QUAD-WITCHING BREAKOUT — NVIDIA RUNS THROUGH THE MELT-UP, AND THE FLAGSHIP TICKET STANDS DOWN ON ITS OWN STOP.</strong> '
 'Friday&rsquo;s expiry close (181.7M NVDA shares) went one way: NVDA <strong>+1.34% ($222.27, $5,378.9B)</strong> with AMZN +1.00% and GOOGL +0.64% ($349.54, $4,255.5B) — while AAPL fell −0.26% ($336.13, $4,936.9B) and MSFT −0.80% ($3,668.0B). '
 'The lead re-widens a FOURTH straight close, 7.24% → <strong>8.95% / $442.1B — past the Sep 11 melt-up finals&rsquo; own 8.25%, the widest since the Sep 10 close</strong>; Apple&rsquo;s #2 cushion narrows to 16.01% / $681.4B; T <strong>8 / 72</strong>. '
 '<em>NVDA source note: the history table still served $222.06 (+1.24%) at ~23:10Z while the same site&rsquo;s quote header and overview page both printed $222.27 (+1.34%) at-close with the after-hours series keyed off it — the header is taken as the working final (the Sep 12/15/18-AM lesson in reverse), and tomorrow&rsquo;s pass locks it.</em> '
 'Calibration first (every AM fair reproduced exactly), then fresh fairs: Dec <strong>65.98 / 28.69 / 4.27 / 0.30</strong>, crown <strong>93.52 / 6.48</strong>, seat 93.09-AAPL / 6.47-NVDA, 3rd 99.13-GOOGL / 0.43-MSFT; P(±5/wk) 60 / 58 / 4. '
 'Against the 01:45Z walk&rsquo;s own mids (now THREE sessions behind — the ladders predate the breakout): <strong>dec-AAPL 23.85 vs 28.69 = −4.84 — INSIDE the band: the CHEAP badge comes off and Best Bets #1 STANDS DOWN on its own written stop (retire on fair &lt; mid + 5); $0 inside fair−5</strong>; '
 '<strong>dec-NVDA&rsquo;s RICH badge comes off too (+2.52) — the whole December book is inside the band for the first time since Sep 8</strong>; '
 'the crown pair inverts: <strong>crownAAPL +6.12 RICH (the 22,532-sh hold marks 2× its model value on a stale mid)</strong> against crownNVDA −6.37 mid-CHEAP ($2,713 of asks inside fair−5), sep2AAPL −8.59 the pass&rsquo;s widest print ($805 inside fair−5), sep2NVDA +7.83, sep3GOOGL&rsquo;s 94.0 ask itself crosses the line (−5.13) — every one of those is a three-session-old ladder against a post-breakout fair: <strong>the September partition heads the re-walk queue, not the ticket queue</strong>; the sep3MSFT sell strengthens a fourth session (fair 0.43, RV 0.10×). '
 '<em>The AM and earlier text follows, kept for the record; where it conflicts with the above, the above is current.</em> ')
rep('data-longform-label="More"><strong>SEP 18 13:2xZ AM (pre-open): the morning check catches a Microsoft revision.</strong>',
    'data-longform-label="More">' + HERO_NEW + '<strong>SEP 18 13:2xZ AM (pre-open): the morning check catches a Microsoft revision.</strong>')

CAT_NEW = ('<strong>Sep 18 23:1xZ PM: the crown&rsquo;s final full week begins with every badge re-dealt.</strong> Next close Monday Sep 21 (T 8 / 72). The chore list after the breakout: '
 '<strong>(1) Best Bets #1 STANDS DOWN — its own stop fired (fair 28.69 &lt; the 23.85 mid + 5): no buy at 23.9¢; re-arm only on a fresh walk printing ≤ 23.69 or a fair back over mid+5</strong>; '
 '(2) the Apple-crown hold marks RICH (+6.12 on the stale 12.6 mid, fair 6.48) — the exit-bid reality is unchanged (≈$892 for the lot), so the position still rides to resolution, but a fresh walk decides whether the 12.4–12.5¢ bids ($275 at or over fair) are worth hitting; '
 '(3) the stale-ladder cheap trio — sep2AAPL −8.59 ($805 inside fair−5), crownNVDA −6.37 ($2,713), sep3GOOGL −5.13 at the ask ($835) — is the outage&rsquo;s first executable-looking September paper, and ALL of it is a pre-breakout book: <strong>re-walk before a dollar moves</strong>; '
 '(4) the 61-fill ledger bake and the fresh book walk, both still owed to the next interactive pass — and after tonight the <strong>Bitcoin tab re-bake outranks them all</strong>: spot broke $80k ($81,228, +4.52% on the AM print, +3.59% over the Sep 1 bake — the series&rsquo; first $80k print and strongest above-bake read) and the Sep 15 ladder mids now sit 15–18 points under fresh fairs up top ($90k −18.4, the widest residual of the series) with the dips flipped rich ($50k +9.7). '
 'Autodata is DOWN a <strong>THIRTY-EIGHTH</strong> feed run (the Sep 18 22:45Z cron silent, this run&rsquo;s ~23:09Z poke touching fetch/poke unanswered — the fix is still one visit to github.com/chad506/Leadsure/actions). '
 '<em>AM text, kept:</em> ')
rep('<strong>Sep 18 13:2xZ AM: tonight&rsquo;s close is the catalyst — the last Friday close before the Sep 30 crown&rsquo;s final week begins.</strong>',
    CAT_NEW + '<strong>Sep 18 13:2xZ AM: tonight&rsquo;s close is the catalyst — the last Friday close before the Sep 30 crown&rsquo;s final week begins.</strong>')

# ---------- B. KPI ----------
rep('id="kpi-edge">dec-AAPL −8.08<', 'id="kpi-edge">sep2AAPL −8.59<')
rep('Best RV · Whole Complex (Sep 17 close vs 01:45Z walk)</div><div class="kpi-value">dec-AAPL 1.34×<',
    'Best RV · Whole Complex (Sep 18 close vs 01:45Z walk)</div><div class="kpi-value">dec-AAPL 1.20×<')

# ---------- C. Best Bets ----------
rep('Walk: Sep 16, 2026 · 01:45 UTC · fairs re-run on the Sep 17 closes at 23:2xZ, finals re-verified Sep 18 13:1xZ (MSFT revised $497.75 — only 3rd-MSFT&rsquo;s fair moves, 1.25 → 1.26; T 9 / 73) — touches are TWO sessions behind, re-check before acting',
    'Walk: Sep 16, 2026 · 01:45 UTC · fairs re-run on the Sep 18 closes at 23:1xZ (T 8 / 72) — touches are THREE sessions behind and predate the breakout: re-walk before acting')

BB_NEW = ('<strong>Sep 18 23:1xZ PM: the quad-witching close (lead 8.95%, past the melt-up finals) re-deals every row against the SAME 01:45Z ladders — now THREE sessions old and pre-breakout. What moved: '
 '#1&rsquo;s own stop FIRED (fair 28.69 &lt; mid + 5, edge −4.84 — the ticket STANDS DOWN after three sessions; $0 inside fair−5); '
 '#2 flips from at-fair to RICH (+6.12 at the stale 12.6 mid, fair 6.48, RV 0.51× — the hold still rides to resolution on the exit-bid logic); '
 '#3&rsquo;s RICH badge comes off (+2.52 at the mid — the December book is all inside the band); '
 '#4 strengthens a fourth session (fair 0.43, RV 0.10× — the strongest sell print yet); '
 'the watch row doubles its premium (+7.83 at the ask). The stale-ladder cheap prints (sep2AAPL −8.59, crownNVDA −6.37, sep3GOOGL −5.13 at the ask) are re-walk queue, not tickets.</strong> · <em>The AM note follows, kept:</em> ')
rep('<strong>Sep 18 13:2xZ AM: the morning pass re-verified the Sep 17 finals',
    BB_NEW + '<strong>Sep 18 13:2xZ AM: the morning pass re-verified the Sep 17 finals')

# --- row #1 dec-AAPL: STAND DOWN ---
rep('<td><span class="pm-badge pm-cheap">#1</span></td>',
    '<td><span class="pm-badge pm-fair">#1</span> <span class="pm-note">stand down</span></td>')
rep('data-bb-touch="dec-AAPL">23.9¢</td>\n                <td class="col-num">31.93%</td>\n                <td class="col-num pm-pos">−8.03</td>\n                <td class="col-num pm-pos">1.34× (1.34×)</td>\n                <td class="col-num">$1,244 <span class="pm-note">inside fair−5 (26.93) · $2,090 ≤ fair — the 34.4–34.5¢ wall stays above fair and does not count</span></td>',
    'data-bb-touch="dec-AAPL">23.9¢</td>\n                <td class="col-num">28.69%</td>\n                <td class="col-num">−4.79</td>\n                <td class="col-num">1.20× (1.20×)</td>\n                <td class="col-num">$0 <span class="pm-note">inside fair−5 (23.69) — nothing on the walked book clears it · $1,631 ≤ fair</span></td>')
rep('<td><span class="pm-badge pm-cheap">DEEP</span> <span class="pm-note">$625 at the 23.9¢ touch (2,616 sh) · $1,018 ≤ 25¢ · $1,244 ≤ 26.93¢</span></td>',
    '<td><span class="pm-badge pm-watch">DEEP · IN BAND</span> <span class="pm-note">$625 at the 23.9¢ touch (2,616 sh) · $1,018 ≤ 25¢ · $1,631 ≤ the 28.69 fair</span></td>')
rep('<td><strong>$300 cap, lift asks ≤ 25¢</strong> — fills at ONE level on the walked book: 23.9¢ × 1,255 sh (touch two sessions old — re-check). Stop: retire on fair &lt; mid + 5. New position — the account holds none.</td>',
    '<td><strong>STAND DOWN — the ticket&rsquo;s own stop fired tonight:</strong> the rule written into it was &ldquo;retire on fair &lt; mid + 5&rdquo;, and the breakout close puts the fair (28.69) 4.84 under the walked 23.85 mid — the first inside-band print since Sep 11. No buy at 23.9¢. Re-arm only if a fresh walk prints a touch ≤ 23.69 (fair−5) or the fair re-crosses mid + 5. New position — the account holds none.</td>')
rep('The widest edge on a real book, and the fair is the most robust number on the tab: 28.4 / 31.9 / 33.3 / 33.7 at σ 1.5 / 2 / 2.5 / 3%/day',
    'Was the widest edge on a real book for three sessions; tonight the stop wrote its own ending. The fair is still the most robust number on the tab: 24.3 / 28.7 / 30.8 / 31.6 at σ 1.5 / 2 / 2.5 / 3%/day')
rep('The market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 1.17%/day to be right — or, at σ 2%, an expected <strong>≈+4.6% NVIDIA-over-Apple drift</strong> to Dec 31 (that is the size of the view you are taking against the market).',
    'The market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 1.47%/day to be right — or, at σ 2%, <strong>essentially no drift view at all (≈0.1%)</strong>: after tonight the market and the model price this coin the same.')
rep('73 trading days for a 7.24% gap.', '72 trading days for an 8.95% gap.')

# --- row #2 Apple crown: RICH on a stale mid ---
rep('<td><span class="pm-badge pm-fair">#2</span></td>', '<td><span class="pm-badge pm-rich">#2</span></td>')
rep('data-bb-touch="sep-crownAAPL">12.7¢</td>\n                <td class="col-num">12.20%</td>\n                <td class="col-num">+0.50</td>\n                <td class="col-num">0.96× (0.97×)</td>\n                <td class="col-num">$0</td>',
    'data-bb-touch="sep-crownAAPL">12.7¢</td>\n                <td class="col-num">6.48%</td>\n                <td class="col-num">+6.22</td>\n                <td class="col-num">0.51× (0.51×)</td>\n                <td class="col-num">$0</td>')
rep('<td><span class="pm-badge pm-watch">AT FAIR</span> <span class="pm-note">$0 of asks at or under the 12.20 fair · twin: NVIDIA-crown 87.15 mid vs an 87.80 fair (−0.65) — the pair now prices the crown almost exactly</span></td>',
    '<td><span class="pm-badge pm-rich">RICH · STALE</span> <span class="pm-note">$0 of asks at or under the 6.48 fair · twin: NVIDIA-crown 87.15 mid vs a 93.52 fair (−6.37) — the stale pair (99.75 summed) prices the pre-breakout crown, not tonight&rsquo;s</span></td>')
rep('<td><strong>HOLD the 22,532 sh (5.86¢ avg, +$1,518 open) — the edge is GONE tonight:</strong> the close cut the crown fair 17.74 → 12.20 (the lead re-widened to 7.24%), so the 12.6 mid sits +0.40 ABOVE fair — there is no price on this book the model would pay, and the ADD is dead (was gated). <strong>Exit is by resolution only:</strong> the bid ladder takes 1,295 sh at 10¢ or better and ≈$892 for the whole position — the $2,839 mark is not a liquidation value; that, not RV, is why there is no trim. Re-decide only on a fresh walk.</td>',
    '<td><strong>HOLD the 22,532 sh (5.86¢ avg) — the mark is RICH tonight:</strong> the breakout cut the crown fair 12.20 → 6.48 (lead 8.95%), so the stale 12.6 mid sits +6.12 ABOVE fair — the model would now SELL this mid, but the mid is three sessions old and the exit reality is what it was: the bid ladder takes 1,295 sh at 10¢ or better, ≈$892 for the whole position, and only $275 of bids rest at or over the 6.48 fair — the $2,839 mark is not a liquidation value. The position still rides to resolution; <strong>a fresh walk, not this stale print, decides whether the 12.4–12.5¢ bids are worth hitting.</strong></td>')
rep('<td>The rank is history, not edge: tonight is the first close of the outage where the tab&rsquo;s biggest position marks AT its model fair — 12.20 vs the 12.6 mid, a coin the model and the market now price the same. The number is still the least robust here: 6.0 / 12.2 / 17.6 / 21.8 across the same σ sweep — at σ 2.5%/day the hold is cheap again, at σ 1.5% it is twice rich. Nine trading days for a 7.24% gap; the position rides to resolution because the exit bid, not the model, says so.</td>',
    '<td>The rank is history, not edge: the tab&rsquo;s biggest position now marks at TWICE its model value — 6.48 fair vs the stale 12.6 mid — one close after marking at fair. The number is still the least robust here: 2.2 / 6.5 / 11.3 / 15.6 across the same σ sweep — at σ 2.5%/day the mark is nearly fair again, at σ 1.5% it is 6× rich. Eight trading days for an 8.95% gap; the position rides to resolution because the exit bid, not the model, says so.</td>')

# --- row #3 dec-NVDA NO: RICH badge off ---
rep('<td><span class="pm-badge pm-rich">#3</span> <span class="pm-note">no ticket</span></td>',
    '<td><span class="pm-badge pm-fair">#3</span> <span class="pm-note">no ticket</span></td>')
rep('<td class="col-num">62.51% <span class="pm-note">(NO 37.49)</span></td>', '<td class="col-num">65.98% <span class="pm-note">(NO 34.02)</span></td>')
rep('<td class="col-num">+5.49 <span class="pm-note">(mid +5.99)</span></td>', '<td class="col-num">+2.02 <span class="pm-note">(mid +2.52)</span></td>')
rep('<td class="col-num">NO 1.17× (1.19×)</td>', '<td class="col-num">NO 1.06× (1.08×)</td>')
rep('<td class="col-num">$981 NO <span class="pm-note">NO-dollars ≤ the 37.49 NO-fair ($1,887 YES-notional of bids ≥ 62.51)</span></td>',
    '<td class="col-num">$423 NO <span class="pm-note">NO-dollars ≤ the 34.02 NO-fair ($853 YES-notional of bids ≥ 65.98)</span></td>')
rep('(≈310 sh over two levels, VWAP 32.2¢); tonight&rsquo;s close compressed the fade again (fair 59.68 → 62.51 — the RICH print survives by 0.99 at the mid).',
    '(≈310 sh over two levels, VWAP 32.2¢); tonight&rsquo;s close KILLED the fade (fair 62.51 → 65.98 — the RICH badge comes off at +2.52, as the Sep 17 note said one more session like this would do; the December book is all inside the band).')
rep('because NO also pays on the Alphabet/Microsoft legs the model prices at 4.8 combined.',
    'because NO also pays on the Alphabet/Microsoft legs the model prices at 4.6 combined.')

# --- row #4 sep3MSFT ---
rep('data-bb-touch="sep-sep3MSFT">4.5¢ bid</td>\n                <td class="col-num">1.26%</td>\n                <td class="col-num">+3.24</td>\n                <td class="col-num">0.28× (0.28×) <span class="pm-note">YES side held; the NO side handed to the buyer is 1.03×</span></td>\n                <td class="col-num">$100</td>',
    'data-bb-touch="sep-sep3MSFT">4.5¢ bid</td>\n                <td class="col-num">0.43%</td>\n                <td class="col-num">+4.07</td>\n                <td class="col-num">0.10× (0.09×) <span class="pm-note">YES side held; the NO side handed to the buyer is 1.04×</span></td>\n                <td class="col-num">$205</td>')
rep('Microsoft needs to pass Alphabet (12.6% below it) in nine sessions — tonight both closed green (MSFT +1.52%, GOOGL +1.30%) and the gap barely moved.',
    'Microsoft needs to pass Alphabet (13.8% below it) in eight sessions — and tonight the gap widened again (GOOGL +0.64%, MSFT −0.80%, the board&rsquo;s worst close).')
rep('the only held leg on the tab priced at 0.28× its model value with a bid that takes all of it — the close cut the fair again (1.55 → 1.25; the Sep 18 morning revision ticks it back to 1.26), so the sell strengthens a third straight session.',
    'the only held leg on the tab priced at 0.10× its model value with a bid that takes all of it — the close cut the fair again (1.26 → 0.43), so the sell strengthens a fourth straight session, the strongest print yet.')

# --- watch row sep2NVDA ---
rep('data-bb-touch="sep-sep2NVDA">14.3¢</td>\n                <td class="col-num">12.19%</td>\n                <td class="col-num">+2.11</td>\n                <td class="col-num">0.85× (0.94×)</td>\n                <td class="col-num">$0</td>',
    'data-bb-touch="sep-sep2NVDA">14.3¢</td>\n                <td class="col-num">6.47%</td>\n                <td class="col-num">+7.83</td>\n                <td class="col-num">0.45× (0.50×)</td>\n                <td class="col-num">$0</td>')
rep('11.6 / 14.3 — $0 of asks at or under the 12.19 fair', '11.6 / 14.3 — $0 of asks at or under the 6.47 fair')
rep('<strong>No ticket — the case DIED tonight:</strong> the close pulls the fair to 12.19, UNDER the 14.3¢ ask (+2.11) — there is no price on this book the model would pay.',
    '<strong>No ticket — and the premium doubled tonight:</strong> the breakout pulls the fair to 6.47, HALF the 14.3¢ ask (+7.83) — there is no price on this book the model would pay.')
rep('Listed so nobody buys it thinking it is a second idea: NVIDIA finishing 2nd ≈ Apple finishing 1st (12.19 vs 12.20). The seat&rsquo;s other side — sep2AAPL 84.5 vs 87.37, −2.87 — sits inside the band from below: both seat legs are quiet, and the walked 82 / 87 spread is wider than either edge.',
    'Listed so nobody buys it thinking it is a second idea: NVIDIA finishing 2nd ≈ Apple finishing 1st (6.47 vs 6.48). The seat&rsquo;s other side — sep2AAPL 84.5 vs 93.09, −8.59 with $805 of asks inside fair−5 — is tonight&rsquo;s widest print, and it is a THREE-session-old pre-breakout ladder: it heads the re-walk queue, not the ticket queue.')

# --- honesty line ---
rep('(7.24% / $358.4B at the Sep 17 close)', '(8.95% / $442.1B at the Sep 18 close)')
rep('pay together only 6.6% of the time (P(Dec | Sep) 54% vs P(Dec | not Sep) 29%, payoff correlation ≈0.18)',
    'pay together only 3.4% of the time (P(Dec | Sep) 53% vs P(Dec | not Sep) 27%, payoff correlation ≈0.14)')
rep('That is why #1 (the December leg, no exposure yet, the most σ-robust fair) outranks #2 — which tonight is not a bet at all but the book&rsquo;s biggest holding marking at fair.',
    'That is why #1 (the December leg, no exposure yet, the most σ-robust fair) outranks #2 — though tonight NEITHER is live: #1 stood down on its own stop and #2 is the book&rsquo;s biggest holding marking rich on a stale mid.')
rep('(#1 at one level; #2&rsquo;s ADD is dead — nothing on the walked book beats the 12.20 fair)',
    '(#1 stands down — $0 inside fair−5 tonight; #2&rsquo;s ADD is dead — nothing on the walked book beats the 6.48 fair)')

# ---------- D. analysis table ----------
NOTE_NEW = ('<strong>Sep 18 23:1xZ PM: caps are the SEP 18 CLOSES (history pages ~23:1xZ; all five Sep 17 finals re-confirmed beneath them; NVDA&rsquo;s page split $222.27 header / $222.06 table — the header taken, disclosed, tomorrow&rsquo;s pass locks it): '
 'NVDA $5,378.9B ($222.27, +1.34%, the quad-witching breakout) / AAPL $4,936.9B ($336.13, −0.26%) / GOOGL $4,255.5B ($349.54, +0.64%) / MSFT $3,668.0B ($493.78, −0.80%, the board&rsquo;s worst) / AMZN $2,729.2B ($253.71, +1.00%) — the lead re-widens a fourth straight close, 7.24% → 8.95% / $442.1B, PAST the Sep 11 melt-up finals&rsquo; 8.25%; the cushion narrows to 16.01%; T = 8 / 72. '
 'Every fair, edge, RV, verdict and tradeable-at-fair below re-ran on these closes (calibration reproduced every Sep 18 AM fair exactly) against the UNCHANGED Sep 16 01:45Z walk mids — now THREE sessions behind and pre-breakout: re-walk before acting. '
 'What moved: dec-AAPL&rsquo;s CHEAP badge comes OFF (−4.84 — Best Bets #1 stands down on its own stop) and dec-NVDA&rsquo;s RICH badge comes off (+2.52) — the December book is all inside the band for the first time since Sep 8; the September partition inverts on the stale ladders (crownAAPL +6.12 RICH, crownNVDA −6.37, sep2AAPL −8.59, sep2NVDA +7.83, sep3GOOGL −5.13 at the ask) — re-walk queue, not tickets; sep3MSFT&rsquo;s sell strengthens (fair 0.43, RV 0.09×).</strong> '
 '· <em>The AM note follows, kept:</em> ')
rep('"Read the full note"><strong>Sep 18 13:2xZ AM (pre-open): the Sep 17 finals re-verified against the history pages',
    '"Read the full note">' + NOTE_NEW + '<strong>Sep 18 13:2xZ AM (pre-open): the Sep 17 finals re-verified against the history pages')

SEPGRP_NEW = ('SEPTEMBER 30 · T = 8 trading days · <strong>Sep 18 23:1xZ PM: the breakout hands the partition to the leaders — crown 93.52 / 6.48, seat 93.09-AAPL / 6.47-NVDA, 3rd 99.13-GOOGL / 0.43-MSFT. '
 'Every September edge below is a fresh fair against a THREE-session-old pre-breakout ladder: crownAAPL +6.12 RICH (the 22,532-sh hold marks 2× model), crownNVDA −6.37 and sep2AAPL −8.59 and sep3GOOGL −5.13-at-the-ask mid-CHEAP ($2,713 / $805 / $835 inside fair−5) — re-walk queue, not tickets; sep2NVDA +7.83; sep3MSFT&rsquo;s sell strengthens a fourth session (fair 0.43, RV 0.09×)</strong> · <em>the AM text, kept:</em> ')
rep('SEPTEMBER 30 · T = 9 trading days · <strong>Sep 18 13:2xZ AM:', SEPGRP_NEW + '<strong>Sep 18 13:2xZ AM:')

DECGRP_NEW = ('DECEMBER 31 — 72 TRADING DAYS · <strong>Sep 18 23:1xZ PM: the December book goes ALL-FAIR for the first time since Sep 8 — '
 'dec-AAPL 23.85 vs 28.69 = −4.84 (CHEAP badge off; Best Bets #1 stands down on its own stop; $0 inside fair−5, $1,631 ≤ fair), '
 'dec-NVDA 68.5 vs 65.98 = +2.52 (RICH badge off — the fade dies on its own fair; $423 NO-dollars at bids ≥ fair), '
 'dec-GOOGL +2.23 and dec-MSFT +0.25 inside the band</strong> · <em>the Sep 17 PM text, kept:</em> ')
rep('DECEMBER 31 — 73 TRADING DAYS · <strong>Sep 17 23:2xZ PM:', DECGRP_NEW + '<strong>Sep 17 23:2xZ PM:')

# --- caps + gaps ---
rep('data-cap="NVDA-sep">5,308.0<', 'data-cap="NVDA-sep">5,378.9<')
rep('data-cap="AAPL-sep">4,949.6<', 'data-cap="AAPL-sep">4,936.9<')
rep('data-gap="AAPL-sep">−6.75%<', 'data-gap="AAPL-sep">−8.22%<')
rep('data-cap="NVDA-dec">5,308.0<', 'data-cap="NVDA-dec">5,378.9<')
rep('data-cap="AAPL-dec">4,949.6<', 'data-cap="AAPL-dec">4,936.9<')
rep('data-gap="AAPL-dec">−6.75%<', 'data-gap="AAPL-dec">−8.22%<')
rep('data-cap="GOOGL-dec">4,228.6<', 'data-cap="GOOGL-dec">4,255.5<')
rep('data-gap="GOOGL-dec">−20.34%<', 'data-gap="GOOGL-dec">−20.89%<')
rep('data-cap="MSFT-dec">3,697.5<', 'data-cap="MSFT-dec">3,668.0<')
rep('data-gap="MSFT-dec">−30.34%<', 'data-gap="MSFT-dec">−31.81%<')
rep('data-cap="AMZN-dec">2,702.1<', 'data-cap="AMZN-dec">2,729.2<')
rep('data-gap="AMZN-dec">−49.09%<', 'data-gap="AMZN-dec">−49.26%<')

# --- model rows ---
rep('data-fair="sep-crownNVDA">87.80%</td><td class="col-num" data-edge="sep-crownNVDA">−0.65</td><td class="col-num" data-pm-rv>1.01×</td><td class="col-num"><span class="pm-badge pm-fair">$2,531</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-crownNVDA">FAIR</span> <span class="pm-note">first sub-fair print since the walk — −0.65</span></td>',
    'data-fair="sep-crownNVDA">93.52%</td><td class="col-num" data-edge="sep-crownNVDA">−6.37</td><td class="col-num" data-pm-rv>1.07×</td><td class="col-num"><span class="pm-badge pm-fair">$8,606</span></td><td><span class="pm-badge pm-cheap" data-verdict="sep-crownNVDA">CHEAP</span> <span class="pm-note">stale-ladder print ($2,713 inside fair−5) — the 01:45Z book predates the breakout: re-walk first</span></td>')
rep('data-fair="sep-crownAAPL">12.20%</td><td class="col-num" data-edge="sep-crownAAPL">+0.40</td><td class="col-num" data-pm-rv>0.97×</td><td class="col-num"><span class="pm-badge pm-fair">$24</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-crownAAPL">FAIR</span> <span class="pm-note">CHEAP badge off — the 22,532-sh hold marks at fair</span></td>',
    'data-fair="sep-crownAAPL">6.48%</td><td class="col-num" data-edge="sep-crownAAPL">+6.12</td><td class="col-num" data-pm-rv>0.51×</td><td class="col-num"><span class="pm-badge pm-rich">$275</span></td><td><span class="pm-badge pm-rich" data-verdict="sep-crownAAPL">RICH</span> <span class="pm-note">the 22,532-sh hold marks 2× model on a stale mid — rides to resolution (Best Bets #2)</span></td>')
rep('data-fair="sep-sep2AAPL">87.37%</td><td class="col-num" data-edge="sep-sep2AAPL">−2.87</td><td class="col-num" data-pm-rv>1.03×</td><td class="col-num"><span class="pm-badge pm-fair">$27</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep2AAPL">FAIR</span> <span class="pm-note">82 / 87 — WIDE</span></td>',
    'data-fair="sep-sep2AAPL">93.09%</td><td class="col-num" data-edge="sep-sep2AAPL">−8.59</td><td class="col-num pm-pos" data-pm-rv>1.10×</td><td class="col-num"><span class="pm-badge pm-fair">$3,074</span></td><td><span class="pm-badge pm-cheap" data-verdict="sep-sep2AAPL">CHEAP</span> <span class="pm-note">82 / 87 WIDE — tonight&rsquo;s widest print, on a pre-breakout ladder ($805 inside fair−5): re-walk first</span></td>')
rep('data-fair="sep-sep2NVDA">12.19%</td><td class="col-num" data-edge="sep-sep2NVDA">+0.76</td><td class="col-num" data-pm-rv>0.94×</td><td class="col-num"><span class="pm-badge pm-watch">$0</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep2NVDA">FAIR</span> <span class="pm-note">THIN · 11.6 / 14.3 · flipped over fair</span></td>',
    'data-fair="sep-sep2NVDA">6.47%</td><td class="col-num" data-edge="sep-sep2NVDA">+7.83</td><td class="col-num" data-pm-rv>0.50×</td><td class="col-num"><span class="pm-badge pm-watch">$24</span></td><td><span class="pm-badge pm-rich" data-verdict="sep-sep2NVDA">RICH</span> <span class="pm-note">THIN · 11.6 / 14.3 · the ask is 2× fair</span></td>')
rep('data-fair="sep-sep2GOOGL">0.44%</td><td class="col-num" data-edge="sep-sep2GOOGL">+1.21</td><td class="col-num" data-pm-rv>0.27×</td>',
    'data-fair="sep-sep2GOOGL">0.43%</td><td class="col-num" data-edge="sep-sep2GOOGL">+1.22</td><td class="col-num" data-pm-rv>0.26×</td>')
rep('data-fair="sep-sep3GOOGL">98.30%</td><td class="col-num" data-edge="sep-sep3GOOGL">−5.30</td><td class="col-num" data-pm-rv>1.06×</td><td class="col-num"><span class="pm-badge pm-fair">$28,148</span></td><td><span class="pm-badge pm-cheap" data-verdict="sep-sep3GOOGL">CHEAP</span> <span class="pm-note">92 / 94 WIDE — the 94.0 ask is −4.30, inside the band; $0 inside fair−5: a spread artifact, not a ticket</span></td>',
    'data-fair="sep-sep3GOOGL">99.13%</td><td class="col-num" data-edge="sep-sep3GOOGL">−6.13</td><td class="col-num" data-pm-rv>1.07×</td><td class="col-num"><span class="pm-badge pm-fair">$37,907</span></td><td><span class="pm-badge pm-cheap" data-verdict="sep-sep3GOOGL">CHEAP</span> <span class="pm-note">92 / 94 WIDE — the 94.0 ask itself is −5.13 tonight ($835 inside fair−5): the partition&rsquo;s first executable-looking cheap print, on a three-session-old book — re-walk first</span></td>')
rep('data-fair="sep-sep3MSFT">1.26%</td><td class="col-num" data-edge="sep-sep3MSFT">+3.29</td><td class="col-num" data-pm-rv>0.28×</td><td class="col-num"><span class="pm-badge pm-fair">$100</span></td>',
    'data-fair="sep-sep3MSFT">0.43%</td><td class="col-num" data-edge="sep-sep3MSFT">+4.12</td><td class="col-num" data-pm-rv>0.09×</td><td class="col-num"><span class="pm-badge pm-fair">$205</span></td>')
rep('data-fair="sep-sep3AAPL">0.43%</td><td class="col-num" data-edge="sep-sep3AAPL">+1.17</td><td class="col-num" data-pm-rv>0.27×</td>',
    'data-fair="sep-sep3AAPL">0.43%</td><td class="col-num" data-edge="sep-sep3AAPL">+1.17</td><td class="col-num" data-pm-rv>0.27×</td>') if False else None
rep('data-fair="sep-sep3NVDA">0.01%</td><td class="col-num" data-edge="sep-sep3NVDA">+0.24</td><td class="col-num" data-pm-rv>0.04×</td>',
    'data-fair="sep-sep3NVDA">0.00%</td><td class="col-num" data-edge="sep-sep3NVDA">+0.25</td><td class="col-num" data-pm-rv>0.00×</td>')
rep('data-fair="dec-NVDA">62.51%</td><td class="col-num" data-edge="dec-NVDA">+5.99</td><td class="col-num" data-pm-rv>0.91×</td><td class="col-num"><span class="pm-badge pm-rich">$1,887</span></td><td><span class="pm-badge pm-rich" data-verdict="dec-NVDA">RICH</span></td><td class="col-num">61%</td>',
    'data-fair="dec-NVDA">65.98%</td><td class="col-num" data-edge="dec-NVDA">+2.52</td><td class="col-num" data-pm-rv>0.96×</td><td class="col-num"><span class="pm-badge pm-fair">$853</span></td><td><span class="pm-badge pm-fair" data-verdict="dec-NVDA">FAIR</span> <span class="pm-note">RICH badge off — the fade dies on its own fair</span></td><td class="col-num">60%</td>')
rep('data-fair="dec-AAPL">31.93%</td><td class="col-num" data-edge="dec-AAPL">−8.08</td><td class="col-num pm-pos" data-pm-rv>1.34×</td><td class="col-num"><span class="pm-badge pm-cheap">$2,090</span> <span class="pm-note">$1,244 ≤ fair−5 · the 34.4–34.5¢ wall sits above fair</span></td><td><span class="pm-badge pm-cheap" data-verdict="dec-AAPL">CHEAP</span></td><td class="col-num">59%</td>',
    'data-fair="dec-AAPL">28.69%</td><td class="col-num" data-edge="dec-AAPL">−4.84</td><td class="col-num" data-pm-rv>1.20×</td><td class="col-num"><span class="pm-badge pm-fair">$1,631</span> <span class="pm-note">$0 ≤ fair−5 · the 34.4–34.5¢ wall sits above fair</span></td><td><span class="pm-badge pm-fair" data-verdict="dec-AAPL">FAIR</span> <span class="pm-note">CHEAP badge off — Best Bets #1 stands down on its own stop</span></td><td class="col-num">58%</td>')
rep('data-fair="dec-GOOGL">4.40%</td><td class="col-num" data-edge="dec-GOOGL">+2.10</td><td class="col-num" data-pm-rv>0.68×</td>',
    'data-fair="dec-GOOGL">4.27%</td><td class="col-num" data-edge="dec-GOOGL">+2.23</td><td class="col-num" data-pm-rv>0.66×</td>')
rep('data-fair="dec-MSFT">0.42%</td><td class="col-num" data-edge="dec-MSFT">+0.13</td><td class="col-num" data-pm-rv>0.76×</td>',
    'data-fair="dec-MSFT">0.30%</td><td class="col-num" data-edge="dec-MSFT">+0.25</td><td class="col-num" data-pm-rv>0.55×</td>')

FOOT_NEW = ('<strong>Sep 18 23:1xZ PM — the quad-witching breakout stands the flagship down.</strong> Friday&rsquo;s expiry closes (history pages ~23:1xZ; all five Sep 17 finals re-confirmed beneath them; NVDA&rsquo;s page split $222.27 header / $222.06 table — the header taken, with the after-hours series keyed off it, and disclosed for the morning pass to lock): '
 'NVDA <strong>+1.34% to $222.27 ($5,378.9B) on 181.7M shares</strong>, AMZN +1.00% ($2,729.2B), GOOGL +0.64% ($4,255.5B — it opened at $357.31 and faded the whole premarket bid), AAPL −0.26% ($4,936.9B), MSFT −0.80% ($3,668.0B, the board&rsquo;s worst) — '
 'the lead re-widens a FOURTH straight close, 7.24% → <strong>8.95% / $442.1B — past the Sep 11 melt-up finals&rsquo; own 8.25%, the widest since the Sep 10 close</strong>; the cushion narrows 17.05% → 16.01% / $681.4B; T <strong>8 / 72</strong>. '
 'Calibration first (the quadrature reproduces every Sep 18 AM fair exactly), then fresh fairs: Dec <strong>65.98 / 28.69 / 4.27 / 0.30 / 0.00</strong>; crown <strong>93.52 / 6.48 / 0.00</strong>; seat <strong>93.09-AAPL / 6.47-NVDA / 0.43-GOOGL</strong>; 3rd <strong>99.13-GOOGL / 0.43-MSFT / 0.43-AAPL / 0.00-NVDA</strong>; P(±5/wk) <strong>60 / 58 / 4</strong>. '
 'The mids are the UNCHANGED Sep 16 01:45Z walk (autodata down a 38th feed run), so every edge is a fresh fair against a THREE-session-old, pre-breakout touch: '
 '<strong>dec-AAPL −4.84 — the CHEAP badge comes off and Best Bets #1 STANDS DOWN on the stop written into its own ticket</strong> (fair &lt; mid + 5; $0 inside fair−5, $1,631 at or under fair); '
 '<strong>dec-NVDA +2.52 — the RICH badge comes off, the fade dies on its own fair</strong> ($423 NO-dollars at bids ≥ fair): the December book is all-FAIR for the first time since Sep 8; '
 '<strong>the crown pair inverts — crownAAPL +6.12 RICH (the 22,532-sh hold marks 2× model; rides to resolution on the exit-bid logic) against crownNVDA −6.37 mid-CHEAP</strong>; '
 'sep2AAPL −8.59 (the pass&rsquo;s widest, $805 inside fair−5) and sep3GOOGL −5.13 at the ask ($835) join it in the <strong>re-walk queue — every September cheap print here is a stale ladder against a post-breakout fair, and none is a ticket until a fresh book says so</strong>; '
 'sep2NVDA +7.83 (the ask is 2× fair); sep3MSFT&rsquo;s sell strengthens a fourth straight session (fair 0.43, RV 0.09× — the strongest print yet). '
 '<em>The AM and Sep 17 PM text follows, kept for the record — its caps, fairs, T counts and depth figures are superseded above.</em> ')
rep('<strong>Sep 18 13:2xZ AM — the morning check catches a Microsoft revision.</strong>', FOOT_NEW + '<strong>Sep 18 13:2xZ AM — the morning check catches a Microsoft revision.</strong>')

# ---------- E. Top Trades #1 pointer ----------
rep('fair 31.93 at the Sep 17 PM re-run — the ticket stands',
    'fair 28.69 at the Sep 18 PM re-run — the ticket STANDS DOWN on its own stop (−4.84, inside the band)')
rep('<strong>Sep 17 23:2xZ PM:</strong> the all-green close re-widens the lead to 7.24% and eases the fair again, 34.14 → 31.93 — the ticket STANDS a third session:',
    '<strong>Sep 18 23:1xZ PM:</strong> the quad-witching breakout (lead 8.95%, past the melt-up finals) pulls the fair 31.93 → 28.69 and FIRES the ticket&rsquo;s own stop — fair &lt; mid + 5 (−4.84 at the walked 23.85 mid): <strong>the ticket STANDS DOWN after three sessions</strong>; $0 inside fair−5; re-arm only on a fresh walk printing ≤ 23.69 or a fair back over mid + 5. <strong>Sep 17 23:2xZ PM:</strong> the all-green close re-widens the lead to 7.24% and eases the fair again, 34.14 → 31.93 — the ticket STANDS a third session:')

# ---------- F. header tape append ----------
TAPE_NEW = (' · <strong>Sep 18 23:1xZ — THE QUAD-WITCHING BREAKOUT: THE LEAD CLEARS THE MELT-UP, THE FLAGSHIP STANDS DOWN, BITCOIN BREAKS $80K:</strong> autodata is down a <strong>THIRTY-EIGHTH</strong> consecutive feed run (the Sep 18 22:45Z cron silent; this run&rsquo;s ~23:09Z poke touching fetch/poke unanswered — the Actions disablement stands). '
 'Caps-only on the Sep 18 expiry closes (history pages ~23:1xZ; all five Sep 17 finals re-confirmed beneath them; NVDA&rsquo;s page split $222.27 header / $222.06 table — the header taken, disclosed): NVDA +1.34% ($222.27, $5,378.9B, 181.7M shares) with AMZN +1.00% and GOOGL +0.64% against AAPL −0.26% ($4,936.9B) and MSFT −0.80% — <strong>the lead re-widens a fourth straight close, 7.24% → 8.95% / $442.1B, past the Sep 11 melt-up finals&rsquo; 8.25% — the widest since the Sep 10 close</strong>; cushion 16.01% / $681.4B, T 8 / 72. '
 'Calibration first, then fresh fairs: Dec 65.98 / 28.69 / 4.27 / 0.30, crown 93.52 / 6.48, seat 93.09 / 6.47, 3rd 99.13 / 0.43; P(±5/wk) 60 / 58 / 4. '
 'Against the unchanged Sep 16 01:45Z walk mids (THREE sessions behind, pre-breakout): <strong>dec-AAPL −4.84 — CHEAP badge off, Best Bets #1 STANDS DOWN on its own stop ($0 inside fair−5)</strong>; <strong>dec-NVDA +2.52 — RICH badge off, the December book all-FAIR for the first time since Sep 8</strong>; crownAAPL +6.12 RICH (the 22,532-sh hold marks 2× model — rides to resolution) vs crownNVDA −6.37; sep2AAPL −8.59 the widest print ($805 inside fair−5); sep3GOOGL −5.13 at the ask; sep2NVDA +7.83 — the September stale-ladder prints head the re-walk queue, not the ticket queue; sep3MSFT&rsquo;s sell strengthens (fair 0.43, RV 0.09×). '
 'BTC: <strong>$81,228.07 (CoinGecko live, +6.2%/24h, range $76,205–$81,304; Kraken live cross $80,996.00 ~0.29% under — both live) — the series&rsquo; FIRST $80k print: +4.52% on the AM print (the strongest bid of the outage), +3.59% OVER the Sep 1 bake (the first above-bake read since Sep 8 and the widest ever)</strong>; T 104.2d: the surge blows the ladder residuals to the series&rsquo; wides — $85k fair 85.0 vs the walked 68.0 mid (−17.0), $90k −18.4, $95k −16.9, $100k −15.1, $110k −8.6, and the dips flip RICH ($60k +6.8, $55k +9.1, $50k +9.7); needed touch to $85k just +4.6% — labeled color, the BTC tab keeps its Sep 1 01:27Z stamps and its re-bake is now the loudest want on the page. '
 'Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.')
OLD_TAPE_END = ('($90k −5.7, $95k −5.9, $100k −5.9; $85k flips back under fair at −3.0, $110k −2.8, $60k −0.7 nearly at fair, $55k +4.5, $50k +7.3; needed touch +9.4%) — labeled color, the BTC tab keeps its Sep 1 01:27Z stamps. Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.')
rep(OLD_TAPE_END, OLD_TAPE_END + TAPE_NEW)

# ---------- G. sync bar ----------
LATEST_NEW = ('<strong>Latest: Sep 18 23:1xZ PM pass (the Friday quad-witching close) — NVIDIA&rsquo;s breakout (+1.34% $222.27, $5,378.9B on 181.7M shares) against a red Apple (−0.26%) re-widens the lead a fourth straight close, 7.24% → 8.95% / $442.1B — past the Sep 11 melt-up finals&rsquo; 8.25%, the widest since Sep 10; cushion 16.01%, T 8 / 72. Fresh fairs (calibration exact): Dec 65.98 / 28.69, crown 93.52 / 6.48, seat 93.09 / 6.47, 3rd 99.13 / 0.43, P(±5/wk) 60 / 58 / 4 — and the badges fall like dominoes against the unchanged (now THREE-session-old, pre-breakout) Sep 16 01:45Z walk mids: dec-AAPL −4.84 CHEAP OFF — Best Bets #1 STANDS DOWN on the stop written into its own ticket; dec-NVDA +2.52 RICH OFF — the December book all-FAIR for the first time since Sep 8; crownAAPL +6.12 RICH (the 22,532-sh hold marks 2× model, rides to resolution); sep2AAPL −8.59, crownNVDA −6.37, sep3GOOGL −5.13-at-the-ask — stale-ladder cheap prints that head the re-walk queue, not the ticket queue; sep3MSFT&rsquo;s sell strengthens a fourth session (fair 0.43). NVDA source split disclosed ($222.27 header / $222.06 table — header taken, morning pass locks it). BTC BREAKS $80K: $81,228.07 (CoinGecko live; Kraken cross $80,996 — both live), +4.52% on the AM print, +3.59% over the Sep 1 bake — first $80k print and strongest above-bake read of the series; ladder residuals at the series&rsquo; wides ($90k −18.4; dips flipped rich) — the Bitcoin tab re-bake is now the loudest want. Autodata DOWN a 38th feed run; tab bakes: Oil Sep 10, Treasuries Sep 9 close, Largest-Company fairs Sep 18 23:1xZ on the Sep 16 01:45Z walk mids, Bitcoin Sep 1, Iran Sep 1; Leaderboard re-marked Sep 15 01:10Z.</strong>')
i = html.index('<strong>Latest: Sep 18 13:2xZ AM pass')
j = html.index('</strong>', i) + len('</strong>')
OLD_LATEST = html[i:j]
R.append((OLD_LATEST, LATEST_NEW))

CHRON_NEW = (' <strong>Sep 18 23:1xZ PM run (the Friday quad-witching close): NVDA +1.34% ($222.27, $5,378.9B, 181.7M shares — the page&rsquo;s $222.27-header / $222.06-table split disclosed, header taken, the morning pass locks it) against AAPL −0.26%, MSFT −0.80% (GOOGL +0.64% faded a $357.31 open, AMZN +1.00%) — the lead re-widens a FOURTH straight close, 7.24% → 8.95% / $442.1B, past the Sep 11 melt-up finals&rsquo; 8.25%, the widest since the Sep 10 close; cushion 16.01%, T 8 / 72. Calibration reproduced every Sep 18 AM fair exactly, then fresh fairs on the Sep 18 closes: Dec 65.98 / 28.69 / 4.27 / 0.30, crown 93.52 / 6.48, seat 93.09 / 6.47, 3rd 99.13 / 0.43, P(±5/wk) 60 / 58 / 4. Against the unchanged Sep 16 01:45Z walk ladders (THREE sessions behind, pre-breakout, disclosed on every touched surface): dec-AAPL −4.84 — the CHEAP badge comes off and Best Bets #1 STANDS DOWN on its own written stop (fair &lt; mid + 5; $0 inside fair−5); dec-NVDA +2.52 — the RICH badge comes off, the December book all-FAIR for the first time since Sep 8; the crown pair inverts (crownAAPL +6.12 RICH — the 22,532-sh hold marks 2× model, rides to resolution; crownNVDA −6.37 mid-CHEAP $2,713 inside fair−5); sep2AAPL −8.59 the pass&rsquo;s widest ($805 inside fair−5); sep3GOOGL&rsquo;s 94.0 ask crosses the line (−5.13, $835); sep2NVDA +7.83 — every September cheap print is a stale pre-breakout ladder: re-walk queue, not tickets; sep3MSFT&rsquo;s sell strengthens a fourth session (fair 0.43, RV 0.09×). BTC BREAKS $80K: $81,228.07 (CoinGecko live, +6.2%/24h, range $76,205–$81,304; Kraken live cross $80,996.00 ~0.29% under — both live, no snapshot rotation), +4.52% on the AM print — the outage&rsquo;s strongest bid — and +3.59% OVER the Sep 1 bake, the series&rsquo; first above-bake read since Sep 8 and its widest ever; T 104.2d — the ladder&rsquo;s up-rungs print the series&rsquo; widest cheap residuals ($85k −17.0 with fair 85.0, $90k −18.4, $95k −16.9, $100k −15.1, $110k −8.6) and the dips flip rich ($60k +6.8, $55k +9.1, $50k +9.7); needed touch +4.6% — the Bitcoin tab re-bake is now the loudest want on the page. Autodata DOWN a THIRTY-EIGHTH feed run (22:45Z cron silent; ~23:09Z poke unanswered). Balances/cards/velocity/ledgers keep their stamps (61 fills owed). No trades placed.</strong>')
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
