#!/usr/bin/env python3
"""Scan the site source for externally-hosted resources and vet their domains.

Two checks, in order of authority:

1. Allowlist (hard gate): every external resource domain found in the source
   must appear in scripts/allowed-external-domains.txt. A new CDN sneaking in
   fails the build until a human adds it deliberately.
2. URLhaus threat feed (best effort): each domain is looked up against
   abuse.ch URLhaus. A positive match fails the scan; network/auth errors
   only warn, since the allowlist is the real gate. Set URLHAUS_AUTH_KEY to
   authenticate (abuse.ch requires a free auth key for API access).

Exit codes: 0 clean, 1 violations found, 2 scanner error.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST_FILE = Path(__file__).resolve().parent / "allowed-external-domains.txt"

# (path, glob) pairs to scan for HTML resource tags. site/ is the built
# output — scanning it catches resources the theme injects at build time
# (fonts, analytics) that never appear in source. Build before running.
HTML_SCAN = [
    (REPO_ROOT / "overrides", "**/*.html"),
    (REPO_ROOT / "docs", "**/*.html"),
    (REPO_ROOT / "site", "**/*.html"),
]
# JS shipped with the site can inject scripts at runtime; flag any URL in it
JS_SCAN = [
    (REPO_ROOT / "docs" / "javascripts", "**/*.js"),
]

# Attribute value may be quoted or (after HTML minification) unquoted
RESOURCE_TAG_RE = re.compile(
    r"<(?:script|link|iframe|embed|source|img)\b[^>]*?(?:src|href)\s*=\s*"
    r"(?:[\"'](https?://[^\"']+)[\"']|(https?://[^\s>\"']+))",
    re.IGNORECASE,
)
BARE_URL_RE = re.compile(r"https?://[^\s\"'`<>()]+")
# Inline <script> bodies — themes inject loaders at runtime (e.g. gtag.js)
INLINE_SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.IGNORECASE | re.DOTALL)


def load_allowlist() -> set[str]:
    domains = set()
    for line in ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            domains.add(line.lower())
    return domains


def domain_of(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.lower().split(":")[0]


def first_party_domains() -> set[str]:
    """The site's own domain (from site_url) — first-party, never flagged."""
    domains = set()
    for line in (REPO_ROOT / "mkdocs.yml").read_text(encoding="utf-8").splitlines():
        match = re.match(r"^site_url\s*:\s*(\S+)", line)
        if match:
            domains.add(domain_of(match.group(1)))
    return domains


def find_external_resources() -> dict[str, set[str]]:
    """Return {domain: {source descriptions}} for every external resource."""
    found: dict[str, set[str]] = {}
    first_party = first_party_domains()

    def record(url: str, source: str) -> None:
        dom = domain_of(url)
        if dom and dom not in first_party:
            found.setdefault(dom, set()).add(source)

    # mkdocs.yml: extra_javascript / extra_css entries with absolute URLs
    mkdocs_yml = REPO_ROOT / "mkdocs.yml"
    in_extra = False
    for lineno, line in enumerate(
        mkdocs_yml.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if re.match(r"^(extra_javascript|extra_css)\s*:", line):
            in_extra = True
            continue
        if in_extra:
            item = re.match(r"^\s+-\s+(https?://\S+)", line)
            if item:
                record(item.group(1), f"mkdocs.yml:{lineno}")
                continue
            if not re.match(r"^\s+-", line):  # left the list block
                in_extra = False

    for base, pattern in HTML_SCAN:
        if not base.is_dir():
            continue
        for path in base.glob(pattern):
            rel = path.relative_to(REPO_ROOT)
            text = path.read_text(encoding="utf-8")
            for match in RESOURCE_TAG_RE.finditer(text):
                record(match.group(1) or match.group(2), str(rel))
            # URLs inside inline scripts (runtime loaders). JSON-LD metadata
            # blocks reference URLs without loading them — skip those.
            for match in INLINE_SCRIPT_RE.finditer(text):
                attrs, body = match.group(1), match.group(2)
                if "ld+json" in attrs.lower():
                    continue
                for url in BARE_URL_RE.finditer(body):
                    record(url.group(0), f"{rel} (inline script)")

    for base, pattern in JS_SCAN:
        if not base.is_dir():
            continue
        for path in base.glob(pattern):
            rel = path.relative_to(REPO_ROOT)
            for match in BARE_URL_RE.finditer(path.read_text(encoding="utf-8")):
                record(match.group(0), str(rel))

    return found


def urlhaus_check(domain: str) -> str | None:
    """Return a description if URLhaus knows the domain as malicious, else None.

    Raises on network/API problems so the caller can downgrade to a warning.
    """
    data = urllib.parse.urlencode({"host": domain}).encode()
    req = urllib.request.Request(
        "https://urlhaus-api.abuse.ch/v1/host/", data=data, method="POST"
    )
    auth_key = os.environ.get("URLHAUS_AUTH_KEY")
    if auth_key:
        req.add_header("Auth-Key", auth_key)
    with urllib.request.urlopen(req, timeout=15) as resp:
        payload = json.loads(resp.read().decode())
    if payload.get("query_status") == "ok" and payload.get("url_count"):
        return f"listed on URLhaus with {payload['url_count']} malicious URL(s)"
    return None


def main() -> int:
    allowlist = load_allowlist()
    resources = find_external_resources()

    if not (REPO_ROOT / "site").is_dir():
        print(
            "warning: site/ not found — run `mkdocs build` first so "
            "theme-injected resources are scanned too",
            file=sys.stderr,
        )

    if not resources:
        print("No externally-hosted resources found in site source.")
        return 0

    failures: list[str] = []
    for dom in sorted(resources):
        sources = ", ".join(sorted(resources[dom]))
        if dom not in allowlist:
            failures.append(
                f"NOT ALLOWLISTED: {dom} (referenced in {sources}) — add to "
                f"{ALLOWLIST_FILE.name} only if you trust it"
            )
        else:
            print(f"allowlisted: {dom} ({sources})")

    for dom in sorted(resources):
        try:
            verdict = urlhaus_check(dom)
        except Exception as exc:  # network / auth — allowlist stays the gate
            print(f"warning: URLhaus lookup failed for {dom}: {exc}", file=sys.stderr)
            continue
        if verdict:
            failures.append(f"THREAT FEED HIT: {dom} — {verdict}")
        else:
            print(f"urlhaus clean: {dom}")

    if failures:
        print("\nExternal resource check FAILED:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("\nExternal resource check passed.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"scanner error: {exc}", file=sys.stderr)
        sys.exit(2)
