#!/usr/bin/env python3
"""
Clean up combined JSON-LD blocks in blog articles.
Splits merged Article+FAQPage blocks into separate <script> tags.
For duplicates, removes the top-of-file combined block.
"""
import re
import json
import os

BLOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'blog')

def has_separate_blocks(content):
    """Check if file has properly separated Article and FAQPage blocks elsewhere."""
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    types_seen = []
    for block in blocks:
        try:
            # Handle combined blocks by parsing as JSON array
            text = block.strip()
            if text.startswith('{'):
                obj = json.loads(text[:text.index('},{') + 1] + '}') if '},{' in text else json.loads(text)
                types_seen.append(obj.get('@type'))
        except:
            pass
    # Check if we found both Article and FAQPage in separate blocks
    return types_seen.count('Article') >= 1 and types_seen.count('FAQPage') >= 1

def fix_combined_json_ld(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all JSON-LD script blocks
    pattern = r'<script type="application/ld\+json">(.*?)</script>'

    def has_combined_block(text):
        """Check if text has combined JSON objects (Article + FAQPage merged)"""
        return '},{"@context"' in text or '},{"@context' in text

    def split_combined(text):
        """Split combined JSON objects into separate script blocks"""
        text = text.strip()
        # Find the split point between the two JSON objects
        split_idx = text.index('},{"@context"')
        first_obj = text[:split_idx + 1]  # Include closing }
        second_obj = '{' + text[split_idx + 1:]  # Add opening {
        return first_obj, second_obj

    blocks = list(re.finditer(pattern, content, re.DOTALL))
    modified = False

    for match in blocks:
        inner = match.group(1)
        if has_combined_block(inner):
            # Check if this article already has proper separate blocks elsewhere
            if has_separate_blocks(content):
                # Remove this block entirely (it's a duplicate)
                content = content.replace(match.group(0), '')
                modified = True
                print(f"  Removed duplicate combined block")
            else:
                # Split into two blocks
                obj1, obj2 = split_combined(inner)
                new_block = f'<script type="application/ld+json">\n    {obj1}\n    </script>\n    <script type="application/ld+json">\n    {obj2}\n    </script>'
                content = content.replace(match.group(0), new_block)
                modified = True
                print(f"  Split combined JSON into two blocks")

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    fixed = 0
    for filename in sorted(os.listdir(BLOG_DIR)):
        if filename.endswith('.html'):
            filepath = os.path.join(BLOG_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            pattern = r'<script type="application/ld\+json">(.*?)</script>'
            blocks = re.findall(pattern, content, re.DOTALL)
            has_combined = any('},{"@context"' in b or '},{"@context' in b for b in blocks)
            if has_combined:
                print(f"Fixing: {filename}")
                if fix_combined_json_ld(filepath):
                    fixed += 1
    print(f"\nDone. Fixed {fixed} file(s).")

if __name__ == '__main__':
    main()