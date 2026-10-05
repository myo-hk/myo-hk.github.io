#!/usr/bin/env python3
"""parse_blog.py — Extract structured sections from blog HTML files."""

import os
import sys
import json
import re
from pathlib import Path
from typing import Optional

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip3 install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


def extract_article_body(html: str) -> str:
    """Extract the main article body from blog HTML, stripping nav/footer/sidebars."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove non-content elements
    for tag in soup.find_all(["nav", "footer", "aside", "header", "script", "style"]):
        tag.decompose()

    # Try common article containers
    article = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"content|article|post", re.I))

    if article:
        return str(article)
    return str(soup)


def parse_blog_sections(html: str) -> list[dict]:
    """
    Split blog HTML into sections by H2/H3 headings.
    Returns: [{"heading": "...", "content": "...", "level": 2}, ...]
    """
    soup = BeautifulSoup(html, "html.parser")
    sections = []
    current_heading = ""
    current_content = []
    current_level = 0

    for tag in soup.find_all(["h2", "h3", "p", "ul", "ol", "blockquote"]):
        if tag.name in ("h2", "h3"):
            # Save previous section
            if current_heading or current_content:
                sections.append({
                    "heading": current_heading.strip(),
                    "content": "\n".join(current_content).strip(),
                    "level": current_level
                })
            current_heading = tag.get_text(strip=True)
            current_level = int(tag.name[1])
            current_content = []
        elif tag.name == "p":
            text = tag.get_text(strip=True)
            if text:
                current_content.append(text)
        elif tag.name in ("ul", "ol"):
            for li in tag.find_all("li", recursive=False):
                text = li.get_text(strip=True)
                if text:
                    current_content.append(f"• {text}")
            # Also handle nested lis
            for li in tag.find_all("li"):
                text = li.get_text(strip=True)
                if text and text not in [c.replace("• ", "") for c in current_content]:
                    if not any(text in c for c in current_content):
                        current_content.append(f"• {text}")
        elif tag.name == "blockquote":
            text = tag.get_text(strip=True)
            if text:
                current_content.append(f"> {text}")

    # Don't forget last section
    if current_heading or current_content:
        sections.append({
            "heading": current_heading.strip(),
            "content": "\n".join(current_content).strip(),
            "level": current_level
        })

    return sections


def parse_blog_file(filepath: str) -> dict:
    """
    Parse a single blog HTML file.
    Returns: {"title": "...", "sections": [{"heading": "...", "content": "...", "level": 2}, ...]}
    """
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Extract title
    title = ""
    title_tag = soup.find("title") or soup.find("h1") or soup.find("h2")
    if title_tag:
        title = title_tag.get_text(strip=True)
        # Clean common suffixes like " | MySite" or " - Blog"
        title = re.sub(r"\s+[|\-–—]\s+.+$", "", title).strip()

    article_html = extract_article_body(html)
    sections = parse_blog_sections(article_html)

    return {
        "title": title,
        "sections": sections,
        "filepath": filepath
    }


def build_blog_index(blog_dir: str = "blog") -> dict:
    """
    Build a complete index of all blog files.
    Returns: {filename: {"title": "...", "sections": [...], "filepath": "..."}}
    """
    blog_path = Path(blog_dir)
    if not blog_path.exists():
        print(f"ERROR: blog directory not found: {blog_dir}", file=sys.stderr)
        sys.exit(1)

    index = {}
    html_files = sorted(blog_path.glob("*.html"))
    print(f"Found {len(html_files)} blog HTML files in {blog_dir}")

    for html_file in html_files:
        try:
            data = parse_blog_file(str(html_file))
            index[html_file.name] = data
        except Exception as e:
            print(f"WARNING: Failed to parse {html_file}: {e}", file=sys.stderr)

    return index


def save_index(index: dict, output_path: str = "scripts/blog_index.json"):
    """Save blog index to JSON file."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Blog index saved to {output_path} ({len(index)} articles)")


def load_index(index_path: str = "scripts/blog_index.json") -> dict:
    """Load blog index from JSON file."""
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parse blog HTML files into structured sections")
    parser.add_argument("--blog-dir", "-d", default="blog", help="Blog directory (default: blog)")
    parser.add_argument("--output", "-o", default="scripts/blog_index.json", help="Output JSON path")
    parser.add_argument("--load", "-l", help="Load existing index instead of rebuilding")
    args = parser.parse_args()

    if args.load:
        index = load_index(args.load)
        print(f"Loaded index with {len(index)} articles from {args.load}")
    else:
        index = build_blog_index(args.blog_dir)
        save_index(index, args.output)

    # Print summary
    for name, data in list(index.items())[:3]:
        print(f"\n{name}: {data['title']}")
        print(f"  {len(data['sections'])} sections:")
        for s in data['sections'][:2]:
            print(f"    [H{str(s['level'])}] {s['heading']}: {len(s['content'])} chars")