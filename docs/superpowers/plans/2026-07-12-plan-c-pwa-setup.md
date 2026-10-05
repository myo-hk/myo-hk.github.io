# Plan C: PWA Setup

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Progressive Web App support to My O! — manifest.json, service worker, offline page, theme-color, and app icons — enabling install-to-homescreen and offline access.

**Architecture:** Pure static HTML site on GitHub Pages. PWA assets are static files served from the root. Service worker registered from a small inline script in each page's body. Icons generated from the existing company logo.

**Tech Stack:** Vanilla JS (service worker), PNG icons, JSON (manifest)

---

### Task 1: Generate PWA Icons

**Files:**
- Create: `image/icon-192x192.png`
- Create: `image/icon-512x512.png`

- [ ] **Step 1: Check if ImageMagick or sips (macOS built-in) is available**

```bash
which convert || which sips || echo "no image tool found"
```
Expected: Either `convert` (ImageMagick) or `sips` (macOS built-in) path.

- [ ] **Step 2: Generate icons from the company logo**

```bash
# macOS built-in (sips)
cp image/01_company_logo.png image/icon-192x192.png
sips -z 192 192 image/icon-192x192.png --out image/icon-192x192.png
cp image/01_company_logo.png image/icon-512x512.png
sips -z 512 512 image/icon-512x512.png --out image/icon-512x512.png
```
Expected: Two icon files created at correct sizes.

Verify:
```bash
sips -g pixelWidth -g pixelHeight image/icon-192x192.png
sips -g pixelWidth -g pixelHeight image/icon-512x512.png
```
Expected: 192x192 and 512x512.

(Alternative if sips not available: Use `python3 -c "from PIL import Image; img = Image.open('image/01_company_logo.png'); img.resize((192,192)).save('image/icon-192x192.png'); img.resize((512,512)).save('image/icon-512x512.png')"`)

- [ ] **Step 3: Commit**

```bash
git add image/icon-192x192.png image/icon-512x512.png
git commit -m "feat(pwa): add PWA app icons at 192x192 and 512x512"
```

---

### Task 2: Create manifest.json

**Files:**
- Create: `manifest.json`

- [ ] **Step 1: Write manifest.json**

```json
{
  "name": "My O! 專屬結婚證書套",
  "short_name": "My O!",
  "description": "香港設計師級結婚證書套品牌 — 客製化亞麻布與磨砂珠光證書套，熱轉印工藝印製新人名字與結婚日期。",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#fdfaf6",
  "theme_color": "#CD853F",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/image/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/image/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "categories": ["lifestyle", "wedding"],
  "lang": "zh-Hant",
  "dir": "ltr"
}
```

- [ ] **Step 2: Validate manifest.json is valid JSON**

```bash
python3 -c "import json; json.loads(open('manifest.json').read()); print('Valid JSON')"
```
Expected: "Valid JSON"

- [ ] **Step 3: Commit**

```bash
git add manifest.json
git commit -m "feat(pwa): add manifest.json with standalone display and icons"
```

---

### Task 3: Create Service Worker

**Files:**
- Create: `sw.js`

- [ ] **Step 1: Write the service worker**

```javascript
// My O! Service Worker — stale-while-revalidate caching strategy
const CACHE_NAME = 'myo-cache-v1';
const STATIC_ASSETS = [
  '/',
  '/v2.html',
  '/poster.html',
  '/llms.txt',
  '/pricing.md',
  '/blog/index.html',
  '/image/01_company_logo.png',
  '/image/icon-192x192.png',
  '/image/icon-512x512.png',
  '/manifest.json'
];

// Install: pre-cache critical assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // Don't fail install if individual assets fail
      return Promise.allSettled(
        STATIC_ASSETS.map((url) =>
          cache.add(url).catch(() => console.warn(`Failed to cache: ${url}`))
        )
      );
    })
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// Fetch: stale-while-revalidate
self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  // Skip non-http(s) requests (chrome-extension, etc.)
  if (!event.request.url.startsWith('http')) return;

  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetchPromise = fetch(event.request)
        .then((response) => {
          // Cache successful responses
          if (response && response.status === 200 && response.type === 'basic') {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => cached); // Fall back to cache on network failure

      return cached || fetchPromise;
    })
  );
});
```

- [ ] **Step 2: Verify the file is valid JavaScript (no syntax errors)**

```bash
node -c sw.js
```
Expected: "Syntax Check OK" (or no output = success).

- [ ] **Step 3: Commit**

```bash
git add sw.js
git commit -m "feat(pwa): add service worker with stale-while-revalidate strategy"
```

---

### Task 4: Add PWA Meta Tags to index.html (Root Layout)

**Files:**
- Modify: `index.html`
- Note: This is the root layout. For individual blog pages, see Task 5 (batch script).

- [ ] **Step 1: Add theme-color, manifest, apple-mobile-web-app, and SW registration**

Before `</head>` in index.html, add:

```html
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#CD853F">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="My O!">
<link rel="apple-touch-icon" href="/image/icon-192x192.png">
```

Before `</body>` in index.html, add:

```html
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch((err) => {
      console.warn('SW registration failed:', err);
    });
  });
}
</script>
```

- [ ] **Step 2: Verify the HTML is well-formed**

```bash
grep -c 'manifest.json' index.html && grep -c 'theme-color' index.html && grep -c 'serviceWorker' index.html
```
Expected: All three show `1`.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat(pwa): add manifest link, theme-color, apple-mobile-web-app, and SW registration to index.html"
```

---

### Task 5: Batch-Add PWA Tags to All Pages

**Files:**
- Create: `scripts/add_pwa_tags.py`
- Modify: All root HTML pages + all 421 blog articles

- [ ] **Step 1: Create the batch script**

Create `scripts/add_pwa_tags.py`:

```python
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

# Files to skip (no HTML, or already handled)
SKIP_FILES = {"HTML-Artifacts.html"}

PWA_HEAD_TAGS = """<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#CD853F">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="My O!">
<link rel="apple-touch-icon" href="/image/icon-192x192.png">"""

# Blog articles need relative paths
PWA_HEAD_TAGS_BLOG = """<link rel="manifest" href="../manifest.json">
<meta name="theme-color" content="#CD853F">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="My O!">
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
    """Add PWA tags to HTML if not already present."""
    if 'manifest.json' in html:
        return html, False

    head_tags = PWA_HEAD_TAGS_BLOG if is_blog else PWA_HEAD_TAGS

    # Add head tags before </head>
    html = html.replace('</head>', f'{head_tags}\n</head>', 1)

    # Add SW script at end, before </body> if it exists, else at end
    if '</body>' in html:
        html = html.replace('</body>', f'{SW_SCRIPT}\n</body>', 1)
    else:
        html += SW_SCRIPT

    return html, True

def main():
    test_mode = "--test" in sys.argv
    changed = 0
    skipped = 0

    # Root HTML files
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

    # Blog articles
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
```

- [ ] **Step 2: Run the script in test mode**

```bash
python3 scripts/add_pwa_tags.py --test
```
Expected: Shows all root + blog files that would get PWA tags.

- [ ] **Step 3: Run the script for real**

```bash
python3 scripts/add_pwa_tags.py
```

- [ ] **Step 4: Verify by spot-checking a root page and a blog page**

```bash
grep -c 'manifest.json' index.html
grep -c 'manifest.json' blog/婚禮攝影價錢比較.html
grep -c 'serviceWorker' blog/婚紗禮服選購指南.html
```
Expected: All show `1`.

- [ ] **Step 5: Commit**

```bash
git add scripts/add_pwa_tags.py index.html v2.html poster.html heic-converter.html privacy.html terms.html blog/
git commit -m "feat(pwa): batch-add PWA meta tags and SW registration to all pages"
```
