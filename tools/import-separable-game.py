#!/usr/bin/env python3
"""Build the Separable-verbs game bank from the family's card pages.

Inputs
  Docs/scheidbare-werkwoorden/{a1,a2,b1,b2}.html         contrast-set cards
  Docs/scheidbare-werkwoorden/tekst-{a1,a2,b1,b2}.html   text cards

Output
  server/Oefenpad.Resources/Games/Data/separable.json

Every card is a frame: the infinitive, its English gloss, the split form, the
perfect and one example sentence with its translation. A card whose page shows a
drawing (<img class="beeld">) also gets a scene; most have none, which is why the
game is text-first. Levels run in band order and page order, four cards each; a
contrast set therefore stays together, and a trailing level of one is folded into
the level before it.

Run:  python tools/import-separable-game.py [--check]
"""

import argparse
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "Docs", "scheidbare-werkwoorden")
ART = os.path.join(ROOT, "assets", "verbs")
OUT = os.path.join(ROOT, "server", "Oefenpad.Resources", "Games", "Data", "separable.json")

BANDS = ("a1", "a2", "b1", "b2")
ARTICLE = re.compile(r"<article\b([^>]*)>(.*?)</article>", re.S)
TAG = re.compile(r"<[^>]+>")


def text(value):
    return " ".join(html.unescape(TAG.sub("", value)).split())


def attr(attrs, name):
    match = re.search(rf'\b{name}="([^"]*)"', attrs)
    return html.unescape(match.group(1)) if match else ""


def dd(body, cls):
    match = re.search(rf'<dd class="{cls}">(.*?)</dd>', body, re.S)
    return match.group(1) if match else ""


def read_page(path, band):
    cards = []
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    for match in ARTICLE.finditer(src):
        attrs, body = match.group(1), match.group(2)
        if "kaart" not in attr(attrs, "class"):
            continue
        slug = attr(attrs, "data-id")
        verb = text(re.search(r'<h3 class="chunk">(.*?)</h3>', body, re.S).group(1))
        gloss = text(re.search(r'<p class="gloss">(.*?)</p>', body, re.S).group(1))
        example = dd(body, "voorbeeld-nl")
        example_nl = text(example.split("<br>")[0]) if example else ""
        example_en = text(re.search(r'<span class="voorbeeld-en">(.*?)</span>', example, re.S).group(1)) if example else ""
        img = re.search(r'<img class="beeld"([^>]*)>', body)
        cards.append({
            "id": slug,
            "verb": verb,
            "gloss": gloss,
            "band": band,
            "split": text(dd(body, "split")),
            "perfect": text(dd(body, "perfect")),
            "example": example_nl,
            "exampleEn": example_en,
            "alt": attr(img.group(1), "alt") if img else None,
            "drawn": bool(img),
        })
    return cards


def read_cards():
    cards = []
    for band in BANDS:
        for name in (f"{band}.html", f"tekst-{band}.html"):
            path = os.path.join(DOCS, name)
            if os.path.exists(path):
                cards.extend(read_page(path, band))
    return cards


def levels_for(cards):
    levels = []
    for band in BANDS:
        rows = [c for c in cards if c["band"] == band]
        if not rows:
            continue
        chunks = [rows[i:i + 4] for i in range(0, len(rows), 4)]
        if len(chunks) > 1 and len(chunks[-1]) < 2:
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
        sys.exit("no separable cards found")
    seen = set()
    for c in cards:
        if c["id"] in seen:
            sys.exit(f"duplicate card id {c['id']}")
        seen.add(c["id"])
        for field in ("verb", "gloss", "split", "perfect", "example", "exampleEn"):
            if not c[field]:
                sys.exit(f"{c['id']}: empty {field}")

    scenes = {}
    frames = []
    for c in cards:
        scene = None
        if c["drawn"] and os.path.exists(os.path.join(ART, c["id"] + ".png")):
            scenes[c["id"]] = {"file": f"verbs/{c['id']}.png", "alt": c["alt"] or ""}
            scene = c["id"]
        frames.append({
            "id": c["id"],
            "verb": c["verb"],
            "gloss": c["gloss"],
            "band": c["band"],
            "split": c["split"],
            "perfect": c["perfect"],
            "example": c["example"],
            "exampleEn": c["exampleEn"],
            "scene": scene,
        })
    return {"scenes": scenes, "frames": frames, "levels": levels_for(cards)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report, write nothing")
    args = parser.parse_args()

    content = build()
    print(f"{len(content['frames'])} separable verbs, {len(content['levels'])} levels, "
          f"{len(content['scenes'])} with a picture")
    per_band = {}
    for level in content["levels"]:
        per_band[level["band"]] = per_band.get(level["band"], 0) + len(level["frames"])
    for band, n in per_band.items():
        print(f"  {band}  {n} verbs")
    if args.check:
        return
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(content, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
