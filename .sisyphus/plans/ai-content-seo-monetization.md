# AI Content SEO 網站開發與變現計畫

## TL;DR

> **Quick Summary**: 基於現有純 HTML 網站，用 AI vibe coding 擴展為 SEO 友好的內容網站。零學習曲線，用 AI 直接生成 HTML 頁面，部署在 GitHub Pages。
> 
> **Deliverables**: 
> - 內容可信度分級框架與驗證 SOP
> - HTML 靜態站 SEO 優化方案（基於現有 index.html 擴展）
> - AI 內容生成流水線（5步驗證法）
> - 變現模式設計（產品銷售 + 聯盟行銷 + 廣告）
> - 30 天 MVP 執行計畫
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 4 waves
> **Critical Path**: 框架設計 → 內容生成 → 上線優化 → 變現
> **技術約束**: 純 HTML + AI vibe coding，零學習曲線

---

## Context

### Original Request
用戶希望成為「AI 內容 SEO 網站開發與變現顧問」，專注於用 AI 生成內容 + 自動化 SEO，快速建出能搜尋排名的內容網站，並把流量變現成廣告、聯盟、訂閱或服務收入。

### Interview Summary
**Key Discussions**:
- 用戶現有網站 `myo-hk.github.io` 是靜態 HTML，銷售結婚證書套
- 用戶強調 AI 內容必須驗證真實性，特別是官方規定（如結婚證書尺寸）
- 用戶希望有多源驗證（Exa, Google, Perplexity 等），但環境限制無法直接控制瀏覽器
- 我們建立了可信度分級框架（Tier 0-4）和三角交叉驗證法
- 通過實際搜尋發現「香港結婚證書是 A4 尺寸」並非法律規定，而是實務慣例
- **技術約束**: 用戶只懂 HTML，不會 WordPress/Next.js，只用 OpenWork AI 做 vibe coding
- **核心需求**: SEO friendly + 方便變現，零學習曲線

**Research Findings**:
- 「香港結婚證書是 A4 尺寸」並非法律規定，而是實務慣例
- 競爭對手分析：Boxberries, BE ONE LETTER, Pinkoi 賣家等
- 用戶自己的社交媒體內容（Threads, IG）有潛在誤導風險
- 多源驗證可用 Exa + Web Fetch 替代瀏覽器控制
- **技術建議**: 保持純 HTML + 新增文章頁面 + sitemap.xml + schema.org 結構化數據，完全足夠 SEO 排名

### Metis Review
**Identified Gaps** (addressed):
- 內容驗證流程缺乏具體的工具整合方案 → 已設計 Exa + Web Fetch 的替代方案
- 變現模式缺乏具體的聯盟產品清單 → 將在計畫中補充
- 網站技術升級路徑不明確 → 已提供 WordPress/Next.js 的選項分析

---

## Work Objectives

### Core Objective
建立一個以 AI 驅動、多源驗證的香港婚慶內容 SEO 網站，在 3 個月內實現穩定流量與多元收入。

### Concrete Deliverables
- 內容可信度分級框架文檔
- HTML 靜態站 SEO 優化方案
- AI 內容生成 SOP（5步驗證法）
- 變現模式設計與聯盟產品清單
- 30 天 MVP 執行計畫

### Definition of Done
- [ ] 框架文檔完成並通過內部審核
- [ ] 網站架構圖完成並確認技術選型
- [ ] SOP 文檔完成並測試至少 3 篇文章
- [ ] 變現模式設計完成並簽約至少 2 個聯盟計畫
- [ ] MVP 上線並有至少 5 篇內容發布

### Must Have
- 所有法律/程序聲明必須有 Tier 0 或 Tier 1 來源支持
- 每篇文章必須有免責聲明和來源註釋
- 內容生成流程必須包含人工驗證步驟
- 保持純 HTML 技術棧，零學習曲線

### Must NOT Have (Guardrails)
- 不得將個人經驗或社交媒體內容當作事實陳述
- 不得在未經交叉驗證的情況下發布法律/程序相關內容
- 不得使用絕對性描述（如「最好」「最平」） without evidence
- 不得引入需要學習的框架（WordPress/Next.js/React）

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.
> Acceptance criteria requiring "user manually tests/confirms" are FORBIDDEN.

### Test Decision
- **Infrastructure exists**: NO
- **Automated tests**: None (focus on content verification)
- **Framework**: Content verification checklist (not code tests)
- **Agent-Executed QA**: ALWAYS (mandatory for all tasks regardless of test choice)

### QA Policy
Every content piece must pass the 5-step verification process before publishing.
Evidence saved to `.sisyphus/evidence/content-{N}-verification.md`.

- **Content Verification**: Use Exa + Web Fetch to cross-reference sources
- **SEO Verification**: Use Exa to check keyword rankings and competitor analysis
- **Fact Verification**: Use Tier 0-1 sources to validate all claims

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — foundation + scaffolding):
├── Task 1: 建立內容可信度分級框架 [quick]
├── Task 2: 設計 Pillar + Cluster 網站架構 [unspecified-high]
└── Task 3: HTML 靜態站 SEO 優化方案 [quick]

Wave 2 (After Wave 1 — content pipeline):
├── Task 4: 建立 AI 內容生成 SOP [deep]
├── Task 5: 關鍵字研究與內容日曆 [unspecified-high]
└── Task 6: 變現模式設計 [unspecified-high]

Wave 3 (After Wave 2 — execution):
├── Task 7: 生成首批 5 篇文章 [deep]
├── Task 8: 網站升級與內容發布 [visual-engineering]
└── Task 9: SEO 優化與數據追蹤設置 [quick]

Wave 4 (After Wave 3 — optimization):
├── Task 10: 數據分析與內容優化 [deep]
├── Task 11: 聯盟計畫整合 [unspecified-high]
└── Task 12: 廣告收入設置 [quick]

Wave FINAL (After ALL tasks — 4 parallel reviews, then user okay):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay
```

### Dependency Matrix

- **1-3**: — — 4-6
- **4-6**: 1-3 — 7-9
- **7-9**: 4-6 — 10-12
- **10-12**: 7-9 — F1-F4

### Agent Dispatch Summary

- **1**: **3** — T1 → `quick`, T2 → `unspecified-high`, T3 → `quick`
- **2**: **3** — T4 → `deep`, T5 → `unspecified-high`, T6 → `unspecified-high`
- **3**: **3** — T7 → `deep`, T8 → `visual-engineering`, T9 → `quick`
- **4**: **3** — T10 → `deep`, T11 → `unspecified-high`, T12 → `quick`
- **FINAL**: **4** — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

> Implementation + Test = ONE Task. Never separate.
> EVERY task MUST have: Recommended Agent Profile + Parallelization info + QA Scenarios.
> **A task WITHOUT QA Scenarios is INCOMPLETE. No exceptions.**

- [ ] 1. 建立內容可信度分級框架

  **What to do**:
  - 創建 Tier 0-4 可信度分級文檔
  - 定義每個 tier 的來源類型、可信度評分、驗證要求
  - 提供實際案例（如結婚證書尺寸）說明如何應用框架
  - 設計三角交叉驗證流程

  **Must NOT do**:
  - 不得將任何單一來源視為絕對真理
  - 不得忽略商業利益相關的潛在偏見

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 文檔任務，需要清晰結構和案例，無需複雜實現
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - `seo`: 不需要用於框架設計

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Tasks 4, 5, 6
  - **Blocked By**: None (can start immediately)

  **References**:
  - 無（新文檔）

  **Acceptance Criteria**:
  - [ ] 文檔創建完成：`.sisyphus/plans/content-verification-framework.md`
  - [ ] 文檔包含 Tier 0-4 定義、案例、驗證流程

  **QA Scenarios**:
  ```
  Scenario: 驗證框架完整性
    Tool: Bash (grep)
    Preconditions: 文檔已創建
    Steps:
      1. grep -c "Tier [0-4]" .sisyphus/plans/content-verification-framework.md
      2. 確認輸出為 5（每個 tier 都有定義）
    Expected Result: 輸出為 5
    Failure Indicators: 輸出小於 5
    Evidence: .sisyphus/evidence/task-1-framework-completeness.txt
  ```

  **Commit**: YES (groups with 1)
  - Message: `feat(content): add content verification framework`
  - Files: `.sisyphus/plans/content-verification-framework.md`

---

- [ ] 2. 設計 Pillar + Cluster 網站架構

  **What to do**:
  - 設計 Pillar Page（核心頁）主題與結構
  - 設計 8-10 篇 Cluster Pages 主題
  - 規劃內部連結策略
  - 創建網站架構圖

  **Must NOT do**:
  - 不得設計與婚慶無關的內容
  - 不得忽略內部連結的重要性

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要內容架構和 SEO 的戰略思考
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Tasks 4, 5, 7
  - **Blocked By**: None (can start immediately)

  **References**:
  - `index.html` - 現有網站結構，作為基礎模板

  **Acceptance Criteria**:
  - [ ] 網站架構圖完成
  - [ ] 包含 Pillar Page 和至少 8 篇 Cluster Pages

  **QA Scenarios**:
  ```
  Scenario: 驗證架構完整性
    Tool: Bash (grep)
    Preconditions: 架構圖已創建
    Steps:
      1. grep -c "Cluster" 架構圖文件
      2. 確認輸出大於等於 8
    Expected Result: 輸出大於等於 8
    Evidence: .sisyphus/evidence/task-2-architecture-completeness.txt
  ```

  **Commit**: YES (groups with 2)
  - Message: `feat(architecture): add pillar-cluster site architecture`

---

- [ ] 3. HTML 靜態站 SEO 優化方案

  **What to do**:
  - 基於現有 `index.html` 設計 SEO 優化模板
  - 添加 schema.org 結構化數據（JSON-LD）
  - 創建 sitemap.xml 生成方案
  - 設計文章頁面模板（基於現有 HTML 風格）
  - 優化 meta tags、Open Graph、canonical URLs

  **Must NOT do**:
  - 不得引入需要學習的框架
  - 不得改變現有網站的 HTML 結構
  - 不得忽略 SEO 基礎設置

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 技術評估和設置對 HTML-only 工作流來說很直接
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Tasks 8, 9
  - **Blocked By**: None (can start immediately)

  **References**:
  - `index.html` - 現有網站結構，作為基礎模板
  - 官方 docs: `https://schema.org/Article` - 文章結構化數據語法

  **Acceptance Criteria**:
  - [ ] SEO 優化文檔完成
  - [ ] 包含 schema.org 模板、sitemap 方案、文章頁面模板

  **QA Scenarios**:
  ```
  Scenario: 驗證 schema.org 結構
    Tool: Bash (grep)
    Preconditions: SEO 優化文檔已創建
    Steps:
      1. grep -c "schema.org" SEO 優化文檔
      2. 確認輸出大於 0
    Expected Result: 輸出大於 0
    Evidence: .sisyphus/evidence/task-3-schema-org.txt
  ```

  **Commit**: YES (groups with 3)
  - Message: `feat(seo): add HTML static site SEO optimization plan`

---

- [ ] 4. 建立 AI 內容生成 SOP

  **What to do**:
  - 設計 5 步驗證法流程
  - 創建 AI prompt 模板
  - 設計人工驗證清單
  - 創建內容審核流程

  **Must NOT do**:
  - 不得省略人工驗證步驟
  - 不得忽略免責聲明

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 需要仔細設計可重複的流程，包含多個驗證步驟
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Tasks 7, 10
  - **Blocked By**: Tasks 1, 2

  **References**:
  - 無

  **Acceptance Criteria**:
  - [ ] SOP 文檔完成
  - [ ] 包含 5 步驗證法、prompt 模板、審核清單

  **QA Scenarios**:
  ```
  Scenario: 驗證 SOP 完整性
    Tool: Bash (grep)
    Preconditions: SOP 文檔已創建
    Steps:
      1. grep -c "Step [1-5]" SOP 文檔
      2. 確認輸出為 5
    Expected Result: 輸出為 5
    Evidence: .sisyphus/evidence/task-4-sop-completeness.txt
  ```

  **Commit**: YES (groups with 4)
  - Message: `feat(sop): add AI content generation SOP`

---

- [ ] 5. 關鍵字研究與內容日曆

  **What to do**:
  - 使用 Exa 搜尋長尾關鍵字
  - 分析競爭對手關鍵字
  - 創建 30 天內容日曆
  - 確定每篇文章的主關鍵字和副關鍵字

  **Must NOT do**:
  - 不得選擇搜尋量過低的關鍵字
  - 不得忽略競爭度分析

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要研究和分析技能
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Tasks 1, 2

  **References**:
  - 無

  **Acceptance Criteria**:
  - [ ] 關鍵字清單完成
  - [ ] 內容日曆完成

  **QA Scenarios**:
  ```
  Scenario: 驗證關鍵字數量
    Tool: Bash (wc)
    Preconditions: 關鍵字清單已創建
    Steps:
      1. wc -l 關鍵字清單文件
      2. 確認行數大於等於 20
    Expected Result: 行數大於等於 20
    Evidence: .sisyphus/evidence/task-5-keyword-count.txt
  ```

  **Commit**: YES (groups with 5)
  - Message: `feat(keywords): add keyword research and content calendar`

---

- [ ] 6. 變現模式設計

  **What to do**:
  - 設計產品銷售策略
  - 研究並選擇聯盟計畫
  - 設計廣告收入策略
  - 創建變現路線圖

  **Must NOT do**:
  - 不得選擇與婚慶無關的聯盟產品
  - 不得忽略用戶體驗

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要商業策略和研究
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5)
  - **Blocks**: Tasks 11, 12
  - **Blocked By**: Tasks 1, 2

  **References**:
  - 無

  **Acceptance Criteria**:
  - [ ] 變現模式文檔完成
  - [ ] 包含至少 3 種變現方式

  **QA Scenarios**:
  ```
  Scenario: 變現方式數量驗證
    Tool: Bash (grep)
    Preconditions: 變現模式文檔已創建
    Steps:
      1. grep -c "變現方式" 變現模式文檔
      2. 確認輸出大於等於 3
    Expected Result: 輸出大於等於 3
    Evidence: .sisyphus/evidence/task-6-monetization-count.txt
  ```

  **Commit**: YES (groups with 6)
  - Message: `feat(monetization): add monetization strategy`

---

- [ ] 7. 生成首批 5 篇文章

  **What to do**:
  - 按照 SOP 生成 5 篇文章
  - 每篇文章必須通過 5 步驗證
  - 加入內部連結
  - 加入免責聲明

  **Must NOT do**:
  - 不得跳過驗證步驟
  - 不得發布未經驗證的內容

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 需要仔細執行 SOP，包含多個驗證步驟
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Tasks 10, 11
  - **Blocked By**: Tasks 4, 5

  **References**:
  - 無

  **Acceptance Criteria**:
  - [ ] 5 篇文章完成
  - [ ] 每篇文章通過 5 步驗證

  **QA Scenarios**:
  ```
  Scenario: 驗證文章數量
    Tool: Bash (ls)
    Preconditions: 文章已生成
    Steps:
      1. ls -1 文章目錄 | wc -l
      2. 確認輸出為 5
    Expected Result: 輸出為 5
    Evidence: .sisyphus/evidence/task-7-article-count.txt
  ```

  **Commit**: YES (groups with 7)
  - Message: `feat(content): generate first 5 articles`

---

- [ ] 8. 網站升級與內容發布

  **What to do**:
  - 基於現有 HTML 擴展網站結構
  - 發布 5 篇文章
  - 設置 SEO 基礎設置
  - 提交 sitemap 到 Google Search Console

  **Must NOT do**:
  - 不得忽略 SEO 基礎設置
  - 不得發布未經驗證的內容

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: 需要前端實現和設計
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 7, 9)
  - **Blocks**: Tasks 10, 11
  - **Blocked By**: Tasks 3, 7

  **References**:
  - `index.html` - 現有網站結構，作為基礎模板

  **Acceptance Criteria**:
  - [ ] 網站升級完成
  - [ ] 5 篇文章發布

  **QA Scenarios**:
  ```
  Scenario: 驗證網站可訪問
    Tool: Bash (curl)
    Preconditions: 網站已發布
    Steps:
      1. curl -I 網站 URL
      2. 確認 HTTP 狀態碼為 200
    Expected Result: HTTP 200
    Evidence: .sisyphus/evidence/task-8-site-accessible.txt
  ```

  **Commit**: YES (groups with 8)
  - Message: `feat(site): upgrade site and publish content`

---

- [ ] 9. SEO 優化與數據追蹤設置

  **What to do**:
  - 設置 GA4
  - 設置 Google Search Console
  - 設置 Hotjar（可選）
  - 提交 sitemap

  **Must NOT do**:
  - 不得忽略數據追蹤設置
  - 不得設置錯誤的追蹤代碼

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 設置任務很直接
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 7, 8)
  - **Blocks**: Task 10
  - **Blocked By**: Task 8

  **References**:
  - 無

  **Acceptance Criteria**:
  - [ ] GA4 設置完成
  - [ ] Search Console 設置完成

  **QA Scenarios**:
  ```
  Scenario: 驗證 GA4 代碼
    Tool: Bash (curl)
    Preconditions: GA4 代碼已添加
    Steps:
      1. curl 網站 URL | grep -c "gtag"
      2. 確認輸出大於 0
    Expected Result: 輸出大於 0
    Evidence: .sisyphus/evidence/task-9-ga4-setup.txt
  ```

  **Commit**: YES (groups with 9)
  - Message: `feat(seo): setup analytics and search console`

---

- [ ] 10. 數據分析與內容優化

  **What to do**:
  - 分析 GA4 數據
  - 分析 Search Console 數據
  - 優化低表現內容
  - 更新內容日曆

  **Must NOT do**:
  - 不得忽略數據分析
  - 不得基於猜測優化內容

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 需要數據分析和戰略優化
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 11, 12)
  - **Blocks**: Final verification
  - **Blocked By**: Tasks 7, 9

  **References**:
  - 無

  **Acceptance Criteria**:
  - [ ] 數據分析報告完成
  - [ ] 優化建議清單完成

  **QA Scenarios**:
  ```
  Scenario: 驗證數據分析報告
    Tool: Bash (grep)
    Preconditions: 報告已創建
    Steps:
      1. grep -c "優化建議" 報告文件
      2. 確認輸出大於 0
    Expected Result: 輸出大於 0
    Evidence: .sisyphus/evidence/task-10-analysis-report.txt
  ```

  **Commit**: YES (groups with 10)
  - Message: `feat(analysis): add data analysis and optimization`

---

- [ ] 11. 聯盟計畫整合

  **What to do**:
  - 簽約至少 2 個聯盟計畫
  - 在內容中加入聯盟連結
  - 設置聯盟追蹤
  - 測試聯盟連結

  **Must NOT do**:
  - 不得加入無關的聯盟產品
  - 不得隱藏聯盟連結的商業性質

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要商業開發和整合
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 10, 12)
  - **Blocks**: Final verification
  - **Blocked By**: Tasks 6, 7

  **References**:
  - 無

  **Acceptance Criteria**:
  - [ ] 至少 2 個聯盟計畫簽約
  - [ ] 聯盟連結已加入內容

  **QA Scenarios**:
  ```
  Scenario: 驗證聯盟連結
    Tool: Bash (grep)
    Preconditions: 聯盟連結已加入
    Steps:
      1. grep -c "affiliate" 內容文件
      2. 確認輸出大於 0
    Expected Result: 輸出大於 0
    Evidence: .sisyphus/evidence/task-11-affiliate-links.txt
  ```

  **Commit**: YES (groups with 11)
  - Message: `feat(affiliate): integrate affiliate programs`

---

- [ ] 12. 廣告收入設置

  **What to do**:
  - 申請 Google AdSense
  - 設置廣告位置
  - 優化廣告收入
  - 測試廣告顯示

  **Must NOT do**:
  - 不得放置過多廣告影響用戶體驗
  - 不得違反 AdSense 政策

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 設置任務很直接
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 10, 11)
  - **Blocks**: Final verification
  - **Blocked By**: Tasks 8, 9

  **References**:
  - 無

  **Acceptance Criteria**:
  - [ ] AdSense 申請完成
  - [ ] 廣告已顯示在網站上

  **QA Scenarios**:
  ```
  Scenario: 驗證廣告顯示
    Tool: Bash (curl)
    Preconditions: 廣告已設置
    Steps:
      1. curl 網站 URL | grep -c "adsense"
      2. 確認輸出大於 0
    Expected Result: 輸出大於 0
    Evidence: .sisyphus/evidence/task-12-ads-display.txt
  ```

  **Commit**: YES (groups with 12)
  - Message: `feat(ads): setup ad revenue`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
>
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, curl endpoint, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Review all changed files for: HTML validity, SEO best practices, schema.org correctness, meta tags completeness. Check AI slop: excessive comments, over-abstraction, generic names.
  Output: `HTML Valid [PASS/FAIL] | SEO [PASS/FAIL] | Schema [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill if UI)
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration (features working together, not isolation). Test edge cases: empty state, invalid input, rapid actions. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance. Detect cross-task contamination: Task N touching Task M's files. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **1**: `feat(content): add content verification framework`
- **2**: `feat(architecture): add pillar-cluster site architecture`
- **3**: `feat(seo): add HTML static site SEO optimization plan`
- **4**: `feat(sop): add AI content generation SOP`
- **5**: `feat(keywords): add keyword research and content calendar`
- **6**: `feat(monetization): add monetization strategy`
- **7**: `feat(content): generate first 5 articles`
- **8**: `feat(site): upgrade site and publish content`
- **9**: `feat(seo): setup analytics and search console`
- **10**: `feat(analysis): add data analysis and optimization`
- **11**: `feat(affiliate): integrate affiliate programs`
- **12**: `feat(ads): setup ad revenue`

---

## Success Criteria

### Verification Commands
```bash
# 驗證框架完整性
grep -c "Tier [0-4]" .sisyphus/plans/content-verification-framework.md  # Expected: 5

# 驗證關鍵字數量
wc -l 關鍵字清單文件  # Expected: >= 20

# 驗證文章數量
ls -1 文章目錄 | wc -l  # Expected: 5

# 驗證網站可訪問
curl -I 網站 URL  # Expected: HTTP 200

# 驗證 GA4 代碼
curl 網站 URL | grep -c "gtag"  # Expected: > 0
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] All tests pass
- [ ] All evidence files exist
- [ ] All QA scenarios passed
- [ ] User explicit approval received
