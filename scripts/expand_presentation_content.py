#!/usr/bin/env python3
"""
expand_presentation_content.py — Main runner for presentation content expansion.

Phase 1: Pilot on presentation 04 only.
Phase 2: Batch 01-10.
Phase 3: 11-40.
"""

import os
import re
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Optional

# Add scripts dir to path so we can import the modules
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))


def run_command(cmd: list, description: str) -> bool:
    """Run a command and report success/failure."""
    print(f"\n>>> {description}")
    print(f"    {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.stdout:
            print(result.stdout[:500])
        if result.returncode != 0:
            print(f"WARNING: {description} returned code {result.returncode}")
            if result.stderr:
                print(f"  STDERR: {result.stderr[:200]}")
            return False
        return True
    except Exception as e:
        print(f"ERROR: {description} failed: {e}")
        return False


def ensure_blog_index(reparse: bool = False) -> dict:
    """Ensure blog_index.json exists (run parse_blog.py if needed)."""
    index_path = "scripts/blog_index.json"

    if reparse and os.path.exists(index_path):
        os.remove(index_path)

    if os.path.exists(index_path):
        print(f"Using existing blog index: {index_path}")
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)

    print("Blog index not found, running parse_blog.py...")
    success = run_command(
        [sys.executable, "scripts/parse_blog.py", "--blog-dir", "blog", "--output", index_path],
        "Parse blog articles"
    )

    if not success:
        print("ERROR: Failed to parse blog articles")
        return {}

    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_presentations(targets: list[str]) -> list[str]:
    """Find presentation directories matching targets (e.g., ['04', '06', 'all'])."""
    pres_dir = Path("presentations")
    if not pres_dir.exists():
        print(f"ERROR: presentations directory not found")
        return []

    if "all" in targets:
        # Get all numeric presentations
        presentations = []
        for d in sorted(pres_dir.iterdir()):
            if d.is_dir() and d.name[0].isdigit():
                presentations.append(d.name)
        return presentations

    # Match by prefix (e.g., "04" matches "04-auspicious-date-guide")
    presentations = []
    for target in targets:
        for d in sorted(pres_dir.iterdir()):
            if d.is_dir() and d.name.startswith(target):
                presentations.append(d.name)

    return sorted(set(presentations))


def find_chapters(pres_name: str) -> list[str]:
    """Find all chapter directories in a presentation."""
    pres_path = Path(f"presentations/{pres_name}/presentation/src/chapters")
    if not pres_path.exists():
        return []

    chapters = []
    for d in sorted(pres_path.iterdir()):
        if d.is_dir() and d.name[0].isdigit():
            chapters.append(d.name)

    return chapters


def find_narrations_file(chapter_dir: str) -> Optional[str]:
    """Find narrations.ts in a chapter directory."""
    chapter_path = Path(chapter_dir)
    narrations = chapter_path / "narrations.ts"
    if narrations.exists():
        return str(narrations)

    # Maybe in a src/ subdirectory
    for sub in ["src", "components"]:
        narrations = chapter_path / sub / "narrations.ts"
        if narrations.exists():
            return str(narrations)

    return None


def find_tsx_files(chapter_dir: str) -> list[str]:
    """Find all tsx files in a chapter directory."""
    chapter_path = Path(chapter_dir)
    tsx_files = []

    for pattern in ["*.tsx", "src/*.tsx", "components/*.tsx"]:
        tsx_files.extend(chapter_path.glob(pattern))

    return [str(f) for f in sorted(tsx_files)]


def get_chapter_topic(chapter_dir: str, pres_name: str) -> str:
    chapter_name = Path(chapter_dir).name
    chapter_slug = re.sub(r'^\d+[-_]', '', chapter_name)

    # Try outline.md first (has chapter descriptions like "結婚資格與文件")
    pres_dir = Path(chapter_dir).parent.parent.parent.parent
    outline_file = pres_dir / "outline.md"
    chapter_num_match = re.match(r'^(\d+)', chapter_name)
    chapter_num = int(chapter_num_match.group(1)) if chapter_num_match else None

    if outline_file.exists():
        try:
            with open(outline_file, "r", encoding="utf-8") as f:
                outline_content = f.read()
            for line in outline_content.split('\n'):
                # Match "## N. slug — desc" or "## Chapter N: desc"
                m = re.match(r'^## (\d+)\.\s+\S+\s*[-—]\s*(.+?)(?:\s*\(|\s*\[|$)', line)
                if not m:
                    m = re.match(r'^## Chapter (\d+):\s*(.+?)\s*\(', line)
                if m:
                    line_num = m.group(1)
                    desc = m.group(2).strip()
                    if int(line_num) == chapter_num and desc and len(desc) >= 3:
                        return desc
        except Exception:
            pass

    # Try h1/h2/h3 from tsx files
    tsx_files = find_tsx_files(chapter_dir)
    for tsx_file in tsx_files:
        try:
            with open(tsx_file, "r", encoding="utf-8") as f:
                content = f.read()
            for tag in ['h1', 'h2', 'h3']:
                for cls in [None, 'el-step-title', 'el-transition-title', 'step-title']:
                    if cls:
                        pattern = rf'<{tag}[^>]*class="[^"]*{re.escape(cls)}[^"]*"[^>]*>([^<]+)</{tag}>'
                    else:
                        pattern = rf'<{tag}[^>]*>([^<]+)</{tag}>'
                    m = re.search(pattern, content)
                    if m:
                        topic = m.group(1).strip()
                        if topic and len(topic) >= 3 and re.search(r'[\u4e00-\u9fff]', topic):
                            return topic
        except Exception:
            continue

    return chapter_slug


def should_skip_chapter(chapter_name: str) -> bool:
    """Skip coldopen (01) and cta (06) chapters - they don't need content expansion."""
    return chapter_name in ("01-coldopen", "06-cta")


def get_matched_blog_content(pres_name: str, chapter_topic: str, blog_index: dict) -> str:
    """Get the best matched blog content for a chapter."""
    from match_blog_to_chapter import match_chapter_to_blog, get_chapter_content_from_blog

    # Find matching blog file
    match = match_chapter_to_blog(chapter_topic, blog_index, pres_name)

    if not match or not match["blog_file"]:
        return ""

    blog_file = match["blog_file"]

    # Get content
    content = get_chapter_content_from_blog(blog_file, chapter_topic, blog_index)

    return content


def process_chapter(
    pres_name: str,
    chapter_dir: str,
    blog_index: dict,
    use_search: bool = True,
    dry_run: bool = False
) -> dict:
    """
    Process a single chapter: expand narrations.ts and tsx bullets.

    Returns: {"narrations_updated": bool, "tsx_updated": int, "used_search": bool}
    """
    results = {"narrations_updated": False, "tsx_updated": 0, "used_search": False}

    chapter_path = Path(chapter_dir)
    chapter_topic = get_chapter_topic(chapter_dir, pres_name)
    chapter_name = chapter_path.name

    print(f"\n  Processing chapter: {chapter_name}")
    print(f"    Topic: {chapter_topic}")

    # Step 1: Get matched blog content
    blog_content = get_matched_blog_content(pres_name, chapter_topic, blog_index)
    blog_chars = len(blog_content)
    print(f"    Blog content: {blog_chars} chars")

    # Step 1.5: Search fallback if blog is thin
    search_facts = []
    if use_search and blog_chars < 200:
        print(f"    Blog content thin ({blog_chars} < 200), triggering search...")
        from search_supplement import search_chapter, synthesize_narration_sentences

        result = search_chapter(pres_name, chapter_name, chapter_topic)
        if result["success"]:
            search_facts = result["facts"]
            results["used_search"] = True
            print(f"    Search found {len(search_facts)} facts")

    # Step 2: Expand narrations.ts
    narrations_file = find_narrations_file(chapter_dir)
    if narrations_file:
        print(f"    Found narrations: {narrations_file}")

        # Read current content
        with open(narrations_file, "r", encoding="utf-8") as f:
            current_content = f.read()

        # Count existing narration strings
        existing_strings = re.findall(r'"([^"]+)"', current_content)
        existing_strings = [s for s in existing_strings if not s.startswith('../') and not s.startswith('import')]

        if len(existing_strings) >= 2:
            print(f"    Skipping: already has {len(existing_strings)} strings")
        else:
            from expand_narrations import expand_narrations
            new_narrations = expand_narrations(blog_content, search_facts, num_steps=3)
            new_strings = re.findall(r'"([^"]+)"', new_narrations)
            new_strings = [s for s in new_strings if not s.startswith('../') and not s.startswith('import')]
            write_new = len(new_strings) >= len(existing_strings) and len(new_strings) >= 1

            if not dry_run:
                backup_file = narrations_file + ".expanded.bak"
                with open(backup_file, "w", encoding="utf-8") as f:
                    f.write(current_content)
                if write_new:
                    with open(narrations_file, "w", encoding="utf-8") as f:
                        f.write(new_narrations)
                    results["narrations_updated"] = True
                    print(f"    Updated narrations.ts ({len(new_strings)} strings)")
                else:
                    print(f"    Skipped: generated only {len(new_strings)} strings, keeping original ({len(existing_strings)})")
            else:
                status = "Would update" if write_new else "Would skip"
                print(f"    [DRY RUN] {status} ({len(new_strings)} vs {len(existing_strings)} strings)")
    else:
        # No existing narrations.ts — construct the expected path and create it
        new_narrations_path = f"{chapter_dir}/narrations.ts"
        print(f"    Creating new narrations: {new_narrations_path}")

        from expand_narrations import expand_narrations
        new_narrations = expand_narrations(blog_content, search_facts, num_steps=3)
        new_strings = re.findall(r'"([^"]+)"', new_narrations)
        new_strings = [s for s in new_strings if not s.startswith('../') and not s.startswith('import')]
        write_new = len(new_strings) >= 1

        if not dry_run:
            if write_new:
                with open(new_narrations_path, "w", encoding="utf-8") as f:
                    f.write(new_narrations)
                results["narrations_updated"] = True
                print(f"    Created narrations.ts ({len(new_strings)} strings)")
            else:
                print(f"    Skipped: generated {len(new_strings)} strings (need >= 1)")
        else:
            print(f"    [DRY RUN] Would create narrations.ts ({len(new_strings)} strings)")

    # Step 3: Expand tsx bullets
    tsx_files = find_tsx_files(chapter_dir)
    print(f"    Found {len(tsx_files)} tsx files")

    for tsx_file in tsx_files:
        tsx_name = Path(tsx_file).name
        print(f"    Processing {tsx_name}")

        # Read current bullets
        from expand_tsx_bullets import extract_tsx_bullets, expand_bullet_list, generate_updated_tsx

        bullets = extract_tsx_bullets(tsx_file)

        if bullets:
            # Expand bullets
            enhanced_bullets = expand_bullet_list(bullets, blog_content, num_bullets=len(bullets))

            if not dry_run:
                # Read full tsx
                with open(tsx_file, "r", encoding="utf-8") as f:
                    tsx_content = f.read()

                # Backup
                backup_file = tsx_file + ".expanded.bak"
                with open(backup_file, "w", encoding="utf-8") as f:
                    f.write(tsx_content)

                # Update
                new_tsx_content = generate_updated_tsx(tsx_content, enhanced_bullets)
                with open(tsx_file, "w", encoding="utf-8") as f:
                    f.write(new_tsx_content)

                results["tsx_updated"] += 1
                print(f"      Updated {tsx_name} ({len(enhanced_bullets)} bullets)")
            else:
                print(f"      [DRY RUN] Would update {tsx_name}:")
                for b in enhanced_bullets[:2]:
                    print(f"        {b[:50]}")

    return results


def process_presentation(
    pres_name: str,
    blog_index: dict,
    use_search: bool = True,
    dry_run: bool = False
) -> dict:
    """Process all chapters in a presentation."""
    print(f"\n{'='*60}")
    print(f"PROCESSING: {pres_name}")
    print(f"{'='*60}")

    chapters = find_chapters(pres_name)
    print(f"Found {len(chapters)} chapters: {chapters}")

    total_results = {"narrations_updated": 0, "tsx_updated": 0, "used_search": False}

    for chapter_name in chapters:
        if should_skip_chapter(chapter_name):
            print(f"\n  Skipping {chapter_name} (coldopen/cta)")
            continue

        chapter_dir = f"presentations/{pres_name}/presentation/src/chapters/{chapter_name}"

        result = process_chapter(pres_name, chapter_dir, blog_index, use_search, dry_run)

        if result["narrations_updated"]:
            total_results["narrations_updated"] += 1
        total_results["tsx_updated"] += result["tsx_updated"]
        if result["used_search"]:
            total_results["used_search"] = True

    return total_results


def main():
    parser = argparse.ArgumentParser(description="Expand presentation content from blog + search")
    parser.add_argument("presentations", nargs="*", default=["04"], help="Presentation numbers (default: 04)")
    parser.add_argument("--all", action="store_true", help="Process all presentations")
    parser.add_argument("--no-search", action="store_true", help="Skip web search fallback")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no file writes")
    parser.add_argument("--reparse", action="store_true", help="Force re-parse of blog articles")
    args = parser.parse_args()

    # Handle targets
    if args.all:
        targets = ["all"]
    elif args.presentations:
        targets = args.presentations
    else:
        targets = ["04"]

    # Find presentations to process
    presentations = find_presentations(targets)
    if not presentations:
        print(f"ERROR: No presentations found for: {targets}")
        sys.exit(1)

    print(f"Will process: {presentations}")

    # Ensure blog index
    blog_index = ensure_blog_index(reparse=args.reparse)
    if not blog_index:
        print("ERROR: Failed to load blog index")
        sys.exit(1)

    print(f"\nBlog index loaded: {len(blog_index)} articles")

    # Process each presentation
    for pres_name in presentations:
        result = process_presentation(
            pres_name,
            blog_index,
            use_search=not args.no_search,
            dry_run=args.dry_run
        )

        print(f"\nResults for {pres_name}:")
        print(f"  Narrations updated: {result['narrations_updated']} chapters")
        print(f"  TSX files updated: {result['tsx_updated']}")
        print(f"  Search used: {result['used_search']}")

    print(f"\n{'='*60}")
    print("PIPELINE COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()