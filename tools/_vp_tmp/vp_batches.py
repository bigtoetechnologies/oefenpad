#!/usr/bin/env python3
"""Drive Grok through the missing Voorzetselpaden drawings, batch by batch.

A batch is a hand-picked group of chunks that belong together (kijken door +
kijken uit, denken aan + denken om + denken van, and so on). The ids still to
be drawn are read from the band page each time, so anything that already
carries an image is skipped and a rerun after a partial run is safe.

    python3 tools/_vp_tmp/vp_batches.py list
    python3 tools/_vp_tmp/vp_batches.py next [--count N] [--timeout S]

Each batch writes into tools/_vp_tmp/batches/<label>/: the prompt, the zip and
the unzipped PNGs. Nothing is applied to a page here; that is
apply-vp-batch.py, after the drawings have been looked at.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GROK = ROOT / "tools/grok/grok.py"
PAGES = ROOT / "Docs/voorzetselpaden"
OUT = Path(__file__).resolve().parent / "batches"
BASE = PAGES / "base-prompt.txt"

# label, band page, chunks. Order matters: the first incomplete batch is next.
BATCHES = [
    ("a1-kijken", "a1", ["kijken door", "kijken uit"]),
    ("a1-doorgeven-geven", "a1", ["doorgeven aan", "geven aan"]),
    ("a1-werken", "a1", ["werken aan", "werken bij"]),
    ("a1-vragen-wachten", "a1", ["vragen aan", "wachten tot"]),
    ("a1-praten-uitnodigen", "a1", ["praten met", "uitnodigen voor"]),
    ("a1-vallen-zwaaien", "a1", ["vallen uit", "zwaaien naar"]),
    ("a2-denken", "a2", ["denken aan", "denken om", "denken van"]),
    ("a2-nadenken", "a2", ["nadenken over"]),
    ("a2-dromen-sterven-ruiken", "a2",
     ["dromen van", "dromen over", "sterven aan", "sterven van",
      "ruiken naar", "ruiken aan"]),
    ("a2-smaken-zeggen-praten-gaan", "a2",
     ["smaken naar", "zeggen tegen", "zeggen van", "praten tegen", "gaan over"]),
    ("a2-beschermen-oppassen-klagen", "a2",
     ["beschermen tegen", "oppassen met", "klagen bij"]),
    ("a2-door-komen-gaan-om", "a2", ["dat komt door", "komen door", "gaan om"]),
    ("a2-kopen-bellen-laten-zien", "a2",
     ["kopen bij", "verkopen aan", "aanbellen bij", "laten zien aan", "geven om"]),
    ("a2-tevreden-wachten-bellen", "a2",
     ["tevreden zijn met", "gelukkig zijn met", "vinden van", "wachten met",
      "antwoorden op", "telefoneren naar"]),
    ("a2-doen-halen-rijden", "a2",
     ["doen aan", "halen uit", "rennen naar", "rijden naar", "uitkijken voor"]),
    ("a2pairs-missing", "a2-pairs",
     ["betalen voor", "beginnen met", "kiezen voor", "kijken naar", "krijgen van"]),
]

# Cards that already show a drawing but have no source PNG in incoming/.
# They are redrawn from the prompt so the file can be promoted again.
REDRAW = [
    ("a2-redraw-praten-tegen-de-hond", "a2", ["praten-tegen-de-hond"]),
]


# Extra instruction appended to a batch's prompt, for a redraw after a reject.
NOTES = {
    "a1-kijken": (
        "CORRECTION FOR kijken-door-kier. Earlier attempts drew the fence as a wall "
        "of solid cobalt boards, which fills the picture and loses the white space. "
        "Draw the fence as WHITE boards with clean cobalt outlines, not as filled "
        "shapes: the only cobalt is the outlines and the person. Use five or six "
        "tall upright boards, spaced so that one narrow gap between two of them is "
        "clearly visible, with the person an adult with adult proportions, whole "
        "figure from head to feet, one eye close to that gap and the other eye shut, "
        "both hands flat on the boards at shoulder height, heels lifted slightly. "
        "The fence is taller than the person and runs across the picture, but the "
        "boards themselves must stay white."),
    "a1-doorgeven-geven": (
        "CORRECTION FOR doorgeven-aan-medespeler. Earlier the baton floated in the "
        "air between the two runners, touched by neither hand. The handover must be "
        "physical: the front runner reaches BACK with one arm, bent at the elbow, "
        "hand open at hip height behind him, and the rear runner presses the baton "
        "into that open hand so the baton is inside the front runner's fingers and "
        "the rear hand is still touching it. Both runners mid-stride facing right, "
        "the third runner further back bent over with hands on knees. No floating "
        "object: the baton must touch both hands."),
    "a1-werken": (
        "CORRECTION FOR werken-bij-winkel. Earlier the row of shopping trolleys read "
        "as flat open trays. Draw six COUNTABLE nested shopping trolleys: each one a "
        "shallow open wire basket, clearly a separate basket with its own visible "
        "wheel at the bottom, the row stepping forward so each basket is offset from "
        "the one behind it, and straight horizontal handle bars that the pushing "
        "figure grips with both hands. Use a bolder line weight for the trolley "
        "frames so they stay readable at thumbnail size. Keep the apron, the shop "
        "doors and the crates; drop tiny detail dots."),
}


def records():
    with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
        subprocess.run([sys.executable, "-I", str(ROOT / "tools/prepositions-pages.py"),
                        "read", "--out", tmp.name], check=True, capture_output=True)
        return json.load(open(tmp.name, encoding="utf-8"))


def drawn_ids(page: str) -> set[str]:
    text = (PAGES / page).read_text(encoding="utf-8")
    have = set()
    for m in re.finditer(r'(?s)<article class="[^"]*kaart[^"]*"([^>]*)>(.*?)</article>',
                         text):
        if 'class="beeld"' in m.group(2):
            have.add(re.search(r'data-id="([^"]+)"', m.group(1)).group(1))
    return have


def outstanding(band_page: str, chunks: list[str], recs: list[dict]) -> list[dict]:
    page = band_page if band_page.endswith(".html") else band_page + ".html"
    have = drawn_ids(page)
    cards = [r for r in recs
             if r["page"] == page and r.get("chunk") in chunks
             and r["id"] not in have]
    order = {c: i for i, c in enumerate(chunks)}
    return sorted(cards, key=lambda r: order[r["chunk"]])


def sentence(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    value = value[0].upper() + value[1:]
    return value if value[-1] in ".!?" else value + "."


def prompt_for(page: str, cards: list[dict], recs: list[dict], label: str) -> str:
    page = page if page.endswith(".html") else page + ".html"
    note = NOTES.get(label)
    glosses = {r["chunk"]: r.get("gloss") or "" for r in recs if r["page"] == page}
    scenes = []
    for r in cards:
        gloss = glosses.get(r["chunk"], "")
        lines = [f"{r['id']}.png — {r['chunk']}" + (f" ({gloss})" if gloss else ""),
                 "Scene: " + sentence(r["scene"])]
        if r.get("must"):
            lines.append("Must read: " + r["must"])
        if r.get("avoid"):
            lines.append("Avoid: " + r["avoid"])
        scenes.append("\n".join(lines))
    base = BASE.read_text(encoding="utf-8").rstrip()
    files = ", ".join(r["id"] + ".png" for r in cards)
    return (base + "\n\nTHE SCENES\n" + "\n\n".join(scenes)
            + ("\n\n" + note if note else "")
            + f"\n\nDELIVERY\nReturn one zip named oefenpad-{label}.zip containing "
              f"exactly these files and nothing else:\n{files}\nAttach the zip to your reply.\n")


def run(*args: str) -> str:
    proc = subprocess.run([sys.executable, str(GROK), *args],
                          capture_output=True, text=True)
    if proc.returncode:
        raise SystemExit(f"grok.py {' '.join(args)} failed:\n{proc.stderr.strip()}")
    return proc.stdout.strip()


def run_batch(label: str, page: str, cards: list[dict], recs: list[dict],
              timeout: int) -> bool:
    folder = OUT / label
    attempt = 1
    while (folder / f"attempt{attempt}").exists():
        attempt += 1
    folder = folder / f"attempt{attempt}"
    folder.mkdir(parents=True)
    (folder / "prompt.txt").write_text(prompt_for(page, cards, recs, label),
                                       encoding="utf-8")
    zipname = f"oefenpad-{label}.zip"
    print(f"batch {label} (attempt{attempt}): {len(cards)} scenes", flush=True)
    for card in cards:
        print("   ", card["id"], flush=True)

    run("new")
    run("compose", str(folder / "prompt.txt"))
    print("chat:", run("send"), flush=True)
    run("wait", zipname, "--timeout", str(timeout))
    run("download", zipname, str(folder))

    archive = folder / zipname
    if not archive.is_file():
        print("  !! zip did not arrive", flush=True)
        return False
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(folder)
    missing = [c["id"] for c in cards if not (folder / f"{c['id']}.png").is_file()]
    if missing:
        print("  !! missing from zip:", ", ".join(missing), flush=True)
        return False
    print("  ready:", len(cards), "png", flush=True)
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["list", "next"])
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=1200)
    ap.add_argument("--force", action="store_true",
                    help="also run batches whose cards all have a drawing")
    ap.add_argument("--batch", help="run only this batch label")
    ap.add_argument("--ids", nargs="+", help="redraw only these scene ids")
    args = ap.parse_args()

    recs = records()
    plan = BATCHES + REDRAW
    if args.batch:
        plan = [b for b in plan if b[0] == args.batch]
        if not plan:
            sys.exit(f"no batch called {args.batch}")
    if args.ids:
        wanted = set(args.ids)

    if args.action == "list":
        for label, page, chunks in plan:
            if page == "a2" and label.startswith("a2-redraw"):
                cards = [r for r in recs if r["id"] in chunks]
            else:
                cards = outstanding(page, chunks, recs)
            state = "done" if not cards else f"{len(cards)} to draw"
            print(f"{label:34s} {page:9s} {state}")
        return

    ran = 0
    for label, page, chunks in plan:
        if ran >= args.count:
            break
        if page == "a2" and label.startswith("a2-redraw"):
            cards = [r for r in recs if r["id"] in chunks]
        else:
            cards = outstanding(page, chunks, recs)
        if args.ids:
            cards = [c for c in cards if c["id"] in wanted]
        if not cards:
            continue
        if not run_batch(label, page, cards, recs, args.timeout):
            sys.exit(f"batch {label} did not complete")
        ran += 1
        recs = records()  # re-read in case something was applied meanwhile
    if not ran:
        print("nothing left to draw")


if __name__ == "__main__":
    main()
