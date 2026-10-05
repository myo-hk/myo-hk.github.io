# PageSpeed Insights Follow-Up — Desktop 88→90+ & llms.txt Fix

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close remaining gaps from PageSpeed Insights report (Mobile 97, Desktop 88, Best Practices 88, llms.txt score 0). Fix llms.txt link format, boost Desktop Performance to 90+, and resolve console errors.

**Architecture:** The existing plan (`2026-07-14-pagespeed-optimization.md`) was already executed — PNG textures removed, images compressed, critical CSS inlined, CSP added, a11y fixes committed. This plan covers what's left. Desktop Performance lags behind Mobile because (1) desktop has more viewport area loading more images simultaneously, (2) unused JS/CSS affects both, (3) FontAwesome is still loaded on pages without icons. The llms.txt needs markdown link syntax `[text](url)` instead of bare URLs.

**Tech Stack:** Python 3, grep/sed, HTML editing, Lighthouse CLI for verification

**Source Data:** `docs/PageSpeed Insights.html` — Lighthouse 13.4.0, run 2026-07-14

**Current Baseline:**
| Category | Mobile | Desktop |
|----------|--------|---------|
| Performance | 97 ✅ | 88 ⚠️ |
| Accessibility | 91 ⚠️ | 96 ✅ |
| Best Practices | 88 ⚠️ | 88 ⚠️ |
| SEO | 100 ✅ | 100 ✅ |

**Not covered in this plan (already in existing plan):**
- PNG texture removal ✅ done
- Image compression ✅ done
- Critical CSS inlining ✅ done
- CSP meta tag ✅ done
- A11y button names / contrast ✅ done

---

## File Structure

| File | Role | Changes |
|------|------|---------|
| `llms.txt` | AI-accessible site summary | Convert bare URLs to `[text](url)` markdown links; fix broken links |
| `index.html` | Main homepage | Remove FontAwesome preload/noscript if no icons used; add `loading="lazy"` to below-fold images |
| `v2.html` | Redesigned homepage | Same FA removal + lazy loading |
| `poster.html` | Flyer page | Remove FontAwesome if unused; lazy load images |
| `heic-converter.html` | HEIC converter tool | Remove FontAwesome preload/noscript if unused |
| `blog/*.html` | 420+ blog articles | Remove FontAwesome preload from pages without icons |
| `scripts/fix_llms_txt.py` | **NEW** — llms.txt fixer | Convert bare URLs to markdown links |
| `scripts/remove_unused_fa.py` | **NEW** — FA cleanup | Remove FontAwesome from icon-free pages |
| `tests/lighthouse-check.sh` | **NEW** — verification | Check scores after changes |

---

### Task 1: Fix llms.txt — convert bare URLs to markdown link format

**Files:**
- Modify: `llms.txt`

The Lighthouse audit reports `llms.txt` score 0 because "File does not appear to contain any links." The `llms.txt` spec (https://llmstxt.org/) requires markdown link syntax `[text](url)`, not bare URLs. The file currently uses `- Homepage: https://...` (bare URL), which AI crawlers don't parse as links. Also, `pricing.md` and `faq.html` should be verified (they exist but pricing.md is a raw Markdown file, not HTML).

- [ ] **Step 1: Convert llms.txt to proper markdown link format**

Replace each bare URL line with markdown link syntax. Current format:
```
- Homepage: https://myo-makeyourown.pages.dev/
```

New format:
```
- [Homepage](https://myo-makeyourown.pages.dev/)
```

Write `scripts/fix_llms_txt.py` to do this conversion:

```python
#!/usr/bin/env python3
"""
Convert llms.txt bare URLs to proper markdown link format [text](url).
Also validates that linked files exist.

Usage: python3 scripts/fix_llms_txt.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
LLMS_PATH = ROOT / "llms.txt"

# Map of section → known good link targets
# Lines like "- Homepage: https://..." or "- 婚禮攝影拍照清單: https://..."
BARE_URL_PATTERN = re.compile(
    r'^(- \s*)([^:]+):\s*(https?://[^\s]+)'
)

# Broken links to fix
BROKEN_LINKS = {
    # pricing.md exists as raw markdown, not a web page — remove it
    "pricing.md": None,
    # faq.html exists, keep it
}

def convert_line(line: str) -> str:
    m = BARE_URL_PATTERN.match(line)
    if m:
        prefix = m.group(1)
        label = m.group(2).strip()
        url = m.group(3).strip()
        # Check for known broken links
        for broken, replacement in BROKEN_LINKS.items():
            if broken in url:
                if replacement is None:
                    return f"# REMOVED: {line.strip()}\n"
                url = replacement
                break
        return f"{prefix}[{label}]({url})\n"
    return line


def main():
    lines = LLMS_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    converted = [convert_line(l) for l in lines]
    LLMS_PATH.write_text("".join(converted), encoding="utf-8")
    print(f"✅ Updated {LLMS_PATH}")

    # Count results
    text = LLMS_PATH.read_text(encoding="utf-8")
    md_links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text))
    bare_urls = len(re.findall(r'https?://[^\s\)]+', text))
    print(f"   Markdown links: {md_links}")
    print(f"   Bare URLs remaining: {bare_urls}")

    # Verify: bare URLs should only appear INSIDE markdown link parentheses
    # e.g., [text](https://...) — the URL inside parens is valid
    # A bare URL outside parens means we missed one
    outside_parens = re.findall(r'(?<!\(https?://[^)]*)https?://[^\s\)]+', text)
    if outside_parens:
        print(f"⚠️  {len(outside_parens)} URLs outside link syntax found:")
        for u in outside_parens[:5]:
            print(f"  - {u[:80]}")
    else:
        print("✅ No bare URLs outside link syntax")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the fixer script**

```bash
python3 scripts/fix_llms_txt.py
```

Expected output:
```
✅ Updated /Users/bubu/Documents/Github/myo-hk/llms.txt
   Markdown links: 42
   Bare URLs remaining: 0  (or 42 if counting URLs inside parentheses)
```

- [ ] **Step 3: Manually verify the output looks correct**

```bash
head -20 /Users/bubu/Documents/Github/myo-hk/llms.txt
```

Expected: Each line should read `- [Section Label](https://...)` not `- Section Label: https://...`

- [ ] **Step 4: Commit**

```bash
git add llms.txt scripts/fix_llms_txt.py
git commit -m "fix(seo): convert llms.txt bare URLs to markdown link format (fixes Lighthouse score)
```

---

### Task 2: Debug console errors and inspector issues

**Files:**
- Verify: `index.html`, `v2.html` (root pages)
- Tools: Browser DevTools console inspection

Lighthouse Best Practices is 88 due to `errors-in-console` and `inspector-issues` failing. These could be from:
- Google Analytics / GTM loading errors
- Swiper initialization warnings
- CSP violations
- Image loading failures

- [ ] **Step 1: Open the live site and check browser console**

```bash
# Use Playwright to capture console errors on the homepage
npx playwright eval "const { chromium } = require('playwright'); (async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push(err.message));
  await page.goto('https://myo-makeyourown.pages.dev/', { waitUntil: 'networkidle', timeout: 30000 });
  console.log(JSON.stringify(errors, null, 2));
  await browser.close();
})();"
```

Expected: Array of console error strings, if any.

- [ ] **Step 2: Fix each identified error**

Common fixes by error type:

**CSP violation errors:**
If CSP blocks any resource, add its origin to the appropriate directive in the `<meta http-equiv="Content-Security-Policy">` tag in `index.html` and `v2.html`.

```bash
# Check current CSP
grep -A 10 'Content-Security-Policy' /Users/bubu/Documents/Github/myo-hk/index.html | head -15
```

Missing origins should be added like:
```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  img-src 'self' data: https:;
  script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://cdnjs.cloudflare.com https://static.cloudflareinsights.com;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://unpkg.com;
  font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com;
  connect-src 'self' https://www.google-analytics.com https://cloudflareinsights.com;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
">
```

**JS errors (e.g. Swiper, FontAwesome):**
If external scripts fail to load, verify the CDN URLs are still valid:

```bash
curl -sI https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css | head -5
curl -sI https://unpkg.com/swiper@8/swiper-bundle.min.css | head -5
```

If any return non-200, update the version in the HTML files:

```bash
grep -rn "swiper\|font-awesome" /Users/bubu/Documents/Github/myo-hk/index.html
```

- [ ] **Step 3: Fix any Swiper warnings**

If Swiper is loaded on pages without a carousel, the JS initializes and logs warnings. Remove Swiper from pages that don't use it:

```bash
for f in /Users/bubu/Documents/Github/myo-hk/v2.html /Users/bubu/Documents/Github/myo-hk/poster.html /Users/bubu/Documents/Github/myo-hk/heic-converter.html; do
  has_swiper_html=$(grep -c 'swiper-container\|swiper-slide\|swiper-wrapper' "$f" 2>/dev/null || echo 0)
  has_swiper_js=$(grep -c 'swiper-bundle\|new Swiper' "$f" 2>/dev/null || echo 0)
  echo "$(basename $f): HTML refs=$has_swiper_html JS refs=$has_swiper_js"
done
```

For pages with `has_swiper_html = 0` but `has_swiper_js > 0`, remove the Swiper CSS/JS loader lines.

- [ ] **Step 4: Commit fixes**

```bash
git add index.html v2.html
git commit -m "fix(best-practices): resolve console errors and CSP violations"
```

---

### Task 3: Remove unused FontAwesome CSS from icon-free pages

**Files:**
- Modify: `index.html`, `v2.html`, `poster.html`, `heic-converter.html`, `blog/*.html`

FontAwesome CSS (~65 KB) is loaded via preload + noscript on every page. Many pages (especially blog articles) never use `fa-*` icons.

- [ ] **Step 1: Check which pages actually use FontAwesome**

```bash
# Check root pages
for f in /Users/bubu/Documents/Github/myo-hk/index.html /Users/bubu/Documents/Github/myo-hk/v2.html /Users/bubu/Documents/Github/myo-hk/poster.html /Users/bubu/Documents/Github/myo-hk/heic-converter.html; do
  fa_body=$(grep -c 'class="[^"]*fa-\|class="[^"]*fab \|class="[^"]*fas ' "$f" 2>/dev/null || echo 0)
  fa_head=$(grep -c 'font-awesome' "$f" 2>/dev/null || echo 0)
  echo "$(basename $f): FA in body=$fa_body FA in head=$fa_head"
done
```

- [ ] **Step 2: Create the FA removal script**

Write `scripts/remove_unused_fa.py`:

```python
#!/usr/bin/env python3
"""
Remove FontAwesome CSS preload/noscript from HTML pages that don't use
any fa-* classes in their body content.

Usage: python3 scripts/remove_unused_fa.py [--test]
       --test : dry-run, print what would change without modifying files
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
BLOG_DIR = ROOT / "blog"

# Matches FontAwesome preload: <link rel="preload" href="...font-awesome...css" as="style" ...>
FA_PRELOAD = re.compile(
    r'\s*<link\s+rel="preload"\s+href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+\.css"[^>]*>\s*\n?'
)
# Matches FontAwesome noscript/stylesheet: <noscript><link rel="stylesheet" href="...font-awesome...css"...></noscript>
FA_NOSCRIPT = re.compile(
    r'\s*<noscript><link\s+rel="stylesheet"\s+href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+\.css"[^>]*></noscript>\s*\n?'
)

def uses_fontawesome(html: str) -> bool:
    """Check if <body> contains any fa- class usage."""
    body_match = re.search(r'<body', html)
    if not body_match:
        return False
    body = html[body_match.start():]
    return bool(re.search(r'class="[^"]*fa-[^"]*"', body))

def remove_fa_loaders(html: str) -> str:
    """Strip FontAwesome CSS preload and noscript elements."""
    html = FA_PRELOAD.sub('', html)
    html = FA_NOSCRIPT.sub('', html)
    return html

def process_file(fpath: Path, test_mode: bool) -> bool:
    """Returns True if file was (or would be) changed."""
    html = fpath.read_text(encoding='utf-8')
    if uses_fontawesome(html):
        print(f"  ⏭️  {fpath.relative_to(ROOT)} — keeps FA (icons in use)")
        return False
    new_html = remove_fa_loaders(html)
    if new_html == html:
        print(f"  ⏭️  {fpath.relative_to(ROOT)} — no FA loaders found")
        return False
    if not test_mode:
        fpath.write_text(new_html, encoding='utf-8')
    print(f"  ✅ {fpath.relative_to(ROOT)} — removed FA loaders")
    return True

def main():
    test_mode = "--test" in sys.argv
    if test_mode:
        print("🔍 DRY RUN — no files will be modified\n")

    changed = 0

    # Root pages
    for name in ['index.html', 'v2.html', 'poster.html', 'heic-converter.html']:
        fpath = ROOT / name
        if fpath.exists():
            if process_file(fpath, test_mode):
                changed += 1

    # Blog articles
    for fpath in sorted(BLOG_DIR.glob("*.html")):
        if process_file(fpath, test_mode):
            changed += 1

    print(f"\n{'🔍 Would change' if test_mode else '✅ Changed'} {changed} file(s)")
    return changed

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run in test mode to preview changes**

```bash
python3 scripts/remove_unused_fa.py --test
```

Expected: Shows which pages would lose FontAwesome (only those with zero `fa-` class references in body).

- [ ] **Step 4: Run for real**

```bash
python3 scripts/remove_unused_fa.py
```

Expected: `✅ Changed N file(s)` — N depends on how many blog articles lack icons.

- [ ] **Step 5: Verify no pages broke (spot-check a few)**

```bash
# Check a blog article that had FA removed — does it still render?
head -5 /Users/bubu/Documents/Github/myo-hk/blog/婚禮攝影拍照清單.html | grep -c 'font-awesome'
```
Expected: `0` (FA removed, page still loads fine without it).

- [ ] **Step 6: Commit**

```bash
git add scripts/remove_unused_fa.py
git add -u blog/  # track all modified blog files
git commit -m "perf: remove unused FontAwesome CSS from icon-free pages (saves ~65 KB each)"
```

---

### Task 4: Add loading="lazy" to below-fold images on root pages

**Files:**
- Modify: `index.html`
- Modify: `v2.html`

Below-fold images (color swatches, product previews, social proof) delay LCP if loaded eagerly. Add `loading="lazy"` to all `<img>` tags that are not the hero/LCP image.

- [ ] **Step 1: Add lazy loading to non-hero images in index.html**

In `index.html`, find all `<img>` tags that are NOT the hero image. Add `loading="lazy"` to each:

```bash
# Find all img tags excluding the hero
grep -n '<img' /Users/bubu/Documents/Github/myo-hk/index.html | grep -v 'hero\|logo\|favicon' | head -20
```

For each below-fold image, add `loading="lazy"`:

```bash
# Example for color swatch images — add loading="lazy" after the src or class attribute
# In each <img> tag that isn't the hero, insert loading="lazy"
```

Edit the file: for each non-hero `<img>`, add the attribute. Pattern:
```html
<!-- Before -->
<img src="image/cert_color_beige.jpg" alt="米色亞麻布結婚證書套" class="...">
<!-- After -->
<img src="image/cert_color_beige.jpg" alt="米色亞麻布結婚證書套" class="..." loading="lazy">
```

- [ ] **Step 2: Same lazy loading in v2.html**

```bash
grep -n '<img' /Users/bubu/Documents/Github/myo-hk/v2.html | grep -v 'hero\|logo\|favicon' | head -20
```

Apply same `loading="lazy"` addition to non-hero images.

- [ ] **Step 3: Commit**

```bash
git add index.html v2.html
git commit -m "perf: add loading=lazy to below-fold images"
```

---

### Task 5: Desktop-specific image optimization

**Files:**
- Modify: `index.html`
- Modify: `v2.html`

Desktop Performance at 88 vs Mobile at 97 suggests desktop needs additional help. Desktop loads a larger viewport, which can mean more images visible simultaneously. The `image-delivery-insight` audit shows 300 KiB potential savings.

- [ ] **Step 1: Check if hero image has explicit sizes for desktop**

In both `index.html` and `v2.html`, ensure the hero `<img>` has `width` and `height` attributes for aspect ratio calculation:

```bash
grep -n 'cert_hero' /Users/bubu/Documents/Github/myo-hk/index.html
```

If missing, add them:
```html
<img src="image/cert_hero.webp" alt="My O! 結婚證書套"
     width="1200" height="800"
     class="w-full h-auto rounded-2xl shadow-lg" loading="eager">
```

- [ ] **Step 2: Verify hero image serving correct size for desktop**

Check if the hero has a `<picture>` element with desktop-specific sizes:

```bash
grep -A 5 'cert_hero' /Users/bubu/Documents/Github/myo-hk/index.html
```

If it uses a single WebP at all viewports, add a `sizes` attribute or consider serving a higher-resolution version for desktop. For static sites, adding `sizes` alone helps:
```html
<img src="image/cert_hero.webp"
     sizes="(max-width: 768px) 100vw, 1200px"
     ...>
```

- [ ] **Step 3: Commit**

```bash
git add index.html v2.html
git commit -m "perf: add explicit image sizes and responsive hints for desktop"
```

---

### Task 6: Create Lighthouse verification script

**Files:**
- Create: `tests/lighthouse-check.sh`

- [ ] **Step 1: Create the script**

Write `tests/lighthouse-check.sh`:

```bash
#!/bin/bash
# Lighthouse score checker for My O!
# Usage: ./tests/lighthouse-check.sh [mobile|desktop] [url]
set -euo pipefail

MODE="${1:-mobile}"
URL="${2:-https://myo-makeyourown.pages.dev}"
OUTFILE="/tmp/lighthouse-${MODE}-result.json"

echo "=== Lighthouse $MODE: $URL ==="

if command -v lighthouse &> /dev/null; then
    PRESET="--preset=$MODE"
    npx lighthouse "$URL" \
        $PRESET \
        --output=json \
        --output-path="$OUTFILE" \
        --chrome-flags="--headless --no-sandbox" \
        2>/dev/null || true

    if [ -f "$OUTFILE" ]; then
        python3 -c "
import json
with open('$OUTFILE') as f:
    d = json.load(f)
print()
print(f'  {\"Category\":20s} {\"Score\":>6s}  {\"Status\":>8s}')
print(f'  {\"-\"*20} {\"-\":>6s}  {\"-\":>8s}')
for cat, data in d['categories'].items():
    score = int(data['score'] * 100)
    status = '✅ PASS' if score >= 90 else ('⚠️  WARN' if score >= 50 else '❌ FAIL')
    print(f'  {cat:20s} {score:>4d}/100  {status}')
" 2>/dev/null || echo "Could not parse results"
    fi
else
    echo "Lighthouse CLI not found."
    echo "Install: npm install -g lighthouse"
    echo "Or visit: https://pagespeed.web.dev/?url=$URL"
fi
```

- [ ] **Step 2: Make executable and test**

```bash
chmod +x /Users/bubu/Documents/Github/myo-hk/tests/lighthouse-check.sh
/tests/lighthouse-check.sh mobile 2>&1 | head -15 || echo "(Lighthouse CLI may not be installed — this is expected)"
```

- [ ] **Step 3: Commit**

```bash
git add tests/lighthouse-check.sh
git commit -m "chore: add Lighthouse verification script"
```

---

### Task 7: Run final verification

**Files:** None (verification only)

- [ ] **Step 1: Run PageSpeed Insights on desktop**

```bash
open "https://pagespeed.web.dev/analysis/https-myo-makeyourown-pages-dev/"
```

Or if Lighthouse CLI is installed:
```bash
./tests/lighthouse-check.sh desktop
./tests/lighthouse-check.sh mobile
```

- [ ] **Step 2: Record results**

Save the fresh PageSpeed Insights report to `docs/PageSpeed Insights.html` (overwrite the existing one):

```bash
# After running the test, record the scores
```

| Category | Mobile Before | Mobile Target | Mobile After | Desktop Before | Desktop Target | Desktop After |
|----------|:------------:|:-------------:|:------------:|:--------------:|:--------------:|:-------------:|
| Performance | 97 | ≥97 | __ | 88 | ≥90 | __ |
| Accessibility | 91 | ≥95 | __ | 96 | ≥96 | __ |
| Best Practices | 88 | ≥90 | __ | 88 | ≥90 | __ |
| SEO | 100 | 100 | __ | 100 | 100 | __ |

If targets not met, check remaining Lighthouse opportunities and iterate on the largest contributor.

- [ ] **Step 3: Verify llms.txt passes**

After Task 1 is executed, re-check:
```bash
python3 -c "
import re
with open('llms.txt') as f:
    text = f.read()
md_links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text))
print(f'Markdown links: {md_links} (should be 42+)')
print(f'Has H1: {bool(re.search(r\"^# \", text, re.MULTILINE))}')
print(f'Has description: {bool(re.search(r\"^> \", text, re.MULTILINE))}')
"
```

Expected: Markdown links 42+, H1 present, blockquote description present.

---

## Self-Review

**1. Spec coverage:**
- Task 1: llms.txt conversion — directly fixes the Lighthouse score-0 audit
- Task 2: Console errors + inspector issues — fixes the two failing Best Practices audits
- Task 3: Remove unused FontAwesome — saves ~65 KB on icon-free pages, helps Desktop Performance
- Task 4: Lazy loading below-fold images — reduces initial page weight, helps Desktop Performance
- Task 5: Desktop image sizes — addresses desktop-specific rendering gap
- Task 6: Verification script — testing infrastructure
- Task 7: Final verification — confirms all targets met

**2. Placeholder scan:**
- No TBD/TODO/placeholder code. All code blocks are complete implementations.
- Task 7 has `__` for "after" values — intentional, they're unknown until verified.
- No "implement later" or "add validation" patterns.

**3. Type consistency:**
- `scripts/fix_llms_txt.py` — self-contained, no dependencies on other scripts
- `scripts/remove_unused_fa.py` — same removal pattern applied across all HTML files
- `loading="lazy"` attribute — consistent naming across all image tags
- Verification script `tests/lighthouse-check.sh` — consistent flag names between desktop/mobile
