# Web Video Presentations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build five complete web video presentations for the My O! Hong Kong wedding site, each with article, script, outline, and React/TS chapter components following the existing scaffold and kraft-paper theme.

**Architecture:** Each presentation lives in its own directory under `presentations/`. Content files (`article.md`, `script.md`, `outline.md`) are static markdown. Chapter components are React TSX files registered in `src/registry/chapters.ts`. The project uses Vite, React, TypeScript, and a shared CSS theme.

**Tech Stack:** Vite, React, TypeScript, CSS modules, Node.js, npm.

---

### Task 1: Prepare shared resources

**Files:**
- Modify: `presentations/common/theme.css` (create if not exists) to define kraft-paper colors.
- Create: `presentations/common/README.md` describing theme usage.

- [ ] **Step 1: Create theme.css with kraft colors**
```css
:root {
  --bg: #f5e6d3; /* kraft paper */
  --text: #2e2e2e;
  --accent: #4b6b44; /* forest green */
}
```
- [ ] **Step 2: Commit theme.css**
```bash
git add presentations/common/theme.css
git commit -m "chore: add kraft-paper theme colors"
```

### Task 2: Video 11 – Certificate Cover Comparison

**Files:**
- Create: `presentations/11-certificate-cover-comparison/article.md`
- Create: `presentations/11-certificate-cover-comparison/script.md`
- Create: `presentations/11-certificate-cover-comparison/outline.md`
- Create chapter component files under `presentations/11-certificate-cover-comparison/src/chapters/01-intro/Chapter1.tsx` etc.
- Modify: `presentations/11-certificate-cover-comparison/src/registry/chapters.ts`

- [ ] **Step 1: Extract key data from source HTML `blog/結婚證書套推薦.html`** (prices, material list, pros/cons).
- [ ] **Step 2: Write article.md with table of products, HK$ prices, material properties.**
- [ ] **Step 3: Write script.md (~1700 chars) with hook, comparison narrative, CTA.**
- [ ] **Step 4: Write outline.md with 6 chapters (hook, material intro, product A, product B, side‑by‑side comparison, CTA).**
- [ ] **Step 5: Scaffold chapter folder `src/chapters/01-intro/` and create Chapter1.tsx and Chapter1.css following pattern.**
- [ ] **Step 6: Add narration strings in `narrations.ts`.**
- [ ] **Step 7: Register Chapter1 in `registry/chapters.ts`.**
- [ ] **Step 8: Run `npm install && npx tsc --noEmit` in the presentation folder, fix any TS errors.**
- [ ] **Step 9: Commit all changes for video 11.**

### Task 3: Video 12 – Customization Heat Transfer

**Files:** similar pattern under `presentations/12-customization-heat-transfer/`.
- [ ] **Step 1: Pull data from `blog/燙印證書套價錢.html` and `blog/燙印證書套價錢比較.html`.**
- [ ] **Step 2: Write article.md with heat‑transfer process, price ranges, visual examples.**
- [ ] **Step 3: Write script.md (1500‑2000 chars) with hook about personalizing certificates.**
- [ ] **Step 4: Write outline.md (5‑7 chapters).**
- [ ] **Step 5‑9: Scaffold chapters, narrations, register, compile, commit.**

### Task 4: Video 13 – Cover Sizing Guide

**Files:** under `presentations/13-cover-sizing-guide/`.
- [ ] **Step 1: Extract sizing tables from `blog/證書套尺寸指南.html`.**
- [ ] **Step 2: Write article.md with measurement guide, printable templates links.**
- [ ] **Step 3: Write script.md with hook about perfect fit.**
- [ ] **Step 4: Write outline.md.**
- [ ] **Step 5‑9: Scaffold chapters, narrations, register, compile, commit.**

### Task 5: Video 14 – Velvet vs Linen Cover

**Files:** under `presentations/14-velvet-vs-linen-cover/`.
- [ ] **Step 1: Pull comparison data from `blog/絲絨vs亞麻布證書套.html` and `blog/證書套材質比較.html`.**
- [ ] **Step 2: Write article.md with tactile description, pros/cons, price.**
- [ ] **Step 3: Write script.md with hook about texture choice.**
- [ ] **Step 4: Write outline.md.**
- [ ] **Step 5‑9: Scaffold chapters, narrations, register, compile, commit.**

### Task 6: Video 15 – Cover Preservation Guide

**Files:** under `presentations/15-cover-preservation-guide/`.
- [ ] **Step 1: Extract care tips from `blog/婚禮證書套保養.html` and `blog/證書套保養指南.html`.**
- [ ] **Step 2: Write article.md with cleaning methods, storage ideas, lifespan.**
- [ ] **Step 3: Write script.md with hook about keeping memories pristine.**
- [ ] **Step 4: Write outline.md.**
- [ ] **Step 5‑9: Scaffold chapters, narrations, register, compile, commit.**

### Task 7: Web Search for Latest 2024‑2025 Product Info

- [ ] **Step 1: Search web for each product category (certificate cover, heat‑transfer, velvet, linen) to capture any new models or price updates (2024‑2025).**
- [ ] **Step 2: Append any new data to the respective article.md files.**
- [ ] **Step 3: Commit updates.**

---

**Execution Choice:** Subagent‑Driven Development (recommended) – will dispatch a fresh subagent per task, review between tasks, and ensure each commit passes TypeScript compilation.

**Next Step:** Dispatch subagents for Task 1 onward.
