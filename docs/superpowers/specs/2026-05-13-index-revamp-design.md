# index.html Revamp Design Specification
**Date:** 2026-05-13
**Author:** CherryClaw Agent
**Version:** 1.0

---

## 1. 概述

### 1.1 項目背景
My O! 結婚證書套網站需要全方位的重新設計，以提升視覺效果、用戶體驗和轉化率。

### 1.2 設計風格
**清新自然風 + 奢華精緻細節**
- 大量奶油白背景 (#FAF8F5)
- 玫瑰金 (#B76E79) + 深棕 (#5D4037) 作為主色
- 淺金 (#D4AF37) 作為點綴
- 自然紋理元素（亞麻布紋理背景）
- 圓潤卡片 + 柔和陰影
- Noto Sans TC 字體（更優雅的中文呈現）

### 1.3 設計目標
1. 視覺升級 — 更時尚、更精緻的視覺效果
2. 用戶體驗優化 — 改善選購流程、互動體驗
3. 轉化率提升 — 加強購買引導、聯絡方式曝光
4. 移動端體驗改進 — 更適合手機瀏覽
5. 內容重新組織 — 調整訊息架構、區塊順序

---

## 2. 內容架構

### 2.1 區塊順序（新）

| 順序 | 區塊 | 說明 |
|------|------|------|
| 1 | 導航欄 | 保持現有結構，響應式漢堡選單 |
| 2 | Hero 區塊 | 精簡文案 + 強 CTA |
| 3 | 選擇顏色 | 第一步驟（向導系統） |
| 4 | 選擇款式 | 第二步驟（向導系統） |
| 5 | 產品特點 | 合併展示 |
| 6 | 聯絡我們 | 最終轉化區塊 |
| 7 | 頁腳 | 保持現有 |
| 8 | 浮動按鈕 | 全程可見 |

---

## 3. 詳細設計

### 3.1 色彩系統

```css
:root {
  /* 背景色 */
  --bg-primary: #FAF8F5;      /* 奶油白 */
  --bg-secondary: #FDFAF6;    /* 淺米色 */
  --bg-card: rgba(255, 255, 255, 0.85);  /* 半透明卡片 */

  /* 主色 */
  --color-primary: #B76E79;   /* 玫瑰金 */
  --color-primary-dark: #9A5A63;
  --color-secondary: #5D4037; /* 深棕 */
  --color-accent: #D4AF37;   /* 淺金 */

  /* 文字色 */
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-light: #999999;

  /* 功能色 */
  --color-success: #4CAF50;
  --color-error: #E57373;

  /* 陰影 */
  --shadow-soft: 0 4px 20px rgba(93, 64, 55, 0.08);
  --shadow-card: 0 8px 30px rgba(93, 64, 55, 0.1);
  --shadow-hover: 0 12px 40px rgba(93, 64, 55, 0.15);
}
```

### 3.2 字體系統

```css
/* 中文 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

/* 英文/數字 */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');

body {
  font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

/* 標題使用襯線字體增添優雅感 */
h1, h2, h3 {
  font-family: 'Playfair Display', 'Noto Sans TC', serif;
}
```

### 3.3 間距系統

```css
:root {
  --space-xs: 0.5rem;   /* 8px */
  --space-sm: 1rem;     /* 16px */
  --space-md: 1.5rem;   /* 24px */
  --space-lg: 2rem;     /* 32px */
  --space-xl: 3rem;     /* 48px */
  --space-2xl: 4rem;    /* 64px */
}
```

---

## 4. 核心功能模組

### 4.1 選購向導系統

#### 步驟指示器
- 位於選擇區塊頂部
- 固定顯示：① 顏色 → ② 款式 → ③ 完成
- 當前步驟高亮（玫瑰金色）
- 已完成步驟顯示勾選標記

#### 選擇卡片
- 半透明奶油白背景
- 圓角 20px
- 微妙邊框光澤效果
- Hover：上浮 4px + 陰影加深
- 選中：邊框變玫瑰金 + 彈跳動畫 + 勾選標記

#### 進度追蹤欄
- 位於頁面底部（移動端）
- 顯示「已選：米色 + 款式1」
- 滑動到最後一步顯示「立即查詢」大按鈕

#### 動畫細節
```css
/* 選中動畫 */
.card.selected {
  transform: scale(1.02);
  border: 2px solid var(--color-primary);
  box-shadow: 0 0 0 4px rgba(183, 110, 121, 0.2);
  animation: selectBounce 0.4s ease-out;
}

@keyframes selectBounce {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1.02); }
}

/* 勾選標記 */
.card.selected::after {
  content: '✓';
  position: absolute;
  top: -10px;
  right: -10px;
  background: var(--color-primary);
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: checkPop 0.3s ease-out 0.1s both;
}

@keyframes checkPop {
  0% { transform: scale(0); opacity: 0; }
  70% { transform: scale(1.2); }
  100% { transform: scale(1); opacity: 1; }
}
```

### 4.2 產品展示升級

#### Lightbox 放大預覽
- 點擊卡片圖片打開全屏 Lightbox
- 背景模糊 + 暗化
- 左右滑動/點擊切換
- 底部縮略圖列表
- 關閉按鈕（右上角）
- 支援觸控縮放

```css
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(10px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.lightbox.active {
  opacity: 1;
  visibility: visible;
}

.lightbox-content {
  max-width: 90%;
  max-height: 90%;
  transform: scale(0.9);
  transition: transform 0.3s ease;
}

.lightbox.active .lightbox-content {
  transform: scale(1);
}
```

### 4.3 浮動快捷按鈕

- 向下滾動 100px 後浮現
- 三個按鈕：💬討論、📱查詢、❤️收藏
- 位置：右下角
- 動畫：滑入 + 輕微彈跳

```css
.floating-actions {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1000;
  transform: translateY(100px);
  opacity: 0;
  transition: all 0.4s ease;
}

.floating-actions.visible {
  transform: translateY(0);
  opacity: 1;
}

.floating-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: white;
  box-shadow: var(--shadow-card);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.floating-btn:hover {
  transform: scale(1.1);
  box-shadow: var(--shadow-hover);
}

.floating-btn.whatsapp {
  background: #25D366;
  color: white;
}
```

### 4.4 移動端 Sticky Bar（增強版）

- 品牌標識 + 名稱
- 已選項目顯示
- 立即查詢按鈕（漸變背景）
- Instagram + WhatsApp 快捷圖標

---

## 5. 響應式斷點

```css
/* 手機優先策略 */
@media (max-width: 639px) {
  /* 緊湊佈局，觸控友好 */
  .section-title { font-size: 1.6rem; }
  .card-padding { padding: 1rem; }
  .btn-primary { padding: 0.6rem 1.2rem; }
}

@media (min-width: 640px) {
  /* 平板 */
  .section-title { font-size: 1.8rem; }
}

@media (min-width: 768px) {
  /* 桌面 */
  .section-title { font-size: 2.2rem; }
  .floating-actions { display: none; } /* 桌面隱藏浮動按鈕 */
}

@media (min-width: 1024px) {
  /* 大桌面 */
  .section-title { font-size: 2.5rem; }
  .grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
}
```

---

## 6. 動畫系統

### 6.1 頁面載入動畫

```css
.fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 交錯動畫 */
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }
.stagger-4 { animation-delay: 0.4s; }
```

### 6.2 滾動觸發動畫

- 卡片區塊進入視口時淡入
- 使用 Intersection Observer API

---

## 7. 技術實現

### 7.1 技術棧
- 保持 Tailwind CSS（通過 CDN）
- 自定義 CSS（變量 + 動畫）
- 原生 JavaScript（無需框架）
- Swiper.js（輪播，現有）

### 7.2 性能優化
- 圖片使用 WebP 格式（如果可用）
- 懶加載圖片
- CSS 動畫使用 transform/opacity（GPU 加速）
- 減少 DOM 操作

### 7.3 可訪問性
- 確保所有交互元素可通過鍵盤訪問
- 顏色對比度符合 WCAG 2.1 AA 標準
- 添加 ARIA 標籤
- 支持 prefers-reduced-motion

---

## 8. 輸出文件

- 新文件：`v2.html`（完整重新設計版本）
- 圖片資源：使用現有 image/ 目錄
- 保持與原站點一致的路徑結構

---

## 9. 待確認事項

- [ ] 字體選擇（Noto Sans TC + Playfair Display）
- [ ] 動畫時長（目前預設值）
- [ ] 是否需要加入社交證明（顧客評價）
- [ ] 討論功能具體形式（評論區/反饋表單）