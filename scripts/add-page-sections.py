"""One-off helper: inserts original helpful sections into pricing, about, downloads and support sources (idempotent)."""
import re, html
from pathlib import Path
R = Path(__file__).resolve().parents[1]
e = html.escape
def ico(p): return f'<span class="gm-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg></span>'
I = {'tag': '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="8" cy="9" r="1.5"/>', 'shield': '<path d="M12 3l8 4v5c0 5-4 8-8 9-4-1-8-4-8-9V7z"/><path d="M9 12l2 2 4-4"/>',
     'sync': '<path d="M20 8a8 8 0 0 0-14-2L4 8M4 4v4h4M4 16a8 8 0 0 0 14 2l2-2M20 20v-4h-4"/>', 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0M16 5a3.5 3.5 0 0 1 0 7M18 20a6 6 0 0 0-3-5"/>',
     'doc': '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>', 'pc': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
     'dl': '<path d="M12 4v11m0 0 4-4m-4 4-4-4M5 20h14"/>', 'chat': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>', 'pin': '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
     'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', 'list': '<path d="M4 6h16M4 12h16M4 18h10"/>', 'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2z"/>'}
def head(k, h, p, i): return f'<header class="gm-head"><span class="gm-kicker">{e(k)}</span><h2 id="{i}">{e(h)}</h2><p>{e(p)}</p></header>'
def caps(items, cls=''): return f'<ul class="gm-capgrid {cls}">' + ''.join(f'<li class="gm-cap">{ico(I[ic]) if ic else ""}<div><h3>{e(h)}</h3><p>{e(b)}</p></div></li>' for ic, h, b in items) + '</ul>'
def steps(items): return '<ol class="gb-steps">' + ''.join(f'<li class="gb-step"><span class="gb-n">{i+1}</span><small>{e(a)}</small><h3>{e(b)}</h3><p>{e(c)}</p></li>' for i, (a, b, c) in enumerate(items)) + '</ol>'
def chips(items): return '<ul class="gm-chips">' + ''.join(f'<li><a href="{h}">{e(n)}</a></li>' for n, h in items) + '</ul>'
def sec(i, kicker, h, p, body, cls='gm'): return f'<section class="{cls}" id="{i}" aria-labelledby="{i}-t">{head(kicker, h, p, i + "-t")}{body}</section>\n'
def go(items):
    c = ''.join(f'<a class="gm-go-card {cl}" href="{h}">{ico(I[ic])}<div><h3>{e(t)}</h3><p>{e(d)}</p></div><span class="gm-go-btn">{e(b)} <i aria-hidden="true">→</i></span></a>' for ic, cl, h, t, d, b in items)
    return f'<div class="gm-go{" gm-go-one" if len(items) == 1 else ""}">{c}</div>\n'

P = {}
P['pricing'] = (
 sec('price-how', 'How pricing works', 'Payment terms', 'Please read these notes before you open the plan builder.',
     caps([('tag', 'One-time installation fee', 'The price shown for a plan is paid once, at the time the software is installed.'),
           ('shield', 'First year included', 'Support and software updates are provided free for the first year after purchase.'),
           ('sync', 'Annual renewal', 'From the second year, an annual renewal is required to continue support and updates. The renewal amount is shown beside the price in the plan builder.'),
           ('doc', 'GST is added on top', 'GST at 18% is charged on the displayed installation price, so the invoice total is higher than the price shown.'),
           ('users', 'LAN access is extra', 'Use on more than one computer in the same office network is optional and is charged separately for each additional PC.'),
           ('list', 'Combined modules', 'Select GST, billing and TDS together in the plan builder to see one price for the modules you choose.')])) +
 sec('price-who', 'Choosing an edition', 'Professional or Business', 'Select the edition that matches how you use the software.',
     caps([('users', 'Professional', 'Suitable for chartered accountants, tax consultants and practices that file returns for several clients and need client-wise records.'),
           ('pc', 'Business', 'Suitable for companies and accounts teams that prepare returns for their own registrations.'),
           ('chat', 'Need help choosing', 'Share the GSTINs and TANs you handle and we will recommend an edition during a demo.')], 'gm-three')) +
 go([('chat', 'gm-go-price', 'free-trial', 'Free trial', 'Use the software with your own data before you decide to buy.', 'Start a free trial'),
     ('list', 'gm-go-tds', 'taxpower-gst-features', 'Feature guide', 'Each module and its features, listed by type of work.', 'Open GST feature guide')]) +
 chips([('System requirements', 'system-requirements'), ('Free trial', 'free-trial'), ('TaxPower TDS features', 'taxpower-tds-features'), ('Contact for a quotation', 'demo-enquiry'), ('Downloads', 'downloads')]))

P['aboutus'] = (
 sec('about-how', 'Our process', 'From the first demo to ongoing support', 'Every customer is handled by the same local team through these stages.',
     steps([('Demo', 'Product demonstration', 'We demonstrate the modules relevant to your work, following your usual filing routine.'),
            ('Install', 'Installation', 'We install TaxPower, load your masters and confirm that returns and certificates open correctly.'),
            ('Train', 'Training', 'Practical sessions for your staff on filing and reconciliation.'),
            ('Support', 'Support', 'Telephone and remote assistance for installation, updates, licences and filing queries.'),
            ('Renew', 'Renewal', 'We inform you before the annual renewal date so that support and updates continue.')])) +
 sec('about-why', 'Local dealer', 'Software by Magnum, service from Nagpur', 'What our customers receive from a dealer based in Nagpur.',
     caps([('chat', 'Language', 'Demonstration, training and support are available in Marathi, Hindi and English.'),
           ('pin', 'Location', 'Our office is in Hingna MIDC, Nagpur. We serve Vidarbha and customers across India.'),
           ('shield', 'Authorized dealer', 'We sell and support TaxPower as an authorized dealer of Magnum Infosystem, the developer of the software.')], 'gm-three')) +
 go([('list', 'gm-go-tds', 'taxpowergst', 'Explore TaxPower GST', 'Return filing, reconciliation, e-invoicing and billing.', 'See TaxPower GST'),
     ('doc', 'gm-go-price', 'taxpowertds', 'Explore TaxPower TDS', 'TDS statements, TRACES activities and certificates.', 'See TaxPower TDS')]) +
 chips([('Software in Vidarbha', 'gst-tds-software-vidarbha'), ('Nagpur', 'gst-tds-software-nagpur'), ('Technical support', 'technical-support'), ('Contact & enquiries', 'demo-enquiry'), ('Blog', 'blog')]))

P['downloads'] = (
 sec('dl-before', 'Before installation', 'Installation checklist', 'Please go through these points before you install.',
     steps([('Check', 'System', 'Compare your Windows version, memory and disk space with the system requirements page.'),
            ('Backup', 'Existing data', 'When updating, first copy your current company data to a safe location.'),
            ('Download', 'Setup file', 'Choose the GST or TDS setup for which you hold a licence or trial, from the list above.'),
            ('Install', 'Supporting packages', 'Some versions need the database and runtime packages listed here. The installer indicates which are required.'),
            ('Contact', 'If installation stops', 'Note the error message and your licence ID and contact technical support.')])) +
 sec('dl-what', 'Supporting downloads', 'Purpose of the additional downloads', 'A brief note on each supporting package listed on this page.',
     caps([('pc', 'Database packages', 'SQL Server Express and PostgreSQL are used to store company data on the computer.'),
           ('doc', 'Runtime packages', '.NET and Java runtimes are required by TaxPower and some of its utilities on Windows.'),
           ('shield', 'GST Signer', 'A utility used with a digital signature certificate for signing returns.')], 'gm-three')) +
 go([('pc', 'gm-go-price', 'system-requirements', 'System requirements', 'Windows version, memory, disk space, internet and DSC details.', 'Check requirements'),
     ('phone', 'gm-go-tds', 'technical-support', 'Technical support', 'Contact our technical support team by phone or email.', 'Contact technical support')]) +
 chips([('Free trial', 'free-trial'), ('Plans & pricing', 'pricing'), ('TaxPower GST', 'taxpowergst'), ('TaxPower TDS', 'taxpowertds')]))

P['support'] = (
 sec('sup-which', 'Who to contact', 'Choose the right contact', 'Contacting the correct team gets your query resolved sooner.',
     caps([('chat', 'Demo, quotation and renewal', 'Use the enquiry form or call us for a demo, a price quotation or a licence renewal.'),
           ('phone', 'Technical issues', 'For installation, updates, licence problems or software errors, contact technical support.'),
           ('doc', 'Training and guidance', 'Request a training session, or refer to the feature guides and blog articles.')], 'gm-three')) +
 sec('sup-ready', 'Before you contact us', 'Details to keep ready', 'These details help us resolve your query faster.',
     steps([('Licence', 'Customer or licence ID', 'It shows the edition and modules you have.'),
            ('Screen', 'Error message', 'Note the text of the message or take a screenshot.'),
            ('Task', 'The task you were doing', 'For example filing, importing data, updating or printing.'),
            ('Version', 'Software version', 'The version is shown inside the software. If it is an old version, update it first.'),
            ('Time', 'Remote assistance', 'For remote assistance, keep the computer switched on, connected to the internet and free.')])) +
 go([('list', 'gm-go-price', 'taxpower-gst-features', 'TaxPower GST features', 'Features of TaxPower GST, listed by task.', 'GST feature guide'),
     ('list', 'gm-go-tds', 'taxpower-tds-features', 'TaxPower TDS features', 'Statements, TRACES, challans and certificates.', 'TDS feature guide')]) +
 chips([('Nagpur', 'gst-tds-software-nagpur'), ('Amravati', 'gst-tds-software-amravati'), ('Akola', 'gst-tds-software-akola'), ('All Vidarbha', 'gst-tds-software-vidarbha'), ('System requirements', 'system-requirements'), ('Downloads', 'downloads')]))

MARK = '<!--tp-extra-sections-->'
END = '<!--/tp-extra-sections-->'
for name, body in P.items():
    f = R / '_site-source' / f'{name}.html'; s = open(f).read()
    s = re.sub(re.escape(MARK) + r'.*?' + re.escape(END), '', s, flags=re.S)
    s = s.replace('</main>', MARK + '\n' + body + END + '\n</main>', 1)
    if 'css/gst-more.css' not in s:
        s = re.sub(r'(<link rel="stylesheet" href="css/support-cards\.css[^>]*>)', r'\1\n  <link rel="stylesheet" href="css/gst-more.css?v=1">', s, count=1)
        if 'css/gst-more.css' not in s: s = s.replace('</head>', '  <link rel="stylesheet" href="css/gst-more.css?v=1">\n</head>', 1)
    open(f, 'w').write(s)
print('ok')
