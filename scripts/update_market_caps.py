#!/usr/bin/env python3
"""
Weekly market cap updater — runs every Monday morning.
Fetches Finnhub profile2 for all POSITIONS, updates fund-data.js,
bumps DATA_VERSION, then commits and pushes to GitHub Pages.

Skips ETFs (FCG, REMX, COPX) and TSM (Finnhub returns TWD for that ticker).
"""

import re, json, urllib.request, time, subprocess, sys
from datetime import date

API_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg'
FUND_DATA = '/Users/chadfisher/Leadsure/fund-data.js'
REPO = '/Users/chadfisher/Leadsure'

# Tickers to skip: ETFs have no market cap; TSM Finnhub returns TWD not USD
SKIP = {'FCG', 'REMX', 'COPX', 'TSM', 'EXPI'}

def fetch_market_caps(symbols):
    caps = {}
    for sym in symbols:
        if sym in SKIP:
            continue
        url = f'https://finnhub.io/api/v1/stock/profile2?symbol={sym}&token={API_KEY}'
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, timeout=10) as r:
                    d = json.loads(r.read())
                mc = d.get('marketCapitalization', 0)
                if mc:
                    caps[sym] = int(mc * 1_000_000)
                    print(f'  {sym}: ${caps[sym]:,}')
                else:
                    print(f'  {sym}: no data (skipping)')
                break
            except Exception as e:
                if attempt == 2:
                    print(f'  {sym} FAILED after 3 attempts: {e}')
                else:
                    time.sleep(2)
        time.sleep(0.15)
    return caps

def update_file(caps):
    with open(FUND_DATA) as f:
        content = f.read()

    updated = 0
    for sym, new_mc in caps.items():
        pattern = rf'("symbol": "{sym}".*?"marketCap": )\d+'
        new_content = re.sub(pattern, rf'\g<1>{new_mc}', content)
        if new_content != content:
            content = new_content
            updated += 1

    today = date.today().strftime('%Y-%m-%d')
    # Increment patch version (e.g. 20260601-1 → 20260608-1)
    content = re.sub(
        r"const DATA_VERSION = '[^']+';",
        f"const DATA_VERSION = '{today}-1';",
        content
    )

    with open(FUND_DATA, 'w') as f:
        f.write(content)

    return updated

def git_commit_push(updated_count):
    today = date.today().strftime('%B %d, %Y')
    msg = (
        f'Weekly market cap update — {today}\n\n'
        f'{updated_count} positions updated via Finnhub profile2.\n'
        f'TSM, FCG, REMX, COPX, EXPI skipped (ETFs or TWD-denominated).\n\n'
        f'Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>'
    )
    subprocess.run(['git', 'add', 'fund-data.js'], cwd=REPO, check=True)
    subprocess.run(['git', 'commit', '-m', msg], cwd=REPO, check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO, check=True)

def main():
    with open(FUND_DATA) as f:
        content = f.read()

    positions_start = content.find('const POSITIONS = [')
    positions_end = content.find('];', positions_start)
    symbols = re.findall(r'"symbol": "([A-Z]+)"', content[positions_start:positions_end])
    print(f'Found {len(symbols)} symbols in POSITIONS')

    print('Fetching market caps...')
    caps = fetch_market_caps(symbols)
    print(f'\nFetched {len(caps)} market caps')

    if not caps:
        print('No data fetched — aborting')
        sys.exit(1)

    updated = update_file(caps)
    print(f'Updated {updated} entries in fund-data.js')

    git_commit_push(updated)
    print('Done — pushed to GitHub Pages')

if __name__ == '__main__':
    main()
