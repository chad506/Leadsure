#!/usr/bin/env python3
"""
Daily closing-price refresh for leadsure.com.

Runs in GitHub Actions (.github/workflows/daily-prices.yml) every weekday after
the US close. It replaces the old Mac launchd job (scripts/update_picks_prices.py),
which only ran when that Mac was awake and stopped pushing after Oct 1, 2026.

What it updates, from Finnhub /quote (c = last close, pc = prior close):
  fund-data.js         POSITIONS[].price / .prevClose, PRICES_AS_OF, DATA_VERSION
  model-picks-data.js  every pick's livePrice / prevClose
  app3.js              the spyCurrentPrice / magsCurrentPrice starting values

Rules (from CLAUDE.md):
  - A position whose entryDate is the session date keeps prevClose = costBasis.
  - Only quotes stamped with today's session date are used; stale or empty
    quotes (halted, delisted, renamed tickers) leave that symbol untouched.
  - If the market was closed today (holiday), nothing is written.
  - If too few quotes come back, nothing is written.
  - After writing, the data files are loaded with node; on any error the
    originals are restored and the script exits non-zero (no commit happens).

Usage: python3 scripts/daily_prices.py [--force] [--dry-run]
"""

import json, os, re, shutil, subprocess, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUND = os.path.join(ROOT, 'fund-data.js')
PICKS = os.path.join(ROOT, 'model-picks-data.js')
APP = os.path.join(ROOT, 'app3.js')
NY = ZoneInfo('America/New_York')
PT = ZoneInfo('America/Los_Angeles')
SPACING = 1.1          # seconds between calls (Finnhub free tier: 60/min)
NUM = r'-?\d+(?:\.\d+)?'


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def api_key(fund_text):
    key = os.environ.get('FINNHUB_API_KEY', '').strip()
    if key:
        return key
    m = re.search(r"SHARED_FINNHUB_KEY\s*=\s*'([^']+)'", fund_text)
    if not m:
        sys.exit('No Finnhub key: set FINNHUB_API_KEY or SHARED_FINNHUB_KEY in fund-data.js')
    return m.group(1)


def quote(sym, key):
    url = f'https://finnhub.io/api/v1/quote?symbol={sym}&token={key}'
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:            # rate limited: back off and retry
                time.sleep(10 * (attempt + 1))
                continue
            if attempt == 3:
                print(f'  {sym}: HTTP {e.code}')
            time.sleep(2)
        except Exception as e:           # network hiccup
            if attempt == 3:
                print(f'  {sym}: {e}')
            time.sleep(2)
    return None


def session_date(q):
    """Trading date (New York) of a Finnhub quote, or None."""
    t = (q or {}).get('t') or 0
    if not t:
        return None
    return datetime.fromtimestamp(t, tz=timezone.utc).astimezone(NY).date()


def positions_block(fund):
    a = fund.index('const POSITIONS = [')
    b = fund.index('];', a)
    return a, b


def main():
    force = '--force' in sys.argv
    dry = '--dry-run' in sys.argv
    fund, picks, app = read(FUND), read(PICKS), read(APP)
    key = api_key(fund)

    pa, pb = positions_block(fund)
    pos_syms = re.findall(r'"symbol": "([^"]+)"', fund[pa:pb])
    pick_syms = re.findall(r"symbol: '([^']+)'", picks)
    symbols = ['SPY', 'MAGS'] + sorted(set(pos_syms + pick_syms) - {'SPY', 'MAGS'})
    print(f'{len(pos_syms)} positions, {len(pick_syms)} picks, {len(symbols)} unique symbols')

    # 1. Which session is today? Use SPY's quote stamp.
    spy = quote('SPY', key)
    session = session_date(spy)
    today_ny = datetime.now(NY).date()
    if session is None:
        sys.exit('SPY quote has no timestamp; aborting without changes')
    if session != today_ny and not force:
        print(f'Market closed today ({today_ny}); latest session is {session}. Nothing to do.')
        return
    print(f'Session date: {session}')

    # 2. Fetch every symbol (SPY already fetched).
    prices = {}
    stale = []
    for i, sym in enumerate(symbols):
        q = spy if sym == 'SPY' else quote(sym, key)
        if sym != 'SPY':
            time.sleep(SPACING)
        c = (q or {}).get('c') or 0
        pc = (q or {}).get('pc') or 0
        if c > 0 and pc > 0 and session_date(q) == session:
            prices[sym] = {'c': round(c, 4), 'pc': round(pc, 4)}
        else:
            stale.append(sym)
        if (i + 1) % 50 == 0:
            print(f'  {i + 1}/{len(symbols)} fetched')
    print(f'Fresh quotes: {len(prices)}/{len(symbols)}; stale or empty: {len(stale)}')
    if stale:
        print('  stale/empty: ' + ', '.join(stale[:60]) + (' ...' if len(stale) > 60 else ''))

    pos_fresh = [s for s in pos_syms if s in prices]
    pick_fresh = [s for s in set(pick_syms) if s in prices]
    if len(pos_fresh) < 0.9 * len(pos_syms) or len(pick_fresh) < 0.7 * len(set(pick_syms)):
        sys.exit(f'Too few fresh quotes (positions {len(pos_fresh)}/{len(pos_syms)}, '
                 f'picks {len(pick_fresh)}/{len(set(pick_syms))}); aborting without changes')

    # 3. fund-data.js POSITIONS (one object per line).
    lines = fund[pa:pb].split('\n')
    changed_pos = 0
    for n, line in enumerate(lines):
        m = re.search(r'"symbol": "([^"]+)"', line)
        if not m or m.group(1) not in prices:
            continue
        p = prices[m.group(1)]
        prev = p['pc']
        ed = re.search(r'"entryDate": "(\d{4}-\d{2}-\d{2})"', line)
        if ed and ed.group(1) == session.isoformat():
            cb = re.search(r'"costBasis": (' + NUM + ')', line)
            if cb:
                prev = float(cb.group(1))
        new = re.sub(r'"price": ' + NUM, f'"price": {p["c"]}', line, count=1)
        new = re.sub(r'"prevClose": ' + NUM, f'"prevClose": {prev}', new, count=1)
        if new != line:
            changed_pos += 1
            lines[n] = new
    new_fund = fund[:pa] + '\n'.join(lines) + fund[pb:]

    # 4. model-picks-data.js (one pick object per line).
    out, changed_picks = [], 0
    for line in picks.split('\n'):
        m = re.search(r"symbol: '([^']+)'", line)
        if m and m.group(1) in prices and 'livePrice:' in line:
            p = prices[m.group(1)]
            new = re.sub(r'livePrice: ' + NUM, f'livePrice: {p["c"]}', line, count=1)
            new = re.sub(r'prevClose: ' + NUM, f'prevClose: {p["pc"]}', new, count=1)
            if new != line:
                changed_picks += 1
            line = new
        out.append(line)
    new_picks = '\n'.join(out)

    # 5. app3.js benchmark starting values.
    new_app = app
    if 'SPY' in prices:
        new_app = re.sub(r'let spyCurrentPrice = ' + NUM + ';', f'let spyCurrentPrice = {prices["SPY"]["c"]};', new_app, count=1)
    if 'MAGS' in prices:
        new_app = re.sub(r'let magsCurrentPrice = ' + NUM + ';', f'let magsCurrentPrice = {prices["MAGS"]["c"]};', new_app, count=1)

    as_of_now = re.search(r"const PRICES_AS_OF = '([^']+)';", fund).group(1)
    nothing_new = (new_fund == fund and new_picks == picks and new_app == app
                   and as_of_now == session.isoformat())
    if nothing_new:
        print('Prices already current; nothing to write.')
        return

    # 6. PRICES_AS_OF (Pacific date = session date at run time) and DATA_VERSION.
    as_of = session.isoformat()
    new_fund = re.sub(r"const PRICES_AS_OF = '[^']+';", f"const PRICES_AS_OF = '{as_of}';", new_fund, count=1)
    m = re.search(r"const DATA_VERSION = '(\d{4}-\d{2}-\d{2})-(\d+)';", fund)
    patch = int(m.group(2)) + 1 if m and m.group(1) == as_of else 1
    version = f'{as_of}-{patch}'
    new_fund = re.sub(r"const DATA_VERSION = '[^']+';", f"const DATA_VERSION = '{version}';", new_fund, count=1)

    print(f'Positions updated: {changed_pos}/{len(pos_syms)}; pick lines updated: {changed_picks}; '
          f'SPY {prices.get("SPY", {}).get("c")}, MAGS {prices.get("MAGS", {}).get("c")}; DATA_VERSION {version}')
    if dry:
        print('Dry run: no files written.')
        return

    backups = {}
    for path, text in ((FUND, new_fund), (PICKS, new_picks), (APP, new_app)):
        backups[path] = read(path)
        write(path, text)

    # 7. Make sure the files still load in a JS engine before anything is committed.
    check = (
        "const fs=require('fs');"
        "const code=fs.readFileSync('fund-data.js','utf8')+'\\n'+fs.readFileSync('model-picks-data.js','utf8')"
        "+'\\n;return {POSITIONS,MODEL_PICKS,PRICES_AS_OF,DATA_VERSION};';"
        "const d=new Function(code)();"
        "if(!Array.isArray(d.POSITIONS)||d.POSITIONS.length<1) throw new Error('POSITIONS missing');"
        "if(!d.MODEL_PICKS||!Array.isArray(d.MODEL_PICKS.models)) throw new Error('MODEL_PICKS missing');"
        "for(const p of d.POSITIONS){ if(!(p.price>0)||!(p.prevClose>0)) throw new Error('bad price '+p.symbol); }"
        "console.log('JS check ok:',d.POSITIONS.length,'positions,',d.MODEL_PICKS.models.length,'models,',d.PRICES_AS_OF,d.DATA_VERSION);"
    )
    try:
        subprocess.run(['node', '-e', check], cwd=ROOT, check=True)
        subprocess.run(['node', '--check', 'app3.js'], cwd=ROOT, check=True)
    except Exception as e:
        for path, text in backups.items():
            write(path, text)
        sys.exit(f'JS check failed ({e}); originals restored, nothing committed')

    msg = os.environ.get('PRICES_MSG_FILE')
    if msg:
        write(msg, f'Daily prices: {as_of} close for {len(prices)} symbols (DATA_VERSION {version})\n\n'
                   f'Positions updated: {changed_pos}/{len(pos_syms)}; pick lines updated: {changed_picks}.\n'
                   + (f'No fresh quote (left unchanged): {", ".join(stale)}\n' if stale else ''))
    print('Done.')


if __name__ == '__main__':
    main()
