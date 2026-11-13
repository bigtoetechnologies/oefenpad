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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["read", "patch", "check"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

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
