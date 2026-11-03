"""Delete built blog pages that no longer have a source article (for example an unpublished CRM post)."""
import pathlib
import shutil
import sys

import cms_posts

root = cms_posts.ROOT
keep = {x['slug'].split('/', 1)[1] for x in cms_posts.load_resources()['posts']}
removed = []
for f in sorted((root / 'blog').glob('*.html')):
    name = f.stem
    if name == 'index' or name in keep:
        continue
    f.unlink()
    shutil.rmtree(root / 'blog' / name, ignore_errors=True)
    removed.append(name)
print('Removed unpublished blog pages:', ', '.join(removed) if removed else 'none')
