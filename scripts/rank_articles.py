#!/usr/bin/env python3
"""
Rank blog articles by SEO value signals to identify top 20 for opening paragraph optimization.
"""
import re
import json
import os

BLOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'blog')

def score_article(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    score = 0
    signals = {}
    
    # 1. Has FAQPage schema (+2)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    has_faq = False
    for block in blocks:
        try:
            d = json.loads(block.strip())
            if d.get('@type') == 'FAQPage':
                has_faq = True
                break
        except:
            pass
    if has_faq:
        score += 2
        signals['faq'] = True
    
    # 2. Has BreadcrumbList (+1)
    has_breadcrumb = False
    for block in blocks:
        try:
            d = json.loads(block.strip())
            if d.get('@type') == 'BreadcrumbList':
                has_breadcrumb = True
                break
        except:
            pass
    if has_breadcrumb:
        score += 1
        signals['breadcrumb'] = True
    
    # 3. Title length (longer = more specific)
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else filename.replace('.html', '')
    title_len = len(title)
    if title_len >= 40:
        score += 2
        signals['long_title'] = True
    elif title_len >= 25:
        score += 1
        signals['medium_title'] = True
    
    # 4. Article body word count (longer = more valuable)
    body_match = re.search(r'<article>(.*?)</article>', content, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<div class="container.*?max-w-3xl">(.*?)</div>\s*</div>\s*<div class="sticky-conversion-bar', content, re.DOTALL)
    word_count = 0
    if body_match:
        text = re.sub(r'<[^>]+>', '', body_match.group(1))
        # Count Chinese characters and English words
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        word_count = chinese_chars + english_words
        if word_count >= 3000:
            score += 2
            signals['long_article'] = True
        elif word_count >= 2000:
            score += 1
            signals['medium_article'] = True
    
    # 5. Short / core filename (indicates core topic)
    name = filename.replace('.html', '')
    if len(name) <= 10:
        score += 1
        signals['short_name'] = True
    
    return {
        'filename': filename,
        'title': title,
        'score': score,
        'signals': signals,
        'word_count': word_count
    }

def main():
    results = []
    for fn in sorted(os.listdir(BLOG_DIR)):
        if not fn.endswith('.html'):
            continue
        filepath = os.path.join(BLOG_DIR, fn)
        result = score_article(filepath)
        results.append(result)
    
    # Sort by score descending
    results.sort(key=lambda r: (-r['score'], -r['word_count']))
    
    # Top 20
    top20 = []
    for i, r in enumerate(results[:20]):
        entry = {
            'rank': i + 1,
            'filename': r['filename'],
            'title': r['title'],
            'score': r['score'],
            'word_count': r['word_count'],
            'signals': r['signals']
        }
        top20.append(entry)
        print(f"#{i+1:2d} | Score: {r['score']} | WC: {r['word_count']:4d} | {r['filename']}")
        print(f"     Title: {r['title'][:80]}")
        print(f"     Signals: {', '.join(k for k, v in r['signals'].items() if v)}")
    
    # Save to file
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    with open(os.path.join(docs_dir, 'top20_articles.json'), 'w', encoding='utf-8') as f:
        json.dump(top20, f, ensure_ascii=False, indent=2)
    print(f"\nSaved top 20 to docs/top20_articles.json")

if __name__ == '__main__':
    main()
