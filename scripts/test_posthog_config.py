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
