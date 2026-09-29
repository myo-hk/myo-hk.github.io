#!/usr/bin/env python3
"""
Generate a single sitemap.xml with ALL pages (root + blog articles).
Usage: python3 scripts/generate_sitemap.py
"""

from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape
import re

ROOT = Path(__file__).parent.parent
BLOG = ROOT / "blog"
NOW = datetime.now().strftime("%Y-%m-%d")
BASE = "https://myo-makeyourown.pages.dev"

HREFLANG_PAIRS = {
    "poster.html": [
        ("zh-HK", f"{BASE}/poster.html"),
        ("en", f"{BASE}/poster-en.html"),
        ("x-default", f"{BASE}/poster.html"),
    ],
    "poster-en.html": [
        ("zh-HK", f"{BASE}/poster.html"),
        ("en", f"{BASE}/poster-en.html"),
        ("x-default", f"{BASE}/poster.html"),
    ],
}

ROOT_PAGES = {
    "index.html":       {"priority": "1.0", "changefreq": "weekly"},
    "v2.html":          {"priority": "0.3", "changefreq": "monthly"},
    "poster.html":      {"priority": "0.5", "changefreq": "monthly"},
    "poster-en.html":   {"priority": "0.5", "changefreq": "monthly"},
    "heic-converter.html": {"priority": "0.5", "changefreq": "monthly"},
    "privacy.html":     {"priority": "0.3", "changefreq": "yearly"},
    "terms.html":       {"priority": "0.3", "changefreq": "yearly"},
}


def add_url(urlset, loc, lastmod, changefreq, priority, alternates=None):
    """Append a <url> entry. `alternates` is a list of (hreflang, url) pairs."""
    lines = []
    for hreflang, alt_url in alternates or []:
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="{hreflang}" href="{escape(alt_url)}"/>'
        )
    alternates_block = ("\n" + "\n".join(lines) + "\n  ") if lines else ""
    urlset.append(f"""  <url>{alternates_block}
    <loc>{escape(loc)}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")


def generate_sitemap():
    """Generate a single sitemap.xml with ALL URLs (root pages + blog articles)."""
    urls = []

    # Root pages
    for filename, meta in ROOT_PAGES.items():
        loc = f"https://myo-makeyourown.pages.dev/{filename}" if filename != "index.html" else "https://myo-makeyourown.pages.dev/"
        add_url(urls, loc, NOW, meta["changefreq"], meta["priority"], HREFLANG_PAIRS.get(filename))

    # Blog index
    add_url(urls, "https://myo-makeyourown.pages.dev/blog/", NOW, "weekly", "0.8")

    # All blog articles
    html_files = sorted(BLOG.glob("*.html"))
    for fpath in html_files:
        if fpath.name == "index.html":
            continue

        content = fpath.read_text(encoding="utf-8", errors="ignore")
        date_match = re.search(
            r'<meta\s+property="article:published_time"\s+content="(\d{4}-\d{2}-\d{2})',
            content,
        )
        lastmod = date_match.group(1) if date_match else NOW

        loc = f"https://myo-makeyourown.pages.dev/blog/{escape(fpath.name)}"
        add_url(urls, loc, lastmod, "monthly", "0.7")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(urls)}
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"sitemap.xml: {len(urls)} URLs total")


if __name__ == "__main__":
    generate_sitemap()
    print("Done.")
