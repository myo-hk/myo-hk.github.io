#!/usr/bin/env python3
"""
Batch add PWA meta tags and service worker registration to all HTML pages.
Usage: python3 scripts/add_pwa_tags.py [--test]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
BLOG_DIR = ROOT / "blog"

SKIP_FILES = {"HTML-Artifacts.html"}

PWA_HEAD_TAGS = """<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#CD853F">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="MyO!">
<link rel="apple-touch-icon" href="/image/icon-192x192.png">"""

PWA_HEAD_TAGS_BLOG = """<link rel="manifest" href="../manifest.json">
<meta name="theme-color" content="#CD853F">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="MyO!">
<link rel="apple-touch-icon" href="../image/icon-192x192.png">"""

SW_SCRIPT = """
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/sw.js').catch(function(err) {
      console.warn('SW registration failed:', err);
    });
  });
}
</script>"""

def add_pwa_tags(html, is_blog=False):
    if 'manifest.json' in html:
        return html, False
    head_tags = PWA_HEAD_TAGS_BLOG if is_blog else PWA_HEAD_TAGS
    html = html.replace('</head>', f'{head_tags}\n</head>', 1)
    if '</body>' in html:
        html = html.replace('</body>', f'{SW_SCRIPT}\n</body>', 1)
    else:
        html += SW_SCRIPT
    return html, True

def main():
    test_mode = "--test" in sys.argv
    changed = 0
    skipped = 0
    for fpath in sorted(ROOT.glob("*.html")):
        if fpath.name in SKIP_FILES:
            continue
        content = fpath.read_text(encoding="utf-8")
        new_content, was_changed = add_pwa_tags(content, is_blog=False)
        if was_changed:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ {fpath.name}")
            changed += 1
        else:
            skipped += 1
    for fpath in sorted(BLOG_DIR.glob("*.html")):
        content = fpath.read_text(encoding="utf-8")
        new_content, was_changed = add_pwa_tags(content, is_blog=True)
        if was_changed:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ blog/{fpath.name}")
            changed += 1
        else:
            skipped += 1
    print(f"\nDone: {changed} updated, {skipped} skipped (already have PWA tags)")

if __name__ == "__main__":
    main()