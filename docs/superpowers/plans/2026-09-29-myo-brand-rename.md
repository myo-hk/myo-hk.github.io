# 品牌更名 My O! → MyO Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將全站 453 個檔案的品牌字串由 `My O!` 更名為 `MyO`（正文）與 `MyO!`（視覺 wordmark），檔名、網域、URL 與 logo 圖檔維持不變。

**Architecture:** 單一 Python 腳本 `scripts/rename_brand.py` 執行三階段有序取代。Phase 1 以 6 個精確錨點保護視覺 wordmark 上下文（轉為 `MyO!`），Phase 2 通配取代其餘為 `MyO`，Phase 3 正規化 `MYO` 大小寫變體。Phase 1 先執行使其產物不再含 `My O` 字面，因此 Phase 2 的通配不會誤傷。產物 `scripts/blog_index.json` 與 `sw.js` 快取版本另行處理，不走文字取代。

**Tech Stack:** Python 3（標準函式庫 `os` / `re` / `pathlib`）、pytest 8.4.2、Playwright 1.40（既有）

**Spec:** `docs/superpowers/specs/2026-09-29-myo-brand-rename-design.md`

## Global Constraints

- 品牌字串僅兩種合法形態：正文 `MyO`（無驚嘆號）、視覺 wordmark `MyO!`（有驚嘆號）。不得出現 `My O`（含空格）任何形態殘留。
- 檔名、目錄名、網域、URL slug 一律不變。`presentations/08-certificate-size-specs/presentation/src/chapters/05-myo/Myo.tsx`、`Myo.css`、`05-myo/` 維持原名。
- `image/` 全部二進位檔不動。logo 圖檔內烙印之「My O!」為既定決策。
- `docs/superpowers/plans/`、`docs/superpowers/specs/`、`docs/PageSpeed Insights.html`、`docs/architecture-diagram.html` 一律不改寫（歷史紀錄與工具產物）。
- PostHog 專案名 `MyO Cert Holder` 不得改動（永久 ID）。
- 所有 Python 批次腳本支援 `--test` 乾跑；`scripts/optimize_blog_head.py` 的既有旗標為 `--dry-run`，不得改動其介面。
- 不新增相依套件。不使用 `as any`、`@ts-ignore` 或任何型別抑制。

## Review Focus

以下五項是 spec 隱含但無測試覆蓋、最可能造成實際傷害的情況。每一項都已在上方對應任務中補上測試步驟。

1. **`alt="My O! Logo"` 若被 Phase 2 通配搶先處理** — 會變成 `alt="MyO Logo"`，logo 替代文字與視覺 wordmark 不一致，且 `optimize_blog_head.py` 的 `FOOTER_LOGO` 正則從此永不匹配（靜默失效，無錯誤訊息）。
2. **`scripts/blog_index.json` 若用文字取代** — 內容會在下一次 `python3 scripts/parse_blog.py` 執行時被重新產生的舊名覆蓋，且無任何錯誤。
3. **`sw.js` `CACHE_NAME` 未升版** — 已安裝 PWA 的回訪用戶會持續由 service worker 取得舊 HTML，看到舊品牌名，發布後無法靠重新整理解決。
4. **`presentations/*/presentation/dist/` 內的 minified JS** — `08-certificate-size-specs` 的 bundle 含 `MYO`，文字取代對 minified 產物無效（雜湊檔名已內嵌），必須 rebuild。
5. **巢狀副本 `Users/baba/Documents/Github/myo-hk/`** — 目錄名含專案名且含完整舊內容，若未排除會造成雙份改寫與 git 混亂。

---

## File Structure

| 檔案 | 動作 | 責任 |
|---|---|---|
| `scripts/rename_brand.py` | 建立 | 三階段取代引擎、排除清單過濾、計數報告 |
| `scripts/test_rename_brand.py` | 建立 | `rename_brand` 的 pytest 套件（沿用 `scripts/test_add_posthog.py` 的 `sys.path.insert` 慣例） |
| `blog/*.html`（421 篇） | 修改 | Phase 1 + Phase 2 |
| 根目錄 18 個檔案 | 修改 | Phase 1 + Phase 2 |
| `scripts/*.py`、`add_sticky_bar.py`、`fix_*.py` | 修改 | Phase 1 + Phase 2（含 `optimize_blog_head.py` 的 `FOOTER_LOGO` 正則與 `FOOTER_LOGO_REPLACEMENT`） |
| `tests/*.ts`、`tests/lighthouse-check.sh` | 手動修改 | `toHaveTitle(/My O/)` 不含驚嘆號，Phase 1/2 皆不會處理 |
| `presentations/08-.../src/**/*.tsx` | 修改 | Phase 3（2 處 `MYO`） |
| `scripts/blog_index.json` | 重新生成 | 不走文字取代 |
| `sw.js` | 手動修改 | `CACHE_NAME` 升版 |
| `README.md`、`AGENTS.md`、`pricing.md`、`docs/ai-visibility-monitoring.md` | 修改 | Phase 2 |

---

### Task 1: rename_brand.py 取代引擎（TDD）

**Files:**
- Create: `scripts/rename_brand.py`
- Test: `scripts/test_rename_brand.py`

**Interfaces:**
- Consumes: 無（首個任務）
- Produces:
  - `PHASE1_ANCHORS: list[tuple[re.Pattern[str], str]]` — 6 個 `(regex, replacement)` 依序套用
  - `PHASE2: tuple[re.Pattern[str], str]` — `(re.compile(r'My O!'), 'MyO')`
  - `PHASE3: tuple[re.Pattern[str], str]` — `(re.compile(r'MYO(?=證書套)'), 'MyO')`
  - `EXCLUDE_DIRS: set[str]` — 目錄名排除集合
  - `EXCLUDE_PATH_SUBSTR: tuple[str, ...]` — 路徑子字串排除元組
  - `TEXT_EXTS: tuple[str, ...]` — 允許的副檔名
  - `apply_phases(text: str) -> tuple[str, int, int, int]` — 回傳 `(新文字, phase1命中, phase2命中, phase3命中)`
  - `is_excluded(rel_path: str) -> bool` — 判斷路徑是否應被排除

- [ ] **Step 1: 寫失敗的測試**

建立 `scripts/test_rename_brand.py`：

```python
#!/usr/bin/env python3
"""
pytest suite for rename_brand.py.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import rename_brand as rb


class TestPhase1Anchors:
    """Phase 1 必須把視覺 wordmark 轉為 MyO! 且保留驚嘆號。"""

    @pytest.mark.parametrize("src,expected", [
        ('<img src="image/01_company_logo.webp" alt="My O! Logo" width="50">',
         '<img src="image/01_company_logo.webp" alt="MyO! Logo" width="50">'),
        ('<img src="image/01_company_logo.webp" alt="My O! logo" width="50">',
         '<img src="image/01_company_logo.webp" alt="MyO! logo" width="50">'),
        ('<span class="QTKDff text-rose-500">My O!</span>專屬結婚證書套',
         '<span class="QTKDff text-rose-500">MyO!</span>專屬結婚證書套'),
        ('<div class="brand">My O!</div>',
         '<div class="brand">MyO!</div>'),
        ('<meta name="apple-mobile-web-app-title" content="My O!">',
         '<meta name="apple-mobile-web-app-title" content="MyO!">'),
        ('<meta property="og:image:alt" content="My O! 證書套公司 Logo">',
         '<meta property="og:image:alt" content="MyO! 證書套公司 Logo">'),
    ])
    def test_phase1_anchored_contexts_keep_bang(self, src, expected):
        out, p1, p2, p3 = rb.apply_phases(src)
        assert p1 == 1, f"應由 Phase 1 處理一次，實際 p1={p1}"
        assert p2 == 0, f"Phase 1 產物不應被 Phase 2 再處理，實際 p2={p2}"
        assert out == expected

    def test_short_name_anchor_keeps_bang(self):
        """單獨驗證 short_name 錨點，避免與 name 欄位混在同一個案例。"""
        src = '{"name": "x", "short_name": "My O!"}'
        out, p1, p2, _ = rb.apply_phases(src)
        assert (p1, p2) == (1, 0)
        assert out == '{"name": "x", "short_name": "MyO!"}'

    def test_mixed_context_routes_each_field_to_correct_phase(self):
        """同一份 JSON 內，short_name 走 Phase 1、name 走 Phase 2。"""
        src = '{"name": "My O! 專屬結婚證書套", "short_name": "My O!"}'
        out, p1, p2, _ = rb.apply_phases(src)
        assert (p1, p2) == (1, 1)
        assert out == '{"name": "MyO 專屬結婚證書套", "short_name": "MyO!"}'

    def test_phase1_alt_substring_must_match_whole_word(self):
        """alt 值為 Logo / logo 兩種；錨點不可誤傷其他值。"""
        src = '<img alt="My O! Logo Collection">'
        out, p1, p2, _ = rb.apply_phases(src)
        # 錨點要求 alt="My O! Logo" 完整閉合引號，此處不閉合 → 落到 Phase 2
        assert p1 == 0
        assert p2 == 1
        assert out == '<img alt="MyO Logo Collection">'


class TestPhase2:
    """Phase 2 處理正文，移除驚嘆號。"""

    @pytest.mark.parametrize("src,expected", [
        ('<title>My O! 專屬結婚證書套：設計師級 | 香港</title>',
         '<title>MyO 專屬結婚證書套：設計師級 | 香港</title>'),
        ('<p class="tip">My O! 貼士：提前規劃能幫你節省更多</p>',
         '<p class="tip">MyO 貼士：提前規劃能幫你節省更多</p>'),
        ('<p>My O! 版權所有。</p>', '<p>MyO 版權所有。</p>'),
        ('"name": "My O! Custom Wedding Certificate Holder"',
         '"name": "MyO Custom Wedding Certificate Holder"'),
    ])
    def test_phase2_body_contexts_drop_bang(self, src, expected):
        out, p1, p2, _ = rb.apply_phases(src)
        assert p1 == 0
        assert p2 == 1
        assert out == expected

    def test_phase2_does_not_double_replace_phase1_output(self):
        """Review Focus #1：Phase 1 產物必須免於 Phase 2 通配。"""
        out, p1, p2, _ = rb.apply_phases('<span>My O!</span>')
        assert (p1, p2) == (1, 0)
        assert out == '<span>MyO!</span>'


class TestPhase3:
    """Phase 3 正規化全大寫 MYO。"""

    def test_phase3_myo_uppercase_to_mixed(self):
        src = 'const CATEGORIES = ["標準尺寸", "MYO證書套"];'
        out, _, _, p3 = rb.apply_phases(src)
        assert p3 == 1
        assert out == 'const CATEGORIES = ["標準尺寸", "MyO 證書套"];'

    def test_phase3_does_not_touch_identifier_myo(self):
        """Myo.tsx 的元件函式名與 05-myo 目錄 id 不是品牌字串。"""
        src = 'export function Myo({ step }) { return null; }'
        out, _, _, p3 = rb.apply_phases(src)
        assert p3 == 0
        assert out == src


class TestIdempotency:
    """重跑不得二次改寫。"""

    @pytest.mark.parametrize("src", [
        '<title>MyO 專屬結婚證書套</title>',
        '<img alt="MyO! Logo">',
        '<div class="brand">MyO!</div>',
        '"MYO證書套"',
    ])
    def test_second_pass_is_noop(self, src):
        once, *_ = rb.apply_phases(src)
        twice, p1, p2, p3 = rb.apply_phases(once)
        assert twice == once
        assert (p1, p2, p3) == (0, 0, 0)


class TestExclusions:
    """Review Focus #2 / #5：產物與巢狀副本必須排除。"""

    @pytest.mark.parametrize("rel,excluded", [
        ('image/01_company_logo.webp', True),
        ('scripts/blog_index.json', True),
        ('docs/superpowers/plans/2026-07-08-seo-bulk-fix.md', True),
        ('docs/superpowers/specs/2026-07-13-homepage-faq-seo-design.md', True),
        ('docs/PageSpeed Insights.html', True),
        ('docs/architecture-diagram.html', True),
        ('presentations/08-certificate-size-specs/presentation/dist/assets/index-x.js', True),
        ('Users/baba/Documents/Github/myo-hk/index.html', True),
        ('index.html', False),
        ('blog/婚禮籌備清單.html', False),
        ('scripts/optimize_blog_head.py', False),
        ('presentations/08-certificate-size-specs/src/registry/chapters.ts', False),
    ])
    def test_is_excluded(self, rel, excluded):
        assert rb.is_excluded(rel) is excluded

    def test_blog_index_json_never_included(self):
        """Review Focus #2：該檔由 parse_blog.py 重新生成，不走文字取代。"""
        assert rb.is_excluded('scripts/blog_index.json') is True


class TestNoResidualSpacedForm:
    """全域約束：不得殘留含空格的 My O。"""

    def test_spaced_form_never_survives(self):
        src = 'My O! 專屬結婚證書套 My O! 貼士：'
        out, *_ = rb.apply_phases(src)
        assert 'My O' not in out
        assert out == 'MyO 專屬結婚證書套 MyO 貼士：'
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `python3 -m pytest scripts/test_rename_brand.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'rename_brand'`

- [ ] **Step 3: 寫入最小實作**

建立 `scripts/rename_brand.py`：

```python
#!/usr/bin/env python3
"""
品牌更名 My O! -> MyO。

三階段有序取代：
  Phase 1  視覺 wordmark / logo 上下文 -> MyO!  （保留驚嘆號）
  Phase 2  其餘全部                     -> MyO   （去驚嘆號）
  Phase 3  大小寫變體 MYO               -> MyO

Phase 1 先執行，其產物已不含 "My O" 字面，故 Phase 2 通配不會誤傷。

Usage:
    python3 scripts/rename_brand.py --test    # 乾跑，不寫入
    python3 scripts/rename_brand.py --write   # 寫入
"""
import os
import re
import sys

# 允許處理的副檔名
TEXT_EXTS = (
    '.html', '.md', '.py', '.json', '.js', '.ts', '.tsx',
    '.txt', '.yml', '.yaml', '.sh', '.css',
)

# 排除的目錄名（任一層級命中即排除）
EXCLUDE_DIRS = {
    '.git', 'node_modules', '.omo', '.gstack', '.worktrees',
    'test-results', 'playwright-report', '.playwright-mcp',
    'Users', 'dist', 'image',
}

# 排除的路徑子字串
EXCLUDE_PATH_SUBSTR = (
    '/presentation/dist/',
    'scripts/blog_index.json',      # 由 parse_blog.py 重新生成
    'docs/superpowers/',             # 歷史決策紀錄
    'docs/PageSpeed Insights.html',  # 工具產出報告
    'docs/architecture-diagram.html',
)

# Phase 1：視覺上下文錨點，依序套用
PHASE1_ANCHORS = [
    (re.compile(r'alt="My O! ([Ll]ogo)"'), r'alt="MyO! \1"'),
    (re.compile(r'(og:image:alt" content=")My O!'), r'\1MyO!'),
    (re.compile(r'>My O!</span>'), '>MyO!</span>'),
    (re.compile(r'>My O!</div>'), '>MyO!</div>'),
    (re.compile(r'("short_name":\s*")My O!(")'), r'\1MyO!\2'),
    (re.compile(r'(apple-mobile-web-app-title" content=")My O!(")'), r'\1MyO!\2'),
]

# Phase 2：正文通配
PHASE2 = (re.compile(r'My O!'), 'MyO')

# Phase 3：全大寫變體（消耗整個 MYO證書套，产出含空格的 MyO 證書套）
PHASE3 = (re.compile(r'MYO證書套'), 'MyO 證書套')

OLD_BRAND = re.compile(r'My O!')


def is_excluded(rel_path):
    """判斷相對於 repo 根的路徑是否應排除。"""
    norm = rel_path.replace(os.sep, '/')
    parts = norm.split('/')
    if any(p in EXCLUDE_DIRS for p in parts[:-1]):
        return True
    return any(s in norm for s in EXCLUDE_PATH_SUBSTR)


def apply_phases(text):
    """依序套用三階段。回傳 (新文字, phase1命中, phase2命中, phase3命中)。"""
    p1 = p2 = p3 = 0
    for rx, repl in PHASE1_ANCHORS:
        text, n = rx.subn(repl, text)
        p1 += n
    text, p2 = PHASE2[0].subn(PHASE2[1], text)
    text, p3 = PHASE3[0].subn(PHASE3[1], text)
    return text, p1, p2, p3


def iter_targets():
    """走訪所有應處理且含品牌字串的檔案。"""
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in files:
            if not name.endswith(TEXT_EXTS):
                continue
            rel = os.path.relpath(os.path.join(root, name), '.').replace(os.sep, '/')
            if is_excluded(rel):
                continue
            yield rel


def main():
    write = '--write' in sys.argv
    dry = '--test' in sys.argv
    if not write and not dry:
        print(__doc__)
        print('必須指定 --test（乾跑）或 --write（寫入）')
        return 1

    baseline = 0
    tot1 = tot2 = tot3 = 0
    changed_files = 0

    for rel in iter_targets():
        text = open(rel, encoding='utf-8').read()
        n_old = len(OLD_BRAND.findall(text))
        if not n_old and not PHASE3[0].search(text):
            continue
        baseline += n_old
        new, a, b, c = apply_phases(text)
        tot1 += a
        tot2 += b
        tot3 += c
        if new != text:
            changed_files += 1
            if write:
                open(rel, 'w', encoding='utf-8').write(new)

    mode = 'WRITE' if write else 'TEST (dry-run)'
    print(f'\n=== rename_brand [{mode}] ===')
    print(f"  My O! 初始總數      : {baseline}")
    print(f'  Phase 1 (-> MyO!)   : {tot1}')
    print(f'  Phase 2 (-> MyO)    : {tot2}')
    print(f'  Phase 3 (MYO->MyO)  : {tot3}')
    print(f'  會修改的檔案數      : {changed_files}')
    print(f'  守恆式 P1+P2        : {tot1 + tot2} (應 == {baseline})')
    ok = (tot1 + tot2) == baseline
    print(f'  守恆式              : {"PASS" if ok else "FAIL"}')
    if not ok:
        return 1
    if not write:
        print('\n乾跑結束，未寫入任何檔案。確認數字無誤後加 --write。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

- [ ] **Step 4: 執行測試確認通過**

Run: `python3 -m pytest scripts/test_rename_brand.py -q`
Expected: PASS — 全部 passed

- [ ] **Step 5: 執行乾跑並比對 spec 數字**

Run: `python3 scripts/rename_brand.py --test`
Expected: 輸出以下數值，與 spec 第 7 節閘門 2 的期望值完全一致

```
  My O! 初始總數      : 6842
  Phase 1 (-> MyO!)   : 2147
  Phase 2 (-> MyO)    : 4695
  Phase 3 (MYO->MyO)  : 2
  會修改的檔案數      : 453
  守恆式 P1+P2        : 6842 (應 == 6842)
  守恆式              : PASS
```

若守恆式為 FAIL，停止並回到 Step 1 補齊 Phase 1 錨點。**數字不符時不得執行 `--write`。**

- [ ] **Step 6: Commit**

```bash
git add scripts/rename_brand.py scripts/test_rename_brand.py
git commit -m "feat(scripts): add rename_brand.py — three-phase My O! -> MyO replacement"
```

---

### Task 2: 執行更名並重新生成產物

**Files:**
- Modify: 453 個檔案（Phase 1 + Phase 2 + Phase 3 自動處理）
- Regenerate: `scripts/blog_index.json`

**Interfaces:**
- Consumes: Task 1 的 `scripts/rename_brand.py`
- Produces: 全站更名後的檔案內容

- [ ] **Step 1: 執行寫入**

Run: `python3 scripts/rename_brand.py --write`
Expected: 守恆式 PASS，且 stdout 顯示 453 檔案已修改

- [ ] **Step 2: 重新生成 blog_index.json（Review Focus #2）**

Run: `python3 scripts/parse_blog.py`
Expected: exit 0，`scripts/blog_index.json` 被重寫

驗證重新生成而非殘留舊名：

Run: `grep -c 'My O' scripts/blog_index.json || echo "0 (乾淨)"`
Expected: 輸出 `0 (乾淨)`

- [ ] **Step 3: 驗證舊名歸零（spec 閘門 1）**

Run:
```bash
python3 -c "
import os, re, sys
sys.path.insert(0,'scripts')
from rename_brand import iter_targets, EXCLUDE_DIRS
hits=[]
for rel in iter_targets():
    t=open(rel,encoding='utf-8').read()
    if re.search(r'My O!|MYO', t): hits.append(rel)
print(f'殘留檔案: {len(hits)}')
for h in hits[:10]: print(' ', h)
sys.exit(1 if hits else 0)
"
```
Expected: 輸出 `殘留檔案: 0`，exit code 0

- [ ] **Step 4: 檢視 diff 抽樣**

Run: `git diff --stat | tail -5`
Expected: 453 files changed

Run: `git diff index.html | head -40`
Expected: `<title>` 與 meta 顯示 `MyO`，logo `alt` 顯示 `MyO!`

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "refactor(brand): rename My O! to MyO across 453 files"
```

---

### Task 3: 修正測試斷言與 sw.js 快取版本

**Files:**
- Modify: `tests/homepage.spec.ts:7`
- Modify: `sw.js:2`

**Interfaces:**
- Consumes: Task 2 完成後的檔案內容
- Produces: 可通過的 Playwright 測試；回訪用戶取得新 HTML

- [ ] **Step 1: 修正 homepage.spec.ts 的正則斷言**

此斷言為 `/My O/`（不含驚嘆號），Phase 1 與 Phase 2 皆不會處理它，必須手動修正。

修改 `tests/homepage.spec.ts:7`：

```typescript
    await expect(page).toHaveTitle(/MyO/);
```

原值為 `await expect(page).toHaveTitle(/My O/);`

- [ ] **Step 2: 確認其餘測試斷言已自動一致**

Run: `grep -n 'My O\|MyO' tests/*.spec.ts tests/lighthouse-check.sh`
Expected:
- `homepage.spec.ts` — `MyO`（含描述文字與新正則）
- `mobile.spec.ts` — `MyO 手機版`（Phase 2 已處理）
- `poster-en.spec.ts` — `MyO Wedding Certificate Holder`（Phase 2 已處理，與 `poster-en.html` 的 `<title>` 同為 `MyO`，自動一致）
- `lighthouse-check.sh` — `MyO`（Phase 2 已處理）

不得出現任何仍含 `My O`（含空格）的行。

- [ ] **Step 3: 升版 sw.js CACHE_NAME（Review Focus #3）**

修改 `sw.js:2`：

```javascript
const CACHE_NAME = 'myo-cache-v3';
```

原值為 `const CACHE_NAME = 'myo-cache-v2';`

同時確認 `sw.js:1` 的註解已由 Phase 2 改為 `// MyO Service Worker`。

- [ ] **Step 4: 執行 Playwright 測試（spec 閘門 3）**

Run: `npm test`
Expected: PASS — Mobile / Desktop / Tablet 三裝置全綠

若 `homepage.spec.ts` 仍失敗，確認斷言已改為 `/MyO/`，且 `index.html` 的 `<title>` 確實含 `MyO`。

- [ ] **Step 5: Commit**

```bash
git add tests/homepage.spec.ts sw.js
git commit -m "fix(tests): update title regex to /MyO/ and bump sw cache to v3"
```

---

### Task 4: 驗證生成器常數一致性

**Files:**
- Verify: `scripts/optimize_blog_head.py`（Task 2 已由 Phase 1 自動改為 `alt="MyO! Logo"`）
- Verify: `scripts/add_pwa_tags.py`、`scripts/add_org_schema_to_articles.py`、`add_sticky_bar.py`

**Interfaces:**
- Consumes: Task 2 完成後的 HTML 與腳本
- Produces: 確認生成器不會還原舊名的證據

- [ ] **Step 1: 執行 spec 閘門 4 的比對指令**

**不得使用 `--dry-run` 的修改檔數作為判斷依據**——最佳化早已套用完畢，`FOOTER_LOGO` 對現有 HTML 的匹配數為 0，該判斷條件必然誤判。

Run:
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
Expected: 輸出 `常數: MyO! Logo / HTML 命中: 421`，exit code 0

- [ ] **Step 2: 確認 FOOTER_LOGO 正則本身也已更新**

Run: `grep -n 'MyO! Logo\|My O! Logo' scripts/optimize_blog_head.py`
Expected: 只出現 `MyO! Logo`（Phase 1 錨點 #1 會同時命中正則與 replacement 兩處）

- [ ] **Step 3: 確認其餘生成器無舊名**

Run:
```bash
grep -n 'My O' scripts/*.py add_sticky_bar.py fix_json_ld_and_table.py fix_medium_issues.py || echo "乾淨"
```
Expected: 輸出 `乾淨`

- [ ] **Step 4: 確認優化腳本可正常執行且無錯誤**

Run: `python3 scripts/optimize_blog_head.py --dry-run`
Expected: exit 0，輸出 `Would modify 0 of 421 files`（最佳化已套用，0 為正確結果，非失效）

---

### Task 5: 最終驗證與抽樣

**Files:**
- Verify: 全站

**Interfaces:**
- Consumes: Task 1–4 全部完成
- Produces: 五道閘門的通過證據

- [ ] **Step 1: 執行閘門 2 計數守恆複驗**

Run: `python3 scripts/rename_brand.py --test`
Expected: `My O! 初始總數: 0`、Phase 1/2/3 皆為 0、守恆式 PASS（證明全部已處理且無二次改寫）

- [ ] **Step 2: 執行閘門 3 測試**

Run: `npm test`
Expected: PASS

- [ ] **Step 3: 執行閘門 5 手動抽樣**

Run:
```bash
for f in index.html poster.html poster-en.html privacy.html manifest.json; do
  echo "--- $f ---"
  grep -oE '<title>[^<]*</title>|alt="MyO!? [Ll]ogo"|"short_name":[^,]*|"name": "MyO[^"]*"' "$f" | head -4
done
```
Expected 每個檔案：
- `<title>` 以 `MyO` 開頭（無驚嘆號）
- logo `alt` 為 `MyO! Logo`（有驚嘆號）
- JSON-LD `"name"` 為 `MyO 專屬結婚證書套`
- `manifest.json` 的 `short_name` 為 `MyO!`

- [ ] **Step 4: 抽樣一篇 blog 文章**

Run:
```bash
f=$(ls blog/*.html | head -1); echo "$f"
grep -oE '<title>[^<]*</title>|alt="MyO!? [Ll]ogo"|MyO 貼士[^<]*|MyO! 貼士[^<]*' "$f" | head -5
```
Expected: `<title>` 含 `MyO`；logo `alt` 為 `MyO! Logo`；內文為 `MyO 貼士`（無驚嘆號）

- [ ] **Step 5: 確認排除清單未被改動**

Run:
```bash
grep -c 'My O' docs/PageSpeed Insights.html docs/architecture-diagram.html
git diff --name-only | grep -c 'docs/superpowers/\|docs/PageSpeed\|docs/architecture-diagram\|image/' || echo "0 (未被改動)"
```
Expected: 第一行顯示非 0（舊名仍在，未被改動）；第二行顯示 `0 (未被改動)`

- [ ] **Step 6: 記錄教訓**

建立 `docs/lessons/brand-rename.md`，記錄兩個可復現陷阱：
- `optimize_blog_head.py` 的 `FOOTER_LOGO` 正則與 HTML 必須同步更新，且「修改檔數為 0」不能作為正則失效的判斷依據（最佳化已套用完畢）
- `blog_index.json` 必須重新生成，文字取代會被下次 `parse_blog.py` 覆蓋

```bash
git add docs/lessons/brand-rename.md
git commit -m "docs(lessons): record brand rename pitfalls"
```

- [ ] **Step 7: 最終 commit**

```bash
git status --short
git add -A
git commit -m "docs: complete My O! -> MyO brand rename"
```

---

## Self-Review

**1. Spec 覆蓋檢查**

| Spec 章節 | 對應任務 |
|---|---|
| 1.2 已確認決策 | Global Constraints |
| 2. 現況盤點（6,842 / 453） | Task 1 Step 5、Task 2 Step 1 |
| 3.1 Phase 1 六錨點（2,147） | Task 1 Step 1、3 |
| 3.1 Phase 2（4,695） | Task 1 Step 1、3 |
| 3.1 Phase 3（2 處） | Task 1 Step 1、3 |
| 3.2 不改寫的 MyO 變體 | Global Constraints（PostHog 專案名） |
| 4 Layer B 生成器 | Task 4 |
| 4 Layer C 產物 | Task 2 Step 2、Task 3 Step 3 |
| 4 Layer D 測試斷言 | Task 3 Step 1、2 |
| 4 Layer E 文件 | Task 2（自動處理） |
| 5 排除清單 | Task 1 Step 3 `EXCLUDE_DIRS` / `EXCLUDE_PATH_SUBSTR` |
| 6 執行順序 | Task 1 → 2 → 3 → 4 → 5 |
| 7 閘門 1 | Task 2 Step 3 |
| 7 閘門 2 | Task 1 Step 5、Task 5 Step 1 |
| 7 閘門 3 | Task 3 Step 4、Task 5 Step 2 |
| 7 閘門 4 | Task 4 Step 1 |
| 7 閘門 5 | Task 5 Step 3、4 |
| 8 已知後果 | 無需實作任務 |

無遺漏。

**2. Placeholder 掃描** — 無 TBD / TODO / 「類似 Task N」/ 未定義函式。`apply_phases`、`is_excluded`、`iter_targets` 皆在 Task 1 Step 3 定義並在後續任務使用。

**3. 型別一致性** — `apply_phases` 回傳 4-tuple `(str, int, int, int)`，Task 1 測試與 Task 5 Step 1 均依此解構。`is_excluded(rel_path: str) -> bool` 回傳純 bool，測試用 `is True` 嚴格比對。

**4. Review Focus 覆蓋**

| # | 覆蓋位置 |
|---|---|
| 1 | Task 1 `test_phase2_does_not_double_replace_phase1_output`、Task 4 Step 1 |
| 2 | Task 1 `test_blog_index_json_never_included`、Task 2 Step 2 |
| 3 | Task 3 Step 3 |
| 4 | Task 1 `test_is_excluded`（dist 路徑）、Global Constraints |
| 5 | Task 1 `test_is_excluded`（`Users/baba/...`） |
