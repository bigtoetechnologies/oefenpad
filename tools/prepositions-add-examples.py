#!/usr/bin/env python3
"""Add new example cards to chunks on the Voorzetselpaden band pages.

    python3 tools/prepositions-add-examples.py brief  PAGE START COUNT OUT.json
    python3 tools/prepositions-add-examples.py add    PAGE cards.json [--dry-run]

PAGE is a band name such as a2-plus. `brief` writes the chunks START..START+COUNT
with their existing cards, for an author to read. `add` takes
{"cards": [{"chunk", "id", "gloss", "scene", "must", "avoid", "note", "nl", "en",
"bouw": [..], "question", "answer": true|false, "alt"}]} and appends each card to
its chunk group, then fixes the group's example count and the page's card count.
Nothing else in the page changes.
"""
import html as H
import json
import re
import sys
from pathlib import Path

PAGES = Path(__file__).resolve().parent.parent / "Docs/voorzetselpaden"
GROUP = re.compile(r'<div class="chunkgroep" data-chunk="(?P<chunk>[^"]*)" data-examples="(?P<n>\d+)">'
                   r'(?P<body>.*?)(?=<div class="chunkgroep"|</section>)', re.S)
CARD_ID = re.compile(r'<article class="kaart[^"]*"[^>]*data-id="([^"]+)"')
E = lambda v: H.escape(str(v).strip(), quote=True)
T = lambda s: H.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def dd(body, cls):
    m = re.search(r'<dd class="%s">(.*?)</dd>' % cls, body, re.S)
    return T(m.group(1)) if m else ""


def brief(page, start, count, out):
    src = (PAGES / f"{page}.html").read_text(encoding="utf-8")
    groups = list(GROUP.finditer(src))[start:start + count]
    res = []
    for g in groups:
        cards = []
        for a in re.finditer(r'<article class="kaart[^"]*"[^>]*data-id="([^"]+)"(.*?)</article>',
                             g.group("body"), re.S):
            b = a.group(2)
            gl = re.search(r'<p class="gloss">(.*?)</p>', b, re.S)
            cards.append({"id": a.group(1), "gloss": T(gl.group(1)) if gl else "",
                          "scene": dd(b, "scene"), "must": dd(b, "must"),
                          "avoid": dd(b, "avoid"), "note": dd(b, "note"),
                          "example": dd(b, "voorbeeld-nl"),
                          "bouw": [T(x) for x in re.findall(r'<dd class="bouw">(.*?)</dd>', b, re.S)],
                          "question": dd(b, "controlevraag")})
        res.append({"chunk": H.unescape(g.group("chunk")), "have": len(cards),
                    "need": max(0, 4 - len(cards)), "cards": cards})
    Path(out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(res)} chunks, {sum(r['need'] for r in res)} new cards needed -> {out}")


def build(c, band):
    bouw = "".join(f'<dt>Build</dt><dd class="bouw">{E(b)}</dd>' for b in c["bouw"])
    return (f'<article class="kaart" data-id="{E(c["id"])}" data-band="{band}" data-kind="proposal" '
            f'data-row="" data-status="needed"><p class="geenbeeld">not drawn yet</p>'
            f'<h3 class="chunk">{E(c["chunk"])}</h3><p class="gloss">{E(c["gloss"])}</p><dl>'
            f'<dt>Scene</dt><dd class="scene">{E(c["scene"])}</dd>'
            f'<dt>Must read</dt><dd class="must">{E(c["must"])}</dd>'
            f'<dt>Avoid</dt><dd class="avoid">{E(c["avoid"])}</dd>'
            f'<dt>Pair / note</dt><dd class="note">{E(c["note"])}</dd>'
            f'<dt>Example</dt><dd class="voorbeeld-nl">{E(c["nl"])}<br>'
            f'<span class="voorbeeld-en">{E(c["en"])}</span></dd>{bouw}'
            f'<dt>Check question</dt><dd class="controlevraag">{E(c["question"])} '
            f'<strong class="antwoord">{"Ja" if c["answer"] else "Nee"}</strong></dd>'
            f'<dt>Alt text</dt><dd class="alt">{E(c["alt"])}</dd></dl>'
            f'<p class="id">{E(c["id"])}.png · nieuw</p></article>')


def problems(c, existing):
    p = [k for k in ("chunk", "id", "gloss", "scene", "must", "avoid", "note", "nl", "en",
                     "question", "alt") if not str(c.get(k, "")).strip()]
    if not c.get("bouw"):
        p.append("bouw")
    if not isinstance(c.get("answer"), bool):
        p.append("answer")
    if c.get("id") in existing:
        p.append("id already used")
    if not re.fullmatch(r"[a-z0-9-]+", str(c.get("id", ""))):
        p.append("id not a slug")
    return p


def add(page, cardsfile, dry):
    path = PAGES / f"{page}.html"
    src = path.read_text(encoding="utf-8")
    cards = json.loads(Path(cardsfile).read_text(encoding="utf-8"))["cards"]
    existing = set()
    for f in PAGES.glob("*.html"):
        existing |= set(CARD_ID.findall(f.read_text(encoding="utf-8")))
    by = {}
    bad = 0
    for c in cards:
        pr = problems(c, existing)
        if pr:
            print("SKIP", c.get("id"), pr)
            bad += 1
            continue
        existing.add(c["id"])
        by.setdefault(H.escape(c["chunk"], quote=True), []).append(c)
    added = 0

    def repl(m):
        nonlocal added
        key = m.group("chunk")
        new = by.pop(key, None) or by.pop(H.unescape(key), None)
        if not new:
            return m.group(0)
        body = m.group("body")
        band = re.search(r'data-band="([^"]*)"', body).group(1)
        n = int(m.group("n")) + len(new)
        i = body.rindex("</article>") + len("</article>")
        body = body[:i] + "".join(build(c, band) for c in new) + body[i:]
        body = re.sub(r'<p class="telling">.*?</p>', f'<p class="telling">{n} examples</p>', body, 1, re.S)
        added += len(new)
        return (f'<div class="chunkgroep" data-chunk="{m.group("chunk")}" data-examples="{n}">' + body)

    out = GROUP.sub(repl, src)
    total = len(re.findall(r'<article class="kaart', out))
    out = re.sub(r'(<div class="sum">.*?<span>)\d+( cards</span>)', lambda m: f"{m.group(1)}{total}{m.group(2)}",
                 out, 1, re.S)
    print(f"{'would add' if dry else 'added'} {added} cards, {bad} skipped, page now {total} cards")
    for k in by:
        print("CHUNK NOT FOUND:", k, [c["id"] for c in by[k]])
    if not dry:
        path.write_text(out, encoding="utf-8")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 5 and a[0] == "brief":
        brief(a[1], int(a[2]), int(a[3]), a[4])
    elif len(a) >= 3 and a[0] == "add":
        add(a[1], a[2], "--dry-run" in a)
    else:
        sys.exit(__doc__)
