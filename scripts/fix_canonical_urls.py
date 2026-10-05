#!/usr/bin/env python3
"""
Batch fix: Replace relative canonical URLs with absolute URLs in blog articles.
Usage: python3 scripts/fix_canonical_urls.py [--test]

Changes: <link rel="canonical" href="文件名.html">
      → <link rel="canonical" href="https://myo-makeyourown.pages.dev/blog/文件名.html">
"""

import re
import json
import glob
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"
REPORT_FILE = Path(__file__).parent.parent / "fix_canonical_report.json"

CANONICAL_PATTERN = re.compile(
    r'(<link\s+rel="canonical"\s+href=")([^"]+\.html)">'
)

def fix_canonical(html, filename):
    """Replace relative canonical URL with absolute URL."""
    changes = []

    def replace_relative(match):
        prefix = match.group(1)
        url = match.group(2)

        # Skip if already absolute
        if url.startswith("http"):
            return match.group(0)

        # Skip if already has full path
        if url.startswith("/blog/") or url.startswith("https://"):
            return match.group(0)

absolute = f'{prefix}https://myo-makeyourown.pages.dev/blog/{url}">'
changes.append({"from": url, "to": f"https://myo-makeyourown.pages.dev/blog/{url}"})
        return absolute

    html = CANONICAL_PATTERN.sub(replace_relative, html)
    return html, changes

def main():
    test_mode = "--test" in __import__("sys").argv
    files = sorted(BLOG_DIR.glob("*.html"))
    total_changes = 0
    all_changes = []

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")

        if 'rel="canonical"' not in content:
            continue

        before = content
        content, changes = fix_canonical(content, fpath.name)

        if changes:
            total_changes += len(changes)
            all_changes.append({"file": str(fpath.name), "changes": changes})

            if not test_mode:
                fpath.write_text(content, encoding="utf-8")
                print(f"  ✓ {fpath.name}: {len(changes)} canonical(s) fixed")

    report = {
        "files_processed": len(files),
        "files_changed": len(all_changes),
        "total_changes": total_changes,
        "test_mode": test_mode,
        "details": all_changes
    }

    REPORT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nReport saved to {REPORT_FILE}")
    print(f"Files processed: {len(files)}")
    print(f"Files changed: {len(all_changes)}")
    print(f"Total canonical URLs fixed: {total_changes}")

if __name__ == "__main__":
    main()