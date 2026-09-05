/* Hyper — Portfolio Scenarios (LIVE)
   Reads the account 0xD71a…95Bc from the Hyperliquid info API in the browser (CORS-open), then prices the book
   at a ladder of price rungs two ways: HOLD AS-IS (today's positions marked at the rung) and WITH ORDERS (every
   resting instruction — reduce-only ladders, stops, opening bids, buy/sell TWAPs — executes along a straight
   path from today's marks to the rung). Same model as the Sep 5 2026 baked build (hyper/scripts), generalised
   to whatever positions the account holds, and re-run every 60 seconds. Read-only: nothing here can trade. */
(function () {
  'use strict';

  var ADDR = '0xD71a41eC000089ae99873AFB4D15CC7d54Dd95Bc';
  var API = 'https://api.hyperliquid.xyz/info';
  var REFRESH_S = 60;
  var TAKER = 0.00035, MAKER = 0.00010;
  var STEPS = 800, GRID_STEPS = 300;
  var FETCH_TIMEOUT_MS = 20000;

  // ---------------------------------------------------------------- formatting
  function usd(v, dp) { dp = dp || 0; var s = Math.abs(v).toLocaleString('en-US', { minimumFractionDigits: dp, maximumFractionDigits: dp }); return (v < 0 ? '−' : '') + '$' + s; }
  function sgn(v, dp) { dp = dp || 0; var s = Math.abs(v).toLocaleString('en-US', { minimumFractionDigits: dp, maximumFractionDigits: dp }); return (v < 0 ? '−' : '+') + '$' + s; }
  function pct(v, dp) { if (dp === undefined) dp = 1; return (v < 0 ? '−' : '+') + (Math.abs(v) * 100).toFixed(dp) + '%'; }
  function pxf(p) { if (p === null || p === undefined || !isFinite(p)) return '—'; if (p >= 1000) return Math.round(p).toLocaleString('en-US'); if (Math.abs(p - Math.round(p)) < 1e-9 && p >= 1) return String(Math.round(p)); if (p >= 10) return p.toFixed(2); if (p >= 1) return p.toFixed(3); return p.toFixed(4); }
  function num(v, dp) { return Number(v).toLocaleString('en-US', { minimumFractionDigits: dp, maximumFractionDigits: dp }); }
  function kf(v) { return (v < 0 ? '−' : '') + '$' + (Math.abs(v) / 1000).toFixed(1) + 'k'; }
  function szf(coin, q) { return coin === 'BTC' ? q.toFixed(3) : (Math.abs(q) >= 100 ? num(q, 0) : q.toFixed(2)); }
  function cls(v) { return v > 0 ? 'pm-pos' : (v < 0 ? 'pm-neg' : ''); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function utc(ms) { var d = new Date(ms); return d.toISOString().slice(0, 16).replace('T', ' ') + ' UTC'; }
  function pt(ms) { return new Date(ms).toLocaleString('en-US', { timeZone: 'America/Los_Angeles', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }) + ' PT'; }

  // ---------------------------------------------------------------- api
  function post(body) {
    var ctl = (typeof AbortController !== 'undefined') ? new AbortController() : null;
    var t = ctl ? setTimeout(function () { ctl.abort(); }, FETCH_TIMEOUT_MS) : null;
    return fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal: ctl ? ctl.signal : undefined })
      .then(function (r) { if (t) clearTimeout(t); if (!r.ok) throw new Error('HTTP ' + r.status + ' from info/' + body.type); return r.json(); },
            function (e) { if (t) clearTimeout(t); throw new Error((e && e.name === 'AbortError') ? 'timeout after ' + (FETCH_TIMEOUT_MS / 1000) + 's on info/' + body.type : (e && e.message ? e.message : String(e))); });
  }

  function parseTrigger(o) {
    var tc = String(o.triggerCondition || '');
    if (/below/i.test(tc)) return 'below';
    if (/above/i.test(tc)) return 'above';
    var ot = String(o.orderType || '');
    if (/stop/i.test(ot)) return o.side === 'A' ? 'below' : 'above';
    if (/take profit/i.test(ot)) return o.side === 'A' ? 'above' : 'below';
    return o.side === 'A' ? 'below' : 'above';
  }

  var cache = { fund: null, fundAt: 0, candles: {}, candlesAt: 0 };
  function withRetry(fn, tries, delayMs) {
    return fn().then(null, function (e) { if (tries <= 1) throw e; return new Promise(function (r) { setTimeout(r, delayMs); }).then(function () { return withRetry(fn, tries - 1, delayMs * 3); }); });
  }
  function load() {
    var t0 = Date.now();
    var fundP = (cache.fund && t0 - cache.fundAt < 600000) ? Promise.resolve(cache.fund) : post({ type: 'userFunding', user: ADDR, startTime: t0 - 86400000 }).then(function (f) { cache.fund = f; cache.fundAt = t0; return f; });
    return Promise.all([
      post({ type: 'webData2', user: ADDR }),
      fundP
    ]).then(function (res) {
      var w = res[0], fund = res[1];
      var metaP = (w.meta && w.meta.marginTables) ? Promise.resolve(w.meta) : post({ type: 'meta' });
      var ordP = (w.openOrders && w.openOrders.length && w.openOrders[0].isTrigger !== undefined) ? Promise.resolve(w.openOrders) : post({ type: 'frontendOpenOrders', user: ADDR });
      return Promise.all([metaP, ordP]).then(function (r2) {
        var meta = r2[0], rawOrders = r2[1];
        var idx = {}; meta.universe.forEach(function (u, i) { idx[u.name] = i; });
        var tables = {}; (meta.marginTables || []).forEach(function (mt) { tables[mt[0]] = mt[1].marginTiers.map(function (x) { return { lb: +x.lowerBound, maxLev: +x.maxLeverage }; }); });
        var chs = w.clearinghouseState;
        var positions = chs.assetPositions.map(function (p) {
          var q = p.position, u = meta.universe[idx[q.coin]], ctx = w.assetCtxs[idx[q.coin]];
          return { coin: q.coin, sz: +q.szi, entry: +q.entryPx, mark: +ctx.markPx, oracle: +ctx.oraclePx, funding: +ctx.funding, prevDay: +ctx.prevDayPx,
                   maxLev: u.maxLeverage, tiers: tables[u.marginTableId] || [{ lb: 0, maxLev: u.maxLeverage }], lev: +q.leverage.value, levType: q.leverage.type,
                   liqPxExch: q.liquidationPx ? +q.liquidationPx : null, uPnl: +q.unrealizedPnl, marginUsed: +q.marginUsed, cumFunding: +(q.cumFunding && q.cumFunding.sinceOpen || 0) };
        }).filter(function (p) { return p.sz !== 0; });
        positions.sort(function (a, b) { return Math.abs(b.sz * b.mark) - Math.abs(a.sz * a.mark); });
        var orders = rawOrders.map(function (o) {
          return { coin: o.coin, side: o.side, sz: +o.sz, px: +o.limitPx, reduceOnly: !!o.reduceOnly, isTrigger: !!o.isTrigger, triggerPx: +(o.triggerPx || 0),
                   trigDir: o.isTrigger ? parseTrigger(o) : null, isLimitTrigger: !!o.isTrigger && /limit/i.test(String(o.orderType || '')), orderType: o.orderType || (o.isTrigger ? 'Trigger' : 'Limit'), oid: o.oid };
        });
        var twaps = (w.twapStates || []).map(function (t) { var s = t[1]; return { id: t[0], coin: s.coin, side: s.side, sz: +s.sz, executed: +s.executedSz, executedNtl: +s.executedNtl, minutes: +s.minutes, reduceOnly: !!s.reduceOnly, timestamp: +s.timestamp }; });
        var fund24 = fund.reduce(function (s, f) { return s + (+f.delta.usdc); }, 0);
        var book = { t: t0, serverTime: w.serverTime || t0, eq: +chs.marginSummary.accountValue, ntl: +chs.marginSummary.totalNtlPos, mmExch: +chs.crossMaintenanceMarginUsed,
                     muExch: +chs.marginSummary.totalMarginUsed, withdrawable: +chs.withdrawable, positions: positions, orders: orders, twaps: twaps, fund24: fund24 };
        // candles for the top two positions (beta, vol)
        var top = positions.slice(0, 2);
        var fresh = t0 - cache.candlesAt < 3600000 && top.every(function (p) { return cache.candles[p.coin]; });
        if (fresh) { book.candles = cache.candles; return book; }
        return Promise.all(top.map(function (p) { return post({ type: 'candleSnapshot', req: { coin: p.coin, interval: '1d', startTime: t0 - 61 * 86400000, endTime: t0 } }); }))
          .then(function (cs) { book.candles = {}; top.forEach(function (p, i) { book.candles[p.coin] = (cs[i] || []).map(function (k) { return { t: +k.t, c: +k.c }; }); }); cache.candles = book.candles; cache.candlesAt = t0; return book; });
      });
    });
  }

  // ---------------------------------------------------------------- model
  function maintOf(pos, notional) { // half of the initial margin at the asset's max leverage, cumulative across margin tiers
    var im = 0, tiers = pos.tiers;
    for (var i = 0; i < tiers.length; i++) {
      var lb = tiers[i].lb, ub = (i + 1 < tiers.length) ? tiers[i + 1].lb : Infinity;
      if (notional <= lb) break;
      im += (Math.min(notional, ub) - lb) / tiers[i].maxLev;
    }
    return 0.5 * im;
  }
  function slipOf(coin) { return (coin === 'BTC' || coin === 'ETH') ? 0.0003 : 0.001; }

  function mkState(book) {
    var st = { cash: book.eq, sz: {}, mark: {}, pos: {} };
    book.positions.forEach(function (p) { st.sz[p.coin] = p.sz; st.mark[p.coin] = p.mark; st.pos[p.coin] = p; st.cash -= p.sz * p.mark; });
    return st;
  }
  function equityAt(st, px) { var e = st.cash; for (var c in st.sz) e += st.sz[c] * px[c]; return e; }
  function maintAt(st, px, szMap) { szMap = szMap || st.sz; var m = 0; for (var c in szMap) m += maintOf(st.pos[c], Math.abs(szMap[c]) * px[c]); return m; }
  function imAt(st, px, szMap) { var m = 0; for (var c in szMap) m += Math.abs(szMap[c]) * px[c] / st.pos[c].lev; return m; }

  function pricesAt(st, targets, f) { var px = {}; for (var c in st.mark) px[c] = (c in targets) ? st.mark[c] + (targets[c] - st.mark[c]) * f : st.mark[c]; return px; }

  // hold as-is: exact crossing by scan + bisection (maintenance is piecewise linear with tiers)
  function holdAsIs(book, targets) {
    var st = mkState(book), N = 400, liq = null, prevF = 0;
    function g(f) { var px = pricesAt(st, targets, f); return equityAt(st, px) - maintAt(st, px); }
    for (var i = 1; i <= N; i++) {
      var f = i / N;
      if (g(f) < 0) { var lo = prevF, hi = f; for (var k = 0; k < 40; k++) { var mid = (lo + hi) / 2; if (g(mid) < 0) hi = mid; else lo = mid; } liq = pricesAt(st, targets, hi); break; }
      prevF = f;
    }
    var pxT = pricesAt(st, targets, 1), eq = equityAt(st, pxT), m = maintAt(st, pxT), ntl = 0;
    for (var c in st.sz) ntl += Math.abs(st.sz[c]) * pxT[c];
    return { eq: eq, pnl: eq - book.eq, maint: m, ntl: ntl, liq: liq, sz: st.sz };
  }

  // with orders along a straight path. opts.twap: 'path' | 'none' | 'first'
  function simulate(book, targets, opts) {
    // Straight-line path in every moved coin. Each coin's price is monotone along the path, so its orders can be
    // queued in the order they will be reached and consumed with a cursor — O(steps + orders) per scenario.
    opts = opts || {}; var mode = opts.twap || 'path'; var N = opts.steps || STEPS;
    var st = mkState(book);
    var tw = book.twaps.filter(function (t) { return t.coin in st.sz; }).map(function (t) { return { coin: t.coin, side: t.side, reduceOnly: t.reduceOnly, rem: Math.max(0, t.sz - t.executed), filled: 0, ntl: 0 }; });
    var stats = {}; for (var c in st.sz) stats[c] = { sold: 0, soldNtl: 0, bought: 0, boughtNtl: 0, twap: 0, twapNtl: 0, ladderSold: 0, ladderNtl: 0, stopSold: 0, stopNtl: 0 };
    var fees = 0, liq = null, liqMaint = null, liqEq = null, liqSz = null;

    function fill(coin, dir, q, fillPx, fee, px, isTwap, kind) {
      if (q <= 0) return 0;
      var after = {}; for (var k in st.sz) after[k] = st.sz[k]; after[coin] = st.sz[coin] + dir * q;
      var reducing = Math.abs(after[coin]) < Math.abs(st.sz[coin]);
      if (!reducing && equityAt(st, px) < imAt(st, px, after)) return 0;   // exchange rejects/cancels adds without initial margin
      st.cash -= dir * q * fillPx; st.cash -= q * fillPx * fee; fees += q * fillPx * fee; st.sz[coin] = after[coin];
      var s = stats[coin];
      if (isTwap) { s.twap += q; s.twapNtl += q * fillPx; }
      else if (!reducing) { s.bought += q; s.boughtNtl += q * fillPx; }   // adds to the position (scale-in)
      else { s.sold += q; s.soldNtl += q * fillPx; if (kind === 'ladder') { s.ladderSold += q; s.ladderNtl += q * fillPx; } else { s.stopSold += q; s.stopNtl += q * fillPx; } }   // closes part of the position
      return q;
    }
    function execOrder(o, p, px) {   // o has been reached by the path at price p; returns true if it is consumed
      var fillPx = 0, fee = MAKER, kind = 'ladder';
      if (o.isTrigger) {
        var marketable = !o.isLimitTrigger || (o.side === 'A' ? o.px <= p : o.px >= p);
        if (!marketable) { o.isTrigger = false; return false; }   // stop-limit / take-profit-limit whose limit is not yet marketable now rests as a plain limit
        var sl = slipOf(o.coin); fillPx = o.triggerPx * (o.side === 'A' ? 1 - sl : 1 + sl); fee = TAKER; kind = 'stop';
      } else fillPx = o.side === 'A' ? Math.max(o.px, p) : Math.min(o.px, p);   // a limit already marketable fills at the better price
      var dir = o.side === 'B' ? 1 : -1, q = o.sz;
      if (o.reduceOnly) { if (st.sz[o.coin] === 0 || Math.sign(st.sz[o.coin]) === dir) return true; q = Math.min(q, Math.abs(st.sz[o.coin])); }
      fill(o.coin, dir, q, fillPx, fee, px, false, kind);
      return true;
    }
    // queues: per coin, the orders the path can reach, sorted in the order the path reaches them
    function firePx(o) { return o.isTrigger ? o.triggerPx : o.px; }
    function firesDown(o) { return o.isTrigger ? o.trigDir === 'below' : o.side === 'B'; }   // reached by a falling price
    var queues = {}, immediate = [], converted = [];
    book.orders.forEach(function (o) {
      if (!(o.coin in st.sz)) return;
      var q = {}; for (var k in o) q[k] = o[k];
      var m0 = st.mark[o.coin], d = (o.coin in targets) ? Math.sign(targets[o.coin] - m0) : 0;
      var already = firesDown(q) ? firePx(q) >= m0 : firePx(q) <= m0;   // condition already true at today's mark
      if (already) { immediate.push(q); return; }
      if (d === 0) return;                                                 // this coin does not move: nothing else on it is reached
      if (firesDown(q) !== (d < 0)) return;                                // wrong side of the path
      if (!queues[o.coin]) queues[o.coin] = [];
      queues[o.coin].push(q);
    });
    for (var qc in queues) queues[qc].sort(function (a, b) { return (targets[qc] < st.mark[qc]) ? firePx(b) - firePx(a) : firePx(a) - firePx(b); });
    var cursor = {}; for (var qc2 in queues) cursor[qc2] = 0;

    if (mode === 'first') {
      var px0 = pricesAt(st, targets, 0);
      tw.forEach(function (t) { if (t.rem <= 0) return; var dir = t.side === 'B' ? 1 : -1; var q = t.rem; if (t.reduceOnly) { if (st.sz[t.coin] === 0 || Math.sign(st.sz[t.coin]) === dir) return; q = Math.min(q, Math.abs(st.sz[t.coin])); }
        var f = fill(t.coin, dir, q, px0[t.coin], TAKER, px0, true); t.filled += f; t.ntl += f * px0[t.coin]; });
    }
    for (var i = 1; i <= N; i++) {
      var px = pricesAt(st, targets, i / N);
      if (mode === 'path') {
        tw.forEach(function (t) { if (t.rem <= 0) return; var dir = t.side === 'B' ? 1 : -1; var q = t.rem / N; if (t.reduceOnly) { if (st.sz[t.coin] === 0 || Math.sign(st.sz[t.coin]) === dir) return; q = Math.min(q, Math.abs(st.sz[t.coin])); }
          var f = fill(t.coin, dir, q, px[t.coin], TAKER, px, true); t.filled += f; t.ntl += f * px[t.coin]; });
      }
      if (i === 1 && immediate.length) { immediate.forEach(function (o) { if (!execOrder(o, px[o.coin], px)) converted.push(o); }); immediate = []; }
      for (var c3 in queues) {
        var list = queues[c3], p = px[c3], down = targets[c3] < st.mark[c3];
        while (cursor[c3] < list.length) {
          var o = list[cursor[c3]], fp = firePx(o);
          if (down ? p > fp : p < fp) break;   // not reached yet (and nothing behind it is either)
          cursor[c3]++;
          if (!execOrder(o, p, px)) converted.push(o);
        }
      }
      if (converted.length) { converted = converted.filter(function (o) { var p2 = px[o.coin]; if (o.side === 'B' ? p2 <= o.px : p2 >= o.px) { execOrder(o, p2, px); return false; } return true; }); }
      var eqNow = equityAt(st, px), mtNow = maintAt(st, px);
      if (eqNow < mtNow) { liq = px; liqMaint = mtNow; liqEq = eqNow; liqSz = {}; for (var cc in st.sz) liqSz[cc] = st.sz[cc]; break; }
    }
    var pxT = pricesAt(st, targets, 1), eq = equityAt(st, pxT), m = maintAt(st, pxT), ntl = 0;
    for (var c2 in st.sz) ntl += Math.abs(st.sz[c2]) * pxT[c2];
    var twapOut = {}; tw.forEach(function (t) { if (!twapOut[t.coin]) twapOut[t.coin] = { filled: 0, ntl: 0, rem: 0 }; twapOut[t.coin].filled += t.filled; twapOut[t.coin].ntl += t.ntl; twapOut[t.coin].rem += t.rem; });
    return { eq: eq, pnl: eq - book.eq, maint: m, ntl: ntl, liq: liq, liqMaint: liqMaint, liqEq: liqEq, liqSz: liqSz, sz: st.sz, fees: fees, stats: stats, twap: twapOut };
  }

  // liquidation solvers on an arbitrary state: coin alone, and joint with the secondary moving beta x the primary's % move
  function solveLiq(st, moves, ref) { // moves: {coin: multiplier on the reference coin's adverse move d}; every mover follows the reference coin's direction
    var sgnRef = st.sz[ref] >= 0 ? 1 : -1;
    function g(d) { var px = {}; for (var c in st.mark) { var m = moves[c]; px[c] = (m === undefined) ? st.mark[c] : st.mark[c] * (1 - m * d * sgnRef); } return equityAt(st, px) - maintAt(st, px); }
    if (g(0) <= 0) return { d: 0 };
    var lo = 0, hi = 0.999; if (g(hi) > 0) return null;
    for (var k = 0; k < 60; k++) { var mid = (lo + hi) / 2; if (g(mid) < 0) hi = mid; else lo = mid; }
    return { d: hi };
  }
  function liqPrice(st, coin, moves) { var r = solveLiq(st, moves, coin); if (!r) return null; var m = moves[coin] || 1; return st.mark[coin] * (1 - m * r.d * (st.sz[coin] >= 0 ? 1 : -1)); }

  function afterTwaps(book) { // the book once every TWAP remainder has filled at today's marks (taker fees), prices unchanged
    var st = mkState(book);
    book.twaps.forEach(function (t) { if (!(t.coin in st.sz)) return; var rem = Math.max(0, t.sz - t.executed); var dir = t.side === 'B' ? 1 : -1; var p = st.mark[t.coin];
      if (t.reduceOnly) { if (st.sz[t.coin] === 0 || Math.sign(st.sz[t.coin]) === dir) return; rem = Math.min(rem, Math.abs(st.sz[t.coin])); }
      st.cash -= dir * rem * p + rem * p * TAKER; st.sz[t.coin] += dir * rem; });
    return st;
  }

  // EFFECTIVE liquidation: the price at which the book crosses maintenance on a straight adverse path with every resting
  // order executing on the way (stops, bids, ladders) — i.e. "as if the stops fire". TWAP remainder excluded by default
  // (it is time-dependent); opts.twap = 'path' includes it spread along the path.
  function effLiq(book, coin, moves, opts) {
    var P = book.positions.filter(function (p) { return p.coin === coin; })[0]; if (!P) return null;
    var adverse = P.sz > 0 ? -1 : 1;                       // a long is hurt by a fall, a short by a rise
    var targets = {};
    book.positions.forEach(function (p) { var m = moves[p.coin]; if (m === undefined) return; targets[p.coin] = p.mark * (1 + adverse * m * (P.sz > 0 ? 1 : 1) * 0.6 * (p.coin === coin ? 1 : 1)); });
    // secondary coins move m × the primary's percentage move, in the same direction
    for (var c in targets) if (c !== coin) targets[c] = book.positions.filter(function (p) { return p.coin === c; })[0].mark * (1 + adverse * 0.6 * moves[c]);
    var r = simulate(book, targets, { twap: (opts && opts.twap) || 'none', steps: 4000 });
    if (opts && opts.full) return r;
    return r.liq ? r.liq[coin] : null;
  }
  function bookAfterTwaps(book) {   // a shallow copy of the book with every TWAP remainder filled at today's marks (taker fees), no TWAPs left
    var stA = afterTwaps(book);
    var b2 = {}; for (var k in book) b2[k] = book[k];
    b2.eq = equityAt(stA, stA.mark);
    b2.positions = book.positions.map(function (p) { var q = {}; for (var k2 in p) q[k2] = p[k2]; q.sz = stA.sz[p.coin]; return q; }).filter(function (p) { return p.sz !== 0; });
    b2.twaps = [];
    return b2;
  }

  function stats60(book, c1, c2) {
    var a = book.candles[c1] || [], b = c2 ? (book.candles[c2] || []) : null;
    function lr(x) { var r = []; for (var i = 1; i < x.length; i++) r.push({ t: x[i].t, v: Math.log(x[i].c / x[i - 1].c) }); return r; }
    function sd(x) { if (x.length < 3) return NaN; var m = x.reduce(function (s, v) { return s + v; }, 0) / x.length; return Math.sqrt(x.reduce(function (s, v) { return s + (v - m) * (v - m); }, 0) / (x.length - 1)); }
    var ra = lr(a), va = ra.map(function (r) { return r.v; }), out = { n: ra.length, sdA30: sd(va.slice(-30)), sdA60: sd(va), betaOk: false };
    if (b) {
      var rb = lr(b), byT = {}; rb.forEach(function (r) { byT[r.t] = r.v; });
      var x = [], y = []; ra.forEach(function (r) { if (byT[r.t] !== undefined) { x.push(r.v); y.push(byT[r.t]); } });   // join on candle timestamp
      var n = x.length; out.n = n; out.sdB30 = sd(rb.map(function (r) { return r.v; }).slice(-30)); out.sdB60 = sd(rb.map(function (r) { return r.v; }));
      if (n >= 10) { var mx = x.reduce(function (s, v) { return s + v; }, 0) / n, my = y.reduce(function (s, v) { return s + v; }, 0) / n; var cov = 0, vx = 0, vy = 0; for (var i = 0; i < n; i++) { cov += (x[i] - mx) * (y[i] - my); vx += (x[i] - mx) * (x[i] - mx); vy += (y[i] - my) * (y[i] - my); }
        if (vx > 0 && vy > 0) { out.beta = cov / vx; out.corr = cov / Math.sqrt(vx * vy); out.betaOk = isFinite(out.beta); } }
      if (!out.betaOk) { out.beta = 1; out.corr = NaN; }
    }
    return out;
  }

  function niceStep(x) { var e = Math.pow(10, Math.floor(Math.log10(x))), m = x / e, best = 1, bd = 1e9; [1, 2, 2.5, 5, 10].forEach(function (c) { var d = Math.abs(Math.log(m / c)); if (d < bd) { bd = d; best = c; } }); return best * e; }
  function rungs(p, loF, hiF) { // step ≈ 1.25% of price rounded to a nice number (BTC → $1,000, HYPE → $1); range loF·p … hiF·p
    var step = niceStep(p * 0.0125), k0 = Math.round(loF * p / step), k1 = Math.round(hiF * p / step), out = []; for (var k = k0; k <= k1; k++) out.push(+(k * step).toPrecision(12)); return { step: step, list: out.filter(function (v) { return v > 0; }) }; }

  // ---------------------------------------------------------------- compute everything
  function compute(book) {
    var P = book.positions[0], S = book.positions[1] || null;
    var st0 = mkState(book);
    var R = { book: book, P: P, S: S, maint0: maintAt(st0, st0.mark), ntl0: book.ntl, buf0: 0 };
    R.buf0 = book.eq - R.maint0;
    R.stat = stats60(book, P.coin, S ? S.coin : null);
    R.beta = S ? R.stat.beta : null;
    // raw = the book as it stands (what the exchange quotes); eff = with every resting order executing on the way down ("as if the stops fire")
    R.rawLiqP = liqPrice(st0, P.coin, (function () { var m = {}; m[P.coin] = 1; return m; })());
    R.rawLiqS = S ? liqPrice(st0, S.coin, (function () { var m = {}; m[S.coin] = 1; return m; })()) : null;
    R.rawLiqJ = S ? liqPrice(st0, P.coin, (function () { var m = {}; m[P.coin] = 1; m[S.coin] = R.beta; return m; })()) : null;
    R.liqP = effLiq(book, P.coin, (function () { var m = {}; m[P.coin] = 1; return m; })());
    R.liqS = S ? effLiq(book, S.coin, (function () { var m = {}; m[S.coin] = 1; return m; })()) : null;
    R.liqJ = S ? effLiq(book, P.coin, (function () { var m = {}; m[P.coin] = 1; m[S.coin] = R.beta; return m; })()) : null;
    R.liqPtw = effLiq(book, P.coin, (function () { var m = {}; m[P.coin] = 1; return m; })(), { twap: 'path' });
    var fullP = effLiq(book, P.coin, (function () { var m = {}; m[P.coin] = 1; return m; })(), { full: true });
    R.eqAtTrigger = fullP.liq ? fullP.liqMaint : null; R.szAtTrigger = fullP.liq ? fullP.liqSz : null;
    R.comove = {}; if (S) [0, 1, 2, 3].concat([R.beta]).forEach(function (k) { var m = {}; m[P.coin] = 1; m[S.coin] = k; R.comove[k] = effLiq(book, P.coin, m); });
    // rungs
    R.rP = P.sz > 0 ? rungs(P.mark, 0.88, 1.38) : rungs(P.mark, 0.62, 1.12); R.rS = S ? (S.sz > 0 ? rungs(S.mark, 0.82, 1.29) : rungs(S.mark, 0.71, 1.18)) : null;
    function tg(c, v) { var t = {}; t[c] = v; return t; }
    R.A = R.rP.list.map(function (x) {
      var row = { x: x, pct: x / P.mark - 1, hold: holdAsIs(book, tg(P.coin, x)), ord: simulate(book, tg(P.coin, x)), none: simulate(book, tg(P.coin, x), { twap: 'none' }), first: simulate(book, tg(P.coin, x), { twap: 'first' }) };
      if (S) { var yb = S.mark * (1 + R.beta * (x / P.mark - 1)); var t2 = tg(P.coin, x); t2[S.coin] = yb; row.yBeta = yb; row.holdBeta = holdAsIs(book, t2); row.ordBeta = simulate(book, t2); }
      return row;
    });
    R.B = S ? R.rS.list.map(function (y) { return { y: y, pct: y / S.mark - 1, hold: holdAsIs(book, tg(S.coin, y)), ord: simulate(book, tg(S.coin, y)) }; }) : null;
    R.G = S ? R.rP.list.map(function (x) { return R.rS.list.map(function (y) { var t = tg(P.coin, x); t[S.coin] = y; return { x: x, y: y, hold: holdAsIs(book, t), ord: simulate(book, t, { steps: GRID_STEPS }) }; }); }) : null;
    // after the TWAPs
    var hasTwap = book.twaps.some(function (t) { return t.coin in st0.sz && t.sz - t.executed > 1e-9; });
    R.hasTwap = hasTwap;
    if (hasTwap) { var stA = afterTwaps(book), bA = bookAfterTwaps(book); R.after = { st: stA, eq: equityAt(stA, stA.mark), maint: maintAt(stA, stA.mark), ntl: 0, liqP: effLiq(bA, P.coin, (function () { var m = {}; m[P.coin] = 1; return m; })()) };
      for (var c in stA.sz) R.after.ntl += Math.abs(stA.sz[c]) * stA.mark[c];
      if (S) { R.after.liqS = effLiq(bA, S.coin, (function () { var m = {}; m[S.coin] = 1; return m; })()); R.after.liqJ = effLiq(bA, P.coin, (function () { var m = {}; m[P.coin] = 1; m[S.coin] = R.beta; return m; })()); } }
    // resting summary per coin
    R.rest = {};
    book.positions.forEach(function (p) {
      var o = book.orders.filter(function (x) { return x.coin === p.coin; }), longSide = p.sz > 0;
      var red = o.filter(function (x) { return !x.isTrigger && x.side === (longSide ? 'A' : 'B'); }), opn = o.filter(function (x) { return !x.isTrigger && x.side === (longSide ? 'B' : 'A'); }), trg = o.filter(function (x) { return x.isTrigger; });
      function agg(list, key) { var n = list.length, sz = 0, ntl = 0, lo = Infinity, hi = -Infinity; list.forEach(function (x) { var q = x.sz, pr = x[key]; sz += q; ntl += q * pr; if (pr < lo) lo = pr; if (pr > hi) hi = pr; }); return { n: n, sz: sz, avg: sz ? ntl / sz : 0, lo: n ? lo : 0, hi: n ? hi : 0 }; }
      var tw = book.twaps.filter(function (t) { return t.coin === p.coin; }).map(function (t) { return { side: t.side, rem: Math.max(0, t.sz - t.executed), sz: t.sz, executed: t.executed, avg: t.executed ? t.executedNtl / t.executed : 0, minutesLeft: Math.max(0, t.minutes - (book.t - t.timestamp) / 60000), reduceOnly: t.reduceOnly }; });
      R.rest[p.coin] = { tp: agg(red, 'px'), open: agg(opn, 'px'), stops: agg(trg.filter(function (x) { return x.trigDir === (longSide ? 'below' : 'above'); }), 'triggerPx'), tpTrig: agg(trg.filter(function (x) { return x.trigDir === (longSide ? 'above' : 'below'); }), 'triggerPx'), twaps: tw };
    });
    R.otherOrders = book.orders.filter(function (o) { return !(o.coin in st0.sz); });
    // exchange checks
    R.checks = book.positions.map(function (p) { var m = {}; m[p.coin] = 1; var lp = liqPrice(st0, p.coin, m); return { coin: p.coin, model: lp, exch: p.liqPxExch }; });
    R.hasStops = book.positions.some(function (p) { return book.orders.some(function (o) { return o.coin === p.coin && o.isTrigger; }); });
    R.im0 = imAt(st0, st0.mark, st0.sz);
    return R;
  }

  // ---------------------------------------------------------------- render
  function liqCell(o, coin, colspan) { return '<td class="col-num pm-neg" colspan="' + colspan + '"><strong>Liquidated</strong> at ' + pxf(o.liq[coin]) + '</td>'; }

  function render(R) {
    var book = R.book, P = R.P, S = R.S, EQ = book.eq, hasTwap = R.hasTwap;
    var isLong = P.sz > 0, A = isLong ? R.A : R.A.slice().reverse();   // A runs from the loss side to the profit side
    function rungNear(f) { var target = P.mark * f, best = A[0], bd = Infinity; A.forEach(function (r) { var d = Math.abs(r.x - target); if (d < bd) { bd = d; best = r; } }); return best; }
    var top = A[A.length - 1], near = rungNear(1), mid1 = rungNear(isLong ? 1.065 : 0.935), mid2 = rungNear(isLong ? 1.13 : 0.87);
    var lo1 = A[0], lo2 = A[1];
    var closeVerb = isLong ? 'sold' : 'bought back', favWord = isLong ? 'up' : 'down', advWord = isLong ? 'down' : 'up', stopVerb = isLong ? 'sell into a fall' : 'buy into a rally';
    var anyShort = book.positions.some(function (p) { return p.sz < 0; });
    var pName = P.coin, sName = S ? S.coin : null;
    var pSide = P.sz > 0 ? 'long' : 'short', sSide = S ? (S.sz > 0 ? 'long' : 'short') : '';
    var restP = R.rest[P.coin], restS = S ? R.rest[S.coin] : null;
    var twRemP = restP.twaps.reduce(function (s, t) { return s + t.rem; }, 0), twRemS = restS ? restS.twaps.reduce(function (s, t) { return s + t.rem; }, 0) : 0;
    var twMin = 0; book.twaps.forEach(function (t) { twMin = Math.max(twMin, t.minutes - (book.t - t.timestamp) / 60000); });

    // header stamp
    document.getElementById('last-updated').innerHTML = 'Live · read ' + utc(book.t) + ' (' + pt(book.t) + ') · account 0xD71a…95Bc: ' + usd(EQ) + ' equity, ' +
      book.positions.map(function (p) { return (p.sz > 0 ? 'long ' : 'short ') + szf(p.coin, Math.abs(p.sz)) + ' ' + p.coin; }).join(' + ') + ' at ' + (book.ntl / EQ).toFixed(1) + '× · liquidation with the stops firing ' + pxf(R.liqP) + ' (' + pName + ' alone)' + (S ? ' / ' + pxf(R.liqJ) + ' (' + sName + ' on beta)' : '') + ' · exchange quotes ' + pxf(R.rawLiqP) + ' for the book as it stands · re-read every ' + REFRESH_S + 's';
    document.getElementById('scen-title').textContent = 'Portfolio Scenarios — The Book From ' + pxf(R.rP.list[0]) + ' to ' + pxf(top.x) + ' on ' + pName + (S ? ', ' + pxf(R.rS.list[0]) + ' to ' + pxf(R.rS.list[R.rS.list.length - 1]) + ' on ' + sName : '');

    // inputs strip
    var inputs = '<span class="hy-input">Book · ' + book.positions.map(function (p) { return '<strong>' + (p.sz > 0 ? 'long ' : 'short ') + szf(p.coin, Math.abs(p.sz)) + ' ' + p.coin + '</strong> at ' + pxf(p.entry) + ' (' + p.levType + ' ' + p.lev + '×)'; }).join(' · ') + '</span>' +
      '<span class="hy-input">Equity · <strong>' + usd(EQ) + '</strong> · ' + usd(book.ntl) + ' notional · ' + (book.ntl / EQ).toFixed(1) + '× effective</span>' +
      '<span class="hy-input">Marks · ' + book.positions.map(function (p) { return '<strong>' + p.coin + ' ' + pxf(p.mark) + '</strong>'; }).join(' · ') + '</span>' +
      '<span class="hy-input">Liquidation, stops firing · <strong>' + pxf(R.liqP) + '</strong> ' + pName + ' alone' + (S ? ' · <strong>' + pxf(R.liqJ) + '</strong> if ' + sName + ' follows at β ' + R.beta.toFixed(2) : '') + ' · exchange quotes <strong>' + pxf(R.rawLiqP) + '</strong> if nothing executes</span>' +
      '<span class="hy-input">As of · <strong>' + utc(book.t) + '</strong></span>';
    document.getElementById('scen-inputs').innerHTML = inputs;

    // lede
    var restBits = [];
    if (restP.tp.n) restBits.push('the ' + szf(pName, restP.tp.sz) + '-' + pName + ' reduce-only ladder at ' + pxf(restP.tp.lo) + '–' + pxf(restP.tp.hi));
    if (restS && restS.tp.n) restBits.push('the ' + szf(sName, restS.tp.sz) + '-' + sName + ' ladder at ' + pxf(restS.tp.lo) + '–' + pxf(restS.tp.hi));
    var stopBits = book.positions.filter(function (p) { return R.rest[p.coin].stops.n; }).map(function (p) { var s = R.rest[p.coin].stops; return szf(p.coin, s.sz) + ' ' + p.coin + ' at ' + pxf(s.lo) + '–' + pxf(s.hi); });
    if (stopBits.length) restBits.push('the stops (' + stopBits.join(', ') + ')');
    if (book.positions.some(function (p) { return R.rest[p.coin].open.n; })) restBits.push('the scale-in bids');
    if (hasTwap) restBits.push('the remainder of the TWAPs (' + book.positions.filter(function (p) { return R.rest[p.coin].twaps.some(function (t) { return t.rem > 0; }); }).map(function (p) { return szf(p.coin, R.rest[p.coin].twaps.reduce(function (s, t) { return s + t.rem; }, 0)) + ' ' + p.coin; }).join(' and ') + ', ~' + Math.round(twMin / 60) + ' hours left)');
    document.getElementById('scen-lede').innerHTML = 'What the Hyperliquid book is worth if <strong>' + pName + '</strong> moves to each rung in ' + pxf(R.rP.step) + ' steps' + (S ? ', and the same for <strong>' + sName + '</strong> in ' + pxf(R.rS.step) + ' steps' : '') + ', re-read from the exchange every ' + REFRESH_S + ' seconds. Every rung is priced two ways. <strong>Hold as-is</strong> marks today’s ' +
      book.positions.map(function (p) { return szf(p.coin, Math.abs(p.sz)) + ' ' + p.coin; }).join(' and ') + ' at the scenario price with nothing executing. <strong>With orders</strong> lets everything resting in the account execute on a straight-line path from today’s marks to the rung' + (restBits.length ? ': ' + restBits.join(', ') : '') + '. The gap between the two columns is the price of the order book you have chosen' + (restP.tp.n ? ' — mostly the take-profit ladder, which caps the upside long before the top rung.' : '.');

    // findings
    var f = [];
    var ladderCostTop = top.hold.eq - top.none.eq, gapTop = top.hold.eq - top.ord.eq, twapGainTop = top.ord.eq - top.none.eq;
    var soldTop = top.ord.stats[pName].ladderSold, soldAvg = soldTop ? top.ord.stats[pName].ladderNtl / soldTop : 0;
    var heldTop = Math.abs(top.ord.sz[pName]), twTop = top.ord.twap[pName] ? top.ord.twap[pName].filled : 0;
    if (top.hold.liq || top.ord.liq) f.push('<li><strong>At ' + pxf(top.x) + '</strong>The far rung on the book’s own side is ' + (top.hold.liq ? 'a liquidation holding as-is (at ' + pxf(top.hold.liq[pName]) + ')' : 'worth ' + usd(top.hold.eq) + ' holding') + ' and ' + (top.ord.liq ? 'a liquidation with orders (at ' + pxf(top.ord.liq[pName]) + ')' : usd(top.ord.eq) + ' with orders') + ' — check the sign of the position and the resting book; this is not the shape the page expects.</li>');
    else f.push('<li><strong>At ' + pxf(top.x) + '</strong>Hold as-is is worth <em>' + usd(top.hold.eq) + '</em> (' + sgn(top.hold.pnl) + ', ' + pct(top.hold.pnl / EQ, 0) + ' on today’s equity)' + (S ? ' with ' + sName + ' flat' : '') + '. With your orders it is <em>' + usd(top.ord.eq) + '</em> (' + sgn(top.ord.pnl) + ')' +
      (soldTop ? ': the ladder has ' + closeVerb + ' ' + szf(pName, soldTop) + ' ' + pName + ' at an average ' + pxf(soldAvg) + ' and you arrive at ' + pxf(top.x) + ' holding ' + szf(pName, heldTop) + ' ' + pName + (twTop ? ' — the ' + szf(pName, Math.max(0, Math.abs(P.sz) - soldTop)) + ' the ladder leaves plus the TWAP’s ' + szf(pName, twTop) : '') + '.' : '.') +
      (hasTwap ? ' Depending on when the TWAP fills, the with-orders figure runs ' + (top.none.liq ? 'a liquidation' : kf(top.none.eq)) + '–' + (top.first.liq ? 'a liquidation' : kf(top.first.eq)) + ' (method block).' : '') + '</li>');
    if (restP.tp.n && !top.hold.liq && !top.ord.liq && !mid1.hold.liq && !mid2.hold.liq && !mid1.none.liq && !mid2.none.liq && !top.none.liq) f.push('<li><strong>The ladder’s price</strong>On its own the take-profit ladder costs ' + usd(mid1.hold.eq - mid1.none.eq) + ' at ' + pxf(mid1.x) + ', ' + usd(mid2.hold.eq - mid2.none.eq) + ' at ' + pxf(mid2.x) + ' and <em>' + usd(ladderCostTop) + '</em> at ' + pxf(top.x) + ' against holding' + (hasTwap ? '; the buy TWAP claws back ' + usd(twapGainTop) + ' of that at ' + pxf(top.x) + ', which is why the with-orders column ends ' + usd(gapTop) + ' behind hold-as-is rather than ' + usd(ladderCostTop) : '') + '. Each rung beyond ' + pxf(mid1.x) + ' adds ' + sgn(mid2.ord.eq - mid1.ord.eq) + ' with orders versus ' + sgn(mid2.hold.eq - mid1.hold.eq) + ' holding, because from there on you own ' + szf(pName, Math.abs(mid2.ord.sz[pName])) + ' ' + pName + ' instead of ' + szf(pName, Math.abs(P.sz)) + '.</li>');
    if (S) { var hb = top.holdBeta, ob = top.ordBeta; f.push('<li><strong>Both legs together</strong>If ' + sName + ' follows ' + pName + ' at its measured beta (' + R.beta.toFixed(2) + '× the percentage move, so ' + pxf(top.yBeta) + ' at ' + pName + ' ' + pxf(top.x) + '), hold as-is reaches <em>' + (hb.liq ? 'liquidation at ' + pxf(hb.liq[pName]) : usd(hb.eq)) + '</em> and with orders <em>' + (ob.liq ? 'liquidation at ' + pxf(ob.liq[pName]) : usd(ob.eq)) + '</em>' + ((!hb.liq && !ob.liq) ? ' — the ' + sName + ' ladder' + (restS.tp.n ? ' (' + szf(sName, restS.tp.sz) + ' resting to ' + pxf(restS.tp.hi) + ')' : '') + ' adds ' + usd((hb.eq - ob.eq) - gapTop) + ' of cap on top of the ' + pName + ' ladder’s' : '') + '.</li>'); }
    var eqT = R.eqAtTrigger; // equity left at the effective trigger = the maintenance margin of the (post-stops) book there
    if (eqT === null) (function () { var st = mkState(book); var px = {}; for (var c in st.mark) px[c] = st.mark[c]; if (R.rawLiqP) px[pName] = R.rawLiqP; eqT = maintAt(st, px); })();
    var downTxt;
    if (lo1.hold.liq && lo2.hold.liq) downTxt = pxf(lo2.x) + ' and ' + pxf(lo1.x) + ' are both liquidations holding as-is. With the stops firing on the way down, ' + pName + ' alone crosses maintenance at ' + pxf(R.liqP) + (S ? ', or ' + pxf(R.liqJ) + ' with ' + sName + ' moving on beta' : '') + ' (the exchange quotes ' + pxf(R.rawLiqP) + ' for the book as it stands, because a resting stop is not part of the position until it trades)' + (R.szAtTrigger ? '; by then the ' + pName + ' stops have cut the book to ' + Object.keys(R.szAtTrigger).map(function (c) { return szf(c, Math.abs(R.szAtTrigger[c])) + ' ' + c; }).join(' + ') + (S ? ' (' + sName + ' held flat in that case)' : '') : '') + '. At the trigger the account is down to its maintenance margin, about <em>' + usd(eqT) + '</em>; the exchange then closes the book by market in 20% chunks and returns what is left, and only a backstop liquidation (equity under two-thirds of maintenance, ≈' + usd(eqT * 2 / 3) + ') takes everything. So one rung down costs roughly ' + Math.round((1 - eqT / EQ) * 100) + '% of the account, not all of it' + (Math.abs(R.liqP - lo2.x) / lo2.x < 0.01 ? ' — and ' + pxf(lo2.x) + ' itself is a knife-edge, ' + usd(Math.abs(R.liqP - lo2.x)) + ' from the hold-as-is trigger' : '') + '.';
    else if (lo1.hold.liq) downTxt = pxf(lo2.x) + ' is survived holding (' + usd(lo2.hold.eq) + ', ' + sgn(lo2.hold.pnl) + ') but ' + pxf(lo1.x) + ' is a liquidation: ' + pName + ' alone crosses maintenance at ' + pxf(R.liqP) + (S ? ', or ' + pxf(R.liqJ) + ' with ' + sName + ' moving on beta' : '') + '. At the trigger the account is down to its maintenance margin, about <em>' + usd(eqT) + '</em>; the exchange closes the book by market in 20% chunks and returns what is left, and only a backstop liquidation (equity under two-thirds of maintenance) takes everything.';
    else downTxt = 'Neither rung against the book liquidates it holding as-is: ' + pxf(lo2.x) + ' leaves ' + usd(lo2.hold.eq) + ' and ' + pxf(lo1.x) + ' leaves ' + usd(lo1.hold.eq) + '; the ' + pName + '-alone trigger is ' + pxf(R.liqP) + (S ? ' (' + pxf(R.liqJ) + ' with ' + sName + ' on beta)' : '') + '.';
    if (restP.stops.n) downTxt += ' The stops (' + szf(pName, restP.stops.sz) + ' ' + pName + ' at ' + pxf(restP.stops.lo) + '–' + pxf(restP.stops.hi) + ')' + ((restP.open.n || twRemP) ? ' ' + stopVerb + ' and the ' + [restP.open.n ? 'bids' : null, twRemP ? 'TWAP' : null].filter(Boolean).join(' and ') + ' put part of it back on beyond them' : ' ' + stopVerb) + ' — with orders the two rungs against the book read ' + R.A.slice(0, 2).map(function (r) { return r.ord.liq ? 'liquidated at ' + pxf(r.ord.liq[pName]) : usd(r.ord.eq); }).join(' / ') + '.';
    f.push('<li><strong>The other side of ' + pxf(near.x) + '</strong>' + downTxt + '</li>');
    if (S) { var bTop = R.B[R.B.length - 1], bLo = R.B[0]; var sSold = bTop.ord.stats[sName].ladderSold, sAvg = sSold ? bTop.ord.stats[sName].ladderNtl / sSold : 0;
      f.push('<li><strong>' + sName + ' on its own</strong>With ' + pName + ' flat, ' + sName + ' at ' + pxf(bTop.y) + ' (' + pct(bTop.pct, 0) + ') is ' + usd(bTop.hold.eq) + ' holding and ' + usd(bTop.ord.eq) + ' with orders' + (sSold ? ' — the ladder sells ' + szf(sName, sSold) + ' at an average ' + pxf(sAvg) + ' and you keep ' + szf(sName, Math.abs(bTop.ord.sz[sName])) : '') + '. ' + sName + ' at ' + pxf(bLo.y) + ' (' + pct(bLo.pct, 0) + ') with ' + pName + ' flat is ' + (bLo.hold.liq ? 'a liquidation at ' + pxf(bLo.hold.liq[sName]) : usd(bLo.hold.eq) + ' holding today’s book — ' + (bLo.hold.eq - bLo.hold.maint < 0.15 * EQ ? 'survivable, but only ' + usd(bLo.hold.eq - bLo.hold.maint) + ' above maintenance' : 'survivable') + '; the ' + sName + '-alone trigger with the stops firing is ' + (R.liqS === null ? 'none — the ' + sName + ' stops flatten the leg before it can take the account down' : pxf(R.liqS))) + (hasTwap && R.after.liqS ? ', and once the TWAPs finish it is ' + pxf(R.after.liqS) : (hasTwap ? ', and once the TWAPs finish it is still none' : '')) + '.</li>'); }
    if (hasTwap) { f.push('<li><strong>The TWAPs</strong>' + book.positions.filter(function (p) { return R.rest[p.coin].twaps.some(function (t) { return t.rem > 0; }); }).map(function (p) { return R.rest[p.coin].twaps.filter(function (t) { return t.rem > 0; }).map(function (t) { return (t.side === 'B' ? 'a buy' : 'a sell') + ' TWAP with ' + szf(p.coin, t.rem) + ' ' + p.coin + ' left (' + Math.round(t.minutesLeft / 60) + ' h)'; }).join(', '); }).join(' and ') + ', executing regardless of price. On the way ' + favWord + ' they ' + (twapGainTop >= 0 ? 'help' : 'hurt') + ': cancelling them turns ' + pxf(top.x) + ' from ' + (top.ord.liq ? 'a liquidation' : usd(top.ord.eq)) + ' into ' + (top.none.liq ? 'a liquidation' : usd(top.none.eq)) + ' on the page’s path assumption, and had they already filled near today’s price ' + pxf(top.x) + ' would be worth ' + (top.first.liq ? 'a liquidation' : usd(top.first.eq)) + '. On the way ' + advWord + ' they add into the liquidation until initial margin runs out. If prices simply sit still until they finish, the book is ' + Object.keys(R.after.st.sz).map(function (c) { return szf(c, Math.abs(R.after.st.sz[c])) + ' ' + c; }).join(' + ') + ' at ' + (R.after.ntl / R.after.eq).toFixed(1) + '× with triggers ' + pxf(R.after.liqP) + ' (' + pName + ' alone)' + (S ? ', ' + pxf(R.after.liqJ) + ' (on beta) and ' + pxf(R.after.liqS) + ' (' + sName + ' alone)' : '') + ((R.after.liqP != null && R.liqP != null) ? ' — the account’s own instructions move the ' + pName + ' trigger by ' + sgn(R.after.liqP - R.liqP) : '') + '.</li>'); }
    else if (restP.stops.n) { f.push('<li><strong>The stops</strong>' + szf(pName, restP.stops.sz) + ' ' + pName + ' of stop-markets at ' + pxf(restP.stops.lo) + '–' + pxf(restP.stops.hi) + ' (' + pct((restP.stops.hi / P.mark - 1), 1) + ' to ' + pct((restP.stops.lo / P.mark - 1), 1) + ' from the mark)' + (restS && restS.stops.n ? ' and ' + szf(sName, restS.stops.sz) + ' ' + sName + ' at ' + pxf(restS.stops.lo) + '–' + pxf(restS.stops.hi) : '') + '. They ' + stopVerb + ' and re-expose nothing on a reversal; the with-orders column on the rungs against the book shows what they leave.</li>'); }
    document.getElementById('scen-findings').innerHTML = f.join('\n');

    // KPIs
    var k = [];
    k.push(['cyan', 'Equity · notional · leverage', usd(EQ) + ' · ' + usd(book.ntl / 1000) + 'k · ' + (book.ntl / EQ).toFixed(1) + '×']);
    k.push(['cyan', pName + ' leg · entry · open P&amp;L', szf(pName, Math.abs(P.sz)) + ' · ' + pxf(P.entry) + ' · ' + sgn(P.uPnl)]);
    if (S) k.push(['cyan', sName + ' leg · entry · open P&amp;L', szf(sName, Math.abs(S.sz)) + ' · ' + pxf(S.entry) + ' · ' + sgn(S.uPnl)]); else k.push(['cyan', 'Funding · last 24h (− = paid)', sgn(book.fund24)]);
    k.push(['peach', 'Liq, stops firing · ' + pName + ' alone' + (S ? ' · on beta · ' + sName + ' alone' : ''), pxf(R.liqP) + (S ? ' · ' + pxf(R.liqJ) + ' · ' + (R.liqS === null ? 'none' : pxf(R.liqS)) : '')]);
    k.push(['peach', 'Exchange quote, nothing executes · ' + pName + (S ? ' · ' + sName : ''), pxf(R.rawLiqP) + (S ? ' · ' + pxf(R.rawLiqS) : '')]);
    k.push(['slate', 'Reduce-only ladders resting', book.positions.map(function (p) { var t = R.rest[p.coin].tp; return t.n ? szf(p.coin, t.sz) + ' ' + p.coin : null; }).filter(Boolean).join(' · ') || 'none']);
    k.push(['slate', 'Stops · TWAP left (' + book.positions.map(function (p) { return p.coin; }).join(' · ') + ')', book.positions.map(function (p) { return szf(p.coin, R.rest[p.coin].stops.sz); }).join(' · ') + ' · ' + book.positions.map(function (p) { return szf(p.coin, R.rest[p.coin].twaps.reduce(function (s, t) { return s + t.rem; }, 0)); }).join(' · ')]);
    k.push(['teal', pxf(top.x) + ' · hold · with orders · gap', kf(top.hold.eq) + ' · ' + kf(top.ord.eq) + ' · ' + kf(gapTop)]);
    document.getElementById('scen-kpis').innerHTML = k.map(function (x) { return '<div class="kpi-card" data-accent="' + x[0] + '"><div class="kpi-label">' + x[1] + '</div><div class="kpi-value">' + x[2] + '</div></div>'; }).join('\n');

    // Table A
    document.getElementById('scen-a-title').textContent = pName + ' in ' + pxf(R.rP.step) + ' Steps — Hold As-Is vs With Orders' + (S ? ' (' + sName + ' flat at ' + pxf(S.mark) + '), Plus ' + sName + ' on Beta' : '');
    document.getElementById('scen-a-note').innerHTML = 'Hold as-is: today’s positions marked at the rung. With orders: the resting ladders, stops, bids and the TWAP remainder execute on a straight path from ' + pxf(P.mark) + ' to the rung; “Sold” is what the ladder and stops sell and the average price; “TWAP adds” is what the TWAP fills and its average price. ROE is P&amp;L on today’s ' + usd(EQ) + '.' + (S ? ' The last three columns repeat the exercise with ' + sName + ' moving ' + R.beta.toFixed(2) + '× ' + pName + '’s percentage move.' : '') + (hasTwap ? ' On liquidated rungs the with-orders trigger differs from hold-as-is because the stops sell and the bids and TWAP buy on the way down; the TWAP is tied to the path, so a longer path has bought less of it by any given level.' : '');
    var rowsA = R.A.map(function (r) {
      var h = r.hold, o = r.ord, s = o.stats[pName], sold = s.sold, soldAvg = sold ? s.soldNtl / sold : 0, tw = o.twap[pName] ? o.twap[pName].filled : 0, twAvg = tw ? o.twap[pName].ntl / tw : 0;
      var html = '<tr><td class="pm-co"><strong>' + pxf(r.x) + '</strong></td><td class="col-num ' + cls(r.pct) + '">' + pct(r.pct) + '</td>';
      html += h.liq ? liqCell(h, pName, 3) : '<td class="col-num"><strong>' + usd(h.eq) + '</strong></td><td class="col-num ' + cls(h.pnl) + '">' + sgn(h.pnl) + '</td><td class="col-num ' + cls(h.pnl) + '">' + pct(h.pnl / EQ, 0) + '</td>';
      if (o.liq) html += liqCell((r.none && r.none.liq) ? r.none : o, pName, 5) + '<td class="col-num">—</td>';
      else html += '<td class="col-num">' + szf(pName, Math.abs(o.sz[pName])) + '</td><td class="col-num">' + (sold ? szf(pName, sold) + ' @ ' + pxf(soldAvg) : 'none') + '</td><td class="col-num">' + (tw ? szf(pName, tw) + ' @ ' + pxf(twAvg) : (hasTwap ? '0' : '—')) + '</td><td class="col-num"><strong>' + usd(o.eq) + '</strong></td><td class="col-num ' + cls(o.pnl) + '">' + sgn(o.pnl) + '</td><td class="col-num ' + cls(o.eq - h.eq) + '">' + sgn(o.eq - h.eq) + '</td>';
      if (S) html += '<td class="col-num">' + pxf(r.yBeta) + '</td><td class="col-num">' + (r.holdBeta.liq ? '<span class="pm-neg">liq ' + pxf(r.holdBeta.liq[pName]) + '</span>' : usd(r.holdBeta.eq)) + '</td><td class="col-num">' + (r.ordBeta.liq ? '<span class="pm-neg">liq ' + pxf(r.ordBeta.liq[pName]) + '</span>' : usd(r.ordBeta.eq)) + '</td>';
      return html + '</tr>';
    });
    document.getElementById('scen-a-wrap').innerHTML = '<table class="pm-table hy-table hy-scen"><thead><tr><th rowspan="2">' + pName + '</th><th rowspan="2" class="col-num">Move</th><th colspan="3" class="hy-grp">Hold as-is</th><th colspan="5" class="hy-grp">With orders</th><th rowspan="2" class="col-num">Orders vs hold</th>' + (S ? '<th colspan="3" class="hy-grp">' + sName + ' on beta</th>' : '') + '</tr><tr><th class="col-num">Equity</th><th class="col-num">P&amp;L</th><th class="col-num">ROE</th><th class="col-num">' + pName + ' held</th><th class="col-num">' + (isLong ? 'Sold' : 'Closed') + ' @ avg</th><th class="col-num">TWAP adds @ avg</th><th class="col-num">Equity</th><th class="col-num">P&amp;L</th>' + (S ? '<th class="col-num">' + sName + '</th><th class="col-num">Hold</th><th class="col-num">With orders</th>' : '') + '</tr></thead><tbody>' + rowsA.join('\n') + '</tbody></table>';

    // Table B
    var secB = document.getElementById('scen-sec-b');
    if (S) {
      secB.hidden = false;
      document.getElementById('scen-b-title').textContent = sName + ' in ' + pxf(R.rS.step) + ' Steps — Hold As-Is vs With Orders (' + pName + ' flat at ' + pxf(P.mark) + ')';
      document.getElementById('scen-b-note').innerHTML = 'Same construction. ' + (restS.tp.n ? 'The ' + sName + ' ladder is ' + restS.tp.n + ' reduce-only orders for ' + szf(sName, restS.tp.sz) + ' from ' + pxf(restS.tp.lo) + ' to ' + pxf(restS.tp.hi) + ' (average ' + pxf(restS.tp.avg) + ')' : 'No reduce-only ladder is resting on ' + sName) + (restS.stops.n ? '; the stops sell ' + szf(sName, restS.stops.sz) + ' at ' + pxf(restS.stops.lo) + '–' + pxf(restS.stops.hi) : '') + (restS.open.n ? '; the bids buy ' + szf(sName, restS.open.sz) + ' at ' + pxf(restS.open.lo) + '–' + pxf(restS.open.hi) : '') + '. ' + sName + ' is ' + Math.round(Math.abs(S.sz * S.mark) / book.ntl * 100) + '% of the book’s notional, so a ' + sName + ' move with ' + pName + ' flat is survivable to ' + pxf(R.liqS) + ' on today’s book' + (hasTwap && R.after.liqS ? '; once the TWAPs have finished, that trigger is ' + pxf(R.after.liqS) : '') + '.';
      var rowsB = R.B.map(function (r) {
        var h = r.hold, o = r.ord, s = o.stats[sName], sold = s.sold, soldAvg = sold ? s.soldNtl / sold : 0, tw = o.twap[sName] ? o.twap[sName].filled : 0, twAvg = tw ? o.twap[sName].ntl / tw : 0;
        var html = '<tr><td class="pm-co"><strong>' + pxf(r.y) + '</strong></td><td class="col-num ' + cls(r.pct) + '">' + pct(r.pct) + '</td>';
        html += h.liq ? liqCell(h, sName, 3) : '<td class="col-num"><strong>' + usd(h.eq) + '</strong></td><td class="col-num ' + cls(h.pnl) + '">' + sgn(h.pnl) + '</td><td class="col-num ' + cls(h.pnl) + '">' + pct(h.pnl / EQ, 0) + '</td>';
        if (o.liq) html += liqCell(o, sName, 5) + '<td class="col-num">—</td>';
        else html += '<td class="col-num">' + szf(sName, Math.abs(o.sz[sName])) + '</td><td class="col-num">' + (sold ? szf(sName, sold) + ' @ ' + pxf(soldAvg) : 'none') + '</td><td class="col-num">' + (tw ? szf(sName, tw) + ' @ ' + pxf(twAvg) : (hasTwap ? '0' : '—')) + '</td><td class="col-num"><strong>' + usd(o.eq) + '</strong></td><td class="col-num ' + cls(o.pnl) + '">' + sgn(o.pnl) + '</td><td class="col-num ' + cls(o.eq - h.eq) + '">' + sgn(o.eq - h.eq) + '</td>';
        return html + '</tr>';
      });
      document.getElementById('scen-b-wrap').innerHTML = '<table class="pm-table hy-table hy-scen"><thead><tr><th rowspan="2">' + sName + '</th><th rowspan="2" class="col-num">Move</th><th colspan="3" class="hy-grp">Hold as-is</th><th colspan="5" class="hy-grp">With orders</th><th rowspan="2" class="col-num">Orders vs hold</th></tr><tr><th class="col-num">Equity</th><th class="col-num">P&amp;L</th><th class="col-num">ROE</th><th class="col-num">' + sName + ' held</th><th class="col-num">' + (S.sz > 0 ? 'Sold' : 'Closed') + ' @ avg</th><th class="col-num">TWAP adds @ avg</th><th class="col-num">Equity</th><th class="col-num">P&amp;L</th></tr></thead><tbody>' + rowsB.join('\n') + '</tbody></table>';
    } else secB.hidden = true;

    // Grid
    var secG = document.getElementById('scen-sec-grid');
    if (S) {
      secG.hidden = false;
      document.getElementById('scen-grid-title').textContent = 'Both Legs — Equity With Orders, ' + pName + ' Down the Side in ' + pxf(R.rP.step) + ' Steps, ' + sName + ' Across in ' + pxf(R.rS.step) + ' Steps';
      var betaCol = {}; R.A.forEach(function (r) { var nearest = null, bd = Infinity; R.rS.list.forEach(function (c) { var d = Math.abs(c - r.yBeta); if (d < bd) { bd = d; nearest = c; } }); if (bd <= 0.7 * R.rS.step) betaCol[r.x] = nearest; });
      var offRows = R.A.filter(function (r) { return betaCol[r.x] === undefined; });
      var offGrid = offRows.length ? [offRows.length + ' row' + (offRows.length === 1 ? '' : 's') + ' (' + pName + ' ' + pxf(offRows[0].x) + (offRows.length > 1 ? '–' + pxf(offRows[offRows.length - 1].x) : '') + ') have their beta-consistent ' + sName + ' beyond the grid’s edge'] : [];
      document.getElementById('scen-grid-note').innerHTML = 'Each cell: equity with orders on a straight path to that ' + pName + '/' + sName + ' pair, in thousands; hover a cell for the exact figure and the hold-as-is equity. LIQ = the path crosses maintenance margin before arriving. Outlined cells sit closest to the beta-consistent pair (' + sName + ' moving ' + R.beta.toFixed(2) + '× ' + pName + ')' + (offGrid.length ? '; off the grid: ' + offGrid.join(', ') : '') + '. ' + R.G.length + ' × ' + R.G[0].length + ' = ' + (R.G.length * R.G[0].length).toLocaleString('en-US') + ' scenarios, each a full path simulation; the table scrolls sideways. An isolated LIQ next to survivors is real, not noise: a rung that stops just short of a stop’s trigger keeps that leg’s full maintenance, while its neighbour fires the stop.';
      var gh = '<tr><th class="hy-grid-corner">' + pName + ' ↓ · ' + sName + ' →</th>' + R.rS.list.map(function (y) { return '<th>' + pxf(y) + '</th>'; }).join('') + '</tr>';
      var gr = R.G.map(function (row) { return '<tr><th class="hy-grid-row">' + pxf(row[0].x) + '</th>' + row.map(function (c) { var o = c.ord, h = c.hold, mark = betaCol[c.x] === c.y ? ' hy-beta' : ''; var tip = pName + ' ' + pxf(c.x) + ' · ' + sName + ' ' + pxf(c.y) + ' — with orders ' + (o.liq ? 'liquidated at ' + pName + ' ' + pxf(o.liq[pName]) : usd(o.eq) + ' (' + sgn(o.pnl) + ')') + ' · hold as-is ' + (h.liq ? 'liquidated' : usd(h.eq) + ' (' + sgn(h.pnl) + ')'); if (o.liq) return '<td class="hy-liq' + mark + '" title="' + esc(tip) + '"><span class="hy-cell-o">LIQ</span></td>'; return '<td class="' + (o.pnl > 0 ? 'hy-up' : 'hy-dn') + mark + '" title="' + esc(tip) + '"><span class="hy-cell-o">' + kf(o.eq) + '</span></td>'; }).join('') + '</tr>'; });
      document.getElementById('scen-grid-wrap').innerHTML = '<table class="pm-table hy-table hy-grid hy-grid-dense"><thead>' + gh + '</thead><tbody>' + gr.join('\n') + '</tbody></table>';
    } else secG.hidden = true;

    // Resting orders table
    var orows = [];
    book.positions.forEach(function (p) {
      var r = R.rest[p.coin], long = p.sz > 0;
      if (r.tp.n) orows.push([p.coin, 'Closing ' + (long ? 'sells above' : 'buys below') + ' (take-profit ladder)', r.tp.n, szf(p.coin, r.tp.sz), pxf(r.tp.lo) + '–' + pxf(r.tp.hi), pxf(r.tp.avg), 'Fill at limit as the path reaches each order (maker fee)']);
      if (r.stops.n) orows.push([p.coin, 'Stop-markets (' + (long ? 'sell, trigger below' : 'buy, trigger above') + ')', r.stops.n, szf(p.coin, r.stops.sz), pxf(r.stops.lo) + '–' + pxf(r.stops.hi), pxf(r.stops.avg), 'Fill at trigger less ' + (slipOf(p.coin) * 100).toFixed(2) + '% slip (taker fee)']);
      if (r.tpTrig.n) orows.push([p.coin, 'Take-profit triggers', r.tpTrig.n, szf(p.coin, r.tpTrig.sz), pxf(r.tpTrig.lo) + '–' + pxf(r.tpTrig.hi), pxf(r.tpTrig.avg), 'Fill at trigger (taker fee)']);
      if (r.open.n) orows.push([p.coin, 'Opening ' + (long ? 'bids below' : 'offers above') + ' (scale-in)', r.open.n, szf(p.coin, r.open.sz), pxf(r.open.lo) + '–' + pxf(r.open.hi), pxf(r.open.avg), 'Fill at limit if initial margin allows (maker fee)']);
      r.twaps.forEach(function (t) { orows.push([p.coin, (t.side === 'B' ? 'Buy' : 'Sell') + ' TWAP' + (t.reduceOnly ? ' (reduce-only)' : ''), 1, szf(p.coin, t.rem) + ' of ' + szf(p.coin, t.sz) + ' left', t.executed ? szf(p.coin, t.executed) + ' done @ ' + pxf(t.avg) : 'nothing done yet', Math.round(t.minutesLeft / 60) + ' h left', 'Remainder spread along the path (taker fee); sensitivities in the method block']); });
    });
    if (R.otherOrders.length) orows.push(['other', 'Orders on coins with no position (ignored)', R.otherOrders.length, '—', '—', '—', 'Would open new positions; not modelled']);
    document.getElementById('scen-orders-note').textContent = book.orders.length + ' open orders and ' + book.twaps.length + ' TWAP' + (book.twaps.length === 1 ? '' : 's') + ' on the account at ' + utc(book.t) + '. Funding in the last 24 h: ' + (book.fund24 < 0 ? usd(-book.fund24) + ' paid' : usd(book.fund24) + ' received') + '.';
    document.getElementById('scen-orders-wrap').innerHTML = orows.length ? '<table class="pm-table hy-table hy-scen"><thead><tr><th>Coin</th><th>Instruction</th><th class="col-num">Orders</th><th class="col-num">Size</th><th class="col-num">Range</th><th class="col-num">Average</th><th>How the model executes it</th></tr></thead><tbody>' + orows.map(function (r) { return '<tr><td class="pm-co"><strong>' + esc(r[0]) + '</strong></td><td>' + esc(r[1]) + '</td><td class="col-num">' + r[2] + '</td><td class="col-num">' + esc(r[3]) + '</td><td class="col-num">' + esc(r[4]) + '</td><td class="col-num">' + esc(r[5]) + '</td><td>' + esc(r[6]) + '</td></tr>'; }).join('\n') + '</tbody></table>' : '<div class="hy-loading">No resting orders or TWAPs — “with orders” equals “hold as-is”.</div>';

    // Method
    var checks = R.checks.map(function (c) { if (!c.exch || !c.model) return c.coin + ': exchange gives no liquidation price'; var d = Math.abs(c.model - c.exch); var ok = d / c.exch < 0.0005; return c.coin + ' ' + pxf(c.model) + ' vs ' + pxf(c.exch) + ' <span class="' + (ok ? 'ok' : 'bad') + '">' + (ok ? '✓' : '✗ off by ' + pxf(d)) + '</span>'; });
    var mmOk = Math.abs(R.maint0 - book.mmExch) / book.mmExch < 0.002;
    var sensRows = [3, 4, 5, 6].filter(function (i) { return R.A[i]; }).map(function (i) { var r = R.A[i]; return '<tr><td class="pm-co"><strong>' + pxf(r.x) + '</strong></td><td class="col-num">' + (r.none.liq ? 'liq ' + pxf(r.none.liq[pName]) : usd(r.none.eq)) + '</td><td class="col-num"><strong>' + (r.ord.liq ? 'liq ' + pxf(r.ord.liq[pName]) : usd(r.ord.eq)) + '</strong></td><td class="col-num">' + (r.first.liq ? 'liq ' + pxf(r.first.liq[pName]) : usd(r.first.eq)) + '</td></tr>'; });
    var down = R.A.slice(0, 2).map(function (r) { return '<tr><td class="pm-co"><strong>' + pxf(r.x) + '</strong></td><td class="col-num">' + (r.none.liq ? 'liq ' + pxf(r.none.liq[pName]) : usd(r.none.eq)) + '</td><td class="col-num"><strong>' + (r.ord.liq ? 'liq ' + pxf(r.ord.liq[pName]) : usd(r.ord.eq)) + '</strong></td><td class="col-num">' + (r.first.liq ? 'liq ' + pxf(r.first.liq[pName]) : usd(r.first.eq)) + '</td></tr>'; });
    var m = [];
    m.push('<div class="pm-method-block"><span class="pm-method-h">The book, as read</span><p>webData2 (positions, marks, margin tiers, open orders with triggers, TWAP states), userFunding and two 60-day candle series for 0xD71a…95Bc, fetched from api.hyperliquid.xyz in this browser at ' + utc(book.t) + ' and re-read every ' + REFRESH_S + ' seconds. ' + book.positions.map(function (p) { return (p.sz > 0 ? 'Long ' : 'Short ') + szf(p.coin, Math.abs(p.sz)) + ' ' + p.coin + ' at ' + pxf(p.entry) + ' (' + p.levType + ' ' + p.lev + '×, max ' + p.maxLev + '×)'; }).join('; ') + '; equity ' + usd(EQ, 2) + '; maintenance ' + usd(R.maint0) + ' — half the initial margin at each asset’s maximum leverage, cumulative across the exchange’s margin tiers. <strong>Every liquidation price on this page is the effective one — the price at which the book crosses maintenance on a straight path against it with every resting order executing on the way (stops, scale-in bids, ladders); the TWAP remainder is excluded because it depends on time, and with it filling along the path the ' + pName + '-alone figure is ' + pxf(R.liqPtw) + '.</strong> The exchange’s own liquidationPx assumes nothing executes; it is shown as the quote for the book as it stands and used for the check below.</p><div class="hy-check">Exchange check, this read — the model’s liquidation for the book as it stands vs the exchange’s liquidationPx: ' + checks.join('; ') + '. Model maintenance ' + usd(R.maint0) + ' vs exchange ' + usd(book.mmExch) + ' <span class="' + (mmOk ? 'ok' : 'bad') + '">' + (mmOk ? '✓' : '✗') + '</span>; initial margin at the account’s leverage settings ' + usd(R.im0) + ' vs exchange margin used ' + usd(book.muExch) + ' <span class="' + (Math.abs(R.im0 - book.muExch) / Math.max(1, book.muExch) < 0.002 ? 'ok' : 'bad') + '">' + (Math.abs(R.im0 - book.muExch) / Math.max(1, book.muExch) < 0.002 ? '✓' : '✗') + '</span>.' + (anyShort ? ' A short leg is open: its rungs run in the book’s favour downward and closes read “bought back”.' : '') + '</div></div>');
    m.push('<div class="pm-method-block"><span class="pm-method-h">Hold as-is</span><p>Equity at a rung = today’s equity + Σ size × (rung − mark) over the positions that move; the others stay at today’s mark. The rung is marked liquidated if equity falls below maintenance anywhere on the straight path from today’s marks to the rung; the crossing is found by bisection. ROE is the P&amp;L divided by today’s equity.</p></div>');
    m.push('<div class="pm-method-block"><span class="pm-method-h">With orders</span><p>The path is walked in ' + STEPS + ' steps. Every open order on a held coin is carried individually: a resting limit fills at its limit price when the path reaches it (maker fee ' + (MAKER * 100).toFixed(3) + '%); a trigger order fills at its trigger price less ' + (slipOf(P.coin) * 100).toFixed(2) + '% (' + P.coin + ') / 0.10% (others) of slippage when the path crosses the trigger in the stated direction (taker fee ' + (TAKER * 100).toFixed(3) + '%); reduce-only orders never exceed the position and are skipped once it is flat; an opening order or TWAP slice that would exceed initial margin at the account’s leverage settings is skipped, as the exchange would skip it. The remainder of each TWAP is spread evenly along the path, so it fills at the average of today’s price and the rung, and a longer path has bought less of it by any given level. Funding is not charged (the book ' + (book.fund24 < 0 ? 'paid ' + usd(-book.fund24) : 'received ' + usd(book.fund24)) + ' in the last 24 hours). Fee tiers are assumed, not read: the base schedule would lower every with-orders figure by a few tens of dollars.</p></div>');
    if (hasTwap) m.push('<div class="pm-method-block"><span class="pm-method-h">TWAP timing — the biggest single assumption</span><p>The tables use the middle of three cases. Cancelled: the TWAPs stop now. Path (the tables): the remainder fills evenly on the way to the rung. First: it finishes near today’s price before the move — the likelier case for a large move, since the TWAPs end in about ' + Math.round(twMin / 60) + ' hours. With ' + (S ? sName + ' flat' : 'nothing else moving') + ':</p><table class="pm-table hy-table hy-sens"><thead><tr><th>' + pName + '</th><th class="col-num">TWAPs cancelled</th><th class="col-num">Path (tables)</th><th class="col-num">TWAPs first</th></tr></thead><tbody>' + sensRows.join('') + down.join('') + '</tbody></table><p>Today’s liquidation prices expire with the TWAPs: at unchanged prices the finished book is ' + Object.keys(R.after.st.sz).map(function (c) { return szf(c, Math.abs(R.after.st.sz[c])) + ' ' + c; }).join(' + ') + ' (' + usd(R.after.ntl / 1000) + 'k, ' + (R.after.ntl / R.after.eq).toFixed(1) + '×) with triggers ' + pxf(R.after.liqP) + ' (' + pName + ' alone)' + (S ? ' / ' + pxf(R.after.liqJ) + ' (on beta) / ' + pxf(R.after.liqS) + ' (' + sName + ' alone)' : '') + '.</p></div>');
    if (S && !R.stat.betaOk) m.push('<div class="pm-method-block"><span class="pm-method-h">' + sName + ' on beta</span><p>Fewer than ten aligned daily candles for ' + pName + ' and ' + sName + ', so no beta could be measured; “' + sName + ' on beta” assumes 1.0× ' + pName + '’s percentage move.</p></div>');
    else if (S) m.push('<div class="pm-method-block"><span class="pm-method-h">' + sName + ' on beta</span><p>Ordinary least squares of ' + sName + '’s daily log return on ' + pName + '’s over the last ' + R.stat.n + ' days gives β ' + R.beta.toFixed(2) + ' with correlation ' + R.stat.corr.toFixed(2) + ' — an R² of ' + (R.stat.corr * R.stat.corr).toFixed(2) + ', so the beta line explains ' + (R.stat.corr * R.stat.corr < 0.5 ? 'less than half' : 'about ' + Math.round(R.stat.corr * R.stat.corr * 100) + '%') + ' of ' + sName + '’s daily variance. “' + sName + ' on beta” moves ' + sName + ' by ' + R.beta.toFixed(2) + '× ' + pName + '’s simple percentage move. Daily realised volatility (30 d): ' + pName + ' ' + (R.stat.sdA30 * 100).toFixed(1) + '%, ' + sName + ' ' + (R.stat.sdB30 * 100).toFixed(1) + '%. The joint trigger depends on the co-move actually realised: ' + [0, 1, R.beta, 2, 3].map(function (kk) { var v = R.comove[kk]; return (v ? pxf(v) : '—') + ' at ' + (kk === R.beta ? 'the measured beta' : kk + '×'); }).join(', ') + '.</p></div>');
    m.push('<div class="pm-method-block"><span class="pm-method-h">What is not modelled</span><p>Liquidation is treated as the end of the scenario, not as a cash flow: on Hyperliquid a cross account that crosses maintenance is closed by market orders (20% of the position at a time above $100k of notional), any collateral left after the closes stays with the trader, and only a backstop liquidation — equity under two-thirds of maintenance without a successful close on the book — forfeits the lot, so a liquidated rung is worth somewhere between nothing and the ≈' + usd(eqT) + ' of maintenance margin the account holds at the trigger. The path is a straight line; a round trip that touches the stops and then rallies would leave the book smaller on the way up than the table shows' + (restP.stops.n ? ' (the ' + pName + ' stops sit ' + pct(restP.stops.hi / P.mark - 1, 1) + ' to ' + pct(restP.stops.lo / P.mark - 1, 1) + ' from the mark' + (restS && restS.stops.n ? ', the ' + sName + ' stops ' + pct(restS.stops.hi / S.mark - 1, 1) + ' to ' + pct(restS.stops.lo / S.mark - 1, 1) : '') + ')' : '') + '. Orders on coins the account does not hold are ignored. Funding is left out and its horizon matters: at the last-24h rate a week costs about ' + usd(Math.abs(book.fund24) * 7) + ' and a month about ' + usd(Math.abs(book.fund24) * 30) + '. Nothing here is a forecast of where ' + pName + (S ? ' or ' + sName : '') + ' goes — the rungs are the question, priced. Read-only: this page cannot place, cancel or modify orders.</p></div>');
    document.getElementById('scen-method').innerHTML = m.join('\n');
  }

  // ---------------------------------------------------------------- driver
  var busy = false, lastOk = null, lastAttempt = 0, nextDue = 0, failures = 0, lastStatus = '';
  var dot = document.getElementById('scen-dot'), statusText = document.getElementById('scen-status-text'), btn = document.getElementById('scen-refresh'), cd = document.getElementById('scen-countdown'), errBox = document.getElementById('scen-error');

  function setStatus(kind, text) { dot.className = 'dot ' + kind; statusText.textContent = text; lastStatus = text; }
  function ago(ms) { var sec = Math.max(0, Math.round((Date.now() - ms) / 1000)); return sec < 90 ? sec + ' s ago' : Math.round(sec / 60) + ' min ago'; }

  function refresh() {
    if (busy) return; busy = true; btn.disabled = true; lastAttempt = Date.now();
    setStatus(lastOk ? 'ok' : 'busy', (lastOk ? lastStatus.replace(/ · reading…$/, '') + ' · reading…' : 'Reading the account from the Hyperliquid info API…'));
    withRetry(load, 3, 2000).then(function (book) {
      if (!book.positions.length) { errBox.hidden = true; failures = 0; lastOk = book.t; setStatus('ok', 'Read ' + utc(book.t) + ' — the account has no open perp positions (equity ' + usd(book.eq) + '). Nothing to scenario.'); document.getElementById('last-updated').textContent = 'Live · ' + utc(book.t) + ' · no open positions · equity ' + usd(book.eq); busy = false; btn.disabled = false; nextDue = Date.now() + REFRESH_S * 1000; return; }
      var R = compute(book);
      render(R);
      errBox.hidden = true; lastOk = book.t; failures = 0;
      setStatus('ok', 'Live · last read ' + utc(book.t).replace(' UTC', ':' + String(new Date(book.t).getUTCSeconds()).padStart(2, '0') + ' UTC') + ' (' + pt(book.t) + ') · ' + book.positions.length + ' position' + (book.positions.length === 1 ? '' : 's') + ', ' + book.orders.length + ' open orders, ' + book.twaps.length + ' TWAP' + (book.twaps.length === 1 ? '' : 's') + ' · ' + R.A.length + (S_count(R)) + ' scenarios priced');
      busy = false; btn.disabled = false; nextDue = Date.now() + REFRESH_S * 1000;
    }).catch(function (e) {
      console.error(e);
      failures += 1;
      if (!lastOk) ['scen-a-wrap', 'scen-b-wrap', 'scen-grid-wrap', 'scen-orders-wrap'].forEach(function (id) { var el = document.getElementById(id); if (el) el.innerHTML = '<div class="hy-loading">Waiting for the first successful read.</div>'; });
      errBox.hidden = false; errBox.textContent = 'Could not read the account (' + failures + ' failed attempt' + (failures === 1 ? '' : 's') + ', three tries each): ' + (e && e.message ? e.message : e) + (lastOk ? '. The numbers on the page are from the read at ' + utc(lastOk) + ' and will update when the API answers again.' : '. Nothing to show yet — the Hyperliquid info API may be unreachable from this network; retrying.');
      setStatus('err', 'Read failed at ' + utc(Date.now()) + (lastOk ? ' — showing the read from ' + utc(lastOk) : ''));
      busy = false; btn.disabled = false; nextDue = Date.now() + Math.min(REFRESH_S, 20 * failures) * 1000;
    });
  }
  function S_count(R) { var n = R.A.length; if (R.B) n += R.B.length + R.G.length * R.G[0].length; return n === R.A.length ? '' : ' + ' + (n - R.A.length); }

  btn.addEventListener('click', function () { refresh(); });
  setInterval(function () {
    var now = Date.now();
    if (!busy) {
      var left = Math.max(0, Math.round((nextDue - now) / 1000));
      cd.textContent = (lastOk ? 'read ' + ago(lastOk) + ' · ' : '') + 'next read in ' + left + 's';
      if (lastOk && now - lastOk > 3 * REFRESH_S * 1000 && dot.className.indexOf('err') < 0) dot.className = 'dot busy';   // amber: the numbers are getting old
      if (now >= nextDue && document.visibilityState !== 'hidden') refresh();
      else if (now >= nextDue + 4 * REFRESH_S * 1000) refresh();   // even a hidden tab re-reads every few minutes
    } else cd.textContent = '';
  }, 1000);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible' && !busy && Date.now() >= nextDue) refresh(); });
  refresh();
})();
