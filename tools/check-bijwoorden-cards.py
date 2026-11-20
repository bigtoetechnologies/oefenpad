#!/usr/bin/env python3
"""Assert the Bijwoorden card pages are consistent with selection.json and the scene TSVs."""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "tools", "_bw_tmp")
OUT = os.path.join(ROOT, "Docs", "bijwoorden")
BANDS = ["a0", "a1", "a2", "b1"]   # no B2 band (owner ruling 20 Nov 2026)
BANNED = re.compile(r"\b(windmill|clog|tulip|canal|cheese)s?\b", re.I)
COLOURS = re.compile(r"\b(red|blue|green|yellow|orange|pink|purple|brown|grey|gray|dark|darker|pale|tinted|glow|glows|glowing)\b", re.I)
# Words of a card phrase that are too common to ban from alt text on their own.
STOP = {"de", "het", "een", "te", "naar", "bij", "per", "'s"}
# Stems hidden inside compound adverbs: the alt text may not use these either ("hoog boven" for omhoog).
STEMS = {
    "omhoog": ["hoog"], "omlaag": ["laag"], "ondersteboven": ["onder", "boven"], "bovenaan": ["boven"],
    "onderaan": ["onder"], "achteraan": ["achter"], "achterin": ["achter"], "achteruit": ["achter"],
    "vooraan": ["voor"], "voorin": ["voor"], "vooruit": ["voor"], "evenveel": ["even", "veel"],
    "rechtdoor": ["recht"], "rechtsaf": ["recht", "rechts"], "linksaf": ["links"], "rechtop": ["recht"],
    "overdag": ["dag"], "'s nachts": ["nacht"], "nergens": ["ergens"], "overal": ["over"],
    "boven": ["boven"], "beneden": ["beneden"], "minder": ["min"], "midden": ["midden"],
    "voorop": ["voor", "op"], "achterop": ["achter", "op"], "ondergronds": ["onder", "grond"],
    "bovengronds": ["boven", "grond"], "verderop": ["verder", "ver", "op"], "hiernaast": ["hier", "naast"],
    "overeind": ["over", "eind"], "onderuit": ["onder", "uit"], "achterover": ["achter", "over"],
    "voorover": ["voor", "over"], "overboord": ["over", "boord"], "aan boord": ["aan", "boord"],
    "hierheen": ["hier", "heen"], "daarheen": ["daar", "heen"], "languit": ["lang", "uit"],
    "opgerold": ["rol", "gerold", "op"], "bovenin": ["boven"], "onderin": ["onder"],
    "verticaal": ["verticaal"], "horizontaal": ["horizontaal"], "schuin": ["schuin"], "dwars": ["dwars"],
    "halverwege": ["halver", "half", "helft"], "onderuit (gaan)": ["onder", "uit", "onderuit"],
}
# Adverbs that are also prepositions: in an example they must not be followed by a noun phrase.
PREP_LIKE = {"rechts", "links", "bovenaan", "onderaan", "vooraan", "achteraan", "voorin", "achterin",
             "boven", "beneden", "binnen", "buiten", "midden", "op", "over", "af", "aan", "uit", "opzij",
             "voorop", "achterop", "bovenin", "onderin"}
PREP_FOLLOW = r"(de|het|een|van|deze|die|dit|dat|mijn|jouw|zijn|haar|onze|hun)"
PERSON = re.compile(r"\b(man|vrouw|jongen|meisje)\b")
# Words this family's cards take: no other family may card them (onderuit is taught as "onderuit (gaan)").
TAKEN_HERE = {"onderuitgaan": "onderuit"}
# Scene words that invite text into the artwork (a sign carries lettering; draw the goods instead).
TEXTY = re.compile(r"\b(signs?|signboards?|posters?|labels?)\b", re.I)
# Cross-family overlaps the owner has ruled on: the word stays here; the other family drops it or uses another sense.
RULED = {
    "boven": "voorzetselpaden draws the preposition sense (above); this card is upstairs",
    "thuis": "ruling 2026-11-20: Bijwoorden keeps it, Vaste uitdrukkingen drops it",
    "onderweg": "ruling 2026-11-20: Bijwoorden keeps it, Vaste uitdrukkingen drops it",
    "overdag": "ruling 2026-11-20: Bijwoorden keeps it, Vaste uitdrukkingen drops it",
    "rechtop": "ruling 2026-11-20: Bijwoorden keeps it, Vaste uitdrukkingen drops it",
}
# Sets added in the B1/B2 expansion of 20 Nov 2026; they follow the stricter example rule (5-9 words).
SINCE_B2 = {"voorop-achterop", "dwars-schuin", "ondergronds-bovengronds", "verderop-hiernaast", "overeind-onderuit",
            "achterover-voorover", "boord", "bovenin-onderin"}
OTHER = ["bijvoeglijke-naamwoorden", "voorzetselpaden", "vaste-uitdrukkingen", "werkwoorden",
         "zelfstandige-naamwoorden", "scheidbare-werkwoorden"]
warnings = []
errors = []


def err(msg):
    errors.append(msg)


sel = json.load(open(os.path.join(TMP, "selection.json"), encoding="utf-8"))
ids_expected = {m["id"]: (b, c["id"], c) for b in BANDS for c in sel.get(b, []) for m in c["members"]}
ids_seen = {}
alts_by_cluster = {}
drawn_lemmas = {}
lemma_of = {m["id"]: m["lemma"].lower() for b in BANDS for c in sel.get(b, []) for m in c["members"]}
total = 0
for b in BANDS:
    text = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    for m in re.finditer(r'<article id="([^"]+)" class="kaart" data-id="([^"]+)" data-band="([^"]+)" '
                         r'data-kind="adverb" data-cluster="([^"]+)"(.*?)</article>', text, re.S):
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
        for cls in ("scene", "must", "avoid", "contrast-note", "voorbeeld-nl", "alt"):
            mm = re.search(rf'<dd class="{cls}"[^>]*>(.*?)</dd>', body, re.S)
            if not mm or not re.sub(r"<[^>]+>", "", mm.group(1)).strip():
                err(f"{cid}: empty {cls}")
        scene = re.search(r'<dd class="scene">(.*?)</dd>', body, re.S)
        if scene:
            n = len(scene.group(1).split())
            if not 35 <= n <= 60:
                err(f"{cid}: scene is {n} words")
            if BANNED.search(scene.group(1)):
                err(f"{cid}: souvenir imagery in scene")
            if TEXTY.search(scene.group(1)):
                err(f"{cid}: scene has a sign or label, which invites text")
            if COLOURS.search(scene.group(1)):
                err(f"{cid}: colour word in scene")
            if re.search(r"\d", scene.group(1)) or re.search(r"\b(text|letters?|words?|numbers?|digits?|label)\b", scene.group(1), re.I):
                err(f"{cid}: scene mentions digits, letters or text")
        alt = re.search(r'<dd class="alt">(.*?)</dd>', body, re.S)
        lemma = re.search(r'<h3 class="chunk">(.*?)</h3>', body).group(1).lower()
        pm = re.search(r'data-partner="([^"]*)"', body)
        partners = pm.group(1).split() if pm else []
        # The alt text must name neither the item nor any partner, nor a word or hidden stem of either.
        # Stems of 4+ letters match as a word prefix (bovenste, hoogste); shorter ones as whole words.
        forbidden = set()
        for ph in [lemma] + [lemma_of[p] for p in partners if p in lemma_of]:
            ph = ph.replace("&#x27;", "'").lower()
            forbidden.add(ph)
            forbidden.update(w for w in ph.split() if w not in STOP)
            forbidden.update(STEMS.get(ph, []))
        alt_text = alt.group(1).replace("&#x27;", "'").lower() if alt else ""
        for w in sorted(forbidden):
            pat = rf"(?<![\w']){re.escape(w)}" + (r"(?!\w)" if len(w) < 4 else "")
            if re.search(pat, alt_text):
                err(f"{cid}: alt text contains {w}")
        alts_by_cluster.setdefault(cluster, set()).update(PERSON.findall(alt_text))
        drawn_lemmas[cid] = lemma.replace("&#x27;", "'")
        av = re.search(r'<dd class="avoid">(.*?)</dd>', body, re.S)
        if av:
            items = [x for x in av.group(1).split(";") if x.strip()]
            if not 3 <= len(items) <= 5:
                err(f"{cid}: avoid has {len(items)} items")
            if not all(re.search(r"\([^)]+\)\.?\s*$", x.strip()) for x in items):
                err(f"{cid}: an avoid item has no bracketed contrast")
            first = re.search(r"\(([^)]+)\)\.?\s*$", items[0].strip()) if items else None
            names = set(partners) | {lemma_of[p] for p in partners if p in lemma_of}
            if partners and (not first or first.group(1) not in names):
                err(f"{cid}: first avoid item does not name a partner")
            for x in items:
                mm = re.search(r"\(([^)]+)\)\.?\s*$", x.strip())
                # An id that is only the hyphenated word (aan-boord) is printed as the word; an id that
                # separates two senses (alleen-solo, op-leeg) stays, since the word alone is ambiguous.
                if mm and mm.group(1) in lemma_of and mm.group(1) == lemma_of[mm.group(1)].replace(" ", "-") and " " in lemma_of[mm.group(1)]:
                    err(f"{cid}: avoid item names the id {mm.group(1)}, not the word {lemma_of[mm.group(1)]}")
        ex = re.search(r'<dd class="voorbeeld-nl">(.*?)<br>', body, re.S)
        lo = 5 if cluster in SINCE_B2 else 3   # sets written before the B2 expansion keep the old 3-10 rule
        hi = 9 if cluster in SINCE_B2 else 10
        if ex and not lo <= len(ex.group(1).split()) <= hi:
            err(f"{cid}: example is {len(ex.group(1).split())} words ({lo}-{hi})")
        if ex and lemma in PREP_LIKE and re.search(rf"\b{re.escape(lemma)} {PREP_FOLLOW}\b", ex.group(1).lower()):
            err(f"{cid}: example uses {lemma} as a preposition")
        if not partners:
            err(f"{cid}: no contrast partner on page (partner skipped?)")
        for p in partners:
            if not re.search(rf"Pair with [^.]*\b{re.escape(p)}\b", body):
                err(f"{cid}: contrast note does not name {p}")
        if re.search(r"\bnbsp\b", body) or "\t" in body:
            err(f"{cid}: stray markup")

for cluster, people in alts_by_cluster.items():
    if len(people) > 1:
        err(f"{cluster}: alt texts switch person word ({', '.join(sorted(people))})")

# Cluster frames: one fixed picture with a single "Only ..." change.
for b in BANDS:
    text = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    for cl, frame in re.findall(r'<section class="cluster" data-cluster="([^"]+)".*?<p class="frame"><strong>Fixed frame.</strong> (.*?)</p>', text, re.S):
        if cl in SINCE_B2 and not 25 <= len(frame.split("Only ")[0].split()) <= 45:
            err(f"{cl}: frame is {len(frame.split('Only ')[0].split())} words before the Only sentence (25-45)")
        if "Only " not in frame:
            err(f"{cl}: frame does not name the one thing that changes (\"Only ...\")")
        if COLOURS.search(frame):
            err(f"{cl}: colour or tint word in frame")
        if TEXTY.search(frame):
            err(f"{cl}: sign or label in frame, which invites text")
# Set sentences: an adverb that is also a preposition may not take a noun ("bovenin de kast" is "boven in de kast").
members_of = {c["id"]: [m["lemma"].lower() for m in c["members"]] for b in BANDS for c in sel.get(b, [])}
for b in BANDS:
    text = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    for cl, zin in re.findall(r'<section class="cluster" data-cluster="([^"]+)".*?<p class="zin">(.*?)<span', text, re.S):
        for lem in members_of.get(cl, []):
            if lem in PREP_LIKE and re.search(rf"\b{re.escape(lem)} {PREP_FOLLOW}\b", zin.lower()):
                err(f"{cl}: set sentence uses {lem} as a preposition")

# Cross-family duplicates: a drawn lemma may not be a card id or chunk in another family.
for fam in OTHER:
    taken = set()
    for f in glob.glob(os.path.join(ROOT, "Docs", fam, "*.html")):
        t = open(f, encoding="utf-8").read()
        taken |= set(re.findall(r'data-id="([^"]+)"', t))
        taken |= {x.strip().lower() for x in re.findall(r'<h3 class="chunk">(.*?)</h3>', t)}
    for cid, lem in drawn_lemmas.items():
        for key in {cid, lem}:
            if key in taken:
                if key in RULED:
                    warnings.append(f"{cid}: also in {fam} ({RULED[key]})")
                else:
                    err(f"{cid}: {key} is also a card in {fam}; skip it as a duplicate or record a ruling")
    for word, here in TAKEN_HERE.items():
        if word in taken:
            err(f"{fam} cards {word}, which Bijwoorden draws as {here}")
    # Cards in other families that borrow a frame from here must point at a drawn card.
    for f in glob.glob(os.path.join(ROOT, "Docs", fam, "*.html")):
        for other, ref in re.findall(r'data-id="([^"]+)"[^>]*data-xref="bijwoorden:([^"]+)"', open(f, encoding="utf-8").read()):
            if ref not in drawn_lemmas:
                err(f"{fam}:{other} cross-references bijwoorden:{ref}, which is not drawn here")

index = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
# A SKIP reason "duplicate of family:id" must point at a card that exists.
for cid, fam, other in re.findall(r"<li><code>([^<]+)</code> \([^)]*\): duplicate of ([\w-]+):([\w-]+)", index):
    pages = glob.glob(os.path.join(ROOT, "Docs", fam, "*.html"))
    if not pages:
        err(f"{cid}: duplicate of unknown family {fam}")
    elif not any(f'data-id="{other}"' in open(p, encoding="utf-8").read() for p in pages):
        err(f"{cid}: duplicate of {fam}:{other}, but that card does not exist")
# The dropped-candidate table: a "duplicate of family:id" must exist, and no candidate may be drawn here.
dropped = re.search(r"Reason left out</th></tr></thead><tbody>(.*?)</tbody>", index, re.S)
if not dropped:
    err("overview: dropped-candidate table missing")
else:
    for fam, other in re.findall(r"duplicate of ([\w-]+):([\w-]+)", dropped.group(1)) + re.findall(r"and ([\w-]+):([\w-]+)", dropped.group(1)):
        pages = glob.glob(os.path.join(ROOT, "Docs", fam, "*.html"))
        if not any(f'data-id="{other}"' in open(p, encoding="utf-8").read() for p in pages):
            err(f"dropped table: {fam}:{other} does not exist")
    for cell in re.findall(r"<tr><td><em>(.*?)</em></td>", dropped.group(1)):
        for w in [x.strip().lower() for x in cell.split(",")]:
            if w in drawn_lemmas.values() or w in drawn_lemmas:
                err(f"dropped table lists {w}, which is drawn here")
# No B2 band: no b2 page, no selection band outside BANDS, and every local link on the pages resolves.
if os.path.exists(os.path.join(OUT, "b2.html")):
    err("Docs/bijwoorden/b2.html exists, but the family has no B2 band")
for b in sel:
    if b not in BANDS:
        err(f"selection.json has band {b}, which has no page")
for f in glob.glob(os.path.join(OUT, "*.html")):
    for href in re.findall(r'href="([^"#:]+\.html)', open(f, encoding="utf-8").read()):
        if not os.path.exists(os.path.normpath(os.path.join(OUT, href))):
            err(f"{os.path.basename(f)}: dangling link {href}")
# Every OVERRIDE entry in select.py (including the EVERYDAY promotions merged into it) is documented
# on the overview, and nothing else is.
import importlib.util
_spec = importlib.util.spec_from_file_location("bw_select", os.path.join(TMP, "select.py"))
_sel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sel)
override = set(_sel.OVERRIDE)
documented = set(re.findall(r"<tr><td><em>([\w-]+)</em></td><td>(?:A0|A1|A2|B1|B2)</td>", index))
if override != documented:
    err(f"OVERRIDE and overview disagree: code only {sorted(override - documented)}, page only {sorted(documented - override)}")
# Band by rank: a set sits in the band of its best-ranked member unless OVERRIDE places it, and an
# OVERRIDE that only repeats the rank band is an error (it hides nothing and needs no reason).
for b in BANDS:
    for c in sel.get(b, []):
        rs = [_sel.fr[m["lemma"]] for m in c["members"] if m["lemma"] in _sel.fr]
        rank_band = _sel.band(min(rs)) if rs else None
        if c["id"] in _sel.OVERRIDE:
            if _sel.OVERRIDE[c["id"]] != b:
                err(f"{c['id']}: on band {b} but OVERRIDE says {_sel.OVERRIDE[c['id']]}")
            if rank_band == _sel.OVERRIDE[c["id"]]:
                err(f"{c['id']}: OVERRIDE repeats the rank band {rank_band}")
            if not _sel.REASON.get(c["id"], "").strip() or _sel.REASON[c["id"]] not in index.replace("&#x27;", "'"):
                err(f"{c['id']}: OVERRIDE reason missing from the overview")
        elif rank_band != b:
            err(f"{c['id']}: rank band {rank_band} but placed in {b}")
# Everyday promotions: the printed reason is checked fact by fact against the lexicon files
# (model: check-zelfstandige-naamwoorden-cards.py), the band is A2 at the highest and below the
# rank band, every member is drawn (partners move together), and the note states no lexicon fact.
import csv
import html as _html
LEXROW = {}
for r in csv.DictReader(open(os.path.join(ROOT, "tools", "lexicon", "woorden.tsv"), encoding="utf-8"), delimiter="\t"):
    LEXROW.setdefault(r["nl"], r)
FREQ = {}
for r in csv.DictReader(open(os.path.join(ROOT, "tools", "lexicon", "woorden-frequentie.tsv"), encoding="utf-8"), delimiter="\t"):
    FREQ[r["nl"]] = int(r["rang"])
FACT = re.compile(r"^(?P<lem>.+?) niveau (?P<niv>\S+)(?:, top2000 (?P<top>\S+))?, herkomst (?P<h>\S+), (?:rank (?P<r>\d+)|(?P<nr>no usable rank))$")
ABSENT = re.compile(r"^(?P<lem>.+?) not in woorden\.tsv$")
NOTE_BANNED = re.compile(r"(?i)coursebook|bijlage|top.?2000|niveau|herkomst|\brank|woorden|lexicon list|\d")
ov_html = {k: (bb, _html.unescape(t)) for k, bb, t in re.findall(
    r"<tr><td><em>([\w-]+)</em></td><td>([AB][0-2])</td><td>(.*?)</td></tr>", index)}
by_id = {c["id"]: (b, c) for b in BANDS for c in sel.get(b, [])}
for cid, (target, _note) in getattr(_sel, "EVERYDAY", {}).items():
    if cid not in by_id:
        err(f"{cid}: EVERYDAY set not in selection.json")
        continue
    b, c = by_id[cid]
    if b != target or BANDS.index(b) > BANDS.index("a2"):
        err(f"{cid}: everyday promotion sits in {b}; it must be its target {target}, A2 at the highest")
    rs = [_sel.fr[m["lemma"]] for m in c["members"] if m["lemma"] in _sel.fr]
    if rs and BANDS.index(_sel.band(min(rs))) <= BANDS.index(b):
        err(f"{cid}: rank already gives {_sel.band(min(rs))}; an everyday promotion must move the set down")
    for m in c["members"]:
        if m["id"] not in ids_seen:
            err(f"{cid}: member {m['id']} is not drawn; a promoted set moves with all its partners")
    if cid not in ov_html:
        err(f"{cid}: everyday promotion not on the overview")
        continue
    ob, txt = ov_html[cid]
    if ob != b.upper():
        err(f"{cid}: overview says {ob}, selection says {b.upper()}")
    mm = re.match(r"^Lexicon: (.*?)\. Basis: (.*?)\. Note: (.*)\.$", txt)
    if not mm:
        err(f"{cid}: reason is not 'Lexicon: ... Basis: ... Note: ...': {txt}")
        continue
    facts, basis, note = mm.groups()
    cited, qual = [], []
    for f in facts.split("; "):
        fa, fm = ABSENT.match(f), FACT.match(f)
        if fa:
            if fa["lem"] in LEXROW:
                err(f"{cid}: says {fa['lem']} is not in woorden.tsv, but it is")
            if fa["lem"] in FREQ:
                err(f"{cid}: says {fa['lem']} is not in woorden.tsv, but it ranks {FREQ[fa['lem']]}")
            cited.append(fa["lem"])
            continue
        if not fm:
            err(f"{cid}: unparseable lexicon fact '{f}'")
            continue
        lem, row = fm["lem"], LEXROW.get(fm["lem"])
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
        if fm["r"] and FREQ.get(lem) != int(fm["r"]):
            err(f"{cid}: says {lem} rank {fm['r']}, woorden-frequentie.tsv says {FREQ.get(lem)}")
        if fm["nr"] and lem in FREQ:
            err(f"{cid}: says {lem} has no usable rank, but it ranks {FREQ[lem]}")
        if ({row["niveau"]} | set(row["herkomst"].split(";"))) & _sel.COURSEBOOK_FOR[b]:
            qual.append(lem)
    want = [m["lemma"] for m in c["members"]]
    if sorted(cited) != sorted(want):
        err(f"{cid}: reason cites {cited}, the set's members are {want}")
    if basis == "judgment, not lexicon data":
        if qual:
            err(f"{cid}: basis judgment, but {qual} is taught at or below {b.upper()}; say coursebook")
    elif basis != f"coursebook ({', '.join(qual)})" or not qual:
        err(f"{cid}: basis '{basis}', but the members taught at or below {b.upper()} are {qual or 'none'}")
    if NOTE_BANNED.search(note):
        err(f"{cid}: note states a lexicon fact outside the checked Lexicon part: '{note}'")
# Band sizes on the overview table agree with the band pages.
for b in BANDS:
    t = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    ns, nc = len(re.findall(r'<section class="cluster"', t)), len(re.findall(r'class="kaart"', t))
    if not re.search(rf'<td><a href="{b}.html">{b.upper()}</a></td><td class="n">{ns}</td><td class="n">{nc}</td>', index):
        err(f"overview: {b.upper()} row does not say {ns} sets, {nc} cards")
    if not re.search(rf"<span>{ns} contrast sets</span><span>{nc} adverbs</span>", t):
        err(f"{b}.html: summary does not say {ns} sets, {nc} adverbs")
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
    print("  warning: " + w)
for e in errors:
    print("  " + e)
sys.exit(1 if errors else 0)
