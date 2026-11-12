#!/usr/bin/env python3
"""Clear review flags that no longer describe their card.

The November 2026 review left a verdict strip on many cards. The scenes
have since been rewritten, so a finding may now object to something that is
no longer there. This applies a decision file:

    {"decisions": [{"id": ..., "action": "clear"|"keep"|"fix", "why": ...}]}

`clear` removes the verdict strip and the severity marker. `keep` leaves the
card alone. `fix` is handed to prepositions-pages.py, which writes the
corrected fields; the flag is cleared afterwards, since the fault is gone.

    python3 tools/prepositions-flags.py decisions.json [--dry-run]
"""
import argparse
import html as H
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "Docs/voorzetselpaden"
HELD = {"a0.html"}          # the art session's uncommitted work lives here

CARD = re.compile(r'<article class="kaart[^"]*"[^>]*data-id="(?P<id>[^"]+)"[^>]*>'
                  r'(?P<body>.*?)</article>', re.S)
FIELDS = ("chunk", "gloss", "voorbeeld-nl", "bouw", "controlevraag",
          "pronominaal", "scene", "must", "avoid", "note")


def clear_card(whole):
    """Strip the verdict strip and its markers from one card."""
    out = re.sub(r'<div class="oordeel (?:wrong-dutch|weak-picture|minor)"[^>]*>.*?</div>',
                 "", whole, flags=re.S)
    out = re.sub(r'\s*data-severity="(?:wrong-dutch|weak-picture|minor)"', "", out, count=1)
    out = re.sub(r'<article class="kaart sev-(?:wrong-dutch|weak-picture|minor)"',
                 '<article class="kaart"', out, count=1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    decisions = json.loads(Path(a.file).read_text(encoding="utf-8"))["decisions"]
    by_id = {d["id"]: d for d in decisions}
    tally = Counter(d["action"] for d in decisions)

    # Dutch corrections first, through the page tool, so one writer owns the markup
    def as_fix(d):
        """Accept the fields at the top level or nested under `fields`."""
        src = dict(d.get("fields") or {})
        src.update({k: v for k, v in d.items() if k in FIELDS})
        out = {"id": d["id"]}
        for k, v in src.items():
            if k in FIELDS:
                out[k] = v
        # a separate English line belongs with its Dutch one
        nl, en = src.get("voorbeeld-nl"), src.get("voorbeeld-en")
        if nl is not None and not isinstance(nl, dict):
            out["voorbeeld-nl"] = {"nl": nl, "en": en or ""}
        elif en and isinstance(out.get("voorbeeld-nl"), dict):
            out["voorbeeld-nl"]["en"] = en
        return out

    fixes = [as_fix(d) for d in decisions if d.get("action") == "fix"]
    if fixes and not a.dry_run:
        tmp = Path(a.file).with_suffix(".fixes.json")
        tmp.write_text(json.dumps({"fixes": fixes}, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, "-I",
                            str(ROOT / "tools/prepositions-pages.py"), "patch", str(tmp)],
                           capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
        if r.returncode:
            sys.exit("the fix pass failed; nothing was cleared")

    # a cleared flag means the fault is gone, and a fixed one has just been mended
    clear_ids = {d["id"] for d in decisions if d.get("action") in ("clear", "fix")}
    touched, held, seen = Counter(), [], set()

    for page in sorted(PAGES.glob("*.html")):
        if page.name == "index.html":
            continue
        src = page.read_text(encoding="utf-8")

        def repl(m):
            cid = m.group("id")
            if cid not in by_id:
                return m.group(0)
            seen.add(cid)
            if page.name in HELD:
                held.append(cid)
                return m.group(0)
            if cid not in clear_ids:
                return m.group(0)
            out = clear_card(m.group(0))
            if out != m.group(0):
                touched[page.name] += 1
            return out

        out = CARD.sub(repl, src)
        if out == src:
            continue
        if len(re.findall(r'<article class="kaart', out)) != out.count("</article>"):
            print(f"  {page.name}: markup would be unbalanced, skipped")
            continue
        if not a.dry_run:
            page.write_text(out, encoding="utf-8")

    print(f"\ndecisions: {dict(tally)}")
    for name, n in sorted(touched.items()):
        print(f"  {name:16s} cleared {n}")
    missing = set(by_id) - seen
    if missing:
        print(f"  not found on any page: {len(missing)} {sorted(missing)[:5]}")
    if held:
        print(f"  held back on {', '.join(sorted(HELD))}: {len(held)}")


if __name__ == "__main__":
    main()
