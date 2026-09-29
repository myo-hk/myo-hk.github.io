#!/usr/bin/env python3
"""
MyO 網站修復腳本 - JSON-LD 合併 + 表格無障礙
用法: python3 fix_json_ld_and_table.py [--test]
"""

import re
import json
import glob
from pathlib import Path

BLOG_DIR = Path(__file__).parent / "blog"
REPORT_FILE = Path(__file__).parent / "fix_report.json"

def get_faq_count(content):
    """計算 FAQPage 中的問題數量"""
    try:
        data = json.loads(content.strip())
        if data.get('@type') == 'FAQPage':
            return len(data.get('mainEntity', []))
    except (json.JSONDecodeError, AttributeError):
        pass
    return 0

def merge_json_ld(html):
    """合併重複的 JSON-LD"""
    # 找出所有 <script type="application/ld+json"> 區塊
    pattern = r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'

    # 使用 finditer 來獲取位置
    matches = list(re.finditer(pattern, html, re.DOTALL))

    if len(matches) <= 1:
        return html, 0

    # 分析每個區塊
    faq_blocks = []
    for i, match in enumerate(matches):
        content = match.group(1)
        count = get_faq_count(content)
        if count > 0:
            faq_blocks.append({
                'index': i,
                'start': match.start(),
                'end': match.end(),
                'content': content,
                'count': count
            })

    # 如果只有一個或沒有 FAQPage，不需要合併
    if len(faq_blocks) <= 1:
        return html, 0

    # 按問題數量排序，保留最多的
    faq_blocks.sort(key=lambda x: x['count'], reverse=True)

    # 構建新 HTML
    new_html = html

    # 刪除多餘的 FAQPage (從後往前刪，避免索引偏移)
    for block in faq_blocks[1:]:
        new_html = new_html[:block['start']] + new_html[block['end']:]

    return new_html, len(faq_blocks) - 1

def add_table_scope(html):
    """為表格 th 添加 scope='col'"""
    # 找所有 <th> 標籤
    def replace_th(match):
        tag = match.group(0)
        if 'scope=' in tag:
            return tag
        return tag.replace('>', ' scope="col">')

    return re.sub(r'<th[^>]*>', replace_th, html)

def process_file(filepath):
    """處理單個 HTML 檔案"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        original = html

        # 1. 合併 JSON-LD
        html, merged = merge_json_ld(html)

        # 2. 添加表格 scope
        html = add_table_scope(html)

        # 寫回
        if html != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

        return {
            'file': filepath.name,
            'status': 'success',
            'merged': merged,
            'table_fixed': 'scope="col"' in html
        }

    except Exception as e:
        return {
            'file': filepath.name,
            'status': 'failed',
            'error': str(e)
        }

def main(test_mode=False):
    """主函數"""
    html_files = sorted(glob.glob(str(BLOG_DIR / "*.html")))
    html_files = [f for f in html_files if 'index.html' not in f]

    print(f"找到 {len(html_files)} 篇文章")

    results = []

    if test_mode:
        html_files = html_files[:5]
        print(f"測試模式：處理 {len(html_files)} 篇")

    for filepath in html_files:
        result = process_file(Path(filepath))
        results.append(result)

        status = "✓" if result['status'] == 'success' else "✗"
        merged_info = f" 合併:{result['merged']}" if result['merged'] > 0 else ""
        print(f"{status} {result['file']}{merged_info}")

    # 報告
    report = {
        "total": len(results),
        "success": sum(1 for r in results if r['status'] == 'success'),
        "failed": sum(1 for r in results if r['status'] == 'failed'),
        "total_merged": sum(r.get('merged', 0) for r in results),
        "table_fixed_count": sum(1 for r in results if r.get('table_fixed'))
    }

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n=== 完成 ===")
    print(f"成功: {report['success']}, 失敗: {report['failed']}")
    print(f"JSON-LD 合併: {report['total_merged']}")
    print(f"表格修復: {report['table_fixed_count']}")

if __name__ == "__main__":
    import sys
    main(test_mode='--test' in sys.argv)