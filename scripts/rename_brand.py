#!/usr/bin/env python3
"""
品牌更名 My O! -> MyO。

三階段有序取代：
  Phase 1  視覺 wordmark / logo 上下文 -> MyO!  （保留驚嘆號）
  Phase 2  其餘全部                     -> MyO   （去驚嘆號）
  Phase 3  大小寫變體 MYO證書套         -> MyO 證書套

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
    # 記錄本次更名陷阱的教訓文件：必須引用舊字串（如 PHASE2 regex 的退化原文）
    # 才能說明陷阱，與 docs/superpowers/ 同屬「保留當時原文」的歷史紀錄類別
    'docs/lessons/brand-rename.md',
    # 取代工具自身：這兩檔自含 `My O!` 字面。若不排除，Phase 2 會把本檔的
    # PHASE2 regex 從 `My O!` 改寫成 `MyO`（變成 no-op），且測試的
    # src / expected 會同步崩壞。兩檔為工具，非品牌內容。
    'scripts/rename_brand.py',
    'scripts/test_rename_brand.py',
    # 執行期暫存：ledger / brief / review package 含品牌字面討論，非專案內容
    '.superpowers/',
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

# Phase 3：全大寫變體（消耗整個 MYO證書套，產出含空格的 MyO 證書套）
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
