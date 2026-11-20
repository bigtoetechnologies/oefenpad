#!/usr/bin/env python3
"""Build Docs/bijvoeglijke-naamwoorden/ from tools/_bn_tmp/.

Inputs : tools/_bn_tmp/selection.json            clusters per band (select.py)
         tools/_bn_tmp/scenes/*.clusters.tsv      frame + contrast sentence per cluster
         tools/_bn_tmp/scenes/*.cards.tsv         one row per adjective
Outputs: Docs/bijvoeglijke-naamwoorden/{a0,a1,a2,b1,b2,index}.html

Adjectives are taught as contrast sets, so the page unit is the cluster: a
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
TMP = os.path.join(ROOT, "tools", "_bn_tmp")
SCENES = os.path.join(TMP, "scenes")
OUT = os.path.join(ROOT, "Docs", "bijvoeglijke-naamwoorden")
BANDS = ["a0", "a1", "a2", "b1", "b2"]

BAND_LEAD = {
    "a0": "Size, age, speed and the open door: the pairs a learner meets in the first weeks.",
    "a1": "Everyday contrasts: temperature, weight, feelings, health, clean and wet, weather, distance, danger and a fair share.",
    "a2": "Finer pairs: depth, sound, light, taste, edges, fit, courage, presence, company, tension and wind, plus the everyday pairs sturdy, fresh air, tidy, spicy and raw.",
    "b1": "The wider pairs: straightness, surface, shyness, nerves, manners, care, comfort, behaviour, decoration, patience, water quality, suppleness, guitars and patterns.",
    "b2": "Material and state: temper, slope, solid and hollow, liquid, see-through, direction, creases, ice, crispness and fertile soil.",
}

# Why B1 and B2 stop short of the 20-set target (owner brief, 20 Nov 2026).
SHORTFALL = [
    ("Colour", "rijp/onrijp, bleek, blond, bont, grauw and every colour word carry meaning by colour, which the cobalt-only art excludes."),
    ("Already carded", "droevig, treurig, somber, opgewekt and woedend repeat blij/verdrietig/boos; traag and vlug repeat snel/langzaam; uitgeput and vermoeid repeat moe; smerig repeats vuil; onveilig repeats veilig."),
    ("Belongs in a lower band", "A lower band is a reason to card a pair lower, not to drop it. eerlijk/oneerlijk (597; an even versus an uneven split of one cake) is carded in A1. krap/ruim (545) stays out as too close to wijd/strak. vrolijk (1779) repeats blij. houten/ijzeren (1343) and gemeen/aardig (912) have not yet been checked for A1/A2. agressief is carded in B2 with mak."),
    ("No honest partner", "nauw (wijd and breed are carded), kaal in the sense bald (Dutch says veel haar, not an adjective), versleten (nieuw and heel are carded), halfvol (vol/leeg is carded)."),
    ("No single picture", "vochtig (damp shows nothing that droog does not), vaag, zeldzaam, betrouwbaar, waardevol and the other abstract adjectives."),
    ("Scene carded elsewhere", "vredig/onrustig as a sleeping child repeats Werkwoorden slapen; geschoren/ongeschoren repeats Werkwoorden scheren; ingepakt/uitgepakt repeats Scheidbare werkwoorden inpakken/uitpakken; geschild/ongeschild repeats Werkwoorden schillen (written up as SKIP)."),
    ("Unkind to draw", "slank/dik and other body-shape pairs were left out as unkind to draw."),
    ("Later, owner's call on tone", "dronken/nuchter (2106, A2 by rank) is parked: a drunk figure next to a sober one needs the owner's call on tone before it is drawn."),
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
    return "\n".join([
        f'<article id="{attr(cid)}" class="kaart" data-id="{attr(cid)}" data-band="{band}" '
        f'data-kind="adjective" data-cluster="{attr(c["id"])}" data-status="proposal" data-severity="">',
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
            if members:                # a set whose every card is SKIP has no page section
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
            words = " · ".join(m["lemma"] if m["id"] == m["lemma"] else f'{m["lemma"]} ({m["id"].split("-", 1)[-1]})'
                               for m, _ in members)
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
        summ = (f'<div class="sum"><span>{len(sets)} contrast sets</span><span>{ncards} adjectives</span>'
                f'<span>frames #{first}–#{last}</span><span>0 getekend</span></div>')
        page = shell(f"Bijvoeglijke naamwoorden — {b.upper()}", esc(BAND_LEAD[b]), nav(b),
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
    ov = "".join(
        f"<tr><td><code>{esc(c['id'])}</code></td><td>{(c.get('rank_band') or 'none').upper()}</td>"
        f"<td>{c['band'].upper()}</td><td>{esc(c['override_reason'])}</td></tr>"
        for b in BANDS for c in selection.get(b, []) if c.get("override") and not c.get("everyday"))
    sf = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in SHORTFALL)
    promoted = [c for b in BANDS for c in selection.get(b, []) if c.get("everyday")]
    promoted_new = [c for c in promoted if c["id"] in EXPANSION_B1]
    new_b1 = sum(1 for c, _ in kept["b1"] if c["id"] not in OLD_B1) + len(promoted_new)
    ev = "".join(
        f"<tr><td><code>{esc(c['id'])}</code></td><td>{(c.get('rank_band') or 'none').upper()}</td>"
        f"<td>{c['band'].upper()}</td><td>{esc(c['override_reason'])}</td></tr>" for c in promoted)
    new_b2 = len(kept["b2"])
    uitleg = f"""
<div class="uitleg">
<h2>How the cards work</h2>
<p>Adjectives are taught in <strong>contrast sets</strong>: two or three words on one axis (groot/klein, heet/warm/koud).
Every drawing in a set is the same picture with one visible thing changed, so the learner sees the pair, not the word.</p>
<p>A card carries the adjective, an English gloss, the scene brief, the one mark that must read, the near misses,
the contrast note naming its partner and the single point of difference, an example sentence, and the alt text.
Each set also carries a fixed frame and one Dutch sentence using every member.</p>
<h2>How a set was placed</h2>
<p>A set sits in the band of its most frequent member (frequency rank in <code>tools/lexicon/woorden-frequentie.tsv</code>:
A0 up to 250, A1 251–1000, A2 1001–2500, B1 2501–5000, B2 5001–10000): the learner already knows one half and the card teaches its partner.
Ranks are looked up by exact lemma. Homograph split rows such as <code>hol (adj)</code> are ranked after the real list, so their number is not a frequency and is not used.</p>
<p>Homograph ranks were checked by hand: laat (verb laten), vroeg (verb vragen) and heel (adverb) overstate frequency; the time words stay in A0 by rank, and heel/kapot is banded by kapot.
Where the rank band is wrong for the sense drawn, or no member has a usable rank, the set takes an <code>OVERRIDE</code> in
<code>tools/_bn_tmp/select.py</code>. Every override and its reason:</p>
<table><thead><tr><th>Set</th><th>Rank band</th><th>Placed</th><th>Reason</th></tr></thead><tbody>{ov}</tbody></table>
<h2>Everyday sets promoted by judgment</h2>
<p>Everyday items sit at the lowest sensible level, A2 at the highest (owner rule, 20 Nov 2026). Where frequency rank put a set
of daily home, food or shopping words in B1 or B2, the whole set moved to A2. The lexicon facts are printed as read from
<code>tools/lexicon/woorden.tsv</code> and <code>woorden-frequentie.tsv</code>; the move itself is judgment, not lexicon data.
{len(promoted)} sets moved:</p>
<table><thead><tr><th>Set</th><th>Rank band</th><th>Placed</th><th>Reason</th></tr></thead><tbody>{ev}</tbody></table>
<h2>Left out on purpose</h2>
<ul><li>Colours (rood, blauw, groen ...): the art style is one cobalt on white, so colour cannot carry meaning.</li>
<li>Abstract adjectives (belangrijk, mogelijk, nodig ...): no honest single picture; they follow the abstract-verb rule.</li>
<li>Dutch cliché food (chips, cheese, herring): souvenir imagery, so knapperig/slap is drawn as a bowl of lettuce, not a paper cone of chips.</li></ul>
<h2>Cards written up as SKIP</h2><ul>{sk}</ul>
<h2>Words shared with other families</h2>
<p>Where two families card the same item or scene, the higher family keeps it (Werkwoorden, Voorzetselpaden, Bijvoeglijke naamwoorden, Zelfstandige naamwoorden, Bijwoorden, Scheidbare werkwoorden, Vaste uitdrukkingen; owner ruling, 20 Nov 2026).
This family keeps opgepompt/leeggelopen, so Scheidbare werkwoorden drops oppompen/leeglopen; it keeps horizontaal/verticaal and opgerold, so Bijwoorden drops them.
It drops geschild/ongeschild, which repeats Werkwoorden schillen.</p>
<h2>Why B1 and B2 have fewer than 20 new sets</h2>
<p>The brief asked for at least 20 new contrast sets in each of B1 and B2. The 20 Nov 2026 expansion added {new_b1} to B1 ({len(promoted_new)} of them since promoted to A2 as everyday sets) and {new_b2} to B2;
the candidates below were checked and dropped.</p>
<table><thead><tr><th>Reason</th><th>Candidates</th></tr></thead><tbody>{sf}</tbody></table>
<h2>Tools</h2>
<pre><code>python3 tools/_bn_tmp/select.py        # selection.json from clusters.txt
python3 tools/build-adjective-cards.py # the five band pages and this overview
python3 tools/check-adjective-cards.py # asserts ids, fields, pairs, counts</code></pre>
</div>"""
    index = shell("Bijvoeglijke naamwoorden — overview",
                  "One card per adjective, taught as contrast pairs. Picture briefs only; no art yet.",
                  nav("index"),
                  f'<table><thead><tr><th>Band</th><th>Sets</th><th>Adjectives</th><th>Frames</th><th>Content</th></tr></thead><tbody>{rows}</tbody></table>' + uitleg)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index)
    print(f"sets {tot_s}  cards {tot_c}  skipped {len(skipped)}")
    for b in BANDS:
        print(f"  {b}: {stats[b][0]} sets, {stats[b][1]} cards, frames #{stats[b][2]}-#{stats[b][3]}")


CSS = load_css()
# B1 sets that predate the 20 Nov 2026 expansion (the shortfall note counts the rest).
OLD_B1 = {"vorm-lijn", "oppervlak", "rijpheid", "schuchter", "rust"}
# B1 expansion sets later promoted to A2 as everyday sets (select.py EVERYDAY); counted as B1 expansion.
EXPANSION_B1 = {"stevigheid", "lucht", "orde", "kruiding", "bereiding"}

if __name__ == "__main__":
    build()
