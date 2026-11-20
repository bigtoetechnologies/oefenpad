#!/usr/bin/env python3
"""Insert the Werkwoorden nav group before Band matrices on every doc page.

The href prefix is derived from the page's existing voorzetselpaden link, so
the same markup works at Docs/, Docs/lexicon/, Docs/archive/ and
Docs/werkwoorden/.  Idempotent: pages that already have the group are skipped.
"""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(ROOT, "Docs")

PAGES = [
    ("index.html", "Overview — every verb"),
    ("a0-irregular.html", "A0 irregular"),
    ("a0-regular.html", "A0 regular"),
    ("a1-irregular.html", "A1 irregular"),
    ("a1-regular.html", "A1 regular"),
    ("a2-irregular.html", "A2 irregular"),
    ("a2-regular.html", "A2 regular"),
    ("b1-irregular.html", "B1 irregular"),
    ("b1-regular.html", "B1 regular"),
    ("matrix.html", "Matrix"),
    ("backlog.html", "Backlog"),
]

ANCHOR = '<details class="nav-group" data-open="0"><summary>Band matrices</summary>'


def group(prefix):
    items = "".join(
        f'<li><a href="{prefix}werkwoorden/{href}" '
        f'data-path="Docs/werkwoorden/{href}">{label}</a></li>'
        for href, label in PAGES
    )
    return (
        '<details class="nav-group" data-open="0"><summary>Werkwoorden</summary>'
        f"<ul>{items}</ul></details>"
    )


changed = 0
for path in sorted(glob.glob(os.path.join(DOCS, "**", "*.html"), recursive=True)):
    text = open(path, encoding="utf-8").read()
    if ANCHOR not in text or "<summary>Werkwoorden</summary>" in text:
        continue
    m = re.search(r'href="([^"]*?)voorzetselpaden/index\.html"', text)
    prefix = m.group(1) if m else ""
    text = text.replace(ANCHOR, group(prefix) + "\n    " + ANCHOR, 1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    changed += 1
    print("wired", os.path.relpath(path, ROOT))

print(f"{changed} pages updated")
