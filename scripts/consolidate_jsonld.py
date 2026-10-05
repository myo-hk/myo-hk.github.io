#!/usr/bin/env python3
"""
Consolidate fragmented JSON-LD blocks into fewer blocks (max 2 per page).
Merges: Organization + Article/BlogPosting/BreadcrumbList + WebPage → one @graph block.
Leaves FAQPage as separate block (required by Google for FAQ rich results).
Usage: python3 scripts/consolidate_jsonld.py [--test]
"""
import re
import json
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"
MAX_BLOCKS = 2  # One for page-level schema, one optional for FAQPage

LD_PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
    re.DOTALL
)

def get_schema_type(content):
    """Extract @type from JSON-LD content."""
    try:
        data = json.loads(content.strip())
        if isinstance(data, dict):
            return data.get("@type")
        elif isinstance(data, list):
            return [item.get("@type") for item in data if isinstance(item, dict)]
        return None
    except (json.JSONDecodeError, AttributeError):
        return None

def main():
    test_mode = "--test" in sys.argv
    files = sorted(BLOG_DIR.glob("*.html"))
    changed = 0
    skipped = 0

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        blocks = list(LD_PATTERN.finditer(content))
        if len(blocks) <= 2:
            continue  # Already consolidated

        # Separate FAQPage from non-FAQPage blocks
        faq_blocks = []
        non_faq = []

        for m in blocks:
            raw = m.group(1).strip()
            stype = get_schema_type(raw)
            if stype == "FAQPage":
                faq_blocks.append(m)
            else:
                non_faq.append(m)

        # Merge all non-FAQPage into one graph
        merged_schemas = []
        for m in non_faq:
            try:
                data = json.loads(m.group(1).strip())
                if isinstance(data, dict):
                    merged_schemas.append(data)
                elif isinstance(data, list):
                    merged_schemas.extend(data)
            except json.JSONDecodeError:
                pass

        if len(merged_schemas) <= 1 and len(faq_blocks) <= 1:
            skipped += 1
            continue  # Nothing to consolidate

        # Build new content: remove all LD blocks, re-insert merged ones
        new_content = LD_PATTERN.sub("__LD_PLACEHOLDER__", content)

        # Serialize merged non-FAQ blocks
        replacements = []
        if len(merged_schemas) > 1:
            merged_json = json.dumps({
                "@context": "https://schema.org",
                "@graph": merged_schemas
            }, ensure_ascii=False, indent=2)
            replacements.append(f'<script type="application/ld+json">\n{merged_json}\n</script>')
        elif len(merged_schemas) == 1:
            merged_json = json.dumps(merged_schemas[0], ensure_ascii=False, indent=2)
            replacements.append(f'<script type="application/ld+json">\n{merged_json}\n</script>')

        # Add FAQ blocks
        for m in faq_blocks:
            try:
                faq_json = json.dumps(json.loads(m.group(1).strip()), ensure_ascii=False, indent=2)
                replacements.append(f'<script type="application/ld+json">\n{faq_json}\n</script>')
            except json.JSONDecodeError:
                replacements.append(m.group(0))

        # Replace placeholders one by one
        for rep in replacements:
            new_content = new_content.replace("__LD_PLACEHOLDER__", rep, 1)
        # Remove any remaining placeholders
        new_content = new_content.replace("__LD_PLACEHOLDER__", "")

        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            print(f"  ✓ {fpath.name}: {len(blocks)} blocks → {len(replacements)} blocks")
            changed += 1

    print(f"\nDone: {changed} files consolidated" + (f", {skipped} skipped (already ≤2 meaningful)" if not test_mode else ""))

if __name__ == "__main__":
    main()
