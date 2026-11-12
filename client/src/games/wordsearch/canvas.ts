/* =================================================================
   canvas.ts — the selection canvas.

   Ported from the old script's drawAllFoundRects() and
   drawSelectionLine(). The canvas sits over .grid-wrapper at the
   same offset as the .grid (4 px inside the wrapper's padding), so
   cell coordinates measured from the grid are already canvas
   coordinates. It is scaled by devicePixelRatio and sized in CSS
   pixels, which the old page did not do: it set the canvas' own
   width/height and would have run out of grid on a HiDPI screen.
   ================================================================= */

import type { Cell } from './model';

export const SELECTION_COLOR = 'rgba(255, 179, 0, 0.85)';
export const FOUND_COLOR = '#2E7D32';

/** Lays the canvas over the grid at its real pixel size. */
export function sizeCanvas(canvas: HTMLCanvasElement, wrapper: HTMLElement): void {
  const ratio = window.devicePixelRatio || 1;
  const width = wrapper.clientWidth;
  const height = wrapper.clientHeight;

  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  canvas.width = Math.round(width * ratio);
  canvas.height = Math.round(height * ratio);
}

function context(canvas: HTMLCanvasElement): CanvasRenderingContext2D | null {
  const ctx = canvas.getContext('2d');
  if (!ctx) return null;
  const ratio = window.devicePixelRatio || 1;
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  return ctx;
}

function rectOf(el: Element, origin: DOMRect): DOMRect {
  const box = el.getBoundingClientRect();
  return new DOMRect(
    box.left - origin.left,
    box.top - origin.top,
    box.width,
    box.height,
  );
}

function roundedRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  radius: number,
): void {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + w - radius, y);
  ctx.arcTo(x + w, y, x + w, y + radius, radius);
  ctx.lineTo(x + w, y + h - radius);
  ctx.arcTo(x + w, y + h, x + w - radius, y + h, radius);
  ctx.lineTo(x + radius, y + h);
  ctx.arcTo(x, y + h, x, y + h - radius, radius);
  ctx.lineTo(x, y + radius);
  ctx.arcTo(x, y, x + radius, y, radius);
  ctx.closePath();
}

/** One rounded outline per found word, hugging diagonals too. */
function drawFoundLine(
  ctx: CanvasRenderingContext2D,
  cells: Element[],
  origin: DOMRect,
  cellWidth: number,
  cellHeight: number,
): void {
  const first = cells[0];
  const last = cells[cells.length - 1];
  if (!first || !last) return;

  const pad = Math.min(cellWidth, cellHeight) * 0.1;
  const radius = Math.min(cellWidth, cellHeight) * 0.28;
  const a = rectOf(first, origin);
  const b = rectOf(last, origin);

  const diagonal = a.left !== b.left && a.top !== b.top;
  if (diagonal) {
    const cx1 = a.left + a.width / 2;
    const cy1 = a.top + a.height / 2;
    const cx2 = b.left + b.width / 2;
    const cy2 = b.top + b.height / 2;
    const dx = cx2 - cx1;
    const dy = cy2 - cy1;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const angle = Math.atan2(dy, dx);
    const cellDim = Math.min(cellWidth, cellHeight);
    const width = dist + cellDim - pad * 2;
    const height = cellDim - pad * 2;

    ctx.save();
    ctx.translate((cx1 + cx2) / 2, (cy1 + cy2) / 2);
    ctx.rotate(angle);
    roundedRect(ctx, -width / 2, -height / 2, width, height, radius);
    ctx.stroke();
    ctx.restore();
    return;
  }

  const left = Math.min(a.left, b.left);
  const top = Math.min(a.top, b.top);
  const right = Math.max(a.left + a.width, b.left + b.width);
  const bottom = Math.max(a.top + a.height, b.top + b.height);

  roundedRect(ctx, left + pad, top + pad, right - left - pad * 2, bottom - top - pad * 2, radius);
  ctx.stroke();
}

interface PaintOptions {
  /** The grid's cells, row-major. */
  cells: Element[];
  size: number;
  /** Found words as endpoint pairs; each is one line on the canvas. */
  found: Array<[Cell, Cell]>;
  /** The live drag line, in client coordinates. */
  drag: { start: Cell; clientX: number; clientY: number } | null;
}

/** Repaints the whole canvas: found outlines first, then the drag line. */
export function paintCanvas(
  canvas: HTMLCanvasElement | null,
  grid: HTMLElement | null,
  options: PaintOptions,
): void {
  if (!canvas || !grid) return;
  const ctx = context(canvas);
  if (!ctx) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const origin = grid.getBoundingClientRect();
  const first = options.cells[0];
  if (!first) return;

  const firstRect = first.getBoundingClientRect();
  const cellWidth = firstRect.width;
  const cellHeight = firstRect.height;

  ctx.strokeStyle = FOUND_COLOR;
  ctx.lineWidth = 3;
  ctx.lineJoin = 'round';

  for (const [from, to] of options.found) {
    const line: Element[] = [];
    const dr = Math.sign(to.r - from.r);
    const dc = Math.sign(to.c - from.c);
    let r = from.r;
    let c = from.c;
    while (r >= 0 && r < options.size && c >= 0 && c < options.size) {
      const el = options.cells[r * options.size + c];
      if (el) line.push(el);
      if (r === to.r && c === to.c) break;
      r += dr;
      c += dc;
    }
    drawFoundLine(ctx, line, origin, cellWidth, cellHeight);
  }

  if (!options.drag) return;

  const cellSize = origin.width / options.size;
  const sx = options.drag.start.c * cellSize + cellSize / 2;
  const sy = options.drag.start.r * cellSize + cellSize / 2;
  const ex = options.drag.clientX - origin.left;
  const ey = options.drag.clientY - origin.top;

  ctx.strokeStyle = SELECTION_COLOR;
  ctx.lineWidth = 2.5;
  ctx.setLineDash([6, 4]);
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(sx, sy);
  ctx.lineTo(ex, ey);
  ctx.stroke();
  ctx.setLineDash([]);

  ctx.fillStyle = SELECTION_COLOR;
  ctx.beginPath();
  ctx.arc(sx, sy, 3, 0, Math.PI * 2);
  ctx.fill();
}
