#!/usr/bin/env python3
"""Build Docs/explanation-cards-pilot.html and check its Dutch text.

The pilot tests three card tiers for verbs the picture families skipped:
  1 picture          one mark carries the meaning
  2 picture + check  a picture plus one yes/no question
  3 scene + text     a fuller scene, 2-4 short Dutch sentences, one question

The check: every Dutch word must sit at or below the verb's own band by
lemma rank in tools/lexicon/woorden-niveau.tsv (A0 250, A1 1000, A2 2500,
B1 5000, B2 10000). The verb itself is exempt. Where a surface form has
several homograph keys the best rank is used, so the check is generous
there. Unresolved words fail the build.

Usage: python3 tools/build-explanation-pilot.py
"""
import csv, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from explanation_lib import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Docs", "explanation-cards-pilot.html")
TEMPLATE = os.path.join(ROOT, "Docs", "card-families-handover.html")

def ex(text, question, answer, scene=None):
    return dict(text=text, question=question, answer=answer, scene=scene)

SRC = "Dutch Wiktionary (nl.wiktionary.org), read 20 November 2026"

ENTRIES = [
 dict(verb="worden", sense="to become", gloss="to become", tier=3, forms={"worden", "wordt"},
  skip="Skip reason today: becoming is an arrow from one state to another and would show no person.",
  picture="Three panels in a row, the same figure at three sizes: small, taller, tall. The figure is the same in every panel, drawn at the same stroke weight.",
  mark="The same figure, three sizes, left to right.",
  alt="Drie tekeningen naast elkaar van dezelfde persoon: eerst klein, dan groter, dan groot.",
  examples=[ex(["Eerst is Sam niet groot.", "Later wordt hij groot."], "Is Sam nu al groot?", "nee")],
  note="The picture shows the change; the text names it. Neither works alone."),

 dict(verb="laten", sense="toestaan dat iets gebeurt (to allow)", gloss="to let, to allow", tier=3, forms={"laten", "laat"},
  skip="Skip reason today: an auxiliary with no picture of its own; the box scene read as geven.",
  picture="A parent stands at an open door with one hand held out flat towards the garden. A child stands in the doorway looking out.",
  mark="The open flat hand: permission, not a push.",
  alt="Een volwassene staat bij een open deur en wijst met een open hand naar buiten. Een kind staat in de deuropening.",
  examples=[
   ex(["Sam wil buiten spelen.", "Zijn moeder zegt: ja.", "Zij laat Sam buiten spelen."], "Speelt Sam nu buiten?", "ja"),
   ex(["De man wil naar binnen gaan.", "De vrouw zegt: ja.", "Zij laat de man naar binnen gaan."], "Gaat de man naar binnen?", "ja",
      "A woman steps aside at an open door with a flat open hand; a man waits on the step."),
   ex(["Sam wil in de auto zitten.", "Zijn vader zegt: ja.", "Hij laat Sam in de auto zitten."], "Zit Sam in de auto?", "ja",
      "A father holds the car door open with a flat hand; Sam sits on the seat."),
   ex(["Sam wil naar binnen.", "De man zegt: nee.", "Hij laat Sam niet naar binnen gaan."], "Gaat Sam naar binnen?", "nee",
      "A man stands in a doorway with one palm raised; Sam stands outside."),
  ],
  note="Wiktionary sense 2. Example 4 shows a refusal, so the verb cannot be read as pushing someone."),

 dict(verb="laten", sense="veroorzaken dat het gebeurt (to have something done; laten zien, to show)", gloss="to have done, to show", band="A1",
  band_why="laten is A0 by lemma rank, but this sense (laten zien, laten maken) is A1 by judgement",
  tier=3, forms={"laten", "laat"},
  skip="Wiktionary lists laten zien under this causative sense, not as a separate entry.",
  picture="Anna holds a photo out towards Piet, who leans in to look. The photo's back faces us: no picture shown inside it.",
  mark="The held-out photo and the leaning figure: one gives, one sees.",
  alt="Een persoon houdt een foto omhoog naar een ander, die zich naar voren buigt om te kijken.",
  examples=[
   ex(["Anna heeft een nieuwe foto.", "Zij laat de foto aan Piet zien.", "Nu ziet Piet de foto."], "Ziet Piet de foto nu?", "ja"),
   ex(["Piet laat zijn fiets maken.", "Hij maakt de fiets niet zelf.", "Een man in de winkel maakt de fiets."], "Maakt Piet de fiets zelf?", "nee",
      "A bicycle on a shop counter; a mechanic works on it; Piet stands back with hands in pockets."),
   ex(["Sam heeft een nieuw huis.", "Hij laat Anna zijn huis zien.", "Zij gaat naar binnen en ziet de kamer."], "Ziet Anna het huis?", "ja",
      "Sam at an open front door with a sweep of the hand inward; Anna on the threshold."),
   ex(["Anna heeft een probleem.", "Zij kan het niet zelf doen.", "Zij laat haar vader komen.", "Haar vader komt naar het huis."], "Komt de vader naar het huis?", "ja",
      "Anna at a door pointing inside; a man walks up the path."),
  ],
  note="Two meanings of one pattern: the person shows, or the person arranges for someone else to act."),

 dict(verb="begrijpen", sense="to understand", gloss="to understand", tier=3, forms={"begrijpen", "begrijpt"},
  skip="Skip reason today: understanding has no single picturable action.",
  picture="Two panels: a figure frowning at a drawing, then the same figure with a raised head and open eyes beside the same drawing.",
  mark="The same drawing in both panels; only the face changes.",
  alt="Twee tekeningen: eerst kijkt iemand fronsend naar een plaatje, daarna kijkt dezelfde persoon blij naar hetzelfde plaatje.",
  examples=[ex(["Anna luistert naar Piet.", "Eerst weet zij het niet.", "Dan zegt Piet het nog een keer.", "Nu begrijpt zij het."], "Weet Anna het nu?", "ja")],
  note="Two panels need the larger card size, not the 170 px thumbnail."),

 dict(verb="hopen", sense="to hope", gloss="to hope", tier=3, forms={"hopen", "hoopt"},
  skip="Skip reason today: the umbrella symbol is not on the closed list of conventions.",
  picture="A figure at a window looks out, hands together near the chin. Outside is a plain sky with one small shape that could be a cloud or a sun.",
  mark="The unresolved sky: the figure does not yet know the outcome.",
  alt="Een persoon staat bij een raam met de handen bij de kin en kijkt naar de lucht buiten.",
  examples=[ex(["Els wil morgen buiten zijn.", "Zij weet niet of er morgen zon is.", "Zij hoopt van wel."], "Weet Els al of er zon is?", "nee")],
  note="Hope is wanting plus not knowing; the question tests the not-knowing."),

 dict(verb="proberen", sense="to try", gloss="to try", tier=3, forms={"proberen", "probeert"},
  skip="Skip reason today: the key-in-the-wrong-lock picture is the literal action, not the verb.",
  picture="A figure bent over a bicycle with a wrench, a tyre half off, sweat marks near the head. A second bicycle stands finished and upright in the background.",
  mark="Work in progress next to the finished bicycle.",
  alt="Een persoon werkt aan een fiets met een sleutel; de band zit half los. Op de achtergrond staat een heel gemaakte fiets.",
  examples=[ex(["Piet probeert zijn fiets te maken.", "Hij werkt al een uur.", "Het is nog niet goed."], "Is de fiets nu al klaar?", "nee")],
  note="Sense chosen: attempt without success yet."),

 dict(verb="twijfelen", sense="geen vertrouwen in iets of iemand hebben (doubting oneself)", gloss="to doubt (oneself)", tier=2, forms={"twijfelen", "twijfelt"},
  skip="Skip reason today: a thought, feeling or attitude, not a visible action.",
  picture="A figure stands at the edge of a platform with a wide gap to a second platform. One foot forward, weight on the back foot. A split thought bubble: one half a small figure landing on the far side, the other the same figure falling into the gap.",
  mark="The split thought bubble: two possible outcomes, none chosen.",
  alt="Een persoon staat aan de rand van een brede kloof. In een gedachtewolk landt een figuurtje aan de overkant, en valt een figuurtje in de kloof.",
  examples=[
   ex(["Jan staat voor de sprong.", "Hij denkt: kan ik dat wel?", "Hij twijfelt aan zichzelf."], "Is Jan zeker dat hij kan springen?", "nee"),
   ex(["Eva heeft morgen een examen.", "Zij heeft veel geleerd.", "Maar zij twijfelt aan zichzelf."], "Is Eva zeker van zichzelf?", "nee",
      "A figure at a desk with books; a thought bubble showing a sheet with a tick and the same sheet crossed out (marks, no letters)."),
   ex(["Piet moet voor de groep praten.", "Hij denkt: kan ik dat?", "Hij twijfelt aan zichzelf."], "Denkt Piet dat hij het goed kan?", "nee",
      "A figure at the front of a row of seated figures; the thought bubble shows a figure speaking and the same figure silent."),
   ex(["Anna wil een nieuwe baan.", "De baan is moeilijk.", "Zij twijfelt aan zichzelf."], "Weet Anna zeker dat zij het kan?", "nee",
      "A figure at a door marked by a bag and a desk; the thought bubble splits into two outcomes."),
  ],
  note="Wiktionary sense 4. Replaces the earlier two-sweaters idea: it shows doubt about one's own ability."),

 dict(verb="twijfelen", sense="tussen twee dingen niet kunnen kiezen (to be unable to choose)", gloss="to waver between two things", tier=3, forms={"twijfelen", "twijfelt"},
  skip="Wiktionary senses 1 and 3 (twijfelen tussen; geen keuze kunnen maken), merged: they differ only in wording.",
  picture="A figure holds up two identical sweaters, one in each hand, and looks from one to the other. Nothing is chosen yet.",
  mark="The eyes and head turned between the two, with neither sweater put down.",
  alt="Een persoon houdt in elke hand een trui omhoog en kijkt van de ene naar de andere.",
  examples=[
   ex(["In de winkel hangen twee jurken.", "Eva wil één jurk kopen.", "Zij twijfelt tussen de lange en de korte jurk."], "Heeft Eva al een jurk gekozen?", "nee"),
   ex(["Sam kan in Utrecht wonen of in Delft.", "Hij twijfelt tussen Utrecht en Delft."], "Weet Sam al waar hij gaat wonen?", "nee",
      "A figure at a fork in a path, one arrow to each side, standing still between them."),
   ex(["In het restaurant is er soep of vis.", "Piet twijfelt tussen soep en vis.", "De man wacht."], "Heeft Piet al gekozen?", "nee",
      "A figure at a table with a menu card (strokes only); a waiter with a pad, waiting."),
   ex(["Eerst twijfelt Els tussen twee fietsen.", "Dan kiest zij één fiets."], "Twijfelt Els nu nog?", "nee",
      "Two panels: a figure between two bicycles; the same figure wheeling one away."),
  ],
  note="Example 4 shows doubt ending, which makes the verb's boundary visible."),

 dict(verb="beweren", sense="to claim", gloss="to claim", tier=3, forms={"beweren", "beweert"},
  skip="Skip reason today: speech whose content is the meaning; the picture would be the praten card.",
  picture="A figure on a low box, one finger raised, chest out. A second figure stands with crossed arms and one raised eyebrow.",
  mark="The raised finger against the crossed arms.",
  alt="Een persoon staat op een kistje met een opgestoken vinger. Een ander staat met de armen over elkaar en kijkt twijfelend.",
  examples=[ex(["Mark zegt: mijn fiets is de snelste van de stad.", "Niemand heeft het gezien.", "Mark beweert het."], "Weet iedereen dat het waar is?", "nee")],
  note="Contrast partner: twijfelen (certain claim against unsure listener)."),

 dict(verb="vertegenwoordigen", sense="spreken of aanwezig zijn in naam van een groep of organisatie (Wiktionary lists one sense)", gloss="to represent", tier=3, forms={"vertegenwoordigen", "vertegenwoordigt"},
  skip="Skip reason today: abstract; any picture would stand in for another verb.",
  picture="A row of small figures stands behind one larger figure at a table. Only the larger figure reaches across to shake hands with a person on the other side.",
  mark="One figure steps forward from a group while the rest stay back.",
  alt="Een rij kleine figuurtjes staat achter één groter figuur aan een tafel. Alleen dat figuur geeft een hand aan iemand aan de overkant.",
  examples=[
   ex(["De buren hebben een probleem met het lawaai.", "Zij kiezen Els.", "Els praat voor alle buren met de gemeente.", "Els vertegenwoordigt de buurt."], "Praat Els alleen voor zichzelf?", "nee"),
   ex(["De koning kan niet naar het feest in een ander land komen.", "Zijn zoon gaat wel.", "Hij vertegenwoordigt zijn vader."], "Is de koning zelf op het feest?", "nee",
      "An empty chair with a crown on it at one side of a hall; a younger figure standing in the doorway of the hall."),
   ex(["Piet heeft een probleem met zijn huis.", "Hij gaat niet zelf naar de rechter.", "Zijn advocaat gaat.", "De advocaat vertegenwoordigt Piet."], "Praat Piet zelf met de rechter?", "nee",
      "A figure with a folder at a high desk facing a judge; Piet stands outside the open door."),
   ex(["Anna speelt voor Nederland in een ander land.", "Zij vertegenwoordigt Nederland."], "Speelt Anna voor Nederland?", "ja",
      "A figure on a pitch beside a flag (no emblem, strokes only), a crowd behind a fence."),
  ],
  note="Group, person and country, one sense. Logo and facial-expression uses are not in Wiktionary for this verb; Dutch seems to use other verbs there (unverified)."),

 dict(verb="aarzelen", sense="onzeker zijn, twijfelen (to hesitate)", gloss="to hesitate", tier=3, forms={"aarzelen", "aarzelt"},
  skip="Skip reason today: a thought, feeling or attitude, not a visible action.",
  picture="A figure stands at a closed door with one hand raised towards the handle, not touching it. The other hand is pulled back to the chest.",
  mark="The hand stopped short of the handle.",
  alt="Een persoon staat bij een dichte deur met een hand vlak voor de klink, maar raakt die niet aan.",
  examples=[
   ex(["Piet staat bij de deur.", "Hij aarzelt even.", "Dan doet hij de deur open."], "Is de deur nu open?", "ja"),
   ex(["Eva moet iets zeggen.", "Zij aarzelt even.", "Dan zegt zij het toch."], "Zegt Eva het uiteindelijk?", "ja",
      "A figure with a raised hand and an open mouth held back; second panel: the mouth open and speaking."),
   ex(["De vrouw heeft een vraag.", "Zij aarzelt niet.", "Zij stelt de vraag meteen."], "Wacht zij lang?", "nee",
      "A figure with an arm raised straight up at once, no pause marks."),
   ex(["Sam staat voor het water.", "Hij aarzelt even.", "Dan springt hij erin."], "Springt Sam in het water?", "ja",
      "Two panels: a figure at the edge, knees bent and still; the same figure mid-air above the water."),
  ],
  note="Wiktionary has one sense, glossed as twijfelen; its examples are all 'pause, then act'. The pair below turns that into the contrast."),

 dict(verb="vermoeden", key="vermoeden (verb)", sense="to suspect, to guess", gloss="to suspect, to guess", tier=3, forms={"vermoeden", "vermoedt"},
  skip="Skip reason today: a thought, feeling or attitude, not a visible action.",
  picture="Front of a house at dusk: the windows are dark and a car stands at the door. A figure on the pavement looks up, finger at the chin.",
  mark="Dark windows with the car outside.",
  alt="Een huis in de avond met donkere ramen. Voor de deur staat een auto. Een persoon op de stoep kijkt omhoog.",
  examples=[ex(["Het huis van de buurman is donker.", "Maar zijn auto staat voor de deur.", "Eva vermoedt: hij slaapt."], "Weet Eva zeker dat hij slaapt?", "nee")],
  note="The picture gives the evidence; the text gives the guess."),
]

MOVED = {"worden", "laten", "begrijpen", "hopen", "proberen"}
ENTRIES = []  # every pilot card now lives in tools/_ex_tmp/*.json and the family pages
PAIR = []
PAIR_NOTE = ""

# ----------------------------------------------------------------------
CSS = """
.mock{margin:0;border:2px solid var(--kobalt);border-radius:14px;padding:14px;background:var(--papier)}
.mock .pic{border:1.5px dashed var(--lijn);border-radius:10px;padding:18px 10px;text-align:center;font-size:12.5px;color:var(--grijs)}
.mock .tekst{margin:12px 0 4px;font-size:17px;font-weight:600;line-height:1.45}
.mock .tekst p{margin:2px 0}
.mock .vraag{margin:10px 0 8px;font-size:17px;font-weight:800;color:var(--kobalt)}
.mock .knoppen{display:flex;gap:10px}
.mock .knoppen span{flex:1;text-align:center;padding:8px;border:2px solid var(--kobalt);border-radius:10px;font-weight:800;font-size:16px}
.mock .uitkomst{margin-top:8px;font-size:12px;color:var(--grijs)}
.mocks{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin:1em 0}
.ok{color:var(--kobalt);font-weight:700}.fout{color:var(--rood);font-weight:700}
"""

def mock(example, pic, gloss):
    t = "".join(f"<p>{e(s)}</p>" for s in example["text"])
    t = f'<div class="tekst">{t}</div>' if t else ""
    return (f'<div class="mock" aria-label="Mock of the game screen"><div class="pic">{e(pic)}</div>{t}'
            f'<div class="vraag">{e(example["question"])}</div>'
            f'<div class="knoppen"><span>ja</span><span>nee</span></div>'
            f'<div class="uitkomst">Right answer: <b>{e(example["answer"])}</b>. Then the gloss: {e(gloss)}.</div></div>')

def build(ranks):
    rows, sections, fail = [], [], False
    for en in ENTRIES:
        band = card_band(en, ranks)
        rank = ranks[en.get("key", en["verb"])]
        worst_all, issues = (0, ""), []
        for exm in en["examples"]:
            w, bad, unk = check_ex(en["forms"], exm, band, ranks)
            if w[0] > worst_all[0]: worst_all = w
            issues += bad + [f"unresolved {u}" for u in unk]
        if issues: fail = True
        status = "OK" if not issues else "; ".join(issues)
        slug = re.sub(r"[^a-z]+", "-", (en["verb"] + "-" + en["sense"].split("(")[0]).lower()).strip("-")[:40]
        n = len(en["examples"])
        rows.append(f'<tr><td><a href="#{slug}">{e(en["verb"])}</a> <span>({e(en["sense"].split("(")[-1].rstrip(")") if "(" in en["sense"] else en["sense"])})</span></td><td>{band}</td><td>{n}</td>'
                    f'<td>{e(worst_all[1]) or "—"} (rank {worst_all[0]})</td><td class="{"ok" if not issues else "fout"}">{e(status)}</td></tr>')
        band_note = f' Band set by hand: {e(en["band_why"])}.' if en.get("band") else ""
        mocks = "".join(mock(exm, exm["scene"] or ("picture: " + en["mark"]), en["gloss"]) for exm in en["examples"])
        more = "" if n > 1 else '<p><em>One example so far; not expanded to four yet.</em></p>'
        sections.append(
            f'<h3 id="{slug}">{e(en["verb"])} — {e(en["sense"])}</h3>'
            f'<p><strong>Band {band}</strong> (lemma rank {rank}) · <strong>Tier {en["tier"]}</strong> · {n} example{"s" if n != 1 else ""}.{band_note} {e(en["skip"])}</p>'
            f'<div class="table-wrap"><table><tbody>'
            f'<tr><th>Scene (example 1)</th><td>{e(en["picture"])}</td></tr>'
            f'<tr><th>Must read</th><td>{e(en["mark"])}</td></tr>'
            f'<tr><th>Alt text (Dutch)</th><td>{e(en["alt"])}</td></tr>'
            f'<tr><th>Note</th><td>{e(en["note"])}</td></tr></tbody></table></div>'
            f'<div class="mocks">{mocks}</div>{more}')
    # pair
    pair_html, pair_rows = "", []
    for pr in PAIR:
        band = band_of(ranks[pr["verb"]])
        w, bad, unk = check_ex(pr["forms"], pr["ex"], band, ranks)
        if bad or unk: fail = True
        pair_rows.append((pr["verb"], band, w, bad, unk))
        pair_html += mock(pr["ex"], f"picture: same figure, same door; {pr['verb']}", pr["verb"])
    return rows, sections, pair_html, pair_rows, fail

def main():
    ranks = load_ranks()
    rows, sections, pair_html, pair_rows, fail = build(ranks)
    tpl = open(TEMPLATE, encoding="utf-8").read()
    head, rest = tpl.split('<main id="main">', 1)
    _, tail = rest.split("</main>", 1)
    head = head.replace("Card families handover — Oefenpad documentation", "Explanation cards pilot — Oefenpad documentation")
    head = head.replace("</style>", CSS + "</style>", 1)
    head = head.replace(' aria-current="page"', "")
    head = head.replace('data-path="Docs/explanation-cards-pilot.html"', 'data-path="Docs/explanation-cards-pilot.html" aria-current="page"')
    ovr = "".join(f"<tr><td>{e(w)}</td><td>{r}</td><td>{band_of(r)}</td><td>{e(why)}</td></tr>" for w, (r, why) in OVERRIDES.items())
    nex = sum(len(x["examples"]) for x in ENTRIES)
    article = f"""
    <nav class="crumbs" aria-label="Breadcrumb">
      <a href="index.html">Docs</a><span>/</span><span>Card families</span>
    </nav>
    <header class="doc-head">
      <h1>Explanation cards pilot</h1>
      <p class="lede">Skipped verbs rebuilt as picture cards, picture-plus-question cards or short Dutch scenes, one card per sense, so the owner can judge the format before any rule changes.</p>
      <p class="doc-meta">Docs/explanation-cards-pilot.html · built by tools/build-explanation-pilot.py</p>
    </header>
    <article class="prose">
<h2 id="what">What this pilot tests</h2>
<p>It tests whether verbs with no honest single drawing can be taught with a picture, a short Dutch scene and one yes/no question. No drawings exist; each card is a brief and a static mock of the game screen.</p>
<div class="table-wrap"><table><thead><tr><th>Tier</th><th>When</th><th>The learner gets</th></tr></thead><tbody>
<tr><td>1. Picture</td><td>One mark carries the meaning</td><td>A single picture, as in the existing families</td></tr>
<tr><td>2. Picture + check</td><td>The picture is clear but could be misread</td><td>The picture and one yes/no question</td></tr>
<tr><td>3. Scene + text</td><td>No single picture carries the verb</td><td>A fuller scene, two to four short Dutch sentences and one question</td></tr>
</tbody></table></div>
<p>The Dutch sits beside the picture, never inside it, so the no-text-in-artwork rule holds. Two earlier rules were amended for this card type on 20 November 2026: no example sentences on verb cards, and meaning never in a sentence the learner must parse. The rules are in <code>Docs/decisions.html</code>.</p>

<h2 id="senses">Senses and examples</h2>
<p>A verb gets one card per sense, and each card shows four examples. The senses come from {e(SRC)}, not from the English gloss.</p>
<div class="table-wrap"><table><thead><tr><th>Verb</th><th>Sense cards here</th><th>Wiktionary lists</th><th>Not covered yet</th></tr></thead><tbody>
<tr><td>twijfelen</td><td>doubt oneself; waver between two things</td><td>4 senses</td><td>doubt whether something is true (twijfelen aan)</td></tr>
<tr><td>vertegenwoordigen</td><td>act in the name of a group</td><td>1 sense</td><td>none; logo and expression uses are not listed</td></tr>
<tr><td>aarzelen</td><td>hesitate</td><td>1 sense</td><td>none</td></tr>
</tbody></table></div>
<p>The pilot is finished: every pilot card now lives in <a href="explanation-cards/index.html">Explanation cards</a>, which covers A0 to B2 and is the page to use. This page stays as the record of the pilot and its three tiers.</p>

<h2 id="pair">Aarzelen and twijfelen overlap</h2>
<p>Dutch Wiktionary glosses aarzelen as "onzeker zijn, twijfelen" and lists twijfelen among its synonyms, so the two are not a clean contrast pair. The pilot therefore teaches them from different scenes: aarzelen is a pause before acting, twijfelen is doubting oneself or being unable to choose between two things. No shared door scene is used.</p>

<h2 id="check">Vocabulary check</h2>
<p>Every Dutch word on a card is at or below the card's band by lemma rank, except the verb itself. A failing row means the build fails. The page holds {nex} examples in {len(ENTRIES)} cards.</p>
<div class="table-wrap"><table><thead><tr><th>Card</th><th>Band</th><th>Examples</th><th>Highest word</th><th>Result</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table></div>
<details><summary>How the check works and where it is weak</summary>
<ul>
<li>Bands by lemma rank: A0 up to 250, A1 to 1000, A2 to 2500, B1 to 5000, B2 to 10000 (<code>tools/lexicon/woorden-niveau.tsv</code>). A card can carry a band set by hand when one sense is later than the lemma.</li>
<li>Inflected forms are mapped to lemmas by suffix rules and a small table. Where a form has several homograph keys the best rank is used, so the check is generous there.</li>
<li>Names are exempt. The check does not judge grammar or naturalness: a native speaker has not read any of this text.</li>
</ul></details>

<h2 id="hand">Ranks set by hand</h2>
<p>The lexicon rank is wrong for these words, as it was for the verb pages, so the check uses the rank below. Each is judgement, not a count.</p>
<div class="table-wrap"><table><thead><tr><th>Word</th><th>Rank used</th><th>Band</th><th>Why</th></tr></thead><tbody>
{ovr}
</tbody></table></div>

<h2 id="cards">The cards</h2>
{''.join(sections)}

<h2 id="open">What is open</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Note</th></tr></thead><tbody>
<tr><td>Native check</td><td>All Dutch text and alt text here is AI-written and unchecked by a native speaker.</td></tr>
<tr><td>Rules</td><td>Recorded in <code>Docs/decisions.html</code> and <code>Docs/project-rules.html</code> on 20 November 2026.</td></tr>

<tr><td>Alt text for examples 2 to 4</td><td>Scene lines only; alt text is written at drawing time.</td></tr>
<tr><td>Larger card size</td><td>Two-panel scenes (begrijpen, worden, aarzelen) do not read at 170 px. Needs a larger size on tier 3 cards.</td></tr>
<tr><td>Drawings</td><td>None made; the illustrator batch costs money and the owner said not to draw yet.</td></tr>
</tbody></table></div>
    </article>
    <footer class="footer">
      <code>Docs/explanation-cards-pilot.html</code> · Oefenpad documentation. This page is the document.
    </footer>
  """
    open(OUT, "w", encoding="utf-8").write(head + '<main id="main">' + article + "</main>" + tail)
    print("wrote", OUT)
    for r in rows:
        print(re.sub(r"<[^>]+>", " ", r))
    for v, b, w, bad, unk in pair_rows:
        print("pair", v, b, w, bad, unk)
    if fail:
        print("CHECK FAILED"); sys.exit(1)

if __name__ == "__main__":
    main()
