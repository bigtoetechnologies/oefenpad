#!/usr/bin/env python3
"""Assert the noun card pages are consistent with selection.json and the scene TSVs."""
import csv
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "tools", "_zn_tmp")
OUT = os.path.join(ROOT, "Docs", "zelfstandige-naamwoorden")
BANDS = ["a0", "a1", "a2", "b1", "b2"]
NEW_BANDS = ("b1", "b2")          # bands authored under the 2026-11-20 expansion rules
# Scenes another (higher-priority) family owns; a noun card must not be drawn in them.
OTHER_FAMILY_SCENES = {
    "washing line": "adjectives droog/nat and winderig/windstil",
}
# Words that ask for text in the artwork; allowed only straight after "no".
ART_TEXT = re.compile(r"\b(letters?|words?|text|numbers?|numerals?|logos?|labels?|writing|signs?|signboards?)\b", re.I)
BANNED = re.compile(r"\b(windmill|clog|tulip|canal|cheese|kaas|klomp(en)?|molens?|tulpen|tulp|grachten|gracht)s?\b", re.I)
COLOURS = re.compile(r"\b(red|blue|green|yellow|orange|pink|purple|brown|grey|gray|white|black)\b", re.I)
COLOURS_NL = re.compile(r"\b(rood|rode|blauwe?|groene?|geel|gele|oranje|paarse?|roze|bruine?|grijs|grijze|wit|witte|zwarte?)\b", re.I)
# Exceptions agreed in the 2026-11-20 review: the arm/been card must show the whole figure,
# so been-een cannot reuse the been drawing.
OWN_DRAWING_EXEMPT = {"been-een", "been-meer"}


def norm(w):
    """Collapse doubled vowels and strip diminutive/plural endings, so
    blaadjes -> blad, kopjes -> kop, huizen -> huiz."""
    w = w.lower()
    for v in ("aa", "ee", "oo", "uu"):
        w = w.replace(v, v[0])
    for suf in ("etjes", "etje", "tjes", "tje", "pjes", "pje", "jes", "je"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def leaks(text, form):
    """True when a word in text is form, an inflection or diminutive of it,
    or (for forms of 4+ letters) a compound containing it."""
    f = norm(form)
    if len(f) < 2:
        return False
    for w in re.findall(r"[a-zà-ÿ']+", text.lower()):
        n = norm(w)
        if n == f or w.startswith(form.lower()) or (len(f) >= 3 and n.startswith(f) and len(n) - len(f) <= 3):
            return True
        if len(f) >= 4 and n.endswith(f) and len(n) - len(f) >= 4:   # compound: kroonblaadjes
            return True
    return False


def component_leak(text, lemma):
    """Return the alt word that is a part of the compound lemma (bed in dekbed,
    tandjes in tandenborstel), or contains the lemma inside it (tak in vertakte)."""
    lem = lemma.lower()
    for w in re.findall(r"[a-zà-ÿ']+", text.lower()):
        stems = {w}
        for suf in ("etjes", "etje", "tjes", "tje", "pjes", "pje", "jes", "je"):
            if w.endswith(suf) and len(w) - len(suf) >= 3:
                stems.add(w[: -len(suf)])
                break
        for n in stems:
            if len(n) >= 3 and len(lem) >= len(n) + 3 and (lem.startswith(n) or lem.endswith(n)):
                return w
        if len(lem) >= 3 and lem in w[1:] and w != lem and w not in INFIX_OK:
            return w
    return None


# Words that contain a lemma by accident of spelling, not as a morpheme.
INFIX_OK = {"horizon"}


def regular_plurals(lemma):
    """Plurals that follow the spelling rules alone (no vowel or stem change)."""
    out = {lemma + "s", lemma + "'s", lemma + "en"}
    stem = lemma
    short = re.search(r"[^aeiou][aeiou][^aeiouwj]$", lemma) or re.match(r"^[aeiou][^aeiouwj]$", lemma)
    if short:                              # short vowel doubles the consonant: kat -> katten, bus -> bussen
        out.add(lemma + lemma[-1] + "en")
        return out
    if stem[-1] == "s":                    # s -> z, f -> v after a long vowel or diphthong
        stem = stem[:-1] + "z"
    elif stem[-1] == "f":
        stem = stem[:-1] + "v"
    m = re.match(r"^(.*?)([aeou])\2([^aeiou]+)$", stem)
    if m:                                  # long vowel in closed syllable: boom -> bomen
        out.add(m.group(1) + m.group(2) + m.group(3) + "en")
    out.add(stem + "en")
    return out
errors = []


def err(msg):
    errors.append(msg)


sel = json.load(open(os.path.join(TMP, "selection.json"), encoding="utf-8"))
ids_expected = {m["id"]: (b, c["id"], c) for b in BANDS for c in sel.get(b, []) for m in c["members"]}
sentences_by_cluster = {}
for p in sorted(glob.glob(os.path.join(TMP, "scenes", "*.clusters.tsv"))):
    for line in open(p, encoding="utf-8").read().splitlines()[1:]:
        f = line.split("\t")
        sentences_by_cluster[f[0]] = f
# Cards authored under the expansion rules, wherever an override has placed their set.
NEW_IDS = set()
for p in sorted(glob.glob(os.path.join(TMP, "scenes", "b[12].cards.tsv"))):
    NEW_IDS |= {line.split("\t")[0] for line in open(p, encoding="utf-8").read().splitlines()[1:]}
LEX = {}
for line in open(os.path.join(ROOT, "tools", "lexicon", "woorden.tsv"), encoding="utf-8").read().splitlines()[1:]:
    f = line.split("\t")
    if len(f) >= 4:
        LEX.setdefault(f[0], (f[2], f[3]))
ids_seen = {}
total = 0
for b in BANDS:
    text = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    for m in re.finditer(r'<article id="([^"]+)" class="kaart" data-id="([^"]+)" data-band="([^"]+)" '
                         r'data-kind="noun" data-article="([^"]+)" data-plural="([^"]*)" data-dim="([^"]+)" data-cluster="([^"]+)"(.*?)</article>', text, re.S):
        cid, did, band, art, plur, dim, cluster, body = m.groups()
        total += 1
        if cid != did:
            err(f"{cid}: id != data-id")
        if band != b:
            err(f"{cid}: band {band} on page {b}")
        if cid in ids_seen:
            err(f"{cid}: duplicate card")
        ids_seen[cid] = cluster
        mem = next((x for x in ids_expected[cid][2]["members"] if x["id"] == cid), None) if cid in ids_expected else None
        if mem:
            if (art, html.unescape(plur), dim) != (mem["article"], mem["plural"], mem["dim"] or "no"):
                err(f"{cid}: article/plural/dim differ from selection")
            if art not in ("de", "het"):
                err(f"{cid}: article {art}")
            if not plur:
                err(f"{cid}: no plural")
            if dim == "yes" and not mem["lemma"].endswith("je"):
                err(f"{cid}: diminutive flag on a non -je word")
            if mem["lemma"].endswith("je") and dim != "yes":
                err(f"{cid}: -je word without diminutive flag")
            if not re.search(rf'<h3 class="chunk">{art} {re.escape(mem["lemma"])}</h3>', body):
                err(f"{cid}: heading lacks article")
            if not re.search(r'class="vormen"', body):
                err(f"{cid}: no forms line")
            ex = re.search(r'<dd class="voorbeeld-nl">(.*?)<br>', body, re.S)
            forms = (mem["lemma"], mem["plural"])
            if ex and not any(re.search(rf"\b{re.escape(f)}", ex.group(1), re.I) for f in forms):
                err(f"{cid}: example does not use the noun or its plural")
        if cid not in ids_expected or ids_expected[cid][1] != cluster:
            err(f"{cid}: not in selection for cluster {cluster}")
        for cls in ("scene", "must", "avoid", "contrast-note", "voorbeeld-nl", "alt"):
            mm = re.search(rf'<dd class="{cls}"[^>]*>(.*?)</dd>', body, re.S)
            if not mm or not re.sub(r"<[^>]+>", "", mm.group(1)).strip():
                err(f"{cid}: empty {cls}")
        scene = re.search(r'<dd class="scene">(.*?)</dd>', body, re.S)
        if scene:
            n = len(scene.group(1).split())
            if not 25 <= n <= 75:
                err(f"{cid}: scene is {n} words")
            sc = html.unescape(scene.group(1))
            if BANNED.search(body):
                err(f"{cid}: souvenir imagery (scene, example or alt)")
            if COLOURS.search(sc):
                err(f"{cid}: colour word in scene")
            if re.search(r"\bfive fingers\b[^.]*\bthumb", sc, re.I):
                err(f"{cid}: five fingers and a thumb is six digits")
            if re.search(r"\btwice (the|as) (height|tall)", sc, re.I):
                err(f"{cid}: scene sets a height against a same-height frame")
            frame_row = sentences_by_cluster.get(cluster)
            if frame_row and re.search(r"\bno (people|person)\b", frame_row[1], re.I):
                stripped = re.sub(r"\bno [a-z]+", "", sc, flags=re.I)
                if re.search(r"\b(a|an|one|small|tiny) (small |tiny )?(person|figure|man|woman)\b(?!')", stripped, re.I):
                    err(f"{cid}: scene adds a person although the frame says no people")
            if mem and cid.endswith("-een") and cid not in OWN_DRAWING_EXEMPT and mem["lemma"] in ids_expected:
                if f"same drawing as the {mem['lemma']} card" not in sc.lower():
                    err(f"{cid}: does not reuse the drawing of card {mem['lemma']}")
            if mem and cid.endswith("-meer") and cid not in OWN_DRAWING_EXEMPT:
                base = cid[: -len("-meer")]
                if base in ids_expected and f"copies of the {base} drawing" not in sc.lower():
                    err(f"{cid}: does not reuse the drawing of card {base}")
        ex_nl = re.search(r'<dd class="voorbeeld-nl">(.*?)<br>', body, re.S)
        if ex_nl and COLOURS_NL.search(ex_nl.group(1)):
            err(f"{cid}: example names a colour a one-colour drawing cannot show")
        if mem and mem["dim"] == "yes" and not mem.get("base"):
            err(f"{cid}: diminutive without its base noun")
        if mem and mem.get("base") and f"van {mem['base']}" not in body:
            err(f"{cid}: base noun {mem['base']} not shown on the card")
        gl = re.search(r'<p class="gloss">(.*?)</p>', body)
        if mem and gl and (";" in gl.group(1) or ":" in gl.group(1)):
            err(f"{cid}: gloss contains a field separator")
        alt = re.search(r'<dd class="alt">(.*?)</dd>', body, re.S)
        if alt and mem:
            a = html.unescape(alt.group(1))
            if COLOURS_NL.search(a):
                err(f"{cid}: colour word in alt text")
            sib = [x for x in ids_expected[cid][2]["members"]]
            for x in sib:
                forms = {x["lemma"], x["plural"]} | ({x["base"].split()[-1]} if x.get("base") else set())
                for f in forms:
                    if leaks(a, f):
                        err(f"{cid}: alt text contains {f} (or a form, stem or compound of it)")
                cl = component_leak(a, x["lemma"])
                if cl:
                    err(f"{cid}: alt word '{cl}' is a part of {x['lemma']} or contains it")
        pm = re.search(r'data-partner="([^"]*)"', body)
        partners = pm.group(1).split() if pm else []
        for cls in ("scene", "must", "avoid", "contrast-note", "voorbeeld-nl", "alt"):
            mm = re.search(rf'<dd class="{cls}"[^>]*>(.*?)</dd>', body, re.S)
            if mm and re.search(r"\d", re.sub(r"<[^>]+>", "", mm.group(1))):
                err(f"{cid}: digit in {cls}")
        if scene:
            for t in ART_TEXT.finditer(sc):
                if not re.search(r"\bno\s+(\w+\s+)?$", sc[max(0, t.start() - 20):t.start()], re.I):
                    err(f"{cid}: scene asks for text in the artwork ({t.group(0)})")
        if scene:
            for ph, owner in OTHER_FAMILY_SCENES.items():
                if ph in sc.lower():
                    err(f"{cid}: scene uses a {ph}, which belongs to {owner}")
        if b in NEW_BANDS or cid in NEW_IDS:
            av = re.search(r'<dd class="avoid">(.*?)</dd>', body, re.S)
            items = [x.strip() for x in html.unescape(av.group(1)).split(";")] if av else []
            head = items[:len(partners)]
            if sorted(re.sub(r".*\(([^)]+)\)\.?$", r"\1", x) for x in head) != sorted(partners):
                err(f"{cid}: avoid list does not name its partners first with their ids")
            cn = re.search(r'<dd class="contrast-note"[^>]*>(.*?)</dd>', body, re.S)
            if cn and not cn.group(1).startswith("Pair with "):
                err(f"{cid}: contrast note does not start with 'Pair with'")
            for cls, pat in (("voorbeeld-nl", r'<dd class="voorbeeld-nl">(.*?)<br>'),
                             ("voorbeeld-en", r'<span class="voorbeeld-en">(.*?)</span>')):
                mm = re.search(pat, body, re.S)
                n = len(html.unescape(mm.group(1)).split()) if mm else 0
                if not 5 <= n <= 9:
                    err(f"{cid}: {cls} example is {n} words (5-9 wanted)")
        if not partners:
            err(f"{cid}: no contrast partner on page (partner skipped?)")
        for p in partners:
            if not re.search(rf"Pair with [^.]*\b{re.escape(p)}\b", body):
                err(f"{cid}: contrast note does not name {p}")
        if re.search(r"\bnbsp\b", body) or "\t" in body:
            err(f"{cid}: stray markup")

sentences = {}
for cl, f in sentences_by_cluster.items():
    if len(f) != 4:
        err(f"{cl}: bad cluster row")
        continue
    sentences[cl] = f
    n = len(f[1].split())
    if not 25 <= n <= 60 or "Only " not in f[1]:
        err(f"{cl}: frame is {n} words or lacks an 'Only' sentence")
    if COLOURS.search(f[1]):
        err(f"{cl}: colour word in frame")
    if BANNED.search(" ".join(f[1:])):
        err(f"{cl}: souvenir imagery in frame or sentence")
    if COLOURS_NL.search(f[2]):
        err(f"{cl}: contrast sentence names a colour")
    if re.search(r"\bfamilie woont\b", f[2]):
        err(f"{cl}: a household is het gezin, not de familie")
for b in BANDS:
    for c in sel.get(b, []):
        f = sentences.get(c["id"])
        if not f:
            err(f"{c['id']}: no cluster row")
            continue
        if not 2 <= len(c["members"]) <= 3:
            err(f"{c['id']}: {len(c['members'])} members")
        for x in c["members"]:
            if not re.search(rf"\b{x['article']} {re.escape(x['lemma'])}\b", f[2], re.I):
                err(f"{c['id']}: sentence lacks '{x['article']} {x['lemma']}'")

        if "irregular" in c["axis"]:
            if all(x["plural"] in regular_plurals(x["lemma"]) for x in c["members"] if x["id"].endswith("-een")):
                err(f"{c['id']}: labelled irregular but the plural follows the spelling rules")
        elif c["id"].endswith("-getal"):
            if any(x["plural"] not in regular_plurals(x["lemma"]) for x in c["members"] if x["id"].endswith("-een")):
                err(f"{c['id']}: irregular plural not labelled irregular")
        if c.get("override") and c.get("rank_band") == c["band"]:
            err(f"{c['id']}: override repeats the rank band {c['band'].upper()}")
        if not c.get("override") and c.get("rank_band") != c["band"]:
            err(f"{c['id']}: band {c['band']} differs from rank band {c.get('rank_band')} without an override")
        if b in NEW_BANDS:
            for x in c["members"]:
                niv, top = LEX.get(x["lemma"], ("", ""))
                if (niv in ("A0", "A1") or top == "1") and x["lemma"] not in sel.get("_coursebook_sense", {}):
                    err(f"{c['id']}: {x['lemma']} is coursebook {niv or 'top-2000'} in woorden.tsv but the set sits in {b.upper()}; promote it with an OVERRIDE")
                if x["id"].endswith("-meer"):
                    continue
                if not x.get("rank"):
                    if x["lemma"] not in sel.get("_no_rank", {}):
                        err(f"{x['id']}: no lexicon rank for the singular {x['lemma']}; list it in NO_RANK with a reason")
                    elif not any(y.get("rank") and y["id"] != x["id"] for y in c["members"]):
                        err(f"{x['id']}: unranked and no ranked partner carries the band")
                elif x["rank"] > 10000:
                    err(f"{x['id']}: rank {x['rank']} is beyond B2")
                elif not c.get("override") and x["rank"] <= 2500:
                    err(f"{x['id']}: rank {x['rank']} is an A-band word inside a {b.upper()} set")
        if c.get("override") and c["band"] != b:
            err(f"{c['id']}: override band {c['band']} but listed under {b}")

index = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
for b in BANDS:
    for c in sel.get(b, []):
        if c.get("override") and not re.search(rf"<tr><td>{re.escape(c['id'])}</td><td>{b.upper()}</td>", index):
            err(f"{c['id']}: override not documented on the overview page")

# Every override reason is checked fact by fact against the lexicon files, as printed on the overview.
LEXROW = {}
for r in csv.DictReader(open(os.path.join(ROOT, "tools", "lexicon", "woorden.tsv"), encoding="utf-8"), delimiter="\t"):
    LEXROW.setdefault(r["nl"], r)
FREQ = {r["nl"]: int(r["rang"]) for r in csv.DictReader(
    open(os.path.join(ROOT, "tools", "lexicon", "woorden-frequentie.tsv"), encoding="utf-8"), delimiter="\t")}
CB_FOR = {k: set(v) for k, v in sel.get("_coursebook_for", {}).items()}
LEX_ROW = sel.get("_lex_row", {})
RANK_BAND = lambda r: "a0" if r <= 250 else "a1" if r <= 1000 else "a2" if r <= 2500 else "b1" if r <= 5000 else "b2"
FACT = re.compile(r"^(?P<lem>.+?) niveau (?P<niv>\S+)(?:, top2000 (?P<top>\S+))?, herkomst (?P<h>\S+), (?:rank (?P<r>\d+)|(?P<nr>no usable rank))$")
NOTE_BANNED = re.compile(r"(?i)coursebook|bijlage|top.?2000|niveau|herkomst|\brank|woorden|lexicon list|\d")
ov_html = {m.group(1): (m.group(2), m.group(3), html.unescape(m.group(4))) for m in re.finditer(
    r"<tr><td>([^<]+)</td><td>([A-B][0-2])</td><td>([A-Z0-9]+)</td><td>(.*?)</td></tr>", index)}
for b in BANDS:
    for c in sel.get(b, []):
        if not c.get("override"):
            continue
        cid = c["id"]
        if cid not in ov_html:
            continue
        ob, orb, txt = ov_html[cid]
        if txt != c["override"]:
            err(f"{cid}: overview reason differs from selection.json")
        if ob != b.upper() or orb != (c.get("rank_band") or "none").upper():
            err(f"{cid}: overview bands {ob}/{orb} differ from selection {b}/{c.get('rank_band')}")
        ranks = [x["rank"] for x in c["members"] if x.get("rank")]
        if ranks and RANK_BAND(min(ranks)) != c.get("rank_band"):
            err(f"{cid}: rank band {c.get('rank_band')} does not follow from best rank {min(ranks)}")
        m = re.match(r"^Lexicon: (.*?)\. Basis: (.*?)\.(?: Note: (.*)\.)?$", txt)
        if not m:
            err(f"{cid}: override reason is not 'Lexicon: ... Basis: ... [Note: ...]': {txt}")
            continue
        facts, basis, note = m.groups()
        cited, qual = [], []
        for f in facts.split("; "):
            fm = FACT.match(f)
            if not fm:
                err(f"{cid}: unparseable lexicon fact '{f}'")
                continue
            lem = fm["lem"]
            row = LEXROW.get(lem)
            if not row:
                err(f"{cid}: cites {lem}, which is not a woorden.tsv row")
                continue
            cited.append(lem)
            if fm["niv"] != (row["niveau"] or "none"):
                err(f"{cid}: says {lem} niveau {fm['niv']}, woorden.tsv says {row['niveau'] or 'none'}")
            if (fm["top"] or "") != row["top2000"]:
                err(f"{cid}: says {lem} top2000 {fm['top'] or 'empty'}, woorden.tsv says {row['top2000'] or 'empty'}")
            if fm["h"] != row["herkomst"]:
                err(f"{cid}: says {lem} herkomst {fm['h']}, woorden.tsv says {row['herkomst']}")
            bare = next((k for k, v in LEX_ROW.items() if v == lem), lem)
            if fm["r"]:
                if FREQ.get(lem) != int(fm["r"]) or lem != bare:
                    err(f"{cid}: says {lem} rank {fm['r']}, woorden-frequentie.tsv says {FREQ.get(lem)}")
            elif bare in FREQ and bare not in sel.get("_no_rank", {}):
                err(f"{cid}: says {lem} has no usable rank, but {bare} ranks {FREQ[bare]}")
            if ({row["niveau"]} | set(row["herkomst"].split(";"))) & CB_FOR.get(b, set()):
                qual.append(lem)
        want = {LEX_ROW.get(x["lemma"], x["lemma"]) for x in c["members"]
                if not (x["id"].endswith("-meer") and LEX_ROW.get(x["lemma"], x["lemma"]) not in LEXROW)}
        if set(cited) != want or len(cited) != len(set(cited)):
            err(f"{cid}: reason cites {cited}, the set's lexicon rows are {sorted(want)}")
        if basis.startswith("coursebook"):
            named = re.fullmatch(r"coursebook \((.*)\)", basis)
            named = named.group(1).split(", ") if named else []
            if not qual or sorted(named) != sorted(qual):
                err(f"{cid}: basis '{basis}', but the members taught at or below {b.upper()} are {qual or 'none'}")
        elif basis == "judgment, not lexicon data":
            if qual:
                err(f"{cid}: basis judgment, but {qual} is taught at or below {b.upper()}; say coursebook")
        else:
            err(f"{cid}: unknown basis '{basis}'")
        if note and NOTE_BANNED.search(note):
            err(f"{cid}: note states a lexicon fact outside the checked Lexicon part: '{note}'")
# Everyday items sit at A2 at the highest (decisions.html, 2026-11-20). A judgment override that
# promotes a set must land at or below the ceiling, and must say its judgment in a note.
BORD = {b: i for i, b in enumerate(BANDS)}
CEIL = sel.get("_judgment_ceiling")
if not CEIL:
    err("selection.json has no _judgment_ceiling (rerun select.py)")
for b in BANDS:
    for c in sel.get(b, []):
        ov = c.get("override") or ""
        if "Basis: judgment" not in ov:
            continue
        if " Note: " not in ov or not ov.split(" Note: ", 1)[1].strip(" ."):
            err(f"{c['id']}: judgment override without a note stating the judgment")
        if CEIL and c.get("rank_band") and BORD[b] < BORD[c["rank_band"]] and BORD[b] > BORD[CEIL]:
            err(f"{c['id']}: judgment promotion to {b.upper()}; everyday items go to {CEIL.upper()} or lower")

# The everyday-item review: every B1/B2 set is in the table as kept; every promoted set sits in an
# A band with an override; the overview rows and counts match selection.json.
RV = sel.get("_everyday_review")
if RV is None:
    err("selection.json has no _everyday_review (rerun select.py)")
    RV = {}
band_of = {c["id"]: b for b in BANDS for c in sel.get(b, [])}
ov_of = {c["id"]: c.get("override") or "" for b in BANDS for c in sel.get(b, [])}
for b in ("b1", "b2"):
    for c in sel.get(b, []):
        if c["id"] not in RV:
            err(f"{c['id']}: sits in {b.upper()} but is not in the everyday-item review (EVERYDAY_REVIEW in select.py)")
        elif RV[c["id"]][1] != "kept":
            err(f"{c['id']}: review says {RV[c['id']][1]} but the set sits in {b.upper()}")
rv_html = {m.group(1): (m.group(2), m.group(3), m.group(4), html.unescape(m.group(5))) for m in re.finditer(
    r'<tr class="review"><td>([^<]+)</td><td>([AB][0-2])</td><td>([AB][0-2])</td><td>(promoted|kept)</td><td>(.*?)</td></tr>', index)}
if set(rv_html) != set(RV):
    err(f"overview review table differs from EVERYDAY_REVIEW: {sorted(set(rv_html) ^ set(RV))}")
for cid, (was, dec, why) in RV.items():
    now = band_of.get(cid)
    if now is None:
        err(f"{cid}: in the everyday-item review but not in selection.json")
        continue
    if was not in ("b1", "b2"):
        err(f"{cid}: review 'was' band {was} is not B1 or B2")
    if dec == "promoted":
        if now not in ("a0", "a1", "a2"):
            err(f"{cid}: review says promoted but the set sits in {now.upper()}")
        if not ov_of[cid]:
            err(f"{cid}: promoted without an OVERRIDE entry")
        want = "judgment: " + ov_of[cid].split(" Note: ", 1)[1].rstrip(".") if " Note: " in ov_of[cid] else None
    elif dec == "kept":
        if now != was:
            err(f"{cid}: review says kept in {was.upper()} but the set sits in {now.upper()}")
        want = why
    else:
        err(f"{cid}: unknown review decision {dec}")
        continue
    if not want:
        err(f"{cid}: review decision {dec} has no reason")
    row = rv_html.get(cid)
    if row and row != (was.upper(), now.upper(), dec, want):
        err(f"{cid}: overview review row {row} differs from selection ({was.upper()}, {now.upper()}, {dec}, {want})")
mcount = re.search(r"(\d+) were promoted to A2 and (\d+) kept", index)
if RV and (not mcount or (int(mcount.group(1)), int(mcount.group(2))) !=
           (sum(v[1] == "promoted" for v in RV.values()), sum(v[1] == "kept" for v in RV.values()))):
    err("overview review counts do not match the review table")

# Band sizes on the overview table match the band pages.
for b in BANDS:
    pg = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    ns, nc = pg.count('<section class="cluster"'), pg.count('class="kaart"')
    if not re.search(rf'<a href="{b}.html">{b.upper()}</a></td><td class="n">{ns}</td><td class="n">{nc}</td>', index):
        err(f"{b}: overview band size differs from the page ({ns} sets, {nc} cards)")

lo = re.search(r"Left out on purpose</h2>(.*?)</ul>", index, re.S)
if lo:
    for i in ids_expected:
        lem = next(x["lemma"] for x in ids_expected[i][2]["members"] if x["id"] == i)
        if re.search(rf"(?<!/)\b{re.escape(lem)}\b(?!/)", re.sub(r"<[^>]+>", "", lo.group(1))):
            err(f"{i}: overview lists {lem} as left out, but it is a card")
skipped = set(re.findall(r"<li><code>([^<]+)</code> \(", index))
for i in ids_expected:
    if i not in ids_seen and i not in skipped:
        err(f"{i}: in selection, neither drawn nor skipped")

nums = [int(x) for b in BANDS for x in re.findall(r'class="framenummer" title="Frame (\d+)"',
        open(os.path.join(OUT, b + ".html"), encoding="utf-8").read())]
if nums != list(range(1, len(nums) + 1)):
    err("frame numbers are not 1..N in order")

print(f"cards {total}  skipped {len(skipped)}  errors {len(errors)}")
for e in errors:
    print("  " + e)
sys.exit(1 if errors else 0)
