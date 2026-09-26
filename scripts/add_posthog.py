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
