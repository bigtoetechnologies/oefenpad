#!/usr/bin/env python3
"""Build Docs/scheidbare-werkwoorden/ from tools/_sw_tmp/.

Inputs : tools/_sw_tmp/selection.json            sets per band (select.py)
         tools/_sw_tmp/scenes/*.clusters.tsv      frame + contrast sentence per set
         tools/_sw_tmp/scenes/*.cards.tsv         one row per verb
Outputs: Docs/scheidbare-werkwoorden/{a0,a1,a2,b1,b2,index}.html

Separable verbs are taught as contrast sets, so the page unit is the set: a
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
TMP = os.path.join(ROOT, "tools", "_sw_tmp")
SCENES = os.path.join(TMP, "scenes")
OUT = os.path.join(ROOT, "Docs", "scheidbare-werkwoorden")
BANDS = ["a0", "a1", "a2", "b1", "b2"]

BAND_LEAD = {
    "a0": "No sets at this level: no separable verb ranks inside the top 250 (the nearest, mee-eten, is 259).",
    "a1": "No sets at this level: the plane pair was the only one, and it is a SKIP now that landen stays in Werkwoorden.",
    "a2": "Everyday pairs: lights and radios, doors, suitcases, buses, phones, trains, umbrellas, tidying, coats, beds, school runs, plates, dishes, gifts, outings, the front door, taps, rubbish, a tent, ticket gates, seat belts, the table, the dishwasher and zips.",
    "b1": "The wider pairs: posting, boxes, looking, copying, moving, words, handing out and in, cables and passing on; then grabbing and letting go, forms, a dog, a printer, a cage, a substitute, a gate, a chair and coffee.",
    "b2": "Rank 5001–10000, or no rank: loading, candles, maps, boats, a vase, working on, breathing, toys, the library, a crowd and pasta.",
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
    panels = "1 panel"
    kind = "separable"
    return "\n".join([
        f'<article id="{attr(cid)}" class="kaart" data-id="{attr(cid)}" data-band="{band}" '
        f'data-kind="separable-verb" data-cluster="{attr(c["id"])}" data-status="proposal" data-severity="">',
        f'<span class="framenummer" title="Frame {number}">#{number}</span>',
        '<div class="geenbeeld">geen beeld</div>',
        f'<h3 class="chunk">{esc(m["lemma"])}</h3>',
        f'<p class="gloss">{esc(m["gloss"])}</p>',
        f'<p class="vlaggen"><span>{esc(c["axis"])}</span><span>{band.upper()}</span>'
        f'<span>{kind}</span><span>{panels}</span></p>',
        "<dl>",
        f'<dt>Scene</dt><dd class="scene">{esc(s["scene"].strip())}</dd>',
        f'<dt>Must read</dt><dd class="must">{esc(s["must"].strip())}</dd>',
        f'<dt>Avoid</dt><dd class="avoid">{esc(s["avoid"].strip())}</dd>',
        f'<dt>Contrast</dt><dd class="contrast-note" data-partner="{attr(" ".join(partners))}">{esc(s["contrast"].strip())}</dd>',
        f'<dt>Split form</dt><dd class="split">{esc(s["split"].strip())}</dd>',
        f'<dt>Example</dt><dd class="voorbeeld-nl">{esc(s["example_nl"].strip())}'
        f'<br><span class="voorbeeld-en">{esc(s["example_en"].strip())}</span></dd>',
        f'<dt>Perfect</dt><dd class="perfect">{esc(s["perfect"].strip())}</dd>',
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
            if members:            # a set whose every card is SKIP gets no section
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
        if sets:
            first = numbers[sets[0][1][0][0]["id"]]
            last = numbers[sets[-1][1][-1][0]["id"]]
        else:
            first = last = None
            body.append('<p class="zin">No contrast sets at this level.</p>')
        stats[b] = (len(sets), ncards, first, last)
        frames = f"frames #{first}–#{last}" if sets else "no frames"
        summ = (f'<div class="sum"><span>{len(sets)} contrast sets</span><span>{ncards} verbs</span>'
                f'<span>{frames}</span><span>0 getekend</span></div>')
        page = shell(f"Scheidbare werkwoorden — {b.upper()}", esc(BAND_LEAD[b]), nav(b),
                     "\n".join(body), summ)
        with open(os.path.join(OUT, b + ".html"), "w", encoding="utf-8") as fh:
            fh.write(page)

    rows = "".join(
        f'<tr><td><a href="{b}.html">{b.upper()}</a></td><td class="n">{stats[b][0]}</td>'
        f'<td class="n">{stats[b][1]}</td><td class="n">{("#%d–#%d" % (stats[b][2], stats[b][3])) if stats[b][0] else "–"}</td>'
        f'<td class="blurb">{esc(BAND_LEAD[b])}</td></tr>' for b in BANDS)
    tot_s = sum(v[0] for v in stats.values())
    tot_c = sum(v[1] for v in stats.values())
    rows += f'<tr class="totaal"><td>Total</td><td class="n">{tot_s}</td><td class="n">{tot_c}</td><td></td><td></td></tr>'
    sk = "".join(f"<li><code>{esc(m['id'])}</code> ({b.upper()}, {esc(cid)}): {esc(why)}</li>"
                 for b, cid, m, why in skipped) or "<li>None.</li>"
    # The separable verbs held back from Docs/werkwoorden/ (backlog_seed.tsv).
    held = []
    with open(os.path.join(ROOT, "tools", "_ww_tmp", "backlog_seed.tsv"), encoding="utf-8") as fh:
        for r_ in csv.DictReader(fh, delimiter="\t"):
            if "separable" in r_["reason"]:
                r_["gloss"] = GLOSS_FIX.get(r_["verb"], r_["gloss"])
                held.append(r_)
    drawn = {m["lemma"] for b in BANDS for _c, ms in kept[b] for m, _s in ms}
    covered = [h for h in held if h["verb"] in drawn]
    open_ = [h for h in held if h["verb"] not in drawn]
    held_rows = "".join(
        f'<tr><td>{esc(h["verb"])}</td><td>{esc(h["gloss"])}</td><td class="n">{esc(h["rank"])}</td><td>{esc(h["band"])}</td></tr>'
        for h in open_)
    sets_rows = "".join(
        f'<tr><td>{esc(c["id"])}</td><td>{esc(" · ".join(m["lemma"] for m, _ in ms))}</td><td>{b.upper()}</td></tr>'
        for b in BANDS for c, ms in kept[b])
    n2 = {b: sum(1 for c, _ in kept[b] if c.get("batch") == 2) for b in BANDS}
    n2p = sum(1 for c, _ in kept["a2"] if c.get("batch") == 2 and c.get("override", {}).get("kind") == "promoted")
    short_rows = "".join(f"<tr><td>{esc(v)}</td><td>{esc(w)}</td></tr>" for v, w in SHORTFALL)
    OVR = load_override()
    n_prom = sum(1 for v in OVR.values() if v[1] == "promoted")
    n_hom = sum(1 for v in OVR.values() if v[1] == "homograph")
    ovs = sorted(((c, bb) for bb in BANDS for c in selection.get(bb, []) if c.get("override")),
                 key=lambda t: (t[0]["override"]["kind"], BANDS.index(t[1]), t[0]["id"]))
    ovr_rows = "".join(
        f'<tr><td>{esc(c["id"])}</td><td>{bb.upper()}</td><td>{c["by_rank"].upper()}</td><td>{c["override"]["kind"]}</td>'
        f'<td>{esc(c["override"]["basis"])}</td><td class="lexicon">{esc(c["override"]["lexicon"])}</td><td>{esc(c["override"]["reason"])}</td></tr>'
        for c, bb in ovs)
    uitleg = f"""
<div class="uitleg">
<h2>How the cards work</h2>
<p>A separable verb is learned in <strong>contrast sets</strong>: two or three verbs that are particle opposites (aandoen/uitdoen)
or that share a stem and are told apart by one visible thing (opruimen/schoonmaken).
Every drawing in a set is the same picture with one thing changed.</p>
<p>A card has two halves. The text half shows the infinitive, the split form in one main clause (<em>ik bel jou op</em>) and the
perfect (<em>heeft opgebeld</em>). The picture half is the scene brief. Each card gets <strong>one drawing in one panel</strong>:
a change is drawn mid-action, with a small arrow where the direction is the difference.
Alt text never names the verb, its finite form, its participle, its particle at the end of a clause, or any form of its partner.</p>
<p>The perfect is written out because the ge- sits between particle and stem (<em>opgebeld</em>, <em>meegenomen</em>) and the
auxiliary is not always hebben (<em>is ingestapt</em>, <em>is aangekomen</em>). Forms were checked against
<code>tools/lexicon/werkwoorden-vormen.tsv</code> (Bijlage 3b) for the stem verbs; the base verb of each compound is listed there when irregular.</p>
<h2>How a set was placed</h2>
<p>One rule places every set, whatever batch it came from. A set sits in the band of its most frequent member (A0 up to 250, A1 251–1000, A2 1001–2500, B1 2501–5000, B2 5001–10000).
A set with no member ranked within 10000 sits in B2, the last band.
No separable verb ranks inside the top 250 (the nearest, mee-eten, is 259), so A0 is empty; A1 is empty for the reason in its lead.</p>
<p>A <em>promotion</em> moves a set to an earlier band and needs a stated daily-life reason; {n_prom} sets are promoted.
Promotions are common here because the lexicon undercounts compound separables (opendoen 8519, instappen 7644, opbellen 8777): it files their split forms under the base verb.
{n_hom} <em>homograph</em> entry moves a set later, because the member that ranks it counts mostly another sense.
Nothing else moves a set. <code>select.py</code> refuses an entry that does not move the set, and a promotion whose stated rank is wrong.</p>
<p>Ranks are lemma ranks, so a homograph lends its other senses to the set. Where the band would still hold without the borrowed sense it is left alone:
wissel (invallen 4866, toekijken 4959), tent (opzetten 2407 also counts <em>een bril opzetten</em> and <em>koffie opzetten</em>; afbreken 4722 keeps the set no later than B1).</p>
<p>Everyday items sit at the lowest sensible level, A2 at the highest (owner rule). Where rank puts a set of daily-life verbs (home, food, clothes, transport) in B1 or B2,
the set is promoted to A2 and its reason is stated as <em>judgment</em>, not lexicon data. Each entry below lists every member's <code>niveau</code>, <code>top2000</code> and <code>herkomst</code>
from <code>tools/lexicon/woorden.tsv</code> and its rank from <code>woorden-frequentie.tsv</code>; most compound separables have no row there at all. The checker re-derives every listed fact.</p>
<details><summary>Every OVERRIDE entry ({len(OVR)})</summary>
<table><thead><tr><th>Set</th><th>Band</th><th>Rank band</th><th>Kind</th><th>Basis</th><th>Lexicon</th><th>Reason</th></tr></thead><tbody>{ovr_rows}</tbody></table></details>
<h2>Verbs that belong to Werkwoorden</h2>
<p>vertrekken and landen are not separable and already have cards in Werkwoorden (<code>a2-regular</code>, <code>a1-regular</code>), so this family does not reuse them.
aankomen now pairs with wegrijden. opstijgen has no separable opposite (neerkomen reads as a crash) and is listed as a SKIP.
ondergaan (the sun) was dropped with opkomen; the slug is also the Werkwoorden row for the inseparable <em>ondergaan</em> (to undergo, heeft ondergaan).
The checker fails on any card id that is already a card in another family or a row in the Werkwoorden source files, and on any of our participles that another family uses as a headword.</p>
<h2>Owner rulings of 20 November</h2>
<ul><li>Bijvoeglijke naamwoorden keeps <em>opgepompt</em> and <em>leeggelopen</em>, so oppompen and leeglopen are dropped here, and their partners opblazen and vollopen with them.</li>
<li>Werkwoorden keeps <em>pinnen</em> (a bank card at a terminal), so the ticket-gate pair is drawn by the way through the open flaps, not by a card on a reader.</li>
<li>Sunrise and sunset, and getting on and off a bike, cannot be told apart as stills by one changed element, so both sets are SKIPs.</li>
<li>The dog set (weglopen/terugkomen) stays: Bijwoorden drops hierheen/daarheen, which drew the same lawn.</li></ul>
<h2>Left out on purpose</h2>
<ul><li>Abstract separables with no honest single picture: voorkomen, voorstellen, uitmaken, plaatsvinden, aannemen as <em>to assume</em>, afvragen, omgaan, inzetten and similar.</li>
<li>A second sense of a verb: ophangen is the phone, aannemen is accepting a gift, opzoeken is looking up a word.</li>
<li>Pairs whose partner is not a real verb: opstaan/gaan zitten, opruimen/rommelen.</li></ul>
<h2>The separable verbs held back from Werkwoorden</h2>
<p><code>tools/_ww_tmp/backlog_seed.tsv</code> tags {len(held)} verbs as separable (two of them also reflexive). {len(covered)} of them now have a card here ({esc(", ".join(h["verb"] for h in covered))}).
The other {len(drawn) - len(covered)} cards here are verbs that were never on that backlog.
The {len(open_)} still without a card are mostly abstract (afvragen, toestaan, uitoefenen). The drawable ones were dropped because another family already draws the same verb or scene; see the section on B1 and B2 below.</p>
<details><summary>Held back and still without a card ({len(open_)})</summary>
<table><thead><tr><th>Verb</th><th>Gloss</th><th>Rank</th><th>Band</th></tr></thead><tbody>{held_rows}</tbody></table></details>
<h2>B1 and B2 against the target</h2>
<p>The target was at least 20 new sets in B1 and 20 in B2. The second batch added {sum(n2.values())} drawn sets; {n2["b1"]} sit in B1, {n2["b2"]} in B2 and {n2["a2"]} in A2 ({n2p} of them promoted as everyday sets). The batch fell short because the drawable separables run out before the target once every verb or scene already drawn elsewhere is dropped.</p>
<table><thead><tr><th>Verb (rank)</th><th>Why it has no set here</th></tr></thead><tbody>{short_rows}</tbody></table>
<h2>Every set</h2>
<details><summary>All {tot_s} sets</summary>
<table><thead><tr><th>Set</th><th>Verbs</th><th>Band</th></tr></thead><tbody>{sets_rows}</tbody></table></details>
<h2>Cards written up as SKIP</h2><ul>{sk}</ul>
<h2>Tools</h2>
<pre><code>python3 tools/_sw_tmp/select.py                  # selection.json from clusters.txt
python3 tools/_sw_tmp/gen.py                     # scenes/*.tsv from the author*.py files
python3 tools/build-scheidbare-werkwoorden-cards.py # the five band pages and this overview
python3 tools/check-scheidbare-werkwoorden-cards.py # asserts ids, fields, perfects, counts</code></pre>
</div>"""
    index = shell("Scheidbare werkwoorden — overview",
                  "One card per separable verb, taught as contrast pairs with the split form and the perfect. Picture briefs only; no art yet.",
                  nav("index"),
                  f'<table><thead><tr><th>Band</th><th>Sets</th><th>Verbs</th><th>Frames</th><th>Content</th></tr></thead><tbody>{rows}</tbody></table>' + uitleg)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index)
    print(f"sets {tot_s}  cards {tot_c}  skipped {len(skipped)}")
    for b in BANDS:
        print(f"  {b}: {stats[b][0]} sets, {stats[b][1]} cards, frames #{stats[b][2]}-#{stats[b][3]}")


CSS = load_css()

# Wrong glosses in tools/_ww_tmp/backlog_seed.tsv (another family's file); corrected here for display only.
GLOSS_FIX = {"opbouwen": "to build up", "terugzetten": "to put back", "opgeven": "to give up", "afvallen": "to lose weight, to drop out"}


# Drawable separables considered for batch 2 (B1 completion, B2) and dropped, with the reason.
SHORTFALL = [
    ("oversteken (4347)", "Voorzetselpaden draws helping someone across the road (helpen bij het oversteken)."),
    ("oplopen (3431) / aflopen (5841), the stairs", "Vaste uitdrukkingen draws naar boven / naar beneden on the stairs; Werkwoorden draws stappen on a stair."),
    ("binnenkomen (3873), aankloppen, aanbellen", "Bijwoorden draws naar binnen through an open door; Werkwoorden bezoeken has a visitor stepping in; Voorzetselpaden has aanbellen bij."),
    ("langskomen (4338) / voorbijlopen", "Voorzetselpaden langs walks an adult past a house front."),
    ("aanspreken (4026)", "Voorzetselpaden has aanspreken op."),
    ("meespelen (5407), meehelpen (6774)", "Voorzetselpaden has meespelen met; Werkwoorden helpen already draws two adults lifting together."),
    ("opvangen (4624), toegooien", "Werkwoorden draws vangen and gooien with a ball."),
    ("aanraken (5104) / terugtrekken (4188)", "Werkwoorden raken draws a fingertip touching."),
    ("aanwijzen (5983) / opsteken (7907)", "Werkwoorden wijzen draws pointing; Voorzetselpaden draws a raised hand in class."),
    ("inschenken / leegdrinken", "Werkwoorden drinken draws a tilted, half-empty glass."),
    ("inzepen / afspoelen", "Werkwoorden wassen draws soaping hands at a basin."),
    ("kwijtraken / terugvinden (4885), keys", "Werkwoorden vinden draws keys found and vergeten draws keys left behind."),
    ("inhalen (4805) / afremmen, cyclists", "Werkwoorden remmen (B2, added the same day) draws a cyclist squeezing the brakes."),
    ("uitknippen / opplakken", "Werkwoorden knippen and plakken draw scissors on paper and a stamp pressed down."),
    ("inslaan (6171) / indraaien, nail and screw", "Werkwoorden gebruiken draws a screwdriver seated in a screw, and maken a hammer and nails."),
    ("opwarmen (6246) / afkoelen (6436)", "Steam rises from food that is heating and from food that is cooling, so the two stills differ only by an arrow; a microwave against a window sill changes the whole setting, not one element."),
    ("aankleden (5239)", "Dressing a child is the aantrekken/uittrekken picture of the A2 coat set."),
    ("uitlaten (5972)", "Werkwoorden and Voorzetselpaden cards already name a dog on a lead as a near miss (uitlaten), and a dog let out of a door is the hek doorlaten picture."),
    ("overstappen (4625)", "No separable opposite (blijven zitten is not separable); a traveller crossing between two trains reads as uitstappen then instappen (A2 bus set)."),
    ("afrekenen (5902)", "Werkwoorden betalen draws a banknote laid on a shop counter."),
    ("oppompen, leeglopen", "Bijvoeglijke naamwoorden keeps opgepompt and leeggelopen (owner ruling 20 November)."),
    ("opengaan (8305) / dichtgaan, lift doors", "Voorzetselpaden has a figure squeezing through closing lift doors."),
    ("openmaken (8287) / dichtplakken, an envelope", "Voorzetselpaden draws an envelope slit open."),
    ("vastmaken", "Voorzetselpaden has vastmaken aan; the seat belt pair uses omdoen instead."),
    ("terugkijken (5301)", "Voorzetselpaden has terugkijken op, and aankijken/wegkijken already covers looking."),
    ("doorzoeken (6298)", "Not separable (doorzóéken, doorzocht)."),
    ("uitrollen / oprollen", "Too close to opvouwen/uitvouwen, and the two stills differ only in which side of the roll lies flat."),
    ("innemen (3201), voorlezen (4369), opladen (4567), afvallen (3605), klaarmaken (3879)", "No separable partner that one visible change tells apart, or the partner is a second sense of an existing card (aankomen)."),
]


def load_override():
    import importlib.util
    spec = importlib.util.spec_from_file_location("sw_select", os.path.join(TMP, "select.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.OVERRIDE

if __name__ == "__main__":
    build()
