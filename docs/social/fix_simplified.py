import json
import re

PATH = 'docs/social/myo-content-27.json'
rows = json.load(open(PATH))

# 明確簡體 → 繁體 對照（已剔除繁簡同形字：划/估/俾/助/西/見）
MAP = {
    "个": "個", "仪": "儀", "价": "價", "优": "優", "养": "養",
    "吓": "嚇", "场": "場", "够": "夠", "张": "張", "择": "擇",
    "晒": "曬", "来": "來", "欧": "歐", "温": "溫", "环": "環",
    "现": "現", "确": "確", "约": "約", "纪": "紀", "统": "統",
    "节": "節", "议": "議", "论": "論", "评": "評", "质": "質",
    "辄": "輒", "过": "過", "选": "選", "顾": "顧", "领": "領",
}

# 需上下文判斷的詞組：只替換指定詞，不動其他同字
PHRASES = [
    ("制作", "製作"),   # 制度/限制/受制 保持不變
    ("保养", "保養"),
    ("确保", "確保"),
    ("建议", "建議"),
    ("质量", "品質"),
    ("环节", "環節"),
    ("选择", "選擇"),
    ("现代", "現代"),
    ("评价", "評價"),
    ("常见", "常見"),
    ("大约", "大約"),
    ("领取", "領取"),
    ("传统", "傳統"),
    ("北欧", "北歐"),
    ("越来越", "越來越"),
    ("纪念日", "紀念日"),
    ("请择日", "請擇日"),
    ("动辄", "動輒"),
    ("每年", "每年"),
]

FIELDS = ['Idea', 'ig_hook', 'ig_caption', 'threads_hook', 'threads_body']

changes = {}
for r in rows:
    for f in FIELDS:
        t = r[f]
        orig = t
        # 先做詞組替換（長詞優先，避免部分替換破壞正確用字）
        for a, b in PHRASES:
            if a in t:
                t = t.replace(a, b)
                changes.setdefault(f"{a}→{b}", 0)
                changes[f"{a}→{b}"] += t.count(b) - orig.count(b)
        # 再做單字替換
        for a, b in MAP.items():
            n = t.count(a)
            if n:
                t = t.replace(a, b)
                changes.setdefault(f"{a}→{b}", 0)
                changes[f"{a}→{b}"] += n
        r[f] = t

# 攝影用語修正：作品 → 產品（呢個品牌賣證書套，唔係攝影）
for r in rows:
    for f in FIELDS:
        if "作品" in r[f]:
            n = r[f].count("作品")
            r[f] = r[f].replace("作品", "產品")
            changes["作品→產品"] = changes.get("作品→產品", 0) + n

json.dump(rows, open(PATH, 'w'), ensure_ascii=False, indent=1)

print("已套用修正：")
for k, v in sorted(changes.items(), key=lambda x: -x[1]):
    print(f"  {k} × {v}")
print(f"\n共 {len(changes)} 類，{sum(changes.values())} 處")
