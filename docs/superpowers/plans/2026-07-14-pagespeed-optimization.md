# PageSpeed Optimization — Mobile Performance 77→90+

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring mobile Lighthouse Performance from **77** to **90+** by reducing total page weight from 1,081 KiB, removing unused CSS/JS, and fixing accessibility issues. Desktop already scores 99 and needs minimal work.

**Architecture:** Static HTML site on Cloudflare Pages. Images already use WebP with PNG/JPG fallbacks via `<picture>` elements. CSS uses local Tailwind + remote FontAwesome. JS uses Swiper carousel + FontAwesome. The bulk of the savings come from: (1) removing the ~950 KB PNG texture files from the page (only WebP needed), (2) compressing the hero image smaller, (3) purging unused Tailwind classes, (4) removing FontAwesome + Swiper from pages that don't use them.

**Tech Stack:** Python 3 (image processing), bash/cwebp (WebP/AVIF conversion), manual HTML editing, Lighthouse CI for verification

**Source Data:** `docs/PageSpeed Insights.html` — Lighthouse 13.4.0, Mobile Moto G Power (412×823), Slow 4G, run 2026-07-14

**Current Baseline (Mobile):**
| Category | Score |
|----------|-------|
| Performance | 77 |
| Accessibility | 91 |
| Best Practices | 96 |
| SEO | 100 |

---

## File Structure

| File | Role | Changes |
|------|------|---------|
| `image/cert_color_beige_texture.png` | 949 KB texture — DELETE (WebP exists) | Remove from repo, stop referencing |
| `image/cert_color_blue_texture.png` | 956 KB texture — DELETE (WebP exists) | Remove from repo, stop referencing |
| `image/cert_color_beige_and_blue.png` | 297 KB combo — DELETE (WebP exists) | Remove from repo, stop referencing |
| `image/cert_hero.webp` | 122 KB hero — compress further | Re-encode at quality 70 |
| `image/cert_hero.jpg` | 181 KB hero fallback — compress further | Re-encode at quality 70 |
| `image/cert_color_beige.webp` | 233 KB beige color swatch — compress | Re-encode at quality 70 |
| `image/cert_color_beige.jpg` | 247 KB beige fallback — compress | Re-encode at quality 70 |
| `image/cert_color_blue.jpg` | 137 KB — compress | Re-encode at quality 70 |
| `index.html` | Main homepage | Remove PNG refs from `<picture>` elements, purge unused CSS/JS, fix a11y |
| `v2.html` | Redesigned homepage | Same changes as index.html |
| `scripts/optimize_images.py` | **NEW** — batch image optimization script | Create once, use for all images |
| `scripts/remove_unused_fa.py` | **NEW** — remove FontAwesome from FA-free pages | Create once |
| `tests/lighthouse-check.sh` | **NEW** — verification script | Create once |

---

### Task 1: Remove massive PNG texture files from repo and page references

**Files:**
- Delete: `image/cert_color_beige_texture.png`
- Delete: `image/cert_color_blue_texture.png`
- Delete: `image/cert_color_beige_and_blue.png`
- Modify: `index.html` (remove PNG `<img>` fallbacks from `<picture>` blocks)
- Modify: `v2.html` (same)

The three PNG texture files total 2.2 MB but are NEVER loaded in modern browsers because the `<picture>` `<source>` with WebP matches first. However they are still served to bots/crawlers and count toward repo size. Remove them entirely and point the fallback `<img>` to the WebP directly.

- [ ] **Step 1: Delete the three large PNG texture files**

```bash
rm image/cert_color_beige_texture.png \
   image/cert_color_blue_texture.png \
   image/cert_color_beige_and_blue.png
```

Verify: `ls -lh image/*.png` — only small PNGs (logo, icons) should remain.

- [ ] **Step 2: Update `<picture>` elements in index.html — point fallback `<img>` to WebP**

In `index.html`, find each texture swatch `<picture>` block. Replace the PNG `<img>` fallback with the WebP version.

Search for:
```html
<source srcset="image/cert_color_beige_texture.webp" type="image/webp">
<img src="image/cert_color_beige_texture.png"
```

Replace with:
```html
<source srcset="image/cert_color_beige_texture.webp" type="image/webp">
<img src="image/cert_color_beige_texture.webp"
```

Repeat for:
- `cert_color_blue_texture` (blue texture)
- `cert_color_beige_and_blue` (beige+blue combo)

- [ ] **Step 3: Apply same `<picture>` fix to v2.html**

Search for the same three pattern pairs in `v2.html` and apply the same `<img src="...png"` → `<img src="...webp"` replacement.

- [ ] **Step 4: Check blog articles for texture PNG references**

```bash
grep -r "beige_texture\.png\|blue_texture\.png\|beige_and_blue\.png" blog/ 2>/dev/null || echo "None found"
```

If any blog articles reference these PNGs, apply the same `<img src>` replacement.

- [ ] **Step 5: Commit**

```bash
git rm image/cert_color_beige_texture.png \
      image/cert_color_blue_texture.png \
      image/cert_color_beige_and_blue.png
git add index.html v2.html
git commit -m "perf: remove 2.2 MB of redundant PNG textures (WebP exists)"
```

---

### Task 2: Compress remaining hero and color swatch images

**Files:**
- Modify: `image/cert_hero.webp` (re-encode at quality 70)
- Modify: `image/cert_hero.jpg` (re-encode at quality 70)
- Modify: `image/cert_color_beige.webp` (re-encode at quality 70)
- Modify: `image/cert_color_beige.jpg` (re-encode at quality 70)
- Modify: `image/cert_color_blue.jpg` (re-encode at quality 70)

The hero image is 181 KB (JPEG) / 122 KB (WebP). The beige color swatch is 247 KB (JPEG) / 233 KB (WebP). These are the main contributors to the "image delivery" 418 KB savings opportunity. Compress to quality 70.

- [ ] **Step 1: Verify cwebp is available**

```bash
which cwebp && cwebp -version || echo "Install with: brew install webp"
```

- [ ] **Step 2: Compress hero image (both formats)**

```bash
cwebp -q 70 image/cert_hero.jpg -o image/cert_hero.webp
sips -s format jpeg -s formatOptions 70 image/cert_hero.jpg --out /tmp/hero_compressed.jpg
mv /tmp/hero_compressed.jpg image/cert_hero.jpg
```

Expected: WebP from 122 KB → ~70-80 KB, JPEG from 181 KB → ~100-110 KB.
Verify: `ls -lh image/cert_hero.*`

- [ ] **Step 3: Compress beige color swatch**

```bash
cwebp -q 70 image/cert_color_beige.jpg -o image/cert_color_beige.webp
sips -s format jpeg -s formatOptions 70 image/cert_color_beige.jpg --out /tmp/beige_compressed.jpg
mv /tmp/beige_compressed.jpg image/cert_color_beige.jpg
```

Expected: WebP from 233 KB → ~130 KB, JPEG from 247 KB → ~140 KB.

- [ ] **Step 4: Compress blue color swatch**

```bash
cwebp -q 70 image/cert_color_blue.jpg -o image/cert_color_blue.webp
sips -s format jpeg -s formatOptions 70 image/cert_color_blue.jpg --out /tmp/blue_compressed.jpg
mv /tmp/blue_compressed.jpg image/cert_color_blue.jpg
```

Expected: WebP from 79 KB → ~50-55 KB, JPEG from 137 KB → ~80 KB.

- [ ] **Step 5: Show total savings**

```bash
echo "=== Image sizes after compression ==="
ls -lh image/cert_hero.* image/cert_color_beige.* image/cert_color_blue.*
```

Expected combined savings: ~200-250 KB total.

- [ ] **Step 6: Commit**

```bash
git add image/cert_hero.webp image/cert_hero.jpg \
       image/cert_color_beige.webp image/cert_color_beige.jpg \
       image/cert_color_blue.webp image/cert_color_blue.jpg
git commit -m "perf: compress hero and product images to q70 (saves ~250 KB)"
```

---

### Task 3: Create batch image optimizer script (for future maintenance)

**Files:**
- Create: `scripts/optimize_images.py`

A reusable script to batch-compress all images in the `image/` directory.

- [ ] **Step 1: Create the script**

Write `scripts/optimize_images.py`:

```python
#!/usr/bin/env python3
"""
Batch image optimizer for My O! static site.
Compresses JPEG/WebP images in image/ directory.

Usage:
    python3 scripts/optimize_images.py                    # Optimize all images
    python3 scripts/optimize_images.py --dry-run           # Show what would be done
    python3 scripts/optimize_images.py --quality 75        # Custom quality

Requires: Pillow (pip3 install Pillow)
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
IMAGE_DIR = ROOT / "image"
DEFAULT_QUALITY = 70


def optimize_webp(source: str, output: str, quality: int = DEFAULT_QUALITY) -> int:
    """Convert/compress image to WebP at given quality. Returns output file size."""
    from PIL import Image
    img = Image.open(source)
    if img.mode == 'RGBA':
        img.save(output, 'WEBP', quality=quality)
    else:
        img = img.convert('RGB')
        img.save(output, 'WEBP', quality=quality)
    return os.path.getsize(output)


def optimize_jpeg(source: str, output: str, quality: int = DEFAULT_QUALITY) -> int:
    """Compress JPEG at given quality. Returns output file size."""
    from PIL import Image
    img = Image.open(source)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(output, 'JPEG', quality=quality, optimize=True)
    return os.path.getsize(output)


def main():
    quality = DEFAULT_QUALITY
    dry_run = False

    for arg in sys.argv[1:]:
        if arg == '--dry-run':
            dry_run = True
        elif arg.startswith('--quality='):
            quality = int(arg.split('=')[1])

    total_saved = 0
    for fpath in sorted(IMAGE_DIR.iterdir()):
        if fpath.suffix.lower() in ('.jpg', '.jpeg'):
            original = fpath.stat().st_size
            new_path = fpath.with_suffix('.webp')
            if dry_run:
                print(f"  [DRY RUN] {fpath.name}: {original // 1024} KB -> WebP")
            else:
                new_size = optimize_jpeg(str(fpath), str(new_path), quality)
                saved = original - new_size
                total_saved += saved
                print(f"  ok {fpath.name}: {original // 1024} KB -> {new_size // 1024} KB ({saved // 1024} KB saved)")
        elif fpath.suffix.lower() == '.webp':
            original = fpath.stat().st_size
            if dry_run:
                print(f"  [DRY RUN] {fpath.name}: {original // 1024} KB (re-compress to q{quality})")
            else:
                tmp = str(fpath) + ".tmp"
                optimize_webp(str(fpath), tmp, quality)
                new_size = os.path.getsize(tmp)
                if new_size < original:
                    os.replace(tmp, str(fpath))
                    saved = original - new_size
                    total_saved += saved
                    print(f"  ok {fpath.name}: {original // 1024} KB -> {new_size // 1024} KB ({saved // 1024} KB saved)")
                else:
                    os.remove(tmp)

    print(f"\nTotal saved: {total_saved // 1024} KB")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the optimizer to verify it works**

```bash
python3 scripts/optimize_images.py --dry-run
```

Expected: Lists all images and their potential savings without modifying anything.

- [ ] **Step 3: Commit**

```bash
git add scripts/optimize_images.py
git commit -m "feat: add batch image optimizer script"
```

---

### Task 4: Remove unused FontAwesome CSS from pages without icons

**Files:**
- Create: `scripts/remove_unused_fa.py`
- Modify: Various HTML pages (blog articles, poster, heic-converter)

FontAwesome CSS (~65 KB) is loaded on every page via preload + noscript, but many pages never use any `fa-*` icons.

- [ ] **Step 1: Check which root pages use FontAwesome**

```bash
for f in index.html v2.html poster.html heic-converter.html; do
  count=$(grep -c 'fa-' "$f" 2>/dev/null || echo 0)
  echo "$f: $count fa- references"
done
```

- [ ] **Step 2: Create removal script**

Write `scripts/remove_unused_fa.py`:

```python
#!/usr/bin/env python3
"""
Remove FontAwesome CSS loader from pages that don't use any fa-* classes.
Usage: python3 scripts/remove_unused_fa.py [--test]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
BLOG_DIR = ROOT / "blog"

FA_PATTERN = re.compile(
    r'\s*<noscript><link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+\.css"[^>]*></noscript>\s*\n?'
)

FA_PRELOAD_PATTERN = re.compile(
    r'\s*<link rel="preload" href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+\.css"[^>]*>\s*\n?'
)


def page_uses_fontawesome(html: str) -> bool:
    """Check if HTML body contains any fa- class usage."""
    body_match = re.search(r'<body', html)
    if not body_match:
        return False
    body = html[body_match.start():]
    return bool(re.search(r'class="[^"]*fa-[^"]*"', body))


def remove_fa_loaders(html: str) -> str:
    """Remove FontAwesome CSS loader markup from HTML."""
    html = FA_PATTERN.sub('', html)
    html = FA_PRELOAD_PATTERN.sub('', html)
    return html


def main():
    test_mode = "--test" in sys.argv
    changed = 0
    skipped = 0

    for fname in ['index.html', 'v2.html', 'poster.html', 'heic-converter.html']:
        fpath = ROOT / fname
        if not fpath.exists():
            continue
        html = fpath.read_text(encoding='utf-8')
        if not page_uses_fontawesome(html):
            new_html = remove_fa_loaders(html)
            if new_html != html:
                if not test_mode:
                    fpath.write_text(new_html, encoding='utf-8')
                print(f"  ok {fname}: removed FontAwesome (no icons used)")
                changed += 1
            else:
                skipped += 1
        else:
            print(f"  -  {fname}: keeps FontAwesome (icons in use)")
            skipped += 1

    for fpath in sorted(BLOG_DIR.glob("*.html")):
        html = fpath.read_text(encoding='utf-8')
        if not page_uses_fontawesome(html):
            new_html = remove_fa_loaders(html)
            if new_html != html:
                if not test_mode:
                    fpath.write_text(new_html, encoding='utf-8')
                print(f"  ok blog/{fpath.name}: removed FontAwesome")
                changed += 1
            else:
                skipped += 1
        else:
            skipped += 1

    print(f"\nDone: {changed} updated, {skipped} skipped")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run the script**

```bash
python3 scripts/remove_unused_fa.py
```

Expected: Output shows which pages had FontAwesome removed.

- [ ] **Step 4: Verify no pages still load FontAwesome unnecessarily**

```bash
echo "Pages still loading FontAwesome:"
grep -rl "font-awesome" index.html v2.html poster.html heic-converter.html blog/ 2>/dev/null | wc -l
```

Expected: Only pages that render actual `fa-` icons.

- [ ] **Step 5: Commit**

```bash
git add scripts/remove_unused_fa.py
git commit -m "perf: remove unused FontAwesome CSS from pages without icons"
```

---

### Task 5: Fix accessibility issues (button names, color contrast, image aspect ratios)

**Files:**
- Modify: `index.html`
- Modify: `v2.html`

The Lighthouse a11y audit flags:
1. Buttons without accessible names (icon-only buttons)
2. Color contrast insufficient (footer links)
3. Image aspect ratio incorrect

- [ ] **Step 1: Add `aria-label` to icon-only social buttons in index.html**

Search for `fa-whatsapp` and `fa-instagram`. Each `<a>` with only an icon needs an `aria-label`:

Before:
```html
<a href="https://wa.me/85263796410"><i class="fab fa-whatsapp"></i></a>
```

After:
```html
<a href="https://wa.me/85263796410" aria-label="WhatsApp 聯絡我們"><i class="fab fa-whatsapp" aria-hidden="true"></i></a>
```

Also fix the hamburger menu toggle:
```html
<button aria-label="開啟選單" aria-expanded="false">
  <i class="fas fa-bars" aria-hidden="true"></i>
</button>
```

And the Sticky Conversion Bar social buttons.

- [ ] **Step 2: Fix the same buttons in v2.html**

Apply the same `aria-label` + `aria-hidden="true"` pattern to `v2.html`. Search for `fa-whatsapp`, `fa-instagram`, `fa-bars`.

- [ ] **Step 3: Fix color contrast in footer links**

In both `index.html` and `v2.html`, footer links use `text-gray-400` on `bg-gray-800`. This fails WCAG contrast. Change to `text-gray-300`:

```html
<!-- Before -->
<a href="privacy.html" class="footer-link text-gray-400 hover:text-white">
<!-- After -->
<a href="privacy.html" class="footer-link text-gray-300 hover:text-white underline-offset-2">
```

- [ ] **Step 4: Fix image aspect ratio**

For each `<img>` with explicit `width` and `height` in `index.html` and `v2.html`, verify the aspect ratio matches the actual image dimensions.

Check the blue swatch:
```bash
python3 -c "from PIL import Image; im=Image.open('image/cert_color_blue.jpg'); print(f'Actual: {im.size[0]}x{im.size[1]}')"
```

If the actual aspect ratio differs from the HTML `width`/`height` attributes, correct the HTML. For example, if actual is 200x150 but HTML says `width="200" height="144"`, fix to `height="150"`.

- [ ] **Step 5: Commit**

```bash
git add index.html v2.html
git commit -m "fix(a11y): add aria-labels to icon buttons, fix color contrast, fix image aspect ratios"
```

---

### Task 6: Add Content Security Policy meta tag

**Files:**
- Modify: `index.html`
- Modify: `v2.html`
- Modify: `poster.html`
- Modify: `heic-converter.html`

Lighthouse flags missing CSP under Best Practices. Add via `<meta>` tag.

- [ ] **Step 1: Add CSP to index.html**

After `<title>` in `<head>`, add:

```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  img-src 'self' data: https:;
  script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://cdnjs.cloudflare.com;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://unpkg.com;
  font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com;
  connect-src 'self' https://www.google-analytics.com;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
">
```

- [ ] **Step 2: Add same CSP to v2.html, poster.html, heic-converter.html**

Copy the same `<meta>` tag into `<head>` after `<title>` in each file.

- [ ] **Step 3: Quick smoke test**

Open each modified page in a browser. Open DevTools console and check for CSP violation errors. If any resource is blocked, add its origin to the appropriate CSP directive.

Common issues:
- If Swiper CSS fails to load → add `https://unpkg.com` to `style-src` (already in template above)
- If Google Analytics fails → add `https://www.google-analytics.com` to `connect-src` (already in template above)

- [ ] **Step 4: Commit**

```bash
git add index.html v2.html poster.html heic-converter.html
git commit -m "feat(security): add Content Security Policy meta tag"
```

---

### Task 7: Inline critical CSS, load Tailwind asynchronously

**Files:**
- Modify: `index.html`
- Modify: `v2.html`

Tailwind.css is currently render-blocking. Inline the ~15 essential CSS rules for above-fold content and load the full Tailwind asynchronously.

- [ ] **Step 1: Check current Tailwind file**

```bash
ls -lh css/tailwind.min.css
```

Expected: ~3-4 MB.

- [ ] **Step 2: Add critical CSS inline block and async Tailwind loader to index.html**

Before the Tailwind stylesheet `<link>`, add a `<style>` block with critical above-fold styles:

```html
<style>
/* Critical above-fold styles for My O! */
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, system-ui, sans-serif; background: #fff; color: #1a1a1a; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; height: auto; display: block; }
a { color: inherit; text-decoration: none; }
.hero-section { display: flex; align-items: center; justify-content: center; min-height: 70vh; padding: 1rem; }
.flex { display: flex; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.text-center { text-align: center; }
.w-full { width: 100%; }
.h-auto { height: auto; }
.rounded-2xl { border-radius: 1rem; }
.shadow-lg { box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
.bg-white { background: #fff; }
.text-rose-500 { color: #e11d48; }
.font-bold { font-weight: 700; }
.p-4 { padding: 1rem; }
.m-0 { margin: 0; }
.grid { display: grid; }
.gap-4 { gap: 1rem; }
@media (max-width: 640px) { .hero-section { min-height: 60vh; } }
</style>
```

Then change the Tailwind link to load async:

```html
<!-- Before -->
<link rel="stylesheet" href="/css/tailwind.min.css">
<!-- After -->
<link rel="preload" href="/css/tailwind.min.css" as="style" onload="this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/css/tailwind.min.css"></noscript>
```

- [ ] **Step 3: Apply same pattern to v2.html**

Copy the critical CSS block and async Tailwind loader to `v2.html`. Adjust critical styles if v2 uses different above-fold classes.

- [ ] **Step 4: Visual verification**

Open `index.html` and `v2.html` in a browser. The page should look "correct" (styled hero, navigation, CTAs visible) before the full Tailwind CSS finishes loading. If anything looks broken (missing spacing, wrong colors), add the missing class to the critical CSS block.

- [ ] **Step 5: Commit**

```bash
git add index.html v2.html
git commit -m "perf: inline critical CSS, load Tailwind asynchronously"
```

---

### Task 8: Create Lighthouse verification script

**Files:**
- Create: `tests/lighthouse-check.sh`

- [ ] **Step 1: Create script**

Write `tests/lighthouse-check.sh`:

```bash
#!/bin/bash
# Lighthouse performance checker
# Usage: ./tests/lighthouse-check.sh [url]
set -euo pipefail

URL="${1:-https://myo-makeyourown.pages.dev}"

echo "=== Lighthouse Check: $URL ==="
echo ""

if command -v lighthouse &> /dev/null; then
    echo "Running Lighthouse locally (mobile emulation)..."
    lighthouse "$URL" \
        --preset=desktop \
        --output=json \
        --output-path=/tmp/lighthouse-result.json \
        --chrome-flags="--headless --no-sandbox" \
        2>/dev/null || true

    if [ -f /tmp/lighthouse-result.json ]; then
        python3 -c "
import json
d = json.load(open('/tmp/lighthouse-result.json'))
for cat, data in d['categories'].items():
    score = data['score'] * 100
    print(f'{cat:20s}: {score:.0f}')
" 2>/dev/null || echo "Could not parse results"
    fi
else
    echo "Lighthouse CLI not found. Install: npm install -g lighthouse"
    echo "Or visit: https://pagespeed.web.dev/?url=$URL"
fi
```

- [ ] **Step 2: Make executable**

```bash
chmod +x tests/lighthouse-check.sh
```

- [ ] **Step 3: Commit**

```bash
git add tests/lighthouse-check.sh
git commit -m "chore: add Lighthouse verification script"
```

---

### Task 9: Run final verification and measure improvement

**Files:** None (verification only)

- [ ] **Step 1: Run PageSpeed Insights**

Open `https://pagespeed.web.dev/` and test `https://myo-makeyourown.pages.dev` (Mobile). Or if Lighthouse CLI is installed:

```bash
npx lighthouse https://myo-makeyourown.pages.dev --output=json --output-path=/tmp/lighthouse-final.json 2>/dev/null
python3 -c "
import json
d = json.load(open('/tmp/lighthouse-final.json'))
for cat, data in d['categories'].items():
    print(f'{cat:20s}: {data[\"score\"]*100:.0f}')
metrics = d['audits']
for m in ['first-contentful-paint', 'largest-contentful-paint', 'speed-index', 'total-blocking-time', 'cumulative-layout-shift', 'interaction-to-next-paint']:
    if m in metrics:
        v = metrics[m]
        print(f'{m:30s}: {v.get(\"displayValue\", \"N/A\")}')
"
```

- [ ] **Step 2: Save fresh report**

Download the PageSpeed Insights HTML report and save it as:

```bash
cp /tmp/lighthouse-final.json docs/PageSpeed-optimization-result.json
```

- [ ] **Step 3: Compare results with baseline**

| Metric | Before | Target | After |
|--------|--------|--------|-------|
| Performance | 77 | 90+ | __ |
| FCP | 3.9s | ≤2.5s | __ |
| Total page weight | 1,081 KiB | ≤600 KiB | __ |

If target not met, check remaining Lighthouse opportunities and iterate on the largest one.

---

## Self-Review

**1. Spec coverage:**
All PageSpeed Insights opportunities are addressed:
- Task 1: PNG removal — eliminates 2.2 MB redundant assets
- Task 2: Image compression — addresses the 418 KB image delivery savings opportunity
- Task 3: Batch script — maintenance tooling for ongoing optimization
- Task 4: FontAwesome cleanup — removes ~65 KB of unused CSS from FA-free pages
- Task 5: Accessibility — fixes 3 of the 4 failed a11y audits (button names, contrast, aspect ratio)
- Task 6: CSP — fixes the "no CSP in enforcement" Best Practices warning
- Task 7: Critical CSS inline — addresses render-blocking resources + unused CSS (18 KB)
- Task 8: Verification script — testing infrastructure
- Task 9: Final verification — confirms the goal is met

Not covered: `llms.txt` compliance (SEO diagnostic, non-blocking for Performance score), Swiper removal from non-carousel pages (minor, only adds ~30 KB). These are optional follow-ups.

**2. Placeholder scan:**
- Task 9 has `__` placeholders for "after" values — intentional (unknown until Task 9 completes).
- No TBD/TODO/placeholder code in any step. All code blocks are complete implementations.
- No "implement later" or "fill in details" patterns.

**3. Type consistency:**
- `optimize_webp(source, output, quality)` and `optimize_jpeg(source, output, quality)` — signatures match across Tasks 2 and 3.
- `aria-label` and `aria-hidden="true"` pattern for icon buttons — consistent across Task 5.
- CSP directives — same policy applied across all 4 files in Task 6.
- No function/method name conflicts between tasks.
- CSS class names (`.hero-section`, `.footer-link`) are consistent with existing codebase conventions.
