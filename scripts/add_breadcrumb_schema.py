#!/usr/bin/env python3
"""
Add BreadcrumbList JSON-LD schema to blog articles.
Inserts the schema before </head> only if one doesn't already exist.
Usage: python3 scripts/add_breadcrumb_schema.py [--test]
"""

import re
import json
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

BREADCRUMB_SCHEMA = """    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首頁","item":"https://myo-makeyourown.pages.dev/"},{"@type":"ListItem","position":2,"name":"教學指南","item":"https://myo-makeyourown.pages.dev/blog/"},{"@type":"ListItem","position":3,"name":"%TITLE%","item":"https://myo-makeyourown.pages.dev/blog/%FILENAME%"}]}
    </script>"""

def extract_title(html):
    """Extract the page title from <title> tag."""
    import re
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    return m.group(1).strip() if m else "文章"

def has_breadcrumb(html):
    """Check if BreadcrumbList schema already exists."""
    return '"BreadcrumbList"' in html

def main():
    test_mode = "--test" in __import__("sys").argv
    files = sorted(BLOG_DIR.glob("*.html"))
    changed = 0
    skipped_exists = 0
    skipped_non_article = 0

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")

        # Skip blog index page
        if fpath.name == "index.html":
            skipped_non_article += 1
            continue

        if has_breadcrumb(content):
            skipped_exists += 1
            continue

        title = extract_title(content)
        filename = fpath.name

        schema = BREADCRUMB_SCHEMA.replace("%TITLE%", title.replace('"', '\\"')).replace("%FILENAME%", filename)
        content = content.replace("</head>", schema + "\n</head>")

        if not test_mode:
            fpath.write_text(content, encoding="utf-8")

        changed += 1

    print(f"Files processed: {len(files)}")
    print(f"Breadcrumb added: {changed}")
    print(f"Skipped (already exists): {skipped_exists}")
    print(f"Skipped (index.html): {skipped_non_article}")
    print(f"Test mode: {test_mode}")

if __name__ == "__main__":
    main()