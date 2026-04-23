/* ============================================
   APP.JS — Portfolio Dashboard Logic (LIVE)
   ============================================ */

// ---- CONFIGURATION ----
// Get your free API key at https://finnhub.io — 60 calls/min on free tier
// Calls Finnhub directly from browser (no proxy needed — they support CORS)
// FINNHUB_API_KEY is now in fund-data.js as SHARED_FINNHUB_KEY
const FINNHUB_API_KEY = typeof SHARED_FINNHUB_KEY !== 'undefined' ? SHARED_FINNHUB_KEY : 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';
const REFRESH_INTERVAL = 120000; // 2 minutes (51 symbols @ 1.1s = ~56s per cycle)

// ---- FUND CONSTANTS ----
const CASH = 140000.00; // From Google Sheet cell B2
const SPY_INCEPTION_PRICE = 680.28; // SPY close on Mar 3, 2026 (day before fund inception Mar 4)
let spyCurrentPrice = 704.08; // Updated live via Finnhub
const MAGS_INCEPTION_PRICE = 61.29; // MAGS (Mag 7 ETF) close on Mar 3, 2026
let magsCurrentPrice = 65.31; // Updated live via Finnhub

// REALIZED_PNL is now in fund-data.js as SHARED_REALIZED_PNL
const REALIZED_PNL = typeof SHARED_REALIZED_PNL !== 'undefined' ? SHARED_REALIZED_PNL : -1638.37;

// ---- POSITION DATA ----
// POSITIONS array is now in fund-data.js (loaded before app3.js)

// ---- DAILY PICKS (Generated Mon Mar 30, 2026) ----
// 15 total picks: 5 per model (3 longs + 2 shorts each)
const DAILY_PICKS = [
  {"symbol": "GOOG", "name": "Alphabet Inc", "direction": "Long", "qty": 18, "price": 293.9, "rationale": "Alphabet\'s Gemini AI models, TPU infrastructure, and Google Cloud AI services position it as one of the three dominant AI platform companies; DeepMind breakthroughs and AI-powered Search Overviews drive both revenue growth and competitive moat expansion."},
  {"symbol": "GE", "name": "GE Aerospace", "direction": "Long", "qty": 18, "price": 295.19, "rationale": "GE Aerospace\'s jet engine fleet generates decades of high-margin aftermarket revenue; AI-powered predictive maintenance and digital twin technology optimize engine performance, creating a durable moat in the aviation infrastructure buildout."},
  {"symbol": "HPE", "name": "Hewlett Packard Enterprise", "direction": "Long", "qty": 209, "price": 24.25, "rationale": "HPE\'s GreenLake hybrid cloud platform and ProLiant AI servers are capturing enterprise AI infrastructure demand; Juniper Networks acquisition expands its AI networking capabilities to deliver end-to-end AI compute solutions."},
  {"symbol": "INFY", "name": "Infosys Ltd", "direction": "Short", "qty": 390, "price": 13.38, "rationale": "Infosys\'s IT outsourcing and consulting business faces structural disruption as AI coding agents and autonomous software development tools replace the billable developer hours that drive its revenue."},
  {"symbol": "PAYX", "name": "Paychex Inc", "direction": "Short", "qty": 55, "price": 91.54, "rationale": "Paychex\'s payroll processing and HR services face automation pressure as AI agents handle tax calculations, benefits administration, and compliance filings autonomously."},
  {"symbol": "META", "name": "Meta Platforms Inc", "direction": "Long", "qty": 10, "price": 578.91, "rationale": "Meta\'s Llama open-source AI models, massive GPU infrastructure, and AI-powered advertising optimization create a flywheel where better AI drives higher ad revenue which funds more compute."},
  {"symbol": "AES", "name": "The AES Corp", "direction": "Long", "qty": 357, "price": 14.16, "rationale": "AES Corporation\'s renewable energy portfolio and battery storage capabilities position it to supply clean power for AI data centers; its partnership with Google for 24/7 carbon-free energy directly serves hyperscaler sustainability mandates."},
  {"symbol": "TEL", "name": "TE Connectivity Ltd", "direction": "Long", "qty": 25, "price": 213.09, "rationale": "TE Connectivity\'s high-speed connectors and sensors are essential building blocks for AI data centers; its power and signal connectivity solutions enable the dense GPU rack architectures."},
  {"symbol": "NSIT", "name": "Insight Enterprises Inc", "direction": "Short", "qty": 76, "price": 68.05, "rationale": "Insight Enterprises\' IT product distribution and solutions business faces margin compression as AI-powered procurement platforms automate vendor selection, pricing negotiation, and technology stack optimization."},
  {"symbol": "GRMN", "name": "Garmin Ltd", "direction": "Short", "qty": 22, "price": 235.92, "rationale": "Garmin\'s GPS navigation and fitness wearable business faces disruption as AI-powered smartphone assistants replicate navigation, health tracking, and fitness coaching capabilities."},
  {"symbol": "CARR", "name": "Carrier Global Corp", "direction": "Long", "qty": 92, "price": 57.46, "rationale": "Carrier\'s HVAC and refrigeration systems are critical for AI data center cooling; its Abound smart building platform integrates AI-driven climate control for high-density compute facilities."},
  {"symbol": "AR", "name": "Antero Resources Corp", "direction": "Long", "qty": 111, "price": 41.38, "rationale": "Antero Resources is a top-five US natural gas producer with premium Appalachian Basin acreage; as AI data center power demand drives a structural increase in gas-fired generation, Antero benefits from rising natural gas prices."},
  {"symbol": "VNET", "name": "VNET Group Inc", "direction": "Long", "qty": 592, "price": 8.61, "rationale": "VNET Group operates carrier-neutral data centers across China and is expanding AI-optimized facilities to meet surging demand from Chinese hyperscalers deploying large language models."},
  {"symbol": "DV", "name": "DoubleVerify Holdings Inc", "direction": "Short", "qty": 537, "price": 9.79, "rationale": "DoubleVerify\'s ad verification and brand safety platform faces disruption as AI-native advertising systems embed fraud detection and viewability measurement directly into programmatic buying."},
  {"symbol": "LUMN", "name": "Lumen Technologies Inc", "direction": "Short", "qty": 750, "price": 7.0, "rationale": "Lumen\'s legacy telecom and fiber network business faces margin pressure despite AI data center interconnect demand; heavy debt load and declining enterprise revenue constrain its ability to capitalize on the AI infrastructure buildout."}
];

// ---- FORMATTERS ----
const fmtCurrency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

const fmtCurrencyCompact = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 0,
  maximumFractionDigits: 0
});

const fmtNumber = new Intl.NumberFormat('en-US', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

const fmtPct = new Intl.NumberFormat('en-US', {
  style: 'percent',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
  signDisplay: 'always'
});

const fmtInt = new Intl.NumberFormat('en-US');
const fmtMarketCap = (val) => {
  if (!val || val === 0) return '\u2014';
  if (val >= 1e12) return '$' + (val / 1e12).toFixed(1) + 'T';
  if (val >= 1e9) return '$' + (val / 1e9).toFixed(1) + 'B';
  if (val >= 1e6) return '$' + (val / 1e6).toFixed(0) + 'M';
  return '$' + val.toFixed(0);
};

// ---- AUTO-RESET: Fix Today's P&L on new trading days ----
// Embedded prices: price = last close, prevClose = close before that.
// On a new day: yesterday's close (embedded price) becomes today's prevClose.
// Today's P&L starts at $0 until Finnhub provides live intraday prices.
(function autoResetForNewDay() {
  if (typeof PRICES_AS_OF === 'undefined') return;
  const now = new Date();
  const todayPacific = now.toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
  if (todayPacific !== PRICES_AS_OF) {
    // New day: embedded 'price' is yesterday's close — use it as today's prevClose.
    // Set price = prevClose so Today's P&L starts at $0 until Finnhub runs.
    console.log('[Dashboard] New day detected (' + todayPacific + ' vs embedded ' + PRICES_AS_OF + ') — resetting for new trading day');
    POSITIONS.forEach(pos => {
      // Yesterday's close (embedded price) becomes today's previous close
      pos.prevClose = pos.price;
      // Price starts at prevClose (Today P&L = $0 until Finnhub updates)
      // Finnhub will provide both live price (c) and correct prevClose (pc)
    });
    // Also reset benchmark for S&P 500 / MAGS
    // (their embedded values are already yesterday's close, no action needed)
  }
})();

// ---- RESTORE ALL CACHED PRICES FROM LOCALSTORAGE ----
// On page load, immediately apply cached prices so KPIs/Today's P&L show
// realistic values before the ~60s Finnhub fetch completes.
(function restoreCachedPrices() {
  try {
    const cached = localStorage.getItem('finnhub_prices');
    const ts = parseInt(localStorage.getItem('finnhub_prices_ts') || '0');
    if (!cached) return;
    const ageMs = Date.now() - ts;
    // Only use if less than 18 hours old (covers overnight + pre-market)
    if (ageMs > 18 * 60 * 60 * 1000) return;

    const priceMap = JSON.parse(cached);
    const cacheDate = new Date(ts).toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
    const todayPacific = new Date().toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
    const isSameDay = cacheDate === todayPacific;

    // Restore benchmarks (always safe — these are current prices)
    if (priceMap.SPY && priceMap.SPY.c > 0) spyCurrentPrice = priceMap.SPY.c;
    if (priceMap.MAGS && priceMap.MAGS.c > 0) magsCurrentPrice = priceMap.MAGS.c;

    let restored = 0;
    POSITIONS.forEach(pos => {
      const c = priceMap[pos.symbol];
      if (c && c.c > 0) {
        if (isSameDay) {
          // Same-day cache: restore both price and prevClose
          pos.price = c.c;
          if (c.pc > 0) pos.prevClose = c.pc;
        } else {
          // Next-day cache: cached price IS yesterday's close.
          // Use it as today's prevClose (more accurate than embedded).
          // Don't update pos.price (it was already set = prevClose by autoReset).
          if (c.pc > 0) {
            // Cache's prevClose is 2 days ago — skip it.
            // But cache's current price is yesterday's close = today's prevClose.
            pos.prevClose = c.c;
          }
        }
        restored++;
      }
    });
    if (restored > 0) {
      console.log('[Dashboard] Restored ' + restored + ' prices from localStorage (' + (isSameDay ? 'same-day' : 'next-day') + ', age: ' + Math.round(ageMs/1000) + 's)');
    }
  } catch (e) { /* ignore */ }
})();

// ---- LIVE PRICE FETCHING (Direct Finnhub API — no proxy needed) ----
let isFirstLoad = true;
let refreshTimer = null;
let isFetching = false; // Guard against overlapping fetches

// Shared helper: fetch a single Finnhub quote
const fetchOneQuote = async (sym) => {
  try {
    const res = await fetch(
      `https://finnhub.io/api/v1/quote?symbol=${sym}&token=${FINNHUB_API_KEY}`
    );
    if (!res.ok) return null;
    const data = await res.json();
    if (data.c === 0 && data.h === 0 && data.l === 0) return null;
    return { symbol: sym, price: data.c, prevClose: data.pc };
  } catch {
    return null;
  }
};

// Global rate limiter — ensures we never exceed Finnhub's 60 calls/min
// Tracks call timestamps and enforces minimum spacing
const rateLimiter = {
  callTimes: [],
  MAX_PER_MIN: 55, // Stay under 60 with headroom
  MIN_SPACING_MS: 1100, // At least 1.1s between calls
  async waitForSlot() {
    const now = Date.now();
    // Remove calls older than 60s
    this.callTimes = this.callTimes.filter(t => now - t < 60000);
    // If at limit, wait until oldest call expires
    if (this.callTimes.length >= this.MAX_PER_MIN) {
      const waitMs = 60000 - (now - this.callTimes[0]) + 100;
      await new Promise(r => setTimeout(r, waitMs));
    }
    // Enforce minimum spacing from last call
    if (this.callTimes.length > 0) {
      const sinceLast = Date.now() - this.callTimes[this.callTimes.length - 1];
      if (sinceLast < this.MIN_SPACING_MS) {
        await new Promise(r => setTimeout(r, this.MIN_SPACING_MS - sinceLast));
      }
    }
    this.callTimes.push(Date.now());
  }
};

// Shared helper: fetch symbols one at a time with global rate limiting
async function fetchSymbolBatches(symbols) {
  const priceMap = {};
  for (let i = 0; i < symbols.length; i++) {
    await rateLimiter.waitForSlot();
    const r = await fetchOneQuote(symbols[i]);
    if (r && r.price > 0) priceMap[r.symbol] = r;
  }
  return priceMap;
}

// Global price map shared between position fetch and model pick fetch
let globalPriceMap = {};

// Broadcast all prices to localStorage for other pages (fund-results, picks-history)
function broadcastPricesToLocalStorage() {
  try {
    const priceCache = {};
    Object.entries(globalPriceMap).forEach(([sym, r]) => {
      priceCache[sym] = { c: r.price, pc: r.prevClose };
    });
    localStorage.setItem('finnhub_prices', JSON.stringify(priceCache));
    localStorage.setItem('finnhub_prices_ts', Date.now().toString());
  } catch (e) { /* localStorage unavailable */ }
}

async function fetchLivePrices() {
  if (isFetching) {
    console.log('[Dashboard] Skipping refresh — previous fetch still running');
    return;
  }
  if (!FINNHUB_API_KEY) {
    // No API key — just render with embedded prices
    if (isFirstLoad) {
      const now = new Date();
      const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
      document.getElementById('last-updated').textContent = `Static prices · ${timeStr}`;
      isFirstLoad = false;
      console.log('[Dashboard] No Finnhub API key set — using embedded prices. Get a free key at https://finnhub.io');
    }
    return;
  }

  const statusEl = document.getElementById('last-updated');
  const btnEl = document.getElementById('btn-refresh');

  isFetching = true;
  try {
    btnEl.classList.add('refreshing');
    statusEl.textContent = 'Refreshing...';

    // Phase 1a: Fetch benchmarks FIRST (SPY + MAGS) — critical for KPIs
    const benchmarks = await fetchSymbolBatches(['SPY', 'MAGS']);
    Object.assign(globalPriceMap, benchmarks);
    if (benchmarks.SPY) spyCurrentPrice = benchmarks.SPY.price;
    if (benchmarks.MAGS) magsCurrentPrice = benchmarks.MAGS.price;

    // Quick render with benchmarks updated (positions still have cached/embedded prices)
    computedPositions = computePositions(POSITIONS);
    renderAll(computedPositions);

    // Phase 1b: Fetch fund positions one at a time with rate limiting
    const positionSymbols = POSITIONS.map(p => p.symbol);
    const uniquePositions = [...new Set(positionSymbols)].filter(s => s !== 'SPY' && s !== 'MAGS');
    const livePriceMap = await fetchSymbolBatches(uniquePositions);

    // Merge into global map
    Object.assign(globalPriceMap, livePriceMap);

    // Merge live prices into positions
    POSITIONS.forEach(pos => {
      const r = livePriceMap[pos.symbol];
      if (r) {
        const oldPrice = pos.price;
        pos.price = r.price;
        if (r.prevClose > 0) {
          pos.prevClose = r.prevClose;
        }
        pos.priceDirection = (r.price > oldPrice) ? 'up'
          : (r.price < oldPrice) ? 'down' : 'flat';
      }
    });

    // Broadcast ALL prices (benchmarks + positions) to other tabs via localStorage
    broadcastPricesToLocalStorage();

    // Recompute and re-render with live position prices
    computedPositions = computePositions(POSITIONS);
    renderAll(computedPositions);
    renderLeaderboardFromPrices(globalPriceMap);

    // Update timestamp
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    statusEl.textContent = `Live · ${timeStr}`;
    statusEl.classList.remove('status-error');
    statusEl.classList.add('status-live');

    if (isFirstLoad) {
      isFirstLoad = false;
      console.log('[Dashboard] Live prices loaded from Finnhub');
      // Phase 2: On first load, also fetch model pick symbols in background
      // This updates the leaderboard with fresh livePrice/prevClose
      // so Today's P&L and Total P&L stay accurate without manual deploys
      fetchModelPickPrices();
    }
  } catch (err) {
    console.error('[Dashboard] Price fetch failed:', err);
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

    if (isFirstLoad) {
      statusEl.textContent = `As of market close`;
      isFirstLoad = false;
    } else {
      statusEl.textContent = `Offline · ${timeStr}`;
    }
    statusEl.classList.add('status-error');
    statusEl.classList.remove('status-live');
  } finally {
    btnEl.classList.remove('refreshing');
    isFetching = false;
  }
}

// Phase 2: Background fetch for all model pick symbols
// Runs once on first load, takes ~45s due to rate limiting
// Updates MODEL_PICKS livePrice/prevClose so leaderboard P&L stays fresh
let modelPicksFetched = false;
async function fetchModelPickPrices() {
  if (modelPicksFetched || !FINNHUB_API_KEY || typeof MODEL_PICKS === 'undefined') return;
  modelPicksFetched = true;

  try {
    // Collect all unique pick symbols not already in the global map
    const pickSymbols = new Set();
    MODEL_PICKS.models.forEach(m => {
      m.picks.forEach(p => {
        if (!globalPriceMap[p.symbol]) pickSymbols.add(p.symbol);
      });
    });
    // Also include DAILY_PICKS symbols
    if (typeof DAILY_PICKS !== 'undefined') {
      DAILY_PICKS.forEach(p => {
        if (!globalPriceMap[p.symbol]) pickSymbols.add(p.symbol);
      });
    }

    const remaining = [...pickSymbols];
    if (remaining.length === 0) return;

    console.log(`[Dashboard] Fetching ${remaining.length} model pick symbols in background...`);

    // Fetch remaining pick symbols with global rate limiting (rate limiter handles pacing)
    const pickPriceMap = await fetchSymbolBatches(remaining);
    Object.assign(globalPriceMap, pickPriceMap);

    console.log(`[Dashboard] Got prices for ${Object.keys(pickPriceMap).length}/${remaining.length} pick symbols`);

    // Update MODEL_PICKS with live data
    MODEL_PICKS.models.forEach(m => {
      m.picks.forEach(p => {
        const live = globalPriceMap[p.symbol];
        if (live) {
          p.livePrice = live.price;
          p.prevClose = live.prevClose;
        }
      });
    });

    // Update DAILY_PICKS too
    if (typeof DAILY_PICKS !== 'undefined') {
      DAILY_PICKS.forEach(p => {
        const live = globalPriceMap[p.symbol];
        if (live) {
          p.price = live.price;
        }
      });
      // Re-render model picks cards with fresh prices
      renderModelPicks();
    }

    // Re-render leaderboard with complete price data
    renderLeaderboardFromPrices(globalPriceMap);

    // Update localStorage with all prices (positions + picks)
    broadcastPricesToLocalStorage();

    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const statusEl = document.getElementById('last-updated');
    if (statusEl) statusEl.textContent = `Live · ${timeStr}`;

  } catch (err) {
    console.error('[Dashboard] Model pick price fetch failed:', err);
  }
}

function startAutoRefresh() {
  fetchLivePrices();
  refreshTimer = setInterval(fetchLivePrices, REFRESH_INTERVAL);
}

function stopAutoRefresh() {
  if (refreshTimer) {
    clearInterval(refreshTimer);
    refreshTimer = null;
  }
}

// Pause auto-refresh when tab is hidden
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    stopAutoRefresh();
  } else {
    fetchLivePrices();
    refreshTimer = setInterval(fetchLivePrices, REFRESH_INTERVAL);
  }
});

// ---- COMPUTE DERIVED VALUES ----
function computePositions(positions) {
  return positions.map(p => {
    const isLong = p.direction === 'Long';
    const price = p.price;
    const prevClose = p.prevClose || p.costBasis;

    // Market value: always positive (absolute exposure)
    const marketValue = p.qty * price;

    // Cost total
    const costTotal = p.qty * p.costBasis;

    // P&L: for longs, profit when price > cost; for shorts, profit when price < cost
    const gainLoss = isLong
      ? (price - p.costBasis) * p.qty
      : (p.costBasis - price) * p.qty;

    const gainLossPct = p.costBasis !== 0
      ? (isLong
        ? (price - p.costBasis) / p.costBasis
        : (p.costBasis - price) / p.costBasis)
      : 0;

    // Day change: % move from previous close
    // For shorts, a price increase is bad (negative day change from portfolio perspective)
    const dayChangePct = prevClose !== 0
      ? (price - prevClose) / prevClose
      : 0;

    // Portfolio-adjusted day change: flip sign for shorts
    const portfolioDayChange = isLong ? dayChangePct : -dayChangePct;

    // Day P&L in dollars (portfolio perspective)
    const dayPnLDollar = isLong
      ? (price - prevClose) * p.qty
      : (prevClose - price) * p.qty;

    return {
      ...p,
      price,
      marketValue,
      costTotal,
      gainLoss,
      gainLossPct,
      dayChangePct,        // raw price change %
      portfolioDayChange,  // portfolio-perspective change %
      dayPnLDollar,        // dollar day P&L (portfolio perspective)
      priceDirection: p.priceDirection || 'flat'
    };
  });
}

// ---- RENDER ALL ----
function renderAll(positions) {
  renderKPIs(positions);
  renderTable(positions);
  renderChart(positions);
  renderTopMovers(positions);
  renderSectorMovers(positions);
  renderTodaySectorMovers(positions);
  renderTodayTopMovers(positions);
}

// ---- RENDER KPI CARDS ----
function renderKPIs(positions) {
  const longs = positions.filter(p => p.direction === 'Long');
  const shorts = positions.filter(p => p.direction === 'Short');

  const longExposure = longs.reduce((sum, p) => sum + p.marketValue, 0);
  const shortExposure = shorts.reduce((sum, p) => sum + p.marketValue, 0);
  const grossExposure = longExposure + shortExposure;
  const netExposure = longExposure - shortExposure;
  const unrealizedPnL = positions.reduce((sum, p) => sum + p.gainLoss, 0);
  const totalPnL = unrealizedPnL + REALIZED_PNL; // Include closed positions

  // Sharpe & Sortino — cross-sectional (position P&L% as return distribution)
  const returns = positions.map(p => p.gainLossPct);
  const avgReturn = returns.reduce((s, r) => s + r, 0) / returns.length;
  const variance = returns.reduce((s, r) => s + Math.pow(r - avgReturn, 2), 0) / returns.length;
  const stdDev = Math.sqrt(variance);
  const sharpeRatio = stdDev !== 0 ? avgReturn / stdDev : 0;

  // Sortino: penalizes only downside volatility (losing positions)
  const losingReturns = returns.filter(r => r < 0);
  const downsideVariance = losingReturns.reduce((s, r) => s + r * r, 0) / returns.length;
  const sortinoRatio = downsideVariance > 0 ? avgReturn / Math.sqrt(downsideVariance) : 0;

  const grossEl = document.getElementById('kpi-total-value');
  if (grossEl) grossEl.textContent = fmtCurrencyCompact.format(grossExposure);
  document.getElementById('kpi-long-exposure').textContent = fmtCurrencyCompact.format(longExposure);
  document.getElementById('kpi-short-exposure').textContent = '-' + fmtCurrencyCompact.format(shortExposure);

  // Cash
  document.getElementById('kpi-cash').textContent = fmtCurrencyCompact.format(CASH);

  // ROI = Total P&L / Cash
  const roi = CASH !== 0 ? totalPnL / CASH : 0;
  const roiEl = document.getElementById('kpi-roi');
  // Annualized ROI: (1 + roi)^(365/days) - 1
  const inceptionDate = new Date('2026-03-04T00:00:00');
  const now = new Date();
  const daysElapsed = Math.max((now - inceptionDate) / (1000 * 60 * 60 * 24), 1);
  const roiAnnualized = Math.pow(1 + roi, 365 / daysElapsed) - 1;
  const roiAnnSign = roiAnnualized >= 0 ? '+' : '';
  roiEl.textContent = (roi >= 0 ? '+' : '') + (roi * 100).toFixed(2) + '%' + ' (' + roiAnnSign + (roiAnnualized * 100).toFixed(0) + '% yr)';
  roiEl.classList.toggle('kpi-gain', roi >= 0);
  roiEl.classList.toggle('kpi-loss', roi < 0);

  // S&P 500 % since inception
  const spyChange = SPY_INCEPTION_PRICE !== 0 ? (spyCurrentPrice - SPY_INCEPTION_PRICE) / SPY_INCEPTION_PRICE : 0;
  const spyEl = document.getElementById('kpi-spy');
  const spyAnnualized = Math.pow(1 + spyChange, 365 / daysElapsed) - 1;
  const spyAnnSign = spyAnnualized >= 0 ? '+' : '';
  spyEl.textContent = (spyChange >= 0 ? '+' : '') + (spyChange * 100).toFixed(2) + '%' + ' (' + spyAnnSign + (spyAnnualized * 100).toFixed(0) + '% yr)';
  spyEl.classList.toggle('kpi-gain', spyChange >= 0);
  spyEl.classList.toggle('kpi-loss', spyChange < 0);

  // Mag 7 % since inception (using MAGS ETF as proxy)
  const magsChange = MAGS_INCEPTION_PRICE !== 0 ? (magsCurrentPrice - MAGS_INCEPTION_PRICE) / MAGS_INCEPTION_PRICE : 0;
  const magsEl = document.getElementById('kpi-mag7');
  if (magsEl) {
    const magsAnnualized = Math.pow(1 + magsChange, 365 / daysElapsed) - 1;
    const magsAnnSign = magsAnnualized >= 0 ? '+' : '';
    magsEl.textContent = (magsChange >= 0 ? '+' : '') + (magsChange * 100).toFixed(2) + '%' + ' (' + magsAnnSign + (magsAnnualized * 100).toFixed(0) + '% yr)';
    magsEl.classList.toggle('kpi-gain', magsChange >= 0);
    magsEl.classList.toggle('kpi-loss', magsChange < 0);
  }

  const pnlEl = document.getElementById('kpi-total-pnl');
  pnlEl.textContent = (totalPnL >= 0 ? '+' : '') + fmtCurrency.format(totalPnL);
  pnlEl.classList.toggle('kpi-gain', totalPnL >= 0);
  pnlEl.classList.toggle('kpi-loss', totalPnL < 0);

  document.getElementById('kpi-positions').textContent = `${longs.length}L / ${shorts.length}S`;

  // Today's P&L (sum of portfolio-perspective day $ changes)
  const todayPnL = positions.reduce((sum, p) => sum + p.dayPnLDollar, 0);
  const todayPnLEl = document.getElementById('kpi-today-pnl');
  if (todayPnLEl) {
    todayPnLEl.textContent = (todayPnL >= 0 ? '+' : '') + fmtCurrency.format(todayPnL);
    todayPnLEl.classList.toggle('kpi-gain', todayPnL >= 0);
    todayPnLEl.classList.toggle('kpi-loss', todayPnL < 0);
  }

  // Alpha vs S&P 500 (portfolio ROI minus SPY return since inception)
  const alpha = roi - spyChange;
  const alphaEl = document.getElementById('kpi-alpha');
  if (alphaEl) {
    const alphaAnnualized = Math.pow(1 + alpha, 365 / daysElapsed) - 1;
    const alphaAnnSign = alphaAnnualized >= 0 ? '+' : '';
    alphaEl.textContent = (alpha >= 0 ? '+' : '') + (alpha * 100).toFixed(2) + '%'
      + ' (' + alphaAnnSign + (alphaAnnualized * 100).toFixed(0) + '% yr)';
    alphaEl.classList.toggle('kpi-gain', alpha >= 0);
    alphaEl.classList.toggle('kpi-loss', alpha < 0);
  }

  // Sortino Ratio
  const sortinoEl = document.getElementById('kpi-sortino');
  if (sortinoEl) {
    sortinoEl.textContent = sortinoRatio.toFixed(2);
    sortinoEl.classList.toggle('kpi-gain', sortinoRatio >= 0);
    sortinoEl.classList.toggle('kpi-loss', sortinoRatio < 0);
  }

  // Sharpe Ratio
  const sharpeEl = document.getElementById('kpi-sharpe');
  if (sharpeEl) {
    sharpeEl.textContent = sharpeRatio.toFixed(2);
    sharpeEl.classList.toggle('kpi-gain', sharpeRatio >= 0);
    sharpeEl.classList.toggle('kpi-loss', sharpeRatio < 0);
  }

  // Exposure bar
  const totalExposure = longExposure + shortExposure;
  const longPct = totalExposure > 0 ? (longExposure / totalExposure * 100).toFixed(1) : '0.0';
  const shortPct = totalExposure > 0 ? (shortExposure / totalExposure * 100).toFixed(1) : '0.0';

  document.getElementById('exposure-long-bar').style.width = longPct + '%';
  document.getElementById('exposure-short-bar').style.width = shortPct + '%';
  document.getElementById('exposure-long-pct').textContent = longPct + '%';
  document.getElementById('exposure-short-pct').textContent = shortPct + '%';

  return { longExposure, shortExposure, totalPnL, netExposure, grossExposure, sharpeRatio };
}

// ---- RENDER TABLE ----
let currentSort = { key: 'symbol', dir: 'asc' };

function renderTable(positions) {
  const tbody = document.getElementById('positions-body');
  tbody.innerHTML = '';

  // Sort
  const sorted = [...positions].sort((a, b) => {
    let aVal = a[currentSort.key];
    let bVal = b[currentSort.key];
    if (typeof aVal === 'string') {
      aVal = aVal.toLowerCase();
      bVal = bVal.toLowerCase();
    }
    if (aVal < bVal) return currentSort.dir === 'asc' ? -1 : 1;
    if (aVal > bVal) return currentSort.dir === 'asc' ? 1 : -1;
    return 0;
  });

  sorted.forEach(p => {
    const tr = document.createElement('tr');
    tr.className = p.direction === 'Long' ? 'row-long' : 'row-short';

    const dirClass = p.direction === 'Long' ? 'dir-long' : 'dir-short';
    const dirLabel = p.direction === 'Long' ? 'LONG' : 'SHORT';

    const todayPnlClass = p.dayPnLDollar >= 0 ? 'num-positive' : 'num-negative';
    const todayPnlSign = p.dayPnLDollar >= 0 ? '+' : '';

    const pnlClass = p.gainLoss >= 0 ? 'num-positive' : 'num-negative';
    const pnlSign = p.gainLoss >= 0 ? '+' : '';

    // Day change from portfolio perspective (flipped for shorts)
    const dayClass = p.portfolioDayChange >= 0 ? 'num-positive' : 'num-negative';
    const daySign = p.portfolioDayChange >= 0 ? '+' : '';

    // Price flash class
    const priceFlash = p.priceDirection === 'up' ? 'flash-up'
      : p.priceDirection === 'down' ? 'flash-down' : '';

    // Market value display: show as negative for shorts (signed exposure)
    const isLong = p.direction === 'Long';
    const mktValDisplay = isLong ? p.marketValue : -p.marketValue;

    tr.innerHTML = `
      <td class="symbol-cell sticky-col">${p.symbol}</td>
      <td class="name-cell" title="${p.name}"><a href="https://www.marketwatch.com/investing/stock/${p.symbol.toLowerCase()}" target="_blank" rel="noopener noreferrer">${p.name}</a></td>
      <td class="industry-cell" title="${p.industry || ''}">${p.industry || ''}</td>
      <td><span class="dir-badge ${dirClass}">${dirLabel}</span></td>
      <td class="num-cell ${todayPnlClass}">${todayPnlSign}${fmtCurrency.format(p.dayPnLDollar)}</td>
      <td class="num-cell ${pnlClass}">${pnlSign}${fmtCurrency.format(p.gainLoss)}</td>
      <td class="num-cell">${fmtMarketCap(p.marketCap)}</td>
      <td class="num-cell">${fmtInt.format(p.qty)}</td>
      <td class="num-cell price-live ${priceFlash}">${fmtCurrency.format(p.price)}</td>
      <td class="num-cell">${fmtCurrency.format(p.costBasis)}</td>
      <td class="num-cell">${fmtCurrency.format(mktValDisplay)}</td>
      <td class="num-cell ${pnlClass}">${fmtPct.format(p.gainLossPct)}</td>
      <td class="num-cell ${dayClass}">${daySign}${(p.portfolioDayChange * 100).toFixed(2)}%</td>
    `;

    tbody.appendChild(tr);
  });
}

// ---- SORT HANDLER ----
function initSort() {
  const headers = document.querySelectorAll('#positions-table th[data-sort]');
  headers.forEach(th => {
    th.addEventListener('click', () => {
      const key = th.dataset.sort;
      if (currentSort.key === key) {
        currentSort.dir = currentSort.dir === 'asc' ? 'desc' : 'asc';
      } else {
        currentSort.key = key;
        currentSort.dir = 'asc';
      }
      headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
      th.classList.add(currentSort.dir === 'asc' ? 'sort-asc' : 'sort-desc');
      renderTable(computedPositions);
    });
  });
}

// ---- CHART ----
let directionChart = null;

function renderChart(positions) {
  const longs = positions.filter(p => p.direction === 'Long');
  const shorts = positions.filter(p => p.direction === 'Short');

  const longValue = longs.reduce((sum, p) => sum + p.marketValue, 0);
  const shortValue = shorts.reduce((sum, p) => sum + p.marketValue, 0);

  const ctx = document.getElementById('direction-chart').getContext('2d');
  const root = document.documentElement;
  const cs = getComputedStyle(root);
  const gainColor = cs.getPropertyValue('--color-gain').trim() || '#0caf60';
  const lossColor = cs.getPropertyValue('--color-loss').trim() || '#e53e3e';
  const surfaceColor = cs.getPropertyValue('--color-surface').trim() || '#ffffff';

  if (directionChart) directionChart.destroy();

  directionChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Long', 'Short'],
      datasets: [{
        data: [longValue, shortValue],
        backgroundColor: [gainColor, lossColor],
        borderColor: surfaceColor,
        borderWidth: 2,
        hoverBorderColor: surfaceColor,
        hoverBorderWidth: 3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(0,0,0,0.85)',
          titleFont: { family: "'Lato', sans-serif", size: 12 },
          bodyFont: { family: "'Inter', sans-serif", size: 11 },
          padding: 10,
          cornerRadius: 6,
          callbacks: {
            label: function(context) {
              return ' ' + fmtCurrencyCompact.format(context.parsed);
            }
          }
        }
      },
      animation: { animateRotate: true, duration: 800 }
    }
  });
}

// ---- TOP GAINERS / LOSERS ----
function renderTopMovers(positions) {
  const sorted = [...positions].sort((a, b) => b.gainLoss - a.gainLoss);
  const gainers = sorted.slice(0, 5);
  const losers = sorted.slice(-5).reverse();

  const renderList = (items, containerId) => {
    const container = document.getElementById(containerId);
    container.innerHTML = items.map(p => {
      const cls = p.gainLoss >= 0 ? 'num-positive' : 'num-negative';
      const sign = p.gainLoss >= 0 ? '+' : '';
      return `
        <div class="mini-item">
          <div class="mini-info">
            <span class="mini-symbol">${p.symbol}</span>
            <span class="mini-dir ${p.direction === 'Long' ? 'dir-long' : 'dir-short'}">${p.direction === 'Long' ? 'LONG' : 'SHORT'}</span>
            <span class="mini-sector">${p.sector || ''}</span>
          </div>
          <span class="mini-pnl ${cls}">${sign}${fmtCurrency.format(p.gainLoss)}</span>
        </div>
      `;
    }).join('');
  };

  renderList(gainers, 'top-gainers');
  renderList(losers, 'top-losers');
}

// ---- TOP SECTOR GAINERS / LOSERS ----
function renderSectorMovers(positions) {
  // Aggregate by sector+direction: sum cost and sum market value, then compute % return
  const sectorMap = {};
  positions.forEach(p => {
    const key = `${p.sector}|${p.direction}`;
    if (!sectorMap[key]) {
      sectorMap[key] = { sector: p.sector, direction: p.direction, totalCost: 0, totalGainLoss: 0 };
    }
    sectorMap[key].totalCost += p.costTotal;
    sectorMap[key].totalGainLoss += p.gainLoss;
  });

  // Convert to array and compute aggregate P&L %
  const sectors = Object.values(sectorMap).map(s => ({
    ...s,
    pct: s.totalCost !== 0 ? s.totalGainLoss / s.totalCost : 0
  }));

  // Sort by pct descending
  const sorted = [...sectors].sort((a, b) => b.pct - a.pct);
  const gainers = sorted.filter(s => s.pct >= 0).slice(0, 5);
  const losers = sorted.filter(s => s.pct < 0).sort((a, b) => a.pct - b.pct).slice(0, 5);

  const renderSectorList = (items, containerId) => {
    const container = document.getElementById(containerId);
    container.innerHTML = items.map(s => {
      const cls = s.pct >= 0 ? 'num-positive' : 'num-negative';
      const sign = s.pct >= 0 ? '+' : '';
      const dirClass = s.direction === 'Long' ? 'dir-long' : 'dir-short';
      const dirLabel = s.direction === 'Long' ? 'LONG' : 'SHORT';
      return `
        <div class="mini-item">
          <div class="mini-info">
            <span class="mini-symbol">${s.sector}</span>
            <span class="mini-dir ${dirClass}">${dirLabel}</span>
          </div>
          <span class="mini-pnl ${cls}">${sign}${(s.pct * 100).toFixed(2)}%</span>
        </div>
      `;
    }).join('');
  };

  renderSectorList(gainers, 'top-sector-gainers');
  renderSectorList(losers, 'top-sector-losers');
}

// ---- TODAY'S TOP SECTOR GAINERS / LOSERS ----
function renderTodaySectorMovers(positions) {
  // Aggregate today's day P&L by sector+direction
  const sectorMap = {};
  positions.forEach(p => {
    const key = `${p.sector}|${p.direction}`;
    if (!sectorMap[key]) {
      sectorMap[key] = { sector: p.sector, direction: p.direction, totalDayPnL: 0, totalMktVal: 0 };
    }
    sectorMap[key].totalDayPnL += p.dayPnLDollar;
    sectorMap[key].totalMktVal += p.marketValue;
  });

  // Compute today's % change for each sector bucket
  const sectors = Object.values(sectorMap).map(s => ({
    ...s,
    dayPct: s.totalMktVal !== 0 ? s.totalDayPnL / s.totalMktVal : 0
  }));

  const sorted = [...sectors].sort((a, b) => b.dayPct - a.dayPct);
  const gainers = sorted.filter(s => s.dayPct >= 0).slice(0, 5);
  const losers = sorted.filter(s => s.dayPct < 0).sort((a, b) => a.dayPct - b.dayPct).slice(0, 5);

  const renderList = (items, containerId) => {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = items.map(s => {
      const cls = s.dayPct >= 0 ? 'num-positive' : 'num-negative';
      const sign = s.dayPct >= 0 ? '+' : '';
      const dirClass = s.direction === 'Long' ? 'dir-long' : 'dir-short';
      const dirLabel = s.direction === 'Long' ? 'LONG' : 'SHORT';
      return `
        <div class="mini-item">
          <div class="mini-info">
            <span class="mini-symbol">${s.sector}</span>
            <span class="mini-dir ${dirClass}">${dirLabel}</span>
          </div>
          <span class="mini-pnl ${cls}">${sign}${(s.dayPct * 100).toFixed(2)}%</span>
        </div>
      `;
    }).join('');
  };

  renderList(gainers, 'today-sector-gainers');
  renderList(losers, 'today-sector-losers');
}

// ---- TODAY'S TOP GAINERS / LOSERS (Individual Positions) ----
function renderTodayTopMovers(positions) {
  const sorted = [...positions].sort((a, b) => b.dayPnLDollar - a.dayPnLDollar);
  const gainers = sorted.slice(0, 5);
  const losers = sorted.slice(-5).reverse();

  const renderList = (items, containerId) => {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = items.map(p => {
      const cls = p.dayPnLDollar >= 0 ? 'num-positive' : 'num-negative';
      const sign = p.dayPnLDollar >= 0 ? '+' : '';
      return `
        <div class="mini-item">
          <div class="mini-info">
            <span class="mini-symbol">${p.symbol}</span>
            <span class="mini-dir ${p.direction === 'Long' ? 'dir-long' : 'dir-short'}">${p.direction === 'Long' ? 'LONG' : 'SHORT'}</span>
            <span class="mini-sector">${p.sector || ''}</span>
          </div>
          <span class="mini-pnl ${cls}">${sign}${fmtCurrency.format(p.dayPnLDollar)}</span>
        </div>
      `;
    }).join('');
  };

  renderList(gainers, 'today-top-gainers');
  renderList(losers, 'today-top-losers');
}

// ---- THEME TOGGLE ----
function initTheme() {
  const toggle = document.querySelector('[data-theme-toggle]');
  const root = document.documentElement;
  let theme = root.getAttribute('data-theme') || 'dark';

  if (toggle) {
    toggle.innerHTML = theme === 'dark'
      ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
      : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

    toggle.addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', theme);
      toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
      toggle.innerHTML = theme === 'dark'
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
      setTimeout(() => renderChart(computedPositions), 50);
    });
  }
}

// ---- INIT ----
let computedPositions = [];

// ---- RENDER MODEL PICKS (today's 5 picks per model) ----
function renderModelPicks() {
  const container = document.getElementById('model-picks-container');
  if (!container || typeof MODEL_PICKS === 'undefined') return;

  // Build set of fund symbols for highlighting overlap
  const fundSymbols = new Set(POSITIONS.map(p => p.symbol));

  // Set date to today only
  const dateEl = document.getElementById('model-picks-date');
  if (dateEl) {
    const today = new Date();
    const opts = { year: 'numeric', month: 'long', day: 'numeric' };
    dateEl.textContent = today.toLocaleDateString('en-US', opts);
  }

  container.innerHTML = MODEL_PICKS.models.map(model => {
    // Only show the latest 5 picks (today's) per model
    const todayPicks = model.picks.slice(-5);
    const picksHTML = todayPicks.map(p => {
      const dirClass = p.direction === 'Long' ? 'dir-long' : 'dir-short';
      const dirLabel = p.direction === 'Long' ? 'LONG' : 'SHORT';
      const mktVal = p.qty * (p.livePrice || p.price);
      const inFund = fundSymbols.has(p.symbol);
      const fundClass = inFund ? ' pick-card-in-fund' : '';
      const fundBadge = inFund ? '<span class="fund-badge" title="Also a live fund position">LIVE</span>' : '';

      return `
        <div class="pick-card${fundClass}">
          <div class="pick-header">
            <div class="pick-symbol-row">
              <a href="https://www.marketwatch.com/investing/stock/${p.symbol.toLowerCase()}" target="_blank" rel="noopener noreferrer" class="pick-symbol">${p.symbol}</a>
              <span class="dir-badge ${dirClass}">${dirLabel}</span>
              ${fundBadge}
            </div>
            <span class="pick-name">${p.name}</span>
            <span class="pick-industry">${p.industry || ''}${p.marketCap ? ' \u00b7 ' + fmtMarketCap(p.marketCap) : ''}</span>
          </div>
          <div class="pick-details">
            <div class="pick-stat">
              <span class="pick-stat-label">Shares</span>
              <span class="pick-stat-value">${fmtInt.format(p.qty)}</span>
            </div>
            <div class="pick-stat">
              <span class="pick-stat-label">Price</span>
              <span class="pick-stat-value">${fmtCurrency.format(p.price)}</span>
            </div>
            <div class="pick-stat">
              <span class="pick-stat-label">Mkt Val</span>
              <span class="pick-stat-value">${fmtCurrency.format(mktVal)}</span>
            </div>
          </div>
          <p class="pick-rationale">${p.rationale}</p>
        </div>
      `;
    }).join('');

    return `
      <div class="model-row">
        <div class="model-label">
          <span class="model-icon">${model.icon}</span>
          <span>${model.name}</span>
        </div>
        <div class="model-picks-grid">
          ${picksHTML}
        </div>
      </div>
    `;
  }).join('');
}

// ---- RENDER MODEL LEADERBOARD ----
function renderLeaderboardFromPrices(priceMap) {
  const tbody = document.getElementById('leaderboard-body');
  if (!tbody || typeof MODEL_PICKS === 'undefined') return;
  if (!priceMap || Object.keys(priceMap).length === 0) return;

  // Update the note
  const noteEl = document.getElementById('leaderboard-note');
  if (noteEl) noteEl.textContent = 'Live';

  // Build set of fund symbols for chosen count
  const fundSymbols = new Set(POSITIONS.map(p => p.symbol));

  // Compute stats for each model
  const modelStats = MODEL_PICKS.models.map(model => {
    let totalPnL = 0;
    let wins = 0;
    let losses = 0;
    const pnlPcts = [];
    let chosenCount = 0;

    model.picks.forEach(pick => {
      // Count picks that overlap with live fund
      if (fundSymbols.has(pick.symbol)) chosenCount++;

      // Use price map first (Finnhub live), fall back to embedded livePrice
      const live = priceMap[pick.symbol];
      const currentPrice = live ? live.price : (pick.livePrice || pick.price);

      const isLong = pick.direction === 'Long';
      const pnl = isLong
        ? (currentPrice - pick.price) * pick.qty
        : (pick.price - currentPrice) * pick.qty;
      const pnlPct = pick.price !== 0
        ? (isLong
          ? (currentPrice - pick.price) / pick.price
          : (pick.price - currentPrice) / pick.price)
        : 0;

      totalPnL += pnl;
      pnlPcts.push(pnlPct);
      if (pnl > 0) wins++;
      else if (pnl < 0) losses++;
    });

    const totalTrades = model.picks.length;
    const resolved = wins + losses;
    const winRate = resolved > 0 ? wins / resolved : 0;
    const avgReturn = pnlPcts.length > 0
      ? pnlPcts.reduce((s, v) => s + v, 0) / pnlPcts.length
      : 0;

    return { ...model, totalPnL, winRate, avgReturn, totalTrades, chosenCount };
  });

  // Sort by totalPnL descending
  const ranked = modelStats.sort((a, b) => b.totalPnL - a.totalPnL);
  const medals = ['\u{1F947}', '\u{1F948}', '\u{1F949}'];

  const fmtLbPnL = new Intl.NumberFormat('en-US', {
    style: 'currency', currency: 'USD',
    minimumFractionDigits: 2, maximumFractionDigits: 2,
    signDisplay: 'always'
  });
  const fmtLbPct = new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 2, maximumFractionDigits: 2,
    signDisplay: 'always'
  });

  tbody.innerHTML = ranked.map((model, i) => {
    const pnlClass = model.totalPnL >= 0 ? 'num-positive' : 'num-negative';
    const wrDisplay = (model.winRate * 100).toFixed(0) + '%';
    const avgClass = model.avgReturn >= 0 ? 'num-positive' : 'num-negative';
    const chosenBadgeClass = model.chosenCount > 0 ? 'chosen-badge-active' : 'chosen-badge-zero';

    return `
      <tr>
        <td class="lb-rank">${medals[i] || i + 1}</td>
        <td class="lb-model"><span class="model-icon">${model.icon}</span> ${model.name}</td>
        <td class="lb-chosen"><span class="chosen-badge ${chosenBadgeClass}">${model.chosenCount}</span></td>
        <td class="num-cell ${pnlClass}">${fmtLbPnL.format(model.totalPnL)}</td>
        <td class="num-cell">${wrDisplay}</td>
        <td class="num-cell ${avgClass}">${fmtLbPct.format(model.avgReturn)}</td>
        <td class="num-cell">${model.totalTrades}</td>
      </tr>
    `;
  }).join('');
}

function init() {
  // Compute with embedded prices (no zeros)
  computedPositions = computePositions(POSITIONS);

  // Render immediately with real data
  renderAll(computedPositions);

  initSort();
  initTheme();
  renderModelPicks();

  // Render leaderboard immediately from embedded livePrice values in MODEL_PICKS
  // (These are updated by the cron job alongside position prices)
  if (typeof MODEL_PICKS !== 'undefined') {
    const embeddedPriceMap = {};
    MODEL_PICKS.models.forEach(m => {
      m.picks.forEach(p => {
        if (p.livePrice && p.livePrice !== p.price) {
          embeddedPriceMap[p.symbol] = { symbol: p.symbol, price: p.livePrice, prevClose: p.price };
        }
      });
    });
    if (Object.keys(embeddedPriceMap).length > 0) {
      renderLeaderboardFromPrices(embeddedPriceMap);
    }
  }

  document.getElementById('btn-refresh').addEventListener('click', fetchLivePrices);

  // Detect horizontally scrollable table and add scroll hint class
  const tableWrapper = document.querySelector('.table-wrapper');
  if (tableWrapper) {
    const checkScroll = () => {
      const isScrollable = tableWrapper.scrollWidth > tableWrapper.clientWidth;
      const isScrolledToEnd = tableWrapper.scrollLeft + tableWrapper.clientWidth >= tableWrapper.scrollWidth - 2;
      tableWrapper.classList.toggle('has-scroll', isScrollable && !isScrolledToEnd);
    };
    checkScroll();
    tableWrapper.addEventListener('scroll', checkScroll, { passive: true });
    window.addEventListener('resize', checkScroll, { passive: true });
  }

  // Show initial timestamp
  const now = new Date();
  const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  document.getElementById('last-updated').textContent = `Updated ${timeStr}`;

  const defaultTh = document.querySelector('#positions-table th[data-sort="symbol"]');
  if (defaultTh) defaultTh.classList.add('sort-asc');

  // Start auto-refreshing (Worker will override prices when available)
  startAutoRefresh();
}

document.addEventListener('DOMContentLoaded', init);
