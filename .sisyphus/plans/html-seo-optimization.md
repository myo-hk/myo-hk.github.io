# HTML 靜態站 SEO 優化方案

> **用途**: 指導所有 HTML 頁面的創建和優化
> **適用範圍**: myo-hk.github.io 純 HTML 靜態站
> **最後更新**: 2026-04-02

---

## 1. SEO 基礎模板

### 完整的 HTML Head 結構

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- 核心 SEO Meta Tags -->
    <title>文章標題 | My O! 專屬結婚證書套</title>
    <meta name="description" content="文章描述（150-160 字元，包含主關鍵字）">
    <meta name="keywords" content="關鍵字1, 關鍵字2, 關鍵字3">
    <link rel="canonical" href="https://myo-hk.github.io/blog/文章檔名.html">
    
    <!-- Open Graph (Facebook/LinkedIn) -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="文章標題">
    <meta property="og:description" content="文章描述">
    <meta property="og:image" content="https://myo-hk.github.io/image/文章封面圖.jpg">
    <meta property="og:image:alt" content="圖片描述">
    <meta property="og:url" content="https://myo-hk.github.io/blog/文章檔名.html">
    <meta property="og:site_name" content="My O! 專屬結婚證書套">
    <meta property="og:locale" content="zh_HK">
    <meta property="article:published_time" content="2026-04-02T00:00:00+08:00">
    <meta property="article:modified_time" content="2026-04-02T00:00:00+08:00">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="文章標題">
    <meta name="twitter:description" content="文章描述">
    <meta name="twitter:image" content="https://myo-hk.github.io/image/文章封面圖.jpg">
    
    <!-- 其他 -->
    <link rel="icon" href="/image/01_company_logo.png" type="image/png">
    <link rel="shortcut icon" href="/image/01_company_logo.png" type="image/png">
    
    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "文章標題",
      "description": "文章描述",
      "image": "https://myo-hk.github.io/image/文章封面圖.jpg",
      "author": {
        "@type": "Organization",
        "name": "My O! 專屬結婚證書套"
      },
      "publisher": {
        "@type": "Organization",
        "name": "My O! 專屬結婚證書套",
        "logo": {
          "@type": "ImageObject",
          "url": "https://myo-hk.github.io/image/01_company_logo.png"
        }
      },
      "datePublished": "2026-04-02",
      "dateModified": "2026-04-02"
    }
    </script>
    
    <!-- 現有樣式 -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
</head>
```

---

## 2. 語義化 HTML5 結構

```html
<body>
    <!-- 導航 -->
    <nav>...</nav>
    
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb">...</nav>
    
    <!-- 主要內容 -->
    <main>
        <article>
            <header>
                <h1>文章標題</h1>
                <p class="meta">
                    <time datetime="2026-04-02">2026年4月2日</time> · 
                    <span>閱讀時間：約 8 分鐘</span>
                </p>
            </header>
            
            <!-- 文章內容 -->
            <div class="content">
                <h2>第一節標題</h2>
                <p>內容...</p>
                
                <h3>子標題</h3>
                <p>內容...</p>
            </div>
            
            <!-- 免責聲明 -->
            <div class="disclaimer">...</div>
            
            <!-- CTA -->
            <div class="cta">...</div>
        </article>
        
        <!-- 相關文章 -->
        <aside>
            <h2>相關文章</h2>
            <ul>
                <li><a href="相關文章1.html">標題</a></li>
                <li><a href="相關文章2.html">標題</a></li>
            </ul>
        </aside>
    </main>
    
    <!-- 頁尾 -->
    <footer>...</footer>
</body>
```

---

## 3. Sitemap.xml 模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://myo-hk.github.io/</loc>
    <lastmod>2026-04-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://myo-hk.github.io/blog/</loc>
    <lastmod>2026-04-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://myo-hk.github.io/blog/香港結婚完整攻略.html</loc>
    <lastmod>2026-04-02</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <!-- 每新增一篇文章，在此添加一個 <url> 區塊 -->
</urlset>
```

**提交到 Google Search Console**:
1. 前往 https://search.google.com/search-console
2. 選擇你的網站
3. 左側選單點擊「Sitemap」
4. 輸入 `sitemap.xml` 並提交

---

## 4. Robots.txt 配置

```txt
User-agent: *
Allow: /

Sitemap: https://myo-hk.github.io/sitemap.xml
```

---

## 5. 文章頁面 HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <!-- 使用上面的 SEO Head 模板 -->
</head>
<body>
    <!-- 導航（複製自 index.html） -->
    <nav class="bg-white p-4 shadow-md sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="flex items-center">
                <img src="/image/01_company_logo.png" class="h-6 w-6 mr-2" alt="My O! logo">
                <span class="text-rose-500 font-bold">My O!</span>
            </a>
            <div class="space-x-6">
                <a href="/" class="text-gray-600 hover:text-rose-500">首頁</a>
                <a href="/blog/" class="text-gray-600 hover:text-rose-500">博客</a>
                <a href="/#contact" class="text-gray-600 hover:text-rose-500">聯絡我們</a>
            </div>
        </div>
    </nav>

    <!-- Breadcrumb -->
    <div class="container mx-auto px-4 py-4">
        <nav aria-label="breadcrumb" class="text-sm text-gray-500">
            <a href="/" class="hover:text-rose-500">首頁</a> &gt;
            <a href="/blog/" class="hover:text-rose-500">博客</a> &gt;
            <span class="text-gray-700">文章標題</span>
        </nav>
    </div>

    <!-- 主要內容 -->
    <main class="container mx-auto px-4 py-8 max-w-3xl">
        <article>
            <header class="mb-8">
                <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-4">文章標題</h1>
                <div class="flex items-center text-sm text-gray-500 space-x-4">
                    <time datetime="2026-04-02">2026年4月2日</time>
                    <span>·</span>
                    <span>閱讀時間：約 8 分鐘</span>
                    <span>·</span>
                    <span>最後更新：2026年4月2日</span>
                </div>
            </header>

            <!-- 文章內容 -->
            <div class="prose prose-lg max-w-none">
                <h2 class="text-2xl font-bold text-gray-800 mt-8 mb-4">第一節標題</h2>
                <p class="text-gray-700 leading-relaxed mb-4">內容...</p>
                
                <h3 class="text-xl font-semibold text-gray-800 mt-6 mb-3">子標題</h3>
                <p class="text-gray-700 leading-relaxed mb-4">內容...</p>
            </div>

            <!-- 免責聲明 -->
            <div class="bg-gray-50 p-4 border-l-4 border-amber-600 my-8 text-sm text-gray-600">
                <strong>免責聲明：</strong>
                本文內容僅供參考，不構成法律意見。香港婚姻登記相關規定可能隨時更新，
                請以<a href="https://www.immd.gov.hk/hkt/marriage/Registration_of_a_Marriage.html" target="_blank" rel="noopener" class="text-amber-600 hover:underline">入境事務處官方網頁</a>
                的最新公佈為準。
            </div>

            <!-- CTA -->
            <div class="bg-rose-50 rounded-2xl p-6 text-center my-8">
                <h3 class="text-xl font-bold text-gray-800 mb-2">準備好定制您的專屬證書套了嗎？</h3>
                <p class="text-gray-600 mb-4">立即透過 WhatsApp 或 Instagram 聯絡我們！</p>
                <a href="https://api.whatsapp.com/send?phone=85263796410" target="_blank" class="inline-block bg-green-500 text-white px-6 py-3 rounded-full font-semibold hover:bg-green-600 transition">
                    <i class="fab fa-whatsapp mr-2"></i>WhatsApp 聯絡我們
                </a>
            </div>
        </article>

        <!-- 相關文章 -->
        <aside class="mt-12">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">相關文章</h2>
            <div class="grid md:grid-cols-2 gap-4">
                <a href="相關文章1.html" class="block p-4 bg-white rounded-xl shadow hover:shadow-md transition">
                    <h3 class="font-semibold text-gray-800 mb-2">相關文章標題 1</h3>
                    <p class="text-sm text-gray-600">簡短描述...</p>
                </a>
                <a href="相關文章2.html" class="block p-4 bg-white rounded-xl shadow hover:shadow-md transition">
                    <h3 class="font-semibold text-gray-800 mb-2">相關文章標題 2</h3>
                    <p class="text-sm text-gray-600">簡短描述...</p>
                </a>
            </div>
        </aside>
    </main>

    <!-- 頁尾（複製自 index.html） -->
    <footer class="bg-gray-800 text-white py-5">
        <div class="container mx-auto px-4 text-center">
            <p class="mb-1 text-sm">© 2026 My O! 版權所有。</p>
            <div class="space-x-2 text-sm">
                <a href="#" class="text-amber-400 hover:text-amber-300">隱私政策</a>
                <a href="#" class="text-amber-400 hover:text-amber-300">服務條款</a>
            </div>
        </div>
    </footer>
</body>
</html>
```

---

## 6. 博客索引頁模板

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <title>博客 | My O! 專屬結婚證書套</title>
    <meta name="description" content="香港婚慶攻略、結婚註冊教學、證書套推薦等實用文章。">
    <link rel="canonical" href="https://myo-hk.github.io/blog/">
    <!-- 其他 SEO tags -->
</head>
<body>
    <!-- 導航 -->
    <nav>...</nav>

    <main class="container mx-auto px-4 py-8 max-w-4xl">
        <h1 class="text-3xl font-bold text-gray-800 mb-8">My O! 博客</h1>
        <p class="text-gray-600 mb-8">香港婚慶攻略、結婚註冊教學、證書套推薦等實用文章。</p>

        <!-- 文章列表 -->
        <div class="space-y-6">
            <!-- Pillar Page -->
            <a href="香港結婚完整攻略.html" class="block p-6 bg-white rounded-xl shadow hover:shadow-md transition">
                <span class="inline-block px-3 py-1 bg-rose-100 text-rose-600 text-sm font-semibold rounded-full mb-2">精選</span>
                <h2 class="text-xl font-bold text-gray-800 mb-2">2026 香港結婚完整攻略：由註冊到婚宴的每一步</h2>
                <p class="text-gray-600 mb-2">從遞交擬結婚通知書到婚禮當日，完整教學。</p>
                <span class="text-sm text-gray-500">2026年4月2日 · 約 15 分鐘閱讀</span>
            </a>

            <!-- Cluster Pages -->
            <a href="結婚註冊流程教學.html" class="block p-6 bg-white rounded-xl shadow hover:shadow-md transition">
                <span class="inline-block px-3 py-1 bg-blue-100 text-blue-600 text-sm font-semibold rounded-full mb-2">教學</span>
                <h2 class="text-xl font-bold text-gray-800 mb-2">香港結婚註冊流程教學（2026 最新版）</h2>
                <p class="text-gray-600 mb-2">詳細步驟教學，包含文件清單和預約流程。</p>
                <span class="text-sm text-gray-500">2026年4月2日 · 約 8 分鐘閱讀</span>
            </a>

            <!-- 更多文章... -->
        </div>
    </main>

    <!-- 頁尾 -->
    <footer>...</footer>
</body>
</html>
```

---

## 7. Core Web Vitals 優化

### 圖片優化
```html
<!-- Lazy Loading -->
<img src="image/photo.jpg" alt="描述" loading="lazy" width="800" height="600">

<!-- WebP 格式（如果可用） -->
<picture>
    <source srcset="image/photo.webp" type="image/webp">
    <img src="image/photo.jpg" alt="描述" loading="lazy">
</picture>
```

### 字體優化
```html
<!-- font-display: swap 已包含在 Google Fonts URL 中 -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
```

### CSS/JS 最小化
- Tailwind CSS CDN 已是最小化版本
- Font Awesome 使用 CDN 最小化版本
- 自定義 CSS 保持在 `<style>` 標籤中，避免額外請求

---

## 8. Mobile-Friendly 檢查清單

- [ ] viewport meta tag 已設置
- [ ] 字體大小至少 16px
- [ ] 按鈕/連結間距至少 44x44px
- [ ] 圖片響應式（max-width: 100%）
- [ ] 導航在手機版可正常使用
- [ ] 內容寬度不超過視窗寬度
- [ ] 測試工具：https://search.google.com/test/mobile-friendly

---

## 9. E-E-A-T 信號強化

### 作者頁面設計
在每篇文章中加入作者資訊：
```html
<div class="author-box flex items-center p-4 bg-gray-50 rounded-xl my-8">
    <img src="/image/01_company_logo.png" alt="My O!" class="w-12 h-12 rounded-full mr-4">
    <div>
        <p class="font-semibold text-gray-800">My O! 團隊</p>
        <p class="text-sm text-gray-600">專注香港婚慶產品，為新人提供高質素結婚證書套。</p>
    </div>
</div>
```

### 關於我們頁面
在頁尾加入「關於我們」連結，創建 `about.html`：
- 公司介紹
- 聯繫方式（WhatsApp, Instagram）
- 專業資歷/經驗
