"""Blog posts written in the TaxPower CRM.

The CRM saves every published article as content/blog/<name>.json. This module merges those
files with the hand-written posts in scripts/resource-pages.json so the blog index, sitemap,
related links and article pages are all built from one list. A broken file is skipped with a
warning so one bad article can never stop the whole site from building.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOCK_TYPES = {'h2', 'h3', 'p', 'list', 'steps', 'note', 'faq', 'links', 'table'}
SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
TIME_RE = re.compile(r'^([01]\d|2[0-3]):[0-5]\d$')


def _text(v, limit=4000):
    return v.strip()[:limit] if isinstance(v, str) else ''


def _clean_block(b):
    if not isinstance(b, dict) or b.get('t') not in BLOCK_TYPES:
        return None
    t, v = b['t'], b.get('v')
    if t == 'table':
        head = [_text(h, 160) for h in (b.get('head') if isinstance(b.get('head'), list) else [])][:8]
        rows = []
        for r in (b.get('rows') if isinstance(b.get('rows'), list) else [])[:60]:
            if isinstance(r, list):
                cells = [_text(c, 400) for c in r][:len(head)]
                cells += [''] * (len(head) - len(cells))
                if any(cells):
                    rows.append(cells)
        return {'t': t, 'head': head, 'rows': rows} if head and any(head) and rows else None
    if t in ('h2', 'h3', 'p', 'note'):
        v = _text(v)
        return {'t': t, 'v': v} if v else None
    if t in ('list', 'steps'):
        items = [_text(i, 600) for i in (v if isinstance(v, list) else [])]
        items = [i for i in items if i]
        return {'t': t, 'v': items} if items else None
    if t == 'faq':
        items = []
        for i in (v if isinstance(v, list) else []):
            if isinstance(i, dict) and _text(i.get('q'), 300) and _text(i.get('a'), 1500):
                items.append({'q': re.sub(r'[*]', '', _text(i['q'], 300)), 'a': _text(i['a'], 1500)})
        return {'t': t, 'v': items} if items else None
    if t == 'links':
        items = []
        for i in (v if isinstance(v, list) else []):
            if isinstance(i, (list, tuple)) and len(i) == 2 and _text(i[0], 120) and _text(i[1], 300):
                href = _text(i[1], 300)
                if re.match(r'^(https?://|[a-z0-9][a-z0-9/_\-#.]*$)', href):
                    items.append([_text(i[0], 120), href])
        return {'t': t, 'v': items} if items else None
    return None


def _normalise(raw, name, site_published):
    if not SLUG_RE.match(name):
        raise ValueError('file name must be lower-case words joined by hyphens')
    title = _text(raw.get('title'), 120)
    description = _text(raw.get('description'), 320)
    if not title or not description:
        raise ValueError('title and description are required')
    blocks = [c for c in (_clean_block(b) for b in raw.get('blocks', [])) if c]
    if not blocks:
        raise ValueError('article has no content')
    words = sum(len(json.dumps(b.get('v', [b.get('head'), b.get('rows')])).split()) for b in blocks)
    published = raw.get('published') if DATE_RE.match(str(raw.get('published', ''))) else site_published
    post = {
        'slug': 'blog/' + name,
        'title': title,
        'description': description,
        'h1': _text(raw.get('h1'), 200) or title,
        'category': _text(raw.get('category'), 40) or 'Guide',
        'minutes': int(raw.get('minutes') or max(1, round(words / 200))),
        'published': published,
        'summary': _text(raw.get('summary'), 400) or description,
        'blocks': blocks,
        'related': [r for r in raw.get('related', []) if isinstance(r, str) and not r.startswith('from:')][:6] or ['free-trial'],
        # pages of the site that should show a link to this article (chosen in the CRM)
        'link_from': [p for p in (raw.get('link_from') if isinstance(raw.get('link_from'), list) else []) if isinstance(p, str) and re.match(r'^[a-z0-9][a-z0-9\-]*$', p)][:12],
    }
    if TIME_RE.match(str(raw.get('time', ''))):
        post['time'] = raw['time']
    cover = _text(raw.get('cover'), 200)
    if cover and re.match(r'^asset/blog/[a-z0-9\-_.]+\.(webp|png|jpg|jpeg)$', cover) and (ROOT / cover).exists():
        post['cover'] = cover
        post['cover_alt'] = _text(raw.get('cover_alt'), 200) or title
    return post


def load_resources():
    """resource-pages.json with CRM posts merged into res['posts'], newest first."""
    res = json.loads((ROOT / 'scripts/resource-pages.json').read_text())
    taken = {x['slug'] for x in res['posts']}
    extra = []
    for f in sorted((ROOT / 'content/blog').glob('*.json')):
        try:
            post = _normalise(json.loads(f.read_text()), f.stem, res['published'])
        except Exception as e:  # skip a bad file, keep building the rest of the site
            print(f'WARNING: skipped content/blog/{f.name}: {e}', file=sys.stderr)
            continue
        if post['slug'] in taken:
            print(f'WARNING: skipped content/blog/{f.name}: slug already used by a built-in post', file=sys.stderr)
            continue
        taken.add(post['slug'])
        extra.append(post)
    posts = res['posts'] + extra
    posts.sort(key=lambda x: (x.get('published', res['published']), x.get('time', '00:00')), reverse=True)
    res['posts'] = posts
    return res
