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
