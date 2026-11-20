#!/usr/bin/env python3
"""Wire the five newer card families into the nav of every Docs page and the
Docs/index.html card grid, from the pages' real card counts. Idempotent:
removes each family's earlier group first, then inserts all of them before
Band matrices."""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "Docs")
FAMILIES = [
    ("bijvoeglijke-naamwoorden", "Bijvoeglijke naamwoorden", "Contrast sets of adjectives"),
    ("zelfstandige-naamwoorden", "Zelfstandige naamwoorden", "Nouns with article and plural"),
    ("bijwoorden", "Bijwoorden", "Adverbs as contrast pairs"),
    ("scheidbare-werkwoorden", "Scheidbare werkwoorden", "Separable verbs, split form and perfect"),
    ("vaste-uitdrukkingen", "Vaste uitdrukkingen", "Fixed chunks as contrast pairs"),
]
SINGLES = [
    ("card-families-handover.html", "Card families handover", "State, rules, rebuild commands and open items."),
    ("lexicon/themes-to-card.html", "Words still to teach, by theme", "Uncarded words grouped by semantic theme."),
    ("explanation-cards-pilot.html", "Explanation cards pilot", "Ten skipped verbs as picture, picture-plus-question or Dutch scene cards."),
]
SINGLES_NAME = "Card families"
ANCHOR = '<details class="nav-group" data-open="0"><summary>Band matrices</summary>'
CARDS_ANCHOR = '<section class="index-group"><h2>Band matrices</h2>'

def pages(d):
    out = [("index.html", "Overview", None)]
    for b in ("a0", "a1", "a2", "b1", "b2"):
        p = os.path.join(DOCS, d, b + ".html")
        if os.path.exists(p):
            n = open(p, encoding="utf-8").read().count('class="kaart"')
            if n: out.append((b + ".html", f"{b.upper()} band", n))
    return out

def nav(d, name, prefix):
    items = "".join(f'<li><a href="{prefix}{d}/{h}" data-path="Docs/{d}/{h}">{l}</a></li>' for h, l, _ in pages(d))
    return f'<details class="nav-group" data-open="0"><summary>{name}</summary><ul>{items}</ul></details>'

def cards(d, name, blurb):
    c = ""
    for h, l, n in pages(d):
        desc = blurb if n is None else f"{n} cards."
        c += f'<a class="index-card" href="{d}/{h}" data-path="Docs/{d}/{h}"><b>{l}</b><span>{desc}</span><code>Docs/{d}/{h}</code></a>'
    return f'<section class="index-group"><h2>{name}</h2><div class="index-grid">{c}</div></section>'

def singles_nav(prefix):
    items = "".join(f'<li><a href="{prefix}{h}" data-path="Docs/{h}">{l}</a></li>'
                    for h, l, _ in SINGLES if os.path.exists(os.path.join(DOCS, h)))
    return f'<details class="nav-group" data-open="0"><summary>{SINGLES_NAME}</summary><ul>{items}</ul></details>' if items else ""

def singles_cards():
    c = "".join(f'<a class="index-card" href="{h}" data-path="Docs/{h}"><b>{l}</b><span>{d}</span><code>Docs/{h}</code></a>'
                for h, l, d in SINGLES if os.path.exists(os.path.join(DOCS, h)))
    return f'<section class="index-group"><h2>{SINGLES_NAME}</h2><div class="index-grid">{c}</div></section>' if c else ""

n = 0
for path in sorted(glob.glob(os.path.join(DOCS, "**", "*.html"), recursive=True)):
    t = open(path, encoding="utf-8").read(); o = t
    if ANCHOR not in t: continue
    for d, name, blurb in FAMILIES:
        t = re.sub(r'<details class="nav-group" data-open="0"><summary>' + re.escape(name) + r'</summary>.*?</details>\s*', "", t, flags=re.S)
        t = re.sub(r'<section class="index-group"><h2>' + re.escape(name) + r'</h2>.*?</section>', "", t, flags=re.S)
    t = re.sub(r'<details class="nav-group" data-open="0"><summary>' + re.escape(SINGLES_NAME) + r'</summary>.*?</details>\s*', "", t, flags=re.S)
    t = re.sub(r'<section class="index-group"><h2>' + re.escape(SINGLES_NAME) + r'</h2>.*?</section>', "", t, flags=re.S)
    m = re.search(r'href="([^"]*?)voorzetselpaden/index\.html"', t)
    prefix = m.group(1) if m else ""
    t = t.replace(ANCHOR, singles_nav(prefix) + ("\n    " if singles_nav(prefix) else "") + "".join(nav(d, nm, prefix) + "\n    " for d, nm, _ in FAMILIES) + ANCHOR, 1)
    if os.path.relpath(path, DOCS) == "index.html":
        assert CARDS_ANCHOR in t
        t = t.replace(CARDS_ANCHOR, singles_cards() + "".join(cards(*f) for f in FAMILIES) + CARDS_ANCHOR, 1)
    if t != o:
        open(path, "w", encoding="utf-8").write(t); n += 1
print(n, "pages updated")
