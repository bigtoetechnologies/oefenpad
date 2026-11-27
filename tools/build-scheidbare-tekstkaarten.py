#!/usr/bin/env python3
"""Build the text cards of the separable-verb family.

Input : tools/_sw_tmp/text.cards.tsv
        id, lemma, band, rank, tier, gloss, split, perfect, example_nl, example_en
Output: Docs/scheidbare-werkwoorden/tekst-{a1,a2,b1,b2}.html

A text card teaches one separable verb that has no contrast set and no picture:
the infinitive, the English gloss, the split form, the perfect and one example
sentence with its translation. It sits in the same family as the contrast-set
cards (Docs/scheidbare-werkwoorden/{a0..b2}.html) and the game importer reads
both. The contrast-set pages are built by build-scheidbare-werkwoorden-cards.py;
this script never touches them.

Run:  python3 tools/build-scheidbare-tekstkaarten.py
"""
import csv
import html
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "_sw_tmp", "text.cards.tsv")
OUT = os.path.join(ROOT, "Docs", "scheidbare-werkwoorden")
BANDS = ["a1", "a2", "b1", "b2"]

LEAD = {
    "a1": "The first separable verbs: daily routine and the most common ones.",
    "a2": "Everyday separable verbs without a contrast pair.",
    "b1": "Wider separable verbs: work, study, plans and opinions.",
    "b2": "The less frequent separable verbs.",
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


def picture(row):
    """A drawing, when assets/verbs/<id>.png exists and the row has an alt text."""
    alt = (row.get("alt") or "").strip()
    if not alt or not os.path.exists(os.path.join(ROOT, "assets", "verbs", row["id"] + ".png")):
        return None
    return (f'<img class="beeld" src="../../assets/verbs/{attr(row["id"])}.png" alt="{attr(alt)}" loading="lazy" '
            'style="display:block;width:100%;max-width:170px;height:auto;margin:0 auto 10px">')


def render(row, number):
    cid = row["id"]
    return "\n".join(x for x in [
        f'<article id="{attr(cid)}" class="kaart" data-id="{attr(cid)}" data-band="{row["band"]}" '
        f'data-kind="separable-verb-text" data-status="text" data-severity="">',
        f'<span class="framenummer" title="Frame {number}">#{number}</span>',
        picture(row),
        f'<h3 class="chunk">{esc(row["lemma"])}</h3>',
        f'<p class="gloss">{esc(row["gloss"])}</p>',
        f'<p class="vlaggen"><span>{row["band"].upper()}</span><span>rang {esc(row["rank"])}</span>'
        '<span>tekstkaart</span></p>',
        "<dl>",
        f'<dt>Split form</dt><dd class="split">{esc(row["split"])}</dd>',
        f'<dt>Example</dt><dd class="voorbeeld-nl">{esc(row["example_nl"])}'
        f'<br><span class="voorbeeld-en">{esc(row["example_en"])}</span></dd>',
        f'<dt>Perfect</dt><dd class="perfect">{esc(row["perfect"])}</dd>',
        "</dl>",
        f'<p class="id">{esc(cid)} · {row["band"].upper()} · rang {esc(row["rank"])}</p>',
        "</article>",
    ] if x is not None)


def main():
    fam = load_family_module()
    with open(SRC, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
    nav_items = [("index", "overview")] + [(f"tekst-{b}", f"tekst {b.upper()}") for b in BANDS]

    def nav(cur):
        return "".join(
            f'<a href="{k}.html"' + (' class="hier"' if k == cur else "") + f">{lab}</a>"
            for k, lab in nav_items)

    number = 0
    for band in BANDS:
        sub = sorted((r for r in rows if r["band"] == band), key=lambda r: (int(r["rank"]), r["lemma"]))
        cards = []
        for r in sub:
            number += 1
            cards.append(render(r, number))
        body = f'<div class="kaarten">\n' + "\n".join(cards) + "\n</div>"
        lead = (f"{esc(LEAD[band])} {len(sub)} text cards: infinitive, English gloss, split form, "
                "perfect and one example sentence with its translation. No picture brief.")
        page = fam.shell(f"Scheidbare werkwoorden — tekstkaarten {band.upper()}", lead, nav(f"tekst-{band}"), body)
        with open(os.path.join(OUT, f"tekst-{band}.html"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(page)
        print(f"tekst-{band}.html  {len(sub)} cards")
    print(f"{number} text cards")


if __name__ == "__main__":
    main()
