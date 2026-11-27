#!/usr/bin/env python3
"""Build the A0-B2 verb-card selection for Docs/werkwoorden.

Selection is by lexicon frequency rank:
  A0  rank <= 250
  A1  rank 251-1000
  A2  every usable verb in 1001-2500 (the regular cap of 60 was lifted 20 Nov 2026)
  B1  every usable verb in 2501-5000 (the regular cap was lifted 20 Nov 2026)
  B2  every usable verb in 5001-10000

From B1 on, every usable verb is on a page: either as a card or as a SKIP row
with its reason in scenes/<page>.tsv.  Drawable verbs left for a later pass are
in LATER and go to the backlog with that reason.

A verb is irregular when Bijlage 3b lists it, when it is an inseparable or
separable prefix on a listed base (vervangen, bezoeken, beschrijven), or when
it is in EXTRA_IRREGULAR (strong verbs the appendix lacks: meten, heffen).
A verb is separable when Bijlage 4 or the hand list says so, or when it starts
with an unambiguous separable particle on a known verb (nadenken, ophouden).
Rank is the wordfreq rank of the spelling; where that spelling is also a
common noun plural (boeken, landen, wijken) the rank is overridden by hand in
rank_of, because the noun inflates it.

Separable, reflexive, sensitive and no-rank verbs are held back and written to
backlog_seed.tsv instead.  Output is JSON plus one TSV per page.
"""
import csv
import json
import os
import re
import subprocess
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "..", "lexicon")
OUT = HERE
DUTCH = "/media/tony/Data/Dutch"

IRREGULAR_PDF = os.path.join(DUTCH, "Bijlage-3b-Onregelmatige-werkwoorden-alfabetisch.pdf")
SEPARABLE_PDF = os.path.join(DUTCH, "Bijlage-4-Scheidbare-werkwoorden.pdf")


def norm(nl):
    return re.sub(r"\s*\([^)]*\)$", "", nl).strip()


GLOSS = {
    "bezorgen": "to deliver", "wandelen": "to go for a walk", "verplaatsen": "to move (an object)",
    "ondersteunen": "to support (help)", "rekenen": "to calculate", "tellen": "to count (things)",
    "kussen": "to kiss (on the cheek)", "branden": "to burn (a fire)", "trappen": "to kick (a can, a ball)",
    # Gloss fixes, 26 Nov 2026 (lexicon glosses were wrong; found in the skipped-verb triage).
    "heersen": "to reign, to prevail", "verkeren": "to be in a state, to mix with",
    "incasseren": "to collect (money), to take a blow", "promoveren": "to gain a doctorate, to be promoted",
    # Gloss qualifiers, 27 Nov 2026 (two cards shared one English gloss after the relaxed-rule cards were added).
    "resteren": "to be left over", "bewerken": "to edit, to work on", "bespelen": "to play (a piano, a stage)",
    "prijken": "to be displayed proudly", "runnen": "to run (a business)", "vertonen": "to show (screen, display)",
    "innen": "to collect (a payment)", "mislukken": "to fail (go wrong)", "verstrekken": "to provide (hand out)",
    "verstoren": "to disrupt", "beletten": "to prevent (forbid, block)", "overheersen": "to dominate (rule over)",
    "pogen": "to strive, to try hard",
    "bekomen": "to agree with (food)", "hernemen": "to take again (retake)",
    "vernemen": "to hear (learn of)", "ontgaan": "to escape (notice)", "bedwingen": "to restrain (subdue)",
    "witwassen": "to launder money", "verpesten": "to spoil", "ontbinden": "to dissolve",
    "betrappen": "to catch (in the act)",
    "ontsnappen": "to escape",  # the lexicon gloss 'to relax' is a data error

    # Fix pass 3, 20 Nov 2026: the carded sense of a former "two senses" SKIP.
    "ruimen": "to clear (snow, rubble)",
    "schakelen": "to change gear",
    "isoleren": "to insulate",
    "pikken": "to peck",
    "stoken": "to stoke (a fire)",
    "zorgen": "to take care (of)",
    "worden": "to become",
    "kunnen": "to be able to",
    "moeten": "to have to",
    "willen": "to want",
    "zullen": "will",
    "houden": "to hold / to keep",
    "vinden": "to find",
    "laten": "to let",
    "stellen": "to put / to pose",
    "voeren": "to feed (animals)",
    "ontstaan": "to arise, to originate",
    "trekken": "to pull",
    "steken": "to stick (in)",
    "wijken": "to give way",
    "verstaan": "to understand (what is said)",
    "schuiven": "to slide (something), to push",
    "zwijgen": "to be silent",
    "scheppen": "to scoop, to shovel",
    "scheiden": "to separate",
    "schijnen": "to shine",
    "missen": "to miss (a bus)",
    "passen": "to try on / to fit",
    "verbinden": "to bandage",
    "stijgen": "to rise",
    "sparen": "to save (money)",
    "leven": "to live (be alive)",
    "wonen": "to live (reside)",
    "zetten": "to put (upright)",
    "leggen": "to lay (flat)",
    "weten": "to know (a fact)",
    "kennen": "to know (a person, a place)",
    "draaien": "to turn (round)",
    "nemen": "to take",
    "pakken": "to grab",
    "roepen": "to call (out)",
    "beginnen": "to begin",
    "starten": "to start (a race)",
    "varen": "to sail (a boat, a ferry)",
    "zeilen": "to sail (with a sail)",
    "stappen": "to step",
    "halen": "to fetch",
    "grijpen": "to seize",
    "dringen": "to push in (a queue)",
    "verlaten": "to leave (a place)",
    "vertrekken": "to depart",
    "ontslaan": "to dismiss (from a job)",
    "vermogen": "to be able to (formal)",
    "spinnen": "to spin (thread); to purr",
    "overvallen": "to raid, to hold up",
    "begeven": "to give way, to break down",
    "laden": "to load",
    "heffen": "to raise, to levy",
    "stoten": "to bump, to knock",
    "blijken": "to turn out",
    "bestrijden": "to combat",
    "behoren": "to belong",
    "kampen": "to struggle",
    "duren": "to last",
    "lossen": "to unload",
    "regelen": "to arrange",
    "bellen": "to call (by phone)",
    "boeken": "to book",
    "plaatsen": "to place",
    "leiden": "to lead",
    "keren": "to turn (back)",
    "redden": "to save (rescue)",
    "eisen": "to demand",
    "reageren": "to react",
    "dromen": "to dream",
    # B1/B2 pass, 20 Nov 2026: one sense per card, the sense drawn.
    "douchen": "to shower", "voeden": "to feed (a baby)", "winkelen": "to go shopping",
    "ruilen": "to swap", "repareren": "to repair", "zoenen": "to kiss",
    "voetballen": "to play football", "fotograferen": "to take a photo",
    "plakken": "to stick (on)", "verwelkomen": "to welcome", "wekken": "to wake (someone)",
    "knippen": "to cut (with scissors)", "serveren": "to serve (food)", "slikken": "to swallow",
    "plukken": "to pick (fruit)", "versieren": "to decorate", "likken": "to lick",
    "zaaien": "to sow", "juichen": "to cheer", "mengen": "to mix", "slopen": "to demolish",
    "vegen": "to sweep", "boren": "to drill", "poetsen": "to brush (teeth)",
    "scheuren": "to tear", "kraken": "to crack (a nut)", "schaken": "to play chess",
    "skiën": "to ski", "smelten": "to melt", "fluiten": "to whistle", "schuilen": "to shelter",
    "glijden": "to slide (down)", "knijpen": "to pinch", "wrijven": "to rub", "vouwen": "to fold",
    "stinken": "to stink", "waaien": "to blow (wind)", "sluipen": "to sneak",
    "behangen": "to wallpaper", "rijgen": "to thread (beads)", "druipen": "to drip",
    "ontwijken": "to dodge", "verjagen": "to chase away", "schaatsen": "to skate",
    "remmen": "to brake", "hakken": "to chop (wood)", "smeren": "to spread (butter)",
    "krabben": "to scratch", "knuffelen": "to cuddle", "persen": "to squeeze (juice)",
    "drogen": "to dry", "zweten": "to sweat", "hoesten": "to cough",
    "blussen": "to put out (a fire)", "tanken": "to fill up (fuel)", "tillen": "to lift",
    "botsen": "to bump (into)", "toveren": "to do magic", "troosten": "to comfort",
    "lassen": "to weld", "pinnen": "to pay by card", "grazen": "to graze",
    "verpakken": "to pack, to package", "blaffen": "to bark", "picknicken": "to picnic",
    "knielen": "to kneel", "fluisteren": "to whisper", "struikelen": "to trip",
    "gapen": "to yawn", "wippen": "to seesaw", "strelen": "to stroke", "wringen": "to wring (out)",
    "broeden": "to brood (eggs)", "gluren": "to peek", "mikken": "to aim",
    "brullen": "to roar", "schillen": "to peel", "stapelen": "to stack",
    "reiken": "to reach (for)", "golfen": "to play golf", "mediteren": "to meditate",
    "warmen": "to warm (up)", "bloeden": "to bleed",
    # Review fix pass, 20 Nov 2026: verbs carded after the B1/B2 review.
    "dekken": "to set (the table)", "zwaaien": "to wave (a flag)", "strijken": "to iron",
    "schommelen": "to swing (on a swing)", "gieten": "to pour", "wenken": "to beckon",
}


# The lexicon files one domain per lemma, usually from its most common nominal
# sense.  For a verb card the tag should name what the action is about, so a few
# dozen are corrected by hand.  Everything not listed keeps the lexicon value.
DOMAIN = {
    # Fix pass 3, 20 Nov 2026: the carded sense of a former "two senses" SKIP.
    "pikken": "Animals", "isoleren": "House & home", "stoken": "House & home",
    "schakelen": "Transport & travel", "ruimen": "Nature & weather",
    # Review fix pass, 20 Nov 2026.
    "zwaaien": "Movement & position", "dekken": "House & home", "strijken": "House & home",
    "wenken": "Communication & language", "schoppen": "Movement & position", "roeren": "Food & drink",
    "lekken": "House & home", "ondertekenen": "Work & jobs", "gieten": "Plants & farming",
    "liggen": "Movement & position", "vallen": "Movement & position",
    "trekken": "Movement & position", "stappen": "Movement & position",
    "treden": "Movement & position", "graven": "Movement & position",
    "zinken": "Movement & position", "stijgen": "Movement & position",
    "landen": "Transport & travel", "lossen": "Transport & travel",
    "leiden": "Abstract & general", "ontstaan": "Abstract & general",
    "verliezen": "Abstract & general", "veranderen": "Abstract & general",
    "redden": "Abstract & general", "breken": "Abstract & general",
    "gelden": "Abstract & general", "verbinden": "Abstract & general",
    "treffen": "Abstract & general", "beleven": "Abstract & general",
    "overnemen": "Abstract & general", "behalen": "Abstract & general",
    "bedenken": "Thought & knowledge",
    "bellen": "Communication & language",
    "melden": "Communication & language",
    "tonen": "Communication & language",
    "presenteren": "Communication & language",
    "zingen": "Arts & media", "tekenen": "Arts & media",
    "kleuren": "Arts & media", "schilderen": "Arts & media",
    "snijden": "Food & drink", "verzorgen": "Body & health",
    "ruiken": "Body & health", "wonen": "House & home",
    "grenzen": "Places & geography", "handhaven": "Law & conflict",
    "wensen": "Emotion & feeling",
    # B1/B2 pass, 20 Nov 2026: the new cards, by what the drawn action is about.
    "douchen": "House & home", "poetsen": "House & home", "vegen": "House & home", "versieren": "House & home", "behangen": "House & home", "vouwen": "House & home", "verpakken": "House & home", "drogen": "House & home", "wringen": "House & home", "wekken": "House & home", "knippen": "House & home", "druipen": "House & home",
    "mengen": "Food & drink", "schillen": "Food & drink", "smeren": "Food & drink", "kraken": "Food & drink", "likken": "Food & drink", "voeden": "Food & drink", "serveren": "Food & drink", "persen": "Food & drink",
    "zoenen": "People & relations", "knuffelen": "People & relations", "verwelkomen": "People & relations", "ruilen": "People & relations", "knijpen": "People & relations",
    "troosten": "Emotion & feeling",
    "repareren": "Technology & tools", "boren": "Technology & tools", "lassen": "Technology & tools", "slopen": "Technology & tools", "hakken": "Technology & tools",
    "zaaien": "Plants & farming", "plukken": "Plants & farming", "verjagen": "Plants & farming",
    "grazen": "Animals", "broeden": "Animals", "blaffen": "Animals", "brullen": "Animals",
    "smelten": "Nature & weather", "waaien": "Nature & weather", "schuilen": "Nature & weather",
    "voetballen": "Sport & games", "schaatsen": "Sport & games", "skiën": "Sport & games", "schaken": "Sport & games", "golfen": "Sport & games", "glijden": "Sport & games", "wippen": "Sport & games", "mikken": "Sport & games", "picknicken": "Sport & games", "stapelen": "Sport & games",
    "slikken": "Body & health", "zweten": "Body & health", "hoesten": "Body & health", "bloeden": "Body & health", "krabben": "Body & health", "gapen": "Body & health", "wrijven": "Body & health", "warmen": "Body & health", "stinken": "Body & health", "mediteren": "Body & health",
    "sluipen": "Movement & position", "ontwijken": "Movement & position", "struikelen": "Movement & position", "knielen": "Movement & position", "leunen": "Movement & position", "reiken": "Movement & position", "tillen": "Movement & position", "gluren": "Movement & position",
    "fluisteren": "Communication & language", "plakken": "Communication & language",
    "fluiten": "Arts & media", "toveren": "Arts & media", "fotograferen": "Arts & media", "rijgen": "Arts & media",
    "tanken": "Transport & travel", "remmen": "Transport & travel", "botsen": "Transport & travel", "blussen": "Work & jobs",
    	"pinnen": "Money & trade", "winkelen": "Money & trade",
}


# One card, one sense (decided 20 November 2026): a second sense of a verb that
# already has a card is carded under <slug>-<sense>.  A sense earns a card only
# when it has its own drawable action, its own English gloss, and no card of its
# own in another family.  Band, rank and forms come from the base verb: the
# frequency list counts spellings, so it cannot separate senses.  The scene rows
# sit in tools/_ww_tmp/scenes/<page>.tsv under the card id.
SECOND_SENSES = [
	("dragen", "kleding", "to wear", "Clothing & appearance"),
	("spelen", "muziek", "to play (an instrument)", "Arts & media"),
	("kloppen", "eieren", "to beat (eggs)", "Food & drink"),
	("bakken", "ei", "to fry", "Food & drink"),
	("poetsen", "schoenen", "to polish", "Clothing & appearance"),
	("schilderen", "muur", "to paint (a wall)", "House & home"),
	# 26 Nov 2026: the commoner or very different sense of a verb that already
	# has a card for its other sense.  Domain None = the base verb's domain.
	("houden", "van", "to love", None),
	("zetten", "koffie", "to make (coffee, tea)", None),
	("stoppen", "tas", "to put (into)", None),
	("schijnen", "zon", "to shine (sun)", None),
	("verliezen", "sleutels", "to lose (an object)", None),
	("missen", "doel", "to miss (a target)", None),
	("missen", "persoon", "to miss (someone)", None),
	("koken", "water", "to boil", None),
	("zakken", "examen", "to fail (an exam)", None),
	("drukken", "knop", "to press", None),
	("zwaaien", "hand", "to wave (goodbye)", None),
	("schudden", "hand", "to shake hands", None),
	("schenken", "drank", "to pour (a drink)", None),
	# 27 Nov 2026: second senses found while carding the verbs that had no card.
	("lenen", "uit", "to lend", None),
	("verzekeren", "gerust", "to assure", None),
	("storten", "afval", "to tip (waste)", None),
	("verzetten", "afspraak", "to reschedule", None),
	("overvallen", "verrassen", "to catch off guard", None),
	("overleggen", "document", "to present (a document)", None),
	("prikken", "datum", "to set a date", None),
	("schokken", "schrik", "to shock", None),
	("betogen", "argument", "to argue (a case)", None),
	("verdringen", "gevoel", "to repress (a feeling)", None),
	("laten", "knippen", "to have done (hair cut)", None),
	("demonstreren", "uitleg", "to demonstrate", None),
	("verbouwen", "gewas", "to grow (crops)", None),
	("stormen", "rennen", "to rush", None),
	("verkiezen", "stem", "to elect", None),
	("beleggen", "vergadering", "to convene (a meeting)", None),
	("zweren", "wond", "to fester", None),
	("verschuiven", "uitstellen", "to postpone", None),
	("treffen", "ontmoeten", "to meet up", None),
	("boeien", "handboeien", "to handcuff", None),
	("bedienen", "machine", "to run (a machine)", None),
	("besturen", "leiden", "to govern, to run", None),
	("scheppen", "maken", "to bring into being", None),
	("verlichten", "ontlasten", "to relieve", None),
	("haken", "vast", "to hook, to catch", None),
	("razen", "storm", "to howl (storm)", None),
	("herinneren", "aan", "to remind (someone of)", None),
	("behandelen", "onderwerp", "to deal with (a topic), to cover", None),
	("bevestigen", "vast", "to attach, to fasten", None),
	("lichten", "anker", "to lift (an anchor), to weigh", None),
	("bevallen", "bevalt", "to please, to suit", None),
	("vestigen", "aandacht", "to draw (attention) to", None),
	("kappen", "stoppen", "to quit, to stop", None),
	("hechten", "aan", "to be attached to", None),
	("sneuvelen", "breken", "to break, to smash (of things)", None),
	("brommen", "cel", "to serve time (in jail)", None),
]


# 27 Nov 2026: reflexive or hyphenated verbs that now have a scene brief; they are cards, not backlog.
FORCE_IN = {"schamen", "de-installeren", "concentreren", "spannen", "verschuilen", "verzoenen", "wildkamperen", "haasten", "amuseren", "verontschuldigen", "omringen", "wagen", "rekken", "verheugen", "bukken", "beklagen", "bemoeien", "vervelen", "ergeren", "gedragen", "veroorloven", "weerzien", "wapenen", "bevinden", "wildplukken", "vergissen", "verbeelden"}


def load_band_overrides():
    """slug -> band, from bands.tsv (26 Nov 2026 re-spread).

    The lexicon rank alone put abstract verbs in the early bands and left A0 with
    six regular verbs.  bands.tsv places a card by lexicon level, then rank, then
    how concrete and everyday the action is; a card not listed keeps the band
    its rank gives.  Slugs and drawings never change."""
    path = os.path.join(HERE, "bands.tsv")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return {r["slug"]: r["band"] for r in csv.DictReader(fh, delimiter="\t")}


BAND_OVERRIDE = load_band_overrides()


def slug_of(word):
    plain = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode()
    return plain.lower().replace("'", "").replace(" ", "-")


def _load_new_glosses():
    """glosses.tsv: the gloss that goes with a new scene brief; overrides GLOSS for the verbs it lists."""
    path = os.path.join(HERE, "glosses.tsv")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter="	"):
                GLOSS[r["verb"]] = r["gloss"]


_load_new_glosses()


def short_gloss(en, word=""):
    """Keep the first sense from the lexicon's a)/b) form."""
    if word in GLOSS:
        return GLOSS[word]
    en = en.strip()
    en = re.sub(r"^a\)\s*", "", en)
    en = re.split(r"\s+b\)\s+", en)[0]
    return en.strip()


def read_tsv(name):
    with open(os.path.join(LEX, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def pdf_text(path):
    return subprocess.run(
        ["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True
    ).stdout


# Strong or mixed verbs that Bijlage 3b does not list.  Each has a past or a
# participle a learner cannot predict (mat/gemeten, hief/geheven).
EXTRA_IRREGULAR = {
    "meten", "heffen", "laden", "spinnen", "stoten", "bergen", "werven",
    "schenden", "spannen", "weven", "barsten", "malen", "zouten", "melken",
    "zwellen", "vlechten", "schrijden", "rijzen", "kijven", "delven",
    "zwelgen", "wreken", "wijten", "wringen",
}

# Bijlage 3b lists the strong sense, but the carded sense is weak.
# scheppen: schiep/geschapen is "to create"; "to scoop" is schepte/geschept.
REGULAR_SENSE = {"scheppen"}

# Prefixes (inseparable and separable) that keep the base verb's strong forms:
# vervangen/verving, bezoeken/bezocht, aanvallen/viel aan.
PREFIXES = (
    "her", "ont", "ver", "be", "ge", "er", "over", "onder", "door", "om",
    "achter", "vol", "weer", "mis", "aan", "af", "bij", "in", "mee", "na",
    "op", "terug", "tegen", "toe", "uit", "weg", "los", "vast", "voor",
    "samen", "neer", "binnen", "buiten", "thuis",
)

# The lexicon marks these "(zich)", but the plain transitive verb is the
# common, drawable one: een tak buigen.
NOT_REFLEXIVE = {"buigen"}

# Prefix + listed base, yet weak: ontmoeten (ontmoette) is not moeten.
NOT_IRREGULAR = {"ontmoeten"}


def irregular_lemmas():
    found = set()
    for line in pdf_text(IRREGULAR_PDF).splitlines():
        m = re.match(r"^\s*([a-zëé]+)\s{2,}", line)
        if m and m.group(1) != "infinitief":
            found.add(m.group(1))
    return found | EXTRA_IRREGULAR


def is_irregular(key, listed):
    """Listed in 3b, or one or more prefixes on a listed base."""
    if key in REGULAR_SENSE or key in NOT_IRREGULAR:
        return False
    if key in listed:
        return True
    for p in PREFIXES:
        rest = key[len(p):]
        if key.startswith(p) and len(rest) >= 4 and is_irregular(rest, listed):
            return True
    return False


# Particles that are always separable when they stand before a verb.  over,
# onder, door, om, voor and achter are left out: they can be inseparable
# (overwinnen, onderzoeken, voorspellen), so those go in the hand list.
SEPARABLE_PARTICLES = (
    "aan", "af", "bij", "in", "mee", "na", "op", "terug", "tegen", "toe",
    "uit", "weg", "los", "vast", "neer", "samen", "binnen", "buiten",
    "thuis", "open", "dicht", "schoon", "kapot", "terecht", "langs", "rond",
)


def separable_lemmas(verb_keys):
    found = set()
    for line in pdf_text(SEPARABLE_PDF).splitlines():
        for m in re.finditer(r"([a-zëé]+)(?:,\s*(?:zich|\(zich\)))?\s+\d{1,2}\b", line):
            if m.group(1) in verb_keys:
                found.add(m.group(1))
    # Common separable verbs that the appendix does not list, or that are easy
    # to miss because they are derived from a strong base.
    found |= {
        "aanbieden", "aankomen", "aanmelden", "aannemen", "aanpakken",
        "aanpassen", "aanvragen", "afnemen", "afsluiten", "afwachten",
        "deelnemen", "doorgeven", "doorgaan", "indienen", "inschrijven",
        "instellen", "inzetten", "meedoen", "meenemen", "meespelen",
        "opbellen", "opendoen", "opgeven", "opnemen", "opruimen", "opstaan",
        "opsturen", "opzoeken", "overkomen", "plaatsvinden", "samenwonen",
        "samenwerken", "schoonmaken", "uitgaan", "uitgeven", "uitleggen",
        "uitvoeren", "uitzoeken", "vasthouden", "voorkomen", "voorstellen",
        "weggooien",
        # Ambiguous particles (over, voor, achter) and verbs the regex below
        # cannot see because their base is not in the verb list.
        "overnemen", "achterlaten", "voorlezen", "aanvallen", "loslaten",
        "nadenken", "ophouden", "toegeven", "terugkomen", "tegenhouden",
        "afspreken", "weggaan", "ophangen", "overstappen", "voorbereiden",
        "doorlopen", "overbrengen", "oversteken", "voordoen", "doorgeven",
        # B1/B2 pass, 20 Nov 2026: particle verbs the rules above miss.
        "hardlopen", "klaarmaken", "kennismaken", "gebruikmaken", "klaarkomen",
        "lesgeven", "uitnodigen", "opletten", "inloggen", "bezighouden", "voortzetten",
        "overgaan", "weergeven", "overgeven", "overdragen", "overlaten", "overlopen",
        "overblijven", "doornemen", "voorbijgaan", "achterblijven", "onderduiken",
        "opbergen", "doortrekken", "onderbrengen", "omkomen", "voorgaan",
        "doorverwijzen", "eruitzien", "voorafgaan", "voornemen", "overhouden",
        "voorschrijven", "weerzien", "autorijden", "kwijtraken", "overhalen",
        "overeenkomen", "omkleden", "vrijlaten", "teleurstellen", "waarmaken",
        "goedkeuren", "overmaken", "wegwezen", "ademhalen", "liefhebben", "stopzetten",
        "uitroeien", "lastigvallen", "doorzetten", "doorsturen", "doodgaan",
        "voorleggen", "oprapen", "bekendmaken", "inzamelen", "doodschieten",
        "terugblikken", "geruststellen", "goedkomen", "uitputten", "verderkomen",
        "vrijkomen", "doorvoeren", "omzetten", "vreemdgaan",
    }
    for key in verb_keys:
        for p in SEPARABLE_PARTICLES:
            rest = key[len(p):]
            if key.startswith(p) and len(rest) >= 4 and rest in verb_keys:
                found.add(key)
    return {w for w in found if w in verb_keys}


# Why each hand-set rank differs from the lexicon's.  Printed on the overview
# page; check-verb-cards.py fails an override that lands in the same band as the
# lexicon rank, because then it changes nothing and only hides the number.
RANK_REASON = {
    "zijn": "wordfreq gave the verb row no score of its own (zipf 2.38); the verb is the commonest word",
    "eten": "wordfreq gave the verb row no score of its own (zipf 2.38); core A0 verb",
    "kosten": "wordfreq gave the verb row no score of its own (zipf 2.38); everyday shop verb",
    "leven": "wordfreq gave the verb row no score of its own (zipf 2.38); common A1 verb",
    "bestaan": "wordfreq gave the verb row no score of its own (zipf 2.38); placed in A2",
    "kussen": "wordfreq gave the verb row no score of its own (zipf 2.38); placed in A2",
    "optreden": "wordfreq gave the verb row no score of its own (zipf 2.38); placed in B1",
    "boeken": "the spelling is mostly the plural of boek",
    "landen": "the spelling is mostly the plural of land",
    "plaatsen": "the spelling is mostly the plural of plaats",
    "stemmen": "the spelling is mostly the plural of stem",
    "plannen": "the spelling is mostly the plural of plan",
    "keren": "the spelling is mostly the plural of keer",
    "eisen": "the spelling is mostly the plural of eis",
    "wijken": "the spelling is mostly the plural of wijk",
    "graven": "the spelling is mostly the plural of graf",
    "golven": "the spelling is mostly the plural of golf",
    "remmen": "the spelling is also the plural of rem (the brakes); the verb alone is placed one band later",
    "hakken": "the spelling is also the plural of hak (heels); the verb alone is placed one band later",
}


# Drawable B1/B2 verbs not carded in the 20 Nov 2026 pass, with the reason.
# gieten and wenken were carded in the review fix pass the same day.
LATER = {
    "bedekken": "drawable, but Voorzetselpaden already draws it four times (bedekken met een deken, deksel, zeil, zand); a fifth cover-up picture would be the same scene.",
    "schuren": "drawable (sandpaper on a plank), but the spelling is also the plural of schuur, so the band needs a lemma count first.",
}


def rank_of(raw, lexicon_rank, tier, top2000):
    """Use the lexicon rank, repairing the handful of verb senses wordfreq
    failed to score (they come back as zipf 2.38 / rank ~9000)."""
    manual = {
        "zijn": 1, "eten": 250, "kosten": 450, "leven": 550,
        "bestaan": 1400, "kussen": 1800, "optreden": 3000,
        # The spelling is also a frequent noun plural (boeken, landen,
        # plaatsen, stemmen, plannen, keren, eisen, wijken, graven, golven),
        # which inflates the wordfreq rank.  Placed by hand, one band later;
        # judgement, not a lemma count.  delen, reizen, vieren, wegen, posten,
        # schatten and stromen keep their rank: the verb sense is the common one
        # or the band already fits.
        "boeken": 1500, "landen": 1300, "plaatsen": 1100, "stemmen": 1400,
        "plannen": 1600, "keren": 1700, "eisen": 1900,
        "wijken": 4000, "graven": 3000, "golven": 6000,
        # B1/B2 pass, 20 Nov 2026: noun plurals that inflate a B1 verb.
        # schaatsen was here too; the review of 20 Nov 2026 reverted it (the
        # singular schaats is rarer than the verb, so the plural cannot carry it).
        "remmen": 6000, "hakken": 6000,
    }
    key = norm(raw)
    if key in manual:
        return manual[key], "handmatig"
    return lexicon_rank, "rang"


def main():
    rows = read_tsv("woorden.tsv")
    pos = {r["nl"]: r["pos"] for r in read_tsv("woorden-woordsoort.tsv")}
    freq = {r["nl"]: int(r["rang"]) for r in read_tsv("woorden-frequentie.tsv")}
    domain = {norm(r["nl"]): r["domein"] for r in read_tsv("woorden-domein.tsv")}
    irregular = irregular_lemmas()

    verbs = {}
    for r in rows:
        if pos.get(r["nl"]) != "verb":
            continue
        key = norm(r["nl"])
        rank, source = rank_of(r["nl"], freq.get(r["nl"], 10**9), r["niveau"], r["top2000"])
        if key not in verbs or rank < verbs[key]["rank"]:
            verbs[key] = {
                "key": key,
                "lexeme": r["nl"],
                "gloss": short_gloss(r["en"], key),
                "rank": rank,
                "rank_source": source,
                "raw_rank": freq.get(r["nl"], 10**9),
                "rank_reason": RANK_REASON.get(key, "") if source == "handmatig" else "",
                "tier": r["niveau"],
                "top2000": r["top2000"],
                "domain": DOMAIN.get(key) or domain.get(key, ""),
                "reflexive": ("(zich)" in r["nl"] or ", zich" in r["nl"]) and key not in NOT_REFLEXIVE,
                "irregular": is_irregular(key, irregular),
                "slug": slug_of(key),
            }

    separable = separable_lemmas(set(verbs))
    sensitive = {"doden", "neuken", "schieten", "vermoorden",
                 # B1/B2 pass: sexual, violent or bodily-crude.
                 "verkrachten", "vrijen", "paren", "masturberen", "pissen", "plassen",
                 "kotsen", "executeren", "martelen", "ontvoeren", "bombarderen",
                 "slachten", "verdrinken", "naaien", "flirten", "verleiden"}
    odd = {"dagen", "ogen", "lesgven", "cc'en", "onderwerpen", "sporen",
           # B1/B2 pass: not verbs, misparsed, or a noun plural ranked as a verb.
           "pasen", "pleistoceen", "paleoceen", "misburik", "stammen", "kondigen",
           "schaffen", "geraken"}
    for key, v in verbs.items():
        v["separable"] = key in separable or "-" in key
        v["sensitive"] = key in sensitive
        v["odd"] = key in odd

    def usable(v):
        if slug_of(v["key"]) in FORCE_IN:
            return True
        return not (v["separable"] or v["reflexive"] or v["sensitive"] or v["odd"])

    def band(v):
        r = v["rank"]
        if r <= 250:
            return "A0"
        if r <= 1000:
            return "A1"
        if r <= 2500:
            return "A2"
        if r <= 5000:
            return "B1"
        if r <= 10000:
            return "B2"
        return None

    selected = []
    deferred = []

    for v in verbs.values():
        b = band(v)
        if b is None:
            continue
        if not usable(v):
            reasons = []
            if v["separable"]:
                reasons.append("separable")
            if v["reflexive"]:
                reasons.append("reflexive")
            if v["sensitive"]:
                reasons.append("sensitive")
            if v["odd"]:
                reasons.append("odd/rare")
            deferred.append({
                "verb": v["key"], "gloss": v["gloss"], "rank": v["rank"],
                "band": b, "reason": ", ".join(reasons),
            })
            continue
        selected.append(v)

    # A2 regulars are capped; irregulars are all kept.  B1 and B2 keep every
    # usable verb except the drawable ones in LATER, which wait for a later pass.
    for v in selected:
        if v["key"] in LATER and band(v) in ("B1", "B2"):
            deferred.append({
                "verb": v["key"], "gloss": v["gloss"], "rank": v["rank"],
                "band": band(v), "reason": "later pass",
                "note": LATER[v["key"]],
            })
    selected = [v for v in selected if not (v["key"] in LATER and band(v) in ("B1", "B2"))]
    for b, cap in (("A2", 10**6),):  # cap lifted 20 Nov 2026: every usable A2 regular is selected
        pool = [v for v in selected if band(v) == b and not v["irregular"]]
        pool.sort(key=lambda v: v["rank"])
        keep = {v["key"] for v in pool[:cap]}
        for v in pool[cap:]:
            deferred.append({
                "verb": v["key"], "gloss": v["gloss"], "rank": v["rank"],
                "band": b, "reason": "beyond page cap",
            })
        selected = [v for v in selected if band(v) != b or v["irregular"] or v["key"] in keep]

    # Write records.
    records = []
    for v in sorted(selected, key=lambda v: (v["rank"])):
        b = band(v)
        records.append({
            "band": BAND_OVERRIDE.get(v["slug"], b),
            "regularity": "irregular" if v["irregular"] else "regular",
            "verb": v["key"],
            "slug": v["slug"],
            "lexeme": v["lexeme"],
            "gloss": v["gloss"],
            "rank": v["rank"],
            "rank_source": v["rank_source"],
            "raw_rank": v["raw_rank"],
            "rank_reason": v["rank_reason"],
            "domain": v["domain"],
            "tier": v["tier"],
        })

    # One card per sense: a second sense of a carded verb is written as its own
    # record under <slug>-<sense>.  Band, rank and forms are the base verb's; the
    # id, the gloss, the domain and the scene are the sense's own.  The scene row
    # in the page TSV is keyed by the id, not by the verb.
    for base, sense, gloss, dom in SECOND_SENSES:
        src = next((r for r in records if r["verb"] == base), None)
        if src is None:
            sys.exit(f"second sense {base}-{sense}: {base} is not a card")
        slug = f"{src['slug']}-{sense}"
        records.append({**src, "slug": slug, "band": BAND_OVERRIDE.get(slug, src["band"]),
                        "gloss": gloss, "domain": dom or src["domain"], "sense": sense})

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "selection.json"), "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)

    pages = {}
    for b in ("A0", "A1", "A2", "B1", "B2"):
        for reg in ("regular", "irregular"):
            sub = [r for r in records if r["band"] == b and r["regularity"] == reg]
            pages[f"{b.lower()}-{reg}"] = sub
            with open(os.path.join(OUT, f"{b.lower()}-{reg}.tsv"), "w", encoding="utf-8") as fh:
                fh.write("verb\tslug\tgloss\trank\tdomain\n")
                for r in sub:
                    fh.write(f"{r['verb']}\t{r['slug']}\t{r['gloss']}\t{r['rank']}\t{r['domain']}\n")

    with open(os.path.join(OUT, "backlog_seed.tsv"), "w", encoding="utf-8") as fh:
        fh.write("verb\tgloss\trank\tband\treason\tnote\n")
        for r in sorted(deferred, key=lambda r: (r["band"], r["rank"])):
            fh.write(f"{r['verb']}\t{r['gloss']}\t{r['rank']}\t{r['band']}\t{r['reason']}\t{r.get('note', '')}\n")

    for name, sub in pages.items():
        irr = sum(1 for r in sub if r["regularity"] == "irregular")
        reg = len(sub) - irr
        print(f"{name:18} {len(sub):3}  irregular {irr:3}  regular {reg:3}")
    print(f"total selected {len(records)}")
    print(f"deferred {len(deferred)}")


if __name__ == "__main__":
    main()
