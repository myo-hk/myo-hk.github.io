# 設計：品牌更名 My O! → MyO

> **日期**：2026-09-29
> **狀態**：待實作
> **影響範圍**：453 個檔案 / 6,842 處
> **決策來源**：與使用者於 brainstorming 階段確認的五項選擇

---

## 1. 目標與範圍

### 1.1 目標

將全站品牌字串由 `My O!`（含空格與驚嘆號）統一更名為 `MyO`，同時讓視覺 wordmark 保留驚嘆號變成 `MyO!`，以對應不變的 logo 圖檔。

### 1.2 已確認決策

| 面向 | 決定 | 理由 |
|---|---|---|
| 正文品牌字串 | `MyO`（去空格、去驚嘆號） | 與 PostHog 專案名 `MyO Cert Holder` 一致 |
| 視覺 wordmark / logo 上下文 | `MyO!`（保留驚嘆號） | logo 圖檔維持 `My O!` 不變，文字需與視覺一致 |
| Logo 圖檔 | 不動 | `image/01_company_logo.png` 內烙印「My O!」+「make your own」，純文字取代無法處理 |
| 檔名 / 目錄名 / 網域 / URL | 全不動 | 避免 SEO 排名損失與外部連結斷裂 |
| SEO 舊名 | 不保留、不宣告、不加 `alternateName` | 使用者明確選擇完全取代 |
| 執行方式 | 單一 Python 批次腳本 + `--test` 乾跑 | 符合 AGENTS.md「禁止跳過 dry-run」規範 |

### 1.3 不在範圍

- Logo 圖檔重新設計或生成
- 檔名、網域、URL slug 變更
- `Myo.tsx` / `Myo.css` / `05-myo/` 檔名與匯入路徑
- PostHog 專案名稱（永久 ID，改名需重建專案）

---

## 2. 現況盤點

### 2.1 總量

| 指標 | 數值 |
|---|---|
| `My O!` 總出現次數（排除清單外） | 6,842 |
| 受影響檔案數 | 451（含 `My O!`）／453（含僅有 `MYO` 的 2 個 TSX） |
| `My O` 後接字元為 `!` 的比例 | 6,842 / 6,842（100%） |

`My O!` 是唯一實際形態，通配取代不會誤傷 `My Optic` 之類的英文詞。

**數字來源**：以唯讀 dry-run 演練實測（完整套用第 5 節排除清單後的 `os.walk` 掃描）。初次盤點所得 6,904 處係在加入三項額外排除（`docs/PageSpeed Insights.html`、`docs/architecture-diagram.html`、`scripts/blog_index.json`）之前計算，數字已過期。

### 2.2 依目錄分布

| 分類 | 處數 | 檔數 |
|---|---|---|
| `blog/` 文章 | 6,716 | 421 |
| 根目錄（index/v2/privacy/terms/faq/poster×2/heic-converter 等） | 106 | 18 |
| `presentations/` 原始碼與 md | 9 | 3 |
| `scripts/` 生成器 | 6 | 4 |
| `tests/` | 4 | 4 |
| `docs/ai-visibility-monitoring.md` | 1 | 1 |
| **合計（文字取代範圍）** | **6,842** | **451** |
| 另加：僅含 `MYO` 的 TSX（Phase 3 處理） | 2 | 2 |
| **實際會被修改** | **6,842** | **453** |
| *（排除）* `docs/superpowers/plans` + `specs` | *90* | *15* |
| *（排除）* `docs/PageSpeed Insights.html` | *16* | *1* |
| *（排除）* `docs/architecture-diagram.html` | *2* | *1* |
| *（排除）* `scripts/blog_index.json` | *44* | *1* |

### 2.3 HTML 內部結構

`blog/` 421 篇文章的 6,716 處中，約 3,400 處落在重複樣板（footer 品牌列、logo `<img alt>`、sticky bar、apple-web-app-title），約 3,300 處為各頁獨有（`<title>`、meta description、JSON-LD `name`、內文「My O! 貼士：」「My O! 版權所有」等）。

---

## 3. 取代規則

### 3.1 三階段有序取代

腳本必須按 Phase 1 → 2 → 3 順序執行。Phase 1 先把視覺上下文保護下來（轉為 `MyO!`，已不含 `My O` 字面），Phase 2 的通配便不會誤傷。

#### Phase 1 — 視覺 wordmark / logo 上下文 → `MyO!`（2,147 處）

以錨定樣式精確匹配，不使用通配：

| # | 錨定樣式 | 數量 |
|---|---|---|
| 1 | `alt="My O! Logo"` 與 `alt="My O! logo"` | 857 |
| 2 | `og:image:alt" content="My O!` | 3 |
| 3 | `>My O!</span>` | 853 |
| 4 | `>My O!</div>` | 2 |
| 5 | `"short_name": "My O!"` | 1 |
| 6 | `apple-mobile-web-app-title" content="My O!"` | 431 |

Phase 1 的 6 個錨點已驗證無誤判風險：

- 857 處 `alt` 屬性的完整值只有兩種：`alt="My O! Logo"`（431）與 `alt="My O! logo"`（426）
- 853 處 `>My O!</span>` 只落在 5 種版面：footer 品牌連結（426）、header 品牌連結（422 + 2）、首頁 h1 rose-500 span（2）、sticky bar brand-name span（1）
- 錨點 5（`manifest.json` `short_name`）與錨點 6（`apple-mobile-web-app-title`）皆渲染於 logo icon 之下，屬視覺識別的一部分，故保留驚嘆號以對應未變的 logo 圖檔

#### Phase 2 — 其餘全部 → `MyO`（4,695 處）

Phase 1 執行後，字面 `My O!` 的剩餘部分全部是正文語境，直接取代為 `MyO`。

計數對帳：Phase 1 的 2,147 + Phase 2 的 4,695 = 6,842，等於第 2.1 節盤點總數。此守恆式已於唯讀 dry-run 中實測通過，且演練後殘留 `My O!` / `MYO` 為 0 檔。

覆蓋：`My O! 專屬結婚證書套` → `MyO 專屬結婚證書套`、`My O! 貼士：` → `MyO 貼士：`、`My O! 版權所有。` → `MyO 版權所有。`、`<title>`、meta description、JSON-LD `Organization.name`、內文敘述。

#### Phase 3 — 大小寫變體正規化（2 處）

| 現況 | 產出 | 位置 |
|---|---|---|
| `MYO證書套` | `MyO 證書套` | `presentations/08-certificate-size-specs/presentation/src/chapters/01-coldopen/Coldopen.tsx:4`（章節分類選單） |
| `MYO證書套` | `MyO 證書套` | `presentations/08-certificate-size-specs/presentation/src/registry/chapters.ts:21`（章節標題） |

此兩處為 `MYO` 全大寫，獨立於 `My O!` 計數之外，故不影響第 2.1 節的 6,842 守恆式。

`presentations/08-.../src/chapters/05-myo/Myo.tsx` 內的 `MyO 證書套` 已是目標寫法，不動。排除 `Myo` 識別字（`Myo.tsx` 的元件函式名、`05-myo` 的目錄與匯入 id），這些是程式碼識別字而非品牌字串。

`presentations/08-.../presentation/dist/assets/index.src-Bb26cSCl.js`（minified）另含 `MYO`，屬建置產物，須以 rebuild 而非文字取代處理。

### 3.2 不改寫的既有 MyO 變體

| 位置 | 值 | 理由 |
|---|---|---|
| `README.md`、`privacy.html` | `MyO Cert Holder` | PostHog 專案名稱，永久 ID |
| `manifest.json` `"name"` | `MyO 專屬結婚證書套` | Phase 2 產出，目標寫法 |

---

## 4. 檔案分層

### Layer A — 使用者可見內容（約 6,820 處，佔總量 99%）

- `blog/*.html`（421 篇，6,716 處）
- 根目錄 8 個使用者可見頁面：`index.html`、`v2.html`、`privacy.html`、`terms.html`、`faq.html`、`poster.html`、`poster-en.html`、`heic-converter.html`（91 處）
- `manifest.json`、`llms.txt`、`package.json`（description）（4 處）
- `presentations/index.html`、`presentations/02-wedding-checklist-timeline/article.md`、`script.md`（9 處）

### Layer B — 生成器（必須同步，否則未來重跑會還原舊名）

| 檔案 | 內容量 | 風險 |
|---|---|---|
| `scripts/optimize_blog_head.py` | `FOOTER_LOGO` 正則硬寫 `alt="My O! Logo"` | **最高**：HTML 改完正則靜默失效，無錯誤訊息 |
| `scripts/add_org_schema_to_articles.py` | `Organization.name` 模板 | 重跑會把 JSON-LD 寫回 `My O!` |
| `scripts/add_pwa_tags.py` | `apple-mobile-web-app-title` 模板 | 同上 |
| `add_sticky_bar.py` | footer 樣板 `alt` 與 `<span>` | 同上 |
| `scripts/optimize_images.py`、`fix_json_ld_and_table.py`、`fix_medium_issues.py` | docstring 內品牌字串 | 低（僅註解） |

### Layer C — 產物（重新生成，非文字取代）

| 檔案 | 處數 | 處理方式 |
|---|---|---|
| `scripts/blog_index.json` | 44 | **重新生成**：先改 HTML，再跑 `python3 scripts/parse_blog.py`。直接 sed 會在下次重跑時被還原 |
| `sw.js` `CACHE_NAME` | 1 | 升版 `myo-cache-v2` → `myo-cache-v3`，使回訪用戶取得新 HTML |
| `presentations/*/presentation/dist/` | 0 | 已驗證不含 `My O!`；其中 `MYO` 僅存在於 08 的 minified js，需 rebuild 而非 sed |

### Layer D — 測試斷言

| 檔案 | 現況 | 改為 |
|---|---|---|
| `tests/homepage.spec.ts` | `toHaveTitle(/My O/)` | `/MyO/`（原正則要求字面空格，更名後會**明確失敗**，屬 fail-fast 的保護） |
| `tests/mobile.spec.ts` | `test.describe('My O! 手機版…')` | `MyO 手機版…` |
| `tests/poster-en.spec.ts` | 斷言 `"My O! Wedding Certificate Holder — Printable A5 Flyer"` | `MyO Wedding Certificate Holder — Printable A5 Flyer` |
| `tests/lighthouse-check.sh` | 註解 | 更新 |

### Layer E — 文件

`README.md`、`AGENTS.md`、`pricing.md`、`docs/ai-visibility-monitoring.md`

---

## 5. 排除清單

腳本以目錄名與副檔名雙重過濾，以下路徑不進入取代範圍：

| 路徑 | 理由 |
|---|---|
| `image/**` | 二進位檔；logo 內烙「My O!」為既定決策 |
| `scripts/blog_index.json` | `parse_blog.py` 產物，於步驟 4 重新生成（第 4 節 Layer C） |
| `docs/superpowers/plans/`、`docs/superpowers/specs/` | 歷史決策紀錄（90 處），記錄當時狀態不應改寫 |
| `docs/PageSpeed Insights.html` | 工具產出報告快照 |
| `docs/architecture-diagram.html` | 圖解產物 |
| `presentations/*/presentation/dist/` | minified 建置產物，需 rebuild |
| `dist/` | 建置產物 |
| `.worktrees/`、`.omo/`、`.gstack/`、`.playwright-mcp/` | 工具狀態與快照 |
| `Users/baba/Documents/Github/myo-hk/` | 意外巢狀 repo 副本 |
| `node_modules/`、`test-results/`、`playwright-report/` | 相依與測試產物 |

---

## 6. 執行順序

順序具決定性，錯序會導致產物與來源不一致：

1. 撰寫 `scripts/rename_brand.py`（支援 `--test` 乾跑 / `--write` 寫入）
2. `python3 scripts/rename_brand.py --test` — 確認乾跑統計符合本 spec 數字
3. `python3 scripts/rename_brand.py --write`
4. `python3 scripts/parse_blog.py` — 重新生成 `scripts/blog_index.json`
5. `sw.js` `CACHE_NAME` 升版為 `myo-cache-v3`
6. 執行五道驗證閘門（見第 7 節）

---

## 7. 驗證閘門

五道全過才算完成。

### 閘門 1 — 舊名歸零

排除清單外，`My O!` 出現次數為 0。`scripts/blog_index.json` 因採重新生成（第 4 節 Layer C），於步驟 4 之後才會歸零，故閘門在步驟 4 之後執行。

### 閘門 2 — 計數守恆

腳本在 `--test` 與 `--write` 皆輸出以下數值，供人工比對。期望值已於唯讀 dry-run 實測：

| 數值 | 期望 | 說明 |
|---|---|---|
| `scanned` 檔案內 `My O!` 初始總數 | **6,842** | 基準值 |
| Phase 1 命中數 | **2,147** | 轉為 `MyO!` |
| Phase 2 命中數 | **4,695** | 轉為 `MyO` |
| Phase 1 + Phase 2 | **== 6,842** | **守恆式**：每個 `My O!` 必須被 Phase 1 或 Phase 2 恰好處理一次 |
| Phase 3 命中數 | **2** | `MYO` 大小寫變體，獨立於 `My O!` 計數之外 |
| 會被寫入的檔案數 | **453** | 451（含 `My O!`）+ 2（僅含 `MYO` 的 TSX） |
| `scripts/blog_index.json` 命中數 | **0** | 該檔被排除於文字取代之外，改以重新生成處理 |
| 處理後殘留 `My O!` / `MYO` | **0** | 漏網偵測 |

若 Phase 1 + Phase 2 不等於初始總數，代表有 `My O!` 未被任一階段處理（漏網），必須回頭補錨點。

### 閘門 3 — 自動化測試

`npm test`（Playwright，Mobile / Desktop / Tablet 三裝置）全綠。測試斷言須已依 Layer D 更新。

`tests/homepage.spec.ts` 原斷言 `toHaveTitle(/My O/)` 要求字面「My O」含空格，更名後的 `MyO` 無空格，故該斷言會**明確失敗**（fail-fast）而非靜默通過。此行為正確——它保證斷言不會在未更新情況下假性通過。

### 閘門 4 — 生成器常數與 HTML 一致

驗證 `scripts/optimize_blog_head.py` 的 `FOOTER_LOGO` 正則與 `FOOTER_LOGO_REPLACEMENT` 中的 `alt` 字串，須與 `blog/*.html` 內的實際值一致（皆為 `alt="MyO! Logo"`）。

**不可使用 `--dry-run` 的「Would modify N files」作為判斷依據。** 實測結果：`FOOTER_LOGO` 對現有 421 篇 HTML 匹配數為 **0**，因為 `optimize_blog_head.py` 的最佳化早已套用完畢，`<img src="..." class="logo">` 的原始待優化型態已不存在。此判斷條件無論正則是否正確都會回報 0，屬誤判。

正確的判斷方式為直接字串比對：

```bash
python3 -c "
import re,sys; sys.path.insert(0,'scripts')
import optimize_blog_head as m
from pathlib import Path
pat = re.search(r'alt=\"([^\"]+)\"', m.FOOTER_LOGO_REPLACEMENT).group(1)
hits = sum(len(re.findall(re.escape(pat), f.read_text(encoding='utf-8')))
           for f in Path('blog').glob('*.html'))
print(f'常數: {pat} / HTML 命中: {hits}')
sys.exit(0 if hits == 421 else 1)
"
```

期望輸出 `常數: MyO! Logo / HTML 命中: 421`，exit code 0。

### 閘門 5 — 手動抽樣

抽查 `index.html`、`poster.html`、`poster-en.html`、`privacy.html` 及任一篇 `blog/*.html`，確認：

- `<title>` 顯示 `MyO`
- JSON-LD `Organization.name` 顯示 `MyO`
- logo `<img alt>` 顯示 `MyO!`
- footer / sticky bar wordmark 顯示 `MyO!`
- `manifest.json` 的 `short_name` 與 `apple-mobile-web-app-title` 顯示 `MyO!`（此二者渲染於 logo icon 下方，與視覺一致）
- 內文「MyO 貼士：」無驚嘆號

---

## 8. 已知後果

以下為已確認並接受的取捨，非缺陷：

1. **Logo 圖與文字不完全一致**：logo 圖檔仍為「My O!」，頁面 wordmark 為「MyO!」。圖檔重製不在本次範圍。
2. **SEO 排名風險**：`My O!` 舊搜尋詞可能失去部分流量。使用者已明確選擇不保留舊名，此為已知取捨。
3. **PostHog 專案名不一致**：專案名維持 `MyO Cert Holder`（永久 ID），與頁面顯示的 `MyO` 字面不同但不衝突。
4. **正文與視覺兩種寫法並存**：`MyO`（正文）與 `MyO!`（wordmark）並存，為使用者明確選擇。錨點清單（第 3.1 節）定義了兩者邊界，未來新增頁面須比照辦理。
