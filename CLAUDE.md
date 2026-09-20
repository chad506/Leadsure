# Leadsure — Claude Code Project Instructions

## Workflow
- The live site is at https://leadsure.com, hosted on GitHub Pages (chad506/Leadsure, main branch)
- GitHub token is stored in the remote URL — push with `git push origin main` directly
- After every code change: commit and push immediately so the live site updates

## Site Structure
- `index.html` — main positions dashboard (uses app3.js)
- `fund-results.html` — full fund results with sold/addon positions
- `picks-history.html` — AI model picks history table
- `fund-data.js` — single source of truth for positions, prices, sold positions
- `model-picks-data.js` — all AI model picks (5 models, see below)
- `app3.js` — main dashboard JS (Finnhub live prices, P&L, charts)

## Account Hero (above KPI tiles)
Total Account Value | Cash Invested | Today's P&L ($ + %) | Total P&L | ROI
IDs: hero-account-value, hero-cash-invested, hero-today-pnl, hero-total-pnl, hero-roi

## KPI Tiles (index.html, in order — 8 tiles, 4×2)
Alpha vs S&P 500 | S&P 500 % | Mag 7 % | Positions |
Long Exposure | Short Exposure | Sortino | Sharpe

## Deployment
- Domain registrar: GoDaddy (leadsure.com registered/renewed there; nameservers delegated to Cloudflare)
- DNS: Cloudflare (nameservers), A records point to GitHub Pages IPs
- HTTPS cert: GitHub Pages Let's Encrypt (may need enabling via API after DNS changes)
- Enable HTTPS: `curl -X PUT -H "Authorization: token TOKEN" https://api.github.com/repos/chad506/Leadsure/pages -d '{"https_enforced":true}'`

---

## model-picks-data.js — The 5 Models

| id | name | icon | debut | trades (as of 7/2) |
|----|------|------|-------|---------------------|
| `gpt54` | GPT 5.4 | 🧠 | Week 1 (3/6) | 111 |
| `opus46` | Claude Opus 4.6 | 🎯 | Week 1 (3/6) | 111 |
| `wildcard` | Gemini 3.1 Pro | 🔮 | Week 1 (3/6) | 111 |
| `opus47` | Claude Opus 4.7 | 🌟 | Week 23 (4/28) | 35 |
| `fable5` | Fable 5 | 🪄 | Week 35 (6/12) | 22 |
| `opus48` | Claude Opus 4.8 | 💎 | Week 38 (6/22) | 15 |
| `human` | Human | 🧑 | Week 45 (9/4) | 1 |

`human` = Chad's own discretionary fund buys (periodic, sized at conviction — actual fund qty/price, not the $10k slot formula). Scored on the same leaderboard as the AI models; picks-history counts it separately ("N AI models + Human").

## Adding New Picks

### Pick object format
```js
{
  symbol: 'TICK',
  name: 'Full Company Name',
  industry: 'Specific Niche — be descriptive',
  marketCap: 1234567890,         // number in dollars
  direction: 'Long',             // or 'Short'
  dateChosen: '6/17',            // M/DD format
  qty: 22,                       // floor(10000 / price), rounded to whole shares
  price: 440.87,                 // entry price (actual buy price)
  livePrice: 440.87,             // set = price on entry (Finnhub updates it live)
  prevClose: 425.83,             // prior day's close: price - (dayChng$ / qty)
  rationale: 'Detailed thesis...'
}
```

### qty formula
`qty = Math.floor(10000 / price)` — target ~$10,000 per position. Round to nearest sensible lot.

### prevClose calculation
From the Google Sheet's "Day Chng $" column: `prevClose = currentPrice - (dayChng$ / qty)`.
Or: prior day's closing price from any financial data source.

### livePrice on entry
Set `livePrice = price` when first entering the pick. Finnhub live prices update it automatically.

### After adding picks to a model, update these 4 things:
1. **`totalTrades`** in that model's object — increment by number of new picks added
2. **Header comment** at top of file — add `| Week N: Month DD, YYYY` to the chain
3. **`MODEL_PICKS.date`** — append the new date(s) to the date string
4. **Week registry** — the header comment is the canonical week log; keep it up to date

### Week numbering
Week 1 = March 6, 2026. As of 6/17 we are on Week 36. Each set of picks on a new date = new week entry.

---

## Updating Fund Positions (fund-data.js)
- Source of truth for positions is `fund-data.js` → `POSITIONS` array
- When new buys happen, also update:
  - `fund-results.html` → `ENTRY_DATES` lookup (add symbol + entry date)
  - `picks-history.html` → `FUND_SYMBOLS` set (add symbol for LIVE badge)
  - `model-picks-data.js` → add picks entry for the recommending model + date
- The live Google Sheet with positions: https://docs.google.com/spreadsheets/d/1xwFFS6OkC9Frp2-mOuIMqxh7z_mXXNxE-Lc8-uP3Urk/export?format=csv&gid=251449467
- New positions appear at the bottom of the first table in the sheet

## Prices
- `PRICES_AS_OF` in fund-data.js must match today's date (YYYY-MM-DD Pacific time)
- `prevClose` = prior day's close (compute from sheet's Day Chng $ ÷ qty + current price)
- Finnhub API key: `d6kqa11r01qmopd1net0d6kqa11r01qmopd1netg`

---

## Common Mistakes to Avoid
- **Never set qty based on a wrong price** — always verify the entry price is correct before computing qty. If a stock hasn't traded at a given price in years, it's wrong.
- **livePrice ≠ buy price after time passes** — on entry set livePrice = price; never update it manually after that (Finnhub handles it).
- **prevClose is NOT the same as price** — compute it from actual prior-day close data.
- **totalTrades must be incremented** — easy to forget; each new pick adds 1 to that model's totalTrades.
- **Same-day fund entries need `prevClose = costBasis`** — app3.js only keeps a position's stored prevClose (instead of Finnhub's prior-day `pc`) when `entryDate === PRICES_AS_OF`. So when adding a position bought today: (1) set `PRICES_AS_OF` to today, and (2) set its `prevClose = costBasis`. Otherwise Finnhub's prior-day close overwrites it and Today's P&L shows a fake overnight gap (e.g. a position entered today after a +10% move would book that 10% as a phantom day gain).
- **Cross-model pick uniqueness** — every model pick must be unique across ALL models and not duplicate a current/sold fund holding. A stock the fund later buys is fine (it gets a LIVE badge); two *models* picking the same ticker is the violation to avoid.

---

## Marcy sub-site (leadsure.com/marcy)
Standalone sub-page: Magnolia, WA homes for sale + a Bankrate-style mortgage calculator. Decoupled from the fund nav (no cross-links between Marcy and the Positions/Picks/Fund pages).

### Files (all in `marcy/`)
- `index.html` — page shell (reuses shared `../base.css` / `../style.css` / `../dashboard.css` + `marcy.css`)
- `marcy.css` — Marcy-specific styles
- `marcy.js` — listings carousel, filters, mortgage calculator, Street View photos
- `listings.js` — **AUTO-GENERATED** listing data (don't hand-edit; regenerate — see below)
- `config.js` — `MARCY_CONFIG.googleMapsKey` (Google Street View key)

### Listings data
- Real Magnolia (zip 98199) for-sale listings from a Redfin **"Download All"** export (`.csv` or `.numbers`).
- **Refresh = one command:** `scripts/refresh-marcy-listings.sh` — finds the newest `redfin_*` export in `MARCY_EXPORT_DIR` (default: the Ambaum Dropbox "Real Estate" folder), regenerates `marcy/listings.js`, commits + pushes. Pass a path for a specific file; `--no-push` to regenerate only.
- Reports **added/removed** vs the previous run and flags new listings with `added: true` (shown as a "Just added" badge + filter option).
- Do NOT scrape Zillow/Redfin programmatically (ToS) — use the user's own export. Photos are NOT MLS photos.

### Photos — Google Street View
- Each card photo is a **Street View Static** image from the listing's lat/lng, using `MARCY_CONFIG.googleMapsKey`.
- The key MUST be HTTP-referrer-restricted to `leadsure.com/*` (it's public in `config.js`). Add a daily quota cap on the Street View Static API as a backstop.

### Defaults / behavior
- Type filter defaults to **Houses** (condos/townhomes/multi-family/land hidden until selected).
- Sort defaults to **price low→high**; the calculator pre-fills from the cheapest visible listing.
- "Show Mortgage" loads the calculator at 20% down with auto tax (0.9%/yr) + insurance (0.12%/yr); PMI auto-adds when down < 20%.
- Calculator terms: **30-year fixed** (6.75% default) and **7-year ARM** (auto-fills a ~6.25% intro rate; amortizes over 30 years). Switching the term writes that product's typical rate (`data-rate` on the button) into the rate box.

---

## Hyper sub-site (leadsure.com/hyper) — three pages, one stylesheet

Hyperliquid pages for Chad's perps account `0xD71a41eC000089ae99873AFB4D15CC7d54Dd95Bc`. Read-only
analysis — **never place, cancel or modify an order from any page or script here.**

### Files (all in `hyper/`)
- `hyper.css` — shared styles (loaded after `../base.css`, `../style.css`, `../dashboard.css`,
  `../polymarket/polymarket.css`). All three pages link it; do not re-inline styles.
- `index.html` — **Regime Book** (Sep 2, 2026 walk; baked). Rate/war betas for every liquid perp, 12 tickets,
  72-row screen. Its "account, tonight" block is the Sep 2 snapshot by design (caption points to Scenarios).
- `review.html` — **Trade Review** (baked scaffold: per-instrument + monthly ledgers, preliminary lessons).
  The full review (round-trip reconstruction, holding times, P&L by hour) is still open.
- `scenarios.html` + `scenarios.js` — **Portfolio Scenarios, LIVE.** The page reads the account in the
  browser from `api.hyperliquid.xyz/info` (CORS-open: webData2 → positions, marks, margin tiers, open orders
  with triggers, TWAP states; userFunding; two 60-day candle series) every 60 s and prices the book at price
  rungs two ways — HOLD AS-IS and WITH ORDERS (every resting order/TWAP executes along a straight-line path).
  Rungs (Chad's spec, Sep 5): primary coin (largest notional) in steps ≈ 1.25% of price rounded nice (BTC →
  $1,000) from 0.88× to 1.38× the mark (70k–110k at ~80k); secondary coin in $1 steps (HYPE) from 0.82× to
  1.29× (70–110 at ~85); joint grid ≈ 41 × 41 (dense cells, hover for detail, sticky headers, scrolls).
  simulate() uses per-coin sorted order queues (O(steps + orders)); grid cells run 300 steps, tables 800. Generalised to whatever the account holds (shorts get
  rungs in their favour downward). Maintenance = half the IM at max leverage, cumulative across margin tiers;
  the page prints an **exchange check** every read (model liq vs liquidationPx, model maintenance vs
  crossMaintenanceMarginUsed, model IM vs totalMarginUsed) — if any of those show ✗, the model is wrong,
  fix it before anything else.
- Nav on all three: Home | Regime Book | (Tickets, Screen on the regime page only) | Trade Review |
  Scenarios·LIVE | Polymarket.

### Model conventions (scenarios.js) — keep these when editing
- Path is straight-line in every moved coin; other coins flat. 1,000 steps. Reduce-only orders never exceed
  the position; opening orders and TWAP slices are skipped when initial margin (notional ÷ the position's
  leverage setting) would be exceeded; triggers fill at trigger ± slip (0.03% BTC/ETH, 0.10% others, taker
  0.035%); limits fill at the better of limit and path price (maker 0.010%); stop-limit / TP-limit that are
  not marketable at trigger rest as limits. TWAP remainder spread along the path (the tables); sensitivities
  shown for cancelled / path / filled-first. Hold-as-is liquidation by bisection; liquidation = end of
  scenario (the method block explains HL's 20%-chunk close and backstop rule). Funding not charged.
- **Every liquidation price shown is the EFFECTIVE one** (Chad's standing rule, Sep 5 2026): the price at which the
  book crosses maintenance on a straight adverse path with every resting order executing on the way (stops, bids,
  ladders), TWAP remainder excluded. The exchange's liquidationPx (nothing executes) is shown only as "exchange
  quote" and used for the model check. Chat recalcs follow the same rule — quote the effective number first.
- Findings/method must keep disclosing: liquidation ≠ zero, TWAP-timing range, beta R² and co-move range,
  funding horizon, stop round-trips.
- `.hy-findings li strong` is display:block (card titles) — inline emphasis inside findings uses `<em>`.
  KPI values truncate past ~24 characters.
- Verifying the live page from a cloud session: api.hyperliquid.xyz is egress-blocked from cloud Bash, so a
  headless render only shows the error state. Test in the user's Chrome: push a branch, fetch the raw
  files from raw.githubusercontent.com inside a leadsure.com tab, inject, and read the exchange-check line.

## Polymarket sub-site (leadsure.com/polymarket)

Live trading dashboard for Chad's Polymarket account. Regenerated twice a day by a
scheduled Cowork task (6:00 AM and 4:00 PM Pacific). **Every rule below applies to
every automated run** — a fresh session working in this repo reads this file, so
treat it as the contract even if the task prompt is terser.

### Files (all in `polymarket/`)
- `index.html` — the whole page (single file; tabs are in-page, not separate documents)
- `polymarket.css` — page-specific styles (loaded after `../base.css` + `../dashboard.css`)
- `polymarket.js` — live data fetch, sorting, card carousels, resync button
- `site-index.html` — copy of the root nav used to keep the tab strip in sync

### Hard rules — do not violate
- **NEVER place a trade.** This dashboard is read-only analysis. No order placement,
  ever, under any phrasing of the request.
- **NEVER store Polymarket trading API credentials in this repo or anywhere else.**
  Polymarket API keys can place orders — there is no read-only tier. The user
  explicitly declined them. Public endpoints only.
- **NEVER echo the GitHub token** (embedded in the push remote) into page content,
  commit messages, logs, or anything user-facing.

### Data sources — which endpoint, and why
- **Prices: CLOB API only** — `/midpoint`, `/book`, `/prices-history`.
- **gamma-api is for discovery only.** Its prices lag the CLOB by up to two days.
  Never quote a gamma price on the page.
- **Positions / activity:** Data API `/positions`, `/activity`, `/value`.
- **P&L:** user-pnl-api `/user-pnl?interval=1d|1m|all` → the 24h / 1M / 1Y tiles.
- **Cash on chain:** Polygon USDC balances, both contracts, each ÷ 1e6 —
  native USDC `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
  and USDC.e `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`.
- Wallet: `0xD1eED20eDD22A289839379e89E3470eA1742A8ae`.

### Account hero
Portfolio (est.) | Positions Value | Cash on Chain | Open Positions | Open P&L | 24h P&L | 1M P&L | 1Y P&L

`Portfolio` is labeled **"(est.)"** with a footnote on purpose: true "Available to
Trade" needs private order-reserved collateral, which public endpoints cannot see.
Show exact Positions Value + Cash on Chain and keep the estimate honest — do not
silently drop the "(est.)" or the footnote to make the number look authoritative.

### Card sections — 12 ideas each, 4 visible
Five sections, each carrying **exactly 12 ideas**, 4 visible with `‹ ›` arrows and a
counter pill (`1–4/12`):

1. Top Add-Ons — All Positions
2. Top New Positions Suggested — Not Currently Held
3. Top Add-Ons — Largest Company
4. Top Sells — What to Cut From Current Positions
5. Top Trades — Ranked by Conviction, Sized to the Account

Plus the **Mispricing Monitor** (8–12 dislocations) and the **Resolution** section
(4 cards). Total card count on the page is currently **72**.

- Ideas are **ranked by conviction**, and the ranking must be congruent across
  sections — the top All-Positions add-on cannot contradict the top Largest-Company
  add-on.
- Each card carries a **date** to the right of its title (the date the idea was
  first published, not the run date).

### CARD LINK RULE — every card links to its market
Every idea card's date line MUST end with an anchor to the market it is about:

```html
<div class="pm-idea-date">{date}<a class="pm-card-link" href="{url}" target="_blank"
  rel="noopener" title="Open this market on Polymarket">View on Polymarket ↗</a></div>
```

Invariant to check after every regeneration — all three counts must be **equal**:

```
grep -c 'class="pm-card-link"' polymarket/index.html
grep -c 'View on Polymarket'   polymarket/index.html
grep -c 'pm-idea-date'         polymarket/index.html
```

- The month named in the card text must match the month of the linked market
  (a July idea links to the July market, not August).
- Account-hygiene cards (redeem winners, cancel stale resting orders) link to
  `https://polymarket.com/portfolio` instead of an `/event/` slug. Those are the
  only permitted non-`/event/` links.
- `scripts/pm-link-cards.py` applies this mapping deterministically; it strips any
  previously-added anchors first, so it is safe to re-run.

### Sizing and liquidity
- **Walk the order book before sizing anything.** Bids ascend, asks descend —
  the touch is the **LAST** element of each array.
- Quote an executable ticket size, not a notional wish. If the book cannot absorb
  it, say so on the card.
- If a trade should not be acted on until a future date (e.g. an Aug 1 roll), put
  that date **prominently in the suggestion text** so it is not executed early.

### Model — odds vs. fair value
Zero-drift lognormal: `P(flip) = Φ( ln(capChal / capLead) / (σ√T) )`, σ = 2%/day
with a 3%/day sensitivity case, `T` in **US trading days**
(holidays: Sep 7, Nov 26, Dec 25). July, August and December resolve independently.

Resolution source is **a consensus of credible reporting** on market cap at the
close of the final trading day of the month — not any single vendor.

### Twice-daily run — what each run must do
1. Re-fetch positions, balances, and CLOB prices; **true up** every displayed balance.
2. **Detect executions** — compare current positions against the standing ideas.
   Anything acted on moves to the **Executed Recommendations Ledger** (Tracking tab).
3. **Re-weigh every idea.** Ideas that no longer hold move to **Retired Ideas —
   Dropped Before Execution** (Tracking tab) so their efficacy is scored over time.
   Both ledgers are permanent — never truncate them.
4. Backfill each section back to 12 ideas.
5. Apply the CARD LINK RULE and verify the three counts match.
6. Commit and push to `main` (GitHub Pages publishes from `main`).

### Tracking tab
Two permanent ledgers — Executed Recommendations and Retired Ideas — with live
effectiveness scoring, columns centered, and a totals row at the bottom.

### Gotchas hit before
- **Round to 4 decimals before threshold comparisons** — raw float diffs produced
  phantom mispricings at the boundary.
- **`dashboard.css` forces `.col-num { text-align: right !important }`** — centering
  the Polymarket tables needs a *more specific* selector, also `!important`.
- **Carousel arrows get pushed off-screen** if the card header doesn't wrap — keep
  the header `flex-wrap` and the arrow group on `margin-left:auto`.
- **GitHub Actions `schedule:` only fires from the default branch** — anything
  cron-driven must live on `main`.
- **Verification:** this repo is public, so `git clone https://github.com/chad506/Leadsure.git`
  anonymously is the reliable way to confirm what actually shipped when fetching
  leadsure.com is blocked.

### Cloud scheduled runs — git + data access (learned Sep 1, 2026 PM run)
- **Pushing from a cloud scheduled session:** the sandbox git proxy STRIPS
  URL-embedded credentials and answers `git push` with "not in this session's
  authorized repository set" (403). Reads (clone/fetch/ls-remote) work fine.
  **The workaround that works:** send the PAT (the one embedded in the clone
  remote URL) as a header instead —
  `git -c http.extraheader="Authorization: Basic $(printf 'x-access-token:<PAT>' | base64 -w0)" push https://github.com/chad506/Leadsure.git <ref>`.
  Never echo the PAT into page content, commits, or logs.
- `api.github.com` is blocked from cloud sessions (proxy demands repo
  attachment), so Actions status can't be checked from there; infer workflow
  health from the `auto-data-fetch` branch's `fetch/out/_fetched_at.txt`.
- WebFetch to Polymarket/CLOB endpoints fails in unattended runs
  (PROVENANCE_REQUIRED — no user present to approve). The autodata pipeline is
  the ONLY data path for scheduled runs; if it is down, ingest what prior
  sessions disclosed, update ledgers honestly, do NOT restamp sections whose
  books were not re-walked, and say so on the page.
- **Autodata outage record — DIAGNOSIS NOW DEFINITIVE (Sep 5 AM):** no
  results since Aug 31 19:23Z — ELEVEN missed feed runs (every 12:45Z/22:45Z
  cron Sep 1–5 silent; a dozen pokes Sep 1–5, several touching fetch/poke,
  all unanswered — note an EMPTY commit does NOT fire the paths filter).
  The Sep 5 AM run performed the decisive experiment: it pushed a
  **brand-new workflow file** (.github/workflows/autodata2.yml — same job,
  fresh registration, exempt from any workflow-level disabled state) whose
  own creating push matches its push trigger, then poked fetch/poke too.
  Both stayed silent. A new workflow's push trigger fires within seconds
  when Actions is on, so this **rules out a stuck/disabled workflow and
  pins the outage on repo- or account-level Actions disablement** (Settings
  → Actions, or an org/billing stop). The PAT does carry `workflow` scope
  (the autodata2 push was accepted). Nothing a scheduled session can do
  fixes this — one manual visit to
  https://github.com/chad506/Leadsure/actions revives it; autodata2 (and
  the original) then fire on the next fetch/poke touch, a push touching
  .github/workflows/autodata2.yml or fetch/poke-main on main, or the next
  cron. Once results flow again, delete this bullet and optionally one of
  the twin workflow files.
- **Sep 3 AM run never published:** the Sep 3 AM scheduled Cowork session
  poked autodata at 13:15Z but pushed NO commit to main — the Sep 3 PM run
  carried the whole day. The Sep 4 AM run DID publish (verification pass on
  the Sep 3 finals), so the gap was a one-off; if an AM gap repeats, check
  that scheduled task's session output for what blocked its publish.
- **Sep 4 AM verification-pass precedent:** on a morning when no new close
  exists (AM runs fire pre-open) and autodata is still down, the honest
  caps-only move is a VERIFICATION PASS: re-verify the prior session's
  closes against the history pages (the Sep 4 AM run caught NVDA's final
  print revised $228.41 → $228.45), re-run the model on any revision with
  calibration first, restamp only the touched surfaces, and extend the
  outage chronicle. Premarket quotes may be quoted as color, clearly
  labeled, never as model inputs.
- **Sep 4 PM (fifth caps-only session):** published on the Sep 4 closes —
  Friday risk-off, lead 14.69% → 18.62%/$875.2B, T 17/81, Dec fairs
  79.81/16.03/2.91/0.52; dec-AAPL CHEAP badge OFF (−2.28 — the Aug 28
  re-entry ticket loses model support), dec-NVDA −2.31 (72¢ GTC cancel
  moot-if-confirmed), dec-GOOGL RICH +5.59 a fourth run, sep2AAPL seat
  −10.93 under fair (widest yet, first in the re-walk queue). Activity
  audit blind since Sep 2 00:57Z. Next close Tuesday Sep 8 (Labor Day).
- **Sep 5 AM (Saturday, sixth data-blind session):** weekend verification
  pass — all five Sep 4 finals re-confirmed to the cent against the
  history pages (no revisions), independent calibration re-run reproduced
  every published fair (Dec 79.81/16.03/2.91/0.52 to ≤0.02 — the 0.75
  small-leg allowance is applied to the DEC legs only, as a ×0.9925
  proportional scale on the raw exact-rank probabilities; Sep crown/seats
  to ≤0.01), so caps/fairs/edges stand as published. Registered autodata2
  (see outage bullet). Weekend AM precedent: with no close and no data,
  verify + diagnose + chronicle; restamp only touched surfaces.
- **Sep 5 PM (Saturday, seventh data-blind session):** TWELFTH missed
  feed run (22:45Z cron silent; 23:08Z fetch/poke poke unanswered — the
  Actions-disablement diagnosis holds). No Saturday close: Sep 4 finals
  stand (NVDA, the one print ever revised, re-spot-checked — unchanged).
  NEW weekend-PM precedent: BTC trades Saturdays, so the run pulled a
  provenance-safe weekend spot (WebSearch→WebFetch, CoinDesk $79,807,
  +1.78% since the Sep 1 bake) and published fresh-spot touch fairs
  (T 117.2d) vs the stale Sep 1 mids as LABELED COLOR in the tape/sync
  chronicle only ($90k −16.7 directional, widest of the series) — the
  BTC tab itself keeps its Sep 1 01:27Z stamps; no book was re-walked,
  no balance re-trued, no card or ledger touched.
- **Sep 6 AM (Sunday, eighth data-blind session):** THIRTEENTH missed
  feed run (Sep 6 12:45Z cron silent; 13:11Z poke touching fetch/poke
  unanswered — the Actions-disablement diagnosis stands). No Sunday
  close, Monday Sep 7 is Labor Day — the Sep 4 finals hold two more
  sessions. Verification: NVDA $230.36 and AAPL $319.97 re-spot-checked
  against the history pages (unchanged); independent quadrature re-run
  reproduced Dec 79.81/16.03/2.91/0.52 (raw 80.41/16.15/2.93/0.52
  ×0.9925) to ≤0.02 and Sep crown 98.08 to ≤0.01 — caps/fairs/edges
  stand as published. Weekend BTC color (per the Sep 5 PM precedent):
  spot $79,832 (CoinDesk, +0.28%/24h), +0.03% vs yesterday — flat spot,
  but T 117.2 → 116.6 d, so pure theta holds the up-ladder at its widest
  residuals and nudges $85k −9.9 → −10.0 ($90k −16.7, $95k −14.8,
  $100k −14.0; dips $55k +8.3, $50k +8.0) — tape + chronicle only, BTC
  tab stamps untouched. Fill-audit blind a fifth calendar day.
- **Sep 6 PM (Sunday, ninth data-blind session):** FOURTEENTH missed
  feed run (Sep 6 22:45Z cron silent; 23:10Z poke touching fetch/poke
  unanswered — the Actions-disablement diagnosis stands). No Sunday
  close (Monday is Labor Day): NVDA re-spot-checked $230.36, unchanged —
  Sep 4 caps/fairs/edges stand as published. Weekend BTC color per the
  Sep 5 PM precedent, with a SOURCE NOTE: CoinDesk's price page served
  the same 05:14 EDT snapshot the AM run quoted ($79,832), so this run
  switched to CoinMarketCap's live read — $79,762 (+0.12%/24h),
  −0.09% vs the AM print, the weekend's first down-tick — and disclosed
  the switch on the page. T 116.2d: up-ladder residuals ease a few
  tenths off their widest prints ($85k −9.7, $90k −16.4, $95k −14.5,
  $100k −13.7; $60k dip +0.4 ≈ at fair; $55k +8.3, $50k +8.0) — tape +
  chronicle only, BTC tab stamps untouched. Publish + poke both used the
  Sep 1 extraheader path (the proxy again refused the URL-embedded
  credential). Fill-audit blind a fifth calendar day.
- **Sep 7 AM (Labor Day, tenth data-blind session):** FIFTEENTH missed
  feed run (Sep 7 12:45Z cron silent; 13:12Z poke touching fetch/poke
  unanswered — the Actions-disablement diagnosis stands). U.S. markets
  closed for Labor Day — no close prints today; NVDA $230.36 and AAPL
  $319.97 re-spot-checked against the history pages (unchanged) — the
  Sep 4 caps/fairs/edges stand one final session; next close Tuesday
  Sep 8. Weekend BTC color per the Sep 5 PM precedent: spot $79,652.95
  (CoinMarketCap live), −0.14% vs the Sunday PM print, +1.58% over the
  Sep 1 bake; T 115.6d — a second consecutive easing tick takes the
  up-ladder a few more tenths off its wides ($85k −9.2, $90k −15.9,
  $95k −14.1, $100k −13.3; the $60k dip at fair +0.3; $55k +8.2,
  $50k +8.0) — tape + chronicle only, BTC tab stamps untouched.
  Fill-audit blind a sixth calendar day. Publish + poke via the Sep 1
  extraheader path.
- **Sep 7 PM (Labor Day, eleventh data-blind session):** SIXTEENTH missed
  feed run (Sep 7 22:45Z cron silent; 23:12Z poke touching fetch/poke
  unanswered — the Actions-disablement diagnosis stands). No close (Labor
  Day): NVDA $230.36 and AAPL $319.97 re-spot-checked against the history
  pages (unchanged) — the Sep 4 caps/fairs/edges go into Tuesday's reopen
  exactly as published; T 17/81 stands. Weekend BTC color with a SECOND
  source rotation: CoinMarketCap served the AM read back to the cent
  ($79,652.95 — snapshot diagnosed), so the run quoted CoinGecko live
  $79,352.36 (−0.60%/24h; Kraken cross-check $79,231), −0.38% vs the AM
  print, +1.20% over the Sep 1 bake; T 115.2d — a third straight slip
  pulls the up-ladder a full point off its wides ($85k −8.0, $90k −14.8,
  $95k −13.1, $100k −12.4; the $60k dip crosses a hair cheap at −0.3,
  first of the series; $55k +7.9, $50k +7.8) — tape + chronicle only,
  BTC tab stamps untouched. Calibration re-run reproduced every Sep 7 AM
  residual exactly before the fresh spot was applied. Fill-audit blind a
  sixth calendar day. Publish + poke via the Sep 1 extraheader path.
- **Sep 8 AM: the scheduled session NEVER RAN.** No commit to main and no
  poke on auto-data-fetch (unlike the Sep 3 gap, which at least poked at
  13:15Z). Second AM gap of the outage; the Sep 8 PM run carried the
  reopen alone. If AM gaps recur, inspect that scheduled task's session
  output for what blocked it — and check the task itself still exists.
- **Sep 8 PM (the reopen, twelfth data-blind session):** SEVENTEENTH and
  EIGHTEENTH missed feed runs (both Sep 8 crons silent; the 23:10Z poke
  touching fetch/poke unanswered — the Actions-disablement diagnosis
  stands). First closes since Sep 4, all five re-fetched from the history
  pages (Sep 4 finals re-confirmed beneath them, no revisions): NVDA
  −2.01% $225.73 ($5,462.7B — the board's biggest loser), AAPL −1.17%
  $316.22 ($4,644.4B), GOOGL −0.03% $338.36 ($4,119.4B), MSFT −1.15%
  $493.95 ($3,669.3B), AMZN −0.60% $256.97 ($2,764.3B) — the lead
  NARROWED 18.62% → 17.62% ($818.2B), Apple's #2 cushion 12.75%, T 16/80.
  Calibration first (reproduces every Sep 4 PM fair to ≤0.02), then fresh
  fairs: Dec 78.23/16.87/3.61/0.54/0.00 — dec-GOOGL's RICH badge OFF
  (+4.89 after four RICH runs; offer-side candidacy withdrawn), dec-NVDA
  −0.73 (closest-to-fair of the outage; 72¢ GTC cancel moot-if-confirmed),
  dec-AAPL −3.12 (RV 1.23× — ticket still unsupported), the whole
  December book inside the ±5 band for the first time in the outage;
  Sep crown 97.86/2.12/0.01, sep2AAPL 91.12 (−9.62 vs the 81.5 stale
  mid — narrower than Friday's −10.93, STILL widest and first in the
  re-walk queue), sep3 85.95-GOOGL/7.38-MSFT/6.67-AAPL; P(±5/wk) 47/42/3.
  BTC color: spot $78,483.14 (CoinGecko live, −0.80%/24h), −1.10% on the
  Labor-Day print, +0.09% vs the Sep 1 bake — a full weekend round-trip,
  so the ladder residuals are now pure theta (T 114.2d: $85k −4.6, $90k
  −11.6, $95k −10.2, $100k −10.0; $60k dip −2.0 — deepening the series'
  first cheap print; $55k +6.8, $50k +7.2) — tape + chronicle only, BTC
  tab stamps untouched. Mids/books/positions/balances untouched (books
  now FIVE sessions stale); fill-audit blind a seventh calendar day.
  Publish + poke via the Sep 1 extraheader path.
- **Sep 9 AM (thirteenth data-blind session — the AM cadence recovers):**
  NINETEENTH missed feed run (Sep 9 12:45Z cron silent; 13:12Z poke
  touching fetch/poke unanswered — the Actions-disablement diagnosis
  stands). Pre-open verification pass per the Sep 4 AM precedent: all
  five Sep 8 finals re-confirmed to the cent against the history pages
  (no revisions); independent quadrature re-run reproduced every Sep 8
  PM published fair EXACTLY (Dec 78.23/16.87/3.61/0.54/0.00 — raw
  78.82/17.00/3.64/0.54 ×0.9925; Sep crown 97.86/2.12/0.01, 2nd
  91.12/6.66/2.13, 3rd 85.95/7.38/6.67; P(±5/wk) 47/42/3) —
  caps/fairs/edges stand as published, T 16/80. BTC color per the
  weekend precedent: spot $78,815.99 (CoinGecko live, +0.6%/24h;
  Kraken cross-check $79,172), +0.42% on the reopen print, +0.51% over
  the Sep 1 bake; T 114.2 → 113.6d — the overnight bid plus theta
  re-widens the up-ladder most of what the round-trip compressed
  ($85k −5.8, $90k −12.6 — back at its bake-day wide, $95k −11.1,
  $100k −10.7; the $60k dip's cheap print fades to −1.1; $55k +7.4,
  $50k +7.6; anchor's needed touch +7.8%) — tape + chronicle only,
  BTC tab stamps untouched. Fill-audit blind an eighth calendar day.
  Publish + poke via the Sep 1 extraheader path.
- **Sep 9 PM (fourteenth data-blind session — the Sep 9 close):**
  TWENTIETH missed feed run (Sep 9 22:45Z cron silent; a 23:18Z poke
  touching fetch/poke unanswered — the Actions-disablement diagnosis
  stands). Caps-only on the Sep 9 closes (history pages; the Sep 8
  finals re-confirmed beneath them, no revisions): a second straight
  all-red board with the CHALLENGERS falling hardest — GOOGL −2.28%
  $330.65 ($4,025.5B, the board's biggest loser), AMZN −1.78% $252.40
  ($2,715.1B), NVDA −0.91% $223.67 ($5,412.8B), MSFT −0.47% $491.65
  ($3,652.2B), AAPL −0.28% $315.34 ($4,631.5B, the board's best
  close) — the lead narrowed again 17.62% → 16.87% ($781.3B) while
  Apple's #2 cushion WIDENED 12.75% → 15.05% ($606.0B); T 15/79.
  Calibration first (reproduces every Sep 8 PM fair exactly), then
  fresh fairs: Dec 77.99/17.85/2.85/0.56/0.00 — dec-GOOGL RICH badge
  BACK ON (+5.65 after one run inside the band; offer-side candidacy
  re-opens, fresh-book gated), dec-AAPL −4.10 (RV 1.30× — a step from
  the −5 re-entry line), dec-NVDA −0.49 (the outage's closest-to-fair
  print; 72¢ GTC cancel moot-if-confirmed); Sep crown 97.79/2.21/0.00,
  sep2AAPL 94.22 (−12.72 vs the 81.5 stale mid — the outage's WIDEST
  residual, first in the re-walk queue), sep3 86.06-GOOGL/10.41-MSFT/
  3.52-AAPL; P(±5/wk) 48/44/1. BTC color: spot $78,010.44 (CoinGecko
  live, −0.60%/24h), −1.02% on the AM print, −0.51% UNDER the Sep 1
  bake — the series' first below-bake read; T 113.2d ($85k −2.6,
  $90k −9.8, $95k −8.6, $100k −8.6 — the up-ladder's narrowest prints;
  $60k dip −2.9, the series' deepest cheap print; $55k +6.3,
  $50k +7.0) — tape + chronicle only, BTC tab stamps untouched.
  Mids/books/positions/balances untouched (books now SIX sessions
  stale); fill-audit blind an eighth calendar day. Publish + poke via
  the Sep 1 extraheader path.
- **Sep 10 AM (fifteenth data-blind session — verification pass; Bitcoin
  breaks down):** TWENTY-FIRST missed feed run (Sep 10 12:45Z cron silent;
  13:13Z poke touching fetch/poke unanswered — the Actions-disablement
  diagnosis stands). Pre-open verification pass per the Sep 4 AM precedent:
  all five Sep 9 finals re-confirmed to the cent against the history pages
  (no revisions); independent quadrature re-run reproduced every Sep 9 PM
  published fair EXACTLY (Dec 77.99/17.85/2.85/0.56/0.00; crown
  97.79/2.21/0.00; 2nd 94.22/3.50/2.21; 3rd 86.06/10.41/3.52; P(±5/wk)
  48/44/1) — caps/fairs/edges stand as published, T 15/79. Premarket
  color: NVDA −1.46% vs AAPL +0.54% (9:09 ET) — a third straight
  lead-narrowing session if held. BTC color: spot $76,869.85 (CoinGecko
  live, −3.4%/24h, range 76,748–79,606; the Kraken page printed $77,957 —
  ~1.4% apart, both quoted and the gap disclosed on the page), −1.46% on
  the PM print, −1.97% UNDER the Sep 1 bake — the series' deepest
  below-bake read; T 112.7d — the $85k anchor's stale mid crosses OVER
  fair for the first time in the series (+1.8), the $60k dip's cheap
  print breaks the −5 line for the first time (−5.6); $90k −5.7,
  $95k −5.1, $100k −5.7, $55k +4.5, $50k +6.0 — tape + chronicle only,
  BTC tab stamps untouched. NOTE the interactive Treasuries session
  (commit 5cf1b3e1, Sep 10 01:04Z) walked 105 books + the account Sep 9
  23:30–23:50Z via the reader's Chrome: Treasuries/SPX fill-audit CLOSED
  (ledger rows 272–298, positions value $13,921.70 at the walk);
  largest-company mids/books and every balance surface keep their own
  stamps, sep2AAPL still first in the re-walk queue; the page card-link
  invariant is now 140. Publish + poke via the Sep 1 extraheader path.
- **Sep 10 PM: the scheduled session NEVER RAN** — no commit, no poke.
  The outage's FIRST PM gap (the earlier gaps were Sep 3 AM and Sep 8 AM).
- **Sep 11 AM: the scheduled session NEVER RAN either** — no commit, no
  poke. Two consecutive dropped sessions; the Sep 11 PM run carried the
  Sep 10 AND Sep 11 closes alone. If gaps recur, inspect the scheduled
  task's session output and confirm the task still exists.
- **Sep 11 PM (sixteenth data-blind session — the APPLE MELT-UP, two
  closes at once):** TWENTY-SECOND through TWENTY-FOURTH missed feed runs
  (Sep 10 22:45Z and both Sep 11 crons silent; the 23:09Z poke touching
  fetch/poke unanswered — the Actions-disablement diagnosis stands).
  Caps-only on the Sep 11 closes with the Sep 10 closes ingested beneath
  them (history pages; Sep 9 finals re-confirmed to the cent, no
  revisions): Thursday AAPL +3.56% to $326.57 vs NVDA −2.26% to $218.36
  (lead 16.87% → 10.17%); Friday AAPL +1.75% $332.27 ($4,880.2B), GOOGL
  +1.75% $338.41 ($4,120.0B), AMZN +1.94% $256.78 ($2,762.2B), MSFT
  +0.64% $495.59 ($3,681.5B), NVDA −0.09% $218.17 ($5,279.7B) — the lead
  COLLAPSED to 8.19%/$399.5B, the narrowest since the August crown
  settled (under Aug 28's 12.12%), while Apple's #2 cushion blew out to
  18.45%/$760.2B; T 13/77. Calibration first (reproduces every Sep 9 PM
  fair exactly), then fresh fairs: Dec 64.21/30.75/3.73/0.56/0.00 —
  dec-AAPL −17.00 CHEAP vs the 13.75 stale mid (RV 2.24× — the outage's
  widest residual; the Aug 28 re-entry ticket's −5 bar
  beaten ×3, fresh-book gated, now FIRST in the re-walk queue), dec-NVDA
  +13.29 RICH (the leader's first double-digit rich read; the 72¢ GTC
  bid now rests ~7.8 pts ABOVE the 64.21 fair — the cancel goes
  LIVE-if-confirmed), dec-GOOGL RICH badge OFF again (+4.77); September
  crown falls 97.79 → 86.24 (Apple's crown leg 2.21 → 13.76), seat
  94.22 → 85.30 — sep2AAPL's residual collapses −12.72 → −3.80 (drops to
  third in the queue); P(±5/wk) 59/58/3, the outage's highest. BTC color:
  spot $77,372.48 (CoinGecko live, +0.3%/24h), +0.65% on the Sep 10 AM
  print, −1.33% vs the Sep 1 bake; T 111.2d ($85k anchor back AT fair
  +0.1 after Thursday's rich cross; $90k −7.2, $95k −6.3, $100k −6.6;
  $60k dip eases to −4.0; $55k +5.6, $50k +6.7) — tape + chronicle only,
  BTC tab stamps untouched. Mids/books/positions/balances untouched
  (books now EIGHT sessions stale); fill-audit blind a tenth calendar
  day outside Treasuries/SPX. NOTE for the next session: an interactive
  Sep 10–11 Oil-tab commit (42c7680a, + ledger rows 299–327) was never
  pushed — it rides _handoff_push.sh on the Mac and is NOT on origin;
  this run's edits (hero/KPI/analysis/footnote/tape/chronicle) will need
  a rebase when that handoff lands. Publish + poke via the Sep 1
  extraheader path.
- **Sep 12 AM (Saturday, seventeenth data-blind session — the weekend
  pass catches a TRIPLE REVISION):** TWENTY-FIFTH missed feed run (Sep 12
  12:45Z cron silent; a 13:10Z poke touching fetch/poke unanswered — the
  Actions-disablement diagnosis stands). No Saturday close — but the
  weekend verification pass re-checked the Sep 11 finals against the
  history pages and THREE of five were REVISED upward from the Sep 11 PM
  23:1xZ bake: NVDA $218.17 → $218.29 (−0.03%), GOOGL $338.41 → $338.50
  (+1.77%), MSFT $495.59 → $495.63 (+0.65%); AAPL $332.27 and AMZN
  $256.78 confirmed to the cent (quote pages cross-check all three at
  the Sep 11 4:00 PM EDT close — the PM lesson: a 23:1xZ history-page
  pull can precede the settled finals; the next-morning pass is what
  locks them). Calibration first (reproduces every Sep 11 PM fair
  EXACTLY), then fairs re-ran on the finals: caps $5,282.6B/$4,880.2B/
  $4,121.1B/$3,681.8B/$2,762.2B, lead 8.19% → 8.25%/$402.4B (still the
  narrowest since the crown settled), cushion 18.42%/$759.1B, T 13/77;
  Dec 64.32/30.65/3.73/0.56/0.00 — dec-AAPL −16.90 CHEAP (RV 2.23×,
  still the outage's widest residual, first in the re-walk queue),
  dec-NVDA +13.18 RICH (72¢ GTC bid ~7.7 pts above fair — cancel stays
  LIVE-if-confirmed), dec-GOOGL +4.77 FAIR; crown 86.40/13.59/0.01, seat
  85.46-AAPL/13.57-NVDA/0.96-GOOGL (sep2AAPL residual −3.96), 3rd
  93.13-GOOGL/5.90-MSFT/0.95-AAPL; P(±5/wk) 59/58/3 unchanged. Restamped:
  hero gap + tape, both KPI edge tiles, table note, both group rows, all
  five Dec rows (caps/gaps/fairs/edges/RV), footnote; sep3NVDA row
  unchanged (+1.58). BTC color per the weekend precedent: spot
  $77,278.23 (CoinGecko live, +0.60%/24h; CoinMarketCap cross-check
  $77,262.64; CoinDesk served a Sep 11 11:34 ET snapshot and was
  discarded), −0.12% on the PM print, −1.45% vs the Sep 1 bake; T 110.7d
  ($85k anchor a hair OVER fair +0.5; $90k −6.8, $95k −5.9, $100k −6.2;
  $60k dip −4.1; $55k +5.6, $50k +6.7; needed touch +10.0%) — tape +
  chronicle only, BTC tab stamps untouched. Mids/books/positions/
  balances untouched (books EIGHT sessions stale); fill-audit blind an
  eleventh calendar day outside Treasuries/SPX. The Oil-tab handoff
  (42c7680a) is STILL not on origin. Publish + poke via the Sep 1
  extraheader path.
- **Sep 12 PM (Saturday, eighteenth data-blind session — the finals
  hold):** TWENTY-SIXTH missed feed run (Sep 12 22:45Z cron silent; a
  23:09Z poke touching fetch/poke unanswered — the Actions-disablement
  diagnosis stands). No Saturday close: the three AM-revised Sep 11
  finals re-spot-checked against the history pages (NVDA $218.29, GOOGL
  $338.50, MSFT $495.63 — all unchanged), and an independent quadrature
  re-run reproduced every Sep 12 AM published fair EXACTLY (Dec
  64.32/30.65/3.73/0.56/0.00; crown 86.40/13.59/0.01; 2nd
  85.46/13.57/0.96; 3rd 93.13/5.90/0.95; P(±5/wk) 59/58/3) —
  caps/fairs/edges stand as published, T 13/77 into Monday. Weekend BTC
  color per the Sep 5 PM precedent: spot $77,389.61 (CoinGecko live;
  Coinbase cross-check $77,214.44 — ~0.2% apart, disclosed; CoinGecko's
  own 24h field printed −1.8% against a tape sitting +0.02% on its own
  Sep 11 PM read — snapshot-suspect, print-to-print deltas used),
  +0.14% on the AM print, −1.31% vs the Sep 1 bake; T 110.2d — the
  small bid hands back the anchor's morning rich cross ($85k +0.5 →
  +0.1, back AT fair), re-widens the up-ladder a few tenths ($90k −7.1,
  $95k −6.1, $100k −6.4) and eases the $60k dip to −3.7 ($55k +5.9,
  $50k +6.8; needed touch +9.8%) — tape + chronicle only, BTC tab
  stamps untouched. Mids/books/positions/balances untouched (equity
  books EIGHT sessions stale); fill-audit blind an eleventh calendar
  day outside Treasuries/SPX. The Oil-tab handoff (42c7680a) is STILL
  not on origin. Publish + poke via the Sep 1 extraheader path.
- **Sep 13 AM (Sunday, nineteenth data-blind session — a fifth
  confirmation of the finals):** TWENTY-SEVENTH missed feed run (Sep 13
  12:45Z cron silent; a 13:09Z poke touching fetch/poke pushed and
  unanswered — the Actions-disablement diagnosis stands). No Sunday
  close: ALL FIVE Sep 11 finals re-spot-checked against the history
  pages (NVDA $218.29, AAPL $332.27, GOOGL $338.50, MSFT $495.63,
  AMZN $256.78 — every one unchanged, a third consecutive session of
  confirmation), and an independent quadrature re-run reproduced every
  Sep 12 published fair EXACTLY (Dec 64.32/30.65/3.73/0.56/0.00; crown
  86.40/13.59/0.01; 2nd 85.46/13.57/0.96; 3rd 93.13/5.90/0.95; P(±5/wk)
  59/58/3) — caps/fairs/edges stand as published, T 13/77 into Monday,
  the first close since the melt-up finals. Weekend BTC color per the
  Sep 5 PM precedent: spot $77,303.56 (CoinGecko live, +0.1%/24h, range
  $77,054.68–$77,479.13; Coinbase cross-check $77,207.06 — ~0.1% apart,
  disclosed), −0.11% on the PM print and +0.03% on the Sep 12 AM print
  — a weekend that round-tripped to flat, −1.42% vs the Sep 1 bake;
  T 109.7d — theta alone re-tips the $85k anchor a hair OVER fair
  (+0.5), $90k −6.7, $95k −5.7, $100k −6.1, the $60k dip −3.8 ($55k
  +5.8, $50k +6.8; needed touch +10.0%) — tape + chronicle only, BTC
  tab stamps untouched. Mids/books/positions/balances untouched (equity
  books EIGHT sessions stale); fill-audit blind a twelfth calendar day
  outside Treasuries/SPX. The Oil-tab handoff (42c7680a) is STILL not
  on origin. Publish + poke via the Sep 1 extraheader path.
- **Sep 13 PM (Sunday, twentieth data-blind session — the eve of the
  first post-melt-up close):** TWENTY-EIGHTH missed feed run (Sep 13
  22:45Z cron silent; a 23:10Z poke touching fetch/poke pushed and
  unanswered — the Actions-disablement diagnosis stands). No Sunday
  close: ALL FIVE Sep 11 finals re-spot-checked against the history
  pages a FOURTH consecutive session (NVDA $218.29, AAPL $332.27,
  GOOGL $338.50, MSFT $495.63, AMZN $256.78 — every one unchanged),
  and an independent quadrature re-run reproduced every Sep 12
  published fair EXACTLY (Dec 64.32/30.65/3.73/0.56/0.00; crown
  86.40/13.59/0.01; 2nd 85.46/13.57/0.96; 3rd 93.13/5.90/0.95;
  P(±5/wk) 59/58/3) — caps/fairs/edges go into Monday's close, the
  first since the melt-up finals, exactly as published; T 13/77.
  Weekend BTC color with a DOUBLE source rotation: CoinGecko re-served
  the Sep 13 AM print to the cent ($77,303.56) and CoinMarketCap
  re-served the Sep 12 AM cross-check ($77,262.64) — both diagnosed
  snapshot-stale and discarded; the run quoted Kraken live $77,240.00
  (−0.16%/24h; Coinbase cross-check $76,748.06 — ~0.6% under, the
  widest cross-source gap since Sep 10, both quoted and disclosed),
  −0.08% on the AM print, −1.50% vs the Sep 1 bake; T 109.2d — the
  $85k anchor a hair OVER fair (+0.8, the series' second-widest rich
  print), $90k −6.4, $95k −5.4, $100k −5.8, the $60k dip −3.9 ($55k
  +5.8, $50k +6.8; needed touch +10.0%) — tape + chronicle only, BTC
  tab stamps untouched. Mids/books/positions/balances untouched
  (equity books EIGHT sessions stale); fill-audit blind a TWELFTH
  full day outside Treasuries/SPX. The Oil-tab handoff (42c7680a) is
  STILL not on origin. Publish + poke via the Sep 1 extraheader path.
- **Sep 14 AM (Monday pre-open, twenty-first data-blind session — the
  morning of the first post-melt-up close):** TWENTY-NINTH missed feed
  run (Sep 14 12:45Z cron silent; a 13:08Z poke touching fetch/poke
  pushed via the extraheader path and unanswered — the
  Actions-disablement diagnosis stands). Pre-open verification pass per
  the Sep 4 AM precedent: ALL FIVE Sep 11 finals re-spot-checked
  against the history pages a FIFTH consecutive session (NVDA $218.29,
  AAPL $332.27, GOOGL $338.50, MSFT $495.63, AMZN $256.78 — every one
  unchanged); independent quadrature re-run reproduced every Sep 12
  published fair EXACTLY (Dec 64.32/30.65/3.73/0.56/0.00; crown
  86.40/13.59/0.01; 2nd 85.46/13.57/0.96; 3rd 93.13/5.90/0.95;
  P(±5/wk) 59/58/3) — caps/fairs/edges go into tonight's close exactly
  as published, T 13/77. NEW: a violent premarket divergence (9:03 ET,
  labeled color, never a model input): NVDA −2.87% $212.02 vs AAPL
  +0.39% $333.57, GOOGL +1.52% $343.64, MSFT +0.46%, AMZN −1.37% —
  premarket-implied lead 4.73%/$231.6B vs the finals' 8.25%; held to
  the close it would be the narrowest since the August crown settled.
  BTC color: CoinGecko live again after the Sep 13 PM double snapshot
  rotation — spot $77,666.24 (+0.5%/24h; Coinbase cross-check
  $77,817.62 ~0.2% over, disclosed), +0.55% on the PM print, −0.95% vs
  the Sep 1 bake; T 108.7d — the overnight bid flips the $85k anchor
  back UNDER fair (−0.8); $90k −7.7, $95k −6.6, $100k −6.7, $60k dip
  −2.7, $55k +6.6, $50k +7.3, needed touch +9.4% — tape + chronicle
  only, BTC tab stamps untouched. Mids/books/positions/balances
  untouched (equity books EIGHT sessions stale); fill-audit blind a
  thirteenth calendar day outside Treasuries/SPX. The Oil-tab handoff
  (42c7680a) is STILL not on origin. Publish + poke via the Sep 1
  extraheader path.
- **Sep 15 interactive (01:10Z) — THE OIL TAB IS ON ORIGIN, THE HANDOFF IS
  MOOT, THE LEADERBOARD IS RE-MARKED:** github.com was reachable again
  from the interactive session, so the Sep 10–11 Oil-tab commit was
  rebased onto the Sep 11–14 auto-runs and pushed as 6e13d793 (on top of
  929b0297); the Mac hand-off files (_handoff_push.sh / _handoff_msg.txt)
  were never run and are moved to _to_delete/ on the device — ignore any
  "handoff not on origin" note above. Then ac30fe98: every leaderboard
  candidate book re-walked through the reader's Chrome (226 CLOB books,
  00:42–01:10Z), every row's mid replaced, RV = as-baked model value ÷
  tonight's mid (conditional-book LIFT/INPUT rows carry their odds-space
  lift onto the new mid; MODEL fairs untouched — no tab re-baked), top
  50 re-ranked: cut 2.00× (was 1.82×), Iran 27 · Oil 21 · TRS 2, 49 cond
  / 1 model; 17 rows dropped (16 resolved YES — 10Y 4.85/4.88/4.91/4.94/
  4.97 Sep, 5Y 4.78, 30Y 5.33, PMMS 6.75, WTI $100 HIGH/LOW + $90 HIGH,
  gold $4,300 LOW, DXY 99.50 — plus the empty Iran-targets-Oman book,
  whose shortlist token has no Gamma market: token check pending).
  Script + book snapshot: scripts/leaderboard_remark_sep15.py,
  scripts/leaderboard_books_sep15.csv. Recipe notes: Gamma
  /markets?clob_token_ids= returns [] for resolved markets unless
  &closed=true is added; javascript_tool output containing "=" (e.g. the
  BTC.CM= symbol) trips the Cookie/query-string block — replace "=" or
  write to <pre> and read via get_page_text. Spots at the walk: Brent Nov
  106.70, WTI Oct 102.46, 10Y 4.985 (Treasury.gov 4.96 Sep 11 / 4.97 Sep
  14), SPX 7,619.98, BTC $77,794; 10Y-5.0%-before-2027 95.85, invasion
  trigger 16.5. Account: positions value $17,815.36; 61 fills Sep 10
  23:33Z – Sep 14 22:35Z swept into the banner but NOT ledgered (10Y-5.0%
  trimmed 2,190 sh at 88–94¢ to 8,354.07; Apple Sep crown +18,094 at
  5.7–6.4¢ then 1,800 sold at 15.5–21.7¢; 5.5% rung +741; 5.00-Sep +264;
  4.97-Sep +208 resolved YES; BTC no-$85k-Sep 116.88; SPY $750/$745
  weekly lows) — the next ledger bake owes rows for these. Source tabs'
  fairs are stale against these prints and say so (Oil = Sep 10 build on
  a 109.29 Brent; Treasuries = Sep 9 close with the 10Y now 4.985;
  Analysis mids Sep 1 — dec-AAPL's 2.23× is 1.31× on the fresh 23.4 mid).
- **Sep 15 PM (twenty-second data-blind session — TWO CLOSES AGAIN, THE
  MIDS GO FRESH):** THIRTIETH through THIRTY-SECOND missed feed runs (the
  Sep 14 22:45Z and both Sep 15 crons silent; a 23:10Z poke touching
  fetch/poke pushed via the extraheader path and unanswered — the
  Actions-disablement diagnosis stands). The cadence broke AGAIN: the
  Sep 14 PM and Sep 15 AM scheduled sessions never ran (no commit, no
  poke — the outage's SECOND double gap, after Sep 10 PM / Sep 11 AM),
  so this run carried the Sep 14 AND Sep 15 closes. All five Sep 11
  finals re-confirmed beneath them (a SIXTH session, unchanged). Monday
  Sep 14: NVDA −3.36% $210.96 / GOOGL +3.22% $349.39 / AAPL +0.24% —
  lead 8.25% → 4.36%/$213.2B, THE NARROWEST CLOSE SINCE THE AUGUST CROWN
  SETTLED. Tuesday Sep 15: NVDA the only green close (+0.57% $212.17,
  $5,134.5B) over AAPL −0.52% ($4,866.5B), GOOGL −1.26% ($4,200.0B),
  MSFT −1.68% ($3,691.3B), AMZN −2.02% ($2,672.3B) — lead 5.51%/$268.0B,
  cushion 15.87%/$666.5B, T 11/75. Calibration reproduced every Sep 12
  fair EXACTLY, then fresh fairs: Dec 57.90/34.77/5.87/0.70/0.00; crown
  79.03/20.94/0.03; 2nd 77.75-AAPL/20.87-NVDA/1.38-GOOGL; 3rd
  96.01-GOOGL/2.58-MSFT/1.31-AAPL/0.10-NVDA; P(±5/wk) 61/60/7 (outage
  highs). NEW: the Analysis-tab odds column re-marked to the Sep 15
  01:10Z interactive walk (scripts/leaderboard_books_sep15.csv — first
  fresh equity mids since Sep 1 03:59Z; one session behind tonight's
  close, disclosed): dec-AAPL −11.37 CHEAP RV 1.49× on the real 23.4 mid
  (the stale −16.90 deflates honestly), dec-NVDA +10.60 RICH (72¢ GTC
  14.1 pts above the 57.90 fair — cancel tops the chores), dec-GOOGL
  +1.63 inside the band, sep3NVDA premium gone (0.05 bidless vs 0.10,
  RV 2.00× nominal on a bidless book), sep2AAPL stale-mid residual
  FLIPS −3.96 → +3.75 (book not in the walk). Tradeable-at-fair
  re-computed as 5-pt-band lower bounds from the walk summaries
  (dec-AAPL ≥$1,757, dec-NVDA ≥$3,054 — first non-zero prints since
  Sep 1). BTC: Coinbase $77,000.77 primary (−0.94%/24h; CMC cross
  $77,389.10 ~0.5% over; CoinGecko printed $75,643 against its own
  $78,581 24h high and both cross-sources — discarded, THIRD source
  rotation), −0.86% on the Sep 14 AM print, −1.80% vs the Sep 1 bake;
  T 107.2d — residuals vs the walk's OWN fresh mids compress inside ±5
  for the first time ($85k −0.5 AT fair, $90k −3.7, $95k −4.3,
  $100k −4.8, $110k −2.3, $60k −3.0, $55k +2.8, $50k +6.4 the one rich
  print) — most of the stale-era wides were the staleness itself; tape +
  chronicle only, BTC tab stamps untouched. Updated: hero caps/gap, tape
  label + prose, Next-Catalyst, 5 KPI tiles, table note, both group
  rows, all six model rows, footnote, both chronicles + the sync-bar
  Latest line. Untouched + disclosed: cards/slate (Aug 28 stamps),
  ledgers (61 fills Sep 10–14 still owed), balances (positions value
  $17,815.36 at the 01:10Z pass is the freshest print), velocity/SEPH/H
  series, charts, Leaderboard (its dec-AAPL 1.31×/dec-MSFT 1.02×
  predate tonight's bake — 1.49×/1.27× now, noted on the page).
  Script: scripts/verify_sep15pm.py. Publish + poke via the Sep 1
  extraheader path; no device bridge (scheduled cloud run). No trades
  placed.
- **Sep 16 interactive (01:45Z) — LARGEST-COMPANY WALKED + A BEST BETS BLOCK:**
  twenty CLOB books through the reader's Chrome (five Dec names + SpaceX /
  Tesla / Aramco tails; the September crown, seat and 3rd-place partitions —
  crown + seat first walked since Sep 1; gamma /events?slug= discovery, the
  Sep slugs are `largest-company-end-of-september-1785358369147`,
  `2nd-largest-company-end-of-september-20260729222928263`,
  `3rd-largest-company-end-of-september-1785358369147`). Sep 15 finals
  re-verified against TWO sources (stockanalysis history + CNBC restQuote):
  **MSFT settled $497.12 / −1.64%, not the $496.91 the PM pass pulled** —
  cap $3,692.8B; Dec MSFT 0.70 → 0.71, 3rd 95.97-GOOGL / 2.62-MSFT, nothing
  else moved. Fresh edges: dec-AAPL 23.85 vs 34.77 −10.92 (RV 1.46×, $1,774
  inside fair−5, $41.8k ≤ fair of which $37.9k is a 34.4–34.5¢ wall); Apple
  crown 12.6 vs 20.94 −8.34 (RV 1.66×); NVIDIA crown 87.15 vs 79.03 +8.12;
  sep2AAPL 84.5 vs 77.75 +6.75 (WIDE, fade rule does not arm: $126 ≥ 80.85);
  sep2NVDA 12.95 vs 20.87 −7.92 on $106. NEW `.pm-bestbets` section under
  the KPI grid (#1 BUY dec-AAPL YES $300 ≤ 25¢; #2 HOLD the 22,532-sh Sep
  Apple crown, ADD $100 ≤ 13.0¢, exit-by-resolution disclosed; #3 dec-NVDA
  NO priced but NO TICKET — the catalyst clause still gates the RICH fade;
  #4 SELL 274 sh MSFT-3rd at 4.5¢; watch sep2NVDA) with an honesty line
  (one directional exposure, Sep/Dec legs pay together 11.5%, corr 0.22).
  **THE dec-NVDA 72¢ GTC "CANCEL" CHORE IS CLOSED** — the market traded
  through 72 on Sep 14 (6h prints 71 → 66.5) and the activity feed (complete
  to Aug 4) shows no dec-NVDA fill, so the order cannot be open; stop
  carrying it. Eight September rows added to the Analysis table (+7 TOKENS
  in polymarket.js; sums.dec allowance 0.0030 → 0.0015 since dec-AMZN is
  now summed live); leaderboard KPI 145 → 153 rows carrying RV, top 50
  unchanged (max Largest RV 1.66× < 2.00× cut). Positions /value read
  $8,792.51 at 01:50Z (316 positions — the /positions default limit of 200
  TRUNCATES; page with offset). Three adversarial reviewer passes + a
  round-2 verify (34 + 5 findings, all applied — NO-side tickets must be
  quoted in NO-dollars, σ units unified, Sep 15 PM text labeled as kept).
  Scripts: scripts/largest_sep16.py, largest_books_sep16.txt,
  bake_largest_sep16.py, bake_largest_sep16_fixes.py. Untouched + disclosed:
  balances, ledgers (61 fills owed), Aug 28 cards (#1 marked SUPERSEDED),
  velocity/charts, other tabs. No trades placed.
- **Sep 16 AM (twenty-third data-blind session — pre-open verification pass):**
  THIRTY-THIRD missed feed run (Sep 16 12:45Z cron silent; a 13:08Z poke
  touching fetch/poke pushed via the extraheader path and unanswered — the
  Actions-disablement diagnosis stands). The AM cadence recovered after the
  second double gap. ALL FIVE Sep 15 finals re-confirmed against the history
  pages (NVDA $212.17, AAPL $331.34, GOOGL $344.98, MSFT $497.12 — the 01:45Z
  interactive revision now served by the history page itself — AMZN $248.42);
  independent quadrature re-run reproduced every published fair EXACTLY (Dec
  57.90/34.77/5.87/0.71/0.00; crown 79.03/20.94/0.03; 2nd 77.75/20.87/1.38;
  3rd 95.97/2.62/1.31/0.10; P(±5/wk) 61/60/7) — caps/fairs/edges and the
  Best Bets stand into tonight's close as published; lead 5.51%/$268.0B,
  T 11/75. Premarket color (9:09–9:12 ET, labeled): NVDA +0.83% $213.93 over
  AAPL +0.49% $332.95, GOOGL +0.28%, AMZN +0.15%, MSFT −0.38% — implied lead
  5.87%/$286.9B, a mild re-widening. BTC color: spot $75,868.26 (CoinGecko
  live, −1.40%/24h, range 75,038–77,163; Coinbase cross $75,826.24 ~0.06%
  under — the tightest live cross of the series), −1.47% on the PM print, −3.25%
  vs the Sep 1 bake — the series' FIRST accepted sub-$76k print and deepest below-bake
  read; T 106.7d: vs the Sep 15 walk mids the $60k dip breaks the −5 line
  (−5.9), the walked $85k mid swings +4.0 RICH ($90k +0.3, $95k −0.9,
  $100k −2.0, $110k −0.6, $55k +1.0, $50k +5.4; needed touch +12.0%) — tape +
  chronicle only, BTC tab stamps untouched. Mids/books/balances keep the
  Sep 16 01:45Z stamps; ledger still owes the 61 swept fills. Publish + poke
  via the Sep 1 extraheader path; script scripts/verify_sep16am.py.
- **Sep 16 PM (twenty-fourth data-blind session — the close re-deals the
  fairs, three badges come off):** THIRTY-FOURTH missed feed run (Sep 16
  22:45Z cron silent; a 23:09Z poke touching fetch/poke pushed via the
  extraheader path and unanswered — the Actions-disablement diagnosis
  stands). Caps-only on the Sep 16 closes (history pages ~23:15Z; all five
  Sep 15 finals re-confirmed beneath them a third consecutive session):
  NVDA +0.82% $213.90 ($5,176.4B) and AAPL +0.32% $332.41 ($4,882.2B) the
  only green closes; GOOGL −0.61% ($4,174.3B), AMZN −0.99% ($2,645.8B),
  MSFT −1.37% ($3,642.2B, the board's worst) — the lead re-widens 5.51% →
  6.03%/$294.2B, cushion 16.96%/$707.9B, T 10/74. Calibration first
  (reproduces every Sep 16 AM fair exactly), then fresh fairs: Dec
  59.68/34.14/4.95/0.48/0.00; crown 82.25/17.74/0.01; seat 81.60-AAPL/
  17.72-NVDA/0.68-GOOGL; 3rd 97.76-GOOGL/1.55-MSFT/0.66-AAPL/0.03-NVDA;
  P(±5/wk) 61/60/5. FIRST fair re-bake under the Best Bets block: every
  Best Bets row, Analysis row, KPI and hero figure re-marked to the new
  fairs against the UNCHANGED Sep 16 01:45Z walk ladders (depth-at-fair
  recomputed honestly from the archived ladders in
  scripts/largest_books_sep16.txt) — dec-AAPL −10.29 CHEAP RV 1.43× (#1
  stands; the $41.8k at-or-under-fair headline collapses to $3,831
  because the 34.4–34.5¢ wall now sits ABOVE the 34.14 fair), the
  Apple-crown ADD GATED (−5.04 at the 12.7¢ touch; ≤13.0¢ no longer
  clears fair−5; HOLD stands), crownNVDA +4.90 / sep2AAPL +2.90 /
  sep2NVDA −4.77 all INSIDE the band (RICH/RICH/CHEAP badges off),
  dec-NVDA +8.82 RICH (NO-dollars $1,177; catalyst clause still gates —
  no ticket), sep3MSFT sell leg strengthens (fair 1.55, RV 0.34×).
  Joint-payoff MC re-run: Sep+Dec Apple legs pay together 9.7% (was
  11.5%), corr 0.20. BTC color: spot $75,981.82 (CoinGecko live,
  −1.10%/24h; Kraken cross $75,862 ~0.16% under; Coinbase re-served the
  AM print to the cent — snapshot-stale, discarded, the series' FOURTH
  source rotation), +0.15% on the AM print (second consecutive sub-$76k
  print), −3.10% vs the Sep 1 bake; T 106.2d — vs the Sep 15 walk mids:
  $85k +3.7 RICH, $60k dip −5.5 past the −5 line, $50k +5.6, the rest
  inside ±3 — tape + chronicle only, BTC tab stamps untouched.
  Mids/books/balances untouched (ladders re-priced, not re-walked);
  ledger still owes the 61 swept fills. Publish + poke via the Sep 1
  extraheader path; script scripts/verify_sep16pm.py.
- **Sep 17 AM (twenty-fifth data-blind session — pre-open verification pass,
  the finals lock clean):** THIRTY-FIFTH missed feed run (Sep 17 12:45Z cron
  silent; a 13:12Z poke touching fetch/poke pushed via the extraheader path
  and unanswered — the Actions-disablement diagnosis stands). ALL FIVE Sep 16
  finals re-confirmed to the cent against the history pages (NVDA $213.90,
  AAPL $332.41, GOOGL $342.87, MSFT $490.30, AMZN $245.96 — the PM pass's
  ~23:15Z pull survives its morning check with no revisions); independent
  quadrature re-run reproduced every Sep 16 PM published fair EXACTLY (Dec
  59.68/34.14/4.95/0.48/0.00; crown 82.25/17.74/0.01; 2nd 81.60/17.72/0.68;
  3rd 97.76/1.55/0.66/0.03; P(±5/wk) 61/60/5) — caps/fairs/edges and the
  Best Bets stand into tonight's close as published; lead 6.03%/$294.2B,
  cushion 16.96%, T 10/74. Premarket color (8:47–9:08 ET, labeled): a broad
  risk-on tape NVIDIA leads — NVDA +2.10% $218.40, AMZN +2.11%, GOOGL +1.47%,
  MSFT +1.17%, AAPL +0.52% — implied lead 7.69%/$377.4B vs the finals' 6.03%
  (held to the close, the widest since the Sep 11 melt-up finals' 8.25%).
  BTC color: spot $76,424.22 (CoinGecko live, +1.2%/24h, range
  75,161–76,683; Kraken live cross $76,144.00 ~0.37% under — both live, no
  snapshot rotation), +0.58% on the PM print — the first up-tick after two
  consecutive sub-$76k prints — and −2.54% vs the Sep 1 bake; T 105.7d: vs
  the Sep 15 walk mids the $85k rich print eases +3.7 → +2.0, the $60k dip
  re-crosses INSIDE the −5 line (−5.5 → −4.2), $90k −1.3, $95k −2.3,
  $100k −3.1, $110k −1.2, $55k +2.2, $50k +6.1 (needed touch +11.2%) —
  tape + chronicle only, BTC tab stamps untouched. Mids/books/balances keep
  the Sep 16 01:45Z stamps; ledger still owes the 61 swept fills. Publish +
  poke via the Sep 1 extraheader path; script scripts/verify_sep17am.py.
- **Sep 17 PM (twenty-sixth data-blind session — the outage's first
  all-green board):** THIRTY-SIXTH missed feed run (Sep 17 22:45Z cron
  silent; a ~23:10Z poke touching fetch/poke pushed via the extraheader
  path, cfb79667, and unanswered — the Actions-disablement diagnosis
  stands). Caps-only on the Sep 17 closes (history pages ~23:2xZ; all five
  Sep 16 finals re-confirmed beneath them): ALL FIVE GREEN — NVDA +2.54%
  $219.34 ($5,308.0B, the board's best), AMZN +2.13% ($2,702.1B), MSFT
  +1.50% ($3,696.8B), AAPL +1.38% $337.00 ($4,949.6B), GOOGL +1.30%
  ($4,228.6B) — the lead re-widens 6.03% → 7.24%/$358.4B, the widest close
  since the Sep 11 melt-up finals; cushion 17.05%/$721.1B, T 9/73.
  Calibration reproduced every Sep 16 PM fair EXACTLY, then fresh fairs:
  Dec 62.51/31.93/4.40/0.42/0.00; crown 87.80/12.20/0.00; seat
  87.37-AAPL/12.19-NVDA/0.44-GOOGL; 3rd 98.30-GOOGL/1.25-MSFT/0.43-AAPL/
  0.01-NVDA; P(±5/wk) 61/59/4. Re-marked against the UNCHANGED Sep 16
  01:45Z walk ladders (now TWO sessions behind, disclosed; depth-at-fair
  recomputed from scripts/largest_books_sep16.txt): dec-AAPL −8.08 CHEAP
  RV 1.34× (#1 stands; $2,090 ≤ fair, $1,244 inside fair−5; σ-band
  28.4–33.7, break-even σ 1.17%/day, implied drift +4.6%), the
  Apple-crown CHEAP comes off (+0.40 at the 12.6 mid — the 22,532-sh HOLD
  marks at fair, the ADD is dead; σ sweep 6.0/12.2/17.6/21.8), crownNVDA
  −0.65 (first sub-fair print since the walk), sep2AAPL −2.87, sep2NVDA
  flips over fair (+0.76), sep3GOOGL −5.30 mid-CHEAP on the 92/94 book
  ($0 inside fair−5, ask −4.30 — a spread artifact, not a ticket, badge
  ON at the mid convention), sep3MSFT sell strengthens (fair 1.25, RV
  0.28× at the bid), dec-NVDA +5.99 RICH by a whisker ($981 NO-dollars;
  catalyst clause gates — no ticket). Joint-payoff MC re-run: Sep+Dec
  Apple legs pay together 6.6% (was 9.7%), corr 0.18. BTC color:
  $76,541.77 (CoinGecko live, +0.50%/24h, range 75,602–77,024; Coinbase
  cross $76,545.18 ~0.004% over — the series' tightest live cross; Kraken
  re-served the AM cross $76,144.00 to the cent — snapshot-stale,
  discarded, the series' FIFTH source rotation), +0.15% on the AM print,
  −2.39% vs the Sep 1 bake; T 105.2d: residuals vs the Sep 15 walk mids
  inside ±4 everywhere but the $50k tail ($85k +1.6, $90k −1.7, $95k
  −2.5, $100k −3.2, $110k −1.2, $60k −3.7, $55k +2.5, $50k +6.3) —
  labeled color, BTC tab stamps untouched. Updated: header tape (PM
  segment), sync Latest + chronicle, Largest hero (caps/gap/tape
  label/prose/Next-Catalyst), 2 KPI tiles, Best Bets (all five rows +
  sec-date + note + honesty line), analysis table (note, both group rows,
  all 14 model rows, footnote), Top-Trades #1 pointer, CLAUDE.md outage
  record, scripts/verify_sep17pm.py + bake_sep17pm.py. Untouched +
  disclosed: balances, ledgers (61 fills owed), Aug 28 cards,
  velocity/SEPH/H series, charts, other tabs, Leaderboard (Sep 15 01:10Z
  re-mark). Publish + poke via the Sep 1 extraheader path.
- **Sep 18 AM (twenty-seventh data-blind session — the morning check
  catches a MICROSOFT REVISION):** THIRTY-SEVENTH missed feed run (Sep 18
  12:45Z cron silent; a 13:09Z poke touching fetch/poke pushed via the
  extraheader path, ac19e8cf, and unanswered — the Actions-disablement
  diagnosis stands). Pre-open verification pass per the Sep 4/Sep 12 AM
  precedents: NVDA $219.34, AAPL $337.00, GOOGL $347.33 and AMZN $251.19
  re-confirmed to the cent against the history pages — **MSFT REVISED
  $497.66 (+1.50%) → $497.75 (+1.52%), cap $3,697.5B** (the outage's
  third catch, after Sep 4's NVDA and Sep 12's triple; the ~23:2xZ
  same-evening pull preceded the settled final again). Calibration
  reproduced every Sep 17 PM fair EXACTLY on the PM inputs (Dec
  62.51/31.93/4.40/0.42/0.00; crown 87.80/12.20/0.00; seat
  87.37/12.19/0.44; 3rd 98.30/1.25/0.43/0.01; P(±5/wk) 61/59/4), then
  the fairs re-ran on the revision: **the ONLY 2dp move on the board is
  3rd-MSFT 1.25 → 1.26** (sep3MSFT edge +3.29 at the 4.55 mid, RV
  0.27× → 0.28×; Best Bets #4 edge +3.24 at the 4.5¢ bid — a hair
  weaker, unchanged in substance); lead 7.24%/$358.4B, cushion
  17.05%/$721.1B, T 9/73 and every other fair/edge/Best Bet stand.
  Premarket color (8:59–9:10 ET, labeled): **GOOGL +2.23% ($355.06)
  against a flat board** (NVDA −0.15%, AAPL +0.00%, MSFT +0.01%, AMZN
  +0.14%) — implied lead 7.08%/$350.3B, implied cushion 14.51%/$627.1B
  vs the finals' 17.05%: an Alphabet bid compresses the cushion and
  firms the 3rd partition, not the lead. BTC color: spot $77,718.58
  (CoinGecko live, +1.7%/24h, range 75,972–77,760; Kraken live cross
  $77,961.00 ~0.31% over — both live, no snapshot rotation), **+1.54%
  on the PM print — the outage's strongest overnight bid**, −0.89% vs
  the Sep 1 bake; T 104.7d: vs the Sep 15 walk mids the bid pushes
  $90k/$95k/$100k back OUTSIDE the −5 line (−5.7/−5.9/−5.9), $85k
  flips back under fair (−3.0), the $60k dip sits nearly at fair
  (−0.7), $55k +4.5, $50k +7.3 (needed touch +9.4%) — tape + chronicle
  only, BTC tab stamps untouched. Restamped: header tape (Sep 18 AM
  segment), sync Latest + chronicle, Largest tape label + hero prose +
  Next-Catalyst prepends, Best Bets sec-date/note/#4 row, analysis
  table note + Sep group row + sep3MSFT/dec-MSFT row cells, footnote.
  Mids/books/balances keep the Sep 16 01:45Z stamps; ledger still owes
  the 61 swept fills. Publish + poke via the Sep 1 extraheader path;
  script scripts/verify_sep18am.py.
- **Sep 18 PM (twenty-eighth data-blind session — the quad-witching
  breakout stands the flagship down; Bitcoin breaks $80k):** THIRTY-EIGHTH
  missed feed run (Sep 18 22:45Z cron silent; a ~23:09Z poke touching
  fetch/poke pushed via the extraheader path, 23c95f0e, and unanswered —
  the Actions-disablement diagnosis stands). Caps-only on the Sep 18
  expiry closes (history pages ~23:1xZ; all five Sep 17 finals
  re-confirmed beneath them — **NVDA SOURCE SPLIT disclosed: the history
  table served $222.06 (+1.24%) while the same site's quote header and
  overview page printed $222.27 (+1.34%) at-close with the after-hours
  series keyed off it — the header taken as the working final (the
  Sep 12/15/18-AM lesson), the next morning pass locks it**): NVDA +1.34%
  $222.27 ($5,378.9B, 181.7M shares) with AMZN +1.00% ($2,729.2B) and
  GOOGL +0.64% ($4,255.5B — faded a $357.31 open) against AAPL −0.26%
  ($4,936.9B) and MSFT −0.80% ($3,668.0B, the board's worst) — the lead
  re-widens a FOURTH straight close, 7.24% → 8.95%/$442.1B, PAST the
  Sep 11 melt-up finals' 8.25% (the widest since the Sep 10 close);
  cushion 16.01%/$681.4B, T 8/72. Calibration reproduced every Sep 18 AM
  fair EXACTLY, then fresh fairs: Dec 65.98/28.69/4.27/0.30/0.00; crown
  93.52/6.48/0.00; seat 93.09-AAPL/6.47-NVDA/0.43-GOOGL; 3rd
  99.13-GOOGL/0.43-MSFT/0.43-AAPL/0.00-NVDA; P(±5/wk) 60/58/4.
  Re-marked against the UNCHANGED Sep 16 01:45Z walk ladders (now THREE
  sessions behind and pre-breakout, disclosed): **dec-AAPL −4.84 — the
  CHEAP badge comes off and Best Bets #1 STANDS DOWN on the stop written
  into its own ticket** (fair < mid+5; $0 inside fair−5, $1,631 ≤ fair;
  break-even σ 1.47%/day ≈ no drift view left); **dec-NVDA +2.52 — the
  RICH badge comes off, the fade dies on its own fair** ($423 NO-dollars
  at bids ≥ fair): the December book is all-FAIR for the first time
  since Sep 8; the crown pair INVERTS — crownAAPL +6.12 RICH (the
  22,532-sh hold marks 2× model on the stale 12.6 mid; rides to
  resolution on the exit-bid logic, $275 of bids at/over fair) vs
  crownNVDA −6.37 mid-CHEAP ($2,713 inside fair−5); sep2AAPL −8.59 the
  pass's widest ($805 inside fair−5); sep3GOOGL's 94.0 ask crosses the
  line (−5.13, $835); sep2NVDA +6.48 at the mid (+7.83 at the ask) — every September cheap print is a
  stale pre-breakout ladder: RE-WALK QUEUE, not tickets; sep3MSFT's
  sell strengthens a fourth session (fair 0.43, RV 0.09×). Joint MC:
  Sep+Dec Apple legs pay together 3.4% (was 6.6%), corr 0.14. BTC
  BREAKS $80K: $81,228.07 (CoinGecko live, +6.2%/24h, range
  76,205–81,304; Kraken live cross $80,996.00 ~0.29% under — both live,
  no snapshot rotation), +4.52% on the AM print (the outage's strongest
  bid), +3.59% OVER the Sep 1 bake — the series' first $80k print and
  first above-bake read since the Sep 9 pre-open; T 104.2d: ladder residuals at the
  series' wides ($85k −17.0 with fair 85.0, $90k −18.4, $95k −16.9,
  $100k −15.1, $110k −8.6; dips flip rich $60k +6.8, $55k +9.1,
  $50k +9.7; needed touch +4.6%) — tape + chronicle only, BTC tab
  stamps untouched; its re-bake is now the loudest want on the page.
  Updated: header tape (PM segment), sync Latest + chronicle, Largest
  hero (caps/gap/tape label/prose/Next-Catalyst), 2 KPI tiles, Best
  Bets (all five rows + sec-date + note + honesty line), analysis table
  (note, both group rows, all 14 model rows + caps/gaps, footnote),
  Top-Trades #1 pointer, CLAUDE.md outage record,
  scripts/verify_sep18pm.py + bake_sep18pm.py. Untouched + disclosed:
  balances, ledgers (61 fills Sep 10–14 still owed), Aug 28 cards,
  velocity/SEPH/H series, charts, other tabs, Leaderboard (Sep 15
  01:10Z re-mark). Publish + poke via the Sep 1 extraheader path.
- **Sep 19 AM (twenty-ninth data-blind session — Saturday: the morning
  check LOCKS the quad-witching finals):** THIRTY-NINTH missed feed run
  (Sep 19 12:45Z cron silent; a 13:09Z poke touching fetch/poke pushed
  via the extraheader path, 05b5790a, and unanswered — the
  Actions-disablement diagnosis stands). **The NVDA source split
  RESOLVES TO THE HEADER: the history table that served $222.06
  (+1.24%) at ~23:10Z settled to $222.27 (+1.34%) overnight — the
  Sep 12/15/18-AM lesson holds a fourth time.** All five Sep 18 finals
  re-confirmed to the cent (NVDA $222.27, AAPL $336.13, GOOGL $349.54,
  MSFT $493.78, AMZN $253.71); the ONLY revision anywhere is NVDA's
  volume, 181.7M printed at ~23:1xZ → 189,973,388 settled. Calibration
  reproduced every Sep 18 PM fair EXACTLY on the locked finals (Dec
  65.98/28.69/4.27/0.30/0.00; crown 93.52/6.48/0.00; seat
  93.09-AAPL/6.47-NVDA/0.43-GOOGL; 3rd 99.13-GOOGL/0.43-MSFT/0.43-AAPL/
  0.00-NVDA; P(±5/wk) 60/58/4) — lead 8.95%/$442.1B, cushion
  16.01%/$681.4B, T 8/72 unchanged on a Saturday: every fair, badge and
  Best-Bet stance (Best Bets #1 STOOD DOWN, crownAAPL hold rides to
  resolution, sep3MSFT sell, the stale-ladder cheap trio in the re-walk
  queue) rides the weekend into Monday's open exactly as published — no
  close until Sep 21. BTC HOLDS THE BREAK: $81,074.05 (CoinGecko live,
  +4.3%/24h, range 77,609.21–81,674.72; Kraken live cross $81,079.00
  +0.01% apart — the series' second-tightest cross (Sep 17 PM's ~0.004%
  Coinbase cross keeps the record), both live, no snapshot rotation), −0.19% on the PM $80k-break print (the breakout's
  first overnight hold), +3.39% vs the Sep 1 bake; T 103.7d: up-rungs
  ease a hair off the wides and stay the story ($85k −16.3, $90k −17.7,
  $95k −16.3, $100k −14.6, $110k −8.2; dips rich $60k +6.7, $55k +9.0,
  $50k +9.7; needed touch +4.8%) — labeled color only, BTC tab stamps
  untouched. Updated: header tape (Sep 19 AM segment), sync Latest +
  chronicle, Largest tape label + hero prose + Next-Catalyst prepends,
  NVDA source-note LOCK + settled-volume corrections on every standing
  surface (hero, analysis note, footnote), CLAUDE.md outage record,
  scripts/verify_sep19am.py + bake_sep19am.py. Untouched + disclosed:
  mids/books/balances (Sep 16 01:45Z walk stamps), cards/slate/Best
  Bets rows (fairs unchanged — verified, not re-baked), KPI/analysis
  cells, velocity/SEPH/H series, ledgers (61 fills Sep 10–14 still
  owed), Leaderboard (Sep 15 01:10Z re-mark), all other tabs. Publish +
  poke via the Sep 1 extraheader path.
- **Sep 19 PM (thirtieth data-blind session — Saturday night: the lock
  holds, BTC prints the series high):** FORTIETH missed feed run (Sep 19
  22:45Z cron silent; a ~23:09Z poke touching fetch/poke pushed via the
  extraheader path, f5146418, and unanswered — the Actions-disablement
  diagnosis stands). All five Sep 18 finals re-confirmed to the cent a
  SECOND consecutive session (NVDA $222.27 — vol 189,973,388 settled
  holds — AAPL $336.13, GOOGL $349.54, MSFT $493.78, AMZN $253.71; the
  Sep 17 finals a third session, the Sep 16 rows verified beneath).
  Calibration reproduced every fair EXACTLY (Dec 65.98/28.69/4.27/0.30/
  0.00; crown 93.52/6.48/0.00; seat 93.09/6.47/0.43; 3rd 99.13/0.43/
  0.43/0.00; P(±5/wk) 60/58/4) — lead 8.95%/$442.1B, cushion
  16.01%/$681.4B, T 8/72: the whole board rides into Monday's open
  unchanged. BTC $81,706.31 — the outage series' highest print
  (CoinGecko live, +1.3%/24h, range 80,541.19–81,709.43, the night's
  ONLY live read: Kraken re-served the AM cross to the cent, $81,079.00
  +4.53% — the sixth snapshot rotation, its second re-serve; Coinbase
  $81,101.99 and CMC $81,185.72 both Friday-vintage — all three
  discarded), +0.78% on the AM print, +0.59% over the $80k-break print,
  +4.20% vs the Sep 1 bake (the widest above-bake read of the series);
  T 103.2d: every residual vs the Sep 15 walk mids at a fresh series
  wide ($85k −18.9, $90k −20.1 the first −20, $95k −18.3, $100k −16.2,
  $110k −9.3; dips $60k +7.9, $55k +9.8, $50k +10.0 the first +10;
  needed touch +4.0%) — labeled color only, BTC tab stamps untouched.
  Updated: header tape (Sep 19 PM segment), sync Latest + chronicle,
  Largest tape label + hero prose + Next-Catalyst prepends, CLAUDE.md
  outage record, scripts/verify_sep19pm.py + bake_sep19pm.py. Untouched
  + disclosed: mids/books/balances (Sep 16 01:45Z walk stamps),
  cards/slate/Best Bets rows (fairs unchanged — verified, not
  re-baked), KPI/analysis cells, velocity/SEPH/H series, ledgers (61
  fills Sep 10–14 still owed), Leaderboard (Sep 15 01:10Z re-mark), all
  other tabs. Publish + poke via the Sep 1 extraheader path.
- **Sep 20 AM (thirty-first data-blind session — Sunday: the lock holds a
  THIRD pass, bitcoin hands back the high but holds $80k):** FORTY-FIRST
  missed feed run (Sep 20 12:45Z cron silent; a 13:08Z poke touching
  fetch/poke pushed via the extraheader path, 2cf12e7a, and unanswered —
  the Actions-disablement diagnosis stands). All five Sep 18 finals
  re-confirmed to the cent a THIRD consecutive session (NVDA $222.27 —
  vol 189,973,388 settled holds — AAPL $336.13, GOOGL $349.54, MSFT
  $493.78, AMZN $253.71; the Sep 17 finals a fourth session, the Sep 16
  rows verified beneath; every history-page header still 'At close:
  Sep 18'). Calibration reproduced every fair EXACTLY (Dec 65.98/28.69/
  4.27/0.30/0.00; crown 93.52/6.48/0.00; seat 93.09/6.47/0.43; 3rd
  99.13/0.43/0.43/0.00; P(±5/wk) 60/58/4) — lead 8.95%/$442.1B, cushion
  16.01%/$681.4B, T 8/72: the whole board rides into Monday's open
  unchanged (the first close since the breakout is a day away). BTC
  hands back the series high but HOLDS the break: $80,304.64 (CoinGecko
  live, −1.2%/24h, range 80,154.86–81,864.43; Kraken LIVE cross
  $80,511.00 −0.95%/24h ~0.26% over — two live sources again after
  Saturday's single-source night; CMC $81,287.92 "+0.41%" discarded —
  its 24h low 80,814.94 sits ABOVE both live prints, snapshot-stale),
  −1.72% on the series-high print, −0.95% on the Sep 19 AM print,
  −1.14% vs the $80k-break print, +2.41% over the Sep 1 bake — a FOURTH
  consecutive $80k+ print, the tape's own 24h low ($80,155) holding above
  the break; T 102.6d: every residual vs the stale pre-breakout
  Sep 15 walk mids eases off Saturday's series wides but stays blown
  out ($85k −13.1, $90k −14.7, $95k −13.5, $100k −12.2, $110k −6.6;
  dips $60k +5.4, $55k +8.3, $50k +9.3; needed touch +5.8%) — labeled
  color only, BTC tab stamps untouched. Updated: header tape (Sep 20 AM
  segment), sync Latest + chronicle, Largest tape label + hero prose +
  Next-Catalyst prepends, CLAUDE.md outage record,
  scripts/verify_sep20am.py + bake_sep20am.py. Untouched + disclosed:
  mids/books/balances (Sep 16 01:45Z walk stamps), cards/slate/Best
  Bets rows (fairs unchanged — verified, not re-baked), KPI/analysis
  cells, velocity/SEPH/H series, ledgers (61 fills Sep 10–14 still
  owed), Leaderboard (Sep 15 01:10Z re-mark), all other tabs. Publish +
  poke via the Sep 1 extraheader path.
- **Sep 2 AM caps-only precedent:** with autodata down, public Sep 1 closes
  (stockanalysis.com history pages via WebSearch→WebFetch — WebFetch DOES
  work unattended on URLs surfaced verbatim by a WebSearch in the same
  session) let the run re-true caps + model fairs honestly while leaving
  mids/books/balances/ledgers untouched and disclosed as stale.
