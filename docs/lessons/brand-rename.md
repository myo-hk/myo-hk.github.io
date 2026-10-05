# 教訓：批次更名時的三個自我毀滅陷阱

> **日期**：2026-09-29
> **關聯 PR**：品牌更名 My O! → MyO（`scripts/rename_brand.py`）
> **狀態**：已解決

---

### 問題

用批次腳本把 453 個檔案的 `My O!` 改為 `MyO`。腳本本身寫對了、乾跑數字也對，但有
三個陷阱會讓「正確的腳本」產出「錯誤的結果」，而且全部是靜默的：

1. **取代腳本改寫了自己** — `rename_brand.py` 與 `test_rename_brand.py` 內含
   `My O!` 字面（作為 regex 與測試輸入）。若不排除，Phase 2 的通配會把
   `PHASE2 = re.compile(r'My O!')` 改寫成 `re.compile(r'MyO')` — 變成永遠匹配不到
   的 no-op 規則，同時所有測試的 `src` / `expected` 一起崩壞。
   腳本會在無錯誤訊息的情況下永久失效。

2. **產物被文字取代後被覆寫回來** — `scripts/blog_index.json` 是 `parse_blog.py`
   的產物。直接改字串，下次任何人重跑 `parse_blog.py` 就會從（已更名的）HTML
   重新生成看似正確的內容，但 `blog_index.json` 裡的摘要文字取自文章 metadata
   而非全文，某些欄位不會跟著更新。

3. **「修改檔數為 0」不能當作正則失效的判斷依據** — `optimize_blog_head.py` 的
   `FOOTER_LOGO` 正則硬寫 `alt="My O! Logo"`。HTML 改名後正則不再匹配，但
   `--dry-run` 顯示的仍是 `Would modify 0 of 421` — 因為最佳化早已套用完畢，
   沒有任何待修改項。**無論正則是否正確，這個判斷條件都回報 0。**

---

### 教訓

批次取代腳本必須排除**三類自我指涉**：

| 類別 | 例子 | 為何 |
|---|---|---|
| 工具自身 | 取代腳本、其測試 | 內含目標字面作為 regex / 測試資料 |
| 產物 | `blog_index.json`、minified bundle | 由其他流程生成，應重新生成 |
| 執行期暫存 | ledger、review package | 記錄了討論過程中的目標字面 |

驗證生成器一致性要用**字串比對**，不要依賴「修改檔數」這種間接指標：

```python
pat = re.search(r'alt="([^"]+)"', MODULE.CONSTANT).group(1)
hits = sum(len(re.findall(re.escape(pat), f.read_text())) for f in Path('blog').glob('*.html'))
sys.exit(0 if hits == EXPECTED else 1)
```

---

### 解法

`scripts/rename_brand.py` 的排除清單分三層：

```python
EXCLUDE_DIRS = {..., 'image'}          # 純二進位

EXCLUDE_PATH_SUBSTR = (
    '/presentation/dist/',             # minified，需 rebuild
    'scripts/blog_index.json',         # 由 parse_blog.py 重新生成
    'docs/superpowers/',               # 歷史決策紀錄
    'scripts/rename_brand.py',         # 工具自身
    'scripts/test_rename_brand.py',
    '.superpowers/',                   # 執行期暫存
)
```

自我保護由測試釘住，不只靠註解：

```python
def test_self_scan_would_corrupt_regex_patterns(self):
    """守恆式測試：證明排除是必要的，而非多餘。"""
    src = open('rename_brand.py', encoding='utf-8').read()
    corrupted, _, p2, _ = rb.apply_phases(src)
    assert corrupted != src, "未排除時工具檔會被改寫，排除清單是必要的"
    assert 're.compile(r\'MyO\')' in corrupted, "PHASE2 regex 會退化成 no-op"
```

---

### 預防

1. 批次取代前先問：**腳本會不會改寫自己？** 把工具自身與其測試加入排除清單。
2. 產物永遠重新生成，不文字取代。產物的來源腳本若含舊名，要一併排除或更新。
3. 驗證正則類生成器時，直接比對常數字串與目標檔案內容，不要相信「修改檔數」。
4. 批次取代後跑一次**冪等性檢查**：再乾跑一次，全部計數應為 0。這同時驗證了
   「沒有漏網」與「不會二次改寫」兩件事。
5. 在 worktree 內執行，別在 `main` 上。任何一個靜默陷阱的後果都是 453 檔的
   錯誤改寫。
