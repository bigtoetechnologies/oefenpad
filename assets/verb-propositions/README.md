# Source art — Voorzetselpaden

The full-size PNGs as they come back from the image generator. This is source
material, not shipped art; the game never reads this folder.

## Folders

| Folder | What | Use |
|---|---|---|
| `referenceimages/style-a/` | The three style A references: `zorgen-om-persoon.png`, `krijgen-van-vriend.png`, `trots-op-kind.png` | Active. Attach these to every Voorzetselpaden generation, with `Docs/voorzetselpaden/base-prompt.txt`. Never ship them. |
| `referenceimages/style-a/origin/` | The three early hand-drawn scenes style A grew from | Provenance only; do not attach |
| `referenceimages/` (top level) | The three brush anchors `wachten-op-*.png` | Retired for Voorzetselpaden on 12 Nov 2026; still the brush reference for other games |
| `archived/00-pilot-1-3/` | The 30 pilot scenes, batches 1–3 | Provenance only; do not use |
| `archived/04-a0-a2/` | Batch 4, 20 scenes | Provenance only; do not use |
| `archived/04b-a2-pairs/` | Batch 4b, 14 of 16 scenes — drawn, not in the game | Kept for its plan and status; redraw before integration |
| `archived/incoming/` | The 48 variants returned for batch 4b, including the 16 new-style variants referenced in the data decision | Provenance only; do not use as style references |
| `archived/_dropped/` | Three rejected scenes (`kiezen-tussen-deuren.png`, `kiezen-voor-plank.png`, `zorgen-om-telefoon.png`) | Provenance only; see its own README |

Everything from the first three generations now lives under `archived/`. The old
drawings are kept for provenance, not as references: do not attach them to a
generation, trace them or treat them as the target style. The only reference
images are the three in `referenceimages/style-a/`.

## New batches

New output goes in its own batch folder at the top level of this directory,
named `<batch>-<band>/`, and is never mixed into `archived/`. The prefixes follow
curriculum order:

| Batches | Band | Folders |
|---|---|---|
| 5–8 | A2+ | `05-a2-plus/` … `08-a2-plus/` |
| 9–13 | B1 | `09-b1/` … `13-b1/` |
| 14–23 | B1+ | `14-b1-plus/` … `23-b1-plus/` |
| 24–32 | B2 | `24-b2/` … `32-b2/` |

`04b` is the exception: it belongs to A2 but sits between batch 4 and batch 5,
so it keeps the `04b-a2-pairs/` name. Redraw batches R1–R10 are named for the
plan in `Docs/archive/prepositions-art-redraw-prompts.md`.

## Pipeline, in order

1. Drop the new PNGs into the folder for their batch. Do not mix batches.
2. Review them on the sheet: `python3 tools/build-prepositions-preview.py`.
   That renders everything in `prepositions.json` **plus** the frames of every
   batch listed in the tool's `PENDING_PLANS`, straight from its folder. Add a
   batch to that list only once its PNGs have arrived; a row without a file
   stops the build.
3. Promote a batch only when the reviewer signs off:
   - white paper to alpha, cobalt `#2B50C8` only, 2:3, 512 × 763,
     written to `assets/voorzetselpaden/<scene-id>.png`;
   - scene + frame records added to
     `server/Oefenpad.Resources/Games/Data/prepositions.json`;
   - status in the batch plan flipped to `drawn`.
4. Rebuild the game-accurate sheet: `python3 tools/build-prepositions-sheet.py`.

Steps 2 and 4 write the same output file, so the last one you run wins. Run the
preview while reviewing new art, and the stock builder after a promotion.

## Conventions

- Filename = scene id: `<verb>-<preposition>-<situation>.png`, lowercase ASCII,
  hyphens only, no diacritics (`geinteresseerd`, not `geïnteresseerd`).
- Delivered redraws carry a `-v2` suffix until integration, so the old file
  survives the comparison.
- 784 × 1168 or 1152 × 1712; both are 2:3, so neither needs cropping.
- RGB, no alpha, white paper. Alpha is made at promotion time, not on drop.
- One idea per image, cobalt only. Cobalt ink in the delivered files sits around
  hue 217–221°; any file far outside that, or with grey, is a redraw.
