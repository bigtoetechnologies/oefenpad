#!/usr/bin/env python3
"""Give every Voorzetselpaden card one continuous reference number.

    python3 tools/number-prepositions-frames.py [--dry-run]

The eight band pages under Docs/voorzetselpaden/ are the master copy. A
reviewer needs to be able to name a single frame wherever it sits, so the
numbers run in document order and carry on from one band to the next, A0
first and B2 last. Each card gets a badge in its top-right corner, and the
band header gets the band's range. Rerunning replaces the badges, so the
numbers are rebuilt rather than doubled whenever cards are added.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "Docs/voorzetselpaden"
BANDS = ["a0", "a1", "a2", "a2-pairs", "a2-plus", "b1", "b1-plus", "b2"]

ARTICLE = re.compile(r'<article class="kaart\b[^"]*"[^>]*>')
OLD_BADGE = re.compile(r'<span class="framenummer"[^>]*>[^<]*</span>')
SUM = re.compile(r'<div class="sum">.*?</div>', re.S)
OLD_RANGE = re.compile(r'<span class="framereeks">.*?</span>')

CSS_KAART = (".kaart{border:1px solid var(--lijn);border-radius:12px;padding:14px;"
             "break-inside:avoid;display:flex;flex-direction:column}")
CSS_KAART_NEW = (".kaart{position:relative;border:1px solid var(--lijn);border-radius:12px;"
                 "padding:14px;break-inside:avoid;display:flex;flex-direction:column}")
CSS_ANCHOR = ".kaart h3{margin:0;font-size:18px;letter-spacing:-.01em}"
CSS_BADGE = (
    ".framenummer{position:absolute;top:8px;right:10px;font:700 11px/1.6 "
    "ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--kobalt);"
    "background:var(--papier);border:1px solid var(--lijn);border-radius:999px;"
    "padding:1px 7px;font-variant-numeric:tabular-nums;letter-spacing:.02em}"
)


def number_page(path: Path, start: int, dry: bool) -> tuple[str, int, int]:
    src = path.read_text(encoding="utf-8")

    if CSS_KAART in src:
        src = src.replace(CSS_KAART, CSS_KAART_NEW, 1)
    if ".framenummer{" not in src:
        if CSS_ANCHOR not in src:
            sys.exit(f"{path.name}: no CSS anchor for .framenummer")
        src = src.replace(CSS_ANCHOR, CSS_ANCHOR + "\n" + CSS_BADGE, 1)

    src = OLD_BADGE.sub("", src)

    number = start

    def badge(match: re.Match) -> str:
        nonlocal number
        span = f'<span class="framenummer" title="Frame {number}">#{number}</span>'
        number += 1
        return match.group(0) + span

    src = ARTICLE.sub(badge, src)
    last = number - 1

    def chip(match: re.Match) -> str:
        block = OLD_RANGE.sub("", match.group(0))
        span = f'<span class="framereeks">frames #{start}–#{last}</span>'
        return block.replace("</div>", span + "</div>")

    src, replaced = SUM.subn(chip, src, count=1)
    if not replaced:
        sys.exit(f"{path.name}: no header .sum block")

    if not dry:
        path.write_text(src, encoding="utf-8")
    return path.name, start, last


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    number = 1
    for band in BANDS:
        name, first, last = number_page(PAGES / f"{band}.html", number, args.dry_run)
        print(f"{name:16} #{first}–#{last}  ({last - first + 1} frames)")
        number = last + 1


if __name__ == "__main__":
    main()
