#!/usr/bin/env python3
"""
Batch-optimize <head> sections of all blog HTML files for PageSpeed.

Changes per file:
1. Insert preconnect hints if missing
2. Convert Font Awesome from render-blocking stylesheet to preload+onload
3. Convert Tailwind CSS from render-blocking stylesheet to preload+onload
4. Convert Google Fonts from render-blocking stylesheet to preload+onload
5. Add width/height/loading-lazy to header and footer logo <img> tags

Usage:
    python3 scripts/optimize_blog_head.py              # apply changes
    python3 scripts/optimize_blog_head.py --dry-run    # preview only
    python3 scripts/optimize_blog_head.py --verbose    # detailed per-file logging
"""

import re
import os
import sys
import glob

BLOG_DIR = "blog"

PRECONNECT_BLOCK = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://cdnjs.cloudflare.com">
    <link rel="preconnect" href="https://unpkg.com">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">"""

# Match only standalone (non-noscript) tailwind stylesheet links
TAILWIND_PATTERN = re.compile(
    r'(?<!<noscript>)<link\s+rel="stylesheet"\s+href="/css/tailwind\.min\.css"\s*>'
)
TAILWIND_REPLACEMENT = (
    '<link rel="preload" href="/css/tailwind.min.css" as="style" '
    'onload="this.rel=\'stylesheet\'">\n'
    '    <noscript><link rel="stylesheet" href="/css/tailwind.min.css"></noscript>'
)

# Match only standalone (non-noscript) Google Fonts stylesheet links
GOOGLE_FONTS_PATTERN = re.compile(
    r'(?<!<noscript>)<link\s+href="https://fonts\.googleapis\.com/css2\?[^"]+"\s+rel="stylesheet"\s*>'
)
GOOGLE_FONTS_REPLACEMENT = (
    '<link rel="preload" '
    'href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" '
    'as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
    '    <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" '
    'rel="stylesheet"></noscript>'
)

# FA with integrity hash
FA_WITH_INTEGRITY = re.compile(
    r'<link\s+rel="stylesheet"\s+'
    r'href="(https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+/css/all\.min\.css)"\s+'
    r'integrity="([^"]+)"\s+'
    r'crossorigin="([^"]+)"\s+'
    r'referrerpolicy="([^"]+)"\s*/>'
)

# FA without integrity
FA_NO_INTEGRITY = re.compile(
    r'<link\s+rel="stylesheet"\s+'
    r'href="(https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+/css/all\.min\.css)"\s+'
    r'crossorigin="([^"]+)"\s+'
    r'referrerpolicy="([^"]+)"\s*/>'
)

FOOTER_LOGO = re.compile(
    r'<img\s+src="\.\./image/01_company_logo\.png"\s+'
    r'alt="MyO! Logo"\s+'
    r'class="logo"\s*>'
)
FOOTER_LOGO_REPLACEMENT = (
    '<img src="../image/01_company_logo.png" alt="MyO! Logo" '
    'width="24" height="24" loading="lazy" class="logo">'
)

HEADER_LOGO = re.compile(
    r'(<img\s+loading="lazy"\s+src="\.\./image/01_company_logo\.png"\s+'
    r'class="[^"]*"\s+alt="[^"]*"\s*>)'
)


def make_fa_preload(href, integrity=None, crossorigin="anonymous", referrerpolicy="no-referrer"):
    int_attr = f' integrity="{integrity}"' if integrity else ''
    preload = (
        f'    <link rel="preload" href="{href}" as="style"'
        f'{int_attr} crossorigin="{crossorigin}"'
        f' referrerpolicy="{referrerpolicy}"'
        f' onload="this.onload=null;this.rel=\'stylesheet\'">\n'
        f'    <noscript><link rel="stylesheet" href="{href}"'
        f'{int_attr} crossorigin="{crossorigin}"'
        f' referrerpolicy="{referrerpolicy}"></noscript>'
    )
    return preload


def add_header_logo_dimensions(match):
    tag = match.group(1)
    if 'width=' not in tag and 'height=' not in tag:
        return tag.replace('src="', 'width="24" height="24" src="', 1)
    return tag


def fix_preconnect_presence(content):
    return 'rel="preconnect"' in content and 'fonts.gstatic.com' in content


def fix_blog_file(filepath, dry_run=False, verbose=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # 1. Font Awesome
    fa_match = FA_WITH_INTEGRITY.search(content)
    if fa_match:
        href, integrity, crossorigin, referrerpolicy = fa_match.groups()
        replacement = make_fa_preload(href, integrity=integrity,
                                      crossorigin=crossorigin,
                                      referrerpolicy=referrerpolicy)
        content = FA_WITH_INTEGRITY.sub(replacement, content, count=1)
        changes.append("FA preload (with integrity)")
    else:
        fa_match = FA_NO_INTEGRITY.search(content)
        if fa_match:
            href, crossorigin, referrerpolicy = fa_match.groups()
            replacement = make_fa_preload(href, crossorigin=crossorigin,
                                          referrerpolicy=referrerpolicy)
            content = FA_NO_INTEGRITY.sub(replacement, content, count=1)
            changes.append("FA preload (no integrity)")

    # 2. Tailwind
    if TAILWIND_PATTERN.search(content):
        content = TAILWIND_PATTERN.sub(TAILWIND_REPLACEMENT, content, count=1)
        changes.append("Tailwind preload")

    # 3. Google Fonts
    if GOOGLE_FONTS_PATTERN.search(content):
        content = GOOGLE_FONTS_PATTERN.sub(GOOGLE_FONTS_REPLACEMENT, content, count=1)
        changes.append("Google Fonts preload")

    # 4. Preconnect block
    if not fix_preconnect_presence(content):
        vp_match = re.search(r'(<meta\s+name="viewport"[^>]*>\s*)', content)
        if vp_match:
            insert_at = vp_match.end()
            content = content[:insert_at] + "\n" + PRECONNECT_BLOCK + "\n" + content[insert_at:]
            changes.append("preconnect hints")

    # 5. Footer logo
    if FOOTER_LOGO.search(content):
        content = FOOTER_LOGO.sub(FOOTER_LOGO_REPLACEMENT, content)
        changes.append("footer logo dimensions")

    # 6. Header logo
    if HEADER_LOGO.search(content):
        content = HEADER_LOGO.sub(add_header_logo_dimensions, content)
        changes.append("header logo dimensions")

    if content == original:
        return False

    if dry_run:
        rel = os.path.relpath(filepath)
        print(f"[DRY-RUN] {rel}: {', '.join(changes)}")
        return True

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    if verbose:
        rel = os.path.relpath(filepath)
        print(f"[OK] {rel}: {', '.join(changes)}")
    return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or dry_run

    files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.html")))
    print(f"Found {len(files)} blog HTML files{' (dry-run mode)' if dry_run else ''}\n")

    modified = 0
    for filepath in files:
        if fix_blog_file(filepath, dry_run=dry_run, verbose=verbose):
            modified += 1

    print(f"\n{'Would modify' if dry_run else 'Modified'} {modified} of {len(files)} files")
    return 0 if modified > 0 or dry_run else 0


if __name__ == "__main__":
    sys.exit(main())