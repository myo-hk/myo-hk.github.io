# 廣告收入設置指南

> **用途**: 指導廣告收入的實施流程
> **適用範圍**: myo-hk.github.io
> **最後更新**: 2026-04-02

---

## Google AdSense 申請流程

### Step 1: 準備工作
- [ ] 網站有至少 10-15 篇高質量文章（目前 5 篇，需繼續擴展）
- [ ] 網站有隱私政策頁面
- [ ] 網站有關於我們頁面
- [ ] 網站有聯繫方式

### Step 2: 申請 AdSense
1. 前往 https://www.google.com/adsense
2. 點擊「立即註冊」
3. 輸入網站 URL：`https://myo-hk.github.io`
4. 填寫個人資料和付款資訊
5. 獲取廣告代碼，加入網站 `<head>`

### Step 3: 放置廣告代碼
```html
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
```

### Step 4: 等待審核
- 審核時間：1-2 週
- 審核標準：內容質量、網站流量、用戶體驗

---

## 廣告位置設計

### 推薦位置
1. **文章內容中間**：每 500 字一個廣告
2. **側邊欄**（桌面版）：固定廣告
3. **頁尾上方**：橫幅廣告

### HTML 廣告單元模板
```html
<!-- 文章內廣告 -->
<div class="my-8 text-center">
  <ins class="adsbygoogle"
       style="display:block"
       data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
       data-ad-slot="XXXXXXXXXX"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>
```

---

## 預估收入

| 月流量 | AdSense 預估 | 備註 |
|--------|-------------|------|
| 1,000 | HK$100-300 | 剛開始 |
| 5,000 | HK$500-1,500 | 穩定增長 |
| 10,000 | HK$1,000-3,000 | 可觀收入 |
| 50,000 | HK$5,000-10,000 | 主要收入來源 |

---

## 其他廣告網絡選項

| 平台 | 最低流量要求 | 預估 RPM | 備註 |
|------|-------------|---------|------|
| Google AdSense | 無 | $1-5 | 最容易申請 |
| Ezoic | 10,000 | $5-15 | 需要較多流量 |
| Mediavine | 50,000 | $15-30 | 高收入但門檻高 |
| AdThrive | 100,000 | $20-40 | 頂級廣告網絡 |

---

## AdSense 政策遵守

- [ ] 不點擊自己的廣告
- [ ] 不鼓勵他人點擊廣告
- [ ] 不放置廣告在彈出視窗
- [ ] 不隱藏廣告標籤
- [ ] 廣告不影響用戶體驗
- [ ] 定期檢查廣告表現
