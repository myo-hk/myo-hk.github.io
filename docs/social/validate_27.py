import json
import re

d = json.load(open('docs/social/myo-content-27.json'))
print(f"1. 物件數量: {len(d)}  {'PASS' if len(d) == 27 else 'FAIL'}")

SIMP = ["证书", "设计", "亚麻", "烫", "结婚", "注册", "对比", "镜头", "确认", "点解",
        "其实", "通过", "联络", "说明", "系统", "质量", "价格", "时间", "发现",
        "经历", "视频", "网络", "显", "变", "万", "银", "钟", "亚", "龙", "凤",
        "衬", "简", "类", "标", "签", "层", "严", "丽", "习", "东", "专"]
txt = json.dumps(d, ensure_ascii=False)
hits = sorted({s for s in SIMP if s in txt})
print(f"2. 簡體字: {hits if hits else '乾淨 PASS'}")

BULLETS = "①②③•・‣"
bad = [(r["id"], [c for c in r["threads_body"] if c in BULLETS]) for r in d]
bad = [x for x in bad if x[1]]
print(f"3. threads_body 列點符號: {bad if bad else '0 PASS'}")

url = [r["id"] for r in d if re.search(r"https?://|www\.", r["threads_body"])]
print(f"3b. threads_body 連結: {url if url else '0 PASS'}")

BPP_HEAD = ("magazine editorial style, Noto Serif TC typography, dusty rose pink accent #B76E79, "
            "hot foil gold accent #D4AF37, deep cocoa brown #4A4540, warm off-white background #FAF8F5, "
            "large negative space, dual thin border frame, low saturation warm tones, "
            "minimalist East Asian wedding aesthetic, clean layout with generous white margins, "
            "refined wedding stationery and certificate imagery, soft diffused natural light")
bad_bpp = [r["id"] for r in d if not r["image_prompt"].startswith(BPP_HEAD)]
print(f"4. BPP 逐字一致開頭: {'全部 27 PASS' if not bad_bpp else 'FAIL ' + str(bad_bpp)}")

PILLARS = {"知識型", "教學型", "對比型", "文化型", "互動型", "品牌型"}
DIMS = {"經典款", "設計師款", "亞麻布", "磨砂珠光", "燙印工藝",
        "註冊流程", "中式習俗", "保養知識", "送禮場景", "品牌故事"}
FMTS = {"Carousel", "Single", "Reels"}
KEYS = {"id", "Idea", "Status", "social_pillar", "content_dimensions", "format",
        "ig_hook", "ig_caption", "threads_hook", "threads_body", "image_prompt", "cta_url"}

errs = []
for r in d:
    i = r.get("id")
    if set(r.keys()) != KEYS:
        errs.append(f"id{i} keys差異={set(r.keys()) ^ KEYS}")
    if r.get("Status") != "AI Drafted":
        errs.append(f"id{i} Status={r.get('Status')}")
    if r.get("format") not in FMTS:
        errs.append(f"id{i} format={r.get('format')}")
    if not set(r.get("social_pillar", [])) <= PILLARS:
        errs.append(f"id{i} pillar={r.get('social_pillar')}")
    if not set(r.get("content_dimensions", [])) <= DIMS:
        errs.append(f"id{i} dim={r.get('content_dimensions')}")
    if not r.get("social_pillar") or not r.get("content_dimensions"):
        errs.append(f"id{i} 標籤為空")
    for f in ["Idea", "ig_hook", "ig_caption", "threads_hook", "threads_body",
              "image_prompt", "cta_url"]:
        if not str(r.get(f, "")).strip():
            errs.append(f"id{i} 空白欄位 {f}")
print(f"5. enum/欄位: {'全部合法 PASS' if not errs else 'FAIL ' + '; '.join(errs[:8])}")

ids = sorted(r["id"] for r in d)
print(f"6. id 1-27: {'PASS' if ids == list(range(1, 28)) else 'FAIL ' + str(ids)}")

ref = {x["id"]: x["cta_url"] for x in json.load(open('/tmp/myo_cta.json'))}
mism = [(r["id"], r.get("cta_url")) for r in d if ref.get(r["id"]) != r.get("cta_url")]
print(f"7. cta_url 對照: {'27/27 相符 PASS' if not mism else 'FAIL ' + str(mism[:3])}")

cap = [len(r["ig_caption"]) for r in d]
thd = [len(r["threads_body"]) for r in d]
print(f"8. ig_caption 字數 min={min(cap)} max={max(cap)}")
print(f"   threads_body 字數 min={min(thd)} max={max(thd)}")

nohash = [r["id"] for r in d if "#" not in r["ig_caption"]]
print(f"9. ig_caption 缺 hashtag: {nohash if nohash else '27/27 PASS'}")

nocta = [r["id"] for r in d if not re.search(r"WhatsApp|wa\.me|DM|私訊|留言|立即|查詢", r["ig_caption"])]
print(f"10. ig_caption 疑似缺 CTA: {nocta if nocta else '27/27 PASS'}")

noq = [r["id"] for r in d if "？" not in r["threads_body"][-30:]]
print(f"11. threads_body 末句非問句: {noq if noq else '27/27 PASS'}")

long_hook = [(r["id"], len(r["ig_hook"])) for r in d if len(r["ig_hook"]) > 22]
print(f"12. ig_hook 偏長(>22字): {long_hook if long_hook else '全部 PASS'}")
