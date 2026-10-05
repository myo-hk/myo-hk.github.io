#!/usr/bin/env python3
"""match_blog_to_chapter.py — Match blog sections to presentation chapters."""

import os
import re
import json
from pathlib import Path
from typing import Optional


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Simple keyword-based similarity between two texts.
    Returns score 0-1 (higher = more similar).
    """
    if not text1 or not text2:
        return 0.0

    # Normalize
    t1 = text1.lower()
    t2 = text2.lower()

    # Remove common punctuation
    t1_clean = re.sub(r'[^\w\s]', ' ', t1)
    t2_clean = re.sub(r'[^\w\s]', ' ', t2)

    # Split into words (simple tokenization)
    words1 = set(t1_clean.split())
    words2 = set(t2_clean.split())

    # Remove stopwords
    stopwords = {'的', '是', '在', '有', '和', '與', '或', '了', '也', '就', '都', '而', '及', '為', '於', '這', '那', '什麼', '怎麼', '如何', '哪'}
    words1 = words1 - stopwords
    words2 = words2 - stopwords

    if not words1 or not words2:
        return 0.0

    # Jaccard similarity
    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0


def extract_chinese_chars(text: str) -> set:
    """Extract meaningful Chinese characters from text (no single-char stopwords)."""
    chinese_stopwords = {'的', '是', '在', '有', '和', '與', '或', '了', '也', '就', '都', '而', '及', '為', '於', '這', '那', '什麼', '怎麼', '如何', '哪', '一', '不', '人', '我', '你', '他', '她', '我', '我哋', '你哋', '佢哋'}
    chars = set()
    for c in text:
        if '\u4e00' <= c <= '\u9fff':  # CJK Unified Ideographs
            if c not in chinese_stopwords and len(c) == 1:
                chars.add(c)
    return chars


def chinese_char_similarity(text1: str, text2: str) -> float:
    """
    Character-level similarity for Chinese text.
    Handles Chinese (no spaces) by comparing character sets.
    Also works for English/mixed text.
    """
    if not text1 or not text2:
        return 0.0
    chars1 = extract_chinese_chars(text1)
    chars2 = extract_chinese_chars(text2)
    if not chars1 or not chars2:
        return 0.0
    intersection = len(chars1 & chars2)
    union = len(chars1 | chars2)
    return intersection / union if union > 0 else 0.0


def text_bigram_similarity(text1: str, text2: str) -> float:
    """Bigram-based Jaccard similarity for Chinese text."""
    if not text1 or not text2:
        return 0.0
    bg1 = {text1[i:i+2] for i in range(len(text1)-1) if '\u4e00' <= text1[i] <= '\u9fff'}
    bg2 = {text2[j:j+2] for j in range(len(text2)-1) if '\u4e00' <= text2[j] <= '\u9fff'}
    if not bg1 or not bg2:
        return 0.0
    return len(bg1 & bg2) / len(bg1 | bg2)


def shared_char_count(text1: str, text2: str) -> int:
    """Count shared meaningful Chinese chars between two texts."""
    c1 = extract_chinese_chars(text1)
    c2 = extract_chinese_chars(text2)
    return len(c1 & c2)


def find_best_matching_section(
    sections: list[dict],
    query: str,
    min_similarity: float = 0.05,
    min_content_chars: int = 15
) -> Optional[dict]:
    """
    Find the best-matching blog section for a query (chapter topic).
    Uses hybrid scoring: char similarity + bigram overlap + shared char count.
    """
    if not sections or not query:
        return None

    best_score = 0
    best_section = None
    best_heading = ""

    for section in sections:
        heading = section.get("heading", "")
        content = section.get("content", "")

        # Heading-as-content for empty sections (heading-only section headers)
        effective_content = content
        if not effective_content or len(effective_content.strip()) < 5:
            hs = max(chinese_char_similarity(heading, query), text_bigram_similarity(heading, query)) * 2.0
            if hs >= 0.3:
                effective_content = heading

        heading_score = max(
            chinese_char_similarity(heading, query),
            text_bigram_similarity(heading, query)
        ) * 2.0

        content_text = effective_content[:500]
        char_sim = chinese_char_similarity(content_text, query)
        bg_sim = text_bigram_similarity(content_text, query)
        shared = shared_char_count(content_text, query)
        shared_score = min(shared / 10.0, 1.0)
        content_score = char_sim + bg_sim + shared_score

        combined_score = heading_score + content_score

        if combined_score > best_score and combined_score >= min_similarity:
            best_score = combined_score
            best_section = section
            best_heading = heading

    if best_section and len(best_section.get("content", "")) >= min_content_chars:
        return {
            "section": best_section,
            "score": best_score,
            "matched_heading": best_heading
        }

    # No section with 50+ chars passed the threshold.
    # Look for the best heading-only match (even if content is thin).
    # This prevents falling through to the noisy "return all sections" fallback.
    best_heading_only_score = 0
    best_heading_only_section = None
    best_heading_only_heading = ""

    for section in sections:
        heading = section.get("heading", "")
        content = section.get("content", "")
        if not heading:
            continue
        heading_score = chinese_char_similarity(heading, query) * 2.0
        if heading_score > best_heading_only_score and heading_score >= 0.3:
            best_heading_only_score = heading_score
            best_heading_only_section = section
            best_heading_only_heading = heading

    if best_heading_only_section:
        h = best_heading_only_heading
        c = best_heading_only_section.get("content", "")
        return {
            "section": {"heading": h, "content": c},
            "score": best_heading_only_score,
            "matched_heading": h
        }

    return None


def match_chapter_to_blog(
    chapter_topic: str,
    blog_index: dict,
pres_slug: str = ""
) -> Optional[dict]:
    """
    Find the best blog article for a PRESENTATION (all chapters share same blog).
    Uses slug keyword translation as primary, bigram fallback as secondary.
    """
    if not blog_index:
        return None

    # Clean presentation slug
    clean_slug = re.sub(r'^\d+[-_]', '', pres_slug).lower()
    slug_words = set(clean_slug.replace('-', ' ').split()) - {'guide', 'wedding', 'hk', 'hong', 'kong', 'marriage', 'comprehensive', 'complete', 'full'}

    # PRIMARY: Translate English keywords to Chinese and search blog titles
    # English → Chinese keyword translation table
    en_to_zh = {
        'auspicious': '吉日', 'good': '好', 'date': '日', 'day': '日',
        'wedding': '結婚', 'marriage': '結婚', 'married': '結婚',
        'invitation': '請柬', 'invite': '請柬',
        'certificate': '證書', 'cert': '證書',
        'ceremony': '儀式', 'ritual': '儀式',
        'photography': '攝影', 'photo': '攝影', 'video': '影片',
        ' banquet': '酒席', 'venue': '場地', 'location': '場地',
        'dress': '婚紗', 'gown': '婚紗',
        'planning': '策劃', 'plan': '策劃',
        'budget': '預算', 'cost': '費用',
        'legal': '法律', 'law': '法律',
        'overseas': '海外', 'abroad': '海外',
        'tradition': '傳統', 'custom': '習俗', 'culture': '文化',
        'honeymoon': '蜜月', 'gift': '禮物', 'souvenir': '回禮',
        'music': '音樂', 'flower': '花', 'cake': '蛋糕',
        'attire': '禮服', 'jewelry': '珠寶', 'ring': '戒指',
        'registration': '註冊', 'register': '登記',
    }
    chinese_keywords = set()
    for word in slug_words:
        if word in en_to_zh:
            chinese_keywords.add(en_to_zh[word])
        # Also check partial matches
        for en, zh in en_to_zh.items():
            if en in word or word in en:
                chinese_keywords.add(zh)

    best_blog = None
    best_score = 0.0

    for blog_name, blog_data in blog_index.items():
        title = blog_data.get("title", "")

        # Score by Chinese keyword presence in title
        keyword_score = 0.0
        for kw in chinese_keywords:
            if kw in title:
                keyword_score += 1.0  # Each matching keyword = 1.0

        if keyword_score > best_score:
            best_score = keyword_score
            best_blog = blog_name

    # Only use keyword matching if we have 2+ matching keywords.
    # Single-char Chinese keywords (e.g. "花" from "flower") are too loose
    # and cause false positives. Fall through to bigram matching instead.
    if best_blog and best_score >= 2:
        return {
            "blog_file": best_blog,
            "matching_section": None,
            "score": best_score,
            "matched_heading": blog_index[best_blog].get("title", "")
        }

# FALLBACK: Use per-chapter bigram matching (chapter_topic → blog title)
    clean_slug = re.sub(r'^\d+[-_]', '', pres_slug).lower()
    slug_words = set(clean_slug.replace('-', ' ').split()) - {'guide', 'wedding', 'hk', 'hong', 'kong', 'marriage'}

    best_score = 0.0
    best_blog = None
    best_section = None
    best_heading = ""

    # Extract Chinese bigrams from chapter_topic (meaningful 2-char combinations)
    topic_bigrams = set()
    topic_chars = [c for c in chapter_topic if '\u4e00' <= c <= '\u9fff']
    for i in range(len(topic_chars) - 1):
        bigram = topic_chars[i] + topic_chars[i+1]
        # Filter out common bigrams that aren't useful for matching
        if bigram not in {'的是', '在有', '和不', '於這', '什麼', '怎麼', '如何'}:
            topic_bigrams.add(bigram)

    for blog_name, blog_data in blog_index.items():
        title = blog_data.get("title", "")
        sections = blog_data.get("sections", [])
        blog_name_lower = blog_name.lower()

        # 1. SLUG WORD MATCHING (English keywords in blog title/filename)
        blog_words = set(re.sub(r'[^\w\s]', '', blog_name_lower).split())
        title_words = set(re.sub(r'[^\w\s]', '', title.lower()).split())
        slug_score = 0.0
        if slug_words & blog_words or slug_words & title_words:
            slug_score = 0.3
        for word in slug_words:
            if len(word) > 3 and (word in blog_name_lower or word in title.lower()):
                slug_score = max(slug_score, 0.4)

        # 2. CHINESE BIGRAM MATCHING (most reliable for Chinese texts)
        title_bigrams = set()
        title_chars = [c for c in title if '\u4e00' <= c <= '\u9fff']
        for i in range(len(title_chars) - 1):
            title_bigrams.add(title_chars[i] + title_chars[i+1])
        bigram_overlap = topic_bigrams & title_bigrams
        bigram_score = len(bigram_overlap) * 0.15  # Each shared bigram = 0.15

        # 3. SINGLE CHAR OVERLAP (fallback)
        topic_chars_set = extract_chinese_chars(chapter_topic)
        title_chars_set = extract_chinese_chars(title)
        char_overlap = len(topic_chars_set & title_chars_set)
        char_score = char_overlap * 0.05  # Each shared char = 0.05

        # 4. Section heading match (for completeness)
        section_score = 0.0
        for section in sections:
            heading = section.get("heading", "")
            if not heading:
                continue
            h_bigrams = {heading[i:i+2] for i in range(len(heading)-1) if '\u4e00' <= heading[i] <= '\u9fff'}
            h_score = len(topic_bigrams & h_bigrams) * 0.15
            if h_score > section_score:
                section_score = h_score
                best_heading = heading

        # Combined score: bigrams are most reliable for Chinese
        combined_score = max(slug_score, bigram_score + char_score, section_score)

        if combined_score > best_score:
            best_score = combined_score
            best_blog = blog_name

    if best_blog and best_score > 0.0:
        return {
            "blog_file": best_blog,
            "matching_section": None,
            "score": best_score,
            "matched_heading": best_heading
        }

    return None


def get_chapter_content_from_blog(
    blog_file: str,
    chapter_topic: str,
    blog_index: dict,
    min_chars: int = 100
) -> str:
    """
    Get content for a chapter from the matched blog article.
    Uses find_best_matching_section to extract only the most relevant section
    based on the chapter_topic, providing per-chapter content isolation.
    """
    if blog_file not in blog_index:
        return ""

    blog_data = blog_index[blog_file]
    sections = blog_data.get("sections", [])

    if not sections:
        return ""

    # Use find_best_matching_section to extract only the most relevant section
    # This ensures each chapter gets different content from the same blog article
    best_match = find_best_matching_section(sections, chapter_topic)

    if best_match and best_match.get("section"):
        section = best_match["section"]
        heading = section.get("heading", "")
        content = section.get("content", "")

        # If heading scored well but content is thin, pull from the NEXT section.
        # Many blogs have heading-only section headers with content in the next block.
        heading_only_score_threshold = 0.3
        if heading and (not content or len(content) < 30) and best_match.get("score", 0) >= heading_only_score_threshold:
            # Find this section's index and get next section's content
            for i, s in enumerate(sections):
                if s.get("heading") == heading and i + 1 < len(sections):
                    next_section = sections[i + 1]
                    next_content = next_section.get("content", "")
                    next_heading = next_section.get("heading", "")
                    if next_content and len(next_content) >= 30:
                        # Use next section's content, prefixed with original heading
                        content = f"{next_content}"
                    break

        if heading:
            return f"{heading}。{content}"
        return content

    # Fallback: return all sections' full content
    all_content = []
    for section in sections:
        heading = section.get("heading", "")
        content = section.get("content", "")

        # Skip empty or very short sections (likely noise)
        if len(content) < 30:
            continue

        if heading:
            all_content.append(f"{heading}。{content}")
        else:
            all_content.append(content)

    return "\n".join(all_content)


def build_presentation_blog_mapping(presentations_dir: str, blog_index: dict) -> dict:
    """
    Build a mapping of presentation slug → best matching blog file.
    Returns: {"04-auspicious-date-guide": "擇吉日結婚指南.html", ...}
    """
    mapping = {}

    pres_path = Path(presentations_dir)
    if not pres_path.exists():
        print(f"WARNING: Presentations directory not found: {presentations_dir}")
        return mapping

    for pres_dir in sorted(pres_path.iterdir()):
        if not pres_dir.is_dir():
            continue

        # Get presentation slug (e.g., "04-auspicious-date-guide")
        pres_slug = pres_dir.name

        # Try to find matching blog
        # First: try exact title match from outline.md
        outline_file = pres_dir / "outline.md"
        pres_title = pres_slug  # fallback

        if outline_file.exists():
            with open(outline_file, "r", encoding="utf-8") as f:
                outline_content = f.read()
            # Use first line as title
            pres_title = outline_content.split('\n')[0].strip()

        # Try to find matching blog by title
        matched_blog = None
        best_score = 0

        for blog_name, blog_data in blog_index.items():
            blog_title = blog_data.get("title", "")
            score = calculate_similarity(blog_title, pres_title)

            # Also try slug matching
            slug_score = calculate_similarity(blog_name, pres_slug)
            score = max(score, slug_score * 0.8)  # Slight penalty for slug-only match

            if score > best_score and score > 0.1:
                best_score = score
                matched_blog = blog_name

        if matched_blog:
            mapping[pres_slug] = matched_blog
            print(f"  {pres_slug} → {matched_blog} (score: {best_score:.2f})")
        else:
            print(f"  {pres_slug} → NO MATCH (best score: {best_score:.2f})")

    return mapping


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Match blog sections to presentation chapters")
    parser.add_argument("--load-index", "-i", default="scripts/blog_index.json", help="Blog index JSON")
    parser.add_argument("--pres-dir", "-p", default="presentations", help="Presentations directory")
    parser.add_argument("--topic", "-t", help="Chapter topic to match")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    args = parser.parse_args()

    if args.demo:
        # Demo matching
        sections = [
            {"heading": "為何要揀好日子", "content": "傳統習俗認為吉日結婚可增添福氣，父母長輩通常有特定要求。", "level": 2},
            {"heading": "如何選擇吉日", "content": "配合雙方八字，選擇對雙方都有利的日子。", "level": 2},
            {"heading": "傳統習俗", "content": "中國傳統婚禮注重吉日選擇，這習俗已有數千年歷史。", "level": 3},
        ]

        topic = "為何要揀好日子"
        match = find_best_matching_section(sections, topic)
        print(f"Topic: {topic}")
        print(f"Best match: {match['matched_heading']} (score: {match['score']:.2f})")
        print(f"Content preview: {match['section']['content'][:100]}")
    elif args.topic:
        if os.path.exists(args.load_index):
            with open(args.load_index, "r", encoding="utf-8") as f:
                blog_index = json.load(f)

            # Find best blog for this topic
            match = None
            best_score = 0
            best_blog = None

            for blog_name, blog_data in blog_index.items():
                score = calculate_similarity(blog_data.get("title", ""), args.topic)
                if score > best_score:
                    best_score = score
                    best_blog = blog_name

            print(f"Topic: {args.topic}")
            print(f"Best blog: {best_blog} (score: {best_score:.2f})")
        else:
            print(f"Blog index not found: {args.load_index}")
            print("Run: python3 scripts/parse_blog.py first")
    else:
        parser.print_help()