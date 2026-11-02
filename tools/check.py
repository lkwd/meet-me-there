#!/usr/bin/env python3
"""Site checks: no placeholder URLs, every local link and asset exists, every #anchor exists.

Usage: python3 tools/check.py            (run from anywhere; checks the repo this file lives in)
       python3 tools/check.py --launch   (also fails while any link in assets/js/config.js is empty)
Standard library only, so it runs the same locally and in CI.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = re.compile(r"REPLACE|example\.com")
SKIP_DIRS = {".git", "node_modules", "tools", ".github"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs = set(), []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src", "poster"):
            if a.get(key):
                self.refs.append((tag, key, a[key], self.getpos()[0]))
        if a.get("srcset"):
            for part in a["srcset"].split(","):
                self.refs.append((tag, "srcset", part.strip().split(" ")[0], self.getpos()[0]))


def site_files(pattern):
    return [p for p in ROOT.rglob(pattern) if not SKIP_DIRS & set(p.relative_to(ROOT).parts)]


def target_file(page, path):
    """Resolve a local URL path from `page` to a file, the way a static host would."""
    base = ROOT if path.startswith("/") else page.parent
    t = (base / unquote(path.lstrip("/"))).resolve()
    if t.is_dir() or path.endswith("/"):
        t = t / "index.html"
    return t


def main():
    errors = []
    pages = {p: Page() for p in site_files("*.html")}
    for p, parser in pages.items():
        parser.feed(p.read_text(encoding="utf-8"))

    for p in site_files("*.html") + site_files("*.js") + site_files("*.css"):
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if PLACEHOLDER.search(line):
                errors.append(f"{p.relative_to(ROOT)}:{n}: placeholder URL: {line.strip()[:100]}")

    for p, parser in pages.items():
        rel = p.relative_to(ROOT)
        if rel.name == "404.html":
            continue  # served at any depth; its links are set by script
        for tag, key, url, line in parser.refs:
            u = urlsplit(url)
            if u.scheme or url.startswith("//") or url.startswith("data:"):
                continue
            if url == "#":
                if tag == "a":
                    continue  # filled from config.js; the element stays hidden until then
                errors.append(f"{rel}:{line}: empty {key} on <{tag}>")
                continue
            target = p if not u.path else target_file(p, u.path)
            if not target.exists():
                errors.append(f"{rel}:{line}: {key}={url} -> missing {target.relative_to(ROOT) if ROOT in target.parents else target}")
                continue
            if u.fragment and target.suffix == ".html":
                ids = pages[target].ids if target in pages else set()
                if u.fragment not in ids:
                    errors.append(f"{rel}:{line}: {key}={url} -> no id \"{u.fragment}\" in {target.relative_to(ROOT)}")

    if "--launch" in sys.argv:
        cfg = (ROOT / "assets/js/config.js").read_text(encoding="utf-8")
        for k, v in re.findall(r'^\s*(\w+):\s*"([^"]*)"', cfg, re.M):
            if k != "launchAt" and not v.strip():
                errors.append(f"assets/js/config.js: links.{k} is empty")
        for p in pages:
            if p.name != "404.html" and 'name="robots" content="noindex"' in p.read_text(encoding="utf-8"):
                errors.append(f"{p.relative_to(ROOT)}: still has noindex (remove on the final domain)")

    for e in errors:
        print(e)
    print(f"{len(pages)} pages checked, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
