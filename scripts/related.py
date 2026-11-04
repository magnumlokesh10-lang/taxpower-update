"""Topic-based 'Related pages' chips for every page (own wording, built into each page)."""
L = {
 'home': 'Home', 'taxpowergst': 'TaxPower GST', 'taxpowertds': 'TaxPower TDS', 'gst-return': 'GST returns', 'gst-billing': 'GST billing',
 'pricing': 'Plans & pricing', 'downloads': 'Downloads', 'aboutus': 'About us', 'support': 'Demo & support FAQs', 'technical-support': 'Technical support',
 'demo-enquiry': 'Contact & enquiries', 'free-trial': 'Free trial', 'system-requirements': 'System requirements',
 'taxpower-gst-features': 'All GST features', 'taxpower-tds-features': 'All TDS features',
 'gst-return-filing-software': 'GST return filing', 'gstr-2b-itc-reconciliation-software': 'GSTR-2B ITC reconciliation',
 'e-invoice-e-way-bill-software': 'E-invoice & e-way bill', 'gst-billing-software': 'GST billing software',
 'tds-return-filing-software': 'TDS return filing', 'form-16-form-16a-certificate-software': 'Form 16 & 16A software',
 'gst-tds-due-dates': 'Due dates calendar', 'blog': 'All blogs', 'sitemap': 'Site map',
 'blog/gstr-1-vs-gstr-3b-difference': 'GSTR-1 vs GSTR-3B', 'blog/gstr-2b-itc-reconciliation-checklist': 'GSTR-2B checklist',
 'blog/tds-return-forms-24q-26q-27q-27eq-explained': 'TDS forms explained', 'blog/form-16-and-form-16a-explained': 'Form 16 & 16A explained',
 'blog/how-to-choose-gst-software': 'Choosing GST software', 'blog/taxpower-new-desktop-icons-download-latest-setup': 'New desktop icons',
 'gst-tds-software-vidarbha': 'Software in Vidarbha', 'gst-tds-software-nagpur': 'Nagpur', 'gst-tds-software-amravati': 'Amravati', 'gst-tds-software-akola': 'Akola',
 'gst-tds-software-washim': 'Washim', 'gst-tds-software-buldhana': 'Buldhana', 'gst-tds-software-yavatmal': 'Yavatmal', 'gst-tds-software-wardha': 'Wardha',
 'gst-tds-software-bhandara': 'Bhandara', 'gst-tds-software-gondia': 'Gondia', 'gst-tds-software-chandrapur': 'Chandrapur', 'gst-tds-software-gadchiroli': 'Gadchiroli',
}
try:  # articles written in the CRM get a label automatically
    import cms_posts
    for _x in cms_posts.load_resources()['posts']:
        L.setdefault(_x['slug'], _x['h1'].split(':')[0][:40])
except Exception:
    pass
CITIES = [k for k in L if k.startswith('gst-tds-software-')]
GST = ['taxpowergst', 'taxpower-gst-features', 'gst-return-filing-software', 'gstr-2b-itc-reconciliation-software', 'e-invoice-e-way-bill-software', 'gst-billing-software', 'gst-billing', 'gst-return']
TDS = ['taxpowertds', 'taxpower-tds-features', 'tds-return-filing-software', 'form-16-form-16a-certificate-software', 'blog/tds-return-forms-24q-26q-27q-27eq-explained', 'blog/form-16-and-form-16a-explained']
BLOG = [k for k in L if k.startswith('blog/')] + ['blog', 'gst-tds-due-dates']
HELP = ['free-trial', 'system-requirements', 'technical-support', 'demo-enquiry', 'downloads', 'support']
EXPLICIT = {
 'home': ['taxpowergst', 'taxpowertds', 'pricing', 'free-trial', 'downloads', 'blog', 'gst-tds-software-nagpur', 'aboutus'],
 'pricing': ['blog/taxpower-gst-tds-software-price-india', 'taxpowergst', 'taxpowertds', 'free-trial', 'system-requirements', 'demo-enquiry', 'taxpower-gst-features', 'taxpower-tds-features'],
 'downloads': ['system-requirements', 'technical-support', 'free-trial', 'taxpowergst', 'taxpowertds', 'pricing'],
 'aboutus': ['taxpowergst', 'taxpowertds', 'demo-enquiry', 'technical-support', 'gst-tds-software-vidarbha', 'pricing'],
 'support': ['technical-support', 'demo-enquiry', 'free-trial', 'downloads', 'system-requirements', 'pricing'],
 'technical-support': ['downloads', 'system-requirements', 'support', 'demo-enquiry', 'free-trial', 'pricing'],
 'demo-enquiry': ['free-trial', 'pricing', 'taxpowergst', 'taxpowertds', 'technical-support', 'aboutus'],
 'blog': ['gst-tds-due-dates', 'taxpowergst', 'taxpowertds', 'taxpower-gst-features', 'taxpower-tds-features', 'free-trial'],
 'sitemap': ['home', 'pricing', 'downloads', 'blog', 'demo-enquiry'],
 'taxpowergst': ['taxpower-gst-features', 'gst-return-filing-software', 'gst-billing-software', 'pricing', 'free-trial', 'taxpowertds', 'gst-tds-due-dates'],
 'taxpowertds': ['taxpower-tds-features', 'tds-return-filing-software', 'form-16-form-16a-certificate-software', 'pricing', 'free-trial', 'taxpowergst', 'gst-tds-due-dates'],
}
EXPLICIT['gst-return'] = EXPLICIT['taxpowergst']; EXPLICIT['gst-billing'] = EXPLICIT['taxpowergst']


def related_slugs(slug):
    if slug in EXPLICIT: out = EXPLICIT[slug]
    elif slug in CITIES: out = ['gst-tds-software-vidarbha', 'taxpowergst', 'taxpowertds', 'taxpower-gst-features', 'taxpower-tds-features', 'pricing', 'demo-enquiry'] + [c for c in CITIES if c != slug][:3]
    elif slug in GST or slug.startswith('blog/') and 'gst' in slug: out = GST + ['pricing', 'free-trial'] + ['gst-tds-due-dates']
    elif slug in TDS: out = TDS + ['pricing', 'free-trial', 'gst-tds-due-dates']
    elif slug in BLOG: out = BLOG + ['taxpowergst', 'taxpowertds', 'pricing']
    elif slug in HELP: out = HELP + ['pricing', 'taxpowergst']
    else: out = ['home', 'taxpowergst', 'taxpowertds', 'pricing', 'demo-enquiry']
    seen, res = set(), []
    for s in out:
        if s != slug and s in L and s not in seen: seen.add(s); res.append(s)
    return res[:8]


def block(slug):
    chips = ''.join(f'<a href="{s}">{L[s]}</a>' for s in related_slugs(slug))
    return guide_cards(slug) + (f'<section class="rel-strip" aria-label="Related pages"><div class="rel-inner"><span class="rel-kicker">Related pages</span>'
            f'<div class="rel-chips">{chips}</div></div></section>')


# Articles written in the CRM can ask to be linked from chosen pages (CRM: "Show a link on these pages").
FEATURED = {}
try:
    import cms_posts as _cp
    for _post in _cp.load_resources()['posts']:
        for _page in _post.get('link_from', []):
            if _page in L and not _page.startswith('blog/') and _page != 'blog':
                FEATURED.setdefault(_page, []).append(_post)
    for _page, _posts in FEATURED.items():
        _base = related_slugs(_page)
        EXPLICIT[_page] = [p['slug'] for p in _posts] + [b for b in _base if b not in {p['slug'] for p in _posts}]
except Exception:
    pass


def _esc(x):
    return x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def guide_cards(slug):
    cards = ''
    for p in FEATURED.get(slug, [])[:2]:
        cards += (f'<a class="rel-guide-card" href="{p["slug"]}"><span class="rel-guide-kicker">Guide</span>'
                  f'<strong>{_esc(p["h1"])}</strong><span class="rel-guide-sum">{_esc((p.get("description") or "")[:150])}</span>'
                  f'<span class="rel-guide-go">Read the guide &rarr;</span></a>')
    return f'<section class="rel-guide" aria-label="Featured guide"><div class="rel-guide-in">{cards}</div></section>' if cards else ''
