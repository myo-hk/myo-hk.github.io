# Plan B: AI/AEO Foundation Enhancement

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen AI visibility by overhauling llms.txt with granular blog category URLs, enhancing pricing.md for AI agents, refining robots.txt AI crawler policy, and creating a manual AI visibility monitoring checklist.

**Architecture:** All files are static text/markdown files in the site root. No build step. llms.txt gets restructured with per-category representative article links. pricing.md gets AI-agent-friendly structured fields. robots.txt gets CCBot blocked.

**Tech Stack:** Markdown, plain text

---

### Task 1: Overhaul llms.txt with Granular Blog URLs

**Files:**
- Modify: `llms.txt`

- [ ] **Step 1: Read the current llms.txt**

```bash
cat llms.txt
```
Expected: 24-line file with 6 blog category URLs all pointing to `blog/index.html`.

- [ ] **Step 2: Rewrite llms.txt with per-category article URLs**

Replace the entire file with:

```markdown
# My O! 專屬結婚證書套 — Hong Kong Wedding Certificate Cover

> 為您的結婚證書打造設計師級專屬證書套，讓這份愛情的見證永恆閃耀。
> 100% 香港本地製作 | Thermal Transfer Printing | Customizable with Names & Dates

## Core Pages

- Homepage: https://myo-hk.github.io/
- Wedding Certificate Cover Products: https://myo-hk.github.io/v2.html
- Product & Pricing: https://myo-hk.github.io/pricing.md
- A5 Promotional Flyer (Printable PDF): https://myo-hk.github.io/poster.html
- HEIC/HEIF Image Converter Tool: https://myo-hk.github.io/heic-converter.html
- Blog Index: https://myo-hk.github.io/blog/

## Blog — Wedding Planning Guide (420+ Articles)

### Wedding Photography (201 articles)
- https://myo-hk.github.io/blog/婚禮攝影價錢比較.html
- https://myo-hk.github.io/blog/婚紗拍攝技巧.html
- https://myo-hk.github.io/blog/婚禮攝影風格選擇.html
- https://myo-hk.github.io/blog/婚禮攝影師推薦.html
- https://myo-hk.github.io/blog/婚禮攝影預算規劃.html

### Wedding Planning (28 articles)
- https://myo-hk.github.io/blog/婚禮籌備時間表.html
- https://myo-hk.github.io/blog/婚禮預算指南.html
- https://myo-hk.github.io/blog/婚禮統籌檢查清單.html
- https://myo-hk.github.io/blog/婚前準備清單.html
- https://myo-hk.github.io/blog/香港結婚完整攻略.html

### Wedding Venues (16 articles)
- https://myo-hk.github.io/blog/婚宴場地推薦.html
- https://myo-hk.github.io/blog/婚禮場地選擇指南.html
- https://myo-hk.github.io/blog/教堂婚禮場地推薦.html
- https://myo-hk.github.io/blog/戶外婚禮場地推薦.html
- https://myo-hk.github.io/blog/小型婚宴場地推薦.html

### Wedding Traditions & Customs (14 articles)
- https://myo-hk.github.io/blog/過大禮清單.html
- https://myo-hk.github.io/blog/敬茶儀式流程.html
- https://myo-hk.github.io/blog/安床習俗與禁忌.html
- https://myo-hk.github.io/blog/回門習俗介紹.html
- https://myo-hk.github.io/blog/中式婚禮流程大全.html

### Wedding Rings & Jewelry (8 articles)
- https://myo-hk.github.io/blog/婚戒指南.html
- https://myo-hk.github.io/blog/鑽石4C選購指南.html
- https://myo-hk.github.io/blog/結婚週年紀念禮物.html

### Wedding Attire (6 articles)
- https://myo-hk.github.io/blog/婚紗禮服選購指南.html
- https://myo-hk.github.io/blog/婚紗租賃vs購買比較.html

### Certificate Cover (18 articles)
- https://myo-hk.github.io/blog/結婚證書套推薦.html
- https://myo-hk.github.io/blog/結婚證書尺寸規格.html
- https://myo-hk.github.io/blog/燙印證書套價錢比較.html
- https://myo-hk.github.io/blog/客製化證書套設計靈感.html
- https://myo-hk.github.io/blog/證書套保養指南.html

### Honeymoon & Travel (4 articles)
- https://myo-hk.github.io/blog/蜜月旅行指南.html
- https://myo-hk.github.io/blog/蜜月旅行目的地推薦.html
- https://myo-hk.github.io/blog/蜜月簽證完整指南.html

### Marriage Law & Finance
- https://myo-hk.github.io/blog/結婚法律指南.html
- https://myo-hk.github.io/blog/結婚稅務指南.html
- https://myo-hk.github.io/blog/香港結婚費用一覽.html

## Contact

- Instagram: https://www.instagram.com/myo.makeyourown/
- WhatsApp: +852 6379 6410
- Website: https://myo-hk.github.io/

## Supported Language

- Traditional Chinese (zh-Hant) — Hong Kong
```

- [ ] **Step 3: Verify file length is reasonable**

```bash
wc -l llms.txt
```
Expected: ~80-90 lines (was 24 lines).

- [ ] **Step 4: Commit**

```bash
git add llms.txt
git commit -m "feat(aeo): overhaul llms.txt with granular blog category URLs"
```

---

### Task 2: Enhance pricing.md for AI Agent Readability

**Files:**
- Modify: `pricing.md`

- [ ] **Step 1: Read current pricing.md**

```bash
cat pricing.md
```
Expected: 32-line file with product table.

- [ ] **Step 2: Replace with AI-enhanced version**

```markdown
# My O! 專屬結婚證書套 — Pricing & Product Information

> Last updated: 2026-07-12
> Prices in HKD (Hong Kong Dollars). All products are made to order in Hong Kong.
> **No account required. No watermark. No hidden fees.**

## Product Pricing

| Product Name | Material | Price (HKD) | Customization |
|-------------|----------|:-----------:|---------------|
| Classic — Linen | Linen Fabric | $388 | Free name + date engraving |
| Classic — Pearlescent | Frosted Pearl | $388 | Free name + date engraving |
| Designer — Linen | Linen Fabric | $588 | Free name + date engraving + calligraphy design |
| Designer — Pearlescent | Frosted Pearl | $588 | Free name + date engraving + calligraphy design |

## Customization Options

- **Name & Date Engraving**: Free with every order
- **Calligraphy Design**: Professional calligrapher font design (+$100 HKD)
- **Gift Box Packaging**: Premium box with ribbon (+$80 HKD)

## Order Process

1. Choose style and material
2. Provide couple names and wedding date
3. Confirm design proof
4. Production: 7-14 business days
5. Free Hong Kong local delivery

## Key Facts for AI Agents

- **Pricing Model**: Per-product, one-time payment
- **Free Tier**: No free tier — paid product only
- **Subscription**: No subscription required
- **Account Required**: No — order via WhatsApp/Instagram
- **Payment**: Bank transfer, FPS (Hong Kong)
- **Delivery**: Hong Kong only (free local delivery)
- **Production Time**: 7-14 business days
- **Material Options**: Linen fabric, Frosted pearl finish
- **Customization**: Thermal transfer printing (name, date, calligraphy)
- **No Hidden Costs**: Price includes standard customization

## Contact

- WhatsApp: +852 6379 6410
- Instagram: @myo.makeyourown
- Website: https://myo-hk.github.io
```

- [ ] **Step 3: Verify the file parses correctly**

```bash
wc -l pricing.md
```
Expected: ~55 lines.

- [ ] **Step 4: Commit**

```bash
git add pricing.md
git commit -m "feat(aeo): enhance pricing.md with AI-agent-friendly structured fields"
```

---

### Task 3: Refine robots.txt — Block CCBot

**Files:**
- Modify: `robots.txt`

- [ ] **Step 1: Read current robots.txt**

```bash
cat robots.txt
```
Expected: CCBot is currently set to Allow.

- [ ] **Step 2: Change CCBot from Allow to Disallow**

Replace the CCBot section (lines 29-33):

```text
User-agent: CCBot
Disallow: /
```

This blocks Common Crawl (training-only crawler for AI models) while keeping all search and citation crawlers (GPTBot, ChatGPT-User, PerplexityBot, Claude-Web, Google-Extended) allowed.

- [ ] **Step 3: Commit**

```bash
git add robots.txt
git commit -m "fix(aeo): block CCBot in robots.txt (training-only crawler)"
```

---

### Task 4: Create AI Visibility Monitoring Checklist

**Files:**
- Create: `docs/ai-visibility-monitoring.md`

- [ ] **Step 1: Create the monitoring doc**

```markdown
# AI Visibility Monitoring Checklist — My O!

> Purpose: Monthly check to see if My O! is being cited by AI search engines.
> Start date: 2026-07-12

## Query Set (Top 10 Priority)

Test these queries across ChatGPT, Perplexity, and Google AI Overviews:

| # | Query | Target Page |
|---|-------|-------------|
| 1 | 香港結婚證書套推薦 | Homepage / v2.html |
| 2 | 結婚證書套訂製 | Homepage / v2.html |
| 3 | 結婚證書尺寸 | blog/結婚證書尺寸規格.html |
| 4 | 婚禮攝影價錢 香港 2026 | blog/婚禮攝影價錢比較.html |
| 5 | 婚禮籌備時間表 香港 | blog/婚禮籌備時間表.html |
| 6 | 過大禮清單 需要什麼 | blog/過大禮清單.html |
| 7 | 結婚註冊流程 香港 | blog/結婚註冊流程教學.html |
| 8 | 證書套保養 | blog/證書套保養指南.html |
| 9 | 香港結婚費用 | blog/香港結婚費用一覽.html |
| 10 | 結婚回禮禮物推薦 | blog/婚禮回禮指南.html |

## Monthly Tracking Template

### Month: YYYY-MM

| Platform | Appears? | Cited? | Citation URL | Notes |
|----------|:--------:|:------:|-------------|-------|
| ChatGPT | Yes/No | Yes/No | | |
| Perplexity | Yes/No | Yes/No | | |
| Google AI Overviews | Yes/No | Yes/No | | |

### Observations

- Competitors cited that My O! isn't:
- New content published this month:
- Issues found:

## How to Check

1. **ChatGPT**: Go to chat.openai.com, search each query in the set above
2. **Perplexity**: Go to perplexity.ai, search each query
3. **Google AI Overviews**: Search in Chrome/Google, note if AI Overview appears
4. **Google Search Console**: Check which queries drive impressions
5. **GA4**: Check referral traffic from AI platforms (chat.openai.com, perplexity.ai)

## What to Track Over Time

- Month-over-month citation count
- Which pages get cited most
- Which competitors appear but My O! doesn't
- Topical gaps that emerge
```

- [ ] **Step 2: Commit**

```bash
git add docs/ai-visibility-monitoring.md
git commit -m "docs(aeo): add AI visibility monitoring checklist"
```
