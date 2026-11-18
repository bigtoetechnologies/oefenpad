#!/usr/bin/env python3
"""Build the master vocabulary list from the coursebook appendix and the games.

Two sources, merged on the Dutch word:

  1. `Nederlands in actie`, Bijlage 8 ("Frequente woorden") -- the 5,000 most
     frequent Dutch lemmas, from C. Tiberius & T. Schoonheim (2014),
     *A Frequency Dictionary of Dutch. Core vocabulary for learners*, Routledge.
     Every lemma carries an English gloss and is highlighted in one of three
     colours: light blue = taught in *Nederlands in gang* (A0-A1), medium blue =
     taught there and in the top 2,000, orange = taught in *Nederlands in actie*
     (B1). No highlight = in the 5,000 but in neither coursebook.

     The highlight is a page fill, not a text colour, so `pdftotext` loses it.
     The colour is recovered by rendering each page and sampling the pixels
     behind each word.

  2. The games' word bank: `server/Oefenpad.Resources/Games/Data/words.json`
     (25 themed categories) and `reels.json` (Verhaalmachine tiles).

Output: `tools/lexicon/woorden.tsv`, one row per distinct Dutch word:

    nl        the lemma as written (lowercase for game words)
    en        English gloss
    niveau    A1 | B1 | open | (empty when the word is not in the 5,000)
    top2000   1 when the word is among the 2,000 most frequent
    herkomst  bijlage8 | spel:<categorie>[;spel:<categorie>...]

`niveau` = `open` means "in the 5,000 but taught in neither coursebook". It is a
candidate pool for B1+/B2, not a B2 label.

The appendix PDF is not in this repository. Pass its path:

    python3 tools/lexicon/extraheer-woorden.py \
        "/path/to/Bijlage-8-Frequente woorden (1).pdf"

Needs poppler (`pdftohtml`, `pdftoppm`) and Pillow. Re-run whenever either
source changes: `woorden-woordsoort.tsv` and `woorden-thema.tsv` are keyed on
the `nl` column.
"""

import collections
import json
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GAME_DATA = os.path.join(ROOT, "server/Oefenpad.Resources/Games/Data")
OUT = os.path.join(ROOT, "tools/lexicon/woorden.tsv")

DPI = 120
HEADERS = ("Nederlands woord", "Bijlage 8", "|", "Woorden die", "Engelse vertaling")

# The page footer (`37 van 148`) is set in the translation column, so a row with
# no lemma appends it to the entry above. One gloss per page carried it.
FOOTER = re.compile(r"^\s*\d+\s+van\s+\d+\s*$")

# The text layer puts a part-of-speech tag in the middle of a glossed word:
# `to an(noun)ce`, `to (adj)ust`, `a) furious b) (adv) very`.
POS_MARK = re.compile(r"\s*\((?:noun|adj|adv|verb|prep|conj|pron|num|interj|art)\.?\)")

# Where the marker swallowed letters the gloss cannot be rebuilt from the text,
# so the four affected entries are written out.
GLOSS_REPAIR = {
    "aankondigen": "to announce",
    "aanpassen": "to adjust",
    "afstemmen": "to tune, to adjust",
    "bekendmaken": "to announce",
}

# `zo’n` is set in a different font on page 147 and was once lost silently.
# These are common lemmas the appendix must yield; a rebuild that drops one
# fails here instead of shrinking the list without a word.
VERWACHT = {"zo’n", "ons", "zijn", "een", "niet"}


def kleur(px):
    """Classify one pixel of the highlight fill behind a word."""
    r, g, b = px
    if abs(r - g) < 8 and abs(g - b) < 8:
        return None  # paper, rules, text
    if b > 200 and b - r > 40:
        return "gang-top2000" if r < 160 else "gang"
    if r > 200 and b < 190:
        return "actie"
    return None


def skip(text, page, top):
    if not text:
        return True
    if text.startswith(HEADERS) or "van 148" in text:
        return True
    return page == 1 and top < 450


def lees_bijlage(pdf):
    """Return [(lemma, gloss, tier)] in page order."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["pdftohtml", "-xml", "-i", "-q", pdf, os.path.join(tmp, "b8")],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["pdftoppm", "-png", "-r", str(DPI), pdf, os.path.join(tmp, "pg")],
            check=True, capture_output=True,
        )
        xml = open(os.path.join(tmp, "b8.xml"), encoding="utf-8").read()
        pages = re.findall(r"<page[^>]*>.*?</page>", xml, re.S)
        scale = DPI / 72 / 1.5  # xml units are points x 1.5; images are points x dpi/72

        out = []
        for nr, page in enumerate(pages, 1):
            img = Image.open(os.path.join(tmp, f"pg-{nr:03d}.png")).convert("RGB")
            rows = collections.defaultdict(list)
            for m in re.finditer(
                r'<text top="(\d+)" left="(\d+)" width="(\d+)" height="(\d+)"[^>]*>(.*?)</text>',
                page, re.S,
            ):
                top, left, w, h = (int(m.group(i)) for i in range(1, 5))
                text = re.sub("<[^>]+>", "", m.group(5))
                text = text.replace("&amp;", "&").replace("&#39;", "'").strip()
                if text:
                    rows[top].append((left, w, h, text))

            for top in sorted(rows):
                cells = sorted(rows[top])
                lemma = [c for c in cells if 100 <= c[0] < 250]
                gloss = " ".join(c[3] for c in cells
                                 if c[0] >= 390 and not FOOTER.match(c[3]))
                gloss = re.sub(r"\s+", " ", gloss).strip()
                if not lemma:
                    # A wrapped gloss sits in a row of its own; a page footer does
                    # too, but the footer is split into `5` + ` van 148` cells, so
                    # only the joined text can be recognised.
                    if out and gloss and not FOOTER.match(gloss):
                        out[-1] = (out[-1][0], (out[-1][1] + " " + gloss).strip(), out[-1][2])
                    continue
                left, w, h, name = lemma[0]
                if skip(name, nr, top):
                    continue
                gloss = POS_MARK.sub("", gloss)
                gloss = re.sub(r"\s+", " ", gloss).strip()
                gloss = GLOSS_REPAIR.get(name.lower(), gloss)
                box = (int(left * scale), int(top * scale),
                       int((left + w) * scale), int((top + h) * scale))
                counts = collections.Counter(kleur(p) for p in img.crop(box).getdata())
                counts.pop(None, None)
                tier = "open"
                if counts and counts.most_common(1)[0][1] > 12:
                    tier = counts.most_common(1)[0][0]
                out.append((name, gloss, tier))
        return out


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: extraheer-woorden.py <Bijlage-8 pdf>")

    woorden = {}
    seen = set()
    for lemma, gloss, tier in lees_bijlage(sys.argv[1]):
        key = lemma.lower()
        if key in seen:
            continue
        seen.add(key)
        woorden[key] = {
            "nl": lemma,
            "en": gloss,
            "niveau": {"gang": "A1", "gang-top2000": "A1", "actie": "B1", "open": "open"}[tier],
            "top2000": "1" if tier == "gang-top2000" else "",
            "herkomst": ["bijlage8"],
        }

    # Rows such as `zijn, z’n` and `een, één` are stored under the whole string,
    # so split the variants before checking that nothing was lost.
    gehad = set()
    for naam in woorden:
        gehad.update(deel.strip() for deel in naam.split(","))
    ontbreekt = VERWACHT - gehad
    assert not ontbreekt, "appendix extraction lost: %s" % sorted(ontbreekt)

    def kandidaten(w):
        """Plural game forms onto the singular lemma the appendix already has."""
        yield w
        for suffix, keep in (("en", -2), ("s", -1), ("e", -1), ("n", -1)):
            if w.endswith(suffix) and len(w) + keep >= 3:
                yield w[:keep]

    def add(key, en, herkomst):
        for cand in kandidaten(key):
            if cand in woorden:
                woorden[cand]["herkomst"].append(herkomst)
                return
        woorden[key] = {"nl": key, "en": en, "niveau": "", "top2000": "", "herkomst": [herkomst]}

    words = json.load(open(os.path.join(GAME_DATA, "words.json"), encoding="utf-8"))
    for cat, body in words.items():
        for item in body["words"]:
            add(item["nl"].lower(), item["en"].lower(), f"spel:{cat}")

    reels = json.load(open(os.path.join(GAME_DATA, "reels.json"), encoding="utf-8"))
    for reel in reels:
        for tile in reel["tiles"]:
            add(re.sub(r"^(de|het)\s+", "", tile["nl"].lower()), tile["en"].lower(), "spel:reels")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("nl\ten\tniveau\ttop2000\therkomst\n")
        for key in sorted(woorden):
            rec = woorden[key]
            fh.write(
                f"{rec['nl']}\t{rec['en']}\t{rec['niveau']}\t{rec['top2000']}"
                f"\t{';'.join(sorted(set(rec['herkomst'])))}\n"
            )
    print(f"{len(woorden)} words -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
