#!/usr/bin/env python3
"""Sep 19 AM (Saturday) bake — the morning check locks the quad-witching finals.
Surfaces: header tape (new AM segment), sync Latest + chronicle append, Largest
tape label + hero-prose prepend + NVDA source-note lock + Next-Catalyst prepend,
analysis table-note + footnote lock phrases, settled-volume corrections.
Every replacement must hit exactly once."""
import io, sys

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

# ---- 1. header tape: append the Sep 19 AM segment ----
TAPE = (" · <strong>Sep 19 13:2xZ — SATURDAY MORNING, THE QUAD-WITCHING FINALS LOCK:</strong> "
 "autodata is down a <strong>THIRTY-NINTH</strong> consecutive feed run (the Sep 19 12:45Z cron silent; "
 "this run&rsquo;s 13:09Z poke touching fetch/poke, 05b5790a, unanswered — the Actions disablement stands, "
 "one manual visit to github.com/chad506/Leadsure/actions revives it). <strong>The NVDA source split RESOLVES "
 "TO THE HEADER: the history table that served $222.06 (+1.24%) at ~23:10Z settled to $222.27 (+1.34%) "
 "overnight</strong> — the Sep 12/15/18-AM lesson holds a fourth time — and ALL FIVE Sep 18 closes "
 "re-confirmed against the history pages to the cent (NVDA $222.27, AAPL $336.13, GOOGL $349.54, MSFT $493.78, "
 "AMZN $253.71; the only revision anywhere is NVDA&rsquo;s volume, the ~23:1xZ pull&rsquo;s 181.7M settling to "
 "190.0M). An independent quadrature re-run reproduced every published fair EXACTLY (Dec 65.98 / 28.69 / 4.27 / "
 "0.30; crown 93.52 / 6.48; seat 93.09 / 6.47; 3rd 99.13 / 0.43; P(±5/wk) 60 / 58 / 4) — lead 8.95% / "
 "$442.1B, cushion 16.01% / $681.4B, T 8 / 72; <strong>every fair, badge and Best-Bet stance rides the weekend "
 "into Monday&rsquo;s open exactly as published</strong> (no close until Sep 21). BTC color: spot $81,074.05 "
 "(CoinGecko live, +4.3%/24h, range $77,609–$81,675; Kraken live cross $81,079.00 just +0.01% apart — "
 "the series&rsquo; second-tightest cross (Sep 17 PM&rsquo;s ~0.004% Coinbase cross keeps the record), both live, no snapshot rotation), <strong>−0.19% on the PM $80k-break "
 "print: the breakout HOLDS its first overnight</strong>, +3.39% vs the Sep 1 bake; T 103.7d: the up-rungs ease "
 "a hair off the series&rsquo; wides and stay the story ($85k −16.3, $90k −17.7, $95k −16.3, "
 "$100k −14.6, $110k −8.2; dips rich $60k +6.7, $55k +9.0, $50k +9.7; needed touch +4.8%) — "
 "labeled color, the BTC tab keeps its Sep 1 01:27Z stamps and its re-bake stays the loudest want on the page. "
 "Mids/books/balances keep the Sep 16 01:45Z walk&rsquo;s stamps; the ledger still owes its 61 fills. "
 "No trades placed.")
rep("its 61 fills. No trades placed.</span>\n",
    "its 61 fills. No trades placed." + TAPE + "</span>\n", "tape-append")

# ---- 2a. sync Latest head replace ----
import re
m = re.search(r"<strong>Latest: Sep 18 23:1xZ PM pass.*?re-marked Sep 15 01:10Z\.</strong>", html, re.S)
assert m, "Latest head not found"
LATEST = ("<strong>Latest: Sep 19 13:2xZ AM pass (Saturday) — the morning check LOCKS the quad-witching "
 "finals: the NVDA source split resolves to the header ($222.27 +1.34% — the history table settled to it "
 "overnight; the only revision anywhere is volume, 181.7M → 190.0M settled), all five Sep 18 closes "
 "re-confirmed to the cent and calibration reproduced every PM fair EXACTLY (Dec 65.98 / 28.69, crown 93.52 / "
 "6.48, seat 93.09 / 6.47, 3rd 99.13 / 0.43, P(±5/wk) 60 / 58 / 4) — lead 8.95% / $442.1B, cushion "
 "16.01%, T 8 / 72: every fair, badge and Best-Bet stance (Best Bets #1 STOOD DOWN, the crownAAPL hold rides, "
 "the sep3MSFT sell, the stale-ladder cheap trio queued for a re-walk) rides the weekend into Monday&rsquo;s "
 "open unchanged. BTC HOLDS the $80k break: $81,074.05 (CoinGecko live +4.3%/24h; Kraken cross $81,079.00 "
 "+0.01% apart — the series&rsquo; second-tightest, both live), −0.19% on the PM print, +3.39% over the "
 "Sep 1 bake; the up-rungs are still 8–18 points cheap vs the pre-breakout Sep 15 walk mids ($90k "
 "−17.7) — the Bitcoin tab re-bake stays the loudest want. Autodata DOWN a 39th feed run; tab bakes: "
 "Oil Sep 10, Treasuries Sep 9 close, Largest-Company fairs Sep 18 23:1xZ on the Sep 16 01:45Z walk mids "
 "(finals locked Sep 19 AM), Bitcoin Sep 1, Iran Sep 1; Leaderboard re-marked Sep 15 01:10Z.</strong>")
html = html[:m.start()] + LATEST + html[m.end():]
edits.append("latest-head")

# ---- 2b. sync chronicle append ----
CHRON = (" <strong>Sep 19 13:2xZ AM run (Saturday): the morning check LOCKS the quad-witching finals — "
 "the history table&rsquo;s $222.06 settled to the header&rsquo;s $222.27 (+1.34%) overnight (the "
 "Sep 12/15/18-AM lesson holds a fourth time); all five Sep 18 finals re-confirmed to the cent, the only "
 "revision NVDA&rsquo;s volume (181.7M → 190.0M settled). Calibration reproduced every Sep 18 PM fair "
 "exactly on the locked finals — lead 8.95% / $442.1B, cushion 16.01%, T 8 / 72 — so every fair, "
 "badge and Best-Bet stance rides the weekend unchanged (no close until Monday Sep 21). BTC $81,074.05 "
 "(CoinGecko live +4.3%/24h; Kraken live cross $81,079.00 +0.01% apart — the series&rsquo; second-tightest "
 "cross, no snapshot rotation), −0.19% on the PM $80k-break print — the breakout holds its first "
 "overnight — +3.39% vs the Sep 1 bake; T 103.7d: the up-rungs ease a hair off the wides and stay the "
 "series&rsquo; widest complex ($85k −16.3, $90k −17.7, $95k −16.3, $100k −14.6, $110k "
 "−8.2; dips rich $50k +9.7), needed touch +4.8%. Autodata DOWN a THIRTY-NINTH feed run (12:45Z cron "
 "silent; 13:09Z poke touching fetch/poke, 05b5790a, unanswered — the Actions-disablement diagnosis "
 "stands). Mids/books/balances keep the Sep 16 01:45Z stamps; the ledger still owes the 61 swept fills. "
 "No trades placed.</strong>")
rep("</strong><span id=\"sync-ago\"", CHRON + "<span id=\"sync-ago\"", "chronicle-append")
# rep consumed the closing </strong> of the last segment; restore it
html = html.replace(CHRON + "<span id=\"sync-ago\"", "</strong>" + CHRON + "<span id=\"sync-ago\"")

# ---- 3a. Largest tape label lock ----
rep("NVDA&rsquo;s own page split $222.27 header / $222.06 table, the header taken, the morning pass re-verifies",
    "NVDA&rsquo;s $222.27 final LOCKED by the Sep 19 morning check — the table&rsquo;s $222.06 settled to the header overnight",
    "label-lock")

# ---- 3b. hero prose prepend ----
HERO = ("<strong>SEP 19 13:2xZ AM (SATURDAY): THE FINALS LOCK — THE SPLIT RESOLVES TO THE HEADER.</strong> "
 "The history table that served $222.06 at ~23:10Z settled to <strong>$222.27 (+1.34%)</strong> overnight; all "
 "five Sep 18 closes re-confirmed to the cent (the only revision: NVDA&rsquo;s volume, 181.7M → 190.0M "
 "settled) and an independent quadrature re-run reproduced every PM fair below EXACTLY — the whole board, "
 "and every Best-Bet stance, rides the weekend into Monday&rsquo;s open unchanged (T 8 / 72; no close until "
 "Sep 21). <em>PM text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>SEP 18 23:1xZ PM: THE QUAD-WITCHING BREAKOUT",
    "data-longform-label=\"More\">" + HERO + "<strong>SEP 18 23:1xZ PM: THE QUAD-WITCHING BREAKOUT",
    "hero-prepend")

# ---- 3c. hero settled-volume fix ----
rep("Friday&rsquo;s expiry close (181.7M NVDA shares) went one way",
    "Friday&rsquo;s expiry close (190.0M NVDA shares settled — the ~23:1xZ pull said 181.7M) went one way",
    "hero-volume")

# ---- 3d. NVDA source-note lock ----
rep("— the header is taken as the working final (the Sep 12/15/18-AM lesson in reverse), and tomorrow&rsquo;s pass locks it.</em>",
    "— the header is taken as the working final (the Sep 12/15/18-AM lesson in reverse). <strong>LOCKED "
    "Sep 19 13:2xZ AM: the table settled to $222.27 overnight — the header was right; volume settled "
    "189,973,388.</strong></em>", "source-note-lock")

# ---- 3e. Next-Catalyst prepend ----
NC = ("<strong>Sep 19 13:2xZ AM: the weekend holds the board — Monday&rsquo;s open is the next "
 "catalyst.</strong> Saturday Sep 19, T 8 / 72 — the finals locked pre-dawn (the split resolved to "
 "$222.27, five-for-five to the cent, quadrature exact; autodata down a 39th feed run — the fix is still "
 "one visit to github.com/chad506/Leadsure/actions). Nothing re-prices until Monday Sep 21; the chore list "
 "stands as written below, and the <strong>September re-walk queue and the Bitcoin tab re-bake</strong> (spot "
 "held $81k overnight — the up-rungs still 8–18 points cheap on the stale Sep 15 mids) head it. "
 "<em>PM text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>Sep 18 23:1xZ PM: the crown&rsquo;s final full week begins",
    "data-longform-label=\"More\">" + NC + "<strong>Sep 18 23:1xZ PM: the crown&rsquo;s final full week begins",
    "nextcat-prepend")

# ---- 4. analysis table-note lock ----
rep("— the header taken, disclosed, tomorrow&rsquo;s pass locks it):",
    "— the header taken, and LOCKED Sep 19 AM: the table settled to $222.27 overnight, volume 190.0M settled):",
    "table-note-lock")

# ---- 5. footnote lock + volume ----
rep("and disclosed for the morning pass to lock):",
    "and disclosed for the morning pass to lock — <strong>LOCKED Sep 19 13:2xZ AM: the table settled to "
    "$222.27 overnight</strong>):", "footnote-lock")
rep("on 181.7M shares</strong>",
    "on 190.0M shares (settled; the ~23:1xZ pull said 181.7M)</strong>", "footnote-volume")

io.open(P, 'w', encoding='utf-8').write(html)
print(f"OK — {len(edits)} edits applied: {edits}; {n0} → {len(html)} bytes (+{len(html)-n0})")
