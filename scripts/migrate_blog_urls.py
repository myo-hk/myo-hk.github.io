#!/usr/bin/env python3
"""
Batch replace myo-hk.github.io → myo-makeyourown.pages.dev in blog HTML files.
Usage: python3 scripts/migrate_blog_urls.py
"""

import glob
import os

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "blog")
OLD = "https://myo-hk.github.io"
NEW = "https://myo-makeyourown.pages.dev"

html_files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.html")))
changed = 0
nochange = 0

for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if OLD not in content:
        nochange += 1
        continue

    new_content = content.replace(OLD, NEW)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

    changed += 1
    print(f"  UPDATED: {os.path.basename(fpath)}")

print(f"\nDone: {changed} files updated, {nochange} files unchanged (already correct)")