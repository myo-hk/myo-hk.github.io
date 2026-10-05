# 教訓：MCP Notion 工具的巢狀陣列序列化與 update_content 匹配失敗

> **日期**：2026-09-30
> **關聯**：MyO 內容庫遷移（建 5 個子頁、更新 27 列）
> **狀態**：已解決
> **環境層**：此坑不限於本專案，其他專案也可能踩到

---

### 問題

**坑 1：巢狀陣列被序列化錯誤**

`notion_API-post-page` 的 `properties` 傳入巢狀結構時失敗：

```json
// 失敗
{"properties": {"title": {"title": [{"type":"text","text":{"content":"📊 內容企劃總覽"}}]}}}
```
→ `validation_error: body.properties.title.title should be an array, instead was {"item":{...}}`

巢狀陣列被壓成 `{"item": ...}` 物件。**解法是把整個 properties 改成 JSON 字串**：

```json
// 成功
{"properties": "{\"title\": {\"title\": [{\"type\": \"text\", \"text\": {\"content\": \"📊 內容企劃總覽\"}}]}}"}
```

注意 `notion_API-patch-page` 的 `properties` 接受物件，而 `post-page` 的需用字串 —— 兩者 schema 宣告不一致。

**坑 2：`update_content` 的 `old_str` 必須逐字相符**

Notion 儲存的 markdown 已經過正規化，與你寫入時的字串有差異（`·` → `•`、`/` → `\/`、換行被重排）。用原始寫入字串當 `old_str` 會得到：

```
No matches found for ### image_prompt 結構（兩段式）...
```

**坑 3：curl 在 zsh 中不做變數字元拆分**

```bash
IDS="id1 id2 id3"
for id in $IDS; do curl ... "https://api.notion.com/v1/pages/$id"; done
# → 只跑一次，$id 是整串，HTTP 000
```

zsh 預設不做 word splitting，整串被當成單一 URL。

### 教訓

**MCP 工具的參數型別宣告與實際序列化行為不一定一致。** 遇到巢狀結構被壓平時，繞過方式是**整段改用 JSON 字串**，而非逐一猜測欄位型別。

`update_content` 屬於**字串比對**操作，不是結構化更新 —— Notion 端已正規化的內容無法用原始字串反查。要可靠更新既有區塊，改用 block API 逐块改寫。

zsh 的 `for x in $VAR` **不等於 bash**。批量呼叫 API 必須改用 `while read` 或陣列。

### 解法

**巢狀陣列 → JSON 字串：**

```json
{"properties": "{\"title\": {\"title\": [{\"type\":\"text\",\"text\":{\"content\":\"...\"}}]}}"}
```

**批量 archive / patch 用 `while read`（zsh 安全）：**

```bash
cat > /tmp/ids.txt <<'EOF'
page-id-1
page-id-2
EOF

TOKEN=$(tr -d ' \n\r' < ~/.local/share/opencode-v1/config/opencode/secrets/notion_token)
ok=0; fail=0
while IFS= read -r id; do
  [ -z "$id" ] && continue
  code=$(curl -s -o /dev/null -w '%{http_code}' -X PATCH "https://api.notion.com/v1/pages/$id" \
    -H "Authorization: Bearer $TOKEN" -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" -d '{"archived":true}')
  [ "$code" = "200" ] && ok=$((ok+1)) || { fail=$((fail+1)); echo "FAIL $code $id"; }
  sleep 0.32
done < /tmp/ids.txt
```

**改既有 block 用 block API 逐块改**（比 `update_content` 可靠，且不受正規化影響）：

```python
def rt(t): return [{"type": "text", "text": {"content": t}}]

# 先列出 blocks 找出目標 index
req = urllib.request.Request(
    f'https://api.notion.com/v1/blocks/{PAGE_ID}/children?page_size=100', headers=H)
blocks = json.loads(urllib.request.urlopen(req).read())['results']

# 逐块 PATCH，key 必須是該 block 實際的 type
rq = urllib.request.Request(f'https://api.notion.com/v1/blocks/{blocks[i]["id"]}',
    data=json.dumps({"heading_3": {"rich_text": rt("新標題")}}).encode(),
    headers=H, method='PATCH')
```

**table 要改內容得逐 row 改：**

```python
rows = json.loads(urllib.request.urlopen(
    urllib.request.Request(f'https://api.notion.com/v1/blocks/{table_id}/children',
                           headers=H)).read())['results']
# rows[i] 是 table_row，PATCH {"table_row": {"cells": [[...],[...],[...]]}}
```

### 預防

1. **巢狀陣列被壓成 `{"item":...}` → 整段改 JSON 字串**，這是 MCP Notion 工具的通用繞法
2. **要改既有內容 → 用 block API 逐块 PATCH**，`update_content` 只適合「剛寫入、尚未正規化」的內容
3. **block PATCH 的 key 必須匹配實際 type**（`heading_3` vs `paragraph` vs `code`），不匹配會得到 `Block type mismatch` —— 先列 blocks 確認 type 再改
4. **批量 API 呼叫在 zsh 用 `while read`**，不要用 `for x in $VAR`
5. 批量操作後**逐項收集非 200 的 ID 並回報**，不要只看總數
