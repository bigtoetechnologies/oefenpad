#!/usr/bin/env python3
"""Build the A0-B1 verb-card selection for Docs/werkwoorden.

Selection is by lexicon frequency rank:
  A0  rank <= 250
  A1  rank 251-1000
  A2  all irregulars in 1001-2500 + the top 60 regulars
  B1  all irregulars in 2501-5000 + the top 60 regulars

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
    "schuiven": "to slide",
    "zwijgen": "to be silent",
    "scheppen": "to scoop, to shovel",
    "scheiden": "to separate",
    "schijnen": "to shine",
    "missen": "to miss",
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
    "starten": "to start (an engine)",
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
}


# The lexicon files one domain per lemma, usually from its most common nominal
# sense.  For a verb card the tag should name what the action is about, so a few
# dozen are corrected by hand.  Everything not listed keeps the lexicon value.
DOMAIN = {
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
}


def slug_of(word):
    plain = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode()
    return plain.lower().replace("'", "").replace(" ", "-")


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
    "zwelgen", "wreken", "wijten",
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
    }
    for key in verb_keys:
        for p in SEPARABLE_PARTICLES:
            rest = key[len(p):]
            if key.startswith(p) and len(rest) >= 4 and rest in verb_keys:
                found.add(key)
    return {w for w in found if w in verb_keys}


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
                "tier": r["niveau"],
                "top2000": r["top2000"],
                "domain": DOMAIN.get(key) or domain.get(key, ""),
                "reflexive": ("(zich)" in r["nl"] or ", zich" in r["nl"]) and key not in NOT_REFLEXIVE,
                "irregular": is_irregular(key, irregular),
                "slug": slug_of(key),
            }

    separable = separable_lemmas(set(verbs))
    sensitive = {"doden", "neuken", "schieten", "vermoorden"}
    odd = {"dagen", "ogen", "lesgven", "cc'en", "onderwerpen", "sporen"}
    for key, v in verbs.items():
        v["separable"] = key in separable or "-" in key
        v["sensitive"] = key in sensitive
        v["odd"] = key in odd

    def usable(v):
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

    # A2/B1 regulars are capped; irregulars are all kept.
    for b, cap in (("A2", 60), ("B1", 60)):
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
            "band": b,
            "regularity": "irregular" if v["irregular"] else "regular",
            "verb": v["key"],
            "slug": v["slug"],
            "lexeme": v["lexeme"],
            "gloss": v["gloss"],
            "rank": v["rank"],
            "rank_source": v["rank_source"],
            "domain": v["domain"],
            "tier": v["tier"],
        })

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "selection.json"), "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)

    pages = {}
    for b in ("A0", "A1", "A2", "B1"):
        for reg in ("regular", "irregular"):
            sub = [r for r in records if r["band"] == b and r["regularity"] == reg]
            pages[f"{b.lower()}-{reg}"] = sub
            with open(os.path.join(OUT, f"{b.lower()}-{reg}.tsv"), "w", encoding="utf-8") as fh:
                fh.write("verb\tslug\tgloss\trank\tdomain\n")
                for r in sub:
                    fh.write(f"{r['verb']}\t{r['slug']}\t{r['gloss']}\t{r['rank']}\t{r['domain']}\n")

    with open(os.path.join(OUT, "backlog_seed.tsv"), "w", encoding="utf-8") as fh:
        fh.write("verb\tgloss\trank\tband\treason\n")
        for r in sorted(deferred, key=lambda r: (r["band"], r["rank"])):
            fh.write(f"{r['verb']}\t{r['gloss']}\t{r['rank']}\t{r['band']}\t{r['reason']}\n")

    for name, sub in pages.items():
        irr = sum(1 for r in sub if r["regularity"] == "irregular")
        reg = len(sub) - irr
        print(f"{name:18} {len(sub):3}  irregular {irr:3}  regular {reg:3}")
    print(f"total selected {len(records)}")
    print(f"deferred {len(deferred)}")


if __name__ == "__main__":
    main()
