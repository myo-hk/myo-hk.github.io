#!/usr/bin/env python3
"""
Batch add GA4 social click tracking + scroll depth to root HTML pages.
Usage: python3 scripts/add_social_tracking.py [--test]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKIP_FILES = {"HTML-Artifacts.html"}

SCROLL_SCRIPT = """
<script>
(function() {
  if (typeof gtag === 'undefined') return;
  var scrollDepths = {25: true, 50: true, 75: true, 90: true};
  var firedDepths = {};
  var scrollHandler = function() {
    var scrollTop = window.scrollY || window.pageYOffset;
    var docHeight = Math.max(
      document.body.scrollHeight, document.documentElement.scrollHeight,
      document.body.offsetHeight, document.documentElement.offsetHeight,
      document.body.clientHeight, document.documentElement.clientHeight
    );
    var windowHeight = window.innerHeight;
    var scrollPercent = Math.round((scrollTop + windowHeight) / docHeight * 100);
    Object.keys(scrollDepths).forEach(function(depth) {
      if (scrollPercent >= parseInt(depth) && !firedDepths[depth]) {
        firedDepths[depth] = true;
        gtag('event', 'scroll_depth', {
          'event_category': 'engagement',
          'event_label': depth + '%',
          'value': parseInt(depth),
          'non_interaction': true
        });
      }
    });
  };
  window.addEventListener('scroll', scrollHandler, {passive: true});
})();
</script>"""

def add_scroll_tracking(html):
    if 'scroll_depth' in html:
        return html, False
    html = html.replace('</body>', f'{SCROLL_SCRIPT}\n</body>', 1)
    return html, True

def add_social_tracking(html, filename=""):
    """Add GA4 onclick to links that don't already have it."""
    def label_for_tag(tag, default):
        lower = tag.lower()
        if 'sticky' in lower:
            return 'sticky_bar'
        return default

    # WhatsApp links (api.whatsapp.com)
    def replace_wa(match):
        tag = match.group(0)
        if 'onclick=' in tag or 'click_whatsapp' in tag:
            return tag
        label = label_for_tag(tag, 'content')
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
        label = label_for_tag(tag, 'content')
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

    for fpath in sorted(ROOT.glob("*.html")):
        if fpath.name in SKIP_FILES:
            continue
        content = fpath.read_text(encoding="utf-8")
        orig = content

        content = add_social_tracking(content, fpath.name)
        content, _ = add_scroll_tracking(content)

        if content != orig:
            if not test_mode:
                fpath.write_text(content, encoding="utf-8")
            print(f"  ✓ {fpath.name}")
            changed += 1
        else:
            print(f"  - {fpath.name} (no changes)")

    print(f"\nDone: {changed} files updated")

if __name__ == "__main__":
    main()
