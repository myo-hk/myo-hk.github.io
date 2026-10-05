# Poster Aspect Ratio 維持實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 確保 poster.html 在任何螢幕大小下都維持 A5 紙張比例 (1:1.414)，不會因為螢幕尺寸改變而變形

**Architecture:** 使用 CSS aspect-ratio 屬性，配合 max-height 限制來維持長寬比。這是最簡潔的 CSS-only 解決方案，無需 JavaScript

**Tech Stack:** 純 CSS（使用 aspect-ratio 屬性和 viewport 單位）

---

## Task 1: 添加 CSS aspect-ratio 到 .a5-flyer 容器

**Files:**
- Modify: `poster.html:38-50`

- [ ] **Step 1: 讀取 current CSS**

定位 `.a5-flyer` 樣式區塊（第 38-50 行）

- [ ] **Step 2: 修改 .a5-flyer CSS 樣式**

將 current:
```css
.a5-flyer {
    width: 100%;
    max-width: 420px;
    min-height: 500px;
    background-color: #F7F5F0;
    padding: 2%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    position: relative;
    page-break-after: always;
    overflow: visible;
}
```

改為:
```css
.a5-flyer {
    width: 100%;
    max-width: 420px;
    aspect-ratio: 148 / 210;
    height: auto;
    max-height: 90vh;
    background-color: #F7F5F0;
    padding: 2%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    position: relative;
    page-break-after: always;
    overflow: visible;
}
```

**變更說明:**
- 移除 `min-height: 500px`（會破壞比例）
- 添加 `aspect-ratio: 148 / 210`（A5 紙張比例）
- 添加 `height: auto`（讓 height 根據 aspect-ratio 自動計算）
- 添加 `max-height: 90vh`（確保在非常高的螢幕上不會超出視窗）

- [ ] **Step 3: 驗證更改**

用瀏覽器打開 poster.html，檢查：
1. 海報是否維持正確比例（不變形）
2. 在手機/平板/桌面環境下都能正常顯示
3. 原有功能（點擊連結、QR code）仍然正常運作

- [ ] **Step 4: 提交變更**

```bash
git add poster.html
git commit -m "feat: maintain A5 aspect ratio for poster on all screen sizes"
```