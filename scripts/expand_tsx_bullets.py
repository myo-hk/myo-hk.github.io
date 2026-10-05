#!/usr/bin/env python3
"""expand_tsx_bullets.py — Enhance tsx slide bullet text from blog content."""

import os
import re
import json
from pathlib import Path
from typing import Optional


def extract_tsx_bullets(filepath: str) -> list[str]:
    """Extract current bullet strings from a tsx file."""
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    bullets = []
    # Match: <span>bullet text</span> patterns
    for match in re.finditer(r'<span>([^<]+)</span>', content):
        text = match.group(1).strip()
        if text:
            bullets.append(text)
    
    return bullets


def enhance_bullet(bullet: str, context: str = "", max_len: int = 60) -> str:
    """
    Enhance a single bullet point with more context.
    Keep it concise (≤60 chars) but add explanatory content.
    """
    if not bullet:
        return bullet
    
    bullet = bullet.strip()
    
    # If already substantial, just clean it
    if len(bullet) >= 50:
        return bullet
    
    # If we have context, try to add to it
    if context:
        context_clean = context.strip()
        # Take first sentence of context (up to 30 chars)
        context_sentence = context_clean[:min(40, len(context_clean))]
        if context_sentence and not context_sentence[-1] in "。！？":
            context_sentence = context_sentence.rsplit('，', 1)[0] if '，' in context_sentence else context_sentence
        
        # Only add if it makes sense and doesn't exceed max
        combined = f"{bullet}，{context_sentence}"
        if len(combined) <= max_len:
            return combined
    
    return bullet


def expand_bullet_list(bullets: list[str], blog_content: str = "", num_bullets: int = 4) -> list[str]:
    """
    Expand a list of bullet points using blog content context.
    Returns a new list of enhanced bullet strings.
    """
    if not bullets:
        # Generate bullets from blog content if none exist
        if blog_content:
            # Extract key sentences from blog content
            sentences = re.split(r'[。！？\n]+', blog_content)
            bullets = []
            for sent in sentences:
                sent = sent.strip()
                if len(sent) > 10 and len(sent) < 80:
                    bullets.append(sent)
            bullets = bullets[:num_bullets]
        else:
            bullets = ["敬請期待"] * num_bullets
    
    enhanced = []
    blog_lines = blog_content.split('\n') if blog_content else []
    
    for i, bullet in enumerate(bullets):
        context = blog_lines[i] if i < len(blog_lines) else ""
        enhanced_bullet = enhance_bullet(bullet, context)
        enhanced.append(enhanced_bullet)
    
    # Ensure we have num_bullets items
    while len(enhanced) < num_bullets:
        enhanced.append("敬請期待")
    
    return enhanced[:num_bullets]


def update_tsx_file(filepath: str, new_bullets: list[str]) -> str:
    """
    Update a tsx file with new bullet text, preserving all existing structure.
    Returns the modified content.
    """
    if not os.path.exists(filepath):
        print(f"WARNING: File not found: {filepath}")
        return ""
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all <span>...</span> occurrences in c1-list-item divs
    # Replace them in order
    modified = content
    bullet_idx = 0
    
    # Replace each <span>text</span> in order
    def replace_span(match):
        nonlocal bullet_idx
        if bullet_idx < len(new_bullets):
            new_text = new_bullets[bullet_idx]
            bullet_idx += 1
            return f'<span>{new_text}</span>'
        return match.group(0)
    
    modified = re.sub(r'<span>[^<]*</span>', replace_span, modified)
    
    return modified


def generate_updated_tsx(tsx_content: str, new_bullets: list[str]) -> str:
    """
    Given existing tsx content and new bullet list, update the bullets.
    Preserves all structure, class names, and formatting.
    """
    bullet_idx = 0
    
    def replace_span(match):
        nonlocal bullet_idx
        full_match = match.group(0)
        
        if bullet_idx < len(new_bullets):
            new_text = new_bullets[bullet_idx]
            bullet_idx += 1
            # Replace only the text part, keep the tags
            return f'<span>{new_text}</span>'
        return full_match
    
    modified = re.sub(r'<span>[^<]*</span>', replace_span, tsx_content)
    return modified


def find_tsx_files(chapter_dir: str) -> list[str]:
    """
    Find all tsx files in a chapter directory.
    Returns list of full paths sorted by name.
    """
    chapter_path = Path(chapter_dir)
    if not chapter_path.exists():
        return []
    
    tsx_files = sorted(chapter_path.glob("*.tsx"))
    return [str(f) for f in tsx_files]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Expand tsx bullet text from blog content")
    parser.add_argument("--tsx", "-t", help="tsx file to update")
    parser.add_argument("--bullets", "-b", nargs="*", help="New bullet strings")
    parser.add_argument("--blog", help="Blog content for context")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    args = parser.parse_args()
    
    if args.demo:
        # Demo
        bullets = [
            "傳統習俗認為吉日結婚可增添福氣",
            "父母長輩通常有特定要求",
            "配合雙方八字",
            "選擇有利日子"
        ]
        blog = """
        傳統習俗認為吉日結婚可增添福氣，父母長輩普遍重視。
        宜嫁娶的吉日需要配合雙方八字，選擇對雙方都有利的日子。
        中國傳統婚禮注重吉日選擇，這習俗已有數千年歷史。
        """
        enhanced = expand_bullet_list(bullets, blog, num_bullets=4)
        print("Original bullets:")
        for b in bullets:
            print(f"  [{len(b)}] {b}")
        print("\nEnhanced bullets:")
        for b in enhanced:
            print(f"  [{len(b)}] {b}")
    elif args.tsx:
        if args.bullets:
            with open(args.tsx, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = generate_updated_tsx(content, args.bullets)
            backup = args.tsx + ".bak"
            with open(backup, "w", encoding="utf-8") as f:
                f.write(content)
            with open(args.tsx, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {args.tsx} (backup: {backup})")
        else:
            bullets = extract_tsx_bullets(args.tsx)
            print(f"Found {len(bullets)} bullets in {args.tsx}:")
            for b in bullets:
                print(f"  [{len(b)}] {b}")
    else:
        parser.print_help()