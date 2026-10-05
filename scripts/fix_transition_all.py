#!/usr/bin/env python3
"""
Batch fix `transition: all 0.2s ease;` in the blog/ directory.
Two patterns exist:
  1. .sticky-conversion-bar .btn-social → transform, box-shadow, background, border-color
  2. .back-to-list-btn → background-color, transform
"""
import os
import glob

BLOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'blog')

files = sorted(glob.glob(os.path.join(BLOG_DIR, '*.html')))
changed = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    old_content = content
    
    # Pattern 1: btn-social sticky bar pattern
    content = content.replace(
        '''            width: 52px;
            height: 52px;
            border-radius: 14px;
            text-decoration: none;
            transition: all 0.2s ease;
            border: 3px solid #333;
            background: #fff;
        }

        .sticky-conversion-bar .btn-ig {''',
        '''            width: 52px;
            height: 52px;
            border-radius: 14px;
            text-decoration: none;
            transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease, border-color 0.2s ease;
            border: 3px solid #333;
            background: #fff;
        }

        .sticky-conversion-bar .btn-ig {'''
    )
    
    # Pattern 2: back-to-list-btn
    content = content.replace(
        '''    padding: 0.5rem 1rem;
    background-color: #fef3c7;
    border-radius: 0.5rem;
    font-weight: 500;
    transition: all 0.2s ease;
}
.back-to-list-btn:hover {''',
        '''    padding: 0.5rem 1rem;
    background-color: #fef3c7;
    border-radius: 0.5rem;
    font-weight: 500;
    transition: background-color 0.2s ease, transform 0.2s ease;
}
.back-to-list-btn:hover {'''
    )
    
    if content != old_content:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        changed += 1

print(f"Fixed `transition: all` in {changed} blog articles")
