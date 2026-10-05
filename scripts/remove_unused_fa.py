#!/usr/bin/env python3
"""
Remove FontAwesome CSS from HTML pages that don't use any fa-* classes.

Handles three FA loading patterns:
  1. <link rel="preload" href="...font-awesome..."> (root pages)
  2. <noscript><link rel="stylesheet" href="...font-awesome..."></noscript> (root pages)
  3. <link rel="stylesheet" href="...font-awesome..."> (blog articles)

Usage: python3 scripts/remove_unused_fa.py [--test]
       --test : dry-run, print what would change without modifying files
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
BLOG_DIR = ROOT / "blog"

# Pattern 1: preload link (root pages like index.html, v2.html)
FA_PRELOAD = re.compile(
    r'\s*<link\s+rel="preload"\s+href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+\.css"[^>]*>\s*\n?'
)

# Pattern 2: noscript wrapper (root pages)
FA_NOSCRIPT = re.compile(
    r'\s*<noscript><link\s+rel="stylesheet"\s+href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+\.css"[^>]*></noscript>\s*\n?'
)

# Pattern 3: direct stylesheet link (blog articles)
FA_STYLESHEET = re.compile(
    r'\s*<link\s+rel="stylesheet"\s+href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+\.css"[^>]*>\s*\n?'
)


def uses_fontawesome(html: str) -> bool:
    """Check if <body> contains any fa- class usage."""
    body_match = re.search(r'<body', html)
    if not body_match:
        return False
    body = html[body_match.start():]
    return bool(re.search(r'class="[^"]*fa-[^"]*"', body))


def remove_fa_loaders(html: str) -> str:
    """Strip all FontAwesome CSS loader elements."""
    html = FA_PRELOAD.sub('', html)
    html = FA_NOSCRIPT.sub('', html)
    html = FA_STYLESHEET.sub('', html)
    return html


def process_file(fpath: Path, test_mode: bool) -> bool:
    """Returns True if file was (or would be) changed."""
    html = fpath.read_text(encoding='utf-8')
    if uses_fontawesome(html):
        print(f"  ⏭️  {fpath.relative_to(ROOT)} — keeps FA (icons in use)")
        return False
    new_html = remove_fa_loaders(html)
    if new_html == html:
        print(f"  ⏭️  {fpath.relative_to(ROOT)} — no FA loaders found")
        return False
    if not test_mode:
        fpath.write_text(new_html, encoding='utf-8')
    print(f"  ✅ {fpath.relative_to(ROOT)} — removed FA loaders")
    return True


def main():
    test_mode = "--test" in sys.argv
    if test_mode:
        print("🔍 DRY RUN — no files will be modified\n")

    changed = 0

    # Root pages
    for name in ['index.html', 'v2.html', 'poster.html', 'poster-en.html',
                 'heic-converter.html', 'faq.html', 'privacy.html', 'terms.html',
                 'HTML-Artifacts.html']:
        fpath = ROOT / name
        if fpath.exists():
            if process_file(fpath, test_mode):
                changed += 1

    # Blog articles
    for fpath in sorted(BLOG_DIR.glob("*.html")):
        if process_file(fpath, test_mode):
            changed += 1

    print(f"\n{'🔍 Would change' if test_mode else '✅ Changed'} {changed} file(s)")
    return changed


if __name__ == "__main__":
    main()