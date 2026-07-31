#!/usr/bin/env python3
"""Apply and verify the CARD LINK RULE on polymarket/index.html.

Every idea card's date line must end with an anchor to the Polymarket market that
card is about. See the "Polymarket sub-site" section of CLAUDE.md.

Usage:
    scripts/pm-link-cards.py polymarket/index.html          # apply (idempotent)
    scripts/pm-link-cards.py polymarket/index.html --check   # verify only, exit 1 on failure

Safe to re-run: existing pm-card-link anchors are stripped before re-applying.
"""
import re
import sys

EVENT = 'https://polymarket.com/event/'
PORTFOLIO = 'https://polymarket.com/portfolio'

# Card-title keyword -> Polymarket event slug.
# When a new market is added to the playbook, add its slug here AND a matching
# rule in pick_url() below. Never guess a slug: confirm it resolves first.
SLUGS = {
    'jul':    'largest-company-end-of-july-20260624192302727',
    'aug':    'largest-company-end-of-august-20260715202138598',
    'dec':    'largest-company-end-of-december-2026',
    '2jul':   '2nd-largest-company-end-of-july-20260624192727948',
    '2aug':   '2nd-largest-company-end-of-august-20260715202554129',
    '3jul':   '3rd-largest-company-end-of-july-20260624193025470',
    '3aug':   '3rd-largest-company-end-of-august-20260715203029875',
    'spyjul': 'what-price-will-spy-hit-in-july-2026',
    'spyaug': 'what-price-will-spy-hit-in-august-2026',
    'btcjul': 'what-price-will-bitcoin-hit-in-july-2026',
    'wtijul': 'what-price-will-wti-hit-in-july-2026',
    'wtiaug': 'what-price-will-wti-hit-in-august-2026',
    'amzn':   'what-price-will-amzn-hit-in-july-2026',
    'nlc':    'mlb-2026-nl-central-champion',
    'nlw':    'mlb-2026-nl-west-champion',
    'ws':     'mlb-world-series-champion-2026',
    'so':     'mlb-strikeouts-leader-pitcher',
    'rbi':    'mlb-rbis-leader',
}

CARD_RE = re.compile(
    r'<h3 class="panel-title">(.*?)</h3>\s*<div class="pm-idea-date">(.*?)</div>',
    re.S,
)
ANCHOR_RE = re.compile(r'\s*<a class="pm-card-link"[^>]*>.*?</a>', re.S)


def pick_url(title_html):
    """Map a card title to (url, human_label). Order matters — most specific first."""
    text = re.sub(r'<[^>]+>', '', title_html).lower()

    def has(*needles):
        return any(n.lower() in text for n in needles)

    if has('3rd-largest august', '3rd-largest aug', '"3rd-largest', '3rd spot', '#3 spot'):
        return EVENT + SLUGS['3aug'], '3rd-largest, August'
    if has('second-place july', '2nd-largest july', '2nd largest july'):
        return EVENT + SLUGS['2jul'], '2nd-largest, July'
    if has('second-place august', 'second place, august', '2nd-largest august',
           '2nd largest august', '2nd-aug'):
        return EVENT + SLUGS['2aug'], '2nd-largest, August'
    if has('wti august', 'wti $140', 'wti $150', '$40-low', 'august $140', 'august tail'):
        return EVENT + SLUGS['wtiaug'], 'WTI, August'
    if has('wti $80-low', 'wti $80', 'wti crude'):
        return EVENT + SLUGS['wtijul'], 'WTI, July'
    if has('august spy', 'spy ladder', 'spy/btc', 'aug 1 roll', 'carry roll'):
        return EVENT + SLUGS['spyaug'], 'SPY, August'
    if has('spy $770', 'spy $700', 'carry ladder'):
        return EVENT + SLUGS['spyjul'], 'SPY, July'
    if has('btc $', 'bitcoin'):
        return EVENT + SLUGS['btcjul'], 'Bitcoin, July'
    if has('amzn $264', 'amazon.com'):
        return EVENT + SLUGS['amzn'], 'AMZN, July'
    if has('pirates', 'padres'):
        return EVENT + SLUGS['nlc'], 'NL Central'
    if has('braves', 'world series'):
        return EVENT + SLUGS['ws'], 'World Series 2026'
    if has('cease', 'skenes', 'strikeout'):
        return EVENT + SLUGS['so'], 'MLB strikeout leader'
    if has('james wood', 'rbi'):
        return EVENT + SLUGS['rbi'], 'MLB RBI leader'
    if has('aramco'):
        return EVENT + SLUGS['dec'], 'Largest company, December'
    # Account-hygiene cards are the ONLY permitted non-/event/ links.
    if has('redeem', 'resting orders', 'cancel stale'):
        return PORTFOLIO, 'Your portfolio'
    if has('september book', 'listing-day kink', 'listing lag'):
        return EVENT + SLUGS['aug'], 'Largest company, August'
    if has('august', 'aug 31', '-aug'):
        return EVENT + SLUGS['aug'], 'Largest company, August'
    if has('december', 'dec 31', '-dec'):
        return EVENT + SLUGS['dec'], 'Largest company, December'
    if has('july', 'jul 31', '-jul', 'thursday', 'print', 're-flip', 'flow',
           'weekend', 'regime', 'stale-feed', 'crown'):
        return EVENT + SLUGS['jul'], 'Largest company, July'
    return EVENT + SLUGS['aug'], 'Largest company, August'


def apply(path):
    html = open(path).read()
    html = ANCHOR_RE.sub('', html)  # idempotent: strip prior anchors first
    count = 0

    def repl(m):
        nonlocal count
        title, date = m.group(1), m.group(2)
        url, _ = pick_url(title)
        count += 1
        return (
            f'<h3 class="panel-title">{title}</h3>\n            '
            f'<div class="pm-idea-date">{date}'
            f'<a class="pm-card-link" href="{url}" target="_blank" rel="noopener" '
            f'title="Open this market on Polymarket">View on Polymarket ↗</a></div>'
        )

    open(path, 'w').write(CARD_RE.sub(repl, html))
    print(f'{path}: {count} cards linked')
    return count


MONTHS = (('july', 'jul'), ('august', 'aug'), ('december', 'dec'))


def check(path):
    html = open(path).read()
    n_anchor = html.count('class="pm-card-link"')
    n_label = html.count('View on Polymarket')
    n_card = html.count('pm-idea-date')
    problems = []

    if not (n_anchor == n_label == n_card):
        problems.append(
            f'count mismatch: pm-card-link={n_anchor}, '
            f'"View on Polymarket"={n_label}, pm-idea-date={n_card}'
        )

    for m in CARD_RE.finditer(html):
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        href = re.search(r'href="([^"]+)"', m.group(2))
        if not href:
            problems.append(f'card has no link: {title[:70]}')
            continue
        url = href.group(1)
        if url == PORTFOLIO:
            continue  # account-hygiene card, exempt by design
        low = title.lower()
        mentioned = [(long_name, short) for long_name, short in MONTHS if long_name in low]
        if mentioned and not any(
            f'-{short}' in url or long_name in url for long_name, short in mentioned
        ):
            names = '/'.join(n for n, _ in mentioned)
            problems.append(f'month mismatch ({names}): {title[:60]} -> {url}')

    if problems:
        print(f'FAIL ({len(problems)} problem(s)):')
        for p in problems:
            print('  -', p)
        return 1
    print(f'OK: {n_card} cards, {n_anchor} links, no month mismatches')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    target = sys.argv[1]
    if '--check' in sys.argv:
        sys.exit(check(target))
    apply(target)
    sys.exit(check(target))
