#!/usr/bin/env python3
"""Top up woorden.tsv to 10,000 words from the verified online candidates.

`extraheer-woorden.py` writes the two sources the owner already owned: the
coursebook appendix and the games' word bank, 7,107 words. `kandidaten.tsv`
holds words extracted from English Wiktionary via kaikki.org (see
`aanvulling.md` for the licence reasoning), already filtered to Dutch lemmas
with an English gloss that are absent from woorden.tsv.

This script chooses which of them to keep. The appendix is the 5,000 most
frequent Dutch lemmas, so the natural continuation is the next most frequent
words; the ranking comes from `wordfreq` (Robyn Speer), which the research pass
also used to gate the candidate file at zipf >= 2.5.

The rule is: sort the candidates by (-zipf, nl) and take as many as the target
needs. `--report` prints that arithmetic without writing anything: the pool
size, how many are already present, the zipf cut-off, how many candidates sit
exactly on it, and what taking more would cost. The measured figures are in
`bronnen.md`; this docstring is the rule, that file is the evidence.

Order of the pipeline:

    extraheer-woorden.py   appendix + games  -> woorden.tsv (7,107)
    knm-woorden.py         + KNM vocabulary  -> woorden.tsv (7,232)
    verrijk-woorden.py     + candidates      -> woorden.tsv (10,000)
    woordsoort.py                            -> woorden-woordsoort.tsv
    thema.py                                 -> woorden-thema.tsv

`verrijk-woorden.py` is idempotent: words already present are never added
again, so a second run adds nothing. Re-running `extraheer-woorden.py` rewrites
woorden.tsv from scratch and will drop the additions; run this again after it.

wordfreq is not a project dependency. Install it to a throwaway directory:

    python3 -m pip install --target /tmp/wf wordfreq
    python3 tools/lexicon/verrijk-woorden.py --wordfreq /tmp/wf

Attribution: the ranking uses wordfreq, whose data derives from Wikipedia,
ParaCrawl, OpenSubtitles, SUBTLEX-NL and Google Books Ngrams. The words added
here come from English Wiktionary via kaikki.org, CC BY-SA 4.0 + GFDL, so this
file and the two files derived from it carry that licence. See README.md.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WOORDEN = os.path.join(HERE, "woorden.tsv")
KANDIDATEN = os.path.join(HERE, "kandidaten.tsv")
TARGET = 10_000


def read_tsv(path):
    with open(path, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in fh if line.strip()]
    return header, rows


def score(krows, present, zipf_frequency):
    """Rank the candidates that are not already on the list: (-zipf, nl)."""
    seen = set()
    scored = []
    for nl, en, *_ in krows:
        key = nl.lower()
        if key in present or key in seen or not en.strip():
            continue
        seen.add(key)
        scored.append((zipf_frequency(nl, "nl"), nl, en))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return scored


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wordfreq", required=True, help="directory wordfreq was installed to")
    ap.add_argument("--target", type=int, default=TARGET)
    ap.add_argument("--report", action="store_true",
                    help="print the selection arithmetic and exit without writing")
    args = ap.parse_args()

    sys.path.insert(0, args.wordfreq)
    from wordfreq import zipf_frequency

    header, rows = read_tsv(WOORDEN)
    assert header == ["nl", "en", "niveau", "top2000", "herkomst"], header

    kheader, krows = read_tsv(KANDIDATEN)
    assert kheader[:2] == ["nl", "en"], kheader

    if args.report:
        # The `kaikki` rows in woorden.tsv were added by an earlier run of this
        # script, so they must not count as "already present" here: the report
        # describes the state before the top-up, which is the state in which the
        # cut-off is visible.
        before = [r for r in rows if r[4] != "kaikki"]
        report(krows, {r[0].lower() for r in before}, len(before),
               score(krows, {r[0].lower() for r in before}, zipf_frequency),
               args.target)
        return

    have = {r[0].lower() for r in rows}
    scored = score(krows, have, zipf_frequency)
    need = args.target - len(rows)
    take = scored[:max(0, need)]

    if need <= 0:
        print(f"{len(rows)} words already, target {args.target} — nothing to add")
        return

    rows += [[nl, en, "", "", "kaikki"] for _, nl, en in take]

    with open(WOORDEN, "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")

    cut = take[-1][0] if take else 0.0
    print(f"added {len(take)} words (zipf cut-off {cut:.2f}); {len(rows)} total")


def report(krows, present, have_count, scored, target):
    """Print how the cut-off was reached, without mutating anything."""
    print(f"candidate rows in kandidaten.tsv: {len(krows)}")
    print(f"skipped (present, blank, repeat):  {len(krows) - len(scored)}")
    print(f"scored with wordfreq:              {len(scored)}")
    print(f"words already on the list:         {have_count}")
    print(f"needed to reach {target}:           {max(0, target - have_count)}")
    take = scored[:max(0, target - have_count)]
    if not take:
        print("nothing to select")
        return
    cut = take[-1][0]
    tied = [t for t in scored if abs(t[0] - cut) < 1e-9]
    taken_tied = [t for t in take if abs(t[0] - cut) < 1e-9]
    print(f"zipf cut-off:                      {cut:.4f}")
    print(f"on the cut-off:                    {len(tied)} tied, "
          f"{len(taken_tied)} taken (alphabetical tie-break)")
    print(f"usable candidates left unused:     {len(scored) - len(take)}")
    zips = [z for z, _, _ in scored]
    print(f"candidate zipf range:              {min(zips):.2f} .. {max(zips):.2f}")
    for th in (3.00, 3.10, 3.20):
        left = sum(1 for z, _, _ in scored[len(take):] if z >= th)
        print(f"  unused with zipf >= {th:.2f}:          {left}")
    print("first taken: " + ", ".join(nl for _, nl, _ in take[:5]))
    print("last taken:  " + ", ".join(nl for _, nl, _ in take[-5:]))


if __name__ == "__main__":
    main()
