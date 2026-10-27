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
 sec('price-how', 'How pricing works', 'What you pay, and when', 'A short guide before you open the plan builder.',
     caps([('tag', 'One-time installation fee', 'The price shown for a plan is paid once, when the software is installed and set up for you.'),
           ('shield', 'First year included', 'Support and software updates are free for the first year after purchase.'),
           ('sync', 'Yearly renewal after that', 'From the second year an annual renewal keeps support and updates going. The builder shows it next to the price.'),
           ('doc', 'GST is added on top', '18% GST is added to the displayed installation price, so your invoice total will be higher than the figure shown.'),
           ('users', 'LAN access is extra', 'Need more than one computer on the same network? Optional LAN access is priced separately per additional PC.'),
           ('list', 'Combine to save', 'Pick GST, billing and TDS together in the plan builder to see a combined price for the modules you choose.')])) +
 sec('price-who', 'Choosing an edition', 'Professional or Business?', 'Two editions, made for two kinds of users.',
     caps([('users', 'Professional', 'For CAs, consultants and tax practices that file for many clients and want client-wise tracking.'),
           ('pc', 'Business', 'For companies and finance teams that prepare returns for their own entities.'),
           ('chat', 'Not sure?', 'Tell us how many GSTINs and TANs you handle and we will suggest the edition during a free demo.')], 'gm-three')) +
 go([('chat', 'gm-go-price', 'free-trial', 'Try it first', 'Start a free trial and test the software on your own data before you decide.', 'Start a free trial'),
     ('list', 'gm-go-tds', 'taxpower-gst-features', 'Compare features', 'See what each module does, grouped by the work you do.', 'Open GST feature guide')]) +
 chips([('System requirements', 'system-requirements'), ('Free trial', 'free-trial'), ('TaxPower TDS features', 'taxpower-tds-features'), ('Contact for a quotation', 'demo-enquiry'), ('Downloads', 'downloads')]))

P['aboutus'] = (
 sec('about-how', 'How we work with you', 'From first call to everyday support', 'A simple path, handled by one local team.',
     steps([('Demo', 'See it on your work', 'We show the modules you need, using steps close to your real filing routine.'),
            ('Install', 'Set it up properly', 'We install TaxPower, load your masters and check that returns and certificates open correctly.'),
            ('Train', 'Teach your team', 'Short, practical sessions so staff can file and reconcile without waiting for us.'),
            ('Support', 'Stay on call', 'Phone and remote help for installation, updates, licences and filing questions.'),
            ('Renew', 'Keep it current', 'We remind you about yearly renewals so support and updates continue without a break.')])) +
 sec('about-why', 'Why a local dealer', 'Software from Magnum, service from Nagpur', 'What it means for you in practice.',
     caps([('chat', 'Your language', 'We explain and support in Marathi, Hindi and English, so the whole team understands the steps.'),
           ('pin', 'Close by', 'Our office is in Hingna MIDC, Nagpur, and we serve every district in Vidarbha as well as customers across India.'),
           ('shield', 'Authorized dealer', 'We sell and support TaxPower as an authorized dealer of Magnum Infosystem, the company that develops it.')], 'gm-three')) +
 go([('list', 'gm-go-tds', 'taxpowergst', 'Explore TaxPower GST', 'Returns, reconciliation, e-invoice and billing in one place.', 'See TaxPower GST'),
     ('doc', 'gm-go-price', 'taxpowertds', 'Explore TaxPower TDS', 'Statements, TRACES and certificates in one workspace.', 'See TaxPower TDS')]) +
 chips([('Software in Vidarbha', 'gst-tds-software-vidarbha'), ('Nagpur', 'gst-tds-software-nagpur'), ('Technical support', 'technical-support'), ('Contact & enquiries', 'demo-enquiry'), ('Blog', 'blog')]))

P['downloads'] = (
 sec('dl-before', 'Before you install', 'A short checklist for a smooth setup', 'Five minutes here saves time later.',
     steps([('Check', 'Your computer', 'Confirm Windows version, memory and disk space against the system requirements page.'),
            ('Backup', 'Existing data', 'If you are updating, copy your current company data to a safe place first.'),
            ('Download', 'The right setup', 'Pick the GST or TDS setup you have a licence or trial for from the list above.'),
            ('Install', 'Supporting items', 'The database and runtime packages listed here are needed by some versions. The installer tells you which.'),
            ('Ask', 'If anything stops', 'Keep the error message and your licence ID ready and call technical support.')])) +
 sec('dl-what', 'What is what', 'Why the extra downloads are here', 'Short notes on the helper packages so you do not install blindly.',
     caps([('pc', 'Database packages', 'SQL Server Express and PostgreSQL store your company data on the computer.'),
           ('doc', 'Runtime packages', '.NET and Java runtimes let TaxPower and some utilities run on Windows.'),
           ('shield', 'GST Signer', 'A small utility used with a digital signature certificate when signing returns.')], 'gm-three')) +
 go([('pc', 'gm-go-price', 'system-requirements', 'Will it run on my PC?', 'Windows, memory, disk, internet and DSC details.', 'Check requirements'),
     ('phone', 'gm-go-tds', 'technical-support', 'Stuck during install?', 'Reach our technical support team by phone or email.', 'Get technical help')]) +
 chips([('Free trial', 'free-trial'), ('Plans & pricing', 'pricing'), ('TaxPower GST', 'taxpowergst'), ('TaxPower TDS', 'taxpowertds')]))

P['support'] = (
 sec('sup-which', 'Which team to call', 'Pick the right door', 'It gets you an answer faster.',
     caps([('chat', 'Demo, quotation, renewal', 'Use the enquiry form or call the sales line for a demo, a price or to renew a licence.'),
           ('phone', 'Technical problem', 'For installation, updates, licence or software errors, use technical support.'),
           ('doc', 'Learning the software', 'Ask for a training session, or read the feature guides and blog explainers first.')], 'gm-three')) +
 sec('sup-ready', 'Before you call', 'Keep these ready', 'A few details help us fix things in one call.',
     steps([('Licence', 'Customer or licence ID', 'It tells us which edition and modules you have.'),
            ('Screen', 'Error message', 'Note the text or take a screenshot of the message.'),
            ('Task', 'What you were doing', 'Filing, importing, updating or printing? The step matters.'),
            ('Version', 'Software version', 'It is shown inside the software. Update first if you are on an old one.'),
            ('Time', 'Remote help', 'For remote help keep the computer on, online and free for a short while.')])) +
 go([('list', 'gm-go-price', 'taxpower-gst-features', 'Look up a feature', 'See what TaxPower GST can do for each task.', 'GST feature guide'),
     ('list', 'gm-go-tds', 'taxpower-tds-features', 'Look up a TDS feature', 'Statements, TRACES, challans and certificates.', 'TDS feature guide')]) +
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
