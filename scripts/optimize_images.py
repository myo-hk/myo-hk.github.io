#!/usr/bin/env python3
"""
Batch image optimizer for MyO static site.
Compresses JPEG/WebP images in image/ directory.

Usage:
    python3 scripts/optimize_images.py                    # Optimize all images
    python3 scripts/optimize_images.py --dry-run           # Show what would be done
    python3 scripts/optimize_images.py --quality 75        # Custom quality

Requires: Pillow (pip3 install Pillow)
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
IMAGE_DIR = ROOT / "image"
DEFAULT_QUALITY = 70


def optimize_webp(source: str, output: str, quality: int = DEFAULT_QUALITY) -> int:
    """Convert/compress image to WebP at given quality. Returns output file size."""
    from PIL import Image
    img = Image.open(source)
    if img.mode == 'RGBA':
        img.save(output, 'WEBP', quality=quality)
    else:
        img = img.convert('RGB')
        img.save(output, 'WEBP', quality=quality)
    return os.path.getsize(output)


def optimize_jpeg(source: str, output: str, quality: int = DEFAULT_QUALITY) -> int:
    """Compress JPEG at given quality. Returns output file size."""
    from PIL import Image
    img = Image.open(source)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(output, 'JPEG', quality=quality, optimize=True)
    return os.path.getsize(output)


def main():
    quality = DEFAULT_QUALITY
    dry_run = False

    for arg in sys.argv[1:]:
        if arg == '--dry-run':
            dry_run = True
        elif arg.startswith('--quality='):
            quality = int(arg.split('=')[1])

    total_saved = 0
    for fpath in sorted(IMAGE_DIR.iterdir()):
        if fpath.suffix.lower() in ('.jpg', '.jpeg'):
            original = fpath.stat().st_size
            new_path = fpath.with_suffix('.webp')
            if dry_run:
                print(f"  [DRY RUN] {fpath.name}: {original // 1024} KB -> WebP")
            else:
                new_size = optimize_jpeg(str(fpath), str(new_path), quality)
                saved = original - new_size
                total_saved += saved
                print(f"  ok {fpath.name}: {original // 1024} KB -> {new_size // 1024} KB ({saved // 1024} KB saved)")
        elif fpath.suffix.lower() == '.webp':
            original = fpath.stat().st_size
            if dry_run:
                print(f"  [DRY RUN] {fpath.name}: {original // 1024} KB (re-compress to q{quality})")
            else:
                tmp = str(fpath) + ".tmp"
                optimize_webp(str(fpath), tmp, quality)
                new_size = os.path.getsize(tmp)
                if new_size < original:
                    os.replace(tmp, str(fpath))
                    saved = original - new_size
                    total_saved += saved
                    print(f"  ok {fpath.name}: {original // 1024} KB -> {new_size // 1024} KB ({saved // 1024} KB saved)")
                else:
                    os.remove(tmp)

    print(f"\nTotal saved: {total_saved // 1024} KB")


if __name__ == "__main__":
    main()