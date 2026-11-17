#!/usr/bin/env python3
"""Write the wordfreq score and frequency rank of every lemma.

`niveau.py` needs a frequency order that is independent of the coursebook, so
that a word's band is not just a restatement of which book teaches it. This
script produces it once and stores it, so the rest of the pipeline stays
dependency-free: `niveau.py` reads this file and never imports wordfreq.

    python3 -m pip install --target /tmp/wf wordfreq
    python3 tools/lexicon/frequentie.py --wordfreq /tmp/wf
    # -> tools/lexicon/woorden-frequentie.tsv   (nl  zipf  rang)

Output is row-aligned with `woorden.tsv` (same `nl`, same order) so the viewer
can join it by position. `rang` 1 is the most frequent lemma in the list.

A lemma that wordfreq has never seen scores 0.0 and sorts to the tail; there are
186 of those, almost all game compounds and a few misspellings (`belangstellilng`).
They are not rare Dutch — they are absent from the corpus — so `niveau.py` gives
them a band from their source instead of their rank. The `zipf` column is printed
to two decimals; the rank is computed on the full-precision score.

Attribution: wordfreq is Robyn Speer's; its data is CC BY-SA 4.0 and needs the
SUBTLEX and OpenSubtitles notices if shipped. See `Docs/lexicon/bronnen.html` §Attribution.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WOORDEN = os.path.join(HERE, "woorden.tsv")
UIT = os.path.join(HERE, "woorden-frequentie.tsv")


def read_tsv(path):
    with open(path, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in fh if line.strip()]
    return header, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wordfreq", required=True, help="directory wordfreq was installed to")
    args = ap.parse_args()

    sys.path.insert(0, args.wordfreq)
    from wordfreq import zipf_frequency

    header, rows = read_tsv(WOORDEN)
    assert header == ["nl", "en", "niveau", "top2000", "herkomst"], header

    score = [zipf_frequency(r[0], "nl") for r in rows]
    order = sorted(range(len(rows)), key=lambda i: (-score[i], rows[i][0]))
    rang = [0] * len(rows)
    for n, i in enumerate(order, start=1):
        rang[i] = n

    with open(UIT, "w", encoding="utf-8") as fh:
        fh.write("nl\tzipf\trang\n")
        for i, r in enumerate(rows):
            fh.write("%s\t%.2f\t%d\n" % (r[0], score[i], rang[i]))

    zero = [rows[i][0] for i in range(len(rows)) if score[i] == 0]
    print(f"wrote {UIT}: {len(rows)} rows, {len(zero)} with no wordfreq score")
    for n in (1000, 2500, 5000, 8000):
        print(f"  rank {n:>5}: zipf {score[order[n - 1]]:.2f}  ({rows[order[n - 1]][0]})")
    if zero:
        print("  no-score sample:", ", ".join(zero[:10]))


if __name__ == "__main__":
    main()
