#!/usr/bin/env python3
"""
Extend short blog article <title> tags to be more SEO-friendly.
Target length: 20-35 Chinese characters (equivalent to 50-60 English chars for SEO).
Titles that are already >= 20 Chinese chars are left unchanged.
Usage: python3 scripts/fix_blog_titles.py [--test]
"""

import re
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

# Mapping of known short titles → extended versions
TITLE_EXTENSIONS: dict[str, str] = {
    "2026 香港結婚完整攻略": "2026香港結婚完整攻略：註冊流程、婚宴籌備與習俗全指南",
    "2026 婚禮攝影價錢比較": "2026婚禮攝影價錢比較：10間人氣攝影師套餐與收費標準",
    "婚禮場地選擇指南：完美場地秘訣": "婚禮場地選擇指南：酒店酒樓教堂戶外場地完整比較秘訣",
    "回門習俗介紹：傳統與現代做法": "回門習俗完整指南：傳統三朝回門日期禮品與現代簡化做法",
    "婚後生活適應指南：從單身到已婚": "婚後生活適應指南：溝通家務財務與長輩相處的新婚秘訣",
    "婚禮攝影價錢比較": "婚禮攝影價錢比較：香港最新收費標準與套餐選擇攻略",
}


def count_chinese_chars(title: str) -> int:
    """Count Chinese characters in a string."""
    return len(re.findall(r"[\u4e00-\u9fff]", title))


def extend_title(match: re.Match[str]) -> str:
    current_title = match.group(1)

    # If title already long enough (>= 20 Chinese chars), skip
    if count_chinese_chars(current_title) >= 20:
        return match.group(0)

    # Check explicit mapping
    if current_title in TITLE_EXTENSIONS:
        new_title = TITLE_EXTENSIONS[current_title]
        return f"<title>{new_title}</title>"

    # Heuristic: extend based on ending keyword.
    # Uses different extensions depending on whether the title already has a colon.
    heuristic_no_colon: dict[str, str] = {
        "指南": "：香港結婚必讀完整攻略與實用大全",
        "比較": "：詳細比較分析與選購建議完整攻略",
        "推薦": "：最新推薦排行榜與人氣選擇完整攻略",
        "介紹": "：傳統習俗與現代做法及禁忌全攻略",
        "教學": "：詳細步驟流程教學與實用貼士大全",
        "選擇": "：人氣選擇要點與購買實用完整攻略",
        "清單": "：最新完整清單與準備攻略實用大全",
        "貼士": "：實用貼士與注意事項總整理完整大全",
        "規劃": "：詳細規劃指南與實用建議完整大全",
        "創意": "：最新創意靈感與設計實用完整攻略",
        "秘訣": "：香港結婚必讀秘訣與實用大全",
        "趨勢": "：香港結婚最新趨勢與推薦大全",
        "靈感": "：創意靈感與設計實用大全",
        "事項": "：完整事項清單與必讀大全",
        "做法": "：傳統與現代做法完整指南",
        "必讀": "：新婚必讀與實用技巧大全",
    }
    heuristic_colon: dict[str, str] = {
        "指南": "，必讀完整攻略與實用技巧",
        "比較": "，詳細分析與選購建議指南",
        "推薦": "，最新推薦排行榜與選擇攻略",
        "介紹": "，傳統習俗與現代做法全攻略",
        "教學": "，詳細步驟教學與實用貼士",
        "選擇": "，人氣選擇要點與購買攻略",
        "清單": "，完整清單與準備攻略大全",
        "貼士": "，實用貼士與注意事項總整理",
        "規劃": "，詳細規劃指南與實用建議",
        "創意": "，最新創意靈感與設計攻略",
        "秘訣": "，香港結婚必讀秘訣與實用大全",
        "趨勢": "，香港結婚最新趨勢與推薦大全",
        "靈感": "，創意靈感與設計實用大全",
        "事項": "，完整事項清單與必讀大全",
        "做法": "，傳統與現代做法完整指南",
                "必讀": "，新婚必讀與實用技巧大全",
    }

    for suffix in heuristic_no_colon:
        if not current_title.endswith(suffix):
            continue
        if "：" in current_title:
            new_title = current_title + heuristic_colon[suffix]
        else:
            new_title = current_title + heuristic_no_colon[suffix]
        if len(new_title) > 50:
            continue
        return f"<title>{new_title}</title>"

    # Generic fallback for all other short titles
    if "：" in current_title:
        new_title = current_title + "，結婚必讀完整攻略與實用大全"
    else:
        new_title = current_title + "：結婚必讀完整攻略與實用大全"
    if len(new_title) <= 50:
        return f"<title>{new_title}</title>"

    return match.group(0)





def main() -> None:
    test_mode = "--test" in sys.argv
    files = sorted(BLOG_DIR.glob("*.html"))
    changed = 0
    skipped = 0

    title_pattern = re.compile(r"<title>(.*?)</title>")

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")

        match = title_pattern.search(content)
        if not match:
            skipped += 1
            continue

        title = match.group(1)
        chinese_count = count_chinese_chars(title)

        # Only extend if short
        if chinese_count >= 20:
            skipped += 1
            continue

        new_content = title_pattern.sub(extend_title, content)

        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            new_match = title_pattern.search(new_content)
            new_title = new_match.group(1) if new_match else "???"
            new_count = count_chinese_chars(new_title)
            marker = "✓" if not test_mode else "○"
            print(
                f"  {marker} {fpath.name}: "
                f'"{title}" ({chinese_count} chars) → '
                f'"{new_title}" ({new_count} chars)'
            )
            changed += 1
        else:
            skipped += 1

    print(f"\nTotal: {changed} extended, {skipped} skipped (already long or no match)")


if __name__ == "__main__":
    main()