#!/usr/bin/env python3
"""Rebuild sitemap.xml from every HTML page in the site.

Any new page (for example blog/my-post/index.html) is picked up
automatically. lastmod comes from the page's last git commit, so editing
a page bumps its date. Pages with <meta name="robots" content="noindex">
and 404.html are left out.
"""
import datetime
import os
import re
import subprocess
import sys
from xml.sax.saxutils import escape

SITE_URL = "https://dhaphase2islamabad.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".github", "node_modules", "scripts", "css", "js", "images", "img"}
SKIP_FILES = {"404.html"}
NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', re.I)


def last_modified(path):
    """Date of the last commit that touched the file, or today if uncommitted."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", path],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        out = ""
    if out and not uncommitted(path):
        return out
    return datetime.date.today().isoformat()


def uncommitted(path):
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--", path],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return False
    return bool(out)


def page_url(rel):
    rel = rel.replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def priority(url):
    depth = url.strip("/").count("/") + 1 if url != "/" else 0
    return {0: "1.0", 1: "0.9", 2: "0.8"}.get(depth, "0.7")


def find_pages():
    pages = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            if not name.endswith(".html") or name in SKIP_FILES:
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8", errors="ignore") as f:
                if NOINDEX.search(f.read()):
                    continue
            rel = os.path.relpath(path, ROOT)
            pages.append((page_url(rel), last_modified(rel)))
    # Home first, then section pages, then deeper pages, alphabetically.
    pages.sort(key=lambda p: (p[0] != "/", p[0].count("/"), p[0]))
    return pages


def build(pages):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, lastmod in pages:
        lines += [
            "  <url>",
            f"    <loc>{escape(SITE_URL + url)}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{priority(url)}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    pages = find_pages()
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(build(pages))
    print(f"sitemap.xml written with {len(pages)} URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
