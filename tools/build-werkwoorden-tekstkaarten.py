#!/usr/bin/env python3
"""Build the usage cards for verbs that cannot be drawn.

Input : tools/_wt_tmp/text.cards.tsv
        slug, lemma, band, rank, gloss, perfect, passage_nl, passage_en,
        collocations, example_nl, example_en
Output: Docs/werkwoorden-tekst/tekst-{b1,b2}.html

An abstract verb (garanderen, beogen, zich richten op) has no honest single
drawing. These cards teach it in use instead: the gloss, a 2-3 sentence passage
with its translation, two or three typical word combinations, the perfect and
one more example sentence. They are B1 and B2 only. The picture cards stay in
Docs/werkwoorden/ (build-verb-cards.py); this script never touches them.

Run:  python3 tools/build-werkwoorden-tekstkaarten.py
"""
import csv
import html
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "_wt_tmp", "text.cards.tsv")
OUT = os.path.join(ROOT, "Docs", "werkwoorden-tekst")
BANDS = ["b1", "b2"]
LEAD = {
    "b1": "Abstract verbs that need a context: opinions, work, news and formal speech.",
    "b2": "Formal and abstract verbs, learned in use rather than from a picture.",
}


def esc(text):
    return html.escape(text, quote=False)


def attr(text):
    return html.escape(text, quote=True)


def load_family_module():
    spec = importlib.util.spec_from_file_location(
        "sw_builder", os.path.join(ROOT, "tools", "build-scheidbare-werkwoorden-cards.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def render(row, number):
    cid = row["slug"]
    colls = [c.strip() for c in row["collocations"].split(" ; ") if c.strip()]
    items = "".join(f"<li>{esc(c)}</li>" for c in colls)
    return "\n".join([
        f'<article id="{attr(cid)}" class="kaart" data-id="{attr(cid)}" data-band="{row["band"]}" '
        f'data-kind="verb-text" data-status="text" data-severity="">',
        f'<span class="framenummer" title="Frame {number}">#{number}</span>',
        f'<h3 class="chunk">{esc(row["lemma"])}</h3>',
        f'<p class="gloss">{esc(row["gloss"])}</p>',
        f'<p class="vlaggen"><span>{row["band"].upper()}</span><span>rang {esc(row["rank"])}</span>'
        '<span>gebruikskaart</span></p>',
        "<dl>",
        f'<dt>In use</dt><dd class="passage-nl">{esc(row["passage_nl"])}'
        f'<br><span class="voorbeeld-en">{esc(row["passage_en"])}</span></dd>',
        f'<dt>Combinations</dt><dd class="combinaties"><ul>{items}</ul></dd>',
        f'<dt>Example</dt><dd class="voorbeeld-nl">{esc(row["example_nl"])}'
        f'<br><span class="voorbeeld-en">{esc(row["example_en"])}</span></dd>',
        f'<dt>Perfect</dt><dd class="perfect">{esc(row["perfect"])}</dd>',
        "</dl>",
        f'<p class="id">{esc(cid)} · {row["band"].upper()} · rang {esc(row["rank"])}</p>',
        "</article>",
    ])


def main():
    fam = load_family_module()
    with open(SRC, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
    os.makedirs(OUT, exist_ok=True)
    nav_items = [(f"tekst-{b}", f"tekst {b.upper()}") for b in BANDS]

    def nav(cur):
        return "".join(
            f'<a href="{k}.html"' + (' class="hier"' if k == cur else "") + f">{lab}</a>"
            for k, lab in nav_items)

    number = 0
    for band in BANDS:
        sub = sorted((r for r in rows if r["band"].lower() == band), key=lambda r: (int(r["rank"]), r["lemma"]))
        cards = []
        for r in sub:
            number += 1
            cards.append(render(r, number))
        body = '<div class="kaarten">\n' + "\n".join(cards) + "\n</div>"
        lead = (f"{esc(LEAD[band])} {len(sub)} usage cards: gloss, a short passage with its translation, "
                "typical combinations, the perfect and one more example. No picture brief.")
        page = fam.shell(f"Werkwoorden — gebruikskaarten {band.upper()}", lead, nav(f"tekst-{band}"), body)
        with open(os.path.join(OUT, f"tekst-{band}.html"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(page)
        print(f"tekst-{band}.html  {len(sub)} cards")
    print(f"{number} usage cards")


if __name__ == "__main__":
    main()
