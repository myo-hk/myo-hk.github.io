#!/usr/bin/env python3
"""
Batch add GA4 click tracking to WhatsApp/Instagram links in blog articles.
Usage: python3 scripts/add_blog_social_tracking.py [--test]
"""
import re
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"


def add_social_onclick(html):
    """Add GA4 onclick events to social links."""
    # WhatsApp links (api.whatsapp.com)
    def replace_wa(match):
        tag = match.group(0)
        if 'onclick=' in tag or 'click_whatsapp' in tag:
            return tag
        label = 'sticky_bar' if 'sticky' in tag.lower() else 'blog_content'
        onclick = f" onclick=\"gtag('event', 'click_whatsapp', {{'event_category': 'engagement', 'event_label': '{label}', 'value': 1}})\""
        return tag[:-1] + onclick + ">" if tag.endswith('>') else tag + onclick

    html = re.sub(
        r'<a[^>]*href="https://api\.whatsapp\.com/send\?phone=85263796410[^"]*"[^>]*>',
        replace_wa,
        html
    )

    # Instagram links
    def replace_ig(match):
        tag = match.group(0)
        if 'onclick=' in tag or 'click_instagram' in tag:
            return tag
        label = 'sticky_bar' if 'sticky' in tag.lower() else 'blog_content'
        onclick = f" onclick=\"gtag('event', 'click_instagram', {{'event_category': 'engagement', 'event_label': '{label}', 'value': 1}})\""
        return tag[:-1] + onclick + ">" if tag.endswith('>') else tag + onclick

    html = re.sub(
        r'<a[^>]*href="https://www\.instagram\.com/myo\.makeyourown/"[^>]*>',
        replace_ig,
        html
    )

    return html


def main():
    test_mode = "--test" in sys.argv
    changed = 0
    skipped = 0

    for fpath in sorted(BLOG_DIR.glob("*.html")):
        content = fpath.read_text(encoding="utf-8")

        if 'click_whatsapp' in content:
            skipped += 1
            continue

        new_content = add_social_onclick(content)
        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ {fpath.name}")
            changed += 1
        else:
            skipped += 1

    print(f"\nDone: {changed} updated, {skipped} skipped")


if __name__ == "__main__":
    main()
