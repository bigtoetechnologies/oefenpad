#!/usr/bin/env python3
"""Read and write the Voorzetselpaden band pages.

The pages under Docs/voorzetselpaden/ are the source of truth. Nothing is
generated from a side file: this tool parses the cards out of the HTML and
writes changes back into the same HTML, leaving every other byte alone.

    python3 tools/prepositions-pages.py read  [--out records.json]
    python3 tools/prepositions-pages.py patch fixes.json [--dry-run]
    python3 tools/prepositions-pages.py check

`patch` takes {"fixes": [{"id": ..., "scene": ..., ...}]} and edits the card
with that data-id, in place, on whichever page holds it. Fields it does not
mention are untouched. A field the card does not yet have is inserted in the
canonical order below. """
import argparse
import html as H
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "Docs/voorzetselpaden"

# dt label -> dd class, in the order they must appear on a card
FIELDS = [
    ("Scene", "scene"),
    ("Must read", "must"),
    ("Avoid", "avoid"),
    ("Pair / note", "note"),
    ("Tests", "tests"),
    ("Example", "voorbeeld-nl"),
    ("Build", "bouw"),
    ("Check question", "controlevraag"),
    ("Contrast", "contrast"),
    ("Pronominal adverb", "pronominaal"),
    ("Alt text", "alt"),
    ("Verdict", "verdict_why"),
]
# fields whose markup is more than escaped text
RICH = {"voorbeeld-nl", "bouw", "controlevraag", "pronominaal"}
LABEL = {cls: lab for lab, cls in FIELDS}
ORDER = [cls for _, cls in FIELDS]

CARD = re.compile(r'<article class="kaart[^"]*"[^>]*data-id="(?P<id>[^"]+)"[^>]*>'
                  r'(?P<body>.*?)</article>', re.S)
BADGES = {"needs_redraw": ('<span class="redraw">redraw</span>', "redraw")}

# the commissioning verdict: is this card worth paying an artist for
VERDICTS = {
    "keep": ('<span class="v-keep">keep</span>', "v-keep"),
    "weak": ('<span class="v-weak">weak</span>', "v-weak"),
    "drop": ('<span class="v-drop">drop</span>', "v-drop"),
}


def pages():
    return sorted(p for p in PAGES.glob("*.html")
                  if p.name != "index.html" and not p.name.startswith("matrix-"))


def text_of(fragment):
    return H.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def read_cards(path):
    src = path.read_text(encoding="utf-8")
    out = {}
    for m in CARD.finditer(src):
        body = m.group("body")
        rec = {"id": m.group("id"), "page": path.name}
        head = src[m.start():m.start() + (body and 0) + 400]
        for attr in ("band", "kind", "row", "status", "severity", "batch"):
            a = re.search(r'data-%s="([^"]*)"' % attr, head)
            if a:
                rec[attr] = a.group(1)
        ch = re.search(r'<h3 class="chunk">(.*?)</h3>', body, re.S)
        gl = re.search(r'<p class="gloss">(.*?)</p>', body, re.S)
        rec["chunk"] = text_of(ch.group(1)) if ch else ""
        rec["gloss"] = text_of(gl.group(1)) if gl else ""
        for cls in ORDER:
            d = re.search(r'<dd class="%s">(.*?)</dd>' % cls, body, re.S)
            if d:
                rec[cls] = text_of(d.group(1))
        rec["needs_redraw"] = 'class="redraw"' in body
        vm = re.search(r'data-verdict="([a-z]+)"', src[m.start():m.start() + 400])
        if vm:
            rec["verdict"] = vm.group(1)
        out[rec["id"]] = rec
    return out


def esc(v):
    return H.escape(str(v), quote=True)


def render(cls, value):
    """The inner HTML for one field."""
    if cls == "voorbeeld-nl":
        nl = esc(value.get("nl", "")) if isinstance(value, dict) else esc(value)
        en = esc(value.get("en", "")) if isinstance(value, dict) else ""
        return nl + (f'<br><span class="voorbeeld-en">{en}</span>' if en else "")
    if cls == "pronominaal":
        nl = esc(value.get("nl", "")) if isinstance(value, dict) else esc(value)
        en = esc(value.get("en", "")) if isinstance(value, dict) else ""
        return nl + (f'<br><span class="pronominaal-en">{en}</span>' if en else "")
    if cls == "controlevraag":
        if isinstance(value, dict):
            q = esc(value.get("question", ""))
            a = "Ja" if value.get("answer") else "Nee"
            return f'{q} <strong class="antwoord">{a}</strong>'
        return esc(value)
    return esc(value)


def set_field(body, cls, value):
    """Replace a dd, or insert the dt/dd pair in canonical order.

    `bouw` may be a list: the learner gets one sentence per variant, so each
    becomes its own dt/dd pair, as the shipped cards have.
    """
    if cls == "bouw" and isinstance(value, (list, tuple)):
        body = re.sub(r'<dt>Build</dt><dd class="bouw">.*?</dd>', "", body, flags=re.S)
        block = "".join(f'<dt>Build</dt><dd class="bouw">{esc(v)}</dd>' for v in value)
        return insert_block(body, "bouw", block)

    pat = re.compile(r'(<dd class="%s">).*?(</dd>)' % cls, re.S)
    if pat.search(body):
        return pat.sub(lambda m: m.group(1) + render(cls, value) + m.group(2),
                       body, count=1)
    block = f'<dt>{LABEL[cls]}</dt><dd class="{cls}">{render(cls, value)}</dd>'
    return insert_block(body, cls, block)


def insert_block(body, cls, block):
    after = ORDER[:ORDER.index(cls)]
    for prev in reversed(after):
        ms = list(re.finditer(r'<dd class="%s">.*?</dd>' % prev, body, re.S))
        if ms:
            end = ms[-1].end()          # after the LAST one: Build repeats
            return body[:end] + block + body[end:]
    m = re.search(r"<dl>", body)
    if m:
        return body[:m.end()] + block + body[m.end():]
    return body.replace("</dl>", block + "</dl>", 1)


def set_badge(body, key):
    markup, cls = BADGES[key]
    if f'class="{cls}"' in body:
        return body
    m = re.search(r'<p class="vlaggen">(.*?)</p>', body, re.S)
    if not m:
        return body
    return body[:m.end() - 4] + markup + body[m.end() - 4:]


def patch(fixes, dry=False):
    want = {}
    for f in fixes:
        want.setdefault(f["id"], {}).update(f)
    touched, changed, notfound = {}, 0, list(want)

    for path in pages():
        src = path.read_text(encoding="utf-8")
        hits = []

        def repl(m):
            nonlocal changed
            cid = m.group("id")
            fix = want.get(cid)
            if not fix:
                return m.group(0)
            if cid in notfound:
                notfound.remove(cid)
            whole, body = m.group(0), m.group("body")
            new = body
            for cls in ORDER:
                if cls not in fix:
                    continue
                val = fix[cls]
                if isinstance(val, (dict, list, tuple)):
                    if not val:
                        continue
                else:
                    val = str(val).strip()
                    if not val:
                        continue
                new = set_field(new, cls, val)
            if "chunk" in fix and str(fix["chunk"]).strip():
                new = re.sub(r'(<h3 class="chunk">).*?(</h3>)',
                             lambda x: x.group(1) + esc(fix["chunk"].strip()) + x.group(2),
                             new, count=1, flags=re.S)
            if "gloss" in fix and str(fix["gloss"]).strip():
                new = re.sub(r'(<p class="gloss">).*?(</p>)',
                             lambda x: x.group(1) + esc(fix["gloss"].strip()) + x.group(2),
                             new, count=1, flags=re.S)
            if fix.get("needs_redraw"):
                new = set_badge(new, "needs_redraw")
            v = str(fix.get("verdict", "")).lower()
            if v in VERDICTS:
                markup, cls = VERDICTS[v]
                for _, oc in VERDICTS.values():
                    new = re.sub(r'<span class="%s">[^<]*</span>' % oc, "", new)
                fm = re.search(r'<p class="vlaggen">(.*?)</p>', new, re.S)
                if fm:
                    new = new[:fm.end() - 4] + markup + new[fm.end() - 4:]
                why = str(fix.get("verdict_why", "")).strip()
                if why:
                    new = set_field(new, "verdict_why", why)
            if v in VERDICTS:
                head = whole[:whole.index(">") + 1]
                nh = re.sub(r'\s*data-verdict="[a-z]*"', "", head)
                nh = nh[:-1] + f' data-verdict="{v}">'
                whole = nh + whole[len(head):]
            if new == body:
                return whole
            changed += 1
            hits.append(cid)
            return whole.replace(body, new, 1)

        out = CARD.sub(repl, src)
        if out != src and not dry:
            path.write_text(out, encoding="utf-8")
        if hits:
            touched[path.name] = hits
    return touched, changed, notfound


# --------------------------------------------------------------------------
# check: content rules that a script can verify
# --------------------------------------------------------------------------
BANDS = ["a0", "a1", "a2", "a2-pairs", "a2-plus", "b1", "b1-plus", "b2"]
GAME = ROOT / "server/Oefenpad.Resources/Games/Data/prepositions.json"
VERB_FORMS = ROOT / "tools/lexicon/werkwoorden-vormen.tsv"
B64 = re.compile(r"data:image/[a-z]+;base64,[A-Za-z0-9+/=]+")
PREPS = {"aan", "achter", "bij", "binnen", "boven", "buiten", "door", "in", "langs",
         "met", "na", "naar", "naast", "om", "onder", "op", "over", "per", "rond",
         "sinds", "te", "tegen", "ten", "tot", "tussen", "uit", "van", "vanaf",
         "voor", "zonder"}
# words of a chunk label that say nothing about the picture
CHUNK_FILLER = PREPS | {"zijn", "hebben", "zich", "er", "eraan", "het", "de", "een",
                        "dat", "maken", "worden", "nog", "is"}
SEPARABLE = ("aan", "af", "door", "in", "mee", "na", "op", "terug", "toe", "uit", "weg")
# Dutch the reviews have found wrong; any live (non-drop) card using it fails
BAD_DUTCH = [
    (re.compile(r"\bdurf\w*\b(?:\s+\w+)*?\s+om\b(?:\s+\w+)*?\s+te\b", re.I),
     "durven takes te without om"),
    (re.compile(r"(?<!\bte )\blijd(?:t|en|)\s+van\b", re.I),
     "lijden van is not standard; use te lijden hebben van"),
    (re.compile(r"\bknieen\b", re.I), "spelling: knieën"),
    (re.compile(r"\bnieuwe haar\b", re.I), "not idiomatic: nieuwe kapsel or mijn haar"),
]
SOUVENIR = re.compile(r"\b(\w*kaas\w*|\w*molen\w*|klomp\w*|tulp\w*|gracht\w*|woonboot\w*|"
                      r"cheese\w*|windmills?|clogs?|tulips?|canals?|houseboat\w*)\b", re.I)
WORD = re.compile(r"[a-zà-ÿ']+", re.I)


def _irregular():
    out = {}
    if VERB_FORMS.exists():
        for line in VERB_FORMS.read_text(encoding="utf-8").splitlines()[1:]:
            col = line.split("\t")
            if len(col) >= 5:
                out[col[0]] = {col[1], col[2], col[4]}
    return out


IRREGULAR = _irregular()


def _stem(inf):
    """The Dutch present-tense stem: vragen -> vraag, letten -> let, zien -> zie."""
    if re.search(r"(?<![aeou])(ie|oe|ee)n$", inf):
        return inf[:-1]
    if re.search(r"aan$", inf):
        return inf[:-2]
    s = inf[:-2]
    if len(s) >= 2 and s[-1] == s[-2] and s[-1] not in "aeiou":
        s = s[:-1]
    elif (len(s) >= 3 and s[-1] not in "aeiouj" and s[-2] in "aou"
          and s[-3] not in "aeiou"):
        s = s[:-1] + s[-2] + s[-1]              # open syllable: vragen -> vraag
    elif (len(s) >= 3 and s[-1] not in "aeiouj" and s[-2] == "e"
          and s[-3] not in "aeiou" and len(s) <= 4):
        s = s[:-1] + "e" + s[-1]                # leven -> leef, geven -> geef
    return re.sub(r"z$", "s", re.sub(r"v$", "f", s))


def word_forms(word):
    """Every form of one chunk word a learner could recognise in an alt."""
    word = word.lower()
    forms = {word}
    if word.endswith(("en", "aan")) and len(word) > 3:
        st = _stem(word)
        if word.endswith("aan"):                # gaan -> ga, gaat; past is irregular
            forms |= {st, word[:-1] + "t"}
        else:
            forms |= {st, st + "t", st + "te", st + "de", st + "ten", st + "den",
                      "ge" + st + "d", "ge" + st + "t", word[:-1]}
        forms |= IRREGULAR.get(word, set())
        for pre in SEPARABLE:
            core = word[len(pre):]
            if word.startswith(pre) and len(core) > 4:
                core_forms = word_forms(core)
                forms |= core_forms
                forms |= {pre + f for f in core_forms if f.startswith("ge")}
    elif len(word) > 2:
        forms |= {word + "e", word + "er"}
        if word.endswith("s"):
            forms.add(word[:-1] + "ze")         # boos -> boze
    return {f for f in forms if len(f) > 2}


def chunk_forms(chunk):
    words = [w.lower() for w in WORD.findall(chunk)]
    out = set()
    for w in words:
        if w not in CHUNK_FILLER:
            out |= word_forms(w)
    return out


def _cards_with_context():
    """Every card in band order with its band, cluster, group and raw markup."""
    cards = []
    for band in BANDS:
        path = PAGES / f"{band}.html"
        src = B64.sub("data:B64", path.read_text(encoding="utf-8"))
        clusters = [(m.start(), m.group(1)) for m in
                    re.finditer(r'<section class="cluster" data-stem="([^"]*)"', src)]
        groups = list(re.finditer(r'<div class="chunkgroep" data-chunk="([^"]*)" '
                                  r'data-examples="(\d+)">(?:<h3>(.*?)</h3>)?', src))
        for gi, g in enumerate(groups):
            stop = groups[gi + 1].start() if gi + 1 < len(groups) else len(src)
            cl = ""
            for pos, stem in clusters:
                if pos < g.start():
                    cl = f"{band}:{pos}:{stem}"
            body = src[g.end():stop]
            arts = list(re.finditer(r'<article class="[^"]*\bkaart\b[^"]*"[^>]*>.*?</article>',
                                    body, re.S))
            for m in arts:
                t = m.group(0)
                head = t[:t.index(">") + 1]

                def dd(cls):
                    d = re.search(r'<dd class="%s">(.*?)</dd>' % cls, t, re.S)
                    return d.group(1) if d else ""
                ex = dd("voorbeeld-nl").split("<br")[0]
                img = re.search(r'<img class="beeld"[^>]*alt="([^"]*)"', t)
                num = re.search(r'title="Frame (\d+)"', t)
                foot = re.search(r'<p class="id">([^<·]*)', t)
                v = re.search(r'data-verdict="([a-z]+)"', head)
                cards.append({
                    "band": band, "cluster": cl, "group": H.unescape(g.group(1)),
                    "group_h3": text_of(g.group(3) or ""),
                    "examples_attr": int(g.group(2)), "group_size": len(arts),
                    "id": re.search(r'data-id="([^"]+)"', head).group(1),
                    "n": int(num.group(1)) if num else None,
                    "h3": text_of((re.search(r'<h3 class="chunk">(.*?)</h3>', t, re.S)
                                   or re.match("()", "")).group(1)),
                    "example": text_of(ex),
                    "builds": [text_of(b) for b in
                               re.findall(r'<dd class="bouw">(.*?)</dd>', t, re.S)],
                    "question": text_of(dd("controlevraag")),
                    "scene": text_of(dd("scene")), "note": text_of(dd("note")),
                    "alt": text_of(dd("alt")), "contrast": text_of(dd("contrast")),
                    "drawn": img is not None,
                    "img_alt": H.unescape(img.group(1)) if img else None,
                    "status": (re.search(r'data-status="([^"]*)"', head) or
                               re.match("()", "")).group(1),
                    "verdict": v.group(1) if v else "",
                    "redraw": 'class="redraw"' in t,
                    "flag_drawn": 'class="getekend"' in t,
                    "flag_game": 'class="inspel"' in t,
                    "foot": (foot.group(1).strip() if foot else ""),
                })
    return cards


def _partners(cards):
    """chunk -> the chunks it is contrasted with, from the pages and the game."""
    by_cluster, slug_to_chunk, id_to_chunk = {}, {}, {}
    for c in cards:
        by_cluster.setdefault(c["cluster"], set()).add(c["group"])
        slug_to_chunk[c["group"].replace(" ", "-")] = c["group"]
        id_to_chunk[c["id"]] = c["group"]
    out = {}
    for c in cards:
        p = out.setdefault(c["group"], set())
        p |= by_cluster.get(c["cluster"], set())
        for v in (c["contrast"],):
            if v:
                p.add(slug_to_chunk.get(v) or id_to_chunk.get(v) or "")
        for m in re.findall(r"[Cc]ontrast with ([a-zë ]+?)[:;,.]", c["note"]):
            if m.strip() in slug_to_chunk.values():
                p.add(m.strip())
    if GAME.exists():
        game = json.loads(GAME.read_text(encoding="utf-8"))
        frames = {f["id"]: f for f in game.get("frames", [])}
        for f in frames.values():
            other = frames.get(f.get("contrast") or "")
            if other:
                out.setdefault(f["frame"], set()).add(other["frame"])
                out.setdefault(other["frame"], set()).add(f["frame"])
    for k, vs in list(out.items()):           # a contrast runs both ways
        for v in vs:
            out.setdefault(v, set()).add(k)
    for k in out:
        out[k].discard(k)
        out[k].discard("")
    return out


def _bare(s):
    return " ".join(WORD.findall(s.lower()))


def audit():
    """Every rule the reviews found broken, as errors (drawn cards and
    totals) or warnings (undrawn cards, whose art is not yet commissioned)."""
    cards = _cards_with_context()
    partners = _partners(cards)
    err, warn = [], []

    def flag(c, msg, hard):
        (err if hard else warn).append(f"#{c['n']} {c['id']} ({c['band']}): {msg}")

    # ids, numbering, footers, group sizes
    seen = {}
    for c in cards:
        if c["id"] in seen:
            err.append(f"duplicate id {c['id']} (#{seen[c['id']]} and #{c['n']})")
        seen[c["id"]] = c["n"]
    nums = [c["n"] for c in cards]
    if nums != list(range(1, len(cards) + 1)):
        err.append("frame numbers are not #1..#%d in band order; run "
                   "tools/number-prepositions-frames.py" % len(cards))
    for c in cards:
        if not c["foot"].startswith(c["id"] + ".png"):
            flag(c, f"footer file {c['foot']!r} does not match the id", True)
        if c["examples_attr"] != c["group_size"]:
            flag(c, f"group {c['group']!r} says data-examples="
                    f"{c['examples_attr']} but holds {c['group_size']}", True)

    for c in cards:
        live = c["verdict"] != "drop"
        hard = c["drawn"]
        if c["drawn"] and not live:
            flag(c, "dropped card carries art", True)
        if not live:
            continue
        # labels
        if c["h3"] != c["group"] or (c["group_h3"] and c["group_h3"] != c["group"]):
            flag(c, f"card heading {c['h3']!r} differs from group {c['group']!r}", hard)
        # sentence and build
        if c["builds"] and _bare(c["builds"][0]) != _bare(c["example"]):
            flag(c, "first build differs from the example", hard)
        for rx, why in BAD_DUTCH:
            for field in [c["example"], c["question"], c["alt"]] + c["builds"]:
                if rx.search(field):
                    flag(c, f"{why}: {field!r}", True)
                    break
        # souvenir imagery
        if SOUVENIR.search(c["scene"]) and not c["redraw"]:
            flag(c, "souvenir imagery in the scene: " +
                 SOUVENIR.search(c["scene"]).group(0), hard)
        # art bookkeeping and alt text
        if c["drawn"]:
            if c["status"] != "drawn" or not c["flag_drawn"]:
                flag(c, "card has art but is not marked drawn", True)
            if c["img_alt"] != c["alt"]:
                flag(c, "img alt differs from the Alt text row", True)
        if not c["alt"]:
            if c["drawn"]:
                flag(c, "no alt text", True)
            continue
        alt_words = set(w.lower() for w in WORD.findall(c["alt"]))
        own = chunk_forms(c["group"]) | chunk_forms(c["h3"])
        leak = sorted(alt_words & own)
        if leak:
            flag(c, f"alt names the chunk ({', '.join(leak)}): {c['alt']!r}", hard)
        other = set()
        for p in partners.get(c["group"], ()):
            other |= chunk_forms(p)
        leak = sorted((alt_words & other) - own)
        if leak:
            flag(c, f"alt names a contrast partner ({', '.join(leak)}): {c['alt']!r}",
                 hard)

    # the game's copy of drawn cards (read only; patches are listed, never applied)
    if GAME.exists():
        game = json.loads(GAME.read_text(encoding="utf-8"))
        ids = set(f["id"] for f in game.get("frames", []))
        for c in cards:
            if c["drawn"] and c["verdict"] != "drop":
                if (c["id"] in ids) != c["flag_game"]:
                    flag(c, "'in the game' flag disagrees with prepositions.json", True)

    # totals on the band headers and the index
    idx = (PAGES / "index.html").read_text(encoding="utf-8")
    groups_by_band = {}
    for c in cards:
        groups_by_band.setdefault(c["band"], set()).add(c["group"])
    for band in BANDS:
        bc = [c for c in cards if c["band"] == band]
        src = B64.sub("", (PAGES / f"{band}.html").read_text(encoding="utf-8"))
        s = re.search(r'<div class="sum">(.*?)</div>', src, re.S)
        s = text_of(re.sub(r"</span>", "|", s.group(1))) if s else ""
        want = [f"{len(groups_by_band[band])} verb-prepositions", f"{len(bc)} cards"]
        drawn = sum(c["drawn"] for c in bc)
        if drawn:
            want.append(f"{drawn} of {len(bc)} drawn")
        for w in want:
            if w not in s.split("|"):
                err.append(f"{band}.html header lacks {w!r}: {s!r}")
        row = re.search(r'<tr><td><a href="%s\.html">.*?</tr>' % re.escape(band), idx, re.S)
        cells = re.findall(r'<td class="n">(\d+)</td>', row.group(0)) if row else []
        if cells != [str(len(groups_by_band[band])), str(len(bc))]:
            err.append(f"index.html row {band} says {cells}, pages give "
                       f"{[len(groups_by_band[band]), len(bc)]}")
    distinct = len({c["group"] for c in cards})
    tot = re.search(r'<tr class="totaal"><td>Total</td><td class="n">(\d+)</td>'
                    r'<td class="n">(\d+)</td>', idx)
    if not tot or tot.groups() != (str(distinct), str(len(cards))):
        err.append(f"index.html total row {tot.groups() if tot else None} != "
                   f"({distinct}, {len(cards)})")
    if f"<span>{distinct} verb-prepositions</span>" not in idx:
        err.append(f"index.html summary does not say {distinct} verb-prepositions")
    return err, warn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["read", "patch", "check"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.action == "check":
        errors, warnings = audit()
        for w in warnings:
            print("  warn  " + w)
        for e in errors:
            print("  ERROR " + e)
        print(f"{len(errors)} errors, {len(warnings)} warnings")

    if a.action in ("read", "check"):
        all_cards = {}
        for p in pages():
            cards = read_cards(p)
            all_cards.update(cards)
            if a.action == "check":
                miss = [c["id"] for c in cards.values()
                        if not c.get("must") or not c.get("avoid")]
                stub = [c["id"] for c in cards.values()
                        if len(c.get("scene", "")) < 60]
                print(f"  {p.name:16s} {len(cards):4d} cards  "
                      f"{len(miss):3d} without must/avoid  {len(stub):3d} stub scenes")
        print(f"total cards: {len(all_cards)}")
        if a.action == "check" and errors:
            sys.exit(1)
        if a.action == "read":
            out = Path(a.out or "records.json")
            out.write_text(json.dumps(list(all_cards.values()), ensure_ascii=False,
                                      indent=1), encoding="utf-8")
            print(f"wrote {out}")
        return

    if not a.file:
        sys.exit("patch needs a fixes file")
    data = json.loads(Path(a.file).read_text(encoding="utf-8"))
    fixes = data.get("fixes") or data.get("briefs") or data
    touched, changed, notfound = patch(fixes, a.dry_run)
    print(f"{'would change' if a.dry_run else 'changed'}: {changed} cards")
    for name, ids in touched.items():
        print(f"  {name:16s} {len(ids)}")
    if notfound:
        print(f"id not found on any page: {notfound}")


if __name__ == "__main__":
    main()
