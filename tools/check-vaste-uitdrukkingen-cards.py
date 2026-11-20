#!/usr/bin/env python3
"""Assert the fixed-expression (vaste uitdrukkingen) card pages are consistent with selection.json and the scene TSVs.

Beyond structure it tests the classes of error the 2026-11-20 review found:
- alt text naming the chunk, a form of it (any article or possessive in between), its partner,
  or the stem of a content word that only this member (or a partner) has;
- register and literal flags outside the allowed values, and 's-/met zijn-chunks flagged spoken;
- scene wording that invites text in the art (arrows, bubbles, signs, unqualified boards/screens/books);
- cross-family duplicates: a card id that Bijwoorden draws, a chunk that Voorzetselpaden cards,
  an example sentence that a Voorzetselpaden page already uses (articles ignored);
- cross-references (data-xref) that do not resolve, and left-out chunks that are still drawn.
Added for the B1/B2 expansion (20 November 2026): the B2 page; every OVERRIDE has a reason, is printed
on the overview, and does not repeat the band its ranks already give; Dutch example sentences of 5-9
words; alt stems matched after inflection is stripped and with a ge- prefix (hurken -> hurkt, gehurkt);
a card id that any other card family (Werkwoorden, Bijvoeglijke naamwoorden, Zelfstandige naamwoorden,
Bijwoorden, Scheidbare werkwoorden) already uses.
Added in the second fix pass (20 November 2026): a set frame that leans on another family's frame
instead of describing its own; a gloss that is an English idiom with another meaning (go round the bend);
an example sentence that repeats the chunk's preposition straight after it (voor anker voor de haven);
every native-check item on the overview names a card in the selection.
Added for the everyday rule (20 November 2026): an everyday promotion sits in A2 or lower, has no OVERRIDE
as well, is printed on the overview as judgment, and every niveau, top2000, herkomst and rank it cites for
each member's rank keys matches tools/lexicon/woorden.tsv and woorden-frequentie.tsv."""
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "tools", "_vu_tmp")
OUT = os.path.join(ROOT, "Docs", "vaste-uitdrukkingen")
BANDS = ["a0", "a1", "a2", "b1", "b2"]
BANNED = re.compile(r"\b(windmill|clog|tulip|canal|cheese)s?\b", re.I)
COLOURS = re.compile(r"\b(red|blue|green|yellow|orange|pink|purple|brown|grey|gray)\b", re.I)
NL_COLOURS = re.compile(r"\b(rood|rode|blauw|blauwe|groen|groene|geel|gele|oranje|roze|paars|bruin|bruine|grijs|grijze)\b", re.I)
STOP = {"de", "het", "een", "zijn", "z'n", "haar", "mijn", "van", "je"}
# Function words: never banned from alt text on their own; their phrase with the noun is.
FUNC = STOP | {"'s", "aan", "op", "in", "uit", "onder", "met", "zonder", "te", "ter", "per", "om", "voor", "achter",
               "naar", "door", "tegen", "over", "bij", "naast", "mee", "plaats"}
DET = r"(?:de|het|een|zijn|z'n|haar|mijn|je|hun|onze|ons|deze|die|dat|dit)"
REGISTERS = {"neutral", "spoken", "formal"}
LITERAL = {"literal", "literal and figurative", "figurative"}
TEXT_CUES = re.compile(r"\b(arrows?|bubbles?|zzz|signs?|signpost|marker post|label|caption|price tag|written|writing)\b", re.I)
WRITABLE = re.compile(r"(?<!wooden )(?<!cutting )\b(board|blackboard|screen|book|exercise book|poster|page|newspaper)\b", re.I)
VZP = os.path.join(ROOT, "Docs", "voorzetselpaden")
BW = os.path.join(ROOT, "Docs", "bijwoorden")
errors = []
FAMILIES = r"(?:Bijwoorden|Werkwoorden|Voorzetselpaden|Bijvoeglijke naamwoorden|Zelfstandige naamwoorden|Scheidbare werkwoorden)"
# English glosses that are idioms with another meaning; the learner's dictionary would mislead.
BAD_GLOSS = re.compile(r"\b(round the bend|off one's rocker|over the moon|under the weather)\b", re.I)


def err(msg):
    errors.append(msg)




def phrase_re(chunk):
    """The chunk with any determiner allowed between its words, and its own determiners swappable."""
    toks = [t for t in re.findall(r"[\w'’]+", chunk.lower())]
    parts = []
    for t in toks:
        if t in ("de", "het", "een", "zijn", "z'n", "haar", "mijn", "je"):
            continue
        parts.append(re.escape(t))
    sep = r"(?:\s+" + DET + r")?\s+"
    body = sep.join(parts)
    return re.compile(r"(?<!\w)" + body + r"(?!\w)")


def content_words(chunk):
    return [t for t in re.findall(r"[\w'’]+", chunk.lower()) if t not in FUNC and len(t) > 2]


def stem(w):
    """Strip diminutive, plural and -en endings, then cut to five letters: knieën -> knie, wieltjes -> wiel."""
    for end in ("tjes", "jes", "tje", "je", "ën", "en", "s"):
        if w.endswith(end) and len(w) - len(end) >= 4:
            w = w[: -len(end)]
            break
    return w[:5] if len(w) > 5 else w


def norm(t):
    t = re.sub(r"[^\w\s']", " ", html.unescape(t).lower())
    return " ".join(w for w in t.split() if w not in ("de", "het", "een"))


def page_text(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"data:[^\"')\s]+", "", t)            # strip base64 images
    return t


sel = json.load(open(os.path.join(TMP, "selection.json"), encoding="utf-8"))
ids_expected = {m["id"]: (b, c["id"], c) for b in BANDS for c in sel.get(b, []) for m in c["members"]}
member = {m["id"]: m for b in BANDS for c in sel.get(b, []) for m in c["members"]}
cluster_of = {m["id"]: c for b in BANDS for c in sel.get(b, []) for m in c["members"]}

# Other families
vzp_pages = [page_text(p) for p in sorted(glob.glob(os.path.join(VZP, "*.html")))
             if not os.path.basename(p).startswith("matrix-")]
vzp_chunks = {html.unescape(x).strip().lower() for t in vzp_pages for x in re.findall(r'data-chunk="([^"]*)"', t)}
vzp_text = norm(" ".join(re.sub(r"<[^>]+>", " ", t) for t in vzp_pages))
bw_ids = {}
for p in glob.glob(os.path.join(BW, "*.html")):
    for x in re.findall(r'data-id="([^"]+)"', open(p, encoding="utf-8").read()):
        bw_ids[x] = os.path.basename(p)
FAMILY_IDS = {"bijwoorden": bw_ids}
other_ids = {}
for fam in ("werkwoorden", "bijvoeglijke-naamwoorden", "zelfstandige-naamwoorden", "bijwoorden", "scheidbare-werkwoorden"):
    for p in glob.glob(os.path.join(ROOT, "Docs", fam, "*.html")):
        for x in re.findall(r'data-id="([^"]+)"', open(p, encoding="utf-8").read()):
            other_ids.setdefault(x, fam)

left_out = []
with open(os.path.join(TMP, "left-out.tsv"), encoding="utf-8") as fh:
    next(fh)
    for line in fh:
        if line.strip():
            left_out.append(line.rstrip("\n").split("\t"))

ids_seen = {}
total = 0
for b in BANDS:
    text = open(os.path.join(OUT, b + ".html"), encoding="utf-8").read()
    for fm in re.finditer(r'<p class="frame">(.*?)</p>', text, re.S):
        if re.search(r"\b" + FAMILIES + r"\b[^.]*\bframe\b|\bframe\b[^.]*\bin " + FAMILIES + r"\b", fm.group(1)):
            err(f"{b}: a set frame leans on another family's frame instead of describing its own")
        if TEXT_CUES.search(re.sub(r"\bno arrows\b", "", fm.group(1))):
            err(f"{b}: a set frame invites text or arrows: {TEXT_CUES.search(fm.group(1)).group(0)}")
    for m in re.finditer(r'<article id="([^"]+)" class="kaart" data-id="([^"]+)" data-band="([^"]+)" '
                         r'data-kind="chunk" data-cluster="([^"]+)"([^>]*)>(.*?)</article>', text, re.S):
        cid, did, band, cluster, tail, body = m.groups()
        total += 1
        if cid != did:
            err(f"{cid}: id != data-id")
        if f"{cid}.png" not in body:
            err(f"{cid}: png name does not match the id")
        if band != b:
            err(f"{cid}: band {band} on page {b}")
        if cid in ids_seen:
            err(f"{cid}: duplicate card")
        ids_seen[cid] = cluster
        if cid not in ids_expected or ids_expected[cid][1] != cluster:
            err(f"{cid}: not in selection for cluster {cluster}")
        if cid in bw_ids:
            err(f"{cid}: Bijwoorden already draws this card ({bw_ids[cid]})")
        elif cid in other_ids:
            err(f"{cid}: {other_ids[cid]} already has a card with this id")
        xm = re.search(r'data-xref="([^"]*)"', tail)
        xref = xm.group(1) if xm else ""
        xref_id = ""
        if xref:
            fam, _, xref_id = xref.partition(":")
            if xref_id not in FAMILY_IDS.get(fam, {}):
                err(f"{cid}: cross-reference {xref} does not resolve")
        for cls in ("scene", "must", "avoid", "contrast-note", "voorbeeld-nl", "alt"):
            mm = re.search(rf'<dd class="{cls}"[^>]*>(.*?)</dd>', body, re.S)
            if not mm or not re.sub(r"<[^>]+>", "", mm.group(1)).strip():
                err(f"{cid}: empty {cls}")
        lemma = html.unescape(re.search(r'<h3 class="chunk" data-chunk="[^"]*">(.*?)</h3>', body).group(1)).lower()
        gl = re.search(r'<p class="gloss">(.*?)</p>', body, re.S)
        if gl and BAD_GLOSS.search(html.unescape(gl.group(1))):
            err(f"{cid}: gloss is an English idiom with another meaning ({BAD_GLOSS.search(html.unescape(gl.group(1))).group(0)})")
        if lemma in vzp_chunks:
            err(f"{cid}: Voorzetselpaden already cards the chunk '{lemma}'")
        scene = re.search(r'<dd class="scene">(.*?)</dd>', body, re.S)
        if scene:
            sc = html.unescape(scene.group(1))
            n = len(sc.split())
            if not 25 <= n <= 75:
                err(f"{cid}: scene is {n} words")
            if BANNED.search(sc):
                err(f"{cid}: souvenir imagery in scene")
            if COLOURS.search(sc):
                err(f"{cid}: colour word in scene")
            if TEXT_CUES.search(sc):
                err(f"{cid}: scene invites text or arrows ({TEXT_CUES.search(sc).group(0)})")
            for sent in re.split(r"(?<=[.;:])\s+", sc):
                if WRITABLE.search(sent) and "blank" not in sent.lower():
                    err(f"{cid}: '{WRITABLE.search(sent).group(0)}' in the scene is not stated to be blank")
        pm = re.search(r'data-partner="([^"]*)"', body)
        partners = pm.group(1).split() if pm else []
        alt = re.search(r'<dd class="alt">(.*?)</dd>', body, re.S)
        if alt:
            alt_t = html.unescape(alt.group(1)).lower()
            forms = [(lemma, phrase_re(lemma))] + [(member[p]["lemma"].lower(), phrase_re(member[p]["lemma"]))
                                                  for p in partners if p in member]
            if xref_id:
                forms.append((xref_id, phrase_re(xref_id)))
            for name, rx in forms:
                if rx.search(alt_t):
                    err(f"{cid}: alt text contains the chunk or a partner chunk ({name})")
            # Stems of content words that tell this member apart from its set.
            set_lemmas = [member[i]["lemma"] for i in [cid] + partners if i in member]
            for i in [cid] + partners:
                if i not in member:
                    continue
                own = set(content_words(member[i]["lemma"]))
                shared = set()
                for other in set_lemmas:
                    if other != member[i]["lemma"]:
                        shared |= set(content_words(other))
                for w in own - shared:
                    if re.search(r"(?<!\w)(?:ge)?" + re.escape(stem(w)), alt_t):
                        err(f"{cid}: alt text contains the stem '{stem(w)}' of {member[i]['lemma']}")
            if NL_COLOURS.search(alt_t):
                err(f"{cid}: colour word in alt")
        ex = re.search(r'<dd class="voorbeeld-nl">(.*?)<br>', body, re.S)
        if ex:
            ex_raw = html.unescape(ex.group(1))
            ex_t = ex_raw.lower()
            if not 5 <= len(ex_raw.split()) <= 9:
                err(f"{cid}: example sentence has {len(ex_raw.split())} words, not 5-9")
            first_w = lemma.split()[0]
            if first_w in FUNC and re.search(re.escape(lemma) + r"\s+(?:\S+\s+)?" + re.escape(first_w) + r"\b", ex_t):
                err(f"{cid}: example repeats '{first_w}' straight after the chunk")
            for w in re.findall(r"[\w']+", lemma):
                if w not in STOP and w not in ex_t:
                    err(f"{cid}: example sentence lacks '{w}'")
            if norm(ex_raw) and norm(ex_raw) in vzp_text:
                err(f"{cid}: example sentence repeats a Voorzetselpaden sentence ({ex_raw.strip()})")
        av = re.search(r'<dd class="avoid">(.*?)</dd>', body, re.S)
        if av:
            items = [x for x in av.group(1).split(";") if x.strip()]
            if not 3 <= len(items) <= 5:
                err(f"{cid}: avoid has {len(items)} items")
            first = re.search(r"\(([^)]*)\)", items[0])
            names = set()
            for p_ in partners:
                if p_ in member:
                    names |= {member[p_]["lemma"].lower(), p_, p_.replace("-", " ")}
            if xref_id:
                names |= {xref_id, xref_id.replace("-", " ")}
            got = html.unescape(first.group(1)).lower() if first else ""
            if (partners or xref_id) and got not in names:
                err(f"{cid}: first avoid item does not name a partner ({got})")
        fl = re.search(r'class="register">([^<]*)</span><span class="betekenis">([^<]*)</span>', body)
        if not fl:
            err(f"{cid}: register or literal flag missing")
        else:
            reg, lit = fl.groups()
            if reg not in REGISTERS:
                err(f"{cid}: register '{reg}' not in {sorted(REGISTERS)}")
            if lit not in LITERAL:
                err(f"{cid}: literal flag '{lit}'")
            if reg == "spoken" and (lemma.startswith("'s ") or lemma.startswith("met zijn ")):
                err(f"{cid}: '{lemma}' is standard written Dutch, not spoken")
        if not partners and not xref_id:
            err(f"{cid}: no contrast partner on page and no cross-reference (partner skipped?)")
        for p in partners + ([xref_id] if xref_id else []):
            if not re.search(rf"Pair with [^.]*\b{re.escape(p)}\b", body):
                err(f"{cid}: contrast note does not name {p}")
        if re.search(r"\bnbsp\b", body) or "\t" in body:
            err(f"{cid}: stray markup")

index = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
skipped = set(re.findall(r"<li><code>([^<]+)</code> \(", index))
listed_out = set(re.findall(r'<li class="weg"><code>([^<]+)</code>', index))
for i in ids_expected:
    if i not in ids_seen and i not in skipped:
        err(f"{i}: in selection, neither drawn nor skipped")
for row in left_out:
    if len(row) != 3 or not all(x.strip() for x in row):
        err(f"left-out.tsv: bad row {row}")
        continue
    i = row[0]
    if i in ids_expected:
        err(f"{i}: left out but still in clusters.txt")
    if i in ids_seen:
        err(f"{i}: left out but still drawn")
    if i not in listed_out:
        err(f"{i}: left out but not listed on the overview")
# Overrides: a reason each, printed on the overview, never repeating the band the ranks give.
for b in BANDS:
    for c in sel.get(b, []):
        if "override" not in c:
            continue
        if not c["override"].strip():
            err(f"{c['id']}: OVERRIDE without a reason")
        if c.get("rank_band") == c["band"]:
            err(f"{c['id']}: OVERRIDE to {c['band']} repeats the band its ranks give")
        if not re.search(rf"<li><code>{re.escape(c['id'])}</code> to {c['band'].upper()}: [^<]+</li>", index):
            err(f"{c['id']}: OVERRIDE reason not printed on the overview")
# Everyday promotions (decision of 20 November 2026): A2 at the highest, printed on the overview as
# judgment, and every lexicon fact in the reason re-read from woorden.tsv and woorden-frequentie.tsv.
import csv
LEXROW = {}
for r in csv.DictReader(open(os.path.join(ROOT, "tools", "lexicon", "woorden.tsv"), encoding="utf-8"), delimiter="\t"):
    LEXROW.setdefault(r["nl"], r)
FREQ = {r["nl"]: int(r["rang"]) for r in csv.DictReader(
    open(os.path.join(ROOT, "tools", "lexicon", "woorden-frequentie.tsv"), encoding="utf-8"), delimiter="\t")}
FACT = re.compile(r"^(?P<chunk>[^:]+): (?P<lem>.+?) (?:not in woorden\.tsv|niveau (?P<niv>\S+)(?:, top2000 (?P<top>\S+))?"
                  r", herkomst (?P<h>\S+), (?:rank (?P<r>\d+)|(?P<nr>no rank)))$")
NOTE_BANNED = re.compile(r"(?i)coursebook|bijlage|top.?2000|niveau|herkomst|\brank|woorden|lexicon|\d")
lexkey = lambda k: re.sub(r"^(.+?)\((\w+)\)$", r"\1 (\2)", k)
printed = {m.group(1): (m.group(2), html.unescape(m.group(3))) for m in re.finditer(
    r'<li class="alledaags"><code>([^<]+)</code> to ([AB][0-2]): (.*?)</li>', index)}
for b in BANDS:
    for c in sel.get(b, []):
        if not c.get("everyday"):
            continue
        cid, txt = c["id"], c["everyday"]
        if b not in ("a0", "a1", "a2"):
            err(f"{cid}: everyday promotion sits in {b.upper()}, above A2")
        if "override" in c:
            err(f"{cid}: has both an OVERRIDE and an everyday promotion")
        if printed.get(cid) != (b.upper(), txt):
            err(f"{cid}: everyday reason not printed on the overview as in selection.json")
        m = re.match(r"^Lexicon: (.*?)\. Basis: judgment, not lexicon data\. Note: (.+)\.$", txt)
        if not m:
            err(f"{cid}: everyday reason is not 'Lexicon: ... Basis: judgment, not lexicon data. Note: ...': {txt}")
            continue
        facts, note = m.groups()
        if NOTE_BANNED.search(note):
            err(f"{cid}: everyday note states a lexicon fact outside the checked Lexicon part: '{note}'")
        want = sorted((x["lemma"], lexkey(k)) for x in c["members"] for k in x["keys"])
        cited = []
        for f in facts.split("; "):
            fm = FACT.match(f)
            if not fm:
                err(f"{cid}: unparseable lexicon fact '{f}'")
                continue
            lem = fm["lem"]
            cited.append((fm["chunk"], lem))
            row = LEXROW.get(lem)
            if fm["niv"] is None:
                if row:
                    err(f"{cid}: says {lem} is not in woorden.tsv, but it is")
                continue
            if not row:
                err(f"{cid}: cites {lem}, which is not a woorden.tsv row")
                continue
            if fm["niv"] != (row["niveau"] or "none"):
                err(f"{cid}: says {lem} niveau {fm['niv']}, woorden.tsv says {row['niveau'] or 'none'}")
            if (fm["top"] or "") != row["top2000"]:
                err(f"{cid}: says {lem} top2000 {fm['top'] or 'empty'}, woorden.tsv says {row['top2000'] or 'empty'}")
            if fm["h"] != row["herkomst"]:
                err(f"{cid}: says {lem} herkomst {fm['h']}, woorden.tsv says {row['herkomst']}")
            if fm["r"] and FREQ.get(lem) != int(fm["r"]):
                err(f"{cid}: says {lem} rank {fm['r']}, woorden-frequentie.tsv says {FREQ.get(lem)}")
            if fm["nr"] and lem in FREQ:
                err(f"{cid}: says {lem} has no rank, but woorden-frequentie.tsv ranks it {FREQ[lem]}")
        if sorted(cited) != want:
            err(f"{cid}: everyday reason cites {sorted(cited)}, the set's rank keys are {want}")
if len(printed) != sum(1 for b in BANDS for c in sel.get(b, []) if c.get("everyday")):
    err("overview prints an everyday promotion that is not in selection.json")
for i in re.findall(r'<li class="native"><code>([^<]+)</code>', index):
    if i not in ids_expected:
        err(f"native-check item {i} is not a card in the selection")
for b in BANDS:
    if f'href="{b}.html"' not in index:
        err(f"overview has no link to {b}.html")
if "holds no chunk in this list" in index:
    err("index still claims Voorzetselpaden holds no chunk in this list")

nums = [int(x) for b in BANDS for x in re.findall(r'class="framenummer" title="Frame (\d+)"',
        open(os.path.join(OUT, b + ".html"), encoding="utf-8").read())]
if nums != list(range(1, len(nums) + 1)):
    err("frame numbers are not 1..N in order")

print(f"cards {total}  skipped {len(skipped)}  left out {len(listed_out)}  errors {len(errors)}")
for e in errors:
    print("  " + e)
sys.exit(1 if errors else 0)
