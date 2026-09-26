#!/usr/bin/env python3
"""
pytest suite for add_posthog_presentations.py.

Covers:
- add_posthog_presentations.py
"""

import pytest
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import add_posthog_presentations as p

MAIN_TSX = '''import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
'''


class TestAddPostHogPresentations:
    def test_adds_dependency_when_missing(self):
        pkg = {"name": "x", "dependencies": {"react": "^19.2.6"}}
        out, changed = p.add_dependency(pkg)
        assert changed is True
        assert "posthog-js" in out["dependencies"]

    def test_dependency_change_is_idempotent(self):
        pkg = {"name": "x", "dependencies": {"react": "^19.2.6"}}
        once, _ = p.add_dependency(pkg)
        twice, changed = p.add_dependency(once)
        assert changed is False
        assert twice["dependencies"] == once["dependencies"]

    def test_preserves_existing_dependencies(self):
        pkg = {"name": "x", "dependencies": {"react": "^19.2.6", "vite": "^8.0.12"}}
        out, _ = p.add_dependency(pkg)
        assert out["dependencies"]["react"] == "^19.2.6"
        assert out["dependencies"]["vite"] == "^8.0.12"

    def test_creates_dependencies_key_when_absent(self):
        pkg = {"name": "x"}
        out, changed = p.add_dependency(pkg)
        assert changed is True
        assert "posthog-js" in out["dependencies"]

    def test_patches_main_tsx(self):
        out, changed = p.patch_main_tsx(MAIN_TSX)
        assert changed is True
        assert 'import "./analytics";' in out

    def test_main_tsx_patch_is_idempotent(self):
        once, _ = p.patch_main_tsx(MAIN_TSX)
        twice, changed = p.patch_main_tsx(once)
        assert changed is False
        assert twice == once

    def test_main_tsx_keeps_create_root(self):
        out, _ = p.patch_main_tsx(MAIN_TSX)
        assert "createRoot(" in out
        assert "<StrictMode>" in out

    def test_analytics_module_uses_manual_pageview(self):
        src = p.render_analytics_ts()
        assert "capture_pageview: false" in src
        assert '"$pageview"' in src

    def test_analytics_module_is_typescript_strict_safe(self):
        """No enums or parameter properties — erasableSyntaxOnly is on."""
        src = p.render_analytics_ts()
        assert "enum " not in src
        assert "WindowWithAnalytics" in src  # typed window.posthog access

    def test_analytics_module_embeds_key(self):
        import posthog_config as cfg

        assert cfg.POSTHOG_KEY in p.render_analytics_ts()

    def test_collect_projects_finds_presentation_dirs(self, tmp_path):
        for slug in ("01-a", "02-b"):
            proj = tmp_path / slug / "presentation"
            (proj / "src").mkdir(parents=True)
            (proj / "package.json").write_text(
                json.dumps({"name": slug, "dependencies": {}}), encoding="utf-8"
            )
            (proj / "src" / "main.tsx").write_text(MAIN_TSX, encoding="utf-8")
        found = p.collect_projects(tmp_path)
        assert len(found) == 2
