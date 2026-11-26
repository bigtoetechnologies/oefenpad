#!/usr/bin/env python3
"""Turn the word-card families into word categories for the word games.

Inputs  Docs/<family>/*.html     one <article class="kaart"> per card (the HTML is the master)
Output  server/Oefenpad.Resources/Games/Data/words.cards.json

Same shape as words.json: { key: { label: {en, nl}, icon, words: [{en, nl}] } }.
Hangman, word search, memory and matching read it next to words.json, so every card
becomes a Dutch word with its English meaning. A card gives its infinitive or
expression (h3.chunk) and its English gloss (p.gloss).

Normalising the Dutch word for the games (they play on A-Z only):
  - upper case, diacritics removed (ë -> E), parentheses and a leading "zich " dropped
  - a card with a hyphen, an apostrophe, a digit or "..." in its Dutch word is skipped
  - a duplicate Dutch word inside one category keeps the first card

Categories: one per family and band, e.g. "Bijwoorden A0". A band with fewer than
MIN words is merged into the next band of that family so memory and matching have
enough pairs. Nouns and adjectives are grouped by theme instead (home, food, body ...):
tools/card-themes.json maps each contrast cluster (the card's data-cluster) to a theme.

Run:  python3 tools/import-card-words.py [--check] [--families a,b,c]
"""

import argparse
import glob
import html
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "Docs")
OUT = os.path.join(ROOT, "server", "Oefenpad.Resources", "Games", "Data", "words.cards.json")

MIN = 12
BAND_ORDER = ["a0", "a1", "a2", "b1", "b2"]

# family -> (key prefix, Dutch label, English label, icon)
FAMILIES = {
    "bijwoorden": ("adverbs", "Bijwoorden", "Adverbs", "🧭"),
    "vaste-uitdrukkingen": ("expressions", "Vaste uitdrukkingen", "Fixed expressions", "💬"),
    "scheidbare-werkwoorden": ("separable", "Scheidbare werkwoorden", "Separable verbs", "🧩"),
    "zelfstandige-naamwoorden": ("nouns", "Zelfstandige naamwoorden", "Nouns", "📦"),
    "bijvoeglijke-naamwoorden": ("adjectives", "Bijvoeglijke naamwoorden", "Adjectives", "🎨"),
}
THEMED = {"zelfstandige-naamwoorden": "nouns", "bijvoeglijke-naamwoorden": "adjectives"}
THEMES = os.path.join(ROOT, "tools", "card-themes.json")
ARTICLES = ("de ", "het ", "een ")

ARTICLE = re.compile(r"<article\b([^>]*)>(.*?)</article>", re.S)
TAG = re.compile(r"<[^>]+>")


def text(value):
    return " ".join(html.unescape(TAG.sub("", value)).split())


def attr(attrs, name):
    match = re.search(rf'\b{name}="([^"]*)"', attrs)
    return html.unescape(match.group(1)) if match else ""


def game_word(dutch, strip_article=False):
    """The Dutch word as the games play it, or None when it cannot be played."""
    word = re.sub(r"\([^)]*\)", "", dutch).strip()
    word = re.sub(r"^zich\s+", "", word)
    if strip_article:
        for art in ARTICLES:
            if word.lower().startswith(art):
                word = word[len(art):]
                break
    if any(ch in word for ch in "-'’0123456789") or "..." in word or "…" in word:
        return None
    plain = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode()
    plain = " ".join(plain.upper().split())
    if not plain or not re.fullmatch(r"[A-Z]+( [A-Z]+)*", plain):
        return None
    return plain


def clean_gloss(gloss):
    gloss = re.sub(r"\s+", " ", gloss).strip()
    return gloss


def read_family(family):
    cards = []
    for path in sorted(glob.glob(os.path.join(DOCS, family, "*.html"))):
        if os.path.basename(path) in ("index.html", "matrix.html", "backlog.html", "AGENTS.html"):
            continue
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        for match in ARTICLE.finditer(src):
            attrs, body = match.group(1), match.group(2)
            if "kaart" not in attr(attrs, "class"):
                continue
            chunk = re.search(r'<h3 class="chunk"[^>]*>(.*?)</h3>', body, re.S)
            gloss = re.search(r'<p class="gloss">(.*?)</p>', body, re.S)
            if not chunk or not gloss:
                continue
            band = attr(attrs, "data-band").lower()
            if band not in BAND_ORDER:
                continue
            cards.append({
                "id": attr(attrs, "data-id"),
                "cluster": attr(attrs, "data-cluster"),
                "band": band,
                "nl": text(chunk.group(1)),
                "en": clean_gloss(text(gloss.group(1))),
            })
    return cards


def themed_categories(family, cards, themes, strip_article):
    key, _label_nl, _label_en, _icon = FAMILIES[family]
    by_theme = {}
    skipped = []
    seen = set()
    for card in cards:
        word = game_word(card["nl"], strip_article)
        if word is None or not card["en"]:
            skipped.append(card["nl"])
            continue
        theme = themes["map"].get(card["cluster"])
        if theme is None:
            skipped.append(card["nl"] + " (no theme)")
            continue
        if (theme, word) in seen:
            continue
        seen.add((theme, word))
        by_theme.setdefault(theme, []).append({"en": card["en"], "nl": word, "_band": card["band"]})
    cats = {}
    for t in themes["themes"]:
        words = sorted(by_theme.get(t["key"], []), key=lambda w: (BAND_ORDER.index(w["_band"]), w["nl"]))
        if not words:
            continue
        cats[f"{key}-{t['key']}"] = {
            "label": {"en": t["en"], "nl": t["nl"]},
            "icon": t["icon"],
            "words": [{"en": w["en"], "nl": w["nl"]} for w in words],
        }
    return cats, skipped


def categories_for(family, cards):
    key, label_nl, label_en, icon = FAMILIES[family]
    if family in THEMED:
        with open(THEMES, encoding="utf-8") as fh:
            themes = json.load(fh)[THEMED[family]]
        return themed_categories(family, cards, themes, strip_article=(family == "zelfstandige-naamwoorden"))
    by_band = {}
    skipped = []
    seen = {}
    for card in cards:
        word = game_word(card["nl"])
        if word is None or not card["en"]:
            skipped.append(card["nl"])
            continue
        if (family, word) in seen:
            continue
        seen[(family, word)] = True
        by_band.setdefault(card["band"], []).append({"en": card["en"], "nl": word})

    bands = [b for b in BAND_ORDER if b in by_band]
    groups = []
    pending = []
    for band in bands:
        pending.append(band)
        if sum(len(by_band[b]) for b in pending) >= MIN:
            groups.append(pending)
            pending = []
    if pending:
        if groups:
            groups[-1].extend(pending)
        else:
            groups.append(pending)

    cats = {}
    for group in groups:
        name = group[0].upper() if len(group) == 1 else f"{group[0].upper()}-{group[-1].upper()}"
        cat_key = f"{key}-{'-'.join(group) if len(group) > 1 else group[0]}"
        words = [w for b in group for w in by_band[b]]
        cats[cat_key] = {
            "label": {"en": f"{label_en} {name}", "nl": f"{label_nl} {name}"},
            "icon": icon,
            "words": words,
        }
    return cats, skipped


def build(families):
    out = {}
    report = []
    for family in families:
        cards = read_family(family)
        cats, skipped = categories_for(family, cards)
        out.update(cats)
        report.append((family, len(cards), sum(len(c["words"]) for c in cats.values()), len(cats), skipped))
    return out, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report, write nothing")
    parser.add_argument("--families", default="bijwoorden,vaste-uitdrukkingen,scheidbare-werkwoorden")
    args = parser.parse_args()
    families = [f for f in args.families.split(",") if f]
    for f in families:
        if f not in FAMILIES:
            sys.exit(f"unknown family {f}")

    content, report = build(families)
    for family, cards, words, cats, skipped in report:
        print(f"{family:24} {cards:4} cards -> {words:4} words in {cats} categories, {len(skipped)} skipped")
        if skipped:
            print("   skipped:", ", ".join(skipped[:12]) + (" ..." if len(skipped) > 12 else ""))
    for key, cat in content.items():
        print(f"  {key:26} {len(cat['words']):4}  {cat['label']['nl']}")
    if args.check:
        return
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(content, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
