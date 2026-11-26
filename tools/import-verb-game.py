#!/usr/bin/env python3
"""Build the Verb game bank from the generated Werkwoorden pages.

Inputs
  Docs/werkwoorden/*.html        the band pages built by build-verb-cards.py

Output
  server/Oefenpad.Resources/Games/Data/verbs.json

  tools/_ww_tmp/examples.tsv     slug<TAB>example, one Dutch sentence per card

Only cards that carry a drawing (an <img class="beeld">) are used. The game
teaches what the verb means: one picture, the infinitive, the gloss, one example
sentence and, for an irregular verb, the forms a learner must recognise. There
is no grammar drill. A second sense of a verb is its own card with its own slug
and its own example.

Run:  python tools/import-verb-game.py [--check]
"""

import argparse
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "Docs", "werkwoorden")
ART = os.path.join(ROOT, "assets", "verbs")
EXAMPLES = os.path.join(ROOT, "tools", "_ww_tmp", "examples.tsv")
OUT = os.path.join(ROOT, "server", "Oefenpad.Resources", "Games", "Data", "verbs.json")

BANDS = ("a0", "a1", "a2", "b1", "b2")
SKIP = {"index.html", "matrix.html", "backlog.html", "AGENTS.html"}
ARTICLE = re.compile(r"<article\b([^>]*)>(.*?)</article>", re.S)
TAG = re.compile(r"<[^>]+>")


def text(value):
    return " ".join(html.unescape(TAG.sub("", value)).split())


def attr(attrs, name):
    match = re.search(rf'\b{name}="([^"]*)"', attrs)
    return html.unescape(match.group(1)) if match else ""


def dd(body, cls):
    match = re.search(rf'<dd class="{cls}">(.*?)</dd>', body, re.S)
    return match.group(0) if match else ""


def read_examples():
    """slug -> example sentence, from tools/_ww_tmp/examples.tsv."""
    out = {}
    if not os.path.exists(EXAMPLES):
        return out
    with open(EXAMPLES, encoding="utf-8") as fh:
        next(fh, None)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[1].strip():
                out[parts[0].strip()] = parts[1].strip()
    return out


def read_cards():
    cards = []
    for band in BANDS:
        path = os.path.join(DOCS, f"{band}-irregular.html")
        if not os.path.exists(path):
            continue
        for name in sorted(os.listdir(DOCS)):
            if not name.startswith(band + "-") or name in SKIP:
                continue
            if not name.endswith(".html"):
                continue
            page = os.path.join(DOCS, name)
            src = open(page, encoding="utf-8").read()
            for match in ARTICLE.finditer(src):
                attrs, body = match.group(1), match.group(2)
                if 'class="beeld"' not in body:
                    continue
                slug = attr(attrs, "data-id")
                verb = text(re.search(r'<h3 class="chunk">(.*?)</h3>', body, re.S).group(1))
                gloss = text(re.search(r'<p class="gloss">(.*?)</p>', body, re.S).group(1))
                alt = attr(re.search(r'<img class="beeld"([^>]*)>', body).group(1), "alt")
                past = re.search(r'<span class="imp"[^>]*>(.*?)</span>', body, re.S)
                perfect = re.search(r'<span class="perf"[^>]*>(.*?)</span>', body, re.S)
                partner = re.search(r'data-partner="([^"]*)"', dd(body, "contrast-note"))
                cards.append({
                    "id": slug,
                    "verb": verb,
                    "gloss": gloss,
                    "band": attr(attrs, "data-band"),
                    "alt": alt,
                    "past": text(past.group(1)) if past else None,
                    "perfect": text(perfect.group(1)) if perfect else None,
                    "regular": not bool(past or perfect),
                    "partner": html.unescape(partner.group(1)) if partner else None,
                })
    return cards


def levels_for(cards):
    """Band order, then page order, four verbs per level.

    A trailing level of one would have nothing to choose between, so it is
    folded into the level before it. A level therefore holds four or five.
    Two cards of the same verb are never in one level: a second sense is its own
    card, and the pair would be each other's distractor.
    """
    levels = []
    for band in BANDS:
        rows = [c for c in cards if c["band"] == band]
        if not rows:
            continue
        chunks = []
        for card in rows:
            if (not chunks or len(chunks[-1]) == 4
                    or any(c["verb"] == card["verb"] for c in chunks[-1])):
                chunks.append([])
            chunks[-1].append(card)
        if (len(chunks) > 1 and len(chunks[-1]) < 2
                and not {c["verb"] for c in chunks[-1]} & {c["verb"] for c in chunks[-2]}):
            chunks[-2].extend(chunks.pop())
        for number, chunk in enumerate(chunks, 1):
            levels.append({
                "id": f"{band}-{number}",
                "name": f"{band.upper()} · {number}",
                "band": band,
                "frames": [c["id"] for c in chunk],
            })
    return levels


def build():
    cards = read_cards()
    if not cards:
        sys.exit("no drawn verb cards found")

    drawn = {c["id"] for c in cards}
    examples = read_examples()
    missing = [c["id"] for c in cards if c["id"] not in examples]
    if missing:
        print(f"{len(missing)} drawn cards have no example: {', '.join(missing[:12])}"
              + (" ..." if len(missing) > 12 else ""))
    scenes = {}
    frames = []
    for card in cards:
        image = os.path.join(ART, card["id"] + ".png")
        if not os.path.exists(image):
            sys.exit(f"missing art for {card['id']}")
        scenes[card["id"]] = {
            "file": f"verbs/{card['id']}.png",
            "alt": card["alt"],
        }
        frames.append({
            "id": card["id"],
            "verb": card["verb"],
            "gloss": card["gloss"],
            "scene": card["id"],
            "band": card["band"],
            "contrast": card["partner"] if card["partner"] in drawn else None,
            "past": card["past"],
            "perfect": card["perfect"],
            "regular": card["regular"],
            "example": examples.get(card["id"]),
        })

    return {"scenes": scenes, "frames": frames, "levels": levels_for(cards)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report, write nothing")
    args = parser.parse_args()

    content = build()
    frames = len(content["frames"])
    levels = content["levels"]
    print(f"{frames} drawn verbs, {len(levels)} levels")
    for level in levels:
        print(f"  {level['band']}  {level['name']:<8} {len(level['frames'])} verbs")
    if any(len(level["frames"]) < 2 for level in levels):
        sys.exit("a level has fewer than two verbs; the choose step needs a distractor")

    if args.check:
        return
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(content, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
