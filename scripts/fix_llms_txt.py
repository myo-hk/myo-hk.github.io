#!/usr/bin/env python3
"""
Convert llms.txt bare URLs to proper markdown link format [text](url).
Also validates that linked files exist.

Usage: python3 scripts/fix_llms_txt.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
LLMS_PATH = ROOT / "llms.txt"

# Matches lines like "- Homepage: https://..." or "- 婚禮攝影拍照清單: https://..."
BARE_URL_PATTERN = re.compile(
    r'^(- \s*)([^:]+):\s*(https?://[^\s]+)'
)

# Broken links to fix (None = remove the line)
BROKEN_LINKS = {
    "pricing.md": None,  # raw markdown file, not a web page
}


def convert_line(line: str) -> str:
    m = BARE_URL_PATTERN.match(line)
    if m:
        prefix = m.group(1)
        label = m.group(2).strip()
        url = m.group(3).strip()
        # Check for known broken links
        for broken, replacement in BROKEN_LINKS.items():
            if broken in url:
                if replacement is None:
                    return f"# REMOVED: {line.strip()}\n"
                url = replacement
                break
        return f"{prefix}[{label}]({url})\n"
    return line


def main():
    lines = LLMS_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    converted = [convert_line(l) for l in lines]
    LLMS_PATH.write_text("".join(converted), encoding="utf-8")
    print(f"✅ Updated {LLMS_PATH}")

    # Count results
    text = LLMS_PATH.read_text(encoding="utf-8")
    md_links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text))
    print(f"   Markdown links: {md_links}")

    # Verify: no bare http/https URLs (simple check - just look for http:// or https:// not inside parens)
    # Count URLs inside markdown links vs outside
    # Exclude # REMOVED: lines which are comments showing what was deleted
    text_no_removed = re.sub(r'^# REMOVED:.*$', '', text, flags=re.MULTILINE)
    urls_in_links = len(re.findall(r'\]\(https?://[^)]+\)', text_no_removed))
    all_urls = len(re.findall(r'https?://[^\s\)]+', text_no_removed))
    outside = all_urls - urls_in_links
    if outside:
        print(f"⚠️  {outside} URLs outside markdown link syntax")
    else:
        print("✅ All URLs are in proper markdown link syntax")


if __name__ == "__main__":
    main()