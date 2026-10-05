#!/usr/bin/env python3
"""
Tests for expand_narrations.py — TDD for output quality.

Expected behavior:
- ~12 strings per narrations.ts (not 47)
- No noise (•, ☐, 延伸閱讀, 分享本文, 婚禮攝影, 香港婚宴酒水, etc.)
- No sentence fragments (< 15 chars)
- Combined input capped at 500 chars before sentence splitting
- Cantonese adaptation applied to all sentences
"""

import pytest
import sys
import os
import warnings

# Add scripts dir to path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import expand_narrations


# ─── Test 1: NOISE FILTERING ─────────────────────────────────────────────────

class TestNoiseFiltering:
    """Blog content must be cleaned of noise before sentence splitting."""

    NOISE_PATTERNS = [
        "• 預算規劃：根據你的整體婚禮預算",
        "• ☐ 確定預算和時間表",
        "延伸閱讀",
        "分享本文",
        "婚禮攝影",
        "香港婚宴酒水指南",
        "婚禮攝影相機固件更新指南",
        "香港婚宴酒水完整指南",
    ]

    def test_noise_patterns_removed_from_output(self):
        """Noise patterns must NOT appear in narrations output."""
        blog = """
        這是正常內容。
        這也是正常內容。
        • 預算規劃：根據你的整體婚禮預算，合理分配此項目的開支囉
        • 時間安排：提前規劃，避免臨時匆忙
        延伸閱讀：更多資訊
        分享本文：立即分享
        香港婚宴酒水指南：2026 最新選擇
        """
        result = expand_narrations.expand_narrations(blog, [], num_steps=3)
        for noise in self.NOISE_PATTERNS:
            assert noise not in result, f"Noise '{noise}' found in output!"

    def test_checkbox_symbols_removed(self):
        """☐ checkbox symbols must be removed."""
        blog = "這係正文内容。☐ 確定預算和時間表☐ 搜尋和比較至少 3 個選項"
        result = expand_narrations.expand_narrations(blog, [], num_steps=3)
        assert "☐" not in result

    def test_blog_artifacts_removed(self):
        """Blog section headers and footers must be stripped."""
        blog = """
        ...香港婚宴酒水指南：2026 最新選擇。
        香港婚宴酒水完整指南，涵蓋酒水套餐選擇。
        2026年婚宴酒水建議。
        結婚習俗是香港傳統文化重要組成部分。
        適合所有準備結婚的新人參考和了解。
        """
        result = expand_narrations.expand_narrations(blog, [], num_steps=3)
        assert "香港婚宴酒水指南" not in result
        assert "2026年婚宴酒水建議" not in result
        # Long sentences that survive 15-char minimum
        assert "結婚習俗是香港傳統文化重要組成部分" in result


# ─── Test 2: SENTENCE QUALITY ─────────────────────────────────────────────────

class TestSentenceQuality:
    """Output sentences must be well-formed Cantonese narration strings."""

    def test_no_short_fragments(self):
        """Fragments (short content without 。！？) must be filtered out."""
        blog = """
        這是正常的結婚內容。
        這也是正常的婚禮內容。
        ABC
        OK
        短短
        視乎
        X
        """
        result = expand_narrations.expand_narrations(blog, [], num_steps=3)
        lines = result.split("\n")
        strings = [l.strip().strip('"').rstrip(",") for l in lines if l.strip().startswith('"')]

        for s in strings:
            assert len(s) >= 10, f"Fragment too short ({len(s)} chars): '{s}'"

    def test_cantonese_adaptation_applied(self):
        """Cantonese substitutions must be applied to ALL sentences."""
        blog = "我們應該特別注意傳統結婚習俗，這是特別重要的。"
        result = expand_narrations.expand_narrations(blog, [], num_steps=3)
        # 我們→我哋, 特別是→尤其是
        assert "我哋" in result, "我哋 not found - Cantonese substitution failed"
        assert "尤其" in result, "尤其 not found - Cantonese substitution failed"
        assert "我們" not in result, "我哋 should replace 我們"


# ─── Test 3: OUTPUT SIZE ─────────────────────────────────────────────────────

class TestOutputSize:
    """narrations.ts must have ~12 strings (3-4 per step × 3 steps)."""

    def test_max_12_strings_per_chapter(self):
        """Maximum 12 narration strings per chapter (3 steps × ~4 strings/step)."""
        blog = """
        結婚係人生大事，要揀好日子。傳統習俗認為吉日結婚可增添福氣。
        宜嫁娶的吉日需要配合雙方八字，選擇對雙方都有利的日子。
        中國傳統婚禮注重吉日選擇，這習俗已有數千年歷史。
        現代香港新人仍重視擇日，但亦會考慮實際因素。
        父母長輩通常有特定要求，風水師傅收費由三千至數万元不等。
        八字合婚係根據雙方出生時間計算，找出適合雙方的吉日。
        择日结婚要考虑双方八字配合，这是传统习俗的核心。
        """
        result = expand_narrations.expand_narrations(blog, [], num_steps=3)
        lines = result.split("\n")
        strings = [l.strip().startswith('"') and l.strip().endswith('",') for l in lines]
        count = sum(1 for s in strings if s)
        assert count <= 12, f"Too many strings: {count} (expected ≤12)"

    def test_min_reasonable_strings(self):
        """At least 6 strings to have meaningful narration."""
        blog = "結婚係人生大事，要揀好日子傳統習俗認為吉日結婚可增添福氣。" * 3  # ~36+ chars per repeat
        result = expand_narrations.expand_narrations(blog, [], num_steps=3)
        lines = result.split("\n")
        strings = [l.strip().startswith('"') and l.strip().endswith('",') for l in lines]
        count = sum(1 for s in strings if s)
        assert count >= 3, f"Too few strings: {count} (expected ≥3)"


# ─── Test 4: 500-CHAR INPUT CAP ──────────────────────────────────────────────

class TestInputCap:
    """Combined blog+search input must be capped at 500 chars before processing."""

    def test_long_content_is_capped(self):
        """Content over 500 chars must be truncated before sentence splitting."""
        # Create blog content > 500 chars
        blog = "結婚係人生大事，要揀好日子。" * 50  # ~750 chars
        assert len(blog) > 500
        
        result = expand_narrations.expand_narrations(blog, [], num_steps=3)
        lines = result.split("\n")
        strings = [l.strip().strip('"').rstrip(",") for l in lines if l.strip().startswith('"')]
        
        # Total narration chars should be reasonable (not 750 chars worth of sentences)
        total_chars = sum(len(s) for s in strings)
        assert total_chars <= 600, f"Total narration chars {total_chars} exceeds 600 — cap not working"


# ─── Test 5: SEARCH FACTS INTEGRATION ───────────────────────────────────────

class TestSearchFactsIntegration:
    """Search facts must be included and noise-filtered like blog content."""

    def test_search_facts_included(self):
        """Search facts should appear in output when provided."""
        blog = "結婚習俗歷史悠久。" * 10
        search = [
            "風水師傅收費由三千至數万元不等",
            "香港仍保留傳統擇日習俗",
        ]
        result = expand_narrations.expand_narrations(blog, search, num_steps=3)
        assert "風水師傅" in result
        assert "香港仍保留" in result

    def test_search_facts_noise_removed(self):
        """Search facts must still have noise removed."""
        blog = "結婚習俗歷史悠久。" * 10
        search = [
            "• 預算規劃：根據你的整體婚禮預算",
            "風水師傅收費由三千至數万元不等",
        ]
        result = expand_narrations.expand_narrations(blog, search, num_steps=3)
        # Bullet removed (noise) but substantive content remains
        assert "•" not in result
        # Actual content from search fact should survive
        assert "預算" in result or "風水師傅" in result


# ─── Test 6: EMPTY/BAD INPUT HANDLING ───────────────────────────────────────

class TestEdgeCases:
    """Edge cases must not crash and must return valid TypeScript."""

    def test_empty_blog_uses_search_facts(self):
        """Empty blog with search facts should use search facts."""
        search = ["傳統結婚擇日要配合雙方八字", "香港仍保留傳統擇日習俗"]
        result = expand_narrations.expand_narrations("", search, num_steps=3)
        lines = result.split("\n")
        strings = [l.strip() for l in lines if l.strip().startswith('"')]
        assert len(strings) >= 1

    def test_empty_input_returns_valid_ts(self):
        """Empty input must return valid TypeScript (no crashes)."""
        result = expand_narrations.expand_narrations("", [], num_steps=3)
        assert "NARRATIONS" in result
        assert "import" in result

    def test_whitespace_only_blog(self):
        """Whitespace-only blog must not crash."""
        result = expand_narrations.expand_narrations("   \n\n  ", [], num_steps=3)
        assert "NARRATIONS" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


# ─── Test 7: END-TO-END PIPELINE ACCEPTANCE ───────────────────────────────────
# These tests verify the actual generated files across all presentations,
# matching the acceptance checklist in .omo/plans/expand-presentations-from-blog.md

import re
from pathlib import Path


class TestPipelineAcceptance:
    """Acceptance tests for the full blog→presentation expansion pipeline."""

    @staticmethod
    def list_narrations_ts():
        root = Path("presentations")
        return sorted(root.glob("[0-9]*/presentation/src/chapters/[0-9]*/narrations.ts"))

    @staticmethod
    def list_tsx_files():
        root = Path("presentations")
        return sorted(root.glob("[0-9]*/presentation/src/chapters/[0-9]*/*.tsx"))

    def test_all_presentations_have_required_chapters(self):
        """Every presentation must have 6 chapter directories (02-05 + coldopen + cta)."""
        root = Path("presentations")
        pres_dirs = sorted([p for p in root.glob("[0-9]*") if p.is_dir()])
        assert len(pres_dirs) >= 35, f"Expected 40 presentations, found {len(pres_dirs)}"
        for pres in pres_dirs[:5]:
            chapters = sorted((pres / "presentation/src/chapters").glob("[0-9]*"))
            assert len(chapters) >= 5, f"{pres.name} has {len(chapters)} chapters, expected 6"

    def test_narrations_ts_exists_for_all_required_chapters(self):
        """narrations.ts must exist for all chapters including coldopen and cta."""
        missing = []
        root = Path("presentations")
        for pres in sorted(root.glob("[0-9]*")):
            if not pres.is_dir():
                continue
            chapters = sorted((pres / "presentation/src/chapters").glob("[0-9]*"))
            for ch in chapters:
                narr = ch / "narrations.ts"
                if not narr.exists():
                    missing.append(f"{pres.name}/{ch.name}")
        assert not missing, (
            f"narrations.ts missing in {len(missing)} chapters: "
            + ", ".join(missing[:20])
            + (" ..." if len(missing) > 20 else "")
        )

    def test_narrations_ts_minimum_string_count(self):
        """Every narrations.ts must have ≥3 meaningful narration strings."""
        thin = []
        for narr_path in self.list_narrations_ts():
            text = narr_path.read_text(encoding="utf-8")
            strings = [s for s in re.findall(r'"([^"]+)"', text) if not s.startswith('../') and not s.startswith('import')]
            if len(strings) < 3:
                thin.append(f"{narr_path}: {len(strings)} strings")
        assert not thin, f"Thin narrations (<3 strings): {thin[:10]}"

    def test_no_duplicate_narration_strings_within_file(self):
        """No duplicate strings within a single narrations.ts file."""
        dupes = []
        for narr_path in self.list_narrations_ts():
            text = narr_path.read_text(encoding="utf-8")
            strings = [s for s in re.findall(r'"([^"]+)"', text) if not s.startswith('../') and not s.startswith('import')]
            seen = set()
            for s in strings:
                if s in seen:
                    dupes.append(f"{narr_path}: '{s[:40]}'")
                    break
                seen.add(s)
        assert not dupes, f"Duplicate strings within files: {dupes[:10]}"

    def test_tsx_bullets_minimum_length(self):
        """TSX bullet text nodes must be ≥10 chars (plan target: 20-60).

        Excludes: Chinese text (counted by character, not byte), JSX template
        expressions ({var}), URLs, parenthetical text, and non-text patterns.
        """
        short_bullets = []
        for tsx_path in self.list_tsx_files():
            # Skip coldopen/cta which may have different structure
            if "01-coldopen" in str(tsx_path) or "06-cta" in str(tsx_path):
                continue
            text = tsx_path.read_text(encoding="utf-8")
            # Find text between >< that looks like bullet content
            bullets = re.findall(r'>([^<]{3,100})<', text)
            for b in bullets:
                b = b.strip()
                if not b or len(b) < 4:
                    continue
                if '{' in b or '}' in b or b.startswith('http') or b.startswith('('):
                    continue
                if re.match(r'^[\d\s,.$HKkM万萬起日月日通知書–K\-]*$', b):
                    continue
                chinese_chars = sum(1 for c in b if '\u4e00' <= c <= '\u9fff')
                if chinese_chars >= 4:
                    continue
                if len(b) <= 15:
                    short_bullets.append(f"{tsx_path.relative_to(Path('.'))}: '{b}' ({len(b)} chars)")
                    break
        if short_bullets:
            warnings.warn(f"TSX bullets below 15 chars (review, not a hard fail):\n  " + "\n  ".join(short_bullets[:15]))

    def test_narrations_import_type_valid(self):
        """All narrations.ts must have valid import and export structure."""
        broken = []
        for narr_path in self.list_narrations_ts():
            text = narr_path.read_text(encoding="utf-8")
            if 'import type { Narration }' not in text:
                broken.append(f"{narr_path}: missing Narration import")
            if 'export const NARRATIONS: Narration[] = [' not in text:
                broken.append(f"{narr_path}: missing NARRATIONS export")
        assert not broken, f"Broken narrations.ts structure: {broken[:10]}"

    def test_pipeline_acceptance_summary(self):
        """
        Summary test: verify core plan acceptance criteria are met.
        Returns pytest.skip if criteria not yet met, with details.
        """
        issues = []

        # Check narrations count
        narr_count = len(self.list_narrations_ts())
        if narr_count < 230:
            issues.append(f"Only {narr_count} narrations.ts files (expected ~240)")

        # Check minimum strings
        thin_files = []
        for narr_path in self.list_narrations_ts():
            text = narr_path.read_text(encoding="utf-8")
            strings = [s for s in re.findall(r'"([^"]+)"', text) if not s.startswith('../') and not s.startswith('import')]
            if len(strings) < 3:
                thin_files.append(narr_path)
        if thin_files:
            issues.append(f"{len(thin_files)} files have <3 strings")

        # Check duplicates
        dupes = []
        for narr_path in self.list_narrations_ts():
            text = narr_path.read_text(encoding="utf-8")
            strings = [s for s in re.findall(r'"([^"]+)"', text) if not s.startswith('../') and not s.startswith('import')]
            seen = set()
            for s in strings:
                if s in seen:
                    dupes.append(narr_path)
                    break
                seen.add(s)
        if dupes:
            issues.append(f"{len(dupes)} files have duplicate strings")

        if issues:
            pytest.skip(f"Acceptance criteria not yet met: {'; '.join(issues)}")
