#!/usr/bin/env python3
"""Assert the adjective card pages are consistent with selection.json and the scene TSVs.

Besides structure (ids, fields, partners, frame numbers) it checks the content rules
the 20 Nov 2026 review found broken, so they are caught mechanically next time:
alt text leaking the word or its partner (also inside compounds), avoid-list shape and
cross-references, numerals-bearing objects, sparkle marks, tints, example length, the
one-noun set sentence, person nouns within a pair, and duplicate glosses.

Since the B1/B2 expansion (20 Nov 2026) it also checks: the B2 page; that every
set's band agrees with an independent rank lookup in the lexicon (or carries an
override whose reason is printed on the overview); that no override repeats its
rank band; that no rank comes from a homograph split row; alt-text stems that
inflection rules cannot derive (STEMS); colour words used as avoid labels;
the exact "Pair with" opening; and cards whose lemma is carded in another family.

Fix pass 2 (20 Nov 2026) adds: every "word (rank)" or "word ranks N" cited in an
override reason must match the lexicon, and every word an override says has "no lexicon
row" must truly have none (the old "absent, so rarer than 10000" reason was false for
participles); set sentences and examples may not use a direction or state adjective as
an adverb after loopt/staat/beweegt/hang; one object keeps one Dutch name across the set
sentence and the alts of a set (tapijt/kleed, grond/gras); and more cross-references
between look-alike cards.

Fix pass 3 (20 Nov 2026) adds: cliche-food props (chips, fries, herring, cheese) to the
souvenir list, checked in scene, must and the fixed frame, plus the Dutch words
(friet, kaas, haring, molen ...) in alt text and set sentences; every fixed frame must end
with one "Only ..." sentence; and cross-references for the lettuce and fair-share sets.

Everyday pass (20 Nov 2026) adds: every everyday promotion sits at A2 or lower, below its
rank band, and is printed in the overview's everyday table; its reason must read
"Everyday promotion. Lexicon: ... Basis: judgment... Note: ..."; every cited niveau,
top2000, herkomst, rank and "no woorden.tsv row" is checked against tools/lexicon, every
member is cited exactly once, the coursebook-support list matches the lexicon, and the
note states no lexicon fact.
"""
import csv
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "tools", "_bn_tmp")
OUT = os.path.join(ROOT, "Docs", "bijvoeglijke-naamwoorden")
BANDS = ["a0", "a1", "a2", "b1", "b2"]
CUTS = [(250, "a0"), (1000, "a1"), (2500, "a2"), (5000, "b1"), (10000, "b2")]
# "not a tulip" is an instruction to the illustrator, not souvenir imagery.
BANNED = re.compile(r"(?<!not a )\b(windmill|clog|tulip|canal|cheese|herring|stroopwafel)s?\b"
                    r"|\b(chips|fries|french fries|paper cone)\b", re.I)
# The same souvenir and cliche-food props in Dutch, for alt text and set sentences (B1/B2 review L9).
BANNED_NL = re.compile(r"\b\w*(molen|klomp|tulp|gracht|kaas|haring|friet|patat|puntzak|stroopwafel)\w*\b", re.I)
COLOURS = re.compile(r"\b(red|blue|green|yellow|orange|pink|purple|brown|grey|gray)\b", re.I)
TINT = re.compile(r"\b(hatching|hatched|shading|shaded|tint|pale|white hair)\b", re.I)
SPARKLE = re.compile(r"\b(sparkles?|gleams?|glints?|glinting|shine|shiny|glitter)\b", re.I)
SPARKLE_OK = {"schoon"}
NUMERAL_OBJECTS = re.compile(r"\b(clocks?|thermometers?|coins?|books?|radios?|signs?|dials?)\b", re.I)
NUMERAL_GUARD = re.compile(r"\b(numerals|blank)\b", re.I)
BAD_LABELS = {"neutral", "not this card", "not this object", "not the stick", "not the set"}
# Sets whose drawings change the subject itself (a cake vs a lemon, a child vs an old man).
TWO_SUBJECTS = {"smaak", "leeftijd-mensen"}
PERSON_NOUNS = {"man", "vrouw", "jongen", "meisje"}
# Near misses that must name each other (review M4, M6, M7, M8, M21, H6, H10).
CROSS = [("moe", "slaperig"), ("slaperig", "moe"), ("zwak", "zwaar"), ("zwaar", "zwak"),
         ("zoet", "lekker"), ("tevreden", "vol"), ("ontevreden", "boos"),
         ("gespannen", "zenuwachtig"), ("gespannen", "bang"), ("zenuwachtig", "gespannen"),
         ("bang", "zenuwachtig"), ("kalm", "ontspannen"), ("ontspannen", "kalm"),
         ("duur", "rijk"), ("goedkoop", "arm"), ("aanwezig", "leeg"), ("afwezig", "leeg"),
         ("vroeg", "ochtend"), ("vroeg", "nacht"), ("eenzaam", "alleen"), ("schoon", "leeg"),
         ("ver", "klein"), ("lelijk", "kapot"), ("mooi", "kapot"),
         # fix pass 2, B1/B2 review M2, M9, M11, M13, L2, L4, L5, L9, L10
         ("benauwd", "warm"), ("benauwd", "pittig"), ("pittig", "benauwd"),
         ("comfortabel", "zacht"), ("ongemakkelijk", "hard"), ("geduldig", "kalm"),
         ("vast", "zacht"), ("vloeibaar", "gesmolten"), ("zorgvuldig", "netjes"),
         ("plat", "vlak"), ("vlak", "plat"), ("braaf", "gehoorzaam"), ("gehoorzaam", "braaf"),
         ("steil", "tegen de wind in"), ("knapperig", "stijf"), ("flauw", "ontevreden"),
         # fix pass 3: lettuce set and the fair-share set
         ("slap", "dood"), ("eerlijk", "groot"), ("oneerlijk", "groot"), ("eerlijk", "heel"),
         ("oneerlijk", "gierig")]
# One object, one Dutch name within a set (review L7).
SYNONYMS = [("tapijt", "kleed"), ("grond", "gras"), ("kruk", "stoel")]
# An adjective right after these verbs is an adverb ("loopt horizontaal"), not the adjective card.
ADVERB_VERBS = re.compile(r"\b(loopt|lopen|staat|staan|beweegt|bewegen|hang|hangt|hangen)\s+(\w+)", re.I)
# Tokens that contain a stem by accident (checked by hand).
INNOCENT = {"arm": {"armen"}, "bot": {"botsende"}, "dicht": {"dichtbij"}, "ver": set()}
# Stems inflection rules cannot derive: an alt containing one leaks the word (review H7 class).
STEMS = {"gekreukt": ["kreuk"], "gestreken": ["strijk", "streek"], "opgepompt": ["pomp"],
         "leeggelopen": ["leeg"], "opgerold": ["rol"], "uitgerold": ["rol"], "geschild": ["schil"],
         "ongeschild": ["schil"], "gestreept": ["streep"], "geruit": ["ruit"], "gestippeld": ["stip"],
         "bevroren": ["vries", "vroor"], "ontdooid": ["dooi"], "winderig": ["wind"], "windstil": ["wind"],
         "doorzichtig": ["zicht"], "ondoorzichtig": ["zicht"], "gekookt": ["kook"],
         "vervuild": ["vuil"], "onbeleefd": ["beleefd"], "ongeduldig": ["geduld"], "geduldig": ["geduld"],
         "feestelijk": ["feest"], "vruchtbaar": ["vrucht"], "zorgvuldig": ["zorg"], "rommelig": ["rommel"],
         "gehoorzaam": ["gehoor"], "vrijgevig": ["geef", "geven"], "beleefd": ["beleef"]}
COLOUR_LABELS = {"rood", "blauw", "groen", "geel", "oranje", "roze", "paars", "bruin", "grijs", "wit", "zwart"}
errors = []


def err(msg):
    errors.append(msg)


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def forms(lemma):
    """The lemma plus its inflected and comparative stems (groot -> grote, dik -> dikke)."""
    f = {lemma}
    v = "aeiou"
    if len(lemma) >= 3 and lemma[-2] == lemma[-3] and lemma[-2] in v and lemma[-1] not in v:
        base = lemma[:-2] + lemma[-1]                    # laag -> lag(e), groot -> grot(e)
    elif len(lemma) <= 5 and lemma[-1] not in v and lemma[-2] in v and lemma[-3:-2] not in ("", *v):
        base = lemma + lemma[-1]                         # dik -> dikk(e), nat -> natt(e)
    else:
        base = lemma
    if base.endswith("f"):
        base = base[:-1] + "v"                           # lief -> liev(e)
    f.update({base + "e", base + "er"})
    return f


def leaks(sentence, lemma):
    hits = []
    toks = re.findall(r"[a-zà-ÿ]+", sentence.lower())
    for t in toks:
        if t in INNOCENT.get(lemma, set()):
            continue
        if any(st in t for st in forms(lemma) | set(STEMS.get(lemma, []))):
            hits.append(t)
    return hits


def has_form(sentence, lemma):
    toks = re.findall(r"[a-zà-ÿ]+", sentence.lower())
    return any(t in forms(lemma) or t == lemma for t in toks)


sel = json.load(open(os.path.join(TMP, "selection.json"), encoding="utf-8"))

# Independent band check against the lexicon (exact lemma only; split rows are not frequencies).
with open(os.path.join(ROOT, "tools", "lexicon", "woorden-frequentie.tsv"), encoding="utf-8") as fh:
    RANK = {r["nl"]: int(r["rang"]) for r in csv.DictReader(fh, delimiter="\t")}


def rank_band(r):
    return next(b for cut, b in CUTS if r <= cut)


index_html = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
for b in BANDS:
    for c in sel.get(b, []):
        if c.get("band") != b:
            err(f"{c['id']}: listed under {b} but band field is {c.get('band')}")
        rs = [RANK[m["lemma"]] for m in c["members"] if m["lemma"] in RANK]
        rb = rank_band(min(rs)) if rs else None
        if c.get("rank_band") != rb:
            err(f"{c['id']}: rank band {c.get('rank_band')} in selection.json, lexicon gives {rb}")
        for m in c["members"]:
            if m.get("rank") is not None and RANK.get(m["lemma"]) != m["rank"]:
                err(f"{m['id']}: rank {m['rank']} is not the exact-lemma rank of {m['lemma']}")
        if c.get("override"):
            if c["override"] == rb:
                err(f"{c['id']}: override {c['override']} repeats the rank band")
            if c["override"] != b:
                err(f"{c['id']}: override {c['override']} but placed in {b}")
            reason = c.get("override_reason", "").strip()
            if not reason:
                err(f"{c['id']}: override without a reason")
            elif html.escape(reason, quote=False) not in index_html:
                err(f"{c['id']}: override reason not printed on the overview")
        elif rb != b:
            err(f"{c['id']}: placed in {b} but its rank band is {rb} and there is no override")
        reason = c.get("override_reason", "")
        for w, n in re.findall(r"\b([a-z]+) \((\d+)\)", reason) + re.findall(r"\b([a-z]+) ranks (\d+)", reason):
            if RANK.get(w) != int(n):
                err(f"{c['id']}: override cites {w} ({n}) but the lexicon gives {RANK.get(w)}")
        for grp in re.findall(r"((?:[a-z]+, )*[a-z]+(?: and [a-z]+)?) (?:has|have) no lexicon row", reason):
            for w in re.split(r", | and ", grp):
                if w in RANK:
                    err(f"{c['id']}: override says {w} has no lexicon row, but it ranks {RANK[w]}")
        if re.search(r"rarer than rank 10000|absent from the 10,000", reason):
            err(f"{c['id']}: override assumes a word absent from the lexicon is rarer than 10000; band it by its base lemma")

# Everyday promotions: every lexicon fact in the printed reason is checked (model:
# tools/check-zelfstandige-naamwoorden-cards.py).
LEXROW = {}
with open(os.path.join(ROOT, "tools", "lexicon", "woorden.tsv"), encoding="utf-8") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        LEXROW.setdefault(r["nl"], r)
CB_FOR = {"a0": {"A1", "les:nig"}, "a1": {"A1", "les:nig"}, "a2": {"A1", "les:nig"}}
EV_FACT = re.compile(r"^(?P<lem>.+?) (?:(?P<norow>no woorden\.tsv row)|niveau (?P<niv>\S+)(?:, top2000 (?P<top>\S+))?, "
                     r"herkomst (?P<h>\S+)), (?:rank (?P<r>\d+)|(?P<nr>no usable rank))$")
EV_NOTE_BANNED = re.compile(r"(?i)coursebook|bijlage|top.?2000|niveau|herkomst|\brank|lexicon|\d")
ev_table = re.search(r"<h2>Everyday sets promoted by judgment</h2>(.*?)</table>", index_html, re.S)
ev_rows = {m.group(1): (m.group(2), m.group(3), html.unescape(m.group(4))) for m in re.finditer(
    r"<tr><td><code>([^<]+)</code></td><td>([A-Z0-9]+)</td><td>([A-B][0-2])</td><td>(.*?)</td></tr>",
    ev_table.group(1) if ev_table else "")}
n_ev = 0
for b in BANDS:
    for c in sel.get(b, []):
        reason = c.get("override_reason", "")
        if not (c.get("everyday") or reason.startswith("Everyday promotion")):
            continue
        n_ev += 1
        cid = c["id"]
        if not c.get("everyday") or not reason.startswith("Everyday promotion"):
            err(f"{cid}: everyday flag and 'Everyday promotion' reason disagree")
        if b not in ("a0", "a1", "a2"):
            err(f"{cid}: everyday promotion placed in {b.upper()}, above A2")
        rb = c.get("rank_band")
        if rb and BANDS.index(b) >= BANDS.index(rb):
            err(f"{cid}: everyday promotion to {b.upper()} does not move it below its rank band {rb.upper()}")
        if cid not in ev_rows:
            err(f"{cid}: everyday promotion missing from the overview's everyday table")
        else:
            orb, ob, txt = ev_rows[cid]
            if txt != reason:
                err(f"{cid}: everyday reason on the overview differs from selection.json")
            if ob != b.upper() or orb != (rb or "none").upper():
                err(f"{cid}: everyday table bands {orb}/{ob} differ from selection {rb}/{b}")
        m = re.match(r"^Everyday promotion\. Lexicon: (.*?)\. Basis: (.*?)\. Note: (.*)\.$", reason)
        if not m:
            err(f"{cid}: everyday reason is not 'Everyday promotion. Lexicon: ... Basis: ... Note: ...'")
            continue
        facts, basis, note = m.groups()
        cited, support = [], []
        for f in facts.split("; "):
            fm = EV_FACT.match(f)
            if not fm:
                err(f"{cid}: unparseable lexicon fact '{f}'")
                continue
            lem = fm["lem"]
            cited.append(lem)
            row = LEXROW.get(lem)
            if fm["norow"]:
                if row:
                    err(f"{cid}: says {lem} has no woorden.tsv row, but it has one")
            elif not row:
                err(f"{cid}: cites {lem} niveau/herkomst, but it is not a woorden.tsv row")
            else:
                if fm["niv"] != (row["niveau"] or "none"):
                    err(f"{cid}: says {lem} niveau {fm['niv']}, woorden.tsv says {row['niveau'] or 'none'}")
                if (fm["top"] or "") != row["top2000"]:
                    err(f"{cid}: says {lem} top2000 {fm['top'] or 'empty'}, woorden.tsv says {row['top2000'] or 'empty'}")
                if fm["h"] != row["herkomst"]:
                    err(f"{cid}: says {lem} herkomst {fm['h']}, woorden.tsv says {row['herkomst']}")
                if ({row["niveau"]} | set(row["herkomst"].split(";"))) & CB_FOR.get(b, set()):
                    support.append(lem)
            if fm["r"] and RANK.get(lem) != int(fm["r"]):
                err(f"{cid}: says {lem} rank {fm['r']}, woorden-frequentie.tsv says {RANK.get(lem)}")
            if fm["nr"] and lem in RANK:
                err(f"{cid}: says {lem} has no usable rank, but it ranks {RANK[lem]}")
        want = [x["lemma"] for x in c["members"]]
        if sorted(cited) != sorted(want):
            err(f"{cid}: reason cites {cited}, the set's members are {want}")
        exp = "judgment, not lexicon data" if not support else f"judgment, with coursebook support ({', '.join(support)})"
        if basis != exp:
            err(f"{cid}: basis '{basis}', lexicon gives '{exp}'")
        if EV_NOTE_BANNED.search(note):
            err(f"{cid}: note states a lexicon fact outside the checked Lexicon part: '{note}'")
if n_ev != len(ev_rows):
    err(f"overview lists {len(ev_rows)} everyday promotions, selection.json has {n_ev}")
m = re.search(r"(\d+) sets moved:", index_html)
if n_ev and (not m or int(m.group(1)) != n_ev):
    err(f"overview's everyday count does not say {n_ev}")

# Band table on the overview agrees with the pages.
for b in BANDS:
    page = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    ns = len(re.findall(r'<section class="cluster"', page))
    nc = len(re.findall(r'<article id=', page))
    if not re.search(rf'<a href="{b}\.html">{b.upper()}</a></td><td class="n">{ns}</td><td class="n">{nc}</td>', index_html):
        err(f"{b}: overview band table does not say {ns} sets, {nc} adjectives")

# Cross-family duplicates: a lemma carded as a headword in another family.
# Priority from the 20 Nov 2026 brief: the earlier family keeps a contested item.
PRIORITY = ["werkwoorden", "voorzetselpaden", "bijvoeglijke-naamwoorden", "zelfstandige-naamwoorden",
            "bijwoorden", "scheidbare-werkwoorden", "vaste-uitdrukkingen"]
warnings = []
OTHER = {}
for path in glob.glob(os.path.join(ROOT, "Docs", "*", "*.html")):
    fam = os.path.basename(os.path.dirname(path))
    if fam in ("bijvoeglijke-naamwoorden", "archive", "lexicon", "design-options", "plans"):
        continue
    for h in re.findall(r'<h3 class="chunk">([^<]*)</h3>', open(path, encoding="utf-8").read()):
        OTHER.setdefault(html.unescape(h).strip().lower(), fam)
ids_expected = {m["id"]: (b, c["id"], c) for b in BANDS for c in sel.get(b, []) for m in c["members"]}
lemma_of = {m["id"]: m["lemma"] for b in BANDS for c in sel.get(b, []) for m in c["members"]}
ids_seen = {}
cards = {}
total = 0
for b in BANDS:
    page = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    for sec in re.finditer(r'<section class="cluster" data-cluster="([^"]+)".*?</section>', page, re.S):
        cl, sbody = sec.group(1), sec.group(0)
        zin = re.search(r'<p class="zin">(.*?)<span class="en">', sbody, re.S)
        zin = text(zin.group(1)) if zin else ""
        mems = [m for m in ids_expected if ids_expected[m][1] == cl]
        for m in mems:
            if not has_form(zin, lemma_of[m]):
                err(f"{cl}: set sentence lacks {lemma_of[m]}")
        two = re.match(r"(?:De|Het|Deze|Dit|Die|Dat) (\w+) (?:is|zit) \w+, maar (?:de|het|deze|dit|die|dat) (\w+) (?:is|zit)", zin)
        if two and two.group(1).lower() != two.group(2).lower() and cl not in TWO_SUBJECTS:
            err(f"{cl}: set sentence names two nouns ({two.group(1)}, {two.group(2)}) for one drawn object")
        fr = re.search(r'<p class="frame"><strong>Fixed frame.</strong>(.*?)</p>', sbody, re.S)
        fr = text(fr.group(1)) if fr else ""
        if not re.search(r"(?:^|\. )Only [^.]+\.$", fr):
            err(f"{cl}: fixed frame does not end with one 'Only ...' sentence naming the single change")
        if BANNED.search(fr):
            err(f"{cl}: souvenir imagery in the fixed frame ({BANNED.search(fr).group(0)})")
        if BANNED_NL.search(zin):
            err(f"{cl}: souvenir imagery in the set sentence ({BANNED_NL.search(zin).group(0)})")
        alts_people = []
        set_alts = []
        for vm in ADVERB_VERBS.finditer(zin):
            if vm.group(2).lower() in {lemma_of[m] for m in mems} or any(vm.group(2).lower() in forms(lemma_of[m]) for m in mems):
                err(f"{cl}: set sentence uses {vm.group(2)} as an adverb ('{vm.group(0)}')")
        for m in re.finditer(r'<article id="([^"]+)" class="kaart" data-id="([^"]+)" data-band="([^"]+)" '
                             r'data-kind="adjective" data-cluster="([^"]+)"(.*?)</article>', sbody, re.S):
            cid, did, band, cluster, body = m.groups()
            total += 1
            if cid != did:
                err(f"{cid}: id != data-id")
            if band != b:
                err(f"{cid}: band {band} on page {b}")
            if cid in ids_seen:
                err(f"{cid}: duplicate card")
            ids_seen[cid] = cluster
            if cid not in ids_expected or ids_expected[cid][1] != cluster:
                err(f"{cid}: not in selection for cluster {cluster}")
            if not re.search(rf'<p class="id">{re.escape(cid)}\.png ', body):
                err(f"{cid}: png name does not match id")
            f = {}
            for cls in ("scene", "must", "avoid", "contrast-note", "voorbeeld-nl", "alt"):
                mm = re.search(rf'<dd class="{cls}"[^>]*>(.*?)</dd>', body, re.S)
                f[cls] = text(mm.group(1).split("<br>")[0]) if mm else ""
                if not f[cls]:
                    err(f"{cid}: empty {cls}")
            gl = re.search(r'<p class="gloss">(.*?)</p>', body)
            f["gloss"] = text(gl.group(1)) if gl else ""
            cards[cid] = f
            lemma = text(re.search(r'<h3 class="chunk">(.*?)</h3>', body).group(1)).lower()
            pm = re.search(r'data-partner="([^"]*)"', body)
            partners = pm.group(1).split() if pm else []

            # scene
            sc = f["scene"]
            n = len(sc.split())
            if not 25 <= n <= 75:
                err(f"{cid}: scene is {n} words")
            for fld in ("scene", "must"):
                if BANNED.search(f[fld]):
                    err(f"{cid}: souvenir imagery in {fld} ({BANNED.search(f[fld]).group(0)})")
            if BANNED_NL.search(f["alt"]):
                err(f"{cid}: souvenir imagery in alt text ({BANNED_NL.search(f['alt']).group(0)})")
            if COLOURS.search(sc):
                err(f"{cid}: colour word in scene")
            if TINT.search(sc):
                err(f"{cid}: tint or pale/white mark carries meaning in scene ({TINT.search(sc).group(0)})")
            if SPARKLE.search(sc) and cid not in SPARKLE_OK:
                err(f"{cid}: sparkle/gleam mark outside schoon ({SPARKLE.search(sc).group(0)})")
            if re.search(r"\barrows?\b", sc, re.I):
                err(f"{cid}: arrow in scene")
            if NUMERAL_OBJECTS.search(sc) and not NUMERAL_GUARD.search(sc):
                err(f"{cid}: scene draws a {NUMERAL_OBJECTS.search(sc).group(0)} without forbidding numerals or writing")
            if re.search(r"from the frame", sc, re.I):
                err(f"{cid}: scene says 'from the frame' instead of naming the objects")

            # alt text: never the word, a form of it, or a partner (also inside compounds)
            for lem, who in [(lemma, "the adjective")] + [(lemma_of.get(p, p), f"partner {p}") for p in partners]:
                h = leaks(f["alt"], lem)
                if h:
                    err(f"{cid}: alt text contains {who} ({', '.join(h)})")
            set_alts.append(f["alt"].lower())
            alts_people.append(frozenset(PERSON_NOUNS & set(re.findall(r"\w+", f["alt"].lower()))))
            if lemma in OTHER:
                fam = OTHER[lemma]
                if PRIORITY.index(fam) < PRIORITY.index("bijvoeglijke-naamwoorden"):
                    err(f"{cid}: '{lemma}' is already a card in {fam}, which has priority")
                else:
                    warnings.append(f"{cid}: '{lemma}' is also a card in {fam}; this family has priority, so {fam} should drop it")

            # avoid list
            av = f["avoid"]
            items = [i.strip() for i in av.rstrip(".").split(";")]
            if not av.endswith("."):
                err(f"{cid}: avoid list lacks the closing full stop")
            if not 3 <= len(items) <= 5:
                err(f"{cid}: avoid list has {len(items)} items")
            labels = []
            for it in items:
                lm = re.search(r"\(([^()]*)\)$", it)
                if not lm:
                    err(f"{cid}: avoid item without a bracketed label: {it[:40]}")
                    continue
                labels.append(lm.group(1).split(",")[0].strip())
                if lm.group(1).split(",")[0].strip().lower() in COLOUR_LABELS:
                    err(f"{cid}: avoid label '{lm.group(1)}' is a colour")
                if lm.group(1).strip().lower() in BAD_LABELS:
                    err(f"{cid}: avoid label '{lm.group(1)}' is not an adjective or 'not the card'")
            if labels and partners and labels[0] not in partners + [lemma_of.get(p) for p in partners]:
                err(f"{cid}: first avoid item is not the partner ({labels[0]})")
            for a, bb in CROSS:
                if cid == a and bb not in labels:
                    err(f"{cid}: avoid list must name ({bb})")

            # contrast
            if not f["contrast-note"].startswith("Pair with "):
                err(f"{cid}: contrast note does not open with 'Pair with'")
            if not partners:
                err(f"{cid}: no contrast partner on page (partner skipped?)")
            for p in partners:
                if not re.search(rf"Pair with [^.]*\b{re.escape(p)}\b(?!-)", body):
                    err(f"{cid}: contrast note does not name {p}")

            # example
            ex = f["voorbeeld-nl"]
            nw = len(ex.split())
            if not 5 <= nw <= 9:
                err(f"{cid}: example is {nw} words")
            if ex == zin:
                err(f"{cid}: example repeats the set sentence")
            if not has_form(ex, lemma):
                err(f"{cid}: example does not use {lemma}")
            for vm in ADVERB_VERBS.finditer(ex):
                if vm.group(2).lower() in forms(lemma):
                    err(f"{cid}: example uses {lemma} as an adverb ('{vm.group(0)}')")
            if re.search(r"\bnbsp\b", body) or "\t" in body:
                err(f"{cid}: stray markup")
        for a, bb in SYNONYMS:
            words = [set(re.findall(r"\w+", s)) for s in [zin.lower()] + set_alts]
            if any(a in w for w in words) and any(bb in w for w in words):
                err(f"{cl}: one object has two names in the set sentence and alts ({a} / {bb})")
        if len({p for p in alts_people if p}) > 1:
            err(f"{cl}: alt texts switch person noun within the set "
                f"({' / '.join(','.join(sorted(p)) or '-' for p in alts_people)})")

seen_gloss = {}
for cid, f in cards.items():
    g = f["gloss"].lower()
    if g in seen_gloss:
        err(f"{cid}: gloss '{g}' duplicates {seen_gloss[g]}; glosses must separate senses")
    seen_gloss[g] = cid

index = index_html
skipped = set(re.findall(r"<li><code>([^<]+)</code> \(", index))
for i in ids_expected:
    if i not in ids_seen and i not in skipped:
        err(f"{i}: in selection, neither drawn nor skipped")

nums = [int(x) for b in BANDS for x in re.findall(r'class="framenummer" title="Frame (\d+)"',
        open(os.path.join(OUT, b + ".html"), encoding="utf-8").read())]
if nums != list(range(1, len(nums) + 1)):
    err("frame numbers are not 1..N in order")

print(f"cards {total}  skipped {len(skipped)}  errors {len(errors)}  warnings {len(warnings)}")
for w in warnings:
    print("  WARNING " + w)
for e in errors:
    print("  " + e)
sys.exit(1 if errors else 0)
