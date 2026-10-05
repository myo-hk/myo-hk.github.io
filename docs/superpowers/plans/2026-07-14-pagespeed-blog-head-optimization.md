# Blog Page Head Optimization — Eliminate Render-Blocking CSS from 421 Blog Pages

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate render-blocking CSS resources from all 421 blog pages by switching Font Awesome, Tailwind CSS, and Google Fonts from synchronous `<link rel="stylesheet">` to non-blocking preload+onload patterns, adding preconnect hints for third-party origins, and fixing image dimension attributes to reduce CLS.

**Architecture:** A single Python batch script (following the established pattern in `scripts/`) performs all fixes on `blog/*.html` files. Root pages (index.html, v2.html, poster.html, privacy.html, faq.html) already use preload patterns and are left untouched.

**Tech Stack:** Python 3 (stdlib only: `re`, `os`, `sys`, `glob`, `pathlib`)

---

## Current State (blog pages)

Blog `<head>` sections have these issues:

1. **No preconnect hints** for `fonts.googleapis.com`, `fonts.gstatic.com`, `cdnjs.cloudflare.com`, `unpkg.com` — compared to index.html which has all of them
2. **Render-blocking Tailwind CSS:** `<link rel="stylesheet" href="/css/tailwind.min.css">` — blocks rendering
3. **Render-blocking Google Fonts:** `<link href="https://fonts.googleapis.com/css2?family=Inter:..." rel="stylesheet">` — blocks rendering
4. **Render-blocking Font Awesome:** `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" ...>` — blocks rendering
5. **Missing image dimensions:** Both header logo and footer sticky-bar logo `<img>` tags lack `width`/`height` attributes, causing CLS

## Target State (after changes)

Blog `<head>` will match index.html's pattern:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com">
<link rel="preconnect" href="https://unpkg.com">
<link rel="dns-prefetch" href="https://www.googletagmanager.com">
<link rel="preload" href="/css/tailwind.min.css" as="style" onload="this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/css/tailwind.min.css"></noscript>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet"></noscript>
<link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" as="style" integrity="sha512-..." crossorigin="anonymous" referrerpolicy="no-referrer" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-..." crossorigin="anonymous" referrerpolicy="no-referrer"></noscript>
```

And image tags will include `width="24" height="24"` to eliminate layout shift.

---

### Task 1: Create batch blog head optimizer script

**Files:**
- Create: `scripts/optimize_blog_head.py`
- Reference: `index.html` (lines 33-46) for the correct preload pattern

**Notes on the two Font Awesome link variants found in blog pages:**
1. With integrity hash (most common):
   ```html
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
   ```
2. Without integrity (some older pages):
   ```html
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
   ```

- [ ] **Step 1: Write the complete script**

```python
#!/usr/bin/env python3
"""
Batch-optimize <head> sections of all blog HTML files for PageSpeed.

Changes per file:
1. Insert preconnect hints if missing
2. Convert Font Awesome from render-blocking stylesheet to preload+onload
3. Convert Tailwind CSS from render-blocking stylesheet to preload+onload
4. Convert Google Fonts from render-blocking stylesheet to preload+onload
5. Add width/height/loading-lazy to header and footer logo <img> tags

Usage:
    python3 scripts/optimize_blog_head.py              # apply changes
    python3 scripts/optimize_blog_head.py --dry-run    # preview only
    python3 scripts/optimize_blog_head.py --verbose    # detailed per-file logging
"""

import re
import os
import sys
import glob

BLOG_DIR = "blog"

PRECONNECT_BLOCK = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://cdnjs.cloudflare.com">
    <link rel="preconnect" href="https://unpkg.com">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">"""

TAILWIND_PATTERN = re.compile(
    r'<link\s+rel="stylesheet"\s+href="/css/tailwind\.min\.css"\s*/>'
)
TAILWIND_REPLACEMENT = (
    '<link rel="preload" href="/css/tailwind.min.css" as="style" '
    'onload="this.rel=\'stylesheet\'">\n'
    '    <noscript><link rel="stylesheet" href="/css/tailwind.min.css"></noscript>'
)

GOOGLE_FONTS_PATTERN = re.compile(
    r'<link\s+href="https://fonts\.googleapis\.com/css2\?[^"]+"\s+rel="stylesheet"\s*/>'
)
GOOGLE_FONTS_REPLACEMENT = (
    '<link rel="preload" '
    'href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" '
    'as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
    '    <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" '
    'rel="stylesheet"></noscript>'
)

# FA with integrity hash: <link rel="stylesheet" href="..." integrity="..." crossorigin="..." referrerpolicy="..." />
FA_WITH_INTEGRITY = re.compile(
    r'<link\s+rel="stylesheet"\s+'
    r'href="(https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+/css/all\.min\.css)"\s+'
    r'integrity="([^"]+)"\s+'
    r'crossorigin="([^"]+)"\s+'
    r'referrerpolicy="([^"]+)"\s*/>'
)

# FA without integrity: <link rel="stylesheet" href="..." crossorigin="..." referrerpolicy="..." />
FA_NO_INTEGRITY = re.compile(
    r'<link\s+rel="stylesheet"\s+'
    r'href="(https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+/css/all\.min\.css)"\s+'
    r'crossorigin="([^"]+)"\s+'
    r'referrerpolicy="([^"]+)"\s*/>'
)

FOOTER_LOGO = re.compile(
    r'<img\s+src="\.\./image/01_company_logo\.png"\s+'
    r'alt="My O! Logo"\s+'
    r'class="logo"\s*/?>'
)
FOOTER_LOGO_REPLACEMENT = (
    '<img src="../image/01_company_logo.png" alt="My O! Logo" '
    'width="24" height="24" loading="lazy" class="logo">'
)

HEADER_LOGO = re.compile(
    r'(<img\s+loading="lazy"\s+src="\.\./image/01_company_logo\.png"\s+'
    r'class="[^"]*"\s+alt="[^"]*"\s*>)'
)


def make_fa_preload(href, integrity=None, crossorigin="anonymous", referrerpolicy="no-referrer"):
    """Build preload+noscript pair for a Font Awesome CSS URL."""
    int_attr = f' integrity="{integrity}"' if integrity else ''
    preload = (
        f'    <link rel="preload" href="{href}" as="style"'
        f'{int_attr} crossorigin="{crossorigin}"'
        f' referrerpolicy="{referrerpolicy}"'
        f' onload="this.onload=null;this.rel=\'stylesheet\'">\n'
        f'    <noscript><link rel="stylesheet" href="{href}"'
        f'{int_attr} crossorigin="{crossorigin}"'
        f' referrerpolicy="{referrerpolicy}"></noscript>'
    )
    return preload


def add_header_logo_dimensions(match):
    """Add width=24 height=24 to header logo if not already present."""
    tag = match.group(1)
    if 'width=' not in tag and 'height=' not in tag:
        return tag.replace('src="', 'width="24" height="24" src="', 1)
    return tag


def fix_preconnect_presence(content):
    """Detect if fonts.gstatic.com preconnect already exists in content."""
    return 'rel="preconnect"' in content and 'fonts.gstatic.com' in content


def fix_blog_file(filepath, dry_run=False, verbose=False):
    """Apply all optimizations to a single blog HTML file. Returns True if changed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # 1. Font Awesome: try with-integrity pattern first, then without
    fa_match = FA_WITH_INTEGRITY.search(content)
    if fa_match:
        href, integrity, crossorigin, referrerpolicy = fa_match.groups()
        replacement = make_fa_preload(href, integrity=integrity,
                                      crossorigin=crossorigin,
                                      referrerpolicy=referrerpolicy)
        content = FA_WITH_INTEGRITY.sub(replacement, content, count=1)
        changes.append("FA preload (with integrity)")
    else:
        fa_match = FA_NO_INTEGRITY.search(content)
        if fa_match:
            href, crossorigin, referrerpolicy = fa_match.groups()
            replacement = make_fa_preload(href, crossorigin=crossorigin,
                                          referrerpolicy=referrerpolicy)
            content = FA_NO_INTEGRITY.sub(replacement, content, count=1)
            changes.append("FA preload (no integrity)")

    # 2. Tailwind CSS
    if TAILWIND_PATTERN.search(content):
        content = TAILWIND_PATTERN.sub(TAILWIND_REPLACEMENT, content, count=1)
        changes.append("Tailwind preload")

    # 3. Google Fonts
    if GOOGLE_FONTS_PATTERN.search(content):
        content = GOOGLE_FONTS_PATTERN.sub(GOOGLE_FONTS_REPLACEMENT, content, count=1)
        changes.append("Google Fonts preload")

    # 4. Preconnect block (insert after <meta name="viewport" ...>)
    if not fix_preconnect_presence(content):
        vp_match = re.search(r'(<meta\s+name="viewport"[^>]*>\s*)', content)
        if vp_match:
            insert_at = vp_match.end()
            content = content[:insert_at] + "\n" + PRECONNECT_BLOCK + "\n" + content[insert_at:]
            changes.append("preconnect hints")

    # 5. Footer logo dimensions
    if FOOTER_LOGO.search(content):
        content = FOOTER_LOGO.sub(FOOTER_LOGO_REPLACEMENT, content)
        changes.append("footer logo dimensions")

    # 6. Header logo dimensions
    if HEADER_LOGO.search(content):
        content = HEADER_LOGO.sub(add_header_logo_dimensions, content)
        changes.append("header logo dimensions")

    if content == original:
        return False

    if dry_run:
        rel = os.path.relpath(filepath)
        print(f"[DRY-RUN] {rel}: {', '.join(changes)}")
        return True

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    if verbose:
        rel = os.path.relpath(filepath)
        print(f"[OK] {rel}: {', '.join(changes)}")
    return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or dry_run

    files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.html")))
    print(f"Found {len(files)} blog HTML files{' (dry-run mode)' if dry_run else ''}\n")

    modified = 0
    for filepath in files:
        if fix_blog_file(filepath, dry_run=dry_run, verbose=verbose):
            modified += 1

    print(f"\n{'Would modify' if dry_run else 'Modified'} {modified} of {len(files)} files")
    return 0 if modified > 0 or dry_run else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run dry-run to preview all changes**

```bash
python3 scripts/optimize_blog_head.py --dry-run
```

Expected: Lists all 421 blog files with their specific changes. Every file should show at minimum "FA preload" + "Tailwind preload" + "Google Fonts preload" + "preconnect hints". Most should also show "footer logo dimensions" and "header logo dimensions".

- [ ] **Step 3: Spot-check a sample file to confirm it's unchanged by dry-run**

```bash
grep 'font-awesome' "blog/婚禮攝影反射拍攝.html" | head -1
```

Expected: Still shows `rel="stylesheet"` (unchanged because dry-run).

- [ ] **Step 4: Apply the changes**

```bash
python3 scripts/optimize_blog_head.py
```

Expected: Runs without errors. Output shows progress (add `--verbose` for per-file details).

- [ ] **Step 5: Verify FA is now preload instead of stylesheet**

```bash
grep 'font-awesome' "blog/婚禮攝影反射拍攝.html" | head -5
```

Expected output (preload with onload + noscript fallback):
```
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" as="style" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer"></noscript>
```

- [ ] **Step 6: Verify preconnect hints were added**

```bash
grep -c 'preconnect' "blog/婚禮攝影反射拍攝.html"
```

Expected: At least 4 preconnect entries (fonts.googleapis.com, fonts.gstatic.com, cdnjs.cloudflare.com, unpkg.com).

- [ ] **Step 7: Verify Tailwind/Google Fonts are preload now**

```bash
grep 'tailwind\|googleapis' "blog/婚禮攝影反射拍攝.html"
```

Expected: Shows `rel="preload"` with `onload` for both. No `rel="stylesheet"` for either.

- [ ] **Step 8: Verify logo image dimensions**

```bash
grep '01_company_logo.png' "blog/婚禮攝影反射拍攝.html"
```

Expected output shows two lines. Header logo (line 348 area): has `width="24" height="24"` before `src=`. Footer logo (line 611 area): has `width="24" height="24" loading="lazy"`.

- [ ] **Step 9: Spot-check a few more files for variance**

```bash
# Check a page without integrity hash
grep 'font-awesome' "blog/婚宴甜品桌設計.html" | head -3
```

```bash
# Check a page with integrity hash 
grep 'font-awesome' "blog/婚禮攝影RAW格式.html" | head -3
```

Both should show the preload+noscript pattern.

- [ ] **Step 10: Commit**

```bash
git add scripts/optimize_blog_head.py blog/
git commit -m "perf: eliminate render-blocking CSS on 421 blog pages

- Convert Font Awesome from synchronous <link rel=stylesheet> to
  preload+onload+noscript pattern (handles both integrity and
  no-integrity variants)
- Convert Tailwind CSS to preload+onload pattern
- Convert Google Fonts to preload+onload pattern
- Add preconnect hints for fonts.googleapis.com, fonts.gstatic.com,
  cdnjs.cloudflare.com, unpkg.com, and dns-prefetch for gtm
- Add width=24 height=24 to header and footer logo <img> tags (CLS fix)

Root pages (index.html, v2.html, poster.html, faq.html, privacy.html)
already had preload patterns and are not affected."
```

---

### Task 2: Verify changes with PageSpeed re-audit

**Context:** After deploying to production, run a new PageSpeed audit on a representative blog article to confirm the render-blocking CSS issue is resolved.

- [ ] **Step 1: Deploy**

```bash
git push
```

Wait for Cloudflare Pages deployment to complete (~1-2 minutes).

- [ ] **Step 2: Run PageSpeed Insights on a blog article**

Test URL: `https://myo-makeyourown.pages.dev/blog/婚禮攝影反射拍攝.html`

Open `https://pagespeed.web.dev/` and run the audit, or use:

```bash
# If lighthouse CLI is installed
npx lighthouse "https://myo-makeyourown.pages.dev/blog/婚禮攝影反射拍攝.html" \
  --output=json --output-path=/tmp/blog-lh.json 2>/dev/null

python3 -c "
import json
d = json.load(open('/tmp/blog-lh.json'))
print('=== Categories ===')
for cat, data in d['categories'].items():
    print(f'  {cat}: {data[\"score\"]*100:.0f}')
print()
print('=== Key metrics ===')
for m in ['first-contentful-paint', 'largest-contentful-paint', 'speed-index',
          'total-blocking-time', 'cumulative-layout-shift', 'interaction-to-next-paint']:
    if m in d['audits']:
        v = d['audits'][m]
        print(f'  {m}: {v.get(\"displayValue\", \"N/A\")}')
print()
print('=== Opportunities ===')
for opp in d.get('audits', {}).values():
    if opp.get('details') and opp['details'].get('type') == 'opportunity':
        print(f'  {opp[\"id\"]}: {opp.get(\"displayValue\", \"N/A\")}')
"
```

- [ ] **Step 3: Check for specific improvements**

Compare with baseline:

| Metric/Diagnostic | Before (Desktop) | Expected After |
|---|---|---|
| Performance | 92 | 95+ |
| Eliminate render-blocking resources | Font Awesome, Tailwind, GF were blocking | 0 blocking CSS resources |
| Preconnect to required origins | cdnjs.cloudflare.com missing | All origins preconnected |
| CLS | small | 0 or near-0 (logos have dimensions) |
| FCP | baseline | should improve (non-blocking CSS) |

---

### Task 3 (Optional): Verify no blog page was corrupted

**Context:** A batch regex replacement on 421 files has inherent risk. Run a quick structural integrity check.

- [ ] **Step 1: Check all blog files still parse as valid HTML**

```bash
# Verify key structural elements survived
MISSING=0
for f in blog/*.html; do
    if ! grep -q '</html>' "$f"; then
        echo "MISSING </html>: $f"
        MISSING=$((MISSING+1))
    fi
done
echo "Files missing </html>: $MISSING"
```

Expected: 0 files missing closing tags.

- [ ] **Step 2: Verify no duplicate preconnect blocks**

```bash
DUPES=0
for f in blog/*.html; do
    count=$(grep -c 'fonts.googleapis.com' "$f" || true)
    if [ "$count" -gt 1 ]; then
        echo "DUPLICATE preconnect: $(basename $f) ($count matches)"
        DUPES=$((DUPES+1))
    fi
done
echo "Files with duplicate preconnect: $DUPES"
```

Expected: 0 duplicates (the script checks for existing preconnect before inserting).

---

## Self-Review

**1. Spec coverage:**
- Task 1: Blog head optimizer script covers all 4 head issues (preconnect hints, FA preload, Tailwind preload, Google Fonts preload) + image dimensions
- Task 2: Verification via PageSpeed re-audit confirms the fix
- Task 3: Structural integrity check prevents corruption

**2. Placeholder scan:**
- No TBD/TODO/placeholder code. All code blocks are complete Python implementations.
- No "implement later" or "fill in details" patterns.
- No empty code blocks.

**3. Type consistency:**
- `make_fa_preload()` handles both FA link variants consistently
- Regex patterns use the same capture group structure
- `fix_blog_file()` returns bool consistently for dry-run/apply paths
- All function names use `snake_case` matching codebase convention (see `scripts/add_sticky_bar.py`)
