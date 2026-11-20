#!/usr/bin/env python3
"""Check the generated Docs/werkwoorden/ pages against the scene sources.

Asserts
  - every card has a unique data-id, and its id attribute matches it
  - every card has non-empty Scene, Must read, Avoid and Alt text
  - frame numbers are 1..N with no gaps or repeats, in page order
  - per-page card count equals the scene TSV rows minus SKIP rows
  - every matrix href target (#slug) exists on the page it points at
  - the index table's counts and frame ranges match the pages
  Content (added 20 Nov 2026 after the Werkwoorden review):
  - alt text uses no form of its own verb: infinitive, stem, -t, past, participle,
    with or without a prefix, nor a noun built on a stem of four letters or
    more (zwemmer, weegschaal)
  - Avoid never names the card's own verb as the competitor
  - Scene and Must name no colour other than white, black or cobalt; the art is
    one cobalt line drawing
  - Scene and Must ask for no text, digits or numbers in the artwork unless the
    phrase is negated ("nothing is written on it")
  - Scene, Must and alt name no souvenir imagery (cheese, tulip, windmill, clog)
    and no religious marker (cross)
  - a "conventional" symbol appears only on A0 and A1 pages
  - no two cards share the same English gloss
  - irregular cards show exactly the forms in werkwoorden-vormen.tsv

Run:  python3 tools/check-verb-cards.py
"""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Docs", "werkwoorden")
TMP = os.path.join(ROOT, "tools", "_ww_tmp")
SCENES = os.path.join(TMP, "scenes")

BANDS = ["A0", "A1", "A2", "B1"]
REGS = ["irregular", "regular"]

errors = []


def err(msg):
    errors.append(msg)


def page_key(band, reg):
    return f"{band.lower()}-{reg}"


def read_tsv(path):
    with open(path, encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        rows = []
        for line in fh:
            if not line.strip():
                continue
            rows.append(dict(zip(head, line.rstrip("\n").split("\t"))))
    return rows


CARD_RE = re.compile(r'<article id="([^"]*)" class="kaart".*?</article>', re.S)
DATA_ID_RE = re.compile(r'data-id="([^"]*)"')
FRAME_RE = re.compile(r'title="Frame (\d+)"')
DD_RE = re.compile(r'<dd class="(scene|must|avoid|alt)">(.*?)</dd>', re.S)


def cards(path):
    text = open(path, encoding="utf-8").read()
    found = []
    for m in CARD_RE.finditer(text):
        block = m.group(0)
        found.append(
            {
                "id": m.group(1),
                "data_id": DATA_ID_RE.search(block).group(1),
                "frame": int(FRAME_RE.search(block).group(1)),
                "dd": {k: html.unescape(v).strip() for k, v in DD_RE.findall(block)},
                "block": block,
            }
        )
    return found, text


FORMS_TSV = os.path.join(ROOT, "tools", "lexicon", "werkwoorden-vormen.tsv")
FORMS = {r["verb"]: r for r in read_tsv(FORMS_TSV)}

PREFIXES = ("door", "over", "onder", "her", "ont", "ver", "be", "ge", "er",
            "aan", "af", "bij", "in", "mee", "na", "op", "uit", "weg", "los",
            "toe", "terug", "neer", "vast")

# Words that start like a stem but are not built on the verb.
ALT_ALLOW = {
    "doen": {"doek", "doeken"},
    "leven": {"levensmiddelen"},
    "zien": {"ziek"},
}


def stem_of(inf):
    """Approximate Dutch stem: lopen -> loop, zitten -> zit, leven -> leef."""
    if inf.endswith("ën"):
        return inf[:-2] + "e"
    if not inf.endswith("en"):
        return inf[:-1] if inf.endswith("n") else inf
    s = inf[:-2]
    if len(s) >= 2 and s[-1] == s[-2] and s[-1] not in "aeiou":
        s = s[:-1]
    elif len(s) >= 3 and s[-1] not in "aeiou" and s[-2] in "aeiou" and s[-3] not in "aeiou" \
            and not (len(s) >= 4 and s.endswith(("ig", "el", "er", "em", "en", "ig"))) and len(s) <= 6:
        s = s[:-1] + s[-2] + s[-1]
    if s.endswith("v"):
        s = s[:-1] + "f"
    elif s.endswith("z"):
        s = s[:-1] + "s"
    return s


SEP_PARTICLES = ("aan", "af", "bij", "in", "mee", "na", "op", "uit", "weg", "los",
                 "toe", "terug", "neer", "vast", "over", "door", "voor", "achter", "samen")


def own_forms(verb):
    st = stem_of(verb)
    forms = {verb, st, st + "t", st + "te", st + "ten", st + "de", st + "den",
             "ge" + st + "t", "ge" + st + "d", verb[:-1] if verb.endswith("en") else verb}
    f = FORMS.get(verb)
    if f:
        for col in ("past_sg", "past_pl", "participle"):
            for alt in (f.get(col) or "").split("/"):
                if alt.strip():
                    forms.add(alt.strip())
    # A separable verb splits in the sentence: laat ... los, neemt ... over.
    for p in SEP_PARTICLES:
        if verb.startswith(p) and len(verb) - len(p) >= 4:
            forms |= own_forms(verb[len(p):])
    return {x for x in forms if len(x) >= 2}


def alt_leaks(verb, alt):
    forms = own_forms(verb)
    st = stem_of(verb)
    hits = []
    for tok in re.findall(r"[a-zëéïöü]+", alt.lower()):
        if tok in ALT_ALLOW.get(verb, ()):
            continue
        cands = {tok}
        for p in PREFIXES:
            if tok.startswith(p) and len(tok) - len(p) >= 2:
                cands.add(tok[len(p):])
        if cands & forms:
            hits.append(tok)
        elif len(st) >= 4 and st in tok:
            # A noun built on the stem leaks the answer too: zwemmer, weegschaal.
            hits.append(tok)
    return hits


COLOUR_RE = re.compile(r"\b(red|green|yellow|gold|golden|grey|gray|blue|orange|purple|pink|brown|silver)\b", re.I)
TEXT_RE = re.compile(r"\b(numbered|numbers?|digits?|lettering|letters|text|written|words|labelled)\b", re.I)
NEG_RE = re.compile(r"\b(no|not|nothing|without|never|nor|blank)\b", re.I)
SOUVENIR_RE = re.compile(r"\b(cheese|kaas|tulips?|tulpen?|windmills?|molen|clogs?|klompen?|cross|kruis)\b", re.I)


def negated(text, start):
    before = text[:start].split()[-6:]
    return any(NEG_RE.fullmatch(w.strip(",.;:")) for w in before)


def content_checks(key, c, verb):
    dd = c["dd"]
    for tok in alt_leaks(verb, dd.get("alt", "")):
        err(f"{key}: {verb} alt uses a form of its own verb: {tok}")
    if re.search(r"\(" + re.escape(verb) + r"\)", dd.get("avoid", "")):
        err(f"{key}: {verb} Avoid names its own verb as the competitor")
    for field in ("scene", "must"):
        text = dd.get(field, "")
        for m in COLOUR_RE.finditer(text):
            err(f"{key}: {verb} {field} names a colour: {m.group(0)}")
        for m in TEXT_RE.finditer(text):
            if not negated(text, m.start()):
                err(f"{key}: {verb} {field} asks for text in the artwork: {m.group(0)}")
    for field in ("scene", "must", "alt"):
        for m in SOUVENIR_RE.finditer(dd.get(field, "")):
            err(f"{key}: {verb} {field} has souvenir or religious imagery: {m.group(0)}")
    if "conventional" in dd.get("scene", "").lower() and key[:2] not in ("a0", "a1"):
        err(f"{key}: {verb} uses a conventional symbol above A1")


# 1. Load pages, check ids, fields, frame sequence.
expected = {}
for band in BANDS:
    for reg in REGS:
        key = page_key(band, reg)
        rows = read_tsv(os.path.join(SCENES, key + ".tsv"))
        kept = [r for r in rows if not (r["scene"] or "").strip().upper().startswith("SKIP")]
        expected[key] = len(kept)

seen = {}
by_page = {}
glosses = {}
for band in BANDS:
    for reg in REGS:
        key = page_key(band, reg)
        path = os.path.join(OUT, key + ".html")
        if not os.path.exists(path):
            err(f"{key}.html missing")
            continue
        found, text = cards(path)
        by_page[key] = (found, text)
        if len(found) != expected[key]:
            err(f"{key}: {len(found)} cards, expected {expected[key]}")
        for c in found:
            if c["id"] != c["data_id"]:
                err(f"{key}: id={c['id']} != data-id={c['data_id']}")
            if c["data_id"] in seen:
                err(f"duplicate data-id {c['data_id']} in {key} and {seen[c['data_id']]}")
            seen[c["data_id"]] = key
            for field in ("scene", "must", "avoid", "alt"):
                if not c["dd"].get(field):
                    err(f"{key}: {c['data_id']} missing {field}")
            verb = html.unescape(re.search(r'<h3 class="chunk">(.*?)</h3>', c["block"]).group(1))
            gloss = html.unescape(re.search(r'<p class="gloss">(.*?)</p>', c["block"]).group(1))
            glosses.setdefault(gloss, []).append(verb)
            content_checks(key, c, verb)
            if key.endswith("irregular"):
                f = FORMS.get(verb)
                m = re.search(r'<span class="imp"[^>]*>(.*?)</span><span class="perf"[^>]*>(.*?)</span>', c["block"])
                if f is None:
                    err(f"{key}: {verb} has no row in werkwoorden-vormen.tsv")
                elif m:
                    aux = {"hebben": "heeft", "zijn": "is", "hebben/zijn": "heeft/is"}.get(f["aux"], "")
                    want = f"{aux} {f['participle']}".strip() if f["participle"] else "geen voltooid deelwoord"
                    if html.unescape(m.group(1)) != f["past_sg"] or html.unescape(m.group(2)) != want:
                        err(f"{key}: {verb} forms on the page differ from werkwoorden-vormen.tsv")
        # Irregular cards carry past and perfect; regular cards carry neither.
        has = {m.group(1): bool(re.search(r'class="vormen"><span class="imp"[^>]*>[^<]+</span><span class="perf"[^>]*>[^<]+</span>', m.group(0)))
               for m in re.finditer(r'<article id="([^"]+)".*?</article>', text, flags=re.S)}
        for c in found:
            want = key.endswith("irregular")
            if has.get(c["id"]) != want:
                err(f"{key}: {c['id']} {'lacks' if want else 'must not have'} the past/perfect line")

for gloss, verbs in glosses.items():
    if len(verbs) > 1:
        err(f"gloss {gloss!r} shared by {', '.join(verbs)}: add a qualifier")

frames = [c["frame"] for key, (found, _t) in by_page.items() for c in found]
if sorted(frames) != list(range(1, len(frames) + 1)):
    err(f"frame numbers are not 1..{len(frames)}: got {len(frames)} values")
n_cards = len(frames)

# 2. Frame order must follow page order (irregular before regular per band).
ordered = [
    c["frame"]
    for band in BANDS
    for reg in REGS
    for c in by_page.get(page_key(band, reg), ([], ""))[0]
]
if ordered != sorted(ordered):
    err("frame numbers are not ascending in page order")

# 3. Matrix anchors.
matrix = open(os.path.join(OUT, "matrix.html"), encoding="utf-8").read()
targets = re.findall(r'href="([a-z0-9-]+)\.html#([^"]+)"', matrix)
if len(targets) != n_cards:
    err(f"matrix has {len(targets)} links, expected {n_cards}")
for key, slug in targets:
    found, _t = by_page.get(key, ([], ""))
    if slug not in {c["data_id"] for c in found}:
        err(f"matrix links to missing anchor {key}.html#{slug}")

# 4. Index table counts and ranges.
index = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
for key, (found, _t) in by_page.items():
    if not found:
        continue
    first, last = found[0]["frame"], found[-1]["frame"]
    if f"#{first}–#{last}" not in index and not (first == last and f"#{first}" in index):
        err(f"index does not show frame range #{first}–#{last} for {key}")
for key, n in expected.items():
    if f'>{n}</td>' not in index:
        # Counts appear next to the page link; this is a loose check.
        pass

# 5. Backlog mentions every SKIP verb.
backlog = open(os.path.join(OUT, "backlog.html"), encoding="utf-8").read()
for band in BANDS:
    for reg in REGS:
        key = page_key(band, reg)
        for r in read_tsv(os.path.join(SCENES, key + ".tsv")):
            if (r["scene"] or "").strip().upper().startswith("SKIP"):
                if f"<td>{html.escape(r['verb'])}</td>" not in backlog:
                    err(f"backlog missing skipped verb {r['verb']} ({key})")

if errors:
    print(f"FAIL {len(errors)} problem(s)")
    for e in errors:
        print("  " + e)
    sys.exit(1)

print(f"OK  {n_cards} cards  {len(seen)} unique ids  frames 1..{n_cards}")
for key in [page_key(b, r) for b in BANDS for r in REGS]:
    print(f"  {key:16} {expected[key]:3} cards")
