#!/usr/bin/env python3
"""Sep 20 AM (Sunday morning) bake — the lock holds a THIRD pass; bitcoin
hands back the series high (-1.72%) but holds the $80k break a fourth
consecutive print, on TWO live sources (CoinGecko + Kraken; CMC discarded).
Surfaces: header tape (new AM segment), sync Latest replace + chronicle
append, Largest tape label tweak + hero-prose prepend + Next-Catalyst
prepend. Every replacement must hit exactly once."""
import io, re, sys

P = 'polymarket/index.html'
html = io.open(P, encoding='utf-8').read()
n0 = len(html)
edits = []

def rep(old, new, tag):
    global html
    c = html.count(old)
    assert c == 1, f"{tag}: expected 1 match, got {c}"
    html = html.replace(old, new)
    edits.append(tag)

# ---- 1. header tape: append the Sep 20 AM segment ----
TAPE = (" · <strong>Sep 20 13:3xZ — SUNDAY MORNING, THE LOCK HOLDS A THIRD PASS AND BITCOIN HANDS BACK THE "
 "HIGH BUT HOLDS $80K:</strong> autodata is down a <strong>FORTY-FIRST</strong> consecutive feed run (the "
 "Sep 20 12:45Z cron silent; this run&rsquo;s 13:08Z poke touching fetch/poke, 2cf12e7a, unanswered — the "
 "Actions disablement stands, one manual visit to github.com/chad506/Leadsure/actions revives it). The "
 "morning pass re-confirmed <strong>all five Sep 18 finals to the cent a THIRD consecutive session</strong> "
 "(NVDA $222.27 on 189,973,388 shares settled, AAPL $336.13, GOOGL $349.54, MSFT $493.78, AMZN $253.71; the "
 "Sep 17 finals re-confirmed beneath them a fourth session, the Sep 16 rows verified beneath those) and an "
 "independent quadrature re-run reproduced every published fair EXACTLY — lead 8.95% / $442.1B, cushion "
 "16.01% / $681.4B, T 8 / 72: <strong>the whole board rides into tomorrow&rsquo;s open exactly as "
 "published</strong> (the first close since the quad-witching breakout is now a day away). <strong>BTC "
 "HANDS BACK THE HIGH BUT HOLDS THE BREAK: $80,304.64</strong> (CoinGecko live, −1.2%/24h, range "
 "$80,155–$81,864; Kraken live cross $80,511.00, −0.95%/24h, ~0.26% over — <strong>two live sources "
 "again</strong> after Saturday&rsquo;s single-source night; CoinMarketCap&rsquo;s $81,287.92 &ldquo;+0.41%&rdquo; "
 "discarded — its 24h low of $80,814.94 sits above both live prints, snapshot-stale), <strong>−1.72% on "
 "the series-high print</strong>, −0.95% on the Sep 19 AM print, −1.14% vs the $80k-break print, still "
 "+2.41% over the Sep 1 bake — a FOURTH consecutive $80k+ print, and the tape&rsquo;s own 24h low "
 "($80,155) never gave the break back; T 102.6d: every residual vs the stale pre-breakout Sep 15 "
 "walk mids eases off Saturday&rsquo;s series wides but stays blown out ($85k −13.1, $90k −14.7, $95k "
 "−13.5, $100k −12.2, $110k −6.6; dips rich $60k +5.4, $55k +8.3, $50k +9.3; needed touch +5.8%) — labeled "
 "color, the BTC tab keeps its Sep 1 01:27Z stamps and its re-bake stays the loudest want on the page. "
 "Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. "
 "No trades placed.")
rep("its re-bake stays the loudest want on the page. Mids/books/balances keep "
    "the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.</span>",
    "its re-bake stays the loudest want on the page. Mids/books/balances keep "
    "the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed."
    + TAPE + "</span>", "tape-append")

# ---- 2a. sync Latest head replace ----
m = re.search(r"<strong>Latest: Sep 19 23:4xZ PM pass \(Saturday night\).*?Leaderboard re-marked Sep 15 01:10Z\.</strong>", html, re.S)
assert m, "Latest head not found"
LATEST = ("<strong>Latest: Sep 20 13:3xZ AM pass (Sunday) — the lock holds a third pass and bitcoin hands "
 "back the high but holds $80k: all five Sep 18 finals re-confirmed to the cent a THIRD consecutive "
 "session (NVDA&rsquo;s 190.0M settled volume holds; the Sep 17 finals a fourth session beneath them) and "
 "calibration reproduced every published fair EXACTLY (Dec 65.98 / 28.69, crown 93.52 / 6.48, seat "
 "93.09 / 6.47, 3rd 99.13 / 0.43, P(±5/wk) 60 / 58 / 4) — lead 8.95% / $442.1B, cushion 16.01%, T 8 / 72: "
 "every fair, badge and Best-Bet stance (Best Bets #1 STOOD DOWN, the crownAAPL hold rides, the sep3MSFT "
 "sell, the stale-ladder cheap trio queued for a re-walk) rides into tomorrow&rsquo;s open unchanged — the "
 "first close since the breakout is a day away. BTC $80,304.64 (CoinGecko live −1.2%/24h with a LIVE "
 "Kraken cross $80,511.00 ~0.26% over — two live sources again; CMC&rsquo;s snapshot discarded), −1.72% "
 "off Saturday&rsquo;s series high but a FOURTH consecutive $80k+ print (+2.41% over the Sep 1 bake), the "
 "24h low $80,155 holding above the break; residuals vs the pre-breakout Sep 15 walk mids ease off "
 "the wides but stay blown out ($90k −14.7) — the Bitcoin tab re-bake stays the loudest want. Autodata "
 "DOWN a 41st feed run; tab bakes: Oil Sep 10, Treasuries Sep 9 close, Largest-Company fairs Sep 18 "
 "23:1xZ on the Sep 16 01:45Z walk mids (finals locked Sep 19–20), Bitcoin Sep 1, Iran Sep 1; Leaderboard "
 "re-marked Sep 15 01:10Z.</strong>")
html = html[:m.start()] + LATEST + html[m.end():]
edits.append("latest-head")

# ---- 2b. sync chronicle append ----
CHRON = (" <strong>Sep 20 13:3xZ AM run (Sunday): the lock holds a third pass — all five Sep 18 finals "
 "re-confirmed to the cent a third consecutive session (the settled volume holds; the Sep 17 finals a "
 "fourth session), calibration reproduced every fair exactly, and the whole board — lead 8.95% / $442.1B, "
 "cushion 16.01%, T 8 / 72 — rides into tomorrow&rsquo;s open unchanged. BTC hands back the series high "
 "but holds the break: $80,304.64 (CoinGecko live −1.2%/24h; Kraken LIVE cross $80,511.00 ~0.26% over — "
 "two live sources after Saturday&rsquo;s single-source night; CMC&rsquo;s $81,287.92 snapshot discarded, "
 "its 24h low above both live prints), −1.72% on the high, −1.14% vs the $80k-break print, +2.41% over "
 "the Sep 1 bake — a fourth consecutive $80k+ print with the 24h low $80,155 holding above the break; "
 "T 102.6d — every residual vs the stale Sep 15 walk mids eases off the series wides but stays "
 "blown out ($85k −13.1, $90k −14.7, $95k −13.5, $100k −12.2, $110k −6.6; dips $60k +5.4, $55k +8.3, "
 "$50k +9.3), needed touch +5.8%. Autodata DOWN a FORTY-FIRST feed run (12:45Z cron silent; 13:08Z poke "
 "touching fetch/poke, 2cf12e7a, unanswered — the Actions-disablement diagnosis stands). "
 "Mids/books/balances keep the Sep 16 01:45Z stamps; the ledger still owes the 61 swept fills. "
 "No trades placed.</strong>")
rep("the 61 swept fills. No trades placed.</strong><span id=\"sync-ago\"",
    "the 61 swept fills. No trades placed.</strong>" + CHRON + "<span id=\"sync-ago\"",
    "chronicle-append")

# ---- 3a. Largest tape label tweak ----
rep("NVDA&rsquo;s $222.27 final LOCKED Sep 19 (morning check; the PM pass re-confirmed all five to the cent) — the table&rsquo;s $222.06 settled to the header overnight",
    "NVDA&rsquo;s $222.27 final LOCKED Sep 19 (re-confirmed to the cent through the Sep 20 morning pass — three consecutive sessions) — the table&rsquo;s $222.06 settled to the header overnight",
    "label-tweak")

# ---- 3b. hero prose prepend ----
HERO = ("<strong>SEP 20 13:3xZ AM (SUNDAY): THE LOCK HOLDS A THIRD PASS.</strong> The morning pass "
 "re-confirmed all five Sep 18 finals to the cent a <strong>third consecutive session</strong> "
 "(NVDA&rsquo;s settled 190.0M volume holds; the Sep 17 finals a fourth session beneath them) and "
 "reproduced every fair below EXACTLY — the board rides into tomorrow&rsquo;s open unchanged (T 8 / 72; "
 "the first close since the breakout is a day away). Off-board, bitcoin handed back Saturday&rsquo;s "
 "series high (−1.72% to $80,304.64) but held the $80k break a fourth consecutive print — pressure still "
 "on the Bitcoin tab&rsquo;s Sep 1 bake, not on these fairs. <em>Saturday text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>SEP 19 23:4xZ PM (SATURDAY NIGHT): THE LOCK HOLDS.",
    "data-longform-label=\"More\">" + HERO + "<strong>SEP 19 23:4xZ PM (SATURDAY NIGHT): THE LOCK HOLDS.",
    "hero-prepend")

# ---- 3c. Next-Catalyst prepend ----
NC = ("<strong>Sep 20 13:3xZ AM: Monday&rsquo;s open is a day away — nothing re-prices before it.</strong> "
 "Sunday morning Sep 20, T 8 / 72 — the finals locked three times over (five-for-five to the cent on all "
 "three passes, quadrature exact each time; autodata down a 41st feed run — the fix is still one visit to "
 "github.com/chad506/Leadsure/actions). The chore list stands, and the <strong>September re-walk queue "
 "and the Bitcoin tab re-bake</strong> (spot $80,304 after handing back the series high — every up-rung "
 "residual on the stale Sep 15 mids still blown out, $90k −14.7) still head it. "
 "<em>Saturday text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>Sep 19 23:4xZ PM: one weekend night down",
    "data-longform-label=\"More\">" + NC + "<strong>Sep 19 23:4xZ PM: one weekend night down",
    "nextcat-prepend")

io.open(P, 'w', encoding='utf-8').write(html)
print(f"OK — {len(edits)} edits applied: {edits}; {n0} → {len(html)} bytes (+{len(html)-n0})")
