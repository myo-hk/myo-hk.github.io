#!/usr/bin/env python3
"""
replace-tailwind-cdn.py — Replace Tailwind CDN <script> tag with local CSS <link> across all HTML files.

Usage:
    python3 scripts/replace-tailwind-cdn.py          # dry-run: show files that would change
    python3 scripts/replace-tailwind-cdn.py --write   # actually write changes
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Pattern 1: Simple CDN script tag (<script src="https://cdn.tailwindcss.com"></script>)
SIMPLE_CDN = re.compile(
    r'\s*<script[^>]*src="https://cdn\.tailwindcss\.com[^>]*></script>\s*'
)

# Pattern 2: Dynamic CDN loading (dns-prefetch + preload + async script block)
# Used by index.html and v2.html
DYNAMIC_CDN = re.compile(
    r'\s*<link[^>]*dns-prefetch[^>]*cdn\.tailwindcss\.com[^>]*>\s*\n'
    r'\s*<link[^>]*preload[^>]*cdn\.tailwindcss\.com[^>]*>\s*\n'
    r'\s*<script>\s*\n'
    r'[^<]*\(function\(\).*?cdn\.tailwindcss\.com.*?\n'
    r'\s*</script>\s*',
    re.DOTALL
)

# Pattern 3: Any remaining standalone dns-prefetch or preconnect links for tailwind CDN
REMAINING_CDN_LINKS = re.compile(
    r'\s*<link[^>]*cdn\.tailwindcss\.com[^>]*>\s*'
)

REPLACEMENT = '\n    <link rel="stylesheet" href="/css/tailwind.min.css">\n'

def find_html_files():
    """Yield all .html files in the repo."""
    for pattern in ['*.html', 'blog/**/*.html']:
        for f in Path(ROOT).glob(pattern):
            if 'node_modules' in str(f) or 'presentations' in str(f):
                continue
            yield f

def process_file(filepath: Path, dry_run: bool = True) -> bool:
    """Replace CDN tag with local link. Returns True if changed."""
    original = filepath.read_text(encoding='utf-8')
    replaced = SIMPLE_CDN.sub(REPLACEMENT, original)
    replaced = DYNAMIC_CDN.sub(REPLACEMENT, replaced)
    replaced = REMAINING_CDN_LINKS.sub('', replaced)
    if replaced == original:
        return False
    if not dry_run:
        filepath.write_text(replaced, encoding='utf-8')
    return True

def main():
    dry_run = '--write' not in sys.argv
    total = changed = 0
    for f in find_html_files():
        total += 1
        if process_file(f, dry_run):
            changed += 1
            print(f"{'[DRY-RUN]' if dry_run else '[CHANGED]'} {f.relative_to(ROOT)}")
    print(f"\n{'DRY-RUN: ' if dry_run else ''}{changed} of {total} HTML files would change.")

if __name__ == '__main__':
    main()