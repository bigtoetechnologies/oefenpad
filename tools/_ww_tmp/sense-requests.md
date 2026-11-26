# Sense requests (26 Nov 2026) — not yet applied

Held back because the drawing thread owns selection.json, scenes/*.tsv and the band pages.
Apply with select.py / scenes/a2-regular.tsv, then rerun build-verb-cards.py,
import-verb-game.py, and add examples.tsv rows for the new slugs.

| slug | verb | sense | gloss | scene brief |
|---|---|---|---|---|
| missen (exists, drawn) | missen | bus | to miss (a bus) | keep as drawn |
| missen-doel | missen | doel | to miss (a target) | adult just released an arrow/ball; it passes beside a clearly marked target, which is untouched |
| missen-persoon | missen | persoon | to miss (someone) | adult alone at a table by a window, looking at a framed photo of another person, with an empty second chair |
| starten (rewrite brief) | starten | — | to start (a race) | adult crouched in sprint starting position on starting blocks, hands on the line, head down, track ahead |

Notes
- starten currently reads "to start (an engine)" with a car-interior brief and has no drawing.
  Replace it with the race brief above; opstarten stays the engine/computer verb.
- Same-verb cards never share a level (importer already enforces this).
