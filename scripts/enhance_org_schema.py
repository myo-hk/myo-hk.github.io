#!/usr/bin/env python3
"""Enhance Organization JSON-LD with description, foundingDate, areaServed."""

import re, json, glob

DESC = "香港設計師級結婚證書套品牌，提供客製化亞麻布與磨砂珠光證書套，採用熱轉印工藝印製新人名字與結婚日期。"

def enhance_org(html: str) -> str:
    def fix_block(m: re.Match) -> str:
        try:
            block = m.group(1).strip()
            data = json.loads(block)
        except json.JSONDecodeError:
            return m.group(0)
        if not isinstance(data, dict) or data.get("@type") != "Organization":
            return m.group(0)
        changed = False
        if "description" not in data:
            data["description"] = DESC
            changed = True
        if "foundingDate" not in data:
            data["foundingDate"] = "2025"
            changed = True
        if "areaServed" not in data:
            data["areaServed"] = "HK"
            changed = True
        if changed:
            return f'<script type="application/ld+json">\n{json.dumps(data, indent=2, ensure_ascii=False)}\n</script>'
        return m.group(0)

    return re.sub(
        r'<script type="application/ld\+json">\n?(.*?)\n?</script>',
        fix_block,
        html,
        flags=re.DOTALL
    )

def main():
    files = sorted(glob.glob("blog/*.html"))
    updated = 0
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            src = f.read()
        out = enhance_org(src)
        if out != src:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(out)
            updated += 1
            print(f"  Updated: {fp}")
    print(f"\nTotal files updated: {updated}")

if __name__ == "__main__":
    main()
