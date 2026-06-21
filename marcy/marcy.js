/* ============================================
   MARCY — listings render + mortgage calculator
   ============================================ */
(function () {
  'use strict';

  var ASSUME = { downPct: 20, taxRate: 0.009, insRate: 0.0012, pmiRate: 0.005 }; // annual rates of price/loan
  var fmt0 = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

  function parseNum(v) {
    var n = parseFloat(String(v == null ? '' : v).replace(/[^0-9.]/g, ''));
    return isNaN(n) ? 0 : n;
  }
  function $(id) { return document.getElementById(id); }

  /* ---------- Listings ---------- */
  function zillowUrl(l) {
    return 'https://www.zillow.com/homes/' + encodeURIComponent(l.address + ', Seattle, WA ' + l.zip) + '_rb/';
  }

  function filterAndSort() {
    var price = ($('f-price') || {}).value || 'any';
    var beds = parseNum(($('f-beds') || {}).value);
    var type = ($('f-type') || {}).value || 'any';
    var sort = ($('listing-sort') || {}).value || 'new';

    var list = MARCY_LISTINGS.filter(function (l) {
      if (beds && l.beds < beds) return false;
      if (type !== 'any' && l.type !== type) return false;
      if (price === 'lt1' && l.price >= 1000000) return false;
      if (price === '1to2' && (l.price < 1000000 || l.price > 2000000)) return false;
      if (price === 'gt2' && l.price <= 2000000) return false;
      return true;
    });
    if (sort === 'price-asc') list.sort(function (a, b) { return a.price - b.price; });
    else if (sort === 'price-desc') list.sort(function (a, b) { return b.price - a.price; });
    else list.sort(function (a, b) { return (a.status === 'New' ? 0 : 1) - (b.status === 'New' ? 0 : 1); });
    return list;
  }

  var HOUSE_SVG = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>';

  function renderListings() {
    var rail = $('marcy-listings');
    if (!rail) return;
    var list = filterAndSort();
    if (!list.length) {
      rail.innerHTML = '<div class="listing-empty">No listings match these filters.</div>';
    } else {
      rail.innerHTML = list.map(function (l) {
        var badge = l.status === 'New'
          ? '<span class="listing-badge badge-new">New</span>'
          : '<span class="listing-badge badge-active">Active</span>';
        var photo = HOUSE_SVG + (l.photo
          ? '<img src="' + l.photo + '" alt="' + l.address + '" loading="lazy" onerror="this.remove()">'
          : '');
        var spec = l.beds + ' bd · ' + l.baths + ' ba · ' + l.sqft.toLocaleString() + ' sqft';
        return '' +
          '<article class="card listing">' +
            '<div class="listing-photo">' + photo + badge + '</div>' +
            '<div class="listing-body">' +
              '<div class="listing-price">' + fmt0.format(l.price) + '</div>' +
              '<div class="listing-addr">' + l.address + '</div>' +
              '<div class="listing-blurb">' + (l.blurb || '') + '</div>' +
              '<div class="listing-spec">' + spec + '</div>' +
              '<div class="listing-actions">' +
                '<button type="button" class="btn-mortgage" data-id="' + l.id + '">Show Mortgage</button>' +
                '<a class="listing-link" href="' + zillowUrl(l) + '" target="_blank" rel="noopener">Details &#8599;</a>' +
              '</div>' +
            '</div>' +
          '</article>';
      }).join('');
    }
    var count = $('listing-count');
    if (count) count.textContent = list.length + (list.length === 1 ? ' home' : ' homes');
    rail.scrollLeft = 0;
  }

  /* ---------- Calculator ---------- */
  function activeTermYears() {
    var btn = document.querySelector('.term-btn.active');
    return btn ? parseNum(btn.getAttribute('data-years')) : 30;
  }

  // Auto-estimate PMI: ~0.5%/yr of the loan when down payment is under 20%, else 0.
  function setPMI() {
    var P = parseNum($('m-price').value);
    var down = parseNum($('m-downd').value);
    var pct = P > 0 ? down / P * 100 : 100;
    var loan = Math.max(P - down, 0);
    var pmi = pct < 20 ? Math.round(loan * ASSUME.pmiRate / 12) : 0;
    $('m-pmi').value = fmt0.format(pmi);
  }

  function applyListing(l, scroll) {
    $('m-price').value = fmt0.format(l.price);
    $('m-downp').value = ASSUME.downPct + '%';
    $('m-downd').value = fmt0.format(Math.round(l.price * ASSUME.downPct / 100));
    $('m-tax').value = fmt0.format(Math.round(l.price * ASSUME.taxRate));
    $('m-ins').value = fmt0.format(Math.round(l.price * ASSUME.insRate));
    $('m-hoa').value = '$0';
    setPMI();
    var src = $('m-source');
    if (src) src.textContent = 'Estimating ' + l.address + ' · ' + ASSUME.downPct + '% down';
    recalc();
    if (scroll) {
      var calc = $('calc');
      if (calc) calc.scrollIntoView({ behavior: 'smooth', block: 'start' });
      var card = document.querySelector('.calc-results');
      if (card) { card.classList.remove('calc-flash'); void card.offsetWidth; card.classList.add('calc-flash'); }
    }
  }

  function recalc() {
    var P = parseNum($('m-price').value);
    var down = parseNum($('m-downd').value);
    var rate = parseNum($('m-rate').value);
    var tax = parseNum($('m-tax').value);
    var ins = parseNum($('m-ins').value);
    var hoa = parseNum($('m-hoa').value);
    var pmi = parseNum($('m-pmi').value);

    var n = activeTermYears() * 12;
    var L = Math.max(P - down, 0);
    var r = rate / 100 / 12;
    var pi = r > 0 ? (L * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1) : (n > 0 ? L / n : 0);
    var taxMo = tax / 12, insMo = ins / 12, other = hoa + pmi;
    var total = pi + taxMo + insMo + other;

    $('m-payment').textContent = fmt0.format(total);
    $('leg-pi').textContent = fmt0.format(pi);
    $('leg-tax').textContent = fmt0.format(taxMo);
    $('leg-ins').textContent = fmt0.format(insMo);
    $('leg-ot').textContent = fmt0.format(other);
    $('m-loan').textContent = fmt0.format(L);
    $('m-interest').textContent = fmt0.format(Math.max(pi * n - L, 0));
    $('m-totalpaid').textContent = fmt0.format(total * n);

    updateDonut([pi, taxMo, insMo, other]);
    buildAmort(L, r, pi, n);
  }

  function buildAmort(L, r, pi, n) {
    var body = $('m-amort-body');
    if (!body) return;
    if (L <= 0 || n <= 0) { body.innerHTML = ''; return; }
    var balance = L, yr = 1, yrP = 0, yrI = 0, rows = [];
    for (var m = 1; m <= n; m++) {
      var interest = balance * r;
      var principal = Math.min(pi - interest, balance);
      balance -= principal;
      yrP += principal; yrI += interest;
      if (m % 12 === 0 || m === n) {
        rows.push('<tr><td>' + yr + '</td><td>' + fmt0.format(yrP) + '</td><td>' + fmt0.format(yrI) + '</td><td>' + fmt0.format(Math.max(balance, 0)) + '</td></tr>');
        yr++; yrP = 0; yrI = 0;
      }
    }
    body.innerHTML = rows.join('');
  }

  /* ---------- Donut ---------- */
  var donut = null;
  function themeColors() {
    var cs = getComputedStyle(document.documentElement);
    return [
      cs.getPropertyValue('--color-primary').trim() || '#00d4ff',
      cs.getPropertyValue('--color-warning').trim() || '#ffab40',
      cs.getPropertyValue('--color-gain').trim() || '#00d68f',
      cs.getPropertyValue('--color-text-faint').trim() || '#4d5d82'
    ];
  }
  function paintLegendDots(colors) {
    ['dot-pi', 'dot-tax', 'dot-ins', 'dot-ot'].forEach(function (id, i) {
      var el = $(id); if (el) el.style.background = colors[i];
    });
  }
  function initDonut() {
    var ctx = $('m-donut');
    if (!ctx || typeof Chart === 'undefined') return;
    var colors = themeColors();
    paintLegendDots(colors);
    donut = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Principal & interest', 'Property tax', 'Insurance', 'HOA + PMI'],
        datasets: [{ data: [0, 0, 0, 0], backgroundColor: colors, borderWidth: 0 }]
      },
      options: {
        responsive: true, maintainAspectRatio: false, cutout: '68%',
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: function (c) { return c.label + ': ' + fmt0.format(c.parsed) + '/mo'; } } }
        }
      }
    });
  }
  function updateDonut(data) {
    if (!donut) return;
    donut.data.datasets[0].data = data.map(function (v) { return Math.round(v); });
    donut.update();
  }
  function refreshDonutColors() {
    var colors = themeColors();
    paintLegendDots(colors);
    if (donut) { donut.data.datasets[0].backgroundColor = colors; donut.update(); }
  }

  /* ---------- Theme toggle (matches the rest of the site) ---------- */
  var SUN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
  var MOON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  function initTheme() {
    var toggle = document.querySelector('[data-theme-toggle]');
    var root = document.documentElement;
    var theme = root.getAttribute('data-theme') || 'dark';
    if (!toggle) return;
    toggle.innerHTML = theme === 'dark' ? SUN : MOON;
    toggle.addEventListener('click', function () {
      theme = theme === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', theme);
      toggle.setAttribute('aria-label', 'Switch to ' + (theme === 'dark' ? 'light' : 'dark') + ' mode');
      toggle.innerHTML = theme === 'dark' ? SUN : MOON;
      refreshDonutColors();
    });
  }

  /* ---------- Wiring ---------- */
  function bind() {
    var rail = $('marcy-listings');
    if (rail) rail.addEventListener('click', function (e) {
      var btn = e.target.closest('.btn-mortgage');
      if (!btn) return;
      var l = MARCY_LISTINGS.find(function (x) { return x.id === btn.getAttribute('data-id'); });
      if (l) applyListing(l, true);
    });

    ['f-price', 'f-beds', 'f-type', 'listing-sort'].forEach(function (id) {
      var el = $(id); if (el) el.addEventListener('change', renderListings);
    });

    var amt = 310;
    var prev = $('rail-prev'), next = $('rail-next');
    if (prev) prev.addEventListener('click', function () { rail.scrollBy({ left: -amt, behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { rail.scrollBy({ left: amt, behavior: 'smooth' }); });

    $('m-price').addEventListener('input', function () {
      var P = parseNum($('m-price').value), pct = parseNum($('m-downp').value);
      $('m-downd').value = fmt0.format(Math.round(P * pct / 100));
      setPMI(); recalc();
    });
    $('m-downd').addEventListener('input', function () {
      var P = parseNum($('m-price').value), d = parseNum($('m-downd').value);
      $('m-downp').value = (P > 0 ? Math.round(d / P * 1000) / 10 : 0) + '%';
      setPMI(); recalc();
    });
    $('m-downp').addEventListener('input', function () {
      var P = parseNum($('m-price').value), pct = parseNum($('m-downp').value);
      $('m-downd').value = fmt0.format(Math.round(P * pct / 100));
      setPMI(); recalc();
    });
    ['m-rate', 'm-tax', 'm-ins', 'm-hoa', 'm-pmi'].forEach(function (id) {
      $(id).addEventListener('input', recalc);
    });

    document.querySelectorAll('.term-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('.term-btn').forEach(function (x) { x.classList.remove('active'); });
        b.classList.add('active');
        recalc();
      });
    });

    var amortBtn = $('m-amort-btn');
    if (amortBtn) amortBtn.addEventListener('click', function () {
      var wrap = $('m-amort-wrap');
      wrap.hidden = !wrap.hidden;
      amortBtn.textContent = wrap.hidden ? 'View amortization schedule' : 'Hide amortization schedule';
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    renderListings();
    initDonut();
    bind();
    if (MARCY_LISTINGS && MARCY_LISTINGS.length) applyListing(MARCY_LISTINGS[0], false);
  });
})();
