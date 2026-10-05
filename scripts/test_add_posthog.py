#!/usr/bin/env python3
"""
pytest suite for add_posthog.py.

Covers:
- add_posthog.py
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import add_posthog

SAMPLE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<script>
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-GQLW7LNP6H');
</script>
</head>
<body>
<a href="#" onclick="gtag('event','click_whatsapp',{'event_category':'contact','event_label':'wa'})">WhatsApp</a>
</body>
</html>
"""


class TestAddPostHog:
    def test_injects_before_head_close(self):
        out, changed = add_posthog.inject(SAMPLE)
        assert changed is True
        assert out.index("myo-posthog-script") < out.index("</head>")

    def test_injection_is_idempotent(self):
        once, _ = add_posthog.inject(SAMPLE)
        twice, changed = add_posthog.inject(once)
        assert changed is False
        assert twice == once
        assert twice.count("__myoPostHog") == 2
        assert twice.count("myo-posthog-script") == 1

    def test_preserves_ga4_measurement_id(self):
        out, _ = add_posthog.inject(SAMPLE)
        assert "G-GQLW7LNP6H" in out
        assert "dataLayer.push(arguments)" in out

    def test_does_not_touch_click_handlers(self):
        out, _ = add_posthog.inject(SAMPLE)
        assert "onclick=\"gtag('event','click_whatsapp'" in out

    def test_uses_manual_pageview_capture(self):
        out, _ = add_posthog.inject(SAMPLE)
        assert "capture_pageview: false" in out
        assert '"$pageview"' in out

    def test_embeds_project_key_and_api_host(self):
        out, _ = add_posthog.inject(SAMPLE)
        assert add_posthog.POSTHOG_KEY in out
        assert add_posthog.API_HOST in out

    def test_lazy_loads_via_assets_host(self):
        out, _ = add_posthog.inject(SAMPLE)
        assert "us-assets.i.posthog.com" not in out  # derived at runtime
        assert '-assets.i.posthog.com") + "/static/array.js"' in out

    def test_buffers_events_until_sdk_loads(self):
        """A click both triggers the load and fires an event — it must queue."""
        out, _ = add_posthog.inject(SAMPLE)
        assert "MAX_QUEUE" not in out  # JS literal, not the Python name
        assert "queue.push" in out
        assert "function flush()" in out

    def test_skips_file_without_head(self):
        out, changed = add_posthog.inject("<p>fragment</p>")
        assert changed is False
        assert out == "<p>fragment</p>"

    def test_handles_cjk_filename(self, tmp_path):
        blog = tmp_path / "blog"
        blog.mkdir()
        target = blog / "婚禮攝影對焦技巧.html"
        target.write_text(SAMPLE, encoding="utf-8")
        with patch.object(add_posthog, "BLOG_DIR", blog):
            stats = add_posthog.process([target])
        assert stats["injected"] == 1
        assert "__myoPostHog" in target.read_text(encoding="utf-8")

    def test_collect_targets_skips_internal_experiment(self, tmp_path):
        blog = tmp_path / "blog"
        blog.mkdir()
        (blog / "a.html").write_text(SAMPLE, encoding="utf-8")
        (blog / "HTML-Artifacts.html").write_text(SAMPLE, encoding="utf-8")
        with patch.object(add_posthog, "BLOG_DIR", blog):
            targets = add_posthog.collect_targets(blog)
        names = {p.name for p in targets}
        assert "a.html" in names
        assert "HTML-Artifacts.html" not in names
