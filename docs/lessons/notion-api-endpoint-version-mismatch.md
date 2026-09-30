# 教訓：Notion API 2022-06-28 版查詢 data source 回傳空結果

> **日期**：2026-09-30
> **關聯**：MyO 內容庫遷移（27 列寫入 + 5 個子頁建置）
> **狀態**：已解決
> **環境層**：此坑不限於本專案，其他專案也可能踩到

---

### 問題

用 `Notion-Version: 2022-06-28` 對 **inline database** 查詢時，`POST /v1/data_sources/{id}/query` 回傳 `results: []`，但同樣條件改用 `POST /v1/databases/{id}/query` 就拿到完整 27 列。

兩者差異：

| 端點 | 2022-06-28 版本 | 結果 |
|---|---|---|
| `POST /v1/data_sources/{data_source_id}/query` | 可呼叫、無錯誤 | **`results: []`（靜默失敗）** |
| `POST /v1/databases/{database_id}/query` | 可呼叫 | 27 列全部回傳 |

2022-06-28 是 database/data_source 拆分**之前**的版本，`data_sources` 命名空間尚未存在，所以查詢靜默回空 —— **沒有 404、沒有錯誤，只有一個空陣列**。

同一版本下建立的頁面，`parent` 回傳值是 `{"type":"database_id","database_id":"..."}` 而非 `data_source_id`，容易誤判寫入位置錯誤。

另一個不一致：同一頁 `b546ee9afad28336b89e019ea358c036` 用 curl `PATCH /v1/pages/{id}` + `{"archived":true}` 回 **404 object_not_found**，但用 MCP `notion_API-patch-page` + `in_trash: true` **成功**。

### 教訓

**Notion API 的版本與端點必須配對使用。** 2022-06-28 只認 `databases/*`；`data_sources/*` 要 2025-09-03 之後的版本。兩者混用時**不會報錯**，只會靜默回空或 404 —— 這是最危險的一類失敗，因為你會以為資料真的沒寫進去，進而重複建立或錯誤回滾。

### 解法

**查詢一律用 `databases/{database_id}/query`**，與 2022-06-28 配對：

```bash
curl -s -X POST "https://api.notion.com/v1/databases/$DB_ID/query" \
  -H "Authorization: Bearer $TOKEN" -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" -d '{"page_size":100}'
```

`data_source_id` 只用於**寫入**時的 parent：

```json
{"parent": {"type": "data_source_id", "data_source_id": "<DS_ID>"}}
```

**單列 archive 失敗時改用 MCP 工具**（`notion_API-patch-page` + `in_trash: true`），不要重試 curl。

**驗證寫入結果時，先抽樣讀回單頁確認 parent：**

```bash
curl -s "https://api.notion.com/v1/pages/$PAGE_ID" \
  -H "Authorization: Bearer $TOKEN" -H "Notion-Version: 2022-06-28" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['parent'])"
```

### 預防

1. **查詢結果為空時，先換端點再下結論。** 空陣列的第一嫌疑是端點／版本錯配，不是「資料不存在」
2. 寫入批次後**必須回查**並印列數 —— 本次正是靠回查發現查詢端點錯誤，否則會誤以為 27 列全部寫入失敗而重做
3. `data_source_id`（寫入）與 `database_id`（查詢）用途不同，記住對應關係：

| 用途 | 參數 | 端點（2022-06-28） |
|---|---|---|
| 查詢 | `database_id` | `POST /v1/databases/{id}/query` |
| 寫入 | `data_source_id` | `POST /v1/pages` |
| 改欄位 | `data_source_id` | `PATCH /v1/data_sources/{id}` |

4. curl 與 MCP 對同一操作行為不一致時（404 vs 成功），**以 MCP 為準並記錄差異**，不要反覆重試 curl
