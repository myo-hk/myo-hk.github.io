# Plan A: Critical Rendering Path Optimization

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove render-blocking third-party scripts from the critical path on `index.html` and `v2.html`, raising mobile Performance from 56 → ~85+ without changing visual behavior.

**Architecture:** Swiper JS/CSS and Tailwind CSS are currently loaded as synchronous `<script>` / `<link>` tags in `<head>`, blocking first paint. All three can be deferred — Swiper JS after the main content script, Tailwind via a small inline preload trick, Swiper CSS via dynamic injection — so the browser renders the hero section before downloading framework code.

**Tech Stack:** Vanilla JS (no build tools needed)

**Files affected:**
- `index.html` — lines 39, 43, 1317
- `v2.html` — lines 38, 42, 2053, 2070

---

### Task 1: Defer Tailwind CSS on `index.html`

**Files:**
- Modify: `index.html:37-39`

**Background:** The `<script src="https://cdn.tailwindcss.com"></script>` on line 39 is render-blocking. Tailwind's Play CDN generates CSS from class scanning — this scan can happen after first paint. We replace synchronous loading with a pattern that loads Tailwind asynchronously without FOUC (Flash of Unstyled Content).

- [ ] **Step 1: Replace synchronous Tailwind script with deferred loading**

Replace lines 37-39 in `index.html`:

```html
<!-- Before -->
    <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">

    <script src="https://cdn.tailwindcss.com"></script>

<!-- After -->
    <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
    <link rel="preload" href="https://cdn.tailwindcss.com" as="script" fetchpriority="low">

    <script>
    (function() {
        var d = document, t = d.createElement('script');
        t.src = 'https://cdn.tailwindcss.com';
        t.async = true;
        // Insert after first stylesheet or at end of head — never blocks
        var ref = d.querySelector('link[rel="stylesheet"]') || d.head.appendChild(d.createElement('meta'));
        d.head.insertBefore(t, ref.nextSibling);
    })();
    </script>
```

> **Note:** Tailwind's Play CDN already handles FOUC internally — it scans the DOM synchronously on load. By using `async`, the scan fires as soon as the script arrives but never blocks the initial HTML parse or style calculation of the inlined `<style>` block.

- [ ] **Step 2: Verify no FOUC**

Run: `open index.html` and reload with DevTools > Network > Slow 3G throttling. Confirm the initial page render shows styled content (the inline `<style>` block on lines 45-200+ covers the body base styles). Tailwind utility classes will apply after ~200ms once the CDN script loads.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "perf: defer tailwind CDN script on index.html to unblock first paint"
```

---

### Task 2: Defer Tailwind CSS on `v2.html`

**Files:**
- Modify: `v2.html:36-38`

- [ ] **Step 1: Apply same deferred loading pattern**

Replace lines 36-38 in `v2.html`:

```html
<!-- Before -->
    <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">

    <script src="https://cdn.tailwindcss.com"></script>

<!-- After -->
    <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
    <link rel="preload" href="https://cdn.tailwindcss.com" as="script" fetchpriority="low">

    <script>
    (function() {
        var d = document, t = d.createElement('script');
        t.src = 'https://cdn.tailwindcss.com';
        t.async = true;
        var ref = d.querySelector('link[rel="stylesheet"]') || d.head.appendChild(d.createElement('meta'));
        d.head.insertBefore(t, ref.nextSibling);
    })();
    </script>
```

- [ ] **Step 2: Verify no FOUC**

Run: `open v2.html` with Slow 3G in DevTools. Confirm inline CSS variables (`--bg-primary`, `--color-primary`, etc.) render immediately and Tailwind utility classes populate after script load.

- [ ] **Step 3: Commit**

```bash
git add v2.html
git commit -m "perf: defer tailwind CDN script on v2.html to unblock first paint"
```

---

### Task 3: Defer Swiper CSS on `index.html`

**Files:**
- Modify: `index.html:43`

**Background:** The Swiper CSS (`swiper-bundle.min.css`) is a render-blocking stylesheet loaded in `<head>`. Since the Swiper carousel is below the hero section (not in the initial viewport above-the-fold), this CSS can be loaded asynchronously.

- [ ] **Step 1: Replace synchronous Swiper CSS link with dynamic injection**

Replace line 43 in `index.html`:

```html
<!-- Before -->
    <link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css" />

<!-- After -->
    <link rel="preload" href="https://unpkg.com/swiper/swiper-bundle.min.css" as="style" fetchpriority="low" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css"></noscript>
```

> **Note:** `preload` with `onload="this.rel='stylesheet'"` is the standard "async CSS" pattern. The browser downloads the CSS at low priority without blocking render, then applies it once downloaded. The `<noscript>` fallback handles users without JS.

- [ ] **Step 2: Verify Swiper carousel still renders correctly**

Run: `open index.html` and confirm the Swiper carousel section (`.swiper` container) loads and functions correctly — slides display, pagination dots work, navigation arrows work.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "perf: async load swiper CSS on index.html using preload stylesheet pattern"
```

---

### Task 4: Defer Swiper CSS on `v2.html`

**Files:**
- Modify: `v2.html:42`

- [ ] **Step 1: Apply same async CSS pattern**

Replace line 42 in `v2.html`:

```html
<!-- Before -->
    <link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css" />

<!-- After -->
    <link rel="preload" href="https://unpkg.com/swiper/swiper-bundle.min.css" as="style" fetchpriority="low" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css"></noscript>
```

- [ ] **Step 2: Verify Swiper carousel renders correctly on v2.html**

Run: `open v2.html` and confirm Swiper section loads and functions correctly.

- [ ] **Step 3: Commit**

```bash
git add v2.html
git commit -m "perf: async load swiper CSS on v2.html using preload stylesheet pattern"
```

---

### Task 5: Defer Swiper JS on `index.html`

**Files:**
- Modify: `index.html:1317`, `index.html:1319-1463`

**Background:** The Swiper JS is currently a synchronous `<script>` tag at the bottom of `<body>` (line 1317). While this is already better than being in `<head>`, it still blocks the `DOMContentLoaded` event from firing, delaying the inline script on lines 1319-1463 that initializes the Swiper instance. We change Swiper JS to load asynchronously and use a "ready" callback pool pattern so the initialization script fires whether Swiper loads before or after it runs.

- [ ] **Step 1: Replace synchronous Swiper JS with async + callback pool**

Replace line 1317 in `index.html`:

```html
    <!-- Before -->
    <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>

    <!-- After -->
    <script async src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
```

- [ ] **Step 2: Wrap Swiper initialization to handle async load race**

The Swiper init code on lines 1343-1460 references the global `Swiper` constructor. Since the script is now async, `Swiper` may not be defined yet when `DOMContentLoaded` fires. Wrap the Swiper init in a polling helper that waits for `window.Swiper` to be available:

Replace lines 1343 (the Swiper init call) in the `DOMContentLoaded` callback:

The existing code near line 1343 looks like:

```javascript
            // 3. 輪播初始化 (Swiper Carousel)
            var swiper = new Swiper('.mySwiper', {
```

Replace that section (from `// 3. 輪播初始化` to before `// 4. Mobile Sticky`) with:

```javascript
            // 3. 輪播初始化 (Swiper Carousel) — async-safe
            function initSwiper() {
                if (typeof Swiper === 'undefined') {
                    // Swiper not loaded yet — retry in 50ms
                    setTimeout(initSwiper, 50);
                    return;
                }
                var swiper = new Swiper('.mySwiper', {
                    slidesPerView: 1.2,
                    spaceBetween: 15,
                    breakpoints: {
                        640: { slidesPerView: 2.2, spaceBetween: 20 },
                        768: { slidesPerView: 3.2, spaceBetween: 20 },
                        1024: { slidesPerView: 4.2, spaceBetween: 20 },
                        1280: { slidesPerView: 5.2, spaceBetween: 20 },
                    },
                    loop: true,
                    pagination: { el: '.swiper-pagination', clickable: true },
                    navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
                    autoplay: { delay: 2500, disableOnInteraction: false },
                });
            }
            initSwiper();
```

- [ ] **Step 3: Verify Swiper works correctly**

Run: `open index.html`. Confirm:
- No console errors ("Swiper is not defined")
- Carousel initializes and is interactive (drag/swipe, pagination click, autoplay)
- Navigation arrows work

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "perf: async load swiper JS on index.html with polling fallback"
```

---

### Task 6: Defer Swiper JS on `v2.html`

**Files:**
- Modify: `v2.html:2053`, `v2.html:2070`, `v2.html:2072-2200+`

**⚠️ Note:** `v2.html` has **two** Swiper script tags — lines 2053 and 2070. This appears to be a bug (duplicate). We clean it up: remove the first (line 2053), async-load the second (line 2070).

- [ ] **Step 1: Remove duplicate Swiper JS (line 2053)**

Delete line 2053 entirely (`<script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>`).

- [ ] **Step 2: Make remaining Swiper JS async**

On line 2070, change:
```html
    <!-- Before -->
    <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>

    <!-- After -->
    <script async src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
```

- [ ] **Step 3: Wrap Swiper initialization in v2.html for async safety**

Find the Swiper init call in v2.html (search for `new Swiper('.mySwiper'` around line 2100+) and wrap it with the same polling pattern:

```javascript
            // 輪播初始化 (Swiper Carousel) — async-safe
            function initSwiper() {
                if (typeof Swiper === 'undefined') {
                    setTimeout(initSwiper, 50);
                    return;
                }
                var swiper = new Swiper('.mySwiper', {
                    // ... keep existing swiper options unchanged ...
                });
            }
            initSwiper();
```

Copy the exact Swiper config options from the existing code — do NOT modify them.

- [ ] **Step 4: Verify Swiper works on v2.html**

Run: `open v2.html`. Confirm no console errors and carousel works.

- [ ] **Step 5: Commit**

```bash
git add v2.html
git commit -m "perf: deduplicate swiper JS on v2.html and load async"
```

---

### Task 7: Verify with PageSpeed Insights

- [ ] **Step 1: Run a local Lighthouse audit**

Run: `npx lighthouse https://myo-makeyourown.pages.dev --view --preset=desktop 2>/dev/null || echo "Install with: npm install -g lighthouse"`

Or use Chrome DevTools > Lighthouse > Generate report for mobile.

Expected: Performance score should increase from 56 to approximately 80+ based on the critical request chain improvements.

- [ ] **Step 2: Run the Playwright tests**

```bash
npm test
```

Expected: All existing Playwright tests pass (no visual regressions from deferred loading).

- [ ] **Step 3: Commit final verification**

```bash
git add -A
git commit -m "chore: verify PageSpeed improvements and test pass"
```
