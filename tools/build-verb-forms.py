#!/usr/bin/env python3
"""Extract past and participle forms for the irregular verb cards.

Source: Bijlage 3b (Onregelmatige werkwoorden, alfabetisch), Nederlands in actie.
Output: tools/lexicon/werkwoorden-vormen.tsv with columns
  verb, past_sg, past_pl, aux, participle, source
aux is hebben, zijn or hebben/zijn.  Verbs the appendix lacks are filled from
MANUAL below and marked source=handmatig.  Run after select.py; then rerun
build-verb-cards.py.
"""
import csv, json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = "/media/tony/Data/Dutch/Bijlage-3b-Onregelmatige-werkwoorden-alfabetisch.pdf"
OUT = os.path.join(HERE, "lexicon", "werkwoorden-vormen.tsv")
SEL = os.path.join(HERE, "_ww_tmp", "selection.json")

# (past_sg, past_pl, aux, participle) for verbs the appendix does not list or lists differently.
# Verbs whose correct forms differ from the appendix go in CORRECT (aux only) or here.
MANUAL = {
    # The appendix splits these over two lines or leaves the participle blank.
    "willen": ("wilde / wou", "wilden / wouden", "hebben", "gewild"),
    "zullen": ("zou", "zouden", "", ""),   # no participle, no perfect
    # Strong or mixed verbs the appendix does not list (select.py EXTRA_IRREGULAR).
    "meten": ("mat", "maten", "hebben", "gemeten"),
    "heffen": ("hief", "hieven", "hebben", "geheven"),
    "laden": ("laadde", "laadden", "hebben", "geladen"),
    "spinnen": ("spon", "sponnen", "hebben", "gesponnen"),
    "stoten": ("stootte / stiet", "stootten / stieten", "hebben", "gestoten"),
    "wijten": ("weet", "weten", "hebben", "geweten"),
    # Derivation from mogen would give "vermogen"; the participle is vermocht.
    "vermogen": ("vermocht", "vermochten", "hebben", "vermocht"),
}

# The appendix row is wrong for the carded sense.  Reviewed 20 Nov 2026.
CORRECT = {
    "wijken": {"aux": "zijn"},              # is geweken
    "springen": {"aux": "hebben/zijn"},     # with a direction: is gesprongen
    "scheiden": {"aux": "hebben/zijn"},     # heeft gescheiden (separate), is gescheiden (divorce)
    "ontstaan": {"aux": "zijn"},            # is ontstaan
    "genezen": {"aux": "hebben/zijn"},      # heeft genezen (cure), is genezen (heal)
}

# Prefixed verbs take the base verb's forms.  Inseparable prefixes keep the
# prefix in the past and drop ge- from the participle (bekijken: bekeek,
# bekeken).  Separable verbs are not carded here, so only these are needed.
INSEPARABLE = ("her", "ont", "ver", "be", "ge", "er", "over", "onder", "door",
               "om", "achter", "vol", "weer", "voor")

# The auxiliary differs from the base verb's.
AUX = {
    "vertrekken": "zijn", "overlijden": "zijn", "verdwijnen": "zijn",
    "ontkomen": "zijn", "vervallen": "zijn", "verlopen": "zijn",
    "bevallen": "hebben/zijn", "ondergaan": "hebben", "begaan": "hebben",
    "bestaan": "hebben", "doorstaan": "hebben", "verstaan": "hebben",
    "voldoen": "hebben", "doorbreken": "hebben/zijn", "overvallen": "hebben",
    "verblijven": "hebben", "begeven": "hebben", "verslaan": "hebben",
    "ontslaan": "hebben", "betreden": "hebben", "behouden": "hebben",
    "onderhouden": "hebben", "onthouden": "hebben", "begraven": "hebben",
    "onderscheiden": "hebben", "betrekken": "hebben", "bevallen": "zijn",
    "doorbreken": "hebben",
}


def derive(verb, rows):
    """Forms of prefix + listed base, or None."""
    for p in INSEPARABLE:
        base = verb[len(p):]
        if verb.startswith(p) and len(base) >= 4:
            d = rows.get(base) or derive_manual(base)
            if d is None:
                d2 = derive(base, rows)
                if d2 is None:
                    continue
                sg, pl, aux, pp = d2
            else:
                sg, pl, aux, pp = d
            part = pp[2:] if pp.startswith("ge") else pp
            return (
                " / ".join(p + x.strip() for x in sg.split("/")),
                " / ".join(p + x.strip() for x in pl.split("/")),
                AUX.get(verb, aux),
                p + part,
            )
    return None


def derive_manual(base):
    return MANUAL.get(base)

ROW = re.compile(r"^\s*([a-zëé]+)\s{2,}(\S+),\s*(\S+)\s+(?:(\(?is\)?)\s+)?(\S+)\s{2,}")

def parse():
    text = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True, check=True).stdout
    rows, last = {}, None
    for line in text.splitlines():
        m = ROW.match(line)
        if m and m.group(1) != "infinitief":
            inf, sg, pl, aux, pp = m.groups()
            rows[inf] = {"sg": [sg], "pl": [pl], "aux": {"is": "zijn", "(is)": "hebben/zijn"}.get(aux, "hebben"), "pp": pp}
            last = inf
            continue
        m2 = re.match(r"^\s{10,}(\S+),\s*(\S+)\s*$", line)   # second line = alternative past
        if m2 and last:
            rows[last]["sg"].append(m2.group(1)); rows[last]["pl"].append(m2.group(2))
    return rows

def main():
    rows = parse()
    flat = {k: (" / ".join(d["sg"]), " / ".join(d["pl"]), d["aux"], d["pp"]) for k, d in rows.items()}
    sel = [r for r in json.load(open(SEL)) if r["regularity"] == "irregular"]
    out, missing = [], []
    for r in sel:
        v = r["verb"]
        if v in MANUAL:
            sg, pl, aux, pp = MANUAL[v]; src = "handmatig"
        elif v in rows:
            d = rows[v]; sg, pl, aux, pp = " / ".join(d["sg"]), " / ".join(d["pl"]), d["aux"], d["pp"]; src = "Bijlage 3b"
        elif derive(v, flat) is not None:
            sg, pl, aux, pp = derive(v, flat); src = "afgeleid van grondwerkwoord"
        else:
            missing.append(v); continue
        if v in CORRECT:
            aux = CORRECT[v].get("aux", aux); src += ", hulpwerkwoord gecorrigeerd"
        out.append([v, sg, pl, aux, pp, src])
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["verb", "past_sg", "past_pl", "aux", "participle", "source"])
        w.writerows(out)
    print(f"{len(out)} written, {len(missing)} missing: {' '.join(missing)}")

main()
