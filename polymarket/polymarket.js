/* ==== Polymarket Watch — charts + live refresh ==== */
(function () {
  'use strict';

  /* ---------- baked odds history (daily CLOB closes, Jun 27 – Jul 26 2026) ---------- */
  var H = {
    julNVDA: [0.91,0.92,0.925,0.905,0.905,0.895,0.84,0.815,0.815,0.825,0.795,0.805,0.81,0.86,0.915,0.915,0.92,0.855,0.915,0.845,0.715,0.55,0.53,0.545,0.68,0.745,0.885,0.89,0.715,0.765,0.77],
    julAAPL: [0.0445,0.043,0.043,0.0435,0.0345,0.0385,0.1205,0.121,0.126,0.1245,0.118,0.112,0.1085,0.092,0.0645,0.0575,0.0655,0.113,0.06,0.1045,0.2675,0.415,0.441,0.411,0.286,0.241,0.1155,0.0965,0.2795,0.2235,0.231],
    decNVDA: [0.74,0.725,0.725,0.62,0.645,0.655,0.605,0.585,0.605,0.615,0.595,0.635,0.655,0.655,0.685,0.695,0.705,0.665,0.72,0.655,0.615,0.52,0.555,0.545,0.605,0.61,0.615,0.645,0.625,0.565,0.575],
    decAAPL: [0.095,0.0815,0.082,0.0965,0.095,0.108,0.1475,0.143,0.132,0.158,0.1555,0.1705,0.1265,0.1265,0.1405,0.1305,0.13,0.1705,0.1285,0.143,0.2285,0.345,0.328,0.3305,0.235,0.2025,0.1985,0.1985,0.2565,0.2995,0.2805],
    decGOOGL: [0.1,0.105,0.115,0.155,0.165,0.16,0.155,0.165,0.175,0.165,0.165,0.165,0.155,0.155,0.145,0.145,0.145,0.12,0.105,0.12,0.125,0.105,0.105,0.105,0.105,0.125,0.105,0.105,0.105,0.095,0.1],
    decSPCX: [0.033,0.033,0.0395,0.0355,0.023,0.0225,0.0215,0.027,0.027,0.0235,0.0215,0.0205,0.022,0.0215,0.0185,0.02,0.019,0.0145,0.0135,0.0125,0.012,0.0085,0.0085,0.0085,0.0085,0.009,0.0095,0.0115,0.0125,0.015,0.015]
  };
  var LABELS = (function () {
    var out = [], d = new Date(Date.UTC(2026, 5, 27));
    for (var i = 0; i < 30; i++) {
      out.push((d.getUTCMonth() + 1) + '/' + d.getUTCDate());
      d.setUTCDate(d.getUTCDate() + 1);
    }
    out.push('now');
    return out;
  })();

  /* series palettes — validated (dataviz six checks) for dark #0f1423 and light #ffffff */
  var PAL = {
    dark:  { NVDA: '#3987e5', AAPL: '#d95926', GOOGL: '#9085e9', SPCX: '#d55181', ink: '#7b8cb0', grid: 'rgba(255,255,255,0.06)' },
    light: { NVDA: '#2a78d6', AAPL: '#eb6834', GOOGL: '#4a3aa7', SPCX: '#e87ba4', ink: '#5e6278', grid: 'rgba(26,31,54,0.08)' }
  };

  /* ---------- live plumbing ---------- */
  var TOKENS = {
    'jul-NVDA': '11728583497514710574356365513249856989304427730091039531942765980605070477300',
    'jul-AAPL': '5823805802875099304203116182652199693089526522530469365767529374822548212673',
    'jul-GOOGL': '46584362414049299081102864761073270023695613262912078060282755871576741137444',
    'jul-MSFT': '110369498265062016820251239100016356984114678897918474918996455047198849953447',
    'jul-AMZN': '78963030528454339216772435409768100324088386511503879377911886576556782601312',
    'aug-NVDA': '95302905537962222918309360338213500184994944787102722256843629723110588711061',
    'aug-AAPL': '42047893977785728528565456844873223397500118970867834014836006695082853076308',
    'aug-GOOGL': '93997509898554464206013458433253360996772270234627522008621917049464308684354',
    'aug-AMZN': '72944522118038991341395250874399215676648471148370200768137239415303143807574',
    'aug-AVGO': '89566957160121255224944240803366911709563437585650671117746762646052979044895',
    'dec-NVDA': '11876606915924142133615854761923277060697657209957870741155164849437788272266',
    'dec-AAPL': '9875273331604434310973374077817381730908757452538191940842519381772366848',
    'dec-GOOGL': '62009449847159122385971991480139610869824965029008686522071073076098387124747',
    'dec-SPCX': '34376240305139645452191650383029377919496221975523712782933090732539681434119',
    'dec-TSLA': '50967548204329017987830198881678379324925229642745345006556239550086450305683'
  };
  var SHARES = { NVDA: 24.2, AAPL: 14.68736, GOOGL: 12.17456, MSFT: 7.42843, AMZN: 10.75711, AVGO: 4.75758, TSLA: 3.75572 }; /* billions */
  var FINNHUB_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';
  var DEADLINES = { jul: '2026-07-31', aug: '2026-08-31', dec: '2026-12-31' };
  var HOLIDAYS = { '2026-09-07': 1, '2026-11-26': 1, '2026-12-25': 1 };
  var SIGMA = 0.02;

  function phi(x) { /* standard normal CDF via erf approximation (Abramowitz-Stegun 7.1.26) */
    var s = x < 0 ? -1 : 1; x = Math.abs(x) / Math.SQRT2;
    var t = 1 / (1 + 0.3275911 * x);
    var y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
    return 0.5 * (1 + s * y);
  }
  function tradingDaysTo(iso) {
    var now = new Date(); var end = new Date(iso + 'T23:59:59Z'); var n = 0;
    var d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
    while (d <= end) {
      var dow = d.getUTCDay(); var key = d.toISOString().slice(0, 10);
      if (dow !== 0 && dow !== 6 && !HOLIDAYS[key]) n++;
      d.setUTCDate(d.getUTCDate() + 1);
    }
    return Math.max(n, 0.5);
  }
  function fair(capChal, capLead, td) { return phi(Math.log(capChal / capLead) / (SIGMA * Math.sqrt(td))); }

  var $ = function (sel) { return document.querySelector(sel); };
  var $$ = function (sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); };
  function setText(sel, txt) { $$(sel).forEach(function (el) { el.textContent = txt; }); }

  var lastTick = null;
  function setPills(live) {
    ['#live-pill', '#live-pill2'].forEach(function (sel) {
      var p = $(sel); if (!p) return;
      p.textContent = live ? 'LIVE' : 'SNAPSHOT';
      p.classList.toggle('is-live', live);
    });
  }
  function fmtAgo() {
    if (!lastTick) return;
    var s = Math.round((Date.now() - lastTick) / 1000);
    var ago = s < 5 ? 'just now' : (s < 120 ? s + 's ago' : Math.round(s / 60) + 'm ago');
    $('#last-updated').textContent = 'Updated ' + ago;
    var el = $('#sync-ago'); if (el) el.textContent = '(' + ago + ')';
  }
  setInterval(fmtAgo, 1000);

  function refresh() {
    var mids = {}; var caps = {};
    var midCalls = Object.keys(TOKENS).map(function (k) {
      return fetch('https://clob.polymarket.com/midpoint?token_id=' + TOKENS[k])
        .then(function (r) { return r.json(); })
        .then(function (j) { mids[k] = parseFloat(j.mid); });
    });
    var quoteCalls = Object.keys(SHARES).map(function (sym) {
      return fetch('https://finnhub.io/api/v1/quote?symbol=' + sym + '&token=' + FINNHUB_KEY)
        .then(function (r) { return r.json(); })
        .then(function (j) { if (j.c) caps[sym] = j.c * SHARES[sym]; });
    });
    return Promise.all(midCalls.concat(quoteCalls)).then(function () {
      /* odds cells + kpis */
      Object.keys(mids).forEach(function (k) {
        if (isNaN(mids[k])) return;
        var pct = (mids[k] * 100);
        var disp = pct >= 1 ? pct.toFixed(1) + '%' : pct.toFixed(2) + '%';
        setText('[data-odds="' + k + '"]', disp);
        setText('[data-odds-kpi="' + k + '"]', disp);
      });
      /* caps + gaps */
      if (caps.NVDA) {
        setText('#hero-lead-cap', '$' + (caps.NVDA / 1000).toFixed(3) + 'T');
        Object.keys(caps).forEach(function (sym) {
          $$('[data-cap^="' + sym + '"]').forEach(function (el) { el.textContent = caps[sym].toLocaleString('en-US', { maximumFractionDigits: 1 }); });
          if (sym !== 'NVDA') {
            var gap = (caps.NVDA / caps[sym] - 1) * 100;
            $$('[data-gap^="' + sym + '"]').forEach(function (el) { el.textContent = gap.toFixed(2) + '%'; });
          }
        });
        if (caps.AAPL) {
          setText('#hero-chal-cap', '$' + (caps.AAPL / 1000).toFixed(3) + 'T');
          setText('#hero-gap', (caps.NVDA / caps.AAPL - 1) * 100 >= 0 ? ((caps.NVDA / caps.AAPL - 1) * 100).toFixed(2) + '% · $' + Math.round(caps.NVDA - caps.AAPL) + 'B' : 'APPLE AHEAD');
        }
        /* model fair + edge per date for AAPL & GOOGL vs NVDA */
        var edgeList = [];
        ['jul', 'aug', 'dec'].forEach(function (ev) {
          var td = tradingDaysTo(DEADLINES[ev]);
          setText('[data-days="' + ev + '"]', Math.round(td));
          ['AAPL', 'GOOGL', 'MSFT', 'AMZN'].forEach(function (sym) {
            if (!caps[sym]) return;
            var key = ev + '-' + sym;
            if (!(key in TOKENS)) return;
            var f = fair(caps[sym], caps.NVDA, td) * 100;
            setText('[data-fair="' + key + '"]', (f >= 1 ? f.toFixed(1) : f.toFixed(2)) + '%');
            if (!isNaN(mids[key])) {
              var edge = mids[key] * 100 - f;
              edgeList.push({ key: key, edge: edge });
              setText('[data-edge="' + key + '"]', (edge >= 0 ? '+' : '−') + Math.abs(edge).toFixed(1));
              var v = $('[data-verdict="' + key + '"]');
              if (v) {
                v.className = 'pm-badge ' + (edge <= -5 ? 'pm-cheap' : edge >= 5 ? 'pm-rich' : 'pm-fair');
                v.textContent = edge <= -5 ? 'CHEAP' : edge >= 5 ? 'RICH' : 'FAIR';
              }
            }
          });
          /* NVDA fair = 1 - sum of challenger fairs (AAPL + GOOGL dominate) */
          if (caps.AAPL && caps.GOOGL && !isNaN(mids[ev + '-NVDA'])) {
            var fN = 100 - fair(caps.AAPL, caps.NVDA, td) * 100 - fair(caps.GOOGL, caps.NVDA, td) * 100 - (ev === 'jul' ? 0.25 : ev === 'aug' ? 1.25 : 3.65);
            setText('[data-fair="' + ev + '-NVDA"]', fN.toFixed(1) + '%');
            var edgeN = mids[ev + '-NVDA'] * 100 - fN;
            setText('[data-edge="' + ev + '-NVDA"]', (edgeN >= 0 ? '+' : '−') + Math.abs(edgeN).toFixed(1));
            var vN = $('[data-verdict="' + ev + '-NVDA"]');
            if (vN) { vN.className = 'pm-badge ' + (edgeN <= -5 ? 'pm-cheap' : edgeN >= 5 ? 'pm-rich' : 'pm-fair'); vN.textContent = edgeN <= -5 ? 'CHEAP' : edgeN >= 5 ? 'RICH' : 'FAIR'; }
            edgeList.push({ key: ev + '-NVDA', edge: edgeN });
          }
        });
        if (edgeList.length) {
          edgeList.sort(function (x, y) { return Math.abs(y.edge) - Math.abs(x.edge); });
          var top = edgeList[0];
          var lbl = top.key.split('-'); var mon = { jul: 'Jul', aug: 'Aug', dec: 'Dec' }[lbl[0]];
          var ke = $('#kpi-edge'); if (ke) ke.textContent = lbl[1] + '-' + mon + ' ' + (top.edge >= 0 ? '+' : '−') + Math.abs(top.edge).toFixed(1);
        }
        /* book sums */
        var sums = { jul: 0.0015, aug: 0.0065, dec: 0.0145 }; /* untracked small legs, baked */
        Object.keys(mids).forEach(function (k) { if (!isNaN(mids[k])) sums[k.slice(0, 3)] += mids[k]; });
        ['jul', 'aug', 'dec'].forEach(function (ev) { setText('[data-sum="' + ev + '"]', (sums[ev] * 100).toFixed(2)); });
        /* hero NVDA odds */
        if (!isNaN(mids['jul-NVDA'])) setText('#hero-nvda-odds', (mids['jul-NVDA'] * 100).toFixed(0) + '% / ' + (mids['aug-NVDA'] * 100).toFixed(0) + '% / ' + (mids['dec-NVDA'] * 100).toFixed(1) + '%');
      }
      lastTick = Date.now();
      var st = $('#sync-time');
      if (st) st.textContent = new Date(lastTick).toLocaleString([], { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', second: '2-digit' });
      setPills(true);
      fmtAgo();
    }).catch(function () {
      setPills(false);
      $('#last-updated').textContent = 'Snapshot · Jul 26, 2026 20:00 UTC (live APIs unreachable)';
      var st = $('#sync-time'); if (st) st.textContent = 'Jul 26, 2026 20:00 UTC (baked snapshot — live APIs unreachable)';
    });
  }

  /* ---------- charts ---------- */
  var charts = [];
  function endLabelPlugin(ink) {
    return {
      id: 'endLabels',
      afterDatasetsDraw: function (chart) {
        var ctx = chart.ctx;
        ctx.save();
        ctx.font = '600 11px Poppins, sans-serif';
        ctx.fillStyle = ink;
        chart.data.datasets.forEach(function (ds, i) {
          var meta = chart.getDatasetMeta(i);
          var last = meta.data[meta.data.length - 1];
          if (last) ctx.fillText(ds.label, Math.min(last.x + 6, chart.chartArea.right - 34), last.y + 4);
        });
        ctx.restore();
      }
    };
  }
  function buildCharts() {
    if (typeof Chart === 'undefined') return;
    charts.forEach(function (c) { c.destroy(); });
    charts = [];
    var mode = document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
    var P = PAL[mode];
    var common = {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { color: P.ink, boxWidth: 14, boxHeight: 3, font: { size: 11 } } },
        tooltip: { callbacks: { label: function (c) { return ' ' + c.dataset.label + ': ' + (c.parsed.y).toFixed(1) + '%'; } } }
      },
      scales: {
        x: { ticks: { color: P.ink, maxTicksLimit: 8, font: { size: 10 } }, grid: { display: false } },
        y: { min: 0, max: 100, ticks: { color: P.ink, callback: function (v) { return v + '%'; }, font: { size: 10 } }, grid: { color: P.grid } }
      },
      elements: { line: { borderWidth: 2, tension: 0.25 }, point: { radius: 0, hoverRadius: 5, hitRadius: 10 } }
    };
    function ds(label, arr, color) { return { label: label, data: arr.map(function (p) { return p * 100; }), borderColor: color, backgroundColor: color, pointBackgroundColor: color }; }
    var el1 = document.getElementById('chart-july');
    if (el1) charts.push(new Chart(el1, { type: 'line', data: { labels: LABELS, datasets: [ds('NVDA', H.julNVDA, P.NVDA), ds('AAPL', H.julAAPL, P.AAPL)] }, options: common, plugins: [endLabelPlugin(P.ink)] }));
    var el2 = document.getElementById('chart-dec');
    if (el2) charts.push(new Chart(el2, { type: 'line', data: { labels: LABELS, datasets: [ds('NVDA', H.decNVDA, P.NVDA), ds('AAPL', H.decAAPL, P.AAPL), ds('GOOGL', H.decGOOGL, P.GOOGL), ds('SPCX', H.decSPCX, P.SPCX)] }, options: common, plugins: [endLabelPlugin(P.ink)] }));
  }

  /* ---------- collapsible cards ---------- */
  $$('.pm-cards .panel-card').forEach(function (card) {
    var p = card.querySelector('p');
    if (!p) return;
    var btn = document.createElement('button');
    btn.className = 'pm-more';
    btn.innerHTML = 'Read more <span class="chev">\u25BC</span>';
    btn.setAttribute('aria-expanded', 'false');
    card.appendChild(btn);
    btn.addEventListener('click', function () {
      var open = card.classList.toggle('expanded');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.innerHTML = (open ? 'Show less' : 'Read more') + ' <span class="chev">\u25BC</span>';
    });
    /* hide the button if the text already fits unclamped (only measurable when visible) */
    if (p.offsetParent !== null && p.scrollHeight <= p.clientHeight + 2) btn.style.display = 'none';
  });


  /* ---------- live account positions ---------- */
  var WALLET = '0xD1eED20eDD22A289839379e89E3470eA1742A8ae';
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function shortTitle(t) {
    return t.replace(/^Will /, '')
      .replace(/ be the largest company in the world by market cap on/, ' \u2014 largest co.')
      .replace(/ be the second-largest company in the world by market cap on/, ' \u2014 2nd largest')
      .replace(/ be the third-largest company in the world by market cap on/, ' \u2014 3rd largest')
      .replace(/ strike out the most batters during the 2026 MLB regular season/, ' \u2014 MLB strikeout leader')
      .replace(/\?$/, '');
  }
  function usd(x) { return '$' + Math.abs(x).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  var ACCT_SHOW = 20;
  var acctExpanded = false;
  var prev24 = {}; var prev24At = 0;
  var entryMap = null;
  function loadEntryMap() {
    if (entryMap) return Promise.resolve(entryMap);
    var pages = [0, 500, 1000].map(function (off) {
      return fetch('https://data-api.polymarket.com/activity?user=' + WALLET + '&limit=500&offset=' + off)
        .then(function (r) { return r.json(); }).catch(function () { return []; });
    });
    return Promise.all(pages).then(function (res) {
      var m = {};
      res.forEach(function (arr) {
        (arr || []).forEach(function (ev) {
          if (ev && ev.type === 'TRADE' && ev.side === 'BUY' && ev.asset) {
            var sz = parseFloat(ev.size) || 0;
            var ts = +ev.timestamp; if (ts > 2e10) ts = ts / 1000;
            if (!m[ev.asset]) m[ev.asset] = { s: 0, st: 0 };
            m[ev.asset].s += sz; m[ev.asset].st += sz * ts;
          }
        });
      });
      entryMap = m; return m;
    });
  }
  function loadPrev24(assets) {
    if (Date.now() - prev24At > 30 * 60 * 1000) { prev24 = {}; }
    var need = assets.filter(function (a) { return !(a in prev24); });
    if (!need.length) return Promise.resolve();
    prev24At = Date.now();
    return Promise.all(need.map(function (a) {
      return fetch('https://clob.polymarket.com/prices-history?market=' + a + '&interval=1d&fidelity=60')
        .then(function (r) { return r.json(); })
        .then(function (j) { if (j.history && j.history.length) prev24[a] = parseFloat(j.history[0].p); })
        .catch(function () {});
    }));
  }
  function applyAcctCollapse() {
    var rows = $$('#acct-body tr');
    rows.forEach(function (r, i) { r.hidden = !acctExpanded && i >= ACCT_SHOW; });
    var btn = $('#acct-more');
    if (!btn) return;
    if (rows.length <= ACCT_SHOW) { btn.hidden = true; return; }
    btn.hidden = false;
    btn.innerHTML = (acctExpanded ? 'Show top ' + ACCT_SHOW : 'Show all ' + rows.length + ' positions') + ' <span class="chev">\u25BC</span>';
    btn.classList.toggle('expanded', acctExpanded);
  }
  function loadWindowPnl() {
    var wins = { '1d': '#acct-pnl24', '1m': '#acct-pnl1m', 'all': '#acct-pnl1y' };
    Object.keys(wins).forEach(function (iv) {
      fetch('https://user-pnl-api.polymarket.com/user-pnl?user_address=' + WALLET + '&interval=' + iv + '&fidelity=' + (iv === '1d' ? '1h' : '1d'))
        .then(function (r) { return r.json(); })
        .then(function (arr) {
          if (!arr || arr.length < 2) return;
          if (iv === 'all' && arr.length > 365) arr = arr.slice(-365);
          var d = arr[arr.length - 1].p - arr[0].p;
          var el = $(wins[iv]); if (!el) return;
          el.textContent = (d >= 0 ? '+' : '\u2212') + usd(d);
          el.className = 'account-hero-stat-value ' + (d >= 0 ? 'pm-pos' : 'pm-neg');
        }).catch(function () {});
    });
  }
  function fetchCash() {
    /* Available to trade = native USDC + bridged USDC.e balances of the proxy wallet on Polygon */
    var tokens = ['0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359', '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'];
    return Promise.all(tokens.map(function (tk, i) {
      return fetch('https://polygon-rpc.com', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jsonrpc: '2.0', id: i + 1, method: 'eth_call', params: [{ to: tk, data: '0x70a08231000000000000000000000000' + WALLET.slice(2).toLowerCase() }, 'latest'] })
      }).then(function (r) { return r.json(); })
        .then(function (j) { return j && j.result ? parseInt(j.result, 16) / 1e6 : 0; })
        .catch(function () { return 0; });
    })).then(function (vals) {
      var sum = vals.reduce(function (s, v) { return s + (isFinite(v) ? v : 0); }, 0);
      return sum > 0 ? sum : null;
    }).catch(function () { return null; });
  }
  function refreshAccount() {
    return Promise.all([
      fetch('https://data-api.polymarket.com/positions?user=' + WALLET + '&limit=500').then(function (r) { return r.json(); }),
      fetch('https://data-api.polymarket.com/value?user=' + WALLET).then(function (r) { return r.json(); }),
      fetchCash()
    ]).then(function (res) {
      var pos = res[0] || [], valArr = res[1] || [], cashBal = res[2];
      if (!pos.length) return null;
      var active = pos.filter(function (p) { return p.currentValue >= 1; })
                      .sort(function (a, b) { return b.currentValue - a.currentValue; });
      return Promise.all([loadEntryMap(), loadPrev24(active.map(function (p) { return p.asset; }))]).then(function () { return { pos: pos, valArr: valArr, active: active, cashBal: cashBal }; });
    }).then(function (ctx) {
      if (!ctx) return;
      var pos = ctx.pos, valArr = ctx.valArr, active = ctx.active, cashBal = ctx.cashBal;
      var body = $('#acct-body');
      if (body && active.length) {
        body.innerHTML = active.map(function (p) {
          var cls = p.cashPnl >= 0 ? 'pm-pos' : 'pm-neg';
          var side = p.outcome === 'No' ? 'dir-short' : 'dir-long';
          var sign = p.cashPnl >= 0 ? '+' : '\u2212';
          var psign = p.percentPnl >= 0 ? '+' : '\u2212';
          var url = 'https://polymarket.com/event/' + encodeURIComponent(p.eventSlug || '') + (p.slug ? '/' + encodeURIComponent(p.slug) : '');
          var nameHtml = p.eventSlug
            ? '<a href="' + url + '" target="_blank" rel="noopener">' + esc(shortTitle(p.title)) + '<span class="pm-ext">\u2197</span></a>'
            : esc(shortTitle(p.title));
          var rowCls = p.outcome === 'No' ? 'row-short' : 'row-long';
          var sub = '';
          if (p.endDate && p.endDate.slice(0, 4) > '1971') {
            var ed = new Date(p.endDate);
            sub = '<div class="pm-sub">Ends ' + (ed.getUTCMonth() + 1) + '/' + ed.getUTCDate() + '/' + String(ed.getUTCFullYear()).slice(2) + '</div>';
          }
          return '<tr class="' + rowCls + '"><td class="pm-co pm-mkt" title="' + esc(p.title) + '">' + nameHtml + sub + '</td>' +
            '<td><span class="dir-badge ' + side + '">' + esc(p.outcome.toUpperCase()) + '</span></td>' +
            '<td class="col-num">' + Math.round(p.size).toLocaleString('en-US') + '</td>' +
            '<td class="col-num">' + (p.avgPrice * 100).toFixed(1) + '\u00A2</td>' +
            '<td class="col-num">' + (p.curPrice * 100).toFixed(1) + '\u00A2</td>' +
            '<td class="col-num">' + usd(p.currentValue) + '</td>' +
            '<td class="col-num ' + cls + '">' + sign + usd(p.cashPnl) + '</td>' +
            '<td class="col-num ' + cls + '">' + psign + Math.abs(p.percentPnl).toFixed(1) + '%</td>' +
            (function () {
              var pv = prev24[p.asset];
              if (pv == null || !isFinite(pv)) return '<td class="col-num">—</td>';
              var d24 = (p.curPrice - pv) * p.size;
              var c24 = d24 >= 0 ? 'pm-pos' : 'pm-neg';
              return '<td class="col-num ' + c24 + '">' + (d24 >= 0 ? '+' : '\u2212') + usd(d24) + '</td>';
            })() +
            (function () {
              var em = entryMap && entryMap[p.asset];
              if (!em || !em.s) return '<td class="col-num">—</td>';
              var d = new Date(em.st / em.s * 1000);
              return '<td class="col-num">' + d.toLocaleDateString([], { month: 'numeric', day: 'numeric', year: '2-digit' }) + '</td>';
            })() + '</tr>';
        }).join('');
        applyAcctCollapse();
      }
      var posSum = pos.reduce(function (s, p) { return s + (p.currentValue || 0); }, 0);
      setText('#acct-value', usd(posSum));
      var haveCash = cashBal != null && isFinite(cashBal);
      var ce = $('#acct-cash');
      if (ce) {
        if (haveCash) ce.textContent = usd(cashBal);
        else if (valArr.length && valArr[0].value != null && valArr[0].value - posSum >= 0) ce.textContent = usd(valArr[0].value - posSum) + ' (est.)';
      }
      var pf = $('#acct-portfolio');
      if (pf) {
        if (haveCash) pf.textContent = usd(posSum + cashBal);
        else if (valArr.length && valArr[0].value != null) pf.textContent = usd(valArr[0].value);
        else pf.textContent = usd(posSum);
      }
      setText('#acct-open', String(active.length));
      var pnl = active.reduce(function (s, p) { return s + p.cashPnl; }, 0);
      var pnlEl = $('#acct-pnl');
      if (pnlEl) { pnlEl.textContent = (pnl >= 0 ? '+' : '\u2212') + usd(pnl); pnlEl.className = 'account-hero-stat-value ' + (pnl >= 0 ? 'pm-pos' : 'pm-neg'); }
      loadWindowPnl();
    }).catch(function () { /* keep baked snapshot */ });
  }

  /* ---------- wiring ---------- */
  var chartsBuiltVisible = false;
  $$('.page-nav .nav-tab[data-view]').forEach(function (tab) {
    tab.addEventListener('click', function (e) {
      e.preventDefault();
      $$('.page-nav .nav-tab[data-view]').forEach(function (t) { t.classList.remove('active'); });
      tab.classList.add('active');
      var view = tab.getAttribute('data-view');
      document.getElementById('view-polymarket').hidden = view !== 'polymarket';
      document.getElementById('view-largest').hidden = view !== 'largest';
      if (view === 'largest' && !chartsBuiltVisible) {
        chartsBuiltVisible = true;
        requestAnimationFrame(buildCharts);
      }
    });
  });

  function forceSync() {
    var btn = document.getElementById('btn-sync');
    var lbl = document.getElementById('btn-sync-label');
    if (btn) { btn.disabled = true; btn.classList.add('is-syncing'); }
    if (lbl) lbl.textContent = 'Syncing…';
    var done = function () {
      if (btn) { btn.disabled = false; btn.classList.remove('is-syncing'); }
      if (lbl) lbl.textContent = 'Sync Now';
    };
    Promise.all([refresh(), refreshAccount()]).then(done, done);
  }
  document.getElementById('btn-refresh').addEventListener('click', forceSync);
  var syncBtn = document.getElementById('btn-sync');
  if (syncBtn) syncBtn.addEventListener('click', forceSync);
  document.getElementById('theme-toggle').addEventListener('click', function () {
    var root = document.documentElement;
    root.setAttribute('data-theme', root.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
    buildCharts();
  });
  var acctMoreBtn = document.getElementById('acct-more');
  if (acctMoreBtn) acctMoreBtn.addEventListener('click', function () { acctExpanded = !acctExpanded; applyAcctCollapse(); });
  applyAcctCollapse();
  buildCharts();
  refresh();
  refreshAccount();
  setInterval(refresh, 60000);
  setInterval(refreshAccount, 60000);
})();
