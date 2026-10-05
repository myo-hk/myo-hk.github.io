#!/usr/bin/env python3
"""
Add HowTo schema to tutorial blog articles that have step-by-step content.
Usage: python3 scripts/add_howto_schema.py [--test]
"""
import re
import json
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

# Target articles with step-by-step tutorial content
TARGET_ARTICLES = [
    "結婚註冊流程教學.html",
    "婚前準備清單.html",
    "婚禮籌備時間表.html",
    "婚禮當天時間表.html",
    "過大禮清單.html",
    "敬茶儀式流程.html",
    "安床習俗與禁忌.html",
    "結婚證書尺寸規格.html",
    "證書套保養指南.html",
    "結婚註冊指南.html",
]

# HowTo definition template for each article
HOWTO_TEMPLATES = {
    "結婚註冊流程教學.html": {
        "name": "香港結婚註冊流程",
        "description": "在香港註冊結婚的完整步驟，從預約到領證。",
        "steps": [
            "遞交擬結婚通知書（婚姻登記處或律師樓）",
            "繳交費用及預約註冊日期",
            "選擇婚禮場地（婚姻登記處／特許場所）",
            "安排證婚人（律師或婚姻監禮人）",
            "在預約日期舉行婚禮儀式",
            "簽署結婚證書並領取副本"
        ]
    },
    "婚前準備清單.html": {
        "name": "婚前準備清單",
        "description": "香港新人婚前必須準備的物品和文件。",
        "steps": [
            "準備身份證明文件（身份證、護照）",
            "預約婚姻登記",
            "確認婚禮場地及日期",
            "選購結婚戒指",
            "安排婚紗禮服",
            "預訂婚禮攝影師及化妝師"
        ]
    },
    "婚禮籌備時間表.html": {
        "name": "婚禮籌備時間表",
        "description": "從求婚到婚禮當日的完整籌備時間規劃。",
        "steps": [
            "12個月前：確定預算及日期",
            "10個月前：預訂場地及攝影師",
            "8個月前：選擇婚紗禮服",
            "6個月前：發送邀請函",
            "3個月前：確認菜單及座位表",
            "1個月前：試菜及最終確認"
        ]
    },
    "婚禮當天時間表.html": {
        "name": "婚禮當天時間表",
        "description": "香港婚禮當日的典型流程與時間安排。",
        "steps": [
            "早上6時：新娘化妝及造型",
            "早上8時：新郎準備",
            "早上10時：接新娘遊戲",
            "中午12時：註冊儀式",
            "下午2時：婚宴午餐",
            "下午5時：戶外拍攝",
            "晚上7時：晚宴開始"
        ]
    },
    "過大禮清單.html": {
        "name": "過大禮所需物品清單",
        "description": "中式傳統過大禮儀式所需的物品和數量。",
        "steps": [
            "準備禮金及禮餅（龍鳳餅、唐餅）",
            "安排海味（乾鮑、花膠、元貝等）",
            "準備水果（椰子、檳榔等吉祥水果）",
            "購買中式禮盒（龍鳳燭、對聯）",
            "準備金器（龍鳳鐲、戒指）",
            "安排媒人陪同送禮"
        ]
    },
    "敬茶儀式流程.html": {
        "name": "香港婚禮敬茶儀式流程",
        "description": "傳統中式婚禮敬茶儀式的完整步驟與禮儀。",
        "steps": [
            "準備敬茶用具（茶壺、茶杯、托盤）",
            "鋪設跪墊（新人跪拜用）",
            "先敬父母（新郎父母先飲茶）",
            "逐一長輩敬茶（按輩分順序）",
            "長輩回禮（利是或金器）",
            "新人互敬（夫妻對拜）"
        ]
    },
    "安床習俗與禁忌.html": {
        "name": "安床習俗與禁忌",
        "description": "中式婚禮安床儀式的正確做法與注意事項。",
        "steps": [
            "選擇吉日吉時進行安床",
            "由好命婆（福氣婦女）負責鋪床",
            "在床上放置龍鳳被及紅棗蓮子",
            "安排小男孩在床上滾動（旺丁）",
            "安床後不宜移動床具",
            "婚禮前不可讓人坐臥新床"
        ]
    },
    "結婚證書尺寸規格.html": {
        "name": "結婚證書尺寸規格查詢",
        "description": "香港結婚證書的標準尺寸和規格說明。",
        "steps": [
            "確認香港結婚證書標準尺寸（210mm × 297mm A4）",
            "選購適合的結婚證書套",
            "選擇證書套材質（亞麻布或磨砂珠光）",
            "提供新人名字和結婚日期進行燙印",
            "確認設計稿後製作（7-14個工作天）"
        ]
    },
    "證書套保養指南.html": {
        "name": "結婚證書套保養方法",
        "description": "亞麻布和磨砂珠光結婚證書套的正確保養方法。",
        "steps": [
            "避免陽光直射（防止褪色）",
            "保持乾燥環境（避免潮濕發霉）",
            "定期用軟布輕拭表面灰塵",
            "避免與尖銳物品接觸（防止刮花）",
            "存放時放入防潮箱或通風處",
            "燙印部分避免用力擦拭"
        ]
    },
    "結婚註冊指南.html": {
        "name": "香港結婚註冊指南",
        "description": "香港註冊結婚的完整流程、文件及費用說明。",
        "steps": [
            "查閱結婚資格（年齡、婚姻狀況）",
            "準備所需文件（身份證、住址證明）",
            "預約婚姻登記處",
            "遞交擬結婚通知書",
            "繳交註冊費用",
            "選擇婚姻監禮人",
            "在預定日期舉行婚禮"
        ]
    }
}

def build_howto_json(filename, steps):
    """Build HowTo JSON-LD."""
    tmpl = HOWTO_TEMPLATES[filename]
    step_list = []
    for i, step_text in enumerate(steps):
        step_list.append({
            "@type": "HowToStep",
            "position": i + 1,
            "name": step_text.split("：")[0] if "：" in step_text else step_text[:20],
            "text": step_text
        })
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": tmpl["name"],
        "description": tmpl["description"],
        "step": step_list
    }

def main():
    test_mode = "--test" in sys.argv
    changed = 0

    for fname in TARGET_ARTICLES:
        fpath = BLOG_DIR / fname
        if not fpath.exists():
            print(f"  SKIP {fname}: file not found")
            continue

        content = fpath.read_text(encoding="utf-8")
        howto_json = build_howto_json(fname, HOWTO_TEMPLATES[fname]["steps"])

        # Insert HowTo schema before </head>
        script_tag = f'\n<script type="application/ld+json">\n{json.dumps(howto_json, ensure_ascii=False, indent=2)}\n</script>\n'
        new_content = content.replace("</head>", script_tag + "</head>", 1)

        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ {fname}: HowTo schema added")
            changed += 1
        else:
            print(f"  ? {fname}: no change (unexpected)")

    print(f"\nDone: {changed} articles updated")

if __name__ == "__main__":
    main()
