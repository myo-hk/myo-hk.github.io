# index.html Revamp Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create v2.html with fresh natural style, selection wizard, enhanced card interactions, floating action buttons, and mobile-optimized experience.

**Architecture:** Single-page HTML with Tailwind CSS + custom CSS variables for theming. Native JavaScript for interactions (no framework). Preserve existing image assets and structure.

**Tech Stack:**
- Tailwind CSS (CDN, existing)
- Custom CSS with CSS variables
- Native JavaScript (no dependencies)
- Swiper.js (existing, preserve)

---

## File Structure

```
index.html (existing) → v2.html (new output)
├── CSS Variables & Base Styles
├── Selection Wizard System
│   ├── Step Indicator
│   ├── Selection Cards
│   └── Progress Bar
├── Lightbox Component
├── Floating Action Buttons
├── Mobile Sticky Bar (enhanced)
├── Animation System
│   ├── Page Load
│   └── Scroll-triggered
└── Responsive Adjustments
```

---

## Implementation Tasks

### Task 1: CSS Variables & Base Styles

**Goal:** Define the complete design system with CSS custom properties for colors, spacing, shadows, and fonts.

**Files:**
- Create: `v2.html` (copy structure from index.html, then modify)

- [ ] **Step 1: Copy index.html to v2.html as base**

```bash
cp index.html v2.html
```

- [ ] **Step 2: Add font imports to `<head>`**

在 `<head>` 中找到現有的 font import，替換為：

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
```

- [ ] **Step 3: Add CSS variables in `<style>` tag**

在 `<style>` 標籤開頭添加：

```css
:root {
  /* 背景色 */
  --bg-primary: #FAF8F5;
  --bg-secondary: #FDFAF6;
  --bg-card: rgba(255, 255, 255, 0.85);
  
  /* 主色 */
  --color-primary: #B76E79;
  --color-primary-dark: #9A5A63;
  --color-secondary: #5D4037;
  --color-accent: #D4AF37;
  
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
  
  /* 間距 */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 1.5rem;
  --space-lg: 2rem;
  --space-xl: 3rem;
  --space-2xl: 4rem;
  
  /* 圓角 */
  --radius-sm: 0.5rem;
  --radius-md: 1rem;
  --radius-lg: 1.25rem;
  --radius-xl: 1.5rem;
  --radius-full: 9999px;
}

/* 基礎樣式更新 */
body {
  font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

h1, h2, h3, .section-title {
  font-family: 'Playfair Display', 'Noto Sans TC', serif;
  color: var(--color-secondary);
}

/* Hero Section 更新 */
.hero-section {
  background: linear-gradient(135deg, var(--bg-primary) 0%, #F5EDE8 100%);
}

/* 卡片基礎樣式更新 */
.card {
  background: var(--bg-card);
  border: 1px solid rgba(183, 110, 121, 0.1);
  backdrop-filter: blur(10px);
}
```

- [ ] **Step 4: Update button styles**

找到 `.btn-primary` 並更新為：

```css
.btn-primary {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: white;
  padding: 0.75rem 1.75rem;
  border-radius: var(--radius-full);
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(183, 110, 121, 0.3);
  font-size: 0.95rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(183, 110, 121, 0.4);
}
```

- [ ] **Step 5: Commit**

```bash
git add v2.html
git commit -m "feat: add CSS variables and base styles to v2.html

- Add color system with CSS custom properties
- Add font imports (Noto Sans TC, Playfair Display)
- Update body and heading styles
- Update card and button styles with new theme"
```

---

### Task 2: Selection Wizard - Step Indicator

**Goal:** Add a visual step indicator showing ① Color → ② Style → ③ Complete

**Files:**
- Modify: `v2.html` (add step indicator HTML and styles)

- [ ] **Step 1: Add step indicator HTML after hero section**

在 `</header>` (hero section end) 之後，添加：

```html
<!-- Step Indicator - 選擇向導 -->
<div class="step-indicator" id="step-indicator">
  <div class="step-item" data-step="1">
    <div class="step-circle">1</div>
    <span class="step-label">選擇顏色</span>
  </div>
  <div class="step-line"></div>
  <div class="step-item" data-step="2">
    <div class="step-circle">2</div>
    <span class="step-label">選擇款式</span>
  </div>
  <div class="step-line"></div>
  <div class="step-item" data-step="3">
    <div class="step-circle">3</div>
    <span class="step-label">完成確認</span>
  </div>
</div>
```

- [ ] **Step 2: Add step indicator styles**

在 `<style>` 中添加：

```css
/* ===== 步驟指示器 ===== */
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-md) var(--space-lg);
  background: var(--bg-card);
  border-bottom: 1px solid rgba(183, 110, 121, 0.1);
  position: sticky;
  top: 60px; /* below nav */
  z-index: 40;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #E8E0DC;
  color: var(--text-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.step-item.active .step-circle {
  background: var(--color-primary);
  color: white;
  box-shadow: 0 4px 12px rgba(183, 110, 121, 0.4);
}

.step-item.completed .step-circle {
  background: var(--color-accent);
  color: white;
}

.step-item.completed .step-circle::after {
  content: '✓';
  font-size: 0.9rem;
}

.step-label {
  font-size: 0.75rem;
  color: var(--text-light);
  font-weight: 500;
}

.step-item.active .step-label {
  color: var(--color-primary);
}

.step-line {
  width: 60px;
  height: 2px;
  background: #E8E0DC;
  margin: 0 var(--space-sm);
  margin-bottom: 1.5rem;
  transition: background 0.3s ease;
}

.step-line.active {
  background: var(--color-primary);
}

/* Mobile responsive */
@media (max-width: 639px) {
  .step-indicator {
    padding: var(--space-sm);
    top: 50px;
  }
  .step-circle {
    width: 28px;
    height: 28px;
    font-size: 0.8rem;
  }
  .step-label {
    font-size: 0.65rem;
  }
  .step-line {
    width: 30px;
    margin: 0 0.25rem;
    margin-bottom: 1rem;
  }
}

/* Hide on desktop */
@media (min-width: 768px) {
  .step-indicator {
    display: none; /* Show only on mobile/tablet for now, can enable on desktop too */
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add v2.html
git commit -m "feat: add step indicator component

- Add step indicator HTML after hero
- Add responsive styles for step indicator
- Steps: Color → Style → Complete"
```

---

### Task 3: Selection Wizard - Cards with Animations

**Goal:** Update selection cards with hover effects, selection animation, and checkmark badge.

**Files:**
- Modify: `v2.html` (update existing card styles and add selection logic)

- [ ] **Step 1: Update selection card styles**

找到 `.select-option` 相關樣式，更新為：

```css
/* ===== 選擇卡片 ===== */
.select-option {
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  overflow: visible;
}

.select-option:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card);
  border-color: rgba(183, 110, 121, 0.2);
}

/* 選中狀態 - 彈跳動畫 */
.select-option.selected {
  border: 2px solid var(--color-primary);
  box-shadow: 0 0 0 4px rgba(183, 110, 121, 0.15), var(--shadow-card);
  transform: scale(1.02);
  animation: selectBounce 0.4s ease-out;
}

@keyframes selectBounce {
  0% { transform: scale(1); }
  40% { transform: scale(1.06); }
  70% { transform: scale(0.98); }
  100% { transform: scale(1.02); }
}

/* 勾選標記 */
.select-option.selected::after {
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
  font-size: 0.85rem;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(183, 110, 121, 0.4);
  animation: checkPop 0.3s ease-out 0.15s both;
  z-index: 10;
}

@keyframes checkPop {
  0% { transform: scale(0); opacity: 0; }
  70% { transform: scale(1.2); }
  100% { transform: scale(1); opacity: 1; }
}

/* 卡片內部圖片容器 */
.image-container {
  width: 100%;
  height: 160px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  margin-top: 0.6rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  border-radius: var(--radius-lg);
  transition: transform 0.3s ease;
}

.select-option:hover .image-container {
  transform: scale(1.02);
}

.select-option-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: var(--radius-lg);
}
```

- [ ] **Step 2: Update design style card**

更新 Swiper 卡片樣式 (`.design-style-card`)：

```css
/* ===== Swiper 設計款式卡片 ===== */
.design-style-card {
  background: var(--bg-card);
  border: 1px solid rgba(183, 110, 121, 0.1);
  box-shadow: var(--shadow-soft);
  border-radius: var(--radius-lg);
  height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 1rem;
  text-align: center;
  overflow: hidden;
  transition: all 0.3s ease;
}

.design-style-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card);
}

.design-style-card.selected {
  border: 2px solid var(--color-primary);
  box-shadow: 0 0 0 4px rgba(183, 110, 121, 0.15), var(--shadow-card);
}

.design-style-card.selected::after {
  content: '✓';
  position: absolute;
  top: 10px;
  right: 10px;
  background: var(--color-primary);
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  animation: checkPop 0.3s ease-out;
}
```

- [ ] **Step 3: Update JavaScript selection logic**

找到 JavaScript 中的選擇邏輯，確保動畫效果觸發：

```javascript
// 更新選擇邏輯，保持現有結構但添加動畫類別
selectOptions.forEach(option => {
  option.addEventListener('click', function(event) {
    const type = this.dataset.type;
    const value = this.dataset.value;

    if (type === 'color') {
      // 清除所有顏色選項的 selected 類別
      document.querySelectorAll('.select-option[data-type="color"]').forEach(sibling => {
        sibling.classList.remove('selected');
      });
      this.classList.add('selected');
      selectedColorInput.value = value;
      
      // 觸發 Lightbox
      const imgSrc = this.querySelector('.select-option-image').src;
      if (imgSrc) {
        openLightbox(imgSrc);
      }
      
      console.log(`Selected color: ${value}`);
      updateStepIndicator(1);

    } else if (type === 'style') {
      document.querySelectorAll('.select-option[data-type="style"]').forEach(sibling => {
        sibling.classList.remove('selected');
      });
      this.classList.add('selected');
      selectedStyleInput.value = value;
      console.log(`Selected style: ${value}`);
      updateStepIndicator(2);
    }
  });
});
```

- [ ] **Step 4: Add step indicator update function**

在 `<script>` 中添加：

```javascript
// 步進指示器更新函數
function updateStepIndicator(step) {
  const stepItems = document.querySelectorAll('.step-item');
  const stepLines = document.querySelectorAll('.step-line');
  
  stepItems.forEach((item, index) => {
    const itemStep = parseInt(item.dataset.step);
    item.classList.remove('active', 'completed');
    
    if (itemStep < step) {
      item.classList.add('completed');
    } else if (itemStep === step) {
      item.classList.add('active');
    }
  });
  
  stepLines.forEach((line, index) => {
    line.classList.remove('active');
    if (index < step - 1) {
      line.classList.add('active');
    }
  });
}
```

- [ ] **Step 5: Commit**

```bash
git add v2.html
git commit -m "feat: add selection card animations

- Add hover effects with translateY and shadow
- Add selection bounce animation
- Add checkmark badge on select
- Add step indicator JavaScript logic"
```

---

### Task 4: Lightbox Component

**Goal:** Create an enhanced image lightbox with navigation, thumbnails, and touch support.

**Files:**
- Modify: `v2.html` (update modal styles and add enhanced lightbox functionality)

- [ ] **Step 1: Update modal to enhanced lightbox**

找到現有的 `#image-modal`，更新為：

```html
<!-- Lightbox 增強版 -->
<div id="image-lightbox" class="lightbox">
  <button class="lightbox-close" aria-label="關閉">&times;</button>
  <button class="lightbox-nav lightbox-prev" aria-label="上一張">&#10094;</button>
  <button class="lightbox-nav lightbox-next" aria-label="下一張">&#10095;</button>
  
  <div class="lightbox-content-wrapper">
    <img class="lightbox-image" id="lightbox-image" src="" alt="產品大圖">
  </div>
  
  <div class="lightbox-thumbnails" id="lightbox-thumbnails">
    <!-- 由 JavaScript 動態生成 -->
  </div>
  
  <div class="lightbox-counter">1 / 4</div>
</div>
```

- [ ] **Step 2: Add lightbox styles**

在 `<style>` 中添加：

```css
/* ===== Lightbox 增強版 ===== */
.lightbox {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.92);
  backdrop-filter: blur(10px);
  z-index: 2000;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.lightbox.active {
  display: flex;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.lightbox-close {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  font-size: 2.5rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2010;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-close:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  font-size: 1.5rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2010;
}

.lightbox-prev { left: 20px; }
.lightbox-next { right: 20px; }

.lightbox-nav:hover {
  background: var(--color-primary);
}

.lightbox-content-wrapper {
  max-width: 85%;
  max-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-image {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.lightbox-thumbnails {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  max-width: 90%;
  overflow-x: auto;
  padding: 10px;
}

.lightbox-thumb {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
  cursor: pointer;
  opacity: 0.5;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.lightbox-thumb:hover {
  opacity: 0.8;
}

.lightbox-thumb.active {
  opacity: 1;
  border-color: var(--color-primary);
}

.lightbox-counter {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-top: 15px;
}

/* Mobile adjustments */
@media (max-width: 639px) {
  .lightbox-nav {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }
  .lightbox-close {
    width: 40px;
    height: 40px;
    font-size: 2rem;
  }
  .lightbox-thumb {
    width: 50px;
    height: 50px;
  }
}
```

- [ ] **Step 3: Update JavaScript for enhanced lightbox**

替換現有的 modal 邏輯為：

```javascript
// Lightbox 功能
const lightbox = document.getElementById('image-lightbox');
const lightboxImage = document.getElementById('lightbox-image');
const lightboxThumbnails = document.getElementById('lightbox-thumbnails');
const lightboxCounter = document.querySelector('.lightbox-counter');
const lightboxClose = document.querySelector('.lightbox-close');
const lightboxPrev = document.querySelector('.lightbox-prev');
const lightboxNext = document.querySelector('.lightbox-next');

let currentImageIndex = 0;
const allColorImages = [];

// 收集所有顏色圖片
document.querySelectorAll('.select-option[data-type="color"]').forEach((option, index) => {
  const img = option.querySelector('.select-option-image');
  if (img && img.src) {
    allColorImages.push({
      src: img.src,
      index: index
    });
  }
});

function openLightbox(imgSrc) {
  currentImageIndex = allColorImages.findIndex(img => img.src === imgSrc);
  if (currentImageIndex === -1) currentImageIndex = 0;
  
  updateLightboxImage();
  lightbox.classList.add('active');
  document.body.style.overflow = 'hidden'; // 禁止背景滾動
}

function closeLightbox() {
  lightbox.classList.remove('active');
  document.body.style.overflow = '';
}

function updateLightboxImage() {
  const currentImg = allColorImages[currentImageIndex];
  if (currentImg) {
    lightboxImage.src = currentImg.src;
    lightboxCounter.textContent = `${currentImageIndex + 1} / ${allColorImages.length}`;
    
    // 更新縮略圖 active 狀態
    document.querySelectorAll('.lightbox-thumb').forEach((thumb, idx) => {
      thumb.classList.toggle('active', idx === currentImageIndex);
    });
  }
}

function nextImage() {
  currentImageIndex = (currentImageIndex + 1) % allColorImages.length;
  updateLightboxImage();
}

function prevImage() {
  currentImageIndex = (currentImageIndex - 1 + allColorImages.length) % allColorImages.length;
  updateLightboxImage();
}

// 生成縮略圖
function generateThumbnails() {
  lightboxThumbnails.innerHTML = '';
  allColorImages.forEach((img, index) => {
    const thumb = document.createElement('img');
    thumb.src = img.src;
    thumb.className = 'lightbox-thumb' + (index === currentImageIndex ? ' active' : '');
    thumb.addEventListener('click', () => {
      currentImageIndex = index;
      updateLightboxImage();
    });
    lightboxThumbnails.appendChild(thumb);
  });
}

// 初始化縮略圖
generateThumbnails();

// 事件監聽
lightboxClose.addEventListener('click', closeLightbox);
lightboxPrev.addEventListener('click', prevImage);
lightboxNext.addEventListener('click', nextImage);

// 點擊背景關閉
lightbox.addEventListener('click', (e) => {
  if (e.target === lightbox) closeLightbox();
});

// ESC 鍵關閉
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && lightbox.classList.contains('active')) {
    closeLightbox();
  }
  if (e.key === 'ArrowLeft') prevImage();
  if (e.key === 'ArrowRight') nextImage();
});

// 觸控滑動支持
let touchStartX = 0;
lightbox.addEventListener('touchstart', (e) => {
  touchStartX = e.touches[0].clientX;
});

lightbox.addEventListener('touchend', (e) => {
  const touchEndX = e.changedTouches[0].clientX;
  const diff = touchStartX - touchEndX;
  
  if (Math.abs(diff) > 50) {
    if (diff > 0) nextImage();
    else prevImage();
  }
});
```

- [ ] **Step 4: Remove old modal code**

找到並刪除舊的 modal HTML 和相關樣式：
- 刪除 `<div id="image-modal" class="modal">...</div>`
- 刪除舊的 `.modal` 樣式

- [ ] **Step 5: Commit**

```bash
git add v2.html
git commit -m "feat: add enhanced lightbox component

- Add full-screen lightbox with backdrop blur
- Add prev/next navigation buttons
- Add thumbnail gallery
- Add keyboard navigation (ESC, arrows)
- Add touch swipe support for mobile
- Add image counter display"
```

---

### Task 5: Floating Action Buttons

**Goal:** Add floating action buttons that appear on scroll (WhatsApp, Instagram, Favorite).

**Files:**
- Modify: `v2.html` (add FAB HTML and styles)

- [ ] **Step 1: Add floating buttons HTML**

在 `</body>` 之前，`<script>` 之前添加：

```html
<!-- Floating Action Buttons -->
<div class="floating-actions" id="floating-actions">
  <button class="floating-btn floating-favorite" id="floating-favorite" aria-label="收藏">
    <i class="far fa-heart"></i>
  </button>
  <a href="https://www.instagram.com/myo.makeyourown/" target="_blank" class="floating-btn floating-instagram" aria-label="Instagram">
    <i class="fab fa-instagram"></i>
  </a>
  <a href="https://api.whatsapp.com/send?phone=85263796410&text=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E6%88%91%E5%BE%9E%E4%BD%A0%E5%80%91%E7%B6%B2%E7%AB%99%E4%B8%8A%E7%9C%8B%E5%88%B0%E9%80%99%E5%80%8B%E7%94%A2%E5%93%81%EEF%BC%81%E6%9C%89%E8%88%88%E8%B6%A3%E4%BA%86%E8%A7%A3%E6%9B%B4%E5%A4%9A%EF%BC%81" target="_blank" class="floating-btn floating-whatsapp" aria-label="WhatsApp">
    <i class="fab fa-whatsapp"></i>
  </a>
</div>
```

- [ ] **Step 2: Add floating button styles**

在 `<style>` 中添加：

```css
/* ===== 浮動快捷按鈕 ===== */
.floating-actions {
  position: fixed;
  bottom: 90px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1000;
  transform: translateX(120%);
  opacity: 0;
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.floating-actions.visible {
  transform: translateX(0);
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
  font-size: 1.4rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  border: none;
}

.floating-btn:hover {
  transform: scale(1.1) translateY(-3px);
  box-shadow: var(--shadow-hover);
}

.floating-btn:active {
  transform: scale(0.95);
}

.floating-favorite {
  color: var(--color-primary);
  background: white;
}

.floating-favorite.active {
  background: var(--color-primary);
  color: white;
}

.floating-favorite.active i::before {
  content: '\f004'; /* filled heart */
}

.floating-instagram {
  background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
  color: white;
}

.floating-whatsapp {
  background: #25D366;
  color: white;
}

/* 桌面版隱藏 */
@media (min-width: 768px) {
  .floating-actions {
    display: none;
  }
}

/* 小手機優化 */
@media (max-width: 380px) {
  .floating-btn {
    width: 48px;
    height: 48px;
    font-size: 1.2rem;
  }
  .floating-actions {
    bottom: 80px;
    right: 15px;
    gap: 10px;
  }
}
```

- [ ] **Step 3: Add floating button JavaScript**

在 `<script>` 中添加：

```javascript
// Floating Actions 顯示/隱藏邏輯
const floatingActions = document.getElementById('floating-actions');
const floatingFavorite = document.getElementById('floating-favorite');
let lastScrollY = 0;

function handleFloatingVisibility() {
  const currentScrollY = window.scrollY;
  
  // 向下滾動超過 150px 時顯示
  if (currentScrollY > 150) {
    floatingActions.classList.add('visible');
  } else {
    floatingActions.classList.remove('visible');
  }
  
  lastScrollY = currentScrollY;
}

window.addEventListener('scroll', handleFloatingVisibility, { passive: true });

// 收藏功能 (使用 localStorage)
const favoriteKey = 'myo_favorite_products';

function toggleFavorite() {
  const selectedColor = document.getElementById('selected-color-input').value;
  const selectedStyle = document.getElementById('selected-style-input').value;
  
  if (!selectedColor && !selectedStyle) {
    alert('請先選擇產品再收藏');
    return;
  }
  
  const favorite = {
    color: selectedColor,
    style: selectedStyle,
    timestamp: new Date().toISOString()
  };
  
  // 切換收藏狀態
  const isFavorite = floatingFavorite.classList.toggle('active');
  
  if (isFavorite) {
    localStorage.setItem(favoriteKey, JSON.stringify(favorite));
  } else {
    localStorage.removeItem(favoriteKey);
  }
}

// 檢查是否有已收藏的產品
function checkExistingFavorite() {
  const saved = localStorage.getItem(favoriteKey);
  if (saved) {
    floatingFavorite.classList.add('active');
  }
}

// 初始化
checkExistingFavorite();
floatingFavorite.addEventListener('click', toggleFavorite);
```

- [ ] **Step 4: Commit**

```bash
git add v2.html
git commit -m "feat: add floating action buttons

- Add WhatsApp, Instagram, Favorite buttons
- Show on scroll (150px threshold)
- Add favorite with localStorage persistence
- Mobile-optimized design
- Smooth slide-in animation"
```

---

### Task 6: Enhanced Mobile Sticky Bar

**Goal:** Enhance the existing sticky conversion bar with selected items display.

**Files:**
- Modify: `v2.html` (update existing sticky bar styles and add selection display)

- [ ] **Step 1: Update sticky bar HTML**

找到現有的 sticky-conversion-bar，替換為：

```html
<!-- Mobile Sticky Bar (Enhanced) -->
<div class="sticky-conversion-bar" id="sticky-conversion-bar">
  <div class="sticky-brand">
    <img src="image/01_company_logo.png" alt="My O! Logo" class="sticky-logo">
    <div class="sticky-brand-text">
      <span class="sticky-brand-name">My O!</span>
      <span class="sticky-brand-handle">myo.makeyourown</span>
    </div>
  </div>
  
  <div class="sticky-selection" id="sticky-selection">
    <span class="selection-text">請選擇產品</span>
  </div>
  
  <div class="sticky-actions">
    <a href="https://api.whatsapp.com/send?phone=85263796410&text=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E6%88%91%E5%BE%9E%E4%BD%A0%E5%80%91%E7%B6%B2%E7%AB%99%E4%B8%8A%E7%9C%8B%E5%88%B0%E9%80%99%E5%80%8B%E7%94%A2%E5%93%81%EF%BC%81%E6%9C%89%E8%88%88%E8%B6%A3%E4%BA%86%E8%A7%A3%E6%9B%B4%E5%A4%9A%EF%BC%81" target="_blank" class="sticky-cta">
      立即查詢
    </a>
  </div>
</div>
```

- [ ] **Step 2: Update sticky bar styles**

找到現有的 `.sticky-conversion-bar` 樣式，替換為：

```css
/* ===== Mobile Sticky Bar 增強版 ===== */
.sticky-conversion-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #ffffff;
  padding: 10px 16px 14px;
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.12);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  border-top: 3px solid var(--color-primary);
}

.sticky-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.sticky-logo {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.sticky-brand-text {
  display: flex;
  flex-direction: column;
}

.sticky-brand-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-secondary);
  line-height: 1.2;
}

.sticky-brand-handle {
  font-size: 0.7rem;
  color: var(--text-light);
  line-height: 1.2;
}

.sticky-selection {
  flex: 1;
  text-align: center;
  min-width: 0;
}

.selection-text {
  font-size: 0.8rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.selection-text.has-selection {
  color: var(--color-primary);
  font-weight: 500;
}

.sticky-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.sticky-cta {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: white;
  padding: 10px 18px;
  border-radius: 25px;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
  box-shadow: 0 3px 0 var(--color-primary-dark), 0 4px 12px rgba(183, 110, 121, 0.3);
  transition: all 0.2s ease;
}

.sticky-cta:active {
  transform: translateY(2px);
  box-shadow: 0 1px 0 var(--color-primary-dark);
}

.sticky-social {
  display: flex;
  gap: 6px;
}

.sticky-social-btn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  font-size: 1.1rem;
  transition: all 0.2s ease;
}

.sticky-ig {
  background: white;
  color: #E1306C;
  border: 1.5px solid #E1306C;
}

.sticky-ig:hover {
  background: #E1306C;
  color: white;
}

.sticky-wa {
  background: white;
  color: #25D366;
  border: 1.5px solid #25D366;
}

.sticky-wa:hover {
  background: #25D366;
  color: white;
}

/* 桌面版隱藏 */
@media (min-width: 768px) {
  .sticky-conversion-bar {
    display: none;
  }
}

/* 超小螢幕 */
@media (max-width: 380px) {
  .sticky-brand-text {
    display: none;
  }
  .sticky-selection {
    display: none;
  }
  .sticky-cta {
    padding: 8px 14px;
    font-size: 0.8rem;
  }
}
```

- [ ] **Step 3: Add selection display JavaScript**

在 `<script>` 中添加：

```javascript
// 更新 Sticky Bar 顯示選中產品
function updateStickySelection() {
  const selectedColor = document.getElementById('selected-color-input').value;
  const selectedStyle = document.getElementById('selected-style-input').value;
  const stickySelection = document.getElementById('sticky-selection');
  
  const colorNames = {
    'beige': '米色',
    'blue': '藍色'
  };
  
  const styleNames = {
    'style1': '款式1',
    'style2': '款式2',
    'style3': '款式3',
    'style4': '款式4',
    'style5': '款式5'
  };
  
  let selectionText = '';
  const selections = [];
  
  if (selectedColor && colorNames[selectedColor]) {
    selections.push(colorNames[selectedColor]);
  }
  if (selectedStyle && styleNames[selectedStyle]) {
    selections.push(styleNames[selectedStyle]);
  }
  
  if (selections.length > 0) {
    selectionText = selections.join(' + ');
    stickySelection.querySelector('.selection-text').textContent = selectionText;
    stickySelection.querySelector('.selection-text').classList.add('has-selection');
  } else {
    stickySelection.querySelector('.selection-text').textContent = '請選擇產品';
    stickySelection.querySelector('.selection-text').classList.remove('has-selection');
  }
}

// 在選擇時調用
// 在現有的選擇邏輯中添加：updateStickySelection();
```

- [ ] **Step 4: Integrate selection update into existing click handlers**

在現有的選擇卡片點擊監聽器中添加調用：

```javascript
// 在選擇顏色和款式的邏輯中，選擇後添加：
updateStickySelection();
```

- [ ] **Step 5: Commit**

```bash
git add v2.html
git commit -m "feat: enhance mobile sticky bar

- Add selection display (color + style)
- Show selected product names
- Improved styling with gradient CTA
- Social buttons (Instagram, WhatsApp)
- Responsive for small screens"
```

---

### Task 7: Animation System

**Goal:** Add page load animations and scroll-triggered fade-in effects.

**Files:**
- Modify: `v2.html` (add animation CSS and JavaScript)

- [ ] **Step 1: Add animation CSS**

在 `<style>` 中添加：

```css
/* ===== 動畫系統 ===== */

/* 頁面載入淡入動畫 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 交錯動畫延遲 */
.fade-in-up {
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
}

.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }
.stagger-4 { animation-delay: 0.4s; }
.stagger-5 { animation-delay: 0.5s; }

/* 區塊進場動畫 */
.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Hero 區塊動畫 */
.hero-section {
  animation: fadeInUp 0.8s ease-out;
}

/* 卡片進場 */
.card, .design-style-card {
  opacity: 0;
  animation: fadeInUp 0.5s ease-out forwards;
}

.card:nth-child(1), .design-style-card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2), .design-style-card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3), .design-style-card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4), .design-style-card:nth-child(4) { animation-delay: 0.4s; }
.card:nth-child(5), .design-style-card:nth-child(5) { animation-delay: 0.5s; }

/* 減少動畫 preference */
@media (prefers-reduced-motion: reduce) {
  .fade-in-up,
  .animate-on-scroll,
  .card, 
  .design-style-card,
  .select-option.selected,
  .select-option.selected::after {
    animation: none;
    opacity: 1;
    transform: none;
  }
  
  .select-option:hover,
  .floating-actions,
  .floating-btn:hover {
    transform: none;
  }
}
```

- [ ] **Step 2: Add scroll trigger JavaScript**

在 `<script>` 中添加：

```javascript
// Intersection Observer for scroll animations
const observerOptions = {
  root: null,
  rootMargin: '0px',
  threshold: 0.1
};

const animateOnScroll = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // Once animated, no need to observe again
      animateOnScroll.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe all animate-on-scroll elements
document.querySelectorAll('.animate-on-scroll').forEach(el => {
  animateOnScroll.observe(el);
});

// Add animate-on-scroll class to relevant sections
document.querySelectorAll('#designs, #product-overview, #contact').forEach(section => {
  section.classList.add('animate-on-scroll');
});
```

- [ ] **Step 3: Update existing cards to have animation**

確保選擇卡片在頁面載入時有進場動畫。更新選擇區塊的 HTML 結構：

為每個區塊添加延遲類別：
- 顏色選擇卡片：`.stagger-1`, `.stagger-2`
- 款式選擇 Swiper slides：各有動畫延遲

- [ ] **Step 4: Commit**

```bash
git add v2.html
git commit -m "feat: add animation system

- Add page load fade-in-up animations
- Add staggered animation delays
- Add Intersection Observer for scroll animations
- Add prefers-reduced-motion support
- Add animate-on-scroll class to main sections"
```

---

### Task 8: Hero Section & Content Refinement

**Goal:** Update hero section with refined styling and better CTA, update product overview section.

**Files:**
- Modify: `v2.html` (update hero and product sections)

- [ ] **Step 1: Update Hero section styles**

更新現有 `.hero-section` 樣式：

```css
/* Hero Section 更新 */
.hero-section {
  background: linear-gradient(135deg, var(--bg-primary) 0%, #F5EDE8 50%, #FDF8F5 100%);
  padding: 3rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* 添加微妙裝飾圖案 */
.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(183, 110, 121, 0.03) 0%, transparent 50%);
  animation: rotate 30s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.hero-section h1 {
  font-size: 2.8rem;
  font-weight: 700;
  color: var(--color-secondary);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.hero-section p {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 1.5rem;
  line-height: 1.7;
}

@media (max-width: 639px) {
  .hero-section {
    padding: 2rem 0;
  }
  .hero-section h1 {
    font-size: 2rem;
  }
  .hero-section p {
    font-size: 0.95rem;
  }
}
```

- [ ] **Step 2: Update section title styles**

更新 `.section-title` 樣式：

```css
.section-title {
  color: var(--color-secondary);
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
  margin: 0.5rem auto 0;
  border-radius: 2px;
}

@media (max-width: 639px) {
  .section-title {
    font-size: 1.6rem;
  }
}
```

- [ ] **Step 3: Update product overview section**

為產品特點區塊添加更好的視覺效果：

```css
/* 產品特點區塊 */
#product-overview {
  background: linear-gradient(180deg, var(--bg-primary) 0%, #F5EDE8 100%);
}

#product-overview ul li {
  padding: 0.75rem 0;
  border-bottom: 1px dashed rgba(183, 110, 121, 0.15);
}

#product-overview ul li:last-child {
  border-bottom: none;
}

#product-overview .feature-icon {
  color: var(--color-primary);
  font-size: 1.5rem;
  margin-right: 0.75rem;
}

/* 客製化文字區塊 */
.customization-text {
  background: rgba(183, 110, 121, 0.08);
  padding: 1.25rem;
  border-radius: var(--radius-md);
  border-left: 4px solid var(--color-primary);
}
```

- [ ] **Step 4: Commit**

```bash
git add v2.html
git commit -m "feat: refine hero and content sections

- Add decorative background pattern to hero
- Update section title with accent line
- Improve product overview styling
- Add gradient backgrounds
- Mobile responsive adjustments"
```

---

### Task 9: Final Responsive & Cross-Browser Check

**Goal:** Ensure all responsive breakpoints work correctly and perform final validation.

**Files:**
- Modify: `v2.html` (responsive adjustments)

- [ ] **Step 1: Add comprehensive responsive styles**

在 `<style>` 末尾添加響應式覆蓋：

```css
/* ===== 響應式最終調整 ===== */

/* 確保選擇區塊在所有設備上正確顯示 */
@media (max-width: 639px) {
  /* 選擇顏色區塊 - 手機版水平排列 */
  #designs .color-option-card {
    flex-direction: row;
    align-items: center;
    padding: 0.75rem;
  }
  
  #designs .color-option-card .color-circle {
    width: 28px;
    height: 28px;
    flex-shrink: 0;
  }
  
  #designs .color-option-card .image-container {
    width: 70px;
    height: 70px;
    margin-left: auto;
  }
  
  /* Swiper 調整 */
  .mySwiper {
    padding: 0 10px;
  }
  
  .swiper-slide {
    width: 85% !important;
  }
  
  /* 確保內容不被 floating actions 遮擋 */
  body {
    padding-bottom: 80px;
  }
}

@media (min-width: 640px) and (max-width: 767px) {
  .card {
    padding: 1rem;
  }
  
  .design-style-card {
    height: 260px;
  }
  
  .design-style-card .image-container-design {
    height: 120px;
  }
}

@media (min-width: 768px) {
  /* 桌面版恢復正常 */
  .hero-section {
    padding: 4rem 0;
  }
  
  .section-title {
    font-size: 2.2rem;
  }
}

/* 確保觸控友好 */
@media (hover: none) and (pointer: coarse) {
  .select-option:active,
  .design-style-card:active {
    transform: scale(0.98);
  }
  
  .btn-primary:active {
    transform: scale(0.96);
  }
}
```

- [ ] **Step 2: Add viewport meta verification**

確保 viewport meta tag 正確：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
```

- [ ] **Step 3: Test basic functionality**

檢查以下功能是否正常：
- [ ] 選項可以點擊選中（視覺反饋）
- [ ] Lightbox 可以打開和關閉
- [ ] 步驟指示器正確更新
- [ ] 浮動按鈕在滾動後出現
- [ ] 手機版 Sticky Bar 顯示
- [ ] 動畫流暢運行

- [ ] **Step 4: Commit**

```bash
git add v2.html
git commit -m "feat: add final responsive adjustments

- Add comprehensive responsive overrides
- Ensure touch-friendly interactions
- Add viewport scaling support
- Mobile-first optimizations complete"
```

---

### Task 10: Final Testing & Validation

**Goal:** Verify the complete implementation against the design spec.

**Files:**
- Test: `v2.html`

- [ ] **Step 1: Design spec verification**

對照設計規範檢查：

| 規範要求 | 實現狀態 |
|----------|----------|
| 色彩系統 (CSS variables) | ✅ Task 1 |
| 字體 (Noto Sans TC, Playfair Display) | ✅ Task 1 |
| 步驟指示器 | ✅ Task 2 |
| 選擇卡片動畫 | ✅ Task 3 |
| 勾選標記動畫 | ✅ Task 3 |
| Lightbox 增強版 | ✅ Task 4 |
| 浮動快捷按鈕 | ✅ Task 5 |
| Mobile Sticky Bar 增強 | ✅ Task 6 |
| 頁面載入動畫 | ✅ Task 7 |
| 滾動觸發動畫 | ✅ Task 7 |
| 響應式設計 | ✅ Task 8, 9 |

- [ ] **Step 2: Check all images are accessible**

確保所有圖片路徑正確：
- `image/01_company_logo.png`
- `image/cert_color_beige.jpg`
- `image/cert_color_blue.jpg`
- `image/cert_style_1.png` - `cert_style_5.png`

- [ ] **Step 3: Verify external CDN resources**

檢查外部資源：
- Tailwind CSS CDN
- Google Fonts
- Font Awesome
- Swiper.js

- [ ] **Step 4: Commit final version**

```bash
git add v2.html
git commit -m "chore: complete v2.html implementation

- All design requirements implemented
- Responsive design verified
- Animation system complete
- Ready for testing"
```

---

## Implementation Complete

**Plan saved to:** `docs/superpowers/plans/2026-05-13-index-revamp-plan.md`

---

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?