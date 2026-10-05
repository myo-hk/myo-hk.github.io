# Plan E: GA4 Custom Event Tracking

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add GA4 custom event tracking for WhatsApp/Instagram button clicks, scroll depth, and conversion actions across the My O! site, enabling measurement of user engagement beyond page views.

**Architecture:** GA4's `gtag()` function is already loaded globally via the Google tag in every page's `<head>`. Custom events are dispatched from inline event handlers on social buttons and via a scroll observer. No new dependencies.

**Tech Stack:** Vanilla JS, Google Analytics 4 (gtag.js)

---

### Task 1: Add WhatsApp Click Tracking to index.html

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Find the WhatsApp button/link in index.html**

```bash
grep -n 'whatsapp\|WhatsApp\|6379' index.html
```
Expected: Line numbers for WhatsApp links (likely multiple — nav, body, and sticky bar).

- [ ] **Step 2: Add onclick event to each WhatsApp link**

For each WhatsApp link found, add an `onclick` attribute. Typical pattern:

```html
<!-- Before -->
<a href="https://wa.me/85263796410" target="_blank" rel="noopener noreferrer">
  <i class="fab fa-whatsapp"></i> WhatsApp
</a>

<!-- After -->
<a href="https://wa.me/85263796410" target="_blank" rel="noopener noreferrer"
   onclick="gtag('event', 'click_whatsapp', {'event_category': 'engagement', 'event_label': 'header', 'value': 1})">
  <i class="fab fa-whatsapp"></i> WhatsApp
</a>
```

Different locations get different `event_label` values:
- Header navigation → `'header'`
- Sticky conversion bar → `'sticky_bar'`
- Footer → `'footer'`
- Body content → `'content'`

- [ ] **Step 3: Verify the events are firing syntactically**

```bash
grep -c 'click_whatsapp' index.html
```
Expected: Count of WhatsApp links (3-5 depending on page structure).

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat(analytics): add GA4 click_whatsapp event tracking"
```

---

### Task 2: Add Instagram Click Tracking to index.html

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Find Instagram links**

```bash
grep -n 'instagram\|myo.makeyourown' index.html
```

- [ ] **Step 2: Add onclick event to each Instagram link**

```html
<a href="https://www.instagram.com/myo.makeyourown/" target="_blank" rel="noopener noreferrer"
   onclick="gtag('event', 'click_instagram', {'event_category': 'engagement', 'event_label': 'footer', 'value': 1})">
  <i class="fab fa-instagram"></i> Instagram
</a>
```

Use consistent `event_label` values: `'header'`, `'sticky_bar'`, `'footer'`, `'content'`.

- [ ] **Step 3: Verify**

```bash
grep -c 'click_instagram' index.html
```

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat(analytics): add GA4 click_instagram event tracking"
```

---

### Task 3: Add Scroll Depth Tracking (Global)

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Add scroll depth tracking script before `</body>`**

```html
<script>
// GA4 Scroll Depth Tracking (fires at 25%, 50%, 75%, 90%)
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
</script>
```

- [ ] **Step 2: Verify the script is present**

```bash
grep -c 'scroll_depth' index.html
```
Expected: `1`.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat(analytics): add GA4 scroll depth tracking (25/50/75/90%)"
```

---

### Task 4: Add WhatsApp/Instagram + Scroll Tracking to All Other Root Pages

**Files:**
- Modify: `v2.html`, `poster.html`, `heic-converter.html`, `privacy.html`, `terms.html`
- Create: `scripts/add_social_tracking.py`

- [ ] **Step 1: Create the batch script**

Create `scripts/add_social_tracking.py`:

```python
#!/usr/bin/env python3
"""
Batch add GA4 social click tracking to root HTML pages.
Adds onclick handlers to WhatsApp and Instagram links.
Usage: python3 scripts/add_social_tracking.py [--test]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKIP_FILES = {"index.html", "HTML-Artifacts.html"}  # index.html handled manually

# Scroll depth script (same in Task 3)
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
    """Add scroll depth script before </body>."""
    if 'scroll_depth' in html:
        return html, False
    html = html.replace('</body>', f'{SCROLL_SCRIPT}\n</body>', 1)
    return html, True

def add_whatsapp_tracking(html):
    """Add onclick to WhatsApp links that don't already have it."""
    def replace_wa(match):
        tag = match.group(0)
        if 'onclick=' in tag or 'click_whatsapp' in tag:
            return tag
        # Extract label from surrounding context (approximate)
        label = 'body'
        if 'sticky' in tag.lower():
            label = 'sticky_bar'
        elif 'footer' in tag.lower():
            label = 'footer'
        onclick = f" onclick=\"gtag('event', 'click_whatsapp', {{'event_category': 'engagement', 'event_label': '{label}', 'value': 1}})\""
        return tag.replace('>', onclick + '>', 1) if tag.endswith('>') else tag + onclick

    return re.sub(
        r'<a[^>]*href="https://wa\.me/[^"]*"[^>]*>',
        replace_wa,
        html
    ), False

def add_instagram_tracking(html):
    """Add onclick to Instagram links that don't already have it."""
    def replace_ig(match):
        tag = match.group(0)
        if 'onclick=' in tag or 'click_instagram' in tag:
            return tag
        label = 'body'
        if 'sticky' in tag.lower():
            label = 'sticky_bar'
        elif 'footer' in tag.lower():
            label = 'footer'
        onclick = f" onclick=\"gtag('event', 'click_instagram', {{'event_category': 'engagement', 'event_label': '{label}', 'value': 1}})\""
        return tag.replace('>', onclick + '>', 1) if tag.endswith('>') else tag + onclick

    return re.sub(
        r'<a[^>]*href="https://www\.instagram\.com/[^"]*"[^>]*>',
        replace_ig,
        html
    ), False

def main():
    test_mode = "--test" in sys.argv
    changed = 0

    for fpath in sorted(ROOT.glob("*.html")):
        if fpath.name in SKIP_FILES:
            continue
        content = fpath.read_text(encoding="utf-8")
        orig = content

        content, _ = add_whatsapp_tracking(content)
        content, _ = add_instagram_tracking(content)
        content, changed_flag = add_scroll_tracking(content)

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
```

- [ ] **Step 2: Run the batch script**

```bash
python3 scripts/add_social_tracking.py
```

- [ ] **Step 3: Spot-check one file**

```bash
grep -c 'click_whatsapp' v2.html
grep -c 'scroll_depth' v2.html
```
Expected: Both show counts > 0.

- [ ] **Step 4: Commit**

```bash
git add scripts/add_social_tracking.py v2.html poster.html heic-converter.html privacy.html terms.html
git commit -m "feat(analytics): batch-add GA4 social click + scroll tracking to all root pages"
```

---

### Task 5: Add Social Click Tracking to Blog Articles (Batch)

**Files:**
- Create: `scripts/add_blog_social_tracking.py`
- Modify: All 421 blog articles

- [ ] **Step 1: Create the blog batch script**

Create `scripts/add_blog_social_tracking.py`:

```python
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
    changes = 0

    # WhatsApp links
    def replace_wa(match):
        tag = match.group(0)
        if 'onclick=' in tag or 'click_whatsapp' in tag:
            return tag
        label = 'sticky_bar' if 'sticky' in tag.lower() else 'blog_content'
        onclick = f" onclick=\"gtag('event', 'click_whatsapp', {{'event_category': 'engagement', 'event_label': '{label}', 'value': 1}})\""
        return tag.replace('>', onclick + '>', 1) if tag.endswith('>') else tag + onclick

    html = re.sub(
        r'<a[^>]*href="https://wa\.me/[^"]*"[^>]*>',
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
        return tag.replace('>', onclick + '>', 1) if tag.endswith('>') else tag + onclick

    html = re.sub(
        r'<a[^>]*href="https://www\.instagram\.com/[^"]*"[^>]*>',
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

        # Skip files that already have tracking
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

    print(f"\nDone: {changed} updated, {skipped} skipped (already tracked or no social links)")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script**

```bash
python3 scripts/add_blog_social_tracking.py
```

- [ ] **Step 3: Spot-check**

```bash
grep -c 'click_whatsapp' blog/婚禮攝影價錢比較.html
```
Expected: Count of WhatsApp links in that article (1-2).

- [ ] **Step 4: Commit**

```bash
git add scripts/add_blog_social_tracking.py blog/
git commit -m "feat(analytics): add GA4 social click tracking to all blog articles"
```
