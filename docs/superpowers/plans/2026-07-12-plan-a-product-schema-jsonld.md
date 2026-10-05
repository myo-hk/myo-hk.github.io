# Plan A: Product Schema + JSON-LD Consolidation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Product schema for certificate covers, HowTo schema for tutorial articles, consolidate fragmented JSON-LD, and add missing schema fields across the My O! site.

**Architecture:** All schema is injected via `<script type="application/ld+json">` blocks in each HTML page's `<head>`. No build step — direct HTML editing + Python batch scripts for blog articles. Product schema targets the two main product lines (linen vs pearlescent, classic vs designer). HowTo schema targets 10+ tutorial blog articles with step-by-step content.

**Tech Stack:** HTML5, JSON-LD (Schema.org), Python 3 for batch scripts

---

### Task 1: Add Product Schema to index.html

**Files:**
- Modify: `index.html` (after line 838, before `</head>`)

- [ ] **Step 1: Read the current JSON-LD block in index.html**

Run: `grep -n 'application/ld+json' index.html`
Expected: Two blocks (WebSite at line 804, Organization at line 820)

- [ ] **Step 2: Add Product schema block after the Organization block**

Insert this before `</head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "My O! 專屬結婚證書套 — 經典款 亞麻布",
  "description": "設計師級亞麻布結婚證書套，採用熱轉印工藝印上新人名字與結婚日期，讓愛情見證永恆閃耀。",
  "brand": {
    "@type": "Brand",
    "name": "My O! 專屬結婚證書套"
  },
  "offers": [
    {
      "@type": "Offer",
      "name": "經典款 亞麻布",
      "price": "388",
      "priceCurrency": "HKD",
      "itemCondition": "https://schema.org/NewCondition",
      "availability": "https://schema.org/InStock"
    },
    {
      "@type": "Offer",
      "name": "經典款 磨砂珠光",
      "price": "388",
      "priceCurrency": "HKD",
      "itemCondition": "https://schema.org/NewCondition",
      "availability": "https://schema.org/InStock"
    },
    {
      "@type": "Offer",
      "name": "設計師款 亞麻布",
      "price": "588",
      "priceCurrency": "HKD",
      "itemCondition": "https://schema.org/NewCondition",
      "availability": "https://schema.org/InStock"
    },
    {
      "@type": "Offer",
      "name": "設計師款 磨砂珠光",
      "price": "588",
      "priceCurrency": "HKD",
      "itemCondition": "https://schema.org/NewCondition",
      "availability": "https://schema.org/InStock"
    }
  ],
  "material": ["亞麻布", "磨砂珠光"],
  "pattern": "熱轉印（燙印）工藝",
  "color": ["米色", "藍色"],
  "countryOfOrigin": "HK",
  "url": "https://myo-hk.github.io/",
  "image": "https://myo-hk.github.io/image/01_company_logo.png"
}
</script>
```

- [ ] **Step 3: Verify the Product schema is valid JSON**

Run: `python3 -c "import json; json.loads(open('index.html').read().split('</script>')[2].split('<script')[1].strip())"`
Expected: No JSON decode error

- [ ] **Step 4: Also add the same Product schema to v2.html**

Read v2.html for its `</head>` position, then insert the same Product schema block.

Run: `grep -n 'application/ld+json' v2.html`

- [ ] **Step 5: Commit**

```bash
git add index.html v2.html
git commit -m "feat(schema): add Product JSON-LD for certificate cover products"
```

---

### Task 2: Add Product Schema to poster.html and heic-converter.html

**Files:**
- Modify: `poster.html`
- Modify: `heic-converter.html`

- [ ] **Step 1: Add Product schema to poster.html**

Read poster.html's JSON-LD area, then add the same Product schema block before `</head>`. The poster is a promotional flyer — its Product schema should reference the same product line.

- [ ] **Step 2: Add WebApplication schema enhancement to heic-converter.html**

Read heic-converter.html and find any existing WebApplication schema. Add these missing fields if absent:

```json
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "HEIC/HEIF Image Converter",
  "applicationCategory": "Multimedia",
  "operatingSystem": "All",
  "browserRequirements": "JavaScript enabled",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "HKD"
  },
  "description": "Free browser-based HEIC/HEIF to PNG/JPG image converter. 100% client-side, no upload required.",
  "url": "https://myo-hk.github.io/heic-converter.html"
}
```

- [ ] **Step 3: Commit**

```bash
git add poster.html heic-converter.html
git commit -m "feat(schema): add Product schema to poster, enhance WebApplication schema"
```

---

### Task 3: Fix Organization Schema — Add foundingDate and description

**Files:**
- Modify: `index.html`
- Modify: `v2.html`
- Modify: `blog/index.html`

- [ ] **Step 1: Update Organization schema in index.html**

Find the Organization block (around line 820-838). Replace it with:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "My O! 專屬結婚證書套",
  "url": "https://myo-hk.github.io",
  "logo": "https://myo-hk.github.io/image/01_company_logo.png",
  "description": "香港設計師級結婚證書套品牌，提供客製化亞麻布與磨砂珠光證書套，採用熱轉印工藝印製新人名字與結婚日期。",
  "foundingDate": "2025",
  "areaServed": "HK",
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

- [ ] **Step 2: Update Organization schema in blog/index.html**

Read blog/index.html, find the Organization block (around line 208). Apply the same changes: add `description`, `foundingDate`, `areaServed`.

- [ ] **Step 3: Batch-update Organization schema in all 421 blog articles**

Create `scripts/enhance_org_schema.py`:

```python
#!/usr/bin/env python3
"""
Batch update Organization JSON-LD in all blog articles.
Adds description, foundingDate, areaServed fields.
Usage: python3 scripts/enhance_org_schema.py [--test]
"""
import re
import json
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

NEW_ORG = {
    "@type": "Organization",
    "name": "My O! 專屬結婚證書套",
    "url": "https://myo-hk.github.io",
    "logo": {
        "@type": "ImageObject",
        "url": "https://myo-hk.github.io/image/01_company_logo.png"
    },
    "description": "香港設計師級結婚證書套品牌，提供客製化亞麻布與磨砂珠光證書套。",
    "foundingDate": "2025",
    "areaServed": "HK",
    "sameAs": ["https://www.instagram.com/myo.makeyourown/"]
}

ORG_PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*\{[^}]*"@type"\s*:\s*"Organization"[^}]*\}\s*</script>',
    re.DOTALL
)

def replace_org(match):
    """Replace the Organization JSON-LD block with the enhanced version."""
    block = match.group(0)
    # Extract existing content
    json_match = re.search(r'<script[^>]*>(.*?)</script>', block, re.DOTALL)
    if not json_match:
        return block
    try:
        existing = json.loads(json_match.group(1).strip())
    except json.JSONDecodeError:
        return block
    # Merge: keep existing fields, add missing ones from NEW_ORG
    merged = {**NEW_ORG, **{k: v for k, v in existing.items() if k != "@type" and k != "name"}}
    return f'<script type="application/ld+json">\n{json.dumps(merged, ensure_ascii=False, indent=2)}\n</script>'

def main():
    test_mode = "--test" in sys.argv
    files = sorted(BLOG_DIR.glob("*.html"))
    changed = 0
    skipped = 0

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        new_content = ORG_PATTERN.sub(replace_org, content)
        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ {fpath.name}")
            changed += 1
        else:
            skipped += 1

    print(f"\nDone: {changed} updated, {skipped} skipped")

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the script to update articles**

```bash
python3 scripts/enhance_org_schema.py
```
Expected: ~421 updated, showing checkmarks for each file.

- [ ] **Step 5: Verify no JSON was corrupted**

```bash
python3 -c "
import re, json
from pathlib import Path
for f in sorted(Path('blog').glob('*.html')):
    for m in re.finditer(r'<script type=\"application/ld\+json\">(.*?)</script>', f.read_text(), re.DOTALL):
        try:
            json.loads(m.group(1).strip())
        except json.JSONDecodeError as e:
            print(f'CORRUPTED: {f.name}: {e}')
print('Validation complete')
"
```
Expected: "Validation complete" with no CORRUPTED lines.

- [ ] **Step 6: Commit**

```bash
git add scripts/enhance_org_schema.py blog/ index.html v2.html
git commit -m "feat(schema): enhance Organization with description/foundingDate across all pages"
```

---

### Task 4: Consolidate Fragmented JSON-LD Blocks in Blog Articles

**Files:**
- Modify: blog articles with 4+ JSON-LD blocks (identified: `婚禮攝影批量處理指南.html`, `婚禮化妝保養時間表.html`, `婚禮攝影師溝通技巧.html`, `婚禮戒指交換儀式.html`, `婚禮蛋糕選擇.html`, `婚禮稅務優惠.html`)
- Create: `scripts/consolidate_jsonld.py`

- [ ] **Step 1: Identify all articles with fragmented JSON-LD**

```bash
python3 -c "
import re
from pathlib import Path
for f in sorted(Path('blog').glob('*.html')):
    blocks = list(re.finditer(r'<script type=\"application/ld\+json\">(.*?)</script>', f.read_text(encoding='utf-8'), re.DOTALL))
    if len(blocks) >= 3:
        print(f'{len(blocks)} blocks: {f.name}')
"
```
Expected: List of articles with 3+ JSON-LD blocks.

- [ ] **Step 2: Create the consolidation script**

Create `scripts/consolidate_jsonld.py`:

```python
#!/usr/bin/env python3
"""
Consolidate fragmented JSON-LD blocks into fewer blocks (max 2 per page).
Merges: Organization + Article → one block.
Leaves FAQPage as separate block (required by Google for FAQ rich results).
Usage: python3 scripts/consolidate_jsonld.py [--test]
"""
import re
import json
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"
MAX_BLOCKS = 2  # One for page-level schema, one optional for FAQPage

LD_PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
    re.DOTALL
)

def get_schema_type(content):
    """Extract @type from JSON-LD content."""
    try:
        data = json.loads(content.strip())
        return data.get("@type")
    except (json.JSONDecodeError, AttributeError):
        return None

def main():
    test_mode = "--test" in sys.argv
    files = sorted(BLOG_DIR.glob("*.html"))
    changed = 0

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        blocks = list(LD_PATTERN.finditer(content))
        if len(blocks) <= 2:
            continue  # Already consolidated

        # Separate FAQPage from non-FAQPage blocks
        faq_blocks = []
        non_faq = []

        for m in blocks:
            raw = m.group(1).strip()
            stype = get_schema_type(raw)
            if stype == "FAQPage":
                faq_blocks.append(m)
            else:
                non_faq.append(m)

        # Merge all non-FAQPage into one graph
        merged_schemas = []
        for m in non_faq:
            try:
                merged_schemas.append(json.loads(m.group(1).strip()))
            except json.JSONDecodeError:
                pass

        if len(merged_schemas) <= 1 and len(faq_blocks) <= 1:
            continue  # Nothing to consolidate

        # Build new content: remove all LD blocks, re-insert merged ones
        new_content = LD_PATTERN.sub("__LD_PLACEHOLDER__", content)

        # Serialize merged non-FAQ blocks
        replacements = []
        if len(merged_schemas) > 1:
            merged_json = json.dumps({
                "@context": "https://schema.org",
                "@graph": merged_schemas
            }, ensure_ascii=False)
            replacements.append(f'<script type="application/ld+json">\n{merged_json}\n</script>')
        elif len(merged_schemas) == 1:
            merged_json = json.dumps(merged_schemas[0], ensure_ascii=False, indent=2)
            replacements.append(f'<script type="application/ld+json">\n{merged_json}\n</script>')

        # Add FAQ blocks
        for m in faq_blocks:
            replacements.append(f'<script type="application/ld+json">\n{m.group(1).strip()}\n</script>')

        # Replace placeholders one by one
        for rep in replacements:
            new_content = new_content.replace("__LD_PLACEHOLDER__", rep, 1)
        # Remove any remaining placeholders
        new_content = new_content.replace("__LD_PLACEHOLDER__", "")

        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ {fpath.name}: {len(blocks)} blocks → {len(replacements)} blocks")
            changed += 1

    print(f"\nDone: {changed} files consolidated")

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run the consolidation script in test mode**

```bash
python3 scripts/consolidate_jsonld.py --test
```
Expected: Shows which files would change and what the new block count is.

- [ ] **Step 4: Run the consolidation script for real**

```bash
python3 scripts/consolidate_jsonld.py
```

- [ ] **Step 5: Run validation to ensure no JSON was corrupted**

```bash
python3 -c "
import re, json
from pathlib import Path
errors = []
for f in sorted(Path('blog').glob('*.html')):
    for m in re.finditer(r'<script type=\"application/ld\+json\">(.*?)</script>', f.read_text(), re.DOTALL):
        try:
            json.loads(m.group(1).strip())
        except json.JSONDecodeError as e:
            errors.append(f'{f.name}: {e}')
if errors:
    for e in errors: print(f'ERROR: {e}')
else:
    print('All JSON-LD valid - no errors')
"
```
Expected: "All JSON-LD valid - no errors"

- [ ] **Step 6: Commit**

```bash
git add scripts/consolidate_jsonld.py blog/
git commit -m "fix(schema): consolidate fragmented JSON-LD blocks across blog articles"
```

---

### Task 5: Add HowTo Schema to Top 10 Tutorial Blog Articles

**Files:**
- Create: `scripts/add_howto_schema.py`
- Modify: Top 10 tutorial blog articles (identified by filename: 結婚註冊流程教學、婚前準備清單、婚禮籌備時間表、婚禮當天時間表、過大禮清單、敬茶儀式流程、安床習俗與禁忌、結婚證書尺寸規格、證書套保養指南、結婚註冊指南)

- [ ] **Step 1: Create the HowTo schema injection script**

Create `scripts/add_howto_schema.py`:

```python
#!/usr/bin/env python3
"""
Add HowTo schema to tutorial blog articles that have step-by-step content.
Usage: python3 scripts/add_howto_schema.py [--test]
"""
import re
import json
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

# Target articles with step-by-step tutorial content
TARGET_ARTICLES = [
    "結婚註冊流程教學.html",
    "婚前準備清單.html",
    "婚禮籌備時間表.html",
    "婚禮當天時間表.html",
    "過大禮清單.html",
    "敬茶儀式流程.html",
    "安床習俗與禁忌.html",
    "結婚證書尺寸規格.html",
    "證書套保養指南.html",
    "結婚註冊指南.html",
]

# HowTo definition template for each article
HOWTO_TEMPLATES = {
    "結婚註冊流程教學.html": {
        "name": "香港結婚註冊流程",
        "description": "在香港註冊結婚的完整步驟，從預約到領證。",
        "steps": [
            "遞交擬結婚通知書（婚姻登記處或律師樓）",
            "繳交費用及預約註冊日期",
            "選擇婚禮場地（婚姻登記處／特許場所）",
            "安排證婚人（律師或婚姻監禮人）",
            "在預約日期舉行婚禮儀式",
            "簽署結婚證書並領取副本"
        ]
    },
    "婚前準備清單.html": {
        "name": "婚前準備清單",
        "description": "香港新人婚前必須準備的物品和文件。",
        "steps": [
            "準備身份證明文件（身份證、護照）",
            "預約婚姻登記",
            "確認婚禮場地及日期",
            "選購結婚戒指",
            "安排婚紗禮服",
            "預訂婚禮攝影師及化妝師"
        ]
    },
    "婚禮籌備時間表.html": {
        "name": "婚禮籌備時間表",
        "description": "從求婚到婚禮當日的完整籌備時間規劃。",
        "steps": [
            "12個月前：確定預算及日期",
            "10個月前：預訂場地及攝影師",
            "8個月前：選擇婚紗禮服",
            "6個月前：發送邀請函",
            "3個月前：確認菜單及座位表",
            "1個月前：試菜及最終確認"
        ]
    },
    "婚禮當天時間表.html": {
        "name": "婚禮當天時間表",
        "description": "香港婚禮當日的典型流程與時間安排。",
        "steps": [
            "早上6時：新娘化妝及造型",
            "早上8時：新郎準備",
            "早上10時：接新娘遊戲",
            "中午12時：註冊儀式",
            "下午2時：婚宴午餐",
            "下午5時：戶外拍攝",
            "晚上7時：晚宴開始"
        ]
    },
    "過大禮清單.html": {
        "name": "過大禮所需物品清單",
        "description": "中式傳統過大禮儀式所需的物品和數量。",
        "steps": [
            "準備禮金及禮餅（龍鳳餅、唐餅）",
            "安排海味（乾鮑、花膠、元貝等）",
            "準備水果（椰子、檳榔等吉祥水果）",
            "購買中式禮盒（龍鳳燭、對聯）",
            "準備金器（龍鳳鐲、戒指）",
            "安排媒人陪同送禮"
        ]
    },
    "敬茶儀式流程.html": {
        "name": "香港婚禮敬茶儀式流程",
        "description": "傳統中式婚禮敬茶儀式的完整步驟與禮儀。",
        "steps": [
            "準備敬茶用具（茶壺、茶杯、托盤）",
            "鋪設跪墊（新人跪拜用）",
            "先敬父母（新郎父母先飲茶）",
            "逐一長輩敬茶（按輩分順序）",
            "長輩回禮（利是或金器）",
            "新人互敬（夫妻對拜）"
        ]
    },
    "安床習俗與禁忌.html": {
        "name": "安床習俗與禁忌",
        "description": "中式婚禮安床儀式的正確做法與注意事項。",
        "steps": [
            "選擇吉日吉時進行安床",
            "由好命婆（福氣婦女）負責鋪床",
            "在床上放置龍鳳被及紅棗蓮子",
            "安排小男孩在床上滾動（旺丁）",
            "安床後不宜移動床具",
            "婚禮前不可讓人坐臥新床"
        ]
    },
    "結婚證書尺寸規格.html": {
        "name": "結婚證書尺寸規格查詢",
        "description": "香港結婚證書的標準尺寸和規格說明。",
        "steps": [
            "確認香港結婚證書標準尺寸（210mm × 297mm A4）",
            "選購適合的結婚證書套",
            "選擇證書套材質（亞麻布或磨砂珠光）",
            "提供新人名字和結婚日期進行燙印",
            "確認設計稿後製作（7-14個工作天）"
        ]
    },
    "證書套保養指南.html": {
        "name": "結婚證書套保養方法",
        "description": "亞麻布和磨砂珠光結婚證書套的正確保養方法。",
        "steps": [
            "避免陽光直射（防止褪色）",
            "保持乾燥環境（避免潮濕發霉）",
            "定期用軟布輕拭表面灰塵",
            "避免與尖銳物品接觸（防止刮花）",
            "存放時放入防潮箱或通風處",
            "燙印部分避免用力擦拭"
        ]
    },
    "結婚註冊指南.html": {
        "name": "香港結婚註冊指南",
        "description": "香港註冊結婚的完整流程、文件及費用說明。",
        "steps": [
            "查閱結婚資格（年齡、婚姻狀況）",
            "準備所需文件（身份證、住址證明）",
            "預約婚姻登記處",
            "遞交擬結婚通知書",
            "繳交註冊費用",
            "選擇婚姻監禮人",
            "在預定日期舉行婚禮"
        ]
    }
}

def build_howto_json(filename, steps):
    """Build HowTo JSON-LD."""
    tmpl = HOWTO_TEMPLATES[filename]
    step_list = []
    for i, step_text in enumerate(steps):
        step_list.append({
            "@type": "HowToStep",
            "position": i + 1,
            "name": step_text.split("：")[0] if "：" in step_text else step_text[:20],
            "text": step_text
        })
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": tmpl["name"],
        "description": tmpl["description"],
        "step": step_list
    }

def main():
    test_mode = "--test" in sys.argv
    changed = 0

    for fname in TARGET_ARTICLES:
        fpath = BLOG_DIR / fname
        if not fpath.exists():
            print(f"  SKIP {fname}: file not found")
            continue

        content = fpath.read_text(encoding="utf-8")
        howto_json = build_howto_json(fname, HOWTO_TEMPLATES[fname]["steps"])

        # Insert HowTo schema before </head>
        script_tag = f'\n<script type="application/ld+json">\n{json.dumps(howto_json, ensure_ascii=False, indent=2)}\n</script>\n'
        new_content = content.replace("</head>", script_tag + "</head>", 1)

        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ {fname}: HowTo schema added")
            changed += 1
        else:
            print(f"  ? {fname}: no change (unexpected)")

    print(f"\nDone: {changed} articles updated")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script in test mode**

```bash
python3 scripts/add_howto_schema.py --test
```
Expected: Shows which files would get HowTo schema.

- [ ] **Step 3: Run the script for real**

```bash
python3 scripts/add_howto_schema.py
```

- [ ] **Step 4: Validate the JSON-LD**

```bash
python3 -c "
import json
from pathlib import Path
for f in sorted(Path('blog').glob('*.html')):
    content = f.read_text(encoding='utf-8')
    if 'HowTo' in content:
        print(f'  Has HowTo: {f.name}')
"
```
Expected: Shows the 10 article filenames with HowTo schema.

- [ ] **Step 5: Commit**

```bash
git add scripts/add_howto_schema.py blog/
git commit -m "feat(schema): add HowTo schema to 10 tutorial blog articles"
```

---

### Task 6: Add BlogPosting Schema (Replace Article Schema)

**Files:**
- Create: `scripts/upgrade_to_blogposting.py`
- Modify: All 421 blog articles

- [ ] **Step 1: Create the schema upgrade script**

Create `scripts/upgrade_to_blogposting.py`:

```python
#!/usr/bin/env python3
"""
Upgrade Article JSON-LD to BlogPosting in blog articles.
BlogPosting is more specific than Article and preferred for blog content.
Usage: python3 scripts/upgrade_to_blogposting.py [--test]
"""
import re
import json
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

def main():
    test_mode = "--test" in sys.argv
    files = sorted(BLOG_DIR.glob("*.html"))
    changed = 0

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        # Find Article schema blocks that are NOT FAQPage
        pattern = re.compile(
            r'(<script type="application/ld\+json">\s*\{[^}]*"@type"\s*:\s*"Article")',
            re.DOTALL
        )
        if not pattern.search(content):
            continue

        new_content = pattern.sub(r'\1Posting', content)  # "Article" → "BlogPosting"
        # Also fix any "ArticlePosting" that would result from double-substitution
        new_content = new_content.replace('"BlogPostingPosting"', '"BlogPosting"')

        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ {fpath.name}")
            changed += 1

    print(f"\nDone: {changed} files upgraded from Article → BlogPosting")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script**

```bash
python3 scripts/upgrade_to_blogposting.py
```

- [ ] **Step 3: Verify changes**

```bash
grep -r '"@type": "BlogPosting"' blog/ | wc -l
```
Expected: Same number as blog articles (minus articles that didn't have Article schema).

- [ ] **Step 4: Commit**

```bash
git add scripts/upgrade_to_blogposting.py blog/
git commit -m "feat(schema): upgrade Article to BlogPosting across all blog articles"
```
