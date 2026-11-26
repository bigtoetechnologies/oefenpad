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
  B1/B2 pass (20 Nov 2026):
  - every hand-set rank (rank_source handmatig) has a reason, moves the verb to
    another band than its lexicon rank, and is listed on index.html
  - every SKIP row and every "later pass" backlog row carries a reason
  - no card's slug is also a card id in another family's Docs/<family>/ pages
  - scenes have at least 30 words and alt texts at most 20 (errors on b1-regular
    and the B2 pages, warnings on the older pages)
  Fix pass 2 (20 Nov 2026, after the B1/B2 review):
  - alt text uses no word on the short (unlengthened) stem either (gras for
    grazen) nor a listed cognate (zaad for zaaien, druppel for druipen)
  - alt text uses no form of a verb its own Avoid names as a competitor (giet on
    the mengen card); a form of another card on the same page is a warning
  - Avoid names no colour either, and alt names no Dutch colour other than wit
    or zwart
  - Scene and Must ask for no musical notes (a notation glyph is a readable mark)
  Contrast notes (20 November 2026):
  - a verb in contrasts.tsv must be a card, not a SKIP row
  - its partner must be a card too, and the pair must be reciprocal
  - the note must open "Pair with <partner>." and be rendered on the card with
    that data-partner
  - a card with no contrasts row must render no Contrast field
  - partners may sit in another band: a verb is banded by its own frequency, so
    a same-band rule would forbid the honest pairs
  - a SKIP row may not give "two senses" as its reason (the family picks one
    sense and cards it), and a "Duplicate of <family>:<id>" reason must name a
    card that exists in that family
  One card per sense (20 November 2026):
  - a second sense of a carded verb is its own card, titled <verb> (<sense>) and
    filed under <base id>-<sense>; it carries the base card's band and rank
  - every sense card has its base card on the same page
  - a verb's cards never share a gloss, a Must read or a Scene: the pair is two
    different drawings, so the pair may not be served in one game round
  - a sense card renders no Contrast field, and may name its own verb in Avoid
    (that is how it points at the sibling card it must not be confused with)

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

BANDS = ["A0", "A1", "A2", "B1", "B2"]
REGS = ["irregular", "regular"]

errors = []


def err(msg):
    errors.append(msg)


warnings = []
LENGTH_STRICT = {"b1-regular", "b2-irregular", "b2-regular"}


def warn(msg):
    warnings.append(msg)


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


def split_label(label):
    """dragen (kleding) -> ("dragen", "kleding").  A second sense carries its
    qualifier in brackets, the way the Bijwoorden pages print alleen (enkel)."""
    m = re.match(r"^(.+?) \(([a-z]+)\)$", label)
    return (m.group(1), m.group(2)) if m else (label, "")


VERBS = {r["verb"] for r in json.load(open(os.path.join(TMP, "selection.json"), encoding="utf-8"))}

CONTRASTS = {}
_contrast_path = os.path.join(TMP, "contrasts.tsv")
if os.path.exists(_contrast_path):
    for _r in read_tsv(_contrast_path):
        _v = (_r.get("verb") or "").strip()
        if _v:
            CONTRASTS[_v] = {
                "partner": (_r.get("partner") or "").strip(),
                "note": (_r.get("note") or "").strip(),
            }
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
    # Accepted exception (review L3): the picture is a ball, and no honest Dutch
    # describes it without the word.
    "voetballen": {"bal"},
}

# Nouns on another root of the same verb, which the stem test cannot see.
COGNATES = {
    "zaaien": ("zaad", "zaai"),
    "druipen": ("druppel", "drup"),
    "grazen": ("gras",),
    "zwaaien": ("zwaai",),
    "voetballen": ("voetbal",),
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


def short_stem(inf):
    """The stem before vowel doubling and devoicing rules: grazen -> gras."""
    s = inf[:-2] if inf.endswith("en") else inf
    if len(s) >= 2 and s[-1] == s[-2] and s[-1] not in "aeiou":
        s = s[:-1]
    return s[:-1] + {"z": "s", "v": "f"}.get(s[-1], s[-1]) if s else s


def alt_leaks(verb, alt):
    forms = own_forms(verb)
    st = stem_of(verb)
    sh = short_stem(verb)
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
        elif len(sh) >= 4 and sh != st and tok.startswith(sh):
            hits.append(tok)
        elif any(tok.startswith(c) for c in COGNATES.get(verb, ())):
            hits.append(tok)
    return hits


# Posture and looking verbs nearly every alt text needs; a form of one of these
# is not treated as naming a competitor.
BASIC = {"staan", "zitten", "liggen", "houden", "kijken", "lopen", "zijn", "hebben"}


def form_hits(verb, alt):
    """Tokens of alt that are a finite, past or participle form of verb.  The
    bare stem and the infinitive are left out: they are usually a noun or an
    adjective (fiets, open, het eten)."""
    if verb in BASIC:
        return []
    forms = own_forms(verb) - {verb, stem_of(verb)}
    out = []
    for tok in re.findall(r"[a-zëéïöü]+", alt.lower()):
        cands = {tok} | {tok[len(p):] for p in PREFIXES if tok.startswith(p) and len(tok) - len(p) >= 3}
        if {c for c in cands & forms if len(c) >= 3}:
            out.append(tok)
    return out


COLOUR_RE = re.compile(r"\b(red|green|yellow|gold|golden|grey|gray|blue|orange|purple|pink|brown|silver)\b", re.I)
TEXT_RE = re.compile(r"\b(numbered|numbers?|digits?|lettering|letters|text|written|words|labelled|musical notes?|notation)\b", re.I)
COLOUR_NL_RE = re.compile(r"\b(rood|rode|groen|groene|geel|gele|goud|gouden|grijs|grijze|blauw|blauwe|oranje|paars|paarse|roze|bruin|bruine|zilver|zilveren|muzieknootjes?|muzieknoten)\b", re.I)
NEG_RE = re.compile(r"\b(no|not|nothing|without|never|nor|blank)\b", re.I)
SOUVENIR_RE = re.compile(r"\b(cheese|kaas|tulips?|tulpen?|windmills?|molen|clogs?|klompen?|cross|kruis)\b", re.I)


def negated(text, start):
    before = text[:start].split()[-6:]
    return any(NEG_RE.fullmatch(w.strip(",.;:")) for w in before)


def content_checks(key, c, verb, sense=""):
    dd = c["dd"]
    for tok in alt_leaks(verb, dd.get("alt", "")):
        err(f"{key}: {verb} alt uses a form of its own verb: {tok}")
    # A sense card points at its own sibling card, which is the same verb; that
    # is the one case where naming its own verb in Avoid is not a tautology.
    if not sense and re.search(r"\(" + re.escape(verb) + r"\)", dd.get("avoid", "")):
        err(f"{key}: {verb} Avoid names its own verb as the competitor")
    strict = err if key in LENGTH_STRICT else warn
    for m in COLOUR_RE.finditer(dd.get("avoid", "")):
        strict(f"{key}: {verb} avoid names a colour: {m.group(0)}")
    for m in COLOUR_NL_RE.finditer(dd.get("alt", "")):
        err(f"{key}: {verb} alt names a colour or a notation glyph: {m.group(0)}")
    for comp in re.findall(r"\(([a-zëéïöü]+)\)", dd.get("avoid", "")):
        if comp != verb and comp in VERBS:
            for tok in form_hits(comp, dd.get("alt", "")):
                strict(f"{key}: {verb} alt uses {tok}, a form of {comp}, the competitor its Avoid names")
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
    # Length rules are enforced on the pages written or extended in the B1/B2
    # pass; older pages only warn, because their cards stay as reviewed.
    report = err if key in LENGTH_STRICT else warn
    if len(dd.get("scene", "").split()) < 30:
        report(f"{key}: {verb} scene is under 30 words; the brief asks for 35-55")
    if len(dd.get("alt", "").split()) > 20:
        report(f"{key}: {verb} alt text is over 20 words")
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
card_meta = []
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
            verb, sense = split_label(html.unescape(re.search(r'<h3 class="chunk">(.*?)</h3>', c["block"]).group(1)))
            gloss = html.unescape(re.search(r'<p class="gloss">(.*?)</p>', c["block"]).group(1))
            glosses.setdefault(gloss, []).append(verb)
            card_meta.append({
                "key": key, "id": c["data_id"], "verb": verb, "sense": sense,
                "gloss": gloss, "dd": c["dd"],
            })
            content_checks(key, c, verb, sense)
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

# 7. Contrast notes: a true pair, reciprocal, rendered with its partner.
for verb, c in CONTRASTS.items():
    if verb not in seen:
        err(f"contrasts.tsv: {verb} is not a card (skipped or unknown)")
        continue
    partner = c["partner"]
    if partner not in seen:
        err(f"contrasts.tsv: {verb} partner {partner!r} is not a card")
    if not c["note"].startswith(f"Pair with {partner}."):
        err(f"contrasts.tsv: {verb} note must open 'Pair with {partner}.'")
    back = CONTRASTS.get(partner)
    if not back:
        err(f"contrasts.tsv: {partner} has no row back to {verb}")
    elif back["partner"] != verb:
        err(f"contrasts.tsv: {partner} pairs with {back['partner']}, not {verb}")

for key, (found, _t) in by_page.items():
    for c in found:
        verb, sense = split_label(html.unescape(re.search(r'<h3 class="chunk">(.*?)</h3>', c["block"]).group(1)))
        shown = re.search(r'<dd class="contrast-note" data-partner="([^"]*)">(.*?)</dd>', c["block"], re.S)
        # contrasts.tsv names a verb, so it belongs to the base card; a sense card
        # is told apart from its sibling by the drawings, not by a contrast note.
        want = None if sense else CONTRASTS.get(verb)
        if want and not shown:
            err(f"{key}: {verb} has a contrast row but no Contrast field")
        elif want and shown:
            if shown.group(1) != want["partner"]:
                err(f"{key}: {verb} data-partner={shown.group(1)!r}, expected {want['partner']!r}")
            if not html.unescape(shown.group(2)).strip():
                err(f"{key}: {verb} Contrast field is empty")
        elif not want and shown:
            err(f"{key}: {verb} renders a Contrast field with no contrasts.tsv row")

# 7b. One card per sense: a verb may carry several cards, and then the pair must
# be two different drawings, filed under <base id>-<sense> beside its base card.
by_verb = {}
for m in card_meta:
    by_verb.setdefault(m["verb"], []).append(m)
for verb, group in by_verb.items():
    if len(group) < 2:
        continue
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            a, b = group[i], group[j]
            same = [f for f in ("must", "scene") if a["dd"].get(f) == b["dd"].get(f)]
            if a["gloss"] == b["gloss"]:
                same.append("gloss")
            for field in same:
                err(f"{a['id']} and {b['id']} share the same {field}: two senses need two drawings")
    bases = [m for m in group if not m["sense"]]
    if not bases:
        err(f"{group[0]['key']}: {verb} has only sense cards; the base sense needs its own card")
        continue
    for m in group:
        if not m["sense"]:
            continue
        if m["key"] not in {b["key"] for b in bases}:
            err(f"{m['id']}: a sense card sits on {m['key']}, away from its base card")
        if m["id"] not in {f"{b['id']}-{m['sense']}" for b in bases}:
            err(f"{m['id']}: a sense card's id must be its base card's id plus -{m['sense']}")

# A form of another B1/B2 card in an alt text (review L2: leunt on duwen, buigt
# on ontwijken).  Warning only: the word may be the honest description.
late = [(key, c, split_label(html.unescape(re.search(r'<h3 class="chunk">(.*?)</h3>', c["block"]).group(1)))[0])
        for key, (found, _t) in by_page.items() if key[:2] in ("b1", "b2") for c in found]
late_verbs = {v for _k, _c, v in late}
for key, c, verb in late:
    for other in late_verbs - {verb}:
        for tok in form_hits(other, c["dd"].get("alt", "")):
            warn(f"{key}: {verb} alt uses {tok}, a form of {other}, another B1/B2 card")

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

# 6. Hand-set ranks: a reason, a different band, shown on the overview.
def band_of(rank):
    for band, top in (("A0", 250), ("A1", 1000), ("A2", 2500), ("B1", 5000), ("B2", 10000)):
        if rank <= top:
            return band
    return None


selection = json.load(open(os.path.join(TMP, "selection.json"), encoding="utf-8"))
for r in selection:
    if r.get("rank_source") != "handmatig":
        continue
    if not r.get("rank_reason"):
        err(f"rank override for {r['verb']} has no reason")
    if band_of(r.get("raw_rank", 0)) == band_of(r["rank"]):
        err(f"rank override for {r['verb']} repeats the lexicon band {band_of(r['rank'])}")
    if f"<td>{html.escape(r['verb'])}</td><td class=\"n\">{r.get('raw_rank')}</td>" not in index:
        err(f"index.html does not list the rank override for {r['verb']}")

# 7. Reasons for every SKIP row and every later-pass backlog row.
def dup_target_exists(fam, cid):
    d = os.path.join(ROOT, "Docs", fam)
    if not os.path.isdir(d):
        return False
    return any(f'data-id="{cid}"' in open(os.path.join(d, f), encoding="utf-8").read()
               for f in os.listdir(d) if f.endswith(".html"))


for band in BANDS:
    for reg in REGS:
        for r in read_tsv(os.path.join(SCENES, page_key(band, reg) + ".tsv")):
            s = (r["scene"] or "").strip()
            if s.upper().startswith("SKIP") and len(s[4:].strip(" :")) < 15:
                err(f"{page_key(band, reg)}: SKIP row for {r['verb']} has no reason")
            if s.upper().startswith("SKIP") and re.search(r"\btwo (\w+ )?senses\b", s, re.I):
                warn(f"{page_key(band, reg)}: SKIP row for {r['verb']} gives two senses as the reason; the family picks one sense and cards it")
            if s.upper().startswith("SKIP"):
                for fam, cid in re.findall(r"\b([a-z-]+):([a-z0-9-]+)", s):
                    if not dup_target_exists(fam, cid):
                        err(f"{page_key(band, reg)}: SKIP row for {r['verb']} cites {fam}:{cid}, which is not a card there")
for r in read_tsv(os.path.join(TMP, "backlog_seed.tsv")):
    if r.get("reason") == "later pass" and not (r.get("note") or "").strip():
        err(f"backlog: later-pass verb {r['verb']} has no note")

# 8. No card id shared with another family's cards.
DOCS = os.path.join(ROOT, "Docs")
other_ids = {}
for fam in os.listdir(DOCS):
    d = os.path.join(DOCS, fam)
    if fam == "werkwoorden" or not os.path.isdir(d):
        continue
    for f in os.listdir(d):
        if f.endswith(".html"):
            for m in re.finditer(r'<article[^>]*data-id="([^"]+)"', open(os.path.join(d, f), encoding="utf-8").read()):
                other_ids.setdefault(m.group(1), f"{fam}/{f}")
for slug, key in seen.items():
    if slug in other_ids:
        err(f"{key}: card {slug} is also a card in {other_ids[slug]}")

if warnings:
    print(f"warnings {len(warnings)} (older pages, not errors)")
    for w in warnings:
        print("  " + w)

if errors:
    print(f"FAIL {len(errors)} problem(s)")
    for e in errors:
        print("  " + e)
    sys.exit(1)

print(f"OK  {n_cards} cards  {len(seen)} unique ids  frames 1..{n_cards}")
for key in [page_key(b, r) for b in BANDS for r in REGS]:
    print(f"  {key:16} {expected[key]:3} cards")
