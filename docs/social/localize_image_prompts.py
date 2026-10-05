import json
import time
import urllib.request

TOKEN = open('/Users/bubu/.local/share/opencode-v1/config/opencode/secrets/notion_token').read().strip()
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Notion-Version': '2022-06-28',
           'Content-Type': 'application/json'}

BPP = ("magazine editorial style, Noto Serif TC typography, dusty rose pink accent #B76E79, "
       "hot foil gold accent #D4AF37, deep cocoa brown #4A4540, warm off-white background #FAF8F5, "
       "large negative space, dual thin border frame, low saturation warm tones, "
       "minimalist East Asian wedding aesthetic, clean layout with generous white margins, "
       "refined wedding stationery and certificate imagery, soft diffused natural light")

SCENES = {
    1: "兩款證書套並排閉合放在暖色木桌上，柔和側光",
    2: "四款證書套排成 2x2 方格，前排米色亞麻布、後排藍色磨砂珠光，俯拍平鋪",
    3: "亞麻布紋理特寫，旁邊放磨砂珠光材質樣本，柔和自然光",
    4: "經典款與設計師款證書套並排，皆為燙金名字，極簡擺放",
    5: "A4 結婚證書放進米色亞麻布證書套內，旁邊標註尺寸線條，乾淨圖解排版",
    6: "燙金工藝特寫，金箔卷與加熱壓頭，手工工作檯環境",
    7: "簡潔資訊圖排版，註冊結婚步驟配上極簡圖示，柔和暖色調",
    8: "註冊結婚收費一覽卡，燙金點綴，極簡設計",
    9: "訂製流程時間軸資訊圖，五個清晰步驟配上圖示",
    10: "亞麻布證書套旁放一塊柔軟布巾與一張小型保養指南卡，暖色靜物",
    11: "兩款證書套並排，左為亞麻布燙金、右為藍色磨砂珠光燙銀",
    12: "中英文名字燙金排版展示，亞麻布底上呈現多種版面方案",
    13: "新舊兩代香港結婚證書並排陳列，呈現歷史演變",
    14: "絲絨證書套與亞麻布證書套平行擺放，兩種材質紋理柔和對比",
    15: "亞麻布證書套雅致陳列於現代書架上，旁邊放小盆栽與蠟燭",
    16: "五個保養貼士以優雅圖示排列於暖米白底上，金色點綴",
    17: "證書套禮盒包裝，繫上絲帶，柔和暖光，節日氛圍",
    18: "設計師款證書套打開平放於中性檯面，封面燙金客製字句",
    19: "證書套旁放小地球儀與護照，象徵跨境運送與國際訂購",
    20: "證書套放入紅色點綴的中式禮盒內，傳統與現代融合",
    21: "中式敬茶場景，證書套擺放於旁邊矮桌上，柔和暖色環境光",
    22: "傳統通勝書冊與燙金證書套並置，柔和環境光",
    23: "證書套擺放於中式漆盤上，旁邊有水果與利是，回門主題",
    24: "左右分割構圖，左側中式婚禮元素、右側西式元素，以暖色調統一",
    25: "簡潔極簡法律須知卡，附結婚註冊要求圖示，金色重點標示",
    26: "客人真實開箱照片拼貼，證書套打開露出燙金名字，溫暖隨性",
    27: "季節回顧版面，多款證書套優雅排成方格",
}

rows = json.load(open('docs/social/myo-content-27.json'))
pages = {c['id']: c['page_id'] for c in json.load(open('docs/social/myo-created-pages.json'))}

SIMP = set("个仪价优养吓场够张择晒来欧温环现确约纪统节议论评质辄顾领东开关无备复数时显")

for r in rows:
    new_scene = SCENES[r['id']]
    bad = sorted({c for c in new_scene if c in SIMP})
    assert not bad, f"id{r['id']} 場景描述含簡體字: {bad}"
    assert not any(c in new_scene for c in '①②③'), f"id{r['id']} 含列點符號"
    r['image_prompt'] = f"{BPP}, {new_scene}"

json.dump(rows, open('docs/social/myo-content-27.json', 'w'), ensure_ascii=False, indent=1)
print("本地 JSON 已更新\n")

ok, fail = 0, 0
for r in rows:
    body = {"properties": {"image_prompt": {"rich_text": [
        {"type": "text", "text": {"content": r['image_prompt']}}]}}}
    req = urllib.request.Request(f"https://api.notion.com/v1/pages/{pages[r['id']]}",
                                 data=json.dumps(body).encode('utf-8'),
                                 headers=HEADERS, method='PATCH')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            got = json.loads(resp.read())['properties']['image_prompt']['rich_text'][0]['plain_text']
            if got == r['image_prompt']:
                ok += 1
            else:
                fail += 1
                print(f"  id{r['id']} 回讀不一致")
    except Exception as e:
        fail += 1
        detail = e.read().decode('utf-8')[:150] if hasattr(e, 'read') else ''
        print(f"  id{r['id']} FAIL {e} {detail}")
    time.sleep(0.32)

print(f"Notion 更新：成功 {ok} / 失敗 {fail}")
