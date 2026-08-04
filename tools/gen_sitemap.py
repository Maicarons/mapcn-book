#!/usr/bin/env python3
"""Generate docs/public/sitemap.xml for the mapcn-book VitePress site.

Scans all publishable Markdown pages and emits an XML sitemap with absolute
URLs rooted at the GitHub Pages base. Run after adding/removing pages, or wire
into CI. Dependency-free (stdlib only).
"""
import os
import xml.sax.saxutils as su

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
BASE = "https://maicarons.github.io/mapcn-book"

# Static top-level pages (no .md source under a simple route).
STATIC = ["", "preface", "downloads"]

# (directory under docs/, site route prefix)
SECTIONS = [
    ("chapters", "/chapters"),
    ("reference", "/reference"),
    ("zh", "/zh"),
    ("en", "/en"),
]


def md_slugs(dirname: str):
    d = os.path.join(DOCS, dirname)
    if not os.path.isdir(d):
        return []
    return sorted(
        f[:-3] for f in os.listdir(d)
        if f.endswith(".md") and f.lower() != "index.md" and f != "404.md"
    )


def main():
    urls = set()
    for s in STATIC:
        urls.add(f"{BASE}/{s}" if s else f"{BASE}/")
    for dirname, prefix in SECTIONS:
        for slug in md_slugs(dirname):
            urls.add(f"{BASE}{prefix}/{slug}")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in sorted(urls):
        lines.append("  <url>")
        lines.append(f"    <loc>{su.escape(u)}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>\n")

    out = os.path.join(DOCS, "public", "sitemap.xml")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"wrote {out} ({len(urls)} urls)")


if __name__ == "__main__":
    main()
