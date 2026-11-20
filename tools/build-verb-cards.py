#!/usr/bin/env python3
"""Build Docs/werkwoorden/ from the selection and the scene notes.

Inputs
  tools/_ww_tmp/selection.json          every selected verb, written by select.py
  tools/_ww_tmp/backlog_seed.tsv        the verbs held back, with reason and note
  tools/_ww_tmp/scenes/<page>.tsv       scene, must, avoid, alt per verb

Outputs
  Docs/werkwoorden/{a0,a1,a2,b1,b2}-{regular,irregular}.html
  Docs/werkwoorden/index.html           overview and coverage
  Docs/werkwoorden/matrix.html           every verb on one table
  Docs/werkwoorden/backlog.html          what still needs cards

Since 20 Nov 2026 the sources are the master: edit tools/_ww_tmp (select.py,
scenes/*.tsv) and rerun this script, which rewrites the ten band pages and the
three generated pages.  Before a rebuild, run it with --out to a scratch folder
and diff against Docs/werkwoorden to make sure nobody hand-edited a page.

Run:  python3 tools/build-verb-cards.py
"""

import csv
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "tools", "_ww_tmp")
SCENES = os.path.join(TMP, "scenes")
OUT = os.path.join(ROOT, "Docs", "werkwoorden")

for _i, _a in enumerate(sys.argv[1:]):
    if _a == "--scenes":
        SCENES = os.path.abspath(sys.argv[2 + _i])
    elif _a == "--out":
        OUT = os.path.abspath(sys.argv[2 + _i])

def load_forms():
    path = os.path.join(ROOT, "tools", "lexicon", "werkwoorden-vormen.tsv")
    if not os.path.exists(path):
        sys.exit(f"missing {path}: run tools/build-verb-forms.py")
    return {r["verb"]: r for r in read_tsv(path)}


FORMS = {}
ART_DIR = os.path.join(ROOT, "assets", "verbs")
DRAWN = set()


def load_drawn():
    """A card is drawn when assets/verbs/<slug>.png exists."""
    if os.path.isdir(ART_DIR):
        DRAWN.update(f[:-4] for f in os.listdir(ART_DIR) if f.endswith(".png"))


REDRAW = {}


def load_redraw():
    """Drawn cards whose brief changed after drawing: tools/_ww_tmp/redraw.tsv."""
    path = os.path.join(TMP, "redraw.tsv")
    if os.path.exists(path):
        for r in read_tsv(path):
            REDRAW[r["slug"]] = r["reason"]

BANDS = ["A0", "A1", "A2", "B1", "B2"]
REGS = ["irregular", "regular"]
LABEL = {"regular": "regelmatig", "irregular": "onregelmatig"}

BAND_LEAD = {
    "A0": "Survival: the first weeks. Being, having, going, eating, and the modals that hold every sentence together.",
    "A1": "Everyday life outside the house: buying, waiting, driving, talking, and the first verbs of feeling.",
    "A2": "Work, society and the first abstract verbs: proving, comparing, deciding, and the verbs of the body.",
    "B1": "The wider vocabulary: institutions, nature, the workshop, and verbs of argument and judgement.",
    "B2": "The long tail: crafts, the garden, the body and its noises, and the everyday verbs a learner reads before speaking.",
}

PAGE_BLURB = {
    "irregular": "The strong verbs. They carry the most frequent meanings, so they come first in every band.",
    "regular": "The weak verbs, past in -te or -de. Regular, so later on the ladder and easier once met.",
}

CSS = """
:root{
  --kobalt:#2B50C8; --papier:#fff; --inkt:#111; --grijs:#666; --lijn:#d9deea;
  --rood:#b3261e; --oranje:#b36b00; --letter:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--papier);color:var(--inkt);font-family:var(--letter);line-height:1.45}
a{color:var(--kobalt)}
header{padding:26px 24px 16px;border-bottom:2px solid var(--kobalt)}
h1{margin:0 0 4px;font-size:clamp(22px,3.4vw,34px);letter-spacing:-.02em}
.lead{margin:0;color:var(--grijs);max-width:80ch}
.lead+.lead{margin-top:4px}
.sum{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.sum span{border:1px solid var(--lijn);border-radius:999px;padding:4px 10px;font-size:13px}
.sum span.waarschuwing{border-color:var(--rood);color:var(--rood)}
nav.banden{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;font-size:13px}
nav.banden a{border:1px solid var(--lijn);border-radius:999px;padding:3px 10px;text-decoration:none}
nav.banden a.hier{background:var(--kobalt);color:#fff;border-color:var(--kobalt)}
main{padding:18px 24px 56px}
.kaarten{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px;margin-top:12px}
.kaart{position:relative;border:1px solid var(--lijn);border-radius:12px;padding:14px;break-inside:avoid;display:flex;flex-direction:column}
.beeld{display:block;width:100%;max-width:170px;height:auto;margin:0 auto 10px}
.geenbeeld{border:1px dashed var(--lijn);border-radius:8px;color:var(--grijs);font-size:12px;
  text-align:center;padding:26px 8px;margin:0 auto 10px;max-width:170px}
.kaart h3{margin:0;font-size:18px;letter-spacing:-.01em}
.framenummer{position:absolute;top:8px;right:10px;font:700 11px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--kobalt);background:var(--papier);border:1px solid var(--lijn);border-radius:999px;padding:1px 7px;font-variant-numeric:tabular-nums;letter-spacing:.02em}
.gloss{margin:2px 0 8px;color:var(--grijs);font-size:14px}
.vormen{display:flex;flex-wrap:wrap;gap:4px 14px;margin:0 0 9px;font-size:13px;font-weight:600;color:var(--kobalt)}
.vormen span::before{font-weight:400;color:var(--grijs);margin-right:5px}
.vormen .imp::before{content:"verleden"}
.vormen .perf::before{content:"perfectum"}
.vlaggen{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 9px}
.vlaggen span{border:1px solid var(--lijn);border-radius:999px;padding:1px 8px;font-size:11px;color:var(--grijs)}
.vlaggen span.getekend{border-color:var(--kobalt);color:var(--kobalt)}
.vlaggen span.opnieuw{border-color:var(--rood);color:var(--rood)}
.vlaggen span.inspel{background:var(--kobalt);color:#fff;border-color:var(--kobalt)}
dl{margin:0;font-size:14px}
dt{margin-top:9px;color:var(--grijs);font-size:11px;text-transform:uppercase;letter-spacing:.05em}
dd{margin:2px 0 0}
.kaart code{background:#eef1f8;padding:0 3px;border-radius:3px;font-size:.92em}
.id{color:var(--grijs);font-size:11px;margin-top:auto;padding-top:9px;font-family:ui-monospace,monospace}
.filters{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;font-size:13px}
.filters button{border:1px solid var(--lijn);border-radius:999px;padding:3px 11px;background:none;
  font-family:inherit;font-size:13px;cursor:pointer}
.filters button[aria-pressed=true]{background:var(--kobalt);color:#fff;border-color:var(--kobalt)}
@media print{
  header{padding:0 0 10px} main{padding:0} .filters,nav.banden{display:none}
  .kaarten{grid-template-columns:repeat(3,1fr);gap:9px}
  .kaart{page-break-inside:avoid;padding:9px} body{font-size:11px}
}
.sectiekop{margin:34px 0 0;padding-top:14px;border-top:3px solid var(--kobalt)}
.sectiekop h2{margin:0;font-size:23px}
.sectiekop p{margin:4px 0 0;color:var(--grijs);max-width:85ch;font-size:14px}
table{border-collapse:collapse;width:100%;margin-top:16px;font-size:14px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--lijn);vertical-align:top}
th{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--grijs)}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.blurb{color:var(--grijs);max-width:44ch}
td.mono{font-family:ui-monospace,monospace;font-size:12px;color:var(--grijs)}
tr.totaal td{font-weight:700;border-top:2px solid var(--kobalt);border-bottom:none}
.uitleg{max-width:80ch;margin-top:22px}
.uitleg h2{font-size:17px;margin:20px 0 6px}
.uitleg p{margin:6px 0}
.uitleg code{background:#f6f7fb;padding:1px 5px;border-radius:4px}
.uitleg li{margin:4px 0}
"""

FILTER_JS = """
<script>
(function(){
  var bar=document.querySelector('.filters'); if(!bar) return;
  var cards=[].slice.call(document.querySelectorAll('.kaart'));
  bar.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    var want=b.dataset.filter;
    [].forEach.call(bar.querySelectorAll('button'),function(x){
      x.setAttribute('aria-pressed', String(x===b)); });
    cards.forEach(function(c){
      c.hidden = !(want==='alles' || c.dataset.domain===want);
    });
  });
})();
</script>
"""


def esc(text):
    return html.escape(text, quote=False)


def attr(text):
    return html.escape(text, quote=True)


def read_tsv(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def page_key(band, reg):
    return f"{band.lower()}-{reg}"


def load_scenes(key):
    path = os.path.join(SCENES, key + ".tsv")
    if not os.path.exists(path):
        return None
    rows = read_tsv(path)
    return {r["verb"].strip(): r for r in rows}


def build():
    FORMS.update(load_forms())
    load_drawn()
    load_redraw()
    with open(os.path.join(TMP, "selection.json"), encoding="utf-8") as fh:
        records = json.load(fh)
    backlog = read_tsv(os.path.join(TMP, "backlog_seed.tsv"))

    pages = {}
    for band in BANDS:
        for reg in REGS:
            sub = [r for r in records if r["band"] == band and r["regularity"] == reg]
            sub.sort(key=lambda r: r["rank"])
            pages[page_key(band, reg)] = sub

    counts = {key: len(v) for key, v in pages.items()}
    skipped = []
    scenes_by_key = {}
    kept = {}

    # Split each page into cards and SKIP rows before numbering, so a skipped
    # verb leaves no gap in the frame sequence.
    for band in BANDS:
        for reg in REGS:
            key = page_key(band, reg)
            rows = pages[key]
            if not rows:
                continue
            scenes = load_scenes(key)
            if scenes is None:
                sys.exit(f"missing scene file: {SCENES}/{key}.tsv")
            missing = [r["verb"] for r in rows if r["verb"] not in scenes]
            if missing:
                sys.exit(f"{key}: no scene for {', '.join(missing)}")
            scenes_by_key[key] = scenes
            kept[key] = []
            for r in rows:
                scene = (scenes[r["verb"]].get("scene") or "").strip()
                if scene.upper().startswith("SKIP"):
                    skipped.append({
                        "verb": r["verb"], "band": r["band"],
                        "regularity": r["regularity"], "rank": r["rank"],
                        "reason": scene[4:].strip().lstrip(":").strip(),
                    })
                else:
                    kept[key].append(r)

    # Frame numbers run on across all eight pages, in page order.  Irregular
    # first in each band, because the frequency ranks put the irregulars there.
    frame = 0
    numbers = {}
    for band in BANDS:
        for reg in REGS:
            for r in kept[page_key(band, reg)]:
                frame += 1
                numbers[(r["band"], r["regularity"], r["verb"])] = frame
    total_frames = frame

    nav = ['<a href="index.html">overview</a>']
    for band in BANDS:
        for reg in REGS:
            key = page_key(band, reg)
            nav.append(f'<a href="{key}.html">{band} {LABEL[reg]}</a>')
    nav.append('<a href="matrix.html">matrix</a>')
    nav.append('<a href="backlog.html">backlog</a>')

    for band in BANDS:
        for reg in REGS:
            key = page_key(band, reg)
            rows = kept[key]
            if not rows:
                continue
            scenes = scenes_by_key[key]

            cards = [
                render_card(r, scenes[r["verb"]], numbers[(r["band"], r["regularity"], r["verb"])])
                for r in rows
            ]
            page_skips = counts[key] - len(rows)

            domains = {}
            for r in rows:
                domains[r["domain"]] = domains.get(r["domain"], 0) + 1
            navhtml = []
            for a in nav:
                a = a.replace(f'href="{key}.html"', f'href="{key}.html" class="hier"')
                navhtml.append(a)

            first = numbers[(band, reg, rows[0]["verb"])]
            last = numbers[(band, reg, rows[-1]["verb"])]
            ranks = [r["rank"] for r in rows]
            html_out = []
            html_out.append("<!DOCTYPE html>")
            html_out.append('<html lang="nl">')
            html_out.append("<head>")
            html_out.append('<meta charset="UTF-8">')
            html_out.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
            html_out.append(f"<title>Werkwoorden — {band} {LABEL[reg]}</title>")
            html_out.append("<style>" + CSS + "</style>")
            html_out.append("</head>")
            html_out.append("<body>")
            html_out.append("<header>")
            html_out.append(f"<h1>Werkwoorden — {band} · {LABEL[reg]}</h1>")
            html_out.append(f'<p class="lead">{esc(BAND_LEAD[band] + " " + PAGE_BLURB[reg])}</p>')
            html_out.append('<p class="lead">One card per verb: the base form (irregular verbs also the past singular and perfect), the scene brief, the one mark that must read, the near misses, and the Dutch alt text. Sorted by lexicon frequency rank.</p>')
            html_out.append(
                '<div class="sum">'
                f'<span>{len(cards)} werkwoorden</span>'
                f'<span class="framereeks">frames #{first}–#{last}</span>'
                f'<span>rang {min(ranks)}–{max(ranks)}</span>'
                f'<span>{sum(1 for r in rows if r["slug"] in DRAWN)} getekend</span>'
                f'<span>{page_skips} met uitlegkaart</span>'
                "</div>"
            )
            html_out.append('<nav class="banden">' + "".join(navhtml) + "</nav>")
            buttons = ['<button data-filter="alles" aria-pressed="true">alles</button>']
            for dom, _n in sorted(domains.items(), key=lambda kv: (-kv[1], kv[0])):
                buttons.append(f'<button data-filter="{attr(dom)}">{esc(dom)}</button>')
            html_out.append('<div class="filters">' + "".join(buttons) + "</div>")
            html_out.append("</header>")
            html_out.append("<main>")
            html_out.append(
                f'<section class="sectiekop"><h2>{band} · {LABEL[reg]}</h2>'
                f"<p>{len(cards)} verbs with a "
                + ("strong" if reg == "irregular" else "weak")
                + f" past, rank {min(ranks)} to {max(ranks)}. One drawing each, in the "
                "Voorzetselpaden style. Cards without a drawing stay as proposals.</p></section>"
            )
            html_out.append('<div class="kaarten">')
            html_out.extend(cards)
            html_out.append("</div>")
            html_out.append("</main>")
            html_out.append(FILTER_JS)
            html_out.append("</body>")
            html_out.append("</html>")
            with open(os.path.join(OUT, key + ".html"), "w", encoding="utf-8") as fh:
                fh.write("\n".join(html_out) + "\n")

    order = [page_key(band, reg) for band in BANDS for reg in REGS]
    card_records = [r for key in order for r in kept[key]]
    write_matrix(card_records, numbers)
    write_index(pages, kept, numbers, skipped, backlog, total_frames, records)
    write_backlog(backlog, skipped)

    print(f"pages {len(pages)}  cards {len(card_records)}  frames {total_frames}  skipped {len(skipped)}")
    for key in order:
        print(f"  {key:16} {len(kept[key]):3}  ({counts[key] - len(kept[key])} skipped)")


def form_lines(r):
    """Irregular verbs carry the forms a learner cannot predict: past singular and perfect."""
    if r["regularity"] != "irregular":
        return []
    f = FORMS.get(r["verb"])
    if f is None:
        sys.exit(f"no forms row for irregular verb {r['verb']}")
    aux = {"hebben": "heeft", "zijn": "is", "hebben/zijn": "heeft/is"}.get(f["aux"], "")
    perfect = f"{aux} {f['participle']}".strip() if f["participle"] else "geen voltooid deelwoord"
    return [
        '<p class="vormen">'
        f'<span class="imp" title="verleden tijd, enkelvoud">{esc(f["past_sg"])}</span>'
        f'<span class="perf" title="voltooid deelwoord met hulpwerkwoord">{esc(perfect)}</span>'
        "</p>"
    ]


def status_of(slug):
    if slug not in DRAWN:
        return "proposal"
    return "redraw" if slug in REDRAW else "drawn"


def render_card(r, s, number):
    dom = r["domain"]
    lines = [
        f'<article id="{attr(r["slug"])}" class="kaart" data-id="{attr(r["slug"])}" data-band="{r["band"].lower()}" '
        f'data-kind="verb" data-regularity="{r["regularity"]}" data-domain="{attr(dom)}" '
        f'data-status="{status_of(r["slug"])}" data-severity="">',
        f'<span class="framenummer" title="Frame {number}">#{number}</span>',
        (f'<img class="beeld" src="../../assets/verbs/{attr(r["slug"])}.png" alt="{attr(s["alt"].strip())}" loading="lazy">'
         if r["slug"] in DRAWN else '<div class="geenbeeld">geen beeld</div>'),
        f'<h3 class="chunk">{esc(r["verb"])}</h3>',
        f'<p class="gloss">{esc(r["gloss"])}</p>',
        '<p class="vlaggen">'
        f'<span>{LABEL[r["regularity"]]}</span><span>rang {r["rank"]}</span><span>{esc(dom)}</span>'
        + ('<span class="getekend">getekend</span>' if r["slug"] in DRAWN else "")
        + (f'<span class="opnieuw" title="{attr(REDRAW[r["slug"]])}">opnieuw tekenen</span>'
           if r["slug"] in DRAWN and r["slug"] in REDRAW else "")
        + "</p>",
        *form_lines(r),
        "<dl>",
        f'<dt>Scene</dt><dd class="scene">{esc(s["scene"].strip())}</dd>',
        f'<dt>Must read</dt><dd class="must">{esc(s["must"].strip())}</dd>',
        f'<dt>Avoid</dt><dd class="avoid">{esc(s["avoid"].strip())}</dd>',
        f'<dt>Alt text</dt><dd class="alt">{esc(s["alt"].strip())}</dd>',
        "</dl>",
        f'<p class="id">{esc(r["slug"])}.png · rang {r["rank"]} · {r["band"]} {LABEL[r["regularity"]]} · lexicon woorden.tsv</p>',
        "</article>",
    ]
    return "\n".join(lines)


def shell(title, lead, body, current=None):
    nav = ['<a href="index.html">overview</a>']
    for band in BANDS:
        for reg in REGS:
            key = page_key(band, reg)
            cls = ' class="hier"' if key == current else ""
            nav.append(f'<a href="{key}.html"{cls}>{band} {LABEL[reg]}</a>')
    nav.append('<a href="matrix.html"' + (' class="hier"' if current == "matrix" else "") + ">matrix</a>")
    nav.append('<a href="backlog.html"' + (' class="hier"' if current == "backlog" else "") + ">backlog</a>")
    return "\n".join([
        "<!DOCTYPE html>",
        '<html lang="nl">',
        "<head>",
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"<title>{title}</title>",
        "<style>" + CSS + "</style>",
        "</head>",
        "<body>",
        "<header>",
        f"<h1>{title}</h1>",
        f'<p class="lead">{lead}</p>',
        '<nav class="banden">' + "".join(nav) + "</nav>",
        "</header>",
        "<main>",
        body,
        "</main>",
        "</body>",
        "</html>",
    ]) + "\n"


def write_matrix(records, numbers):
    rows = []
    ordered = sorted(records, key=lambda r: numbers[(r["band"], r["regularity"], r["verb"])])
    for r in ordered:
        n = numbers[(r["band"], r["regularity"], r["verb"])]
        rows.append(
            "<tr>"
            f'<td class="n">{n}</td>'
            f'<td><a href="{page_key(r["band"], r["regularity"])}.html#{attr(r["slug"])}">{esc(r["verb"])}</a></td>'
            f'<td>{esc(r["gloss"])}</td>'
            f'<td>{r["band"]}</td>'
            f'<td>{LABEL[r["regularity"]]}</td>'
            f'<td class="n">{r["rank"]}</td>'
            f'<td>{esc(r["domain"])}</td>'
            '<td>voorstel</td>'
            "</tr>"
        )
    body = "\n".join([
        '<section class="sectiekop"><h2>Matrix</h2>'
        f"<p>All {len(records)} cards, one row each, in frame order. "
        "The skipped and held-back verbs are on <a href=\"backlog.html\">backlog.html</a>. "
        "Generated by <code>tools/build-verb-cards.py</code> from "
        "<code>selection.json</code>; do not edit by hand.</p></section>",
        "<table>",
        "<thead><tr><th>Frame</th><th>Verb</th><th>English</th><th>Band</th>"
        "<th>Vorm</th><th>Rang</th><th>Domein</th><th>Status</th></tr></thead>",
        "<tbody>",
        "\n".join(rows),
        "</tbody>",
        "</table>",
    ])
    with open(os.path.join(OUT, "matrix.html"), "w", encoding="utf-8") as fh:
        fh.write(shell("Werkwoorden — matrix", "Every verb, its band, regularity, frequency rank and lexicon domain, in frame order.", body, "matrix"))


def band_of(rank):
    for band, top in (("A0", 250), ("A1", 1000), ("A2", 2500), ("B1", 5000), ("B2", 10000)):
        if rank <= top:
            return band
    return "-"


def override_rows(records):
    """Hand-set ranks, with the reason select.py gives for each."""
    rows = []
    for r in sorted((r for r in records if r.get("rank_source") == "handmatig"), key=lambda r: r["rank"]):
        raw = r.get("raw_rank", 0)
        rows.append(
            "<tr>"
            f'<td>{esc(r["verb"])}</td>'
            f'<td class="n">{raw}</td><td>{band_of(raw)}</td>'
            f'<td class="n">{r["rank"]}</td><td>{band_of(r["rank"])}</td>'
            f'<td class="blurb">{esc(r.get("rank_reason", ""))}</td>'
            "</tr>"
        )
    return rows


def explanation_cards():
    """verb -> (band page, anchor) for every explanation card on the family pages."""
    import glob, json, re as _re, sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from explanation_lib import band_of, load_ranks
    ranks = load_ranks()
    out = {}
    for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_ex_tmp", "*.json"))):
        for c in json.load(open(f, encoding="utf-8")):
            if c.get("hold"): continue
            band = (c.get("band") or band_of(ranks[c.get("key", c["verb"])])).lower()
            anchor = _re.sub(r"[^a-z]+", "-", (c["verb"] + "-" + c["sense"].split("(")[0]).lower()).strip("-")[:40]
            out.setdefault(c["verb"], (band, anchor))
            if c.get("key"): out.setdefault(c["key"].split(" (")[0], (band, anchor))
    return out

def write_index(pages, kept, numbers, skipped, backlog, total_frames, records):
    skipped_by_page = {}
    for r in skipped:
        key = page_key(r["band"], r["regularity"])
        skipped_by_page[key] = skipped_by_page.get(key, 0) + 1
    lines = []
    for band in BANDS:
        for reg in REGS:
            key = page_key(band, reg)
            rows = kept[key]
            if not rows:
                continue
            ranks = [r["rank"] for r in rows]
            first = numbers[(band, reg, rows[0]["verb"])]
            last = numbers[(band, reg, rows[-1]["verb"])]
            lines.append(
                "<tr>"
                f'<td><a href="{key}.html">{band} · {LABEL[reg]}</a></td>'
                f'<td class="n">{len(rows)}</td>'
                f'<td class="n">{skipped_by_page.get(key, 0)}</td>'
                f'<td class="n">#{first}–#{last}</td>'
                f'<td class="n">{min(ranks)}–{max(ranks)}</td>'
                f'<td class="blurb">{BAND_LEAD[band]} {PAGE_BLURB[reg]}</td>'
                "</tr>"
            )
    n_cards = sum(len(v) for v in kept.values())
    counts = {}
    for r in backlog:
        counts[r["reason"]] = counts.get(r["reason"], 0) + 1
    body = "\n".join([
        "<table>",
        "<thead><tr><th>Page</th><th class='n'>Cards</th><th class='n'>Explanation card</th>"
        "<th class='n'>Frames</th><th class='n'>Rank</th><th>What it is</th></tr></thead>",
        "<tbody>",
        "\n".join(lines),
        f'<tr class="totaal"><td>Total</td><td class="n">{n_cards}</td>'
        f'<td class="n">{len(skipped)}</td>'
        f'<td class="n">#1–#{total_frames}</td><td></td>'
        f'<td>{n_cards} picture cards + {len(skipped)} explanation cards = {n_cards + len(skipped)} selected; '
        f'{len(backlog)} more held back before selection</td></tr>',
        "</tbody>",
        "</table>",
        '<div class="uitleg">',
        "<h2 id=\"tellingen\">What the counts mean</h2>",
        "<p>The two numbers without a card count different verbs and never overlap. Together they are "
        f"the {len(skipped) + len(backlog)} verbs with no card yet, all listed on "
        "<a href=\"backlog.html\">backlog.html</a>.</p>",
        "<table><thead><tr><th>Count</th><th class='n'>Verbs</th><th>Definition</th></tr></thead><tbody>",
        f'<tr><td>Selected</td><td class="n">{n_cards + len(skipped)}</td><td>Every verb '
        "<code>select.py</code> put on one of the ten band pages, in <code>selection.json</code>. "
        "Each one has a scene row. Selected = picture cards + explanation cards.</td></tr>",
        f'<tr><td>Cards</td><td class="n">{n_cards}</td><td>Selected verbs whose scene row is a picture '
        "brief: one card, one frame number.</td></tr>",
        f'<tr><td>Explanation card</td><td class="n">{len(skipped)}</td><td>Selected verbs whose scene row begins '
        "with <code>SKIP:</code>: no honest single drawing carries them, so they are taught with an explanation card "
        "(a picture, a short Dutch scene and a question) instead. The reason is about the picture. See "
        "<a href=\"../explanation-cards/index.html\">Explanation cards</a>.</td></tr>",
        f'<tr><td>Held back</td><td class="n">{len(backlog)}</td><td>Verbs <code>select.py</code> set aside '
        "before any scene was written, in <code>backlog_seed.tsv</code>: separable, reflexive, sensitive, "
        "odd lemmas, A2 regulars below the cut, and drawable verbs left for a later pass. They are on no "
        "band page.</td></tr>",
        "</tbody></table>",
        "<h2>What these pages are</h2>",
        "<p>One card per Dutch verb, in its base form. Each card carries a picture brief: "
        "<em>Scene</em> (what is drawn), <em>Must read</em> (the one mark that has to be legible "
        "at thumbnail size), <em>Avoid</em> (the near-miss actions, each with the competing verb) "
        "and <em>Alt text</em> (Dutch, for a screen reader). The art is the Voorzetselpaden "
        "style: flat cobalt #2B50C8 on white, no text. The brief is in "
        "<a href=\"base-prompt.txt\">base-prompt.txt</a>.</p>",
        f"<p>{len(DRAWN)} of {total_frames} cards are drawn so far: a card counts as drawn when "
        "<code>assets/verbs/&lt;slug&gt;.png</code> exists, and the rest are proposals.</p>",
        "<p>Irregular cards also carry the forms a learner cannot predict: the past singular and the "
        "perfect (auxiliary plus participle), taken from Bijlage 3b into "
        "<code>tools/lexicon/werkwoorden-vormen.tsv</code>. Regular cards carry the base form only, because "
        "<em>-te/-de</em> and <em>ge-</em> are one rule taught once. There are no example sentences and no "
        "contrast pairs in this pass.</p>",
        "<h2>How the bands were cut</h2>",
        "<p>By lexicon frequency rank, from <code>tools/lexicon/woorden-frequentie.tsv</code>: "
        "A0 up to 250, A1 up to 1000, A2 up to 2500, B1 up to 5000, B2 up to 10,000. Irregular and regular "
        "verbs are separate pages, because a learner meets them in a different order. The "
        "ranks were cross-checked against the coursebook appendices in "
        "<code>/media/tony/Data/Dutch</code> (Bijlage 3b for irregular verbs, Bijlage 4 for "
        "separable verbs), which is also what the cross-check in "
        "<code>Docs/voorzetselpaden/</code> used.</p>",
        "<h2 id=\"rang-handmatig\">Ranks set by hand</h2>",
        "<p>The rank is the frequency of the spelling, not of the verb. Where the spelling is mostly "
        "a noun plural, or where wordfreq gave the verb row no score of its own, "
        "<code>select.py</code> sets the rank by hand. Each override moves the verb to another band; "
        "<code>check-verb-cards.py</code> fails one that does not. The ranks for noun plurals are "
        "judgement, not a lemma count.</p>",
        "<table><thead><tr><th>Verb</th><th class='n'>Lexicon rank</th><th>Band</th>"
        "<th class='n'>Rank used</th><th>Band</th><th>Why</th></tr></thead><tbody>",
        "\n".join(override_rows(records)),
        "</tbody></table>",
        "<h2 id=\"b1-b2\">B1 completed and B2 added (20 November 2026)</h2>",
        "<p>The cap of sixty regulars was lifted for B1 and B2: every usable verb in those bands is now on "
        "a page, as a card or as a SKIP row with its reason. B1 now has "
        f"{len(kept['b1-irregular']) + len(kept['b1-regular'])} cards and B2 "
        f"{len(kept['b2-irregular']) + len(kept['b2-regular'])}. The budget for this pass was up to 120 new "
        "cards; the pass added 83 (27 in B1, 56 in B2). The review fix pass the same day added 11 more "
        "(verbs wrongly skipped for \"two senses\" or \"another family drew it\", plus gieten and wenken) "
        "and moved schaatsen back to B1. A third pass replaced every remaining \"two senses\" reason: "
        "ruimen, schakelen, pikken, isoleren and stoken were carded in their most drawable sense, and the "
        "other twenty kept SKIP with a reason about the picture. The B1/B2 pages stop short because "
        f"{sum(1 for r in skipped if r['band'] in ('B1', 'B2'))} B1 and B2 verbs have no honest single "
        "drawing. Most of the B1/B2 tail is abstract, administrative, "
        "a screen action, a kind of speaking, or the same picture as a card that already exists. "
        f"{sum(1 for r in backlog if r['reason'] == 'later pass')} drawable verbs wait for a later pass, "
        "each with its reason on the backlog.</p>",
        "<h2 id=\"overlap\">Lemmas another family also carries</h2>",
        "<p>These verbs have a card here and a related card in another family. The scenes differ, "
        "so nothing is redrawn, but a game should not serve both cards of a pair in one round.</p>",
        "<table><thead><tr><th>Werkwoorden</th><th>Other family</th><th>Their card</th></tr></thead><tbody>",
        "\n".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in OVERLAP),
        "</tbody></table>",
        "<h2>What is not here</h2>",
        "<p>Separable verbs, reflexive verbs, a handful of sensitive or rare lemmas, the "
        "regular verbs below the A2 cut, and a few drawable B1/B2 verbs left for a later pass: these "
        f"{len(backlog)} verbs were held back before selection and are listed with their reason on "
        f"<a href=\"backlog.html\">backlog.html</a>. The {len(skipped)} skipped verbs were selected but have "
        "no honest single drawing; they are listed there too, under \"Verbs the writer could not draw\". "
        "The same page also tracks the other word classes still to be given cards.</p>",
        "<h2>Where the words came from</h2>",
        "<p><code>tools/_ww_tmp/select.py</code> writes the selection; "
        "<code>tools/build-verb-cards.py</code> turns it, plus the scene notes in "
        "<code>tools/_ww_tmp/scenes/</code>, into these pages. Conventions and the rerun "
        "recipe are in <a href=\"AGENTS.html\">AGENTS.html</a>.</p>",
        "</div>",
    ])
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(shell(
            "Werkwoorden — beeldplannen",
            "One card per Dutch verb for every band from A0 to B2: the base form (irregular verbs add the past and perfect), a picture brief, and the frequency rank that put it there.",
            body,
        ))


# Near-duplicate lemmas across families (review L11, 20 Nov 2026).  The scenes
# differ; listed so a game does not serve both in one round.
OVERLAP = [
    ("tillen", "Scheidbare werkwoorden", "optillen"),
    ("vouwen", "Scheidbare werkwoorden", "opvouwen, uitvouwen"),
    ("drogen", "Scheidbare werkwoorden", "afdrogen"),
    ("schillen", "Bijvoeglijke naamwoorden", "geschild"),
    ("waaien", "Bijvoeglijke naamwoorden", "winderig"),
    ("strijken", "Voorzetselpaden", "een hekel hebben aan (strijken)"),
    ("schommelen", "Voorzetselpaden", "vechten om (de schommel)"),
    ("zwaaien", "Voorzetselpaden", "zwaaien naar (four cards)"),
    ("ondertekenen", "Voorzetselpaden", "een contract ondertekenen met (five cards)"),
]


REASON_ANCHOR = {
    "separable": "scheidbaar",
    "reflexive": "wederkerend",
    "sensitive": "gevoelig",
    "odd/rare": "zeldzaam",
    "beyond page cap": "voorbij-de-grens",
    "later pass": "later",
}


def write_backlog(backlog, skipped):
    reasons = [
        ("separable", "Scheidbare werkwoorden", "The separable half needs a card of its own: two halves that only make sense together, and a particle the picture has to place. One of these is also reflexive."),
        ("reflexive", "Wederkerende werkwoorden", "The drawing needs the person acting on themselves, and the card needs the pronoun. Deferred until the card shape has a field for it."),
        ("sensitive", "Gevoelige werkwoorden", "Usable in a lesson, but not in an app that has to be safe on a phone at a bus stop."),
        ("odd/rare", "Zeldzaam of kapot lemma", "In the lexicon but not worth a card: either a parsing artefact or a form no A0-A1 learner meets."),
        ("beyond page cap", "Voorbij de paginagrens", "A2 regular verbs below the top sixty. They are sound candidates; the A2 page was capped at sixty to keep that pass finishable. B1 and B2 have no cap since 20 November 2026."),
        ("later pass", "Voor een latere ronde", "Drawable B1 and B2 verbs that did not get a card in the 20 November 2026 pass. The note says why each one waits."),
    ]
    groups = {}
    for r in backlog:
        groups.setdefault(r["reason"], []).append(r)

    parts = []
    parts.append(
        '<section class="sectiekop"><h2>Backlog</h2>'
        "<p>Everything that still needs a card, and why it does not have one yet. "
        "The held-back groups are from <code>tools/_ww_tmp/backlog_seed.tsv</code>, written by "
        "<code>select.py</code>; the skipped verbs are the SKIP rows in "
        "<code>tools/_ww_tmp/scenes/</code>.</p></section>"
    )
    parts.append("<table><thead><tr><th>Group</th><th class='n'>Verbs</th><th>Why they wait</th></tr></thead><tbody>")
    for key, title, why in reasons:
        n = len(groups.get(key, []))
        parts.append(f'<tr><td><a href="#{REASON_ANCHOR.get(key, key)}">{title}</a></td><td class="n">{n}</td><td class="blurb">{why}</td></tr>')
    parts.append(f'<tr class="totaal"><td>Held back before selection</td><td class="n">{len(backlog)}</td>'
                 '<td class="blurb">In <code>backlog_seed.tsv</code>; on no band page. Still need cards: see the handover.</td></tr>')
    parts.append(f'<tr><td><a href="#geen-beeld">Verbs taught by explanation card</a></td><td class="n">{len(skipped)}</td>'
                 '<td class="blurb">Selected for a band page; no honest single drawing, so each gets an explanation card.</td></tr>')
    parts.append(f'<tr class="totaal"><td>Total without a card</td><td class="n">{len(backlog) + len(skipped)}</td>'
                 '<td class="blurb">Held back plus explanation-card verbs. The two groups never overlap; the overview '
                 'defines both.</td></tr>')
    parts.append("</tbody></table>")

    for key, title, why in reasons:
        rows = groups.get(key, [])
        if not rows:
            continue
        parts.append(f'<section class="sectiekop" id="{REASON_ANCHOR.get(key, key)}"><h2>{title}</h2><p>{why}</p></section>')
        parts.append("<table><thead><tr><th>Verb</th><th>English</th><th class='n'>Rang</th><th>Band</th><th>Reason</th></tr></thead><tbody>")
        for r in rows:
            parts.append(
                f'<tr><td>{esc(r["verb"])}</td><td>{esc(r["gloss"])}</td>'
                f'<td class="n">{r["rank"]}</td><td>{r["band"]}</td><td class="mono">{esc(r["reason"])}'
                + (f'<br>{esc(r["note"])}' if r.get("note") else "")
                + "</td></tr>"
            )
        parts.append("</tbody></table>")

    if skipped:
        parts.append(
            '<section class="sectiekop" id="geen-beeld"><h2>Verbs taught by explanation card</h2>'
            "<p>Abstract or figurative verbs with no honest single action. They have no picture card; each is taught with a picture, a short Dutch scene and a question.</p></section>"
        )
        parts.append("<table><thead><tr><th>Verb</th><th>Band</th><th class='n'>Rang</th><th>Why no single picture</th><th>Explanation card</th></tr></thead><tbody>")
        excards = explanation_cards()
        for r in skipped:
            parts.append(
                f'<tr><td>{esc(r["verb"])}</td><td>{r["band"]} {LABEL[r["regularity"]]}</td>'
                f'<td class="n">{r["rank"]}</td><td>{esc(r["reason"])}</td>'
                f'<td>{("<a href=\"../explanation-cards/" + excards[r["verb"]][0] + ".html#" + excards[r["verb"]][1] + "\">card</a>") if r["verb"] in excards else "to be written"}</td></tr>'
            )
        parts.append("</tbody></table>")

    parts.append(
        '<div class="uitleg">'
        "<h2>Word classes still to come</h2>"
        "<p>The werkwoorden pages are the second card family after Voorzetselpaden. The same "
        "shape, one card per item with a scene brief, is still owed for:</p>"
        "<ul>"
        "<li><strong>Bijvoeglijke naamwoorden</strong> — adjectives with a comparability the "
        "picture can show: groot, duur, leeg, nat, moe.</li>"
        "<li><strong>Bijwoorden</strong> — adverbs and adverbial phrases of time and manner: "
        "gisteren, straks, plotseling, meteen.</li>"
        "<li><strong>Zelfstandige naamwoorden</strong> — nouns with their article and plural, "
        "which is where the lexicon already carries verified data.</li>"
        "<li><strong>Vaste uitdrukkingen</strong> — fixed chunks that are not verb + "
        "preposition: op tijd, ter plekke, met opzet.</li>"
        "<li><strong>Scheidbare werkwoorden</strong> — the group above, but with their own "
        "brief: two halves, one drawing or two.</li>"
        "<li><strong>Vervoegingen</strong> — conjugation drills. On 20 November the owner decided "
        "that unpredictable forms are vocabulary: irregular cards now carry the past singular and "
        "the perfect. Regular forms, other persons and the other tenses stay out; whether a game "
        "drills them is still open (see <code>Docs/verb-games-plan.html</code>).</li>"
        "<li><strong>Voorbeeldzinnen</strong> — dropped from this pass on purpose. If they come "
        "back, they come back as a separate field, not as part of the picture brief.</li>"
        "</ul>"
        "<h2>To make this list smaller</h2>"
        "<p>Add a verb to <code>tools/_ww_tmp/select.py</code> (or lift it out of the "
        "deferred set), rerun it, write the scene row in "
        "<code>tools/_ww_tmp/scenes/&lt;page&gt;.tsv</code>, and rerun "
        "<code>tools/build-verb-cards.py</code>. The frame numbers renumber themselves.</p>"
        "</div>"
    )
    with open(os.path.join(OUT, "backlog.html"), "w", encoding="utf-8") as fh:
        fh.write(shell(
            "Werkwoorden — backlog",
            "What still needs a card: the verbs held back before selection, the selected verbs skipped for want of a picture, and the other word classes.",
            "\n".join(parts),
        ))


if __name__ == "__main__":
    build()
