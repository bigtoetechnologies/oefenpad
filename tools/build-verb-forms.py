#!/usr/bin/env python3
"""Extract past and participle forms for the irregular verb cards.

Source: Bijlage 3b (Onregelmatige werkwoorden, alfabetisch), Nederlands in actie.
Output: tools/lexicon/werkwoorden-vormen.tsv with columns
  verb, past_sg, past_pl, aux, participle, source
aux is hebben, zijn or hebben/zijn.  Verbs the appendix lacks are filled from
MANUAL below and marked source=handmatig.  Run after select.py; then rerun
build-verb-cards.py.  Only carded verbs get rows: an irregular verb whose
scene row is SKIP gets none.  Existing rows are never changed or dropped
(another family may append them, and some were corrected by hand); only carded
verbs missing from the TSV are appended.  --dry-run reports without writing.
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
    # stiet is archaic; the review of 20 Nov 2026 kept the form a learner should use.
    "stoten": ("stootte", "stootten", "hebben", "gestoten"),
    "wijten": ("weet", "weten", "hebben", "geweten"),
    # Derivation from mogen would give "vermogen"; the participle is vermocht.
    "vermogen": ("vermocht", "vermochten", "hebben", "vermocht"),
    # B2 pass, 20 Nov 2026: strong verbs the appendix does not list.
    "wringen": ("wrong", "wrongen", "hebben", "gewrongen"),
}

# The appendix lists the verb but its row does not parse: no plural given.
PARTIAL = {
    "rijgen": ("reeg", "regen", "hebben", "geregen"),   # Bijlage 3b line 133: reeg, geregen
}

# The appendix row is wrong or incomplete for the carded sense.  Reviewed 20 Nov 2026.
# Keys: aux, and past_sg / past_pl / participle where the forms themselves change.
CORRECT = {
    "wijken": {"aux": "zijn"},              # is geweken
    "springen": {"aux": "hebben/zijn"},     # with a direction: is gesprongen
    "scheiden": {"aux": "hebben/zijn"},     # heeft gescheiden (separate), is gescheiden (divorce)
    "ontstaan": {"aux": "zijn"},            # is ontstaan
    "genezen": {"aux": "hebben/zijn"},      # heeft genezen (cure), is genezen (heal)
    "smelten": {"aux": "hebben/zijn"},      # heeft gesmolten (transitive), is gesmolten (the snow)
    # Fix pass 20 Nov 2026.  The appendix gives the second row of each on a
    # continuation line the parser skips.  schuilen (to shelter): the weak forms
    # are the usual ones for the carded sense, so they come first.
    "schuilen": {"past_sg": "schuilde / school", "past_pl": "schuilden / scholen",
                 "participle": "geschuild / gescholen"},
    "waaien": {"past_sg": "waaide / woei", "past_pl": "waaiden / woeien"},
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

SCENES = os.path.join(HERE, "_ww_tmp", "scenes")


def carded_verbs():
    """Verbs with a card: a scene row in tools/_ww_tmp/scenes/<page>.tsv that is
    not a SKIP row.  Irregular SKIP verbs have no card, so no forms are needed
    and none are written for them (their forms were never reviewed)."""
    carded = set()
    for name in os.listdir(SCENES):
        if not name.endswith(".tsv") or name == "retired.tsv":
            continue
        with open(os.path.join(SCENES, name), encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE):
                if r.get("scene") and not r["scene"].startswith("SKIP:"):
                    carded.add(r["verb"])
    return carded


def main():
    import sys
    dry = "--dry-run" in sys.argv[1:]
    rows = parse()
    flat = {k: (" / ".join(d["sg"]), " / ".join(d["pl"]), d["aux"], d["pp"]) for k, d in rows.items()}
    carded = carded_verbs()
    sel = [r for r in json.load(open(SEL)) if r["regularity"] == "irregular" and r["verb"] in carded]
    computed, missing = {}, []
    for r in sel:
        v = r["verb"]
        if v in MANUAL:
            sg, pl, aux, pp = MANUAL[v]; src = "handmatig"
        elif v in PARTIAL:
            sg, pl, aux, pp = PARTIAL[v]; src = "Bijlage 3b, meervoud aangevuld"
        elif v in rows:
            d = rows[v]; sg, pl, aux, pp = " / ".join(d["sg"]), " / ".join(d["pl"]), d["aux"], d["pp"]; src = "Bijlage 3b"
        elif derive(v, flat) is not None:
            sg, pl, aux, pp = derive(v, flat); src = "afgeleid van grondwerkwoord"
        else:
            missing.append(v); continue
        if v in CORRECT:
            c = CORRECT[v]
            if "aux" in c:
                aux = c["aux"]; src += ", hulpwerkwoord gecorrigeerd"
            if {"past_sg", "past_pl", "participle"} & set(c):
                sg, pl, pp = c.get("past_sg", sg), c.get("past_pl", pl), c.get("participle", pp)
                src += ", vormen aangevuld"
        computed[v] = [v, sg, pl, aux, pp, src]
    # Merge, never overwrite: every existing row is kept as it stands, in its
    # original order (other families append rows too, and rows were corrected
    # by hand).  Only carded verbs missing from the TSV are appended.  Where a
    # kept row differs from what the appendix gives, it is reported, not changed:
    # correct it by hand, in the TSV and on the page.
    out, have = [], set()
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                if r["verb"] in have:
                    continue
                out.append([r["verb"], r["past_sg"], r["past_pl"], r["aux"], r["participle"], r["source"]])
                have.add(r["verb"])
    differ = [v for v in computed if v in have and
              next(x for x in out if x[0] == v)[1:5] != computed[v][1:5]]
    added = [computed[v] for v in computed if v not in have]
    out.extend(added)
    print(f"{len(carded)} carded verbs, {len(sel)} irregular carded; "
          f"{len(added)} rows added, 0 rows changed, {len(out)} rows in total")
    if added:
        print("  added: " + " ".join(r[0] for r in added))
    if differ:
        print(f"  {len(differ)} kept rows differ from the appendix (not changed): " + " ".join(differ))
    if missing:
        print(f"  {len(missing)} carded irregular verbs have no forms; add them to MANUAL: " + " ".join(missing))
    if dry:
        print("dry run: nothing written")
        return
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["verb", "past_sg", "past_pl", "aux", "participle", "source"])
        w.writerows(out)

main()
