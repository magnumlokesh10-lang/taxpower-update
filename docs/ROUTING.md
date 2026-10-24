# How the pages are built

Every tab is its own real page (home, taxpowergst, taxpowertds, pricing, downloads, aboutus, support). Clicking a tab opens that page; nothing scrolls between tabs.

- Edit page content in `_site-source/*.html`, shared header in `nav.html`, footer in `footer.html`, titles and descriptions in `scripts/seo-routes.json`.
- Build: `python scripts/build-pages.py` then `python scripts/build-landing-pages.py` (needs `lxml` and `Pillow`). For a preview on GitHub Pages use `TAXPOWER_BASE_PATH=/<repo>/` before both commands. Commit the generated HTML.
- Each page loads only the CSS and JS it uses. The list comes from the `<head>` of its file in `_site-source/` (home has its own list in `scripts/build-pages.py`).
- `gst-return`, `gst-billing`, `technical-support` and `demo-enquiry` are extra entry URLs; they open the GST or Support page and jump to that part.
- Check: `node tests/pages.cjs`.
