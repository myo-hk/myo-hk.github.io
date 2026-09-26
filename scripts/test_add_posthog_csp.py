#!/usr/bin/env python3
"""
pytest suite for add_posthog_csp.py.

Covers:
- add_posthog_csp.py
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import add_posthog_csp as csp

SAMPLE = """<!DOCTYPE html>
<html><head>
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com; connect-src 'self' https://www.google-analytics.com https://*.googletagmanager.com;">
</head><body></body></html>
"""


class TestAddPostHogCsp:
    def test_adds_wildcard_to_script_src(self):
        out, changed = csp.add_csp(SAMPLE)
        assert changed is True
        script_src = csp.get_directive(out, "script-src")
        assert "https://*.posthog.com" in script_src

    def test_adds_wildcard_to_connect_src(self):
        out, _ = csp.add_csp(SAMPLE)
        assert "https://*.posthog.com" in csp.get_directive(out, "connect-src")

    def test_adds_worker_src_when_absent(self):
        out, _ = csp.add_csp(SAMPLE)
        assert "worker-src" in out
        assert "'self' blob: data:" in csp.get_directive(out, "worker-src")

    def test_never_enumerates_specific_subdomains(self):
        out, _ = csp.add_csp(SAMPLE)
        assert "us.i.posthog.com" not in out
        assert "us-assets.i.posthog.com" not in out

    def test_never_adds_frame_ancestors(self):
        """frame-ancestors is ignored in a meta CSP; adding it is a no-op lie."""
        out, _ = csp.add_csp(SAMPLE)
        assert "frame-ancestors" not in out

    def test_preserves_existing_directives(self):
        out, _ = csp.add_csp(SAMPLE)
        for token in [
            "https://www.googletagmanager.com",
            "https://cdnjs.cloudflare.com",
            "https://fonts.gstatic.com",
            "https://www.google-analytics.com",
            "'unsafe-inline'",
        ]:
            assert token in out

    def test_is_idempotent(self):
        once, _ = csp.add_csp(SAMPLE)
        twice, changed = csp.add_csp(once)
        assert changed is False
        assert twice == once
        assert twice.count("posthog.com") == 2

    def test_does_not_duplicate_existing_worker_src(self):
        with_worker = SAMPLE.replace(
            "font-src", "worker-src 'self' blob: data:; font-src"
        )
        out, _ = csp.add_csp(with_worker)
        assert out.count("worker-src") == 1

    def test_unchanged_when_no_csp_meta(self):
        plain = "<html><head><title>x</title></head><body></body></html>"
        out, changed = csp.add_csp(plain)
        assert changed is False
        assert out == plain

    def test_aborts_when_script_src_missing(self):
        """A policy without script-src means hand-rolled; do not guess."""
        odd = SAMPLE.replace("script-src 'self' https://www.googletagmanager.com; ", "")
        out, changed = csp.add_csp(odd)
        assert changed is False
        assert out == odd
