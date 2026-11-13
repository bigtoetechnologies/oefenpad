#!/usr/bin/env python3
"""Build the verb x preposition matrix pages from the band pages.

    python3 tools/build-prepositions-matrix.py

One page per band, Docs/voorzetselpaden/matrix-<band>.html: prepositions
across the top, verbs down the left, a check mark where a chunk exists. The
band pages are the source; nothing here is edited by hand. Cards whose
verdict is "drop" are left out, like the counts on the band pages. Also
adds a "matrix" link to each band page's nav and index row, once.
"""
import html as H
import re
from collections import OrderedDict
from pathlib import Path

PAGES = Path(__file__).resolve().parent.parent / "Docs/voorzetselpaden"
BANDS = [("a0", "A0"), ("a1", "A1"), ("a2", "A2"), ("a2-pairs", "A2 pairs (4b)"),
         ("a2-plus", "A2+"), ("b1", "B1"), ("b1-plus", "B1+"), ("b2", "B2")]
PREPS = ["aan", "achter", "bij", "binnen", "boven", "buiten", "door", "in", "jegens", "langs",
         "met", "na", "naar", "naartoe", "om", "onder", "op", "over", "rond", "tegen",
         "tegenover", "tot", "tussen", "uit", "van", "vandaan", "volgens", "voor", "zonder"]
OTHER = "overig"
ARTICLE = re.compile(r'<article class="kaart[^"]*"([^>]*)>(.*?)</article>', re.S)


def sortkey(verb):
    v = re.sub(r"^(zich|een|het|de)\s+", "", verb)
    return v.casefold()


def read_band(band):
    """chunk -> number of active cards, in page order."""
    src = (PAGES / f"{band}.html").read_text(encoding="utf-8")
    chunks = OrderedDict()
    for m in ARTICLE.finditer(src):
        if 'data-verdict="drop"' in m.group(1):
            continue
        h = re.search(r'<h3 class="chunk">(.*?)</h3>', m.group(2), re.S)
        if not h:
            continue
        chunk = H.unescape(re.sub(r"<[^>]+>", "", h.group(1))).strip().casefold()
        chunks[chunk] = chunks.get(chunk, 0) + 1
    return chunks


def split(chunk):
    words = chunk.split()
    if len(words) > 1 and words[-1] in PREPS:
        return " ".join(words[:-1]), words[-1]
    return chunk, OTHER


CSS = """
:root{--kobalt:#2B50C8;--papier:#fff;--inkt:#111;--grijs:#666;--lijn:#d9deea;--vlak:#f6f7fb;
  --letter:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif}
*{box-sizing:border-box}
body{margin:0;background:var(--papier);color:var(--inkt);font-family:var(--letter);line-height:1.4}
a{color:var(--kobalt)}
header{padding:26px 24px 16px;border-bottom:2px solid var(--kobalt)}
h1{margin:0 0 4px;font-size:clamp(22px,3.4vw,34px);letter-spacing:-.02em}
.lead{margin:0;color:var(--grijs);max-width:80ch}
.sum{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.sum span{border:1px solid var(--lijn);border-radius:999px;padding:4px 10px;font-size:13px}
nav.banden{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;font-size:13px}
nav.banden a{border:1px solid var(--lijn);border-radius:999px;padding:3px 10px;text-decoration:none}
nav.banden a.hier{background:var(--kobalt);color:#fff;border-color:var(--kobalt)}
main{padding:18px 24px 56px}
.wrap{overflow:auto;max-height:78vh;border:1px solid var(--lijn);border-radius:10px}
table{border-collapse:separate;border-spacing:0;font-size:14px}
th,td{padding:5px 9px;border-bottom:1px solid var(--lijn);border-right:1px solid var(--lijn);text-align:center;white-space:nowrap}
thead th{position:sticky;top:0;background:var(--kobalt);color:#fff;font-weight:700;z-index:2;
  border-color:var(--kobalt)}
tbody th{position:sticky;left:0;background:#fff;text-align:left;font-weight:600;z-index:1}
thead th:first-child{left:0;z-index:3;text-align:left}
tbody tr:hover th,tbody tr:hover td{background:var(--vlak)}
td.ja{color:var(--kobalt);font-weight:800;font-size:16px}
td.leeg{color:transparent}
td.n,th.n{color:var(--grijs);font-weight:400;background:var(--vlak)}
tfoot td,tfoot th{position:sticky;bottom:0;background:var(--vlak);font-weight:700}
tfoot th{left:0;z-index:3;text-align:left}
"""


def page(band, label, chunks):
    cells = OrderedDict()  # verb -> {prep: (chunk, n)}
    for chunk, n in chunks.items():
        verb, prep = split(chunk)
        cells.setdefault(verb, {})[prep] = (chunk, n)
    used = {p for row in cells.values() for p in row}
    cols = [p for p in PREPS if p in used] + ([OTHER] if OTHER in used else [])
    verbs = sorted(cells, key=sortkey)
    head = "".join(f"<th>{H.escape(p)}</th>" for p in cols)
    body = []
    for v in verbs:
        row = cells[v]
        tds = []
        for p in cols:
            if p in row:
                chunk, n = row[p]
                tds.append(f'<td class="ja" title="{H.escape(chunk)} · {n} card{"s" if n != 1 else ""}">✓</td>')
            else:
                tds.append('<td class="leeg">·</td>')
        tds.append(f'<td class="n">{len(row)}</td>')
        body.append(f'<tr><th scope="row">{H.escape(v)}</th>{"".join(tds)}</tr>')
    foot = "".join(f'<td>{sum(1 for r in cells.values() if p in r)}</td>' for p in cols)
    nav = ('<nav class="banden"><a href="index.html">overview</a>' + "".join(
        f'<a href="matrix-{b}.html"{" class=\"hier\"" if b == band else ""}>{H.escape(l)}</a>'
        for b, l in BANDS) + "</nav>")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Voorzetselpaden — matrix {H.escape(label)}</title>
<style>{CSS}</style>
</head>
<body>
<header>
<h1>Verb × preposition, {H.escape(label)}</h1>
<p class="lead">A check mark means this band has a chunk with that verb and preposition. Hover a check for the chunk and its card count. Chunks that end in no preposition sit under <em>{OTHER}</em>. Cards marked drop are left out. <a href="{band}.html">Open the {H.escape(label)} cards</a>.</p>
<div class="sum"><span>{len(verbs)} verbs</span><span>{len(chunks)} chunks</span><span>{len(cols)} prepositions</span></div>
{nav}
</header>
<main>
<div class="wrap"><table>
<thead><tr><th>verb</th>{head}<th class="n">chunks</th></tr></thead>
<tbody>
{chr(10).join(body)}
</tbody>
<tfoot><tr><th>verbs per preposition</th>{foot}<td></td></tr></tfoot>
</table></div>
</main>
</body>
</html>
"""


def link_nav():
    """One 'matrix' link on each band page nav and index row. Safe to repeat."""
    for band, _ in BANDS + [("index", "")]:
        p = PAGES / f"{band}.html"
        s = p.read_text(encoding="utf-8")
        if "matrix-" in s.split("</nav>")[0] and band != "index":
            continue
        if band == "index":
            if "matrix-a0.html" in s:
                continue
            s = s.replace("<th>Band</th>", "<th>Band</th>", 1)
            s = re.sub(r'(<tr><td><a href="([a-z0-9-]+)\.html">[^<]*</a></td>)',
                       lambda m: m.group(1) + f'<td><a href="matrix-{m.group(2)}.html">matrix</a></td>',
                       s)
            s = s.replace("<th>Band</th>", "<th>Band</th><th>Matrix</th>", 1)
        else:
            s = s.replace("</nav>", f'<a href="matrix-{band}.html">matrix</a></nav>', 1)
        p.write_text(s, encoding="utf-8")


def main():
    for band, label in BANDS:
        chunks = read_band(band)
        (PAGES / f"matrix-{band}.html").write_text(page(band, label, chunks), encoding="utf-8")
        verbs = {split(c)[0] for c in chunks}
        print(f"matrix-{band}.html  {len(chunks)} chunks, {len(verbs)} verbs")
    link_nav()


if __name__ == "__main__":
    main()
