# Galgje, ported to React

`HangmanGame.tsx` is the React port of the old `src/galgje/` page, against the
server-authoritative API (`/api/games/hangman`). `gallows.ts` holds the canvas
drawing, carried over stroke for stroke.

The class names and DOM nesting are the contract with
`client/src/styles/games/hangman.css`; the sheet is unchanged by this port.

## What the server decides

The word, the picture clue and the answer never reach the browser while a round
is playing. The view carries the pattern (`gap` / `text` / `revealed`), the
guessed letters, the wrong count and, once the round is over, the answer.

That has one consequence worth knowing: the view does **not** say which guessed
letters were in the word, so the keyboard's green `correct` / red `wrong` marks
cannot be derived from `guessed` alone. The component remembers the letters the
server judged correct for the current round (`positiveLetters`, keyed by round
id) and colours from that.

`positiveLetters` is **still required** after the port; it is not a leftover
workaround. Removing it makes every guessed letter colour the same.

## Round changes

Difficulty, category and translation each need a new round. If a guess has been
made (`guessed.length > 0` and the round is still playing), the change first
opens the confirmation overlay, as the old page did. Turning translation *off*
does not need a new round.

## What was deliberately dropped

- The `uk` alphabet and keyboard rows, and the language switch. The game is
  Dutch-only.
- The old save/restore key `oefenpad-galgje-save`. A round lives on the server;
  there is no client-side state to restore.
- Ukrainian in the translation list. The service only answers in English, so the
  settings offer `Uit` and `English` only.

Settings and stats keep the old keys, `oefenpad-galgje-settings` and
`oefenpad-galgje-stats`, with the same shape.
