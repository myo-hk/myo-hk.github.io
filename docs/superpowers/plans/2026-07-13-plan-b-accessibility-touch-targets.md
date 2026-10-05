# Plan B: Accessibility Touch Target Size Fix

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the "Touch targets do not have sufficient size or spacing" accessibility failure on `index.html` and `v2.html`, raising mobile Accessibility from 85 → 90+.

**Architecture:** The PageSpeed Insights report identifies Swiper pagination bullets (`.swiper-pagination-bullet`) as the failing elements on mobile. These are 8px circles by default, well below the 48×48px minimum touch target size required by WCAG 2.2 (Target Size, SC 2.5.8). The fix applies CSS to meet the minimum size without breaking the Swiper layout.

**Tech Stack:** Vanilla CSS (no build tools needed)

**Files affected:**
- `index.html` — add CSS block in existing `<style>` section
- `v2.html` — add CSS block in existing `<style>` section

---

### Background

The Swiper pagination render function creates `<span class="swiper-pagination-bullet">` elements. Default Swiper CSS sets:
- `width: 8px; height: 8px;`
- No margin/padding between bullets

WCAG 2.2 Target Size minimum is **24×24px** (for CSS pixels), with an exception for inline/spaced elements if adjacent targets have at least 4px spacing. The safest fix is to enlarge the bullets to 24×24px with adequate spacing.

---

### Task 1: Fix Swiper pagination bullet size on `index.html`

**Files:**
- Modify: `index.html` — insert CSS after the existing Swiper-related custom styles (around line 280)

- [ ] **Step 1: Locate the insertion point**

Find line 280 in `index.html` (the end of the existing `.swiper-pagination-bullet-active` block at lines 280-281):

```css
.swiper-pagination-bullet-active {
    background: #CD853F;
}
```

- [ ] **Step 2: Add touch-target-size CSS after the existing Swiper pagination rule**

After line 281, insert:

```css
/* -- Accessibility: touch target size ≥ 24×24px (WCAG 2.2 SC 2.5.8) -- */
.swiper-pagination-bullet {
    width: 24px !important;
    height: 24px !important;
    margin: 0 6px !important;
}
```

> **Why `!important`:** Swiper injects its own CSS via JS which takes specificity priority. The `!important` flags ensure our fix overrides the injected defaults.

- [ ] **Step 3: Verify the fix visually**

Run: `open index.html`

Resize browser to mobile width (412px). Open DevTools and inspect a pagination bullet. Confirm:
- Computed width: 24px
- Computed height: 24px
- The bullets are visually well-spaced and easy to tap

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "fix(a11y): enlarge swiper pagination bullets to 24px for WCAG touch target compliance"
```

---

### Task 2: Fix Swiper pagination bullet size on `v2.html`

**Files:**
- Modify: `v2.html` — insert CSS after the existing Swiper-related custom styles (around line 617)

- [ ] **Step 1: Locate the insertion point**

Find line 617 in `v2.html`:

```css
.swiper-pagination-bullet-active {
    background: var(--color-primary);
}
```

- [ ] **Step 2: Add touch-target-size CSS**

After that line, insert:

```css
/* -- Accessibility: touch target size ≥ 24×24px (WCAG 2.2 SC 2.5.8) -- */
.swiper-pagination-bullet {
    width: 24px !important;
    height: 24px !important;
    margin: 0 6px !important;
}
```

- [ ] **Step 3: Verify the fix visually**

Run: `open v2.html` at mobile width. Inspect pagination bullets to confirm 24×24px computed size.

- [ ] **Step 4: Commit**

```bash
git add v2.html
git commit -m "fix(a11y): enlarge swiper pagination bullets to 24px on v2.html"
```

---

### Task 3: Run accessibility validation

- [ ] **Step 1: Run Lighthouse accessibility audit**

Open Chrome DevTools > Lighthouse > Category: Accessibility > Generate report (mobile).

Expected: The "Touch targets" audit should now show **0 failures** (previously 1+). Accessibility score should increase from 85 → 90+ (the exact delta depends on other passing/failing audits since scoring is weighted).

- [ ] **Step 2: Run Playwright tests**

```bash
npm test
```

Expected: All tests pass.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: verify a11y fix with Lighthouse and Playwright tests"
```
