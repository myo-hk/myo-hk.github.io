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


def _has_host_in_directive(policy: str, directive: str) -> bool:
    """Return True when `directive`'s source list already contains POSTHOG_CSP_HOST."""
    sources = get_directive(policy, directive)
    return POSTHOG_CSP_HOST in sources


def _patch_policy(policy: str):
    """Patch `policy` in place. Returns the (possibly updated) policy string."""
    for directive in REQUIRED_DIRECTIVES:
        policy = _append_to_directive(policy, directive)
        if policy is None:
            return None  # hand-rolled policy — refuse to guess

    if not re.search(r"(?:^|;)\s*worker-src\s", policy):
        policy = policy.rstrip().rstrip(";")
        policy = f"{policy}; {WORKER_SRC}"
    return policy


def _needs_patch(html: str) -> bool:
    """Return True when the page needs patching; False when fully patched.

    A page is considered fully patched only when the PostHog host is present
    in *both* script-src and connect-src.  A partially-patched page (host in
    one directive but not the other) must still be repaired — a coarse
    substring check on the whole HTML would miss that case.
    """
    policy = get_directive(html, "default-src")  # placeholder; checked below
    meta = META_RE.search(html)
    if not meta:
        return False
    policy = meta.group(2)
    return not (_has_host_in_directive(policy, "script-src")
                and _has_host_in_directive(policy, "connect-src"))


def add_csp(html: str):
    """Return (new_html, changed). Idempotent."""
    meta = META_RE.search(html)
    if not meta:
        return html, False
    if not _needs_patch(html):
        return html, False

    policy = meta.group(2)
    policy = _patch_policy(policy)
    if policy is None:
        return html, False

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
            if not _needs_patch(original):
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
