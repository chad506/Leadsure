# -*- coding: utf-8 -*-
"""Review-pass fixes for the Sep 16 01:45Z Largest-Company bake — three adversarial reviewers
(data fact-check / model attack / trader) returned 9 + 15 + 10 findings; every confirmed one is applied here.
Headline corrections: the dec-NVDA "72¢ GTC bid" cannot be open (market traded through 72 on Sep 14; activity
feed complete to Aug 4 shows no dec-NVDA fill) — chore CLOSED; NO-side tickets quoted in NO-dollars; the $41.8k
"at fair" is led by the $1,774 inside fair−5 everywhere; σ units unified; ranking rule restated; row count 8 not 9."""
REPO = '/home/claude/Leadsure'
P = REPO + '/polymarket/index.html'
h = open(P, encoding='utf-8').read()
n = 0
def rep(old, new, count=1):
    global h, n
    c = h.count(old); assert c == count, f'expected {count}, got {c}: {old[:100]!r}'
    h = h.replace(old, new); n += 1

# ---- Best Bets price-note: ranking rule as actually applied
rep('Rank order = RV at the executable price, then book depth, then the account&rsquo;s existing exposure. <strong>Read the honesty line under the table before acting: rows #1–#3 are one factor.</strong>',
    'Rank order = RV at the executable price, <em>discounted</em> for how robust the fair is to σ and for exposure the account already carries — which is why a 1.45× outranks a 1.65× tonight; book depth breaks ties. <strong>Read the honesty line under the table before acting: rows #1–#3 share one directional exposure.</strong> Resolution per each market&rsquo;s rules (a consensus of credible reporting on market cap at the close of the last trading day — Sep 30 and Dec 31 are both trading days); capital is locked until resolution, and the resolver&rsquo;s share counts are a live risk on an 11-day binary (a 0.5% share-count difference is ~10% of the 5.51% gap).')

# ---- #1 row: depth cell, $ at fair, σ units + drift equivalent
rep('<td class="col-num">$41,805</td>\n                <td><span class="pm-badge pm-cheap">DEEP</span> <span class="pm-note">$625 at the touch · $1,774 inside fair−5 · $37,940 of it is a two-level wall at 34.4–34.5¢</span></td>',
    '<td class="col-num">$1,774 <span class="pm-note">inside fair−5 · $41,805 ≤ fair, of which $37,940 is a 34.4–34.5¢ wall at RV 1.01×</span></td>\n                <td><span class="pm-badge pm-cheap">DEEP</span> <span class="pm-note">$625 at the 23.9¢ touch (2,616 sh) · $1,018 ≤ 25¢ · $1,774 ≤ 29.77¢</span></td>')
rep('so the market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 0.88%/day to be right — the last six closes (Sep 8–15) realized ~1.75% pair-implied. 75 trading days for a 5.51% gap.',
    'so the market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 0.88%/day to be right — or, at σ 2%, an expected <strong>+6.3% NVIDIA-over-Apple drift</strong> to Dec 31 (that is the size of the view you are taking against the market). Realized σ<sub>rel</sub> on the NVDA/AAPL pair over the six daily returns Sep 8–15 was ~2.5%/day (2.7 without the Sep 8 print) — six observations, one of them the −5.9% melt-up day: it supports the direction, not the digit. 75 trading days for a 5.51% gap.')

# ---- #2 row: NO-dollar twin, exit-by-resolution, drift equivalent
rep('twin: NVIDIA-crown NO at 13.0¢ (RV 1.61×, $561 at one level, $8,378 of bids ≥ fair)',
    'twin: NVIDIA-crown NO at 13.0¢ (RV 1.61×, $561 of NO at one level, $1,554 of NO-dollars ≤ the 20.97 NO-fair — $8,378 YES-notional)')
rep('For size past $100 use the NVIDIA-crown NO leg at 13.0¢ flat instead of walking the Apple asks.</td>',
    'For size past $100 use the NVIDIA-crown NO leg at 13.0¢ flat instead of walking the Apple asks. <strong>Exit is by resolution only:</strong> the bid ladder takes 1,295 sh above 10¢ and ≈$892 for the whole position — the $2,839 mark is not a liquidation value; that, not RV, is why there is no trim.</td>')
rep('(break-even σ 1.41%/day). Eleven trading days for a 5.51% gap: a coin the model calls 21% and the market 12.6.',
    '(break-even σ 1.41%/day, or a +2.3% NVIDIA-over-Apple drift in eleven sessions at σ 2%). Eleven trading days for a 5.51% gap: a coin the model calls 21% and the market 12.6.')

# ---- #3 row: the 72¢ chore is CLOSED (order cannot be open); NO-dollar units; touch-based edge
rep('<td class="col-num pm-odds" data-bb-touch="dec-NVDA">68.0 / 69.0</td>\n                <td class="col-num">57.90% <span class="pm-note">(NO 42.10)</span></td>\n                <td class="col-num">+10.60</td>\n                <td class="col-num">NO 1.32× (1.34×)</td>\n                <td class="col-num">$2,928</td>\n                <td><span class="pm-badge pm-cheap">DEEP</span> <span class="pm-note">$164 of YES bids at 68, $1,843 at ≥65 — sell YES / buy NO at 32¢</span></td>\n                <td><strong>FIRST: cancel the 72¢ GTC bid</strong> — it rests 14.1 points ABOVE fair and would fill at RV 0.80×. Then, only if you want the NO-side book: <strong>$100 cap, NO ≤ 35¢</strong> (≈312 sh at 32¢).</td>\n                <td>Same thesis as #1 (NVIDIA loses the crown) with a worse multiple, because NO also pays on the Alphabet/Microsoft legs the model prices at 6.6 combined. It ranks for the chore, not the ticket: the resting 72¢ bid is the one live order on this tab that contradicts the model.</td>',
    '<td class="col-num pm-odds" data-bb-touch="dec-NVDA">68.0 / 69.0</td>\n                <td class="col-num">57.90% <span class="pm-note">(NO 42.10)</span></td>\n                <td class="col-num">+10.10 <span class="pm-note">(mid +10.60)</span></td>\n                <td class="col-num">NO 1.32× (1.34×)</td>\n                <td class="col-num">$1,710 NO <span class="pm-note">NO-dollars ≤ the 42.10 NO-fair ($2,928 YES-notional of bids ≥ 57.90)</span></td>\n                <td><span class="pm-badge pm-cheap">DEEP</span> <span class="pm-note">$77 of NO at 32¢ (the 68 bid × 240.8 sh), then 33¢ × 615.5 — buy NO = sell YES into the bid, one book</span></td>\n                <td><strong>$100 cap, NO ≤ 35¢</strong> (≈310 sh over two levels, VWAP 32.2¢). <strong>The 72¢ GTC chore is CLOSED:</strong> the bid this page carried since August cannot be open — the market traded through 72 on Sep 14 (six-hour prints 71.0 → 66.5) and the account&rsquo;s activity feed, complete back to Aug 4, shows no dec-NVDA fill, so it was cancelled or never rested. Nothing to cancel; confirm in portfolio → open orders.</td>\n                <td>Same directional exposure as #1 (NVIDIA loses the crown) with a worse multiple, because NO also pays on the Alphabet/Microsoft legs the model prices at 6.6 combined. It stays on the board as the NO-side expression for a NO-side book — #1 is the sharper version of the same view.</td>')

# ---- #4 row: RV convention note
rep('<td class="col-num">0.58× (0.58×)</td>\n                <td class="col-num">$91</td>',
    '<td class="col-num">0.58× (0.58×) <span class="pm-note">YES side held; the NO side handed to the buyer is 1.02×</span></td>\n                <td class="col-num">$91</td>')

# ---- watch row: it can take $100
rep('The same event as #2 at a worse price on a book that cannot take $100.</td>',
    'The same event as #2 at a worse price on a thinner book: $100 fills to 20.3¢ at a 16.6¢ VWAP (≈604 sh), RV ≈1.26× — worse than #2 or its NVIDIA-crown NO twin.</td>')

# ---- honesty line
rep('<strong>The honesty line.</strong> #1, #2, #3 and the watch row are ONE factor — the NVIDIA–Apple market-cap spread (5.51% / $268.0B at the Sep 15 close) — at two horizons (Sep 30, Dec 31). A portfolio of all of them is one bet, and it is a bet the account already carries:',
    '<strong>The honesty line.</strong> #1, #2, #3 and the watch row are ONE directional exposure — the NVIDIA–Apple market-cap spread (5.51% / $268.0B at the Sep 15 close) — at two horizons (Sep 30, Dec 31). One exposure, two coins: under the model the September and December Apple legs pay together only 11.5% of the time (P(Dec | Sep) 55% vs P(Dec | not Sep) 30%, payoff correlation ≈0.22), so the December leg diversifies the September one — that, as much as the exposure count, is why #1 outranks #2. It is an exposure the account already carries:')
rep('Sizing: the caps above are what the book absorbs inside fair−5 without moving the touch, scaled to a tab whose held legs mark ~$3.3k; they are not a percent-of-portfolio rule. <strong>Chores, not bets:</strong> cancel the dec-NVDA 72¢ GTC (row #3); the three Dec YES scraps the model prices at zero — SpaceX 53,096 sh (marked $265; the bids under it pay $96 for the first 30,154 sh and 0.2¢ for the rest), Aramco 36,795 sh ($55), Amazon 2,533 sh ($4) — are $324 of marks with no model support and a bid stack that returns less than half of it: sell the SpaceX top two levels, leave the dust.',
    'Sizing: the caps above are what the book absorbs inside fair−5 (#1 at one level; #2 clears three levels and part of a fourth), scaled to a tab whose held legs mark ~$3.4k; they are not a percent-of-portfolio rule. Fees: every RV here assumes none — check the market&rsquo;s fee flag before sizing; settlement lags resolution by the market&rsquo;s review window. <strong>Chores, not bets:</strong> the dec-NVDA 72¢ GTC chore is CLOSED (row #3 — the order cannot be open); the three Dec YES scraps the model prices at zero — SpaceX 53,096 sh (marked $265; the bids under it pay $96 for the first 30,154 sh and 0.2¢ for the rest), Aramco 36,795 sh ($55), Amazon 2,533 sh ($4) — are $324 of marks with no model support and a bid stack that returns little more than half of it (~$179): sell the SpaceX top two levels, leave the dust.')

# ---- Analysis footnote: allowance wording
rep('the SpaceX / Tesla / Aramco tails at 0.5 / 0.15 / 0.15 — the small-leg allowance of 0.75 re-read off their own books and unchanged;',
    'the SpaceX / Tesla / Aramco tails at 0.5 / 0.15 / 0.15 = 0.80 tonight against the 0.75 allowance in use (SpaceX 0.45 → 0.5 on a 0.4 / 0.6 book) — re-setting it moves no Dec fair by more than 0.03 (dec-NVDA 57.87, dec-AAPL 34.75), so the fairs are kept on 0.75 and the allowance is re-set at the next full bake;')

# ---- $41.8k caveats on the other surfaces
rep('and the door is real — $625 of asks at the 23.9¢ touch, $1,774 inside fair−5, $41.8k at or under fair</strong>',
    'and the door is real — $625 of asks at the 23.9¢ touch, $1,774 inside fair−5 ($41.8k at or under fair, but $37.9k of that is a 34.4–34.5¢ wall at RV 1.01×)</strong>')
rep('dec-AAPL 23.85 vs 34.77 = −10.92 CHEAP (RV 1.46×; $625 at the 23.9¢ touch, $41,805 at or under fair — Best Bets #1)',
    'dec-AAPL 23.85 vs 34.77 = −10.92 CHEAP (RV 1.46×; $625 at the 23.9¢ touch, $1,774 inside fair−5, $41,805 at or under fair of which $37,940 is a 34.4–34.5¢ wall — Best Bets #1)')
rep('dec-NVDA 68.5 vs 57.90 = +10.60 RICH ($2,928 of bids above fair; the 72¢ GTC cancel is Best Bets #3)',
    'dec-NVDA 68.5 vs 57.90 = +10.60 RICH ($2,928 YES-notional of bids above fair = $1,710 of NO-dollars; the NO-side ticket is Best Bets #3, and the 72¢ GTC chore is CLOSED — the order cannot be open)')
rep('<td class="col-num pm-pos" data-pm-rv>1.46×</td><td class="col-num"><span class="pm-badge pm-cheap">$41,805</span></td>',
    '<td class="col-num pm-pos" data-pm-rv>1.46×</td><td class="col-num"><span class="pm-badge pm-cheap">$41,805</span> <span class="pm-note">$1,774 ≤ fair−5</span></td>')
rep('the ticket is re-written in Best Bets #1 ($300 cap, lift ≤ 25¢, 1,255 sh at the 23.9¢ touch; RV 1.45×; $41.8k of asks at or under fair). Everything below is the Aug 28 text, kept for the record.',
    'the ticket is re-written in Best Bets #1 ($300 cap, lift ≤ 25¢, 1,255 sh at the 23.9¢ touch; RV 1.45×; $1,774 of asks inside fair−5, $41.8k at or under fair of which $37.9k is a 34.4–34.5¢ wall). The cap doubles $150 → $300 because the σ-band caveat that sized the Aug 28 ticket no longer bites: the fair holds 32.6–35.2 across σ 1.5–3%/day. Everything below is the Aug 28 text, kept for the record.')
rep('<h3 class="panel-title"><span class="pm-badge pm-cheap">#1 · THE RE-ENTRY — THE BOARD&rsquo;S FIRST BUY SINCE THE PRINT</span> LIVE · $150 CAP · GLOBAL #1 BUY dec-AAPL YES',
    '<h3 class="panel-title"><span class="pm-badge pm-watch">SUPERSEDED SEP 16 → BEST BETS #1 ($300 ≤ 25¢)</span> <span class="pm-badge pm-cheap">#1 · THE RE-ENTRY — THE BOARD&rsquo;S FIRST BUY SINCE THE PRINT</span> LIVE · $150 CAP · GLOBAL #1 BUY dec-AAPL YES')
rep('<div class="pm-exec"><strong>THE TICKET:</strong> <strong>BUY dec-AAPL YES — $150 cap, lift asks ≤23.70¢ (≈952 sh at ≈15.75¢), GLOBAL #1.',
    '<div class="pm-exec"><strong>THE TICKET (Aug 28 — SUPERSEDED Sep 16 by Best Bets #1: $300 cap, lift ≤ 25¢; the ≤23.70¢ limit below is under the market and will not fill):</strong> <strong>BUY dec-AAPL YES — $150 cap, lift asks ≤23.70¢ (≈952 sh at ≈15.75¢), GLOBAL #1.')

# ---- Sep 15 PM text kept-labels: hero tape, table note, Next Catalyst; hero AAPL odds stat
rep('<strong>What the Best Bets block below adds:</strong> a rank, a ticket size the book can absorb, and the honesty line that every one of them is the same factor — the NVDA–AAPL spread — at two horizons. <strong>THE ROUND TRIP',
    '<strong>What the Best Bets block below adds:</strong> a rank, a ticket size the book can absorb, and the honesty line that every one of them is the same directional exposure — the NVDA–AAPL spread — at two horizons. One correction to the Sep 15 PM chore list: the dec-NVDA 72¢ GTC bid cannot be open (the market traded through 72 on Sep 14 with no fill in the account&rsquo;s activity feed) — that chore is CLOSED. <em>The Sep 15 PM text follows, kept for the record; where it conflicts with the above, the above is current.</em> <strong>THE ROUND TRIP')
rep('Tradeable-at-fair is the FULL ladder tonight (every level at or beating the model), not the 5-point lower bound of the Sep 15 PM pass.</strong> · Model: exact-rank quadrature/MC',
    'Tradeable-at-fair is the FULL ladder tonight (every level at or beating the model), not the 5-point lower bound of the Sep 15 PM pass.</strong> · <em>The Sep 15 PM note follows, kept for the record — where it conflicts with the bold text above (MSFT $3,691.3B / −1.68%; crown and seat &ldquo;not in the walk&rdquo;; the lower-bound Tradeable column), the bold text is current.</em> · Model: exact-rank quadrature/MC')
rep('<div class="account-hero-stat-label">Next Catalyst</div><div class="account-hero-stat-value pm-hero-prose" data-longform="4" data-longform-label="More"><strong>Autodata is DOWN a THIRTY-SECOND',
    '<div class="account-hero-stat-label">Next Catalyst</div><div class="account-hero-stat-value pm-hero-prose" data-longform="4" data-longform-label="More"><strong>Sep 16 01:45Z:</strong> the chore list below is Sep 15 PM&rsquo;s and is superseded where it conflicts with Best Bets — the dec-AAPL ticket is live at 23.9¢ (−10.92, RV 1.46×, $1,774 inside fair−5), the crown and seat books ARE walked (12.6 / 84.5 — residuals −8.34 / +6.75), the 72¢ GTC is not open (chore closed), the Leaderboard citations read 1.46× / 1.29×. Next close: Wednesday Sep 16 — the Sep 15 finals are settled (MSFT $497.12). <em>Sep 15 PM text, kept:</em> <strong>Autodata is DOWN a THIRTY-SECOND')
rep('id="hero-nvda-odds">SETTLED NO / 81.5% / 23.4%<', 'id="hero-nvda-odds">SETTLED NO / 84.5% / 23.85%<')

# ---- row count 8, not 9 (sep3NVDA already carried RV); leaderboard 364 → 372
rep('nine September rows added to its table, 145 → 154 rows carrying RV', 'eight September rows added to its table and sep3NVDA re-marked, 145 → 153 rows carrying RV')
rep('<div class="kpi-value">50 / 154</div>', '<div class="kpi-value">50 / 153</div>')
rep('Nine September rows added to the Analysis table.', 'Eight September rows added to the Analysis table (sep3NVDA re-marked).')
rep('one column, one order: the 364 rows across the Analysis, Treasuries, Oil, Bitcoin and Iran tables',
    'one column, one order: the 372 rows (364 at the Sep 15 re-mark + the eight September rows the Sep 16 bake added to the Analysis table) across the Analysis, Treasuries, Oil, Bitcoin and Iran tables')

# ---- sync chronicle: Latest line + Sep 16 segment
rep('#3 cancel the dec-NVDA 72¢ GTC, #4 sell the 274-sh Microsoft-3rd leg);', '#3 the dec-NVDA NO side — the 72¢ GTC chore CLOSED, the order cannot be open; #4 sell the 274-sh Microsoft-3rd leg);')
rep('dec-AAPL 23.85 vs 34.77 −10.92 CHEAP (RV 1.46×, $41.8k of asks at or under fair)', 'dec-AAPL 23.85 vs 34.77 −10.92 CHEAP (RV 1.46×, $1,774 of asks inside fair−5; $41.8k at or under fair, $37.9k of it a 34.4–34.5¢ wall)')
rep('#3 CANCEL the dec-NVDA 72¢ GTC, optional NO $100 ≤ 35¢;', '#3 the dec-NVDA NO side, $100 ≤ 35¢ — and the 72¢ GTC chore CLOSED: the market traded through 72 on Sep 14 with no fill in the activity feed (complete to Aug 4), so the order cannot be open;')
rep('with the one-factor honesty line.', 'with the one-exposure honesty line (Sep/Dec Apple legs pay together 11.5% — corr ≈0.22). Reviewed by three adversarial passes (data / model / trader — 34 findings, every confirmed one applied, incl. NO-dollar units on NO tickets and the σ-unit fix).')

open(P, 'w', encoding='utf-8').write(h)
print('fix edits applied:', n)

# ======================= ROUND 2 (5 findings) =======================
h = open(P, encoding='utf-8').read(); n = 0
rep('dec-NVDA 68.5 vs 57.90 = +10.60 RICH unchanged (72¢ GTC still 14.1 points above fair — cancel).',
    'dec-NVDA 68.5 vs 57.90 = +10.60 RICH unchanged (the 72¢ GTC chore is CLOSED — the order cannot be open; the NO side is priced at Best Bets #3, no ticket under the catalyst clause).')
# #3 → priced, no ticket (the tab's standing catalyst clause gates dec-NVDA RICH fades)
rep('<td><span class="pm-badge pm-rich">#3</span></td>', '<td><span class="pm-badge pm-rich">#3</span> <span class="pm-note">no ticket</span></td>')
rep('<td><strong>$100 cap, NO ≤ 35¢</strong> (≈310 sh over two levels, VWAP 32.2¢). <strong>The 72¢ GTC chore is CLOSED:</strong>',
    '<td><strong>No ticket.</strong> The tab&rsquo;s standing catalyst clause holds dec-NVDA RICH out of the ticket queue (NVIDIA reports inside the December window; the fade file&rsquo;s three-for-three record of model error) — the long side got through on the Aug 28 re-entry rule with its stop written in (#1); the fade of the same market did not, and tonight changes nothing about that. If the clause is ever waived: $100 cap, NO ≤ 35¢ (≈310 sh over two levels, VWAP 32.2¢). <strong>The 72¢ GTC chore is CLOSED:</strong>')
rep('It stays on the board as the NO-side expression for a NO-side book — #1 is the sharper version of the same view.</td>',
    'It stays on the board so the twin of #1 is visible and priced — #1 is the sharper, rule-cleared version of the same view.</td>')
rep('so the market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 0.88%/day to be right — or, at σ 2%,',
    'NVIDIA&rsquo;s November report sits inside the window — that is the σ, and it is why the stop is in the ticket (the Aug 28 re-entry rule, row 104, cleared the long side through the catalyst clause; the RICH-side fade of the same market stays gated, row #3). The market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 0.88%/day to be right — or, at σ 2%,')
# chronicle / Latest / Next-Catalyst mentions of #3
rep('#3 the dec-NVDA NO side — the 72¢ GTC chore CLOSED, the order cannot be open; #4', '#3 the dec-NVDA NO side priced but NO ticket under the catalyst clause — and the 72¢ GTC chore CLOSED, the order cannot be open; #4')
rep('#3 the dec-NVDA NO side, $100 ≤ 35¢ — and the 72¢ GTC chore CLOSED:', '#3 the dec-NVDA NO side priced, no ticket (the catalyst clause still gates the RICH fade) — and the 72¢ GTC chore CLOSED:')
# Top Trades note + slate card: label the Aug 28 text
rep('every other card keeps its Aug 28 stamp and has not been re-walked · Ranked by <strong>dollars tradeable at a price that still beats fair</strong>',
    'every other card keeps its Aug 28 stamp and has not been re-walked; the 72¢ GTC chore named below is CLOSED (the order cannot be open) · <em>Aug 28 note, kept:</em> Ranked by <strong>dollars tradeable at a price that still beats fair</strong>')
rep('<div class="pm-exec"><strong>THE TICKET:</strong> <strong>Execute in rank order, POST everything the same hour: (1) BUY dec-AAPL, $150 at asks ≤23.70¢;',
    '<div class="pm-exec"><strong>THE TICKET (Aug 28 slate — item (1) SUPERSEDED Sep 16 by Best Bets #1, $300 ≤ 25¢; the 72¢ GTC chore is CLOSED):</strong> <strong>Execute in rank order, POST everything the same hour: (1) BUY dec-AAPL, $150 at asks ≤23.70¢;')
# #2 exit clause wording
rep('the bid ladder takes 1,295 sh above 10¢ and ≈$892 for the whole position', 'the bid ladder takes 1,295 sh at 10¢ or better and ≈$892 for the whole position')
# footnote: allowance clause out of the parenthetical
rep('(five Dec names plus the SpaceX / Tesla / Aramco tails at 0.5 / 0.15 / 0.15 = 0.80 tonight against the 0.75 allowance in use (SpaceX 0.45 → 0.5 on a 0.4 / 0.6 book) — re-setting it moves no Dec fair by more than 0.03 (dec-NVDA 57.87, dec-AAPL 34.75), so the fairs are kept on 0.75 and the allowance is re-set at the next full bake; the September crown, seat and 3rd-place partitions) was pulled through the reader&rsquo;s Chrome 01:44–01:46Z with cache-busted /book calls, asset_id and timestamp validated (oldest 1.3 minutes).',
    '(five Dec names plus the SpaceX / Tesla / Aramco tails; the September crown, seat and 3rd-place partitions) was pulled through the reader&rsquo;s Chrome 01:44–01:46Z with cache-busted /book calls, asset_id and timestamp validated (oldest 1.3 minutes). The tails read 0.5 / 0.15 / 0.15 = 0.80 tonight against the 0.75 small-leg allowance in use (SpaceX 0.45 → 0.5 on a 0.4 / 0.6 book); re-setting it moves no Dec fair by more than 0.03 (dec-NVDA 57.87, dec-AAPL 34.75), so the fairs are kept on 0.75 and the allowance is re-set at the next full bake.')
# watch row: the seat fade's own arming rule does not fire tonight
rep('is the same coin again, on a 5-point-wide book with $791 of bids above fair.</td>',
    'is the same coin again, on a 5-point-wide book with $791 of bids above fair — and its own arming rule (a bid ≥ 80.85 on ≥ $300) does not fire: $126 sits at 81–82.</td>')
open(P, 'w', encoding='utf-8').write(h)
print('round-2 edits applied:', n)
