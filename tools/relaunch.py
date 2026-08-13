#!/usr/bin/env python3
"""Take the site out from behind its holding page.

Run from the repository root:

    python3 tools/relaunch.py --check     # say what would change, touch nothing
    python3 tools/relaunch.py             # do it

Putting the site behind a holding page took five separate edits across
eighteen files, and every one of them has to be undone in the right order or
the site comes back up half-hidden - pages that Google is still told to
ignore, links that point at a filename that no longer exists, a sitemap
listing two pages. This does all five and reports what it touched.

It refuses to run twice, and it changes nothing in git: after it finishes you
review the diff and commit yourself.

What it does NOT undo, on purpose:

  * the five writing/example-*.html templates keep their noindex. They still
    say "Headline of the first essay". Remove the line yourself on the day
    each one holds a real piece.
  * nothing is written about the XXX affiliation, cv.pdf or the unwritten
    passages. Those are content, and the script has no opinion about them -
    but it does count them at the end so the number is in front of you before
    you publish.
"""

import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "https://hannes-meilicke.com"

# The navigation every content page uses, in the order the sections are read.
NAV = [("", "Home"), ("#about", "About"), ("#writing", "Writing"),
       ("#research", "Research"), ("#cv", "CV"), ("#contact", "Contact")]

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{live}/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>
  <url><loc>{live}/writing/books-2025.html</loc><changefreq>yearly</changefreq><priority>0.6</priority></url>
  <url><loc>{live}/writing/books-2024.html</loc><changefreq>yearly</changefreq><priority>0.5</priority></url>
  <url><loc>{live}/writing/books-2023.html</loc><changefreq>yearly</changefreq><priority>0.5</priority></url>
  <url><loc>{live}/writing/books-2022.html</loc><changefreq>yearly</changefreq><priority>0.5</priority></url>
  <url><loc>{live}/writing/books-2021.html</loc><changefreq>yearly</changefreq><priority>0.5</priority></url>
  <url><loc>{live}/writing/books-2020.html</loc><changefreq>yearly</changefreq><priority>0.5</priority></url>
  <url><loc>{live}/writing/books-2019.html</loc><changefreq>yearly</changefreq><priority>0.5</priority></url>
  <url><loc>{live}/writing/books-2018.html</loc><changefreq>yearly</changefreq><priority>0.5</priority></url>
  <url><loc>{live}/impressum.html</loc><changefreq>yearly</changefreq><priority>0.2</priority></url>
  <url><loc>{live}/datenschutz.html</loc><changefreq>yearly</changefreq><priority>0.2</priority></url>
</urlset>
""".format(live=LIVE)


def nav_block(indent, base):
    inner = "\n".join('%s  <a href="%s%s">%s</a>' % (indent, base, frag, label)
                      for frag, label in NAV)
    return '%s<div class="nav-links">\n%s\n%s</div>' % (indent, inner, indent)


class Run:
    def __init__(self, dry):
        self.dry = dry
        self.done = []
        self.warn = []

    def note(self, msg):
        self.done.append(msg)

    def write(self, path, text):
        if not self.dry:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)

    def read(self, path):
        with open(path, encoding="utf-8") as fh:
            return fh.read()


def preflight(run):
    """Refuse to run unless the repo really is in holding-page mode."""
    problems = []
    if not os.path.exists(os.path.join(ROOT, "site.html")):
        problems.append("site.html is missing - the site looks already relaunched")
    if os.path.exists(os.path.join(ROOT, "holding.html")):
        problems.append("holding.html already exists - move it aside first")
    idx = os.path.join(ROOT, "index.html")
    if os.path.exists(idx):
        # read the whole file: these pages are small, and a marker in the body
        # is worth more than one in the head, which comments keep pushing down
        with open(idx, encoding="utf-8") as fh:
            body = fh.read()
        if "This site is being written" not in body:
            problems.append("index.html is not the holding page - stopping rather than guessing")
    return problems


def step_swap(run):
    """index.html (holding) -> holding.html, site.html -> index.html."""
    os.rename(os.path.join(ROOT, "index.html"), os.path.join(ROOT, "holding.html")) if not run.dry else None
    os.rename(os.path.join(ROOT, "site.html"), os.path.join(ROOT, "index.html")) if not run.dry else None
    run.note("index.html (holding) -> holding.html, kept for next time")
    run.note("site.html -> index.html, the real site is the front door again")


def step_home_head(run):
    """The home page stops hiding from search engines and points at / again."""
    p = os.path.join(ROOT, "index.html" if not run.dry else "site.html")
    s = run.read(p)
    before = s
    s = re.sub(r'[ \t]*<!-- The site is behind a holding page\..*?-->\n', '', s, flags=re.S)
    s = re.sub(r'[ \t]*<meta name="robots" content="noindex">\n', '', s)
    s = s.replace('<link rel="canonical" href="%s/site.html">' % LIVE,
                  '<link rel="canonical" href="%s/">' % LIVE)
    s = s.replace('<meta property="og:url" content="%s/site.html">' % LIVE,
                  '<meta property="og:url" content="%s/">' % LIVE)
    if s != before:
        run.write(p, s)
        run.note("home page: noindex removed, canonical and og:url back to /")


def step_writing(run):
    """Reading notes rejoin the index; every /site.html link becomes /."""
    freed = relinked = 0
    for p in sorted(glob.glob(os.path.join(ROOT, "writing", "*.html"))):
        name = os.path.basename(p)
        s = run.read(p)
        before = s
        if name.startswith("books-"):
            s = re.sub(r'[ \t]*<meta name="robots" content="noindex">\n', '', s)
            if s != before:
                freed += 1
        s2 = s.replace('href="/site.html', 'href="/')
        s2 = s2.replace('"/site.html"', '"/"')
        if s2 != s:
            relinked += 1
        s = s2
        if s != before:
            run.write(p, s)
    run.note("writing: %d reading-notes pages are indexable again" % freed)
    run.note("writing: %d pages relinked from /site.html to /" % relinked)
    run.warn.append("the five writing/example-*.html templates keep their noindex - "
                    "remove it per page as you write each piece")


def step_public_nav(run):
    """404 and the two legal pages get the full navigation back."""
    for name in ("404.html", "impressum.html", "datenschutz.html"):
        p = os.path.join(ROOT, name)
        s = run.read(p)
        m = re.search(r'([ \t]*)(<!-- Holding-page mode.*?-->\n)?[ \t]*<div class="nav-links">.*?</div>',
                      s, re.S)
        if not m:
            run.warn.append("%s: no navigation block found, left alone" % name)
            continue
        s = s[:m.start()] + nav_block(m.group(1), "/") + s[m.end():]
        run.write(p, s)
        run.note("%s: navigation restored to the full set" % name)


def step_sitemap(run):
    run.write(os.path.join(ROOT, "sitemap.xml"), SITEMAP)
    run.note("sitemap.xml: 11 pages listed again")


def count_unfinished():
    """Not a gate, just a number to look at before publishing."""
    counts = {}
    for label, pattern, needle in (
        ("draft passages", ["index.html", "site.html", "writing/*.html"], "is-placeholder"),
        ("XXX markers", ["index.html", "site.html"], "XXX"),
    ):
        n = 0
        for pat in pattern:
            for p in glob.glob(os.path.join(ROOT, pat)):
                try:
                    n += open(p, encoding="utf-8").read().count(needle)
                except OSError:
                    pass
        counts[label] = n
    counts["cv.pdf present"] = os.path.exists(os.path.join(ROOT, "cv.pdf"))
    return counts


def main():
    ap = argparse.ArgumentParser(description="Take the site out from behind its holding page.")
    ap.add_argument("--check", action="store_true", help="report only, change nothing")
    args = ap.parse_args()

    problems = preflight(None)
    if problems:
        print("\n  Not in holding-page mode, or not safe to run:\n")
        for p in problems:
            print("    - %s" % p)
        print()
        return 1

    run = Run(dry=args.check)

    if args.check:
        print("\n  DRY RUN - nothing will be written.\n")
        # in check mode the files have not moved, so report intent only
        run.note("index.html (holding) -> holding.html")
        run.note("site.html -> index.html")
        run.note("home page: noindex removed, canonical and og:url back to /")
        run.note("writing: 8 reading-notes pages made indexable, links repointed to /")
        run.note("404 / impressum / datenschutz: navigation restored")
        run.note("sitemap.xml: 11 pages listed again")
        run.warn.append("the five writing/example-*.html templates keep their noindex")
    else:
        step_swap(run)
        step_home_head(run)
        step_writing(run)
        step_public_nav(run)
        step_sitemap(run)

    print("\n  %s\n" % ("Would do:" if args.check else "Done:"))
    for d in run.done:
        print("    %s" % d)
    if run.warn:
        print("\n  Note:\n")
        for w in run.warn:
            print("    %s" % w)

    c = count_unfinished()
    print("\n  Still unfinished, for your eyes before you publish:\n")
    print("    draft passages still marked to-be-written : %d" % c["draft passages"])
    print("    XXX affiliation markers                   : %d" % c["XXX markers"])
    print("    cv.pdf present                            : %s"
          % ("yes" if c["cv.pdf present"] else "NO - two buttons will 404"))

    if not args.check:
        print("\n  Nothing has been committed. Review, then:\n")
        print("    git add -A && git commit -m \"Take the site back out from behind the holding page\"")
        print("    git push origin main\n")
    else:
        print("\n  Run without --check to apply.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
