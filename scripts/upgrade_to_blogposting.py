#!/usr/bin/env python3
"""
Upgrade Article JSON-LD to BlogPosting in blog articles.
BlogPosting is more specific than Article and preferred for blog content.
Usage: python3 scripts/upgrade_to_blogposting.py [--test]
"""
import re
import json
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

def upgrade_schema(obj):
    """Recursively upgrade 'Article' to 'BlogPosting' in a parsed JSON object."""
    changed = False
    if isinstance(obj, dict):
        if obj.get("@type") == "Article":
            obj["@type"] = "BlogPosting"
            changed = True
        for val in obj.values():
            if upgrade_schema(val):
                changed = True
    elif isinstance(obj, list):
        for item in obj:
            if upgrade_schema(item):
                changed = True
    return changed

def main():
    test_mode = "--test" in sys.argv
    files = sorted(BLOG_DIR.glob("*.html"))
    changed = 0

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")

        def fix_block(m):
            raw = m.group(1).strip()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return m.group(0)
            if not upgrade_schema(data):
                return m.group(0)
            new_json = json.dumps(data, ensure_ascii=False, indent=2)
            return f'<script type="application/ld+json">\n{new_json}\n</script>'

        new_content = re.sub(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            fix_block,
            content,
            flags=re.DOTALL
        )

        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ {fpath.name}")
            changed += 1

    print(f"\nDone: {changed} files upgraded from Article → BlogPosting")

if __name__ == "__main__":
    main()
