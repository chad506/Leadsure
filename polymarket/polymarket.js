/* ==== baked odds history (daily CLOB closes, Jun 27 2026 onward; FRIDAY pre-open walk Aug 28 13:23 UTC re-read the 'now' point with caps frozen at the Aug 27 closes — NVDA $227.98 ($5,517.1B) vs AAPL $4,620.3B / GOOGL $4,147.3B, lead 19.41% / $896.8B; T 2/23/87: fairs Dec NVDA 78.68 / AAPL 15.55 / GOOGL 4.12 on a 0.75 small-leg allowance — the December book held its overshoot (dec-NVDA 80.5, +1.82) while dec-GOOGL walked to 8.5 (+4.38, the complex's largest residual) and dec-AAPL sat at 11.15 (-4.40, 0.60 from the re-entry bar) ==== */
(function () {
  'use strict';

  /* ==== baked odds history (daily CLOB closes, Jun 27 2026 onward; FRIDAY pre-open walk Aug 28 13:23 UTC re-read the 'now' point — caps frozen at the Aug 27 closes (NVDA $5,517.1B / AAPL $4,620.3B / GOOGL $4,147.3B, lead 19.41% / $896.8B), dec mids 80.5/11.15/8.5/0.45 vs fairs 78.68/15.55/4.12 — dec-NVDA +1.82 still over its fair, dec-AAPL -4.40 under, dec-GOOGL +4.38 the widest residual; July legs frozen) ==== */
  var H = {
    decNVDA: [0.725,0.725,0.62,0.645,0.655,0.605,0.585,0.605,0.615,0.595,0.635,0.655,0.655,0.685,0.695,0.705,0.665,0.72,0.655,0.615,0.52,0.555,0.545,0.605,0.61,0.615,0.645,0.625,0.565,0.575,0.51,0.485,0.485,0.575,0.705,0.695,0.725,0.735,0.805],
    decAAPL: [0.082,0.082,0.0965,0.095,0.108,0.1475,0.143,0.132,0.158,0.1555,0.1705,0.1265,0.1265,0.1405,0.1305,0.13,0.1705,0.1285,0.143,0.2285,0.345,0.328,0.3305,0.235,0.2025,0.1985,0.1985,0.2565,0.2995,0.281,0.353,0.289,0.3565,0.251,0.1645,0.1405,0.1435,0.141,0.1115],
    decGOOGL: [0.115,0.115,0.155,0.165,0.16,0.155,0.165,0.175,0.165,0.165,0.165,0.155,0.155,0.145,0.145,0.145,0.12,0.105,0.12,0.125,0.105,0.105,0.105,0.105,0.125,0.105,0.105,0.105,0.095,0.095,0.105,0.135,0.145,0.13,0.105,0.125,0.115,0.125,0.085],
    decSPCX: [0.0395,0.0395,0.0355,0.023,0.0225,0.0215,0.027,0.027,0.0235,0.0215,0.0205,0.022,0.0215,0.0185,0.02,0.019,0.0145,0.0135,0.0125,0.012,0.0085,0.0085,0.0085,0.0085,0.009,0.0095,0.0115,0.0125,0.015,0.0105,0.0095,0.017,0.0155,0.0175,0.0115,0.011,0.0115,0.0115,0.0045]
  };
  /* The September rank books listed Jul 29 and this page began recording them on
     Aug 10 (post-close walk, fetched 00:40 UTC Aug 11 — the first print), so the
     series grows one point per run (twenty-seventh print: Aug 28 FRIDAY pre-open
     walk, books fetched 13:23 UTC — the seat ran ON through its own fair overnight:
     sep2AAPL 81.5 -> 85.5 (+4.0, matching the series' second-largest jump) against
     an unmoved 83.15 fair — the fade that retired at +0.98 now reads +2.35 the
     OTHER way; sep2GOOGL 12.5 -> 9.5 (-3.0) under its 12.70 fair, sep2NVDA held
     6.5 vs 3.25. Seeded, not back-filled — no synthetic history. */
  var SEPH = { sep2AAPL: [0.585,0.565,0.575,0.49,0.51,0.53,0.53,0.565,0.545,0.57,0.57,0.54,0.545,0.57,0.57,0.675,0.645,0.745,0.77,0.805,0.755,0.755,0.755,0.765,0.805,0.815,0.855], sep2GOOGL: [0.31,0.315,0.315,0.32,0.325,0.34,0.34,0.34,0.34,0.34,0.34,0.375,0.36,0.395,0.36,0.265,0.25,0.21,0.18,0.165,0.195,0.21,0.21,0.195,0.14,0.125,0.095], sep2NVDA: [0.085,0.08,0.08,0.095,0.085,0.085,0.08,0.085,0.08,0.075,0.075,0.08,0.075,0.07,0.07,0.05,0.05,0.05,0.05,0.045,0.045,0.045,0.045,0.05,0.07,0.065,0.065] };
  var SEP_LABELS = ['8/10', '8/11', '8/11 PM', '8/12', '8/12 PM', '8/13', '8/13 PM', '8/14', '8/14 PM', '8/15', '8/15 PM', '8/16', '8/16 PM', '8/17', '8/17 PM', '8/18 PM', '8/18 LATE', '8/19', '8/20', '8/20 PM', '8/21', '8/22', '8/22 PM', '8/23', '8/27', '8/27 PM', '8/28'];

  var LABELS = (function () {
    var out = [], d = new Date(Date.UTC(2026, 5, 27));
    for (var i = 0; i < 38; i++) {
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
    /* Bitcoin tab — Aug 21 2026: August monthly ladder + 'before 2027' ladder, YES tokens */
    'btc-aug-re80k': '102270650225797845195454805763498397874386067232149902550118294787057200324741',
    'btc-aug-re82_5k': '58559007481908595732343519640998477965598707756438174409311033318259996889965',
    'btc-aug-re85k': '112241751071174396487292868128075924275858867204192436670566953710907627910138',
    'btc-aug-re87_5k': '58934772812121845536960060739940872473706732919207396740821739825921647791275',
    'btc-aug-re90k': '72739316523858479816906805619832308458888360975886863074336484009500930856438',
    'btc-aug-re100k': '18258395755041392118198940898057846234774760894152262988568951221464458542850',
    'btc-aug-di75k': '52967959241395817429602158891216394752909947915176073432962965400546600207163',
    'btc-aug-di72_5k': '79697021471149273297867285272226524165531438782155382582295930999430106675621',
    'btc-aug-di70k': '12441167212229750268659752951509231773978449399558023877007225411177778794121',
    'btc-aug-di67_5k': '45349201673033527447768645359864385869991777646128023206959790874029348120325',
    'btc-aug-di65k': '43898757872820987638297146930820621323643875433360934741436059076419637367671',
    'btc-aug-di62_5k': '97454153157320890301565733152088528189410505166162922730489352561967591530343',
    'btc-aug-di60k': '88902974378195889166057110964513688920047250482309636378282580896757420591128',
    'btc-aug-di57_5k': '105934924793101961671194607931144938442778142774865876808979595111561162727678',
    'btc-aug-di55k': '70459296325871889453156773347249996978545476708208151499368447748521658358017',
    'btc-aug-di52_5k': '55524689612005448388368447943683952282193574718980087284475487813080937536215',
    'btc-aug-di50k': '74739074909584676497787401686892858852610063847464192700752443429685992559595',
    'btc-aug-di47_5k': '38047243640275994623018060409505748484658089693620691895063154581347365967394',
    'btc-aug-di45k': '37046509536395159361335902951771808094145892190769810696385162495774938829015',
    'btc-aug-di42_5k': '108302454607081176309311291655387968923267938167375542356953661581919615932612',
    'btc-aug-di40k': '80229713107491604988166227575420811552403620778847461006375175585272053257376',
    'btc-dec-re80k': '93924969469939330995194645669345334142528685509853517456507765752635309176671',
    'btc-dec-re85k': '27201221676173593121678787264361008606480627771007041356248031697735484721466',
    'btc-dec-re90k': '89384721767526056909881321094852287855436067743554155484781205764118128944311',
    'btc-dec-re95k': '37011650970792437921328530439273985710481032638212715110420998355785945483754',
    'btc-dec-re100k': '56078938060096976448086754249497300447360333783952000147427828224794011030104',
    'btc-dec-re110k': '74843373582432484858627201602003648342208168490128239235522790524493414154441',
    'btc-dec-re120k': '65965214225073605704712365855887384729237451947822407248598722221769498441791',
    'btc-dec-re130k': '106722178102302988256241610384561546855057790384749278490135208236665942286983',
    'btc-dec-re140k': '71296910957902084356560391757722633648005498400799774895345285101862220728868',
    'btc-dec-re150k': '9408196828451163378822245032645030045707991112669125056198742225498158094445',
    'btc-dec-re160k': '82383148892491951057986758727379275490538136042110607950765593149629854993897',
    'btc-dec-re170k': '91771200478987002878887468575926960041640880090910228629453422737528263499583',
    'btc-dec-re180k': '74565691184914883284595890202312045107598400454020809925536957708002527360857',
    'btc-dec-re190k': '44277901818108806761236452190579702355420207259376614876965091268791774916719',
    'btc-dec-re200k': '61368943128255287414565270336856615453000675377332178800733742873558311943412',
    'btc-dec-re250k': '13433573766910980267981622064090484781359464703732825845886677588040916221533',
    'btc-dec-re500k': '91920414851381703961459336798965934286338468050347816160274927361190904665656',
    'btc-dec-re1000k': '18571303954259773157233385333455041418270179723020753158306812650937565180666',
    'btc-dec-di60k': '104279604547231872129402198190232956636095665469278761891693384128061158683041',
    'btc-dec-di55k': '115462087336983275104521488923966022755348986822352694745153736621832003960847',
    'btc-dec-di50k': '13887983551129862992605123088744175927084435631400400451585519366058907542147',
    'btc-dec-di45k': '9894510651052373088408067031031513212801618531203062911959630395716258202132',
    'btc-dec-di40k': '4255890554350661695724949176183233033027635903850796430457642328613772591960',
    'btc-dec-di35k': '19830138103155427354579425893303398904208550475895360582465715721785944321950',
    'btc-dec-di30k': '32100646597103151520708930825184762124585961199171649862922931416837210460836',
    'btc-dec-di25k': '58908160299895538838177673280060816284346493901538403975218911918392404378292',
    'btc-dec-di20k': '59683974246799525831244219921114455736275705032978487912646746315061494194144',
    'btc-dec-di15k': '63985397218239656926367525871649971575041102854345777114360978052613472299768',
    'btc-dec-di10k': '42439528758178981890895605039938161151582654744978607695897321288347422769852',
    'btc-dec-di5k': '78813286502861287035170675523688055494398144118547987619022209059970667952352',
    'sep-sep2AAPL': '69436436951640881186918962093978129047876125081246052069821867405322712154087',
    'sep-sep2GOOGL': '112917653797517457474191727734311838332458686889832634273844237276119071933739',
    'sep-sep2NVDA': '58255742710354753372638105507395301856276470581760095695579319734210276720718',
    'sep-sep3AAPL': '112996809883883766789820608824059367455551434396689079529794719824285513465225',
    'sep-sep3NVDA': '6369142801468538078435462495249654721381776375778296596920715169671444692617',
    'sep-sepGOOGL': '11286203532633435050461029087857565736892531921887062202100644346193481478173',
    'aug-NVDA': '95302905537962222918309360338213500184994944787102722256843629723110588711061',
    'aug-AAPL': '42047893977785728528565456844873223397500118970867834014836006695082853076308',
    'aug-GOOGL': '93997509898554464206013458433253360996772270234627522008621917049464308684354',
    'aug-AMZN': '72944522118038991341395250874399215676648471148370200768137239415303143807574',
    'aug-AVGO': '89566957160121255224944240803366911709563437585650671117746762646052979044895',
    'dec-NVDA': '11876606915924142133615854761923277060697657209957870741155164849437788272266',
    'dec-AAPL': '9875273331604434310973374077817381730908757452538191940842519381772366848',
    'dec-GOOGL': '62009449847159122385971991480139610869824965029008686522071073076098387124747',
    'dec-SPCX': '34376240305139645452191650383029377919496221975523712782933090732539681434119',
    'dec-TSLA': '50967548204329017987830198881678379324925229642745345006556239550086450305683',
    /* Treasuries tab (6% long-bond scenario) */
    'trs-10y48': '57813774524155463423838033259397133747187306761649300584910471142751787047106',
    'trs-10y50': '22397766228589110871783272985290872433765236471932774952155419500943165057456',
    'trs-10y52': '70090363170367815297146294007692529992906189341824085184699164213923074932193',
    'trs-10y55': '108315584853799729838614333748063377472256875592940383916811669252949563879956',
    'trs-10y57': '19807745274820218436318664068726385243490453006769046292026430944247457642518',
    'trs-10y60': '33659372827600316727835785655881220724422400527200618608139639039116681963297',
    'trs-nocuts': '12403602920039269077597917340921667997547115084613238528792639013246536343316',
    'trs-sephike': '63842529068710005716169325380315470359047749786610778647370693404952498013178',
    'trs-dechike': '111662129652828266889360374468657435151479595863413519836161861837506140152890',
    'trs-hike26': '75028752776148090296091099469912621384650554615761384992997579209329182670110',
    'trs-spx6200': '49955818039428095386956976055681140865441561732095652149645714273344189549953',
    'trs-spx5800': '34357288327330056667349828087095149953359155962095457849915526561277102684498',
    'trs-spx5200': '43862694280485931410720845136506753152245240145650454010850206036552462953242',
    'trs-gold5k': '25472502502236710744675799561400967135875595061119902215625578202260735017994',
    'trs-gold6k': '79773570476744632615747480307256906441402089435470166694872527952303027818942',
    'trs-stagf': '29221647660001052534885426446639848390010824454348882014638265430112051361512',
    'trs-emerg': '8618184031231342643840589970076443003283607991865226846156174312081261691762',
    'trs-recess': '100379208559626151022751801118534484742123694725746262280150222742563282755057',
    'trs-cpi45': '74673761985513157199971989678705947308950428080518161992747749503329915181832',
    'trs-mort7': '83519912354085399762068008706537393573148541011886846818970046660026074594792'
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

  /* ---------- EXACT-RANK MODEL (adopted Aug 1 2026 PM — replaces the pairwise plug) ----------
     These books resolve on "is X the LARGEST company", not on "does X pass today's leader".
     The old formula priced the second event: challenger = P(chal > lead), leader = 100 − Σ(challengers).
     That is a union bound, and it double-counts overtakes: P(A passes ∪ G passes) < P(A) + P(G),
     because a bad NVDA draw pushes everyone past it at once. The plug absorbed the whole error,
     The residual made the leader biased LOW — by 6.3 pts in August and 24.5 in December — and, contrary to how this
     was first written up, the CHALLENGERS carried an equal and opposite error (Dec: AAPL +9.2, GOOGL +10.9, MSFT +3.8,
     AMZN +0.6, summing to the leader's 24.5). Every leg was wrong, not just the plug.
     Correct version, same diffusion: give every name idiosyncratic log-vol σ/√2 so the log-RATIO
     of any pair keeps the published σ = 2%/day (any common market factor cancels in a ranking),
     then integrate P(X is the max) over X's own shock:
         P(X largest) = ∫ φ(z) Π_{j≠X} Φ( [ln(cX/cj) + s·z] / s ) dz,   s = (σ/√2)·√T
     Simpson, 481 nodes on [-8, 8]; agrees with a 3 M-path Monte Carlo to within simulation noise and -
     unlike the old formula - the legs sum to 100 by construction instead of by subtraction. Scaled down
     by the untracked small legs, read off THEIR OWN books (see SMALL below), so the modelled set shares
     the rest.
     KNOWN LIMIT: sigma = 2%/day was only ever calibrated on the four leader-vs-challenger pairs. This
     integral needs all ten pairs and the six challenger-vs-challenger vols are free parameters. Sweeping
     them 1.3-2.8%/day moves Dec NVDA over 41.8-55.8 and NVDA-2nd-Aug over 16.1-26.0 - a wider band than
     the disclosed sigma=3% case. Disclosed in the methodology box; do not quote these fairs as precise. */
  function rankFair(caps, syms, td, smallLegs) {
    var s = (SIGMA / Math.SQRT2) * Math.sqrt(td);
    var N = 481, a = -8, h = 16 / (N - 1), scale = 1 - (smallLegs || 0) / 100, out = {};
    var W = [], Z = [];
    for (var k = 0; k < N; k++) {
      var z = a + k * h;
      Z.push(z);
      W.push((k === 0 || k === N - 1) ? 1 : (k % 2 ? 4 : 2));
    }
    syms.forEach(function (t) {
      var tot = 0;
      for (var k2 = 0; k2 < N; k2++) {
        var z2 = Z[k2], pr = Math.exp(-0.5 * z2 * z2) / Math.sqrt(2 * Math.PI);
        for (var j = 0; j < syms.length; j++) {
          if (syms[j] === t) continue;
          pr *= phi((Math.log(caps[t] / caps[syms[j]]) + s * z2) / s);
        }
        tot += W[k2] * pr;
      }
      out[t] = tot * h / 3 * 100 * scale;
    });
    return out;
  }

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
        .then(function (j) { mids[k] = parseFloat(j.mid); })
        .catch(function () { /* leave baked value for this token */ });
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
      try { updateTrs(mids); } catch (e) { /* never break the shared refresh */ }
      try { updateBtc(mids); } catch (e) { /* never break the shared refresh */ }
      /* caps + gaps */
      if (caps.NVDA) {
        var leadCap = Math.max.apply(null, Object.keys(caps).map(function (k2) { return caps[k2]; }));
        Object.keys(caps).forEach(function (sym) {
          $$('[data-cap^="' + sym + '"]').forEach(function (el) { el.textContent = caps[sym].toLocaleString('en-US', { maximumFractionDigits: 1 }); });
          var gap = (leadCap / caps[sym] - 1) * 100;
          $$('[data-gap^="' + sym + '"]').forEach(function (el) { el.textContent = gap < 0.005 ? '\u2014' : gap.toFixed(2) + '%'; });
        });
        if (caps.AAPL) {
          /* Aug 4 2026: Alphabet passed Apple — the #2 slot must be computed over ALL quoted names, not assumed AAPL/NVDA */
          var NAMES = { NVDA: 'NVIDIA', AAPL: 'Apple', GOOGL: 'Alphabet', MSFT: 'Microsoft', AMZN: 'Amazon', AVGO: 'Broadcom', TSLA: 'Tesla' };
          var ranked = Object.keys(caps).sort(function (x, y) { return caps[y] - caps[x]; });
          var lead = ranked[0], chal = ranked[1];
          setText('#hero-lead-label', 'Current #1 \u00B7 ' + (NAMES[lead] || lead));
          setText('#hero-chal-label', '#2 ' + (NAMES[chal] || chal)); /* Aug 5 PM: Apple re-took #2 — the slot is computed, no baked NEW tag */
          setText('#hero-lead-cap', '$' + (caps[lead] / 1000).toFixed(3) + 'T');
          setText('#hero-chal-cap', '$' + (caps[chal] / 1000).toFixed(3) + 'T');
          setText('#hero-gap', ((caps[lead] / caps[chal] - 1) * 100).toFixed(2) + '% \u00B7 $' + Math.round(caps[lead] - caps[chal]) + 'B');
        }
        /* model fair + edge per date — EXACT-RANK: P(sym is the largest), not P(sym passes today's
           leader). See rankFair() above for why the old pairwise plug was biased. */
        var edgeList = [];
        var RACE = ['AAPL', 'NVDA', 'GOOGL', 'MSFT', 'AMZN'];
        var SMALL = { jul: 0.15, aug: 0.45, dec: 0.80 }; /* untracked competitors, taken from THEIR OWN books, not guessed:
             aug = Tesla 0.15 + Aramco 0.25 + Broadcom 0.05 (Aug legs' own books re-read where quoted; Microsoft and Amazon are tracked names, not small legs);
             dec = Tesla 0.15 + SpaceX 0.45 + Aramco 0.15 (re-read Aug 28 13:23Z off their OWN books — SpaceX eased another half-tick overnight, total 0.75). Re-read every run — a mis-set allowance
             moves the leader leg by ~0.6 pt, which is an eighth of the edges this page trades on. */
        var live = RACE.filter(function (s) { return caps[s]; });
        /* a single failed quote would drop a name from the ranking and inflate every survivor
           (losing AAPL alone prints NVDA-Aug at 88 instead of 72) — keep the baked fairs instead */
        if (live.length < RACE.length) return;
        ['jul', 'aug', 'dec'].forEach(function (ev) {
          var td = tradingDaysTo(DEADLINES[ev]);
          setText('[data-days="' + ev + '"]', Math.round(td));
          var rf = rankFair(caps, live, td, SMALL[ev]);
          RACE.forEach(function (sym) {
            if (!caps[sym]) return;
            var key = ev + '-' + sym;
            if (!(key in TOKENS)) return;
            var f = rf[sym];
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
        var sums = { jul: 0.0015, aug: 0.0045, dec: 0.0030 }; /* untracked legs at their own mids: aug = TSLA+ARAMCO+MSFT 0.15c each; dec = ARAMCO 0.15 + AMZN 0.15 (re-read Aug 23 13:22Z off their own books) */
        Object.keys(mids).forEach(function (k) { if (!isNaN(mids[k])) sums[k.slice(0, 3)] += mids[k]; });
        ['jul', 'aug', 'dec'].forEach(function (ev) { setText('[data-sum="' + ev + '"]', (sums[ev] * 100).toFixed(2)); });
        /* hero AAPL odds (label reads "AAPL Odds Jul / Aug / Dec") */
        if (!isNaN(mids['aug-AAPL'])) setText('#hero-nvda-odds', (mids['aug-AAPL'] * 100).toFixed(1) + '% / ' + (mids['sep-sep2AAPL'] * 100).toFixed(1) + '% / ' + (mids['dec-AAPL'] * 100).toFixed(2) + '%');
      }
      lastTick = Date.now();
      var st = $('#sync-time');
      if (st) st.textContent = new Date(lastTick).toLocaleString([], { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', second: '2-digit' });
      setPills(true);
      fmtAgo();
    }).catch(function () {
      setPills(false);
      $('#last-updated').textContent = 'Snapshot · Aug 28, 2026 13:23 UTC — Friday pre-open walk (live APIs unreachable)';
      var st = $('#sync-time'); if (st) st.textContent = 'Aug 28, 2026 13:23 UTC — Friday pre-open walk: caps frozen at the Aug 27 closes (NVDA $227.98, lead 19.41%), sep2AAPL ran to 85.5 (+2.35 OVER its fair), BTC slipped to $79,275 giving the December anchor back to 29.5 (under the 30c line), and the window printed two resting-order sells at 99-99.9c ($360.33, rows 253-254); balances re-baked (baked snapshot — live APIs unreachable)';
    });
  }

  /* ---------- treasuries tab: live fair/edge/implied recompute ---------- */
  /* Aug 10 2026: the scenario decomposition (P6 x P|6% + (1-P6) x P|no-6%) is retired.
     Its P6 was two-thirds drift extrapolation off a coefficient with t = 0.84, and the
     per-row conditionals were hand-set. The ladder now carries two models that actually
     fit the 2026 series - a zero-drift random walk and a fitted AR(1) - and the fair is
     their equal-weight mixture. data-pc holds the martingale leg, data-pe the AR(1) leg.
     Rows with data-trs-nomodel have no yield model and are left alone: their mid still
     refreshes, but nothing pretends to price them. */
  function updateTrs(mids) {
    $$('#trs-table-body tr[data-trs-row]').forEach(function (row) {
      if (row.getAttribute('data-trs-nomodel')) return;
      var k = row.getAttribute('data-trs-row');
      var mid = mids[k];
      if (mid == null || isNaN(mid)) return;
      var pc = parseFloat(row.getAttribute('data-pc'));
      var pe = parseFloat(row.getAttribute('data-pe'));
      if (isNaN(pc) || isNaN(pe)) return;
      var fair = 0.5 * (pc + pe);
      var edge = mid - fair;
      var f = row.querySelector('[data-trs-fair]'); if (f) f.textContent = (fair * 100).toFixed(1) + '%';
      var e = row.querySelector('[data-trs-edge]');
      if (e) {
        e.textContent = (edge >= 0 ? '+' : '\u2212') + Math.abs(edge * 100).toFixed(1);
        e.className = 'col-num' + (edge <= -0.025 ? ' pm-pos' : '');
      }
      var v = row.querySelector('[data-trs-verdict]');
      if (v) {
        v.className = 'pm-badge ' + (edge <= -0.025 ? 'pm-cheap' : edge >= 0.025 ? 'pm-rich' : 'pm-fair');
        v.textContent = edge <= -0.025 ? 'CHEAP' : edge >= 0.025 ? 'RICH' : 'FAIR';
      }
    });
  }


  /* ---------- bitcoin tab: live edge/verdict recompute ----------
     Aug 21 2026. Each row bakes its σ2.35 reflection-principle fair in data-fair
     (a fraction); the mid refreshes live and edge = mid − fair is recomputed with the
     CHEAP ≤ −2.5 / RICH ≥ +2.5 thresholds at full precision — the same rule that baked the table, so the two agree at the baked mids (rounding first would flip Dec $25k, edge +2.4977); a row whose verdict flips live has its Value-rank cell replaced with 're-rank on next bake'. Rows with data-btc-tail are
     the sub-2¢ legs with no model resolution: their mid still refreshes, nothing else. */
  function updateBtc(mids) {
    $$('#btc-table-body tr[data-btc-row]').forEach(function (row) {
      if (row.getAttribute('data-btc-tail')) return;
      var k = row.getAttribute('data-btc-row');
      var mid = mids[k];
      if (mid == null || isNaN(mid)) return;
      var fair = parseFloat(row.getAttribute('data-fair'));
      if (isNaN(fair)) return;
      var edge = mid - fair;
      var f = row.querySelector('[data-btc-fair]'); if (f) f.textContent = (fair * 100).toFixed(1) + '%';
      var e = row.querySelector('[data-btc-edge]');
      if (e) {
        e.textContent = (edge >= 0 ? '+' : '\u2212') + Math.abs(edge * 100).toFixed(1);
        e.className = 'col-num' + (edge <= -0.025 ? ' pm-pos' : '');
      }
      var v = row.querySelector('[data-btc-verdict]');
      if (v) {
        var was = v.textContent.trim();
        var now = edge <= -0.025 ? 'CHEAP' : edge >= 0.025 ? 'RICH' : 'FAIR';
        v.className = 'pm-badge ' + (now === 'CHEAP' ? 'pm-cheap' : now === 'RICH' ? 'pm-rich' : 'pm-fair');
        v.textContent = now;
        if (now !== was) { var rk = row.children[1]; if (rk) { rk.className = 'col-num pm-note'; rk.textContent = 're-rank on next bake'; } }
      }
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
    var el1 = document.getElementById('chart-september');
    if (el1) {
      var sepOpts = JSON.parse(JSON.stringify(common));
      sepOpts.elements = { point: { radius: 4, hoverRadius: 6 } };
      charts.push(new Chart(el1, { type: 'line', data: { labels: SEP_LABELS, datasets: [
        ds('AAPL 2nd', SEPH.sep2AAPL, P.AAPL), ds('GOOGL 2nd', SEPH.sep2GOOGL, P.GOOGL), ds('NVDA 2nd', SEPH.sep2NVDA, P.NVDA)
      ] }, options: sepOpts, plugins: [endLabelPlugin(P.ink)] }));
    }
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

  /* ---------- one control for every row-level explanation in the fair-value table ----------
     27 rows each carry a written "why this is cheap/rich". Clamped to two lines by
     default so the table stays a table; this opens them all at once, and any single
     cell also opens on click. */
  (function () {
    [['trs-reason-toggle', 'trs-table-body'], ['btc-reason-toggle', 'btc-table-body']].forEach(function (pair) {
      var btn = document.getElementById(pair[0]);
      var body = document.getElementById(pair[1]);
      if (!btn || !body) return;
      btn.addEventListener('click', function () {
        var open = body.classList.toggle('reasoning-open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        btn.innerHTML = (open ? 'Hide reasoning' : 'Show all reasoning') + ' <span class="chev">\u25BC</span>';
        if (!open) $$('#' + pair[1] + ' .pm-sub.is-open').forEach(function (el) { el.classList.remove('is-open'); });
      });
    });
    $$('#trs-table-body .pm-sub, #btc-table-body .pm-sub, #track-table .pm-sub, #retired-table .pm-sub').forEach(function (el) {
      el.addEventListener('click', function () { el.classList.toggle('is-open'); });
    });
  })();

  /* ---------- generic long-form disclosures ----------
     Same idiom as the cards, but for standalone blocks: methodology, sensitivity
     notes, section footnotes, the page standfirst. data-longform="N" clamps to N
     lines. Text stays in the DOM (clamped, not hidden) so find-in-page still works. */
  var discloseSync = [];
  $$('[data-longform]').forEach(function (el) {
    var lines = parseInt(el.getAttribute('data-longform'), 10);
    if (lines > 0) el.style.webkitLineClamp = String(lines);
    var label = el.getAttribute('data-longform-label') || 'Read more';
    var btn = document.createElement('button');
    btn.className = 'pm-more pm-more-block';
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = label + ' <span class="chev">▼</span>';
    if (el.id) btn.setAttribute('aria-controls', el.id);
    el.parentNode.insertBefore(btn, el.nextSibling);
    btn.addEventListener('click', function () {
      var open = el.classList.toggle('lf-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.innerHTML = (open ? 'Show less' : label) + ' <span class="chev">▼</span>';
    });
    /* A block inside a hidden tab measures 0/0, so the "does it even overflow?"
       question cannot be answered until that tab is first shown. Re-run on reveal. */
    var measure = function () {
      if (el.offsetParent === null || el.classList.contains('lf-open')) return;
      btn.style.display = el.scrollHeight > el.clientHeight + 2 ? '' : 'none';
    };
    discloseSync.push(measure);
    measure();
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
      if (ce && walletCash != null) ce.textContent = usd(walletCash) + ' + ' + usd(ENGINE_CASH);
      var pf = $('#acct-portfolio');
      /* ENGINE_CASH: CLOB sale proceeds settled off-chain (exchange balance). Reconstructed
         each run from the trade ledger vs the Jul 30 23:45Z anchor (engine ~ $0), because
         neither data-api /value (positions only) nor the on-chain USDC balances see it. */
      if (pf) pf.textContent = usd(posVal + (walletCash != null ? walletCash : 0) + ENGINE_CASH);
      setText('#acct-open', String(active.length));
      var pnl = active.reduce(function (s, p) { return s + p.cashPnl; }, 0);
      var pnlEl = $('#acct-pnl');
      if (pnlEl) { pnlEl.textContent = (pnl >= 0 ? '+' : '\u2212') + usd(pnl); pnlEl.className = 'account-hero-stat-value ' + (pnl >= 0 ? 'pm-pos' : 'pm-neg'); }
      loadWindowPnl();
    }).catch(function () { /* keep baked snapshot */ });
  }

  var ENGINE_CASH = 0; /* STILL UNOBSERVABLE — Aug 28 2026 Friday PRE-OPEN update (13:23Z): THIRTY-EIGHTH consecutive run at $882.32 ($875.00 native + $7.32 bridged, re-read on-chain this walk). The overnight window printed four fills, all SELLS off resting orders — the WTI-130 rail residue cleared in three clips at 99.9c ($39.75, row 253) and the SPY-730 park trimmed 323.82 sh at 99c ($320.58, row 254) — so ~$360.33 more settled engine-side where no public endpoint can read it, taking the disclosed hole to ~$4,863. Still all one direction: the dark pool absorbs every sale. Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 27 2026 Thursday EVENING update (22:43Z): THIRTY-SEVENTH consecutive run at $882.32 ($875.00 native + $7.32 bridged, re-read on-chain this walk). The nine-hour window since the morning walk printed exactly two fills, both SELLS at 99c — the SPY-720-low carry park closed ($118.13, row 251) and the GOOGL-390 nibble closed ($21.06, row 252) — so ~$139.19 more settled engine-side where no public endpoint can read it, on top of the morning's disclosed ~$4,364. Small, and again all one direction: the dark pool absorbs every sale. Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 23 2026 Sunday MORNING update (13:22Z): THIRTY-FIFTH consecutive run at $882.32 ($875.00 native + $7.32 bridged, re-read on-chain this walk) — and a SECOND consecutive fully empty tape: ZERO trades in the fourteen hours since the Saturday evening snapshot, so nothing moved on-chain or engine-side BY CONSTRUCTION. The -$410.42 fall in the floor is entirely marks — the 10Y-5.0% rung crashing 23.5 -> 15.5 on a shut bond market (-$751) against a BTC bounce that handed back ~$470 — plus $13.01 of Soto-walks value that left the /positions feed with its CLOB mid still printing 97.65 (a feed anomaly this page reports rather than papers over). Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 22 2026 Saturday EVENING update (23:08Z): THIRTY-FOURTH consecutive run at $882.32 ($875.00 native + $7.32 bridged, re-read on-chain this walk) — and the cleanest window of the whole series: ZERO trades in the ten hours since the morning snapshot, the first fully empty tape since Aug 15, so nothing moved on-chain or engine-side BY CONSTRUCTION. The -$309.62 fall in the floor is entirely marks (the August BTC sweep bleeding to -$1,029 and the December ladder giving back ~$398). Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 18 2026 Tuesday LATE update (02:04Z Aug 19, second evening pass): TWENTY-EIGHTH
     consecutive run at $882.32 ($875.00 native + $7.32 bridged, re-read on-chain this walk) — and the ~3h window ran $31.00 of
     selling (two MU-700 clips at 99c, rows 195) against a $134.00 OpenAI THIRD add (row 194, 23:05:33Z — the fill that closes the
     share-count gap the last walk disclosed: 1,809.5 + 884.8 + 565.2 = 3,259.5 exactly), plus a $0.0014 yield. Net $103.00 of
     buying, all engine-side, chain unmoved. The dark pool absorbs every trade in BOTH directions now. Floor stays 0; the hero
     figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 18 2026 Tuesday PM update: TWENTY-SEVENTH consecutive run at $882.32 —
     and the window ran $139.36 of NET SELLING through it: eight fills — $342.97 of sales (the BTC-57.5 NO exit in four clips,
     a BTC-60k dust trim, the Padres guard-rail payout, 124 sh of MU-840 hit at the bid into the crash) against a $203.61
     OpenAI add — plus a $1.16 taker rebate, all settled engine-side while the chain sat unmoved. The dark pool keeps
     absorbing every sale. Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 17 2026 Monday AM update: TWENTY-FIFTH consecutive run at $882.32 —
     the window's two fills were both SELLS (row 180 Gold-5k trim $9.37, row 181 WTI-130 skim $5.82 = ~$15.19 of proceeds)
     so a touch more settled engine-side where no public endpoint can read it. Small, consistent in direction: the dark pool
     absorbs every sale. Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 16 2026 Sunday PM update: TWENTY-FOURTH consecutive run at $882.32 —
     and the window ran $40.11 of NET BUYING through it: three fills (a $1.60 WTI-130 skim out, $40.11 of EWY-152/GOOGL-390
     NO nibbles in — rows 177-179) with the chain unmoved, all engine-side. The ledger also books row 176: Friday's 258-sh
     BTC-55k buy ($241.18, 23:01Z) that the Saturday-evening run misread as a resurfaced ghost — that too was engine-funded.
     Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 16 2026 Sunday AM update: TWENTY-THIRD consecutive run at $882.32 —
     the window's one trade was a $2.00 SELL (row 175, 2.02 sh of MU-700 at 99c, 23:56Z Saturday), so ~$2 more settled
     engine-side where no public endpoint can read it. Trivial in size, consistent in direction: the dark pool absorbs
     every sale. Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 15 2026 Saturday PM update: TWENTY-SECOND consecutive run at $882.32 —
     and the zero-fill streak broke THROUGH it: the window's one trade (row 174, $261.35 of MU-880 bought at 87c, 22:12Z)
     printed while the chain sat unmoved, so the buy was funded ENTIRELY from the engine balance no public endpoint can
     read — the dark pool spent again. Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 15 2026 Saturday update: TWENTY-FIRST consecutive run at $882.32 —
     and the cleanest null result yet: ZERO trades since the Aug 14 post-close true-up (the first fully empty window since
     Aug 11 PM), so nothing moved on-chain or engine-side by construction. Floor stays 0; the hero figure remains a FLOOR,
     not an estimate.
     Prior note, kept verbatim — Aug 13 2026 PM update: EIGHTEENTH consecutive run at $882.32 — and the window ran
     $585.58 of NET BUYING through it: 18 fills (rows 158-168) bought $997.39 (two $300 MU legs, a $300 BTC-dip NO, Treasury rungs)
     against $411.81 of sales (the SPY-780 skim at 95/97c, three MU trims, the Anthropic-IPO punt at 27.7c) with the chain unmoved —
     more direct evidence the engine balance spends. Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 13 2026 AM update: SEVENTEENTH consecutive run at $882.32. The overnight window
     sold $41.19 of Braves (row 156) and collected a $1.43 maker rebate — ~$42.62 more settled engine-side where no public
     endpoint can read it. Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 12 2026 PM update: SIXTEENTH consecutive run at $882.32 — and tonight the flow
     ran the OTHER way: five fills (rows 151-155) bought $133.25 of Treasury rungs against $59.06 of Braves sales, so ~$74.19 of
     net purchases were funded ENTIRELY from the engine balance no public endpoint can see — direct evidence the dark pool is
     real and spendable, on top of yesterday's ~$194 of proceeds that vanished into it. Floor stays 0; the hero figure remains
     a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 12 2026 AM update: FOURTEENTH consecutive run at $882.32 — and this one is NOT
     trivial: the window printed three fills (rows 148-150) — $199.98 of SPY-low carry sales (690 stub at 97.8c, the whole 680 leg
     at 98.6c) against a $5.91 rung-0 add — so ~$194.07 of net proceeds settled engine-side where no public endpoint can read them.
     Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 11 2026 PM update: THIRTEENTH consecutive run at $882.32 — trivially so,
     because the window printed ZERO trades (the first empty tape since Aug 6 AM). Nothing moved on-chain or engine-side;
     the floor stays 0 and the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 11 2026 AM update: the chain printed $882.32 a TWELFTH
     consecutive run while the window since the Aug 7 true-up sold $1,076 (SPY-790/680/690 trims, the Apple-crown
     NO clips at 94-96c, a McGonigle stub) and bought $272 (10Y rungs 1-2 adds, the median-home bucket, an SPX
     punt) - roughly $800 MORE of net proceeds settled engine-side where no public endpoint can read them.
     Floor stays 0; the hero figure remains a FLOOR, not an estimate.
     Prior note, kept verbatim — Aug 7 2026 AM update: the overnight tape sold $221.96 more
     (223 sh Apple-crown NO at 95c + 10 sh walks NO at 98c) plus a $2.53 taker rebate — ~$224 of new proceeds
     settled engine-side while the chain read $882.32 a TENTH consecutive run. The dark pool is now >= ~$1,222
     from the last two sessions alone, on top of the standing >= $563 of unexplained inflow evidence. Floor stays 0.
     Prior note, kept verbatim — Aug 6 2026 PM update: THE LIQUIDATION MOVED ~$1,000 INTO THE DARK.
     Five fills between 21:34Z and 21:57Z sold $1,018.75 of rank-book positions and bought $20.74 of MSFT-3rd-Sept —
     net sale proceeds of $998.01 settled into the order engine, where no public endpoint can see them, while the
     on-chain USDC read exactly $882.32 for a NINTH consecutive run. The floor therefore UNDERCOUNTS the account by
     at least ~$998 tonight on top of the standing >= $563 of unexplained inflow evidence. Floor stays 0 — the page
     reports what it can verify, not what it can infer.
     Original failure note, kept verbatim:
     RECONSTRUCTION FAILED — Aug 2 2026, and the page now says so rather than printing a made-up number.
     Rolling the ledger forward from the Aug 2 01:12Z anchor of 1,013.74 gives 1,013.74 + 3.20 rebate + 5.51 sale
     - 1,573.84 deployed = -551.39, which is impossible: the account cannot spend cash it does not have.
     The buys are real (9 fills, /activity), so the anchor was LOW by at least 560.10 and there is an inflow the
     public endpoints cannot see - most likely a direct exchange-side deposit, or negRisk conversions being
     reported as BUYs with a usdcSize that never left the balance. Until the on-chain USDC moves and re-anchors
     the chain, engine cash is UNOBSERVABLE and is floored at 0, which makes the hero figure a FLOOR, not an
     estimate. Do not "fix" this by back-solving a number that makes the arithmetic close. */

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
    { act: 'SELL', tok: '62131357779217648903043004312290004169149177020747768355527511163218119967855', sh: 4177.0, px: 0.4851 } /* token filled in Jul 31 AM: NVDA-Aug-largest NO (was blank) */,
    { act: 'BUY', tok: '11728583497514710574356365513249856989304427730091039531942765980605070477300', sh: 3617.0, px: 0.6176 },
    { act: 'BUY', tok: '44485368873643784531862401772918820589721230664189835980509638753050855169710', sh: 1136.0, px: 0.5147 },
    { act: 'BUY', tok: '24709869777541994161985607099029324252686151170116658170228927775726765767759', sh: 1003.0, px: 0.8038 },
    { act: 'BUY', tok: '52571501528156787027187935562201905991806996165843090033663476160970921418771', sh: 858.0, px: 0.7759 },
    { act: 'SELL', tok: '22380582002052839082465005899114395003938630732672759582910297636521820401881', sh: 541.8, px: 0.9967 } /* WTI $95 NO — guard-rail 4th payout, Jul 31 overnight */,
    { act: 'SELL', tok: '11728583497514710574356365513249856989304427730091039531942765980605070477300', sh: 898.6, px: 0.8868 } /* NVDA-crown July YES — rulebook clips 84.6–92.6¢ */,
    { act: 'SELL', tok: '44485368873643784531862401772918820589721230664189835980509638753050855169710', sh: 544.2, px: 0.9144 } /* AAPL-crown July NO — block trim */,
    { act: 'SELL', tok: '24709869777541994161985607099029324252686151170116658170228927775726765767759', sh: 169.5, px: 0.9440 } /* NVDA-2nd July NO — block trim */,
    { act: 'SELL', tok: '96738271970978473626692761675665650558731868524608528797496705773854589776782', sh: 1797.0, px: 0.405 } /* BACKFILL Jul 30: Apple-2nd-Aug NO unwind after the print */,
    { act: 'SELL', tok: '11728583497514710574356365513249856989304427730091039531942765980605070477300', sh: 1824.0, px: 0.9687 },
    { act: 'SELL', tok: '24709869777541994161985607099029324252686151170116658170228927775726765767759', sh: 834.0, px: 0.9749 },
    { act: 'SELL', tok: '44485368873643784531862401772918820589721230664189835980509638753050855169710', sh: 592.0, px: 0.9895 },
    { act: 'SELL', tok: '52571501528156787027187935562201905991806996165843090033663476160970921418771', sh: 386.0, px: 0.9732 },
    { act: 'SELL', tok: '96594539864896017658091700429432931825025677922116471396340225316561885246', sh: 172.0, px: 0.9033 },
    { act: 'BUY', tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', sh: 135.0, px: 0.2677 },
    { act: 'SELL', tok: '104098056569585630015084344840169131752297298541471048703501533175367050520184', sh: 523.6, px: 0.9953 } /* WTI $90 July NO — full exit 16:30Z, guard-rail fifth payout */,
    { act: 'SELL', tok: '22380582002052839082465005899114395003938630732672759582910297636521820401881', sh: 542.1, px: 0.9988 } /* WTI $95 July NO — second 542-sh tranche lifted 99.8-99.9c */,
    { act: 'SELL', tok: '52571501528156787027187935562201905991806996165843090033663476160970921418771', sh: 472.7, px: 0.9829 } /* Apple-2nd July stub — sold 98.7-99.5c pre-settlement instead of riding */,
    { act: 'SELL', tok: '11554673541814555978405662589194531433610823807505275391222087447793922121663', sh: 63.5, px: 0.9875 } /* SpaceX July-cap NO — band broke; exit at 98-99c, not the card's 35c bid */,
    { act: 'BUY', tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', sh: 768.8, px: 0.3760 } /* Alphabet-2nd-Aug YES — successor-trade adds at 31.7/41.0c */,
    { act: 'BUY', tok: '22397766228589110871783272985290872433765236471932774952155419500943165057456', sh: 6864.46, px: 0.2271 } /* 10Y-5.0% YES — overnight execution of the Treasuries tab's #1 ticket at 4x size, 21.3-24.5c walk */,
    { act: 'SELL', tok: '88070604095019933483120371166318147806645160089526649541840854734212832936177', sh: 39.3, px: 0.99 } /* Phillies 100+ wins NO — guard-rail seventh payout at 99c */,
    { act: 'BUY', tok: '65352899435250001909112885455763971360013158662453391169470389250673340297697', sh: 42.53, px: 0.9435 } /* 10Y-dips-below-3.6% NO top-up — Treasuries low-ladder carry */,
    { act: 'BUY', tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', sh: 787.12, px: 0.3701 } /* Alphabet-2nd-Aug adds, 5 clips 36.0-35.0c — paid 9.5 pts OVER the 27.5% exact-rank fair */,
    { act: 'BUY', tok: '45785223831320903636994814819281571811919629332215573777456567635993484304860', sh: 111.11, px: 0.9036 } /* MU weekly <$720 NO — worst leg of the ladder vs realized vol */,
    { act: 'BUY', tok: '', sh: 477.17, px: 0.3781 } /* 8/7/26 MU week->$900 RESOLVED NO at the Friday close — row frozen at 0 (final −$180.42); tok blanked so the dead book's 50c placeholder can never re-mark it */ /* MU weekly >$900 YES */,
    { act: 'BUY', tok: '90636609665072628934561741191110505683107177678969080679996981652330626258363', sh: 300.0, px: 0.7869 } /* MU >$700 end-Aug */,
    { act: 'BUY', tok: '106686425884931414831660414537151585336396834374452525127171574247454082548832', sh: 294.12, px: 0.6887 } /* MU >$760 end-Aug */,
    { act: 'BUY', tok: '74982300354231902205849663538606152588940436342760335825517353633724464241850', sh: 300.0, px: 0.5599 } /* MU >$820 end-Aug */,
    { act: 'BUY', tok: '68110003550119804768382100356048768439318034246758143453631320291674571791684', sh: 600.0, px: 0.5499 } /* MU >$840 end-Aug — biggest single MU leg */,
    { act: 'BUY', tok: '53049739028670365953377531513580183628183853707672301760004000111406343250709', sh: 300.0, px: 0.49 } /* MU >$860 end-Aug */,
    { act: 'BUY', tok: '16715935133118487637818437087975087219587423634360983683750200849648271646473', sh: 299.36, px: 0.9442 } /* SPY $680-low Aug NO — index down-touch carry */,
    { act: 'BUY', tok: '99310206238906312712351993273929763851099659261404992891652117635117564819942', sh: 96.31, px: 0.1838 } /* Trump #1-searched-person YES — no model, token-size punt */,
    { act: 'BUY', tok: '12403602920039269077597917340921667997547115084613238528792639013246536343316', sh: 28.22, px: 0.8908 } /* No Fed cuts in 2026 YES — Treasuries tab congruent, filled at fair */,
    { act: 'SELL', tok: '31155907477701757690022379073336112499706938908180279820755007284862306962906', sh: 31.25, px: 0.977 } /* Anthropic 0.9-1.2T NO — guard-rail EIGHTH near-par payout, 3 clips 96.5-98.5c */,
    { act: 'BUY', tok: '73765233196749292869366451654880406567953679806142840993718162290941523229389', sh: 1240.98, px: 0.0669 } /* SPY $790-high Aug YES — the cheap side of the index skew */,
    { act: 'BUY', tok: '28968413545616763951382294393977143128717157799818103817407198720924087703276', sh: 1191.16, px: 0.845 } /* Apple-crown-Aug NO, 2 clips — 4.8 pts OVER the 79.7% NO-fair and the opposite side of the page's own Apple-Aug call */,
    { act: 'BUY', tok: '93997509898554464206013458433253360996772270234627522008621917049464308684354', sh: 3275.42, px: 0.0634 } /* Alphabet-crown-Aug YES — filled 0.7 pt INSIDE the 7.0% exact-rank fair, the night's best-priced ticket */,
    { act: 'BUY', tok: '986625934884180891112686496117276469393361067047414381654886200953641996403', sh: 1105.19, px: 0.1414 } /* SPY $780-high Aug YES, 2 clips 13.5/14.5c — the page's Saturday skew card, executed */,
    { act: 'BUY', tok: '47694332922547868411610882826731694023995060415214591827642518726120615225440', sh: 558.15, px: 0.5474 } /* SPY $760-high Aug YES — the near-money rung of the same skew trade */,
    { act: 'SELL', tok: '37115377809826927694181763076177973521362201008447468754472846079605723267622', sh: 5.61, px: 0.982 } /* Nick Kurtz AL MVP NO — guard-rail NINTH near-par payout */,
    { act: 'BUY', tok: '88756945498515564655643791084153591360846567860732500416226379530632897154253', sh: 819.21, px: 0.7403 } /* AMZN $280-high Aug YES — new complex, no model on this page */,
    { act: 'BUY', tok: '70495113508210767655365291291788468538934663465126471715738169362699788708131', sh: 104.12, px: 0.9619 } /* AMZN $224-low Aug NO — the carry side of the same ladder */,
    { act: 'BUY', tok: '54288500488899075246367627195163472475615595062225751818759128802176967336777', sh: 469.51, px: 0.8303 } /* Ethereum reaches $2,000 by Dec 31 YES — new complex, no model */,
    { act: 'BUY', tok: '22397766228589110871783272985290872433765236471932774952155419500943165057456', sh: 78.20, px: 0.2000 } /* 10Y-5.0% rung top-up at 20c — INSIDE the card's stop-adding-above-23c rule */,
    { act: 'SELL', tok: '88756945498515564655643791084153591360846567860732500416226379530632897154253', sh: 819.21, px: 0.9568 } /* 8/3/26 Sold the whole unmodelled leg in 7 clips 93–98¢ the session before AMZN fell 2.3 */,
    { act: 'SELL', tok: '93997509898554464206013458433253360996772270234627522008621917049464308684354', sh: 536.42, px: 0.1621 } /* 8/3/26 Trimmed 536 of 3,275 sh into the Monday spike at 11.8–19.5¢ */,
    { act: 'SELL', tok: '47694332922547868411610882826731694023995060415214591827642518726120615225440', sh: 40.00, px: 0.8400 } /* 8/3/26 First profit-take on the skew card at 84¢; SPY touched $760 the next day and the */,
    { act: 'BUY', tok: '47694332922547868411610882826731694023995060415214591827642518726120615225440', sh: 212.07, px: 0.8768 } /* 8/3/26 Reversed the morning trim an hour later at 87.2¢ */,
    { act: 'BUY', tok: '40766732854727988997103264850535062908745561898964808306819900954273411201269', sh: 311.76, px: 0.6508 } /* 8/3/26 Added the next rung up at 65.1¢; round-tripped out at 94.3¢ avg the following se */,
    { act: 'BUY', tok: '96738271970978473626692761675665650558731868524608528797496705773854589776782', sh: 808.47, px: 0.6279 } /* 8/3/26 Bought the NO at 62.8¢ hours before Alphabet passed Apple on the tape */,
    { act: 'BUY', tok: '22397766228589110871783272985290872433765236471932774952155419500943165057456', sh: 121.80, px: 0.1918 } /* 8/3/26 Third add inside the card’s stop-adding-above-23¢ rule (19–20¢); position 8,182  */,
    { act: 'BUY', tok: '86153684421253045841026634173780053732858134081585356454716135535905962818488', sh: 419.08, px: 0.0495 } /* 8/3/26 Bought the 2.8σ tail this page’s Monitor #3 flagged as the RICH side */,
    { act: 'SELL', tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', sh: 189.00, px: 0.4783 } /* 8/4/26 Nine clips 46–50¢ into the flip rally */,
    { act: 'SELL', tok: '37115377809826927694181763076177973521362201008447468754472846079605723267622', sh: 10.98, px: 0.9880 } /* 8/4/26 Guard rail payout #10 */,
    { act: 'SELL', tok: '22950994476993217816620059342676363932633660110705295996162691702412928292772', sh: 9.74, px: 0.9702 } /* 8/4/26 Guard rail payout #11 at 97.0¢ avg */,
    { act: 'SELL', tok: '47694332922547868411610882826731694023995060415214591827642518726120615225440', sh: 730.21, px: 0.9900 } /* 8/4/26 The touch paid: whole remaining leg (incl. the buy-back) sold at 99¢ */,
    { act: 'SELL', tok: '986625934884180891112686496117276469393361067047414381654886200953641996403', sh: 772.10, px: 0.6183 } /* 8/4/26 18 clips 41→78¢ as SPY ran */,
    { act: 'BUY', tok: '71247391199380658995824617898942777181447594510008171102068161507178943839629', sh: 537.63, px: 0.9326 } /* 8/4/26 Took the carry family’s theme one rung closer to spot at 93.3¢ (the card named t */,
    { act: 'BUY', tok: '106686425884931414831660414537151585336396834374452525127171574247454082548832', sh: 389.61, px: 0.7770 } /* 8/4/26 Added against the standing DO-NOT-ADD card */,
    { act: 'BUY', tok: '46727839354464696273296516236823936849490843247643416964597722256143450327668', sh: 158.54, px: 0.8259 } /* 8/4/26 A ninth Micron leg, again unmodelled */,
    { act: 'SELL', tok: '40766732854727988997103264850535062908745561898964808306819900954273411201269', sh: 311.76, px: 0.9425 } /* 8/4/26 Full exit at 94.3¢ avg against the 65.1¢ entry */,
    { act: 'BUY', tok: '53049739028670365953377531513580183628183853707672301760004000111406343250709', sh: 606.56, px: 0.6195 } /* 8/4/26 Biggest add of the day ($376) into the MU squeeze */,
    { act: 'SELL', tok: '73765233196749292869366451654880406567953679806142840993718162290941523229389', sh: 30.00, px: 0.4740 } /* 8/4/26 Two token clips at 46–48.1¢ off a 1,241-sh position that cost 6.7¢ */,
    { act: 'SELL', tok: '31351186768315326460771976161382920909043553573272353666473916390357183809529', sh: 8.10, px: 0.9988 } /* 8/4/26 Guard rail payout #12 at 99.9¢ */,
    { act: 'BUY', tok: '28968413545616763951382294393977143128717157799818103817407198720924087703276', sh: 326.09, px: 0.9229 } /* 8/4/26 Added the crown NO at 92.3¢ */,
    { act: 'BUY', tok: '27073303004572553849637491269750009119441121163110046345436572485239448486478', sh: 27.27, px: 0.5673 } /* 8/5/26 BTC $60k-dip Aug NO — token-size, unmodelled, no card */,
    { act: 'SELL', tok: '45785223831320903636994814819281571811919629332215573777456567635993484304860', sh: 27.77, px: 0.9800 } /* 8/5/26 MU-week <$720 NO — quarter-skim at 98¢ two sessions before resolution */,
    { act: 'SELL', tok: '71464108500672983676536398854219674504864814997435981582754166649109871191554', sh: 5.49, px: 0.9800 } /* 8/5/26 10Y-below-3.7% NO trim at 98¢ — shrinks the violated low-ladder leg */,
    { act: 'SELL', tok: '74753385292355732879917809656352834782762051527133442900841490505532116166739', sh: 7.50, px: 0.9940 } /* 8/5/26 WTI $130-high NO at 99.4¢ — guard-rail payout THIRTEEN */,
    { act: 'SELL', tok: '73765233196749292869366451654880406567953679806142840993718162290941523229389', sh: 120.00, px: 0.5230 } /* 8/5/26 PM SPY $790 — the exit ladder's first rung PRINTED: 120 sh at 50.3–53.3¢, then SPY faded to a 44.45 mid */,
    { act: 'SELL', tok: '45785223831320903636994814819281571811919629332215573777456567635993484304860', sh: 83.34, px: 0.9900 } /* 8/5/26 PM MU-week <$720 NO — the whole remaining leg lifted at 99¢, two sessions before Friday resolution */,
    { act: 'BUY', tok: '40684707985730872491849941128992064766674278074233806919820229239102287677521', sh: 142.86, px: 0.7000 } /* 8/5/26 PM MU >$880 monthly at 70¢ — against the DO-NOT-ADD card; marked 49.5¢ the same day */,
    { act: 'BUY', tok: '29132439792600455451030084891481768959658744162592479354164537623610669187848', sh: 101.40, px: 0.8875 } /* 8/5/26 PM MU >$720 monthly at 88.75¢ — second same-day DO-NOT-ADD violation; marked 77.5¢ */,
    { act: 'SELL', tok: '37115377809826927694181763076177973521362201008447468754472846079605723267622', sh: 20.86, px: 0.9926 } /* 8/5/26 PM Nick Kurtz AL MVP NO — guard-rail payout FOURTEEN, 3 clips 98.8–99.4¢ */,
    { act: 'SELL', tok: '986625934884180891112686496117276469393361067047414381654886200953641996403', sh: 5.94, px: 0.9500 } /* 8/5/26 PM SPY $780 token skim at 95¢ — the leg closed the day at 72¢ */,
    { act: 'SELL', tok: '74753385292355732879917809656352834782762051527133442900841490505532116166739', sh: 1.31, px: 0.9940 } /* 8/5/26 PM WTI $130-high NO dust clip at 99.4¢ */,
    { act: 'SELL', tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', sh: 1985.53, px: 0.2529 } /* 8/6/26 THE LIQUIDATION 21:34Z: whole Alphabet-2nd-Aug YES leg at 25.29¢ — ~1 pt under the 26.2% fair */,
    { act: 'SELL', tok: '96738271970978473626692761675665650558731868524608528797496705773854589776782', sh: 1004.30, px: 0.3480 } /* 8/6/26 Apple-2nd-Aug NO — the wrong-way leg's exit card, hit 10 pts below its 44.5/46/48 ladder */,
    { act: 'SELL', tok: '93997509898554464206013458433253360996772270234627522008621917049464308684354', sh: 2739.00, px: 0.0328 } /* 8/6/26 Alphabet-crown-Aug stub closed at 3.28¢ vs 0.8% fair */,
    { act: 'BUY', tok: '46552579038506701209087110814172553391939526036683166770317364680747842791908', sh: 274.11, px: 0.0730 } /* 8/6/26 MSFT-3rd-Sept YES — new uncarded punt at 7.30¢ vs 10.9% fair */,
    { act: 'SELL', tok: '52111153087993944251381388500455000347142130118001080456457518631547320289410', sh: 448.54, px: 0.2416 } /* 8/6/26 Apple-3rd-Aug residue out at 24.16¢ — the Aug 4 flagship ends −$56 realised */,
    { act: 'SELL', tok: '28968413545616763951382294393977143128717157799818103817407198720924087703276', sh: 223.33, px: 0.9500 } /* 8/7/26 04:06Z Apple-crown-Aug NO — 3 clips at 95¢ flat, 4.5 pts OVER the 90.5 mid and a point under the 96.1 NO-fair; trims the add card's own leg */,
    { act: 'SELL', tok: '22950994476993217816620059342676363932633660110705295996162691702412928292772', sh: 10.00, px: 0.9800 } /* 8/7/26 10:26Z Judge/Soto walks (Soto) — guard-rail payout FIFTEEN, 10 sh at 98¢ off an 84¢ basis */,
    { act: 'BUY', tok: '106686425884931414831660414537151585336396834374452525127171574247454082548832', sh: 1358.02, px: 0.8161 } /* 8/7/26 15:34Z MU >$760-Aug YES — the DO-NOT-ADD violated again, $1,108.36 in one clip at 81.6c avg vs a ~62% canyon fair; position now 2,042 sh */,
    { act: 'BUY', tok: '114360814676723656908472400412863358263807885083510208644030301446128034414560', sh: 159.09, px: 0.8800 } /* 8/7/26 20:32Z SPY LOW-$720 Aug NO — uncarded add to the low-ladder NO family at 88c */,
    { act: 'SELL', tok: '31225139866242944635093305486513254364151240001212431906638320551757774431080', sh: 24.30, px: 0.9940 } /* 8/9/26 Skenes strikeouts NO — guard-rail payout SIXTEEN at 99.4c */,
    { act: 'SELL', tok: '83247781037352156539108067944461291821683755894607244160607042790356561625563', sh: 6.09, px: 0.8900 } /* 8/9/26 Dem House YES — uncarded token-size trim */,
    { act: 'BUY', tok: '57813774524155463423838033259397133747187306761649300584910471142751787047106', sh: 48.06, px: 0.6658 } /* 8/10/26 10Y-4.8% rung 0 — filled 2.6 pts above the midpoint feed; no walked book exists for this rung */,
    { act: 'SELL', tok: '28968413545616763951382294393977143128717157799818103817407198720924087703276', sh: 808.69, px: 0.9400 } /* 8/10/26 Apple-crown-Aug NO — 808.69 sh distributed at 94c across two clips, 485.2 sh left */,
    { act: 'BUY', tok: '70090363170367815297146294007692529992906189341824085184699164213923074932193', sh: 133.46, px: 0.1199 } /* 8/10/26 10Y-5.2% rung 2 at 11.99c — inside the 13.8 mixture fair, the only ladder add tonight that is */,
    { act: 'BUY', tok: '22397766228589110871783272985290872433765236471932774952155419500943165057456', sh: 698.02, px: 0.2521 } /* 8/10/26 10Y-5.0% rung 1 at 25.21c — breaks the 23c stop AND the fired kill-switch; also cleared the offers and created the 34.0 mid */,
    { act: 'BUY', tok: '25472502502236710744675799561400967135875595061119902215625578202260735017994', sh: 155.84, px: 0.4620 } /* 8/10/26 Gold $5,000 YES — bought the book this page has called RICH since Aug 1 */,
    { act: 'SELL', tok: '73765233196749292869366451654880406567953679806142840993718162290941523229389', sh: 815.14, px: 0.4154 } /* 8/10/26 22:36Z SPY $790-high YES — 815 sh sold at 41.5c, 10.5 points UNDER the exit ladder's own >=52c rung-two stage; 275.8 sh left */,
    { act: 'BUY', tok: '106752699603266763784849736065272688687603139761745952185531728847192670959259', sh: 90.75, px: 0.9587 } /* 8/10/26 22:33Z 10Y-below-3.9% NO at 95.87c — uncarded low-ladder carry add; marked 84.65 next session */,
    { act: 'SELL', tok: '16715935133118487637818437087975087219587423634360983683750200849648271646473', sh: 126.30, px: 0.9820 } /* 8/10/26 22:56Z SPY $680-low Aug NO — carry harvested at 98.2c, three weeks early */,
    { act: 'SELL', tok: '71247391199380658995824617898942777181447594510008171102068161507178943839629', sh: 134.40, px: 0.9780 } /* 8/10/26 22:56Z SPY $690-low Aug NO — first tranche of the carry harvest at 97.8c */,
    { act: 'SELL', tok: '113965991162694738091596214172224948535191089741567025863788017322656669423753', sh: 10.74, px: 0.8900 } /* 8/11/26 00:06Z Kevin McGonigle AL ROY YES — 10.74 sh skimmed at 89c off a 48c basis; 4.9-sh stub left */,
    { act: 'SELL', tok: '28968413545616763951382294393977143128717157799818103817407198720924087703276', sh: 111.60, px: 0.9600 } /* 8/11/26 00:41Z Apple-crown-Aug NO — 2 clips at 96c flat, 2.33 under the 98.33 NO-fair; 373.6 sh left */,
    { act: 'BUY', tok: '44232628347532822259491012067675561686962656316673918558243384084964699327839', sh: 150.48, px: 0.3389 } /* 8/11/26 01:05Z Median US home $419-426K YES at 33.89c — EXECUTED Treasuries Rate-Trades #12 (33.7c effective-ask rec) */,
    { act: 'BUY', tok: '22397766228589110871783272985290872433765236471932774952155419500943165057456', sh: 300.00, px: 0.3267 } /* 8/11/26 10Y-5.0% rung 1 — 4 clips 30-35c through the fired kill-switch AND the 23c stop; position 9,180 sh */,
    { act: 'BUY', tok: '8219112177725900658693363566472942258165213154127853429017405042838900394122', sh: 2.86, px: 0.3500 } /* 8/11/26 03:09Z SPX $8,200-high Dec YES — token-size punt, no model, no card */,
    { act: 'BUY', tok: '70090363170367815297146294007692529992906189341824085184699164213923074932193', sh: 200.00, px: 0.1740 } /* 8/11/26 13:14-13:31Z 10Y-5.2% rung 2 — 2 clips at 17.9/16.9c, ABOVE the 13.8 mixture fair the tab published (row 146) */,
    { act: 'SELL', tok: '71247391199380658995824617898942777181447594510008171102068161507178943839629', sh: 373.23, px: 0.9780 } /* 8/11/26 06:06Z SPY $690-low Aug NO — the rest of the carry leg harvested at 97.8c; ~30 sh remain */,
    { act: 'BUY', tok: '57813774524155463423838033259397133747187306761649300584910471142751787047106', sh: 8.96, px: 0.6600 } /* 8/12/26 00:01Z 10Y-4.8% rung 0 — 8.96-sh uncarded add at 66c against the card's add-nothing; still no walked book */,
    { act: 'SELL', tok: '71247391199380658995824617898942777181447594510008171102068161507178943839629', sh: 30.00, px: 0.9780 } /* 8/12/26 12:34Z SPY $690-low Aug NO — the final ~30-sh stub at 97.8c, five minutes after CPI; leg closed */,
    { act: 'SELL', tok: '16715935133118487637818437087975087219587423634360983683750200849648271646473', sh: 173.06, px: 0.9860 } /* 8/12/26 13:11Z SPY $680-low Aug NO — whole remaining leg at 98.6c, 41 min post-CPI; carry harvested 13 sessions early */,
    { act: 'BUY', tok: '57813774524155463423838033259397133747187306761649300584910471142751787047106', sh: 4.80, px: 0.6600 } /* 8/12/26 17:04Z 10Y-4.8% rung 0 — fourth token add against the card's add-nothing; hours later the rung finally grew a walked book (68/70) */,
    { act: 'BUY', tok: '22397766228589110871783272985290872433765236471932774952155419500943165057456', sh: 200.00, px: 0.2600 } /* 8/12/26 18:11-20:57Z 10Y-5.0% rung 1 — 3 clips 25-27c through the fired kill-switch AND the 23c stop, again; position 9,380 sh */,
    { act: 'SELL', tok: '62604142436062146035823440216234221528806401973102274199745936240471112633499', sh: 64.20, px: 0.9200 } /* 8/12/26 18:22-20:47Z Braves NL East YES — uncarded trim, 3 clips at 92c flat off a 78.76c basis; 268.4 sh remain */,
    { act: 'BUY', tok: '70090363170367815297146294007692529992906189341824085184699164213923074932193', sh: 400.00, px: 0.1440 } /* 8/12/26 20:48-20:57Z 10Y-5.2% rung 2 — 5 clips 12.9-15.9c, 0.6 OVER the 13.8 mixture fair; position 3,468 sh */,
    { act: 'BUY', tok: '108315584853799729838614333748063377472256875592940383916811669252949563879956', sh: 220.00, px: 0.0920 } /* 8/12/26 20:57-21:02Z 10Y-5.5% rung 3 — the tab's flagged RICH leg (+7.6 at the AM walk) BOUGHT at 9.2c avg; position 2,032 sh */,
    { act: 'SELL', tok: '62604142436062146035823440216234221528806401973102274199745936240471112633499', sh: 44.07, px: 0.9345 } /* 8/13/26 03:17Z Braves NL East YES — second uncarded trim: 2 clips at 93/94c (avg 93.45) off the 78.76c basis; 224.3 sh remain */,
    { act: 'BUY', tok: '57813774524155463423838033259397133747187306761649300584910471142751787047106', sh: 126.24, px: 0.6235 } /* 8/13/26 13:36-13:46Z 10Y-4.8% rung 0 — 5 clips 60-66c against the card's NOT-ACTIONABLE/no-book flag; position 318.7 sh */,
    { act: 'SELL', tok: '74753385292355732879917809656352834782762051527133442900841490505532116166739', sh: 1.12, px: 0.9940 } /* 8/13/26 13:37Z WTI $130-high Aug NO dust clip at 99.4c — guard-rail payout SEVENTEEN */,
    { act: 'BUY', tok: '108315584853799729838614333748063377472256875592940383916811669252949563879956', sh: 180.00, px: 0.0764 } /* 8/13/26 13:44-14:05Z 10Y-5.5% rung 3 — the RICH-flagged leg bought AGAIN, 180 sh at 7.2-8.2c; position 2,212.5 sh */,
    { act: 'SELL', tok: '74982300354231902205849663538606152588940436342760335825517353633724464241850', sh: 131.25, px: 0.8571 } /* 8/13/26 14:18Z+17:24Z MU >$820 — 2 clips at 84/88c... hours before rebuying the same leg 5-9 points higher (row 165) */,
    { act: 'SELL', tok: '986625934884180891112686496117276469393361067047414381654886200953641996403', sh: 160.60, px: 0.9604 } /* 8/13/26 14:24-14:31Z SPY $780-high YES — THE CARDED >=85c SKIM EXECUTED at 95/97c (avg 96.04), 160.6 of 166.6 sh */,
    { act: 'SELL', tok: '90636609665072628934561741191110505683107177678969080679996981652330626258363', sh: 56.25, px: 0.9700 } /* 8/13/26 14:53Z MU >$700 — uncarded trim at 97c off a 78c basis; 243.75 sh remain */,
    { act: 'SELL', tok: '21209890653812186814248619913047412762177779312349880099050240669177189381593', sh: 70.67, px: 0.2770 } /* 8/13/26 17:42Z Anthropic-IPO YES — half the punt sold at 27.7c off a 10.6c basis, hours after the page flagged the wake-up; 70.67 sh remain */,
    { act: 'BUY', tok: '8881400370038397971838140193303727239318785128034801687960768890227554347129', sh: 357.14, px: 0.8400 } /* 8/13/26 21:41Z BTC $57.5k-dip Aug NO — NEW $300 carry leg at 84c, no card, no model */,
    { act: 'BUY', tok: '74982300354231902205849663538606152588940436342760335825517353633724464241850', sh: 322.58, px: 0.9300 } /* 8/13/26 21:45Z MU >$820 REBOUGHT at 93c — the same leg trimmed at 84/88c this morning (row 160); position 491.3 sh */,
    { act: 'BUY', tok: '102587121003409847003377550152130425968333220239163333181571343484358987889222', sh: 319.15, px: 0.9400 } /* 8/13/26 21:46Z MU >$800 — a TENTH Micron strike, $300 at 94c, unmodelled */,
    { act: 'SELL', tok: '106686425884931414831660414537151585336396834374452525127171574247454082548832', sh: 73.52, px: 0.9500 } /* 8/13/26 22:05Z MU >$760 at 95c — THE CARDED >=85c TRANCHE finally prints, 73.5 of the 760-sh level; 1,968.2 sh remain */,
    { act: 'SELL', tok: '28968413545616763951382294393977143128717157799818103817407198720924087703276', sh: 167.61, px: 0.9800 } /* 8/14/26 03:35Z Apple-crown-Aug NO — THE CARDED >=97c DISTRIBUTION prints AGAIN, overnight and unprompted: 167.61 sh at 98c flat, a tick OVER the 97.2 bid the PM card named; 206.0 sh remain */,
    { act: 'SELL', tok: '62604142436062146035823440216234221528806401973102274199745936240471112633499', sh: 120.38, px: 0.9453 } /* 8/14/26 05:18-05:19Z Braves NL East YES — THIRD uncarded trim: 3 clips 94/95/96c (avg 94.53) off the 78.76c basis; 104.0 sh remain */,
    { act: 'BUY', tok: '68110003550119804768382100356048768439318034246758143453631320291674571791684', sh: 454.55, px: 0.88 } /* 8/14/26 PM: uncarded MU-840 add, 15:58Z */,
    { act: 'BUY', tok: '95689164730031768195988398128003790785419450590110486478840404402798985620715', sh: 431.77, px: 0.9264 } /* 8/14/26 PM: NEW SPY-730-low NO park, 16:04Z */,
    { act: 'SELL', tok: '90636609665072628934561741191110505683107177678969080679996981652330626258363', sh: 171.95, px: 0.9802 } /* 8/14/26 PM: second MU-700 trim, five clips 98/99c into the close */,
    { act: 'BUY', tok: '40684707985730872491849941128992064766674278074233806919820229239102287677521', sh: 298.85, px: 0.87 } /* 8/15/26 22:12Z: the streak-breaker — uncarded MU-880 add at 87c, lifting a 1.14-sh ask on a 73/87 canyon; funded engine-side while the chain read $882.32 */,
    { act: 'SELL', tok: '90636609665072628934561741191110505683107177678969080679996981652330626258363', sh: 2.02, px: 0.99 } /* 8/15/26 23:56Z: THIRD MU-700 trim — 2.02 sh at 99c flat, 44 minutes after the 880 buy; 69.8 sh remain */,
    { act: 'BUY', tok: '68400022093573165474037038700563901937737223661702772285033991069743666651631', sh: 258.06, px: 0.93 } /* 8/15/26 23:01Z BTC-55k-dip-Aug NO — backfilled 8/16 PM: the Saturday-evening run misread this fill as a resurfaced ghost position; the activity tape shows a real BUY five minutes before that snapshot */,
    { act: 'SELL', tok: '74753385292355732879917809656352834782762051527133442900841490505532116166739', sh: 1.61, px: 0.996 } /* 8/16/26 15:15Z WTI-130-Aug NO dust skim at the top of book */,
    { act: 'BUY', tok: '76101753352724923398774796382225351539663488663617616077670010848908402792427', sh: 21.51, px: 0.93 } /* 8/16/26 17:39Z EWY-152-low-Aug NO — uncarded $20 nibble, new market */,
    { act: 'BUY', tok: '102989311994667094556238101108060401526072526012421040716014843890342965446870', sh: 21.28, px: 0.94 } /* 8/16/26 17:40Z GOOGL-390-high-Aug NO — uncarded $20 nibble, new market, one minute after the EWY leg */,
    { act: 'SELL', tok: '25472502502236710744675799561400967135875595061119902215625578202260735017994', sh: 14.07, px: 0.6658 } /* 8/17/26 06:30Z Gold-5k YES — overnight trim of the RICH gold leg, 3 clips 65-68c (avg 66.6) off the 46.2c basis; 141.8 sh remain, cleared ~6.6 over the 60.0 mid */,
    { act: 'SELL', tok: '74753385292355732879917809656352834782762051527133442900841490505532116166739', sh: 5.84, px: 0.996 } /* 8/17/26 08:50Z WTI-130-Aug NO — guard-rail dust skim EIGHTEEN at 99.6c; 101.9 sh remain at a 98.1c basis */,
    { act: 'SELL', tok: '106686425884931414831660414537151585336396834374452525127171574247454082548832', sh: 84.11, px: 0.98 } /* 8/17/26 13:31:30Z MU-760 YES — BACKFILL: 84.11 sh at 98.0c, thirty seconds before the morning snapshot, so the AM window missed it. Nine points ABOVE the >=85c level the saga card begged for through five idle walks */,
    { act: 'BUY', tok: '54288500488899075246367627195163472475615595062225751818759128802176967336777', sh: 203.49, px: 0.86 } /* 8/17/26 14:30Z + 18:11Z ETH-$2,000-by-Dec YES — two clips at 86.0c against a card that has said 'no thesis, no adds' for twenty-five runs; blends 469.5 sh at 79.9c into 673.0 sh at 83.2c */,
    { act: 'SELL', tok: '62604142436062146035823440216234221528806401973102274199745936240471112633499', sh: 76.30, px: 0.96 } /* 8/17/26 18:04-18:05Z Braves-NL-East YES — FOURTH uncarded trim, 3 clips at 96.0c flat off the 78.76c basis; 27.7 sh remain of an original ~333 */,
    { act: 'SELL', tok: '46727839354464696273296516236823936849490843247643416964597722256143450327668', sh: 158.53, px: 0.96 } /* 8/17/26 19:49Z MU-740 YES — leg CLEARED into the +4.13% Micron rip */,
    { act: 'SELL', tok: '29132439792600455451030084891481768959658744162592479354164537623610669187848', sh: 101.40, px: 0.964 } /* 8/17/26 19:51Z MU-720 YES — leg CLEARED */,
    { act: 'SELL', tok: '102587121003409847003377550152130425968333220239163333181571343484358987889222', sh: 155.00, px: 0.97 } /* 8/17/26 19:51Z MU-800 YES — took the ENTIRE 97c shelf (150 sh) plus a tick; the next bid down is 71.1 */,
    { act: 'BUY', tok: '78959017184382580042532738046363918551357602274462396865643365060706535362447', sh: 1809.50, px: 0.215 } /* 8/17/26 19:52Z OpenAI-IPO-by-Dec-31 YES — $401.59, the largest single new-market entry this ledger has logged; the page has never priced it */,
    { act: 'SELL', tok: '8881400370038397971838140193303727239318785128034801687960768890227554347129', sh: 206.45, px: 0.9481 } /* 8/18/26 14:22-14:31Z BTC-57.5k-dip Aug NO — 4 clips 94-96c (avg 94.81) off the 84c basis; $195.74 of proceeds, 150.69 sh remain */,
    { act: 'SELL', tok: '27073303004572553849637491269750009119441121163110046345436572485239448486478', sh: 6.81, px: 0.85 } /* 8/18/26 14:29Z BTC-60k-dip Aug NO — dust trim at 85c off the 54.99c basis; 20.46 sh remain */,
    { act: 'BUY', tok: '78959017184382580042532738046363918551357602274462396865643365060706535362447', sh: 884.80, px: 0.2232 } /* 8/18/26 18:00Z OpenAI-IPO YES — SECOND add to the unmodelled book, $203.61 at 22.32c; /positions reports 3,259.5 sh, more than the two logged fills sum to — noted, not invented */,
    { act: 'SELL', tok: '51975208337783084633896338822048148162597649121187786496006470069098203674553', sh: 39.30, px: 0.998 } /* 8/18/26 18:33Z Padres-100-wins NO — guard-rail payout NINETEEN at 99.8c */,
    { act: 'SELL', tok: '68110003550119804768382100356048768439318034246758143453631320291674571791684', sh: 124.00, px: 0.83 } /* 8/18/26 22:57:27Z MU-840 YES — 124 sh SOLD AT THE BID into the -7.02% Micron crash, twelve minutes before this snapshot; hit 83.0 on an 83/92 canyon; 930.55 sh remain */,
    { act: 'BUY', tok: '78959017184382580042532738046363918551357602274462396865643365060706535362447', sh: 565.22, px: 0.23 } /* 8/18/26 23:05:33Z OpenAI-IPO YES — the THIRD add, $134.00 at 23.0c, printed 4 minutes after the PM walk's snapshot. This is the fill that closes the share-count gap that walk disclosed: 1,809.5 + 884.8 + 565.2 = 3,259.5, matching /positions exactly — the endpoint was ahead of the activity tape, not wrong */,
    { act: 'SELL', tok: '90636609665072628934561741191110505683107177678969080679996981652330626258363', sh: 31.31, px: 0.99 } /* 8/19/26 00:00-00:38Z MU-700 YES — two clips at 99c (1.01 + 30.30 sh, $31.00), the deepest-ITM rung worked out at a 1c discount to par; 38.46 sh remain */ ,
    { act: 'BUY', tok: '68110003550119804768382100356048768439318034246758143453631320291674571791684', sh: 10.00, px: 0.84 } /* 8/19/26 MU>840 ten-share probe */,
    { act: 'SELL', tok: '27073303004572553849637491269750009119441121163110046345436572485239448486478', sh: 20.46, px: 0.9275 } /* 8/19/26 BTC 60k-dip NO residue out */,
    { act: 'BUY', tok: '22397766228589110871783272985290872433765236471932774952155419500943165057456', sh: 10.00, px: 0.33 } /* 8/19/26 rung-1 ten-share add — eighth violation */,
    { act: 'SELL', tok: '54288500488899075246367627195163472475615595062225751818759128802176967336777', sh: 673.00, px: 0.9681 } /* 8/19/26 ETH-2k whole leg out */,
    { act: 'SELL', tok: '8881400370038397971838140193303727239318785128034801687960768890227554347129', sh: 150.68, px: 0.9775 } /* 8/19/26 BTC 57.5k-dip NO residue out */,
    { act: 'BUY', tok: '95689164730031768195988398128003790785419450590110486478840404402798985620715', sh: 315.79, px: 0.9519 } /* 8/19/26 SPY-730 NO carry add */,
    { act: 'BUY', tok: '74843373582432484858627201602003648342208168490128239235522790524493414154441', sh: 1250.00, px: 0.0852 } /* 8/19/26 BTC-110k Dec ladder rung */,
    { act: 'BUY', tok: '56078938060096976448086754249497300447360333783952000147427828224794011030104', sh: 4666.67, px: 0.1138 } /* 8/19/26 BTC-100k Dec anchor */,
    { act: 'BUY', tok: '17572937743553622007574854767800179053257989607150990127742127678112949966531', sh: 294.12, px: 0.3557 } /* 8/19/26 ETH-3k re-entry */,
    { act: 'BUY', tok: '71296910957902084356560391757722633648005498400799774895345285101862220728868', sh: 401.14, px: 0.0374 } /* 8/19/26 BTC-140k tail */,
    { act: 'SELL', tok: '78959017184382580042532738046363918551357602274462396865643365060706535362447', sh: 550.00, px: 0.6809 } /* 8/20/26 OpenAI spike-sell 62-72c */,
    { act: 'BUY', tok: '78959017184382580042532738046363918551357602274462396865643365060706535362447', sh: 1533.07, px: 0.2353 } /* 8/20/26 OpenAI round trip back in */,
    { act: 'SELL', tok: '68400022093573165474037038700563901937737223661702772285033991069743666651631', sh: 258.06, px: 0.9861 } /* 8/20/26 BTC 55k-dip NO last leg out */,
    { act: 'BUY', tok: '65965214225073605704712365855887384729237451947822407248598722221769498441791', sh: 740.43, px: 0.07 } /* 8/20/26 14:07Z BTC-120k Dec — fourth ladder strike, uncarded */,
    { act: 'SELL', tok: '28968413545616763951382294393977143128717157799818103817407198720924087703276', sh: 206.01, px: 0.972 } /* 8/20/26 15:20Z Apple-crown-Aug NO — THE CARDED PRINT: all 206.01 sh in one clip at 97.2c; first carded fill in thirteen windows */,
    { act: 'BUY', tok: '56078938060096976448086754249497300447360333783952000147427828224794011030104', sh: 1167.62, px: 0.16 } /* 8/20/26 15:21Z BTC-100k anchor add #1 at 16c */,
    { act: 'SELL', tok: '106686425884931414831660414537151585336396834374452525127171574247454082548832', sh: 1884.12, px: 0.939 } /* 8/20/26 15:58Z MU-760 — the saga leg CLEARED in one 93.9c print, $1,764.87 */,
    { act: 'BUY', tok: '56078938060096976448086754249497300447360333783952000147427828224794011030104', sh: 3750.00, px: 0.16 } /* 8/20/26 15:59Z BTC-100k anchor add #2 — the Micron proceeds rotated within a minute; position 9,584.29 sh at a 13.42c blend */,
    { act: 'SELL', tok: '56078938060096976448086754249497300447360333783952000147427828224794011030104', sh: 804.20, px: 0.2752 } /* 8/21/26 BTC-100k Dec anchor — six clips 22→31c into the overnight rip, $221.30 */,
    { act: 'BUY', tok: '74843373582432484858627201602003648342208168490128239235522790524493414154441', sh: 1370.50, px: 0.1484 } /* 8/21/26 BTC-110k Dec — doubled the rung at a 14.84c avg mid-rip ($203.42) */,
    { act: 'SELL', tok: '74843373582432484858627201602003648342208168490128239235522790524493414154441', sh: 210.00, px: 0.1833 } /* 8/21/26 BTC-110k — a quarter of the add back out 108 min later, 20→17c */,
    { act: 'SELL', tok: '65965214225073605704712365855887384729237451947822407248598722221769498441791', sh: 50.00, px: 0.16 } /* 8/21/26 BTC-120k — 50-sh skim at 16c, +9 over the 7c entry */,
    { act: 'SELL', tok: '31351186768315326460771976161382920909043553573272353666473916390357183809529', sh: 4.73, px: 0.999 }, /* 8/21/26 Yelich RBI NO — THE CARDED RAIL SKIM at 99.9c, the band's top tick; twentieth rail payout, second consecutive carded fill */,
    { act: 'SELL', tok: '31977324180919863717921382273587438114623773321828830676048293337319126765438', sh: 17.44, px: 0.997 } /* 8/21/26 WTI-140 NO — harvested at 99.7c, the exact tick the ≤99.6c park spent four runs trying to BUY */,
    { act: 'BUY', tok: '27201221676173593121678787264361008606480627771007041356248031697735484721466', sh: 393.88, px: 0.6347 } /* 8/21/26 14:46Z BTC $85k-Dec YES — uncarded fifth December strike, $250.00 at 63.47c */,
    { act: 'SELL', tok: '22950994476993217816620059342676363932633660110705295996162691702412928292772', sh: 2.57, px: 0.98 } /* 8/21/26 15:01Z Judge/Soto walks (Soto) — guard-rail payout TWENTY-ONE, 2.57 sh at 98c */,
    { act: 'SELL', tok: '25472502502236710744675799561400967135875595061119902215625578202260735017994', sh: 5.92, px: 0.68 } /* 8/21/26 17:12Z Gold-5k YES — CARDED PARTIAL: 5.92 of 141.77 sh at 68c, 14 pts over the card's 54.1c walk plan; 135.85 sh remain */,
    { act: 'BUY', tok: '58559007481908595732343519640998477965598707756438174409311033318259996889965', sh: 2123.46, px: 0.4709 } /* 8/21/26 21:33Z BTC $82.5k-Aug YES — $999.94, the largest of five simultaneous August touch buys, 45 min before the tab that models them was committed */,
    { act: 'BUY', tok: '112241751071174396487292868128075924275858867204192436670566953710907627910138', sh: 1880.46, px: 0.2659 } /* 8/21/26 21:35Z BTC $85k-Aug YES — $500.01 at 26.59c */,
    { act: 'BUY', tok: '58934772812121845536960060739940872473706732919207396740821739825921647791275', sh: 4992.45, px: 0.1662 } /* 8/21/26 21:00-21:33Z BTC $87.5k-Aug YES — 2 clips 13.0/16.8c, $829.77 */,
    { act: 'BUY', tok: '72739316523858479816906805619832308458888360975886863074336484009500930856438', sh: 5194.27, px: 0.0963 } /* 8/21/26 21:33Z BTC $90k-Aug YES — $500.05 at 9.63c */,
    { act: 'BUY', tok: '74843373582432484858627201602003648342208168490128239235522790524493414154441', sh: 298.44, px: 0.1675 } /* 8/21/26 21:48Z BTC $110k-Dec YES — third add to the rung, $50.00; position 2,708.94 sh at an 11.75c blend */,
    { act: 'SELL', tok: '74982300354231902205849663538606152588940436342760335825517353633724464241850', sh: 142.00, px: 0.95 } /* 8/22/26 02:17Z MU >$820 YES — 142 sh at 95c flat into a bid side the prior walk quoted as DEAD (1.1c x 45); 349.33 sh remain */,
    { act: 'SELL', tok: '95689164730031768195988398128003790785419450590110486478840404402798985620715', sh: 187.00, px: 0.94 } /* 8/22/26 02:27Z SPY $730-low Aug NO — uncarded carry trim at 94c, a hair OVER the 93.63c blend; 560.56 sh remain */,
    { act: 'BUY', tok: '102270650225797845195454805763498397874386067232149902550118294787057200324741', sh: 418.02, px: 0.782 } /* 8/22/26 02:33Z BTC $80k-Aug YES at 78.2c — bought AGAINST the tab's own no-order card, five hours before the leg repriced 80.85 -> 60.1 */,
    { act: 'SELL', tok: '31977324180919863717921382273587438114623773321828830676048293337319126765438', sh: 13.08, px: 0.9980 } /* WTI $140-high NO — rail payout #22, two clips 99.8c (park limit stayed unbuyable; the harvest side paid instead) */,
    { act: 'SELL', tok: '90636609665072628934561741191110505683107177678969080679996981652330626258363', sh: 38.38, px: 0.9900 } /* MU >$700 dust sells, 4 clips 99c over three sessions — the residue worked out at the skim line */,
    { act: 'SELL', tok: '74753385292355732879917809656352834782762051527133442900841490505532116166739', sh: 62.12, px: 0.9980 } /* WTI $130-high NO — rail payout #23, four clips 99.8c at 09:24Z Aug 24 */,
    { act: 'SELL', tok: '', sh: 418.01, px: 0.9805 } /* BTC Aug-$80k YES — SOLD 96.4-98.8c into the touch spike as Binance printed $80,000; market resolved YES hours later: row FROZEN at 100, final -$8.17 (the rail's price for not riding to par); tok blanked — the dead book still quotes a garbage 75 mid */,
    { act: 'BUY', tok: '56078938060096976448086754249497300447360333783952000147427828224794011030104', sh: 1573.70, px: 0.3147 } /* BTC Dec-$100k YES add at 31.47c — bought the morning AFTER the $80k touch, 5.8 pts over the next day's own re-sale price */,
    { act: 'SELL', tok: '31155907477701757690022379073336112499706938908180279820755007284862306962906', sh: 18.75, px: 0.9950 } /* Anthropic 0.9-1.2T NO — rail payout #24, final 18.75 sh at 99.5c; the leg is CLOSED after eight near-par harvests */,
    { act: 'BUY', tok: '82271942242710769570803784095231328067346679435915271504441012044356319382263', sh: 78.12, px: 0.3265 } /* Seattle Seahawks NFC West YES — uncarded $25.51 token punt, no model on this page */,
    { act: 'SELL', tok: '72739316523858479816906805619832308458888360975886863074336484009500930856438', sh: 5194.27, px: 0.0576 } /* BTC Aug-$90k YES — Tuesday sweep liquidation leg 4/4 at 5.76c avg */,
    { act: 'SELL', tok: '58934772812121845536960060739940872473706732919207396740821739825921647791275', sh: 4992.44, px: 0.1004 } /* BTC Aug-$87.5k YES — sweep liquidation leg 3/4 at 10.04c */,
    { act: 'SELL', tok: '112241751071174396487292868128075924275858867204192436670566953710907627910138', sh: 1880.46, px: 0.2164 } /* BTC Aug-$85k YES — sweep liquidation leg 2/4 at 21.64c */,
    { act: 'SELL', tok: '58559007481908595732343519640998477965598707756438174409311033318259996889965', sh: 2123.46, px: 0.4465 } /* BTC Aug-$82.5k YES — sweep liquidation leg 1/4 at 44.65c; the four sells recovered $2,155.43 of the $2,829.77 the four legs cost */,
    { act: 'SELL', tok: '31351186768315326460771976161382920909043553573272353666473916390357183809529', sh: 14.20, px: 0.9990 } /* Yelich RBI NO — rail payout #25, three 4.73-sh clips at 99.9c */,
    { act: 'SELL', tok: '56078938060096976448086754249497300447360333783952000147427828224794011030104', sh: 5176.89, px: 0.2568 } /* BTC Dec-$100k YES — the >=25c distribution queue-join FILLED: 5,176.89 sh at 25.68c avg ($1,329.33), the largest single print since Aug 6 */,
    { act: 'SELL', tok: '21209890653812186814248619913047412762177779312349880099050240669177189381593', sh: 70.67, px: 0.5770 } /* Anthropic highest-IPO-cap YES — punt-shelf exit at 57.7c, 7.7 pts over the >=50c re-open trigger; +$33.28 realized on the 10.61c residue basis */,
    { act: 'SELL', tok: '114360814676723656908472400412863358263807885083510208644030301446128034414560', sh: 39.77, px: 0.9800 } /* SPY $720-low NO — near-band harvest, 39.77 sh at 98c */,
    { act: 'SELL', tok: '70495113508210767655365291291788468538934663465126471715738169362699788708131', sh: 104.12, px: 0.9900 } /* AMZN $224-low NO — full exit of the carry leg at 99c, +$3.97 realized over the 96.19c fill */,
    { act: 'SELL', tok: '102587121003409847003377550152130425968333220239163333181571343484358987889222', sh: 79.78, px: 0.9800 } /* MU >$800 YES trim at 98c — the resting offer finally printed */,
    { act: 'BUY', tok: '56078938060096976448086754249497300447360333783952000147427828224794011030104', sh: 1491.15, px: 0.2735 } /* BTC Dec-$100k YES re-buy at 27.35c — 1.67 pts over the previous night's own distribution sale */,
    { act: 'SELL', tok: '62174033562645769120246190297623781610533939632822008848983822335275512869792', sh: 38.68, px: 0.9960 } /* James Wood RBI NO — rail payout #26, half the leg at 99.6c */,
    { act: 'SELL', tok: '74982300354231902205849663538606152588940436342760335825517353633724464241850', sh: 24.43, px: 0.9800 } /* MU >$820 YES trim at 98c — second clip of the resting offer */,
    { act: 'SELL', tok: '114360814676723656908472400412863358263807885083510208644030301446128034414560', sh: 119.32, px: 0.99 } /* 8/27/26 17:51Z SPY $720-low Aug NO — the carry park CLOSED at 99c, two sessions early; ~+$13 realized over the 88c basis */,
    { act: 'SELL', tok: '102989311994667094556238101108060401526072526012421040716014843890342965446870', sh: 21.27, px: 0.99 } /* 8/27/26 18:59Z GOOGL $390-high Aug NO — the Aug 16 nibble closed at 99c off a 94c entry, +$1.06 */,
    { act: 'SELL', tok: '74753385292355732879917809656352834782762051527133442900841490505532116166739', sh: 39.79, px: 0.999 } /* 8/28/26 01:53-05:55Z WTI $130-high Aug NO — rail payout #27, the residue cleared at 99.9c in three clips */,
    { act: 'SELL', tok: '95689164730031768195988398128003790785419450590110486478840404402798985620715', sh: 323.82, px: 0.99 } /* 8/28/26 10:50Z SPY $730-low Aug NO — the last low-ladder park trimmed itself at 99c; 236.74 sh remain */
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
    { tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', side: 'BUY', retPx: 0.3015 } /* NVDA-2nd-July YES 94.3c carry — collapsed to ~30c on the re-flip; never filled */,
    { tok: '93997509898554464206013458433253360996772270234627522008621917049464308684354', side: 'BUY', retPx: 0.0705 } /* Alphabet-Aug convexity punt (re-run) — ran 2.1x past its 3.3c limit unfilled; retired Jul 31 AM */,
    { tok: '99989724583763374403799114487538400642955271680502705587990647202176759344135', side: 'BUY', retPx: 0.55 } /* GOOGL-3rd-Aug carry, second retirement: thesis self-destructed at the Jul 31 open */,
    { tok: '58255742710354753372638105507395301856276470581760095695579319734210276720718', side: 'BUY', retPx: 0.165 } /* September kink bids (NVDA-2nd-Sept <=30c) — resolution repriced 42.5 -> 16.5 straight through the bid zone */,
    { tok: '', side: 'BUY', retPx: 0 } /* Post-print re-entry test — condition met on settled caps; superseded by the released Dec tickets; process card, unscoreable */,
    { tok: '99989724583763374403799114487538400642955271680502705587990647202176759344135', side: 'BUY', retPx: 0.62 } /* GOOGL-3rd-Aug YES third listing — book repriced 51/54 -> 62/63 straight through fair overnight; edge gone */,
    { tok: '', side: 'BUY', retPx: 0 } /* Trades #10 July final-accounting card — self-retiring process card; ledger closed at 64 decisions +$4,151 */,
    { tok: '62009449847159122385971991480139610869824965029008686522071073076098387124747', side: 'BUY', retPx: 0.16 } /* Alphabet-Dec YES — exact-rank correction cut the fair 29.0 -> 18.1%, edge -13.5 -> -2.1 */,
    { tok: '42047893977785728528565456844873223397500118970867834014836006695082853076308', side: 'BUY', retPx: 0.18 } /* Apple-Aug YES re-entry — ask widened 16 -> 18c AND fair fell 22.8 -> 20.3%, edge -6.8 -> -2.3 */,
    { tok: '57813774524155463423838033259397133747187306761649300584910471142751787047106', side: 'BUY', retPx: 0.69 } /* Treasuries rung 0 (10Y 4.8%) — repriced 63 -> 69c against an unchanged 65.4% fair; CHEAP inverted to RICH */,
    { tok: '112917653797517457474191727734311838332458686889832634273844237276119071933739', side: 'SELL', retPx: 0.325 } /* Alphabet-2nd-Sept NO — WORKED: YES 38.5 -> 32.5, 5.5 of 7.9 pts captured, edge closed to -2.4 */,
    { tok: '95302905537962222918309360338213500184994944787102722256843629723110588711061', side: 'SELL', retPx: 0.755 } /* NVDA-Aug NO — leader leg came in 77.5 -> 75.5, edge -5.5 -> -2.9, under the bar */,
    { tok: '11876606915924142133615854761923277060697657209957870741155164849437788272266', side: 'SELL', retPx: 0.545 } /* NVDA-Dec NO — the six-day flagship; +31.7 was a model artifact, residue arbitraged to -3.9 */,
    { tok: '99989724583763374403799114487538400642955271680502705587990647202176759344135', side: 'BUY', retPx: 0.505 } /* Alphabet-3rd-Aug YES — thesis broken: Alphabet took #2 on Aug 4; fair collapsed 64.7 -> 42.8, CHEAP flipped to RICH */,
    { tok: '22227957563975750716653233638849839957651843503812478121278991305586251655238', side: 'BUY', retPx: 0.105 } /* NVDA-2nd-Aug YES — NVDA lead widened to 11.6%; fair 21.7 -> 13.6, -1.6 at the ask */,
    { tok: '58255742710354753372638105507395301856276470581760095695579319734210276720718', side: 'BUY', retPx: 0.205 } /* NVDA-2nd-Sept YES — fair 26.7 -> 21.4 (T=41); +3.6 at the 25c ask */,
    { tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', side: 'SELL', retPx: 0.495 } /* Alphabet-2nd-Aug NO hedge — Alphabet TOOK #2; NO -1.9 at the ask, hedge premise dead */,
    { tok: '9875273331604434310973374077817381730908757452538191940842519381772366848', side: 'BUY', retPx: 0.1915 } /* Apple-Dec YES — caps moved against it; fair 28.2 -> 19.4, edge -0.2 */,
    { tok: '', side: 'BUY', retPx: 0 } /* Monday roll (BTC/WTI carry order) — written for Monday's open, unexecuted through Tuesday's close; process card */,
    { tok: '86153684421253045841026634173780053732858134081585356454716135535905962818488', side: 'SELL', retPx: 0.026 } /* MSFT-3rd-Aug fade exhibit — WORKED: tail collapsed 4.95 -> 2.6c; the account bought it at 4.77 instead */,
    { tok: '28968413545616763951382294393977143128717157799818103817407198720924087703276', side: 'SELL', retPx: 0.91 } /* Apple-crown-Aug NO trim — NO repriced 84.5 -> 91 with Apple's fair falling; position now AT model, nothing to trim against */,
    { tok: '', side: 'BUY', retPx: 0 } /* Micron $840 'no book' exhibit — OBE: the book rebuilt (55/75) and MU ripped; folded into the Micron complex card */,
    { tok: '112917653797517457474191727734311838332458686889832634273844237276119071933739', side: 'BUY', retPx: 0.39 } /* Alphabet-2nd-Sept YES — WORKED: 33/35 -> 37/41 overnight, 4 of the 5.9 published points captured; -0.1 left at the 41c ask */,
    { tok: '70495113508210767655365291291788468538934663465126471715738169362699788708131', side: 'BUY', retPx: 0.9395 } /* AMZN $224-low NO — QUOTE PENDING resolved against it: first real CLOB walk 90x162 / 97.9x20; nothing left at the executable */,
    { tok: '62009449847159122385971991480139610869824965029008686522071073076098387124747', side: 'BUY', retPx: 0.155 } /* Alphabet-Dec YES — thesis broken by the re-flip: fair collapsed 21.7 -> 12.9 on GOOGL -4.0%; the 16c resting bid is now a losing fill */,
    { tok: '52111153087993944251381388500455000347142130118001080456457518631547320289410', side: 'BUY', retPx: 0.23 } /* Apple-3rd-Aug YES — the card's own invalidation fired: Alphabet handed #2 straight back; Apple is #2 again, not 3rd */,
    { tok: '112996809883883766789820608824059367455551434396689079529794719824285513465225', side: 'BUY', retPx: 0.29 } /* Apple-3rd-Sept YES (the orphan) — same invalidation; Apple is no longer the sitting third. Successor: Apple-2nd-Sept YES */,
    { tok: '11286203532633435050461029087857565736892531921887062202100644346193481478173', side: 'BUY', retPx: 0.065 } /* Alphabet-Sept crown ask watch — the 12c ask collapsed to 6/7 and the fair to 5.6% on the GOOGL slide; edge gone */,
    { tok: '11876606915924142133615854761923277060697657209957870741155164849437788272266', side: 'SELL', retPx: 0.655 } /* NVDA-Dec NO decision card — edge closed: mid 65.5 vs 65.8 fair (-0.3); the +6.0 RICH converged in one session */,
    { tok: '69436436951640881186918962093978129047876125081246052069821867405322712154087', side: 'BUY', retPx: 0.515 } /* Apple-2nd-Sept YES — the #1 ticket CONVERGED UNEXECUTED overnight: 40c rec -> 49/54 vs 51.3 fair at T=39 */,
    { tok: '99989724583763374403799114487538400642955271680502705587990647202176759344135', side: 'SELL', retPx: 0.62 } /* Alphabet-3rd-Aug — sell-YES/buy-NO captured: YES 69 -> 62 (NO 38 vs 35.4 NO-fair); scored in YES terms */,
    { tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', side: 'BUY', retPx: 0.21 } /* Alphabet-2nd-Aug hold-at-model — account sold the whole leg at 25.29c (row 122) */,
    { tok: '52111153087993944251381388500455000347142130118001080456457518631547320289410', side: 'BUY', retPx: 0.245 } /* Apple-3rd-Aug residue — account sold all 448 sh at 24.16c (row 126) */,
    { tok: '93997509898554464206013458433253360996772270234627522008621917049464308684354', side: 'BUY', retPx: 0.0305 } /* Alphabet-crown-Aug stub — account closed at 3.28c (row 124) */,
    { tok: '57813774524155463423838033259397133747187306761649300584910471142751787047106', side: 'BUY', retPx: 0.615 } /* 10Y-4.8 rung 0 — CAPTURED: 52.5 -> 61.5 vs 65.4 fair in one session; second retirement of this rung */,
    { tok: '22227957563975750716653233638849839957651843503812478121278991305586251655238', side: 'SELL', retPx: 0.075 } /* NVDA-2nd-Aug NO rest-only orphan — edge under bar (-2.7); scored in YES terms (sell-YES ≡ buy-NO) */,
    { tok: '6369142801468538078435462495249654721381776375778296596920715169671444692617', side: 'SELL', retPx: 0.065 } /* NVDA-3rd-Sept NO — CAPTURED UNEXECUTED: NO 88 -> 95 touch overnight (YES 12/13 -> 5/8); 7 of the 9.5 pts converged in one session; scored in YES terms */,
    { tok: '99989724583763374403799114487538400642955271680502705587990647202176759344135', side: 'BUY', retPx: 0.71 } /* Alphabet-3rd-Aug NO rich-hedge sell — converged without a fill: NO 34.5 -> 29 onto the 29.1 NO-fair; the >=35c offer never printed; scored in YES terms (sell-NO ≡ buy-YES) */,
    { tok: '11286203532633435050461029087857565736892531921887062202100644346193481478173', side: 'SELL', retPx: 0.075 } /* Alphabet-Sept-crown NO — the #1 ticket CONVERGED UNEXECUTED a second September time: NO 89 touch -> 93 (YES 11.5 -> 7.5) vs a 97.6 NO-fair re-derived on Friday's caps; edge under bar. Fourth one-session September convergence. Scored in YES terms */,
    { tok: '22227957563975750716653233638849839957651843503812478121278991305586251655238', side: 'SELL', retPx: 0.0495 } /* NVDA-2nd-Aug rich fade — CAPTURED: 7.15 -> 4.95 in one session, 2.2 of the +4.27 converged; +3.13 left is under the bar */,
    { tok: '11876606915924142133615854761923277060697657209957870741155164849437788272266', side: 'SELL', retPx: 0.705 } /* NVDA-Dec far-crown refusal — edge closed +2.72 -> +0.19 as the fair rose to the market on the re-widened lead; nothing left to refuse */,
    { tok: '9875273331604434310973374077817381730908757452538191940842519381772366848', side: 'BUY', retPx: 0.1455 } /* Apple-Dec far-crown YES hedge — edge -3.81 -> -2.41 under the bar; the <=15.8c walk never filled */,
    { tok: '86153684421253045841026634173780053732858134081585356454716135535905962818488', side: 'SELL', retPx: 0.054 } /* MSFT-3rd-Aug write-at-7c — fair rose 3.25 -> 4.28 underneath it; +1.12 at the mid, the write premium is gone */,
    { tok: '70090363170367815297146294007692529992906189341824085184699164213923074932193', side: 'BUY', retPx: 0.1685 } /* 10Y-5.2 rest-bid card — mid ran 6.85 -> 16.85 THROUGH the old fair while the bid stayed pulled; mixture fair 13.8 is now UNDER the mid. The account bought 200 sh at 17.4 instead (row 147) */,
    { tok: '28968413545616763951382294393977143128717157799818103817407198720924087703276', side: 'BUY', retPx: 0.9515 } /* Apple-crown-Aug NO add-zone (listed in All-Positions AND Largest-Company adds) — -2.9 at the 95.4 ask, under the bar; the account is distributing 94-96c */,
    { tok: '99989724583763374403799114487538400642955271680502705587990647202176759344135', side: 'SELL', retPx: 0.625 } /* Alphabet-3rd-Aug NO hold-at-fair (both add lists) — hold premise dead: NO 9.6 rich vs the 27.94 NO-fair; superseded by the 42c resting-offer exit. Scored in YES terms (hold-NO = short-YES) */,
    { tok: '69436436951640881186918962093978129047876125081246052069821867405322712154087', side: 'BUY', retPx: 0.565 } /* Apple-2nd-Sept watch (New #3 + Largest #4) — FIFTH September self-convergence: -8.2 CHEAP -> +6.11 RICH -> -1.97 FAIR in five sessions; walked book read empty this run */,
    { tok: '31225139866242944635093305486513254364151240001212431906638320551757774431080', side: 'BUY', retPx: 0.967 } /* Skenes don't-hit-that-bid — WORKED: the 40.1c bid refused Jul 27 became a 96.7 mid; ~$258 never given away. The guard-rail queue owns the leg now */,
    { tok: '57813774524155463423838033259397133747187306761649300584910471142751787047106', side: 'BUY', retPx: 0.665 } /* 10Y-4.8 rung 0 'only gap left' (Payoff #6) — retired on its own Aug 12 no-book deadline; the -11.1 edge was never transactable */,
    { tok: '95302905537962222918309360338213500184994944787102722256843629723110588711061', side: 'BUY', retPx: 0.945 } /* NVDA-crown-Aug YES flagship (New #1 / Largest #1 / Trades #1) — CONVERGED UNEXECUTED on the record-lead tape: book chased 92/93 -> 94/95 while the fair ran 98.02 -> 99.25; -4.75 mid / -4.25 at the 95c ask, under the bar at every entry. The AM card said post the <=93c walk at the open; it never printed */,
    { tok: '84136147843234982343387328371427319914867576606050691793138736029250260155687', side: 'BUY', retPx: 0.74 } /* Apple-2nd-Aug YES <=72c (New #2 / Largest #2 / Trades #3) — the hold NARROWED 6.99 -> 6.14% and the book chased 71/72 -> 73/75 into a falling 78.27 fair; -4.27 mid / -3.27 at the ask, edge gone */,
    { tok: '99989724583763374403799114487538400642955271680502705587990647202176759344135', side: 'BUY', retPx: 0.725 } /* Alphabet-3rd-Aug YES entry, unwind-gated (New #3 / Largest #3 / Trades #5 step 2) — book 68/70 -> 72/73 vs a 75.21 fair; -2.71 mid / -2.21 at the ask. The NO-unwind half survives as the Sells exit card */,
    { tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', side: 'SELL', retPx: 0.19 } /* Alphabet-2nd-Aug rich fade (Largest #4 / Trades #4) — WORKED UNEXECUTED: 24.0 -> 19.0 vs a 21.15 fair; +5.85 RICH converged to -2.15 in one session; the $0-cap card banked its information */,
    { tok: '52111153087993944251381388500455000347142130118001080456457518631547320289410', side: 'SELL', retPx: 0.215 } /* Apple-3rd-Aug rich tail (Largest #5 / Trades #7) — WORKED UNEXECUTED: 25.0 -> 21.5 vs a 20.98 fair; +7.00 converged to +0.52; the $125 door never mattered */,
    { tok: '42047893977785728528565456844873223397500118970867834014836006695082853076308', side: 'SELL', retPx: 0.0325 } /* Apple-crown-Aug YES rich complement exhibit (Trades #6) — 5.10 -> 3.25 vs a 0.37 fair; +2.88 residue under the bar; superseded by the all-three-partitions-under-par exhibit */,
    { tok: '', side: 'BUY', retPx: 0 } /* 'December closed both its tickets' watch (Trades #9 / Largest #10) — premise broken the other way: neither re-open level hit, but a +3% NVDA day ran the Dec fair THROUGH the sleeping book (70.67 -> 76.96 vs a 71.5 mid). Successors: the NVDA-Dec 71c rest and the Alphabet-Dec NO fade. Process card, unscoreable */,
    { tok: '62009449847159122385971991480139610869824965029008686522071073076098387124747', side: 'SELL', retPx: 0.115 } /* Alphabet-Dec NO fade — WORKED UNEXECUTED: 12.5 -> 11.5 overnight, +4.2 left at the 11c bid, under the bar; neither ticket step (16c bid-pull, NO <=88c) ever posted. Scored in YES terms */,
    { tok: '', side: 'BUY', retPx: 0 } /* August under-par partition basket — leak closed in one session (2nd seat 97.75 -> 101.40, ask baskets back over par); the 34-sh window never printed; multi-token, unscoreable */,
    { tok: '11876606915924142133615854761923277060697657209957870741155164849437788272266', side: 'BUY', retPx: 0.725 } /* NVDA-Dec crown YES 72c rest — Apple's +1% day cut the fair 77.2 -> 76.6; -4.6 joining the bid, under bar at every price; CANCEL the 200-sh GTC */,
    { tok: '112917653797517457474191727734311838332458686889832634273844237276119071933739', side: 'SELL', retPx: 0.34 } /* Alphabet-2nd-Sept rich fade — edge gone: GOOGL's +1.1% open ran the MC fair 28.30 -> 30.23 under an unmoved 34.0 mid; +3.8 at the mid / +2.8 at the 33c bid, never ungated. Scored in YES terms */,
    { tok: '88181040897286103762090116883791794441997393429026713037275553532748007513417', side: 'SELL', retPx: 0.86 }, /* Apple-2nd-Aug rich watch — edge died from the model's side (fair chased the mid) */
    { tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', side: 'BUY', retPx: 0.135 } /* Alphabet-2nd-Aug cheap watch — edge < 5 at mid and lift one session after opening */,
    { tok: '52111153087993944251381388500455000347142130118001080456457518631547320289410', side: 'BUY', retPx: 0.165 } /* Apple-3rd-Aug cheap watch — the -6.9 overshoot converged to +0.2 IN ITS SLEEP: 10.5 -> 16.5 over the weekend against a 16.3 fair. Third August watch killed by model-vs-book convergence with zero fills; the <=15c re-open never funded past its $85 door */,
    { tok: '62009449847159122385971991480139610869824965029008686522071073076098387124747', side: 'SELL', retPx: 0.115 } /* Alphabet-Dec armed re-fire fade watch — edge faded +5.8 -> +4.8 under the bar as the mid came in 12.5 -> 11.5 on the Saturday-evening books; the trigger was met two runs on a door that shrank $59 -> $34 -> gone. Scored in YES terms */,
    { tok: '99989724583763374403799114487538400642955271680502705587990647202176759344135', side: 'BUY', retPx: 0.795 } /* Alphabet-3rd-Aug cheap-floor watch — the seat's first CHEAP print died in its sleep: 73.5 -> 79.5 overnight on zero cap news, edge -8.0 -> -2.0 under the bar before the $114 door ever reached its $250 gate. Sixth August watch killed by model-vs-book convergence with zero fills */,
    { tok: '11876606915924142133615854761923277060697657209957870741155164849437788272266', side: 'BUY', retPx: 0.755 } /* NVDA-Dec re-open watch — December unfroze on the Sunday-evening books and converged: 73.5 -> 75.5 closed the cheap print -3.3 -> -1.3 before the watch's >=5-under-fair bid trigger ever armed; the fourth December watch dead by convergence, zero by fills */,
    { tok: '46552579038506701209087110814172553391939526036683166770317364680747842791908', side: 'BUY', retPx: 0.0875 } /* 8/17/26 PM — MSFT-3rd-September ADD: fifteen walks with the fair above the mark ended in one session. Microsoft fell 3.04% and the fair fell with it, 12.1 -> 8.25, closing the -2.6 to +0.5. The hold stays; the ADD retires */,
    { tok: '986625934884180891112686496117276469393361067047414381654886200953641996403', side: 'SELL', retPx: 0.605 } /* 8/17/26 PM — the SPY-$780-high >=90c re-skim: payable at 92.0 two runs ago, never posted, and tonight the leg collapsed 89.5 -> 60.5 on a 0.47% SPY down day. The most expensive unposted order this page has logged */,
    { tok: '69436436951640881186918962093978129047876125081246052069821867405322712154087', side: 'BUY', retPx: 0.675 } /* 8/18/26 PM — Apple-2nd-Sept lift: the widest edge this page ever printed (-11.3) CONVERGED UNEXECUTED in one session — mid 57.0 -> 67.5 (+10.5, the series' biggest move) as the gap-crush pushed the fair to 69.1; -1.65 left. The $150 at 58.90c would mark +$21.90 tonight */,
    { tok: '112917653797517457474191727734311838332458686889832634273844237276119071933739', side: 'SELL', retPx: 0.265 } /* 8/18/26 PM — Alphabet-2nd-Sept fade: WORKED UNEXECUTED — 36.0 -> 26.5 (-9.5, its biggest-ever move) onto a 21.8 fair; +4.7 left, under the bar. The 65-67c NO fill never printed. Scored in YES terms */,
    { tok: '89706022921501149384847021353587496883277465141816802927673604440172434177565', side: 'BUY', retPx: 0.065 } /* 8/18/26 PM — Alphabet-2nd-August $100 ticket: killed by the caps, not the book — Apple's +1.45% day pulled the #2 gap to 8.66%, cutting the fair 14.8 -> 9.45 over an unmoved 6.5 mid; -5.3 -> -2.95, under the bar */,
    { tok: '54288500488899075246367627195163472475615595062225751818759128802176967336777', side: 'SELL', retPx: 0.885 } /* 8/20/26 — ETH-2k no-thesis card: position closed by the account at 96.81c avg (row 198); scored from the 88.5 retirement mark */,
    { tok: '46552579038506701209087110814172553391939526036683166770317364680747842791908', side: 'BUY', retPx: 0.0795 } /* 8/20/26 — MSFT-3rd-Sept watch epilogue: aged out with the mark ON the T=29 fair (7.95 vs 7.7) */,
    { tok: '58255742710354753372638105507395301856276470581760095695579319734210276720718', side: 'BUY', retPx: 0.045 } /* 8/21/26 — NVDA-2nd-Sept cheap watch: died by its own model on a closed-market walk — T 29→28 cut the fair 10.05→9.66, the 5.0c-ask edge slipped to -4.66 under the bar; ~$85 door never neared the $500 gate */,
    { tok: '9875273331604434310973374077817381730908757452538191940842519381772366848', side: 'BUY', retPx: 0.1345 } /* 8/27/26 — Apple-Dec lift (GLOBAL #1 for six runs, -7.35 at its widest): the NVDA print re-marked the caps live (+7.20%) and the fair fell 20.95 -> 15.80 — edge -2.35, under the bar. Zero fills across seven walks of published edge; the frozen-cap edge was never banked and the print says it was never fully real */,
    { tok: '69436436951640881186918962093978129047876125081246052069821867405322712154087', side: 'SELL', retPx: 0.805 } /* 8/27/26 — sep2AAPL fade (GLOBAL #2, +8.33 at its widest): the print took the mid 76.5 -> 80.5 AND the fair 68.17 -> 79.52 — edge +0.98, dead. The market was pricing the earnings gap the frozen caps could not see; the $300 door gate kept the ticket partial and unposted, which tonight reads as the gate working */,
    { tok: '', side: 'SELL', retPx: 0 } /* 8/27/26 — MU 860/880 inversion exhibit: the reopened tape normalised the ordering (860 87.0 > 880 82.0 mids on 2,000-sh bids) — anomaly gone, nothing to capture; two-token exhibit, unscoreable */

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
      ['polymarket', 'largest', 'treasuries', 'bitcoin', 'tracking'].forEach(function (v) {
        var el = document.getElementById('view-' + v);
        if (el) el.hidden = v !== view;
      });
      if (view === 'largest' && !chartsBuiltVisible) {
        chartsBuiltVisible = true;
        requestAnimationFrame(buildCharts);
      }
      requestAnimationFrame(function () {
        scrollerUpdates.forEach(function (u) { u(); });
        discloseSync.forEach(function (m) { m(); });
      });
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
