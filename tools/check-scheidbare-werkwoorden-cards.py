#!/usr/bin/env python3
"""Assert the separable-verb card pages are consistent with selection.json and the scene TSVs.

Content checks added after the 2026-11-20 review: one panel per card; no digits, blank clock
faces, no canal water, no 'seen from behind' viewpoint flip; no card id that another family
already uses; alt text free of every form of the verb and of its partner (participle with and
without particle, stem- and particle-prefixed words, listed derived nouns), of its own particle
closing a clause, and of another card's split form.

Beyond the adjective checks: the split form, the example, and the perfect.  The perfect is
rebuilt from the particle and the base verb (ge- between particle and stem; auxiliary and
irregular participle from tools/lexicon/werkwoorden-vormen.tsv) and compared with the card."""
import csv
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "tools", "_sw_tmp")
OUT = os.path.join(ROOT, "Docs", "scheidbare-werkwoorden")
BANDS = ["a0", "a1", "a2", "b1", "b2"]
BANNED = re.compile(r"\b(windmill|clog|tulip|canal|cheese)s?\b", re.I)
# particles that are adverbs or adjectives: banned anywhere in the card's own or partner's alt
ADVERB_PARTICLES = {"los", "vast", "weg", "mee", "thuis", "neer", "open", "dicht", "schoon", "stil", "rond", "terug",
                    "vrij", "kwijt", "klaar", "leeg", "vol"}
# nouns built on a stem that a prefix test cannot see (checked by hand)
DERIVED = {"opschrijven": {"schrift"}, "landen": {"landing", "landingsbaan"}, "afsluiten": {"gesloten"}}
COLOURS = re.compile(r"\b(red|blue|green|yellow|orange|pink|purple|brown|grey|gray)\b", re.I)
errors = []


def err(msg):
    errors.append(msg)


def tokens(t):
    return re.findall(r"[a-zëéï']+", t.lower())


VORMEN = {r["verb"]: r for r in csv.DictReader(open(os.path.join(ROOT, "tools", "lexicon", "werkwoorden-vormen.tsv"), encoding="utf-8"), delimiter="\t")}
# roots absent from the shared table, kept in this family's own file (never overrides a shared row)
for r in csv.DictReader(open(os.path.join(TMP, "vormen-extra.tsv"), encoding="utf-8"), delimiter="\t"):
    VORMEN.setdefault(r["verb"], r)
sel = json.load(open(os.path.join(TMP, "selection.json"), encoding="utf-8"))
expected = {}
for b in BANDS:
    for c in sel.get(b, []):
        for m in c["members"]:
            expected[m["id"]] = (b, c, m)

# the authored rows, for fields the pages also carry (split, perfect)
rows = {}
for fn in os.listdir(os.path.join(TMP, "scenes")):
    if fn.endswith(".cards.tsv"):
        for r in csv.DictReader(open(os.path.join(TMP, "scenes", fn), encoding="utf-8", newline=""), delimiter="\t", quoting=csv.QUOTE_NONE):
            rows[r["id"]] = r

PREFIX_INSEP = ("be", "ge", "ver", "ont", "er", "her")


def expected_perfect(lemma, particle):
    root = lemma[len(particle):] if lemma.startswith(particle) else None
    if root is None:
        return None
    if root in VORMEN:
        v = VORMEN[root]
        aux = v["aux"].split("/")
        return aux, particle + v["participle"]
    # regular: ge- + stem + t/d, unless the root has an inseparable prefix
    return None


def forms(lemma, split, perfect):
    """Every token shape that names this verb: lemma, root, finite, participle with and without
    the particle, stem prefix, particle prefix (long particles) and listed derived nouns."""
    fin, particle = split.split(" ... ")
    fin, particle = fin.lower(), particle.lower()
    part = perfect.split()[-1].lower()
    root = lemma[len(particle):] if lemma.startswith(particle) else lemma
    stem = re.sub(r"(en|n)$", "", root)
    exact = {lemma, root, fin, fin + "t", part, part[len(particle):]} | DERIVED.get(lemma, set())
    prefixes = set()
    if len(stem) >= 4:
        prefixes.add(stem)
    if len(fin) >= 4:
        prefixes.add(fin)
    if len(particle) >= 4:
        prefixes.add(particle)
    if particle in ADVERB_PARTICLES:
        exact.add(particle)
    return exact, prefixes, particle


def leaks(alt, lemma, split, perfect):
    exact, prefixes, _p = forms(lemma, split, perfect)
    return sorted({t for t in tokens(alt) if t in exact or any(t.startswith(x) for x in prefixes)})


# alt words that contain a stem by accident, checked by hand
STEM_OK = {"afwassen": {"volwassene"}, "afruimen": {"kruimels"}}
# strong participles in -en for roots missing from werkwoorden-vormen.tsv (checked by hand)
STRONG_EN = {"ingeladen", "uitgeladen", "opgevouwen", "uitgevouwen"}
# movement verbs formed on a regular root that take zijn
ZIJN_REG = {"instappen", "uitstappen", "opstappen", "afstappen", "afkoelen", "kwijtraken"}
# compounds whose auxiliary differs from the base verb
AUX_EXCEPTION = {"opstaan": "zijn"}


def check_perfect(cid, lemma, particle, perfect):
    m = re.fullmatch(r"(heeft|is) (\S+)", perfect.strip())
    if not m:
        err(f"{cid}: perfect '{perfect}' is not 'heeft/is + participle'")
        return
    aux, part = m.groups()
    exp = expected_perfect(lemma, particle)
    if exp:
        auxes, p = exp
        if part != p:
            err(f"{cid}: participle {part} != {p} from {lemma}")
        if lemma in AUX_EXCEPTION:
            if {"heeft": "hebben", "is": "zijn"}[aux] != AUX_EXCEPTION[lemma]:
                err(f"{cid}: {lemma} takes {AUX_EXCEPTION[lemma]}")
        elif {"heeft": "hebben", "is": "zijn"}[aux] not in auxes:
            err(f"{cid}: auxiliary {aux} vs lexicon {auxes} (check by hand if the compound differs)")
    else:
        if not part.startswith(particle + "ge"):
            err(f"{cid}: participle {part} should be {particle}+ge+...")
        if not re.search(r"(t|d)$", part) and part not in STRONG_EN:
            err(f"{cid}: regular participle {part} should end in -t or -d")
        if aux != ("is" if lemma in ZIJN_REG else "heeft"):
            err(f"{cid}: auxiliary {aux} unexpected for regular compound {lemma}")


# frames per set, for checks that read scene and frame together
cl_frames = {}
for fn in os.listdir(os.path.join(TMP, "scenes")):
    if fn.endswith(".clusters.tsv"):
        for r in csv.DictReader(open(os.path.join(TMP, "scenes", fn), encoding="utf-8", newline=""), delimiter="\t", quoting=csv.QUOTE_NONE):
            cl_frames[r["cluster"]] = r["frame"]

# card ids already used by the other families (Werkwoorden owns vertrekken, landen)
OTHER_IDS = {}
for dirpath, _dirs, files in os.walk(os.path.join(ROOT, "Docs")):
    if "archive" in dirpath or dirpath.rstrip("/").endswith("scheidbare-werkwoorden"):
        continue
    for fn in files:
        if fn.endswith(".html"):
            for i in re.findall(r'<article id="([^"]+)"', open(os.path.join(dirpath, fn), encoding="utf-8").read()):
                OTHER_IDS.setdefault(i, os.path.relpath(os.path.join(dirpath, fn), ROOT))

SKIPPED = {i for i, r in rows.items() if r["scene"].strip().upper().startswith("SKIP")}
# Werkwoorden source rows, drawn or SKIP (ondergaan 'to undergo' sits there as a SKIP, not as an <article>)
WW_SLUGS = {}
for fn in sorted(os.listdir(os.path.join(ROOT, "tools", "_ww_tmp"))):
    if re.fullmatch(r"(a0|a1|a2|b1|b2)-(regular|irregular)\.tsv", fn):
        for r in csv.DictReader(open(os.path.join(ROOT, "tools", "_ww_tmp", fn), encoding="utf-8"), delimiter="\t"):
            WW_SLUGS.setdefault(r["slug"], fn)
# finite forms of the other drawn cards; light verbs every alt needs are allowed
# (judged by hand: these verbs carry most alt sentences and do not name one card)
LIGHT = {"zet", "doe", "maak", "pak", "haal", "legt", "leg", "houd", "laat", "loopt", "kijk", "geef", "gaat", "komt", "staat",
         "sta", "trek", "draai", "breng", "druk", "blijf", "steek", "sluit", "stap", "hang", "val", "loop", "kom"}
FINITES = {}
for oid, orow in rows.items():
    if oid in SKIPPED or " ... " not in orow["split"]:
        continue
    f_ = orow["split"].split(" ... ")[0].lower()
    if f_ in LIGHT or f_.rstrip("t") in LIGHT or re.sub(r"dt$", "d", f_) in LIGHT:
        continue
    for t in (f_, f_ + "t", re.sub(r"(.)\1$", r"\1", f_) + "t"):
        if len(t) >= 3:
            FINITES.setdefault(t, oid)

ids_seen = {}
total = 0
for b in BANDS:
    text = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    for m in re.finditer(r'<article id="([^"]+)" class="kaart" data-id="([^"]+)" data-band="([^"]+)" '
                         r'data-kind="separable-verb" data-cluster="([^"]+)"(.*?)</article>', text, re.S):
        cid, did, band, cluster, body = m.groups()
        total += 1
        if cid != did:
            err(f"{cid}: id != data-id")
        if band != b:
            err(f"{cid}: band {band} on page {b}")
        if cid in ids_seen:
            err(f"{cid}: duplicate card")
        ids_seen[cid] = cluster
        if cid not in expected or expected[cid][1]["id"] != cluster:
            err(f"{cid}: not in selection for set {cluster}")
        for cls in ("scene", "must", "avoid", "contrast-note", "split", "voorbeeld-nl", "perfect", "alt"):
            mm = re.search(rf'<dd class="{cls}"[^>]*>(.*?)</dd>', body, re.S)
            if not mm or not re.sub(r"<[^>]+>", "", mm.group(1)).strip():
                err(f"{cid}: empty {cls}")
        scene = html.unescape(re.search(r'<dd class="scene">(.*?)</dd>', body, re.S).group(1))
        n = len(scene.split())
        if not 35 <= n <= 55:
            err(f"{cid}: scene is {n} words")
        if not scene.startswith("One drawing, one panel."):
            err(f"{cid}: scene must start 'One drawing, one panel.' (one drawing per card)")
        if re.search(r"\d", scene):
            err(f"{cid}: digit in scene")
        frame_txt = cl_frames.get(cluster, "")
        if re.search(r"\b(clock|watch)(es)?\b", scene + frame_txt, re.I) and not re.search(r"\bblank\b", scene + " " + frame_txt, re.I):
            err(f"{cid}: a clock is drawn but nothing says its face is blank")
        if re.search(r"seen from behind", scene, re.I):
            err(f"{cid}: viewpoint flip ('seen from behind'); keep one camera per set, turn the figure instead")
        if re.search(r"\b(river|quay|canal)", scene + frame_txt, re.I):
            err(f"{cid}: water that reads as a canal")
        if cid in OTHER_IDS:
            err(f"{cid}: slug already a card in {OTHER_IDS[cid]}")
        if cid in WW_SLUGS:
            err(f"{cid}: slug is already a Werkwoorden row in tools/_ww_tmp/{WW_SLUGS[cid]}")
        if BANNED.search(scene):
            err(f"{cid}: souvenir imagery in scene")
        if COLOURS.search(scene):
            err(f"{cid}: colour word in scene")
        if re.search(r"\b(label|caption|word|letters|number)s?\b", scene, re.I):
            err(f"{cid}: scene mentions text in the drawing")
        lemma = html.unescape(re.search(r'<h3 class="chunk">(.*?)</h3>', body).group(1)).lower()
        split = html.unescape(re.search(r'<dd class="split">(.*?)</dd>', body, re.S).group(1)).strip()
        ex = html.unescape(re.search(r'<dd class="voorbeeld-nl">(.*?)<br>', body, re.S).group(1)).strip()
        perfect = html.unescape(re.search(r'<dd class="perfect">(.*?)</dd>', body, re.S).group(1)).strip()
        alt = html.unescape(re.search(r'<dd class="alt">(.*?)</dd>', body, re.S).group(1)).strip()
        avoid = html.unescape(re.search(r'<dd class="avoid">(.*?)</dd>', body, re.S).group(1))
        sep = "not separable" not in re.search(r'class="vlaggen">(.*?)</p>', body, re.S).group(1)
        if not sep or (expected.get(cid) and not expected[cid][2]["separable"]):
            err(f"{cid}: every card in this family must be separable")

        # split form and example
        if sep:
            sm = re.fullmatch(r"(\S+) \.\.\. (\S+)", split)
            if not sm:
                err(f"{cid}: split '{split}' is not 'finite ... particle'")
            else:
                fin, particle = sm.groups()
                toks = tokens(ex)
                if fin.lower() not in toks or particle.lower() not in toks:
                    err(f"{cid}: example does not show the split form {split}")
                elif toks.index(particle.lower()) <= toks.index(fin.lower()) + 1 and not ex.rstrip(".").lower().endswith(particle.lower()):
                    err(f"{cid}: particle must stand apart from the finite verb")
                if not ex.rstrip(" .!?").lower().endswith(particle.lower()) and toks[-1] != particle.lower():
                    err(f"{cid}: particle should close the main clause in the example")
                if not lemma.startswith(particle.lower()) and particle.lower() not in lemma:
                    err(f"{cid}: particle {particle} not in {lemma}")
                check_perfect(cid, lemma, particle.lower(), perfect)
                # alt text must not use any form of the verb, nor its particle closing a clause
                for t in leaks(alt, lemma, split, perfect):
                    err(f"{cid}: alt text contains '{t}', a form of the verb")
                # another card's finite verb, even without its particle, reads as that card (tilt: optillen)
                for t in tokens(alt):
                    if t in FINITES and FINITES[t] != cid:
                        err(f"{cid}: alt text contains '{t}', the finite verb of {FINITES[t]}")
                # the particle may only appear as a preposition before a determiner ("in een koffer")
                if re.search(rf"\b{re.escape(particle.lower())}\b(?!\s+(de|het|een|zijn|haar|hun|mijn|dit|deze|die|dat|twee|drie|beide|één)\b)", alt.lower()):
                    err(f"{cid}: alt text uses the particle '{particle}' as a particle, not a preposition")
                # another card's finite verb together with its particle reads as that card
                for oid, orow in rows.items():
                    if oid == cid or orow["scene"].upper().startswith("SKIP") or " ... " not in orow["split"]:
                        continue
                    ofin, opart = [x.lower() for x in orow["split"].split(" ... ")]
                    if re.search(rf"\b{re.escape(ofin)}t?\b.*\b{re.escape(opart)}\b\s*([,.;:]|$|(en|maar|terwijl|die|dat)\b)", alt.lower()):
                        err(f"{cid}: alt text uses '{ofin} ... {opart}', the split form of {oid}")
        if not 3 <= len(ex.split()) <= 10:
            err(f"{cid}: example is {len(ex.split())} words")
        if expected.get(cid) and expected[cid][1].get("batch") == 2 and not 5 <= len(ex.split()) <= 9:
            err(f"{cid}: batch-2 example is {len(ex.split())} words, not 5-9")
        if sep and " ... " in split:
            # a compound or derived word that hides the stem inside it (schroevendraaier, vergiet, voetpomp)
            _ex, _pre, _p = forms(lemma, split, perfect)
            for t in tokens(alt):
                for x in _pre | {x for x in _ex if len(x) >= 4 and x not in ADVERB_PARTICLES}:
                    if len(x) >= 4 and x in t and not t.startswith(x) and t not in STEM_OK.get(lemma, set()):
                        err(f"{cid}: alt word '{t}' hides '{x}', a form of the verb")

        # avoid: partner first, bracketed items are known ids or 'not ...'
        items = [x.strip() for x in avoid.split(";") if x.strip()]
        if not 3 <= len(items) <= 5:
            err(f"{cid}: {len(items)} avoid items")
        for it in items:
            mb = re.search(r"\(([^)]*)\)\.?$", it)
            if not mb:
                err(f"{cid}: avoid item without bracket: {it[:40]}")
            elif not (mb.group(1) in expected or mb.group(1) in OTHER_IDS or mb.group(1).startswith("not ")):
                err(f"{cid}: avoid bracket '{mb.group(1)}' is not a card id here or in another family")
            elif mb.group(1) in SKIPPED:
                err(f"{cid}: avoid bracket '{mb.group(1)}' names a SKIP card, which is never drawn")
        pm = re.search(r'data-partner="([^"]*)"', body)
        partners = pm.group(1).split() if pm else []
        if not partners:
            err(f"{cid}: no contrast partner on page (partner skipped?)")
        else:
            first = re.search(r"\(([^)]*)\)", items[0]) if items else None
            if not first or first.group(1) not in partners:
                err(f"{cid}: first avoid item must name a partner")
        for p in partners:
            if not re.search(rf"Pair with [^.]*\b{re.escape(p)}\b", body):
                err(f"{cid}: contrast note does not name {p}")
            if re.search(rf"\b{re.escape(p)}\b", alt.lower()):
                err(f"{cid}: alt text contains partner {p}")
            if p in rows:
                for t in leaks(alt, p, rows[p]["split"], rows[p]["perfect"]):
                    err(f"{cid}: alt text contains '{t}', a form of partner {p}")
        if re.search(r"\bnbsp\b", body) or "\t" in body:
            err(f"{cid}: stray markup")

# sets: frame ends with 'Only', sentence uses every member's particle
for fn in os.listdir(os.path.join(TMP, "scenes")):
    if fn.endswith(".clusters.tsv"):
        for r in csv.DictReader(open(os.path.join(TMP, "scenes", fn), encoding="utf-8", newline=""), delimiter="\t", quoting=csv.QUOTE_NONE):
            if not re.search(r"\. Only [^.]+\.$", r["frame"].strip()):
                err(f"{r['cluster']}: frame must end with an 'Only ...' sentence")
            if not 25 <= len(r["frame"].split()) <= 60:
                err(f"{r['cluster']}: frame is {len(r['frame'].split())} words")
            toks = tokens(r["sentence_nl"])
            members = [c for b in BANDS for c in sel.get(b, []) if c["id"] == r["cluster"]]
            for m in members[0]["members"] if members else []:
                if rows[m["id"]]["scene"].upper().startswith("SKIP"):
                    continue
                key = rows[m["id"]]["split"].split()[-1].lower()
                if key not in toks:
                    err(f"{r['cluster']}: sentence lacks '{key}' for {m['id']}")

# banding: select.py must report no problems, and every override must be printed on the overview
import importlib.util
_spec = importlib.util.spec_from_file_location("sw_select", os.path.join(TMP, "select.py"))
_sel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sel)
for p_ in _sel.problems:
    err(f"select.py: {p_}")
for b in BANDS:
    for c in sel.get(b, []):
        if c["id"] not in _sel.OVERRIDE and c.get("by_rank") != b:
            err(f"{c['id']}: on page {b} but its rank band is {c.get('by_rank')} and it has no OVERRIDE")

# another family's headword (a card's chunk) that is one of our verbs, or starts with it
OTHER_HEADS = {}
for dirpath, _dirs, files in os.walk(os.path.join(ROOT, "Docs")):
    if "archive" in dirpath or dirpath.rstrip("/").endswith("scheidbare-werkwoorden"):
        continue
    for fn in files:
        if fn.endswith(".html"):
            for h in re.findall(r'<h3 class="chunk">([^<]+)</h3>', open(os.path.join(dirpath, fn), encoding="utf-8").read()):
                OTHER_HEADS.setdefault(html.unescape(h).strip().lower(), os.path.relpath(os.path.join(dirpath, fn), ROOT))
# a different sense, judged by hand
# Batch 1 predates this check; its prepositional look-alikes (achterlaten in, stilstaan bij ...) are other senses.
HEAD_OK = {
    "opkomen": "Voorzetselpaden opkomen voor is to stand up for; here the sun rises",
    "terugkomen": "Voorzetselpaden terugkomen op is to return to a subject; here a dog comes back",
    "afstappen": "Voorzetselpaden afstappen van is to abandon an idea; here a rider gets off a bike",
    "opscheppen": "Voorzetselpaden opscheppen over is to boast; here pasta is served",
    "ondergaan": "Werkwoorden usage card ondergaan is the inseparable to undergo; here the sun sets (dropped)",
}
for i, (b, c, m) in expected.items():
    lem = m["lemma"]
    for h, where in OTHER_HEADS.items():
        if (h == lem or (c.get("batch") == 2 and h.split()[0] == lem)) and lem not in HEAD_OK:
            err(f"{i}: '{h}' is already a card in {where}")

# our participles as another family's headword (opgepompt, leeggelopen): one owner per word
for i, r in rows.items():
    if i in SKIPPED or not r["perfect"].strip():
        continue
    part = r["perfect"].split()[-1].lower()
    if part in OTHER_HEADS:
        err(f"{i}: participle '{part}' is already a headword in {OTHER_HEADS[part]}")

index = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
for k in _sel.OVERRIDE:
    if f"<td>{k}</td>" not in index:
        err(f"OVERRIDE {k}: not printed on the overview")

# Every OVERRIDE row on the overview is checked fact by fact against the lexicon files
# (model: tools/check-zelfstandige-naamwoorden-cards.py).
LEXROW = {}
for r_ in csv.DictReader(open(os.path.join(ROOT, "tools", "lexicon", "woorden.tsv"), encoding="utf-8"), delimiter="\t"):
    LEXROW.setdefault(r_["nl"], r_)
FREQ = {r_["nl"]: int(r_["rang"]) for r_ in csv.DictReader(
    open(os.path.join(ROOT, "tools", "lexicon", "woorden-frequentie.tsv"), encoding="utf-8"), delimiter="\t")}
RANK_BAND = lambda r: "a0" if r <= 250 else "a1" if r <= 1000 else "a2" if r <= 2500 else "b1" if r <= 5000 else "b2"
FACT = re.compile(r"^(?P<lem>\S+) (?:niveau (?P<niv>\S+)(?:, top2000 (?P<top>\S+))?, herkomst (?P<h>\S+)|(?P<absent>not in woorden\.tsv)), "
                  r"(?:rank (?P<r>\d+)|(?P<nr>no rank))$")
ov_html = {m_.group(1): [html.unescape(x) for x in m_.groups()[1:]] for m_ in re.finditer(
    r"<tr><td>([^<]+)</td><td>([AB][0-2])</td><td>([AB][0-2])</td><td>([a-z]+)</td><td>([^<]+)</td>"
    r"<td class=\"lexicon\">([^<]*)</td><td>([^<]*)</td></tr>", index)}
ov_sel = {c["id"]: (b, c) for b in BANDS for c in sel.get(b, []) if c.get("override")}
if set(ov_html) != set(ov_sel) or set(ov_sel) != set(_sel.OVERRIDE):
    err(f"OVERRIDE rows on the overview {sorted(set(ov_html) ^ set(ov_sel))} differ from selection.json / select.py")
for cid, (b, c) in ov_sel.items():
    if cid not in ov_html:
        continue
    ob, orb, kind, basis, lexicon, reason = ov_html[cid]
    o = c["override"]
    if (ob, orb, kind, basis, lexicon, reason) != (b.upper(), c["by_rank"].upper(), o["kind"], o["basis"], o["lexicon"], o["reason"]):
        err(f"{cid}: overview OVERRIDE row differs from selection.json")
    ranks = [FREQ[x["lemma"]] for x in c["members"] if x["lemma"] in FREQ]
    want_rb = RANK_BAND(min(ranks)) if ranks else "b2"
    if c["by_rank"] != want_rb:
        err(f"{cid}: rank band {c['by_rank']} does not follow from the members' ranks ({want_rb})")
    if kind == "promoted":
        if basis != "judgment":
            err(f"{cid}: a promotion is printed as judgment, not '{basis}'")
        if BANDS.index(b) >= BANDS.index(want_rb):
            err(f"{cid}: promoted to {b} but its rank band is {want_rb}")
    elif kind == "homograph":
        if BANDS.index(b) <= BANDS.index(want_rb):
            err(f"{cid}: homograph entry must sit later than rank band {want_rb}")
    else:
        err(f"{cid}: unknown OVERRIDE kind {kind}")
    cited = []
    for f in lexicon.split("; "):
        fm = FACT.match(f)
        if not fm:
            err(f"{cid}: unparseable lexicon fact '{f}'")
            continue
        lem = fm["lem"]
        cited.append(lem)
        row = LEXROW.get(lem)
        if fm["absent"]:
            if row:
                err(f"{cid}: says {lem} is not in woorden.tsv, but it is")
        elif not row:
            err(f"{cid}: cites {lem} niveau {fm['niv']}, but {lem} is not a woorden.tsv row")
        else:
            if fm["niv"] != (row["niveau"] or "none"):
                err(f"{cid}: says {lem} niveau {fm['niv']}, woorden.tsv says {row['niveau'] or 'none'}")
            if (fm["top"] or "") != row["top2000"]:
                err(f"{cid}: says {lem} top2000 {fm['top'] or 'empty'}, woorden.tsv says {row['top2000'] or 'empty'}")
            if fm["h"] != (row["herkomst"] or "none"):
                err(f"{cid}: says {lem} herkomst {fm['h']}, woorden.tsv says {row['herkomst']}")
        if fm["r"] and FREQ.get(lem) != int(fm["r"]):
            err(f"{cid}: says {lem} rank {fm['r']}, woorden-frequentie.tsv says {FREQ.get(lem)}")
        if fm["nr"] and lem in FREQ:
            err(f"{cid}: says {lem} has no rank, but it ranks {FREQ[lem]}")
    if cited != [x["lemma"] for x in c["members"]]:
        err(f"{cid}: lexicon facts cite {cited}, the set's members are {[x['lemma'] for x in c['members']]}")
    rm = re.match(r"(A0|A1|A2|B1|B2)(?: by (\S+) (\d+)|, no member ranked);\s*\S", reason)
    if kind != "promoted":
        pass
    elif not rm:
        err(f"{cid}: reason must open with the rank band and then give the reason after a semicolon")
    elif rm.group(1).lower() != want_rb or (rm.group(2) and (FREQ.get(rm.group(2)) != int(rm.group(3)) or int(rm.group(3)) != min(ranks))) \
            or (not rm.group(2) and ranks):
        err(f"{cid}: reason states the wrong rank band or best rank (rank band {want_rb}, best {min(ranks) if ranks else None})")
skipped = set(re.findall(r"<li><code>([^<]+)</code> \(", index))
for i in expected:
    if i not in ids_seen and i not in skipped:
        err(f"{i}: in selection, neither drawn nor skipped")

nums = [int(x) for b in BANDS for x in re.findall(r'class="framenummer" title="Frame (\d+)"',
        open(os.path.join(OUT, b + ".html"), encoding="utf-8").read())]
if nums != list(range(1, len(nums) + 1)):
    err("frame numbers are not 1..N in order")

# band sizes on the overview and each page's summary agree with the cards actually on the page
for b in BANDS:
    pg = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    n_sets = len(re.findall(r'<section class="cluster"', pg))
    fr_ = [int(x) for x in re.findall(r'class="framenummer" title="Frame (\d+)"', pg)]
    want = f"#{fr_[0]}–#{fr_[-1]}" if fr_ else "–"
    row = re.search(rf'<tr><td><a href="{b}.html">{b.upper()}</a></td><td class="n">(\d+)</td><td class="n">(\d+)</td><td class="n">([^<]*)</td>', index)
    if not row or (int(row.group(1)), int(row.group(2)), row.group(3)) != (n_sets, len(fr_), want):
        err(f"{b}: overview band row {row.groups() if row else None} differs from the page ({n_sets} sets, {len(fr_)} cards, {want})")
    sm = re.search(r'<div class="sum"><span>(\d+) contrast sets</span><span>(\d+) verbs</span>', pg)
    if not sm or (int(sm.group(1)), int(sm.group(2))) != (n_sets, len(fr_)):
        err(f"{b}: page summary differs from its {n_sets} sets and {len(fr_)} cards")
    if n_sets != len([c for c in sel.get(b, []) if any(m["id"] not in SKIPPED for m in c["members"])]):
        err(f"{b}: page has {n_sets} sets, selection.json has a different number of drawn sets")

print(f"cards {total}  skipped {len(skipped)}  errors {len(errors)}")
for e in errors:
    print("  " + e)
sys.exit(1 if errors else 0)
