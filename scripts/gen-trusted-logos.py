#!/usr/bin/env python3
"""Rewrite the trusted-clients logo rows in _site-source/index.html from scripts/trusted-clients.json.

Logos alternate between two rows, so a logo never shows in both rows at once.
Add a logo: put the .webp in asset/clients/, add an entry to trusted-clients.json
(slug, name, file, w, h, dark=1 if the logo has white text), then run this script.
"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(ROOT, 'scripts/trusted-clients.json')))
CARD_PX, PX_PER_SEC = 220, 38

def card(c, hidden=False):
    cls = 'company-logo-card' + (' is-dark' if c.get('dark') else '')
    alt = '' if hidden else f"{c['name']} logo"
    h = ' aria-hidden="true"' if hidden else ''
    return f'<li class="{cls}"{h}><img src="{c["file"]}" alt="{alt}" width="{c["w"]}" height="{c["h"]}" loading="eager" decoding="async"></li>'

def row(items, cls, label):
    # make sure one set is wider than a big screen, then double it for the seamless loop
    base = items
    while len(base) * CARD_PX < 2400:
        base = base + items
    dur = round(len(base) * CARD_PX / PX_PER_SEC)
    cards = ''.join(card(c) for c in base) + ''.join(card(c, True) for c in base)
    return (f'<div class="company-logo-marquee is-animated {cls}" role="group" aria-label="{label}">'
            f'<ul class="company-logo-track" style="--dur:{dur}s">{cards}</ul></div>')

html = (row(L[0::2], 'row-a', 'Companies that use TaxPower') + '\n      ' +
        row(L[1::2], 'row-b', 'More companies that use TaxPower'))
p = os.path.join(ROOT, '_site-source/index.html')
s = open(p, encoding='utf-8').read()
pat = re.compile(r'(<!--logos:start-->).*?(<!--logos:end-->)', re.S)
if not pat.search(s):
    m = re.search(r'<div class="company-logo-marquee.*?</ul></div>\s*<div class="company-logo-marquee.*?</ul></div>', s, re.S)
    s = s.replace(m.group(0), '<!--logos:start--><!--logos:end-->')
s = pat.sub(lambda m: m.group(1) + html + m.group(2), s)
open(p, 'w', encoding='utf-8').write(s)
print('rows:', len(L[0::2]), len(L[1::2]))
