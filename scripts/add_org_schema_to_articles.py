#!/usr/bin/env python3
"""
Batch-add Organization JSON-LD to blog articles.
Adds the Organization schema block just before </head> if not already present.
"""
import re
import json
import os

BLOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'blog')

ORG_SCHEMA = '''    <script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "MyO 專屬結婚證書套",
    "url": "https://myo-makeyourown.pages.dev",
    "logo": "https://myo-makeyourown.pages.dev/image/01_company_logo.png",
    "sameAs": [
        "https://www.instagram.com/myo.makeyourown/"
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+852-6379-6410",
        "contactType": "customer service",
        "areaServed": "HK",
        "availableLanguage": ["Chinese", "English"]
    }
}
</script>'''

def has_org_schema(content):
    """Check if Organization JSON-LD already exists."""
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    blocks = re.findall(pattern, content, re.DOTALL)
    for block in blocks:
        try:
            data = json.loads(block.strip())
            if data.get('@type') == 'Organization':
                return True
        except:
            continue
    return False

def add_org_schema(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_org_schema(content):
        return False  # Already has Organization schema

    # Insert Organization schema before </head>
    content = content.replace('</head>', '\n' + ORG_SCHEMA + '\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    added = 0
    skipped = 0

    for filename in sorted(os.listdir(BLOG_DIR)):
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(BLOG_DIR, filename)
        if add_org_schema(filepath):
            added += 1
        else:
            skipped += 1

    print(f"Added Organization schema to {added} article(s)")
    print(f"Skipped {skipped} article(s) (already had Organization schema)")

if __name__ == '__main__':
    main()