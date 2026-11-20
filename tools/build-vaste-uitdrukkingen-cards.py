#!/usr/bin/env python3
"""Build Docs/vaste-uitdrukkingen/ from tools/_vu_tmp/.

Inputs : tools/_vu_tmp/selection.json            clusters per band (select.py)
         tools/_vu_tmp/scenes/*.clusters.tsv      frame + contrast sentence per cluster
         tools/_vu_tmp/scenes/*.cards.tsv         one row per chunk
Outputs: Docs/vaste-uitdrukkingen/{a0,a1,a2,b1,b2,index}.html

Fixed expressions are taught as contrast sets, so the page unit is the cluster: a
shared frame, a contrast sentence, then one card per member. A card row whose
scene starts with "SKIP:" is dropped from its page and listed on the index.
Rerunning overwrites every page, so run it only when you mean to rebuild.
"""
import csv
import glob
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "tools", "_vu_tmp")
SCENES = os.path.join(TMP, "scenes")
OUT = os.path.join(ROOT, "Docs", "vaste-uitdrukkingen")
BANDS = ["a0", "a1", "a2", "b1", "b2"]

BAND_LEAD = {
    "a0": "Time, school and work, and road vehicles: the chunks a learner needs in the first weeks.",
    "a1": "Where things and people are: sides, corners, stairs, tables, beds, the sea, and who is by the hand.",
    "a2": "Finer pairs: boat or plane, how things stand together, wall or ceiling, feet, numbers of people, steps, a window ajar, the pan on the boil, pyjamas or a suit.",
    "b1": "Intent, arriving, upside down, wind, tidiness, cutting, and the horse, the shore, the bend, the lion, the cupboard, the ship.",
    "b2": "Rarer chunks with one visible change: on stage or in the wings, trot and gallop, in step, single file.",
}

# Targets set on 20 November 2026 for the B1 and B2 expansion; the shortfall is printed on the overview.
TARGET_NEW = 20
NEW_SINCE = {"b1": {"paard-stal", "wal", "bloem-knop", "bocht", "dier-wild", "toneel", "meubel-onder", "schip", "pan-vuur"}}

# Forms and senses no native speaker has confirmed yet; printed on the overview, checked against the selection.
NATIVE_CHECK = [
    ("door-de-bocht-gaan", "the figurative sense 'give in' is the reviewer's recollection, not verified; 'kort door de bocht' is certain"),
    ("in-de-knop", "garden Dutch has both 'in de knop' and 'in knop'; if 'in knop' is the standard form, the chunk changes and loses its article like 'in bloei'"),
    ("aan-de-kade", "a collocation rather than a frozen chunk; kept as the partner of voor anker"),
]


def esc(t):
    return html.escape(t, quote=False)


def attr(t):
    return html.escape(t, quote=True)


def read_tsv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))


def load_css():
    # Reuse the Werkwoorden stylesheet so the families look the same.
    src = open(os.path.join(ROOT, "tools", "build-verb-cards.py"), encoding="utf-8").read()
    start = src.index('CSS = """') + len('CSS = """')
    css = src[start:src.index('"""', start)]
    return css + """
.cluster{margin-top:30px;padding-top:14px;border-top:3px solid var(--kobalt)}
.cluster h2{margin:0;font-size:23px;letter-spacing:-.01em}
.cluster h2 .woorden{color:var(--kobalt)}
.cluster .as{margin:2px 0 0;color:var(--grijs);font-size:13px;text-transform:uppercase;letter-spacing:.05em}
.cluster .zin{margin:10px 0 0;max-width:80ch;font-size:16px}
.cluster .zin .en{color:var(--grijs);font-size:14px;display:block}
.cluster .frame{margin:8px 0 0;max-width:85ch;font-size:14px;color:var(--grijs)}
.contrast dd{border-left:3px solid var(--kobalt);padding-left:8px}
.voorbeeld .en{color:var(--grijs);display:block;font-size:13px}
"""


def load_scenes():
    clusters, cards = {}, {}
    for path in sorted(glob.glob(os.path.join(SCENES, "*.clusters.tsv"))):
        for r in read_tsv(path):
            clusters[r["cluster"].strip()] = r
    for path in sorted(glob.glob(os.path.join(SCENES, "*.cards.tsv"))):
        for r in read_tsv(path):
            cards[r["id"].strip()] = r
    return clusters, cards


def render_card(m, c, s, number, partners):
    cid = m["id"]
    band = c["band"]
    xref = f' data-xref="{attr(c["xref"])}"' if c.get("xref") else ""
    return "\n".join([
        f'<article id="{attr(cid)}" class="kaart" data-id="{attr(cid)}" data-band="{band}" '
        f'data-kind="chunk" data-cluster="{attr(c["id"])}" data-status="proposal" data-severity=""{xref}>',
        f'<span class="framenummer" title="Frame {number}">#{number}</span>',
        '<div class="geenbeeld">geen beeld</div>',
        f'<h3 class="chunk" data-chunk="{attr(m["lemma"])}">{esc(m["lemma"])}</h3>',
        f'<p class="gloss">{esc(m["gloss"])}</p>',
        f'<p class="vlaggen"><span>{esc(c["axis"])}</span><span>{band.upper()}</span>'
        f'<span class="register">{esc(s["register"].strip())}</span><span class="betekenis">{esc(s["literal"].strip())}</span></p>',
        "<dl>",
        f'<dt>Scene</dt><dd class="scene">{esc(s["scene"].strip())}</dd>',
        f'<dt>Must read</dt><dd class="must">{esc(s["must"].strip())}</dd>',
        f'<dt>Avoid</dt><dd class="avoid">{esc(s["avoid"].strip())}</dd>',
        f'<dt>Contrast</dt><dd class="contrast-note" data-partner="{attr(" ".join(partners))}">{esc(s["contrast"].strip())}</dd>',
        f'<dt>Example</dt><dd class="voorbeeld-nl">{esc(s["example_nl"].strip())}'
        f'<br><span class="voorbeeld-en">{esc(s["example_en"].strip())}</span></dd>',
        f'<dt>Alt text</dt><dd class="alt">{esc(s["alt"].strip())}</dd>',
        "</dl>",
        f'<p class="id">{esc(cid)}.png · {band.upper()} · {esc(c["id"])}</p>',
        "</article>",
    ])


def shell(title, lead, nav, body, extra_head=""):
    return "\n".join([
        "<!DOCTYPE html>", '<html lang="nl">', "<head>", '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"<title>{title}</title>", "<style>" + CSS + "</style>", "</head>", "<body>",
        "<header>", f"<h1>{title}</h1>", f'<p class="lead">{lead}</p>',
        extra_head, '<nav class="banden">' + nav + "</nav>", "</header>",
        "<main>", body, "</main>", "</body>", "</html>",
    ]) + "\n"


def build():
    with open(os.path.join(TMP, "selection.json"), encoding="utf-8") as fh:
        selection = json.load(fh)
    left_out = read_tsv(os.path.join(TMP, "left-out.tsv"))
    cl_rows, card_rows = load_scenes()

    kept = {b: [] for b in BANDS}      # band -> [(cluster, [(member, row)])]
    skipped = []
    for b in BANDS:
        for c in selection.get(b, []):
            if c["id"] not in cl_rows:
                sys.exit(f"no cluster row for {c['id']}")
            members = []
            for m in c["members"]:
                s = card_rows.get(m["id"])
                if s is None:
                    sys.exit(f"{c['id']}: no card row for {m['id']}")
                if s["scene"].strip().upper().startswith("SKIP"):
                    skipped.append((b, c["id"], m, s["scene"].strip()[4:].lstrip(": ").strip()))
                else:
                    members.append((m, s))
            if members:
                kept[b].append((c, members))

    # Frame numbers run on across the pages, A0 first, only for drawn cards.
    numbers, n = {}, 0
    for b in BANDS:
        for c, members in kept[b]:
            for m, _s in members:
                n += 1
                numbers[m["id"]] = n

    nav_items = [("index", "overview")] + [(b, b.upper()) for b in BANDS]

    def nav(cur):
        return "".join(
            f'<a href="{k}.html"' + (' class="hier"' if k == cur else "") + f">{lab}</a>"
            for k, lab in nav_items
        )

    os.makedirs(OUT, exist_ok=True)
    stats = {}
    for b in BANDS:
        sets = kept[b]
        body, ncards = [], 0
        for c, members in sets:
            row = cl_rows[c["id"]]
            ids = [m["id"] for m, _ in members]
            words = " · ".join(m["lemma"] for m, _ in members)
            cards = []
            for m, s in members:
                partners = [i for i in ids if i != m["id"]]
                cards.append(render_card(m, c, s, numbers[m["id"]], partners))
            ncards += len(cards)
            body.append(
                f'<section class="cluster" data-cluster="{attr(c["id"])}" data-band="{b}">'
                f'<h2><span class="woorden">{esc(words)}</span></h2>'
                f'<p class="as">{esc(c["axis"])} · {len(cards)} cards</p>'
                f'<p class="zin">{esc(row["sentence_nl"].strip())}'
                f'<span class="en">{esc(row["sentence_en"].strip())}</span></p>'
                f'<p class="frame"><strong>Fixed frame.</strong> {esc(row["frame"].strip())}</p>'
                '<div class="kaarten">' + "\n".join(cards) + "</div></section>"
            )
        first = numbers[sets[0][1][0][0]["id"]]
        last = numbers[sets[-1][1][-1][0]["id"]]
        stats[b] = (len(sets), ncards, first, last)
        summ = (f'<div class="sum"><span>{len(sets)} contrast sets</span><span>{ncards} chunks</span>'
                f'<span>frames #{first}–#{last}</span><span>0 getekend</span></div>')
        page = shell(f"Vaste uitdrukkingen — {b.upper()}", esc(BAND_LEAD[b]), nav(b),
                     "\n".join(body), summ)
        with open(os.path.join(OUT, b + ".html"), "w", encoding="utf-8") as fh:
            fh.write(page)

    rows = "".join(
        f'<tr><td><a href="{b}.html">{b.upper()}</a></td><td class="n">{stats[b][0]}</td>'
        f'<td class="n">{stats[b][1]}</td><td class="n">#{stats[b][2]}–#{stats[b][3]}</td>'
        f'<td class="blurb">{esc(BAND_LEAD[b])}</td></tr>' for b in BANDS)
    tot_s = sum(v[0] for v in stats.values())
    tot_c = sum(v[1] for v in stats.values())
    rows += f'<tr class="totaal"><td>Total</td><td class="n">{tot_s}</td><td class="n">{tot_c}</td><td></td><td></td></tr>'
    sk = "".join(f"<li><code>{esc(m['id'])}</code> ({b.upper()}, {esc(cid)}): {esc(why)}</li>"
                 for b, cid, m, why in skipped) or "<li>None.</li>"
    nc = "".join(f"<li class=\"native\"><code>{esc(i)}</code>: {esc(why)}</li>" for i, why in NATIVE_CHECK)
    lo = "".join(f'<li class="weg"><code>{esc(r["id"])}</code> {esc(r["chunk"])}: {esc(r["reason"])}</li>'
                 for r in left_out)
    overrides = "".join(f"<li><code>{esc(k)}</code> to {b.upper()}: {esc(why)}</li>" for k, (b, why) in OVERRIDE_LIST)
    everyday = "".join(f"<li class=\"alledaags\"><code>{esc(c['id'])}</code> to {b.upper()}: {esc(c['everyday'])}</li>"
                       for b in BANDS for c in selection.get(b, []) if c.get("everyday")) or "<li>None.</li>"
    new_b1 = sum(1 for c, _ in kept["b1"] if c["id"] in NEW_SINCE["b1"])
    new_b2 = len(kept["b2"])
    uitleg = f"""
<div class="uitleg">
<h2>How the cards work</h2>
<p>Fixed expressions are taught in <strong>contrast sets</strong>: two to four chunks that one visible element separates
(op tijd / te laat, aan zee / op zee). Every drawing in a set is the same picture with one thing changed, so the learner sees the pair, not the phrase.</p>
<p>A card carries the chunk, an English gloss, the scene brief, the one mark that must read, the near misses, the contrast note naming its partner,
an example sentence, the alt text, a register flag (neutral, spoken, formal) and a literal or figurative flag.
Each set also carries a fixed frame and one Dutch sentence using every member.</p>
<h2>What counts as a chunk here</h2>
<p>A chunk has a fixed form: no article (<em>aan tafel</em>, <em>op zee</em>), a frozen word (<em>ter plekke</em>, <em>te voet</em>)
or a preposition the learner cannot predict (<em>op het platteland</em>). Free preposition-plus-noun combinations, where any noun
fits (<em>in de trein</em>, <em>zonder melk</em>), belong to the single-preposition cards in Voorzetselpaden, and single adverbs
belong to Bijwoorden. Voorzetselpaden holds verb-plus-preposition chunks; no card here repeats one of its chunks, example sentences
or scenes, and the checker tests that. Three cards have their partner drawn in Bijwoorden and point to it instead of drawing it twice.</p>
<p>Chunks that need a sequence or a sign (om de beurt, voor het eerst, te koop) are written up as SKIP and listed below.</p>
<h2>How a set was placed</h2>
<p>The lexicon holds single words, so a chunk is ranked by its most frequent <em>content</em> word (<code>tools/lexicon/woorden-frequentie.tsv</code>:
A0 up to 250, A1 251&ndash;1000, A2 1001&ndash;2500, B1 2501&ndash;5000, B2 5001&ndash;10000).
Lexicon rows split by part of speech are keyed explicitly (<code>pas(noun)</code>, <code>arm(noun)</code>); a set whose content words are all
missing from the 10,000-lemma list has no rank and is placed by an override. Prepositions and articles are left out on purpose: they would put every chunk in A0.
A set sits in the band of its most frequent member. Banding is editorial, with frequency as a first pass: a rare second word
(plafond, sok, arm) pulls a set up only where the overrides below say so, and sets keyed on a homograph or a pronoun
(laat, kop, elkaar) are placed by hand. The overrides live in <code>OVERRIDE</code> in <code>tools/_vu_tmp/select.py</code>, each with its reason;
the checker rejects an override that only repeats the band the ranks give:</p>
<ul>{overrides}</ul>
<p>Everyday items sit at the lowest sensible level, A2 at the highest, whatever the corpus rank of their words (decision of 20 November 2026).
The sets below were moved down from B1 or B2 under that rule. The move is judgment, not lexicon data; each line gives every member's rank keys
as the lexicon has them (<code>niveau</code>, <code>top2000</code> and <code>herkomst</code> from <code>tools/lexicon/woorden.tsv</code>, rank from
<code>woorden-frequentie.tsv</code>), and the checker re-reads each fact. The entries live in <code>EVERYDAY</code> in <code>tools/_vu_tmp/select.py</code>,
which also lists the B1 and B2 sets considered and kept.</p>
<ul>{everyday}</ul>
<h2>Weakest pictures</h2>
<p>Sets that lean on a small cue and need an artist's care: <code>ochtends</code>/<code>avonds</code> (half sun against a dark window and a lit lamp),
the four stair cards (no arrows; the place on the stair and the way the body faces carry the meaning),
<code>in-de-pas</code>/<code>uit-de-pas</code> (which knee one child of four raises, seen from the front) and <code>in-draf</code>/<code>in-galop</code> (the leg pattern of a moving horse).</p>
<h2>B1 and B2 against the target</h2>
<p>The target for the expansion of 20 November 2026 was at least {TARGET_NEW} new contrast sets in B1 and {TARGET_NEW} in B2.
This family reached <strong>{new_b1} new sets in B1</strong> and <strong>{new_b2} in B2</strong>, so it is short by {TARGET_NEW - new_b1} and {TARGET_NEW - new_b2}.</p>
<table><thead><tr><th>Reason</th><th>What it removed</th></tr></thead><tbody>
<tr><td>Only fixed chunks count</td><td>Free preposition-plus-noun combinations (in de kelder, op het terras) are out, and most fixed chunks with a literal picture are built on common nouns.</td></tr>
<tr><td>Banding follows the commonest content word</td><td>Literal chunks such as in bad, binnen bereik, op je gemak and in de war rank in A1 or A2, so they cannot fill B1 or B2 without an override that the rule forbids.</td></tr>
<tr><td>Other families draw the picture first</td><td>Kneeling, sitting cross-legged, sailing, a locked door, a level stick, a creased or ironed shirt, near and far, on board: listed below under chunks left out.</td></tr>
<tr><td>No honest single picture</td><td>Sunrise against sunset, heads or tails, up and down, back and forth, and a breakdown against a tow.</td></tr>
</tbody></table>
<h2>Native check before art</h2><ul>{nc}</ul>
<h2>Cards written up as SKIP</h2><ul>{sk}</ul>
<h2>Chunks left out</h2>
<p>Removed after the review of 20 November 2026: single words drawn in another family, free combinations, and chunks whose only partner was removed.
Rows marked "B1/B2 candidate" were considered for the B1 and B2 expansion and dropped for the reason given.</p>
<ul>{lo}</ul>
<h2>Tools</h2>
<pre><code>python3 tools/_vu_tmp/convert.py       # scenes/*.txt to the TSVs
python3 tools/_vu_tmp/select.py        # selection.json from clusters.txt
python3 tools/build-vaste-uitdrukkingen-cards.py # the five band pages and this overview
python3 tools/check-vaste-uitdrukkingen-cards.py # asserts ids, fields, pairs, alt leaks, cross-family duplicates</code></pre>
</div>"""
    index = shell("Vaste uitdrukkingen — overview",
                  "One card per fixed expression, taught as contrast sets. Picture briefs only; no art yet.",
                  nav("index"),
                  f'<table><thead><tr><th>Band</th><th>Sets</th><th>Chunks</th><th>Frames</th><th>Content</th></tr></thead><tbody>{rows}</tbody></table>' + uitleg)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index)
    print(f"sets {tot_s}  cards {tot_c}  skipped {len(skipped)}")
    for b in BANDS:
        print(f"  {b}: {stats[b][0]} sets, {stats[b][1]} cards, frames #{stats[b][2]}-#{stats[b][3]}")


CSS = load_css()


def _overrides():
    import importlib.util
    spec = importlib.util.spec_from_file_location("vu_select", os.path.join(TMP, "select.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return sorted(mod.OVERRIDE.items())  # (cluster, (band, reason))


OVERRIDE_LIST = _overrides()

if __name__ == "__main__":
    build()
