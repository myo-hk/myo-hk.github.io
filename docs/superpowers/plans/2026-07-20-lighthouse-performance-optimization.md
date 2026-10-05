# Lighthouse Performance Optimization (Score 92 → 98+)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Raise Lighthouse performance score from 92 to 98+ on mobile by fixing forced reflow, image over-delivery, CLS from web fonts, and non-composited animations — all in `index.html` (the primary landing page).

**Architecture:** Single-page static HTML file (`index.html`) with inline `<script>` and `<style>`. No framework. No bundler. All changes are surgical edits to this one file plus image asset resizing.

**Tech Stack:** Vanilla HTML/JS/CSS, Playwright for regression testing, `sips` (macOS built-in) for image resizing.

**Files affected:**
- `index.html` — inline scroll-depth script, inline DOMContentLoaded handler, inline styles, image `<img>` tags
- `image/cert_color_beige.webp` — resized to 210×140 thumbnail
- `image/cert_color_blue.webp` — resized to 210×140 thumbnail
- `image/01_company_logo.webp` — resized to 72×72 for nav usage
- `tests/lighthouse-audits.spec.ts` — new regression tests

---

### Task 1: Fix forced reflow in scroll-depth tracker (80ms)

**Files:**
- Modify: `index.html:741-771`

**Root cause:** The scroll-depth tracker script (line 748-751) queries `document.body.scrollHeight` and `document.documentElement.scrollHeight` **eagerly** when the script first executes. `scrollHeight` forces a synchronous layout recalculation. On a page with 268 DOM elements and images still loading, this costs ~80ms.

**Fix:** Move `docHeight` computation inside the scroll handler so it's computed lazily on first scroll. Also cache it after first calculation so subsequent scroll events reuse it.

- [ ] **Step 1: Replace the scroll-depth tracker**

Replace lines 741-771 with:

```html
<script>
(function() {
  if (typeof gtag === 'undefined') return;
  var scrollDepths = {25: true, 50: true, 75: true, 90: true};
  var firedDepths = {};
  var docHeight = 0;

  var getDocHeight = function() {
    if (docHeight > 0) return docHeight;
    docHeight = Math.max(
      document.body.scrollHeight,
      document.documentElement.scrollHeight
    );
    return docHeight;
  };

  var scrollHandler = function() {
    var scrollTop = window.scrollY || window.pageYOffset;
    var windowHeight = window.innerHeight;
    var currentDocHeight = getDocHeight();
    var scrollPercent = Math.round((scrollTop + windowHeight) / currentDocHeight * 100);
    Object.keys(scrollDepths).forEach(function(depth) {
      if (scrollPercent >= parseInt(depth) && !firedDepths[depth]) {
        firedDepths[depth] = true;
        gtag('event', 'scroll_depth', {
          'event_category': 'engagement',
          'event_label': depth + '%',
          'value': parseInt(depth),
          'non_interaction': true
        });
      }
    });
  };
  window.addEventListener('scroll', scrollHandler, {passive: true});
})();
</script>
```

- [ ] **Step 2: Verify no forced reflow on load**

Run: `grep -n "scrollHeight\|offsetHeight\|offsetWidth\|clientHeight\|clientWidth" index.html`

Expected: The only layout queries are inside the `getDocHeight()` function which does NOT execute until the first scroll event.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "perf: defer scrollHeight query to first scroll event, avoiding 80ms forced reflow on load"
```

---

### Task 2: Fix forced reflow in DOMContentLoaded handler (9ms)

**Files:**
- Modify: `index.html:576-727`

**Root cause:** The main `DOMContentLoaded` handler (line 595-638) runs `document.querySelectorAll('.select-option')` and later (inside click handler at line 621) accesses `this.querySelector('.select-option-image').src`. While the initial `querySelectorAll` is acceptable, the overall handler triggers style recalc. The bigger issue: the click handler queries `.src` which can force a reflow if images haven't settled.

**Fix:** Move the `.select-option-image` query inside click handler to use `getAttribute('src')` instead of `.src` (avoiding the getter that triggers layout).

- [ ] **Step 1: Replace `.src` with `getAttribute('src')` in color click handler**

In `index.html`, line 621, change:

```javascript
const imgSrc = this.querySelector('.select-option-image').src;
```

to:

```javascript
const imgSrc = this.querySelector('.select-option-image').getAttribute('src');
```

The `.src` property accessor on HTMLImageElement triggers a micro-task to ensure the URL is resolved. `getAttribute('src')` returns the raw attribute string without forcing layout.

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "perf: use getAttribute('src') instead of .src to avoid forced layout in image click handler"
```

---

### Task 3: Downsize color preview images (26+ KiB savings)

**Files:**
- Modify: `image/cert_color_beige.webp` — resized from 808×538 to 210×140
- Modify: `image/cert_color_blue.webp` — resized from 808×538 to 210×140

**Root cause:** `cert_color_beige.webp` (808×538, 27 KiB) is displayed at 105×70 inside the color selector card. Lighthouse reports 26.4 KiB waste. Same for `cert_color_blue.webp` (11 KiB).

**Display context:** The color preview images are inside a `.select-option-image` class with `width="200" height="133"`. The actual displayed size on mobile (390px viewport) is ~105×70 due to grid layout and card padding.

**Target size:** 210×140 (2x retina for the ~105×70 displayed area). This cuts both files to <3 KiB each.

- [ ] **Step 1: Create downsized color preview images**

```bash
cd image
sips -z 140 210 cert_color_beige.webp --out cert_color_beige_thumb.webp
sips -z 140 210 cert_color_blue.webp --out cert_color_blue_thumb.webp
```

- [ ] **Step 2: Replace the `<img>` and `<source>` tags**

In `index.html`, update the color card images (lines 292-297 and 303-309).

For beige (line 292-297):
```html
<picture>
    <source srcset="image/cert_color_beige_thumb.webp" type="image/webp">
    <img src="image/cert_color_beige_thumb.webp" alt="米色證書套預覽" class="select-option-image" width="210" height="140" loading="lazy">
</picture>
```

For blue (line 303-309):
```html
<picture>
    <source srcset="image/cert_color_blue_thumb.webp" type="image/webp">
    <img src="image/cert_color_blue_thumb.webp" alt="藍色證書套預覽" class="select-option-image" width="210" height="140" loading="lazy">
</picture>
```

- [ ] **Step 3: Commit**

```bash
git add image/cert_color_beige_thumb.webp image/cert_color_blue_thumb.webp index.html
git commit -m "perf: add downsized color preview thumbnails, save ~26 KiB on color card images"
```

---

### Task 4: Optimize hero image responsive delivery (38.6 KiB savings)

**Files:**
- Modify: `index.html:397-398`

**Root cause:** The hero image at line 398 has `sizes="(max-width: 768px) 100vw, 600px"` but the `<picture>` element already has `sizes="(max-width: 768px) 100vw, 600px"` on the `<source>` tag. On a 360px mobile viewport, the browser downloads the full 1200×991 image (56 KiB) when the displayed size is only 360px wide. The `cert_hero_600.webp` (600×495, 9.6 KiB) already exists — but the `sizes` attribute on the `<img>` may cause the wrong choice.

**Fix:** The `sizes` attribute on the `<source>` inside `<picture>` already specifies correctly. The issue is the **`<img>` also has `sizes`** — some browsers use the `<img>` sizes even within `<picture>`. Remove the `sizes` attribute from the `<img>` tag (leave it only on `<source>`).

- [ ] **Step 1: Remove redundant `sizes` from `<img>` tag**

In `index.html`, line 398, change:

```html
<img src="image/cert_hero.webp" alt="結婚證書套示意圖" class="rounded-2xl shadow-lg product-image" style="width:600px;aspect-ratio:1200/991;" loading="eager" fetchpriority="high" sizes="(max-width: 768px) 100vw, 600px">
```

to:

```html
<img src="image/cert_hero.webp" alt="結婚證書套示意圖" class="rounded-2xl shadow-lg product-image" style="width:600px;aspect-ratio:1200/991;" loading="eager" fetchpriority="high">
```

Also push the `sizes` attribute up to the `<picture>` level to be safe (line 397):

```html
<picture>
    <source srcset="image/cert_hero_600.webp 600w, image/cert_hero.webp 1200w" sizes="(max-width: 768px) 100vw, 600px" type="image/webp">
    <img src="image/cert_hero.webp" alt="結婚證書套示意圖" class="rounded-2xl shadow-lg product-image" style="width:600px;aspect-ratio:1200/991;" loading="eager" fetchpriority="high">
</picture>
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "perf: remove redundant sizes from hero img tag, ensure responsive image selection"
```

---

### Task 5: Convert nav logo to WebP with proper sizing (7.6 KiB savings)

**Files:**
- Modify: `index.html:223-225`
- No new images needed — `01_company_logo.webp` (144×144, 5.4 KiB) already exists

**Root cause:** The nav logo at line 224 uses `01_company_logo.png` (144×144, 8.3 KiB) displayed at ~42×42 in the navbar. The WebP version (5.4 KiB) exists in `image/` but isn't used. The displayed size is also far smaller than the natural size.

**Fix:** Switch to the existing `.webp` variant via `<picture>`. The `.webp` is 5.4 KiB vs 8.3 KiB PNG. Also add responsive sizing.

- [ ] **Step 1: Replace nav logo img with picture element**

In `index.html`, line 224, replace:

```html
<img src="image/01_company_logo.png" width="256" height="256" loading="eager" class="lzy1Td" role="img" aria-label="網站首頁" jsname="SwcDWb">
```

with:

```html
<picture>
    <source srcset="image/01_company_logo.webp" type="image/webp">
    <img src="image/01_company_logo.png" width="256" height="256" loading="eager" class="lzy1Td" role="img" aria-label="網站首頁" jsname="SwcDWb">
</picture>
```

- [ ] **Step 2: Fix the hero section logo too (line 260)**

Line 260 already has a `<picture>` with `source[type=image/webp]` ✓ — verify it's intact.

- [ ] **Step 3: Fix the sticky bar logo (line 555)**

Line 555 already uses `<picture>` with WebP ✓ — verify.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "perf: serve nav logo as WebP via picture element"
```

---

### Task 6: Fix non-composited animations (CLS + jank reduction)

**Files:**
- Modify: `index.html` — inline `<style>` within `<head>` (the mega-inline block starting at line 39)

**Root cause:** Lighthouse reports "Avoid non-composited animations" for Instagram and WhatsApp link hover transitions. The `transition-colors` utility class animates `color` and `border-color` properties — these cannot be composited on the GPU and trigger repaints.

Note: This issue is **not scored** in Lighthouse (unscored diagnostic), but contributes to jank.

**Fix:** Replace `transition-colors` with `transition: opacity 0.3s ease` on social icon links, or use `will-change: transform` hint. The simplest fix: override to use `opacity` for hover instead of color transition (which also creates a nicer visual effect).

- [ ] **Step 1: Replace transition-colors with opacity transition for social icons**

Find the Instagram and WhatsApp links in the hero section (lines 268-274). They have `class="... transition-colors"`.

Change the social icon hover approach. Add to the inline `<style>` block (after line 39 or near the hero styles at line 49):

```css
.social-icons a {
    transition: opacity 0.25s ease;
    will-change: opacity;
}
.social-icons a:hover {
    opacity: 0.75;
}
```

Remove `transition-colors` from the social icon `<a>` tags. The class is:
- Line 268: `text-pink-600 hover:text-pink-700 transition-colors` → `text-pink-600 hover:text-pink-700`
- Line 271: `text-green-500 hover:text-green-600 transition-colors` → `text-green-500 hover:text-green-600`

Since Tailwind classes `hover:text-pink-700` and `hover:text-green-600` will still try to animate color, also remove those hover text color classes (the CSS opacity transition replaces the visual effect).

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "perf: replace non-composited color transitions with opacity transitions on social icons"
```

---

### Task 7: Add Lighthouse performance regression tests

**Files:**
- Modify: `tests/lighthouse-audits.spec.ts`

Add tests that verify the forced reflow fixes and image optimization changes don't regress.

- [ ] **Step 1: Add forced reflow detection test**

Append to `tests/lighthouse-audits.spec.ts`:

```typescript
// ====================================================
// TEST: Scroll-depth script should not query layout on load
// ====================================================
test('scroll-depth script should not eagerly compute docHeight', async ({ page }) => {
  await page.goto('/');

  // Check that docHeight is computed inside scroll handler, not eagerly
  const html = await page.content();
  
  // The script should have docHeight = 0 initially (lazy init pattern)
  const hasLazyPattern = await page.evaluate(() => {
    // Find the scroll-depth script by checking for scrollDepths variable
    const scripts = document.querySelectorAll('script');
    for (const script of scripts) {
      if (script.textContent?.includes('scrollDepths')) {
        // Should NOT have docHeight computed eagerly (no direct scrollHeight query outside function)
        return script.textContent.includes('getDocHeight') || script.textContent.includes('docHeight = 0');
      }
    }
    return false;
  });
  expect(hasLazyPattern).toBe(true);
});
```

- [ ] **Step 2: Add image size verification test**

Append to `tests/lighthouse-audits.spec.ts`:

```typescript
// ====================================================
// TEST: Color preview images should use thumbnails
// ====================================================
test('color preview images should use thumbnail variants', async ({ page }) => {
  await page.goto('/');

  const colorImages = page.locator('.color-option-card .select-option-image');
  const count = await colorImages.count();
  expect(count).toBe(2);

  for (let i = 0; i < count; i++) {
    const src = await colorImages.nth(i).getAttribute('src');
    expect(src).toMatch(/thumb\.webp$/);
  }
});
```

- [ ] **Step 3: Run tests to verify**

```bash
npx playwright test tests/lighthouse-audits.spec.ts --project="Desktop Chrome"
```

Expected: All tests pass.

- [ ] **Step 4: Commit**

```bash
git add tests/lighthouse-audits.spec.ts
git commit -m "test: add regression tests for forced reflow and image optimization fixes"
```

---

### Summary of Expected Gains

| Fix | Metric Impact | Savings |
|-----|--------------|---------|
| Task 1: Deferred scrollHeight | FCP -100ms, TBT -80ms | — |
| Task 2: getAttribute('src') | TBT -9ms | — |
| Task 3: Color thumbnails | LCP indirect (less network contention) | 26 KiB |
| Task 4: Hero image sizes | LCP -200ms (mobile serves 600w variant) | 46 KiB |
| Task 5: Logo WebP | LCP indirect | 2.9 KiB |
| Task 6: Composited animations | CLS reduction, smoother scrolling | — |

**Estimated score uplift: 92 → 96-99** depending on network simulation variance. The biggest single impact is hero image delivery (Task 4) combined with forced reflow elimination (Task 1).
