# 海報佈局重新設計實作計劃

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 poster.html 的產品特點區域改為對角線排列，並將顏色圖片置於中央，節省垂直空間，同時增加文字大小。

**Architecture:** 使用 CSS Grid 實現對角線佈局，將 highlights-section 改為包含 color-combo-img 的新結構，四個特點分別定位於四個角落。

**Tech Stack:** HTML5, CSS3 (Grid, Flexbox)

---

## 檔案結構

- Modify: `poster.html` - 海報 HTML 檔案

---

### Task 1: 重構 highlights-section 結構

**Files:**
- Modify: `poster.html:818-848`

- [ ] **Step 1: 讀取目前 highlights-section HTML 結構**

位置：行 818-848

- [ ] **Step 2: 將 highlights-section 改為 Grid 容器，包含 color-combo-img**

```html
<div class="highlights-section">
    <!-- 左上特點 -->
    <div class="highlight-item top-left">
        <span class="highlight-icon">💖</span>
        <div class="highlight-content">
            <span class="highlight-title">完美尺寸</span>
            <span class="highlight-desc">適用香港婚姻登記處 A4 證書<br>約 30.7cm × 22.6cm</span>
        </div>
    </div>
    
    <!-- 右上特點 -->
    <div class="highlight-item top-right">
        <span class="highlight-icon">✨</span>
        <div class="highlight-content">
            <span class="highlight-title">高質感封面</span>
            <span class="highlight-desc">硬殼包覆磨砂珠光或亞麻布紋<br>手感細緻</span>
        </div>
    </div>
    
    <!-- 中央顏色圖片 -->
    <div class="highlight-center">
        <div class="color-combo-section">
            <img src="image/cert_color_beige_and_blue.png" alt="米色藍色组合" class="color-combo-img">
        </div>
    </div>
    
    <!-- 左下特點 -->
    <div class="highlight-item bottom-left">
        <span class="highlight-icon">🛡️</span>
        <div class="highlight-content">
            <span class="highlight-title">穩妥保護</span>
            <span class="highlight-desc">厚卡內襯、固定帶<br>防潮防塵</span>
        </div>
    </div>
    
    <!-- 右下特點 -->
    <div class="highlight-item bottom-right">
        <span class="highlight-icon">🎨</span>
        <div class="highlight-content">
            <span class="highlight-title">精緻印刷</span>
            <span class="highlight-desc">熱轉印燙印工藝<br>呈現燙金/銀質感</span>
        </div>
    </div>
</div>
```

- [ ] **Step 3: 刪除原本獨立的 color-combo-section（已移入 highlights-section）**

位置：行 813-816

---

### Task 2: 更新 CSS 樣式 - highlights-section Grid 佈局

**Files:**
- Modify: `poster.html` CSS 區塊

- [ ] **Step 1: 更新 highlights-section CSS**

```css
.highlights-section {
    position: relative;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    grid-template-rows: 1fr auto 1fr;
    gap: 3px;
    margin-bottom: 3px;
    min-height: 120px;
}
```

- [ ] **Step 2: 新增四個角落特點樣式**

```css
.highlight-item.top-left {
    grid-column: 1;
    grid-row: 1;
    justify-self: start;
    align-self: start;
}

.highlight-item.top-right {
    grid-column: 3;
    grid-row: 1;
    justify-self: end;
    align-self: start;
    text-align: right;
}

.highlight-item.bottom-left {
    grid-column: 1;
    grid-row: 3;
    justify-self: start;
    align-self: end;
}

.highlight-item.bottom-right {
    grid-column: 3;
    grid-row: 3;
    justify-self: end;
    align-self: end;
    text-align: right;
}
```

- [ ] **Step 3: 新增中央區域樣式**

```css
.highlight-center {
    grid-column: 2;
    grid-row: 2;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 10px;
}
```

- [ ] **Step 4: 更新 highlight-item 為 column 排列並增加字體大小 40-50%**

```css
.highlight-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    padding: 1px;
}
```

---

### Task 3: 增加文字大小 40-50%

**Files:**
- Modify: `poster.html` CSS 區塊

- [ ] **Step 1: 更新 highlight-title 字體大小**

原本：`clamp(6px, 1.3vw, 8px)`
改為：`clamp(8px, 1.8vw, 11px)` (+40-50%)

- [ ] **Step 2: 更新 highlight-desc 字體大小**

原本：`clamp(4px, 1vw, 6px)`
改為：`clamp(6px, 1.4vw, 9px)` (+40-50%)

- [ ] **Step 3: 更新 highlight-icon 大小**

原本：`clamp(7px, 1.5vw, 10px)`
改為：`clamp(10px, 2.1vw, 14px)` (+40-50%)

- [ ] **Step 4: 更新 personalize-section 文字大小**

```css
.personalize-title {
    font-size: clamp(9px, 1.8vw, 12px); /* +40-50% */
}

.personalize-text {
    font-size: clamp(6px, 1.4vw, 9px); /* +40-50% */
}
```

---

### Task 4: 驗證與提交

**Files:**
- Modify: `poster.html`

- [ ] **Step 1: 在瀏覽器中開啟 poster.html 驗證**
- 確認四個特點在四個角落
- 確認顏色圖片在中央
- 確認文字大小增加
- 確認佈局正常顯示

- [ ] **Step 2: 提交變更**

```bash
git add poster.html
git commit -m "重構：海報特點區域對角線排列與文字放大

- 四個特點改為對角線排列
- 顏色圖片置於中央
- 特點與客製化文字增加 40-50%
- 使用 CSS Grid 實現新佈局

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

---

## 驗收清單

- [ ] 四個特點呈對角線排列（左上、右上、右下、左下）
- [ ] 顏色圖片置於四個特點中央
- [ ] highlight-title 字體增加 40-50%
- [ ] highlight-desc 字體增加 40-50%
- [ ] personalize-section 文字增加 40-50%
- [ ] 頁面在瀏覽器正常顯示
- [ ] 所有連結功能正常（品牌返回首頁、QR Code 連結）