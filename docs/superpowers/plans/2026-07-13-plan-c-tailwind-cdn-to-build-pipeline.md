# Plan C: Tailwind CDN → Build-Time CSS Pipeline

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Tailwind CDN Play script (`cdn.tailwindcss.com`) across all 426 HTML files with a locally pre-built, tree-shaken CSS file, reducing unused CSS by ~150+ KiB and eliminating render-blocking script loads.

**Architecture:** Currently every HTML page loads `https://cdn.tailwindcss.com` which generates CSS at runtime by scanning the DOM — extremely wasteful. Instead, we set up a local Tailwind CLI + PostCSS build that scans all HTML files for utility class usage, generates a minimal CSS file (`css/tailwind.min.css`), and replaces the CDN `<script>` tag with a `<link>` to the local file across all pages.

**Tech Stack:** Tailwind CSS CLI v3, PostCSS, cssnano, Python batch-replace script

**Files to create:**
- `package.json` — add `tailwindcss`, `postcss`, `cssnano`, `autoprefixer` as devDependencies
- `tailwind.config.js` — content paths scanning all `./**/*.html`, `./blog/**/*.html`
- `postcss.config.js` — PostCSS plugins pipeline
- `css/tailwind.src.css` — Tailwind directives (`@tailwind base/components/utilities`)
- `scripts/build-tailwind.py` — Build script + batch HTML updater

**Files to modify:**
- All 426 HTML files (root pages + blog articles) — replace CDN `<script>` with local `<link>`

---

### Task 1: Initialize Tailwind build toolchain

**Files:**
- Create: `package.json` (if no existing root package.json with Tailwind deps)
- Create: `tailwind.config.js`
- Create: `postcss.config.js`
- Create: `css/tailwind.src.css`
- Create: `.gitignore` entry for `node_modules`

- [ ] **Step 1: Check if root package.json exists**

```bash
ls package.json 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

If it exists, read it to check existing dependencies.

- [ ] **Step 2: Create `tailwind.config.js`**

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*.html',
    './blog/**/*.html',
    './css/*.css',
  ],
  safelist: [
    // Safelist any classes used dynamically (e.g. by JS)
    'swiper-pagination-bullet-active',
    'active',
    'hidden',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

> **Note:** If the existing `package.json` already includes Tailwind (for Playwright tests), skip creating a new one and just ensure the build deps are present.

- [ ] **Step 3: Create `postcss.config.js`**

```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {}),
  },
};
```

- [ ] **Step 4: Create `css/tailwind.src.css`**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 5: Install dependencies**

```bash
npm install --save-dev tailwindcss postcss autoprefixer cssnano
```

- [ ] **Step 6: Verify build works**

```bash
npx tailwindcss -i css/tailwind.src.css -o css/tailwind.min.css --minify
```

Expected output: A file `css/tailwind.min.css` is created, size approximately 50-200 KiB (tree-shaken for actual usage — much smaller than Play CDN's ~30,000+ class full build).

- [ ] **Step 7: Commit**

```bash
git add tailwind.config.js postcss.config.js css/ package.json package-lock.json
git commit -m "build: init tailwind CLI build pipeline with tree-shaking"
```

---

### Task 2: Build batch-replace script

**Files:**
- Create: `scripts/replace-tailwind-cdn.py`

- [ ] **Step 1: Create `scripts/replace-tailwind-cdn.py`**

```python
#!/usr/bin/env python3
"""
replace-tailwind-cdn.py — Replace Tailwind CDN <script> tag with local CSS <link> across all HTML files.

Usage:
    python3 scripts/replace-tailwind-cdn.py          # dry-run: show files that would change
    python3 scripts/replace-tailwind-cdn.py --write   # actually write changes
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Pattern: the CDN script tag (with optional whitespace/newlines)
CDN_PATTERN = re.compile(
    r'\s*<script[^>]*src="https://cdn\.tailwindcss\.com[^>]*></script>\s*'
)

REPLACEMENT = '\n    <link rel="stylesheet" href="/css/tailwind.min.css">\n'

def find_html_files():
    """Yield all .html files in the repo."""
    for pattern in ['*.html', 'blog/**/*.html']:
        for f in Path(ROOT).glob(pattern):
            if 'node_modules' in str(f) or 'presentations' in str(f):
                continue
            yield f

def process_file(filepath: Path, dry_run: bool = True) -> bool:
    """Replace CDN tag with local link. Returns True if changed."""
    original = filepath.read_text(encoding='utf-8')
    replaced = CDN_PATTERN.sub(REPLACEMENT, original)
    if replaced == original:
        return False
    if not dry_run:
        filepath.write_text(replaced, encoding='utf-8')
    return True

def main():
    dry_run = '--write' not in sys.argv
    total = changed = 0
    for f in find_html_files():
        total += 1
        if process_file(f, dry_run):
            changed += 1
            print(f"{'[DRY-RUN]' if dry_run else '[CHANGED]'} {f.relative_to(ROOT)}")
    print(f"\n{'DRY-RUN: ' if dry_run else ''}{changed} of {total} HTML files would change.")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run dry-run to verify scope**

```bash
python3 scripts/replace-tailwind-cdn.py
```

Expected: Shows 426 files (all existing HTML files with Tailwind CDN). Verify no `node_modules` or `presentations/` files are included.

- [ ] **Step 3: Commit**

```bash
git add scripts/replace-tailwind-cdn.py
git commit -m "feat: add batch script to replace tailwind CDN with local CSS link"
```

---

### Task 3: Rebuild the CSS

- [ ] **Step 1: Run a fresh production build**

```bash
NODE_ENV=production npx tailwindcss -i css/tailwind.src.css -o css/tailwind.min.css --minify
```

- [ ] **Step 2: Record the file size**

```bash
ls -lh css/tailwind.min.css
```

Expected: ~50-200 KiB (vs ~500+ KiB from CDN Play build that includes ALL classes).

> **Note:** If the output is unexpectedly tiny (< 5 KiB), the `content` globs in `tailwind.config.js` may not be matching all HTML files. Run `npx tailwindcss -i css/tailwind.src.css -o css/tailwind.min.css --minify --verbose` to see which files are being scanned.

- [ ] **Step 3: Commit**

```bash
git add css/tailwind.min.css
git commit -m "build: generate first tree-shaken tailwind CSS build"
```

---

### Task 4: Replace CDN across all HTML files

- [ ] **Step 1: Run the batch replace script with write mode**

```bash
python3 scripts/replace-tailwind-cdn.py --write
```

Expected: 426 files modified. Verify the diff:

```bash
git diff --stat
```

Should show 426 files changed, 1 insertion and 1 deletion each (remove CDN `<script>`, add local `<link>`).

- [ ] **Step 2: Spot-check a root page and a blog article**

```bash
grep 'tailwind' index.html
grep 'tailwind' blog/婚禮籌備清單.html
```

Expected: Only `/css/tailwind.min.css` references (no `cdn.tailwindcss.com`).

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "perf: replace tailwind CDN with local build across all 426 HTML pages"
```

---

### Task 5: Verify all pages render correctly

- [ ] **Step 1: Serve the site locally**

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/index.html`. Confirm:
- The page loads and styling is identical to the CDN version
- No layout shifts or missing styles

- [ ] **Step 2: Check a blog article**

Open `http://localhost:8000/blog/婚禮籌備清單.html`. Confirm styling matches the current site.

- [ ] **Step 3: Check v2.html**

Open `http://localhost:8000/v2.html`. Confirm all styling, including CSS variable-based design, is intact.

- [ ] **Step 4: Run Playwright tests**

```bash
npm test
```

Expected: All tests pass.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: verify all pages render correctly with local tailwind CSS"
```

---

### Task 6: Add build script and CI automation

**Files:**
- Modify: `package.json` — add build scripts

- [ ] **Step 1: Add npm scripts**

In `package.json`, add to the `"scripts"` section:

```json
"build:css": "tailwindcss -i css/tailwind.src.css -o css/tailwind.min.css --minify",
"build": "npm run build:css",
"prebuild": "npm run build:css",
```

- [ ] **Step 2: Test the build script**

```bash
npm run build:css
```

Expected: `css/tailwind.min.css` is regenerated.

- [ ] **Step 3: Commit**

```bash
git add package.json
git commit -m "build: add npm scripts for tailwind CSS build pipeline"
```

---

### Task 7: Final PageSpeed verification

- [ ] **Step 1: Deploy and test**

Push to GitHub/GitHub Pages and run `https://pagespeed.web.dev/` on the live site.

Expected:
- Mobile Performance: should increase from 56 → ~85+ (removing Tailwind CDN's 124 KiB render-blocking script + 780ms critical path delay)
- "Reduce unused CSS" warning should show significantly less potential savings (from 18 KiB to near 0)

- [ ] **Step 2: Record the new score**

```bash
# Optional: run lighthouse CLI on production
npx lighthouse https://myo-makeyourown.pages.dev --preset=desktop --output=json 2>/dev/null | grep -E '"performance"|"accessibility"'
```

- [ ] **Step 3: Commit any final adjustments**

```bash
git add -A
git commit -m "chore: final verification and adjustments after tailwind CDN migration"
```
