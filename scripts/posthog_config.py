#!/usr/bin/env python3
"""
Single source of truth for PostHog client configuration.

Every script that injects PostHog imports from here, so rotating the
project key or switching cloud region is a one-line change.

The project token is a public write key — PostHog's project-create tool
documents it as safe to embed in client-side code.
"""

from pathlib import Path

# --- Project (set in Task 1) -------------------------------------------------
POSTHOG_KEY = "phc_Bh9JEckmeRh3GGbBNyV45tj44L6NqxmeBqAxRPRtdzK5"
POSTHOG_HOST = "https://myo-makeyourown.pages.dev"

# --- SDK ---------------------------------------------------------------------
API_HOST = "https://us.i.posthog.com"
SDK_DEFAULTS = "2026-05-30"

# Marker used for idempotency checks and CSS/CSP scripts.
SCRIPT_MARKER = "myo-posthog-script"
GUARD_MARKER = "__myoPostHog"

# Trigger the lazy load on the first of: interaction, or this timeout.
LOAD_DELAY_MS = 3000
TRIGGER_EVENTS = ["touchstart", "click", "scroll", "keydown", "mouseover"]

# Cap buffered gtag events in case array.js never loads.
MAX_QUEUE = 50

# --- Filesystem --------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
PRESENTATIONS_DIR = ROOT / "presentations"
SKIP_FILES = {"HTML-Artifacts.html"}

# Root-level HTML pages that get the loader.
ROOT_PAGES = [
    "index.html",
    "v2.html",
    "poster.html",
    "poster-en.html",
    "heic-converter.html",
    "faq.html",
    "privacy.html",
    "terms.html",
]

# Only these five carry a Content-Security-Policy <meta>.
CSP_PAGES = ["index.html", "v2.html", "poster.html", "poster-en.html", "heic-converter.html"]
