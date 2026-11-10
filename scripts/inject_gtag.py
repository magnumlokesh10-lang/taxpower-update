#!/usr/bin/env python3
"""Add the Google tag (Analytics) right after <head> on every built page.

The snippet is the one Google Analytics gave for taxpower.co. A small helper after it
reports three actions as events: a saved enquiry (generate_lead), a phone-number click
(click_call) and a WhatsApp click (click_whatsapp). Running this twice is safe.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG_ID = 'GTM-TD9RZJ97'
SNIPPET = f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtm.js?id={TAG_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  document.addEventListener('taxpower:enquiry-saved', function(){{ gtag('event', 'generate_lead', {{page_path: location.pathname}}); }});
  document.addEventListener('click', function(e){{
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null; if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('tel:') === 0) gtag('event', 'click_call', {{page_path: location.pathname}});
    else if (/wa\\.me|whatsapp/i.test(h)) gtag('event', 'click_whatsapp', {{page_path: location.pathname}});
  }}, true);
</script>
'''
SKIP_DIRS = {'_site-source', 'node_modules', '.git', 'scripts', '.github'}


def run():
    done = 0
    for path in ROOT.rglob('*.html'):
        if SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding='utf-8')
        if TAG_ID in text or '<head>' not in text:
            continue
        path.write_text(text.replace('<head>', '<head>\n' + SNIPPET, 1), encoding='utf-8')
        done += 1
    print('Google tag added to', done, 'pages.')


if __name__ == '__main__':
    run()
