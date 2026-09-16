# -*- coding: utf-8 -*-
"""Largest-Company tab re-bake + Best Bets block, Sep 16 2026 01:45Z interactive session.
Inputs: scripts/largest_sep16.py (fairs, calibration) and scripts/largest_books_sep16.txt (20 books).
Every edit is an exact-string replacement that must match exactly once."""
import re, sys
REPO = '/home/claude/Leadsure'
P = REPO + '/polymarket/index.html'
h = open(P, encoding='utf-8').read()
n_edits = 0
def rep(old, new, count=1):
    global h, n_edits
    c = h.count(old)
    assert c == count, f'expected {count} match(es), got {c}: {old[:90]!r}'
    h = h.replace(old, new); n_edits += 1

WALK = 'Sep 16 01:45Z'

# ---------------------------------------------------------------- hero tape label + lead paragraph
rep('The tape (caps = the Sep 15 close · equity mids = the Sep 15 01:10Z interactive walk · autodata DOWN — no cloud book walk)',
    'The tape (caps = the Sep 15 finals, MSFT revised to $497.12 · equity mids = the <strong>Sep 16 01:45Z interactive walk — twenty Largest-Company books incl. the September crown and seat, their first walk since Sep 1</strong> · autodata DOWN — no cloud book walk)')
rep('<strong>THE ROUND TRIP — TWO CLOSES AT ONCE AGAIN, AND THE LEAD TOUCHED 4.36%.</strong> The Sep 14 PM and Sep 15 AM scheduled sessions left no trace',
    '<strong>SEP 16 01:45Z — THE WHOLE COMPLEX IS WALKED, AND THE BEST BETS ARE NAMED BELOW.</strong> Twenty books through the reader&rsquo;s Chrome 01:44–01:46Z (every timestamp inside 1.3 minutes of the walk, asset_id-validated), the Sep 15 finals re-verified against two sources (MSFT&rsquo;s close settled <strong>$497.12, not $496.91</strong> — −1.64%, cap $3,692.8B; the other four to the cent), calibration reproduced every Sep 15 PM fair exactly, then the fairs re-ran: Dec <strong>57.90 / 34.77 / 5.87 / 0.71</strong>, crown 79.03 / 20.94, seat 77.75 / 20.87, 3rd 95.97-GOOGL / 2.62-MSFT. Against the fresh mids: <strong>dec-AAPL 23.85 vs 34.77 = −10.92 CHEAP, RV 1.46×, and the door is real — $625 of asks at the 23.9¢ touch, $1,774 inside fair−5, $41.8k at or under fair</strong>; <strong>the September crown, walked for the first time since Sep 1: Apple 12.6 vs 20.94 = −8.34 CHEAP (RV 1.66×, the tab&rsquo;s best multiple; the account is already long 22,532 sh at 5.86¢), NVIDIA 87.15 vs 79.03 = +8.12 RICH — the two legs are one bet, priced consistently</strong>; the seat book flips the other way (sep2AAPL 84.5 vs 77.75 = +6.75 RICH on a 5-point-wide book; sep2NVDA 12.95 vs 20.87 = −7.92 CHEAP on $106 of asks — the thin twin of the crown trade); dec-NVDA 68.5 vs 57.90 = +10.60 RICH unchanged (72¢ GTC still 14.1 points above fair — cancel). <strong>What the Best Bets block below adds:</strong> a rank, a ticket size the book can absorb, and the honesty line that every one of them is the same factor — the NVDA–AAPL spread — at two horizons. <strong>THE ROUND TRIP — TWO CLOSES AT ONCE AGAIN, AND THE LEAD TOUCHED 4.36%.</strong> The Sep 14 PM and Sep 15 AM scheduled sessions left no trace')

# ---------------------------------------------------------------- KPIs
rep('<div class="kpi-value" data-odds-kpi="dec-AAPL">23.4%</div>', '<div class="kpi-value" data-odds-kpi="dec-AAPL">23.85%</div>')
rep('<div class="kpi-value" data-odds-kpi="dec-GOOGL">7.5%</div>', '<div class="kpi-value" data-odds-kpi="dec-GOOGL">6.5%</div>')
rep('<div class="kpi-value" id="kpi-edge">dec-AAPL −11.37</div>', '<div class="kpi-value" id="kpi-edge">dec-AAPL −10.92</div>')
rep('<div class="kpi-label">Biggest Edge · Whole Complex</div><div class="kpi-value">dec-AAPL −11.37</div>',
    '<div class="kpi-label">Best RV · Whole Complex (Sep 16 walk)</div><div class="kpi-value">sep-crownAAPL 1.66×</div>')
rep('<div class="kpi-label">August crown</div><div class="kpi-value">SETTLED Aug 31</div>',
    '<div class="kpi-label">AAPL · Sep 30 crown</div><div class="kpi-value" data-odds-kpi="sep-crownAAPL">12.6%</div>')

# ---------------------------------------------------------------- BEST BETS block (new), inserted after the KPI grid
BEST = '''
      <!-- ===================== BEST BETS (Sep 16 01:45Z walk) ===================== -->
      <section class="table-section pm-bestbets" aria-label="Best bets">
        <div class="table-header-row">
          <h2 class="section-title">Best Bets — Ranked by Relative Value, Sized to the Book</h2>
          <span class="pm-sec-date">Walk: Sep 16, 2026 · 01:45 UTC (Tuesday 6:45 PM PT, after the Sep 15 close)</span>
          <span class="price-note" data-longform="2" data-longform-label="Read the full note">Every row below was walked tonight — <strong>price = the executable touch, not a mid</strong>; RV = model value ÷ that price (site standard is the mid — both shown); &ldquo;$ at fair&rdquo; = the dollars resting on the book at prices that still beat the model. Fairs are the exact-rank quadrature on the <strong>Sep 15 finals</strong> (σ<sub>rel</sub> 2%/day, T = 11 / 75). Rank order = RV at the executable price, then book depth, then the account&rsquo;s existing exposure. <strong>Read the honesty line under the table before acting: rows #1–#3 are one factor.</strong></span>
        </div>
        <div class="table-wrapper">
          <table class="pm-table pm-bestbets-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Bet</th>
                <th class="col-num">Touch</th>
                <th class="col-num">Model fair</th>
                <th class="col-num">Edge (pts)</th>
                <th class="col-num" title="Model value ÷ executable price · (÷ mid)">RV @ touch (mid)</th>
                <th class="col-num">$ at fair</th>
                <th>Book</th>
                <th>The ticket</th>
                <th>Why it ranks here</th>
              </tr>
            </thead>
            <tbody id="pm-bestbets-body">
              <tr class="pm-bb-top">
                <td><span class="pm-badge pm-cheap">#1</span></td>
                <td class="pm-co pm-mkt"><span class="dir-badge dir-long">BUY YES</span> <a href="https://polymarket.com/event/largest-company-end-of-december-2026" target="_blank" rel="noopener">Apple largest company · Dec 31<span class="pm-ext">↗</span></a></td>
                <td class="col-num pm-odds" data-bb-touch="dec-AAPL">23.9¢</td>
                <td class="col-num">34.77%</td>
                <td class="col-num pm-pos">−10.87</td>
                <td class="col-num pm-pos">1.45× (1.46×)</td>
                <td class="col-num">$41,805</td>
                <td><span class="pm-badge pm-cheap">DEEP</span> <span class="pm-note">$625 at the touch · $1,774 inside fair−5 · $37,940 of it is a two-level wall at 34.4–34.5¢</span></td>
                <td><strong>$300 cap, lift asks ≤ 25¢</strong> — fills at ONE level tonight: 23.9¢ × 1,255 sh. Stop: retire on fair &lt; mid + 5. New position — the account holds none.</td>
                <td>The widest edge on a real book, and the fair is the most robust number on the tab: 32.6 / 34.8 / 35.2 / 35.0 at σ 1.5 / 2 / 2.5 / 3%/day, so the market&rsquo;s 23.85 needs σ<sub>rel</sub> ≈ 0.88%/day to be right — the last six closes (Sep 8–15) realized ~1.75% pair-implied. 75 trading days for a 5.51% gap.</td>
              </tr>
              <tr>
                <td><span class="pm-badge pm-cheap">#2</span></td>
                <td class="pm-co pm-mkt"><span class="dir-badge dir-long">HOLD · ADD YES</span> <a href="https://polymarket.com/event/largest-company-end-of-september-1785358369147" target="_blank" rel="noopener">Apple largest company · Sep 30<span class="pm-ext">↗</span></a></td>
                <td class="col-num pm-odds" data-bb-touch="sep-crownAAPL">12.7¢</td>
                <td class="col-num">20.94%</td>
                <td class="col-num pm-pos">−8.24</td>
                <td class="col-num pm-pos">1.65× (1.66×)</td>
                <td class="col-num">$4,726</td>
                <td><span class="pm-badge pm-fair">OK</span> <span class="pm-note">$59 at 12.7, $2,101 inside fair−5 · twin: NVIDIA-crown NO at 13.0¢ (RV 1.61×, $561 at one level, $8,378 of bids ≥ fair)</span></td>
                <td><strong>HOLD the 22,532 sh (5.86¢ avg, +$1,518 open) — ADD $100 cap ≤ 13.0¢</strong> (≈782 sh, VWAP 12.8¢ over four levels). For size past $100 use the NVIDIA-crown NO leg at 13.0¢ flat instead of walking the Apple asks.</td>
                <td>The best multiple on the tab — but it is already the tab&rsquo;s biggest position, and the number is less robust than #1: 14.1 / 20.9 / 25.8 / 29.2 across the same σ sweep (break-even σ 1.41%/day). Eleven trading days for a 5.51% gap: a coin the model calls 21% and the market 12.6.</td>
              </tr>
              <tr>
                <td><span class="pm-badge pm-rich">#3</span></td>
                <td class="pm-co pm-mkt"><span class="dir-badge dir-short">BUY NO</span> <a href="https://polymarket.com/event/largest-company-end-of-december-2026" target="_blank" rel="noopener">NVIDIA largest company · Dec 31<span class="pm-ext">↗</span></a></td>
                <td class="col-num pm-odds" data-bb-touch="dec-NVDA">68.0 / 69.0</td>
                <td class="col-num">57.90% <span class="pm-note">(NO 42.10)</span></td>
                <td class="col-num">+10.60</td>
                <td class="col-num">NO 1.32× (1.34×)</td>
                <td class="col-num">$2,928</td>
                <td><span class="pm-badge pm-cheap">DEEP</span> <span class="pm-note">$164 of YES bids at 68, $1,843 at ≥65 — sell YES / buy NO at 32¢</span></td>
                <td><strong>FIRST: cancel the 72¢ GTC bid</strong> — it rests 14.1 points ABOVE fair and would fill at RV 0.80×. Then, only if you want the NO-side book: <strong>$100 cap, NO ≤ 35¢</strong> (≈312 sh at 32¢).</td>
                <td>Same thesis as #1 (NVIDIA loses the crown) with a worse multiple, because NO also pays on the Alphabet/Microsoft legs the model prices at 6.6 combined. It ranks for the chore, not the ticket: the resting 72¢ bid is the one live order on this tab that contradicts the model.</td>
              </tr>
              <tr>
                <td><span class="pm-badge pm-rich">#4</span></td>
                <td class="pm-co pm-mkt"><span class="dir-badge dir-short">SELL YES</span> <a href="https://polymarket.com/event/3rd-largest-company-end-of-september-1785358369147" target="_blank" rel="noopener">Microsoft 3rd place · Sep 30<span class="pm-ext">↗</span></a></td>
                <td class="col-num pm-odds" data-bb-touch="sep-sep3MSFT">4.5¢ bid</td>
                <td class="col-num">2.62%</td>
                <td class="col-num">+1.88</td>
                <td class="col-num">0.58× (0.58×)</td>
                <td class="col-num">$91</td>
                <td><span class="pm-badge pm-watch">THIN</span> <span class="pm-note">1,982 sh bid at 4.5¢ — absorbs the whole position seven times over</span></td>
                <td><strong>SELL all 274.11 sh at 4.5¢ — one print, $12.34</strong> (7.29¢ basis, −$7.6 realized). Microsoft needs to pass Alphabet (12.1% below it) in eleven sessions.</td>
                <td>Small, but the only held leg on the tab priced at 0.58× its model value with a bid that takes all of it. Inside the ±5 verdict band, so the table calls it FAIR — RV is why it is here.</td>
              </tr>
              <tr>
                <td><span class="pm-badge pm-watch">watch</span></td>
                <td class="pm-co pm-mkt"><span class="dir-badge dir-long">YES</span> <a href="https://polymarket.com/event/2nd-largest-company-end-of-september-20260729222928263" target="_blank" rel="noopener">NVIDIA 2nd place · Sep 30<span class="pm-ext">↗</span></a></td>
                <td class="col-num pm-odds" data-bb-touch="sep-sep2NVDA">14.3¢</td>
                <td class="col-num">20.87%</td>
                <td class="col-num pm-pos">−6.57</td>
                <td class="col-num pm-pos">1.46× (1.61×)</td>
                <td class="col-num">$106</td>
                <td><span class="pm-badge pm-watch">THIN · WIDE</span> <span class="pm-note">11.6 / 14.3 — $58 of asks under 16¢</span></td>
                <td><strong>No ticket.</strong> The account already holds 1,009.68 sh at 4.95¢ (+$80.8 open). The same event as #2 at a worse price on a book that cannot take $100.</td>
                <td>Listed so nobody buys it thinking it is a second idea: NVIDIA finishing 2nd ≈ Apple finishing 1st (20.87 vs 20.94). The seat&rsquo;s other side — sep2AAPL 84.5 vs 77.75 RICH — is the same coin again, on a 5-point-wide book with $791 of bids above fair.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="pm-footnote" data-longform="3" data-longform-label="Read the full honesty line"><strong>The honesty line.</strong> #1, #2, #3 and the watch row are ONE factor — the NVIDIA–Apple market-cap spread (5.51% / $268.0B at the Sep 15 close) — at two horizons (Sep 30, Dec 31). A portfolio of all of them is one bet, and it is a bet the account already carries: 22,532 sh of the September Apple crown (basis $1,320, marked $2,839) plus the NVIDIA-2nd and NVIDIA-crown-NO scraps — ~$3,020 of the tab&rsquo;s book on this spread before a dollar of tonight&rsquo;s tickets. That is why #1 (the December leg, no exposure yet, the most σ-robust fair) outranks #2 (the better multiple, the bigger existing position, the less robust fair). The model is a driftless pairwise lognormal with σ<sub>rel</sub> 2%/day and no view on earnings, product cycles or the AI-capex tape; if you believe NVIDIA drifts up against Apple, every CHEAP here is smaller than printed — the σ sweep shows how much of each edge survives a different volatility, none of it survives a directional view. Sizing: the caps above are what the book absorbs inside fair−5 without moving the touch, scaled to a tab whose held legs mark ~$3.3k; they are not a percent-of-portfolio rule. <strong>Chores, not bets:</strong> cancel the dec-NVDA 72¢ GTC (row #3); the three Dec YES scraps the model prices at zero — SpaceX 53,096 sh (marked $265; the bids under it pay $96 for the first 30,154 sh and 0.2¢ for the rest), Aramco 36,795 sh ($55), Amazon 2,533 sh ($4) — are $324 of marks with no model support and a bid stack that returns less than half of it: sell the SpaceX top two levels, leave the dust. <strong>Not walked / not re-trued tonight:</strong> the account&rsquo;s balances, the ledgers (61 Sep 10–14 fills still owed) and the Aug 28 idea cards keep their stamps; the leaderboard&rsquo;s top 50 is unchanged (every Largest-Company RV below is under its 2.00× cut) and its Analysis-row citations now read off this bake. Prices from the CLOB only; no trades placed.</p>
      </section>
'''
rep('''        <div class="kpi-card" data-accent="slate"><div class="kpi-label">AAPL · Sep 30 crown</div><div class="kpi-value" data-odds-kpi="sep-crownAAPL">12.6%</div></div>
      </section>

      <!-- ===================== TOP TRADES ===================== -->''',
    '''        <div class="kpi-card" data-accent="slate"><div class="kpi-label">AAPL · Sep 30 crown</div><div class="kpi-value" data-odds-kpi="sep-crownAAPL">12.6%</div></div>
      </section>
''' + BEST + '''
      <!-- ===================== TOP TRADES ===================== -->''')

# ---------------------------------------------------------------- Top Trades: point the Aug 28 #1 card at the re-priced ticket
rep('<span class="pm-sec-date">Ideas as of Aug 28, 2026 · 3:47 PM PT (Friday post-close walk)</span>\n          <span class="price-note" data-longform="2" data-longform-label="Read the full note">Ranked by <strong>dollars tradeable at a price that still beats fair</strong>',
    '<span class="pm-sec-date">Ideas as of Aug 28, 2026 · 3:47 PM PT (Friday post-close walk) · #1 re-priced Sep 16, 2026 01:45Z — see Best Bets above</span>\n          <span class="price-note" data-longform="2" data-longform-label="Read the full note"><strong>Sep 16 01:45Z:</strong> the #1 ticket&rsquo;s ≤23.70¢ limit is now UNDER the market (touch 23.9¢) — the live version is Best Bets #1 ($300 cap ≤ 25¢, fair 34.77); every other card keeps its Aug 28 stamp and has not been re-walked · Ranked by <strong>dollars tradeable at a price that still beats fair</strong>')
rep('<div class="pm-idea-date">Idea added Aug 28, 2026 <a class="pm-card-link" href="https://polymarket.com/event/largest-company-end-of-december-2026" target="_blank" rel="noopener" title="Open this market on Polymarket">View on Polymarket ↗</a></div>\n            <p>The season&rsquo;s biggest edge arrives with the season&rsquo;s cleanest paperwork:',
    '<div class="pm-idea-date">Idea added Aug 28, 2026 <span class="pm-reviewed">· Re-priced Sep 16, 2026</span><a class="pm-card-link" href="https://polymarket.com/event/largest-company-end-of-december-2026" target="_blank" rel="noopener" title="Open this market on Polymarket">View on Polymarket ↗</a></div>\n            <p><strong>Sep 16 01:45Z re-mark:</strong> the market walked 14.35 → 23.9¢ while the fair climbed 23.70 → 34.77 on the Sep 15 finals, so the ≤23.70¢ limit written here never fills again — the ticket is re-written in Best Bets #1 ($300 cap, lift ≤ 25¢, 1,255 sh at the 23.9¢ touch; RV 1.45×; $41.8k of asks at or under fair). Everything below is the Aug 28 text, kept for the record. The season&rsquo;s biggest edge arrives with the season&rsquo;s cleanest paperwork:')

# ---------------------------------------------------------------- Analysis table note (prepend)
rep('<span class="price-note" id="table-note" data-longform="2" data-longform-label="Read the full note">Model: exact-rank quadrature/MC on the cap diffusion, σ<sub>rel</sub> = 2%/day · caps = <strong>the Sep 15 closes (history pages, fetched ~23:2xZ',
    '<span class="price-note" id="table-note" data-longform="2" data-longform-label="Read the full note"><strong>Sep 16 01:45Z: every row below is re-marked to tonight&rsquo;s walk — twenty books, the September crown / seat / 3rd-place partitions included for the first time since Sep 1 — and the Sep 15 finals are SETTLED (two sources; MSFT revised $496.91 → $497.12, −1.64%, cap $3,692.8B; NVDA / AAPL / GOOGL / AMZN to the cent): Dec fairs 57.90 / 34.77 / 5.87 / 0.71 / 0.00, crown 79.03 / 20.94 / 0.03, seat 77.75-AAPL / 20.87-NVDA / 1.38-GOOGL, 3rd 95.97-GOOGL / 2.62-MSFT / 1.31-AAPL / 0.10-NVDA (the MSFT revision moves only the sub-point legs). Tradeable-at-fair is the FULL ladder tonight (every level at or beating the model), not the 5-point lower bound of the Sep 15 PM pass.</strong> · Model: exact-rank quadrature/MC on the cap diffusion, σ<sub>rel</sub> = 2%/day · caps = <strong>the Sep 15 closes (history pages, fetched ~23:2xZ')

# ---------------------------------------------------------------- September group row + rows
rep('''<tr class="pm-group"><td colspan="10">SEPTEMBER 30 · T = 11 trading days · odds re-marked to the <strong>Sep 15 01:10Z interactive walk</strong> where the book was walked (sep3NVDA was; the crown and seat books were NOT — their color stays Sep 1-stale and says so), fairs re-run on the <strong>Sep 15 closes</strong>''',
    '''<tr class="pm-group"><td colspan="10">SEPTEMBER 30 · T = 11 trading days · <strong>Sep 16 01:45Z: the crown, seat and 3rd-place books are WALKED</strong> — Apple-crown 12.6 vs 20.94 CHEAP (RV 1.66×, $4,726 of asks at or under fair — Best Bets #2), NVIDIA-crown 87.15 vs 79.03 RICH (the same coin: $8,378 of bids above fair), the seat inverted — sep2AAPL 84.5 vs 77.75 RICH on a 5-point-wide book, sep2NVDA 12.95 vs 20.87 CHEAP on $106 of asks; Alphabet-3rd 93.0 vs 95.97 inside the band, Microsoft-3rd 4.55 vs 2.62 RICH by multiple (0.58×) though inside the ±5 band — the account&rsquo;s 274 sh are Best Bets #4 · <em>the Sep 15 PM context, kept:</em> odds had been re-marked to the <strong>Sep 15 01:10Z interactive walk</strong> where the book was walked (sep3NVDA was; the crown and seat books were NOT), fairs re-run on the <strong>Sep 15 closes</strong>''')
rep('''<tr><td class="pm-co">NVIDIA <span class="pm-note">(3rd place)</span></td><td class="col-num pm-note">—</td><td class="col-num pm-note">—</td><td class="col-num pm-odds" data-odds="sep-sep3NVDA">0.05%</td><td class="col-num" data-fair="sep-sep3NVDA">0.10%</td><td class="col-num" data-edge="sep-sep3NVDA">−0.05</td><td class="col-num" data-pm-rv>2.00×</td><td class="col-num"><span class="pm-badge pm-fair">$0</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep3NVDA">FAIR</span></td><td class="col-num">—</td></tr>''',
    '''<tr><td class="pm-co">NVIDIA <span class="pm-note">(crown · #1)</span></td><td class="col-num" data-cap="NVDA-sep">5,134.5</td><td class="col-num" data-gap="NVDA-sep">—</td><td class="col-num pm-odds" data-odds="sep-crownNVDA">87.15%</td><td class="col-num" data-fair="sep-crownNVDA">79.03%</td><td class="col-num" data-edge="sep-crownNVDA">+8.12</td><td class="col-num" data-pm-rv>0.91×</td><td class="col-num"><span class="pm-badge pm-rich">$8,378</span></td><td><span class="pm-badge pm-rich" data-verdict="sep-crownNVDA">RICH</span></td><td class="col-num">—</td></tr>
              <tr><td class="pm-co">Apple <span class="pm-note">(crown · #1)</span></td><td class="col-num" data-cap="AAPL-sep">4,866.5</td><td class="col-num" data-gap="AAPL-sep">−5.22%</td><td class="col-num pm-odds" data-odds="sep-crownAAPL">12.6%</td><td class="col-num" data-fair="sep-crownAAPL">20.94%</td><td class="col-num" data-edge="sep-crownAAPL">−8.34</td><td class="col-num pm-pos" data-pm-rv>1.66×</td><td class="col-num"><span class="pm-badge pm-cheap">$4,726</span></td><td><span class="pm-badge pm-cheap" data-verdict="sep-crownAAPL">CHEAP</span></td><td class="col-num">—</td></tr>
              <tr><td class="pm-co">Apple <span class="pm-note">(2nd place)</span></td><td class="col-num pm-note">—</td><td class="col-num pm-note">—</td><td class="col-num pm-odds" data-odds="sep-sep2AAPL">84.5%</td><td class="col-num" data-fair="sep-sep2AAPL">77.75%</td><td class="col-num" data-edge="sep-sep2AAPL">+6.75</td><td class="col-num" data-pm-rv>0.92×</td><td class="col-num"><span class="pm-badge pm-rich">$791</span></td><td><span class="pm-badge pm-rich" data-verdict="sep-sep2AAPL">RICH</span> <span class="pm-note">82 / 87 — WIDE</span></td><td class="col-num">—</td></tr>
              <tr><td class="pm-co">NVIDIA <span class="pm-note">(2nd place)</span></td><td class="col-num pm-note">—</td><td class="col-num pm-note">—</td><td class="col-num pm-odds" data-odds="sep-sep2NVDA">12.95%</td><td class="col-num" data-fair="sep-sep2NVDA">20.87%</td><td class="col-num" data-edge="sep-sep2NVDA">−7.92</td><td class="col-num pm-pos" data-pm-rv>1.61×</td><td class="col-num"><span class="pm-badge pm-watch">$106</span></td><td><span class="pm-badge pm-cheap" data-verdict="sep-sep2NVDA">CHEAP</span> <span class="pm-note">THIN · 11.6 / 14.3</span></td><td class="col-num">—</td></tr>
              <tr><td class="pm-co">Alphabet <span class="pm-note">(2nd place)</span></td><td class="col-num pm-note">—</td><td class="col-num pm-note">—</td><td class="col-num pm-odds" data-odds="sep-sep2GOOGL">1.65%</td><td class="col-num" data-fair="sep-sep2GOOGL">1.38%</td><td class="col-num" data-edge="sep-sep2GOOGL">+0.27</td><td class="col-num" data-pm-rv>0.84×</td><td class="col-num"><span class="pm-badge pm-fair">$0</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep2GOOGL">FAIR</span></td><td class="col-num">—</td></tr>
              <tr><td class="pm-co">Alphabet <span class="pm-note">(3rd place)</span></td><td class="col-num pm-note">—</td><td class="col-num pm-note">—</td><td class="col-num pm-odds" data-odds="sep-sep3GOOGL">93.0%</td><td class="col-num" data-fair="sep-sep3GOOGL">95.97%</td><td class="col-num" data-edge="sep-sep3GOOGL">−2.97</td><td class="col-num" data-pm-rv>1.03×</td><td class="col-num"><span class="pm-badge pm-fair">$5,320</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep3GOOGL">FAIR</span></td><td class="col-num">—</td></tr>
              <tr><td class="pm-co">Microsoft <span class="pm-note">(3rd place)</span></td><td class="col-num pm-note">—</td><td class="col-num pm-note">—</td><td class="col-num pm-odds" data-odds="sep-sep3MSFT">4.55%</td><td class="col-num" data-fair="sep-sep3MSFT">2.62%</td><td class="col-num" data-edge="sep-sep3MSFT">+1.93</td><td class="col-num" data-pm-rv>0.58×</td><td class="col-num"><span class="pm-badge pm-fair">$91</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep3MSFT">FAIR</span> <span class="pm-note">held 274 sh — Best Bets #4</span></td><td class="col-num">—</td></tr>
              <tr><td class="pm-co">Apple <span class="pm-note">(3rd place)</span></td><td class="col-num pm-note">—</td><td class="col-num pm-note">—</td><td class="col-num pm-odds" data-odds="sep-sep3AAPL">1.6%</td><td class="col-num" data-fair="sep-sep3AAPL">1.31%</td><td class="col-num" data-edge="sep-sep3AAPL">+0.29</td><td class="col-num" data-pm-rv>0.82×</td><td class="col-num"><span class="pm-badge pm-fair">$0</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep3AAPL">FAIR</span></td><td class="col-num">—</td></tr>
              <tr><td class="pm-co">NVIDIA <span class="pm-note">(3rd place)</span></td><td class="col-num pm-note">—</td><td class="col-num pm-note">—</td><td class="col-num pm-odds" data-odds="sep-sep3NVDA">0.25%</td><td class="col-num" data-fair="sep-sep3NVDA">0.10%</td><td class="col-num" data-edge="sep-sep3NVDA">+0.15</td><td class="col-num" data-pm-rv>0.40×</td><td class="col-num"><span class="pm-badge pm-fair">$0</span></td><td><span class="pm-badge pm-fair" data-verdict="sep-sep3NVDA">FAIR</span> <span class="pm-note">bidless · 0.5¢ ask</span></td><td class="col-num">—</td></tr>''')

# ---------------------------------------------------------------- December group row + rows
rep('''<tr class="pm-group"><td colspan="10">DECEMBER 31 — 75 TRADING DAYS · fairs re-run on the <strong>Sep 15 closes</strong> (exact-rank quadrature + MC, pairwise σrel 2%/day, 0.75 small-leg allowance, calibration reproduces every Sep 12 fair exactly) · odds re-marked to the <strong>Sep 15 01:10Z walk</strong>''',
    '''<tr class="pm-group"><td colspan="10">DECEMBER 31 — 75 TRADING DAYS · <strong>Sep 16 01:45Z: odds re-marked to tonight&rsquo;s walk</strong> — dec-AAPL 23.85 vs 34.77 = −10.92 CHEAP (RV 1.46×; $625 at the 23.9¢ touch, $41,805 at or under fair — Best Bets #1), dec-NVDA 68.5 vs 57.90 = +10.60 RICH ($2,928 of bids above fair; the 72¢ GTC cancel is Best Bets #3), dec-GOOGL 6.5 vs 5.87 back to +0.63, dec-MSFT 0.55 vs 0.71 (fair +0.01 on the MSFT revision) · fairs re-run on the <strong>Sep 15 finals</strong> (exact-rank quadrature + MC, pairwise σrel 2%/day, 0.75 small-leg allowance, calibration reproduces every Sep 15 PM fair exactly) · <em>the Sep 15 PM context, kept:</em> odds had been re-marked to the <strong>Sep 15 01:10Z walk</strong>''')
rep('''<td class="col-num pm-odds" data-odds="dec-NVDA">68.5%</td><td class="col-num" data-fair="dec-NVDA">57.90%</td><td class="col-num" data-edge="dec-NVDA">+10.60</td><td class="col-num" data-pm-rv>0.85×</td><td class="col-num"><span class="pm-badge pm-rich">≥$3,054</span></td>''',
    '''<td class="col-num pm-odds" data-odds="dec-NVDA">68.5%</td><td class="col-num" data-fair="dec-NVDA">57.90%</td><td class="col-num" data-edge="dec-NVDA">+10.60</td><td class="col-num" data-pm-rv>0.85×</td><td class="col-num"><span class="pm-badge pm-rich">$2,928</span></td>''')
rep('''<td class="col-num pm-odds" data-odds="dec-AAPL">23.4%</td><td class="col-num" data-fair="dec-AAPL">34.77%</td><td class="col-num" data-edge="dec-AAPL">−11.37</td><td class="col-num" data-pm-rv>1.49×</td><td class="col-num"><span class="pm-badge pm-cheap">≥$1,757</span></td>''',
    '''<td class="col-num pm-odds" data-odds="dec-AAPL">23.85%</td><td class="col-num" data-fair="dec-AAPL">34.77%</td><td class="col-num" data-edge="dec-AAPL">−10.92</td><td class="col-num pm-pos" data-pm-rv>1.46×</td><td class="col-num"><span class="pm-badge pm-cheap">$41,805</span></td>''')
rep('''<td class="col-num pm-odds" data-odds="dec-GOOGL">7.5%</td><td class="col-num" data-fair="dec-GOOGL">5.87%</td><td class="col-num" data-edge="dec-GOOGL">+1.63</td><td class="col-num" data-pm-rv>0.78×</td><td class="col-num"><span class="pm-badge pm-fair">$68</span></td>''',
    '''<td class="col-num pm-odds" data-odds="dec-GOOGL">6.5%</td><td class="col-num" data-fair="dec-GOOGL">5.87%</td><td class="col-num" data-edge="dec-GOOGL">+0.63</td><td class="col-num" data-pm-rv>0.90×</td><td class="col-num"><span class="pm-badge pm-fair">$477</span></td>''')
rep('''<td class="col-num" data-cap="MSFT-dec">3,691.3</td><td class="col-num" data-gap="MSFT-dec">−28.11%</td><td class="col-num pm-odds" data-odds="dec-MSFT">0.55%</td><td class="col-num" data-fair="dec-MSFT">0.70%</td><td class="col-num" data-edge="dec-MSFT">−0.15</td><td class="col-num" data-pm-rv>1.27×</td><td class="col-num"><span class="pm-badge pm-fair">$0</span></td>''',
    '''<td class="col-num" data-cap="MSFT-dec">3,692.8</td><td class="col-num" data-gap="MSFT-dec">−28.08%</td><td class="col-num pm-odds" data-odds="dec-MSFT">0.55%</td><td class="col-num" data-fair="dec-MSFT">0.71%</td><td class="col-num" data-edge="dec-MSFT">−0.16</td><td class="col-num" data-pm-rv>1.29×</td><td class="col-num"><span class="pm-badge pm-fair">$10</span></td>''')
rep('''<td class="col-num pm-odds" data-odds="dec-AMZN">0.15%</td><td class="col-num" data-fair="dec-AMZN">0%</td><td class="col-num" data-edge="dec-AMZN">+0.15</td><td class="col-num" data-pm-rv>0.00×</td><td class="col-num"><span class="pm-badge pm-fair">$2</span></td>''',
    '''<td class="col-num pm-odds" data-odds="dec-AMZN">0.15%</td><td class="col-num" data-fair="dec-AMZN">0%</td><td class="col-num" data-edge="dec-AMZN">+0.15</td><td class="col-num" data-pm-rv>0.00×</td><td class="col-num"><span class="pm-badge pm-fair">$0</span></td>''')

# ---------------------------------------------------------------- Analysis footnote (prepend)
rep('<p class="pm-footnote" data-longform="4" data-longform-label="Read the full analysis"><strong>The caps are the Sep 15 closes, and the odds are a walked book again — one session apart</strong>',
    '<p class="pm-footnote" data-longform="4" data-longform-label="Read the full analysis"><strong>Sep 16 01:45Z — the twenty-book walk.</strong> Every Largest-Company book on this tab (five Dec names plus the SpaceX / Tesla / Aramco tails at 0.5 / 0.15 / 0.15 — the small-leg allowance of 0.75 re-read off their own books and unchanged; the September crown, seat and 3rd-place partitions) was pulled through the reader&rsquo;s Chrome 01:44–01:46Z with cache-busted /book calls, asset_id and timestamp validated (oldest 1.3 minutes). The Sep 15 finals were re-verified against stockanalysis history pages AND CNBC&rsquo;s quote service: MSFT settled at <strong>$497.12 (−1.64%)</strong>, not the $496.91 the PM pass pulled at 23:2xZ — the Sep 12 lesson again, a same-evening pull preceding the settled final; the other four held to the cent. Calibration first (the model reproduces every Sep 15 PM fair exactly on the PM inputs), then the revision: MSFT cap $3,692.8B, Dec MSFT 0.70 → 0.71, 3rd-place GOOGL 96.01 → 95.97 / MSFT 2.58 → 2.62, everything else unchanged. The fresh mids move three things: <strong>dec-AAPL&rsquo;s edge tightens −11.37 → −10.92 (23.4 → 23.85) with RV 1.49× → 1.46× — still the widest edge on a deep book</strong>; <strong>the September crown prints its first walked edge since Sep 1 — Apple 12.6 vs 20.94 (−8.34, RV 1.66×), NVIDIA 87.15 vs 79.03 (+8.12)</strong>, the four walked legs summing to 99.95 with Alphabet at 0.15 and Microsoft bidless at a 0.1¢ ask; and the seat, walked for the first time since the 81.5 stale mid, sits at 84.5 / 12.95 / 1.65 — sep2AAPL +6.75 RICH on a 5-point spread, sep2NVDA −7.92 CHEAP on $106 of asks. dec-GOOGL 6.5 vs 5.87 falls back inside the band (+0.63). The Best Bets block above ranks what is actionable; this table is the whole board. <strong>The Sep 15 PM text follows, kept for the record.</strong> <strong>The caps are the Sep 15 closes, and the odds are a walked book again — one session apart</strong>')

# ---------------------------------------------------------------- sync chronicle: Latest line + new segment
rep('<strong>Latest: Sep 15 23:5xZ — Largest-Company re-baked on the Sep 15 close (two closes ingested), odds re-marked to the Sep 15 01:10Z walk; tab bakes: Oil Sep 10, Treasuries Sep 9 close, Largest-Company Sep 15, Bitcoin Sep 1, Iran Sep 1; Leaderboard re-marked Sep 15 01:10Z.</strong>',
    '<strong>Latest: Sep 16 01:45Z — Largest-Company re-walked (20 books incl. the September crown / seat / 3rd partitions, first since Sep 1), Sep 15 finals settled (MSFT revised $497.12), fairs re-run, a ranked BEST BETS block added to the tab (#1 dec-AAPL YES 23.9¢ vs 34.77, #2 hold/add Sep Apple crown 12.7¢ vs 20.94, #3 cancel the dec-NVDA 72¢ GTC, #4 sell the 274-sh Microsoft-3rd leg); tab bakes: Oil Sep 10, Treasuries Sep 9 close, Largest-Company Sep 16 01:45Z, Bitcoin Sep 1, Iran Sep 1; Leaderboard re-marked Sep 15 01:10Z (top 50 unchanged by tonight&rsquo;s walk).</strong>')
rep('''no tab besides Largest-Company re-baked. No trades placed.</span> <span id="sync-ago" class="pm-sync-ago"></span></span>''',
    '''no tab besides Largest-Company re-baked. No trades placed.</span> <strong>Sep 16 01:45Z interactive: the Largest-Company complex WALKED — twenty CLOB books through the reader&rsquo;s Chrome (01:44–01:46Z, asset_id + timestamp validated), the Sep 15 finals re-verified against two sources (MSFT settled $497.12 / −1.64%, revised from the PM pass&rsquo;s $496.91; cap $3,692.8B), calibration reproduced every Sep 15 PM fair, fairs re-ran (Dec 57.90 / 34.77 / 5.87 / 0.71; crown 79.03 / 20.94; seat 77.75 / 20.87; 3rd 95.97-GOOGL / 2.62-MSFT). Fresh edges: dec-AAPL 23.85 vs 34.77 −10.92 CHEAP (RV 1.46×, $41.8k of asks at or under fair), Apple-crown 12.6 vs 20.94 −8.34 CHEAP (RV 1.66× — first crown walk since Sep 1), NVIDIA-crown 87.15 vs 79.03 +8.12 RICH, sep2AAPL 84.5 vs 77.75 +6.75 RICH (WIDE), sep2NVDA 12.95 vs 20.87 −7.92 CHEAP (THIN $106), dec-NVDA +10.60 RICH unchanged. NEW on the tab: a ranked Best Bets block (#1 BUY dec-AAPL YES $300 cap ≤ 25¢; #2 HOLD the 22,532-sh Sep Apple crown, ADD $100 cap ≤ 13.0¢; #3 CANCEL the dec-NVDA 72¢ GTC, optional NO $100 ≤ 35¢; #4 SELL the 274-sh Microsoft-3rd leg at 4.5¢) with the one-factor honesty line. Nine September rows added to the Analysis table. Untouched + disclosed: balances, ledgers (61 fills owed), Aug 28 cards, velocity, charts; Leaderboard top 50 unchanged (every Largest-Company RV under the 2.00× cut). Prices from the CLOB only; no trades placed.</strong> <span id="sync-ago" class="pm-sync-ago"></span></span>''')

# ---------------------------------------------------------------- Leaderboard: KPI count + brief note
rep('<div class="kpi-label">Rows ranked / carrying RV</div><div class="kpi-value">50 / 145</div>',
    '<div class="kpi-label">Rows ranked / carrying RV</div><div class="kpi-value">50 / 154</div>')
rep('The model values are NOT re-baked — that is what “relative value” means here: the Analysis fairs are the Sep 12 quadrature on the Sep 11 closes,',
    '<strong>Sep 16 01:45Z note:</strong> the Largest-Company tab re-baked on the Sep 15 finals and a fresh twenty-book walk (nine September rows added to its table, 145 → 154 rows carrying RV); its best lines — Sep Apple crown 1.66×, dec-AAPL 1.46×, sep2NVDA 1.61× on a $106 book — all sit UNDER this board&rsquo;s 2.00× cut, so the top 50 below is unchanged; the &ldquo;best unconditional lines below the cut&rdquo; are now those, and the two Analysis figures quoted in the footnote (dec-AAPL 1.31×, dec-MSFT 1.02×) read 1.46× / 1.29× on the Sep 16 bake. The model values are NOT re-baked — that is what “relative value” means here: the Analysis fairs (as ranked on Sep 15) are the Sep 12 quadrature on the Sep 11 closes,')

open(P, 'w', encoding='utf-8').write(h)
print('index.html edits applied:', n_edits)

# ---------------------------------------------------------------- polymarket.js: TOKENS for the new rows + sums.dec allowance
J = REPO + '/polymarket/polymarket.js'
js = open(J, encoding='utf-8').read()
old = "    'sep-sepGOOGL': '11286203532633435050461029087857565736892531921887062202100644346193481478173',\n"
assert js.count(old) == 1
new = old + """    /* Sep 16 2026: the rest of the September partitions + the two remaining Dec race names, so the
       Best Bets / Analysis rows added that night refresh live (gamma /events?slug= discovery, YES tokens) */
    'sep-crownNVDA': '23705583736348706533988510839759433821053113814025766422082583385077433681175',
    'sep-crownAAPL': '16478316053646921296729034019554519840110001466229869274618614366503964308841',
    'sep-sep2MSFT': '55280273017462604050110364006593514037065825484513723750243853675453069122185',
    'sep-sep3GOOGL': '105940453485945394790582500621710713657132376521484683541477221278559910577368',
    'sep-sep3MSFT': '46552579038506701209087110814172553391939526036683166770317364680747842791908',
    'dec-MSFT': '391670908629060088409431896998377161667071768186645889213963384874929102170',
    'dec-AMZN': '23899766443614969608658296541413892746074395565401020148911064394383451718287',
"""
js = js.replace(old, new)
old2 = "var sums = { jul: 0.0015, aug: 0.0045, dec: 0.0030 }; /* untracked legs at their own mids: aug = TSLA+ARAMCO+MSFT 0.15c each; dec = ARAMCO 0.15 + AMZN 0.15 (re-read Aug 23 13:22Z off their own books) */"
assert js.count(old2) == 1
js = js.replace(old2, "var sums = { jul: 0.0015, aug: 0.0045, dec: 0.0015 }; /* untracked legs at their own mids: aug = TSLA+ARAMCO+MSFT 0.15c each; dec = ARAMCO 0.15 only — AMZN joined TOKENS Sep 16 2026 and is summed live (re-read Sep 16 01:45Z off its own book: 0.15) */")
open(J, 'w', encoding='utf-8').write(js)
print('polymarket.js: TOKENS +7, sums.dec allowance updated')

# ---------------------------------------------------------------- polymarket.css: best-bets styling
C = REPO + '/polymarket/polymarket.css'
css = open(C, encoding='utf-8').read()
marker = '/* ---- best bets (Sep 16 2026) ---- */'
if marker not in css:
    css += '''
''' + marker + '''
.pm-bestbets { border: 1px solid var(--color-gain-border); border-left: 4px solid var(--color-gain); border-radius: var(--radius-md, 10px); padding: var(--space-3) var(--space-4); background: var(--color-surface); }
.pm-bestbets .section-title { white-space: normal; }
.pm-bestbets .pm-sec-date { white-space: normal; }
.pm-bestbets .price-note { white-space: normal; }
.pm-bestbets-table td { vertical-align: top; white-space: normal; font-size: var(--text-sm); line-height: 1.5; }
.pm-bestbets-table td:nth-child(9), .pm-bestbets-table td:nth-child(10) { min-width: 220px; max-width: 360px; }
.pm-bestbets-table tr.pm-bb-top td { background: var(--color-gain-bg); }
.pm-bestbets-table .pm-note { display: block; font-weight: 400; margin-top: 2px; }
.pm-bestbets .pm-footnote { max-width: none; }
'''
    open(C, 'w', encoding='utf-8').write(css)
    print('polymarket.css: best-bets styles appended')
