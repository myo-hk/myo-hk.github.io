# Poster Aspect Ratio 維持規格

> **建立日期:** 2026-05-15
> **功能名稱:** 海報長寬比維持
> **目標:** 確保 poster.html 在任何螢幕大小下都維持 A5 紙張比例 (1:1.414)

## 1. 問題描述

目前 poster.html 在不同螢幕大小的瀏覽器中開啟時：
- 寬度會隨螢幕調整（最多 420px）
- 但高度是固定的 `min-height: 500px`
- 這導致在不同螢幕比例下，海報的外觀會變形

## 2. 期望行為

- **桌面環境:** 海報維持固定的 A5 長寬比例 (148mm × 210mm = 1:1.414)
- **手機環境:** 海報在小螢幕上也能維持比例，不會被裁剪或變形
- **打印:** 不受影響，保持原有的打印優化樣式

## 3. 技術方案

### 方案：CSS aspect-ratio + max-height 限制

使用 CSS `aspect-ratio` 屬性來維持固定比例：

```css
.a5-flyer {
    aspect-ratio: 148 / 210;  /* A5 紙張比例 */
    height: auto;
    max-height: 90vh;  /* 限制最大高度 */
}
```

### 備用方案：JavaScript 自動縮放

如果 CSS aspect-ratio 在舊版瀏覽器不相容，使用 JavaScript 計算：

```javascript
function maintainAspectRatio() {
    const poster = document.querySelector('.a5-flyer');
    const aspectRatio = 148 / 210;
    const width = poster.offsetWidth;
    poster.style.height = (width / aspectRatio) + 'px';
}
```

## 4. 驗收標準

- [ ] 在 1920x1080 桌面環境中，海報維持正確 A5 比例
- [ ] 在 375x667 手機環境中，海報維持正確 A5 比例，不會被裁剪
- [ ] 在平板環境（如 768x1024）中測試通過
- [ ] 打印樣式保持正常（不受影響）
- [ ] 原有功能（品牌連結、QR code 點擊）保持正常

## 5. 檔案變更

- **修改:** `poster.html` - 添加 aspect-ratio CSS 屬性
- **影響:** 只有 `.a5-flyer` 容器的 CSS 樣式