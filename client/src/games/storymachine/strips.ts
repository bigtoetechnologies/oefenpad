/* Pure helpers behind the story machine's spin. The server decides what
   every reel lands on; this only describes the movement on screen. */

/** ms for the first free reel to settle. */
export const SPIN_BASE = 900;

/** each later free reel settles this much after the previous one. */
export const SPIN_STAGGER = 260;

/** Pictures in a spinning strip. The last one is the tile that lands. */
export const STRIP_LENGTH = 14;

export type StripDirection = 'up' | 'down';

/**
 * Walks the strip past the window and back again, the way a real drum
 * turns over. `strip` is the list of pictures the reel shows, top to
 * bottom; the holder moves the strip by the height of its rows, so this
 * returns a number of rows only and never a pixel count.
 *
 *   up:   rows 0 -> (length - 1)   the strip's last row sits in the window
 *   down: rows 0 -> -(length - 1)  the strip's first row sits in the window
 *
 * Out of range counts return the last row, the resting position.
 */
export function settleRow(count: number, direction: StripDirection): number {
  if (count < 1) return 0;
  return direction === 'up' ? count - 1 : -(count - 1);
}

/**
 * The free reels settle one after another, so the last of them is on
 * screen for the shortest time. Stagger them across all free reels and
 * keep the last duration inside the old game's first-reel length.
 */
export function spinDuration(order: number, free: number): number {
  if (free <= 1) return SPIN_BASE;
  const step = Math.min(SPIN_STAGGER, (SPIN_BASE - 360) / (free - 1));
  return Math.round(SPIN_BASE - order * step);
}
