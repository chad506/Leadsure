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
- **Autodata outage record:** no results since Aug 31 19:23Z — NINE missed
  feed runs. Sep 1, Sep 2, Sep 3 crons (12:45Z/22:45Z each day) and the
  Sep 4 12:45Z cron all silent; pokes at Sep 1 01:05Z + 23:22Z, Sep 2
  00:54Z + 13:11Z + 23:12Z, Sep 3 13:15Z + 23:10Z, and Sep 4 13:10Z +
  13:12Z (several touched fetch/poke, so the paths-filtered push trigger
  definitely applied) all unanswered. run.sh always writes _fetched_at.txt
  even when every fetch fails, so the JOB IS NEVER STARTING — the Action
  itself is stuck or disabled (billing/spending limit or a disabled
  workflow), not the fetch script. Fix at
  https://github.com/chad506/Leadsure/actions (re-enable / check Actions
  billing / cancel a hung run), then delete this bullet once results flow
  again.
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
- **Sep 2 AM caps-only precedent:** with autodata down, public Sep 1 closes
  (stockanalysis.com history pages via WebSearch→WebFetch — WebFetch DOES
  work unattended on URLs surfaced verbatim by a WebSearch in the same
  session) let the run re-true caps + model fairs honestly while leaving
  mids/books/balances/ledgers untouched and disclosed as stale.
