#!/usr/bin/env python3
"""Sep 22 AM (Tuesday pre-open) bake — the morning check LOCKS the first
post-breakout close CLEAN (all five Sep 21 finals to the cent, volumes
included; zero revisions; quadrature exact), the premarket leans NARROWER
(implied lead 9.45% vs the finals' 10.52% — the first give-back leaning
since the breakout), and bitcoin consolidates the squeeze at the series'
first $86k morning ($86,009.01 on the second-tightest live cross; Kraken/
CMC flagged as a fresh-but-lagged pair — a new source-defense shape).
Surfaces: header tape (new AM segment), sync Latest replace + chronicle
append, Largest tape label LOCKED marker, hero-prose prepend, Next-Catalyst
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

# ---- 1. header tape: append the Sep 22 AM segment ----
TAPE = (" · <strong>Sep 22 13:2xZ — TUESDAY PRE-OPEN: THE MORNING CHECK LOCKS THE POST-BREAKOUT CLOSE "
 "CLEAN, BITCOIN CONSOLIDATES THE SQUEEZE:</strong> autodata is down a <strong>FORTY-FIFTH</strong> "
 "consecutive feed run (the Sep 22 12:45Z cron silent; this run&rsquo;s 13:11Z poke touching fetch/poke, "
 "46479ced, unanswered — the Actions disablement stands, one manual visit to "
 "github.com/chad506/Leadsure/actions revives it). The morning pass re-confirmed <strong>all five Sep 21 "
 "finals to the cent, VOLUMES INCLUDED</strong> (NVDA $227.38 on 108,496,004 shares, AAPL $338.98, GOOGL "
 "$354.97, MSFT $501.61, AMZN $258.45 — every history-page header &ldquo;At close: Sep 21&rdquo;; the "
 "Sep 18 finals re-confirmed beneath them a SEVENTH session, NVDA&rsquo;s 190.0M and AAPL&rsquo;s revised "
 "85.93M volumes holding; the Sep 17 rows verified beneath those) and an independent quadrature re-run "
 "reproduced every published fair EXACTLY — lead 10.52% / $523.9B, cushion 15.21% / $657.1B, T 7 / 71: "
 "<strong>the whole board goes into tonight&rsquo;s close exactly as published — zero revisions</strong>. "
 "Premarket (9:06&ndash;9:11 ET, labeled color, never a model input): MSFT +1.23% $507.76 leads AAPL "
 "+0.38% and GOOGL +0.33% against NVDA −0.59% $226.03 and AMZN −0.75% — implied lead 9.45% / $472.3B vs "
 "the finals&rsquo; 10.52%, implied cushion 15.26%: <strong>the tape leans NARROWER into the close — the "
 "first give-back leaning since the breakout</strong>. <strong>BITCOIN CONSOLIDATES THE SQUEEZE — AN "
 "EIGHTH STRAIGHT $80K+ PRINT AND THE SERIES&rsquo; FIRST $86K MORNING: $86,009.01</strong> (CoinGecko "
 "LIVE, +1.7%/24h, range 84,142.22&ndash;87,329.89 — the 24h% banks its own discarded Monday $84,609 "
 "print as baseline, cosmetic; Coinbase LIVE $86,004.64 +1.79%, 0.005% under — the series&rsquo; "
 "second-tightest live cross, Sep 17 PM&rsquo;s ~0.004% keeps the record; Kraken $85,458.00 +4.61% and "
 "CMC $85,406.76 +4.98% print ~0.6&ndash;0.7% under as a lagged pair — fresh numbers, NOT re-serves of "
 "the Sep 21 reads, flagged and passed over: the live pair carries the print), <strong>−0.61% on the "
 "Monday-night squeeze print</strong> — the touch consolidates rather than extends — +5.89% over the "
 "$80k-break print, +9.69% over the Sep 1 bake; T 100.7d: every surviving-rung residual vs the stale "
 "pre-breakout Sep 15 walk mids eases off Monday&rsquo;s blow-out and stays far past the old series "
 "wides ($90k −36.2, $95k −32.8, $100k −28.8, $110k −17.7; dips $60k +14.8, $55k +13.7, $50k +11.9; "
 "needed touch to $90k +4.6%) — labeled color; <strong>the BTC tab&rsquo;s re-bake stays a NEED</strong>, "
 "its Sep 1 01:27Z stamps stay until a real walk. Mids/books/balances keep the Sep 16 01:45Z "
 "walk&rsquo;s stamps; the ledger still owes its 61 fills. No trades placed.")
rep("the ledger still owes its 61 fills. No trades placed.</span>",
    "the ledger still owes its 61 fills. No trades placed." + TAPE + "</span>", "tape-append")

# ---- 2a. sync Latest head replace ----
m = re.search(r"<strong>Latest: Sep 21 23:3xZ PM pass.*?Leaderboard re-marked Sep 15 01:10Z\.</strong>", html, re.S)
assert m, "Latest head not found"
LATEST = ("<strong>Latest: Sep 22 13:2xZ AM pass (Tuesday pre-open) — the morning check LOCKS the first "
 "post-breakout close clean: all five Sep 21 finals re-confirmed to the cent, volumes included "
 "(NVDA&rsquo;s 108.5M holds; the Sep 18 finals a seventh session beneath them), and calibration "
 "reproduced every published fair EXACTLY (Dec 69.04 / 25.86 / 4.07, crown 97.07 / 2.93, seat "
 "96.69 / 2.93, 3rd 99.37, P(±5/wk) 58 / 56 / 4) — lead 10.52% / $523.9B, cushion 15.21%, T 7 / 71: "
 "every fair, badge and Best-Bet stance (#1 stand-down holding at re-arm ≤ 20.86, the crownAAPL hold "
 "riding its exit bid, the sep3MSFT sell, the September cheap trio in the re-walk queue) goes into "
 "tonight&rsquo;s close exactly as published. The premarket leans NARROWER — the first give-back "
 "leaning since the breakout (labeled color): MSFT +1.23% leads while NVDA −0.59% and AMZN −0.75% hand "
 "back — implied lead 9.45% / $472.3B vs the finals&rsquo; 10.52%. BTC consolidates the squeeze at the "
 "series&rsquo; first $86k morning: $86,009.01 (CoinGecko LIVE +1.7%/24h; Coinbase LIVE $86,004.64 — "
 "0.005% apart, the series&rsquo; second-tightest live cross; Kraken $85,458 / CMC $85,407 "
 "~0.6&ndash;0.7% under as a lagged pair — fresh prints, not re-serves, flagged), −0.61% on the "
 "Monday-night print — an EIGHTH consecutive $80k+ print (+9.69% over the Sep 1 bake); surviving-rung "
 "residuals vs the pre-breakout Sep 15 walk mids ease but stay far past the old wides ($90k −36.2) — "
 "the Bitcoin tab re-bake stays the page&rsquo;s loudest NEED. Autodata DOWN a 45th feed run; tab "
 "bakes: Oil Sep 10, Treasuries Sep 9 close, Largest-Company fairs Sep 21 23:3xZ on the Sep 16 01:45Z "
 "walk mids (locked by this pass), Bitcoin Sep 1, Iran Sep 1; Leaderboard re-marked Sep 15 "
 "01:10Z.</strong>")
html = html[:m.start()] + LATEST + html[m.end():]
edits.append("latest-head")

# ---- 2b. sync chronicle append ----
CHRON = (" <strong>Sep 22 13:2xZ AM run (Tuesday pre-open): the morning check locks the first "
 "post-breakout close CLEAN — all five Sep 21 finals re-confirmed to the cent with every volume "
 "holding (NVDA&rsquo;s 108,496,004; the Sep 18 finals a seventh session beneath them, the 190.0M NVDA "
 "and revised 85.93M AAPL volumes intact; the Sep 17 rows verified beneath those), calibration "
 "reproduced every fair exactly, and the whole board — lead 10.52% / $523.9B, cushion 15.21%, "
 "T 7 / 71 — goes into tonight&rsquo;s close exactly as published; the premarket leans NARROWER, the "
 "first give-back leaning since the breakout (MSFT +1.23% leads, NVDA −0.59% and AMZN −0.75% hand "
 "back; implied lead 9.45% / $472.3B — labeled color). BTC consolidates the squeeze: $86,009.01 "
 "(CoinGecko LIVE +1.7%/24h, range 84,142.22&ndash;87,329.89 — its 24h% banks its own discarded "
 "Monday $84,609 print as baseline, cosmetic, the price live and Coinbase-confirmed; Coinbase LIVE "
 "$86,004.64 +1.79% — 0.005% apart, the series&rsquo; second-tightest live cross; Kraken $85,458.00 "
 "+4.61% and CMC $85,406.76 +4.98% ~0.6&ndash;0.7% under — a lagged pair, fresh prints rather than "
 "re-serves, flagged and passed over), −0.61% on the Monday-night squeeze print, +5.89% over the "
 "$80k-break print, +9.69% over the Sep 1 bake — an eighth consecutive $80k+ print and the "
 "series&rsquo; first $86k morning; T 100.7d — surviving-rung residuals vs the stale Sep 15 walk mids "
 "ease off Monday&rsquo;s blow-out and hold far past the old series wides ($90k −36.2, $95k −32.8, "
 "$100k −28.8, $110k −17.7; dips $60k +14.8, $55k +13.7, $50k +11.9), needed touch +4.6%. Autodata "
 "DOWN a FORTY-FIFTH feed run (12:45Z cron silent; 13:11Z poke touching fetch/poke, 46479ced, "
 "unanswered — the Actions-disablement diagnosis stands). Mids/books/balances keep the Sep 16 01:45Z "
 "stamps; the ledger still owes the 61 swept fills. No trades placed.</strong>")
rep("the 61 swept fills. No trades placed.</strong><span id=\"sync-ago\"",
    "the 61 swept fills. No trades placed.</strong>" + CHRON + "<span id=\"sync-ago\"",
    "chronicle-append")

# ---- 3a. Largest tape label: LOCKED marker + seventh-session count ----
rep("The tape (caps = the Sep 21 closes, history pages ~23:1xZ — the Sep 18 finals re-confirmed to the "
    "cent beneath them a sixth session, NVDA&rsquo;s",
    "The tape (caps = the Sep 21 closes, history pages ~23:1xZ, LOCKED by the Sep 22 morning pass — "
    "every price and volume to the cent · the Sep 18 finals re-confirmed beneath them a seventh "
    "session, NVDA&rsquo;s",
    "label-tweak")

# ---- 3b. hero prose prepend ----
HERO = ("<strong>SEP 22 13:2xZ AM (TUESDAY PRE-OPEN): THE MORNING CHECK LOCKS THE BREAKOUT CLOSE "
 "CLEAN.</strong> All five Sep 21 finals re-confirmed to the cent, <strong>volumes included</strong> "
 "(NVDA&rsquo;s 108.5M holds; the Sep 18 finals a seventh session beneath them), and every fair below "
 "reproduced EXACTLY — the board goes into tonight&rsquo;s close unchanged (T 7 / 71), while the "
 "premarket leans NARROWER for the first time since the breakout (MSFT +1.23% leads, NVDA −0.59% hands "
 "back; implied lead 9.45% vs 10.52% — labeled color, never a model input). Off-board, bitcoin "
 "consolidates Monday&rsquo;s squeeze at $86,009 on the series&rsquo; second-tightest live cross "
 "(−0.61% overnight, an eighth straight $80k+ print) — pressure stays on the Bitcoin tab&rsquo;s Sep 1 "
 "bake, not on these fairs. <em>Monday-night text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>SEP 21 23:3xZ PM (THE FIRST POST-BREAKOUT CLOSE): ALL FIVE GREEN, NVIDIA ON TOP",
    "data-longform-label=\"More\">" + HERO + "<strong>SEP 21 23:3xZ PM (THE FIRST POST-BREAKOUT CLOSE): ALL FIVE GREEN, NVIDIA ON TOP",
    "hero-prepend")

# ---- 3c. Next-Catalyst prepend ----
NC = ("<strong>Sep 22 13:2xZ AM: the model has its fresh input — tonight&rsquo;s close either extends "
 "the 10.52% lead or hands the breakout its first give-back.</strong> Tuesday pre-open Sep 22, "
 "T 7 / 71 — the Sep 21 finals locked CLEAN on the first morning check (every price and volume to the "
 "cent; quadrature exact; autodata down a 45th feed run — the fix is still one visit to "
 "github.com/chad506/Leadsure/actions). The premarket leans narrower (implied lead 9.45% vs 10.52% — "
 "labeled color). The chore list stands: the <strong>September re-walk queue and the Bitcoin tab "
 "re-bake</strong> (spot $86,009 consolidating Monday&rsquo;s $85k touch — every surviving up-rung "
 "residual on the stale Sep 15 mids still far past the old series wides, $90k −36.2) still head it, "
 "and tonight&rsquo;s close re-deals the fairs. <em>Monday-morning text, kept:</em> ")
rep("data-longform-label=\"More\"><strong>Sep 21 13:3xZ AM: the catalyst is HOURS AWAY",
    "data-longform-label=\"More\">" + NC + "<strong>Sep 21 13:3xZ AM: the catalyst is HOURS AWAY",
    "nextcat-prepend")

io.open(P, 'w', encoding='utf-8').write(html)
print(f"OK — {len(edits)} edits applied: {edits}; {n0} → {len(html)} chars (+{len(html)-n0})")
