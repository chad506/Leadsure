#!/usr/bin/env python3
"""Sep 19 PM (Saturday night) bake — the lock holds a second pass; bitcoin
prints the outage series' high on the night's only live source (Kraken re-serve
+ Coinbase/CMC Friday-vintage = all three crosses discarded).
Surfaces: header tape (new PM segment), sync Latest replace + chronicle append,
Largest tape label tweak + hero-prose prepend + Next-Catalyst prepend.
Every replacement must hit exactly once."""
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

# ---- 1. header tape: append the Sep 19 PM segment ----
TAPE = (" · <strong>Sep 19 23:4xZ — SATURDAY NIGHT, THE LOCK HOLDS AND BITCOIN PRINTS THE SERIES HIGH:</strong> "
 "autodata is down a <strong>FORTIETH</strong> consecutive feed run (the Sep 19 22:45Z cron silent; "
 "this run&rsquo;s ~23:09Z poke touching fetch/poke, f5146418, unanswered — the Actions disablement stands, "
 "one manual visit to github.com/chad506/Leadsure/actions revives it). The evening pass re-confirmed "
 "<strong>all five Sep 18 finals to the cent a SECOND consecutive session</strong> (NVDA $222.27 on "
 "189,973,388 shares settled, AAPL $336.13, GOOGL $349.54, MSFT $493.78, AMZN $253.71; the Sep 17 finals "
 "re-confirmed beneath them a third session) and an independent quadrature re-run reproduced every published "
 "fair EXACTLY — lead 8.95% / $442.1B, cushion 16.01% / $681.4B, T 8 / 72: <strong>the whole board rides "
 "into Monday&rsquo;s open exactly as published</strong> (no close until Sep 21). <strong>BTC PRINTS THE "
 "SERIES HIGH: $81,706.31</strong> (CoinGecko live, +1.3%/24h, range $80,541–$81,709 — the night&rsquo;s "
 "ONLY live read: Kraken re-served the AM cross to the cent ($81,079.00, the series&rsquo; sixth snapshot "
 "rotation), Coinbase and CoinMarketCap both served Friday-vintage snapshots (+6.3% &ldquo;24h&rdquo; prints "
 "carrying Friday&rsquo;s $76.2k low) — all three discarded), +0.78% on the AM print, <strong>+0.59% over "
 "Friday&rsquo;s $80k-break print and +4.20% over the Sep 1 bake — the widest above-bake read of the "
 "series</strong>; T 103.2d: every residual vs the stale Sep 15 walk mids blows to a fresh series wide "
 "($85k −18.9, $90k −20.1 — the series&rsquo; first −20 print, $95k −18.3, $100k −16.2, $110k −9.3; dips "
 "rich $60k +7.9, $55k +9.8, $50k +10.0 — the first +10; needed touch +4.0%) — labeled color, the BTC tab "
 "keeps its Sep 1 01:27Z stamps and its re-bake stays the loudest want on the page. Mids/books/balances keep "
 "the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.")
rep("owes its 61 fills. No trades placed.</span>",
    "owes its 61 fills. No trades placed." + TAPE + "</span>", "tape-append")

# ---- 2a. sync Latest head replace ----
m = re.search(r"<strong>Latest: Sep 19 13:2xZ AM pass.*?Leaderboard re-marked Sep 15 01:10Z\.</strong>", html, re.S)
assert m, "Latest head not found"
LATEST = ("<strong>Latest: Sep 19 23:4xZ PM pass (Saturday night) — the lock holds and bitcoin prints the "
 "series high: all five Sep 18 finals re-confirmed to the cent a SECOND consecutive session (NVDA&rsquo;s "
 "190.0M settled volume holds; the Sep 17 finals a third session beneath them) and calibration reproduced "
 "every published fair EXACTLY (Dec 65.98 / 28.69, crown 93.52 / 6.48, seat 93.09 / 6.47, 3rd 99.13 / 0.43, "
 "P(±5/wk) 60 / 58 / 4) — lead 8.95% / $442.1B, cushion 16.01%, T 8 / 72: every fair, badge and Best-Bet "
 "stance (Best Bets #1 STOOD DOWN, the crownAAPL hold rides, the sep3MSFT sell, the stale-ladder cheap trio "
 "queued for a re-walk) rides into Monday&rsquo;s open unchanged. BTC $81,706.31 — the outage series&rsquo; "
 "highest print (CoinGecko live +1.3%/24h, the night&rsquo;s ONLY live read — Kraken re-served the AM cross "
 "to the cent and Coinbase/CMC served Friday-vintage snapshots; all three discarded), +0.59% over "
 "Friday&rsquo;s $80k break, +4.20% over the Sep 1 bake (the widest above-bake read); every up-rung residual "
 "on the pre-breakout Sep 15 walk mids sits at a fresh series wide ($90k −20.1, the first −20 print) — the "
 "Bitcoin tab re-bake stays the loudest want. Autodata DOWN a 40th feed run; tab bakes: Oil Sep 10, "
 "Treasuries Sep 9 close, Largest-Company fairs Sep 18 23:1xZ on the Sep 16 01:45Z walk mids (finals locked "
 "Sep 19), Bitcoin Sep 1, Iran Sep 1; Leaderboard re-marked Sep 15 01:10Z.</strong>")
html = html[:m.start()] + LATEST + html[m.end():]
edits.append("latest-head")

# ---- 2b. sync chronicle append ----
CHRON = (" <strong>Sep 19 23:4xZ PM run (Saturday night): the lock holds — all five Sep 18 finals "
 "re-confirmed to the cent a second consecutive session (the settled volume holds; the Sep 17 finals a "
 "third session), calibration reproduced every fair exactly, and the whole board — lead 8.95% / $442.1B, "
 "cushion 16.01%, T 8 / 72 — rides into Monday&rsquo;s open unchanged. BTC prints the series high "
 "$81,706.31 on the night&rsquo;s only live source (CoinGecko +1.3%/24h; Kraken re-served the AM cross to "
 "the cent — the sixth snapshot rotation, its second re-serve — and Coinbase/CMC served Friday-vintage "
 "snapshots; all three discarded), +0.59% over the $80k break and +4.20% over the Sep 1 bake, the widest "
 "above-bake read of the series; T 103.2d — every residual vs the stale Sep 15 walk mids at a fresh series "
 "wide ($85k −18.9, $90k −20.1 the first −20, $95k −18.3, $100k −16.2, $110k −9.3; dips $60k +7.9, $55k "
 "+9.8, $50k +10.0 the first +10), needed touch +4.0%. Autodata DOWN a FORTIETH feed run (22:45Z cron "
 "silent; ~23:09Z poke touching fetch/poke, f5146418, unanswered — the Actions-disablement diagnosis "
 "stands). Mids/books/balances keep the Sep 16 01:45Z stamps; the ledger still owes the 61 swept fills. "
 "No trades placed.</strong>")
rep("the 61 swept fills. No trades placed.</strong><span id=\"sync-ago\"",
    "the 61 swept fills. No trades placed.</strong>" + CHRON + "<span id=\"sync-ago\"",
    "chronicle-append")

# ---- 3a. Largest tape label tweak ----
rep("NVDA&rsquo;s $222.27 final LOCKED by the Sep 19 morning check — the table&rsquo;s $222.06 settled to the header overnight",
    "NVDA&rsquo;s $222.27 final LOCKED Sep 19 (morning check; the PM pass re-confirmed all five to the cent) — the table&rsquo;s $222.06 settled to the header overnight",
    "label-tweak")

# ---- 3b. hero prose prepend ----
HERO = ("<strong>SEP 19 23:4xZ PM (SATURDAY NIGHT): THE LOCK HOLDS.</strong> The evening pass re-confirmed "
 "all five Sep 18 finals to the cent a <strong>second consecutive session</strong> (NVDA&rsquo;s settled "
 "190.0M volume holds; the Sep 17 finals a third session beneath them) and reproduced every fair below "
 "EXACTLY — the board rides into Monday&rsquo;s open unchanged (T 8 / 72; no close until Sep 21). "
 "Off-board, bitcoin printed the outage series&rsquo; high ($81,706.31, +4.20% over the Sep 1 bake) on the "
 "night&rsquo;s only live source — pressure on the Bitcoin tab&rsquo;s Sep 1 bake, not on these fairs. "
 "<em>AM text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>SEP 19 13:2xZ AM (SATURDAY): THE FINALS LOCK",
    "data-longform-label=\"More\">" + HERO + "<strong>SEP 19 13:2xZ AM (SATURDAY): THE FINALS LOCK",
    "hero-prepend")

# ---- 3c. Next-Catalyst prepend ----
NC = ("<strong>Sep 19 23:4xZ PM: one weekend night down — Monday&rsquo;s open is still the catalyst.</strong> "
 "Saturday night Sep 19, T 8 / 72 — the finals locked twice over (five-for-five to the cent on both passes, "
 "quadrature exact both times; autodata down a 40th feed run — the fix is still one visit to "
 "github.com/chad506/Leadsure/actions). Nothing re-prices until Monday Sep 21; the chore list stands, and "
 "the <strong>September re-walk queue and the Bitcoin tab re-bake</strong> (spot at the series high "
 "$81,706 — every up-rung residual on the stale Sep 15 mids at a fresh series wide, $90k −20.1) still "
 "head it. <em>AM text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>Sep 19 13:2xZ AM: the weekend holds the board",
    "data-longform-label=\"More\">" + NC + "<strong>Sep 19 13:2xZ AM: the weekend holds the board",
    "nextcat-prepend")

io.open(P, 'w', encoding='utf-8').write(html)
print(f"OK — {len(edits)} edits applied: {edits}; {n0} → {len(html)} bytes (+{len(html)-n0})")
