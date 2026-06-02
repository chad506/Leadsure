#!/usr/bin/env python3
"""
Daily picks price updater — runs Mon-Fri at 4:30pm PT (market close + 30 min).
Fetches Finnhub quotes for every symbol in model-picks-data.js and updates
livePrice + prevClose for every pick entry, then commits and pushes.
"""

import re, json, urllib.request, time, subprocess, sys
from datetime import date

API_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg'
PICKS_FILE = '/Users/chadfisher/Leadsure/model-picks-data.js'
FUND_DATA  = '/Users/chadfisher/Leadsure/fund-data.js'
REPO       = '/Users/chadfisher/Leadsure'

def get_symbols(content):
    return sorted(set(re.findall(r"symbol: '([A-Z]+)'", content)))

def fetch_prices(symbols):
    prices = {}
    total = len(symbols)
    for i, sym in enumerate(symbols, 1):
        url = f'https://finnhub.io/api/v1/quote?symbol={sym}&token={API_KEY}'
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, timeout=10) as r:
                    d = json.loads(r.read())
                c  = round(d.get('c',  0), 4)
                pc = round(d.get('pc', 0), 4)
                if c > 0:
                    prices[sym] = {'c': c, 'pc': pc}
                    print(f'  [{i}/{total}] {sym}: {c} (pc={pc})')
                else:
                    print(f'  [{i}/{total}] {sym}: no price (skipping)')
                break
            except Exception as e:
                if attempt == 2:
                    print(f'  [{i}/{total}] {sym} FAILED: {e}')
                else:
                    time.sleep(2)
        time.sleep(0.5)   # ~2 req/s — well within free-tier 60/min
    return prices

def update_picks(content, prices):
    """Replace livePrice and prevClose inside every pick object."""
    def patch_entry(m):
        entry = m.group(0)
        sym_m = re.search(r"symbol: '([A-Z]+)'", entry)
        if not sym_m:
            return entry
        sym = sym_m.group(1)
        if sym not in prices:
            return entry
        p = prices[sym]
        entry = re.sub(r'livePrice: [\d.]+',  f'livePrice: {p["c"]}',  entry)
        entry = re.sub(r'prevClose: [\d.]+',  f'prevClose: {p["pc"]}', entry)
        return entry

    # Match each JS object literal that contains a symbol field
    return re.sub(r'\{[^{}]*symbol: \'[A-Z]+\'[^{}]*\}', patch_entry, content)

def bump_data_version(fund_data_content):
    today = date.today().strftime('%Y-%m-%d')
    # Read current patch number and increment
    m = re.search(r"const DATA_VERSION = '(\d{4}-\d{2}-\d{2})-(\d+)';", fund_data_content)
    if m and m.group(1) == today:
        patch = int(m.group(2)) + 1
    else:
        patch = 1
    new_ver = f'{today}-{patch}'
    return re.sub(r"const DATA_VERSION = '[^']+';",
                  f"const DATA_VERSION = '{new_ver}';",
                  fund_data_content), new_ver

def git_commit_push(updated_count, version):
    today = date.today().strftime('%B %d, %Y')
    msg = (
        f'Update picks livePrices — {today} (DATA_VERSION {version})\n\n'
        f'{updated_count} symbols updated in model-picks-data.js.\n\n'
        f'Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>'
    )
    subprocess.run(['git', 'add', 'model-picks-data.js', 'fund-data.js'], cwd=REPO, check=True)
    subprocess.run(['git', 'commit', '-m', msg], cwd=REPO, check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO, check=True)

def main():
    with open(PICKS_FILE) as f:
        picks_content = f.read()
    with open(FUND_DATA) as f:
        fund_content = f.read()

    symbols = get_symbols(picks_content)
    print(f'Found {len(symbols)} unique symbols across all picks')

    print('Fetching prices from Finnhub...')
    prices = fetch_prices(symbols)
    print(f'\nFetched {len(prices)}/{len(symbols)} prices')

    if len(prices) < len(symbols) * 0.5:
        print('Fewer than 50% of prices fetched — aborting to avoid bad write')
        sys.exit(1)

    print('Updating model-picks-data.js...')
    new_picks = update_picks(picks_content, prices)

    print('Bumping DATA_VERSION in fund-data.js...')
    new_fund, version = bump_data_version(fund_content)

    with open(PICKS_FILE, 'w') as f:
        f.write(new_picks)
    with open(FUND_DATA, 'w') as f:
        f.write(new_fund)

    git_commit_push(len(prices), version)
    print(f'Done — {len(prices)} picks prices updated, pushed as DATA_VERSION {version}')

if __name__ == '__main__':
    main()
