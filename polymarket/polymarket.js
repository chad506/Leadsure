/* ==== Polymarket Watch — charts + live refresh ==== */
(function () {
  'use strict';

  /* ---------- baked odds history (daily CLOB closes, Jun 27 – Jul 30 2026 + live) ---------- */
  var H = {
    julNVDA: [0.925,0.925,0.905,0.905,0.895,0.84,0.815,0.815,0.825,0.795,0.805,0.81,0.86,0.915,0.915,0.92,0.855,0.915,0.845,0.715,0.55,0.53,0.545,0.68,0.745,0.885,0.89,0.715,0.765,0.795,0.295,0.215,0.08,0.6345,0.6345],
    julAAPL: [0.043,0.043,0.0435,0.0345,0.0385,0.1205,0.121,0.126,0.1245,0.118,0.112,0.1085,0.092,0.0645,0.0575,0.0655,0.113,0.06,0.1045,0.2675,0.415,0.441,0.411,0.286,0.241,0.1155,0.0965,0.2795,0.2235,0.2155,0.698,0.7815,0.925,0.354,0.354],
    decNVDA: [0.725,0.725,0.62,0.645,0.655,0.605,0.585,0.605,0.615,0.595,0.635,0.655,0.655,0.685,0.695,0.705,0.665,0.72,0.655,0.615,0.52,0.555,0.545,0.605,0.61,0.615,0.645,0.625,0.565,0.575,0.51,0.485,0.485,0.575,0.575],
    decAAPL: [0.082,0.082,0.0965,0.095,0.108,0.1475,0.143,0.132,0.158,0.1555,0.1705,0.1265,0.1265,0.1405,0.1305,0.13,0.1705,0.1285,0.143,0.2285,0.345,0.328,0.3305,0.235,0.2025,0.1985,0.1985,0.2565,0.2995,0.281,0.353,0.289,0.3565,0.257,0.257],
    decGOOGL: [0.115,0.115,0.155,0.165,0.16,0.155,0.165,0.175,0.165,0.165,0.165,0.155,0.155,0.145,0.145,0.145,0.12,0.105,0.12,0.125,0.105,0.105,0.105,0.105,0.125,0.105,0.105,0.105,0.095,0.095,0.105,0.135,0.145,0.13,0.13],
    decSPCX: [0.0395,0.0395,0.0355,0.023,0.0225,0.0215,0.027,0.027,0.0235,0.0215,0.0205,0.022,0.0215,0.0185,0.02,0.019,0.0145,0.0135,0.0125,0.012,0.0085,0.0085,0.0085,0.0085,0.009,0.0095,0.0115,0.0125,0.015,0.0105,0.0095,0.017,0.0155,0.0175,0.0175]
  };
  var LABELS = (function () {
    var out = [], d = new Date(Date.UTC(2026, 5, 27));
    for (var i = 0; i < 34; i++) {
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
        var leadCap = Math.max.apply(null, Object.keys(caps).map(function (k2) { return caps[k2]; }));
        Object.keys(caps).forEach(function (sym) {
          $$('[data-cap^="' + sym + '"]').forEach(function (el) { el.textContent = caps[sym].toLocaleString('en-US', { maximumFractionDigits: 1 }); });
          var gap = (leadCap / caps[sym] - 1) * 100;
          $$('[data-gap^="' + sym + '"]').forEach(function (el) { el.textContent = gap < 0.005 ? '\u2014' : gap.toFixed(2) + '%'; });
        });
        if (caps.AAPL) {
          var lead = caps.AAPL > caps.NVDA ? 'AAPL' : 'NVDA', chal = lead === 'AAPL' ? 'NVDA' : 'AAPL';
          setText('#hero-lead-label', 'Current #1 \u00B7 ' + (lead === 'AAPL' ? 'Apple' : 'NVIDIA'));
          setText('#hero-chal-label', '#2 ' + (chal === 'AAPL' ? 'Apple' : 'NVIDIA'));
          setText('#hero-lead-cap', '$' + (caps[lead] / 1000).toFixed(3) + 'T');
          setText('#hero-chal-cap', '$' + (caps[chal] / 1000).toFixed(3) + 'T');
          setText('#hero-gap', ((caps[lead] / caps[chal] - 1) * 100).toFixed(2) + '% \u00B7 $' + Math.round(caps[lead] - caps[chal]) + 'B');
        }
        /* model fair + edge per date — LEADER-AWARE: key off whichever company is largest today.
           Challenger fair = P(chal ends above leader); leader fair = 100 − Σ challenger fairs − small legs. */
        var edgeList = [];
        var RACE = ['AAPL', 'NVDA', 'GOOGL', 'MSFT', 'AMZN'];
        var leadSym = RACE.filter(function (s) { return caps[s]; }).reduce(function (a, b) { return caps[a] >= caps[b] ? a : b; });
        ['jul', 'aug', 'dec'].forEach(function (ev) {
          var td = tradingDaysTo(DEADLINES[ev]);
          setText('[data-days="' + ev + '"]', Math.round(td));
          var sumCh = 0;
          RACE.forEach(function (sym) { if (sym !== leadSym && caps[sym]) sumCh += fair(caps[sym], caps[leadSym], td) * 100; });
          RACE.forEach(function (sym) {
            if (!caps[sym]) return;
            var key = ev + '-' + sym;
            if (!(key in TOKENS)) return;
            var f = sym === leadSym
              ? 100 - sumCh - (ev === 'jul' ? 0.25 : ev === 'aug' ? 1.25 : 3.65)
              : fair(caps[sym], caps[leadSym], td) * 100;
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
        /* hero AAPL odds (label reads "AAPL Odds Jul / Aug / Dec") */
        if (!isNaN(mids['jul-AAPL'])) setText('#hero-nvda-odds', (mids['jul-AAPL'] * 100).toFixed(0) + '% / ' + (mids['aug-AAPL'] * 100).toFixed(0) + '% / ' + (mids['dec-AAPL'] * 100).toFixed(1) + '%');
      }
      lastTick = Date.now();
      var st = $('#sync-time');
      if (st) st.textContent = new Date(lastTick).toLocaleString([], { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', second: '2-digit' });
      setPills(true);
      fmtAgo();
    }).catch(function () {
      setPills(false);
      $('#last-updated').textContent = 'Snapshot · Jul 30, 2026 23:45 UTC — after hours (live APIs unreachable)';
      var st = $('#sync-time'); if (st) st.textContent = 'Jul 30, 2026 23:45 UTC · after hours (baked snapshot — live APIs unreachable)';
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
  var acctSort = { idx: null, dir: -1 };
  function parseCell(td) {
    var t = td.textContent.trim();
    if (t === '\u2014' || t === '') return -Infinity;
    var m = t.match(/^(\d+)\/(\d+)\/(\d+)$/);
    if (m) return (+m[3]) * 10000 + (+m[1]) * 100 + (+m[2]);
    var n = parseFloat(t.replace(/\u2212/g, '-').replace(/[$%\u00A2,+]/g, ''));
    if (!isNaN(n)) return n;
    return t.toLowerCase();
  }
  function sortAcct(idx, dir) {
    var body = $('#acct-body'); if (!body) return;
    var rows = Array.prototype.slice.call(body.querySelectorAll('tr'));
    rows.sort(function (ra, rb) {
      var va = parseCell(ra.children[idx]), vb = parseCell(rb.children[idx]);
      if (va === vb) return 0;
      if (typeof va === 'string' || typeof vb === 'string') { va = String(va); vb = String(vb); return va < vb ? dir : -dir; }
      return (vb - va) * dir;
    });
    rows.forEach(function (r) { body.appendChild(r); });
    applyAcctCollapse();
  }
  function initAcctSort() {
    $$('.pm-acct-table thead th').forEach(function (th, idx) {
      th.classList.add('pm-sortable');
      th.addEventListener('click', function () {
        var dir = (acctSort.idx === idx && acctSort.dir === 1) ? -1 : 1; /* first click: descending (dir=1 = big first) */
        acctSort = { idx: idx, dir: dir };
        $$('.pm-acct-table thead th').forEach(function (t) { t.classList.remove('sort-asc', 'sort-desc'); });
        th.classList.add(dir === 1 ? 'sort-desc' : 'sort-asc');
        sortAcct(idx, dir);
      });
    });
  }
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
  function fetchWalletCash() {
    /* native USDC + bridged USDC.e held by the proxy wallet on Polygon. Polymarket's
       "Available to trade" = this MINUS collateral reserved by open resting orders,
       which is private to the order engine and not publicly readable. */
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
      fetchWalletCash()
    ]).then(function (res) {
      var pos = res[0] || [], valArr = res[1] || [], walletCash = res[2];
      if (!pos.length) return null;
      var active = pos.filter(function (p) { return p.currentValue >= 1; })
                      .sort(function (a, b) { return b.currentValue - a.currentValue; });
      return Promise.all([loadEntryMap(), loadPrev24(active.map(function (p) { return p.asset; }))]).then(function () { return { pos: pos, valArr: valArr, active: active, walletCash: walletCash }; });
    }).then(function (ctx) {
      if (!ctx) return;
      var pos = ctx.pos, valArr = ctx.valArr, active = ctx.active, walletCash = ctx.walletCash;
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
        if (acctSort.idx != null) sortAcct(acctSort.idx, acctSort.dir);
      }
      var posSum = pos.reduce(function (s, p) { return s + (p.currentValue || 0); }, 0);
      /* data-api /value is positions-only; prefer it as authoritative when present */
      var posVal = valArr.length && valArr[0].value != null ? valArr[0].value : posSum;
      setText('#acct-value', usd(posVal));
      var ce = $('#acct-cash');
      if (ce && walletCash != null) ce.textContent = usd(walletCash);
      var pf = $('#acct-portfolio');
      if (pf) pf.textContent = usd(posVal + (walletCash != null ? walletCash : 0));
      setText('#acct-open', String(active.length));
      var pnl = active.reduce(function (s, p) { return s + p.cashPnl; }, 0);
      var pnlEl = $('#acct-pnl');
      if (pnlEl) { pnlEl.textContent = (pnl >= 0 ? '+' : '\u2212') + usd(pnl); pnlEl.className = 'account-hero-stat-value ' + (pnl >= 0 ? 'pm-pos' : 'pm-neg'); }
      loadWindowPnl();
    }).catch(function () { /* keep baked snapshot */ });
  }

  /* ---------- decision tracking ledger ---------- */
  var TRACKED = [
    { act: 'SELL', tok: '34376240305139645452191650383029377919496221975523712782933090732539681434119', sh: 10645.17, px: 0.0097 },
    { act: 'SELL', tok: '55689044028128278672494108251217443782536678376777545334307559186551480418539', sh: 507.60, px: 0.1626 },
    { act: 'SELL', tok: '105122145715401868862282894819487928240289369378439043280447797378511530042214', sh: 614.25, px: 0.0574 },
    { act: 'SELL', tok: '89220876555191016916241799318314090743516702009053928118059298766028257434413', sh: 1830, px: 0.1209 },
    { act: 'BUY', tok: '42047893977785728528565456844873223397500118970867834014836006695082853076308', sh: 443.38, px: 0.2308 },
    { act: 'BUY', tok: '54398790535896757998414933803834478150495648270732685658889540342278545164806', sh: 219.78, px: 0.9133 },
    { act: 'BUY', tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', sh: 228.41, px: 0.2201 },
    { act: 'BUY', tok: '42047893977785728528565456844873223397500118970867834014836006695082853076308', sh: 399.32, px: 0.2670 },
    { act: 'BUY', tok: '54398790535896757998414933803834478150495648270732685658889540342278545164806', sh: 100.00, px: 0.9000 },
    { act: 'BUY', tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', sh: 53.62, px: 0.2201 },
    { act: 'SELL', tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', sh: 80.00, px: 0.5249 },
    { act: 'BUY', tok: '54398790535896757998414933803834478150495648270732685658889540342278545164806', sh: 320, px: 0.9068 } /* token corrected Jul 30 PM: prior entry carried the Alphabet-JULY-NO token by mistake */,
    { act: 'BUY', tok: '42047893977785728528565456844873223397500118970867834014836006695082853076308', sh: 408.16, px: 0.49 },
    { act: 'SELL', tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', sh: 259.98, px: 0.8115 },
    { act: 'SELL', tok: '75848210276979954337354349909329862141109563590210566057575338891512846216329', sh: 1366.20, px: 0.7504 },
    { act: 'BUY', tok: '62131357779217648903043004312290004169149177020747768355527511163218119967855', sh: 192.0, px: 0.5207 },
    { act: 'BUY', tok: '5823805802875099304203116182652199693089526522530469365767529374822548212673', sh: 353.0, px: 0.7925 },
    { act: 'BUY', tok: '73927186257882802877663040737479279251981612783026680169571204930062095676076', sh: 36391.0, px: 0.0032 },
    { act: 'BUY', tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', sh: 484.0, px: 0.1006 },
    { act: 'SELL', tok: '11122870307832213829937141164621963143556849554535072384599725110500454191759', sh: 699.0, px: 0.9965 },
    { act: 'SELL', tok: '54398790535896757998414933803834478150495648270732685658889540342278545164806', sh: 320.0, px: 0.8861 },
    { act: 'SELL', tok: '79162765079028727202719931536645059951675772849915793147357039418708378144838', sh: 201.0, px: 0.862 },
    { act: 'SELL', tok: '5823805802875099304203116182652199693089526522530469365767529374822548212673', sh: 656.0, px: 0.7433 },
    { act: 'SELL', tok: '42047893977785728528565456844873223397500118970867834014836006695082853076308', sh: 2097.19, px: 0.4579 },
    { act: 'SELL', tok: '62131357779217648903043004312290004169149177020747768355527511163218119967855', sh: 565.71, px: 0.5080 },
    { act: 'SELL', tok: '9875273331604434310973374077817381730908757452538191940842519381772366848', sh: 1262.87, px: 0.3540 },
    { act: 'SELL', tok: '111327393597485860518383875037840373186301110591311759745870941465618542615273', sh: 1210.99, px: 0.9772 },
    { act: 'SELL', tok: '96387637149724428553445768391618256120718991754377697284782652889309617461095', sh: 739.77, px: 0.9718 },
    { act: 'SELL', tok: '76489196366809276678703167395741335062889477749411701459047587268289649419879', sh: 520.84, px: 0.9674 },
    { act: 'SELL', tok: '114033095271617070714983865791504478906266507670567428753203001241312040895286', sh: 2149.06, px: 0.5053 },
    { act: 'SELL', tok: '9875273331604434310973374077817381730908757452538191940842519381772366848', sh: 2841.46, px: 0.3518 },
    { act: 'SELL', tok: '17084797490500037409044502348008267729869356460292539382657498083054409006802', sh: 73.61, px: 0.999 },
    { act: 'SELL', tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', sh: 200.0, px: 0.8600 },
    { act: 'SELL', tok: '79162765079028727202719931536645059951675772849915793147357039418708378144838', sh: 17.5, px: 0.91 },
    { act: 'BUY', tok: '62131357779217648903043004312290004169149177020747768355527511163218119967855', sh: 2895.11, px: 0.6516 },
    { act: 'BUY', tok: '42047893977785728528565456844873223397500118970867834014836006695082853076308', sh: 1243.0, px: 0.5970 },
    { act: 'SELL', tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', sh: 602.69, px: 0.9180 },
    { act: 'BUY', tok: '5823805802875099304203116182652199693089526522530469365767529374822548212673', sh: 215.29, px: 0.9316 },
    { act: 'SELL', tok: '79162765079028727202719931536645059951675772849915793147357039418708378144838', sh: 129.78, px: 0.9281 },
    { act: 'BUY', tok: '79162765079028727202719931536645059951675772849915793147357039418708378144838', sh: 63.16, px: 0.9519 },
    { act: 'BUY', tok: '22380582002052839082465005899114395003938630732672759582910297636521820401881', sh: 1269.70, px: 0.9451 },
    { act: 'BUY', tok: '96738271970978473626692761675665650558731868524608528797496705773854589776782', sh: 1694.92, px: 0.5900 },
    { act: 'SELL', tok: '42047893977785728528565456844873223397500118970867834014836006695082853076308', sh: 3104.0, px: 0.4089 },
    { act: 'SELL', tok: '', sh: 4177.0, px: 0.4851 },
    { act: 'BUY', tok: '11728583497514710574356365513249856989304427730091039531942765980605070477300', sh: 3617.0, px: 0.6176 },
    { act: 'BUY', tok: '44485368873643784531862401772918820589721230664189835980509638753050855169710', sh: 1136.0, px: 0.5147 },
    { act: 'BUY', tok: '24709869777541994161985607099029324252686151170116658170228927775726765767759', sh: 1003.0, px: 0.8038 },
    { act: 'BUY', tok: '52571501528156787027187935562201905991806996165843090033663476160970921418771', sh: 858.0, px: 0.7759 }
  ];
  function refreshTracking() {
    Promise.all(TRACKED.map(function (t, i) {
      return fetch('https://clob.polymarket.com/midpoint?token_id=' + t.tok)
        .then(function (r) { return r.json(); })
        .then(function (j) {
          var cur = parseFloat(j.mid);
          if (isNaN(cur)) return null;
          var nowEl = $('[data-track-now="' + i + '"]');
          if (nowEl) nowEl.textContent = (cur * 100).toFixed(1) + '\u00A2';
          var delta = t.act === 'SELL' ? (t.px - cur) * t.sh : (cur - t.px) * t.sh;
          var dEl = $('[data-track-delta="' + i + '"]');
          if (dEl) {
            dEl.textContent = (delta >= 0 ? '+' : '\u2212') + usd(delta) + (t.act === 'SELL' ? ' saved' : '');
            dEl.className = 'col-num ' + (delta >= 0 ? 'pm-pos' : 'pm-neg');
          }
          var vEl = $('[data-track-verdict="' + i + '"]');
          if (vEl) {
            if (delta >= 1) { vEl.className = 'pm-badge pm-cheap'; vEl.textContent = t.act === 'SELL' ? 'GOOD SELL' : 'WORKING'; }
            else if (delta <= -1) { vEl.className = 'pm-badge pm-rich'; vEl.textContent = t.act === 'SELL' ? 'EARLY' : 'UNDERWATER'; }
            else { vEl.className = 'pm-badge pm-fair'; vEl.textContent = 'FLAT'; }
          }
          return delta;
        }).catch(function () { return null; });
    })).then(function (ds) {
      var vals = ds.filter(function (d) { return d != null && isFinite(d); });
      if (!vals.length) return;
      var tot = vals.reduce(function (s, d) { return s + d; }, 0);
      var el = document.getElementById('track-total-delta');
      if (el) {
        el.textContent = (tot >= 0 ? '+' : '\u2212') + usd(tot) + ' net';
        el.className = 'col-num ' + (tot >= 0 ? 'pm-pos' : 'pm-neg');
      }
      var v = document.getElementById('track-total-verdict');
      if (v) {
        if (tot >= 1) { v.className = 'pm-badge pm-cheap'; v.textContent = 'NET POSITIVE'; }
        else if (tot <= -1) { v.className = 'pm-badge pm-rich'; v.textContent = 'NET NEGATIVE'; }
        else { v.className = 'pm-badge pm-fair'; v.textContent = 'FLAT'; }
      }
    });
  }

  /* ---------- retired ideas ledger (appended by the auto-run) ---------- */
  var RETIRED = [ /* {tok, side ('BUY'|'SELL'), retPx} — indices align with #retired-body rows' data-retired-* attrs; tok:'' = unscoreable (no live market) */
    { tok: '93997509898554464206013458433253360996772270234627522008621917049464308684354', side: 'BUY', retPx: 0.047 },
    { tok: '', side: 'BUY', retPx: 0 },
    { tok: '88181040897286103762090116883791794441997393429026713037275553532748007513417', side: 'BUY', retPx: 0.555 },
    { tok: '', side: 'BUY', retPx: 0 },
    { tok: '', side: 'BUY', retPx: 0 },
    { tok: '', side: 'BUY', retPx: 0 },
    { tok: '54398790535896757998414933803834478150495648270732685658889540342278545164806', side: 'BUY', retPx: 0.895 },
    { tok: '', side: 'SELL', retPx: 0 }, /* MSFT-3rd: no bid side exists — midpoint would mislead; unscored */
    { tok: '', side: 'BUY', retPx: 0 },
    { tok: '11728583497514710574356365513249856989304427730091039531942765980605070477300', side: 'BUY', retPx: 0.445 },
    { tok: '76489196366809276678703167395741335062889477749411701459047587268289649419879', side: 'BUY', retPx: 0.979 },
    { tok: '79162765079028727202719931536645059951675772849915793147357039418708378144838', side: 'BUY', retPx: 0.795 },
    { tok: '9875273331604434310973374077817381730908757452538191940842519381772366848', side: 'BUY', retPx: 0.362 }, /* Apple-Dec add — edge < 5 pts post-trim */
    { tok: '', side: 'SELL', retPx: 0 }, /* WTI $80-low July NO — resolved YES to zero before the salvage sell; unscoreable */
    { tok: '62174033562645769120246190297623781610533939632822008848983822335275512869792', side: 'SELL', retPx: 0.9485 }, /* James Wood RBI NO sell — thesis reversed */
    { tok: '', side: 'BUY', retPx: 0 }, /* MSFT-3rd-Aug NO — 99.8¢ indicative, dominated; QUOTE PENDING failed twice */
    { tok: '11728583497514710574356365513249856989304427730091039531942765980605070477300', side: 'BUY', retPx: 0.255 }, /* NVDA-July YES re-flip hedge — rich vs model, July book closed */
    { tok: '76489196366809276678703167395741335062889477749411701459047587268289649419879', side: 'BUY', retPx: 0.9735 }, /* BTC $57.5k July NO top-up — account sold the whole leg */
    { tok: '111327393597485860518383875037840373186301110591311759745870941465618542615273', side: 'BUY', retPx: 0.9775 }, /* SPY $770 NO carry add — account sold the whole leg */
    { tok: '96387637149724428553445768391618256120718991754377697284782652889309617461095', side: 'BUY', retPx: 0.9820 }, /* SPY $700 NO carry add — account sold the whole leg */
    { tok: '', side: 'SELL', retPx: 0 }, /* July carry hold-to-resolution (Sells #7 / New #11) — account sold all three legs early; multi-token, unscoreable */
    { tok: '', side: 'BUY', retPx: 0 }, /* August under-parity basket — leak closed within one session (94.8 -> 97.35 mid); multi-token, unscoreable */
    { tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', side: 'BUY', retPx: 0.775 }, /* NVDA-2nd-July add — accumulate zone (≤75¢) gone; the account is distributing at 85–87¢ per Sells #2 */
    { tok: '', side: 'BUY', retPx: 0 }, /* December under-parity basket — leak closed overnight (94.45 -> 99.8 mid); multi-token, unscoreable */
    { tok: '', side: 'BUY', retPx: 0 }, /* Second-place August pair — pair repriced to 94-95c vs 96.5 fair, edge < 5 pts; multi-token, unscoreable */
    { tok: '99989724583763374403799114487538400642955271680502705587990647202176759344135', side: 'BUY', retPx: 0.84 }, /* GOOGL-3rd-Aug carry — GOOGL closed to 12.2% behind NVDA; fair fell 94.8 -> 88.4, edge < 5 at the 85c ask */
    { tok: '102965342134187381913982590329414198291915202774878597893115242870459924108426', side: 'BUY', retPx: 0.0915 }, /* Cease add — price ran 31% past the card's own 7.0c limit; the Sells trim card owns the leg now */
    { tok: '79162765079028727202719931536645059951675772849915793147357039418708378144838', side: 'BUY', retPx: 0.935 }, /* Apple-2nd-July NO add — 4.7 pts at the 95c executable, under the 5-pt bar with 2 sessions left */
    { tok: '', side: 'BUY', retPx: 0 }, /* July carry re-entry (BTC $57.5k NO + SPY $700 NO) — decayed to 0.2/1.3 pts at the asks with resolution Aug 1; multi-token, unscoreable */
    { tok: '22227957563975750716653233638849839957651843503812478121278991305586251655238', side: 'BUY', retPx: 0.335 }, /* NVDA-2nd-Aug YES add — thesis inverted by the Jul 30 print; stub sold at 40.9c */
    { tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', side: 'BUY', retPx: 0.3015 } /* NVDA-2nd-July YES 94.3c carry — collapsed to ~30c on the re-flip; never filled */
  ]; /* {tok, side ('BUY'|'SELL'), retPx} — indices align with #retired-body rows' data-retired-* attrs */
  function refreshRetired() {
    RETIRED.forEach(function (t, i) {
      fetch('https://clob.polymarket.com/midpoint?token_id=' + t.tok)
        .then(function (r) { return r.json(); })
        .then(function (j) {
          var cur = parseFloat(j.mid);
          if (isNaN(cur) || !t.retPx) return;
          var nowEl = $('[data-retired-now="' + i + '"]');
          if (nowEl) nowEl.textContent = (cur * 100).toFixed(1) + '\u00A2';
          var mv = (cur - t.retPx) / t.retPx * 100;
          var goodDrop = t.side === 'BUY' ? mv <= 0 : mv >= 0;
          var mEl = $('[data-retired-move="' + i + '"]');
          if (mEl) {
            mEl.textContent = (mv >= 0 ? '+' : '\u2212') + Math.abs(mv).toFixed(1) + '%';
            mEl.className = 'col-num ' + (goodDrop ? 'pm-pos' : 'pm-neg');
          }
          var vEl = $('[data-retired-verdict="' + i + '"]');
          if (vEl) {
            if (Math.abs(mv) < 5) { vEl.className = 'pm-badge pm-fair'; vEl.textContent = 'FLAT'; }
            else if (goodDrop) { vEl.className = 'pm-badge pm-cheap'; vEl.textContent = 'GOOD DROP'; }
            else { vEl.className = 'pm-badge pm-rich'; vEl.textContent = 'TOO EARLY'; }
          }
        }).catch(function () {});
    });
  }

  /* ---------- idea-scroller arrows ---------- */
  var scrollerUpdates = [];
  function initScrollers() {
    $$('.pm-cards').forEach(function (pc) {
      var n = pc.children.length;
      if (n <= 4) return;
      var sec = pc.closest('section'); if (!sec) return;
      var hdr = sec.querySelector('.table-header-row'); if (!hdr) return;
      var ctl = document.createElement('span');
      ctl.className = 'pm-scroll-ctl';
      ctl.innerHTML = '<button class="pm-scroll-btn" aria-label="Previous ideas">\u2039</button><span class="pm-scroll-pos"></span><button class="pm-scroll-btn" aria-label="More ideas">\u203A</button>';
      hdr.appendChild(ctl);
      var btns = ctl.querySelectorAll('button');
      var pos = ctl.querySelector('.pm-scroll-pos');
      function cardStep() {
        var c = pc.children[0];
        var w = c ? c.getBoundingClientRect().width : 0;
        return (w > 0 ? w : 300) + 16;
      }
      function update() {
        var step = cardStep();
        var first = Math.round(pc.scrollLeft / step) + 1;
        var last = Math.min(first + 3, n);
        pos.textContent = first + '\u2013' + last + ' / ' + n;
        btns[0].disabled = pc.scrollLeft <= 4;
        btns[1].disabled = pc.clientWidth > 0 && pc.scrollLeft >= pc.scrollWidth - pc.clientWidth - 4;
      }
      function page(dir) {
        var step = cardStep();
        var max = pc.scrollWidth - pc.clientWidth;
        var target = Math.max(0, Math.min(max, pc.scrollLeft + dir * step * 4));
        if (typeof pc.scrollTo === 'function') {
          try { pc.scrollTo({ left: target, behavior: 'smooth' }); } catch (e) { pc.scrollLeft = target; }
        } else { pc.scrollLeft = target; }
        setTimeout(update, 450);
      }
      btns[0].addEventListener('click', function (e) { e.preventDefault(); page(-1); });
      btns[1].addEventListener('click', function (e) { e.preventDefault(); page(1); });
      pc.addEventListener('scroll', function () { requestAnimationFrame(update); });
      scrollerUpdates.push(update);
      update();
    });
  }

  /* ---------- wiring ---------- */
  var chartsBuiltVisible = false;
  $$('.page-nav .nav-tab[data-view]').forEach(function (tab) {
    tab.addEventListener('click', function (e) {
      e.preventDefault();
      $$('.page-nav .nav-tab[data-view]').forEach(function (t) { t.classList.remove('active'); });
      tab.classList.add('active');
      var view = tab.getAttribute('data-view');
      ['polymarket', 'largest', 'tracking'].forEach(function (v) {
        var el = document.getElementById('view-' + v);
        if (el) el.hidden = v !== view;
      });
      if (view === 'largest' && !chartsBuiltVisible) {
        chartsBuiltVisible = true;
        requestAnimationFrame(buildCharts);
      }
      requestAnimationFrame(function () { scrollerUpdates.forEach(function (u) { u(); }); });
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
  initAcctSort();
  initScrollers();
  var acctMoreBtn = document.getElementById('acct-more');
  if (acctMoreBtn) acctMoreBtn.addEventListener('click', function () { acctExpanded = !acctExpanded; applyAcctCollapse(); });
  applyAcctCollapse();
  buildCharts();
  refresh();
  refreshAccount();
  refreshTracking();
  refreshRetired();
  setInterval(refresh, 60000);
  setInterval(refreshAccount, 60000);
  setInterval(refreshTracking, 60000);
  setInterval(refreshRetired, 60000);
})();
