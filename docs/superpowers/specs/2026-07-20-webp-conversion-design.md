# WebP Conversion — Site-Wide Image Optimization

**Date:** 2026-07-20
**Status:** Approved Design
**Approach:** Direct WebP (Approach 1)

## Goal

Convert all content images across the site from PNG/JPG to WebP format, remove `<picture>` / `<source>` fallback wrappers, and serve WebP directly. This reduces image payload, improves page load speed, and follows SEO best practices for image optimization.

## Scope

**6 pages affected:**
- `index.html` — homepage (logo, style previews, hero image, sticky bar logo)
- `v2.html` — redesigned homepage (same images)
- `poster.html` — A5 promo poster (logo, style previews)
- `privacy.html` — privacy policy (logo)
- `terms.html` — terms of service (logo)
- `faq.html` — FAQ page (logo)

**Blog articles (420+):** No `image/` references — no changes needed.

**Not in scope (keep as PNG):**
- `icon-192x192.png` / `icon-512x512.png` — PWA/apple-touch-icon (required format)
- Favicon `<link rel="icon">` references — stay as PNG for universal browser support

## Source File Conversion

Only 2 PNG files lack WebP counterparts:

| Source | Target | Method |
|--------|--------|--------|
| `image/01_company_logo_converted.png` | `image/01_company_logo_converted.webp` | `cwebp -q 80` |
| `image/cert_style_3.png` | `image/cert_style_3.webp` | `cwebp -q 80` |

All other images already have `.webp` variants in the `image/` directory (logo, color swatches, style 1/2/3_chinese/4/5, hero).

## HTML Changes

### Pattern: Remove `<picture>` wrappers, replace `<img src>` with `.webp`

**Before:**
```html
<picture>
  <source srcset="image/xxx.webp" type="image/webp">
  <img src="image/xxx.png" ...>
</picture>
```

**After:**
```html
<img src="image/xxx.webp" ...>
```

### Changes per page

| Page | `<picture>` → `<img>` | `src=".png"` → `.webp` | `src=".jpg"` → `.webp` |
|------|----------------------|----------------------|----------------------|
| `index.html` | 3 (logo ×2, sticky bar) | 5 (style 1-5) | 0 |
| `v2.html` | 3 (logo ×2, sticky bar) | 5 (style 1-5) | 3 (beige, blue, hero) |
| `poster.html` | 1 (logo) | 5 (style 1-5) | 0 |
| `privacy.html` | 2 (logo ×2) | 0 | 0 |
| `terms.html` | 2 (logo ×2) | 0 | 0 |
| `faq.html` | 2 (logo ×2) | 0 | 0 |

**Total: ~28 edits** (13 `<picture>` removals + 15 `src` extensions changed)

## Conversion Method

```bash
cwebp -q 80 image/01_company_logo_converted.png -o image/01_company_logo_converted.webp
cwebp -q 80 image/cert_style_3.png -o image/cert_style_3.webp
```

`cwebp` at quality 80 provides ~70-80% size reduction over PNG with negligible visual loss.

## Success Criteria

1. All `<img src>` references across the 6 pages point to `.webp` files
2. All `<picture>` / `<source>` wrappers removed (content images only)
3. Favicon and PWA icon references preserved as PNG
4. All pages render correctly in browser — no broken images
5. `lsp_diagnostics` clean on all edited files
6. Measurably smaller transferred image payload

## Verification

1. `lsp_diagnostics` on each edited file
2. Manual browser check of each page for broken images
3. Compare total image weight before/after
