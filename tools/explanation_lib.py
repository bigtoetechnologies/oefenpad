"""Shared vocabulary check for explanation cards (pilot and family builders)."""
import csv, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEX = os.path.join(ROOT, "tools", "lexicon")
OUT = os.path.join(ROOT, "Docs", "explanation-cards-pilot.html")
TEMPLATE = os.path.join(ROOT, "Docs", "card-families-handover.html")

BANDS = [("A0", 250), ("A1", 1000), ("A2", 2500), ("B1", 5000), ("B2", 10000)]
def band_of(rank):
    for b, top in BANDS:
        if rank <= top:
            return b
    return "B2+"
CEIL = dict(BANDS)

NAMES = {"sam", "jan", "els", "mark", "anna", "piet", "eva", "utrecht", "delft", "nederland"}

# surface form -> lemma, for forms the suffix rules cannot reach
INFL = {
    "wordt": "worden", "zegt": "zeggen", "mag": "mogen", "weet": "weten",
    "kan": "kunnen", "is": "zijn", "ben": "zijn", "heeft": "hebben",
    "denkt": "denken", "ziet": "zien", "ging": "gaan", "gaat": "gaan",
    "staat": "staan", "komt": "komen", "doet": "doen", "laat": "laten",
    "hij": "hij", "zijn": "zijn", "hen": "hen", "zij": "zij, ze",
    "ze": "zij, ze", "wij": "wij, we", "we": "wij, we", "je": "jij, je",
    "mijn": "mijn, m’n", "ik": "ik", "heb": "hebben", "geen": "geen",
    "gemaakt": "maken", "gezien": "zien", "geweest": "zijn",
    "beste": "goed", "snelste": "snel", "grootste": "groot",
    "nog": "nog", "al": "al (pron)", "dan": "dan (conj)", "maar": "maar (conj)",
    "waar": "waar", "wat": "wat", "wie": "wie", "of": "of", "dat": "dat (conj)",
    "ja": "ja", "nee": "nee", "niet": "niet", "wel": "wel",
    "kijkt": "kijken", "loopt": "lopen", "woont": "wonen", "leeft": "leven (verb)", "ligt": "liggen",
    "kent": "kennen", "leest": "lezen", "geeft": "geven", "schrijft": "schrijven", "neemt": "nemen",
    "legt": "leggen", "draagt": "dragen", "eet": "eten", "blijft": "blijven", "kost": "kosten",
    "zet": "zetten", "wint": "winnen", "won": "winnen", "kwam": "komen", "gegeten": "eten",
    "zwemt": "zwemmen", "telt": "tellen", "vertelt": "vertellen", "betaalt": "betalen", "haalt": "halen",
    "kinderen": "kind", "huizen": "huis", "mannen": "man", "tassen": "tas", "jassen": "jas",
    "oren": "oor", "dozen": "doos", "zussen": "zus", "sneller": "snel", "groter": "groot", "sterker": "sterk",
    "had": "hebben", "hadden": "hebben", "wist": "weten", "zou": "zullen", "zouden": "zullen", "zal": "zullen",
    "nam": "nemen", "gaf": "geven", "zei": "zeggen", "bleef": "blijven", "dacht": "denken", "gedaan": "doen",
    "gestorven": "sterven", "kon": "kunnen", "konden": "kunnen", "kun": "kunnen", "kunt": "kunnen", "hoeft": "hoeven",
    "rent": "rennen", "probeert": "proberen", "lukt": "lukken", "klopt": "kloppen", "kookt": "koken", "vergeet": "vergeten",
    "giet": "gieten", "spaart": "sparen", "durft": "durven", "slaat": "slaan", "vecht": "vechten", "beweegt": "bewegen",
    "klimt": "klimmen", "vult": "vullen", "tilt": "tillen", "blaast": "blazen", "breekt": "breken", "draagt": "dragen",
    "belooft": "beloven", "gekocht": "kopen", "gelopen": "lopen", "gehad": "hebben", "geschreven": "schrijven",
    "gegeten": "eten", "gebroken": "breken", "gevonden": "vinden", "gebleven": "blijven", "geworden": "worden",
    "liep": "lopen", "dronk": "drinken", "deed": "doen", "kreeg": "krijgen", "kwam": "komen", "zag": "zien", "ging": "gaan",
    "jaren": "jaar", "foto's": "foto", "auto's": "auto", "collega's": "collega", "steden": "stad", "leden": "lid",
    "benen": "been", "kinderen": "kind", "problemen": "probleem", "stukken": "stuk", "minuten": "minuut", "weken": "week",
    "brieven": "brief", "eieren": "ei", "kamers": "kamer", "huizen": "huis", "namen": "naam", "straten": "straat",
    "zware": "zwaar", "hoge": "hoog", "lege": "leeg", "volle": "vol", "grote": "groot", "kleine": "klein", "rode": "rood",
    "hoger": "hoog", "langer": "lang", "kleiner": "klein", "harder": "hard", "zachter": "zacht", "rustiger": "rustig",
    "sterren": "ster", "laarzen": "laars", "foto’s": "foto", "tv": "televisie",
    "praat": "praten", "zit": "zitten", "maakt": "maken", "geleerd": "leren", "gekozen": "kiezen", "kiest": "kiezen", "één": "een, één", "jurken": "jurk", "speelt": "spelen", "werkt": "werken", "alle": "al (pron)", "snelste": "snel",
}

# Hand-set ranks. wordfreq conflates these with homographs or gives the row
# no score, so the lexicon rank is far too high. The page prints each one.
CORE = "closed-class or core everyday word; wordfreq rank is a homograph artefact, A0 by judgement"
HOMO = "homograph artefact: wordfreq ranks another word with the same spelling; everyday word, band by judgement"
OVERRIDES = {
    "weer": (450, HOMO), "eten": (250, HOMO), "leven": (550, HOMO), "dood": (600, HOMO), "rijk": (800, HOMO),
    "licht": (500, HOMO), "duur": (400, HOMO), "goede": (250, HOMO), "beste": (250, HOMO), "laag": (600, HOMO),
    "fout": (800, HOMO), "moe": (600, HOMO), "pas": (600, HOMO), "kost": (450, HOMO), "past": (300, HOMO),
    "lief": (800, HOMO), "gek": (900, HOMO), "arm": (900, HOMO), "vers": (1500, HOMO), "verder": (400, HOMO),
    "midden": (400, HOMO), "kijk": (500, HOMO), "gelijk": (500, HOMO),

    "is": (1, "form of zijn; wordfreq gave the verb row no score of its own"),
    "zijn": (1, "verb and possessive; wordfreq gave the verb row no score of its own"),
    "dan": (250, CORE), "naar": (250, CORE), "te": (250, CORE), "al": (250, CORE), "haar": (250, CORE), "moet": (250, CORE), "meer": (250, CORE), "toen": (250, CORE), "net": (250, CORE), "rond": (250, CORE), "alle": (250, CORE),
    "dat": (250, CORE), "waar": (250, CORE), "maar": (250, CORE), "goed": (250, CORE),
    "morgen": (450, "everyday time word; the lexicon rank is the noun morning, A1 by judgement"),
}

# ----------------------------------------------------------------------
# Pilot data. rank/band come from the lexicon at build time.
# forms = surface forms of the verb itself (exempt from the ceiling)
# ----------------------------------------------------------------------
def load_ranks():
    r = {}
    for row in csv.DictReader(open(os.path.join(LEX, "woorden-niveau.tsv"), encoding="utf-8"), delimiter="\t"):
        r[row["nl"]] = int(row["rang"])
    return r

_INDEX = {}
def _index(ranks):
    key = id(ranks)
    if key not in _INDEX:
        idx = {}
        for k, v in ranks.items():
            for b in {k, k.split(" (")[0], k.split(",")[0].strip()}:
                if b not in idx or v < idx[b][0]:
                    idx[b] = (v, k)
        _INDEX.clear(); _INDEX[key] = idx
    return _INDEX[key]

def lookup(word, ranks):
    """Best lemma rank for a surface form, or None."""
    idx = _index(ranks)
    w = word.lower().replace("’", "'")
    if w in OVERRIDES: return (OVERRIDES[w][0], w)
    cands = []
    if w in INFL: cands.append(INFL[w])
    cands.append(w)
    for suf in ("t", "en", "e", "s", "de", "te", "n"):
        if w.endswith(suf) and len(w) > len(suf) + 2:
            cands.append(w[: -len(suf)])
            cands.append(w[: -len(suf)] + "en")
    for c in cands:
        if c in idx: return idx[c]
        base = c.split(" (")[0]
        if base in idx: return idx[base]
    return None

def check_ex(forms, example, band, ranks):
    ceil = CEIL[band]
    worst, bad, unknown = (0, ""), [], []
    for sentence in example["text"] + [example["question"]]:
        for tok in re.findall(r"[A-Za-zÀ-ÿ'’]+", sentence):
            lw = tok.lower()
            if lw in NAMES or lw in forms: continue
            hit = lookup(tok, ranks)
            if hit is None:
                unknown.append(tok); continue
            if hit[0] > worst[0]: worst = (hit[0], tok)
            if hit[0] > ceil: bad.append(f"{tok} ({band_of(hit[0])}, rank {hit[0]})")
    return worst, bad, unknown

def e(s): return html.escape(s, quote=False)

