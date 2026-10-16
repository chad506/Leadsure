/* Leadsure password screen. Loaded first in <head> on every page.
   This is a privacy curtain for casual visitors; the repo is public, so it is not real security.
   To change the password: set G to the SHA-256 hex of (newPassword + ':gate'), and update functions/_middleware.js in leadsure-deals. */
(function () {
  var G = '829296bb2e66715a20f27d4a5262055d7ffd184cef6f47d6001c9e79cd50c4cd';
  var C = 'ls_gate';
  function hasPass() {
    if (document.cookie.split(/;\s*/).indexOf(C + '=' + G) > -1) return true;
    try { return localStorage.getItem(C) === G; } catch (e) { return false; }
  }
  if (hasPass()) return;

  var root = document.documentElement;
  root.className += ' ls-locked';
  var css = document.createElement('style');
  css.textContent =
    'html.ls-locked,html.ls-locked body{background:#0b1220!important;overflow:hidden!important}' +
    'html.ls-locked body>*:not(#ls-gate){display:none!important}' +
    '#ls-gate{position:fixed;inset:0;z-index:2147483647;display:flex;align-items:center;justify-content:center;padding:16px;background:#0b1220;' +
    'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}' +
    '#ls-gate form{background:#fff;border-radius:14px;box-shadow:0 20px 50px rgba(0,0,0,.35);padding:34px 30px 28px;width:100%;max-width:360px;text-align:center;color:#0f172a}' +
    '#ls-gate .lg{font-weight:800;letter-spacing:.12em;font-size:22px}#ls-gate .lg span{color:#16a34a}' +
    '#ls-gate p{color:#475569;font-size:14px;margin:8px 0 22px}' +
    '#ls-gate input{width:100%;box-sizing:border-box;padding:12px 14px;border:1px solid #cbd5e1;border-radius:9px;font-size:16px;outline:none}' +
    '#ls-gate input:focus{border-color:#16a34a;box-shadow:0 0 0 3px rgba(22,163,74,.15)}' +
    '#ls-gate button{margin-top:12px;width:100%;padding:12px;border:0;border-radius:9px;background:#16a34a;color:#fff;font-size:15px;font-weight:600;cursor:pointer}' +
    '#ls-gate .er{color:#dc2626;font-size:13px;margin-top:10px;min-height:18px}#ls-gate .nt{font-size:12px;color:#94a3b8;margin-top:14px}';
  (document.head || root).appendChild(css);

  function sha256(s) {
    return crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)).then(function (b) {
      return Array.prototype.map.call(new Uint8Array(b), function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
    });
  }

  function unlock() {
    var host = location.hostname, dom = /(^|\.)leadsure\.com$/.test(host) ? '; Domain=.leadsure.com' : '';
    document.cookie = C + '=' + G + dom + '; Path=/; Max-Age=31536000; Secure; SameSite=Lax';
    try { localStorage.setItem(C, G); } catch (e) {}
    var el = document.getElementById('ls-gate');
    if (el) el.parentNode.removeChild(el);
    root.className = root.className.replace(/\s*ls-locked/g, '');
  }

  function show() {
    if (document.getElementById('ls-gate')) return;
    var d = document.createElement('div');
    d.id = 'ls-gate';
    d.innerHTML = '<form autocomplete="on"><div class="lg">LEAD<span>SURE</span></div>' +
      '<p>This site is private. Enter the password to continue.</p>' +
      '<input type="password" name="password" placeholder="Password" autocomplete="current-password" required>' +
      '<button type="submit">Enter</button><div class="er"></div>' +
      '<div class="nt">You\'ll stay signed in on this device.</div></form>';
    document.body.appendChild(d);
    var f = d.querySelector('form'), inp = d.querySelector('input'), er = d.querySelector('.er');
    inp.focus();
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      sha256(inp.value + ':gate').then(function (h) {
        if (h === G) unlock();
        else { er.textContent = 'Wrong password. Try again.'; inp.select(); }
      });
    });
  }

  if (document.body) show();
  else document.addEventListener('DOMContentLoaded', show);
})();
