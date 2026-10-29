#!/bin/bash
# Build the site for a root domain (https://taxpower.co/ or *.pages.dev) into ./dist.
# Used by Cloudflare Pages. Run from anywhere:  bash scripts/cf-build.sh
set -e
cd "$(dirname "$0")/.."
pip install -q lxml pillow 2>/dev/null || pip3 install -q lxml pillow
export TAXPOWER_BASE_PATH=/
( cd scripts && python3 build-pages.py && python3 build-landing-pages.py )
rm -rf dist && mkdir dist
for item in *; do
  case "$item" in dist|scripts|tests|docs|_site-source|node_modules|README.md|_config.yml|wrangler.jsonc|nav.html|footer.html) continue;; esac
  cp -r "$item" dist/
done
echo "Built dist/: $(find dist -name '*.html' | wc -l) html files"
