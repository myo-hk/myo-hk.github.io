# Plan D: Duplicate Homepage Resolution

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve duplicate content risk between index.html (original homepage) and v2.html (redesigned homepage) by adding canonical tags and clarifying which version Google should index.

**Architecture:** Both files are static HTML in the site root. The fix is minimal — add a `<link rel="canonical">` pointing from v2.html to index.html, plus a `noindex` meta tag on v2.html if it should not be indexed independently. Update the sitemap priority for v2.html.

**Tech Stack:** HTML5 meta tags

---

### Task 1: Decide on Strategy

Two options exist. Choose one before proceeding:

**Option A: v2.html is an alternative design (not the canonical version)**
- Keep `index.html` as canonical homepage
- Add `<link rel="canonical" href="https://myo-hk.github.io/">` to `v2.html`
- Keep `v2.html` indexable (it's a variation, users may find it useful)
- Update sitemap priority: `v2.html` → `0.3`

**Option B: v2.html is a replacement/experiment**
- Add `<link rel="canonical" href="https://myo-hk.github.io/">` to `v2.html`
- Add `<meta name="robots" content="noindex, follow">` to `v2.html`
- Remove `v2.html` from sitemap entirely

> This plan implements **Option A** (safer, preserves both pages). Adjust to Option B if preferred.

- [ ] **Step 1: Confirm the strategy decision**

```bash
grep -c 'v2' sitemap.xml
```
Expected: confirms v2.html is currently in the sitemap (with priority 0.5).

---

### Task 2: Add Canonical Tag to v2.html

**Files:**
- Modify: `v2.html`

- [ ] **Step 1: Read v2.html head section**

```bash
grep -n 'canonical\|noindex\|robots' v2.html
```
Expected: Current state of canonical/tags (likely none for v2.html).

- [ ] **Step 2: Add canonical link before `</head>`**

Locate `</head>` in v2.html. Insert:

```html
<link rel="canonical" href="https://myo-hk.github.io/">
```

- [ ] **Step 3: Verify the canonical link is present**

```bash
grep 'canonical' v2.html
```
Expected: `<link rel="canonical" href="https://myo-hk.github.io/">`

- [ ] **Step 4: Commit**

```bash
git add v2.html
git commit -m "fix(seo): add canonical link from v2.html to index.html to resolve duplicate content"
```

---

### Task 3: Update Sitemap Priority for v2.html

**Files:**
- Modify: `scripts/generate_sitemap.py`

- [ ] **Step 1: Read the current priority for v2.html**

```bash
grep 'v2.html' scripts/generate_sitemap.py
```
Expected: `"v2.html": {"priority": "0.5", "changefreq": "monthly"}`

- [ ] **Step 2: Change v2.html priority to 0.3**

In `scripts/generate_sitemap.py`, change:
```python
"v2.html": {"priority": "0.5", "changefreq": "monthly"},
```
to:
```python
"v2.html": {"priority": "0.3", "changefreq": "monthly"},
```

- [ ] **Step 3: Regenerate the sitemap**

```bash
python3 scripts/generate_sitemap.py
```

- [ ] **Step 4: Verify the change**

```bash
grep -A2 'v2' sitemap.xml
```
Expected: Shows `<priority>0.3</priority>`.

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_sitemap.py sitemap.xml
git commit -m "fix(seo): lower v2.html sitemap priority to 0.3 (alternative homepage)"
```
