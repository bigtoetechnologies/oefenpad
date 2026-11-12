/* =================================================================
   gallows.ts — the hangman drawing, carried over line for line from
   the old src/galgje/script.js so the strokes land in the same
   places on the 280 × 260 canvas.
   ================================================================= */

export const CANVAS_WIDTH = 280;
export const CANVAS_HEIGHT = 260;

/** Strokes only, like --inkt in light mode; near-white in dark. */
const LIGHT = '#455A64';
const DARK = '#E0E0E0';

export function drawGallows(canvas: HTMLCanvasElement, wrong: number, dark: boolean): void {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const colour = dark ? DARK : LIGHT;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = colour;
  ctx.fillStyle = colour;
  ctx.lineWidth = 4;
  ctx.lineCap = 'round';

  // Ground, always visible.
  ctx.beginPath();
  ctx.moveTo(30, 240);
  ctx.lineTo(120, 240);
  ctx.stroke();

  if (wrong >= 1) {
    ctx.beginPath();
    ctx.moveTo(60, 240);
    ctx.lineTo(60, 40);
    ctx.stroke();
  }
  if (wrong >= 2) {
    ctx.beginPath();
    ctx.moveTo(60, 40);
    ctx.lineTo(185, 40);
    ctx.stroke();
  }
  if (wrong >= 3) {
    ctx.beginPath();
    ctx.moveTo(185, 40);
    ctx.lineTo(185, 75);
    ctx.stroke();
  }
  if (wrong >= 4) {
    ctx.beginPath();
    ctx.arc(185, 97, 22, 0, Math.PI * 2);
    ctx.stroke();
  }
  if (wrong >= 5) {
    ctx.beginPath();
    ctx.moveTo(185, 119);
    ctx.lineTo(185, 185);
    ctx.stroke();
  }
  if (wrong >= 6) {
    ctx.beginPath();
    ctx.moveTo(185, 135);
    ctx.lineTo(150, 165);
    ctx.stroke();
  }
  if (wrong >= 7) {
    ctx.beginPath();
    ctx.moveTo(185, 135);
    ctx.lineTo(220, 165);
    ctx.stroke();
  }
  if (wrong >= 8) {
    ctx.beginPath();
    ctx.moveTo(185, 185);
    ctx.lineTo(160, 222);
    ctx.stroke();
  }
  if (wrong >= 9) {
    ctx.beginPath();
    ctx.moveTo(185, 185);
    ctx.lineTo(210, 222);
    ctx.stroke();
  }
  if (wrong >= 10) {
    // X eyes: the man is done for.
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(172, 88);
    ctx.lineTo(182, 98);
    ctx.moveTo(182, 88);
    ctx.lineTo(172, 98);
    ctx.moveTo(188, 88);
    ctx.lineTo(198, 98);
    ctx.moveTo(198, 88);
    ctx.lineTo(188, 98);
    ctx.stroke();
  }
}
