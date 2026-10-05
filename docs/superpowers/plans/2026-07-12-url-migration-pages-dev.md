# URL Migration: `myo-hk.github.io` → `myo-makeyourown.pages.dev`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate all hardcoded `https://myo-hk.github.io` references across the codebase to `https://myo-makeyourown.pages.dev` so that canonical URLs, OG tags, JSON-LD schemas, sitemaps, CTA links, and AI SEO files (`llms.txt`) all point to the live Cloudflare Pages deployment.

**Architecture:** The site is a pure static HTML site (no build step) deployed to Cloudflare Pages. The migration is a pure find-and-replace across ~500+ HTML/JS/PY/MD/TSX files, plus regenerating sitemaps. Two approaches are used: batch `sed` for simple text replacements across hundreds of files, and manual edits for structured files where precision matters (JSON-LD, canonical tags, TSX components). All blog articles have a JS fallback that dynamically overrides `canonical`/`og:url` via `window.location.href`, so those two tags are already covered — but `og:image` and JSON-LD remain hardcoded.

**Tech Stack:** Python 3 (batch scripts), sed (bulk replacements), shell (verification), git

---

## File Structure

### Files to modify (by task):

| Task | Files | Count | Method |
|------|-------|-------|--------|
| 1 | `scripts/generate_sitemap.py` | 1 | Manual edit |
| 2 | `robots.txt` | 1 | Manual edit |
| 3 | `index.html`, `v2.html`, `poster.html`, `heic-converter.html`, `privacy.html`, `terms.html` | 6 | Manual edit per file |
| 4 | `blog/*.html` (~421 files) | ~421 | Python batch script |
| 5 | `sitemap.xml`, `blog/sitemap.xml` | 2 | Regenerate via script |
| 6 | `README.md`, `llms.txt`, `pricing.md` | 3 | Manual edit |
| 7 | `scripts/generate-presentations/generate.js` | 1 | Manual edit |
| 8 | 3 TSX CTA components + ~76 script/outline.md files | ~79 | sed (markdown) + manual (TSX) |
| 9 | Verify everything | — | Shell commands |

### Batch script to create:

| Script | Purpose |
|--------|---------|
| `scripts/migrate_blog_urls.py` | Batch replace `myo-hk.github.io` → `myo-makeyourown.pages.dev` in all ~421 blog HTML files |

---

### Task 1: Update sitemap generation script

**Files:**
- Modify: `scripts/generate_sitemap.py:41-46,75`

- [ ] **Step 1: Replace hardcoded OLD_URL with NEW_URL in generate_root_sitemap()**

Edit `scripts/generate_sitemap.py` line 42:
```
OLD: loc = f"https://myo-hk.github.io/{filename}" if filename != "index.html" else "https://myo-hk.github.io/"
NEW: loc = f"https://myo-makeyourown.pages.dev/{filename}" if filename != "index.html" else "https://myo-makeyourown.pages.dev/"
```

- [ ] **Step 2: Replace blog index URL in generate_root_sitemap()**

Edit line 46:
```
OLD: add_url(urls, "https://myo-hk.github.io/blog/", NOW, "weekly", "0.8")
NEW: add_url(urls, "https://myo-makeyourown.pages.dev/blog/", NOW, "weekly", "0.8")
```

- [ ] **Step 3: Replace blog article URL template in generate_blog_sitemap()**

Edit line 75:
```
OLD: loc = f"https://myo-hk.github.io/blog/{escape(filename)}"
NEW: loc = f"https://myo-makeyourown.pages.dev/blog/{escape(filename)}"
```

- [ ] **Step 4: Verify changes**

```bash
grep -n 'myo-hk.github.io' scripts/generate_sitemap.py
```
Expected: no matches (all 3 occurrences should be replaced).

---

### Task 2: Update robots.txt

**Files:**
- Modify: `robots.txt:32-33`

- [ ] **Step 1: Replace sitemap URLs in robots.txt**

Edit lines 32-33:
```
OLD: Sitemap: https://myo-hk.github.io/sitemap.xml
NEW: Sitemap: https://myo-makeyourown.pages.dev/sitemap.xml

OLD: Sitemap: https://myo-hk.github.io/blog/sitemap.xml
NEW: Sitemap: https://myo-makeyourown.pages.dev/blog/sitemap.xml
```

- [ ] **Step 2: Verify**

```bash
grep -n 'Sitemap' robots.txt
```
Expected: `https://myo-makeyourown.pages.dev/sitemap.xml` and `.../blog/sitemap.xml`

---

### Task 3: Update root HTML pages (6 files)

**Files:**
- Modify: `index.html`
- Modify: `v2.html`
- Modify: `poster.html`
- Modify: `heic-converter.html`
- Modify: `privacy.html`
- Modify: `terms.html`

Each file has the same set of changes. The exact fields vary slightly per file (e.g., `index.html` has `og:url` for `/`, `heic-converter.html` has `og:url` for `/heic-converter.html`). Below is the canonical list of what to change per file — use exact `oldString`/`newString` matching.

**Pattern for ALL 6 files — replace these exact strings:**

1. `<link rel="canonical" href="https://myo-hk.github.io/` → `<link rel="canonical" href="https://myo-makeyourown.pages.dev/`

2. `<meta property="og:url" content="https://myo-hk.github.io` → `<meta property="og:url" content="https://myo-makeyourown.pages.dev`

3. `<meta property="og:image" content="https://myo-hk.github.io/` → `<meta property="og:image" content="https://myo-makeyourown.pages.dev/`

4. `<meta name="twitter:image" content="https://myo-hk.github.io/` → `<meta name="twitter:image" content="https://myo-makeyourown.pages.dev/` (only in privacy.html, terms.html)

5. JSON-LD `"url": "https://myo-hk.github.io` → `"url": "https://myo-makeyourown.pages.dev` (multiple per file)

6. JSON-LD `"logo": "https://myo-hk.github.io/` → `"logo": "https://myo-makeyourown.pages.dev/` (multiple per file)

7. JSON-LD `"image": "https://myo-hk.github.io/` → `"image": "https://myo-makeyourown.pages.dev/` (in Product schema)

8. JSON-LD `"urlTemplate": "https://myo-hk.github.io/` → `"urlTemplate": "https://myo-makeyourown.pages.dev/` (in Sitelinks Search Box, only index.html and v2.html)

- [ ] **Step 1: Update index.html**

Edit `index.html` using exact string replacements:
- `https://myo-hk.github.io/` → `https://myo-makeyourown.pages.dev/` (canonical, og:url, og:image)
- All JSON-LD URLs (WebSite Search, Organization, Product schemas)

Verify:
```bash
grep -c 'myo-hk.github.io' index.html
```
Expected: 0

- [ ] **Step 2: Update v2.html**

Same patterns as index.html.

Verify:
```bash
grep -c 'myo-hk.github.io' v2.html
```
Expected: 0

- [ ] **Step 3: Update poster.html**

Same patterns. Note: poster.html already has `myo-makeyourown.pages.dev` in the QR code section (lines 1080, 1083) — do NOT touch those, they're correct.

Verify:
```bash
grep -c 'myo-hk.github.io' poster.html
```
Expected: 0

- [ ] **Step 4: Update heic-converter.html**

Verify:
```bash
grep -c 'myo-hk.github.io' heic-converter.html
```
Expected: 0

- [ ] **Step 5: Update privacy.html**

Also replace `twitter:image` URL.

Verify:
```bash
grep -c 'myo-hk.github.io' privacy.html
```
Expected: 0

- [ ] **Step 6: Update terms.html**

Also replace `twitter:image` URL.

Verify:
```bash
grep -c 'myo-hk.github.io' terms.html
```
Expected: 0

---

### Task 4: Batch update all ~421 blog HTML files

**Files:**
- Create: `scripts/migrate_blog_urls.py`
- Modify: `blog/*.html` (~421 files)

Each blog HTML file has these hardcoded `myo-hk.github.io` references:
- `<link rel="canonical" href="https://myo-hk.github.io/blog/...">`
- `<meta property="og:image" content="https://myo-hk.github.io/image/...">`
- `<meta property="og:url" content="https://myo-hk.github.io/blog/...">`
- `<meta name="twitter:image" content="https://myo-hk.github.io/image/...">`
- JSON-LD BreadcrumbList: `"item":"https://myo-hk.github.io/"` and `"item":"https://myo-hk.github.io/blog/..."`
- JSON-LD Organization: `"url":"https://myo-hk.github.io"`, `"logo":"https://myo-hk.github.io/image/..."`

- [ ] **Step 1: Create batch migration script**

Create `scripts/migrate_blog_urls.py`:

```python
#!/usr/bin/env python3
"""
Batch replace myo-hk.github.io → myo-makeyourown.pages.dev in blog HTML files.
Usage: python3 scripts/migrate_blog_urls.py
"""

import glob
import os

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "blog")
OLD = "https://myo-hk.github.io"
NEW = "https://myo-makeyourown.pages.dev"

html_files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.html")))
changed = 0
nochange = 0

for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if OLD not in content:
        nochange += 1
        continue

    new_content = content.replace(OLD, NEW)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

    changed += 1
    print(f"  UPDATED: {os.path.basename(fpath)}")

print(f"\nDone: {changed} files updated, {nochange} files unchanged (already correct)")
```

- [ ] **Step 2: Run the migration script**

```bash
python3 scripts/migrate_blog_urls.py
```
Expected output: lists ~421 files updated, 0 unchanged.

- [ ] **Step 3: Spot-check a few files to confirm**

```bash
grep -c 'myo-hk.github.io' blog/婚禮蛋糕選擇.html blog/婚禮攝影拍照清單.html blog/結婚證書套保養.html
```
Expected: each file shows 0

---

### Task 5: Regenerate sitemaps

**Files:**
- Modify: `sitemap.xml` (regenerated)
- Modify: `blog/sitemap.xml` (regenerated)

- [ ] **Step 1: Run the sitemap generator**

```bash
python3 scripts/generate_sitemap.py
```
Expected output:
```
Root sitemap: 7 URLs → sitemap.xml
Blog sitemap: ~420 URLs → blog/sitemap.xml
Done.
```

- [ ] **Step 2: Verify new URLs in sitemaps**

```bash
grep -o 'https://[^"]*' sitemap.xml | head -5
grep -o 'https://[^"]*' blog/sitemap.xml | head -5
```
Expected: All URLs start with `https://myo-makeyourown.pages.dev/`

- [ ] **Step 3: Confirm no old URL remains in sitemaps**

```bash
grep -c 'myo-hk.github.io' sitemap.xml blog/sitemap.xml
```
Expected: both show 0

---

### Task 6: Update README, llms.txt, pricing.md

**Files:**
- Modify: `README.md`
- Modify: `llms.txt`
- Modify: `pricing.md`

- [ ] **Step 1: Update README.md**

Replace all remaining `myo-hk.github.io` references in README.md. Key locations:
- Line 5: Live Site link
- Line 6: 教學指南 link
- Line 256, 463, 605, 612, 853

```bash
sed -i '' 's|https://myo-hk\.github\.io|https://myo-makeyourown.pages.dev|g' README.md
```

Verify:
```bash
grep -c 'myo-hk.github.io' README.md
```
Expected: 0

- [ ] **Step 2: Update llms.txt**

```bash
sed -i '' 's|https://myo-hk\.github\.io|https://myo-makeyourown.pages.dev|g' llms.txt
```

Verify:
```bash
grep -c 'myo-hk.github.io' llms.txt
```
Expected: 0

- [ ] **Step 3: Update pricing.md**

```bash
sed -i '' 's|https://myo-hk\.github\.io|https://myo-makeyourown.pages.dev|g' pricing.md
```

Verify:
```bash
grep -c 'myo-hk.github.io' pricing.md
```
Expected: 0

---

### Task 7: Update presentation generator script

**Files:**
- Modify: `scripts/generate-presentations/generate.js:179,205,479-480,863`

This script generates CTA TSX components and narration scripts. It has 4 locations with `myo-hk.github.io`:

- Line 179: outline template — `呼籲行動（myo-hk.github.io）`
- Line 205: script template — `上 myo-hk.github.io`
- Lines 479-480: CTA TSX template — `<a href="https://myo-hk.github.io/">` and display text `myo-hk.github.io`
- Line 863: narrator data — `上 myo-hk.github.io`

- [ ] **Step 1: Replace all 4 occurrences**

```bash
sed -i '' 's|myo-hk\.github\.io|myo-makeyourown.pages.dev|g' scripts/generate-presentations/generate.js
```

- [ ] **Step 2: Verify**

```bash
grep -c 'myo-hk.github.io' scripts/generate-presentations/generate.js
```
Expected: 0

---

### Task 8: Update presentation files (TSX components + script/outline markdowns)

**Files:**
- Modify: `presentations/01-hong-kong-wedding-flow/presentation/src/chapters/06-after/After.tsx:164,170`
- Modify: `presentations/02-wedding-checklist-timeline/presentation/src/chapters/06-cta/CTA.tsx:60,65`
- Modify: `presentations/03-wedding-cost-breakdown/presentation/src/chapters/06-cta/CTA.tsx:56,57`
- Modify: ~38 `presentations/*/script.md` files (line 15 each)
- Modify: ~38 `presentations/*/outline.md` files (line 31 each)

- [ ] **Step 1: Update 3 TSX CTA components — manual edit per file**

**presentations/01-hong-kong-wedding-flow/presentation/src/chapters/06-after/After.tsx**

Two changes:
```
L164: href="https://myo-hk.github.io"
   →  href="https://myo-makeyourown.pages.dev"
L170: <span>myo-hk.github.io</span>
   →  <span>myo-makeyourown.pages.dev</span>
```

**presentations/02-wedding-checklist-timeline/presentation/src/chapters/06-cta/CTA.tsx**

Two changes:
```
L60: href="https://myo-hk.github.io/"
   →  href="https://myo-makeyourown.pages.dev/"
L65: myo-hk.github.io
   →  myo-makeyourown.pages.dev
```

**presentations/03-wedding-cost-breakdown/presentation/src/chapters/06-cta/CTA.tsx**

Two changes:
```
L56: href="https://myo-hk.github.io/"
   →  href="https://myo-makeyourown.pages.dev/"
L57: myo-hk.github.io
   →  myo-makeyourown.pages.dev
```

- [ ] **Step 2: Batch update all presentation script.md and outline.md files**

```bash
find presentations -name 'script.md' -o -name 'outline.md' | xargs sed -i '' 's|myo-hk\.github\.io|myo-makeyourown.pages.dev|g'
```

- [ ] **Step 3: Verify no old URL remains in presentations**

```bash
grep -r 'myo-hk.github.io' presentations/ --include='*.md' --include='*.tsx' --include='*.ts'
```
Expected: no matches

---

### Task 9: Final verification sweep

- [ ] **Step 1: Full codebase scan for remaining myo-hk.github.io references**

```bash
grep -r 'myo-hk.github.io' . --include='*.html' --include='*.js' --include='*.ts' --include='*.tsx' --include='*.py' --include='*.md' --include='*.txt' --include='*.json' --exclude-dir='node_modules' --exclude-dir='.git' --exclude-dir='.opencode' --exclude-dir='docs/superpowers/plans'
```

Expected: no matches (except historical plan documents which are intentionally preserved)

- [ ] **Step 2: Verify sitemap is well-formed**

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml'); print('sitemap.xml: OK')"
python3 -c "import xml.etree.ElementTree as ET; ET.parse('blog/sitemap.xml'); print('blog/sitemap.xml: OK')"
```
Expected: both print OK

- [ ] **Step 3: Verify canonical URLs in root HTML files**

```bash
grep -h 'rel="canonical"' index.html v2.html poster.html heic-converter.html privacy.html terms.html
```
Expected: all show `https://myo-makeyourown.pages.dev/...`

- [ ] **Step 4: Verify live site access (optional, requires network)**

```bash
curl -sI https://myo-makeyourown.pages.dev/ | head -5
```
Expected: HTTP/2 200

---

## Self-Review

**1. Spec coverage:**
- Task 1-2: Sitemap generation + robots.txt — covers all infrastructure files
- Task 3: Root HTML pages — covers all 6 non-blog HTML files
- Task 4: Blog batch script — covers all ~421 blog articles
- Task 5: Sitemap regeneration — regenerates with new URLs
- Task 6: README/llms.txt/pricing.md — covers all documentation with embedded URLs
- Task 7: Presentation generator — covers the build tool that generates CTA components
- Task 8: Presentation files — covers 3 TSX CTA components + ~76 markdown files
- Task 9: Verification — covers full codebase sweep + spot-checks

**2. No placeholder scan:** All steps have concrete commands, exact before/after strings, verification commands with expected output. No TBDs, TODOs, or "implement later".

**3. Type consistency:** All references to old URL use the exact string `https://myo-hk.github.io` and new URL uses `https://myo-makeyourown.pages.dev` consistently across every task.

**Deliberately excluded (low priority):**
- `docs/superpowers/plans/` — historical plan documents, not served or executed
- `fix_canonical_report.json` — stale SEO audit report, should be deleted or ignored
- `js library/*.min.js` — vendor files, irrelevant
