# 主頁 FAQ + 獨立 FAQ 頁面 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add visible FAQ accordion section to homepage + create dedicated FAQ page + fix footer link, improving SEO keyword coverage and AI Overview citation potential.

**Architecture:** All static HTML. Homepage FAQ uses pure CSS accordion (no JS dependency). FAQ page mirrors existing page template (nav + content + footer). Both pages include FAQPage JSON-LD. Sitemap updated.

**Tech Stack:** HTML5, Vanilla CSS, JSON-LD

**Design doc:** `docs/superpowers/specs/2026-07-13-homepage-faq-seo-design.md`

---

### Task 1: Create faq.html page

**Files:**
- Create: `faq.html`
- Reference: `terms.html` (copy existing page structure pattern)

- [ ] **Step 1: Create faq.html from terms.html template**

Read `terms.html` to understand the page structure, then write `faq.html` following the same navbar, container, and footer pattern.

Content structure (20 Q&A items in 4 categories):

```
產品相關 (Product)
Q1: 證書套的尺寸是否適合香港婚姻登記處的 A4 結婚證書？
Q2: 亞麻布和磨砂珠光材質有什麼分別？
Q3: 設計師款和經典款有什麼分別？
Q4: 證書套可以作為結婚禮物送人嗎？
Q5: 你們有實體店嗎？

訂製相關 (Customization)
Q6: 可以在證書套上印製哪些文字？
Q7: 可以用英文名字和中文名字混合印嗎？
Q8: 可以只訂購一個證書套嗎？
Q9: 確認訂單後可以修改內容嗎？
Q10: 你們的證書套支援海外結婚證書尺寸嗎？

訂購與送貨 (Order & Delivery)
Q11: 訂購流程是怎樣的？
Q12: 訂製一個證書套需要多久時間？
Q13: 付款方式有哪些？
Q14: 送貨方式及運費如何計算？
Q15: 可以到店自取嗎？

售後與其他 (After-sales)
Q16: 如何清潔和保養結婚證書套？
Q17: 如果收到的證書套有問題，可以退換嗎？
Q18: 證書套的價格是多少？
Q19: 如何聯絡客服？
Q20: 可以在證書套上印照片或圖案嗎？
```

Each Q&A:
- Question as `<h3>` with class `text-lg font-semibold text-gray-800 mb-2`
- Answer as `<p>` with class `text-gray-700 mb-4`

Page head tags:
```html
<title>My O! 常見問題 — 結婚證書套 FAQ | 香港</title>
<meta name="description" content="結婚證書套常見問題：尺寸、訂製、價格、運送等一站式解答。為您的結婚證書套選擇提供最全面的資訊。">
<link rel="canonical" href="https://myo-makeyourown.pages.dev/faq.html">
<meta property="og:title" content="My O! 常見問題 — 結婚證書套 FAQ | 香港">
<meta property="og:description" content="結婚證書套常見問題：尺寸、訂製、價格、運送等一站式解答。">
<meta property="og:url" content="https://myo-makeyourown.pages.dev/faq.html">
<meta property="og:type" content="website">
<meta name="robots" content="index, follow">
```

FAQPage JSON-LD (insert before `</head>`):
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "證書套的尺寸是否適合香港婚姻登記處的 A4 結婚證書？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "適合。我們的證書套專為香港 A4 結婚證書設計，內尺寸約 31cm × 22.5cm，完美容納標準證書，無需摺疊。"
      }
    },
    ... repeat for all 20 Q&A items
  ]
}
</script>
```

- [ ] **Step 2: Test faq.html renders correctly**

Run: `python3 -m http.server 8000` in the project root, then verify `http://localhost:8000/faq.html` loads with proper nav, FAQ content, and footer.

- [ ] **Step 3: Commit**

```bash
git add faq.html
git commit -m "feat(faq): create dedicated FAQ page with 20 Q&A items and FAQPage schema"
```

---

### Task 2: Add FAQ accordion section to homepage (index.html)

**Files:**
- Modify: `index.html` — insert FAQ section between the hidden section (line 1097) and `#contact` section (line 1099)

- [ ] **Step 1: Insert FAQ accordion HTML**

Insert after line 1097 (`</section>` of the hidden bg-rose-50 section) and before line 1099 (`<section id="contact">`):

```html
    <!-- FAQ Section — SEO content -->
    <section id="faq" class="py-6 bg-white">
        <div class="container mx-auto px-4 max-w-4xl">
            <h2 class="section-title text-center">常見問題</h2>
            <p class="text-md text-gray-700 mb-6 text-center max-w-3xl mx-auto">關於結婚證書套，您可能想了解的問題：</p>

            <div class="space-y-3">
                <!-- Q1 -->
                <details class="card cursor-pointer">
                    <summary class="font-semibold text-gray-800 text-lg px-4 py-3 cursor-pointer list-none flex justify-between items-center">
                        <span>證書套的尺寸是否適合香港婚姻登記處的 A4 結婚證書？</span>
                        <span class="text-rose-500 text-xl transition-transform duration-300">▼</span>
                    </summary>
                    <div class="px-4 pb-4 text-gray-700 leading-relaxed">
                        適合。我們的證書套專為香港 A4 結婚證書設計，內尺寸約 31cm × 22.5cm，完美容納標準證書，無需摺疊。另備有其他尺寸可選。
                        <a href="faq.html" class="text-rose-600 hover:text-rose-700 ml-1 font-medium">了解更多 →</a>
                    </div>
                </details>

                <!-- Q2 -->
                <details class="card cursor-pointer">
                    <summary class="font-semibold text-gray-800 text-lg px-4 py-3 cursor-pointer list-none flex justify-between items-center">
                        <span>可以在證書套上印製哪些文字？</span>
                        <span class="text-rose-500 text-xl transition-transform duration-300">▼</span>
                    </summary>
                    <div class="px-4 pb-4 text-gray-700 leading-relaxed">
                        可以印上新人名字（中英文均可）和結婚日期，採用熱轉印（燙印）工藝，呈現燙金或燙銀質感。設計師款更可加入指定字句。
                        <a href="faq.html" class="text-rose-600 hover:text-rose-700 ml-1 font-medium">了解更多 →</a>
                    </div>
                </details>

                <!-- Q3 -->
                <details class="card cursor-pointer">
                    <summary class="font-semibold text-gray-800 text-lg px-4 py-3 cursor-pointer list-none flex justify-between items-center">
                        <span>亞麻布和磨砂珠光材質有什麼分別？</span>
                        <span class="text-rose-500 text-xl transition-transform duration-300">▼</span>
                    </summary>
                    <div class="px-4 pb-4 text-gray-700 leading-relaxed">
                        亞麻布（米色）紋理自然質樸，手感溫暖，適合簡約風格；磨砂珠光（藍色）帶細緻光澤，更顯華麗。兩款均為硬殼封面，耐用防潮。
                        <a href="faq.html" class="text-rose-600 hover:text-rose-700 ml-1 font-medium">了解更多 →</a>
                    </div>
                </details>

                <!-- Q4 -->
                <details class="card cursor-pointer">
                    <summary class="font-semibold text-gray-800 text-lg px-4 py-3 cursor-pointer list-none flex justify-between items-center">
                        <span>訂製一個證書套需要多久時間？</span>
                        <span class="text-rose-500 text-xl transition-transform duration-300">▼</span>
                    </summary>
                    <div class="px-4 pb-4 text-gray-700 leading-relaxed">
                        一般訂製需時約 7-14 個工作天（視乎訂單量），確認設計稿後開始製作。如有急單可與我們聯絡協調。
                        <a href="faq.html" class="text-rose-600 hover:text-rose-700 ml-1 font-medium">了解更多 →</a>
                    </div>
                </details>

                <!-- Q5 -->
                <details class="card cursor-pointer">
                    <summary class="font-semibold text-gray-800 text-lg px-4 py-3 cursor-pointer list-none flex justify-between items-center">
                        <span>如何清潔和保養結婚證書套？</span>
                        <span class="text-rose-500 text-xl transition-transform duration-300">▼</span>
                    </summary>
                    <div class="px-4 pb-4 text-gray-700 leading-relaxed">
                        建議以乾軟布輕拭表面，避免接觸水份或化學溶劑。存放於陰涼乾燥處，避免陽光直射。
                        <a href="faq.html" class="text-rose-600 hover:text-rose-700 ml-1 font-medium">了解更多 →</a>
                    </div>
                </details>

                <!-- Q6 -->
                <details class="card cursor-pointer">
                    <summary class="font-semibold text-gray-800 text-lg px-4 py-3 cursor-pointer list-none flex justify-between items-center">
                        <span>證書套的價格是多少？</span>
                        <span class="text-rose-500 text-xl transition-transform duration-300">▼</span>
                    </summary>
                    <div class="px-4 pb-4 text-gray-700 leading-relaxed">
                        經典款 HK$388（亞麻布／磨砂珠光），設計師款 HK$588，價格已包含名字與日期印刷。詳情可參閱我們的
                        <a href="pricing.md" class="text-rose-600 hover:text-rose-700 font-medium">定價頁面</a>。
                        <a href="faq.html" class="text-rose-600 hover:text-rose-700 ml-1 font-medium">了解更多 →</a>
                    </div>
                </details>

                <!-- Q7 -->
                <details class="card cursor-pointer">
                    <summary class="font-semibold text-gray-800 text-lg px-4 py-3 cursor-pointer list-none flex justify-between items-center">
                        <span>訂購流程是怎樣的？</span>
                        <span class="text-rose-500 text-xl transition-transform duration-300">▼</span>
                    </summary>
                    <div class="px-4 pb-4 text-gray-700 leading-relaxed">
                        選擇款式與顏色 → 提供新人名字與結婚日期 → 我們確認設計稿 → 製作 → 送貨。全程可透過 Instagram 或 WhatsApp 溝通。
                        <a href="faq.html" class="text-rose-600 hover:text-rose-700 ml-1 font-medium">了解更多 →</a>
                    </div>
                </details>

                <!-- Q8 -->
                <details class="card cursor-pointer">
                    <summary class="font-semibold text-gray-800 text-lg px-4 py-3 cursor-pointer list-none flex justify-between items-center">
                        <span>可以只訂購一個證書套嗎？</span>
                        <span class="text-rose-500 text-xl transition-transform duration-300">▼</span>
                    </summary>
                    <div class="px-4 pb-4 text-gray-700 leading-relaxed">
                        可以。您可以按需要訂購一個或一對，沒有最低數量限制。
                        <a href="faq.html" class="text-rose-600 hover:text-rose-700 ml-1 font-medium">了解更多 →</a>
                    </div>
                </details>
            </div>

            <div class="text-center mt-6">
                <a href="faq.html" class="text-rose-600 hover:text-rose-700 font-semibold">查看全部常見問題 →</a>
            </div>
        </div>
    </section>
```

Add minimal CSS for details/summary accordion animation (append to existing `<style>` block before the closing `</style>` tag):

```css
/* FAQ Accordion 樣式 */
#faq details.card {
    overflow: hidden;
    transition: all 0.3s ease;
}
#faq details.card summary::-webkit-details-marker {
    display: none;
}
#faq details.card summary .text-rose-500 {
    transition: transform 0.3s ease;
}
#faq details.card[open] summary .text-rose-500 {
    transform: rotate(180deg);
}
```

- [ ] **Step 2: Add FAQPage JSON-LD to index.html head**

Insert before `</head>` (after the existing Product schema at line 893 or before line 894):

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "證書套的尺寸是否適合香港婚姻登記處的 A4 結婚證書？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "適合。我們的證書套專為香港 A4 結婚證書設計，內尺寸約 31cm × 22.5cm，完美容納標準證書，無需摺疊。"
      }
    },
    {
      "@type": "Question",
      "name": "可以在證書套上印製哪些文字？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "可以印上新人名字（中英文均可）和結婚日期，採用熱轉印（燙印）工藝，呈現燙金或燙銀質感。"
      }
    },
    {
      "@type": "Question",
      "name": "亞麻布和磨砂珠光材質有什麼分別？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "亞麻布（米色）紋理自然質樸，手感溫暖，適合簡約風格；磨砂珠光（藍色）帶細緻光澤，更顯華麗。"
      }
    },
    {
      "@type": "Question",
      "name": "訂製一個證書套需要多久時間？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "一般訂製需時約 7-14 個工作天（視乎訂單量），確認設計稿後開始製作。"
      }
    },
    {
      "@type": "Question",
      "name": "如何清潔和保養結婚證書套？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "建議以乾軟布輕拭表面，避免接觸水份或化學溶劑。存放於陰涼乾燥處，避免陽光直射。"
      }
    },
    {
      "@type": "Question",
      "name": "證書套的價格是多少？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "經典款 HK$388（亞麻布／磨砂珠光），設計師款 HK$588，價格已包含名字與日期印刷。"
      }
    },
    {
      "@type": "Question",
      "name": "訂購流程是怎樣的？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "選擇款式與顏色 → 提供新人名字與結婚日期 → 我們確認設計稿 → 製作 → 送貨。全程可透過 Instagram 或 WhatsApp 溝通。"
      }
    },
    {
      "@type": "Question",
      "name": "可以只訂購一個證書套嗎？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "可以。您可以按需要訂購一個或一對，沒有最低數量限制。"
      }
    }
  ]
}
</script>
```

- [ ] **Step 3: Fix footer link**

Change line 1120:
```html
<a href="#" class="footer-link">常見問題</a>
```
to:
```html
<a href="faq.html" class="footer-link">常見問題</a>
```

- [ ] **Step 4: Verify homepage renders**

Run: `python3 -m http.server 8000`
Check `http://localhost:8000/`:
- FAQ section visible between product overview and contact section
- All 8 accordion items open/close on click
- "了解更多 →" links point to `faq.html`
- Footer "常見問題" links to `faq.html` not `#`

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat(homepage): add FAQ accordion section with 8 Q&A and fix footer link"
```

---

### Task 3: Update sitemap.xml

**Files:**
- Modify: `sitemap.xml`

- [ ] **Step 1: Add faq.html URL entry**

After the `index.html` entry (around line 8), add:

```xml
  <url>
    <loc>https://myo-makeyourown.pages.dev/faq.html</loc>
    <lastmod>2026-07-13</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
```

- [ ] **Step 2: Verify sitemap is valid XML**

Run: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml'); print('Valid XML')"`
Expected output: `Valid XML`

- [ ] **Step 3: Commit**

```bash
git add sitemap.xml
git commit -m "fix(sitemap): add faq.html URL entry"
```

---

### Task 4: Update llms.txt (optional but recommended)

**Files:**
- Modify: `llms.txt`

- [ ] **Step 1: Add FAQ page to Core Pages section**

After the existing Core Pages entries (around line 12), add:
```
- FAQ: https://myo-makeyourown.pages.dev/faq.html
```

- [ ] **Step 2: Commit**

```bash
git add llms.txt
git commit -m "docs(llms): add FAQ page to llms.txt"
```

---

## 驗收清單

- [ ] `faq.html` — 可訪問，20 條問題分類排列，FAQPage JSON-LD 有效
- [ ] `index.html` — FAQ accordion 顯示 8 條問題，點擊展開/摺疊
- [ ] `index.html` — footer「常見問題」連結指向 faq.html
- [ ] `index.html` — FAQPage JSON-LD 存在且無語法錯誤
- [ ] `sitemap.xml` — 包含 faq.html URL，XML 格式有效
- [ ] `llms.txt` — 包含 faq.html 連結
