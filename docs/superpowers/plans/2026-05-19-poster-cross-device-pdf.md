# Poster Cross-Device Consistency & PDF Download Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure poster.html renders identically across desktop/tablet/mobile AND provide PDF download functionality while maintaining print-to-web consistency.

**Architecture:**
- Use existing JavaScript `transform: scale()` approach for cross-device consistency (already implemented)
- Add html2canvas + jsPDF for client-side PDF generation
- PDF download button triggers capture of poster element and generates A4 PDF

**Tech Stack:** html2canvas (v1.4.1), jsPDF (v2.5.1), vanilla JavaScript

---

## File Structure

- **Modify:** `poster.html` - Add PDF download button and JS library imports
- **No new files required** - All functionality added inline

---

## Task 1: Add PDF Download Button

**Files:**
- Modify: `poster.html:805-815` (add button after `<body>` opening tag)

- [ ] **Step 1: Add PDF download button HTML**

Add this button right after `<body>` tag (line 805):

```html
    <!-- PDF Download Button -->
    <button id="downloadPdfBtn" style="position: fixed; top: 20px; right: 20px; z-index: 9999; background: #2D2926; color: #F7F5F0; border: none; padding: 12px 20px; border-radius: 8px; font-family: 'Montserrat', sans-serif; font-size: 12px; font-weight: 500; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <i class="fas fa-download" style="margin-right: 8px;"></i>下載 PDF
    </button>
```

- [ ] **Step 2: Verify button appears in browser**

Run: Open `poster.html` in browser
Expected: Button visible in top-right corner

- [ ] **Step 3: Commit**

```bash
git add poster.html
git commit -m "feat: add PDF download button UI"
```

---

## Task 2: Integrate html2canvas + jsPDF Libraries

**Files:**
- Modify: `poster.html:9-10` (add CDN script tags)

- [ ] **Step 1: Add library CDN links**

Add these two lines after the Font Awesome CDN (line 9):

```html
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
```

- [ ] **Step 2: Verify libraries load without errors**

Run: Open browser DevTools Console, navigate to poster.html
Expected: No 404 errors, both scripts loaded

- [ ] **Step 3: Commit**

```bash
git add poster.html
git commit -m "feat: add html2canvas and jsPDF libraries"
```

---

## Task 3: Implement PDF Generation Logic

**Files:**
- Modify: `poster.html:1014-1015` (add PDF generation script before closing `</body>`)

- [ ] **Step 1: Add PDF generation JavaScript**

Replace the existing `</script>` at line 1014 with:

```javascript
        // 等比縮放海報以適應螢幕 - 永遠按比例縮放
        (function() {
            const poster = document.querySelector('.a5-flyer');
            const baseWidth = 420;
            let savedScale = '';

            function scalePoster() {
                const viewportWidth = window.innerWidth;
                const padding = 20;
                const availableWidth = viewportWidth - padding;

                // 永遠計算比例，讓海報永遠按比例顯示
                const scale = Math.min(1, availableWidth / baseWidth);
                poster.style.transform = 'scale(' + scale + ')';
                poster.style.transformOrigin = 'top center';
                savedScale = 'scale(' + scale + ')';
            }

            // 初始執行
            scalePoster();

            // 監聽視窗大小變化
            window.addEventListener('resize', scalePoster);
            window.addEventListener('orientationchange', function() {
                setTimeout(scalePoster, 100);
            });

            // 打印前禁用縮放
            window.addEventListener('beforeprint', function() {
                poster.style.transform = 'none';
            });

            // 打印後恢復縮放
            window.addEventListener('afterprint', function() {
                poster.style.transform = savedScale;
            });
        })();

        // PDF 下載功能
        (function() {
            const downloadBtn = document.getElementById('downloadPdfBtn');
            const poster = document.querySelector('.a5-flyer');

            downloadBtn.addEventListener('click', async function() {
                // 禁用按鈕防止重複點擊
                downloadBtn.disabled = true;
                downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right: 8px;"></i>生成中...';

                try {
                    // 暫時移除 transform 以獲取真實尺寸
                    const originalTransform = poster.style.transform;
                    poster.style.transform = 'none';

                    // 等待下一幀確保 DOM 更新
                    await new Promise(resolve => requestAnimationFrame(resolve));

                    // 使用 html2canvas 捕獲海報
                    const canvas = await html2canvas(poster, {
                        scale: 2, // 2x 解析度確保清晰
                        useCORS: true,
                        allowTaint: true,
                        backgroundColor: '#F7F5F0',
                        width: poster.offsetWidth,
                        height: poster.offsetHeight
                    });

                    // 恢復 transform
                    poster.style.transform = originalTransform;

                    // 計算 A4 尺寸 (210mm x 297mm in pixels at 96 DPI)
                    const a4WidthMm = 210;
                    const a4HeightMm = 297;
                    const dpi = 96;
                    const a4WidthPx = Math.round(a4WidthMm * dpi / 25.4); // ~794px
                    const a4HeightPx = Math.round(a4HeightMm * dpi / 25.4); // ~1123px

                    // 創建 jsPDF 實例 (縱向 A4)
                    const { jsPDF } = window.jspdf;
                    const pdf = new jsPDF({
                        orientation: 'portrait',
                        unit: 'mm',
                        format: 'a4'
                    });

                    // 計算圖片在 A4 上的尺寸 (保持比例)
                    const imgWidthMm = a4WidthMm; // 寬度充滿
                    const imgHeightMm = (canvas.height / canvas.width) * imgWidthMm;

                    // 如果高度超過 A4，則縮小以容納
                    let finalWidthMm = imgWidthMm;
                    let finalHeightMm = imgHeightMm;
                    if (imgHeightMm > a4HeightMm) {
                        finalHeightMm = a4HeightMm;
                        finalWidthMm = (canvas.width / canvas.height) * a4HeightMm;
                    }

                    // 居中放置
                    const xOffset = (a4WidthMm - finalWidthMm) / 2;
                    const yOffset = (a4HeightMm - finalHeightMm) / 2;

                    // 將 canvas 轉換為圖片數據
                    const imgData = canvas.toDataURL('image/jpeg', 0.95);

                    // 添加圖片到 PDF
                    pdf.addImage(imgData, 'JPEG', xOffset, yOffset, finalWidthMm, finalHeightMm);

                    // 下載 PDF
                    pdf.save('myo-poster.pdf');

                } catch (error) {
                    console.error('PDF 生成失敗:', error);
                    alert('PDF 生成失敗，請稍後再試。');
                    // 恢復 transform
                    poster.style.transform = originalTransform;
                }

                // 恢復按鈕狀態
                downloadBtn.disabled = false;
                downloadBtn.innerHTML = '<i class="fas fa-download" style="margin-right: 8px;"></i>下載 PDF';
            });
        })();
    </script>
```

- [ ] **Step 2: Verify PDF downloads correctly**

Run: Open poster.html in browser, click "下載 PDF" button
Expected: PDF file downloads with A4 size containing the poster

- [ ] **Step 3: Commit**

```bash
git add poster.html
git commit -m "feat: implement PDF download with html2canvas and jsPDF"
```

---

## Task 4: Verify Cross-Device Consistency

**Files:**
- No changes - testing task

- [ ] **Step 1: Test desktop (1920x1080)**

Run: Open poster.html at 1920x1080
Expected: Poster at 420px width, no text wrapping, layout intact

- [ ] **Step 2: Test tablet (768x1024)**

Run: Open poster.html at 768x1024 (use DevTools device mode)
Expected: Poster scales proportionally, same layout as desktop

- [ ] **Step 3: Test mobile (375x667)**

Run: Open poster.html at 375x667 (use DevTools device mode)
Expected: Poster scales proportionally, same layout as desktop, no text wrapping

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "test: verify cross-device consistency"
```

---

## Task 5: Verify Print Preview Matches Webpage

**Files:**
- No changes - testing task

- [ ] **Step 1: Test Chrome print preview**

Run: Open poster.html, press Ctrl/Cmd+P
Expected: Poster centered, scaled to fill page, no URL/page numbers

- [ ] **Step 2: Test iOS Safari print (if available)**

Run: Open poster.html on iOS Safari, use share > Print
Expected: Poster centered, scaled properly, no URL/footer

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "test: verify print preview consistency"
```

---

## Task 6: Final Review and Push

- [ ] **Step 1: Review all changes**

Run: `git diff --stat`
Expected: Only poster.html modified

- [ ] **Step 2: Push to fork**

```bash
git push origin main
```

- [ ] **Step 3: Verify PR status**

Run: `gh pr list --repo upstream/myo-hk`
Expected: PR #14 or new PR if needed

---

## Self-Review Checklist

1. **Spec coverage:**
   - [x] Cross-device consistency via JS scale() - Task 1-4
   - [x] Print preview matches webpage - Task 5
   - [x] PDF download button - Task 1-3
   - [x] Both webpage display AND download - Task 1-3

2. **Placeholder scan:** No TBD/TODO patterns found

3. **Type consistency:** N/A - no type system used in this project

---

**Plan complete and saved to `docs/superpowers/plans/2026-05-19-poster-cross-device-pdf.md`**

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**