/* =================================================================
   confetti.ts — the celebration burst.

   Each game keeps its own palette and timing; the DOM work lives
   here. The pieces are plain divs animated by .confetti-piece, which
   each game's scoped sheet already defines.
   ================================================================= */

export interface ConfettiOptions {
  colors?: string[];
  count?: number;
  /** Seconds per piece animation, as [min, max]: it is written to animationDuration. */
  duration?: [number, number];
  /** Seconds before a piece starts, as [min, max]. */
  delay?: [number, number];
  /** Top offset range in px. */
  top?: [number, number];
  width?: [number, number];
  height?: [number, number];
  /** Defaults to true: empty the container first. */
  clear?: boolean;
  /** Remove each piece after this many milliseconds. */
  removeAfter?: number;
}

function randomBetween(range: [number, number] | undefined): number {
  const [min, max] = range ?? [0, 1];
  return min + Math.random() * (max - min);
}

export function spawnConfetti(
  container: HTMLElement | null,
  options: ConfettiOptions = {},
): void {
  if (!container) return;

  const colors = options.colors
    ?? ['#E8601F', '#2B50C8', '#15307F', '#7E9BE0', '#C44A12'];
  const count = options.count ?? 80;

  if (options.clear !== false) container.innerHTML = '';

  for (let i = 0; i < count; i++) {
    const piece = document.createElement('div');
    piece.className = 'confetti-piece';
    piece.style.left = `${Math.random() * 100}%`;
    piece.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    piece.style.animationDuration = `${randomBetween(options.duration).toFixed(2)}s`;
    piece.style.animationDelay = `${randomBetween(options.delay).toFixed(2)}s`;

    if (options.top) piece.style.top = `${randomBetween(options.top).toFixed(1)}px`;
    if (options.width) piece.style.width = `${randomBetween(options.width).toFixed(1)}px`;
    if (options.height) piece.style.height = `${randomBetween(options.height).toFixed(1)}px`;

    container.appendChild(piece);

    if (options.removeAfter) {
      const lifetime = options.removeAfter;
      window.setTimeout(() => piece.remove(), lifetime);
    }
  }
}
