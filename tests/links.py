"""Internal link check: every page must be linked from at least 3 other pages, and no link may point to a missing page."""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
pages = {p.stem: p for p in root.glob('*.html') if p.stem not in ('nav', 'footer', 'index')}
pages.update({f'blog/{p.stem}': p for p in (root / 'blog').glob('*.html') if p.stem != 'index'})
inbound = {k: set() for k in pages}
broken = []
for slug, p in pages.items():
    for h in re.findall(r'href="([^"#?]+)', p.read_text()):
        if re.match(r'(https?:|mailto:|tel:|/|asset/|css/|js/|data:)', h) or '.' in h.split('/')[-1]: continue
        t = h.strip('/')
        if t == 'index': t = 'home'
        if t not in pages: broken.append((slug, h)); continue
        if t != slug: inbound[t].add(slug)
low = {k: len(v) for k, v in inbound.items() if len(v) < 3}
print('pages:', len(pages), '| broken:', len(broken), '| under-linked:', low)
for b in broken[:20]: print('BROKEN', b)
sys.exit(1 if broken or low else 0)
