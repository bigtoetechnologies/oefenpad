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
canonical order below. A card marked owner_edit is refused unless the fix
says "force": true, so a hand-written scene is never silently replaced.
"""
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
    ("Paar / notitie", "note"),
    ("Toetst", "tests"),
]
LABEL = {cls: lab for lab, cls in FIELDS}
ORDER = [cls for _, cls in FIELDS]

CARD = re.compile(r'<article class="kaart[^"]*"[^>]*data-id="(?P<id>[^"]+)"[^>]*>'
                  r'(?P<body>.*?)</article>', re.S)
BADGES = {"needs_redraw": ('<span class="redraw">opnieuw tekenen</span>', "redraw"),
          "owner_edit": ('<span class="eigenaar">door de eigenaar</span>', "eigenaar")}


def pages():
    return sorted(p for p in PAGES.glob("*.html") if p.name != "index.html")


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
        rec["owner_edit"] = 'class="eigenaar"' in body
        rec["needs_redraw"] = 'class="redraw"' in body
        out[rec["id"]] = rec
    return out


def esc(v):
    return H.escape(str(v), quote=True)


def set_field(body, cls, value):
    """Replace a dd, or insert the dt/dd pair in canonical order."""
    pat = re.compile(r'(<dd class="%s">).*?(</dd>)' % cls, re.S)
    if pat.search(body):
        return pat.sub(lambda m: m.group(1) + esc(value) + m.group(2), body, count=1)
    block = f'<dt>{LABEL[cls]}</dt><dd class="{cls}">{esc(value)}</dd>'
    after = ORDER[:ORDER.index(cls)]
    for prev in reversed(after):
        m = re.search(r'<dd class="%s">.*?</dd>' % prev, body, re.S)
        if m:
            return body[:m.end()] + block + body[m.end():]
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
    touched, changed, refused, notfound = {}, 0, [], list(want)

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
            if 'class="eigenaar"' in body and not fix.get("force"):
                refused.append(cid)
                return whole
            new = body
            for cls in ORDER:
                if cls in fix and str(fix[cls]).strip():
                    new = set_field(new, cls, str(fix[cls]).strip())
            if "chunk" in fix and str(fix["chunk"]).strip():
                new = re.sub(r'(<h3 class="chunk">).*?(</h3>)',
                             lambda x: x.group(1) + esc(fix["chunk"].strip()) + x.group(2),
                             new, count=1, flags=re.S)
            if "gloss" in fix and str(fix["gloss"]).strip():
                new = re.sub(r'(<p class="gloss">).*?(</p>)',
                             lambda x: x.group(1) + esc(fix["gloss"].strip()) + x.group(2),
                             new, count=1, flags=re.S)
            for key in ("needs_redraw", "owner_edit"):
                if fix.get(key):
                    new = set_badge(new, key)
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
    return touched, changed, refused, notfound


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
    touched, changed, refused, notfound = patch(fixes, a.dry_run)
    print(f"{'would change' if a.dry_run else 'changed'}: {changed} cards")
    for name, ids in touched.items():
        print(f"  {name:16s} {len(ids)}")
    if refused:
        print(f"REFUSED, owner_edit (pass force:true to override): {refused}")
    if notfound:
        print(f"id not found on any page: {notfound}")


if __name__ == "__main__":
    main()
