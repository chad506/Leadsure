#!/usr/bin/env python3
"""Sep 21 AM (Monday pre-open) bake — the lock holds a FIFTH pass on the
morning of the first post-breakout close; the premarket leans WIDER (implied
lead 9.68% vs the finals' 8.95%); bitcoin firms to the door of the series
high (+0.98%, -0.11% under it) on a Kraken+Coinbase+CMC consensus that
catches and discards CoinGecko's first bad print of the series ($84,609
"+5.3%" with a claimed $85,046 24h high no exchange's own range shows).
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

# ---- 1. header tape: append the Sep 21 AM segment ----
TAPE = (" · <strong>Sep 21 13:3xZ — MONDAY PRE-OPEN, THE MORNING OF THE FIRST POST-BREAKOUT CLOSE: THE LOCK "
 "HOLDS A FIFTH PASS, THE PREMARKET LEANS WIDER:</strong> autodata is down a <strong>FORTY-THIRD</strong> "
 "consecutive feed run (the Sep 21 12:45Z cron silent; this run&rsquo;s 13:09Z poke touching fetch/poke, "
 "03f77c89, unanswered — the Actions disablement stands, one manual visit to "
 "github.com/chad506/Leadsure/actions revives it). The morning pass re-confirmed <strong>all five Sep 18 "
 "finals to the cent a FIFTH consecutive session</strong> (NVDA $222.27 on 189,973,388 shares settled, "
 "AAPL $336.13, GOOGL $349.54, MSFT $493.78, AMZN $253.71; the Sep 17 finals re-confirmed beneath them a "
 "sixth session, the Sep 16 rows verified beneath those; every history-page header still &ldquo;At close: "
 "Sep 18&rdquo;) and an independent quadrature re-run reproduced every published fair EXACTLY — lead "
 "8.95% / $442.1B, cushion 16.01% / $681.4B, T 8 / 72: <strong>the whole board goes into TODAY&rsquo;s "
 "close — the first since the quad-witching breakout — exactly as published</strong>. Premarket "
 "(9:07&ndash;9:14 ET, labeled color, never a model input): NVDA +0.60% $223.60 leads AMZN +0.54%, GOOGL "
 "+0.36% and MSFT +0.34% against AAPL −0.07% — implied lead 9.68% / $477.5B vs the finals&rsquo; 8.95%, "
 "implied cushion 15.52%: the tape leans WIDER into the close. <strong>BTC FIRMS TO THE DOOR OF THE "
 "SERIES HIGH — A SIXTH STRAIGHT $80K PRINT, AND THE CONSENSUS CATCHES COINGECKO&rsquo;S FIRST BAD PRINT: "
 "$81,618.00</strong> (Kraken live, +1.48%/24h, own range $80,213&ndash;$81,880; Coinbase live $81,681.35, "
 "+1.49%/24h, ~0.08% over — the two exchanges 0.08% apart; CMC $81,478.68, +1.18%/24h, ~0.17% under, "
 "range $80,150&ndash;$82,075 — a 0.25%-spread three-way consensus; CoinGecko printed $84,609.17 "
 "&ldquo;+5.3%&rdquo;, ~3.7% over the consensus, with a claimed $85,046 24h high that no exchange&rsquo;s "
 "own range corroborates — discarded: not a stale re-serve like its Sep 13/15 PM discards but the aggregator&rsquo;s first fresh-but-wrong print of the series), <strong>+0.98% "
 "on the Sunday-night print</strong>, −0.11% under the series high, +0.48% over the $80k-break print, "
 "+4.09% over the Sep 1 bake; T 101.6d: the firmer spot re-widens every residual vs the stale "
 "pre-breakout Sep 15 walk mids — the up-rungs hold inside Saturday&rsquo;s series wides ($85k −18.4, "
 "$90k −19.5, $95k −17.7, $100k −15.6, $110k −8.8) while all three dips print FRESH series wides "
 "($60k +8.1, $55k +9.9, $50k +10.1; needed touch +4.1%) — labeled color, the BTC tab keeps its Sep 1 "
 "01:27Z stamps and its re-bake stays the loudest want on the page. Mids/books/balances keep the Sep 16 "
 "01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.")
rep("needed touch +5.2%) — labeled color, the BTC tab keeps its Sep 1 01:27Z stamps and its re-bake stays "
    "the loudest want on the page. Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the "
    "ledger still owes its 61 fills. No trades placed.</span>",
    "needed touch +5.2%) — labeled color, the BTC tab keeps its Sep 1 01:27Z stamps and its re-bake stays "
    "the loudest want on the page. Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the "
    "ledger still owes its 61 fills. No trades placed."
    + TAPE + "</span>", "tape-append")

# ---- 2a. sync Latest head replace ----
m = re.search(r"<strong>Latest: Sep 20 23:3xZ PM pass \(Sunday night\).*?Leaderboard re-marked Sep 15 01:10Z\.</strong>", html, re.S)
assert m, "Latest head not found"
LATEST = ("<strong>Latest: Sep 21 13:3xZ AM pass (Monday pre-open) — the morning of the first post-breakout "
 "close: all five Sep 18 finals re-confirmed to the cent a FIFTH consecutive session (NVDA&rsquo;s 190.0M "
 "settled volume holds; the Sep 17 finals a sixth session beneath them) and calibration reproduced every "
 "published fair EXACTLY (Dec 65.98 / 28.69, crown 93.52 / 6.48, seat 93.09 / 6.47, 3rd 99.13 / 0.43, "
 "P(±5/wk) 60 / 58 / 4) — lead 8.95% / $442.1B, cushion 16.01%, T 8 / 72: every fair, badge and Best-Bet "
 "stance (Best Bets #1 STOOD DOWN, the crownAAPL hold rides, the sep3MSFT sell, the stale-ladder cheap "
 "trio queued for a re-walk) goes into today&rsquo;s close exactly as published. The premarket leans "
 "WIDER (labeled color): NVDA +0.60% over AAPL −0.07% — implied lead 9.68% / $477.5B. BTC $81,618.00 "
 "(Kraken live +1.48%/24h, LIVE Coinbase $81,681.35 ~0.08% over, CMC ~0.17% under — a 0.25%-spread "
 "consensus; CoinGecko&rsquo;s $84,609 print, with a claimed $85k 24h high no exchange corroborates, is "
 "DISCARDED — its first fresh-but-wrong print of the series, after two stale-snapshot discards Sep 13/15 PM), +0.98% on the Sunday-night print and −0.11% under the series "
 "high — a SIXTH consecutive $80k+ print (+4.09% over the Sep 1 bake); residuals vs the pre-breakout "
 "Sep 15 walk mids re-widen everywhere — up-rungs inside Saturday&rsquo;s wides ($90k −19.5), all three "
 "dips at fresh series wides — the Bitcoin tab re-bake stays the loudest want. Autodata DOWN a 43rd feed "
 "run; tab bakes: Oil Sep 10, Treasuries Sep 9 close, Largest-Company fairs Sep 18 23:1xZ on the Sep 16 "
 "01:45Z walk mids (finals locked Sep 19&ndash;21), Bitcoin Sep 1, Iran Sep 1; Leaderboard re-marked "
 "Sep 15 01:10Z.</strong>")
html = html[:m.start()] + LATEST + html[m.end():]
edits.append("latest-head")

# ---- 2b. sync chronicle append ----
CHRON = (" <strong>Sep 21 13:3xZ AM run (Monday pre-open): the lock holds a fifth pass on the morning of "
 "the first post-breakout close — all five Sep 18 finals re-confirmed to the cent a fifth consecutive "
 "session (the settled volume holds; the Sep 17 finals a sixth session), calibration reproduced every "
 "fair exactly, and the whole board — lead 8.95% / $442.1B, cushion 16.01%, T 8 / 72 — goes into "
 "today&rsquo;s close exactly as published; the premarket leans wider (NVDA +0.60% over AAPL −0.07%, "
 "implied lead 9.68% / $477.5B — labeled color). BTC firms to the door of the series high: $81,618.00 "
 "(Kraken live +1.48%/24h; LIVE Coinbase $81,681.35 ~0.08% over and CMC $81,478.68 ~0.17% under — a "
 "0.25%-spread three-way consensus that catches and discards CoinGecko&rsquo;s $84,609.17 print, the "
 "aggregator&rsquo;s first bad read of the series: its claimed $85,046 24h high appears in no "
 "exchange&rsquo;s own range), +0.98% on the Sunday-night print, −0.11% under the series high, +0.48% "
 "over the $80k-break print, +4.09% over the Sep 1 bake — a sixth consecutive $80k+ print; T 101.6d — "
 "the firmer spot re-widens every residual vs the stale Sep 15 walk mids: up-rungs inside "
 "Saturday&rsquo;s wides ($85k −18.4, $90k −19.5, $95k −17.7, $100k −15.6, $110k −8.8), all three dips "
 "at fresh series wides ($60k +8.1, $55k +9.9, $50k +10.1), needed touch +4.1%. Autodata DOWN a "
 "FORTY-THIRD feed run (12:45Z cron silent; 13:09Z poke touching fetch/poke, 03f77c89, unanswered — the "
 "Actions-disablement diagnosis stands). Mids/books/balances keep the Sep 16 01:45Z stamps; the ledger "
 "still owes the 61 swept fills. No trades placed.</strong>")
rep("the 61 swept fills. No trades placed.</strong><span id=\"sync-ago\"",
    "the 61 swept fills. No trades placed.</strong>" + CHRON + "<span id=\"sync-ago\"",
    "chronicle-append")

# ---- 3a. Largest tape label tweak ----
rep("re-confirmed to the cent through the Sep 20 evening pass — four consecutive sessions",
    "re-confirmed to the cent through the Sep 21 morning pass — five consecutive sessions",
    "label-tweak")

# ---- 3b. hero prose prepend ----
HERO = ("<strong>SEP 21 13:4xZ AM (MONDAY PRE-OPEN): THE LOCK HOLDS A FIFTH PASS — THE FIRST POST-BREAKOUT "
 "CLOSE IS TODAY.</strong> The morning pass re-confirmed all five Sep 18 finals to the cent a "
 "<strong>fifth consecutive session</strong> (the settled volume holds; the Sep 17 finals a sixth session "
 "beneath them) and reproduced every fair below EXACTLY — the board goes into today&rsquo;s close "
 "unchanged (T 8 / 72), and the premarket leans wider (NVDA +0.60% over AAPL −0.07%, implied lead 9.68% — "
 "labeled color, never a model input). Off-board, bitcoin firmed to $81,618.00 on a Kraken&ndash;Coinbase "
 "consensus that discarded CoinGecko&rsquo;s first bad print of the series — a sixth straight $80k+ "
 "print, 0.1% under the series high — pressure on the Bitcoin tab&rsquo;s Sep 1 bake, not on these "
 "fairs. <em>Sunday-night text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>SEP 20 23:3xZ PM (SUNDAY NIGHT): THE LOCK HOLDS A FOURTH PASS",
    "data-longform-label=\"More\">" + HERO + "<strong>SEP 20 23:3xZ PM (SUNDAY NIGHT): THE LOCK HOLDS A FOURTH PASS",
    "hero-prepend")

# ---- 3c. Next-Catalyst prepend ----
NC = ("<strong>Sep 21 13:3xZ AM: the catalyst is HOURS AWAY — today&rsquo;s close is the model&rsquo;s "
 "first fresh input since the breakout.</strong> Monday pre-open Sep 21, T 8 / 72 — the finals locked "
 "five times over (five-for-five to the cent on every pass, quadrature exact each time; autodata down a "
 "43rd feed run — the fix is still one visit to github.com/chad506/Leadsure/actions). The premarket "
 "leans wider (implied lead 9.68% vs 8.95% — labeled color). The chore list stands: the <strong>September re-walk queue "
 "and the Bitcoin tab re-bake</strong> (spot $81,618 on the exchange consensus — all three dip residuals "
 "on the stale Sep 15 mids at fresh series wides, $90k −19.5) still head it, and tonight&rsquo;s close "
 "re-deals the fairs. <em>Sunday-night text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>Sep 20 23:3xZ PM: tomorrow&rsquo;s open IS the catalyst",
    "data-longform-label=\"More\">" + NC + "<strong>Sep 20 23:3xZ PM: tomorrow&rsquo;s open IS the catalyst",
    "nextcat-prepend")

io.open(P, 'w', encoding='utf-8').write(html)
print(f"OK — {len(edits)} edits applied: {edits}; {n0} → {len(html)} chars (+{len(html)-n0})")
