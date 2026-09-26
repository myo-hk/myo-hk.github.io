# 教訓：PostHog 延遲載入的三個靜默陷阱與簡報空白頁故障

> **日期**：2026-09-26
> **關聯 PR**：posthog-integration（Tasks 1–6）
> **狀態**：已解決

---

### 問題

#### 1. 延遲載入後 `$pageview` 時間戳失真

PostHog loader 在首次互動或 3 秒後才載入 SDK，`$pageview` 的時間戳是「互動時刻」而非「頁面載入時刻」，1.5 秒內跳出的訪客完全不會被記錄。

#### 2. `worker-src` 缺失導致 session replay 靜默失效

缺少 `worker-src 'self' blob: data:` 時，session replay 在 console 不報錯、不拋異常，完全靜默失效。

#### 3. `<meta>` CSP 中的 `frame-ancestors` 無效

Spec 忽略 meta 形式的 `frame-ancestors` directive，看起來像修好了但實際上沒有作用。

#### 4. 簡報全數空白（生產事故）

所有 40 個簡報在 GitHub Pages 上渲染空白頁。根本原因：

- 每個專案的 `vite.config.ts` 以 `index.html` 為入口
- 建構腳本 `vite build && cp dist/index.html index.html` 把構建產物回寫到入口檔案
- 倉庫中儲存的 `index.html` 是上一次成功建構後的產物，但下一次建構時輸入已被替換
- 由於 `dist/` 受 `.gitignore` 保護，建構產物僅透過 `git add -f` 進入版本庫
- 一旦 `dist/` 被清除（CI 重跑、fresh clone），建構會失敗但舊的 `dist/` 殘留會掩蓋錯誤，讓失敗看起來像成功
- 結果：40 個簡報的 `index.html` 全部引用了不存在的 JS bundle，生產環境全數空白

### 教訓

PostHog 的 lazy-load 把「載入成本」換成了「時間戳失真」與「更多 CSP 依賴」。延遲載入時必須 `capture_pageview: false` + 手動補發 `$pageview`，且 `worker-src` 是 session replay 的硬性前提，不能靠錯誤訊號發現。

簡報建構的最大陷阱是**輸入與輸出的路徑衝突**：Vite 的入口 `index.html` 同時是建構目標。一旦建構腳本把產物寫回入口，倉庫中的來源就被破壞了，後續每次建構都會失敗——只是殘留的 `dist/` 讓失敗看不出來。

### 解法

**PostHog 延遲載入**：`scripts/posthog_config.py` 集中管理設定；三個腳本（靜態頁、CSP、簡報）各自有 pytest 覆蓋 idempotency 與 directive 存在性。

**簡報建構修復**：新增 `index.src.html` 作為獨立的 Vite 入口，建構輸出到 `dist/index.html` 後再覆寫服務用的 `index.html`。此設計確保倉庫中的 `index.src.html` 永遠是可建構的來源。

```bash
# 正確的建構流程（現已由 _scaffold.sh 模板固化）
cd presentations/XX-slug/presentation
npx vite build --base ""
cp dist/index.html index.html
git add -f index.html assets/   # 強制加入，因為 dist/ 在 .gitignore 中
```

### 預防

**新增任何延遲載入的第三方 SDK 時，先確認三件事**：
1. 首屏事件時間戳是否失真
2. 是否依賴 CSP 中不存在的 directive
3. 事件是否在 SDK 就緒前觸發，需要 queue

**新增簡報時的操作規範**：
- 建構後必須 `git add -f` 將新 bundle hash 的 `index.html` 和 `assets/` 強制加入版本庫
- 未 force-add 就 push 會立刻恢復空白頁故障
- 刪除 `dist/` 目錄後必須重新建構，不能依賴舊的構建產物
