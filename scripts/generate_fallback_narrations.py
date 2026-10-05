#!/usr/bin/env python3
"""
generate_fallback_narrations.py — Generate generic narrations when blog match fails.

This script generates narrations.ts for chapters with no blog content match:
- English slug topics (candles, personal, year1, etc.)
- Chapters where outline.md description lacks 。！？ punctuation

Strategy:
1. Use presentation title (from outline.md) + chapter number
2. Generate 3-6 generic wedding-related sentences
3. Apply Cantonese adaptation
4. Output narrations.ts format
"""

import os
import re
from pathlib import Path
from typing import Optional

# Import from expand_narrations
from expand_narrations import adapt_to_cantonese_full, generate_narrations_ts, distribute_sentences_to_steps


# Generic wedding narration templates by chapter type
CHAPTER_TEMPLATES = {
    # Certificate-related chapters
    "certificate": [
        "結婚證書係愛情嘅見證，揀一個靚嘅證書套好重要。",
        "我哋提供亞麻布同磨砂珠光兩種材質，質感一流。",
        "熱轉印工藝可以印低你哋嘅名字同結婚日期，獨一無二。",
        "證書套尺寸係標準 A5，完美fit入所有結婚證書。",
        "每款設計都經過精心打磨，確保每一處細節都完美。",
    ],
    # Ring-related chapters
    "ring": [
        "婚戒係婚姻嘅象徵，揀選需要細心考慮。",
        "鑽石嘅 4C 標準係切工、顏色、淨度同克拉數。",
        "香港有多家本地珠寶品牌，提供高性價比選擇。",
        "建議預留預算嘅 5-10% 購買婚戒。",
        "試戴時要注意指環闊度同手型嘅匹配。",
    ],
    # Venue-related chapters
    "venue": [
        "婚宴場地係婚禮成功嘅關鍵，要提早預訂。",
        "香港酒店婚宴價錢由三萬到三十萬唔等。",
        "戶外婚禮要準備後備方案，以防天氣變化。",
        "場地佈置要配合整體婚禮主題同色調。",
        "試食好重要，確保賓客滿意菜品質素。",
    ],
    # Photography-related chapters
    "photo": [
        "婚禮攝影係記錄幸福時刻，唔可以馬虎。",
        "攝影風格分傳統、自然同藝術三種。",
        "建議睇多啲攝影師嘅作品集，先至做決定。",
        "拍攝時間要預留充足，唔好太趕。",
        "戶外拍攝要留意光線同天氣條件。",
    ],
    # Dress-related chapters
    "dress": [
        "婚紗係新娘最重要嘅戰袍，要精心挑選。",
        "試婚紗最好提早三到六個月開始。",
        "婚紗款式要配合身形同婚禮場地。",
        "婚紗保養好重要，要避免陽光直射。",
        "婚紗租賃同購買各有優缺點，要衡量。",
    ],
    # Timeline/planning chapters
    "timeline": [
        "婚禮籌備要提早開始，建議至少一年前。",
        "制定 checklist 可以唔好漏低任何細節。",
        "預算分配要合理，唔好超支。",
        "供應商要提早預訂，好日子好快被搶光。",
        "婚禮前一晚要早啲瞓，保持最佳狀態。",
    ],
    # Tradition/custom-related chapters
    "tradition": [
        "中國傳統婚禮習俗有數千年歷史。",
        "过大禮、安床、上頭係必要流程。",
        "吉日選擇要配合雙方八字，唔可以隨便。",
        "敬茶儀式要準備茶具同茶葉，有特定要求。",
        "傳統習俗可以簡化，但唔可以完全省略。",
    ],
    # Legal/documentation chapters
    "legal": [
        "結婚登記要遞交擬結婚通知書，至少 15 日前。",
        "婚姻登記處有 5 間，要預約先可以辦理。",
        "監禮人制度可以喺戶外舉行法律婚禮。",
        "結婚文件要帶備身份證同住址證明。",
        "海外結婚要注意當地法律要求。",
    ],
    # Makeup/hair chapters
    "makeup": [
        "新娘化妝要試妝，確保當日效果滿意。",
        "妝容要配合婚紗款式同婚禮主題。",
        "髮型要考慮頭飾同面型嘅匹配。",
        "化妝用品要用防水配方，唔好溶妝。",
        "建議帶備補妝用品，隨時保持完美。",
    ],
    # Default fallback (generic wedding content)
    "default": [
        "婚禮係人生最重要嘅時刻之一，要精心籌備。",
        "每對新人都有獨特嘅故事，值得被記錄。",
        "細節決定成敗，唔可以忽略任何小地方。",
        "預留時間處理突發狀況，保持彈性。",
        "享受整個過程，唔好太緊張。",
    ],
}


def classify_chapter(chapter_slug: str, pres_title: str) -> str:
    """
    Classify chapter into a category based on slug and presentation title.
    Returns category key for CHAPTER_TEMPLATES.
    """
    slug_lower = chapter_slug.lower()
    
    # Direct keyword matching
    category_keywords = {
        "certificate": ["certificate", "cert", "cover", "size", "dimension", "preservation"],
        "ring": ["ring", "diamond", "4c", "jewelry", "band"],
        "venue": ["venue", "location", "hotel", "banquet", "place"],
        "photo": ["photo", "photography", "camera", "shoot", "picture"],
        "dress": ["dress", "gown", "bridal", "attire", "groom"],
        "timeline": ["timeline", "checklist", "planning", "schedule", "budget"],
        "tradition": ["tradition", "custom", "culture", "auspicious", "taboo"],
        "legal": ["legal", "law", "registration", "document", "notice", "officer"],
        "makeup": ["makeup", "hair", "beauty", "cosmetic", "styling"],
    }
    
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in slug_lower:
                return category
    
    # Check presentation title
    pres_lower = pres_title.lower()
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in pres_lower:
                return category
    
    return "default"


def get_presentation_title(pres_dir: str) -> str:
    """Extract Chinese presentation title from outline.md."""
    outline_file = Path(pres_dir) / "outline.md"
    if not outline_file.exists():
        return ""
    
    with open(outline_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # First line is usually "# Title"
    first_line = content.split("\n")[0].strip()
    # Remove markdown heading marker
    title = re.sub(r"^#+\s*", "", first_line)
    # Remove " — Outline" suffix if present
    title = re.sub(r"\s*—\s*Outline$", "", title)
    
    return title


def generate_fallback_narrations(
    chapter_slug: str,
    pres_title: str,
    chapter_number: int,
    num_steps: int = 3
) -> str:
    """
    Generate fallback narrations when blog match fails.
    
    Args:
        chapter_slug: Chapter directory name (e.g., "03-content")
        pres_title: Presentation title from outline.md (e.g., "結婚證書尺寸規格")
        chapter_number: Chapter number (2-5)
        num_steps: Number of steps (default: 3)
    
    Returns:
        TypeScript source for narrations.ts
    """
    # Classify chapter to get appropriate templates
    category = classify_chapter(chapter_slug, pres_title)
    templates = CHAPTER_TEMPLATES.get(category, CHAPTER_TEMPLATES["default"])
    
    # Select 6-9 sentences based on chapter number
    # Earlier chapters get first sentences, later chapters get later sentences
    num_sentences = min(9, max(6, len(templates)))
    start_idx = min(chapter_number - 2, max(0, len(templates) - num_sentences))
    selected = templates[start_idx:start_idx + num_sentences]
    
    # Add presentation context if available
    intro_sentences = []
    if pres_title and len(pres_title) >= 3:
        # Create intro from presentation title
        intro_sentences = [
            f"我哋今日講下{pres_title}嘅重點。",
            f"呢個章節會詳細介紹{pres_title}嘅關鍵知識。",
        ]
    
    # Combine intro + templates
    all_sentences = intro_sentences + selected
    
    # Apply Cantonese adaptation
    adapted = [adapt_to_cantonese_full(s) for s in all_sentences]
    
    # Distribute across steps
    step_sentences = distribute_sentences_to_steps(adapted, num_steps)
    
    return generate_narrations_ts(step_sentences)


def process_all_missing_chapters(dry_run: bool = False) -> dict:
    """
    Find all chapters missing narrations.ts and generate fallback content.
    
    Returns: {"created": int, "skipped": int, "errors": list}
    """
    results = {"created": 0, "skipped": 0, "errors": []}
    
    presentations_dir = Path("presentations")
    if not presentations_dir.exists():
        results["errors"].append("Presentations directory not found")
        return results
    
    # Find all chapter directories
    for pres_dir in sorted(presentations_dir.iterdir()):
        if not pres_dir.is_dir() or not pres_dir.name[0].isdigit():
            continue
        
        pres_title = get_presentation_title(pres_dir)
        print(f"\nProcessing: {pres_dir.name} ({pres_title})")
        
        chapters_dir = pres_dir / "presentation" / "src" / "chapters"
        if not chapters_dir.exists():
            continue
        
        for chapter_dir in sorted(chapters_dir.iterdir()):
            if not chapter_dir.is_dir() or not chapter_dir.name[0].isdigit():
                continue
            
            # Skip coldopen and cta
            if chapter_dir.name in ("01-coldopen", "06-cta"):
                continue
            
            narrations_file = chapter_dir / "narrations.ts"
            
            # Skip if already exists
            if narrations_file.exists():
                with open(narrations_file, "r", encoding="utf-8") as f:
                    content = f.read()
                # Count existing strings
                strings = re.findall(r'"([^"]+)"', content)
                strings = [s for s in strings if not s.startswith("../") and not s.startswith("import")]
                if len(strings) >= 2:
                    print(f"  Skipping {chapter_dir.name}: already has {len(strings)} strings")
                    results["skipped"] += 1
                    continue
            
            # Extract chapter number and slug
            chapter_name = chapter_dir.name
            chapter_num_match = re.match(r"^(\d+)", chapter_name)
            if not chapter_num_match:
                continue
            
            chapter_num = int(chapter_num_match.group(1))
            chapter_slug = re.sub(r"^\d+[-_]", "", chapter_name)
            
            print(f"  Generating for {chapter_name}...")
            
            # Generate fallback narrations
            try:
                narrations = generate_fallback_narrations(
                    chapter_slug=chapter_slug,
                    pres_title=pres_title,
                    chapter_number=chapter_num,
                    num_steps=3
                )
                
                if not dry_run:
                    with open(narrations_file, "w", encoding="utf-8") as f:
                        f.write(narrations)
                    
                    # Verify
                    with open(narrations_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    strings = re.findall(r'"([^"]+)"', content)
                    strings = [s for s in strings if not s.startswith("../") and not s.startswith("import")]
                    
                    print(f"    Created with {len(strings)} strings")
                    results["created"] += 1
                else:
                    strings = re.findall(r'"([^"]+)"', narrations)
                    strings = [s for s in strings if not s.startswith("../") and not s.startswith("import")]
                    print(f"    [DRY RUN] Would create with {len(strings)} strings")
                    
            except Exception as e:
                error_msg = f"{pres_dir.name}/{chapter_name}: {e}"
                results["errors"].append(error_msg)
                print(f"    ERROR: {e}")
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate fallback narrations for chapters with no blog match")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no file writes")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample data")
    args = parser.parse_args()
    
    if args.demo:
        # Demo generation
        narrations = generate_fallback_narrations(
            chapter_slug="03-content",
            pres_title="結婚證書尺寸規格",
            chapter_number=3,
            num_steps=3
        )
        print("Generated narrations.ts:")
        print(narrations)
    else:
        results = process_all_missing_chapters(dry_run=args.dry_run)
        print(f"\n{'='*60}")
        print(f"RESULTS:")
        print(f"  Created: {results['created']} chapters")
        print(f"  Skipped: {results['skipped']} chapters")
        if results["errors"]:
            print(f"  Errors: {len(results['errors'])}")
            for err in results["errors"][:5]:
                print(f"    - {err}")