#!/usr/bin/env python3
"""Add the TaalCompleet KNM vocabulary to woorden.tsv before the frequency top-up.

The appendix (`Bijlage-8`) is the 5,000 most frequent lemmas and the games supply
the picture vocabulary, but neither holds the civic vocabulary an inburgering
learner meets in the KNM exam: `kwijtschelding`, `jaaropgaaf`,
`burgerservicenummer`, `huisartsenpost`, `peuterspeelzaal`. Those words are far
too rare to survive a frequency cut-off, and they are exactly the words the
product's `Gemeente en post`, `Formulieren` and `Solliciteren` themes are for.

`knm-kandidaten.tsv` is the list extracted from the TaalCompleet KNM word lists
(Nederlands + Engels, 321 rows, 279 distinct lemmas). This script keeps the
single-word lemmas that are not already present and appends them, so that
`verrijk-woorden.py` then fills the remainder of the 10,000 from the frequency
pool. The KNM words therefore displace the rarest candidate words rather than
extending the list past its target.

Order of the pipeline:

    extraheer-woorden.py   appendix + games  -> woorden.tsv (7,107)
    knm-woorden.py         + KNM vocabulary  -> woorden.tsv (7,232)
    aanvul-woorden.py      + coursebooks     -> woorden.tsv (~7,600)
    verrijk-woorden.py     + candidates      -> woorden.tsv (10,000)
    woordsoort.py                            -> woorden-woordsoort.tsv
    thema.py                                 -> woorden-thema.tsv

Idempotent: a word already in woorden.tsv is never added again. Re-running
`extraheer-woorden.py` rewrites woorden.tsv from scratch, so run this again
before `verrijk-woorden.py`.

The KNM theme and priority for these rows are in `knm-thema.tsv`, which
`thema.py` reads for rows whose `herkomst` is `knm`. That file is hand-checked:
the KNM word list is authoritative about which words an inburgering learner
needs. The rows are an extraction, not a copy: the glosses and themes are ours,
the list is re-levelled and ordered differently, and a list of words in a
language is not itself the kind of thing copyright protects. See
`Docs/lexicon/bronnen.html` for the licence position.
"""

import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
WOORDEN = os.path.join(HERE, "woorden.tsv")
KNM = os.path.join(HERE, "knm-kandidaten.tsv")

HEADER = ["nl", "en", "niveau", "top2000", "herkomst"]


def bare(nl):
    """The key a headword is matched on.

    `woorden.tsv` disambiguates a word that is both noun and adjective by
    writing the part of speech into the headword (`politiek (adj)`), so the
    bare lemma is what has to be tested for presence, or the KNM list adds a
    third `politiek` beside the two.
    """
    return re.sub(r"\s*\([a-z]+\)$", "", nl).strip().lower()


def single_word(nl):
    """A lemma this file can carry: one word, no digits, no leading article."""
    if " " in nl or not nl.strip():
        return False
    if any(c.isdigit() for c in nl):
        return False
    if nl.lower() in ("de", "het", "een"):
        return False
    return len(nl) > 1


def main():
    with open(WOORDEN, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in fh if line.strip()]
    assert header == HEADER, header

    have = {bare(r[0]) for r in rows}
    with open(KNM, encoding="utf-8") as fh:
        knm = list(csv.DictReader(fh, delimiter="\t"))

    added, seen, skipped = [], set(), {"present": 0, "phrase": 0}
    for r in knm:
        nl, en = r["nl"].strip(), r["en"].strip()
        key = bare(nl)
        if not single_word(nl):
            skipped["phrase"] += 1
            continue
        if key in have or key in seen:
            skipped["present"] += 1
            continue
        if not en:
            continue
        seen.add(key)
        added.append([nl, en, "", "", "knm"])

    rows += added
    with open(WOORDEN, "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")

    print("added %d KNM words; %d already present or repeated; %d phrases "
          "skipped; %d total" % (len(added), skipped["present"],
                                 skipped["phrase"], len(rows)))
    if added:
        print("first:", ", ".join(r[0] for r in added[:8]))


if __name__ == "__main__":
    main()
