#!/usr/bin/env python3
"""expand_narrations.py — Generate enriched narrations.ts from blog + search content."""

import os
import re
import sys
from typing import Optional

# ─── NOISE PATTERNS ───────────────────────────────────────────────────────────
# These are stripped BEFORE sentence splitting to prevent noise from polluting output.

NOISE_PATTERNS: list[str] = [
    # Bullet/checklist symbols
    "•", "☐", "☑", "○", "◉", "▣",
    # Blog structural noise
    "延伸閱讀", "分享本文", "分享到", "相關文章",
    # Blog artifact prefixes (lines starting with ...)
    "...香港", "...婚禮", "...結婚",
    # Blog section headers (often repeat at end of article)
    "香港婚宴酒水指南", "香港婚宴酒水完整指南", "2026年婚宴酒水建議",
    "婚禮攝影相機固件更新指南", "婚禮攝影相機快門壽命指南",
    "婚禮攝影後製預設推薦", "婚禮攝影風格指南",
    # Action-oriented noise (not narration)
    "立即查詢", "了解更多", "免費咨詢", "點擊查看",
    # Contact/sharing noise
    "WhatsApp", "Instagram", "Facebook", "youtube",
]

# Patterns matched as substrings (shorter noise phrases)
NOISE_SUBSTRINGS: list[str] = [
    "香港婚宴酒水指南",
    "婚禮攝影相機",
    "延伸閱讀",
    "分享本文",
]


def clean_content(text: str) -> str:
    """
    Remove noise patterns from blog content BEFORE sentence splitting.
    This prevents noise symbols from appearing as individual sentences.
    """
    if not text:
        return text

    result = text

    # Remove lines that are mostly noise
    lines = result.split("\n")
    cleaned_lines = []
    for line in lines:
        # Skip lines that are just noise symbols
        stripped = line.strip()
        if not stripped:
            continue
        # Skip lines that start with noise bullets and have no real content
        if stripped.startswith("• ") or stripped.startswith("☐ ") or stripped.startswith("○ "):
            # Keep the line only if it has substantial content after the bullet
            after_bullet = re.sub(r"^[•☐○◉▣]\s*", "", stripped)
            if len(after_bullet) < 10:
                continue
            line = after_bullet
        # Skip artifact prefixes (lines starting with ...)
        if stripped.startswith("...") and len(stripped) < 60:
            continue
        cleaned_lines.append(line)
    result = "\n".join(cleaned_lines)

    # Remove known noise substrings (line by line to avoid breaking sentences)
    for noise in NOISE_SUBSTRINGS:
        result = result.replace(noise, "")

    # Remove noise characters
    for noise in NOISE_PATTERNS:
        result = result.replace(noise, "")

    # Collapse multiple spaces/newlines
    result = re.sub(r"\n{3,}", "\n\n", result)
    result = re.sub(r" {2,}", " ", result)
    result = re.sub(r"[•☐○◉▣]\s*", "", result)
    result = re.sub(r"\s*[•☐○◉▣]\s*", " ", result)

    return result.strip()


def split_into_sentences(text: str, max_len: int = 45) -> list[str]:
    """
    Split Chinese text into spoken-style sentences (~20-45 chars each).
    Tries to preserve natural breaks (。！？) first, then character count.
    """
    if not text:
        return []

    sentences = []
    raw_sentences = re.split(r'(?<=[。！？])', text)

    for part in raw_sentences:
        if not part:
            continue
        part = part.strip()
        if not part:
            continue

        if len(part) <= max_len:
            if part:
                sentences.append(part)
        else:
            while len(part) > max_len:
                bp = max_len
                for i in range(max_len - 10, max_len):
                    if part[i:i+1] in "，、的了是就有也在和與或":
                        bp = i + 1
                        break
                sentences.append(part[:bp].strip())
                part = part[bp:]
            if part.strip():
                sentences.append(part.strip())

    sentences = [s for s in sentences if len(s) >= 10 or re.search(r'[。！？]+$', s)]
    return sentences


def distribute_sentences_to_steps(sentences: list[str], num_steps: int = 3) -> list[list[str]]:
    """
    Distribute sentences across steps, with each step getting ~equal sentences.
    Returns: [[step1_sentences], [step2_sentences], [step3_sentences]]
    """
    if not sentences:
        return [[] for _ in range(num_steps)]

    # Calculate chars per step target (aim for ~150-300 chars per step)
    total_chars = sum(len(s) for s in sentences)
    target_chars_per_step = min(300, max(150, total_chars // num_steps))

    steps = [[] for _ in range(num_steps)]
    step_char_counts = [0] * num_steps
    current_step = 0

    for sentence in sentences:
        s_len = len(sentence)

        # If current step is getting full, move to next
        if step_char_counts[current_step] + s_len > target_chars_per_step * 1.3:
            if current_step < num_steps - 1:
                current_step += 1

        steps[current_step].append(sentence)
        step_char_counts[current_step] += s_len

    # Ensure each step has at least 1 sentence
    for i in range(num_steps):
        if not steps[i]:
            # Steal from previous step if available
            if i > 0 and steps[i-1]:
                stolen = steps[i-1].pop()
                steps[i].append(stolen)
            elif i < num_steps - 1 and steps[i+1]:
                stolen = steps[i+1].pop(0)
                steps[i].append(stolen)

    return steps


def adapt_to_cantonese(text: str) -> str:
    """
    Adapt text to natural Cantonese spoken style.
    - Replace 非常 → 好/幾
    - Replace 我們 → 我哋
    - Add 啦, 呀, 囉, 喎, 吖 particles where natural
    - Shorten some formal phrases
    """
    if not text:
        return text

    # Simple substitutions (these are common)
    replacements = [
        (r'我們', '我哋'),
        (r'非常', '好'),
        (r'特別是', '尤其是'),
        (r'也就是說', '即係'),
        (r'也就是', '即係'),
        (r'因此', '所以'),
        (r'但是', '但係'),
        (r'可以說', '可以話'),
    ]

    result = text
    for old, new in replacements:
        result = re.sub(old, new, result)

    # Add final particle to sentences that sound more natural with one
    if result and result[-1] not in "。！？啦呀囉吖":
        if len(result) > 10 and result[-1] not in "，。！？":
            if result[-1] == '的':
                result = result[:-1] + '嘅'
            elif result[-1] == '了':
                pass
            elif '的' in result:
                result += '囉'

    return result


def adapt_to_cantonese_full(text: str) -> str:
    """Full Cantonese adaptation including broader 特別→尤其 replacement."""
    if not text:
        return text
    result = adapt_to_cantonese(text)
    # Apply broader 特別→尤其 replacement (catches 特別重要, 特別注意, etc.)
    result = re.sub(r'特別([^是])', r'尤其\1', result)
    return result


MAX_NARRATION_STRINGS = 12

def generate_narrations_ts(step_sentences: list[list[str]]) -> str:
    # Flatten all sentences, cap at MAX_NARRATION_STRINGS
    all_sentences = []
    for sentences in step_sentences:
        for sentence in sentences:
            if len(all_sentences) >= MAX_NARRATION_STRINGS:
                break
            sentence = adapt_to_cantonese_full(sentence)
            escaped = sentence.replace('"', '\\"')
            all_sentences.append(f'  "{escaped}",')
        if len(all_sentences) >= MAX_NARRATION_STRINGS:
            break

    lines = [
        'import type { Narration } from "../types";',
        "",
        "export const NARRATIONS: Narration[] = [",
        *all_sentences,
        "];",
    ]

    return "\n".join(lines)


def expand_narrations(
    blog_content: str,
    search_facts: list[str],
    num_steps: int = 3
) -> str:
    """
    Main function: combine blog content + search facts, generate narrations.ts.

    Returns: TypeScript source for narrations.ts
    """
    # Apply Cantonese substitution FIRST (before noise removal so replacements work)
    if blog_content:
        blog_content = adapt_to_cantonese_full(blog_content)
    if search_facts:
        search_facts = [adapt_to_cantonese_full(f) for f in search_facts]

    # Clean noise from blog and search content
    if blog_content:
        blog_content = clean_content(blog_content)
    if search_facts:
        search_facts = [clean_content(f) for f in search_facts if clean_content(f)]

    # Combine content sources (blog first, then search facts if available)
    all_content = []
    if blog_content:
        all_content.append(blog_content)
    if search_facts:
        all_content.append("\n".join(search_facts))

    def find_smart_truncate(text: str, max_len: int = 800) -> str:
        if len(text) <= max_len:
            return text
        segment = text[max_len - 100 : max_len]
        for i in range(len(segment) - 1, -1, -1):
            if segment[i] in "。！？\n":
                return text[: max_len - 100 + i + 1]
        for i in range(len(segment) - 1, -1, -1):
            if segment[i] in "、的了是就有也在和與或":
                return text[: max_len - 100 + i + 1]
        return text[:max_len]


    # Process blog sentences (strict filter: require 。！？)
    blog_sentences = []
    if blog_content:
        blog_combined = blog_content
        if len(blog_combined) > 800:
            blog_combined = find_smart_truncate(blog_combined, 800) + " "
        raw = split_into_sentences(blog_combined, max_len=45)
        blog_sentences = [s for s in raw if re.search(r'[。！？]+$', s)]

    # Process search facts separately (no 。！？ requirement — factual statements)
    fact_sentences = [f for f in search_facts if len(f) >= 10]

    # Fallback chain: blog → facts → emergency
    if not blog_sentences and not fact_sentences:
        return generate_narrations_ts([[], [], []])

    # Combine: prefer blog, fill gaps with facts
    sentences = blog_sentences[:]
    for f in fact_sentences:
        if len(sentences) >= 12:
            break
        if f not in sentences:
            sentences.append(f)

    # Distribute across steps
    step_sentences = distribute_sentences_to_steps(sentences, num_steps)

    return generate_narrations_ts(step_sentences)


def get_current_narrations_ts(filepath: str) -> list[str]:
    """Read existing narrations.ts, extract the strings."""
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract strings from the array
    strings = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith('"') and line.endswith('",'):
            strings.append(line[1:-2])  # Remove leading " and trailing ",

    return strings


def count_narrations_per_step(filepath: str) -> dict:
    """Count how many narration strings exist per step in current narrations.ts."""
    strings = get_current_narrations_ts(filepath)
    # We can't know exact step boundaries without reading the file,
    # so estimate based on string count
    return {"total": len(strings), "estimated_steps": len(strings) if len(strings) <= 3 else 3}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Expand narrations.ts from blog content")
    parser.add_argument("--blog", "-b", help="Blog section content (text)")
    parser.add_argument("--search", "-s", nargs="*", help="Search fact strings")
    parser.add_argument("--steps", "-n", type=int, default=3, help="Number of steps (default: 3)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample data")
    args = parser.parse_args()

    if args.demo:
        blog = """
        傳統習俗認為吉日結婚可增添福氣，父母長輩通常有特定要求。
        宜嫁娶的吉日需要配合雙方八字，選擇對雙方都有利的日子。
        中國傳統婚禮注重吉日選擇，這習俗已有數千年歷史。
        """
        search_facts = [
            "傳統結婚擇日要配合雙方八字",
            "香港仍保留傳統擇日習俗",
            "風水師傅收費由三千至數万元不等"
        ]
    else:
        blog = args.blog or ""
        search_facts = args.search or []

    result = expand_narrations(blog, search_facts, args.steps)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result + "\n")
        print(f"Written to {args.output}")
    else:
        print(result)


# Test with a sample
if __name__ == "__main__" and len(sys.argv) == 1:
    # Demo run
    blog = """
    傳統習俗認為吉日結婚可增添福氣，父母長輩通常有特定要求。
    宜嫁娶的吉日需要配合雙方八字，選擇對雙方都有利的日子。
    中國傳統婚禮注重吉日選擇，這習俗已有數千年歷史。
    現代香港新人仍重視擇日，但亦會考慮實際因素。
    """
    search_facts = [
        "傳統結婚擇日要配合雙方八字",
        "香港仍保留傳統擇日習俗",
        "風水師傅收費由三千至數万元不等"
    ]
    result = expand_narrations(blog, search_facts, num_steps=3)
    print(result)