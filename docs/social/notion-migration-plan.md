# MyO Notion 內容庫遷移計劃

> **日期**：2026-09-30
> **目標頁面**：Notion workspace `myo-makeyourown`
> **母頁**：`MyO Cert HoderSocial Media Idea`（`3e96ee9afad2807e822fcb479a3305aa`）
> **參考藍圖**：TeaWikiHK 社群媒體運營手冊（`3d46ee9afad281b4ad0dc581e76d7145`）
> **狀態**：待批准，尚未執行任何 Notion 寫入

---

## 1. 品牌色真相（從 repo 抽取，非茶色）

TeaWiki 用琥珀金 `#C8963A`。**MyO 不是金色品牌**，不可沿用。實查結果：

| 角色 | 色值 | 出處 |
|---|---|---|
| 主色（玫瑰粉） | `#B76E79` | `v2.html:73` `--color-primary` |
| 主色深 | `#9A5A63` | `v2.html:74` `--color-primary-dark` |
| 副色（深褐） | `#5D4037` | `v2.html:75` `--color-secondary` |
| 強調（燙金） | `#D4AF37` | `v2.html:76` `--color-accent` |
| 背景（暖米白） | `#FAF8F5` | `v2.html:68` `--bg-primary` |
| 背景次要 | `#FDFAF6` | `v2.html:69` `--bg-secondary` |
| 文字主 | `#333333` | `v2.html:79` |
| 宣傳單底色 | `#F7F5F0` | `poster.html` |
| 宣傳單文字階梯 | `#4A4540` / `#5A5550` / `#2D2926` | `poster.html` |
| 淺金 | `#f6dba6` | `index.html` |
| 淺粉底 | `#ffece6` | `index.html` |

`#25D366`（WhatsApp 綠）與 `#E1306C`（IG 粉）**不是品牌色**，排除。

### MyO BPP（每張圖必須完整貼上）

```
magazine editorial style, Noto Serif TC typography, dusty rose pink accent #B76E79,
hot foil gold accent #D4AF37, deep cocoa brown #4A4540, warm off-white background #FAF8F5,
large negative space, dual thin border frame, low saturation warm tones,
minimalist East Asian wedding aesthetic, clean layout with generous white margins,
refined wedding stationery and certificate imagery, soft diffused natural light
```

### 尺寸（沿用 TeaWiki，IG 規格不變）

| 用途 | 比例 |
|---|---|
| IG Single | 1:1 |
| IG Carousel | 4:5 |
| IG Stories | 9:16 |
| IG Reels 封面 | 9:16 |
| Threads 配圖 | 1:1 |

---

## 2. 六個子頁（不含電子報）

TeaWiki 有 7 個，MyO 去掉「電子報系統」→ 6 個。

| # | 子頁 | 內容大綱 |
|---|---|---|
| 1 | 📊 **內容企劃總覽** | 三個月主題路線、27 列分配、四大支柱佔比、逐月 KPI 目標 |
| 2 | 📱 **雙平台策略** | IG 定位／Threads 定位、**IG→Threads 變形規則**、視覺調性、Link in bio |
| 3 | 🎨 **品牌視覺手冊** | MyO BPP、品牌色表、尺寸表、生成注意事項 |
| 4 | 📝 **執行流程 SOP** | 五步操作、執行節奏、狀態定義、每週檢查清單 |
| 5 | 📈 **數據追蹤模板** | 月度目標、每週追蹤表、每月總結模板 |
| 6 | 📂 **內容庫存隊列** | inline database（27 列），即現有 DB 原地改造 |

### 子頁 2 的關鍵規則：IG→Threads 變形

TeaWiki 的做法**不是一稿兩投**，是單向變形：

```
IG 寫完 → 刪走列點同精美詞彙 → 加大白話 → 變問句或吐槽 → 配手機隨手拍 → 發 Threads
```

實際資料佐證：IG caption 有 emoji 分段與完整資訊架構；Threads body 是散文段落、問句結尾、字數明顯更短。

### 子頁 1 的節奏（使用者已確認：照抄 TeaWiki）

- IG 貼文：每日 1 帖
- IG Stories：每日 3 檔（早 8:00 / 午 12:30 / 晚 8:00）
- Threads：每日 2 則
- 27 列內容，兩平台合計約 27 則主題

---

## 3. 27 列主題分配

### M1（10 列）破冰探索 · 認識你的結婚證書套
目標：建立產品認知，把「結婚證書」變成值得被設計的物件。

| # | Idea | 格式原型 | 主題標籤 | 對應真實文章 |
|---|---|---|---|---|
| 01 | MyO 品牌故事 | 品牌型 | 品牌故事 | `index.html` |
| 02 | 四款產品一覽 | 對比型 | 經典款／設計師款 | `結婚證書套推薦.html` |
| 03 | 亞麻布 vs 磨砂珠光 | 對比型 | 亞麻布／磨砂珠光 | `證書套材質比較.html` |
| 04 | 經典款 vs 設計師款 | 對比型 | 經典款／設計師款 | `燙印證書套價錢比較.html` |
| 05 | 為何是 A4 尺寸 | 知識型 | 尺寸規格 | `結婚證書尺寸規格.html` |
| 06 | 燙印工藝怎麼做 | 教學型 | 燙印工藝 | `客製化證書套設計.html` |
| 07 | 註冊結婚流程 | 知識型 | 註冊流程 | `註冊結婚流程.html` |
| 08 | 註冊結婚費用 | 知識型 | 註冊流程 | `註冊結婚費用.html` |
| 09 | 訂製流程與 7–14 工作天 | 教學型 | 訂製流程 | `證書套定制指南.html` |
| 10 | 證書套保養指南 | 教學型 | 保養知識 | `證書套保養指南.html` |

### M2（9 列）工藝深度 · 用手感受差異
目標：建立專業權威，把材質差異講成可感知的價值。

| # | Idea | 格式原型 | 主題標籤 | 對應真實文章 |
|---|---|---|---|---|
| 11 | 燙金 vs 燙銀 | 對比型 | 燙印工藝 | `燙印證書套價錢.html` |
| 12 | 中英文名字怎麼排 | 教學型 | 訂製流程 | `客製化證書套設計靈感.html` |
| 13 | 結婚證書的由來 | 知識型 | 品牌故事 | `結婚證書歷史.html` |
| 14 | 絲絨 vs 亞麻布 | 對比型 | 亞麻布 | `絲絨vs亞麻布證書套.html` |
| 15 | 婚後證書放邊度 | 互動型 | 保養知識 | `婚禮證書套保養.html` |
| 16 | 保養五個貼士 | 教學型 | 保養知識 | `證書套保養貼士.html` |
| 17 | 幾時送證書套最啱 | 文化型 | 送禮場景 | `證書套送禮指南.html` |
| 18 | 刻邊啲字句靈感 | 互動型 | 訂製流程 | `客製化證書套設計靈感.html` |
| 19 | 海外新人點買 | 知識型 | 海外新人 | `海外結婚指南.html` |

### M3（8 列）香港婚禮文化 · 在地連結
目標：把產品接進香港婚禮現實，建立文化認同。

| # | Idea | 格式原型 | 主題標籤 | 對應真實文章 |
|---|---|---|---|---|
| 20 | 過大禮點解要帶證書套 | 文化型 | 中式習俗 | `過大禮清單.html` |
| 21 | 敬茶儀式 | 文化型 | 中式習俗 | `敬茶儀式流程.html` |
| 22 | 上頭吉日 | 文化型 | 中式習俗 | `上頭儀式介紹.html` |
| 23 | 回門習俗 | 文化型 | 中式習俗 | `回門習俗介紹.html` |
| 24 | 中西婚禮習俗比較 | 對比型 | 中式習俗 | `中西婚禮習俗比較.html` |
| 25 | 結婚註冊法律須知 | 知識型 | 註冊流程 | `結婚註冊指南.html` |
| 26 | 客人實錄 | 品牌型 | 客戶實錄 | `婚禮證書套保養.html` |
| 27 | 品牌回顧與下季預告 | 品牌型 | 品牌故事 | `index.html` |

**格式原型分佈**：對比型 9、教學型 6、知識型 6、文化型 4、互動型 2、品牌型 3 ≈ 均衡。

### KPI（對齊 TeaWiki 結構，但換掉不存在的工具指標）

TeaWiki 有「找茶測驗點擊」；MyO 沒有測驗工具，改用 WhatsApp 點擊（PostHog 已有 `click_whatsapp` 事件）。

| 指標 | M1 | M2 | M3（累計） |
|---|---|---|---|
| IG Followers 增長 | +10–15% | +20–25% | +40% |
| Threads Followers 增長 | +15–20% | +35% | +50% |
| IG Reels 平均觸及 | 基準線 | ×1.5 | ×2 |
| Threads 互動率 | >1% | >1.8% | >2.5% |
| Stories 回覆數 | 起步 | ×2 | ×3 |
| WhatsApp 點擊 | 基準線 | ×1.5 | ×2 |
| 品牌詞搜尋量（MyO／結婚證書套） | 起步 | 成長 | 品牌資產 |

---

## 4. Schema 變更規格

### 4.1 `content_dimensions` multi_select 選項置換

**現有（茶，要移除）**：普洱茶、烏龍茶、白茶、綠茶、茶具、健康養生、節慶禮盒、季節限定、基礎、文化在地

**新（MyO，10 個）**：

| 選項 | 用途 |
|---|---|
| 經典款 | HK$388 系列 |
| 設計師款 | HK$588 系列 |
| 亞麻布 | 米色材質 |
| 磨砂珠光 | 藍色材質 |
| 燙印工藝 | 熱轉印／燙金燙銀 |
| 註冊流程 | 婚姻登記署相關 |
| 中式習俗 | 過大禮、敬茶、上頭、回門 |
| 保養知識 | 證書套保養 |
| 送禮場景 | 送禮建議 |
| 品牌故事 | 品牌與客戶實錄 |

### 4.2 保持不變的欄位

`Status`（Human Idea → AI Drafted → AI Image Ready → Human Commenting → Human Approved → Published，**這是 MyO 自己的 AI 協作流程，不改成 TeaWiki 的 ⏳✏️✅🚀**）、`Idea`、`id`、`publish_date`、`social_pillar`（6 個格式原型沿用）、`ig_hook`、`ig_caption`、`threads_hook`、`threads_body`、`image_prompt`、`cta_url`、`image_url`、`image_file`、`other_comment`

### 4.3 `cta_url` 格式

中文檔名需 URL 編碼，格式：

```
https://myo-makeyourown.pages.dev/blog/%E8%AD%89%E6%9B%B8%E8%A8%BC%E6%9B%B8%E5%A5%97.html
```

寫入前逐列驗證檔名存在於 `blog/`。

---

## 5. 執行順序（7 步）

| 步 | 動作 | 可逆 |
|---|---|---|
| 1 | **備份** 48 列茶內容 + schema → `docs/social/notion-backup-2026-09-30.json` | — |
| 2 | 建 6 個子頁（空殼 → 填內容） | 可刪 |
| 3 | 更新 `content_dimensions` 選項 | 可改回 |
| 4 | archive 48 列茶內容（移入 Notion 垃圾桶） | **可從垃圾桶恢復** |
| 5 | 寫入 27 列 MyO 內容 | 可逐列刪 |
| 6 | 連回子頁索引與 inline database | 可解 |
| 7 | 全量驗證 | — |

**步驟 4 放在步驟 5 之後才安全** — 實際執行順序為 1→2→3→4→5→6→7，每步完成即驗證，任一步失敗即停。

---

## 6. 回滾方案

| 情況 | 回滾動作 |
|---|---|
| 27 列內容有問題 | 逐列 archive，內容已在本地 JSON 備份 |
| schema 選項換錯 | `update-a-data-source` 改回原本 10 個茶選項 |
| 48 列茶內容需找回 | Notion 垃圾桶 → Restore all |
| 子頁內容有問題 | 刪除子頁（不影響 DB） |
| 全域要撤銷 | 依備份 JSON 重建 |

備份檔必須在**步驟 1** 生成並確認可讀，才允許進入步驟 4。

---

## 7. 風險

| 風險 | 影響 | 緩解 |
|---|---|---|
| repo 內 0 支影片，Reels 素材不存在 | M1 的 Reels 無法執行 | 列 01–09 設計為 Carousel／Single 為主，Reels 從列 11 開始並同步建立拍攝流程 |
| 中文檔名 URL 編碼出錯 | cta_url 死鏈 | 寫入前逐列 `curl -I` 驗證 HTTP 200 |
| 27 列 × 8 欄位內容量大 | 品質不均 | 分批寫入，每批 9 列後驗證 |
| 玫瑰粉 + 金撞色偏甜 | 視覺偏離「設計師級」定位 | BPP 鎖定 `low saturation warm tones` + `deep cocoa brown` 主文字，粉色只作強調 |
| Stories 每日 3 檔 + Threads 每日 2 則 | 產能過載 | 已與使用者確認照抄節奏；若 M2 週補追不上，降為 Stories 2 檔 |
| Notion API 速率限制 | 寫入中斷 | 逐列寫入 + 失敗重試 + 完成後全量驗證 |

---

## 8. 待確認

- [ ] 子頁 6「內容庫存隊列」是否直接用現有 inline DB（原地改造），或另建新 DB 保留茶內容？
- [ ] 27 列的 `publish_date` 是否要按 M1/M2/M3 實際排日期（2026-10 / 11 / 12）？
