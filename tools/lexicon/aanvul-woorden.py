#!/usr/bin/env python3
"""Add the coursebook vocabulary that the appendix and the games miss.

Three coursebooks were read for this list: *Nederlands in gang* (A1-A2),
*Nederlands in actie* (A2-B1, whose Bijlage 8 is already our primary source)
and *TaalCompleet B1* (themes 1-5). Each teaches words that the frequency
appendix does not contain: `bijsluiter`, `schroevendraaier`, `huurprijs`,
`onze`, `mensen`, `gefeliciteerd`. They are exactly the everyday vocabulary a
learner meets in the first year, and a frequency cut alone cannot recover them.

`aanvul-woorden.tsv` is the hand-checked result: one row per headword, with an
English gloss written against the book's meaning and a `herkomst` tag naming
the book (`les:nig`, `les:taalcompleet`, `les:register`). A handful of rows are
tagged `handmatig`: words confirmed as gaps by a wordfreq pass over the 8,000
most frequent Dutch words rather than read from a single book (`onze`,
`sprake`, `excuses`).

Only single-word lemmas are carried here. Phrases, proper nouns, transparent
inflections and diminutives of a word the list already has are not. The file is
deliberately not a copy of any book's list: the glosses are ours, the words are
re-levelled by the frequency axis, and the list as a whole is larger and
ordered differently.

Order of the pipeline:

    extraheer-woorden.py   appendix + games  -> woorden.tsv (7,107)
    knm-woorden.py         + KNM vocabulary  -> woorden.tsv (7,232)
    aanvul-woorden.py      + coursebooks     -> woorden.tsv (~7,600)
    verrijk-woorden.py     + candidates      -> woorden.tsv (10,000)
    woordsoort.py                            -> woorden-woordsoort.tsv
    thema.py                                 -> woorden-thema.tsv

Because this runs before `verrijk-woorden.py`, the coursebook words displace
the least frequent candidate words instead of extending the list past its
10,000 target. Idempotent: a word already in `woorden.tsv` is never added
again. Re-running `extraheer-woorden.py` rewrites woorden.tsv from scratch, so
run this again before `verrijk-woorden.py`.

`zo’n` is a special case: it is an appendix row (page 147, `A1`, top 2,000)
that an earlier extraction lost. It is carried here so a rebuild cannot drop it
silently, and it is written with the appendix's own tier, not as a blank-tier
addition. `extraheer-woorden.py` now asserts its presence, so normally this
branch never fires.
"""

import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
WOORDEN = os.path.join(HERE, "woorden.tsv")
AANVUL = os.path.join(HERE, "aanvul-woorden.tsv")

HEADER = ["nl", "en", "niveau", "top2000", "herkomst"]


def norm(s):
    """The key a headword is matched on.

    `woorden.tsv` writes a part of speech into the headword when a word is both
    noun and adjective (`recht (noun)`), lists variants after a comma
    (`wij, we`), and uses the curly apostrophe (`zo’n`). Presence has to be
    tested on the bare, comma-split, apostrophe-normalised form, or this script
    adds a duplicate of a word the list already has.
    """
    s = s.lower().replace("\u2019", "'").replace("\u2018", "'")
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"^(de|het|een)\s+", "", s.strip())
    s = re.sub(r"^zich\s+", "", s)
    return s.strip(" .,;:")


def keys_of(nl):
    return [k for k in (norm(part) for part in nl.split(",")) if k]


def single_word(nl):
    """A lemma this file can carry: one word, no digits, no leading article."""
    if " " in nl or not nl.strip():
        return False
    if any(c.isdigit() for c in nl):
        return False
    if nl.lower() in ("de", "het", "een"):
        return False
    return len(nl) > 1


# An appendix row an earlier extraction lost. Written with the appendix's tier
# and gloss rather than as a blank-tier addition.
RESTORE = {
    "zo'n": ["zo\u2019n", "such a", "A1", "1", "bijlage8"],
}


def main():
    with open(WOORDEN, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in fh if line.strip()]
    assert header == HEADER, header

    have = set()
    for r in rows:
        have.update(keys_of(r[0]))
    with open(AANVUL, encoding="utf-8") as fh:
        extra = list(csv.DictReader(fh, delimiter="\t"))

    added, seen, skipped = [], set(), {"present": 0, "phrase": 0}
    for r in extra:
        nl, en = r["nl"].strip(), r["en"].strip()
        key = norm(nl)
        if not single_word(nl):
            skipped["phrase"] += 1
            continue
        if key in have or key in seen:
            skipped["present"] += 1
            continue
        if not en:
            continue
        seen.add(key)
        if key in RESTORE:
            added.append(list(RESTORE[key]))
        else:
            added.append([nl, en, "", "", r["herkomst"].strip()])

    rows += added
    with open(WOORDEN, "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")

    print("added %d coursebook words; %d already present or repeated; %d "
          "phrases skipped; %d total" % (len(added), skipped["present"],
                                         skipped["phrase"], len(rows)))
    if added:
        print("first:", ", ".join(r[0] for r in added[:8]))


if __name__ == "__main__":
    main()
