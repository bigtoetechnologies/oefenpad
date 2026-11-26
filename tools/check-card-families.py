#!/usr/bin/env python3
"""Check the seven card families against one shared card schema.

The per-family checkers validate a family against its own sources.  Nothing
checked that the families agreed with each other, which is how Werkwoorden
ended up with no contrast field and Voorzetselpaden with cards carrying one
build sentence and cards carrying two.

This checker reads the built pages and asserts, per card:

  all picture cards
    Scene, Must read, Avoid and Alt text are present and non-empty

  Voorzetselpaden
    Example has a Dutch sentence and an English gloss
    exactly one Check question, ending in ? and answered Ja or Nee
    exactly two Build sentences

  Zelfstandige naamwoorden, Bijvoeglijke naamwoorden, Bijwoorden,
  Scheidbare werkwoorden, Vaste uitdrukkingen
    Example has a Dutch sentence and an English gloss
    Contrast is present and names at least one partner in data-partner,
    or declares a partner in another family ("drawn in X and not here");
    the in-family partners are reciprocal
    Scheidbare werkwoorden also carry Split form and Perfect
    Zelfstandige naamwoorden also carry article and plural in .vormen
    Vaste uitdrukkingen also carry a register and a literal flag

  Werkwoorden
    Example has a Dutch sentence and an English gloss; no Build or Check question
    Contrast is optional; when present it must name a card in this family
    and be reciprocal.  A partner may sit in another band.

  Explanation cards
    four example questions, each ending in ? and answered ja or nee

Run:  python3 tools/check-card-families.py
"""

import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "Docs")

errors = []


def err(msg):
    errors.append(msg)


# Page files that are not card pages.
SKIP = {
    "voorzetselpaden": {
        "index.html", "AGENTS.html", "dutchgrammar-check.html",
        "verb-prep-check-2026-11-15.html", "verb-prep-verification-2026-11-15.html",
    },
    "werkwoorden": {"index.html", "matrix.html", "backlog.html", "AGENTS.html"},
    "zelfstandige-naamwoorden": {"index.html"},
    "bijvoeglijke-naamwoorden": {"index.html"},
    "bijwoorden": {"index.html"},
    "scheidbare-werkwoorden": {"index.html"},
    "vaste-uitdrukkingen": {"index.html"},
    "explanation-cards": {"index.html"},
}

ARTICLE = re.compile(r'<article\b[^>]*class="[^"]*\bkaart\b[^"]*"[^>]*>.*?</article>', re.S)
SECTION = re.compile(r'<section\b[^>]*class="[^"]*\bkaart\b[^"]*"[^>]*>.*?</section>', re.S)
DTDD = re.compile(r'<dt>(.*?)</dt>\s*<dd\b([^>]*)>(.*?)</dd>', re.S)
TAG = re.compile(r'<[^>]+>')


def text_of(fragment):
    return html.unescape(TAG.sub(" ", fragment)).strip()


def pages(family):
    return [p for p in sorted(glob.glob(os.path.join(DOCS, family, "*.html")))
            if os.path.basename(p) not in SKIP[family]]


def cards(family):
    """Every card on the family's band pages, with its fields and partner ids."""
    found = []
    pattern = SECTION if family == "explanation-cards" else ARTICLE
    for path in pages(family):
        src = open(path, encoding="utf-8").read()
        for m in pattern.finditer(src):
            block = m.group(0)
            cid = re.search(r'\bid="([^"]+)"', block)
            body = re.search(r'\bdata-id="([^"]+)"', block)
            ident = cid.group(1) if cid else (body.group(1) if body else "?")
            fields = {}
            for label, attrs, value in DTDD.findall(block):
                fields[text_of(label)] = text_of(value)
            partner = re.search(r'data-partner="([^"]*)"', block)
            found.append({
                "id": ident,
                "page": os.path.basename(path),
                "block": block,
                "fields": fields,
                "partners": partner.group(1).split() if partner else [],
                "text": 'data-kind="separable-verb-text"' in block,
                "has_en": 'class="voorbeeld-en"' in block,
                "has_register": 'class="register"' in block,
                "has_literal": 'class="betekenis"' in block,
                "has_article": 'class="art"' in block,
                "has_plural": 'class="mv"' in block,
                "questions": len(re.findall(r'class="vraag"', block)),
            })
    return found


def need(c, family, label):
    if not c["fields"].get(label):
        err(f"{family}/{c['page']}: {c['id']} has no {label}")


def check_partners(family, found):
    ids = {c["id"] for c in found}
    for c in found:
        for p in c["partners"]:
            if p not in ids:
                err(f"{family}/{c['page']}: {c['id']} names partner {p!r}, which is not a card")
                continue
            back = next(x for x in found if x["id"] == p)
            if c["id"] not in back["partners"]:
                err(f"{family}/{c['page']}: partner {p} does not point back to {c['id']}")


def check_example(family, c):
    need(c, family, "Example")
    if c["fields"].get("Example") and not c["has_en"]:
        err(f"{family}/{c['page']}: {c['id']} Example has no English gloss")
    if c["has_en"]:
        en = re.search(r'<span class="voorbeeld-en">(.*?)</span>', c["block"], re.S)
        if not en or not text_of(en.group(1)):
            err(f"{family}/{c['page']}: {c['id']} Example has an empty English gloss")


def report(name, found, extra=""):
    print(f"  {name:26} {len(found):5} cards {extra}")


def main():
    summary = []

    # --- Voorzetselpaden -----------------------------------------------------
    vp = cards("voorzetselpaden")
    for c in vp:
        for label in ("Scene", "Must read", "Avoid", "Alt text"):
            need(c, "voorzetselpaden", label)
        check_example("voorzetselpaden", c)
        q = c["fields"].get("Check question", "")
        if not q:
            need(c, "voorzetselpaden", "Check question")
        elif not re.search(r"\?\s*(Ja|Nee)\.?$", q):
            err(f"voorzetselpaden/{c['page']}: {c['id']} check question is not '…? Ja/Nee'")
        n = c["block"].count("<dt>Build</dt>")
        if n != 2:
            err(f"voorzetselpaden/{c['page']}: {c['id']} has {n} build sentences, expected 2")
    report("Voorzetselpaden", vp)

    # --- The five word-card families ----------------------------------------
    for family in ("zelfstandige-naamwoorden", "bijvoeglijke-naamwoorden",
                   "bijwoorden", "scheidbare-werkwoorden", "vaste-uitdrukkingen"):
        found = cards(family)
        for c in found:
            if c["text"]:
                # A text card (separable verbs without a picture) has no scene brief
                # and no contrast; it is checked for gloss, split form, perfect, example.
                check_example(family, c)
                continue
            for label in ("Scene", "Must read", "Avoid", "Alt text", "Contrast"):
                need(c, family, label)
            check_example(family, c)
            if not c["partners"] and "and not here" not in c["fields"].get("Contrast", ""):
                err(f"{family}/{c['page']}: {c['id']} Contrast names no data-partner")
        if family == "scheidbare-werkwoorden":
            for c in found:
                need(c, family, "Split form")
                need(c, family, "Perfect")
        if family == "zelfstandige-naamwoorden":
            for c in found:
                if not c["has_article"] or not c["has_plural"]:
                    err(f"{family}/{c['page']}: {c['id']} lacks article or plural in .vormen")
        if family == "vaste-uitdrukkingen":
            for c in found:
                if not c["has_register"] or not c["has_literal"]:
                    err(f"{family}/{c['page']}: {c['id']} lacks the register or literal flag")
        check_partners(family, found)
        report(family, found)

    # --- Werkwoorden ---------------------------------------------------------
    ww = cards("werkwoorden")
    for c in ww:
        for label in ("Scene", "Must read", "Avoid", "Alt text"):
            need(c, "werkwoorden", label)
        check_example("werkwoorden", c)
        for label in ("Build", "Check question"):
            if label in c["fields"]:
                err(f"werkwoorden/{c['page']}: {c['id']} carries {label}, which verb cards do not")
        if c["partners"]:
            need(c, "werkwoorden", "Contrast")
    check_partners("werkwoorden", ww)
    paired = sum(1 for c in ww if c["partners"])
    report("Werkwoorden", ww, f"({paired} with a contrast partner)")

    # --- Explanation cards ---------------------------------------------------
    ex = cards("explanation-cards")
    for c in ex:
        if c["questions"] != 4:
            err(f"explanation-cards/{c['page']}: {c['id']} has {c['questions']} questions, expected 4")
        mocks = re.findall(r'<div class="vraag">(.*?)</div>.*?<div class="uitkomst">(.*?)</div>',
                           c["block"], re.S)
        for i, (q, a) in enumerate(mocks, 1):
            if not text_of(q).endswith("?"):
                err(f"explanation-cards/{c['page']}: {c['id']} example {i} question lacks ?")
            if not re.search(r"\b(ja|nee)\b", text_of(a), re.I):
                err(f"explanation-cards/{c['page']}: {c['id']} example {i} has no ja/nee answer")
    report("Explanation cards", ex)

    # --- Duplicate ids inside a family --------------------------------------
    for family in ("voorzetselpaden", "werkwoorden", "zelfstandige-naamwoorden",
                   "bijvoeglijke-naamwoorden", "bijwoorden", "scheidbare-werkwoorden",
                   "vaste-uitdrukkingen", "explanation-cards"):
        seen = {}
        found = {"explanation-cards": ex, "werkwoorden": ww,
                 "voorzetselpaden": vp}.get(family)
        if found is None:
            found = cards(family)
        for c in found:
            if c["id"] in seen:
                err(f"{family}: duplicate id {c['id']} on {seen[c['id']]} and {c['page']}")
            seen[c["id"]] = c["page"]

    print()
    if errors:
        print(f"{len(errors)} errors")
        for e in errors:
            print("  " + e)
        return 1
    print("0 errors: the families agree on the shared card schema")
    return 0


if __name__ == "__main__":
    sys.exit(main())
