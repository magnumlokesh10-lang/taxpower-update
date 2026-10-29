"""Post-build step: add FAQPage schema from the visible FAQ blocks and a speakable hint to each page's WebPage schema."""
import html as H, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DET = re.compile(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*(.*?)</details>', re.S)
SKIP = {'nav.html', 'footer.html'}


def clean(s):
    return H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()


def process(path):
    s = path.read_text()
    if 'id="site-structured-data"' not in s:
        return False
    items = []
    for q, a in DET.findall(s):
        q, a = clean(q), clean(a)
        if q.endswith('?') and len(a) > 20 and q not in [i['name'] for i in items]:
            items.append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    out = s
    # speakable hint on the WebPage node
    m = re.search(r'(<script type="application/ld\+json" id="site-structured-data"[^>]*>)(.*?)(</script>)', out, re.S)
    if m:
        try:
            data = json.loads(m.group(2))
            for node in data.get('@graph', []):
                t = node.get('@type')
                if (t == 'WebPage' or (isinstance(t, list) and 'WebPage' in t)) and 'speakable' not in node:
                    node['speakable'] = {'@type': 'SpeakableSpecification', 'cssSelector': ['h1', '.lp-lead', '.hx-lead']}
            out = out[:m.start(2)] + json.dumps(data) + out[m.end(2):]
        except ValueError:
            pass
    if len(items) >= 2 and 'id="faq-structured-data"' not in out:
        block = '<script type="application/ld+json" id="faq-structured-data">' + json.dumps(
            {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': items}) + '</script>'
        out = out.replace('</head>', block + '</head>', 1)
    if out != s:
        path.write_text(out)
        return len(items) >= 2
    return False


def run():
    n = 0
    for p in ROOT.rglob('*.html'):
        rel = p.relative_to(ROOT)
        if p.name in SKIP or rel.parts[0] in {'_site-source', 'tests', 'docs', 'dist', 'node_modules'}:
            continue
        n += bool(process(p))
    print('FAQ schema added to', n, 'pages')


if __name__ == '__main__':
    run()
