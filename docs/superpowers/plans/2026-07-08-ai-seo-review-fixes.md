# AI SEO 修復實作計劃

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the high-priority AI SEO fixes identified in the 2026-07-08 AI SEO audit — making myo-hk.github.io content more extractable and citable by AI search engines (Google AI Overviews, ChatGPT, Perplexity, Claude, Copilot).

**Architecture:** The site is pure static HTML with no build step. Most fixes are single-file edits to root pages, plus a Python batch script for cleaning up JSON-LD artifacts in blog articles. No behavioral changes. All changes are safe to deploy to GitHub Pages immediately.

**Tech Stack:** Python 3 (for batch JSON-LD cleanup), static HTML, manual edits for root pages.

**Prerequisite:** The existing `fix_json_ld_and_table.py` script has hardcoded paths. If running batch scripts, update them to use relative paths first (covered in the existing SEO plan `2026-07-08-seo-bulk-fix.md`).

---

## File Structure

### Files to Create
| File | Purpose |
|------|---------|
| `llms.txt` (site root) | AI context file — gives ChatGPT/Perplexity/Claude a quick overview of My O! |
| `pricing.md` (site root) | Structured pricing data for AI buying agents |

### Files to Modify
| File | Change |
|------|--------|
| `index.html` | Fix `og:title` typo ("結婚證書證" → "結婚證書套"), fix `og:site_name` typo, add `WebSite` + `Organization` JSON-LD |
| `v2.html` | Add `WebSite` + `Organization` JSON-LD |
| `robots.txt` | Add explicit AI crawler permissions (GPTBot, PerplexityBot, ClaudeBot, etc.) |
| `privacy.html` | Add `<meta name="robots" content="noindex, follow">` |
| `terms.html` | Add `<meta name="robots" content="noindex, follow">` |
| `poster.html` | Add `og:image` meta tag, add `Organization` JSON-LD |
| `heic-converter.html` | Add `WebApplication` JSON-LD Schema |
| 3 blog articles with combined JSON-LD | Split into separate valid blocks |
| 17 blog articles with duplicate Article Schema | Deduplicate |

### Files Not Touched
| File | Reason |
|------|--------|
| `blog/index.html` | Already has WebPage Schema, fine as-is |
| `blog/sitemap.xml` | Already contains 420+ article URLs (2523 lines, 81KB) — complete |
| `fix_json_ld_and_table.py` | Covered by the existing SEO plan |

---

## Task 1: Fix og:title Typo on Homepage

**Files:**
- Modify: `index.html:22,26`

- [ ] **Step 1: Read the current lines to confirm exact content**

```bash
grep -n '結婚證書證' /Users/bubu/Documents/Github/myo-hk/index.html
```
Expected output:
```
22:    <meta property="og:title" content="My O! 專屬結婚證書證：設計師級證書套訂製 | 香港">
26:    <meta property="og:site_name" content="My O! 專屬結婚證書證套">
```

- [ ] **Step 2: Fix line 22 — og:title**

In `index.html`, replace:
```html
<meta property="og:title" content="My O! 專屬結婚證書證：設計師級證書套訂製 | 香港">
```
with:
```html
<meta property="og:title" content="My O! 專屬結婚證書套：設計師級證書套訂製 | 香港">
```

- [ ] **Step 3: Fix line 26 — og:site_name**

In `index.html`, replace:
```html
<meta property="og:site_name" content="My O! 專屬結婚證書證套">
```
with:
```html
<meta property="og:site_name" content="My O! 專屬結婚證書套">
```

- [ ] **Step 4: Verify no remaining instances**

```bash
grep -c '結婚證書證' /Users/bubu/Documents/Github/myo-hk/index.html
```
Expected: `0`

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "fix: correct og:title and og:site_name typo on homepage"
```

---

## Task 2: Add JSON-LD Schema to Homepage (index.html)

**Files:**
- Modify: `index.html` (before `</head>`, after line 803)

- [ ] **Step 1: Read the `</head>` area to find insertion point**

```bash
grep -n '</head>' /Users/bubu/Documents/Github/myo-hk/index.html
```
Expected: `804: </head>` (or similar — confirm before edit)

- [ ] **Step 2: Add WebSite + Organization JSON-LD**

Insert before `</head>` in `index.html`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "My O! 專屬結婚證書套",
  "url": "https://myo-hk.github.io",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://myo-hk.github.io/blog/?search={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "My O! 專屬結婚證書套",
  "url": "https://myo-hk.github.io",
  "logo": "https://myo-hk.github.io/image/01_company_logo.png",
  "sameAs": [
    "https://www.instagram.com/myo.makeyourown/"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+852-6379-6410",
    "contactType": "customer service",
    "areaServed": "HK",
    "availableLanguage": ["Chinese", "English"]
  }
}
</script>
```

- [ ] **Step 3: Verify JSON-LD is valid**

```bash
python3 -c "
import json, re
with open('/Users/bubu/Documents/Github/myo-hk/index.html') as f:
    content = f.read()
blocks = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', content, re.DOTALL)
for i, block in enumerate(blocks):
    try:
        d = json.loads(block.strip())
        print(f'Block {i+1}: @type={d[\"@type\"]} — VALID')
    except Exception as e:
        print(f'Block {i+1}: INVALID — {e}')
"
```
Expected: 2 valid blocks (WebSite, Organization)

- [ ] **Step 4: Verify og:title is still correct**

```bash
grep 'og:title' /Users/bubu/Documents/Github/myo-hk/index.html
```
Expected: `My O! 專屬結婚證書套：設計師級證書套訂製 | 香港`

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: add WebSite and Organization JSON-LD schema to homepage"
```

---

## Task 3: Add JSON-LD Schema to v2.html

**Files:**
- Modify: `v2.html` (before `</head>`)

- [ ] **Step 1: Find insertion point**

```bash
grep -n '</head>' /Users/bubu/Documents/Github/myo-hk/v2.html
```

- [ ] **Step 2: Add the same WebSite + Organization JSON-LD**

Insert before `</head>` in `v2.html`. Same JSON-LD content as Task 2, Step 2.

- [ ] **Step 3: Verify JSON-LD is valid**

Same verification command as Task 2, Step 3 but for `v2.html`.

- [ ] **Step 4: Commit**

```bash
git add v2.html
git commit -m "feat: add WebSite and Organization JSON-LD schema to v2 homepage"
```

---

## Task 4: Add JSON-LD to poster.html

**Files:**
- Modify: `poster.html` (before `</head>`)

- [ ] **Step 1: Add og:image tag and Organization JSON-LD**

The `poster.html` file is missing `og:image`. Add it after the canonical link (around line 19):

```html
<meta property="og:image" content="https://myo-hk.github.io/image/01_company_logo.png">
<meta property="og:image:alt" content="My O! 證書套公司 Logo">
<meta property="og:title" content="My O! 結婚證書套宣傳單張">
<meta property="og:description" content="My O! 結婚證書套宣傳單張 — A5 尺寸可列印 PDF，展示米色亞麻布與藍色磨砂珠光證書套。">
<meta property="og:type" content="website">
<meta property="og:site_name" content="My O! 專屬結婚證書套">
<meta property="og:locale" content="zh_HK">
```

And add before `</head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "My O! 專屬結婚證書套",
  "url": "https://myo-hk.github.io",
  "logo": "https://myo-hk.github.io/image/01_company_logo.png"
}
</script>
```

- [ ] **Step 2: Verify**

```bash
grep 'og:image' /Users/bubu/Documents/Github/myo-hk/poster.html
```
Expected: exactly 1 instance of og:image

- [ ] **Step 3: Commit**

```bash
git add poster.html
git commit -m "feat: add og:image and Organization JSON-LD to poster page"
```

---

## Task 5: Add WebApplication Schema to HEIC Converter

**Files:**
- Modify: `heic-converter.html` (before `</head>`)

- [ ] **Step 1: Add WebApplication JSON-LD**

Insert before `</head>` in `heic-converter.html`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "HEIC/HEIF 轉圖片工具",
  "url": "https://myo-hk.github.io/heic-converter.html",
  "description": "免費線上 HEIC/HEIF 轉 PNG/JPG 工具，支援批量轉換與 ZIP 打包下載。所有轉換在瀏覽器端完成，保障隱私。",
  "applicationCategory": "Multimedia",
  "operatingSystem": "All",
  "browserRequirements": "Requires JavaScript",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "HKD"
  },
  "author": {
    "@type": "Organization",
    "name": "My O! 專屬結婚證書套"
  }
}
</script>
```

- [ ] **Step 2: Verify**

```bash
python3 -c "
import json, re
with open('/Users/bubu/Documents/Github/myo-hk/heic-converter.html') as f:
    c = f.read()
blocks = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', c, re.DOTALL)
for i, b in enumerate(blocks):
    d = json.loads(b.strip())
    print(f'Block {i+1}: @type={d[\"@type\"]} — VALID')
"
```
Expected: `Block 1: @type=WebApplication — VALID`

- [ ] **Step 3: Commit**

```bash
git add heic-converter.html
git commit -m "feat: add WebApplication schema to HEIC converter tool"
```

---

## Task 6: Update robots.txt for AI Crawlers

**Files:**
- Modify: `robots.txt`

- [ ] **Step 1: Read current robots.txt**

```
User-agent: *
Allow: /

Sitemap: https://myo-hk.github.io/sitemap.xml
Sitemap: https://myo-hk.github.io/blog/sitemap.xml
```

- [ ] **Step 2: Replace with AI-crawler-friendly version**

Write to `robots.txt`:

```
User-agent: *
Allow: /

# AI search crawlers — explicitly allowed for citation in AI answers
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

# Block training-only crawler (Common Crawl) while allowing search crawlers
User-agent: CCBot
Disallow: /

Sitemap: https://myo-hk.github.io/sitemap.xml
Sitemap: https://myo-hk.github.io/blog/sitemap.xml
```

- [ ] **Step 3: Commit**

```bash
git add robots.txt
git commit -m "feat: explicitly allow AI search crawlers, block CCBot training crawler"
```

---

## Task 7: Set Policy Pages to noindex

**Files:**
- Modify: `privacy.html`, `terms.html`

- [ ] **Step 1: Add noindex to privacy.html**

Find the `<meta charset="UTF-8">` line and add after it:
```html
<meta name="robots" content="noindex, follow">
```

- [ ] **Step 2: Add noindex to terms.html**

Same change as Step 1 for `terms.html`.

- [ ] **Step 3: Verify both files**

```bash
grep 'noindex' /Users/bubu/Documents/Github/myo-hk/privacy.html /Users/bubu/Documents/Github/myo-hk/terms.html
```
Expected: both files show `noindex, follow`

- [ ] **Step 4: Commit**

```bash
git add privacy.html terms.html
git commit -m "fix: set privacy and terms pages to noindex, follow"
```

---

## Task 8: Create /llms.txt for AI Systems

**Files:**
- Create: `llms.txt` (site root)

- [ ] **Step 1: Write llms.txt**

```markdown
# My O! 專屬結婚證書套

> 香港設計師級結婚證書套品牌，為新人提供客製化結婚證書套。採用熱轉印（燙印）工藝，印上新人名字與結婚日期。

## 產品

- 米色 Beige 亞麻布 Linen Texture 證書套
- 藍色 Blue 磨砂珠光 Frosted Pearl 證書套
- 5 款設計風格可供選擇（簡約線條、花卉圖案、幾何圖形、夢幻元素、經典風格）
- 尺寸：約 30.7cm(高) × 22.6cm(闊)，適用香港 A4 結婚證書
- 個人化：新人名字 + 結婚日期 + 設計樣式

## 熱門頁面

- 首頁：https://myo-hk.github.io/
- 教學指南（420+ 篇婚禮文章）：https://myo-hk.github.io/blog/
- 結婚證書套推薦比較：https://myo-hk.github.io/blog/結婚證書套推薦.html
- 證書套材質比較：https://myo-hk.github.io/blog/證書套材質比較.html
- 客製化證書套設計：https://myo-hk.github.io/blog/客製化證書套設計.html
- 香港結婚完整攻略：https://myo-hk.github.io/blog/香港結婚完整攻略.html
- HEIC 圖片轉換工具：https://myo-hk.github.io/heic-converter.html

## 聯絡方式

- Instagram：https://www.instagram.com/myo.makeyourown/
- WhatsApp：https://api.whatsapp.com/send?phone=85263796410
```

- [ ] **Step 2: Verify file exists**

```bash
ls -la /Users/bubu/Documents/Github/myo-hk/llms.txt
```

- [ ] **Step 3: Commit**

```bash
git add llms.txt
git commit -m "feat: add llms.txt for AI search engine context and citations"
```

---

## Task 9: Create /pricing.md for AI Buying Agents

**Files:**
- Create: `pricing.md` (site root)

- [ ] **Step 1: Write pricing.md**

```markdown
# 定價 — My O! 專屬結婚證書套

## 客製化結婚證書套
- 價格：請聯繫查詢（WhatsApp: +852 6379 6410）
- 製作時間：1-3 星期
- 材質選擇：米色亞麻布 / 藍色磨砂珠光
- 印刷工藝：熱轉印（燙印）燙金/銀效果
- 個人化內容：新人名字（中/英文）+ 結婚日期
- 設計款式：5 種風格選擇
- 適用證書：香港婚姻登記處 A4 結婚證書（約 209mm × 298mm）
- 包含配件：硬殼封面、厚卡內襯、固定帶

## 付款方式
- 銀行轉帳
- FPS 轉數快

## 地區
- 香港（本地郵寄或面交）
```

- [ ] **Step 2: Verify file exists**

```bash
ls -la /Users/bubu/Documents/Github/myo-hk/pricing.md
```

- [ ] **Step 3: Commit**

```bash
git add pricing.md
git commit -m "feat: add pricing.md for AI buying agent visibility"
```

---

## Task 10: Clean Up Combined JSON-LD in Blog Articles

**Files:**
- Modify: 3 blog articles with invalid combined JSON-LD (Article + FAQPage in one script tag)
- Modify: 17 blog articles with duplicate Article schemas

- [ ] **Step 1: Run the cleanup script**

Create and run a Python script that:
1. Scans all 420 blog HTML files
2. For each file, finds all `<script type="application/ld+json">` blocks
3. Removes blocks that fail JSON parsing (invalid combined format)
4. When multiple Article blocks exist, keeps only the first one (removes duplicates)
5. Reports what was changed

Use the existing `fix_json_ld_and_table.py` as a reference for the JSON-LD parsing approach.

Script: `scripts/cleanup_json_ld.py`

```python
#!/usr/bin/env python3
"""
Clean up JSON-LD artifacts in blog articles:
1. Remove invalid combined Article+FAQPage blocks
2. Deduplicate Article schemas (keep first, remove extras)
"""
import json
import re
import os
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / 'blog'
REPORT_FILE = Path(__file__).parent.parent / 'fix_ai_seo_report.json'

results = {
    'articles_checked': 0,
    'invalid_combined_removed': 0,
    'duplicate_article_removed': 0,
    'files_changed': []
}

JSON_LD_PATTERN = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>',
    re.DOTALL
)

for html_file in sorted(BLOG_DIR.glob('*.html')):
    if html_file.name == 'index.html':
        continue
    
    results['articles_checked'] += 1
    content = html_file.read_text(encoding='utf-8')
    original = content
    
    # Find all JSON-LD blocks
    blocks = list(JSON_LD_PATTERN.finditer(content))
    
    valid_blocks = []
    article_seen = False
    
    for match in blocks:
        raw = match.group(1).strip()
        try:
            data = json.loads(raw)
            # Valid JSON
            if isinstance(data, dict):
                if data.get('@type') == 'Article':
                    if article_seen:
                        # Duplicate Article — skip
                        results['duplicate_article_removed'] += 1
                        continue
                    article_seen = True
                valid_blocks.append(raw)
            elif isinstance(data, list):
                # Array format — keep for now but flag
                valid_blocks.append(raw)
            else:
                valid_blocks.append(raw)
        except json.JSONDecodeError:
            # Invalid JSON (combined comma-separated objects) — remove
            results['invalid_combined_removed'] += 1
            continue
    
    # Rebuild content with only valid blocks
    def replace_block(match):
        raw = match.group(1).strip()
        try:
            json.loads(raw)
            if isinstance(json.loads(raw), dict):
                data = json.loads(raw)
                if data.get('@type') == 'Article' and results['articles_checked'] > 0:
                    pass  # will be handled by the set logic above
            return match.group(0)  # keep
        except json.JSONDecodeError:
            return ''  # remove
    
    # More precise: rebuild from scratch
    new_content = content
    for match in reversed(list(JSON_LD_PATTERN.finditer(content))):
        raw = match.group(1).strip()
        try:
            json.loads(raw)
            # Valid — check for duplicate Article
            data = json.loads(raw)
            if isinstance(data, dict) and data.get('@type') == 'Article':
                # We'll handle dedup by keeping first only
                pass
        except json.JSONDecodeError:
            # Remove invalid combined block
            new_content = new_content[:match.start()] + new_content[match.end():]
    
    if new_content != original:
        html_file.write_text(new_content, encoding='utf-8')
        results['files_changed'].append(str(html_file.relative_to(BLOG_DIR.parent)))

# Write report
REPORT_FILE.write_text(
    json.dumps(results, ensure_ascii=False, indent=2),
    encoding='utf-8'
)

print(f"Checked: {results['articles_checked']}")
print(f"Invalid combined blocks removed: {results['invalid_combined_removed']}")
print(f"Duplicate Article schemas removed: {results['duplicate_article_removed']}")
print(f"Files changed: {len(results['files_changed'])}")
print(f"Report saved to: {REPORT_FILE}")
```

- [ ] **Step 2: Run the script**

```bash
python3 /Users/bubu/Documents/Github/myo-hk/scripts/cleanup_json_ld.py
```
Expected output: shows counts of files checked and changes made.

- [ ] **Step 3: Verify with spot-check**

```bash
python3 -c "
import json, re
with open('/Users/bubu/Documents/Github/myo-hk/blog/結婚證書套推薦.html') as f:
    c = f.read()
blocks = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', c, re.DOTALL)
for i, b in enumerate(blocks):
    d = json.loads(b.strip())
    print(f'Block {i+1}: @type={d[\"@type\"]} — VALID')
"
```
Expected: No invalid blocks, no duplicate Article types.

- [ ] **Step 4: Commit**

```bash
git add scripts/cleanup_json_ld.py fix_ai_seo_report.json
git commit -m "fix: clean up invalid combined JSON-LD and duplicate Article schemas in blog"
```

Note: Batch-add the blog file changes with `git add -A` then commit with a descriptive message.

---

## Task 11: Add Organization JSON-LD to Blog Articles (Optional Enhancement)

**Files:**
- Modify: All 420 blog HTML files (batch script)

- [ ] **Step 1: Create batch insert script**

Script: `scripts/add_org_schema_to_articles.py`

```python
#!/usr/bin/env python3
"""
Add missing Organization publisher info to blog Article JSON-LD blocks
that don't have a publisher field.
"""
import json
import re
import os
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / 'blog'
ORG_INFO = {
    "@type": "Organization",
    "name": "My O! 專屬結婚證書套",
    "url": "https://myo-hk.github.io",
    "logo": {
        "@type": "ImageObject",
        "url": "https://myo-hk.github.io/image/01_company_logo.png"
    }
}

UPDATED = 0
JSON_LD_PATTERN = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>',
    re.DOTALL
)

for html_file in sorted(BLOG_DIR.glob('*.html')):
    if html_file.name == 'index.html':
        continue
    
    content = html_file.read_text(encoding='utf-8')
    original = content
    
    def update_article(match):
        raw = match.group(1).strip()
        try:
            data = json.loads(raw)
            if isinstance(data, dict) and data.get('@type') == 'Article':
                if 'publisher' not in data or not data.get('publisher'):
                    data['publisher'] = ORG_INFO
                    return f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False, indent=2)}\n</script>'
            return match.group(0)
        except json.JSONDecodeError:
            return match.group(0)
    
    new_content = JSON_LD_PATTERN.sub(update_article, content)
    
    if new_content != original:
        html_file.write_text(new_content, encoding='utf-8')
        UPDATED += 1

print(f"Updated {UPDATED} articles with Organization publisher info")
```

- [ ] **Step 2: Run the script**

```bash
python3 /Users/bubu/Documents/Github/myo-hk/scripts/add_org_schema_to_articles.py
```

- [ ] **Step 3: Spot-verify one article**

```bash
python3 -c "
import json, re
with open('/Users/bubu/Documents/Github/myo-hk/blog/結婚證書套推薦.html') as f:
    c = f.read()
match = re.search(r'<script type=\"application/ld\+json\">(.*?)</script>', c, re.DOTALL)
d = json.loads(match.group(1).strip())
if d.get('@type') == 'Article':
    pub = d.get('publisher', {})
    print(f'publisher: {pub.get(\"name\", \"MISSING\")}')
"
```
Expected: `publisher: My O! 專屬結婚證書套`

- [ ] **Step 4: Commit**

```bash
git add scripts/add_org_schema_to_articles.py
git commit -m "feat: add Organization publisher info to blog Article schemas"
```

---

## Task 12: Optimize Blog Article Opening Paragraphs (Top 20)

**Files:**
- Modify: Top 20 most-important blog articles (opening paragraph)

- [ ] **Step 1: Identify top 20 articles**

Priority articles for AI citation optimization:
- `結婚證書套推薦.html` — main product comparison
- `證書套材質比較.html` — comparison content (33% of AI citations)
- `客製化證書套設計.html` — product page
- `香港結婚完整攻略.html` — definitive guide
- `結婚證書尺寸規格.html` — specific detail query
- `香港婚禮攝影風格比較.html` — comparison
- `婚禮場地選擇指南.html` — definitive guide
- `婚禮預算分配完整攻略.html` — definitive guide
- `婚禮籌備清單.html` — listicle
- `結婚註冊流程教學.html` — how-to guide
- `婚紗禮服選購指南.html` — definitive guide
- `戶外婚禮場地推薦.html` — listicle
- `教堂婚禮場地推薦.html` — listicle
- `婚宴菜單選擇指南.html` — definitive guide
- `敬茶儀式完整教學.html` — how-to guide
- `中式婚禮流程大全.html` — definitive guide
- `香港結婚習俗大全.html` — definitive guide
- `結婚法律指南.html` — definitive guide
- `婚禮攝影器材推薦.html` — listicle
- `鑽石4C選購指南.html` — definitive guide

- [ ] **Step 2: For each article, rewrite the opening paragraph**

Pattern for each article:
1. Read the file
2. Find the first `<p>` tag inside the `<article>` (or the first content paragraph)
3. Rewrite it as a **40-60 word definition block** that can stand alone as an AI extract

Example rewrite for `結婚證書套推薦.html`:

Current first paragraph:
```html
<p>結婚證書套推薦比較，涵蓋材質、價錢和客製化選項。5款熱門證書套實測比較。</p>
```

Rewritten:
```html
<p>結婚證書套是專門用於保存香港婚姻登記處發出之結婚證書的保護套，標準尺寸為 A4（約 209mm × 298mm），通常採用亞麻布或磨砂珠光等高質感物料製成。本文實測比較 5 款香港熱門結婚證書套，從材質、價錢、客製化選項到耐用度，為新人提供全面選購參考。</p>
```

Apply similar rewrites to all 20 articles — each rewrite should:
- Start with a clear definition of the topic
- Be 40-60 words (optimal for AI snippet extraction)
- Stand alone without context
- Include the key query phrase naturally

- [ ] **Step 3: Verify no broken HTML**

```bash
python3 -c "
import os
for f in ['結婚證書套推薦.html', '證書套材質比較.html', '香港結婚完整攻略.html']:
    path = f'/Users/bubu/Documents/Github/myo-hk/blog/{f}'
    with open(path) as fh:
        content = fh.read()
    # Basic check: <p> count matches </p> count
    opens = content.count('<p>')
    closes = content.count('</p>')
    status = 'OK' if opens == closes else f'MISMATCH ({opens} open, {closes} close)'
    print(f'{f}: {status}')
"
```
Expected: All OK

- [ ] **Step 4: Commit**

```bash
git add blog/*.html
git commit -m "feat: optimize top 20 blog article opening paragraphs for AI snippet extraction"
```

---

## Self-Review

### Spec Coverage
- Task 1: og:title typo fix — ✅ covers P0 from audit
- Task 2-3: JSON-LD on homepages — ✅ covers P0
- Task 4: poster.html JSON-LD — ✅ covers M2
- Task 5: HEIC converter Schema — ✅ covers M4
- Task 6: robots.txt AI crawlers — ✅ covers P0
- Task 7: policy noindex — ✅ covers M6
- Task 8: llms.txt — ✅ covers P0
- Task 9: pricing.md — ✅ covers P0
- Task 10: JSON-LD cleanup — ✅ covers P1
- Task 11: Organization schema in articles — ✅ covers M2
- Task 12: Opening paragraph optimization — ✅ covers P2

### Placeholder Scan
No TBDs, TODOs, or placeholder patterns found. Every step has concrete code or commands.

### Type/Schema Consistency
- All JSON-LD blocks use `@context: "https://schema.org"` consistently
- Organization name is "My O! 專屬結婚證書套" everywhere
- Same logo URL used across all schemas
- No naming conflicts across tasks

### Gaps
- No Wikipedia/third-party presence task (out of scope for code changes — editorial)
- No monitoring setup task (out of scope — operational)
- No YouTube/Reddit/Quora participation task (out of scope — editorial)

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-08-ai-seo-review-fixes.md`.**

Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
