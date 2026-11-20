#!/usr/bin/env python3
"""Build Docs/zelfstandige-naamwoorden/ from tools/_zn_tmp/.

Inputs : tools/_zn_tmp/selection.json            sets per band (select.py)
         tools/_zn_tmp/scenes/*.clusters.tsv      frame + contrast sentence per cluster
         tools/_zn_tmp/scenes/*.cards.tsv         one row per noun
The TSV file name is the authoring batch, not the band: a set promoted by an
OVERRIDE keeps its rows in b1.*/b2.* and is placed by selection.json.
Outputs: Docs/zelfstandige-naamwoorden/{a0,a1,a2,b1,b2,index}.html

Nouns are taught as contrast sets, so the page unit is the cluster: a
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
TMP = os.path.join(ROOT, "tools", "_zn_tmp")
SCENES = os.path.join(TMP, "scenes")
OUT = os.path.join(ROOT, "Docs", "zelfstandige-naamwoorden")
BANDS = ["a0", "a1", "a2", "b1", "b2"]

BAND_LEAD = {
    "a0": "The home, the person, the vehicle and the town, plus the plural huis/huizen.",
    "a1": "Furniture, footwear, pets, farm animals, fruit, doors, books, body parts, plants and sky, plus kind/kinderen, schip/schepen, been/benen and boom/bomen.",
    "a2": "Cups, cutlery, clothes, bags, birds and fish, light and headwear, plus ei/eieren, muis/muizen, glas/glazen and blad/bladeren. "
          "Promoted on coursebook level: arm and leg joints, basket/bucket, terrace/balcony, shed/greenhouse and tomato/pepper; "
          "promoted by judgment as daily words: lemon/orange, biscuit/waffle, sock/stocking, towel/sheet, blanket/duvet, mouth, comb/toothbrush, "
          "crossroads/roundabout, winter wear, the tap and the crane, oven/microwave, berries, vacuum cleaner/broom, pumpkin/melon, nuts, pans, "
          "socket/switch and sandal/flip-flop.",
    "b1": "Wild and farm animals, insects, frog/tortoise, bird parts, water and land, house spaces, face, fingers, tree parts, "
          "tools, fastenings, jewellery, vehicles, wound/plaster, plus the same-word sets het pad/de pad and de slang.",
    "b2": "Birds, reptiles, sea and garden animals, sieves and the stove, garden and painting tools, "
          "seats, fasteners and hand tools, sleeves, jewellery, sports gear, boats, instruments and the irregular plural rund/runderen.",
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
.vormen .art::before{content:"lidwoord"}
.vormen .mv::before{content:"meervoud"}
.vormen .dim{color:var(--grijs);font-weight:400}
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
        f'data-kind="noun" data-article="{attr(m["article"])}" data-plural="{attr(m["plural"])}" '
        f'data-dim="{attr(m.get("dim") or "no")}" data-cluster="{attr(c["id"])}" data-status="proposal" data-severity="">',
        f'<span class="framenummer" title="Frame {number}">#{number}</span>',
        '<div class="geenbeeld">geen beeld</div>',
        f'<h3 class="chunk">{esc(m["article"])} {esc(m["lemma"])}</h3>',
        f'<p class="gloss">{esc(m["gloss"])}</p>',
        '<p class="vormen">'
        f'<span class="art" title="lidwoord">{esc(m["article"])}</span>'
        f'<span class="mv" title="meervoud">{esc(m["plural"])}</span>'
        + ('<span class="dim" title="verkleinwoord">verkleinwoord'
           + (f' van {esc(m["base"])}' if m.get("base") else "") + "</span>" if m.get("dim") == "yes" else "")
        + "</p>",
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
            words = " · ".join(f'{m["article"]} {m["lemma"]}' for m, _ in members)
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
        summ = (f'<div class="sum"><span>{len(sets)} contrast sets</span><span>{ncards} nouns</span>'
                f'<span>frames #{first}–#{last}</span><span>0 getekend</span></div>')
        page = shell(f"Zelfstandige naamwoorden — {b.upper()}", esc(BAND_LEAD[b]), nav(b),
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
    ov_rows = "".join(
        f'<tr><td>{esc(c["id"])}</td><td>{c["band"].upper()}</td><td>{(c.get("rank_band") or "none").upper()}</td><td>{esc(c["override"])}</td></tr>'
        for bb in BANDS for c, _m in kept[bb] if c.get("override"))
    rv = selection.get("_everyday_review", {})
    where = {c["id"]: bb for bb in BANDS for c, _m in kept[bb]}
    notes = {c["id"]: c["override"].split(" Note: ", 1)[1].rstrip(".") for bb in BANDS for c, _m in kept[bb]
             if c.get("override") and " Note: " in c["override"]}
    rv_rows = "".join(
        f'<tr class="review"><td>{esc(k)}</td><td>{v[0].upper()}</td><td>{where[k].upper()}</td><td>{v[1]}</td>'
        f'<td>{esc(v[2] if v[1] == "kept" else "judgment: " + notes[k])}</td></tr>' for k, v in rv.items())
    n_rv_p = sum(1 for v in rv.values() if v[1] == "promoted")
    n_rv_k = sum(1 for v in rv.values() if v[1] == "kept")
    rk_rows = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>"
                      for k, v in selection.get("_no_rank", {}).items())
    lookalike = [c for bb in BANDS for c, _m in kept[bb]
                 if not c["id"].endswith("-getal") and not c["axis"].startswith("same word")]
    n_lookalike = len(lookalike)
    n_b1_in_b2 = sum(1 for c, _m in kept["b1"] if not c.get("override")
                     for m in c["members"] if m.get("rank") and m["rank"] > 5000)
    ovs = [c for bb in BANDS for c, _m in kept[bb] if c.get("override")]
    n_cb = sum(1 for c in ovs if "Basis: coursebook" in c["override"])
    n_judg = sum(1 for c in ovs if "Basis: judgment" in c["override"])
    cbf = selection.get("_coursebook_for", {})
    cb_rule = "A bands: " + " or ".join(cbf.get("a2", [])) + "; B1: " + " or ".join(cbf.get("b1", []))
    n_same = sum(1 for c in lookalike if len({m["article"] for m in c["members"]}) == 1)
    uitleg = f"""
<div class="uitleg">
<h2>How the cards work</h2>
<p>Nouns are taught in <strong>contrast sets</strong>: two or three look-alike or often-confused words (kat/hond, stoel/bank, het bos/de bos).
Every drawing in a set is the same picture with one visible thing changed, so the learner sees the pair, not the word.</p>
<p>A card carries the noun with its article (de/het), its plural, a diminutive flag where the headword is a diminutive (het kopje),
an English gloss, the scene brief, the one mark that must read, the near misses, the contrast note, an example sentence and the alt text.
Each set carries a fixed frame and one Dutch sentence that uses every member with its own article.</p>
<h2>This is a pilot</h2>
<p>Nouns are the largest class (about 6,300 in the lexicon). This pass takes only concrete, drawable nouns: no abstract nouns, no names,
no nouns whose picture would need text. It is meant to test the card shape with article and plural before the class is done in full.</p>
<h2>Where article and plural come from</h2>
<p>The lexicon has no article or plural column (<code>woorden.tsv</code> holds nl, en, niveau, top2000, herkomst only). Every article and plural here was written
from certain knowledge and is <strong>not verified by the lexicon</strong>. A native check of the list in <code>tools/_zn_tmp/clusters.txt</code> is the open step.
Words whose article or plural is uncertain (hout, haar) were left out.</p>
<h2>Set types</h2>
<ul><li><strong>Look-alike nouns</strong> (kat/hond, jas/trui, mes/vork/lepel): the drawings share a frame and differ in one feature.</li>
<li><strong>Same word, different gender</strong>: het bos (forest) and de bos (bunch), het pad (path) and de pad (toad). Both senses are real Dutch.</li>
<li><strong>Same word, same article</strong>: de kraan (tap, crane; A2) and de slang (snake, hose; B1). The article and plural do not change; only the thing does.</li>
<li><strong>Singular and plural</strong> (ids ending <code>-een</code> and <code>-meer</code>). Irregular plurals: kind/kinderen, ei/eieren, blad/bladeren, glas/glazen, schip/schepen.
Regular plurals that change spelling: huis/huizen, muis/muizen, been/benen, boom/bomen; these are labelled "one or more", not "irregular".
The drawing differs only in number, and the single card reuses the drawing of the noun's own card where one exists (been is the exception: the arm/been card must show the whole figure, so been-een and been-meer draw the bare leg).
The plural card carries the article de, as every Dutch plural does.
het rund (B2) is drawn as the A1 koe card without its udder, so the learner meets one animal drawing; the gloss names the single animal (cow, bull or ox), not the counting term.</li>
<li><strong>Part sets</strong> (A2, B1, B2): one drawing with a small ring on the part named, as in the A1 face set: arm and leg joints, bird, boat, mouth, face area (the A1 head reused), fingers, tree, shirt.</li>
<li><strong>Theme sets</strong>: {n_same} of the {n_lookalike} look-alike and part sets share one article (kat/hond, both de), so they teach the word and not a de/het contrast, and a few (vogel/vis, sleutel/slot, zon/maan/ster) are themes rather than look-alikes.
That is accepted: the set is a picture contrast, and the article is shown on every card.</li></ul>
<h2>How a set was placed</h2>
<p>By default a set sits in the band of its most frequent member (rank in <code>tools/lexicon/woorden-frequentie.tsv</code>: A0 up to 250, A1 251–1000,
A2 1001–2500, B1 2501–5000, B2 5001–10000). The rank is always the singular lemma's; plural cards (kinderen, runderen) take their singular's rank.
Rank is a tiebreak only for concrete nouns: newspapers rarely mention shoes or cows, but a beginner needs them.
Where rank and theme disagree, the <code>OVERRIDE</code> table in <code>tools/_zn_tmp/select.py</code> places the set by theme. Every override:</p>
<table><thead><tr><th>Set</th><th>Band</th><th>Rank would give</th><th>Reason</th></tr></thead><tbody>{ov_rows}</tbody></table>
<p>Each reason is rendered from the lexicon by <code>select.py</code> and re-checked by the checker against the files, so a wrong fact fails the checker.
<strong>Lexicon</strong> gives every member's <code>niveau</code>, <code>top2000</code> and <code>herkomst</code> (<code>tools/lexicon/woorden.tsv</code>) and its rank.
<code>niveau</code> A1 means taught in <em>Nederlands in gang</em>, B1 taught in <em>Nederlands in actie</em>, open means in Bijlage 8 but taught in neither coursebook.
<code>herkomst</code> bijlage8 means the word is in Bijlage 8, the 5,000 most frequent lemmas (Tiberius &amp; Schoonheim 2014): a frequency list, not a teaching list.
les:taalcompleet is the TaalCompleet B1 theme vocabulary.</p>
<p><strong>Basis</strong> is <em>coursebook</em> only when a named member is taught at or below the target band ({cb_rule}); every other override says
<em>judgment, not lexicon data</em>, and its note gives the judgment. Coursebook: {n_cb} overrides; judgment: {n_judg}.
The checker also fails any B1 or B2 set holding a coursebook A1 or top-2000 word, unless the card draws another sense (wortel: the root, not the carrot).</p>
<h2>Everyday-item review</h2>
<p>Everyday items sit at the lowest sensible level, A2 at the highest (owner rule, <code>Docs/decisions.html</code>, 20 November 2026).
Every set that sat in B1 or B2 on 20 November 2026 was checked against it: {n_rv_p} were promoted to A2 and {n_rv_k} kept.
A set was promoted only when it holds a very common daily-life item (home, food, clothes, body, transport, shop); its partners moved with it.
Each promotion is an override above, with its lexicon facts and the judgment. A set whose items are wild animals, specialist tools or rare objects stayed.
The checker fails any B1 or B2 set missing from this table, and any judgment promotion above A2.</p>
<table><thead><tr><th>Set</th><th>Was</th><th>Now</th><th>Decision</th><th>Reason</th></tr></thead><tbody>{rv_rows}</tbody></table>
<p>A set takes the band of its most frequent member, so a set can hold rarer words: {n_b1_in_b2} members of B1 sets rank in B2 on their own.</p>
<p>The lexicon's suffixed rows ("arm (noun)", "kussen (noun)") carry a placeholder rank from a failed lookup (about 9,600 and up), so they are never used.
A noun with no usable bare rank is listed in <code>NO_RANK</code> in <code>select.py</code> and banded by its partners alone:</p>
<table><thead><tr><th>Noun</th><th>Reason</th></tr></thead><tbody>{rk_rows}</tbody></table>
<p>Some ranks are shared with a homograph: knoop (button, knot), kam (comb, crest), stam (trunk, tribe), kas (greenhouse, cash), schuur (shed, the verb schuren),
pols (wrist, pulse), ezel (donkey, easel), pony (pony, fringe), jaguar (the animal, the car brand), pink (little finger, the English word), zeil and schep (nouns, and forms of the verbs zeilen and scheppen),
mot (moth, a quarrel) and kruk (stool, crutch or door handle). None changes a band: a partner ranks in the same band, an override places the set, or the drawn sense is the everyday one
(knoop, kam; inference, not measured). de kraan and de slang draw both senses, so the shared rank is the right one.</p>
<h2>Objects drawn in another family too</h2>
<p>No noun card repeats another family's item, but these objects also appear there, and the illustrator should reuse one drawing of each:
eend and vijver (adjectives bevroren/ontdooid, werkwoorden voeren), kruk (adjectives stevig/wankel: four legs, as here), fauteuil (comfortabel), ezel (koppig/gehoorzaam),
slak (langzaam), citroen (zuur, werkwoorden persen), rits (scheidbare dichtritsen), kraan (opendraaien), vergiet (afgieten), stopcontact and kabel (aansluiten),
anker (vaste uitdrukkingen voor anker), sok (op sokken), zaag (zagen), bezem (vegen), tandenborstel (poetsen), kwast and penseel (schilderen), walnoot (kraken).
handdoek/laken was moved off the washing line, which belongs to the adjectives (droog, winderig/windstil).</p>
<h2>Left out on purpose</h2>
<ul><li>Abstract nouns (idee, probleem, tijd): no honest single picture.</li>
<li>Names and brands, and nouns that need text in the picture (brief, kaart, a signboard).</li>
<li>Words with an irregular article or plural the author could not vouch for (haar, hout).</li>
<li>stad/steden as a plural set: three skylines read as one city with parks. schip/schepen replaced it (review 2026-11-20).</li>
<li>B1/B2 candidates whose article the author could not vouch for: luipaard and ree (de and het both in use), matras, duin and accordeon (de and het both in use).</li>
<li>B1/B2 candidates whose band is not certain: kussen (pillow), whose bare rank 2300 is shared with the verb kussen and would put a set in A2; vat (barrel), whose rank 2690 is shared with the verb form vat (vatten); gans, which the lexicon holds only as the adjective gans (whole).</li>
<li>B1/B2 candidates that would repeat an earlier card: mok (the same object as the A2 beaker card), handtas (the A2 bag card), kalkoen and haan (no partner in band).</li>
<li>Souvenir imagery: tulp, klomp and gracht are in the B2 lexicon and are left out under the project rule.</li>
<li>rots/kiezel (B1, dropped 2026-11-20): the contrast was size only, and kiezel (rank 8985) was drawn while commoner pairs were held back. Its place went to the fly and microwave sets.</li>
<li>Drawable B1 pairs held back by the cap of about 40 sets per band: duif/valk, rat/mol, spin/mier, perron/halte, stoep/fietspad, microfoon/koptelefoon, wolk/regenboog.</li></ul>
<p>Candidates for a later pass: a same-word set for the root and the carrot (the carrot is the coursebook A1 sense), and pan (rank 2128) as an A2 card of its own.</p>
<h2>Cards written up as SKIP</h2><ul>{sk}</ul>
<h2>Tools</h2>
<pre><code>python3 tools/_zn_tmp/select.py                              # selection.json from clusters.txt
python3 tools/build-zelfstandige-naamwoorden-cards.py        # the five band pages and this overview
python3 tools/check-zelfstandige-naamwoorden-cards.py        # asserts ids, fields, pairs, articles, counts</code></pre>
</div>"""
    index = shell("Zelfstandige naamwoorden — overview",
                  "One card per concrete noun with article and plural, taught as contrast sets. Picture briefs only; no art yet.",
                  nav("index"),
                  f'<table><thead><tr><th>Band</th><th>Sets</th><th>Nouns</th><th>Frames</th><th>Content</th></tr></thead><tbody>{rows}</tbody></table>' + uitleg)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index)
    print(f"sets {tot_s}  cards {tot_c}  skipped {len(skipped)}")
    for b in BANDS:
        print(f"  {b}: {stats[b][0]} sets, {stats[b][1]} cards, frames #{stats[b][2]}-#{stats[b][3]}")


CSS = load_css()

if __name__ == "__main__":
    build()
