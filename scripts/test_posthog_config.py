#!/usr/bin/env python3
"""pytest suite for posthog_config.py."""

import re
import sys
import os

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import posthog_config


class TestPostHogConfig:
    def test_key_is_a_phc_token(self):
        assert re.fullmatch(r"phc_[A-Za-z0-9]{20,}", posthog_config.POSTHOG_KEY), (
            f"POSTHOG_KEY looks like a placeholder: {posthog_config.POSTHOG_KEY!r}. "
            "Update scripts/posthog_config.py with the token from Task 1."
        )

    def test_api_host_is_a_posthog_endpoint(self):
        assert posthog_config.API_HOST == "https://us.i.posthog.com"
        assert posthog_config.API_HOST.endswith(".i.posthog.com")

    def test_asset_host_derivation_is_valid(self):
        """The loader rewrites .i.posthog.com -> -assets.i.posthog.com."""
        assets = posthog_config.API_HOST.replace(
            ".i.posthog.com", "-assets.i.posthog.com"
        )
        assert assets == "https://us-assets.i.posthog.com"

    def test_skip_files_excludes_internal_experiment(self):
        assert "HTML-Artifacts.html" in posthog_config.SKIP_FILES

    def test_csp_pages_are_a_subset_of_root_pages(self):
        assert set(posthog_config.CSP_PAGES).issubset(set(posthog_config.ROOT_PAGES))

    def test_trigger_events_include_click_and_scroll(self):
        """scroll_depth fires on scroll; social clicks fire on click."""
        assert "click" in posthog_config.TRIGGER_EVENTS
        assert "scroll" in posthog_config.TRIGGER_EVENTS

    def test_load_delay_ms(self):
        """Downstream scripts gate the lazy-load timer on this value."""
        assert posthog_config.LOAD_DELAY_MS == 3000

    def test_max_queue(self):
        """Downstream scripts cap the gtag event buffer at this value."""
        assert posthog_config.MAX_QUEUE == 50

    def test_script_marker(self):
        """Idempotency marker used by HTML injection scripts (Tasks 2/3/5)."""
        assert posthog_config.SCRIPT_MARKER == "myo-posthog-script"

    def test_guard_marker(self):
        """Idempotency guard marker used by HTML injection scripts."""
        assert posthog_config.GUARD_MARKER == "__myoPostHog"

    def test_root_pages_exact_contents(self):
        """Every root-level page must appear — a missing entry silently skips loader injection."""
        assert len(posthog_config.ROOT_PAGES) == 7
        assert posthog_config.ROOT_PAGES == [
            "index.html",
            "v2.html",
            "poster.html",
            "heic-converter.html",
            "faq.html",
            "privacy.html",
            "terms.html",
        ]

    def test_html_artifacts_not_in_root_pages(self):
        """HTML-Artifacts.html is an internal experiment — skip it, don't load it."""
        assert "HTML-Artifacts.html" not in posthog_config.ROOT_PAGES
        assert "HTML-Artifacts.html" in posthog_config.SKIP_FILES
