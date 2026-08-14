#!/usr/bin/env python3
"""Look over the whole site and report what is broken or unfinished.

    python3 tools/check.py            # everything
    python3 tools/check.py --brief    # one line per category

Run it before publishing. It reads the files on disk - it does not need a
server, a network connection or a browser - and reports six things:

    structure   HTML that does not close, duplicate ids, dead anchors
    links       internal hrefs that point at nothing
    images      referenced files that are missing, and files nothing uses
    weight      anything over the 400 KB ceiling images/README.md sets
    content     placeholders, XXX markers, template copy still in place
    meta        title, description, canonical, og:image, noindex per page

Exit code is 0 when nothing is broken, 1 when something is. Unfinished
content is reported but never fails the run - it is a count to look at, not
an error, and the site is deliberately full of it while it is being written.
"""

import argparse
import glob
import html.parser
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
SIZE_CEILING = 400 * 1024

BOLD, DIM, RED, YEL, GRN, OFF = "\033[1m", "\033[2m", "\033[31m", "\033[33m", "\033[32m", "\033[0m"
if not sys.stdout.isatty():
    BOLD = DIM = RED = YEL = GRN = OFF = ""


def pages():
    out = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    out += sorted(glob.glob(os.path.join(ROOT, "writing", "*.html")))
    return out


def rel(p):
    return os.path.relpath(p, ROOT)


class Nesting(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("stray </%s>" % tag)
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for j in range(len(self.stack) - 1, i, -1):
                    self.errors.append("<%s> opened line %d never closed"
                                       % (self.stack[j][0], self.stack[j][1]))
                del self.stack[i:]
                return
        self.errors.append("stray </%s>" % tag)


def check_structure():
    bad = []
    for p in pages():
        s = open(p, encoding="utf-8").read()
        n = Nesting()
        n.feed(s)
        for e in n.errors:
            bad.append("%s: %s" % (rel(p), e))
        for tag, line in n.stack:
            bad.append("%s: <%s> opened line %d never closed" % (rel(p), tag, line))

        ids = re.findall(r'\sid="([^"]+)"', s)
        for dup in {i for i in ids if ids.count(i) > 1}:
            bad.append('%s: duplicate id="%s"' % (rel(p), dup))

        # same-page anchors must exist on that page
        for frag in set(re.findall(r'href="#([^"]+)"', s)):
            if frag not in ids:
                bad.append('%s: href="#%s" has no matching id' % (rel(p), frag))
    return bad


def check_links():
    bad = []
    for p in pages():
        s = open(p, encoding="utf-8").read()
        for href in set(re.findall(r'href="(/[^"#?]*)"', s)):
            if href == "/":
                continue
            if not os.path.exists(os.path.join(ROOT, href.lstrip("/"))):
                bad.append("%s: -> %s" % (rel(p), href))
        # relative hrefs that are not anchors, mail or external
        for href in set(re.findall(r'href="(?!https?:|mailto:|#|/)([^"]+)"', s)):
            target = os.path.normpath(os.path.join(os.path.dirname(p), href.split("#")[0]))
            if href.split("#")[0] and not os.path.exists(target):
                bad.append("%s: -> %s" % (rel(p), href))
    return bad


def check_images():
    referenced, missing = set(), []
    for p in pages():
        s = open(p, encoding="utf-8").read()
        for attr in ("src", "data-src"):
            for v in re.findall(r'\b%s="([^"]+\.(?:jpg|jpeg|png|svg|gif|avif|webp))"' % attr, s, re.I):
                if v.startswith(("http", "data:")):
                    continue
                key = v.lstrip("/")
                referenced.add(key)
                if not os.path.exists(os.path.join(ROOT, key)):
                    missing.append("%s: %s" % (rel(p), v))
    css = open(os.path.join(ROOT, "style.css"), encoding="utf-8").read()
    for v in re.findall(r'url\(["\']?([^"\')]+\.(?:jpg|jpeg|png|svg|gif|avif|webp))', css, re.I):
        if not v.startswith(("http", "data:")):
            referenced.add(v.lstrip("/"))

    on_disk = set()
    for root, _, files in os.walk(os.path.join(ROOT, "images")):
        for fn in files:
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".svg", ".gif", ".avif", ".webp")):
                on_disk.add(rel(os.path.join(root, fn)))
    unused = sorted(on_disk - referenced)
    return missing, unused


def check_weight():
    heavy = []
    for root, _, files in os.walk(os.path.join(ROOT, "images")):
        for fn in files:
            p = os.path.join(root, fn)
            try:
                size = os.path.getsize(p)
            except OSError:
                continue
            if size > SIZE_CEILING:
                heavy.append((size, rel(p)))
    for extra in ("fonts.css", "style.css", "og.jpg"):
        p = os.path.join(ROOT, extra)
        if os.path.exists(p) and os.path.getsize(p) > SIZE_CEILING:
            heavy.append((os.path.getsize(p), extra))
    return sorted(heavy, reverse=True)


def check_content():
    counts = defaultdict(int)
    where = defaultdict(list)
    patterns = {
        "unwritten passages": r'is-placeholder',
        "XXX markers": r'XXX',
        "template copy": r'Headline of the (?:first|second) essay|An opinion piece, in eight|Month 2026',
    }
    for p in pages():
        s = open(p, encoding="utf-8").read()
        for label, pat in patterns.items():
            n = len(re.findall(pat, s))
            if n:
                counts[label] += n
                where[label].append("%s (%d)" % (rel(p), n))
    counts["cv.pdf missing"] = 0 if os.path.exists(os.path.join(ROOT, "cv.pdf")) else 1
    return counts, where


def check_meta():
    rows = []
    for p in pages():
        s = open(p, encoding="utf-8").read()
        def has(pat):
            return bool(re.search(pat, s))
        rows.append({
            "page": rel(p),
            "title": has(r"<title>[^<]+</title>"),
            "desc": has(r'name="description" content="[^"]+"'),
            "canonical": has(r'rel="canonical"'),
            "og:image": has(r'property="og:image"'),
            "noindex": has(r'name="robots"[^>]*noindex'),
            "csp": has(r'http-equiv="Content-Security-Policy"'),
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description="Report what is broken or unfinished.")
    ap.add_argument("--brief", action="store_true", help="one line per category")
    args = ap.parse_args()

    broken = 0
    print("\n%sChecking %d pages in %s%s" % (BOLD, len(pages()), rel(ROOT) or ".", OFF))

    # --- structure
    bad = check_structure()
    broken += len(bad)
    print("\n%sstructure%s  %s" % (BOLD, OFF,
          ("%sok%s" % (GRN, OFF)) if not bad else ("%s%d problems%s" % (RED, len(bad), OFF))))
    if bad and not args.brief:
        for b in bad[:20]:
            print("    %s" % b)

    # --- links
    bad = check_links()
    broken += len(bad)
    print("%slinks%s      %s" % (BOLD, OFF,
          ("%sok%s" % (GRN, OFF)) if not bad else ("%s%d dead%s" % (RED, len(bad), OFF))))
    if bad and not args.brief:
        for b in bad[:20]:
            print("    %s" % b)

    # --- images
    missing, unused = check_images()
    broken += 0  # a missing picture hides its own frame; it is not a break
    print("%simages%s     %s missing, %s unused" % (
        BOLD, OFF,
        ("%s%d%s" % (YEL, len(missing), OFF)) if missing else ("%s0%s" % (GRN, OFF)),
        ("%s%d%s" % (DIM, len(unused), OFF)) if unused else "0"))
    if not args.brief:
        for b in missing[:12]:
            print("    missing  %s" % b)
        if len(missing) > 12:
            print("    %s... and %d more%s" % (DIM, len(missing) - 12, OFF))
        for b in unused[:8]:
            print("    %sunused   %s%s" % (DIM, b, OFF))
        if len(unused) > 8:
            print("    %s... and %d more%s" % (DIM, len(unused) - 8, OFF))

    # --- weight
    heavy = check_weight()
    print("%sweight%s     %s" % (BOLD, OFF,
          ("%sall under 400 KB%s" % (GRN, OFF)) if not heavy
          else ("%s%d files over 400 KB%s" % (YEL, len(heavy), OFF))))
    if heavy and not args.brief:
        for size, name in heavy[:10]:
            print("    %6.0f KB  %s" % (size / 1024, name))

    # --- content
    counts, where = check_content()
    total = sum(v for k, v in counts.items() if k != "cv.pdf missing")
    print("%scontent%s    %s%d unfinished%s" % (BOLD, OFF, YEL if total else GRN, total, OFF))
    if not args.brief:
        for label in ("unwritten passages", "XXX markers", "template copy"):
            if counts.get(label):
                print("    %-20s %d" % (label, counts[label]))
        if counts["cv.pdf missing"]:
            print("    %-20s two buttons link to it" % "cv.pdf missing")

    # --- meta
    rows = check_meta()
    # a 404 deliberately has no canonical - it must not declare itself the
    # preferred version of anything
    gaps = [r for r in rows
            if not (r["title"] and r["desc"]
                    and (r["canonical"] or r["page"] == "404.html"))]
    noindexed = [r["page"] for r in rows if r["noindex"]]
    nocsp = [r["page"] for r in rows if not r["csp"]]
    print("%smeta%s       %s, %d noindexed, %d without CSP" % (
        BOLD, OFF,
        ("%sall pages tagged%s" % (GRN, OFF)) if not gaps
        else ("%s%d pages missing a tag%s" % (YEL, len(gaps), OFF)),
        len(noindexed), len(nocsp)))
    if not args.brief:
        for r in gaps:
            lack = [k for k in ("title", "desc", "canonical") if not r[k]]
            print("    %s: no %s" % (r["page"], ", ".join(lack)))
        if noindexed:
            print("    %snoindex: %s%s" % (DIM, ", ".join(noindexed), OFF))

    print("\n%s%s%s\n" % (
        GRN if not broken else RED,
        "Nothing broken." if not broken else "%d structural problems - fix before publishing." % broken,
        OFF))
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
