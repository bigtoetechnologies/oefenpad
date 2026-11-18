#!/usr/bin/env python3
"""Assign every lemma to one of five bands on our own scale.

The `niveau` column in `woorden.tsv` is not a level. It is the coursebook's own
tiering — `A1` if the word is filled light blue in Bijlage 8 (taught in
*Nederlands in gang*), `B1` if orange (*Nederlands in actie*), `open` if it is in
the 5,000 most frequent lemmas but in neither book — and it is empty for the
4,839 rows the appendix does not contain. Two of its three values borrow CEFR's
names without CEFR's meaning, which is why the viewer calls it `trede` (tier)
and it is nowhere presented as a CEFR level.

This script writes a separate axis, `niveau`, and it is ours:

    Start        rank     1-1,000   roughly A0-A1
    Basis        rank 1,001-2,500   roughly A1-A2
    Midden       rank 2,501-5,000   roughly A2-B1
    Gevorderd    rank 5,001-8,000   roughly B1-B2
    Verdieping   rank 8,001-10,000  roughly B2 and past it

The band is set by frequency rank, taken from `woorden-frequentie.tsv` (run
`frequentie.py` first), because rank answers "when does a learner meet this
word", which is the question a study order needs. The coursebook tier answers a
different question — "where does a coursebook teach it" — and stays in the data
as `trede` so the two can be compared. They do not coincide: see the calibration
table this script prints, and `Docs/lexicon/index.html` §"Our level scale".

The CEFR ranges above are an alignment of convenience, not a measurement and not
a claim about any individual word. Do not print a CEFR label next to a lemma on
the strength of its band.

A lemma wordfreq has never seen is absent from the corpus, which makes it rarer
than everything the corpus does contain, so it belongs in `Verdieping` — not in
`Start` where a rank of 'not found' would otherwise read as 'very frequent'. The
The one exception is direct evidence about when a learner meets the word: the
coursebook's own tier, the KNM list, and the coursebook vocabulary added by
`aanvul-woorden.py` override the rank.

    no-score rows:
    appendix A1 -> Start        appendix B1 -> Midden
    appendix open -> Gevorderd  KNM -> Basis        game word -> Verdieping
    les:nig -> Basis            les:taalcompleet / les:register -> Midden

`grondslag` records which rule fired.

`--why <word>` prints the band and the rule, like `domein.py --why`.

Output is row-aligned with `woorden.tsv`: `nl  niveau  rang  grondslag`.
The `rang` is copied from `woorden-frequentie.tsv` (and checked against it) so the
band can be audited from one file; `grondslag` says whether the rank or the
fallback rule set the band.
"""

import argparse
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WOORDEN = os.path.join(HERE, "woorden.tsv")
FREQ = os.path.join(HERE, "woorden-frequentie.tsv")
UIT = os.path.join(HERE, "woorden-niveau.tsv")

BANDS = ["Start", "Basis", "Midden", "Gevorderd", "Verdieping"]
CUTS = [(1_000, "Start"), (2_500, "Basis"), (5_000, "Midden"), (8_000, "Gevorderd")]
TAIL = "Verdieping"

# The no-score fallback: the appendix's own tier, then the source.
TREDE_BAND = {"A1": "Start", "B1": "Midden", "open": "Gevorderd"}

# A coursebook word wordfreq has never seen still has direct evidence about
# when a learner meets it: the book that teaches it. Without this branch such a
# row falls through to the game fallback (`spel`) and lands in Verdieping, which
# is exactly wrong for a word *Nederlands in gang* teaches in its first year.
LES_BAND = {
    "les:nig": "Basis",          # Nederlands in gang, A0-A2
    "les:taalcompleet": "Midden",  # TaalCompleet B1, A2-B1
    "les:register": "Midden",      # Nederlands in actie register, A2-B1
    "handmatig": "Basis",         # a confirmed high-frequency gap
}


def read_tsv(path):
    with open(path, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in fh if line.strip()]
    return header, rows


def band_of(rank):
    for cut, name in CUTS:
        if rank <= cut:
            return name
    return TAIL


def assign(row, freq_row):
    """Return (band, grondslag) for one woorden.tsv row."""
    _nl, _en, trede, _top2000, herkomst = row
    _nl2, zipf, rang = freq_row
    if float(zipf) > 0:
        return band_of(int(rang)), "rang"
    if trede in TREDE_BAND:
        return TREDE_BAND[trede], "trede"
    if "knm" in herkomst:
        return "Basis", "knm"
    tags = herkomst.split(";")
    for tag, band in LES_BAND.items():
        if tag in tags:
            return band, "les"
    return TAIL, "spel"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--why", metavar="WORD", help="explain one word and exit")
    args = ap.parse_args()

    wh, wrows = read_tsv(WOORDEN)
    assert wh == ["nl", "en", "niveau", "top2000", "herkomst"], wh
    fh_header, frows = read_tsv(FREQ)
    assert fh_header == ["nl", "zipf", "rang"], fh_header
    if len(wrows) != len(frows):
        raise SystemExit(f"row count differs: woorden {len(wrows)}, frequentie {len(frows)}")
    for i, (w, f) in enumerate(zip(wrows, frows)):
        if w[0] != f[0]:
            raise SystemExit(f"row {i + 2}: woorden {w[0]!r} != frequentie {f[0]!r}")

    out = []
    for i, (w, f) in enumerate(zip(wrows, frows)):
        band, grondslag = assign(w, f)
        assert band in BANDS, (w[0], band)
        out.append([w[0], band, f[2], grondslag])

        if args.why and w[0] == args.why:
            nl, en, trede, _top, herkomst = w
            print(f"word:      {nl}")
            print(f"gloss:     {en}")
            print(f"zipf:      {f[1]}   rang: {f[2]}")
            print(f"trede:     {trede or '(geen)'}   herkomst: {herkomst}")
            print(f"result:    {band}")
            print(f"grondslag: {grondslag}")
            return

    if args.why:
        raise SystemExit(f"{args.why!r} is not in woorden.tsv (check the exact spelling)")

    with open(UIT, "w", encoding="utf-8") as fh:
        fh.write("nl\tniveau\trang\tgrondslag\n")
        for r in out:
            fh.write("\t".join(r) + "\n")

    bounds = {name: (1 if i == 0 else CUTS[i - 1][0] + 1, cut)
              for i, (cut, name) in enumerate(CUTS)}
    bounds[TAIL] = (CUTS[-1][0] + 1, len(out))

    counts = {b: 0 for b in BANDS}
    for _, band, _, _ in out:
        counts[band] += 1
    print(f"wrote {UIT}: {len(out)} rows")
    for b in BANDS:
        lo, hi = bounds[b]
        print(f"  {b:<11} {counts[b]:>5}  rank {lo:,}-{hi:,}")

    grond = {}
    for _, _, _, g in out:
        grond[g] = grond.get(g, 0) + 1
    print("  grondslag: " + ", ".join(f"{k} {v}" for k, v in sorted(grond.items())))

    # Calibration against the appendix tier: the whole point of keeping both
    # axes is that this table can be read and argued with.
    tiers = ["A1", "B1", "open", "(geen)"]
    grid = {b: [0] * len(tiers) for b in BANDS}
    for i, (_, band, _, _) in enumerate(out):
        t = wrows[i][2] or "(geen)"
        grid[band][tiers.index(t)] += 1
    print("\ncalibration: band × appendix trede")
    print(f"  {'band':<11}" + "".join(f"{t:>7}" for t in tiers) + "   total")
    for b in BANDS:
        print(f"  {b:<11}" + "".join(f"{v:7}" for v in grid[b]) + f"{sum(grid[b]):8}")
    totals = [sum(grid[b][j] for b in BANDS) for j in range(len(tiers))]
    print(f"  {'total':<11}" + "".join(f"{v:7}" for v in totals) + f"{sum(totals):8}")

    a1 = grid["Start"][0] + grid["Basis"][0]
    b1 = grid["Midden"][1] + grid["Gevorderd"][1] + grid["Verdieping"][1]
    if totals[0]:
        print(f"  {a1}/{totals[0]} = {100 * a1 / totals[0]:.0f}% of the appendix A1 tier "
              f"is in Start or Basis")
    if totals[1]:
        print(f"  {b1}/{totals[1]} = {100 * b1 / totals[1]:.0f}% of the appendix B1 tier "
              f"is in Midden or beyond")


if __name__ == "__main__":
    main()
