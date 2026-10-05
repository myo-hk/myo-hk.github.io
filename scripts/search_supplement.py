#!/usr/bin/env python3
"""search_supplement.py — Web search fallback for thin blog sections."""

import os
import sys
import json
import time
import random
import re
from typing import Optional
from urllib.parse import quote

# Use standard library as much as possible (no extra pip installs needed)
try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
except ImportError:
    print("ERROR: urllib not available", file=sys.stderr)
    sys.exit(1)


def build_search_query(pres_title: str, chapter_name: str, step_topic: str = "") -> str:
    """
    Build a search query from presentation + chapter info.
    Returns a query string ready for DuckDuckGo.
    """
    parts = []

    # Add presentation title keywords (strip common prefixes like "04-", "結婚")
    clean_title = re.sub(r"^\d+[-_]", "", pres_title)
    if clean_title:
        parts.append(clean_title)

    # Add chapter name
    if chapter_name:
        parts.append(chapter_name)

    # Add step topic if provided
    if step_topic:
        parts.append(step_topic)

    query = " ".join(parts)

    # Add Hong Kong specificity
    if "香港" not in query:
        query += " 香港"

    return query.strip()


def fetch_duckduckgo(query: str, num_results: int = 5) -> list[dict]:
    """
    Fetch search results from DuckDuckGo HTML (no API key needed).
    Returns: [{"title": "...", "snippet": "..."}, ...]
    """
    # Polite rate limiting
    time.sleep(0.5)

    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-HK,zh-TW,zh;q=0.9,en;q=0.8",
    }

    req = Request(url, headers=headers)

    try:
        response = urlopen(req, timeout=10)
        html = response.read().decode("utf-8", errors="replace")
    except (URLError, HTTPError, TimeoutError) as e:
        print(f"  WARNING: Search failed for '{query}': {e}", file=sys.stderr)
        return []

    # Parse results
    results = []
    # DuckDuckGo HTML result format
    result_pattern = re.compile(
        r'<a class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?'
        r'<a class="result__snippet"[^>]*>(.*?)</a>',
        re.DOTALL
    )

    # Simpler parsing: find result blocks
    # Split by result blocks
    blocks = re.split(r'<div class="result"', html)

    for block in blocks[1:num_results+1]:  # Skip first (empty), take num_results
        try:
            # Extract title
            title_match = re.search(r'<a class="result__a"[^>]*>(.*?)</a>', block, re.DOTALL)
            title = title_match.group(1) if title_match else ""
            title = re.sub(r'<[^>]+>', "", title).strip()

            # Extract snippet
            snippet_match = re.search(r'<a class="result__snippet"[^>]*>(.*?)</a>', block, re.DOTALL)
            snippet = snippet_match.group(1) if snippet_match else ""
            snippet = re.sub(r'<[^>]+>', "", snippet).strip()

            # Extract URL
            url_match = re.search(r'href="(https?://[^"]*)"', block)
            url = url_match.group(1) if url_match else ""

            if title and snippet:
                results.append({
                    "title": title,
                    "snippet": snippet,
                    "url": url
                })
        except Exception:
            continue

    # Also try the simpler result__title pattern
    if not results:
        # Try simpler pattern
        for match in re.finditer(r'<a class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL):
            title = re.sub(r'<[^>]+>', "", match.group(1)).strip()
            if title and len(title) > 5:
                # Try to get snippet after this
                pos = match.end()
                snippet_match = re.search(r'<p class="result__snippet">(.*?)</p>', html[pos:pos+500], re.DOTALL)
                snippet = snippet_match.group(1) if snippet_match else ""
                snippet = re.sub(r'<[^>]+>', "", snippet).strip()

                results.append({
                    "title": title,
                    "snippet": snippet[:300],
                    "url": ""
                })
                if len(results) >= num_results:
                    break

    return results[:num_results]


def extract_facts_from_results(results: list[dict], query: str) -> list[str]:
    """
    Extract factual statements from search results.
    Returns a list of factual sentences suitable for narration.
    """
    facts = []

    for r in results:
        snippet = r.get("snippet", "")
        if not snippet:
            continue

        # Clean HTML
        snippet = re.sub(r'<[^>]+>', "", snippet)

        # Split by sentence-ending punctuation
        sentences = re.split(r'[。！？\n]', snippet)
        for sent in sentences:
            sent = sent.strip()
            if len(sent) > 15 and len(sent) < 200:
                # Filter for factual content (numbers, specific terms)
                if any(c in sent for c in "（）「」『』0123456789一二三四五六七八九十"):
                    facts.append(sent)

    # Deduplicate similar facts
    unique_facts = []
    for f in facts:
        # Skip if too similar to existing
        if not any(f[:30] in uf[:30] for uf in unique_facts):
            unique_facts.append(f)

    return unique_facts[:5]  # Max 5 facts


def search_chapter(pres_title: str, chapter_name: str, step_topic: str = "") -> dict:
    """
    Perform search for a chapter's supplementary content.
    Returns: {"query": "...", "results": [...], "facts": [...], "success": bool}
    """
    query = build_search_query(pres_title, chapter_name, step_topic)
    print(f"  Searching: {query}")

    results = fetch_duckduckgo(query, num_results=5)

    if not results:
        print(f"  No results found")
        return {"query": query, "results": [], "facts": [], "success": False}

    facts = extract_facts_from_results(results, query)
    print(f"  Found {len(results)} results, extracted {len(facts)} facts")

    return {
        "query": query,
        "results": results,
        "facts": facts,
        "success": True
    }


def synthesize_narration_sentences(facts: list[str], topic: str, max_chars: int = 300) -> list[str]:
    """
    Convert factual search results into Cantonese-style narration sentences.
    """
    sentences = []
    current_chars = 0

    for fact in facts:
        if current_chars + len(fact) + 2 > max_chars:
            break

        # Clean and adapt to spoken style
        sentence = fact.strip()
        if sentence and sentence[-1] not in "。！？":
            sentence += "。"

        sentences.append(sentence)
        current_chars += len(sentence)

    return sentences


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Search supplement for thin blog sections")
    parser.add_argument("--query", "-q", help="Search query (for testing)")
    parser.add_argument("--title", "-t", default="測試標題", help="Presentation title")
    parser.add_argument("--chapter", "-c", default="測試章節", help="Chapter name")
    parser.add_argument("--step", "-s", default="", help="Step topic")
    args = parser.parse_args()

    if args.query:
        # Test mode
        results = fetch_duckduckgo(args.query)
        print(f"\nQuery: {args.query}")
        print(f"Results: {len(results)}")
        for r in results[:3]:
            print(f"  - {r['title']}")
            print(f"    {r['snippet'][:150]}...")
    else:
        result = search_chapter(args.title, args.chapter, args.step)
        print(f"\nQuery: {result['query']}")
        print(f"Success: {result['success']}")
        print(f"Facts found: {len(result['facts'])}")
        for i, fact in enumerate(result['facts'], 1):
            print(f"  {i}. {fact[:100]}")