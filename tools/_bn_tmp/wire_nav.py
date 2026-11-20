#!/usr/bin/env python3
"""Insert the Bijvoeglijke naamwoorden nav group (and an index card group on
Docs/index.html) before Band matrices on every doc page. Idempotent."""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(ROOT, "Docs")
PAGES = [("index.html", "Overview — every adjective", "Contrast sets, the band cuts and how sets were placed."),
         ("a0.html", "A0 band", "Size, age, speed, the open door — 14 cards."),
         ("a1.html", "A1 band", "Temperature, weight, feelings, health, danger — 46 cards."),
         ("a2.html", "A2 band", "Cleanliness, thickness, brightness, edges, company — 22 cards."),
         ("b1.html", "B1 band", "Taste, surface, ripeness, shyness, calm, weather — 14 cards.")]
ANCHOR = '<details class="nav-group" data-open="0"><summary>Band matrices</summary>'
NAME = "Bijvoeglijke naamwoorden"
def group(p):
    items = "".join(f'<li><a href="{p}bijvoeglijke-naamwoorden/{h}" data-path="Docs/bijvoeglijke-naamwoorden/{h}">{l}</a></li>' for h, l, _ in PAGES)
    return f'<details class="nav-group" data-open="0"><summary>{NAME}</summary><ul>{items}</ul></details>'
def cards():
    c = "".join(f'<a class="index-card" href="bijvoeglijke-naamwoorden/{h}" data-path="Docs/bijvoeglijke-naamwoorden/{h}"><b>{l}</b><span>{d}</span><code>Docs/bijvoeglijke-naamwoorden/{h}</code></a>' for h, l, d in PAGES)
    return f'<section class="index-group"><h2>{NAME}</h2><div class="index-grid">{c}</div></section>'
n = 0
for path in sorted(glob.glob(os.path.join(DOCS, "**", "*.html"), recursive=True)):
    t = open(path, encoding="utf-8").read()
    if ANCHOR not in t or f"<summary>{NAME}</summary>" in t: continue
    m = re.search(r'href="([^"]*?)voorzetselpaden/index\.html"', t)
    t = t.replace(ANCHOR, group(m.group(1) if m else "") + "\n    " + ANCHOR, 1)
    if os.path.relpath(path, DOCS) == "index.html":
        a = '<section class="index-group"><h2>Band matrices</h2>'
        assert a in t; t = t.replace(a, cards() + a, 1)
    open(path, "w", encoding="utf-8").write(t); n += 1
print(n, "pages updated")
