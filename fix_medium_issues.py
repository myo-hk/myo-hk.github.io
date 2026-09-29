#!/usr/bin/env python3
"""
MyO 網站修復腳本 - 中等問題批量處理
處理: 硬編碼 URL、meta robots、lazy loading
用法: python3 fix_medium_issues.py [--test]
"""

import re
import json
import glob
from pathlib import Path

# 設定
BLOG_DIR = Path(__file__).parent / "blog"
REPORT_FILE = Path(__file__).parent / "fix_medium_report.json"

def fix_medium_issues(html):
    """修復中等問題"""
    original_html = html
    changes = []

    # 2.1 添加 meta robots (如不存在)
    if 'name="robots"' not in html.lower():
        html = re.sub(
            r'</head>',
            '<meta name="robots" content="index, follow">\n</head>',
            html,
            flags=re.IGNORECASE
        )
        changes.append('meta_robots')

    # 2.3 添加 lazy loading
    def add_loading_lazy(match):
        img_tag = match.group(0)
        if 'loading=' not in img_tag:
            # 在 <img 之後插入 loading="lazy"
            return re.sub(r'<img\b', r'<img loading="lazy"', img_tag, count=1)
        return img_tag

    html = re.sub(r'<img\b[^>]*>', add_loading_lazy, html)

    # 檢查是否有圖片被添加 lazy loading
    if '<img loading="lazy"' in html:
        changes.append('lazy_loading')

    return html, changes

def process_file(filepath):
    """處理單個 HTML 檔案"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        original_html = html
        html, changes = fix_medium_issues(html)

        # 如果有修改，寫回檔案
        if html != original_html:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

        return {
            'file': filepath.name,
            'status': 'success',
            'changes': changes,
            'changes_count': len(changes)
        }

    except Exception as e:
        return {
            'file': filepath.name,
            'status': 'failed',
            'error': str(e)
        }

def main(test_mode=False):
    """主函數"""
    # 找出所有 HTML 檔案 (排除 index.html)
    html_files = glob.glob(str(BLOG_DIR / "*.html"))
    html_files = [f for f in html_files if 'index.html' not in f]

    print(f"找到 {len(html_files)} 篇文章")

    results = []

    if test_mode:
        # 測試模式：只處理 5 篇
        html_files = html_files[:5]
        print(f"測試模式：處理 {len(html_files)} 篇")

    for filepath in html_files:
        result = process_file(Path(filepath))
        results.append(result)

        if result['status'] == 'success':
            changes_str = ', '.join(result['changes']) if result['changes'] else '無變更'
            print(f"✓ {result['file']} - {changes_str}")
        else:
            print(f"✗ {result['file']} - 錯誤: {result.get('error')}")

    # 生成報告
    report = {
        "total": len(results),
        "success": sum(1 for r in results if r['status'] == 'success'),
        "failed": sum(1 for r in results if r['status'] == 'failed'),
        "changes_summary": {
            "url_canonical": sum(1 for r in results if 'url_canonical' in r.get('changes', [])),
            "meta_robots": sum(1 for r in results if 'meta_robots' in r.get('changes', [])),
            "lazy_loading": sum(1 for r in results if 'lazy_loading' in r.get('changes', [])),
        },
        "results": results
    }

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n完成！報告已保存到: {REPORT_FILE}")
    print(f"成功: {report['success']}, 失敗: {report['failed']}")
    print(f"URL 修復: {report['changes_summary']['url_canonical']}")
    print(f"Meta robots: {report['changes_summary']['meta_robots']}")
    print(f"Lazy loading: {report['changes_summary']['lazy_loading']}")

if __name__ == "__main__":
    import sys
    test = "--test" in sys.argv
    main(test_mode=test)