#!/usr/bin/env python3
"""
pytest suite for rename_brand.py.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import rename_brand as rb


class TestPhase1Anchors:
    """Phase 1 必須把視覺 wordmark 轉為 MyO! 且保留驚嘆號。"""

    @pytest.mark.parametrize("src,expected", [
        ('<img src="image/01_company_logo.webp" alt="My O! Logo" width="50">',
         '<img src="image/01_company_logo.webp" alt="MyO! Logo" width="50">'),
        ('<img src="image/01_company_logo.webp" alt="My O! logo" width="50">',
         '<img src="image/01_company_logo.webp" alt="MyO! logo" width="50">'),
        ('<span class="QTKDff text-rose-500">My O!</span>專屬結婚證書套',
         '<span class="QTKDff text-rose-500">MyO!</span>專屬結婚證書套'),
        ('<div class="brand">My O!</div>',
         '<div class="brand">MyO!</div>'),
        ('<meta name="apple-mobile-web-app-title" content="My O!">',
         '<meta name="apple-mobile-web-app-title" content="MyO!">'),
        ('<meta property="og:image:alt" content="My O! 證書套公司 Logo">',
         '<meta property="og:image:alt" content="MyO! 證書套公司 Logo">'),
    ])
    def test_phase1_anchored_contexts_keep_bang(self, src, expected):
        out, p1, p2, p3 = rb.apply_phases(src)
        assert p1 == 1, f"應由 Phase 1 處理一次，實際 p1={p1}"
        assert p2 == 0, f"Phase 1 產物不應被 Phase 2 再處理，實際 p2={p2}"
        assert out == expected

    def test_short_name_anchor_keeps_bang(self):
        """單獨驗證 short_name 錨點，避免與 name 欄位混在同一個案例。"""
        src = '{"name": "x", "short_name": "My O!"}'
        out, p1, p2, _ = rb.apply_phases(src)
        assert (p1, p2) == (1, 0)
        assert out == '{"name": "x", "short_name": "MyO!"}'

    def test_mixed_context_routes_each_field_to_correct_phase(self):
        """同一份 JSON 內，short_name 走 Phase 1、name 走 Phase 2。"""
        src = '{"name": "My O! 專屬結婚證書套", "short_name": "My O!"}'
        out, p1, p2, _ = rb.apply_phases(src)
        assert (p1, p2) == (1, 1)
        assert out == '{"name": "MyO 專屬結婚證書套", "short_name": "MyO!"}'

    def test_phase1_alt_substring_must_match_whole_word(self):
        """alt 值為 Logo / logo 兩種；錨點不可誤傷其他值。"""
        src = '<img alt="My O! Logo Collection">'
        out, p1, p2, _ = rb.apply_phases(src)
        # 錨點要求 alt="My O! Logo" 完整閉合引號，此處不閉合 → 落到 Phase 2
        assert p1 == 0
        assert p2 == 1
        assert out == '<img alt="MyO Logo Collection">'


class TestPhase2:
    """Phase 2 處理正文，移除驚嘆號。"""

    @pytest.mark.parametrize("src,expected", [
        ('<title>My O! 專屬結婚證書套：設計師級 | 香港</title>',
         '<title>MyO 專屬結婚證書套：設計師級 | 香港</title>'),
        ('<p class="tip">My O! 貼士：提前規劃能幫你節省更多</p>',
         '<p class="tip">MyO 貼士：提前規劃能幫你節省更多</p>'),
        ('<p>My O! 版權所有。</p>', '<p>MyO 版權所有。</p>'),
        ('"name": "My O! Custom Wedding Certificate Holder"',
         '"name": "MyO Custom Wedding Certificate Holder"'),
    ])
    def test_phase2_body_contexts_drop_bang(self, src, expected):
        out, p1, p2, _ = rb.apply_phases(src)
        assert p1 == 0
        assert p2 == 1
        assert out == expected

    def test_phase2_does_not_double_replace_phase1_output(self):
        """Phase 1 產物必須免於 Phase 2 通配。"""
        out, p1, p2, _ = rb.apply_phases('<span>My O!</span>')
        assert (p1, p2) == (1, 0)
        assert out == '<span>MyO!</span>'


class TestPhase3:
    """Phase 3 正規化全大寫 MYO。"""

    def test_phase3_myo_uppercase_to_mixed(self):
        src = 'const CATEGORIES = ["標準尺寸", "MYO證書套"];'
        out, _, _, p3 = rb.apply_phases(src)
        assert p3 == 1
        assert out == 'const CATEGORIES = ["標準尺寸", "MyO 證書套"];'

    def test_phase3_does_not_touch_identifier_myo(self):
        """Myo.tsx 的元件函式名與 05-myo 目錄 id 不是品牌字串。"""
        src = 'export function Myo({ step }) { return null; }'
        out, _, _, p3 = rb.apply_phases(src)
        assert p3 == 0
        assert out == src


class TestIdempotency:
    """重跑不得二次改寫。"""

    @pytest.mark.parametrize("src", [
        '<title>MyO 專屬結婚證書套</title>',
        '<img alt="MyO! Logo">',
        '<div class="brand">MyO!</div>',
        '"MyO 證書套"',
    ])
    def test_second_pass_is_noop(self, src):
        once, *_ = rb.apply_phases(src)
        twice, p1, p2, p3 = rb.apply_phases(once)
        assert twice == once
        assert (p1, p2, p3) == (0, 0, 0)


class TestExclusions:
    """產物與巢狀副本必須排除。"""

    @pytest.mark.parametrize("rel,excluded", [
        ('image/01_company_logo.webp', True),
        ('scripts/blog_index.json', True),
        ('docs/superpowers/plans/2026-07-08-seo-bulk-fix.md', True),
        ('docs/superpowers/specs/2026-07-13-homepage-faq-seo-design.md', True),
        ('docs/PageSpeed Insights.html', True),
        ('docs/architecture-diagram.html', True),
        ('presentations/08-certificate-size-specs/presentation/dist/assets/index-x.js', True),
        ('Users/baba/Documents/Github/myo-hk/index.html', True),
        ('index.html', False),
        ('blog/婚禮籌備清單.html', False),
        ('scripts/optimize_blog_head.py', False),
        ('presentations/08-certificate-size-specs/src/registry/chapters.ts', False),
    ])
    def test_is_excluded(self, rel, excluded):
        assert rb.is_excluded(rel) is excluded

    def test_blog_index_json_never_included(self):
        """該檔由 parse_blog.py 重新生成，不走文字取代。"""
        assert rb.is_excluded('scripts/blog_index.json') is True

    def test_rename_tool_files_excluded_from_own_scan(self):
        """取代工具自身必須排除，否則 Phase 2 會改寫 PHASE2 自身 regex。"""
        assert rb.is_excluded('scripts/rename_brand.py') is True
        assert rb.is_excluded('scripts/test_rename_brand.py') is True

    def test_self_scan_would_corrupt_regex_patterns(self):
        """守恆式測試：證明排除是必要的，而非多餘。"""
        import os
        tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rename_brand.py')
        src = open(tool, encoding='utf-8').read()
        corrupted, p1, p2, _ = rb.apply_phases(src)
        assert corrupted != src, "未排除時工具檔會被改寫，排除清單是必要的"
        assert p2 > 0
        assert 're.compile(r\'MyO\')' in corrupted, "PHASE2 regex 會退化成 no-op"


class TestNoResidualSpacedForm:
    """全域約束：不得殘留含空格的 My O。"""

    def test_spaced_form_never_survives(self):
        src = 'My O! 專屬結婚證書套 My O! 貼士：'
        out, *_ = rb.apply_phases(src)
        assert 'My O' not in out
        assert out == 'MyO 專屬結婚證書套 MyO 貼士：'
