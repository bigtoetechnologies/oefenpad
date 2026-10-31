# Story Machine — design and art spec

A slot machine that deals a sentence. The player picks 2 to 6 reels,
pulls the handle, and reads the result aloud. Built at
`src/storymachine/`, standalone: four files, no framework, no build step.

## Why a machine and not dice

Reels are positional and dice are not. Reel 1 is always WHO, reel 2 is
always DOES WHAT, so every pull lands as a sentence skeleton instead of
a handful of loose nouns. That single property is what turns a toy into
a language exercise, and it is why the reel order in `reels.js` is part
of the design rather than a list.

| Reel | Slot | Added at |
|------|------|----------|
| 1 | Who | 2 reels |
| 2 | Does what | 2 reels |
| 3 | Where | 3 reels |
| 4 | With what | 4 reels |
| 5 | But then | 5 reels |
| 6 | And in the end (wildcard) | 6 reels |

Reel 6 draws an ending most of the time and anything at all the rest,
so the last beat can still surprise. It never repeats a tile already on
screen.

## The machine never writes the story

There is no sentence on screen. The pictures are the prompt, and
spelling the result out does the player's job for them. The only
on-screen text is a screen-reader-only announcement listing the tiles.

## The word cards

Under each reel sits a face-down card. Turning it over shows that
tile's word in the chosen language, so vocabulary is something the
player asks for rather than something the machine hands them. A pull
turns every card back over.

The back is the BigToe Games mascot card, taken from
`bigtoegames/scratchassets/playingcards/card_square_{light,dark}.jpg`
and scaled to 420px square at `art/cardback_{light,dark}.jpg`. There is
no landscape back in that repo, so the cards are square — the existing
backs are either square (1408px) or portrait (240x336, Solitaire).
Replace the two files to rebrand; nothing else refers to them.

Reels 4 to 6 carry a `join` (`met`, `maar dan`, `en uiteindelijk`) for
a read-aloud or print view later. Nothing renders it today.

## The art

72 tiles, 12 per reel. The full list, with ids and both languages, is
`src/storymachine/reels.js`; that file is the spec a generator should
read. Today each tile's `art` is an emoji placeholder. Replacing it
with a path is the only change the game needs.

| Rule | Why |
|------|-----|
| No text baked into the image, ever | One art set serves every language. Words are drawn in HTML, per locale |
| One idea per tile, readable as a silhouette at 64px | A phone reel tile is about that size |
| Vague beats specific — "a door", not "a red door with a letterbox" | The player supplies the story. Detail does it for them |
| Flat and bold, not photographic | Reels are read while moving |
| No culture-specific symbols | The audience is not Dutch |

Proposed layout: `src/storymachine/art/<reel-id>/<tile-id>.svg`, so
`art/who/fox.svg`. Tile ids are stable; treat them as filenames.

## What is not built

- No scoring, no timer, no progress. It is a prompt, not a test.
- No audio.
- No print view. A classroom wants one — six tiles in a row on A4.
- No sentence display, by design.
- No Quick Wins card back. The BigToe mascot is a placeholder.
- Real art. Everything above runs on emoji.
