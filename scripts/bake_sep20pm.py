#!/usr/bin/env python3
"""Sep 20 PM (Sunday night) bake — the lock holds a FOURTH pass on the eve of
the first post-breakout close; bitcoin firms off the morning (+0.65%) to a
fifth straight $80k+ print on THREE live sources (CoinGecko + Kraken +
Coinbase; CoinGecko's carried 24h range flagged, not discarded).
Surfaces: header tape (new PM segment), sync Latest replace + chronicle
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

# ---- 1. header tape: append the Sep 20 PM segment ----
TAPE = (" · <strong>Sep 20 23:3xZ — SUNDAY NIGHT, THE LOCK HOLDS A FOURTH PASS ON THE EVE OF THE FIRST "
 "POST-BREAKOUT CLOSE:</strong> autodata is down a <strong>FORTY-SECOND</strong> consecutive feed run (the "
 "Sep 20 22:45Z cron silent; this run&rsquo;s 23:07Z poke touching fetch/poke, ee9064d9, unanswered — the "
 "Actions disablement stands, one manual visit to github.com/chad506/Leadsure/actions revives it). The "
 "evening pass re-confirmed <strong>all five Sep 18 finals to the cent a FOURTH consecutive session</strong> "
 "(NVDA $222.27 on 189,973,388 shares settled, AAPL $336.13, GOOGL $349.54, MSFT $493.78, AMZN $253.71; the "
 "Sep 17 finals re-confirmed beneath them a fifth session, the Sep 16 rows verified beneath those; every "
 "history-page header still &ldquo;At close: Sep 18&rdquo;) and an independent quadrature re-run reproduced "
 "every published fair EXACTLY — lead 8.95% / $442.1B, cushion 16.01% / $681.4B, T 8 / 72: <strong>the whole "
 "board rides into tomorrow&rsquo;s open exactly as published — and tomorrow IS the first close since the "
 "quad-witching breakout</strong>. <strong>BTC FIRMS OFF THE MORNING — A FIFTH STRAIGHT $80K PRINT, ON THREE "
 "LIVE SOURCES: $80,827.29</strong> (CoinGecko live, −1.10%/24h; its 24h range $80,155–$81,864 carries the "
 "morning&rsquo;s extremes — both sit inside the two windows&rsquo; overlap, so flagged, not discarded; "
 "Kraken live $80,517.00, −0.85%/24h, ~0.38% under, with its own range $80,213–$81,850; Coinbase live "
 "$80,260.34, −1.23%/24h, ~0.70% under — three live reads at once, spread 0.71%, every one over $80k), "
 "<strong>+0.65% on the morning print</strong>, −1.08% on the series high, −0.49% vs the $80k-break print, "
 "+3.08% over the Sep 1 bake; T 102.2d: the firmer spot re-widens every residual vs the stale pre-breakout "
 "Sep 15 walk mids off the morning&rsquo;s easing, but all eight hold inside Saturday&rsquo;s series wides "
 "($85k −15.2, $90k −16.6, $95k −15.2, $100k −13.5, $110k −7.5; dips rich $60k +6.5, $55k +9.0, $50k +9.7; "
 "needed touch +5.2%) — labeled color, the BTC tab keeps its Sep 1 01:27Z stamps and its re-bake stays the "
 "loudest want on the page. Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger "
 "still owes its 61 fills. No trades placed.")
rep("needed touch +5.8%) — labeled color, the BTC tab keeps its Sep 1 01:27Z stamps and its re-bake stays "
    "the loudest want on the page. Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the "
    "ledger still owes its 61 fills. No trades placed.</span>",
    "needed touch +5.8%) — labeled color, the BTC tab keeps its Sep 1 01:27Z stamps and its re-bake stays "
    "the loudest want on the page. Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the "
    "ledger still owes its 61 fills. No trades placed."
    + TAPE + "</span>", "tape-append")

# ---- 2a. sync Latest head replace ----
m = re.search(r"<strong>Latest: Sep 20 13:3xZ AM pass \(Sunday\).*?Leaderboard re-marked Sep 15 01:10Z\.</strong>", html, re.S)
assert m, "Latest head not found"
LATEST = ("<strong>Latest: Sep 20 23:3xZ PM pass (Sunday night) — the lock holds a fourth pass on the eve of "
 "the first post-breakout close: all five Sep 18 finals re-confirmed to the cent a FOURTH consecutive "
 "session (NVDA&rsquo;s 190.0M settled volume holds; the Sep 17 finals a fifth session beneath them) and "
 "calibration reproduced every published fair EXACTLY (Dec 65.98 / 28.69, crown 93.52 / 6.48, seat "
 "93.09 / 6.47, 3rd 99.13 / 0.43, P(±5/wk) 60 / 58 / 4) — lead 8.95% / $442.1B, cushion 16.01%, T 8 / 72: "
 "every fair, badge and Best-Bet stance (Best Bets #1 STOOD DOWN, the crownAAPL hold rides, the sep3MSFT "
 "sell, the stale-ladder cheap trio queued for a re-walk) rides into tomorrow&rsquo;s open unchanged — and "
 "tomorrow IS the first close since the breakout. BTC $80,827.29 (CoinGecko live −1.10%/24h, with LIVE "
 "Kraken $80,517.00 and LIVE Coinbase $80,260.34 crosses — three live sources, spread 0.71%, every read "
 "over $80k; CoinGecko&rsquo;s 24h range carries the morning&rsquo;s extremes and is flagged), +0.65% off "
 "the morning print but −1.08% under Saturday&rsquo;s series high — a FIFTH consecutive $80k+ print "
 "(+3.08% over the Sep 1 bake); residuals vs the pre-breakout Sep 15 walk mids re-widen on the firmer spot "
 "but hold inside Saturday&rsquo;s wides ($90k −16.6) — the Bitcoin tab re-bake stays the loudest want. "
 "Autodata DOWN a 42nd feed run; tab bakes: Oil Sep 10, Treasuries Sep 9 close, Largest-Company fairs "
 "Sep 18 23:1xZ on the Sep 16 01:45Z walk mids (finals locked Sep 19–20), Bitcoin Sep 1, Iran Sep 1; "
 "Leaderboard re-marked Sep 15 01:10Z.</strong>")
html = html[:m.start()] + LATEST + html[m.end():]
edits.append("latest-head")

# ---- 2b. sync chronicle append ----
CHRON = (" <strong>Sep 20 23:3xZ PM run (Sunday night): the lock holds a fourth pass — all five Sep 18 "
 "finals re-confirmed to the cent a fourth consecutive session (the settled volume holds; the Sep 17 "
 "finals a fifth session), calibration reproduced every fair exactly, and the whole board — lead 8.95% / "
 "$442.1B, cushion 16.01%, T 8 / 72 — rides into tomorrow&rsquo;s open unchanged; tomorrow is the first "
 "close since the quad-witching breakout. BTC firms off the morning: $80,827.29 (CoinGecko live "
 "−1.10%/24h; LIVE Kraken $80,517.00 ~0.38% under and LIVE Coinbase $80,260.34 ~0.70% under — three live "
 "sources at once, spread 0.71%, every read over $80k; CoinGecko&rsquo;s 24h range carries the "
 "morning&rsquo;s extremes — both sit inside the two windows&rsquo; overlap — flagged, not discarded), "
 "+0.65% on the morning print, −1.08% on the series high, −0.49% vs the $80k-break print, +3.08% over the "
 "Sep 1 bake — a fifth consecutive $80k+ print; T 102.2d — the firmer spot re-widens every residual vs "
 "the stale Sep 15 walk mids off the morning&rsquo;s easing but all eight hold inside Saturday&rsquo;s "
 "series wides ($85k −15.2, $90k −16.6, $95k −15.2, $100k −13.5, $110k −7.5; dips $60k +6.5, $55k +9.0, "
 "$50k +9.7), needed touch +5.2%. Autodata DOWN a FORTY-SECOND feed run (22:45Z cron silent; 23:07Z poke "
 "touching fetch/poke, ee9064d9, unanswered — the Actions-disablement diagnosis stands). "
 "Mids/books/balances keep the Sep 16 01:45Z stamps; the ledger still owes the 61 swept fills. "
 "No trades placed.</strong>")
rep("the 61 swept fills. No trades placed.</strong><span id=\"sync-ago\"",
    "the 61 swept fills. No trades placed.</strong>" + CHRON + "<span id=\"sync-ago\"",
    "chronicle-append")

# ---- 3a. Largest tape label tweak ----
rep("re-confirmed to the cent through the Sep 20 morning pass — three consecutive sessions",
    "re-confirmed to the cent through the Sep 20 evening pass — four consecutive sessions",
    "label-tweak")

# ---- 3b. hero prose prepend ----
HERO = ("<strong>SEP 20 23:3xZ PM (SUNDAY NIGHT): THE LOCK HOLDS A FOURTH PASS — THE FIRST POST-BREAKOUT "
 "CLOSE IS TOMORROW.</strong> The evening pass re-confirmed all five Sep 18 finals to the cent a "
 "<strong>fourth consecutive session</strong> (the settled volume holds; the Sep 17 finals a fifth session "
 "beneath them) and reproduced every fair below EXACTLY — the board rides into Monday&rsquo;s open "
 "unchanged (T 8 / 72). Off-board, bitcoin firmed to $80,827.29 on three live sources — a fifth straight "
 "$80k+ print, still 1.1% under Saturday&rsquo;s high — pressure on the Bitcoin tab&rsquo;s Sep 1 bake, "
 "not on these fairs. <em>Sunday-morning text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>SEP 20 13:3xZ AM (SUNDAY): THE LOCK HOLDS A THIRD PASS.",
    "data-longform-label=\"More\">" + HERO + "<strong>SEP 20 13:3xZ AM (SUNDAY): THE LOCK HOLDS A THIRD PASS.",
    "hero-prepend")

# ---- 3c. Next-Catalyst prepend ----
NC = ("<strong>Sep 20 23:3xZ PM: tomorrow&rsquo;s open IS the catalyst — the first close since the "
 "quad-witching breakout.</strong> Sunday night Sep 20, T 8 / 72 — the finals locked four times over "
 "(five-for-five to the cent on every pass, quadrature exact each time; autodata down a 42nd feed run — "
 "the fix is still one visit to github.com/chad506/Leadsure/actions). The chore list stands: the "
 "<strong>September re-walk queue and the Bitcoin tab re-bake</strong> (spot $80,827 on three live "
 "sources — every up-rung residual on the stale Sep 15 mids re-widened, $90k −16.6) still head it, and "
 "Monday&rsquo;s close hands the model its first fresh input since the breakout. "
 "<em>Sunday-morning text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>Sep 20 13:3xZ AM: Monday&rsquo;s open is a day away",
    "data-longform-label=\"More\">" + NC + "<strong>Sep 20 13:3xZ AM: Monday&rsquo;s open is a day away",
    "nextcat-prepend")

io.open(P, 'w', encoding='utf-8').write(html)
print(f"OK — {len(edits)} edits applied: {edits}; {n0} → {len(html)} bytes (+{len(html)-n0})")
