import json
import urllib.request

TOKEN = open('/Users/bubu/.local/share/opencode-v1/config/opencode/secrets/notion_token').read().strip()
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json',
}

rows = {r['id']: r for r in json.load(open('docs/social/myo-content-27.json'))}
pages = {c['id']: c['page_id'] for c in json.load(open('docs/social/myo-created-pages.json'))}

for i in (16, 27):
    txt = rows[i]['image_prompt']
    body = {"properties": {"image_prompt": {"rich_text": [{"type": "text", "text": {"content": txt}}]}}}
    req = urllib.request.Request(f"https://api.notion.com/v1/pages/{pages[i]}",
                                 data=json.dumps(body).encode('utf-8'),
                                 headers=HEADERS, method='PATCH')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            d = json.loads(resp.read())
            got = d['properties']['image_prompt']['rich_text'][0]['plain_text']
            ok = got == txt
            print(f"  id{i} HTTP {resp.status}  回讀一致: {'YES' if ok else 'NO'}")
            if not ok:
                print(f"    預期: {txt[:90]}")
                print(f"    實際: {got[:90]}")
    except Exception as e:
        detail = e.read().decode('utf-8')[:200] if hasattr(e, 'read') else ''
        print(f"  id{i} FAIL {e}  {detail}")
