# PostHog Analytics Integration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install PostHog on every page of the myo-hk static site (422 blog pages, 7 root pages, 1 presentation index) and all 40 Vite/React presentations, with autocapture, heatmaps, session replay, exception capture, console log capture, and Web Vitals — while leaving Google Analytics 4 fully intact.

**Architecture:** Three independent layers, each with its own test suite and its own commit.

1. **Config** — a single Python module holds the project key and API host. Every downstream script imports from it, so rotating the key is a one-line change.
2. **Static HTML** — a dry-run-first Python injector wraps the existing `window.gtag` so the 422 pages' existing `onclick` GA4 calls forward to PostHog with zero edits to the click handlers. A second script patches the 4 pages that carry a CSP `<meta>`.
3. **Presentations** — a dry-run-first Python script adds `posthog-js` to each of the 40 projects, writes a typed `src/analytics.ts` with identical logic, and adds one import line to `src/main.tsx`. All 40 `main.tsx` files are byte-identical (verified: single MD5), so one patch is safe.

PostHog loads lazily — on the first user interaction or after 3s, whichever comes first. Full SDK is ~73 KB gzipped, session replay recorder adds ~35 KB gzipped on demand. Deferring keeps that off the critical path.

**Tech Stack:** Python 3.9 (stdlib only, no new deps) · pytest · posthog-js 1.4xx via npm · Vite 8 + React 19 + TypeScript 5.9 (existing presentation toolchain)

**Spec:** Design approved in conversation on 2026-09-26. No separate spec document was written (bounded-work path in `brainstorming`). The design decisions this plan implements are frozen in **Global Constraints** below — an executor who reads only this file has everything needed.

---

## Global Constraints

These are decisions, not preferences. Do not deviate without asking the user first.

**Analytics configuration**
- GA4 measurement ID `G-GQLW7LNP6H` stays exactly as-is. Never remove, rename, or reorder the `gtag` definition.
- PostHog API host: `https://us.i.posthog.com` (US Cloud — **confirmed by the user** on 2026-09-26; see Task 1 Step 0).
- PostHog `defaults: '2026-05-30'` — the current SDK defaults version.
- `capture_pageview: false` on init, followed by an explicit `posthog.capture('$pageview', {...})` after load. PostHog's own initial-pageview fires on `setTimeout(1)` after `init()`, which with lazy loading would timestamp the pageview at interaction time rather than page-load time.
- `autocapture: true` (drives heatmaps, dead-click, and rage-click detection).
- Session replay needs no extra config — it has been lazy-loaded by default since posthog-js v1.411.

**CSP** (applies only to `index.html`, `v2.html`, `poster.html`, `heic-converter.html`)
- Use the wildcard `https://*.posthog.com` only. PostHog's docs explicitly warn that subdomains change and single subdomains must not be enumerated. Do **not** list `us.i.posthog.com` or `us-assets.i.posthog.com`.
- Add `https://*.posthog.com` to both `script-src` and `connect-src`.
- Add `worker-src 'self' blob: data:;` — session replay's rrweb recorder uses a Worker with a blob URL. Without this directive, session recording fails **silently**: no console error, no recordings, no clue.
- **Never add `frame-ancestors` to a `<meta>` CSP.** The spec ignores that directive in meta form; it only works as an HTTP header. Adding it looks like a fix and does nothing. PostHog's toolbar is served from `posthog.com` origin, so the site CSP does not restrict it anyway.
- `img-src` already permits `https:`, so replay snapshots and heatmap assets are covered without a change.

**Scope**
- Injected: `blog/*.html` (421), `blog/index.html`, `index.html`, `v2.html`, `poster.html`, `heic-converter.html`, `faq.html`, `privacy.html`, `terms.html`, `presentations/index.html`.
- Skipped: `HTML-Artifacts.html` (internal PDF-download experiment; `add_pwa_tags.py` already skips it).
- `presentations/*/presentation/index.html` is the Vite entry and is **overwritten** by `cp dist/index.html index.html` on every build. Never hand-edit it; the React module in Task 5 is the durable integration point.

**Repo conventions**
- Every Python script defaults to read-only and requires `--test` (or `--dry-run`) before writing. Follow `scripts/add_pwa_tags.py`.
- Blog filenames are Traditional Chinese. Always `encoding="utf-8"` on read and write.
- Test files are pytest classes named `Test<ScriptName>`, using `tmp_path` and `unittest.mock.patch.object` to redirect module-level path constants — see `scripts/test_seo_fixes.py`.
- Do not touch `transition: all` or any unrelated CSS/HTML. This change adds a script to `<head>` and nothing else.
- Conventional commits: `feat(analytics):`, `fix(analytics):`, `chore(analytics):`, `docs:`.

---

## Review Focus

Five failure modes that automated tests do **not** catch. A human or the executing agent must check these by hand.

1. **Late-load pageview timestamp.** `$pageview` is recorded when `array.js` finishes loading, not at page load. On a Hong Kong connection to `us.i.posthog.com` (2–4 round trips), any visitor who bounces inside ~1.5s is invisible. This is a known, accepted trade-off of the deferred-load decision. Document it in the PostHog project description so nobody later "discovers" it as a tracking bug.

2. **Event ordering between the gtag bridge and the loader.** The very first `click_whatsapp` fires *before* PostHog exists, because the click is what triggers the load. Without the queue in the Task 2 loader, the highest-intent event on the whole site — the WhatsApp click — is the one event guaranteed to be lost. Verify by clicking WhatsApp on the deployed site and confirming the event arrives in PostHog Live Events.

3. **`scroll_depth` fires up to 4× per session**, on scroll. Combined with `mouseover` as a trigger event, the loader can be invoked from a scroll handler. Confirm the queue cap and the `myo-posthog-script` id guard together prevent double-injection of `array.js` (a duplicate SDK instance would double-count every event).

4. **Idempotency across 422 files.** Re-running the injector must produce zero changes on the second run. If `add_pwa_tags.py` is ever run again on an already-injected page, it must not stack a second PostHog block. Run the injector twice and diff.

5. **Silent session-replay failure.** If `worker-src` is missing or malformed, replay simply never records. No error surfaces. After deployment, confirm at least one recording exists in PostHog — do not conclude success from the absence of console errors.

---

## Task 1: PostHog project and shared config module

**Files:**
- Create: `scripts/posthog_config.py`
- Create: `scripts/test_posthog_config.py`

**Step 0: Decisions — RESOLVED, no longer blocking**

Three open decisions were put to the user and answered. The plan proceeds with these values; nothing below needs re-asking.

| # | Decision | Answer | Consequence for this plan |
|---|---|---|---|
| 1 | **Cloud region** | **US Cloud** | `API_HOST = "https://us.i.posthog.com"` and the assets host `https://us-assets.i.posthog.com` in `posthog_config.py` are correct as written. No edits needed. |
| 2 | **Session replay** | **All open — enabled site-wide, no consent banner** | `session_recording_opt_in: true` at 10% sample / 30-day retention stands. No consent-gate component is in scope. |
| 3 | **Project name** | **`MyO Cert Holder`** | Used verbatim in `project-create` (Step 1) and `project-settings-update` (Step 2). The name is permanent. Verified unblocked: the account has `user_access_level: admin` and `effective_membership_level: 8`, so `project-create` will succeed and quota is available. |

Because decision 2 is "all open, no banner", two things follow concretely:

- **No consent gate work.** Task 5 gains no consent component, and Task 4's E2E suite gains no banner assertions. The scope in this plan is already correct — nothing to remove.
- **`privacy.html` carries the full disclosure burden.** With replay recording every session and no consent mechanism in front of it, the privacy page must state plainly what is recorded (session replay, heatmaps, console logs), that IP addresses are anonymized, the 10% sample rate, and the 30-day retention. Task 6 already does this — treat it as required, not optional.

**Step 1: Create the PostHog project**

The MCP tool is `project-create`. Its only input is `name`.

```
posthog_exec: call project-create {"name": "MyO Cert Holder"}
```

**Ask the user to confirm the name before calling** — `project-create` is annotated `destructiveHint: false` but the tool description states it consumes organization plan quota, and the name is permanent.

Record the returned project `id` and `token` (the `phc_...` value). The tool description confirms the token is safe in client-side code.

**Step 1b: Make the new project active**

A freshly created project does **not** become the active project. Every later MCP call that omits an explicit `id` — including `project-get {}` in Task 6 and any `insights`/`query-*` verification — would silently target the previously active project (the Teawikhk one) and return plausible but wrong data.

```
posthog_exec: call switch-project {"id": <PROJECT_ID>}
posthog_exec: call project-get {}
```

Expected: `project-get` reports the new project's name and id. If it still reports the old project, stop and fix the switch before continuing — every downstream verification depends on it.

**Step 2: Configure the new project**

`project-settings-update` is PATCH-semantics, so send only the fields being changed. `id` accepts the numeric project id.

```
posthog_exec: call project-settings-update {
  "id": <PROJECT_ID>,
  "name": "MyO Cert Holder",
  "description": "Deferred load: PostHog loads on first interaction or 3s, so $pageview is timestamped when array.js finishes loading, not at page load. Visitors who bounce within ~1.5s are not counted. This is an accepted trade-off, not a tracking bug.",
  "timezone": "Asia/Hong_Kong",
  "base_currency": "HKD",
  "anonymize_ips": true,
  "recording_domains": ["https://myo-makeyourown.pages.dev"],
  "app_urls": ["https://myo-makeyourown.pages.dev/"],
  "session_recording_opt_in": true,
  "heatmaps_opt_in": true,
  "autocapture_exceptions_opt_in": true,
  "autocapture_web_vitals_opt_in": true,
  "capture_console_log_opt_in": true,
  "capture_dead_clicks": true,
  "session_recording_sample_rate": "0.10",
  "session_recording_minimum_duration_milliseconds": 2000,
  "session_recording_retention_period": "30d"
}
```

The `description` field satisfies **Review Focus #1** — the late-load pageview trade-off is recorded in PostHog itself, so a future maintainer reading the project does not "discover" it as a tracking bug. Do not guess its name: `project-get` reports the field as `product_description`, so if the schema check below rejects `description`, use the name the schema returns.

Two fields are typed as union-of-1 and carry a `DO NOT GUESS` hint. Resolve them before calling:

```
posthog_exec: schema project-settings-update app_urls
posthog_exec: schema project-settings-update capture_dead_clicks
posthog_exec: schema project-settings-update description
```

Notes on the values chosen:
- `anonymize_ips: true` — the existing Teawikhk project has this off. For a Hong Kong site under PDPO, drop the IP.
- `recording_domains` is PostHog's authorized-domains list. Without it, session replay and heatmaps record for any origin that embeds the key.
- `session_recording_sample_rate: "0.10"` — 10% is enough to read heatmaps and watch replays on a site with modest traffic, and keeps the 30-day retention window affordable.

**Step 3: Write the config module**

Create `scripts/posthog_config.py`:

```python
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
POSTHOG_KEY = "phc_REPLACE_WITH_PROJECT_TOKEN_FROM_TASK_1"
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
    "heic-converter.html",
    "faq.html",
    "privacy.html",
    "terms.html",
]

# Only these four carry a Content-Security-Policy <meta>.
CSP_PAGES = ["index.html", "v2.html", "poster.html", "heic-converter.html"]
```

**Step 4: Write the config test**

Create `scripts/test_posthog_config.py`:

```python
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
```

**Step 5: Run tests**

```
python3 -m pytest scripts/test_posthog_config.py -v
```

Expected: 6 passed. `test_key_is_a_phc_token` fails until the real token from Step 1 replaces the placeholder — that failure is the signal that Task 1 Step 3 was not completed.

**Step 6: Commit**

```
git add scripts/posthog_config.py scripts/test_posthog_config.py
git commit -m "feat(analytics): add shared PostHog config module"
```

---

## Task 2: Static HTML injector with gtag bridge

**Files:**
- Create: `scripts/add_posthog.py`
- Create: `scripts/test_add_posthog.py`

**Step 1: Write the failing test**

Create `scripts/test_add_posthog.py`:

```python
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
        assert twice.count("__myoPostHog") == 1

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
```

**Step 2: Run the test to confirm it fails**

```
python3 -m pytest scripts/test_add_posthog.py -v
```

Expected: collection error — `ModuleNotFoundError: No module named 'add_posthog'`. That is the correct red state.

**Step 3: Write the implementation**

Create `scripts/add_posthog.py`:

```python
#!/usr/bin/env python3
"""
Inject the deferred PostHog loader into all static HTML pages.

The loader wraps the existing window.gtag so the 422 pages' current
onclick="gtag('event', ...)" calls forward to PostHog untouched.

 Usage:
     python3 scripts/add_posthog.py --test   # dry run, no writes
     python3 scripts/add_posthog.py          # write
 """

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import posthog_config as cfg

POSTHOG_KEY = cfg.POSTHOG_KEY
API_HOST = cfg.API_HOST
SDK_DEFAULTS = cfg.SDK_DEFAULTS
SCRIPT_ID = cfg.SCRIPT_MARKER
GUARD = cfg.GUARD_MARKER
TRIGGER_EVENTS = cfg.TRIGGER_EVENTS
LOAD_DELAY_MS = cfg.LOAD_DELAY_MS
MAX_QUEUE = cfg.MAX_QUEUE

BLOG_DIR = cfg.BLOG_DIR
ROOT = cfg.ROOT
SKIP_FILES = cfg.SKIP_FILES
ROOT_PAGES = cfg.ROOT_PAGES

LOADER_TEMPLATE = """<!-- PostHog: lazy load on first interaction or {delay}ms. See scripts/add_posthog.py -->
<script>
(function () {{
  if (window.{guard}) return;
  window.{guard} = true;
  var KEY = "{key}";
  var API_HOST = "{api_host}";
  var DEFAULTS = "{defaults}";
  var queue = [];
  var loaded = false;
  var injected = false;

  function client() {{
    var c = window.posthog;
    return c && typeof c.capture === "function" ? c : null;
  }}

  function enqueue(name, props) {{
    if (loaded) {{
      var c = client();
      if (c) c.capture(name, props);
      return;
    }}
    if (queue.length < {max_queue}) queue.push([name, props]);
  }}

  function flush() {{
    var c = client();
    if (!loaded || !c) return;
    while (queue.length) {{
      var item = queue.shift();
      c.capture(item[0], item[1]);
    }}
  }}

  function start() {{
    if (injected) return;
    injected = true;
    var s = document.createElement("script");
    s.id = "{script_id}";
    s.type = "text/javascript";
    s.crossOrigin = "anonymous";
    s.async = true;
    s.src = API_HOST.replace(".i.posthog.com", "-assets.i.posthog.com") + "/static/array.js";
    s.onload = function () {{
      var c = client();
      if (!c) return;
      c.init(KEY, {{ api_host: API_HOST, defaults: DEFAULTS, capture_pageview: false, autocapture: true }});
      loaded = true;
      c.capture("$pageview", {{
        $current_url: window.location.href,
        $referrer: document.referrer
      }});
      flush();
    }};
    document.head.appendChild(s);
  }}

  // Bridge existing gtag('event', name, params) calls into PostHog.
  // The original still runs first, so GA4 behaviour is unchanged.
  if (typeof window.gtag === "function") {{
    var original = window.gtag;
    window.gtag = function () {{
      var args = Array.prototype.slice.call(arguments);
      original.apply(window, args);
      if (args[0] !== "event" || typeof args[1] !== "string") return;
      var p = args[2] || {{}};
      var props = {{}};
      if (p.event_category !== undefined) props.category = p.event_category;
      if (p.event_label !== undefined) props.label = p.event_label;
      if (p.value !== undefined) props.value = p.value;
      if (p.non_interaction !== undefined) props.non_interaction = p.non_interaction;
      enqueue(args[1], props);
      if (!loaded) start();
    }};
  }}

  function onFirstInteraction() {{
    start();
    for (var i = 0; i < {events}.length; i++) {{
      document.removeEventListener({events}[i], onFirstInteraction, true);
    }}
  }}

  var TRIGGERS = {events};
  for (var j = 0; j < TRIGGERS.length; j++) {{
    document.addEventListener(TRIGGERS[j], onFirstInteraction, {{ capture: true, passive: true }});
  }}
  setTimeout(start, {delay});
}})();
</script>
"""


def render_loader() -> str:
    """Build the loader block with config values substituted."""
    events = json.dumps(TRIGGER_EVENTS)
    return LOADER_TEMPLATE.format(
        delay=LOAD_DELAY_MS,
        guard=GUARD,
        key=POSTHOG_KEY,
        api_host=API_HOST,
        defaults=SDK_DEFAULTS,
        max_queue=MAX_QUEUE,
        script_id=SCRIPT_ID,
        events=events,
    )


def inject(html: str):
    """Return (new_html, changed). Idempotent: a second call is a no-op."""
    if GUARD in html:
        return html, False
    if "</head>" not in html:
        return html, False
    return html.replace("</head>", render_loader() + "</head>", 1), True


def collect_targets(blog_dir: Path):
    """Blog articles plus blog/index.html, excluding internal experiments."""
    targets = []
    for path in sorted(blog_dir.glob("*.html")):
        if path.name in SKIP_FILES:
            continue
        targets.append(path)
    return targets


def process(paths):
    """Apply inject() to each path. Returns a stats dict."""
    stats = {"scanned": 0, "injected": 0, "skipped": 0, "errors": 0}
    loader = render_loader()
    for path in paths:
        stats["scanned"] += 1
        try:
            original = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"  ERROR {path.name}: {exc}")
            stats["errors"] += 1
            continue
        if GUARD in original:
            print(f"  skip   {path.name} (already injected)")
            stats["skipped"] += 1
            continue
        new_html, changed = inject(original)
        if not changed:
            print(f"  skip   {path.name} (no </head>)")
            stats["skipped"] += 1
            continue
        if "--test" in sys.argv:
            print(f"  inject {path.name} (+{len(new_html) - len(original)} bytes)")
        else:
            path.write_text(new_html, encoding="utf-8")
            print(f"  wrote  {path.name}")
        stats["injected"] += 1
    return stats


def main():
    targets = list(collect_targets(BLOG_DIR))
    for name in ROOT_PAGES:
        candidate = ROOT / name
        if candidate.exists():
            targets.append(candidate)
    index = ROOT / "presentations" / "index.html"
    if index.exists():
        targets.append(index)

    mode = "DRY RUN (pass no --test to write)" if "--test" in sys.argv else "WRITE"
    print(f"add_posthog.py — {len(targets)} files — {mode}\n")
    stats = process(targets)
    print(
        f"\nscanned={stats['scanned']} injected={stats['injected']} "
        f"skipped={stats['skipped']} errors={stats['errors']}"
    )
    if stats["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 4: Run the test to confirm it passes**

```
python3 -m pytest scripts/test_add_posthog.py -v
```

Expected: 12 passed.

**Step 5: Run the dry run**

```
python3 scripts/add_posthog.py --test | tail -20
```

Expected: 430 files scanned (421 blog articles + `blog/index.html` + 7 root pages + `presentations/index.html`), 430 injected, 0 errors. Confirm the byte delta per file is roughly +3.5 KB and identical across files.

If the count is not 430, stop and reconcile the arithmetic before continuing.

**Step 6: Commit**

```
git add scripts/add_posthog.py scripts/test_add_posthog.py
git commit -m "feat(analytics): add PostHog static HTML injector with gtag bridge"
```

---

## Task 3: CSP allowlist for the four protected pages

**Files:**
- Create: `scripts/add_posthog_csp.py`
- Create: `scripts/test_add_posthog_csp.py`

**Step 1: Write the failing test**

Create `scripts/test_add_posthog_csp.py`:

```python
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
```

**Step 2: Run the test to confirm it fails**

```
python3 -m pytest scripts/test_add_posthog_csp.py -v
```

Expected: `ModuleNotFoundError: No module named 'add_posthog_csp'`.

**Step 3: Write the implementation**

Create `scripts/add_posthog_csp.py`:

```python
#!/usr/bin/env python3
"""
Add the PostHog CSP allowlist to pages that carry a
Content-Security-Policy <meta> tag.

PostHog's docs require the wildcard *.posthog.com because subdomains
change without notice. worker-src is mandatory for session replay.

Usage:
    python3 scripts/add_posthog_csp.py --test
    python3 scripts/add_posthog_csp.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import posthog_config as cfg

POSTHOG_CSP_HOST = "https://*.posthog.com"
WORKER_SRC = "worker-src 'self' blob: data:;"
REQUIRED_DIRECTIVES = ("script-src", "connect-src")

ROOT = cfg.ROOT
CSP_PAGES = cfg.CSP_PAGES

META_RE = re.compile(
    r'(<meta\s+http-equiv="Content-Security-Policy"\s+content=")([^"]*)("\s*/?>)'
)


def get_directive(policy: str, directive: str) -> str:
    """Return the source list for `directive`, or '' when absent."""
    match = re.search(rf"(?:^|;)\s*{re.escape(directive)}\s+([^;]*)", policy)
    return match.group(1).strip() if match else ""


def _append_to_directive(policy: str, directive: str):
    """Append the PostHog host to `directive`. None when absent."""
    match = re.search(rf"(?:^|;)(\s*{re.escape(directive)}\s+)([^;]*)", policy)
    if not match:
        return None
    sources = match.group(2).rstrip()
    if POSTHOG_CSP_HOST in sources:
        return policy
    updated = f"{sources} {POSTHOG_CSP_HOST}"
    return policy[: match.start(2)] + updated + policy[match.end(2) :]


def add_csp(html: str):
    """Return (new_html, changed). Idempotent."""
    if POSTHOG_CSP_HOST in html:
        return html, False
    meta = META_RE.search(html)
    if not meta:
        return html, False

    policy = meta.group(2)
    for directive in REQUIRED_DIRECTIVES:
        updated = _append_to_directive(policy, directive)
        if updated is None:
            # Hand-rolled policy without a required directive. Refuse to guess.
            return html, False
        policy = updated

    if not re.search(r"(?:^|;)\s*worker-src\s", policy):
        policy = policy.rstrip().rstrip(";")
        policy = f"{policy}; {WORKER_SRC}"

    return html[: meta.start(2)] + policy + html[meta.end(2) :], True


def main():
    mode = "DRY RUN (pass no --test to write)" if "--test" in sys.argv else "WRITE"
    print(f"add_posthog_csp.py — {len(CSP_PAGES)} files — {mode}\n")
    changed_count = 0
    missing = []

    for name in CSP_PAGES:
        path = ROOT / name
        if not path.exists():
            missing.append(f"{name} (not found)")
            continue
        original = path.read_text(encoding="utf-8")
        new_html, changed = add_csp(original)
        if not changed:
            if POSTHOG_CSP_HOST in original:
                print(f"  skip   {name} (already patched)")
            else:
                missing.append(f"{name} (no usable CSP meta)")
            continue
        if "--test" in sys.argv:
            print(f"  patch  {name}")
        else:
            path.write_text(new_html, encoding="utf-8")
            print(f"  wrote  {name}")
        changed_count += 1

    print(f"\npatched={changed_count}")
    if missing:
        print("NEEDS MANUAL REVIEW:")
        for item in missing:
            print(f"  - {item}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 4: Run the test to confirm it passes**

```
python3 -m pytest scripts/test_add_posthog_csp.py -v
```

Expected: 10 passed.

**Step 5: Run the dry run**

```
python3 scripts/add_posthog_csp.py --test
```

Expected: 4 files patched, no manual-review entries.

**Step 6: Commit**

```
git add scripts/add_posthog_csp.py scripts/test_add_posthog_csp.py
git commit -m "feat(analytics): add PostHog CSP allowlist script"
```

---

## Task 4: Apply to all static pages and verify no regression

**Files:**
- Modify: 430 HTML files (via Task 2 script)
- Modify: 4 HTML files (via Task 3 script)
- Create: `tests/posthog.spec.ts`

**Step 1: Confirm the working tree is clean**

```
git status --porcelain
```

Expected: empty. Any modified HTML here means something outside this plan touched the tree — resolve it before continuing so the diff stays reviewable.

**Step 2: Dry run, then write**

```
python3 scripts/add_posthog.py --test | tail -5
python3 scripts/add_posthog.py | tail -5
python3 scripts/add_posthog_csp.py --test
python3 scripts/add_posthog_csp.py
```

**Step 3: Verify counts and idempotency (Review Focus #4)**

```
grep -rl '__myoPostHog' blog/*.html | wc -l
grep -rl 'https://\*.posthog.com' *.html
python3 scripts/add_posthog.py --test | tail -3
python3 scripts/add_posthog_csp.py --test
```

Expected:
- 422 files contain `__myoPostHog` (421 articles + `blog/index.html`)
- `https://*.posthog.com` appears in exactly `index.html`, `v2.html`, `poster.html`, `heic-converter.html`
- Both re-runs report `injected=0` / `patched=0` — the second run is a clean no-op

The third and fourth commands are the idempotency proof. If they report any injections, the guard is broken; fix it before committing.

**Step 4: Confirm GA4 survived**

```
grep -c 'G-GQLW7LNP6H' "blog/婚禮攝影對焦技巧.html" index.html
grep -c "function gtag(){dataLayer.push(arguments);}" "blog/婚禮攝影對焦技巧.html"
git diff --stat -- "blog/婚禮攝影對焦技巧.html"
```

Expected: both greps return 1; the diff stat shows only additions inside `<head>`, no deletions in the body.

**Step 5: Add the E2E regression test**

Create `tests/posthog.spec.ts`:

```typescript
import { test, expect } from "@playwright/test";

const GA4_ID = "G-GQLW7LNP6H";

const PAGES = [
  { path: "/index.html", name: "home" },
  { path: "/faq.html", name: "faq" },
  { path: "/blog/index.html", name: "blog index" },
  { path: "/blog/婚禮攝影對焦技巧.html", name: "blog article (CJK filename)" },
];

test.describe("PostHog loader", () => {
  // Static assertions use the `request` fixture, not a live page, so they can
  // never race the 3000ms lazy-load timer.
  for (const { path, name } of PAGES) {
    test(`${name} ships the deferred loader and keeps GA4`, async ({ request }) => {
      const res = await request.get(path);
      expect(res.ok()).toBe(true);
      const html = await res.text();

      expect(html).toContain("__myoPostHog");
      expect(html).toContain("i.posthog.com");
      expect(html).toContain(GA4_ID);
      expect(html).toContain("dataLayer.push(arguments)");

      // The SDK must never be fetched synchronously from <head>.
      expect(html).not.toMatch(/<script[^>]+src="https:\/\/[^"]*posthog\.com/);
    });
  }

  for (const { path, name } of PAGES) {
    test(`${name} loads with no CSP violations`, async ({ page }) => {
      const violations: string[] = [];
      // Registered BEFORE navigation — CSP violations fire during initial load,
      // so a listener attached after goto() would miss them.
      page.on("console", (msg) => {
        const text = msg.text();
        if (/Content Security Policy|Refused to/i.test(text)) {
          violations.push(text);
        }
      });
      page.on("pageerror", (err) => violations.push(String(err)));

      await page.goto(path, { waitUntil: "load" });
      // Force the deferred path so array.js is actually requested under CSP.
      await page.evaluate(() => {
        document.body.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      await page.waitForTimeout(1500);

      expect(violations).toEqual([]);
    });
  }

  test("deferred loader does not block first paint", async ({ page }) => {
    const start = Date.now();
    await page.goto("/index.html", { waitUntil: "domcontentloaded" });
    // The loader is deferred, so DCL must not wait on PostHog's CDN.
    expect(Date.now() - start).toBeLessThan(3000);
  });

  test("gtag bridge forwards social clicks without throwing", async ({ page }) => {
    await page.goto("/index.html");
    const result = await page.evaluate(() => {
      const w = window as unknown as {
        gtag?: (...args: unknown[]) => void;
        posthog?: { capture?: (n: string, p?: unknown) => void };
      };
      try {
        w.gtag?.("event", "click_whatsapp", {
          event_category: "contact",
          event_label: "wa",
        });
      } catch (err) {
        return { threw: String(err) };
      }
      return { threw: null, sdkReady: typeof w.posthog?.capture === "function" };
    });
    // The bridge must never throw, whether or not array.js has resolved yet.
    expect(result.threw).toBeNull();
  });
});
```

**Step 6: Run the E2E suite**

`playwright.config.js` sets `baseURL: 'http://localhost:8080'` and has **no `webServer` block**, so the static server must already be listening on 8080. Start it in a separate terminal and leave it running:

```
python3 -m http.server 8080
```

Then, in a second terminal:

```
npm test
```

Expected: all existing tests still pass, plus the 10 new PostHog tests (4 pages × static assertions + 4 pages × CSP, plus the first-paint and gtag-bridge tests). Any pre-existing failure is unrelated — record it and move on, do not fix it here.

Also run the existing script suite to confirm nothing regressed:

```
python3 -m pytest scripts/ -q
```

**Step 7: Commit**

```
git add blog/ *.html presentations/index.html tests/posthog.spec.ts
git commit -m "feat(analytics): inject deferred PostHog loader into all static pages"
```

---

## Task 5: Presentations — 40 Vite/React projects

**Files:**
- Create: `scripts/add_posthog_presentations.py`
- Create: `scripts/test_add_posthog_presentations.py`
- Modify: 40 × `presentation/src/analytics.ts` (created)
- Modify: 40 × `presentation/src/main.tsx` (one import line)
- Modify: 40 × `presentation/package.json`
- Modify: 40 × `presentation/package-lock.json`
- Modify: 40 × `presentation/dist/` + `presentation/index.html` (build output)

`presentations/_scaffold.sh` uses `01-hong-kong-wedding-flow/presentation` as its template (line 36), so updating 01 propagates the integration to every future presentation. No separate scaffold edit is needed.

**Step 1: Write the failing test**

Create `scripts/test_add_posthog_presentations.py`:

```python
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
```

**Step 2: Run the test to confirm it fails**

```
python3 -m pytest scripts/test_add_posthog_presentations.py -v
```

Expected: `ModuleNotFoundError: No module named 'add_posthog_presentations'`.

**Step 3: Write the implementation**

Create `scripts/add_posthog_presentations.py`:

```python
#!/usr/bin/env python3
"""
Add PostHog to every presentations/*/presentation Vite project.

Writes src/analytics.ts, adds the posthog-js dependency, and adds a
single side-effect import to src/main.tsx.

The presentation entry index.html is NOT touched: the build overwrites
it with cp dist/index.html index.html.

Usage:
    python3 scripts/add_posthog_presentations.py --test
    python3 scripts/add_posthog_presentations.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import posthog_config as cfg

POSTHOG_KEY = cfg.POSTHOG_KEY
API_HOST = cfg.API_HOST
SDK_DEFAULTS = cfg.SDK_DEFAULTS
SCRIPT_ID = cfg.SCRIPT_MARKER
TRIGGER_EVENTS = cfg.TRIGGER_EVENTS
LOAD_DELAY_MS = cfg.LOAD_DELAY_MS
MAX_QUEUE = cfg.MAX_QUEUE

PRESENTATIONS_DIR = cfg.PRESENTATIONS_DIR

POSTHOG_JS_VERSION = "^1.421.0"

ANALYTICS_TS_TEMPLATE = """// PostHog — generated by scripts/add_posthog_presentations.py
// Lazy load on first interaction or {delay}ms. Mirrors the loader in
// scripts/add_posthog.py so the static site and the decks behave alike.

const API_HOST = "{api_host}";
const PROJECT_KEY = "{key}";
const DEFAULTS = "{defaults}";
const LOAD_DELAY_MS = {delay};
const MAX_QUEUE = {max_queue};
const TRIGGER_EVENTS = {events};

type PostHogClient = {{
  init: (key: string, config: Record<string, unknown>) => void;
  capture: (name: string, properties?: Record<string, unknown>) => void;
}};

type WindowWithAnalytics = Window & {{
  posthog?: PostHogClient;
  gtag?: (...args: unknown[]) => void;
}};

const win = window as WindowWithAnalytics;
const queue: Array<[string, Record<string, unknown>]> = [];
let loaded = false;
let injected = false;

function client(): PostHogClient | null {{
  const c = win.posthog;
  return c !== undefined && typeof c.capture === "function" ? c : null;
}}

function enqueue(name: string, props: Record<string, unknown>): void {{
  if (loaded) {{
    const c = client();
    if (c !== null) c.capture(name, props);
    return;
  }}
  if (queue.length < MAX_QUEUE) queue.push([name, props]);
}}

function flush(): void {{
  const c = client();
  if (!loaded || c === null) return;
  while (queue.length > 0) {{
    const item = queue.shift();
    if (item !== undefined) c.capture(item[0], item[1]);
  }}
}}

function start(): void {{
  if (injected) return;
  injected = true;
  const s = document.createElement("script");
  s.id = "{script_id}";
  s.type = "text/javascript";
  s.crossOrigin = "anonymous";
  s.async = true;
  s.src = API_HOST.replace(".i.posthog.com", "-assets.i.posthog.com") + "/static/array.js";
  s.onload = () => {{
    const c = client();
    if (c === null) return;
    c.init(PROJECT_KEY, {{
      api_host: API_HOST,
      defaults: DEFAULTS,
      capture_pageview: false,
      autocapture: true,
    }});
    loaded = true;
    c.capture("$pageview", {{
      $current_url: window.location.href,
      $referrer: document.referrer,
    }});
    flush();
  }};
  document.head.appendChild(s);
}}

// Bridge the deck's existing gtag('event', ...) calls into PostHog.
function bridgeGtag(): void {{
  const original = win.gtag;
  if (typeof original !== "function") return;
  win.gtag = (...args: unknown[]): void => {{
    original(...args);
    if (args[0] !== "event" || typeof args[1] !== "string") return;
    const params = (args[2] ?? {{}}) as Record<string, unknown>;
    const props: Record<string, unknown> = {{}};
    if (params.event_category !== undefined) props.category = params.event_category;
    if (params.event_label !== undefined) props.label = params.event_label;
    if (params.value !== undefined) props.value = params.value;
    if (params.non_interaction !== undefined) props.non_interaction = params.non_interaction;
    enqueue(args[1], props);
    if (!loaded) start();
  }};
}}

function onFirstInteraction(): void {{
  start();
  for (const name of TRIGGER_EVENTS) {{
    document.removeEventListener(name, onFirstInteraction, true);
  }}
}}

bridgeGtag();
for (const name of TRIGGER_EVENTS) {{
  document.addEventListener(name, onFirstInteraction, {{ capture: true, passive: true }});
}}
window.setTimeout(start, LOAD_DELAY_MS);
"""

MAIN_TSX_IMPORT = 'import "./analytics";'


def render_analytics_ts() -> str:
    """Build the analytics module source."""
    return ANALYTICS_TS_TEMPLATE.format(
        delay=LOAD_DELAY_MS,
        api_host=API_HOST,
        key=POSTHOG_KEY,
        defaults=SDK_DEFAULTS,
        max_queue=MAX_QUEUE,
        events=json.dumps(TRIGGER_EVENTS),
        script_id=SCRIPT_ID,
    )


def add_dependency(pkg: dict):
    """Return (new_pkg, changed). Adds posthog-js to dependencies."""
    deps = pkg.setdefault("dependencies", {})
    if "posthog-js" in deps:
        return pkg, False
    deps["posthog-js"] = POSTHOG_JS_VERSION
    return pkg, True


def patch_main_tsx(src: str):
    """Return (new_src, changed). Adds the side-effect import after App."""
    if MAIN_TSX_IMPORT in src:
        return src, False
    anchor = 'import App from "./App";'
    if anchor not in src:
        return src, False
    return src.replace(anchor, f"{anchor}\n{MAIN_TSX_IMPORT}", 1), True


def collect_projects(presentations_dir: Path):
    """Every presentations/<slug>/presentation directory containing package.json."""
    found = []
    for child in sorted(presentations_dir.iterdir()):
        if not child.is_dir():
            continue
        project = child / "presentation"
        if (project / "package.json").exists():
            found.append(project)
    return found


def process(projects):
    """Apply all three edits. Returns a stats dict."""
    stats = {"projects": len(projects), "deps": 0, "modules": 0, "main": 0, "errors": 0}
    module_src = render_analytics_ts()
    dry_run = "--test" in sys.argv

    for project in projects:
        name = project.parent.name
        try:
            pkg_path = project / "package.json"
            pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
            new_pkg, dep_changed = add_dependency(pkg)
            if dep_changed:
                stats["deps"] += 1
                if not dry_run:
                    pkg_path.write_text(
                        json.dumps(new_pkg, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8",
                    )

            analytics_path = project / "src" / "analytics.ts"
            if not analytics_path.exists():
                stats["modules"] += 1
                if not dry_run:
                    analytics_path.write_text(module_src, encoding="utf-8")

            main_path = project / "src" / "main.tsx"
            main_src = main_path.read_text(encoding="utf-8")
            new_src, main_changed = patch_main_tsx(main_src)
            if main_changed:
                stats["main"] += 1
                if not dry_run:
                    main_path.write_text(new_src, encoding="utf-8")

            changed = dep_changed or main_changed or not analytics_path.exists()
            print(f"  {'patch ' if changed else 'skip  '} {name}")
        except (OSError, ValueError, KeyError) as exc:
            print(f"  ERROR {name}: {exc}")
            stats["errors"] += 1

    return stats


def main():
    projects = collect_projects(PRESENTATIONS_DIR)
    mode = "DRY RUN (pass no --test to write)" if "--test" in sys.argv else "WRITE"
    print(f"add_posthog_presentations.py — {len(projects)} projects — {mode}\n")
    stats = process(projects)
    print(
        f"\nprojects={stats['projects']} deps={stats['deps']} "
        f"modules={stats['modules']} main={stats['main']} errors={stats['errors']}"
    )
    if stats["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 4: Run the test to confirm it passes**

```
python3 -m pytest scripts/test_add_posthog_presentations.py -v
```

Expected: 12 passed.

**Step 5: Dry run, then write**

```
python3 scripts/add_posthog_presentations.py --test | tail -8
python3 scripts/add_posthog_presentations.py | tail -8
```

Expected: `projects=40 deps=40 modules=40 main=40 errors=0`.

**Step 6: Typecheck one project before installing all 40**

```
cd presentations/01-hong-kong-wedding-flow/presentation && npm install && npm run build
```

Expected: no errors. This is the gate — `erasableSyntaxOnly` and `noUnusedLocals` are enabled, and the generated module must satisfy both. Fix `render_analytics_ts()` before proceeding if tsc complains.

**Step 7: Install and build all 40**

```
bash presentations/build-scripts/build-all.sh
```

This script installs and builds sequentially. It is long-running (40 npm installs + 40 Vite builds). Expect 20–40 minutes.

If the script fails partway, resume by iterating the remaining directories directly:

```
cd presentations && for d in */presentation; do (cd "$d" && npm install --silent && npm run build) || echo "FAILED: $d"; done
```

**Step 8: Verify the build output**

```
ls presentations/01-hong-kong-wedding-flow/presentation/dist/assets/ | grep -i posthog
grep -c 'G-GQLW7LNP6H' presentations/01-hong-kong-wedding-flow/presentation/index.html
for d in presentations/*/presentation; do [ -f "$d/index.html" ] || echo "MISSING: $d"; done
git status --porcelain presentations/ | wc -l
```

Expected:
- a `posthog-*.js` chunk in `dist/assets/`
- `1` — GA4 tag survived the build
- no `MISSING:` lines
- a non-zero changed-file count (40 projects × package.json, package-lock.json, main.tsx, analytics.ts, index.html, dist/)

**Step 9: Commit**

```
git add scripts/add_posthog_presentations.py scripts/test_add_posthog_presentations.py presentations/
git commit -m "feat(analytics): add PostHog to all 40 Vite presentations"
```

---

## Task 6: Documentation and end-to-end verification

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `scripts/AGENTS.md`
- Modify: `presentations/AGENTS.md`
- Modify: `privacy.html`
- Create: `docs/lessons/posthog-deferred-load.md`

**Step 1: Update the privacy policy (PDPO obligation)**

Open `privacy.html` and add a subsection under the analytics section stating that PostHog is used in addition to Google Analytics, that it records page views, autocaptured clicks, heatmaps, session replays, and Web Vitals, that IP addresses are anonymised at ingestion, that session replay is sampled at 10%, and that recordings are retained for 30 days.

This is a real legal requirement, not documentation polish. Hong Kong's PDPO requires transparency about the purpose of data collection, and enabling session replay without disclosing it is a genuine compliance gap.

If `privacy.html` is generated by a script, edit the script, not the output.

**Step 2: Update `README.md`**

In the analytics or tracking section, add:

```markdown
### PostHog

Product analytics via PostHog (project: MyO Cert Holder), alongside GA4 (`G-GQLW7LNP6H`).
GA4 remains the source of truth for traffic reporting; PostHog provides
autocapture, heatmaps, session replay, and Web Vitals.

The SDK loads lazily — on first interaction or after 3s — so it does not
affect first paint. Configuration lives in `scripts/posthog_config.py`.
```

**Step 3: Update `AGENTS.md`**

Add to the file map:

```markdown
| `scripts/posthog_config.py` | PostHog 專案金鑰與 SDK 設定（單一來源） |
| `scripts/add_posthog.py` | 批次注入延遲載入的 PostHog loader（`--test` dry-run） |
| `scripts/add_posthog_csp.py` | 為 4 個 CSP 頁面加入 PostHog allowlist |
| `scripts/add_posthog_presentations.py` | 為 40 個 Vite 簡報加入 PostHog 模組 |
```

Add to the core commands block:

```bash
python3 scripts/add_posthog.py --test
python3 scripts/add_posthog_csp.py --test
python3 scripts/add_posthog_presentations.py --test
```

Add to Anti-Patterns:

```markdown
- 勿在 CSP 中列舉 PostHog 特定子網域 — 一律用 `https://*.posthog.com`
- 勿移除 PostHog 的 `worker-src 'self' blob: data:` — 缺少時 session replay 靜默失效
- 勿在 `frame-ancestors` 上嘗試修 CSP — meta 標籤會忽略該 directive
```

**Step 4: Update `scripts/AGENTS.md` and `presentations/AGENTS.md`**

In `scripts/AGENTS.md`, add the three new scripts to the appropriate category and their `--test` usage to the commands table.

In `presentations/AGENTS.md`, document that every presentation now carries a generated `src/analytics.ts` and that `presentations/01-hong-kong-wedding-flow/presentation` is the scaffold template, so a new deck inherits PostHog automatically. Note that hand-editing `presentation/index.html` is pointless because the build overwrites it.

**Step 5: Write the lesson file**

Create `docs/lessons/posthog-deferred-load.md`:

```markdown
# 教訓：PostHog 延遲載入的三個靜默陷阱

> **日期**：2026-09-26
> **狀態**：已解決

---

### 問題
1. 延遲載入後 `$pageview` 的時間戳是「互動時刻」而非「頁面載入時刻」，
   1.5 秒內跳出��訪客完全不會被記錄。
2. 缺少 `worker-src 'self' blob: data:` 時，session replay 靜默失效，
   console 沒有任何錯誤。
3. 在 `<meta>` CSP 中加入 `frame-ancestors` 完全無效（spec 忽略 meta 形式的
   該 directive），看起來像修好了但其實沒有。

### 教訓
PostHog 的 lazy-load 把「載入成本」換成了「時間戳失真」與「更多 CSP 依賴」。
延遲載入時必須 `capture_pageview: false` + 手動補發 `$pageview`，
且 worker-src 是 session replay 的硬性前提，不能靠錯誤訊號發現。

### 解法
`scripts/posthog_config.py` 集中管理設定；三個腳本（靜態頁、CSP、簡報）
各自有 pytest 覆蓋 idempotency 與 directive 存在性。

### 預防
新增任何延遲載入的第三方 SDK 時，先確認三件事：
(1) 首屏事件時間戳是否失真；(2) 是否依賴 CSP 中不存在的 directive；
(3) 事件是否在 SDK 就緒前觸發，需要 queue。
```

**Step 6: Run the full verification suite**

```
python3 -m pytest scripts/ -q
npm test
npm run build:css
```

All three must pass before committing.

**Step 7: Commit**

```
git add README.md AGENTS.md scripts/AGENTS.md presentations/AGENTS.md privacy.html docs/lessons/posthog-deferred-load.md
git commit -m "docs: document PostHog integration and deferred-load pitfalls"
```

**Step 8: Verify end-to-end after deployment**

Push to `main`, wait for GitHub Pages to deploy (2–5 minutes), then:

```
python3 -m http.server 8000
```

Open `http://localhost:8000/` in a browser. Open the network panel filtered to `posthog`. Confirm:

1. A request to `us-assets.i.posthog.com/static/array.js` after first interaction
2. A POST to `us.i.posthog.com/i/v0/e/` carrying `$pageview`
3. No CSP violation in the console on `index.html`, `v2.html`, `poster.html`, or `heic-converter.html`

Click the WhatsApp button, then in PostHog switch to the new project and open **Activity → Live events**:

```
posthog_exec: call project-get {}
```

Confirm `click_whatsapp` arrives. This is Review Focus #2 — the event most likely to be lost to the load race, and the one worth checking by hand.

Then open **Activity → Recordings** and confirm at least one recording exists. This is Review Focus #5 — absence of console errors does not mean replay works.

**Step 9: Record the outcome**

Report to the user:
- Project id and token location (`scripts/posthog_config.py`)
- Files changed: 430 static pages, 4 CSP patches, 40 presentations
- Live-event confirmation for `click_whatsapp`
- Recording confirmation
- The late-load pageview trade-off, restated so it is a documented decision rather than a future surprise

---

## Self-Review Checklist

Run before declaring the plan complete.

- [x] Every task specifies files to create/modify with exact paths
- [x] Every code block is complete and runnable — no `...`, no omitted helpers
- [x] Every test has an explicit command with an expected result
- [x] Every write step has its dry-run counterpart
- [x] Every script has a `--test` mode
- [x] Task commits are staged file-by-file, not `git add -A`
- [x] No placeholders remain — the `import json` gap in Task 2 and the
      `PLACEHOLDER_US` line in Task 4 were both fixed in place, not deferred
      to a "fix this before running" note
- [x] Global Constraints are referenced by the tasks that depend on them
- [x] The two open decisions (region, replay consent) were surfaced as a
      blocking gate rather than silently assumed, then **answered by the user**:
      US Cloud, and replay fully open with no consent banner. Both are recorded
      in Task 1 Step 0 with their downstream consequences.

### Verified against the repository during self-review

- [x] Playwright `testDir` is `./tests`, so the spec is `tests/posthog.spec.ts`
      (not `tests/e2e/…`)
- [x] `playwright.config.js` sets `baseURL: 'http://localhost:8080'` and has no
      `webServer` block — Task 4 Step 6 now starts `python3 -m http.server 8080`
      first
- [x] Presentations use React `^19.2.6` / Vite `^8.0.12`; test fixtures updated
      to match instead of pinning invented versions
- [x] `npm run build` already runs `tsc -b`, so Task 5 uses it as the type gate
      rather than a redundant `npx tsc --noEmit`
- [x] `presentation/dist/` is **not** gitignored (contradicting the README's
      2026-06-21 changelog note) and `assets` is a symlink to `dist/assets`, so
      `git add presentations/` does stage the rebuilt bundles
- [x] E2E console listener is registered before `page.goto()` so CSP violations
      raised during initial load are actually observed
- [x] E2E static assertions use the `request` fixture, removing the race against
      the 3000 ms lazy-load timer

### Still required before implementation starts

- [x] **Resolved** — region = US Cloud; session replay = all open, no banner.
      Both recorded in Task 1 Step 0.
- [x] **Resolved** — project name confirmed by the user as **`MyO Cert Holder`**.
      Admin access and plan quota verified via `project-get` (`user_access_level: admin`,
      `effective_membership_level: 8`). `project-create` is now unblocked.
- [ ] `schema project-settings-update app_urls` and `… capture_dead_clicks`
      resolved against the live schema (both carry a `DO NOT GUESS` hint)
- [ ] `switch-project` issued after creation — a newly created project does not
      become the active project automatically, so later MCP calls would hit the
      wrong project

