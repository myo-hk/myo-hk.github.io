import json
import urllib.request

TOKEN = open('/Users/bubu/.local/share/opencode-v1/config/opencode/secrets/notion_token').read().strip()
DB = 'e466ee9a-fad2-83d7-80a2-8171ac6b0f8b'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json',
}

# 只收「繁體有明確不同寫法」的簡體字。
# 已剔除繁簡同形 / 港式正字：西 划 制 助 估 俾 干 只 冲 面 里 台 后 系 杆 斗 周 見
SIMP = set(
    "个仪价优养吓场够张择晒来欧温环现确约纪统节议论评质辄顾领"
    "买卖东西开关无处备复数时显阳阴队阶际陆陈岁广庆库应废击则刚创删荐换据"
    "宁岛币纸纯细终绍经结给继续维缩网罗义习联职脑舰艺药蓝虑虽补装观规视览觉"
    "订让训记讲许论诊词译试诗诚话询该详误说读课调谅谈谋谜谢证识谱贝贞负贡"
    "财责贤败货贩贪贫购贯贱贴贵贷贸贺贼贾贿赁资赋赌赏赔赚赛赞赠赢赵赶趋跃践踪"
    "车轨转轮软轰轻载较辅辆辈辉输边达迁运还进远违连迟适选逊递逻遗邮邻郑酝释"
    "钟钢铁银铜铝销锁镜闭问闲间闷闻阀阁阅韩页顶项顺须顽顿颁颂预领颇颈频颗题颜额"
    "风飘飞饥饭饮饱饰饼馆驾验骑鱼鸟鸡鸣鹅麦黄齐齿龄龙龚龟业丛东丝丢两严丧临举义乌"
    "乐乔乡书乱争亏云仅仑仓们众伙会伟传伤伦伪体佣侠侣侥侦侧侨债倾偿储儿兑党兰关兴"
    "兽内冈册写军农冯冲决况冻凄凉凛几凤凭凯击凿刘剑剥剧劝办务动励劲劳势匀区医华协"
    "单卖卢卤卧卫却厂厅历厉压厌厕厢厦厨县参双发变叙叠叶号叹吁后吕吗吨听启吴呕员"
    "呛呜咏咙响哑哗唤啧啬喷团园围国图圆圣场坏块坚坛坝坞坟坠垒垦垫墙壮声壳壶处头夸"
    "夹夺奋奖妆妇妈娄娇娱婴婶孙学宝实宠审宪宫宽宾对寻导寿将尔尘尧尴尸尽层届属屡屿"
    "岂岖岗岛岭岳峡峥峦巅巩币帅师帐帘帜带帧帮幂并庄庆庐庙庞废开异弃弥弯弹强归当"
    "录彻径忆忧怀态怜总恋恳恶恼悦悬惊惧惨惩惫惯愤愿懒戏战户扑执扩扫扬扰抚抛抠抢护"
    "报担拟拢拣拥拦拧拨挂挚挠挡挣挤挥捞损捡捣掷掸掺揽搀搁搂搅携摄摆摇摊撑擞攒敌敛斋"
    "斗斩断旧旷晋晓晕暂术朴机杀杂权条杨极构枢枣枪枫柜标栈栋栏树栖样档桥桦桨桩梦检楼"
    "椭欢欧歼残殴毁毕毡气氢汇汉汤沟没沥沦沧沪泪泷泻泼泽洁洒洼浅浆浇浊测济浏浑浓涂涌"
    "涛涡涣涤润涧涨涩淀渊渍渎渐渔渗温湾湿溃滚滞满滤滥滨滩潜澜濒灭灯灵灾灿炉点炼炽烁"
    "烂烛烟烦烧烫烬热爱爷牵状犹独狭狮狱猎猪猫献玛环玺珑瑶璃璎瓯电画畅疗疟疡疮疯痒痪"
    "痴瘫皱盏盐监盖盗盘着睁瞒瞩矫矶矿码砖砚础硅硕碍碱礼祸禄禅离秃秆种积称秽稳穷窃窍"
    "窑窜窝窥窦竖竞笋笔笕笺笼筑筛签简箩箫篮篱籁类粪粮紧纠红纤级纫纬纯纱纲纳纵纶纷纸"
    "纹纺纽线练组绅细织终绎经绑绒结绕绘给绚络绝绞绢绣继绩绪续绮绳维绵综绽绿缀缄缅缆"
    "缉缎缓缔缕编缘缚缝缠缤缩缪缴罗罚罢羁羟翘耸耻聂聋职聪肃肠肤肿胀胁胆胜胧脉胶脏脐"
    "脑脓脚脱脸腊腌腻腾舆舰舱艰艳节芜苇苍苏苹茎荐荚荡荣荤药莲获莹莺萝萤营萧蒋蓝蓟蔷"
    "蔼蕴虏虑虚虽虾蚁蚂蚕蛊蛮蜡蝇蝉衅衔补衬袄袜袭装裤褛"
)

TEXT_FIELDS = ['Idea', 'ig_hook', 'ig_caption', 'threads_hook', 'threads_body', 'image_prompt']

# SIMP 由簡體「詞組」串接而成，故夾帶了繁簡同形的單字（东西→西、划船→划、制度→制）。
# 這些字單獨使用時繁體寫法相同，若不剔除會把正確繁體誤判為殘留並被「修正」而損毀內容。
SAME_IN_BOTH = set('西划制助估俾见周干只冲面里台后系杆斗')

SIMP -= SAME_IN_BOTH


def txt(p, k):
    """title 屬性用 title 陣列，其餘用 rich_text 陣列。"""
    prop = p.get(k, {})
    arr = prop.get('title') if prop.get('type') == 'title' else prop.get('rich_text')
    arr = arr or []
    return arr[0].get('plain_text', '') if arr else ''


req = urllib.request.Request(
    f'https://api.notion.com/v1/databases/{DB}/query',
    data=json.dumps({"page_size": 100}).encode(),
    headers=HEADERS, method='POST')
rows = json.loads(urllib.request.urlopen(req, timeout=30).read())['results']
rows.sort(key=lambda r: r['properties']['id']['number'])

results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))


check("列數 = 27", len(rows) == 27, f"實際 {len(rows)}")

ids = [r['properties']['id']['number'] for r in rows]
check("id 1–27 無重複無遺漏", sorted(ids) == list(range(1, 28)), f"{sorted(ids)}")

miss = []
for r in rows:
    p = r['properties']
    n = p['id']['number']
    for k in TEXT_FIELDS:
        if not txt(p, k).strip():
            miss.append(f"id{n}.{k}")
    if not p['cta_url'].get('url'):
        miss.append(f"id{n}.cta_url")
    if not p['social_pillar'].get('multi_select'):
        miss.append(f"id{n}.social_pillar")
    if not p['content_dimensions'].get('multi_select'):
        miss.append(f"id{n}.content_dimensions")
check("欄位完整性（Idea + 5 文案 + url + 2 標籤）", not miss, str(miss[:6]))

blob = json.dumps(rows, ensure_ascii=False)
TEA = ['普洱', '烏龍', '綠茶', '白茶', '蓋碗', '紫砂', '奶茶', 'teawiki']
tea = [w for w in TEA if w in blob]
check("茶品牌殘留", not tea, str(tea))

simp = sorted({c for c in blob if c in SIMP})
check("簡體字殘留", not simp, ''.join(simp))

pho = [w for w in ['攝影', '婚攝', '作品'] if w in blob]
check("攝影用語殘留", not pho, str(pho))

STYLE_TAIL = '（風格沿用品牌手冊 BPP：雜誌編輯風、玫瑰粉 #B76E79 襯燙金 #D4AF37、暖米白底、大留白）'
body_ok = sum(1 for r in rows if txt(r['properties'], 'image_prompt').endswith(STYLE_TAIL))
check("image_prompt 保留一行風格指引", body_ok == 27, f"{body_ok}/27")

no_bpp = sum(1 for r in rows
             if 'magazine editorial style' in txt(r['properties'], 'image_prompt'))
check("image_prompt 已移除 BPP 全文（內容導向）", no_bpp == 0, f"仍有 {no_bpp} 列含 BPP 原文")

myo = sum(1 for r in rows
          if 'myo-makeyourown.pages.dev' in (r['properties']['cta_url'].get('url') or ''))
check("cta_url 指向 MyO 網域", myo == 27, f"{myo}/27")

st = {}
for r in rows:
    s = r['properties']['Status']['status']['name']
    st[s] = st.get(s, 0) + 1
check("Status 全部 AI Drafted", list(st) == ['AI Drafted'], str(st))

nolink = sum(1 for r in rows if 'http' not in txt(r['properties'], 'threads_body'))
check("threads_body 無連結（變形規則）", nolink == 27, f"{nolink}/27")

bullet = sum(1 for r in rows
             if any(c in txt(r['properties'], 'threads_body') for c in '①②③•・‣'))
check("threads_body 無列點符號（變形規則）", bullet == 0, f"違例 {bullet}")

nohash = sum(1 for r in rows if '#' in txt(r['properties'], 'ig_caption'))
check("ig_caption 有 hashtag", nohash == 27, f"{nohash}/27")

print("=" * 60)
print("MyO Notion 內容庫最終驗證")
print("=" * 60)
for name, ok, detail in results:
    line = f"  {'PASS' if ok else 'FAIL'}  {name}"
    if detail and not ok:
        line += f"\n         → {detail}"
    print(line)
passed = sum(1 for _, ok, _ in results if ok)
print(f"\n  {passed}/{len(results)} 項通過")

print("\n格式原型分佈（social_pillar）：")
pil = {}
for r in rows:
    for d in r['properties']['social_pillar']['multi_select']:
        pil[d['name']] = pil.get(d['name'], 0) + 1
for k, v in sorted(pil.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print("\n主題標籤分佈（content_dimensions）：")
dims = {}
for r in rows:
    for d in r['properties']['content_dimensions']['multi_select']:
        dims[d['name']] = dims.get(d['name'], 0) + 1
for k, v in sorted(dims.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print("\n各月內容數：")
m1 = sum(1 for r in rows if r['properties']['id']['number'] <= 10)
m2 = sum(1 for r in rows if 11 <= r['properties']['id']['number'] <= 19)
m3 = sum(1 for r in rows if r['properties']['id']['number'] >= 20)
print(f"  M1 破冰探索: {m1} 條")
print(f"  M2 工藝深度: {m2} 條")
print(f"  M3 本地文化: {m3} 條")
