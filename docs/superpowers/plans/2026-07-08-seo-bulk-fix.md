# SEO Bulk Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix all Critical and High-priority SEO issues identified in the 2026-07-08 audit across all 427 pages (6 root + 421 blog articles).

**Architecture:** The site is pure static HTML with no build step. Fixes are applied via Python batch scripts (reusing/fixing existing scripts in the repo) plus targeted single-file edits. All changes are backward-compatible HTML edits — no behavioral changes.

**Tech Stack:** Python 3 (for batch scripts), static HTML, `sed`/`awk` for light batch edits, manual edits for root pages.

**Prerequisite check:** All existing scripts in repo root (`fix_json_ld_and_table.py`, `fix_medium_issues.py`) have hardcoded paths (`/Users/babubu/...`). Before using, update the `BLOG_DIR` and `REPORT_FILE` constants to use `pathlib.Path.cwd()` relative paths instead.

---

## File Structure

### Files to Create
| File | Purpose |
|------|---------|
| `scripts/generate_sitemap.py` | Generates complete `sitemap.xml` and `blog/sitemap.xml` with ALL pages |
| `scripts/fix_blog_titles.py` | Batch-extends blog article `<title>` tags to 20-35 Chinese characters |

### Files to Modify
| File | Change |
|------|--------|
| `index.html` | Add `<meta name="description">`, expand `<title>`, add `<link rel="canonical">`, add `<meta name="robots">` |
| `v2.html` | Add `<meta name="description">`, expand `<title>`, add `<link rel="canonical">` pointing to `index.html`, add `<meta name="robots" content="noindex, follow">` |
| `poster.html` | Add `<meta name="description">` |
| `heic-converter.html` | Add `<meta name="description">`, `<meta name="robots">`, OG tags, canonical |
| `robots.txt` | Add second Sitemap line for `blog/sitemap.xml` |
| All 421 blog HTML files | Replace relative canonical URLs with absolute URLs, add `<meta name="robots">` where missing |
| `fix_json_ld_and_table.py` | Fix hardcoded paths, extend to handle remaining articles |
| `fix_medium_issues.py` | Fix hardcoded paths, ensure robots tag is added correctly |

### Files Not Touched
| File | Reason |
|------|--------|
| `privacy.html` | Already well-optimized |
| `terms.html` | Already well-optimized |
| `blog/index.html` | Already well-optimized (except canonical — minor) |
| `blog/sitemap.xml` | Will be regenerated entirely by `generate_sitemap.py` |
| `sitemap.xml` | Will be regenerated entirely by `generate_sitemap.py` |

---

## Task Breakdown

### Task 1: Fix Hardcoded Paths in Existing Scripts

**Files:**
- Modify: `fix_json_ld_and_table.py` (lines 12-13)
- Modify: `fix_medium_issues.py` (lines 14-15)
- Modify: `generate_sitemap.py` (new file — will be written with portable paths)

- [ ] **Step 1: Fix `fix_json_ld_and_table.py` paths**

Replace lines 12-13:
```python
# OLD
BLOG_DIR = Path("/Users/babubu/Documents/GitHub/myo-hk/blog")
REPORT_FILE = Path("/Users/babubu/Documents/GitHub/myo-hk/fix_report.json")

# NEW
import os
BLOG_DIR = Path(__file__).parent / "blog"
REPORT_FILE = Path(__file__).parent / "fix_report.json"
```

- [ ] **Step 2: Fix `fix_medium_issues.py` paths**

Replace lines 14-15 the same way:
```python
# OLD
BLOG_DIR = Path("/Users/babubu/Documents/GitHub/myo-hk/blog")
REPORT_FILE = Path("/Users/babubu/Documents/GitHub/myo-hk/fix_medium_report.json")

# NEW
BLOG_DIR = Path(__file__).parent / "blog"
REPORT_FILE = Path(__file__).parent / "fix_medium_report.json"
```

- [ ] **Step 3: Verify scripts run without path errors**

Run: `python3 fix_medium_issues.py --test`
Run: `python3 fix_json_ld_and_table.py --test`
Expected: No file-not-found errors, scripts report their findings.

- [ ] **Step 4: Commit**

```bash
git add fix_json_ld_and_table.py fix_medium_issues.py
git commit -m "fix: update hardcoded paths in SEO scripts to use relative paths"
```

---

### Task 2: Fix Homepage SEO (`index.html`)

**Files:**
- Modify: `index.html` (lines 14-32)

- [ ] **Step 1: Add meta description, expanded title, canonical, and robots to `index.html`**

Current `<head>` section (lines 14-26):
```html
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My O!專屬證書套</title>
    <meta property="og:image" content="https://myo-hk.github.io/image/01_company_logo.png">
    <meta property="og:image:alt" content="My O! 證書套公司 Logo">
    <meta property="og:title" content="My O!專屬證書套">
    <meta property="og:description" content="為您的結婚證書打造設計師級專屬證書套，讓這份愛情的見證永恆閃耀。">
    <meta property="og:url" content="https://myo-hk.github.io">
    <meta property="og:type" content="website">
    
    <link rel="icon" href="image/01_company_logo.png" type="image/png">
    <link rel="shortcut icon" href="image/01_company_logo.png" type="image/png">
```

Replace with:
```html
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My O! 專屬結婚證書套：設計師級證書套訂製 | 香港</title>
    <meta name="description" content="My O! 為您的結婚證書打造設計師級專屬證書套，採用熱轉印工藝印上新人名字與結婚日期。多款顏色材質可選，米色亞麻布與藍色磨砂珠光，讓愛情見證永恆閃耀。">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://myo-hk.github.io/">
    <meta property="og:image" content="https://myo-hk.github.io/image/01_company_logo.png">
    <meta property="og:image:alt" content="My O! 證書套公司 Logo">
    <meta property="og:title" content="My O! 專屬結婚證書套：設計師級證書套訂製 | 香港">
    <meta property="og:description" content="My O! 為您的結婚證書打造設計師級專屬證書套，採用熱轉印工藝印上新人名字與結婚日期。多款顏色材質可選，讓愛情見證永恆閃耀。">
    <meta property="og:url" content="https://myo-hk.github.io">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="My O! 專屬結婚證書套">
    <meta property="og:locale" content="zh_HK">
    
    <link rel="icon" href="image/01_company_logo.png" type="image/png">
    <link rel="shortcut icon" href="image/01_company_logo.png" type="image/png">
```

- [ ] **Step 2: Verify no HTML syntax errors**

Run: `python3 -c "import html.parser; p=html.parser.HTMLParser(); p.feed(open('index.html').read()); print('OK')"`
Expected: Prints "OK"

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "fix: add meta description, expanded title, canonical, and robots to homepage"
```

---

### Task 3: De-prioritize `v2.html` (Redesigned Homepage)

**Files:**
- Modify: `v2.html` (lines 14-26)

- [ ] **Step 1: Set v2.html as noindex with canonical pointing to index.html**

Current `<head>`:
```html
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My O!專屬證書套</title>
    <meta property="og:image" content="https://myo-hk.github.io/image/01_company_logo.png">
    <meta property="og:image:alt" content="My O! 證書套公司 Logo">
    <meta property="og:title" content="My O!專屬證書套">
    <meta property="og:description" content="為您的結婚證書打造設計師級專屬證書套，讓這份愛情的見證永恆閃耀。">
    <meta property="og:url" content="https://myo-hk.github.io">
    <meta property="og:type" content="website">
```

Replace with:
```html
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My O! 專屬結婚證書套：設計師級證書套訂製 | 香港</title>
    <meta name="description" content="My O! 為您的結婚證書打造設計師級專屬證書套，採用熱轉印工藝印上新人名字與結婚日期。多款顏色材質可選，讓愛情見證永恆閃耀。">
    <meta name="robots" content="noindex, follow">
    <link rel="canonical" href="https://myo-hk.github.io/">
    <meta property="og:image" content="https://myo-hk.github.io/image/01_company_logo.png">
    <meta property="og:image:alt" content="My O! 證書套公司 Logo">
    <meta property="og:title" content="My O! 專屬結婚證書套：設計師級證書套訂製 | 香港">
    <meta property="og:description" content="My O! 為您的結婚證書打造設計師級專屬證書套，採用熱轉印工藝印上新人名字與結婚日期。多款顏色材質可選，讓愛情見證永恆閃耀。">
    <meta property="og:url" content="https://myo-hk.github.io">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="My O! 專屬結婚證書套">
    <meta property="og:locale" content="zh_HK">
```

- [ ] **Step 2: Commit**

```bash
git add v2.html
git commit -m "fix: set v2.html to noindex with canonical to index.html to resolve duplicate content"
```

---

### Task 4: Fix `poster.html` and `heic-converter.html` Meta

**Files:**
- Modify: `poster.html` (add meta description after line 18)
- Modify: `heic-converter.html` (add full SEO meta tags after line 16)

- [ ] **Step 1: Add meta description to `poster.html`**

After line 17 (`<meta name="robots" content="index, follow">`), insert:
```html
    <meta name="description" content="My O! 結婚證書套宣傳單張 — A5 尺寸可列印 PDF，展示米色亞麻布與藍色磨砂珠光證書套，五款設計風格與 QR Code 連結。">
    <link rel="canonical" href="https://myo-hk.github.io/poster.html">
```

- [ ] **Step 2: Add full SEO meta tags to `heic-converter.html`**

After line 16 (`<title id="pageTitle">HEIC/HEIF 轉圖片工具</title>`), insert:
```html
    <meta name="description" content="免費線上 HEIC/HEIF 轉 PNG/JPG 工具，支援批量轉換與 ZIP 打包下載。無需上傳伺服器，所有轉換在瀏覽器端完成，保障隱私。">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://myo-hk.github.io/heic-converter.html">
    <meta property="og:type" content="website">
    <meta property="og:title" content="HEIC/HEIF 轉圖片工具 — 免費線上批量轉換">
    <meta property="og:description" content="免費線上 HEIC/HEIF 轉 PNG/JPG，支援批量轉換與 ZIP 打包下載。所有轉換在瀏覽器端完成，保障隱私。">
    <meta property="og:image" content="https://myo-hk.github.io/image/01_company_logo.png">
    <meta property="og:url" content="https://myo-hk.github.io/heic-converter.html">
    <meta property="og:site_name" content="My O! 專屬結婚證書套">
    <meta property="og:locale" content="zh_HK">
    <meta name="twitter:card" content="summary_large_image">
```

Also add after the `</style>` tag (before `</head>`):
```html
    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"WebApplication","name":"HEIC/HEIF 轉圖片工具","description":"免費線上 HEIC/HEIF 轉 PNG/JPG 工具，支援批量轉換與 ZIP 打包下載。","url":"https://myo-hk.github.io/heic-converter.html","operatingSystem":"All","browserRequirements":"Requires JavaScript"}
    </script>
```

- [ ] **Step 3: Commit**

```bash
git add poster.html heic-converter.html
git commit -m "fix: add SEO meta tags to poster.html and heic-converter.html"
```

---

### Task 5: Batch Fix Blog Article Canonical URLs to Absolute

**Files:**
- Modify: All 421 blog article `.html` files

- [ ] **Step 1: Write the batch fix script**

Create `scripts/fix_canonical_urls.py`:
```python
#!/usr/bin/env python3
"""
Batch fix: Replace relative canonical URLs with absolute URLs in blog articles.
Usage: python3 scripts/fix_canonical_urls.py [--test]

Changes: <link rel="canonical" href="文件名.html"> 
      → <link rel="canonical" href="https://myo-hk.github.io/blog/文件名.html">
"""

import re
import json
import glob
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"
REPORT_FILE = Path(__file__).parent.parent / "fix_canonical_report.json"

CANONICAL_PATTERN = re.compile(
    r'(<link\s+rel="canonical"\s+href=")([^"]+\.html)(">.*?-->\s*)?'
)

def fix_canonical(html, filename):
    """Replace relative canonical URL with absolute URL."""
    changes = []
    
    def replace_relative(match):
        prefix = match.group(1)
        url = match.group(2)
        suffix = match.group(3) or ">"
        
        # Skip if already absolute
        if url.startswith("http"):
            return match.group(0)
        
        # Skip if already has full path
        if url.startswith("/blog/") or url.startswith("https://"):
            return match.group(0)
        
        absolute = f'{prefix}https://myo-hk.github.io/blog/{url}{suffix}'
        changes.append({"from": url, "to": f"https://myo-hk.github.io/blog/{url}"})
        return absolute
    
    html = CANONICAL_PATTERN.sub(replace_relative, html)
    return html, changes

def main():
    test_mode = "--test" in __import__("sys").argv
    files = sorted(BLOG_DIR.glob("*.html"))
    total_changes = 0
    all_changes = []
    
    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        
        if 'rel="canonical"' not in content:
            continue
        
        before = content
        content, changes = fix_canonical(content, fpath.name)
        
        if changes:
            total_changes += len(changes)
            all_changes.append({"file": str(fpath.name), "changes": changes})
            
            if not test_mode:
                fpath.write_text(content, encoding="utf-8")
                print(f"  ✓ {fpath.name}: {len(changes)} canonical(s) fixed")
    
    report = {
        "files_processed": len(files),
        "files_changed": len(all_changes),
        "total_changes": total_changes,
        "test_mode": test_mode,
        "details": all_changes
    }
    
    REPORT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"\nReport saved to {REPORT_FILE}")
    print(f"Files processed: {len(files)}")
    print(f"Files changed: {len(all_changes)}")
    print(f"Total canonical URLs fixed: {total_changes}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run in test mode to preview changes**

Run: `python3 scripts/fix_canonical_urls.py --test`
Expected: Prints report showing which files would be changed. Verify the canonical patterns look correct.

- [ ] **Step 3: Run to apply changes**

Run: `python3 scripts/fix_canonical_urls.py`
Expected: All blog articles with relative canonical URLs are updated to absolute. Report saved to `fix_canonical_report.json`.

- [ ] **Step 4: Verify a sample**

Run:
```bash
grep 'rel="canonical"' "blog/香港結婚完整攻略.html"
```
Expected: `href="https://myo-hk.github.io/blog/香港結婚完整攻略.html"` (absolute URL)

- [ ] **Step 5: Commit**

```bash
git add scripts/fix_canonical_urls.py fix_canonical_report.json
git commit -m "fix: batch replace relative canonical URLs with absolute URLs across all blog articles"
```

---

### Task 6: Batch Add Meta Robots to Blog Articles

**Files:**
- Modify: `fix_medium_issues.py` (already has robots tag logic — ensure it works)
- Modify: All 421 blog article `.html` files (via script)

- [ ] **Step 1: Fix `fix_medium_issues.py` and run it**

First verify the robots insertion logic works. The existing code at lines 31-37:
```python
    if 'name="robots"' not in html.lower():
        html = re.sub(
            r'</head>',
            '<meta name="robots" content="index, follow">\n</head>',
            html,
            flags=re.IGNORECASE
        )
```

This logic is correct. Run it:
```bash
python3 fix_medium_issues.py
```

Expected: 416+ blog articles get `<meta name="robots" content="index, follow">` added before `</head>`.

- [ ] **Step 2: Verify robots tags were added**

Run:
```bash
grep -c 'meta name="robots"' blog/*.html | grep ':0$' | wc -l
```
Expected: `0` (all files have robots tags now, except intentionally excluded ones)

- [ ] **Step 3: Commit**

```bash
git add fix_medium_issues.py fix_medium_report.json
git commit -m "fix: add meta robots tags to all blog articles via batch script"
```

---

### Task 7: Batch Add Remaining JSON-LD to Blog Articles

**Files:**
- Modify: `fix_json_ld_and_table.py` (fix paths, then run)
- Modify: ~130 blog article `.html` files (via script)

- [ ] **Step 1: Fix `fix_json_ld_and_table.py` paths** (already done in Task 1 if sequential)

- [ ] **Step 2: Run the JSON-LD fix script to add Article schema to remaining articles**

Run: `python3 fix_json_ld_and_table.py`
Expected: ~130 articles missing JSON-LD get Article schema added. Merge any duplicate FAQPage blocks.

- [ ] **Step 3: Verify JSON-LD coverage**

Run:
```bash
grep -c 'application/ld+json' blog/*.html | awk -F: '{s+=$2} END {print s " out of " NR " files have JSON-LD"}'
```
Expected: 420+ files with JSON-LD.

- [ ] **Step 4: Commit**

```bash
git add fix_json_ld_and_table.py fix_report.json
git commit -m "fix: add Article JSON-LD schema to remaining blog articles via batch script"
```

---

### Task 8: Update `robots.txt` to Reference Blog Sitemap

**Files:**
- Modify: `robots.txt`

- [ ] **Step 1: Add blog sitemap reference**

Current `robots.txt`:
```
User-agent: *
Allow: /

Sitemap: https://myo-hk.github.io/sitemap.xml
```

Replace with:
```
User-agent: *
Allow: /

Sitemap: https://myo-hk.github.io/sitemap.xml
Sitemap: https://myo-hk.github.io/blog/sitemap.xml
```

- [ ] **Step 2: Commit**

```bash
git add robots.txt
git commit -m "fix: add blog/sitemap.xml reference to robots.txt"
```

---

### Task 9: Generate Complete Sitemaps

**Files:**
- Create: `scripts/generate_sitemap.py`
- Regenerate: `sitemap.xml`
- Regenerate: `blog/sitemap.xml`

- [ ] **Step 1: Write the sitemap generation script**

Create `scripts/generate_sitemap.py`:
```python
#!/usr/bin/env python3
"""
Generate complete sitemap.xml and blog/sitemap.xml for myo-hk.
Discovers ALL HTML files and includes them.
Usage: python3 scripts/generate_sitemap.py
"""

from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape
import re

ROOT = Path(__file__).parent.parent
BLOG = ROOT / "blog"
NOW = datetime.now().strftime("%Y-%m-%d")

# Pages that are not blog articles and should be in root sitemap
ROOT_PAGES = {
    "index.html":       {"priority": "1.0", "changefreq": "weekly"},
    "v2.html":          {"priority": "0.5", "changefreq": "monthly"},
    "poster.html":      {"priority": "0.5", "changefreq": "monthly"},
    "heic-converter.html": {"priority": "0.5", "changefreq": "monthly"},
    "privacy.html":     {"priority": "0.3", "changefreq": "yearly"},
    "terms.html":       {"priority": "0.3", "changefreq": "yearly"},
}

def add_url(urlset, loc, lastmod, changefreq, priority):
    urlset.append(f"""  <url>
    <loc>{escape(loc)}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

def generate_root_sitemap():
    """Generate sitemap.xml for root-level pages."""
    urls = []
    
    for filename, meta in ROOT_PAGES.items():
        loc = f"https://myo-hk.github.io/{filename}" if filename != "index.html" else "https://myo-hk.github.io/"
        add_url(urls, loc, NOW, meta["changefreq"], meta["priority"])
    
    # Add blog index
    add_url(urls, "https://myo-hk.github.io/blog/", NOW, "weekly", "0.8")
    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"Root sitemap: {len(urls)} URLs → sitemap.xml")

def generate_blog_sitemap():
    """Generate blog/sitemap.xml with ALL blog articles."""
    urls = []
    html_files = sorted(BLOG.glob("*.html"))
    
    for fpath in html_files:
        if fpath.name == "index.html":
            continue
        
        # Try to extract date from published_time meta
        content = fpath.read_text(encoding="utf-8", errors="ignore")
        date_match = re.search(r'<meta\s+property="article:published_time"\s+content="(\d{4}-\d{2}-\d{2})', content)
        lastmod = date_match.group(1) if date_match else NOW
        
        filename = fpath.name
        loc = f"https://myo-hk.github.io/blog/{escape(filename)}"
        add_url(urls, loc, lastmod, "monthly", "0.7")
    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""
    (BLOG / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"Blog sitemap: {len(urls)} URLs → blog/sitemap.xml")

if __name__ == "__main__":
    generate_root_sitemap()
    generate_blog_sitemap()
    print("Done. Verify with: wget -qO- https://myo-hk.github.io/sitemap.xml | head -5")
```

- [ ] **Step 2: Run sitemap generation**

Run: `python3 scripts/generate_sitemap.py`
Expected:
```
Root sitemap: 7 URLs → sitemap.xml
Blog sitemap: 420 URLs → blog/sitemap.xml
Done.
```

- [ ] **Step 3: Verify sitemap coverage**

Run:
```bash
echo "Root sitemap:" && grep -o '<loc>' sitemap.xml | wc -l
echo "Blog sitemap:" && grep -o '<loc>' blog/sitemap.xml | wc -l
echo "Blog articles:" && ls blog/*.html | wc -l
```
Expected: Root sitemap count should match ROOT_PAGES + 1 (blog index). Blog sitemap should equal `ls blog/*.html | wc -l` minus 1 (exclude index.html).

- [ ] **Step 4: Commit**

```bash
git add scripts/generate_sitemap.py sitemap.xml blog/sitemap.xml
git commit -m "fix: regenerate complete sitemaps covering all 420+ blog articles and root pages"
```

---

### Task 10: Add BreadcrumbList Schema to Blog Articles

**Files:**
- Create: `scripts/add_breadcrumb_schema.py`
- Modify: All 421 blog article `.html` files (via script)

- [ ] **Step 1: Write the BreadcrumbList schema script**

Create `scripts/add_breadcrumb_schema.py`:
```python
#!/usr/bin/env python3
"""
Add BreadcrumbList JSON-LD schema to blog articles.
Inserts the schema before </head> only if one doesn't already exist.
Usage: python3 scripts/add_breadcrumb_schema.py [--test]
"""

import json
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

BREADCRUMB_SCHEMA = """    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首頁","item":"https://myo-hk.github.io/"},{"@type":"ListItem","position":2,"name":"教學指南","item":"https://myo-hk.github.io/blog/"},{"@type":"ListItem","position":3,"name":"%TITLE%","item":"https://myo-hk.github.io/blog/%FILENAME%"},"itemListElement":[{"@type":"ListItem","position":1,"name":"首頁","item":"https://myo-hk.github.io/"},{"@type":"ListItem","position":2,"name":"教學指南","item":"https://myo-hk.github.io/blog/"},{"@type":"ListItem","position":3,"name":"%TITLE%","item":"https://myo-hk.github.io/blog/%FILENAME%"}]}
    </script>"""

def extract_title(html):
    """Extract the page title from <title> tag."""
    import re
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    return m.group(1).strip() if m else "文章"

def has_breadcrumb(html):
    """Check if BreadcrumbList schema already exists."""
    return '"BreadcrumbList"' in html

def main():
    test_mode = "--test" in __import__("sys").argv
    files = sorted(BLOG_DIR.glob("*.html"))
    changed = 0
    skipped_exists = 0
    skipped_non_article = 0
    
    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        
        # Skip blog index page
        if fpath.name == "index.html":
            skipped_non_article += 1
            continue
        
        if has_breadcrumb(content):
            skipped_exists += 1
            continue
        
        title = extract_title(content)
        filename = fpath.name
        
        schema = BREADCRUMB_SCHEMA.replace("%TITLE%", title).replace("%FILENAME%", filename)
        content = content.replace("</head>", schema + "\n</head>")
        
        if not test_mode:
            fpath.write_text(content, encoding="utf-8")
        
        changed += 1
    
    print(f"Files processed: {len(files)}")
    print(f"Breadcrumb added: {changed}")
    print(f"Skipped (already exists): {skipped_exists}")
    print(f"Skipped (index.html): {skipped_non_article}")
    print(f"Test mode: {test_mode}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run in test mode**

Run: `python3 scripts/add_breadcrumb_schema.py --test`
Expected: Shows how many files would be modified.

- [ ] **Step 3: Apply changes**

Run: `python3 scripts/add_breadcrumb_schema.py`
Expected: ~420 blog articles get BreadcrumbList schema.

- [ ] **Step 4: Verify**

Run:
```bash
grep -c 'BreadcrumbList' blog/*.html | awk -F: '{s+=$2} END {print s " breadcrumb schemas added"}'
```
Expected: 420 entries.

- [ ] **Step 5: Commit**

```bash
git add scripts/add_breadcrumb_schema.py
git commit -m "feat: add BreadcrumbList JSON-LD schema to all blog articles"
```

---

### Task 11: Fix Blog Index Hardcoded Canonical URL

**Files:**
- Modify: `blog/index.html` (line 19)

- [ ] **Step 1: Update canonical URL to be dynamic**

Line 19:
```html
    <link rel="canonical" href="https://myo-hk.github.io/blog/index.html">
```

Replace with dynamic JS (like other pages do):
```html
    <link rel="canonical" href="https://myo-hk.github.io/blog/">
```

(Since the blog index is always served at `/blog/`, no dynamic JS needed — the path never changes.)

- [ ] **Step 2: Commit**

```bash
git add blog/index.html
git commit -m "fix: use canonical URL without index.html for blog index page"
```

---

### Task 12: Preconnect Hints for Third-Party CDNs

**Files:**
- Modify: `index.html` (after line 26)
- Modify: All blog article templates via batch (or add to fix script)

- [ ] **Step 1: Add preconnect hints to root pages**

In `index.html`, after the canonical link (or before `</head>`), add:
```html
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
    <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">
```

- [ ] **Step 2: Add preconnect hints to blog index**

Same block in `blog/index.html` before `</head>`.

- [ ] **Step 3: Commit**

```bash
git add index.html blog/index.html
git commit -m "perf: add preconnect and dns-prefetch hints for third-party CDNs"
```

---

### Task 13: Batch Extend Blog Article Titles

**Files:**
- Create: `scripts/fix_blog_titles.py`
- Modify: All 421 blog article `.html` files (via script)

- [ ] **Step 1: Write the title extension script**

Create `scripts/fix_blog_titles.py`:
```python
#!/usr/bin/env python3
"""
Extend short blog article <title> tags to be more SEO-friendly.
Target length: 20-35 Chinese characters (equivalent to 50-60 English chars for SEO).
Titles that are already >= 20 Chinese chars are left unchanged.
Usage: python3 scripts/fix_blog_titles.py [--test]

Mapping: for short titles, appends a descriptive suffix.
"""

import re
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

# Mapping of known short titles → extended versions
TITLE_EXTENSIONS = {
    "2026 香港結婚完整攻略": "2026香港結婚完整攻略：註冊流程、婚宴籌備與習俗全指南",
    "2026 婚禮攝影價錢比較": "2026婚禮攝影價錢比較：10間人氣攝影師套餐與收費標準",
    "婚禮場地選擇指南：完美場地秘訣": "婚禮場地選擇指南：酒店酒樓教堂戶外場地完整比較秘訣",
    "回門習俗介紹：傳統與現代做法": "回門習俗完整指南：傳統三朝回門日期禮品與現代簡化做法",
    "婚後生活適應指南：從單身到已婚": "婚後生活適應指南：溝通家務財務與長輩相處的新婚秘訣",
    "婚禮攝影價錢比較": "婚禮攝影價錢比較：香港最新收費標準與套餐選擇攻略",
}

def count_chinese_chars(title):
    """Count Chinese character count in a string."""
    return len(re.findall(r'[\u4e00-\u9fff]', title))

def extend_title(match):
    current_title = match.group(1)
    
    # If title already long enough (>= 20 Chinese chars), skip
    if count_chinese_chars(current_title) >= 20:
        return match.group(0)
    
    # Check mapping
    if current_title in TITLE_EXTENSIONS:
        new_title = TITLE_EXTENSIONS[current_title]
        return f'<title>{new_title}</title>'
    
    # For titles not in mapping, attempt heuristic: add "香港" / "完整指南"
    # Only apply to titles that end with key categories
    heuristic_suffixes = {
        "指南": "：香港結婚必讀完整攻略",
        "比較": "：香港結婚必讀完整攻略",
        "推薦": "：香港結婚必讀完整攻略",
        "介紹": "：傳統習俗與現代做法全攻略",
        "教學": "：香港結婚必讀完整攻略",
        "選擇": "：香港結婚必讀完整攻略",
        "清單": "：香港結婚必讀完整攻略",
        "貼士": "：香港結婚必讀完整攻略",
        "規劃": "：香港結婚必讀完整攻略",
        "創意": "：香港結婚必讀完整攻略",
    }
    
    for suffix, extension in heuristic_suffixes.items():
        if current_title.endswith(suffix):
            new_title = current_title + extension
            # Don't exceed 50 chars total
            if len(new_title) > 50:
                continue
            return f'<title>{new_title}</title>'
    
    return match.group(0)

def main():
    test_mode = "--test" in __import__("sys").argv
    files = sorted(BLOG_DIR.glob("*.html"))
    changed = 0
    skipped = 0
    
    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        
        title_pattern = re.compile(r'<title>(.*?)</title>')
        match = title_pattern.search(content)
        
        if not match:
            skipped += 1
            continue
        
        title = match.group(1)
        chinese_count = count_chinese_chars(title)
        
        # Only extend if short
        if chinese_count >= 20:
            skipped += 1
            continue
        
        new_content = title_pattern.sub(extend_title, content)
        
        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            new_match = title_pattern.search(new_content)
            new_title = new_match.group(1) if new_match else "???"
            print(f"  {'✓' if not test_mode else '○'} {fpath.name}: \"{title}\" ({chinese_count} chars) → \"{new_title}\" ({count_chinese_chars(new_title)} chars)")
            changed += 1
        else:
            skipped += 1
    
    print(f"\nTotal: {changed} extended, {skipped} skipped (already long or no match)")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run in test mode**

Run: `python3 scripts/fix_blog_titles.py --test`
Expected: Shows which titles would be extended and what the new titles would look like.

- [ ] **Step 3: Run to apply changes**

Run: `python3 scripts/fix_blog_titles.py`
Expected: Short article titles extended to 20+ Chinese characters.

- [ ] **Step 4: Verify**

Run:
```bash
grep '<title>' blog/*.html | head -5
```
Expected: Titles appear longer and more descriptive.

- [ ] **Step 5: Commit**

```bash
git add scripts/fix_blog_titles.py
git commit -m "fix: extend short blog article titles for better SEO (20+ Chinese chars)"
```

---

## Execution Order

Tasks are grouped into **3 independent batches** that can be run in parallel:

**Batch A (No code dependencies between these):**
- Task 2: Fix homepage SEO
- Task 3: Fix v2.html
- Task 4: Fix poster.html / heic-converter.html
- Task 8: Update robots.txt
- Task 11: Fix blog index canonical

**Batch B (Depend on Task 1 being done first; independent of each other):**
- Task 5: Fix canonical URLs (via new script)
- Task 6: Add meta robots (via fixed existing script)
- Task 7: Add JSON-LD (via fixed existing script)
- Task 9: Generate sitemaps (via new script)
- Task 13: Extend blog titles (via new script)

**Batch C (Optional but recommended):**
- Task 10: Add BreadcrumbList schema
- Task 12: Preconnect hints

**Prerequisite:** Task 1 (fix script paths) must finish before Batch B starts.

---

## Self-Review Check

**1. Spec coverage:**
- ✅ Sitemap regeneration → Task 9
- ✅ Homepage meta description + title → Task 2
- ✅ Canonical URLs absolute → Task 5
- ✅ Meta robots tags → Task 6
- ✅ JSON-LD schema coverage → Task 7
- ✅ v2.html duplicate content → Task 3
- ✅ poster/heic converter SEO → Task 4
- ✅ robots.txt blog sitemap reference → Task 8
- ✅ Blog index canonical → Task 11
- ✅ Preconnect hints → Task 12
- ✅ BreadcrumbList schema → Task 10
- ✅ Blog title extension → Task 13
- ✅ Fix existing script paths → Task 1

**2. Placeholder scan:** ✅ No placeholders, TBDs, or vague steps. Every step has exact code or commands.

**3. Type consistency:** ✅ All scripts use consistent naming (`BLOG_DIR` pattern, same imports, same `--test` flag convention). Scripts are in `scripts/` directory. Report files use `.json` extension in repo root.
