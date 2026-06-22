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
- DNS: Cloudflare (nameservers), A records point to GitHub Pages IPs
- HTTPS cert: GitHub Pages Let's Encrypt (may need enabling via API after DNS changes)
- Enable HTTPS: `curl -X PUT -H "Authorization: token TOKEN" https://api.github.com/repos/chad506/Leadsure/pages -d '{"https_enforced":true}'`

---

## model-picks-data.js — The 5 Models

| id | name | icon | debut | trades (as of 6/17) |
|----|------|------|-------|---------------------|
| `gpt54` | GPT 5.4 | 🧠 | Week 1 (3/6) | 111 |
| `opus46` | Claude Opus 4.6 | 🎯 | Week 1 (3/6) | 111 |
| `wildcard` | Gemini 3.1 Pro | 🔮 | Week 1 (3/6) | 111 |
| `opus47` | Claude Opus 4.7 | 🌟 | Week 23 (4/28) | 70 |
| `fable5` | Fable 5 | 🪄 | Week 35 (6/12) | 15 |
| `opus48` | Claude Opus 4.8 | 💎 | Week 38 (6/22) | 5 |

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
