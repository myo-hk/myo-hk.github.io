# 教訓：poster.html PDF 列印縮放公式

> **日期**：2026-07-20  
> **關聯 PR**：Lighthouse CLS 深度修復  
> **狀態**：已解決

---

### 問題

`poster.html` 提供「下載 PDF」功能，透過 `window.print()` 輸出 A5 海報到 A4 紙張。  
多次嘗試後仍無法正確縮放：

| # | 嘗試 | 問題 |
|---|------|------|
| 1 | `html2canvas` + `jsPDF` | 圖片被 CSS 壓扁（`object-fit: cover`、`flex`、`padding` 無法被正確捕捉）|
| 2 | `window.open()` + `document.write()` | POPUP 視窗中所有圖片變空白（重建 DOM 丟失圖片資源參照）|
| 3 | `@media print` + `transform: scale(calc(...))` | 海報被推到右下，左邊大片空白、右邊內容飛出 A4 |

### 教訓

**核心洞察**：print 時必須先「釘死」容器在 `(0, 0)`，再從左上角縮放。  
`margin: 0 auto` / flex 居中會在 print 時將容器推到畫面中央，`transform-origin: top left` 在此基礎上縮放 → 位移放大。

### 解法

```css
@media print {
  .a5-flyer {
    position: absolute !important;   /* 脫離排版流，避免居中位移 */
    left: 0 !important;
    top: 0 !important;
    margin: 0 !important;            /* 拔除 margin: 0 auto */
    width: 420px !important;         /* 海報原始設計寬度 */
    transform: scale(1.8898) !important;  /* A4 width(793.7px) / poster(420px) */
    transform-origin: top left !important;
  }
}
```

### 關鍵數字

| 參數 | 數值 | 來源 |
|------|------|------|
| 海報設計寬度 | 420px | `.a5-flyer` |
| A4 寬度（96 DPI） | 793.7px | `210mm × 3.7795 px/mm` |
| A4 高度 | 1123px | 海報高度 530px × 1.8898 = 1002px（< A4 高度，正常留白） |
| 縮放倍數 | 1.8898 | `793.7 / 420`，硬編碼避免 `calc()` 單位混算 |

### 預防

- 任何涉及 `window.print()` 的列印功能，優先測試 `position: absolute` + 硬編碼 `scale()`
- 勿用 `html2canvas` 處理現代 CSS 佈局（flexbox、gap、object-fit）
- 勿用 `window.open()` 重建 DOM 做列印 —— 圖片資源會斷

---

## 教訓：翻譯文案會撐破 A5 單頁高度上限

> **日期**：2026-09-29
> **關聯變更**：新增 `poster-en.html`（英文版）
> **狀態**：已解決

### 問題

`poster.html` 是固定寬度（420px）、高度由內容決定的海報。列印時整體 `scale(1.8898)`，
因此**高度預算 = `1123 / 1.8898 = 594px`**（設計稿 px）。超出就會印成兩頁，第二頁是空白。

把同一版面翻成英文後（英文通常比中文長 1.5–2 倍），`.a5-flyer` 從 578px 變成 **620px**，
溢出差 26px —— 下載的 PDF 多出一張空白頁。

量測結果（`getBoundingClientRect`）：

| 區塊 | 中文版 | 英文版（修前） | 英文版（修後） |
|------|--------|----------------|----------------|
| `.highlights-section` | 159px | **206px** | 135px |
| `.personalize-section` | — | 69px | 47px |
| `.a5-flyer` 總高 | 578px | **620px** ❌ | 527px ✅ |

主因是 `.highlight-item` 欄寬僅 101px，約 21 個英文字元就換行：
「Secure Protection」（17 字元）標題爆成兩行、四個說明文各多佔一行。

### 解法

1. **改文案而非改版面**。固定寬度的列印版面不可用「放大字體」救場——
   欄寬 101px 是硬上限，標題字級一放大就重新換行。改用更短的英文字串：
   - `Secure Protection` → `Safe Protection`
   - `Fits the HK Registry of Marriages` → `Fits HK A4 certificate`
   - 說明文重寫成每行 ≤ 21 字元，並保留 `<br>` 控制斷行位置
2. **量測驗證，不要目視**。判斷標準是 `.a5-flyer.offsetHeight ≤ 594`。
3. 把這條上限寫成回歸測試（`tests/poster-en.spec.ts`）：

```ts
const A4_HEIGHT_PX = 1123;
const PRINT_SCALE = 1.8898;
expect(height * PRINT_SCALE).toBeLessThanOrEqual(A4_HEIGHT_PX);
```

### 預防

- **任何要新增翻譯版本的固定版面頁面，先量高度預算再動手。**
  高度上限 = `A4 高度px ÷ scale`，不是看起來「排得下」。
- 翻譯後必量 `.a5-flyer.offsetHeight`，並與原版對比；
  差異超過 10% 就會明顯改變成品比例。
- 欄寬固定時，`<br>` 必須按目標語言的字元數重新定位，照抄原版的斷行點會炸。

