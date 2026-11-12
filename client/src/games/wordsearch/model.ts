/* =================================================================
   model.ts — the shapes the word search keeps.

   The server owns the puzzle: the grid, the hidden placements and
   whether a selection was right. Everything here is either what the
   view hands us or what the player's own actions have shown us so
   far — the cells of a word they have already found or been hinted.
   ================================================================= */

export interface CategoryView {
  id: string;
  name: string;
  icon: string;
}

export interface WordEntry {
  index: number;
  text: string;
  translation: string | null;
  imageUrl: string | null;
}

export interface WordSearchView {
  difficulty: string;
  category: CategoryView;
  size: number;
  grid: string[][];
  words: WordEntry[];
  found: boolean[];
  hintsLeft: number;
  done: boolean;
}

export interface HintCell {
  r: number;
  c: number;
}

/**
 * The payload the server puts in the `view` slot of a move result. The two
 * actions answer different shapes: a found selection sends
 * `{ view, foundIndex }`, a wrong selection sends the bare view, and a hint
 * sends `{ view, hint }`. Both are read through here so nothing downstream
 * has to know which action produced it.
 */
export interface MovePayload {
  view: WordSearchView;
  foundIndex?: number | null;
  hint?: {
    index: number;
    cells: HintCell[];
  };
}

/** The view out of a move payload, whichever shape it arrived in. */
export function viewOf(payload: MovePayload | WordSearchView | null | undefined): WordSearchView {
  const candidate = payload as MovePayload & Partial<WordSearchView>;
  if (candidate && typeof candidate === 'object' && candidate.view) return candidate.view;
  return payload as WordSearchView;
}

/** The index of the word a selection found, or -1 when it was wrong. */
export function foundIndexOf(payload: MovePayload | null | undefined): number {
  const index = payload?.foundIndex;
  return typeof index === 'number' && index >= 0 ? index : -1;
}

export interface Cell {
  r: number;
  c: number;
}

/** The cells of every word the browser has seen a placement for. */
export type PlacementMap = Record<number, Cell[]>;

/**
 * The extra a resumed word search carries: the outlines of the words the
 * player had already found. The placements still hidden never travel.
 */
export interface WordSearchResume {
  placements: PlacementMap;
}

export interface WordSearchSettings {
  soundEffects: boolean;
  difficulty: string;
  category: string;
  /** Language code fed to `translateTo`; '' is off. Ukrainian is not offered. */
  translateTo: string;
}

export interface WordSearchStats {
  wins: number;
  streak: number;
  bestStreak: number;
}

/* The old page's storage keys, so settings and stats survive the move. */
export const SETTINGS_KEY = 'oefenpad-woordzoeker-settings';
export const STATS_KEY = 'oefenpad-woordzoeker-stats';

export const DEFAULT_DIFFICULTY = 'beginner';
export const DEFAULT_CATEGORY = 'animals';

/** A hint lights a whole word; the old page held it for a little over 5 s. */
export const HINT_MS = 5500;
/** Three wrong-flashes of .35 s plus a breath, as the old .cell.error rule. */
export const ERROR_MS = 1100;

/** Translation targets the API knows about. Ukrainian is deliberately absent. */
export const TRANSLATE_LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'nl', name: 'Nederlands' },
];

export function isStraightLine(start: Cell, end: Cell): boolean {
  const dr = end.r - start.r;
  const dc = end.c - start.c;
  return (dr === 0 && dc !== 0)
    || (dc === 0 && dr !== 0)
    || (Math.abs(dr) === Math.abs(dc) && dr !== 0);
}

/** Every cell from `start` to `end`, both included, when they form a line. */
export function cellsInLine(start: Cell, end: Cell, size: number): Cell[] {
  if (!isStraightLine(start, end)) return [];

  const dr = Math.sign(end.r - start.r);
  const dc = Math.sign(end.c - start.c);
  const cells: Cell[] = [];
  let r = start.r;
  let c = start.c;

  for (;;) {
    if (r < 0 || r >= size || c < 0 || c >= size) break;
    cells.push({ r, c });
    if (r === end.r && c === end.c) break;
    r += dr;
    c += dc;
  }

  return cells;
}

/** Cells covered by a straight run, derived from the two endpoints selected. */
export function placementFrom(
  r1: number,
  c1: number,
  r2: number,
  c2: number,
  size: number,
): Cell[] {
  return cellsInLine({ r: r1, c: c1 }, { r: r2, c: c2 }, size);
}

export function cellKey(r: number, c: number): string {
  return `${r},${c}`;
}

/** A cell belongs to a found word once its index is in the placement map. */
export function foundCells(
  placements: PlacementMap,
  found: boolean[],
): Set<string> {
  const cells = new Set<string>();
  for (const [index, line] of Object.entries(placements)) {
    if (!found[Number(index)]) continue;
    for (const cell of line) cells.add(cellKey(cell.r, cell.c));
  }
  return cells;
}

/** The cell size the old page chose for this grid and window width. */
export function cellSizeFor(size: number, windowWidth: number): number {
  const maxWidth = Math.min(windowWidth - 200, 500);
  return Math.max(16, Math.min(36, Math.floor(maxWidth / size)));
}

export function fontSizeFor(cellSize: number): number {
  if (cellSize > 28) return 15;
  if (cellSize > 22) return 13;
  if (cellSize > 18) return 11;
  return 9;
}
