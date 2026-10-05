# WebP Conversion — Site-Wide Image Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert all PNG/JPG content images across the site to WebP format and update HTML references to serve WebP directly, removing `<picture>`/`<source>` fallback wrappers.

**Architecture:** Direct WebP approach — no `<picture>` wrappers, serve `.webp` directly as `<img src>`. Favicon and PWA icons (`icon-192x192.png`, `icon-512x512.png`) stay as PNG since those are required formats. Two orphan PNG files need `cwebp` conversion; all other images already have `.webp` variants.

**Tech Stack:** `cwebp` (Homebrew libwebp) for image conversion, HTML edits for 7 pages.

---

## File Structure

### Converted files
| File | Action |
|------|--------|
| `image/01_company_logo_converted.png` | Convert to `.webp` (100K → ~20K) |
| `image/cert_style_3.png` | Convert to `.webp` (104K → ~15K) |

### Modified HTML files
| File | Changes |
|------|---------|
| `index.html` | Remove 3 `<picture>` wrappers, change 5 `<img src=".png">` to `.webp` |
| `v2.html` | Remove 8 `<picture>` wrappers, change 3 `<img src=".jpg">` + 5 `<img src=".png">` to `.webp` |
| `poster.html` | Remove 1 `<picture>` wrapper, change 5 `<img src=".png">` to `.webp` |
| `privacy.html` | Remove 2 `<picture>` wrappers |
| `terms.html` | Remove 2 `<picture>` wrappers |
| `faq.html` | Remove 2 `<picture>` wrappers |
| `blog/index.html` | Remove 1 `<picture>` wrapper |

### Unchanged files (kept as PNG)
- `image/icon-192x192.png`
- `image/icon-512x512.png`
- All favicon `<link rel="icon">` references

---

### Task 1: Convert remaining source images to WebP

**Files:**
- Modify: `image/01_company_logo_converted.png` → `image/01_company_logo_converted.webp`
- Modify: `image/cert_style_3.png` → `image/cert_style_3.webp`

- [ ] **Step 1: Convert 01_company_logo_converted.png to WebP**

Run:
```bash
cwebp -q 80 image/01_company_logo_converted.png -o image/01_company_logo_converted.webp
```
Expected: ~20-30K output, no errors.

- [ ] **Step 2: Convert cert_style_3.png to WebP**

Run:
```bash
cwebp -q 80 image/cert_style_3.png -o image/cert_style_3.webp
```
Expected: ~15-25K output, no errors.

- [ ] **Step 3: Verify both WebP files exist**

Run:
```bash
ls -lh image/01_company_logo_converted.webp image/cert_style_3.webp
```
Expected: Both files present, sizes reasonable.

- [ ] **Step 4: Commit**

```bash
git add image/01_company_logo_converted.webp image/cert_style_3.webp
git commit -m "perf: convert remaining PNG sources to WebP"
```

---

### Task 2: Update index.html — Logo and sticky bar WebP

**Files:**
- Modify: `index.html:224-227` — nav logo `<picture>` wrapper
- Modify: `index.html:263` — hero logo `<picture>` wrapper
- Modify: `index.html:558` — sticky bar logo `<picture>` wrapper

- [ ] **Step 1: Replace nav logo `<picture>` with direct `<img>`**

In `index.html`, replace:
```html
<picture>
    <source srcset="image/01_company_logo.webp" type="image/webp">
    <img src="image/01_company_logo.png" width="256" height="256" loading="eager" class="lzy1Td" role="img" aria-label="網站首頁" jsname="SwcDWb">
</picture>
```
With:
```html
<img src="image/01_company_logo.webp" width="256" height="256" loading="eager" class="lzy1Td" role="img" aria-label="網站首頁" jsname="SwcDWb">
```

- [ ] **Step 2: Replace hero logo `<picture>` with direct `<img>`**

Replace:
```html
<picture> <source srcset="image/01_company_logo.webp" type="image/webp"> <img src="image/01_company_logo.png" alt="My O! logo" width="112" height="112" loading="eager" class="w-28 md:w-36 h-auto"> </picture>
```
With:
```html
<img src="image/01_company_logo.webp" alt="My O! logo" width="112" height="112" loading="eager" class="w-28 md:w-36 h-auto">
```

- [ ] **Step 3: Replace sticky bar logo `<picture>` with direct `<img>`**

Replace:
```html
<picture> <source srcset="image/01_company_logo.webp" type="image/webp"> <img src="image/01_company_logo.png" alt="My O! Logo" width="50" height="50" loading="lazy" class="logo"> </picture>
```
With:
```html
<img src="image/01_company_logo.webp" alt="My O! Logo" width="50" height="50" loading="lazy" class="logo">
```

- [ ] **Step 4: Run lsp_diagnostics on index.html**

Run: `lsp_diagnostics` for `index.html`
Expected: Clean diagnostics with no errors related to HTML or image references.

---

### Task 3: Update index.html — Style preview images

**Files:**
- Modify: `index.html:327` style 1 `src`
- Modify: `index.html:339` style 2 `src`
- Modify: `index.html:351` style 3 `src`
- Modify: `index.html:363` style 4 `src`
- Modify: `index.html:375` style 5 `src`

- [ ] **Step 1: Change style 1 from PNG to WebP**

Replace `src="image/cert_style_1.png"` with `src="image/cert_style_1.webp"` on line 327.

- [ ] **Step 2: Change style 2 from PNG to WebP**

Replace `src="image/cert_style_2.png"` with `src="image/cert_style_2.webp"` on line 339.

- [ ] **Step 3: Change style 3 from PNG to WebP**

Replace `src="image/cert_style_3_chinese.png"` with `src="image/cert_style_3_chinese.webp"` on line 351.

- [ ] **Step 4: Change style 4 from PNG to WebP**

Replace `src="image/cert_style_4.png"` with `src="image/cert_style_4.webp"` on line 363.

- [ ] **Step 5: Change style 5 from PNG to WebP**

Replace `src="image/cert_style_5.png"` with `src="image/cert_style_5.webp"` on line 375.

- [ ] **Step 6: Run lsp_diagnostics to verify**

Run: `lsp_diagnostics` for `index.html`
Expected: Clean.

- [ ] **Step 7: Commit**

```bash
git add index.html
git commit -m "perf: update index.html to serve WebP directly"
```

---

### Task 4: Update v2.html — Logos and color swatches

**Files:**
- Modify: `v2.html:1791` — nav logo
- Modify: `v2.html:1825` — hero logo
- Modify: `v2.html:1876-1878` — beige color `<picture>` wrapper + .jpg
- Modify: `v2.html:1888-1890` — blue color `<picture>` wrapper + .jpg
- Modify: `v2.html:2073` — sticky bar logo

- [ ] **Step 1: Replace nav logo `<picture>` with direct `<img>`**

Replace:
```html
<picture> <source srcset="image/01_company_logo.webp" type="image/webp"> <img src="image/01_company_logo.png" class="lzy1Td" role="img" aria-label="網站首頁" jsname="SwcDWb" loading="eager"> </picture>
```
With:
```html
<img src="image/01_company_logo.webp" class="lzy1Td" role="img" aria-label="網站首頁" jsname="SwcDWb" loading="eager">
```

- [ ] **Step 2: Replace hero logo `<picture>` with direct `<img>`**

Replace:
```html
<picture> <source srcset="image/01_company_logo.webp" type="image/webp"> <img src="image/01_company_logo.png" alt="My O! logo" class="w-28 md:w-36 h-auto" loading="eager"> </picture>
```
With:
```html
<img src="image/01_company_logo.webp" alt="My O! logo" class="w-28 md:w-36 h-auto" loading="eager">
```

- [ ] **Step 3: Replace beige color thumb `<picture>` wrapper**

Replace:
```html
<picture>
    <source srcset="image/cert_color_beige.webp" type="image/webp">
    <img src="image/cert_color_beige.jpg" alt="米色證書套預覽" class="select-option-image" width="200" height="133" loading="lazy">
</picture>
```
With:
```html
<img src="image/cert_color_beige.webp" alt="米色證書套預覽" class="select-option-image" width="200" height="133" loading="lazy">
```

- [ ] **Step 4: Replace blue color thumb `<picture>` wrapper**

Replace:
```html
<picture>
    <source srcset="image/cert_color_blue.webp" type="image/webp">
    <img src="image/cert_color_blue.jpg" alt="藍色證書套預覽" class="select-option-image" width="200" height="144" loading="lazy">
</picture>
```
With:
```html
<img src="image/cert_color_blue.webp" alt="藍色證書套預覽" class="select-option-image" width="200" height="144" loading="lazy">
```

- [ ] **Step 5: Replace sticky bar logo `<picture>` with direct `<img>`**

Replace:
```html
<picture> <source srcset="image/01_company_logo.webp" type="image/webp"> <img src="image/01_company_logo.png" alt="My O! Logo" class="sticky-logo" width="50" height="50" loading="lazy"> </picture>
```
With:
```html
<img src="image/01_company_logo.webp" alt="My O! Logo" class="sticky-logo" width="50" height="50" loading="lazy">
```

---

### Task 5: Update v2.html — Style preview images and hero

**Files:**
- Modify: `v2.html:1905-1907` — style 1
- Modify: `v2.html:1917-1919` — style 2
- Modify: `v2.html:1929-1931` — style 3
- Modify: `v2.html:1941-1943` — style 4
- Modify: `v2.html:1953-1955` — style 5
- Modify: `v2.html:1979-1981` — hero image

- [ ] **Step 1: Replace style 1 `<picture>` wrapper**

Replace:
```html
<picture>
    <source srcset="image/cert_style_1.webp" type="image/webp">
    <img src="image/cert_style_1.png" alt="款式1" class="w-full h-auto rounded-md" width="437" height="465" loading="lazy">
</picture>
```
With:
```html
<img src="image/cert_style_1.webp" alt="款式1" class="w-full h-auto rounded-md" width="437" height="465" loading="lazy">
```

- [ ] **Step 2: Replace style 2 `<picture>` wrapper**

Replace:
```html
<picture>
    <source srcset="image/cert_style_2.webp" type="image/webp">
    <img src="image/cert_style_2.png" alt="款式2" class="w-full h-auto rounded-md" width="548" height="455" loading="lazy">
</picture>
```
With:
```html
<img src="image/cert_style_2.webp" alt="款式2" class="w-full h-auto rounded-md" width="548" height="455" loading="lazy">
```

- [ ] **Step 3: Replace style 3 `<picture>` wrapper**

Replace:
```html
<picture>
    <source srcset="image/cert_style_3_chinese.webp" type="image/webp">
    <img src="image/cert_style_3_chinese.png" alt="款式3" class="w-full h-auto rounded-md" width="656" height="262" loading="lazy">
</picture>
```
With:
```html
<img src="image/cert_style_3_chinese.webp" alt="款式3" class="w-full h-auto rounded-md" width="656" height="262" loading="lazy">
```

- [ ] **Step 4: Replace style 4 `<picture>` wrapper**

Replace:
```html
<picture>
    <source srcset="image/cert_style_4.webp" type="image/webp">
    <img src="image/cert_style_4.png" alt="款式4" class="w-full h-auto rounded-md" width="608" height="288" loading="lazy">
</picture>
```
With:
```html
<img src="image/cert_style_4.webp" alt="款式4" class="w-full h-auto rounded-md" width="608" height="288" loading="lazy">
```

- [ ] **Step 5: Replace style 5 `<picture>` wrapper**

Replace:
```html
<picture>
    <source srcset="image/cert_style_5.webp" type="image/webp">
    <img src="image/cert_style_5.png" alt="款式5" class="w-full h-auto rounded-md" width="490" height="518" loading="lazy">
</picture>
```
With:
```html
<img src="image/cert_style_5.webp" alt="款式5" class="w-full h-auto rounded-md" width="490" height="518" loading="lazy">
```

- [ ] **Step 6: Replace hero image `<picture>` wrapper**

Replace:
```html
<picture>
    <source srcset="image/cert_hero_600.webp 600w, image/cert_hero.webp 1200w" sizes="(max-width: 768px) 100vw, 600px" type="image/webp">
    <img src="image/cert_hero.jpg" alt="結婚證書套示意圖" class="rounded-2xl shadow-lg product-image" width="600" height="495" style="aspect-ratio: 1200/991" loading="eager" fetchpriority="high" sizes="(max-width: 768px) 100vw, 600px">
</picture>
```
With:
```html
<img src="image/cert_hero.webp" alt="結婚證書套示意圖" class="rounded-2xl shadow-lg product-image" width="600" height="495" style="aspect-ratio: 1200/991" loading="eager" fetchpriority="high" sizes="(max-width: 768px) 100vw, 600px">
```

- [ ] **Step 7: Run lsp_diagnostics on v2.html**

Run: `lsp_diagnostics` for `v2.html`
Expected: Clean.

- [ ] **Step 8: Commit**

```bash
git add v2.html
git commit -m "perf: update v2.html to serve WebP directly"
```

---

### Task 6: Update poster.html — Logo and style previews

**Files:**
- Modify: `poster.html:933` — logo
- Modify: `poster.html:986` — style 1
- Modify: `poster.html:993` — style 2
- Modify: `poster.html:1000` — style 3
- Modify: `poster.html:1007` — style 4
- Modify: `poster.html:1014` — style 5

- [ ] **Step 1: Replace logo `<picture>` with direct `<img>`**

Replace:
```html
<picture> <source srcset="image/01_company_logo.webp" type="image/webp"> <img src="image/01_company_logo.png" alt="My O! Logo"> </picture>
```
With:
```html
<img src="image/01_company_logo.webp" alt="My O! Logo">
```

- [ ] **Step 2: Change style 1 from PNG to WebP**

`img src="image/cert_style_1.png"` → `src="image/cert_style_1.webp"` (line 986)

- [ ] **Step 3: Change style 2 from PNG to WebP**

`img src="image/cert_style_2.png"` → `src="image/cert_style_2.webp"` (line 993)

- [ ] **Step 4: Change style 3 from PNG to WebP**

`img src="image/cert_style_3_chinese.png"` → `src="image/cert_style_3_chinese.webp"` (line 1000)

- [ ] **Step 5: Change style 4 from PNG to WebP**

`img src="image/cert_style_4.png"` → `src="image/cert_style_4.webp"` (line 1007)

- [ ] **Step 6: Change style 5 from PNG to WebP**

`img src="image/cert_style_5.png"` → `src="image/cert_style_5.webp"` (line 1014)

- [ ] **Step 7: Run lsp_diagnostics on poster.html**

Run: `lsp_diagnostics` for `poster.html`
Expected: Clean.

- [ ] **Step 8: Commit**

```bash
git add poster.html
git commit -m "perf: update poster.html to serve WebP directly"
```

---

### Task 7: Update privacy.html, terms.html, faq.html — Logo wrappers

**Files:**
- Modify: `privacy.html:209,270`
- Modify: `terms.html:209,267`
- Modify: `faq.html:415,524`

- [ ] **Step 1: Update privacy.html — both logo `<picture>` wrappers**

Line 209 replace:
```html
<picture> <source srcset="image/01_company_logo.webp" type="image/webp"> <img src="image/01_company_logo.png" class="h-6 w-6 mr-2" alt="My O! logo"> </picture>
```
With:
```html
<img src="image/01_company_logo.webp" class="h-6 w-6 mr-2" alt="My O! logo">
```

Line 270 replace:
```html
<picture> <source srcset="image/01_company_logo.webp" type="image/webp"> <img src="image/01_company_logo.png" alt="My O! Logo" class="logo"> </picture>
```
With:
```html
<img src="image/01_company_logo.webp" alt="My O! Logo" class="logo">
```

- [ ] **Step 2: Update terms.html — both logo `<picture>` wrappers**

Same pattern as privacy.html lines 209/270. Replace both `<picture>` wrappers with direct `<img src="image/01_company_logo.webp">`.

- [ ] **Step 3: Update faq.html — both logo `<picture>` wrappers**

Same pattern as privacy.html lines 209/270. Replace both `<picture>` wrappers with direct `<img src="image/01_company_logo.webp">`.

- [ ] **Step 4: Run lsp_diagnostics on all three files**

Run: `lsp_diagnostics` on `privacy.html`, `terms.html`, `faq.html`
Expected: Clean diagnostics for all three.

- [ ] **Step 5: Commit**

```bash
git add privacy.html terms.html faq.html
git commit -m "perf: update privacy/terms/faq pages to serve WebP directly"
```

---

### Task 8: Update blog/index.html — Logo wrapper

**Files:**
- Modify: `blog/index.html:237` — nav logo

- [ ] **Step 1: Replace nav logo `<picture>` with direct `<img>`**

Line 237 replace:
```html
<picture> <source srcset="../image/01_company_logo.webp" type="image/webp"> <img src="../image/01_company_logo.png" class="h-6 w-6 mr-2" alt="My O! logo"> </picture>
```
With:
```html
<img src="../image/01_company_logo.webp" class="h-6 w-6 mr-2" alt="My O! logo">
```

- [ ] **Step 2: Run lsp_diagnostics on blog/index.html**

Run: `lsp_diagnostics` for `blog/index.html`
Expected: Clean.

- [ ] **Step 3: Commit**

```bash
git add blog/index.html
git commit -m "perf: update blog/index.html to serve WebP directly"
```

---

### Task 9: Final verification

**Files:** All modified HTML files

- [ ] **Step 1: Verify no remaining PNG/JPG references in HTML `<img src>` or `<source srcset>`**

Run:
```bash
grep -rn 'src="image/.*\.\(png\|jpg\)"' index.html v2.html poster.html privacy.html terms.html faq.html blog/index.html
```
Expected: Only favicon `<link rel="icon">` references remain (those stay as PNG).

- [ ] **Step 2: Verify favicon references remain intact**

Run:
```bash
grep -rn 'rel="icon"\|rel="shortcut icon"\|rel="apple-touch-icon"' index.html v2.html poster.html privacy.html terms.html faq.html blog/index.html
```
Expected: All favicon lines present and unchanged.

- [ ] **Step 3: Quick build check if build script exists**

Run: `npm run build:css` (if applicable) — just verify the project still builds.
Expected: No errors.

- [ ] **Step 4: Final tally — estimated weight savings**

Calculate: Sum of all removed PNG/JPG sizes vs new WebP sizes:
- Nav logo: 8.3K → 5.4K (-2.9K)
- Hero logo: 8.3K → 5.4K (-2.9K)
- Style 1: 105K → 14K (-91K)
- Style 2: 62K → 11K (-51K)
- Style 3 chinese: 75K → 12K (-63K)
- Style 4: 54K → 7.3K (-46.7K)
- Style 5: 78K → 9.7K (-68.3K)
- Beige color (v2): 238K → 27K (-211K)
- Blue color (v2): 132K → 11K (-121K)
- Hero (v2): 126K → 56K (-70K)
- **Total savings per page load: ~728K (index.html logged-in), ~1.2MB (v2.html full load)**

Expected: Estimated 70-80% reduction in image payload across all affected pages.

- [ ] **Step 5: Final commit if any changes remain**

```bash
git status
```
Expected: Clean working tree (no uncommitted changes).
