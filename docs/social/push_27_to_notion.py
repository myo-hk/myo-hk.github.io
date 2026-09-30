import json
import time
import urllib.request

TOKEN = open('/Users/bubu/.local/share/opencode-v1/config/opencode/secrets/notion_token').read().strip()
DS = '6226ee9a-fad2-83cf-a751-87af1eb87d26'
API = 'https://api.notion.com/v1'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json',
}

rows = json.load(open('docs/social/myo-content-27.json'))


def rt(text):
    return {"rich_text": [{"type": "text", "text": {"content": text[:1900]}}]}


def ms(names):
    return {"multi_select": [{"name": n} for n in names]}


created, failed = [], []

for r in rows:
    props = {
        "Idea": {"title": [{"type": "text", "text": {"content": r['Idea']}}]},
        "id": {"number": r['id']},
        "Status": {"status": {"name": r['Status']}},
        "social_pillar": ms(r['social_pillar']),
        "content_dimensions": ms(r['content_dimensions']),
        "ig_hook": rt(r['ig_hook']),
        "ig_caption": rt(r['ig_caption']),
        "threads_hook": rt(r['threads_hook']),
        "threads_body": rt(r['threads_body']),
        "image_prompt": rt(r['image_prompt']),
        "cta_url": {"url": r['cta_url']},
    }
    body = {
        "parent": {"type": "data_source_id", "data_source_id": DS},
        "properties": props,
    }
    req = urllib.request.Request(f"{API}/pages", data=json.dumps(body).encode('utf-8'),
                                 headers=HEADERS, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            created.append((r['id'], data['id']))
            print(f"  OK  id{r['id']:>2}  {r['Idea'][:34]}")
    except Exception as e:
        detail = ''
        if hasattr(e, 'read'):
            detail = e.read().decode('utf-8')[:200]
        failed.append((r['id'], str(e), detail))
        print(f"  FAIL id{r['id']:>2}  {e}  {detail}")
    time.sleep(0.35)

print(f"\n---- 建立成功 {len(created)} / 失敗 {len(failed)} ----")
json.dump([{'id': i, 'page_id': p} for i, p in created],
          open('docs/social/myo-created-pages.json', 'w'), indent=1)
if failed:
    print("失敗清單：")
    for f in failed:
        print("  ", f)
