#!/usr/bin/env python3
"""Parse a Redfin 'Download All' export (.numbers or .csv) into marcy/listings.js.

Usage:  parse-redfin.py <export.numbers|export.csv> <out/listings.js>

Columns are matched by header NAME (case-insensitive substring), so it keeps
working if Redfin reorders columns. .numbers requires the `numbers-parser`
package (the wrapper script installs it in a venv); .csv needs nothing extra.
"""
import sys, json, csv, datetime, os


def num(v):
    try:
        return float(str(v).replace(',', '').replace('$', '').strip())
    except (TypeError, ValueError):
        return None


def cleannum(v):
    n = num(v)
    if n is None:
        return 0
    return int(n) if n == int(n) else round(n, 1)


def s(v):
    return '' if v is None else str(v).strip()


def mtype(t):
    t = (t or '').lower()
    if 'condo' in t or 'co-op' in t:
        return 'Condo'
    if 'town' in t:
        return 'Townhome'
    if 'single' in t or 'residential' in t:
        return 'House'
    if 'multi' in t:
        return 'Multi-family'
    if 'land' in t or 'lot' in t:
        return 'Land'
    return t.title() or 'Home'


def read_rows(path):
    if path.lower().endswith('.numbers'):
        from numbers_parser import Document
        return Document(path).sheets[0].tables[0].rows(values_only=True)
    with open(path, newline='', encoding='utf-8-sig') as f:
        return [list(r) for r in csv.reader(f)]


def col_map(header):
    cols = [(i, s(h).upper()) for i, h in enumerate(header)]

    def find(*names):
        for n in names:
            for i, h in cols:
                if n in h:
                    return i
        return None

    return {k: find(*v) for k, v in {
        'type': ['PROPERTY TYPE'], 'addr': ['ADDRESS'], 'zip': ['ZIP'],
        'price': ['PRICE'], 'beds': ['BEDS'], 'baths': ['BATHS'],
        'sqft': ['SQUARE FEET'], 'year': ['YEAR BUILT'], 'dom': ['DAYS ON MARKET'],
        'loc': ['LOCATION'], 'status': ['STATUS'], 'url': ['URL'],
        'lat': ['LATITUDE'], 'lng': ['LONGITUDE'],
    }.items()}


def main():
    if len(sys.argv) != 3:
        sys.exit('usage: parse-redfin.py <export.numbers|csv> <out/listings.js>')
    src, out = sys.argv[1], sys.argv[2]
    rows = read_rows(src)
    if not rows:
        sys.exit('empty file: ' + src)
    c = col_map(rows[0])
    if c['addr'] is None or c['price'] is None:
        sys.exit('could not find ADDRESS/PRICE columns — is this a Redfin export?')

    def g(r, key):
        i = c.get(key)
        return r[i] if (i is not None and i < len(r)) else None

    listings = []
    for r in rows[1:]:
        addr, price, status = s(g(r, 'addr')), num(g(r, 'price')), s(g(r, 'status'))
        if not addr or not price or price <= 0:
            continue
        if 'sold' in status.lower():
            continue
        try:
            zipc = str(int(num(g(r, 'zip'))))
        except (TypeError, ValueError):
            zipc = s(g(r, 'zip')) or '98199'
        dom, year = num(g(r, 'dom')), num(g(r, 'year'))
        typ = mtype(s(g(r, 'type')))
        blurb = ' · '.join([typ, s(g(r, 'loc')) or 'Magnolia'] +
                                (['built %d' % int(year)] if year else []))
        listings.append({
            'id': 'mag-%03d' % (len(listings) + 1),
            'address': addr, 'zip': zipc, 'price': int(price),
            'beds': cleannum(g(r, 'beds')), 'baths': cleannum(g(r, 'baths')),
            'sqft': int(num(g(r, 'sqft'))) if num(g(r, 'sqft')) else 0,
            'type': typ, 'status': 'New' if (dom is not None and dom <= 7) else 'Active',
            'blurb': blurb, 'photo': None, 'url': s(g(r, 'url')) or None,
            'lat': num(g(r, 'lat')), 'lng': num(g(r, 'lng')),
        })
    if not listings:
        sys.exit('no valid listings parsed from ' + src)

    hdr = ("/* AUTO-GENERATED from %s on %s by scripts/refresh-marcy-listings.sh.\n"
           "   Real Magnolia (98199) for-sale listings. Re-run the script to refresh. */\n"
           % (os.path.basename(src), datetime.date.today().isoformat()))
    with open(out, 'w', encoding='utf-8') as f:
        f.write(hdr + 'const MARCY_LISTINGS = ' + json.dumps(listings, indent=2) + ';\n')
    print('Wrote %d listings to %s' % (len(listings), out))


if __name__ == '__main__':
    main()
