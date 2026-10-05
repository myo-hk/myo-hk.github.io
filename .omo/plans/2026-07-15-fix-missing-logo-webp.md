# Fix Missing Company Logo WebP Across Site

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the missing `image/01_company_logo.webp` file and verify it's served correctly, fixing broken logos across all 8 pages.

**Root Cause:** Commit `184406f` updated all `<picture>`/meta/JSON-LD references to point to `01_company_logo.webp` but never generated the actual `.webp` file. The PNG (144×144, 8KB) exists but the WebP version doesn't. Cloudflare Pages returns a 200 HTML page (its SPA fallback) instead of the image, so `<picture>` elements pick the WebP source, get HTML, and show broken images.

**Tech Stack:** cwebp (v1.6.0), Cloudflare Pages, static HTML

**Affected files (30 references total):**
| File | References | Locations |
|------|-----------|-----------|
| `index.html` | 4 | og:image, JSON-LD, hero `<picture>` (L260), sticky bar `<picture>` (L555) |
| `v2.html` | 6 | og:image, 2× JSON-LD, nav `<picture>` (L1791), hero `<picture>` (L1825), sticky bar `<picture>` (L2073) |
| `blog/index.html` | 4 | og:image, twitter:image, JSON-LD, nav `<picture>` (L237) |
| `poster.html` | 3 | 2× JSON-LD, footer `<picture>` (L933) |
| `privacy.html` | 4 | og:image, twitter:image, nav `<picture>` (L209), footer `<picture>` (L270) |
| `terms.html` | 4 | og:image, twitter:image, nav `<picture>` (L209), footer `<picture>` (L267) |
| `faq.html` | 4 | og:image, twitter:image, nav `<picture>` (L415), footer `<picture>` (L524) |
| `heic-converter.html` | 1 | og:image (L24) |

**Note:** `index.html` nav logo at L224 uses direct `<img src="01_company_logo.png">` (no `<picture>`) — this is the only nav that works. All other pages use `<picture>` with the missing WebP and the logo in their nav is broken.

---

### Task 1: Generate 01_company_logo.webp from PNG

**Files:**
- Create: `image/01_company_logo.webp`
- Source: `image/01_company_logo.png` (144×144, 8KB, 8-bit colormap, 72 DPI)

- [ ] **Step 1.1: Convert PNG to WebP**

```bash
cd /Users/bubu/Documents/Github/myo-hk
cwebp -q 80 image/01_company_logo.png -o image/01_company_logo.webp
```

Expected output:
```
Saving file 'image/01_company_logo.webp'
File:      image/01_company_logo.webp
Size:      XXXX bytes
```

- [ ] **Step 1.2: Verify the WebP file**

```bash
file image/01_company_logo.webp
identify image/01_company_logo.webp 2>/dev/null || sips -g all image/01_company_logo.webp
```

Expected: `RIFF (little-endian) data, Web/P image, VP8 encoding, 144x144`  
WebP should be significantly smaller than 8KB PNG (target: ~3-5KB at quality 80).

---

### Task 2: Verify All 30 References Are Already Correct

**Files:** Read-only verification — no edits needed

The HTML references are already correct (they point to `01_company_logo.webp` and have PNG fallbacks). We just need the file to exist. Verify no path typos:

- [ ] **Step 2.1: Spot-check the `<picture>` pattern on index.html**

Read `index.html` lines 258-262 and 553-556 to confirm `srcset="image/01_company_logo.webp"` uses relative path (matches `src="image/01_company_logo.png"`).

No code changes needed — paths are already correct.

---

### Task 3: Generate and Serve Correctly via Local Dev Server

- [ ] **Step 3.1: Start local HTTP server and verify**

```bash
cd /Users/bubu/Documents/Github/myo-hk
python3 -m http.server 8000 --bind 127.0.0.1
```

In another terminal:
```bash
curl -sI http://127.0.0.1:8000/image/01_company_logo.webp | grep -i 'content-type\|http/'
```

Expected: `content-type: image/webp` (Python's `http.server` infers MIME from extension).

- [ ] **Step 3.2: Verify the file renders in browser**

Open `http://127.0.0.1:8000/` and visually confirm:
- Hero logo in header section displays correctly
- Sticky bar logo (resize to mobile <768px) displays correctly
- No broken image icons

---

### Task 4: Deploy to GitHub Pages

- [ ] **Step 4.1: Stage, commit, and push**

```bash
cd /Users/bubu/Documents/Github/myo-hk
git add image/01_company_logo.webp
git commit -m "fix: add missing 01_company_logo.webp for <picture> elements"
git push origin main
```

**Note:** Work on `main` branch since all previous changes (PageSpeed fix in `6eeb487`, pricing merge in `3955748`) are already on `main`. If you prefer a dedicated branch, use `fix/missing-logo-webp`.

---

### Task 5: Verify on Live Site

- [ ] **Step 5.1: Wait for Cloudflare Pages deployment** (~1-2 min)

- [ ] **Step 5.2: Verify Content-Type header**

```bash
curl -sI https://myo-makeyourown.pages.dev/image/01_company_logo.webp | grep -i 'content-type\|http/'
```

Expected: `HTTP/2 200` + `content-type: image/webp`  
(Failure: `content-type: text/html` means file still missing or deployment incomplete)

- [ ] **Step 5.3: Verify hero logo renders**

```bash
curl -s https://myo-makeyourown.pages.dev/image/01_company_logo.webp | file -
```

Expected: `RIFF (little-endian) data, Web/P image`

- [ ] **Step 5.4: Verify page loads without broken images**

Open `https://myo-makeyourown.pages.dev/` in a browser. Check for broken image icons in:
- Hero section (centered logo below nav)
- Sticky conversion bar (bottom of page on mobile, inspect with F12 responsive mode)
- Open browser console — verify no image loading errors related to `01_company_logo.webp`

---

### Task 6: Cross-page Verification (blog + secondary pages)

- [ ] **Step 6.1: Check blog nav logo**

Open `https://myo-makeyourown.pages.dev/blog/` — the nav logo in the top-left should now display correctly (uses `<picture>` with WebP source).

- [ ] **Step 6.2: Check faq.html, privacy.html, terms.html**

Quick spot-check: Open 2-3 pages and confirm their nav logo and footer logo are no longer broken.

---

### Task 7: Clean Up Branch (if not using main)

- [ ] **Step 7.1: If a feature branch was used, create PR and merge**

```bash
gh pr create --repo chungyuicheung/myo-hk --base main --head ashashash001001-stack:fix/missing-logo-webp \
  --title "fix: add missing 01_company_logo.webp" \
  --body "Root cause: commit 184406f updated all <picture>/meta/JSON-LD references to .webp but never generated the actual file. The .webp is referenced across 8 HTML files (30 occurrences)."
```
