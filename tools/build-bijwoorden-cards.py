#!/usr/bin/env python3
"""Build Docs/bijwoorden/ (Bijwoorden: adverbs and adverbial phrases) from tools/_bw_tmp/.

Inputs : tools/_bw_tmp/selection.json            clusters per band (select.py)
         tools/_bw_tmp/scenes/*.clusters.tsv      frame + contrast sentence per cluster
         tools/_bw_tmp/scenes/*.cards.tsv         one row per adverb
Outputs: Docs/bijwoorden/{a0,a1,a2,b1,index}.html (no B2 band: see the overview)

Adverbs are taught as contrast sets, so the page unit is the cluster: a
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

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "bw_select", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_bw_tmp", "select.py"))
_sel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sel)
OVERRIDE, REASON = _sel.OVERRIDE, _sel.REASON

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "tools", "_bw_tmp")
SCENES = os.path.join(TMP, "scenes")
OUT = os.path.join(ROOT, "Docs", "bijwoorden")
BANDS = ["a0", "a1", "a2", "b1"]   # no B2 band for this family (owner ruling 20 Nov 2026)

BAND_LEAD = {
    "a0": "Company, place, amount and state: also and only, on and off, at home and on the way, a lot and few, enough and too many, finished and busy.",
    "a1": "Where things are and which way: used up and left over, upstairs and downstairs, left and right, everywhere and nowhere, in and out, more and fewer, day and night.",
    "a2": "Aim, movement and route: on target and off, up and down, forward and backward, straight on and turning, together and apart, front and back of a queue, next door and further on.",
    "b1": "Finer places and postures: top, halfway and bottom of the stairs, front and back seat, middle and aside, upright and upside down, on the front and back of a bike, across and slantwise, underground and above ground, on one's feet and going flying, leaning back and bending forward, on board and overboard, at the top and at the bottom of a cupboard.",
}


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
    return "\n".join([
        f'<article id="{attr(cid)}" class="kaart" data-id="{attr(cid)}" data-band="{band}" '
        f'data-kind="adverb" data-cluster="{attr(c["id"])}" data-status="proposal" data-severity="">',
        f'<span class="framenummer" title="Frame {number}">#{number}</span>',
        '<div class="geenbeeld">geen beeld</div>',
        f'<h3 class="chunk">{esc(m["lemma"])}</h3>',
        f'<p class="gloss">{esc(m["gloss"])}</p>',
        f'<p class="vlaggen"><span>{esc(c["axis"])}</span><span>{band.upper()}</span></p>',
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
    cl_rows, card_rows = load_scenes()

    kept = {b: [] for b in BANDS}      # band -> [(cluster, [(member, row)])]
    skipped = []
    skipped_sets = []
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
            elif c["id"] not in skipped_sets:
                skipped_sets.append(c["id"])

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
            # Show the id's suffix only where it tells two senses of one word apart (alleen-solo, op-leeg).
            def head(m):
                slug = "-".join(w for w in "".join(ch if ch.isalpha() else " " for ch in m["lemma"].lower()).split())
                return f'{m["lemma"]} ({m["id"][len(slug) + 1:]})' if m["id"].startswith(slug + "-") else m["lemma"]
            words = " · ".join(head(m) for m, _ in members)
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
        summ = (f'<div class="sum"><span>{len(sets)} contrast sets</span><span>{ncards} adverbs</span>'
                f'<span>frames #{first}–#{last}</span><span>0 getekend</span></div>')
        page = shell(f"Bijwoorden — {b.upper()}", esc(BAND_LEAD[b]), nav(b),
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
    uitleg = f"""
<div class="uitleg">
<h2>How the cards work</h2>
<p>Adverbs are taught in <strong>contrast sets</strong>: two or three words on one axis (hier/daar, binnen/buiten, rechtdoor/linksaf/rechtsaf).
Every drawing in a set is the same picture with one visible thing changed, so the learner sees the pair, not the word.
This family has no time adverbs, because one drawing per card cannot show before and after (see the backlog below).</p>
<p>A card carries the adverb, an English gloss, the scene brief, the one mark that must read, the near misses,
the contrast note naming its partner and the single point of difference, an example sentence, and the alt text.
Each set also carries a fixed frame and one Dutch sentence using every member.</p>
<h2>How the sets were chosen</h2>
<p>The sets were picked by hand from the lexicon words tagged <code>adv</code>, plus core adverbs and fixed phrases the tagger
misses (rechtsaf, naar binnen, 's nachts, bij elkaar). Only pairs whose contrast is spatial or situational were kept.
Manner adverbs that are really adjectives (snel, langzaam, hard, zacht) are left to
<a href="../bijvoeglijke-naamwoorden/index.html">Bijvoeglijke naamwoorden</a>, and place words that are prepositions (op, in, naast) to Voorzetselpaden.
Where an adverb shares a form with an adjective (alleen, af, bezig, mis, apart), the card draws the adverb sense only.
The amount words (veel, weinig, genoeg, te veel, meer, minder, evenveel) are included as indefinite numerals: they are drawn and exemplified
before a noun (veel appels, genoeg kopjes), not as adverbs in the strict sense, and stay here until a quantity family exists.</p>
<h2>How a set was placed</h2>
<p>A set sits in the band of its most frequent member (frequency rank in <code>tools/lexicon/woorden-frequentie.tsv</code>:
A0 up to 250, A1 251–1000, A2 1001–2500, B1 2501–10000): the learner already knows one half and the card teaches its partner.
Lexicon entries with a part-of-speech suffix (<code>morgen (adv)</code>, <code>al (adv)</code>, <code>meer num</code>, <code>midden (adv)</code>)
are found by stripping the suffix; their ranks (8500 and up) look like placeholders, but none of them decides a band.
{len(OVERRIDE)} sets are placed by hand in <code>OVERRIDE</code> in <code>tools/_bw_tmp/select.py</code>, each for the reason below.
{len(_sel.EVERYDAY)} of them ({', '.join(_sel.EVERYDAY)}) are everyday promotions under the owner rule that everyday items sit at A2 at the highest:
their reason is rendered from the lexicon (<code>niveau</code>, <code>top2000</code> and <code>herkomst</code> from <code>woorden.tsv</code>, and the rank),
and <em>Basis: judgment, not lexicon data</em> says plainly that the lexicon does not support the move; the note gives the judgment.
The checker re-reads every cited fact. Niveau <em>open</em> means in Bijlage 8 (a frequency list) but taught in neither coursebook.</p>
<table><thead><tr><th>Set</th><th>Band</th><th>Reason</th></tr></thead><tbody>{''.join(f'<tr><td><em>{esc(k)}</em></td><td>{v.upper()}</td><td>{esc(REASON[k])}</td></tr>' for k, v in OVERRIDE.items())}</tbody></table>
<h2>Why this family has no B2 band</h2>
<p>There are too few honest spatial adverbs past rank 5000 to fill a band, so B1 takes every set ranked 2501–10000.
The expansion of 20 November 2026 aimed at ten new sets each in B1 and B2; six candidate B2 sets were written,
three of them repeated another family's card and were dropped, and the three that remained are folded into B1.
Most adverbs ranked 2501–10000 are time, frequency, degree or sentence adverbs
(spoedig, dikwijls, enigszins, weliswaar, kortom, desnoods), which have no single picture.
The spatial and situational candidates that remained were left out for the reasons below.</p>
<table><thead><tr><th>Candidate</th><th>Reason left out</th></tr></thead><tbody>
<tr><td><em>stroomopwaarts, stroomafwaarts</em></td><td>Moving against the current is the scene of Voorzetselpaden <code>vechten-tegen-de-stroming</code>.</td></tr>
<tr><td><em>achterna</em></td><td>Following someone is the scene of the Voorzetselpaden chunk <code>achter … aan</code> (achter de dief aan).</td></tr>
<tr><td><em>tegemoet</em></td><td>Ranks 2412 (A2), so a set with it would sit in A2; its natural partner achterna is out (above).</td></tr>
<tr><td><em>naar voren, naar achteren</em></td><td>voren ranks 1604, so the set sits in A2, and moving to the front or back repeats vooruit/achteruit and vooraan/achteraan.</td></tr>
<tr><td><em>verticaal, horizontaal</em></td><td>duplicate of bijvoeglijke-naamwoorden:verticaal and bijvoeglijke-naamwoorden:horizontaal (a plank on a wall); the adjective examples already use both words adverbially.</td></tr>
<tr><td><em>hierheen, daarheen</em></td><td>duplicate of scheidbare-werkwoorden:terugkomen and scheidbare-werkwoorden:weglopen (adult at the edge of a lawn, only the dog's direction changes); a side view also cannot mark the adult as the speaker.</td></tr>
<tr><td><em>languit, opgerold</em></td><td>opgerold is a duplicate of bijvoeglijke-naamwoorden:opgerold (one word, two drawings); languit has no other partner.</td></tr>
<tr><td><em>bijeen, uiteen</em></td><td>B1 by rank (2701, 3030), but they repeat the A2 set bij elkaar/apart.</td></tr>
<tr><td><em>middenin</em></td><td>Repeats midden, already drawn in B1.</td></tr>
<tr><td><em>scheef</em></td><td>Its partner, level or straight, is the adjective card <code>recht</code>.</td></tr>
<tr><td><em>overhoop</em></td><td>Tidy against messy is drawn by the adjective pair keurig/rommelig.</td></tr>
<tr><td><em>hardop</em></td><td>Reading aloud against reading silently is drawn as sound or none, the adjective pair luid/stil; Voorzetselpaden also draws someone talking aloud to himself.</td></tr>
<tr><td><em>gelijktijdig, afwisselend</em></td><td>At the same time needs a second moment to compare with; alternating needs a sequence and has no partner adverb.</td></tr>
<tr><td><em>voorwaarts, zijwaarts</em></td><td>Repeat vooruit/achteruit.</td></tr>
<tr><td><em>eromheen, erdoor, eronder, ernaast, ertussen, daarboven, daaronder</em></td><td>Pronominal adverbs (er/daar plus a preposition): the picture is the preposition's, which Voorzetselpaden teaches.</td></tr>
<tr><td><em>binnenstebuiten, achterstevoren</em></td><td>A garment inside out and one back to front look alike at thumbnail size from the front; no honest single picture separates them.</td></tr>
<tr><td><em>halfweg, ginder</em></td><td>Belgian Dutch; the Netherlands says halverwege and daar.</td></tr>
</tbody></table>
<h2>Left out on purpose</h2>
<ul><li>Time adverbs (gisteren, vandaag, morgen, nu, straks, altijd, nooit, vaak, zelden, soms, al, nog, eerst, daarna): a card has one drawing, a clock-free cue and no second panel, so before and after cannot be shown. Only the day-and-night pair (overdag, 's nachts) survives, drawn with sun and moon.</li>
<li>Stance adverbs (misschien, zeker, wel, niet): no object to draw, and a shrug, a tick or a cross needs text or is not in the style.</li>
<li>Sets that would redraw another family's card (hier/daar, binnen/buiten, samen/alleen, helemaal/bijna/een beetje, expres/per ongeluk): one drawing per word, so the other family keeps it. The backlog names the card each one duplicates.</li>
<li>Manner adverbs that duplicate adjective sets (snel, langzaam, hard, zacht, stil, luid, dichtbij, ver).</li></ul>
<h2>Cards written up as SKIP (backlog)</h2><p>{len(skipped_sets)} whole sets, {len(skipped)} cards. A set is skipped as a whole so that no drawn card is left without its partner.</p><ul>{sk}</ul>
<h2>Tools</h2>
<pre><code>python3 tools/_bw_tmp/select.py             # selection.json from clusters.txt
python3 tools/_bw_tmp/author.py             # scene TSVs from the author_*.py data
python3 tools/build-bijwoorden-cards.py     # the four band pages and this overview
python3 tools/check-bijwoorden-cards.py     # asserts ids, fields, pairs, counts</code></pre>
</div>"""
    index = shell("Bijwoorden — overview",
                  "One card per adverb, taught as contrast pairs. Picture briefs only; no art yet.",
                  nav("index"),
                  f'<table><thead><tr><th>Band</th><th>Sets</th><th>Adverbs</th><th>Frames</th><th>Content</th></tr></thead><tbody>{rows}</tbody></table>' + uitleg)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index)
    print(f"sets {tot_s}  cards {tot_c}  skipped {len(skipped)}")
    for b in BANDS:
        print(f"  {b}: {stats[b][0]} sets, {stats[b][1]} cards, frames #{stats[b][2]}-#{stats[b][3]}")


CSS = load_css()

if __name__ == "__main__":
    build()
